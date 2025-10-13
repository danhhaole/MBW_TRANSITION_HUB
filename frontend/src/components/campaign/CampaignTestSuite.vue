<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-7xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Campaign Wizard Test Suite</h1>
        <p class="text-gray-600">Test all campaign wizard components and workflow builder</p>
      </div>

      <!-- Navigation Tabs -->
      <div class="mb-6">
        <nav class="flex space-x-8">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            class="py-2 px-1 border-b-2 font-medium text-sm transition-colors"
            :class="activeTab === tab.id 
              ? 'border-blue-500 text-blue-600' 
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="bg-white rounded-lg shadow">
        <!-- Full Wizard Test -->
        <div v-if="activeTab === 'wizard'" class="p-6">
          <div class="mb-4">
            <h2 class="text-xl font-semibold mb-2">Full Campaign Wizard</h2>
            <p class="text-gray-600 mb-4">Test the complete wizard with all steps including workflow builder</p>
            <Button @click="openWizard" variant="solid" theme="blue" size="lg">
              <FeatherIcon name="play" class="h-5 w-5 mr-2" />
              Launch Campaign Wizard
            </Button>
          </div>
          
          <CampaignWizardFixed
            v-model="showWizard"
            @success="onWizardSuccess"
            @draft-created="onDraftCreated"
          />
        </div>

        <!-- Workflow Builder Test -->
        <div v-if="activeTab === 'workflow'" class="p-6">
          <WorkflowDemo />
        </div>

        <!-- API Debugger -->
        <div v-if="activeTab === 'api'" class="p-6">
          <ApiDebugger />
        </div>

        <!-- Components Test -->
        <div v-if="activeTab === 'components'" class="p-6 space-y-8">
          <div>
            <h2 class="text-xl font-semibold mb-4">Individual Components</h2>
            
            <!-- Header Test -->
            <div class="mb-6">
              <h3 class="text-lg font-medium mb-3">Campaign Wizard Header</h3>
              <div class="border border-gray-200 rounded-lg">
                <CampaignWizardHeader
                  campaign-name="Test Campaign"
                  :current-step="2"
                  :total-steps="5"
                  :can-save="true"
                  :can-proceed="true"
                  :can-finalize="false"
                  @exit="console.log('Exit clicked')"
                  @back="console.log('Back clicked')"
                  @save="console.log('Save clicked')"
                  @save-and-continue="console.log('Save and continue clicked')"
                  @update:campaign-name="console.log('Name updated:', $event)"
                />
              </div>
            </div>

            <!-- Stepper Test -->
            <div class="mb-6">
              <h3 class="text-lg font-medium mb-3">Campaign Wizard Stepper</h3>
              <div class="border border-gray-200 rounded-lg p-4">
                <CampaignWizardStepper
                  :steps="testSteps"
                  :current-step="3"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Results & Logs -->
        <div v-if="activeTab === 'results'" class="p-6">
          <h2 class="text-xl font-semibold mb-4">Test Results & Logs</h2>
          
          <!-- Success Messages -->
          <div v-if="results.length > 0" class="mb-6">
            <h3 class="text-lg font-medium mb-3">Results</h3>
            <div class="space-y-2">
              <div
                v-for="(result, index) in results"
                :key="index"
                class="p-3 rounded-lg"
                :class="result.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'"
              >
                <div class="flex items-center">
                  <FeatherIcon 
                    :name="result.type === 'success' ? 'check-circle' : 'x-circle'" 
                    class="h-4 w-4 mr-2" 
                  />
                  <span class="font-medium">{{ result.title }}</span>
                </div>
                <p class="text-sm mt-1">{{ result.message }}</p>
                <div class="text-xs mt-2 opacity-75">{{ result.timestamp }}</div>
              </div>
            </div>
            
            <Button @click="clearResults" variant="outline" theme="gray" size="sm" class="mt-4">
              Clear Results
            </Button>
          </div>

          <!-- Debug Logs -->
          <div v-if="debugLogs.length > 0">
            <h3 class="text-lg font-medium mb-3">Debug Logs</h3>
            <div class="bg-black text-green-400 p-4 rounded-lg text-sm font-mono max-h-96 overflow-y-auto">
              <div v-for="(log, index) in debugLogs" :key="index" class="mb-1">
                <span class="text-gray-400">[{{ log.timestamp }}]</span>
                <span class="ml-2">{{ log.message }}</span>
              </div>
            </div>
            
            <Button @click="clearLogs" variant="outline" theme="gray" size="sm" class="mt-4">
              Clear Logs
            </Button>
          </div>

          <!-- Empty State -->
          <div v-if="results.length === 0 && debugLogs.length === 0" class="text-center py-12">
            <FeatherIcon name="file-text" class="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-gray-900 mb-2">No Results Yet</h3>
            <p class="text-gray-600">Run some tests to see results and logs here</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import CampaignWizardFixed from './CampaignWizardFixed.vue'
import CampaignWizardHeader from './CampaignWizardHeader.vue'
import CampaignWizardStepper from './CampaignWizardStepper.vue'
import WorkflowDemo from './WorkflowDemo.vue'
import ApiDebugger from './ApiDebugger.vue'

// State
const activeTab = ref('wizard')
const showWizard = ref(false)
const results = ref([])
const debugLogs = ref([])

// Tabs configuration
const tabs = [
  { id: 'wizard', label: 'Full Wizard' },
  { id: 'workflow', label: 'Workflow Builder' },
  { id: 'components', label: 'Components' },
  { id: 'api', label: 'API Debugger' },
  { id: 'results', label: 'Results & Logs' }
]

// Test data
const testSteps = [
  { number: 1, label: 'Information', description: 'Campaign details' },
  { number: 2, label: 'Select Source', description: 'Data source' },
  { number: 3, label: 'Target Segment', description: 'Audience selection' },
  { number: 4, label: 'Create Triggers', description: 'Workflow setup' },
  { number: 5, label: 'Review & Activate', description: 'Final review' }
]

// Methods
const openWizard = () => {
  showWizard.value = true
  addLog('Campaign wizard opened')
}

const onWizardSuccess = (data) => {
  addResult('success', 'Campaign Created', `Campaign "${data.data?.campaign_name || 'Untitled'}" created successfully`)
  addLog(`Campaign creation successful: ${JSON.stringify(data)}`)
  showWizard.value = false
}

const onDraftCreated = (data) => {
  addResult('success', 'Draft Saved', 'Campaign draft saved successfully')
  addLog(`Draft created: ${JSON.stringify(data)}`)
}

const addResult = (type, title, message) => {
  results.value.unshift({
    type,
    title,
    message,
    timestamp: new Date().toLocaleTimeString()
  })
}

const addLog = (message) => {
  debugLogs.value.unshift({
    message,
    timestamp: new Date().toLocaleTimeString()
  })
}

const clearResults = () => {
  results.value = []
}

const clearLogs = () => {
  debugLogs.value = []
}

// Global console override for capturing logs
const originalConsoleLog = console.log
console.log = (...args) => {
  originalConsoleLog(...args)
  addLog(args.join(' '))
}
</script>
