<template>
  <div class="p-6 space-y-6">
    <div>
      <h2 class="text-2xl font-bold mb-4">Campaign Wizard Demo</h2>
      <Button @click="openWizard" variant="solid" theme="blue">
        Open Campaign Wizard
      </Button>
    </div>

    <!-- Direct Workflow Test -->
    <WorkflowTest />

    <!-- Workflow Demo -->
    <WorkflowDemo />

    <!-- API Debugger -->
    <ApiDebugger />
    
    <CampaignWizard
      v-model="showWizard"
      @success="onSuccess"
      @draft-created="onDraftCreated"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button } from 'frappe-ui'
import CampaignWizard from './CampaignWizardFixed.vue'
import ApiDebugger from './ApiDebugger.vue'
import WorkflowDemo from './WorkflowDemo.vue'
import WorkflowTest from './WorkflowTest.vue'

const showWizard = ref(false)

const openWizard = () => {
  showWizard.value = true
}

const onSuccess = (data) => {
  console.log('Campaign wizard success:', data)
  showWizard.value = false
}

const onDraftCreated = (data) => {
  console.log('Draft created:', data)
}
</script>
