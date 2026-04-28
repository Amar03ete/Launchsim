<template>
  <div class="workbench-panel">
    <div class="scroll-container">
      <!-- Step 01: Ontology -->
      <div class="step-card" :class="{ 'active': currentPhase === 0, 'completed': currentPhase > 0 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">01</span>
            <span class="step-title">Ontology Generation</span>
          </div>
          <div class="step-status">
            <span v-if="currentPhase > 0" class="badge success">Completed</span>
            <span v-else-if="currentPhase === 0" class="badge processing">Generating</span>
            <span v-else class="badge pending">Waiting</span>
          </div>
        </div>
        
        <div class="card-content">
          <p class="api-note">POST /api/graph/ontology/generate</p>
          <p class="description">
            LLM analyzes document content and simulation requirements, extracts reality seeds, and automatically generates appropriate ontology structures
          </p>

          <!-- Loading / Progress -->
          <div v-if="currentPhase === 0 && ontologyProgress" class="progress-section">
            <div class="spinner-sm"></div>
            <span>{{ ontologyProgress.message || 'Analyzing documents...' }}</span>
          </div>

          <!-- Detail Overlay -->
          <div v-if="selectedOntologyItem" class="ontology-detail-overlay">
            <div class="detail-header">
               <div class="detail-title-group">
                  <span class="detail-type-badge">{{ selectedOntologyItem.itemType === 'entity' ? 'ENTITY' : 'RELATION' }}</span>
                  <span class="detail-name">{{ selectedOntologyItem.name }}</span>
               </div>
               <button class="close-btn" @click="selectedOntologyItem = null">×</button>
            </div>
            <div class="detail-body">
               <div class="detail-desc">{{ selectedOntologyItem.description }}</div>
               
               <!-- Attributes -->
               <div class="detail-section" v-if="selectedOntologyItem.attributes?.length">
                  <span class="section-label">ATTRIBUTES</span>
                  <div class="attr-list">
                     <div v-for="attr in selectedOntologyItem.attributes" :key="attr.name" class="attr-item">
                        <span class="attr-name">{{ attr.name }}</span>
                        <span class="attr-type">({{ attr.type }})</span>
                        <span class="attr-desc">{{ attr.description }}</span>
                     </div>
                  </div>
               </div>

               <!-- Examples (Entity) -->
               <div class="detail-section" v-if="selectedOntologyItem.examples?.length">
                  <span class="section-label">EXAMPLES</span>
                  <div class="example-list">
                     <span v-for="ex in selectedOntologyItem.examples" :key="ex" class="example-tag">{{ ex }}</span>
                  </div>
               </div>

               <!-- Source/Target (Relation) -->
               <div class="detail-section" v-if="selectedOntologyItem.source_targets?.length">
                  <span class="section-label">CONNECTIONS</span>
                  <div class="conn-list">
                     <div v-for="(conn, idx) in selectedOntologyItem.source_targets" :key="idx" class="conn-item">
                        <span class="conn-node">{{ conn.source }}</span>
                        <span class="conn-arrow">→</span>
                        <span class="conn-node">{{ conn.target }}</span>
                     </div>
                  </div>
               </div>
            </div>
          </div>

          <!-- Generated Entity Tags -->
          <div v-if="projectData?.ontology?.entity_types" class="tags-container" :class="{ 'dimmed': selectedOntologyItem }">
            <span class="tag-label">GENERATED ENTITY TYPES</span>
            <div class="tags-list">
              <span 
                v-for="entity in projectData.ontology.entity_types" 
                :key="entity.name" 
                class="entity-tag clickable"
                @click="selectOntologyItem(entity, 'entity')"
              >
                {{ entity.name }}
              </span>
            </div>
          </div>

          <!-- Generated Relation Tags -->
          <div v-if="projectData?.ontology?.edge_types" class="tags-container" :class="{ 'dimmed': selectedOntologyItem }">
            <span class="tag-label">GENERATED RELATION TYPES</span>
            <div class="tags-list">
              <span 
                v-for="rel in projectData.ontology.edge_types" 
                :key="rel.name" 
                class="entity-tag clickable"
                @click="selectOntologyItem(rel, 'relation')"
              >
                {{ rel.name }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 02: Graph Build -->
      <div class="step-card" :class="{ 'active': currentPhase === 1, 'completed': currentPhase > 1 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">02</span>
            <span class="step-title">GraphRAG Build</span>
          </div>
          <div class="step-status">
            <span v-if="currentPhase > 1" class="badge success">Completed</span>
            <span v-else-if="currentPhase === 1" class="badge processing">{{ buildProgress?.progress || 0 }}%</span>
            <span v-else class="badge pending">Waiting</span>
          </div>
        </div>

        <div class="card-content">
          <p class="api-note">POST /api/graph/build</p>
          <p class="description">
            Based on the generated ontology, automatically chunk documents and invoke Neo4j to build knowledge graphs, extract entities and relationships, and form temporal memory and community summaries
          </p>
          
          <!-- Stats Cards -->
          <div class="stats-grid">
            <div class="stat-card">
              <span class="stat-value">{{ graphStats.nodes }}</span>
              <span class="stat-label">Entity Nodes</span>
            </div>
            <div class="stat-card">
              <span class="stat-value">{{ graphStats.edges }}</span>
              <span class="stat-label">Relation Edges</span>
            </div>
            <div class="stat-card">
              <span class="stat-value">{{ graphStats.types }}</span>
              <span class="stat-label">SCHEMA Types</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 03: Complete -->
      <div class="step-card" :class="{ 'active': currentPhase === 2, 'completed': currentPhase >= 2 }">
        <div class="card-header">
          <div class="step-info">
            <span class="step-num">03</span>
            <span class="step-title">Build Complete</span>
          </div>
          <div class="step-status">
            <span v-if="currentPhase >= 2" class="badge accent">In Progress</span>
          </div>
        </div>
        
        <div class="card-content">
          <p class="api-note">POST /api/simulation/create</p>
          <p class="description">Graph build is complete. Please proceed to the next step to set up the simulation environment</p>
          <button 
            class="action-btn" 
            :disabled="currentPhase < 2"
            @click="handleEnterEnvSetup"
          >
            Enter Environment Setup ➝
          </button>
        </div>
      </div>
    </div>

    <!-- Bottom Info / Logs -->
    <div class="system-logs">
      <div class="log-header">
        <span class="log-title">SYSTEM DASHBOARD</span>
        <span class="log-id">{{ projectData?.project_id || 'NO_PROJECT' }}</span>
      </div>
      <div class="log-content" ref="logContent">
        <div class="log-line" v-for="(log, idx) in systemLogs" :key="idx">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-msg">{{ log.msg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, nextTick } from 'vue'

const props = defineProps({
  currentPhase: { type: Number, default: 0 },
  projectData: Object,
  ontologyProgress: Object,
  buildProgress: Object,
  graphData: Object,
  systemLogs: { type: Array, default: () => [] }
})

const emit = defineEmits(['next-step'])

const selectedOntologyItem = ref(null)
const logContent = ref(null)

// Enter environment setup — emit to parent (MainView handles simulation creation)
const handleEnterEnvSetup = () => {
  if (props.currentPhase < 2) return
  emit('next-step')
}

const selectOntologyItem = (item, type) => {
  selectedOntologyItem.value = { ...item, itemType: type }
}

const graphStats = computed(() => {
  const nodes = props.graphData?.node_count || props.graphData?.nodes?.length || 0
  const edges = props.graphData?.edge_count || props.graphData?.edges?.length || 0
  const types = props.projectData?.ontology?.entity_types?.length || 0
  return { nodes, edges, types }
})

const formatDate = (dateStr) => {
  if (!dateStr) return '--:--:--'
  const d = new Date(dateStr)
  return d.toLocaleTimeString('en-US', { hour12: false }) + '.' + d.getMilliseconds()
}

// Auto-scroll logs section
watch(() => props.systemLogs.length, () => {
  nextTick(() => {
    if (logContent.value) {
      logContent.value.scrollTop = logContent.value.scrollHeight
    }
  })
})
</script>

<style scoped>
.workbench-panel {
  height: 100%;
  background: #0A0A14;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  font-family: 'Space Grotesk', system-ui, sans-serif;
  color: #E0E0E0;
}

.scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scrollbar-width: thin;
  scrollbar-color: #1A1A2E transparent;
}

