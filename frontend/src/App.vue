<template>
  <router-view />
</template>

<script setup>
// Use Vue Router to manage pages
</script>

<style>
/* Global style reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'JetBrains Mono', 'Space Grotesk', 'Noto Sans SC', monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #FFFFFF;
  background-color: #0B0B0E;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #0B0B0E;
}

::-webkit-scrollbar-thumb {
  background: #00F0FF;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #00C0CC;
}

button {
  font-family: inherit;
}

/* ========== HOME PAGE STYLES ========== */

.home-container {
  min-height: 100vh;
  background-color: #0B0B0E;
  background-image: 
    linear-gradient(rgba(0, 240, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  font-family: 'Space Grotesk', 'Noto Sans SC', system-ui, sans-serif;
  color: #FFFFFF;
}

.navbar {
  height: 60px;
  background: #050508;
  color: #FFFFFF;
  border-bottom: 1px solid #1A1A24;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.nav-brand {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  letter-spacing: 1px;
  font-size: 1.2rem;
}

.nav-links {
  display: flex;
  align-items: center;
}

.github-link {
  color: #FFFFFF;
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s;
}

.github-link:hover {
  opacity: 0.8;
}

.arrow {
  font-family: sans-serif;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

.hero-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 80px;
  position: relative;
}

.hero-left {
  flex: 1;
  padding-right: 60px;
}

.tag-row {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
}

.orange-tag {
  background: #FF4500;
  color: #FFFFFF;
  padding: 4px 10px;
  font-weight: 700;
  letter-spacing: 1px;
  font-size: 0.75rem;
}

.version-text {
  color: #999;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.main-title {
  font-size: 4.5rem;
  line-height: 1.2;
  font-weight: 500;
  margin: 0 0 40px 0;
  letter-spacing: -2px;
  color: #FFFFFF;
}

.gradient-text {
  background: linear-gradient(90deg, #00F0FF 0%, #FF003C 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.hero-desc {
  font-size: 1.05rem;
  line-height: 1.8;
  color: #AAAAAA;
  max-width: 640px;
  margin-bottom: 50px;
  font-weight: 400;
  text-align: justify;
}

.hero-desc p {
  margin-bottom: 1.5rem;
}

.highlight-bold {
  color: #FFFFFF;
  font-weight: 700;
}

.highlight-orange {
  color: #00F0FF;
  font-weight: 700;
  font-family: 'JetBrains Mono', monospace;
}

.highlight-code {
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 6px;
  border-radius: 2px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9em;
  color: #00F0FF;
  font-weight: 600;
}

.slogan-text {
  font-size: 1.2rem;
  font-weight: 520;
  color: #FFFFFF;
  letter-spacing: 1px;
  border-left: 3px solid #00F0FF;
  padding-left: 15px;
  margin-top: 20px;
}

.blinking-cursor {
  color: #FF4500;
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.decoration-square {
  width: 16px;
  height: 16px;
  background: #FF4500;
}

.hero-right {
  flex: 0.8;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-end;
}

.logo-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 40px;
}

.hero-logo {
  max-width: 500px;
  width: 100%;
}

.scroll-down-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #1A1A24;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #00F0FF;
  font-size: 1.2rem;
  transition: all 0.2s;
}

.scroll-down-btn:hover {
  border-color: #00F0FF;
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
}

.dashboard-section {
  display: flex;
  gap: 60px;
  border-top: 1px solid #1A1A24;
  padding-top: 60px;
  align-items: flex-start;
}

.dashboard-section .left-panel,
.dashboard-section .right-panel {
  display: flex;
  flex-direction: column;
}

.left-panel {
  flex: 0.8;
}

.panel-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}

.status-dot {
  color: #00F0FF;
  font-size: 0.8rem;
  text-shadow: 0 0 5px rgba(0, 240, 255, 0.5);
}

.section-title {
  font-size: 2rem;
  font-weight: 520;
  margin: 0 0 15px 0;
  color: #FFFFFF;
}

.section-desc {
  color: #AAAAAA;
  margin-bottom: 25px;
  line-height: 1.6;
}

.metrics-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.metric-card {
  border: 1px solid #1A1A24;
  background: rgba(255, 255, 255, 0.02);
  padding: 20px 30px;
  min-width: 150px;
}

.metric-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.8rem;
  font-weight: 520;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.85rem;
  color: #999;
}

