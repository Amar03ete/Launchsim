

# LaunchSim

**Product Launch Predictor for Startups**

*A multi-agent swarm intelligence engine specialized for predicting market reactions before product launches. Entirely on your hardware.*

## What is LaunchSim?

LaunchSim is an advanced AI-driven prediction platform that enables startups to simulate real-world market reactions before launching a product. Built on multi-agent technology, it creates a dynamic digital environment where thousands of intelligent AI personas represent diverse segments of the ecosystem—such as early adopters, price-sensitive users, investors, and critics.

By uploading product details, pitch materials, or research inputs and describing goals in natural language, founders can initiate a simulation that mirrors how their product would be perceived in reality. Each AI agent is designed with distinct personality traits, memory, and behavioral logic, allowing them to generate authentic reactions, hold discussions, influence one another, and evolve opinions over time.

As these interactions unfold, LaunchSim captures complex social dynamics—such as trends, debates, and network effects—providing a realistic preview of how a product might perform in the market.

The platform then analyzes this simulated ecosystem to deliver:

- Deep sentiment insights across different user segments
- Identification of key concerns, objections, and risks
- Indicators of engagement and viral potential
- Actionable recommendations for product improvements and strategic pivots

A standout feature of LaunchSim is its "Before vs After" simulation capability, allowing users to test changes, compare outcomes, and instantly evaluate the impact of improvements without real-world consequences.

LaunchSim empowers founders to move beyond assumptions and intuition, replacing uncertainty with data-driven foresight. By rehearsing product launches in a controlled, intelligent simulation, it enables faster iteration, smarter decision-making, and significantly reduced risk—turning every "what if" into a measurable outcome.

## Workflow

1. **Graph Build** — Extracts entities (people, companies, events) and relationships from your document. Builds a knowledge graph with individual and group memory via Neo4j.
2. **Env Setup** — Generates hundreds of agent personas, each with unique personality, opinion bias, reaction speed, influence level, and memory of past events.
3. **Simulation** — Agents interact on simulated social platforms: posting, replying, arguing, shifting opinions. The system tracks sentiment evolution, topic propagation, and influence dynamics in real time.
4. **Report** — A ReportAgent analyzes the post-simulation environment, interviews a focus group of agents, searches the knowledge graph for evidence, and generates a structured analysis.
5. **Interaction** — Chat with any agent from the simulated world. Ask them why they posted what they posted. Full memory and personality persists.

## System Output & Insights

LaunchSim analyzes the simulated ecosystem to provide:

- **Sentiment Mapping** across user segments
- **Key Risks & Concerns** identified through agent discussions
- **Viral Potential Indicators** based on interaction patterns
- **Actionable Product Pivot Recommendations**

A powerful "Before vs After" simulation allows startups to test improvements and instantly compare outcomes, enabling rapid iteration without real-world risk.

## Screenshots


<p align="center">
  <img src="static/image/Screenshot/demo simple split view.png" width="400" alt="Split View">
  <img src="static/image/Screenshot/graph.png" width="400" alt="Knowledge Graph Intelligence">
</p>

<p align="center">
  <img src="static/image/Screenshot/simulation .png" width="400" alt="Market Simulation">
  <img src="static/image/Screenshot/report generation .png" width="400" alt="Report Analysis">
</p>

## Quick Start

### Prerequisites

- Docker & Docker Compose (recommended), **or**
- Python 3.11+, Node.js 18+, Neo4j 5.15+, Ollama

### Option A: Docker (easiest)

```bash
git clone https://github.com/yourorg/launchsim.git
cd launchsim
cp .env.example .env

# Start all services (Neo4j, Ollama, LaunchSim)
docker compose up -d

# Pull the required models into Ollama
docker exec launchsim-ollama ollama pull qwen2.5:32b
docker exec launchsim-ollama ollama pull nomic-embed-text
```

Open `http://localhost:3000` — that's it.

### Option B: Manual

**1. Start Neo4j**

