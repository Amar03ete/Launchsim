<template>
  <div class="main-view">
    <!-- Header -->
    <header class="app-header">
      <div class="header-left">
        <div class="brand" @click="router.push('/')">LAUNCHSIM</div>
      </div>
      
      <div class="header-center">
        <div class="view-switcher">
          <button 
            v-for="mode in ['graph', 'split', 'workbench']" 
            :key="mode"
            class="switch-btn"
            :class="{ active: viewMode === mode }"
            @click="viewMode = mode"
          >
            {{ { graph: 'Graph', split: 'Split', workbench: 'Workbench' }[mode] }}
          </button>
        </div>
      </div>

      <div class="header-right">
        <div class="workflow-step">
          <span class="step-num">Step {{ currentStep }}/5</span>
          <span class="step-name">{{ stepNames[currentStep - 1] }}</span>
        </div>
        <div class="step-divider"></div>
        <span class="status-indicator" :class="statusClass">
          <span class="dot"></span>
          {{ statusText }}
        </span>
      </div>
    </header>

    <!-- Main Content Area -->
    <main class="content-area">
      <!-- Left Panel: Graph (only shown in Steps 1-2) -->
      <div 
        v-if="currentStep <= 2"
        class="panel-wrapper left" 
        :style="leftPanelStyle"
      >
        <GraphPanel 
          :graphData="graphData"
          :loading="graphLoading"
          :currentPhase="currentPhase"
          @refresh="refreshGraph"
          @toggle-maximize="toggleMaximize('graph')"
        />
      </div>

      <!-- Right Panel: Step Components -->
      <div 
        class="panel-wrapper right" 
        :style="currentStep <= 2 ? rightPanelStyle : { width: '100%', opacity: 1, transform: 'translateX(0)' }"
      >
        <!-- Step 1: Graph Build -->
        <Step1GraphBuild 
          v-if="currentStep === 1"
          :currentPhase="currentPhase"
          :projectData="projectData"
          :ontologyProgress="ontologyProgress"
          :buildProgress="buildProgress"
          :graphData="graphData"
          :systemLogs="systemLogs"
          @next-step="handleNextStep"
        />

        <!-- Step 2: Env Setup -->
        <Step2EnvSetup
          v-else-if="currentStep === 2"
          :simulationId="simulationId"
          :projectData="projectData"
          :graphData="graphData"
          :systemLogs="systemLogs"
          @go-back="handleGoBack"
          @next-step="handleNextStep"
          @add-log="addLog"
        />

        <!-- Step 3: Simulation -->
        <Step3Simulation
          v-else-if="currentStep === 3"
          :simulationId="simulationId"
          :maxRounds="maxRounds"
          :projectData="projectData"
          :graphData="graphData"
          :systemLogs="systemLogs"
          @go-back="handleGoBack"
          @next-step="handleNextStep"
          @add-log="addLog"
          @update-status="handleStatusUpdate"
        />

        <!-- Step 4: Report -->
        <Step4Report
          v-else-if="currentStep === 4"
          :reportId="reportId"
          :simulationId="simulationId"
          :systemLogs="systemLogs"
          @go-back="handleGoBack"
          @add-log="addLog"
          @update-status="handleStatusUpdate"
        />

        <!-- Step 5: Interaction -->
        <Step5Interaction
          v-else-if="currentStep === 5"
          :reportId="reportId"
          :simulationId="simulationId"
          @go-back="handleGoBack"
          @add-log="addLog"
          @update-status="handleStatusUpdate"
        />
      </div>
    </main>

    <!-- System Logs (shown in steps 1-2) -->
    <div v-if="currentStep <= 2 && systemLogs.length > 0" class="global-logs">
      <div class="log-header">
        <span class="log-title">SYS LOG</span>
        <span class="log-count">{{ systemLogs.length }}</span>
      </div>
      <div class="log-content" ref="logContainer">
        <div class="log-line" v-for="(log, idx) in systemLogs.slice(-20)" :key="idx">
          <span class="log-time">{{ log.time }}</span>
          <span class="log-msg">{{ log.msg }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GraphPanel from '../components/GraphPanel.vue'
import Step1GraphBuild from '../components/Step1GraphBuild.vue'
import Step2EnvSetup from '../components/Step2EnvSetup.vue'
import Step3Simulation from '../components/Step3Simulation.vue'
import Step4Report from '../components/Step4Report.vue'
import Step5Interaction from '../components/Step5Interaction.vue'
import { generateOntology, getProject, buildGraph, getTaskStatus, getGraphData } from '../api/graph'
import { createSimulation } from '../api/simulation'
import { getPendingUpload, clearPendingUpload } from '../store/pendingUpload'

const route = useRoute()
const router = useRouter()

// Layout State
const viewMode = ref('split') // graph | split | workbench

// Step State
const currentStep = ref(1) // 1-5
const stepNames = ['Graph Build', 'Env Setup', 'Simulation', 'Report', 'Interaction']

// Data State
const currentProjectId = ref(route.params.projectId)
const loading = ref(false)
const graphLoading = ref(false)
const error = ref('')
const projectData = ref(null)
const graphData = ref(null)
const currentPhase = ref(-1) // -1: Upload, 0: Ontology, 1: Build, 2: Complete
const ontologyProgress = ref(null)
const buildProgress = ref(null)
const systemLogs = ref([])

// Simulation & Report IDs
const simulationId = ref(null)
const reportId = ref(null)
const maxRounds = ref(null)

// Polling timers
let pollTimer = null
let graphPollTimer = null

// Log scroll ref
const logContainer = ref(null)

// --- Computed Layout Styles ---
const leftPanelStyle = computed(() => {
  if (viewMode.value === 'graph') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'workbench') return { width: '0%', opacity: 0, transform: 'translateX(-20px)', pointerEvents: 'none' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

const rightPanelStyle = computed(() => {
  if (viewMode.value === 'workbench') return { width: '100%', opacity: 1, transform: 'translateX(0)' }
  if (viewMode.value === 'graph') return { width: '0%', opacity: 0, transform: 'translateX(20px)', pointerEvents: 'none' }
  return { width: '50%', opacity: 1, transform: 'translateX(0)' }
})

// --- Status Computed ---
const statusClass = computed(() => {
  if (error.value) return 'error'
  if (currentStep.value === 5) return 'completed'
  if (currentStep.value >= 3) return 'processing'
  if (currentPhase.value >= 2) return 'completed'
  return 'processing'
})

const statusText = computed(() => {
  if (error.value) return 'Error'
  const texts = ['Building Graph', 'Env Setup', 'Simulating', 'Generating Report', 'Interacting']
  return texts[currentStep.value - 1] || 'Initializing'
})

// --- Helpers ---
const addLog = (msg) => {
  const now = new Date()
  const time = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }) + '.' + String(now.getMilliseconds()).padStart(3, '0')
  systemLogs.value.push({ time, msg })
  if (systemLogs.value.length > 200) systemLogs.value.shift()
  nextTick(() => {
    if (logContainer.value) logContainer.value.scrollTop = logContainer.value.scrollHeight
  })
}

// --- Layout Methods ---
const toggleMaximize = (target) => {
  viewMode.value = viewMode.value === target ? 'split' : target
}

const handleStatusUpdate = (status) => {
  addLog(`Status update: ${status}`)
}

const handleNextStep = async (params = {}) => {
  if (currentStep.value < 5) {
    // When moving from Step 1 → Step 2, create simulation instance
    if (currentStep.value === 1) {
      await createSimulationInstance()
    }

    // Capture maxRounds from Step2
    if (currentStep.value === 2 && params.maxRounds) {
      maxRounds.value = params.maxRounds
    }

    // Capture reportId from Step3 next-step event
    if (currentStep.value === 3 && params.reportId) {
      reportId.value = params.reportId
    }

    currentStep.value++
    addLog(`→ Entering Step ${currentStep.value}: ${stepNames[currentStep.value - 1]}`)
  }
}

const handleGoBack = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    addLog(`← Back to Step ${currentStep.value}: ${stepNames[currentStep.value - 1]}`)
  }
}

