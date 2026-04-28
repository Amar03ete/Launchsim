<template>
  <div class="home-container">
    <!-- Top Navigation Bar -->
    <nav class="navbar">
      <div class="nav-brand">LAUNCHSIM</div>
      <div class="nav-links">
        <a href="https://github.com/Amar03ete/launchsim" target="_blank" class="github-link">
          Visit our Github <span>↗</span>
        </a>
      </div>
    </nav>

    <div class="main-content">
      <!-- Hero Sci-Fi Landing Page Section -->
      <section class="hero-section">
        <div class="hero-content">
          <div class="tag-row">
            <div class="scanning-dot"></div>
            <span class="orange-tag">SYS.LINK.ESTABLISHED</span>
            <span class="version-text">[OVERRIDE v0.2.0]</span>
          </div>

          <h1 class="main-title">
            <span class="glitch-text" data-text="SIMULATE THE MARKET">SIMULATE THE MARKET</span><br>
            <span class="gradient-text glitch-text" data-text="PREDICT THE FUTURE">PREDICT THE FUTURE</span>
          </h1>

          <div class="hero-desc">
            <p>
              From a single product pitch, <span class="highlight-bold">LaunchSim</span> extracts reality seeds and builds a parallel market of <span class="highlight-orange">autonomous AI agents</span> (investors, critics, early adopters). Inject variables, observe emergent behavior, and pinpoint exact <span class="highlight-code">"local optima"</span> for your launch strategy.
            </p>
            <p class="slogan-text">
              >_ LOCAL PREDICTION ENGINE ENGAGED <span class="blinking-cursor">█</span>
            </p>
          </div>

          <button class="hero-cta-btn" @click="scrollToBottom">
            <span style="opacity: 0.5; margin-right: 15px">>></span> INITIALIZE NEURAL LINK 
          </button>
        </div>
        
        <div class="hero-graphics">
          <img src="../assets/logo/launchsim_hud.png" alt="Neural HUD Interface" class="hero-logo" />
        </div>
      </section>

      <!-- Dashboard: Two-Column Layout -->
      <section class="dashboard-section">
        <div class="holo-overlay"></div>
        <!-- Left Column: Status & Steps -->
        <div class="left-panel">
          <div class="panel-header">
            <span class="status-dot">■</span> System Status
          </div>

          <h2 class="section-title">System Link Active</h2>
          <p class="section-desc">
            Neural simulation engine engaged. Inject variables to spin up an autonomous parallel market.
          </p>

          <div class="metrics-row">
            <div class="metric-card">
              <div class="metric-value">Neural</div>
              <div class="metric-label">Deep Graph Extraction Pipeline</div>
            </div>
            <div class="metric-card">
              <div class="metric-value">Agents</div>
              <div class="metric-label">Autonomous Market Behaviors</div>
            </div>
          </div>

          <div class="steps-container">
            <div class="steps-header">
              <span class="diamond-icon">◇</span> Workflow Sequence
            </div>
            <div class="workflow-list">
              <div v-for="(step, i) in steps" :key="i" class="workflow-item">
                <span class="step-num">{{ step.num }}</span>
                <div class="step-info">
                  <div class="step-title">{{ step.title }}</div>
                  <div class="step-desc">{{ step.desc }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Interactive Console -->
        <div class="right-panel">
          <div class="console-box">
            
            <div class="console-section">
              <div class="console-header">
                <span style="color: #00F0FF">>_ 01 / The Idea / Simulation Pitch</span>
                <span style="color: #444">Priority Input</span>
              </div>
              <div class="input-wrapper">
                <textarea 
                  v-model="formData.simulationRequirement" 
                  class="code-input" 
                  placeholder="// Describe your simulation or startup idea in detail...&#10;// Required if skipping file upload! Include: Target Audience, Value Prop, Market.&#10;// Example: 'A social network for dogs.' (Expand this!)" 
                  rows="8" 
                  :disabled="loading"
                ></textarea>
                <div class="model-badge">Engine: Neural Sub-Routines + Cloud Graph</div>
              </div>
              <div v-if="files.length === 0 && formData.simulationRequirement.length > 0 && formData.simulationRequirement.length < 50" style="color: #FF003C; font-size: 0.8rem; padding-top: 10px; font-family: 'JetBrains Mono', monospace;">
                ⚠️ Need minimum 50 characters to simulate raw ideas properly.
              </div>
            </div>

            <div class="console-divider">
              <span class="console-divider-text">Optional Injection</span>
            </div>

            <div class="console-section">
              <div class="console-header">
                <span style="color: #555">02 / Pitch Deck &amp; Research (Optional)</span>
                <span style="color: #333">Supported: PDF, MD, TXT</span>
              </div>
              <div style="display: flex; gap: 16px;">
                <div
                  class="upload-zone"
                  @dragover.prevent="handleDragOver"
                  @dragleave.prevent="handleDragLeave"
                  @drop.prevent="handleDrop"
                  @click="triggerFileInput"
                  style="flex: 1;"
                >
                  <input ref="fileInput" type="file" multiple accept=".pdf,.md,.txt" @change="handleFileSelect" style="display: none" :disabled="loading" />
                  <div v-if="files.length === 0" class="upload-placeholder">
                    <div class="upload-icon">↑</div>
                    <div class="upload-title">Drag pitch deck here</div>
                    <div class="upload-hint">or click to browse</div>
                  </div>
                  <div v-else class="file-list">
                    <div v-for="(file, index) in files" :key="index" class="file-item">
                      <span>📄</span>
                      <span class="file-name">{{ file.name }}</span>
                      <button @click.stop="removeFile(index)" class="remove-btn">×</button>
                    </div>
                  </div>
                </div>
                
                <div style="flex: 1; padding: 12px; font-size: 0.78rem; background: rgba(0, 240, 255, 0.03); border: 1px dashed rgba(0,240,255,0.15); color: #555; line-height: 1.7;">
                  <strong style="color: #00F0FF; display: block; margin-bottom: 8px;">Document Guide:</strong>
                  If uploading a pitch deck, include:<br/>
                  - <strong style="color: #888">Business Model:</strong> How does it make money?<br/>
                  - <strong style="color: #888">Target Audience:</strong> Who is it for?<br/>
                  - <strong style="color: #888">Value Prop:</strong> Why is it better?<br/>
                  <em style="color: #333">Supported: .pdf, .md, .txt</em>
                </div>
              </div>
            </div>

            <div class="btn-section">
              <button class="start-engine-btn" @click="startSimulation" :disabled="!canSubmit || loading">
                <span v-if="!loading">Initialize Simulation</span>
                <span v-else>Processing Local Market...</span>
                <span>↗</span>
              </button>
            </div>
          </div>
        </div>
      </section>

      <HistoryDatabase />
    </div>
  </div>
</template>

<script setup>
import './Home.css'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import HistoryDatabase from '../components/HistoryDatabase.vue'

const router = useRouter()

const steps = [
  { num: '01', title: 'Graph Build', desc: 'Extract reality seeds from your document, build knowledge graph with Neo4j + GraphRAG' },
  { num: '02', title: 'Env Setup', desc: 'Generate agent personas, configure simulation parameters via LLM' },
  { num: '03', title: 'Simulation', desc: 'Run multi-agent simulation with dynamic memory updates and emergent behavior' },
  { num: '04', title: 'Report', desc: 'ReportAgent analyzes the simulation results and generates a detailed prediction report' },
  { num: '05', title: 'Interaction', desc: 'Chat with any agent from the simulated world or discuss findings with ReportAgent' },
]

const formData = ref({ simulationRequirement: '' })
const files = ref([])
const loading = ref(false)
const isDragOver = ref(false)
const fileInput = ref(null)

const canSubmit = computed(() => {
  const req = formData.value.simulationRequirement.trim()
  if (files.value.length === 0) return req.length >= 50
  return req !== ''
})

const triggerFileInput = () => { if (!loading.value) fileInput.value?.click() }
const handleFileSelect = (event) => { addFiles(Array.from(event.target.files)) }
const handleDragOver = () => { isDragOver.value = true }
const handleDragLeave = () => { isDragOver.value = false }
const handleDrop = (e) => { isDragOver.value = false; addFiles(Array.from(e.dataTransfer.files)) }

const addFiles = (newFiles) => {
  const allowed = ['.pdf', '.md', '.txt']
  const valid = newFiles.filter(f => allowed.some(ext => f.name.toLowerCase().endsWith(ext)))
  files.value = [...files.value, ...valid]
}

const removeFile = (index) => { files.value.splice(index, 1) }

const scrollToBottom = () => { window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }) }

