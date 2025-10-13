<template>
  <div class="p-6 space-y-6">
    <div>
      <h2 class="text-2xl font-bold mb-4">Workflow Builder Demo</h2>
      <div class="flex space-x-4">
        <Button @click="showTemplateSelector = true" variant="solid" theme="blue">
          Test Template Selector
        </Button>
        <Button @click="showWorkflowBuilder = true" variant="outline" theme="blue">
          Test Workflow Builder
        </Button>
      </div>
    </div>

    <!-- Template Selector Demo -->
    <div v-if="showTemplateSelector" class="border border-gray-200 rounded-lg">
      <div class="p-4 border-b border-gray-200 bg-gray-50">
        <h3 class="font-semibold">Template Selector</h3>
      </div>
      <div style="height: 600px;">
        <WorkflowTemplateSelector
          v-model="selectedTemplate"
          @continue="onTemplateSelected"
          @back="showTemplateSelector = false"
        />
      </div>
    </div>

    <!-- Workflow Builder Demo -->
    <div v-if="showWorkflowBuilder" class="border border-gray-200 rounded-lg">
      <div class="p-4 border-b border-gray-200 bg-gray-50">
        <h3 class="font-semibold">Workflow Builder</h3>
      </div>
      <div style="height: 600px;">
        <WorkflowBuilder
          :selected-template="selectedTemplate"
          :is-custom="isCustom"
          @back="showWorkflowBuilder = false"
          @back-to-templates="backToTemplates"
          @continue="onWorkflowComplete"
          @save-draft="saveDraft"
        />
      </div>
    </div>

    <!-- Results Display -->
    <div v-if="workflowSteps.length > 0" class="bg-gray-50 rounded-lg p-6">
      <h3 class="text-lg font-semibold mb-4">Workflow Result</h3>
      <div class="space-y-3">
        <div
          v-for="(step, index) in workflowSteps"
          :key="step.id"
          class="flex items-center p-3 bg-white rounded-lg border"
        >
          <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
            <span class="text-sm font-medium text-blue-600">{{ index + 1 }}</span>
          </div>
          <div class="flex-1">
            <div class="flex items-center mb-1">
              <FeatherIcon :name="step.icon" class="h-4 w-4 mr-2 text-gray-600" />
              <span class="font-medium text-gray-900">{{ step.name }}</span>
            </div>
            <p class="text-xs text-gray-600">{{ step.description }}</p>
            <div v-if="step.delay > 0" class="text-xs text-blue-600 mt-1">
              Send after {{ step.delay }} {{ step.delayUnit }}
            </div>
            <div v-else class="text-xs text-green-600 mt-1">
              Send immediately
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-4">
        <Button @click="clearResults" variant="outline" theme="gray" size="sm">
          Clear Results
        </Button>
      </div>
    </div>

    <!-- Debug Info -->
    <div v-if="debugInfo" class="bg-black text-green-400 p-4 rounded text-xs font-mono">
      <div class="mb-2 text-white">Debug Info:</div>
      <pre>{{ debugInfo }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import WorkflowTemplateSelector from './WorkflowTemplateSelector.vue'
import WorkflowBuilder from './WorkflowBuilder.vue'

// State
const showTemplateSelector = ref(false)
const showWorkflowBuilder = ref(false)
const selectedTemplate = ref(null)
const isCustom = ref(false)
const workflowSteps = ref([])
const debugInfo = ref('')

// Methods
const onTemplateSelected = (data) => {
  selectedTemplate.value = data.template
  isCustom.value = data.isCustom
  showTemplateSelector.value = false
  showWorkflowBuilder.value = true
  
  debugInfo.value = JSON.stringify({
    event: 'template_selected',
    template: data.template?.name || 'Custom',
    isCustom: data.isCustom
  }, null, 2)
  
  console.log('Template selected:', data)
}

const backToTemplates = () => {
  showWorkflowBuilder.value = false
  showTemplateSelector.value = true
  selectedTemplate.value = null
  isCustom.value = false
  
  debugInfo.value = JSON.stringify({
    event: 'back_to_templates'
  }, null, 2)
}

const onWorkflowComplete = (data) => {
  workflowSteps.value = data.steps
  showWorkflowBuilder.value = false
  
  debugInfo.value = JSON.stringify({
    event: 'workflow_complete',
    stepsCount: data.steps.length,
    steps: data.steps.map(s => ({
      name: s.name,
      type: s.type,
      delay: s.delay,
      delayUnit: s.delayUnit
    }))
  }, null, 2)
  
  console.log('Workflow completed:', data)
}

const saveDraft = (data) => {
  debugInfo.value = JSON.stringify({
    event: 'save_draft',
    stepsCount: data.steps.length,
    template: data.template?.name || 'Custom'
  }, null, 2)
  
  console.log('Draft saved:', data)
}

const clearResults = () => {
  workflowSteps.value = []
  debugInfo.value = ''
  selectedTemplate.value = null
  isCustom.value = false
}
</script>