// Create simulation instance when entering Step 2
const createSimulationInstance = async () => {
  if (!currentProjectId.value || simulationId.value) return
  try {
    addLog('Creating simulation instance...')
    const res = await createSimulation({ project_id: currentProjectId.value })
    if (res.success && res.data) {
      simulationId.value = res.data.simulation_id
      addLog(`✓ Simulation instance created: ${simulationId.value}`)
    } else {
      addLog(`✗ Failed to create simulation: ${res.error || 'Unknown error'}`)
    }
  } catch (err) {
    addLog(`✗ Error creating simulation: ${err.message}`)
  }
}

// --- Data Logic ---
const initProject = async () => {
  addLog('Initializing LaunchSim project view...')
  if (currentProjectId.value === 'new') {
    await handleNewProject()
  } else {
    await loadProject()
  }
}

const handleNewProject = async () => {
  const pending = getPendingUpload()
  if (!pending.isPending || pending.files.length === 0) {
    error.value = 'No pending files found. Please return to home and try again.'
    addLog('Error: No pending files found for new project.')
    return
  }
  
  try {
    loading.value = true
    currentPhase.value = 0
    ontologyProgress.value = { message: 'Uploading and analyzing documents...' }
    addLog('Starting ontology generation...')
    
    const formData = new FormData()
    pending.files.forEach(f => formData.append('files', f))
    formData.append('simulation_requirement', pending.simulationRequirement)
    
    const res = await generateOntology(formData)
    if (res.success) {
      clearPendingUpload()
      currentProjectId.value = res.data.project_id
      projectData.value = res.data
      router.replace({ name: 'Process', params: { projectId: res.data.project_id } })
      ontologyProgress.value = null
      addLog(`✓ Ontology generated. Project ID: ${res.data.project_id}`)
      await startBuildGraph()
    } else {
      error.value = res.error || 'Ontology generation failed'
      addLog(`✗ Error: ${error.value}`)
    }
  } catch (err) {
    error.value = err.message
    addLog(`✗ Exception: ${err.message}`)
  } finally {
    loading.value = false
  }
}