.steps-container {
  border: 1px solid #1A1A24;
  background: rgba(255, 255, 255, 0.02);
  padding: 30px;
  position: relative;
}

.steps-header {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #999;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.diamond-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.workflow-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.workflow-item {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.step-num {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #FFFFFF;
  opacity: 0.3;
}

.step-info {
  flex: 1;
}

.step-title {
  font-weight: 520;
  font-size: 1rem;
  margin-bottom: 4px;
}

.step-desc {
  font-size: 0.85rem;
  color: #666666;
}

.right-panel {
  flex: 1.2;
}

.console-box {
  border: 1px solid #1A1A24;
  background: #0D0D12;
  padding: 8px;
}

.console-section {
  padding: 20px;
}

.console-section.btn-section {
  padding-top: 0;
}

.console-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #666;
}

.upload-zone {
  border: 1px dashed #1A1A24;
  height: 150px;
  overflow-y: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #050508;
}

.upload-zone.has-files {
  align-items: flex-start;
}

.upload-zone:hover {
  background: #111118;
  border-color: #00F0FF;
}

.upload-placeholder {
  text-align: center;
}

.upload-icon {
  width: 40px;
  height: 40px;
  border: 1px solid #333;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: #00F0FF;
}

.upload-title {
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.upload-hint {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #999;
}

.file-list {
  width: 100%;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.file-item {
  display: flex;
  align-items: center;
  background: #111;
  color: #FFF;
  padding: 8px 12px;
  border: 1px solid #333;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
}

.file-name {
  flex: 1;
  margin: 0 10px;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #FF003C;
  transition: all 0.2s;
}

.remove-btn:hover {
  text-shadow: 0 0 8px rgba(255, 0, 60, 0.8);
}

.console-divider {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.console-divider::before,
.console-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #EEE;
}

.console-divider span {
  padding: 0 15px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #BBB;
  letter-spacing: 1px;
}

.input-wrapper {
  position: relative;
  border: 1px solid #1A1A24;
  background: #050508;
}

.code-input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.9rem;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  min-height: 250px;
  color: #00F0FF;
}

.code-input::placeholder {
  color: #444;
}

.model-badge {
  position: absolute;
  bottom: 10px;
  right: 15px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: #AAA;
}

.start-engine-btn {
  width: 100%;
  background: #00F0FF;
  color: #000;
  border: none;
  padding: 20px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.start-engine-btn:not(:disabled) {
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.4);
}

.start-engine-btn:hover:not(:disabled) {
  background: #FFFFFF;
  color: #000;
  box-shadow: 0 0 25px rgba(255, 255, 255, 0.6);
  transform: translateY(-2px);
}

.start-engine-btn:active:not(:disabled) {
  transform: translateY(0);
}

.start-engine-btn:disabled {
  background: #1A1A24;
  color: #444;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@keyframes pulse-border {
  0% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0.2); }
  70% { box-shadow: 0 0 0 6px rgba(0, 0, 0, 0); }
  100% { box-shadow: 0 0 0 0 rgba(0, 0, 0, 0); }
}

@media (max-width: 1024px) {
  .dashboard-section {
    flex-direction: column;
  }
  .hero-section {
    flex-direction: column;
  }
  .hero-left {
    padding-right: 0;
    margin-bottom: 40px;
  }
  .hero-logo {
    max-width: 200px;
    margin-bottom: 20px;
  }
}
</style>
