import uuid
import json
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Callable
import math

from .graph_storage import GraphStorage
from .embedding_service import EmbeddingService
from .ner_extractor import NERExtractor

logger = logging.getLogger('mirofish.memory_storage')


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = sum(a * a for a in v1) ** 0.5
    norm_b = sum(b * b for b in v2) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class MemoryStorage(GraphStorage):
    """
    In-memory replacement for Neo4j.
    Stores all graphs, nodes, and edges in Python dictionaries.
    Bypasses AuraDB requirements and allows LaunchSim to run offline / 'Entirely on hardware'.
    """

    def __init__(self, embedding_service: Optional[EmbeddingService] = None, ner_extractor: Optional[NERExtractor] = None):
        self._embedding = embedding_service or EmbeddingService()
        self._ner = ner_extractor or NERExtractor()

        # State storage
        # graphs: dict of graph_id -> { "graph_id", "name", "description", "ontology_json", "created_at" }
        self._graphs: Dict[str, Dict[str, Any]] = {}
        # nodes: dict of graph_id -> list of node dicts
        self._nodes: Dict[str, List[Dict[str, Any]]] = {}
        # edges: dict of graph_id -> list of edge dicts
        self._edges: Dict[str, List[Dict[str, Any]]] = {}

    def create_graph(self, name: str, description: str = "") -> str:
        graph_id = str(uuid.uuid4())
        self._graphs[graph_id] = {
            "graph_id": graph_id,
            "name": name,
            "description": description,
            "ontology_json": "{}",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self._nodes[graph_id] = []
        self._edges[graph_id] = []
        logger.info(f"Created Memory graph '{name}' with id {graph_id}")
        return graph_id

    def delete_graph(self, graph_id: str) -> None:
        self._graphs.pop(graph_id, None)
        self._nodes.pop(graph_id, None)
        self._edges.pop(graph_id, None)
        logger.info(f"Deleted Memory graph {graph_id}")

    def set_ontology(self, graph_id: str, ontology: Dict[str, Any]) -> None:
        if graph_id in self._graphs:
            self._graphs[graph_id]["ontology_json"] = json.dumps(ontology, ensure_ascii=False)

    def get_ontology(self, graph_id: str) -> Dict[str, Any]:
        graph = self._graphs.get(graph_id)
        if graph and graph.get("ontology_json"):
            return json.loads(graph["ontology_json"])
        return {}

    def add_text(self, graph_id: str, text: str) -> str:
        episode_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        ontology = self.get_ontology(graph_id)

        # NER Extraction
        logger.info(f"[add_text] Memory Storage: Starting NER extraction for chunk ({len(text)} chars)...")
        extraction = self._ner.extract(text, ontology)
        entities = extraction.get("entities", [])
        relations = extraction.get("relations", [])

        # Embeddings
        entity_summaries = [f"{e['name']} ({e['type']})" for e in entities]
        fact_texts = [r.get("fact", f"{r['source']} {r['type']} {r['target']}") for r in relations]
        all_texts = entity_summaries + fact_texts

        all_embeddings = []
        if all_texts:
            try:
                all_embeddings = self._embedding.embed_batch(all_texts)
            except Exception as e:
                logger.warning(f"Batch embedding failed: {e}")
                all_embeddings = [[] for _ in all_texts]

        entity_embeddings = all_embeddings[:len(entities)]
        relation_embeddings = all_embeddings[len(entities):]

        # Merge Entities (Match by lowercase name)
        nodes_db = self._nodes.setdefault(graph_id, [])
        entity_uuid_map = {}

        for idx, ent in enumerate(entities):
            ename = ent["name"]
            etype = ent["type"]
            attrs = ent.get("attributes", {})
            summary = entity_summaries[idx]
            embedding = entity_embeddings[idx] if idx < len(entity_embeddings) else []
            e_lower = ename.lower()

            # Find existing
            existing_node = next((n for n in nodes_db if n["name"].lower() == e_lower), None)
            if existing_node:
                existing_node["summary"] = summary if not existing_node.get("summary") else existing_node["summary"]
                existing_node["attributes"].update(attrs)
                existing_node["embedding"] = embedding
                if etype and etype != "Entity" and etype not in existing_node["labels"]:
                    existing_node["labels"].append(etype)
                entity_uuid_map[e_lower] = existing_node["uuid"]
            else:
                new_uuid = str(uuid.uuid4())
                nodes_db.append({
                    "uuid": new_uuid,
                    "name": ename,
                    "labels": [etype] if etype and etype != "Entity" else [],
                    "summary": summary,
                    "attributes": attrs,
                    "embedding": embedding,
                    "created_at": now
                })
                entity_uuid_map[e_lower] = new_uuid

        # Create Relations
        edges_db = self._edges.setdefault(graph_id, [])
        for idx, rel in enumerate(relations):
            src_name = rel["source"].lower()
            tgt_name = rel["target"].lower()
            if src_name not in entity_uuid_map or tgt_name not in entity_uuid_map:
                continue
            
            src_uuid = entity_uuid_map[src_name]
            tgt_uuid = entity_uuid_map[tgt_name]

            edges_db.append({
                "uuid": str(uuid.uuid4()),
                "name": rel["type"],
                "fact": rel["fact"],
                "source_node_uuid": src_uuid,
                "target_node_uuid": tgt_uuid,
                "fact_embedding": relation_embeddings[idx] if idx < len(relation_embeddings) else [],
                "attributes": {},
                "episode_ids": [episode_id],
                "created_at": now,
                "valid_at": None,
                "invalid_at": None,
                "expired_at": None
            })

        logger.info(f"[add_text] Extracted {len(entities)} entities, {len(relations)} relations.")
        return episode_id

    def add_text_batch(self, graph_id: str, chunks: List[str], batch_size: int = 3, progress_callback: Optional[Callable] = None) -> List[str]:
        episode_ids = []
        total = len(chunks)
        for i, chunk in enumerate(chunks):
            if chunk and chunk.strip():
                episode_ids.append(self.add_text(graph_id, chunk))
            if progress_callback:
                progress_callback((i + 1) / total)
        return episode_ids

    def wait_for_processing(self, episode_ids: List[str], progress_callback: Optional[Callable] = None, timeout: int = 600) -> None:
        if progress_callback: progress_callback(1.0)

    # Readers
    def get_all_nodes(self, graph_id: str, limit: int = 2000) -> List[Dict[str, Any]]:
        nodes = self._nodes.get(graph_id, [])
        return sorted(nodes, key=lambda x: x["created_at"], reverse=True)[:limit]

    def get_node(self, uuid: str) -> Optional[Dict[str, Any]]:
        for g_nodes in self._nodes.values():
            for n in g_nodes:
                if n["uuid"] == uuid:
                    return n
        return None

    def get_node_edges(self, node_uuid: str) -> List[Dict[str, Any]]:
        edges = []
        for g_edges in self._edges.values():
            for e in g_edges:
                if e["source_node_uuid"] == node_uuid or e["target_node_uuid"] == node_uuid:
                    edges.append(e)
        return edges

    def get_nodes_by_label(self, graph_id: str, label: str) -> List[Dict[str, Any]]:
        return [n for n in self._nodes.get(graph_id, []) if label in n.get("labels", [])]

    def get_all_edges(self, graph_id: str) -> List[Dict[str, Any]]:
        edges = self._edges.get(graph_id, [])
        return sorted(edges, key=lambda x: x["created_at"], reverse=True)

    # Search
    def search(self, graph_id: str, query: str, limit: int = 10, scope: str = "edges"):
        result = {"edges": [], "nodes": [], "query": query}
        query_vector = []
        try:
            query_vector = self._embedding.embed(query)
        except Exception:
            pass

        query_lower = query.lower()

        if scope in ("edges", "both"):
            edges = self._edges.get(graph_id, [])
            scored_edges = []
            for e in edges:
                # Naive Keyword Score
                k_score = 1.0 if query_lower in e.get("fact", "").lower() or query_lower in e.get("name", "").lower() else 0.0
                # Vector Score
                v_score = cosine_similarity(query_vector, e.get("fact_embedding", [])) if query_vector else 0.0
                e_copy = dict(e)
                e_copy.pop("fact_embedding", None)
                e_copy["score"] = 0.7 * v_score + 0.3 * k_score
                if e_copy["score"] > 0:
                    scored_edges.append(e_copy)
            scored_edges.sort(key=lambda x: x["score"], reverse=True)
            result["edges"] = scored_edges[:limit]

        if scope in ("nodes", "both"):
            nodes = self._nodes.get(graph_id, [])
            scored_nodes = []
            for n in nodes:
                k_score = 1.0 if query_lower in n.get("name", "").lower() or query_lower in n.get("summary", "").lower() else 0.0
                v_score = cosine_similarity(query_vector, n.get("embedding", [])) if query_vector else 0.0
                n_copy = dict(n)
                n_copy.pop("embedding", None)
                n_copy["score"] = 0.7 * v_score + 0.3 * k_score
                if n_copy["score"] > 0:
                    scored_nodes.append(n_copy)
            scored_nodes.sort(key=lambda x: x["score"], reverse=True)
            result["nodes"] = scored_nodes[:limit]

        return result

    def get_graph_info(self, graph_id: str) -> Dict[str, Any]:
        nodes = self._nodes.get(graph_id, [])
        labels = set()
        for n in nodes:
            for l in n.get("labels", []):
                labels.add(l)
        
        return {
            "graph_id": graph_id,
            "node_count": len(nodes),
            "edge_count": len(self._edges.get(graph_id, [])),
            "entity_types": list(labels)
        }

    def get_graph_data(self, graph_id: str) -> Dict[str, Any]:
        nodes = self._nodes.get(graph_id, [])
        edges = self._edges.get(graph_id, [])

        node_map = {n["uuid"]: n["name"] for n in nodes}

        clean_nodes = []
        for n in nodes:
            nc = dict(n)
            nc.pop("embedding", None)
            clean_nodes.append(nc)

        clean_edges = []
        for e in edges:
            ec = dict(e)
            ec.pop("fact_embedding", None)
            ec["fact_type"] = ec["name"]
            ec["source_node_name"] = node_map.get(ec["source_node_uuid"], "")
            ec["target_node_name"] = node_map.get(ec["target_node_uuid"], "")
            ec["episodes"] = ec.get("episode_ids", [])
            clean_edges.append(ec)

        return {
            "graph_id": graph_id,
            "nodes": clean_nodes,
            "edges": clean_edges,
            "node_count": len(clean_nodes),
            "edge_count": len(clean_edges)
        }