```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/launchsim \
  neo4j:5.18-community
```

**2. Start Ollama & pull models**

```bash
ollama serve &
ollama pull qwen2.5:32b      # LLM (or qwen2.5:14b for less VRAM)
ollama pull nomic-embed-text  # Embeddings (768d)
```

**3. Configure & run backend**

```bash
cp .env.example .env
# Edit .env if your Neo4j/Ollama are on non-default ports

cd backend
pip install -r requirements.txt
python run.py
```

**4. Run frontend**

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Configuration

All settings are in `.env` (copy from `.env.example`):

```bash
# LLM — points to local Ollama (OpenAI-compatible API)
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:32b

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=launchsim

# Embeddings
EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_BASE_URL=http://localhost:11434
```

Works with any OpenAI-compatible API — swap Ollama for Claude, GPT, or any other provider by changing `LLM_BASE_URL` and `LLM_API_KEY`.

## Architecture

LaunchSim features a clean abstraction layer between the application and the graph database:

```
┌─────────────────────────────────────────┐
│              Flask API                   │
│  graph.py  simulation.py  report.py     │
└──────────────┬──────────────────────────┘
               │ app.extensions['neo4j_storage']
┌──────────────▼──────────────────────────┐
│           Service Layer                  │
│  EntityReader  GraphToolsService         │
│  GraphMemoryUpdater  ReportAgent         │
└──────────────┬──────────────────────────┘
               │ storage: GraphStorage
┌──────────────▼──────────────────────────┐
│         GraphStorage (abstract)          │
│              │                            │
│    ┌─────────▼─────────┐                │
│    │   Neo4jStorage     │                │
│    │  ┌───────────────┐ │                │
│    │  │ EmbeddingService│ ← Ollama       │
│    │  │ NERExtractor   │ ← Ollama LLM   │
│    │  │ SearchService  │ ← Hybrid search │
│    │  └───────────────┘ │                │
│    └───────────────────┘                │
└─────────────────────────────────────────┘
               │
        ┌──────▼──────┐
        │  Neo4j CE   │
        │  5.15       │
        └─────────────┘
```

**Key design decisions:**

- `GraphStorage` is an abstract interface — swap Neo4j for any other graph DB by implementing one class
- Dependency injection via Flask `app.extensions` — no global singletons
- Hybrid search: 0.7 × vector similarity + 0.3 × BM25 keyword search
- Synchronous NER/RE extraction via local LLM (replaces Zep's async episodes)
- All original dataclasses and LLM tools (InsightForge, Panorama, Agent Interviews) preserved

## Hardware Requirements

| Component | Minimum | Recommended |
|---|---|---|
| RAM | 16 GB | 32 GB |
| VRAM (GPU) | 10 GB (14b model) | 24 GB (32b model) |
| Disk | 20 GB | 50 GB |
| CPU | 4 cores | 8+ cores |

CPU-only mode works but is significantly slower for LLM inference. For lighter setups, use `qwen2.5:14b` or `qwen2.5:7b`.

## Use Cases

- **Product Launch Prediction** — Simulate market reactions to new startup products before launch
- **Investor Sentiment Analysis** — Test pitch decks against simulated investor personas
- **User Adoption Forecasting** — Predict how different user segments (early adopters, price-sensitive) will respond
- **Viral Dynamics Modeling** — Observe how network effects and social interactions amplify product visibility
- **Competitive Analysis** — Compare reactions to your product vs. competitors in the Indian startup ecosystem

## License

AGPL-3.0. See [LICENSE](./LICENSE).

## Credits & Attribution

LaunchSim is built using multi-agent simulation technology. The simulation engine is powered by [OASIS](https://github.com/camel-ai/oasis) from the CAMEL-AI team.

**Key technologies:**
- Local LLM inference via [Ollama](https://ollama.ai/)
- Graph database: [Neo4j Community Edition](https://neo4j.com/)
- Embeddings: nomic-embed-text via Ollama
- Frontend: Vue.js
- Backend: Python FastAPI