const loadProject = async () => {
  try {
    loading.value = true
    addLog(`Loading existing project: ${currentProjectId.value}`)
    const res = await getProject(currentProjectId.value)
    if (res.success) {
      projectData.value = res.data
      updatePhaseByStatus(res.data.status)
      addLog(`Project loaded. Status: ${res.data.status}`)
      
      if (res.data.status === 'ontology_generated' && !res.data.graph_id) {
        await startBuildGraph()
      } else if (res.data.status === 'graph_building' && res.data.graph_build_task_id) {
        currentPhase.value = 1
        startPollingTask(res.data.graph_build_task_id)
        startGraphPolling()
      } else if (res.data.status === 'graph_completed' && res.data.graph_id) {
        currentPhase.value = 2
        await loadGraph(res.data.graph_id)
      }
    } else {
      error.value = res.error
      addLog(`✗ Error loading project: ${res.error}`)
    }
  } catch (err) {
    error.value = err.message
    addLog(`✗ Exception: ${err.message}`)
  } finally {
    loading.value = false
  }
}

const updatePhaseByStatus = (status) => {
  switch (status) {
    case 'created':
    case 'ontology_generated': currentPhase.value = 0; break
    case 'graph_building': currentPhase.value = 1; break
    case 'graph_completed': currentPhase.value = 2; break
    case 'failed': error.value = 'Project failed'; break
  }
}

const startBuildGraph = async () => {
  try {
    currentPhase.value = 1
    buildProgress.value = { progress: 0, message: 'Starting build...' }
    addLog('Initiating graph build...')
    
    const res = await buildGraph({ project_id: currentProjectId.value })
    if (res.success) {
      addLog(`✓ Graph build task started. ID: ${res.data.task_id}`)
      startGraphPolling()
      startPollingTask(res.data.task_id)
    } else {
      error.value = res.error
      addLog(`✗ Error starting build: ${res.error}`)
    }
  } catch (err) {
    error.value = err.message
    addLog(`✗ Exception: ${err.message}`)
  }
}

const startGraphPolling = () => {
  fetchGraphData()
  graphPollTimer = setInterval(fetchGraphData, 10000)
}

const fetchGraphData = async () => {
  try {
    const projRes = await getProject(currentProjectId.value)
    if (projRes.success && projRes.data.graph_id) {
      const gRes = await getGraphData(projRes.data.graph_id)
      if (gRes.success) {
        graphData.value = gRes.data
      }
    }
  } catch (err) {
    // Silent - graph not ready yet
  }
}

const startPollingTask = (taskId) => {
  pollTaskStatus(taskId)
  pollTimer = setInterval(() => pollTaskStatus(taskId), 2000)
}

const pollTaskStatus = async (taskId) => {
  try {
    const res = await getTaskStatus(taskId)
    if (res.success) {
      const task = res.data
      if (task.message && task.message !== buildProgress.value?.message) {
        addLog(task.message)
      }
      buildProgress.value = { progress: task.progress || 0, message: task.message }
      
      if (task.status === 'completed') {
        addLog('✓ Graph build complete.')
        stopPolling()
        stopGraphPolling()
        currentPhase.value = 2
        const projRes = await getProject(currentProjectId.value)
        if (projRes.success && projRes.data.graph_id) {
          projectData.value = projRes.data
          await loadGraph(projRes.data.graph_id)
        }
      } else if (task.status === 'failed') {
        stopPolling()
        error.value = task.error
        addLog(`✗ Task failed: ${task.error}`)
      }
    }
  } catch (e) {
    console.error(e)
  }
}

