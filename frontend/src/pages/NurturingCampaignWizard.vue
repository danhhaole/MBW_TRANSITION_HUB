<template>
  <div v-if="show" class="fixed inset-0 bg-white z-[9] flex flex-col">
    <!-- Header - Reuse existing component -->
    <CampaignWizardHeader
      :campaign-name="campaignData.campaign_name || __('New Nurturing Campaign')"
      :current-step="currentStep"
      :total-steps="totalSteps"
      :loading="false"
      :saving="saving"
      :finalizing="finalizing"
      :auto-saving="false"
      :save-success="false"
      :can-save="true"
      :can-proceed="canProceed"
      :can-finalize="isLastStep"
      :is-edit-mode="false"
      @exit="closeWizard"
      @back="prevStep"
      @save="saveDraft"
      @save-and-continue="nextStep"
      @finalize="finalizeCampaign"
      @update:campaign-name="campaignData.campaign_name = $event"
    />

    <!-- Stepper - Reuse existing component -->
    <CampaignWizardStepper
      :steps="formattedSteps"
      :current-step="currentStep"
      @step-click="handleStepClick"
    />

    <!-- Content Area -->
    <div class="flex-1 overflow-y-auto bg-gray-50">
      <div class="max-w-7xl mx-auto px-6 py-8">
        <!-- Step 1: Campaign Information & Target Segment -->
        <CampaignStep1
          v-if="currentStep === 1"
          :campaign-name="campaignData.campaign_name"
          :objective="campaignData.objective"
          :config-data="campaignData.config_data"
          :conditions="campaignData.conditions"
          :candidate-count="campaignData.candidate_count"
          :show-error="showValidationError"
          @update:campaign-name="campaignData.campaign_name = $event"
          @update:objective="campaignData.objective = $event"
          @update:config-data="campaignData.config_data = $event"
          @update:conditions="campaignData.conditions = $event"
          @validate="handleValidate"
          @change="handleConditionsChange"
        />

        <!-- Step 2: Content Timeline -->
        <CampaignStep2
          v-else-if="currentStep === 2"
          :triggers="campaignData.triggers"
          :campaign-name="campaignData.campaign_name"
          @update:triggers="campaignData.triggers = $event"
        />

        <!-- Placeholder steps -->
        <div v-else class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">
            {{ steps[currentStep - 1].title }}
          </h3>
          <p class="text-gray-600">
            {{ __('This step will be implemented soon') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { call } from 'frappe-ui'
import CampaignWizardHeader from '@/components/campaign/CampaignWizardHeader.vue'
import CampaignWizardStepper from '@/components/campaign/CampaignWizardStepper.vue'
import CampaignStep1 from '@/components/campaign_new/nurturing/Step1_CampaignInfo.vue'
import CampaignStep2 from '@/components/campaign_new/nurturing/Step2_ContentTimeline.vue'
import { useCampaignStore } from '@/stores/campaign'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  campaignType: {
    type: String,
    default: 'NURTURING'
  },
  editCampaignId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['close', 'success', 'campaign-created'])

const campaignStore = useCampaignStore()
const toast = useToast()

const currentStep = ref(1)
const saving = ref(false)
const finalizing = ref(false)
const showValidationError = ref(false)
const loadingTriggers = ref(false)

const campaignData = ref({
  campaign_name: '',
  objective: '',
  config_data: {},
  conditions: [],
  candidate_count: 0,
  channel: '',
  type: props.campaignType, // 'NURTURING'
  status: 'Draft',
  triggers: [] // Timeline triggers for nurturing
})

const steps = ref([
  { title: __('Campaign Info'), key: 'info' },
  { title: __('Content Design'), key: 'content' },
  { title: __('Review'), key: 'review' }
])

const totalSteps = computed(() => steps.value.length)

const formattedSteps = computed(() => {
  return steps.value.map((step, index) => ({
    number: index + 1,
    label: step.title,  // CampaignWizardStepper expects 'label' not 'title'
    key: step.key,
    status: currentStep.value > index + 1 ? 'completed' : currentStep.value === index + 1 ? 'active' : 'pending'
  }))
})

const isLastStep = computed(() => currentStep.value === totalSteps.value)

const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return campaignData.value.campaign_name?.trim()
    // config_data/conditions are optional
  }
  
  if (currentStep.value === 2) {
    // Validate triggers
    if (!campaignData.value.triggers || campaignData.value.triggers.length === 0) {
      return false
    }
    
    // Check each trigger has required fields
    return campaignData.value.triggers.every(trigger => {
      const hasChannel = !!trigger.channel
      
      // Sender account is optional now
      
      // Validate content based on channel
      let hasContent = false
      if (trigger.channel === 'email') {
        // Email: must have subject and content
        hasContent = !!(trigger.content?.email_subject?.trim() && trigger.content?.email_content?.trim())
      } else if (trigger.channel === 'zalo') {
        // Zalo: must have at least one block with content
        if (trigger.content?.blocks && Array.isArray(trigger.content.blocks)) {
          hasContent = trigger.content.blocks.some(block => {
            if (block.type === 'text') {
              return !!(block.text_content?.trim())
            }
            if (block.type === 'image') {
              return !!(block.image)
            }
            return false
          })
        } else {
          // Fallback for old format
          hasContent = !!(trigger.content?.message?.trim())
        }
      } else if (trigger.channel === 'messenger') {
        // Messenger: check for blocks structure or simple message
        if (trigger.content?.blocks && Array.isArray(trigger.content.blocks)) {
          hasContent = trigger.content.blocks.some(block => {
            if (block.type === 'text') {
              return !!(block.text_content?.trim())
            }
            if (block.type === 'image') {
              return !!(block.image)
            }
            return false
          })
        } else {
          // Simple message format
          hasContent = !!(trigger.content?.message?.trim())
        }
      }
      
      return hasChannel && hasContent
    })
  }
  
  return true
})

