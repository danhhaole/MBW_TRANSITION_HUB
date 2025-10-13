<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold mb-6">Workflow Template Selector Test</h2>
    
    <!-- Direct test of WorkflowTemplateSelector -->
    <div class="border border-gray-200 rounded-lg" style="height: 600px;">
      <WorkflowTemplateSelector
        v-model="selectedTemplate"
        @continue="onContinue"
        @back="onBack"
      />
    </div>
    
    <!-- Results -->
    <div v-if="result" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
      <h3 class="font-semibold text-green-800 mb-2">Result:</h3>
      <pre class="text-sm text-green-700">{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import WorkflowTemplateSelector from './WorkflowTemplateSelector.vue'

const selectedTemplate = ref(null)
const result = ref(null)

const onContinue = (data) => {
  result.value = data
  console.log('Continue clicked:', data)
}

const onBack = () => {
  console.log('Back clicked')
}
</script>