const startSimulation = () => {
  if (!canSubmit.value || loading.value) return
  
  let submitFiles = [...files.value]
  
  if (submitFiles.length === 0) {
    const mockBlob = new Blob([formData.value.simulationRequirement], { type: 'text/plain' })
    const mockFile = new File([mockBlob], 'User_Generated_Idea.txt', { type: 'text/plain' })
    submitFiles.push(mockFile)
  }

  import('../store/pendingUpload.js').then(({ setPendingUpload }) => {
    setPendingUpload(submitFiles, formData.value.simulationRequirement)
    router.push({ name: 'Process', params: { projectId: 'new' } })
  })
}
</script>

<style scoped>
/* Scanning dot animation */
.scanning-dot {
  width: 8px;
  height: 8px;
  background: #FF003C;
  border-radius: 50%;
  box-shadow: 0 0 10px #FF003C;
  animation: pulse 1s infinite;
  flex-shrink: 0;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 10px #FF003C; }
  50% { opacity: 0.7; transform: scale(0.85); box-shadow: 0 0 4px #FF003C; }
}

/* Hero CTA Button */
.hero-cta-btn {
  padding: 22px 50px;
  background: rgba(0, 240, 255, 0.05);
  border: 1px solid #00F0FF;
  color: #00F0FF;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px);
  box-shadow: inset 0 0 20px rgba(0, 240, 255, 0.1), 0 0 20px rgba(0, 240, 255, 0.05);
  text-transform: uppercase;
  letter-spacing: 4px;
  position: relative;
  overflow: hidden;
}

.hero-cta-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(0,240,255,0.1) 50%, transparent 100%);
  transform: translateX(-100%);
  transition: transform 0.6s;
}

.hero-cta-btn:hover::before {
  transform: translateX(100%);
}

.hero-cta-btn:hover {
  background: rgba(0, 240, 255, 0.12);
  box-shadow: inset 0 0 30px rgba(0, 240, 255, 0.2), 0 0 40px rgba(0, 240, 255, 0.15);
  text-shadow: 0 0 15px rgba(0, 240, 255, 0.8);
}
</style>