const handleValidate = (isValid) => {
  console.log('Conditions validation:', isValid)
}

const handleConditionsChange = (conditions) => {
  console.log('Conditions changed:', conditions)
}

const handleStepClick = (stepNumber) => {
  // Allow clicking on previous steps only
  if (stepNumber < currentStep.value) {
    currentStep.value = stepNumber
  }
}

// Load triggers when entering Step 2
const loadTriggers = async () => {
  if (!campaignData.value.name) {
    return
  }

  loadingTriggers.value = true
  try {
    const result = await call('mbw_mira.api.campaign_social.get_nurturing_campaign_triggers', {
      campaign_id: campaignData.value.name
    })

    if (result.success && result.data) {
      campaignData.value.triggers = result.data
      console.log('✅ Triggers loaded:', result.data)
    } else {
      console.error('❌ Error loading triggers:', result.message)
    }
  } catch (error) {
    console.error('❌ Error loading triggers:', error)
  } finally {
    loadingTriggers.value = false
  }
}

// Watch for step changes to load triggers
watch(currentStep, async (newStep, oldStep) => {
  if (newStep === 2 && oldStep !== 2 && campaignData.value.name) {
    await loadTriggers()
  }
})

const closeWizard = () => {
  if (confirm(__('Are you sure you want to close? Unsaved changes will be lost.'))) {
    emit('close')
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    showValidationError.value = false
  }
}

const nextStep = async () => {
  if (!canProceed.value) {
    showValidationError.value = true
    toast.error(__('Please fill in all required fields'))
    return
  }

  showValidationError.value = false
  await saveDraft()
  
  if (currentStep.value < totalSteps.value) {
    currentStep.value++
  }
}

const saveDraft = async () => {
  saving.value = true
  try {
    // Step 1: Save campaign
    if (!campaignData.value.name) {
      // Create new campaign
      // Extract target_pool from config_data
      console.log('Campaign config_data:', campaignData.value.config_data)
      const targetPool = campaignData.value.config_data?.selectedSegment?.value || null
      
      const result = await campaignStore.submitNewCampaign({
        campaign_name: campaignData.value.campaign_name,
        description: campaignData.value.objective,
        target_pool: targetPool,
        condition_filter: JSON.stringify(campaignData.value.conditions),
        type: campaignData.value.type,
        status: 'DRAFT'
      })

      if (result.success && result.data?.name) {
        campaignData.value.name = result.data.name
        toast.success(__('Campaign created successfully'))
        
        // Emit event to refresh campaign list
        emit('campaign-created', { name: result.data.name })
      } else {
        toast.error(result.error || __('Failed to create campaign'))
        return
      }
    } else if (currentStep.value === 1) {
      // Update existing campaign info (Step 1 fields)
      try {
        // Extract target_pool from config_data
        console.log('Campaign config_data:', campaignData.value.config_data)
        const targetPool = campaignData.value.config_data?.selectedSegment || null
        
        await call('frappe.client.set_value', {
          doctype: 'Mira Campaign',
          name: campaignData.value.name,
          fieldname: {
            campaign_name: campaignData.value.campaign_name,
            description: campaignData.value.objective,
            target_pool: targetPool,
            condition_filter: JSON.stringify(campaignData.value.conditions)
          }
        })
        console.log('✅ Campaign info updated')
      } catch (error) {
        console.error('❌ Error updating campaign info:', error)
        toast.error(__('Failed to update campaign info'))
        return
      }
    }

    // Step 2: Save triggers (timeline messages)
    if (currentStep.value === 2 && campaignData.value.name) {
      try {
        // Prepare triggers data - extract sender_account value
        const triggersData = campaignData.value.triggers.map(trigger => ({
          ...trigger,
          sender_account: typeof trigger.sender_account === 'object' 
            ? trigger.sender_account?.value 
            : trigger.sender_account
        }))

        const result = await call('mbw_mira.api.campaign_social.save_nurturing_campaign_triggers', {
          campaign_id: campaignData.value.name,
          triggers: triggersData
        })

        if (result.success) {
          console.log('✅ Triggers saved:', result.data)
          toast.success(__('Timeline messages saved successfully'))
        } else {
          console.error('❌ Error saving triggers:', result.message)
          toast.error(result.message || __('Failed to save timeline messages'))
          return
        }
      } catch (error) {
        console.error('❌ Error saving triggers:', error)
        toast.error(__('Failed to save timeline messages'))
        return
      }
    }

    // Don't show toast for auto-save
  } catch (error) {
    console.error('Error saving draft:', error)
    toast.error(__('An error occurred while saving'))
  } finally {
    saving.value = false
  }
}