.step-card {
  background: rgba(255,255,255,0.03);
  padding: 20px;
  border: 1px solid #1A1A2E;
  transition: all 0.3s ease;
  position: relative;
}

.step-card.active {
  border-color: rgba(0, 240, 255, 0.35);
  background: rgba(0, 240, 255, 0.04);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.06);
}

.step-card.completed {
  border-color: rgba(0, 255, 136, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.step-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 18px;
  font-weight: 700;
  color: #2A2A3A;
}

.step-card.active .step-num { color: #00F0FF; }
.step-card.completed .step-num { color: #00FF88; }

.step-title {
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.5px;
  color: #E0E0E0;
}

.badge {
  font-size: 9px;
  padding: 3px 8px;
  font-weight: 700;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px;
}

.badge.success { background: rgba(0, 255, 136, 0.1); color: #00FF88; border: 1px solid rgba(0, 255, 136, 0.3); }
.badge.processing { background: rgba(0, 240, 255, 0.1); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.3); }
.badge.accent { background: rgba(0, 240, 255, 0.1); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.3); }
.badge.pending { background: rgba(255,255,255,0.04); color: #444; border: 1px solid #1A1A2E; }

.api-note {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #333;
  margin-bottom: 8px;
  letter-spacing: 0.5px;
}

.description {
  font-size: 12px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 16px;
}

/* Tags */
.tags-container {
  margin-top: 12px;
  transition: opacity 0.3s;
}

.tags-container.dimmed {
  opacity: 0.3;
  pointer-events: none;
}

.tag-label {
  display: block;
  font-size: 10px;
  color: #444;
  margin-bottom: 8px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.entity-tag {
  background: rgba(0,240,255,0.04);
  border: 1px solid rgba(0,240,255,0.2);
  padding: 4px 10px;
  font-size: 11px;
  color: #00F0FF;
  font-family: 'JetBrains Mono', monospace;
  transition: all 0.2s;
}

.entity-tag.clickable { cursor: pointer; }
.entity-tag.clickable:hover {
  background: rgba(0,240,255,0.12);
  border-color: rgba(0,240,255,0.5);
  text-shadow: 0 0 8px rgba(0,240,255,0.5);
}

/* Ontology Detail Overlay */
.ontology-detail-overlay {
  position: absolute;
  top: 60px;
  left: 20px;
  right: 20px;
  bottom: 20px;
  background: rgba(10, 10, 20, 0.98);
  backdrop-filter: blur(10px);
  z-index: 10;
  border: 1px solid rgba(0, 240, 255, 0.3);
  box-shadow: 0 0 30px rgba(0, 240, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #1A1A2E;
  background: rgba(0,0,0,0.3);
}

.detail-title-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-type-badge {
  font-size: 9px;
  font-weight: 700;
  color: #000;
  background: #00F0FF;
  padding: 2px 6px;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}

.detail-name {
  font-size: 13px;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
  color: #E0E0E0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #555;
  cursor: pointer;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover { color: #FF003C; }

.detail-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  scrollbar-width: thin;
  scrollbar-color: #1A1A2E transparent;
}

.detail-desc {
  font-size: 12px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #1A1A2E;
}

.detail-section { margin-bottom: 16px; }

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px;
}

.attr-list, .conn-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.attr-item {
  font-size: 11px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: baseline;
  padding: 6px;
  background: rgba(255,255,255,0.03);
  border: 1px solid #1A1A2E;
}

.attr-name {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 600;
  color: #00F0FF;
}

.attr-type { color: #444; font-size: 10px; }
.attr-desc { color: #666; flex: 1; min-width: 150px; }

.example-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.example-tag {
  font-size: 11px;
  background: rgba(255,255,255,0.04);
  border: 1px solid #1A1A2E;
  padding: 3px 8px;
  color: #888;
  font-family: 'JetBrains Mono', monospace;
}

.conn-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  padding: 6px;
  background: rgba(255,255,255,0.03);
  border: 1px solid #1A1A2E;
  font-family: 'JetBrains Mono', monospace;
}

.conn-node { font-weight: 600; color: #E0E0E0; }
.conn-arrow { color: #333; }

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  background: rgba(0,240,255,0.02);
  padding: 16px;
  border: 1px solid #1A1A2E;
}

.stat-card { text-align: center; }

.stat-value {
  display: block;
  font-size: 22px;
  font-weight: 700;
  color: #00F0FF;
  font-family: 'JetBrains Mono', monospace;
  text-shadow: 0 0 10px rgba(0,240,255,0.4);
}

.stat-label {
  font-size: 9px;
  color: #444;
  text-transform: uppercase;
  margin-top: 4px;
  display: block;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 1px;
}

/* Action Button */
.action-btn {
  width: 100%;
  background: linear-gradient(90deg, rgba(0,240,255,0.9) 0%, rgba(0,128,255,0.9) 100%);
  color: #000;
  border: none;
  padding: 16px;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.action-btn:hover:not(:disabled) {
  filter: brightness(1.15);
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.4);
}

.action-btn:disabled {
  background: rgba(255,255,255,0.06);
  color: #333;
  cursor: not-allowed;
}

.progress-section {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #00F0FF;
  margin-bottom: 12px;
  font-family: 'JetBrains Mono', monospace;
}

.spinner-sm {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(0,240,255,0.2);
  border-top-color: #00F0FF;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* System Logs */
.system-logs {
  background: #060609;
  padding: 12px 16px;
  font-family: 'JetBrains Mono', monospace;
  border-top: 1px solid #1A1A2E;
  flex-shrink: 0;
}

.log-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid #1A1A2E;
  padding-bottom: 6px;
  margin-bottom: 6px;
  font-size: 10px;
  color: #333;
  letter-spacing: 1px;
}

.log-content {
  display: flex;
  flex-direction: column;
  gap: 3px;
  max-height: 80px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #1A1A2E transparent;
}

.log-line {
  font-size: 11px;
  display: flex;
  gap: 12px;
  line-height: 1.5;
}

.log-time { color: #333; min-width: 75px; font-size: 10px; }
.log-msg { color: #5A5A7A; }
</style>