const loadGraph = async (graphId) => {
  graphLoading.value = true
  addLog(`Loading graph data: ${graphId}`)
  try {
    const res = await getGraphData(graphId)
    if (res.success) {
      graphData.value = res.data
      const nodeCount = res.data.node_count || res.data.nodes?.length || 0
      addLog(`✓ Graph loaded. ${nodeCount} nodes.`)
    }
  } catch (e) {
    addLog(`✗ Graph load error: ${e.message}`)
  } finally {
    graphLoading.value = false
  }
}

const refreshGraph = () => {
  if (projectData.value?.graph_id) {
    loadGraph(projectData.value.graph_id)
  }
}

const stopPolling = () => {
  if (pollTimer) { clearInterval(pollTimer); pollTimer = null }
}

const stopGraphPolling = () => {
  if (graphPollTimer) { clearInterval(graphPollTimer); graphPollTimer = null }
}

onMounted(() => { initProject() })
onUnmounted(() => { stopPolling(); stopGraphPolling() })
</script>

<style scoped>
/* ===== BASE ===== */
.main-view {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #080810;
  overflow: hidden;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  color: #E0E0E0;
}

/* ===== HEADER ===== */
.app-header {
  height: 56px;
  border-bottom: 1px solid #1A1A2E;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #0A0A14;
  z-index: 100;
  position: relative;
  flex-shrink: 0;
}

.header-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.brand {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  font-size: 16px;
  letter-spacing: 2px;
  cursor: pointer;
  color: #fff;
  text-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
}

.brand:hover {
  color: #00F0FF;
}

/* View Switcher */
.view-switcher {
  display: flex;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid #1A1A2E;
  padding: 3px;
  gap: 3px;
}

.switch-btn {
  border: none;
  background: transparent;
  padding: 5px 14px;
  font-size: 11px;
  font-weight: 600;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.switch-btn.active {
  background: rgba(0, 240, 255, 0.1);
  color: #00F0FF;
  border: 1px solid rgba(0, 240, 255, 0.3);
}

/* Status Indicator */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.workflow-step {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #444;
  font-size: 11px;
}

.step-name {
  font-weight: 700;
  color: #E0E0E0;
}

.step-divider {
  width: 1px;
  height: 14px;
  background: #1A1A2E;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #555;
  font-weight: 500;
  font-family: 'JetBrains Mono', monospace;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #333;
  flex-shrink: 0;
}

.status-indicator.processing .dot { background: #00F0FF; box-shadow: 0 0 8px #00F0FF; animation: pulse 1.2s infinite; }
.status-indicator.processing { color: #00F0FF; }
.status-indicator.completed .dot { background: #00FF88; box-shadow: 0 0 8px #00FF88; }
.status-indicator.completed { color: #00FF88; }
.status-indicator.error .dot { background: #FF003C; box-shadow: 0 0 8px #FF003C; }
.status-indicator.error { color: #FF003C; }

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

/* ===== CONTENT AREA ===== */
.content-area {
  flex: 1;
  display: flex;
  position: relative;
  overflow: hidden;
  min-height: 0;
}

.panel-wrapper {
  height: 100%;
  overflow: hidden;
  transition: width 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), opacity 0.3s ease, transform 0.3s ease;
  will-change: width, opacity, transform;
}

.panel-wrapper.left {
  border-right: 1px solid #1A1A2E;
}

/* ===== GLOBAL LOGS ===== */
.global-logs {
  height: 120px;
  background: #060609;
  border-top: 1px solid #1A1A2E;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.log-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 16px;
  border-bottom: 1px solid #1A1A2E;
}

.log-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 700;
  color: #333;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.log-count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #333;
  background: rgba(255,255,255,0.04);
  padding: 1px 6px;
  border: 1px solid #1A1A2E;
}

.log-content {
  flex: 1;
  overflow-y: auto;
  padding: 6px 16px;
  scrollbar-width: thin;
  scrollbar-color: #1A1A2E transparent;
}

.log-line {
  display: flex;
  gap: 12px;
  padding: 1.5px 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  line-height: 1.5;
}

.log-time {
  color: #333;
  flex-shrink: 0;
  font-size: 10px;
}

.log-msg {
  color: #5A5A7A;
}

.log-msg:last-child {
  color: #8080A0;
}
</style>