const finalizeCampaign = async () => {
  if (!canProceed.value) {
    showValidationError.value = true
    toast.error(__('Please complete all required fields'))
    return
  }

  finalizing.value = true
  try {
    // Extract target_pool from config_data
    const targetPool = campaignData.value.config_data?.selectedSegment?.value || null
    
    const result = await campaignStore.updateCampaign(campaignData.value.name, {
      campaign_name: campaignData.value.campaign_name,
      description: campaignData.value.objective,
      target_pool: targetPool,
      condition_filter: JSON.stringify(campaignData.value.conditions),
      status: 'Active'
    })

    if (result.success) {
      toast.success(__('Campaign activated successfully!'))
      emit('success', result.data)
      emit('close')
    } else {
      toast.error(result.error || __('Failed to activate campaign'))
    }
  } catch (error) {
    console.error('Error activating campaign:', error)
    toast.error(__('An error occurred while activating campaign'))
  } finally {
    finalizing.value = false
  }
}

// Load campaign data for editing
const loadCampaignData = async (campaignId) => {
  try {
    console.log('📂 Loading nurturing campaign data:', campaignId)
    
    const result = await call('frappe.client.get', {
      doctype: 'Mira Campaign',
      name: campaignId
    })
    
    if (result) {
      // Parse config data and conditions from separate fields
      let configData = {}
      let conditions = []
      
      // Build config_data from target_pool
      if (result.target_pool) {
        // Get segment details to rebuild config_data
        try {
          const segmentResult = await call('frappe.client.get', {
            doctype: 'Mira Segment',
            name: result.target_pool
          })
          
          if (segmentResult) {
            configData = {
              selectedSegment: {
                label: segmentResult.segment_name || segmentResult.name,
                value: segmentResult.name
              }
            }
          }
        } catch (error) {
          console.error('Error loading segment details:', error)
          // Fallback: create basic config with just the ID
          configData = {
            selectedSegment: {
              label: result.target_pool,
              value: result.target_pool
            }
          }
        }
      } else {
        // Fallback to old format
        configData = result.config_data ? JSON.parse(result.config_data) : {}
      }
      
      // Parse condition_filter for filter conditions
      if (result.condition_filter) {
        try {
          conditions = JSON.parse(result.condition_filter)
        } catch (error) {
          console.error('Error parsing condition_filter:', error)
          // Fallback to old format
          conditions = result.conditions ? JSON.parse(result.conditions) : []
        }
      } else {
        // Fallback to old format or source_config
        if (result.conditions) {
          conditions = JSON.parse(result.conditions)
        } else if (result.source_config) {
          try {
            const sourceConfig = JSON.parse(result.source_config)
            conditions = sourceConfig.conditions || []
          } catch (error) {
            conditions = []
          }
        }
      }
      
      campaignData.value = {
        name: result.name,
        campaign_name: result.campaign_name || '',
        objective: result.description || '',
        config_data: configData,
        conditions: conditions,
        candidate_count: result.candidate_count || 0,
        channel: result.channel || '',
        type: result.type || 'NURTURING',
        status: result.status || 'DRAFT'
      }
      
      console.log('✅ Campaign data loaded:', campaignData.value)
    }
  } catch (error) {
    console.error('❌ Error loading campaign:', error)
    toast.error(__('Failed to load campaign data'))
  }
}

// Reset campaign data
const resetCampaignData = () => {
  campaignData.value = {
    campaign_name: '',
    objective: '',
    config_data: {},
    conditions: [],
    candidate_count: 0,
    channel: '',
    type: props.campaignType,
    status: 'DRAFT'
  }
  currentStep.value = 1
}

// Watch for prop changes
watch(() => props.show, (newVal) => {
  if (newVal && props.editCampaignId) {
    // Load existing campaign data
    loadCampaignData(props.editCampaignId)
  } else if (newVal) {
    // Reset for new campaign
    resetCampaignData()
  }
})
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
