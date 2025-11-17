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
        <!-- Step 1: Campaign Info -->
        <CampaignStep1
          v-if="currentStep === 1"
          :campaign-name="campaignData.campaign_name"
          :objective="campaignData.objective"
          :campaign-id="campaignData.name"
          :campaign-tags="campaignData.campaign_tags"
          :config-data="campaignData.config_data"
          :conditions="campaignData.conditions"
          :candidate-count="campaignData.candidate_count"
          :show-error="showValidationError"
          :start-date="campaignData.start_date"
          @update:campaign-name="campaignData.campaign_name = $event"
          @update:objective="campaignData.objective = $event"
          @update:campaign-tags="campaignData.campaign_tags = $event"
          @update:config-data="campaignData.config_data = $event"
          @update:conditions="campaignData.conditions = $event"
          @update:start-date="campaignData.start_date = $event"
          @validate="handleValidate"
          @change="handleConditionsChange"
        />

        <!-- Step 2: Content Timeline -->
        <CampaignStep2
          v-else-if="currentStep === 2"
          :triggers="campaignData.triggers"
          :campaign-name="campaignData.campaign_name"
           :name="campaignData.name"
          :ladipage-url="campaignData.ladipage_url"
          :ladipage-id="campaignData.ladipage_id"
          :company-info="campaignData.company_info"
          :job-info="campaignData.job_info"
          @update:triggers="campaignData.triggers = $event"
          @update:ladipage-url="campaignData.ladipage_url = $event"
          @update:ladipage-id="campaignData.ladipage_id = $event"
        />

        <!-- Step 3: Settings & Triggers -->
        <CampaignStep3
          v-else-if="currentStep === 3"
          :start-date="campaignData.start_date"
          :triggers="campaignData.step3_triggers"
          @update:start-date="campaignData.start_date = $event"
          @update:triggers="campaignData.step3_triggers = $event"
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
import CampaignStep3 from '@/components/campaign_new/nurturing/Step3_Settings.vue'
import { useCampaignStore } from '@/stores/campaign'
import { useToast } from '@/composables/useToast'
import moment from 'moment'

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
  campaign_tags: [],
  config_data: {
    selectedSegment: null
  },
  conditions: [],
  candidate_count: 0,
  triggers: [],
  start_date: '',
  step3_triggers: [],
  ladipage_url: '',
  ladipage_id: '',
  company_info: '',
  job_info: '',
  name: null
})

const initialCampaignData = ref(null)

const hasUnsavedChanges = computed(() => {
  if (!initialCampaignData.value) return false
  
  // Deep compare the two objects
  return JSON.stringify(campaignData.value) !== JSON.stringify(initialCampaignData.value)
})

const steps = ref([
  { title: __('Campaign Info'), key: 'info' },
  { title: __('Content Design'), key: 'content' },
  { title: __('Settings & Actions'), key: 'settings' }
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
  
  if (currentStep.value === 3) {
    // Step 3: Settings & Triggers - optional validation
    // Triggers are optional, but if present, should be valid
    if (campaignData.value.step3_triggers && campaignData.value.step3_triggers.length > 0) {
      return campaignData.value.step3_triggers.every(trigger => {
        // Basic validation: trigger must have type and at least one action
        return !!(trigger.trigger_type && trigger.actions && trigger.actions.length > 0)
      })
    }
    return true // Triggers are optional
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

// Load campaign flows and convert to triggers for Step 3
const loadCampaignFlows = async (campaignId) => {
  try {
    console.log('🔀 Loading flows for campaign:', campaignId)
    
    const result = await call('mbw_mira.api.campaign_flow.get_campaign_flows', {
      campaign_id: campaignId
    })
    
    if (result.success && result.data) {
      campaignData.value.step3_triggers = result.data
      console.log('✅ Loaded step3 triggers from flows:', result.data)
      console.log('📊 Step3 Triggers detail:', JSON.stringify(result.data, null, 2))
    } else {
      console.log('ℹ️ No flows found for campaign')
      campaignData.value.step3_triggers = []
    }
  } catch (error) {
    console.error('❌ Error loading flows:', error)
    campaignData.value.step3_triggers = []
  }
}

// Watch for step changes to load triggers
watch(currentStep, async (newStep, oldStep) => {
  if (newStep === 2 && oldStep !== 2 && campaignData.value.name) {
    await loadTriggers()
  }
  if (newStep === 3 && oldStep !== 3 && campaignData.value.name) {
    await loadCampaignFlows(campaignData.value.name)
  }
})

const loadCampaignTags = async (campaignId) => {
  try {
    console.log('🏷️ Loading campaign tags:', campaignId)
    
    // Get campaign document with _user_tags field
    const campaign = await call('frappe.client.get', {
      doctype: 'Mira Campaign',
      name: campaignId,
      fields: ['_user_tags']
    })
    
    if (campaign && campaign._user_tags) {
      // Parse _user_tags string format: ",test,abc" -> ["test", "abc"]
      const tagTitles = campaign._user_tags
        .split(',')
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0) // Remove empty strings
      
      console.log('📋 Parsed tags from _user_tags:', tagTitles)
      
      if (tagTitles.length > 0) {
        // Get tag colors from Mira Tag doctype
        const colorResponse = await call('frappe.client.get_list', {
          doctype: 'Mira Tag',
          fields: ['title', 'color'],
          filters: [['title', 'in', tagTitles]]
        })
        
        const colorMap = {}
        for (const tag of colorResponse || []) {
          colorMap[tag.title] = tag.color
        }
        
        // Map tags with colors
        campaignData.value.campaign_tags = tagTitles.map(tagTitle => ({
          label: tagTitle,
          value: tagTitle,
          color: colorMap[tagTitle] || '#6B7280'
        }))
        
        console.log('✅ Campaign tags loaded:', campaignData.value.campaign_tags)
      } else {
        campaignData.value.campaign_tags = []
        console.log('ℹ️ No tags found for campaign')
      }
    } else {
      campaignData.value.campaign_tags = []
      console.log('ℹ️ No _user_tags field or empty')
    }
  } catch (error) {
    console.error('❌ Error loading campaign tags:', error)
    campaignData.value.campaign_tags = []
    // Don't show error toast as tags are optional
  }
}

const closeWizard = () => {
  // Only show confirmation if there are unsaved changes
  if (hasUnsavedChanges.value) {
    if (confirm(__('Are you sure you want to close? Unsaved changes will be lost.'))) {
      emit('close')
    }
  } else {
    // No changes, close directly
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
  
  // Only save if there are actual changes
  if (hasUnsavedChanges.value) {
    console.log('📝 Changes detected, saving before next step...')
    await saveDraft()
  } else {
    console.log('⏭️ No changes detected, skipping save')
  }
  
  if (currentStep.value < totalSteps.value) {
    currentStep.value++
    // Update initial state after moving to next step
    initialCampaignData.value = JSON.parse(JSON.stringify(campaignData.value))
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
const targetPool = campaignData.value.config_data?.selectedSegment?.value || campaignData.value.config_data?.selectedSegment || null
      
      const result = await campaignStore.submitNewCampaign({
        campaign_name: campaignData.value.campaign_name,
        description: campaignData.value.objective,
        target_pool: targetPool,
        condition_filter: JSON.stringify(campaignData.value.conditions),
        type: campaignData.value.type,
        status: 'DRAFT',
        start_date: campaignData.value.start_date === 'SEND_NOW' ? moment().format('YYYY-MM-DDTHH:mm') : (campaignData.value.start_date || moment().format('YYYY-MM-DDTHH:mm')),
      })

      if (result.success && result.data?.name) {
        campaignData.value.name = result.data.name
        toast.success(__('Campaign created successfully'))
        
        // Add tags if any were selected before campaign was created
        if (campaignData.value.campaign_tags && campaignData.value.campaign_tags.length > 0) {
          console.log('🏷️ Adding tags to newly created campaign:', campaignData.value.campaign_tags)
          try {
            for (const tag of campaignData.value.campaign_tags) {
              await call('frappe.desk.doctype.tag.tag.add_tag', {
                tag: tag.value,
                dt: 'Mira Campaign',
                dn: campaignData.value.name
              })
            }
            console.log('✅ Tags added to campaign')
          } catch (error) {
            console.error('❌ Error adding tags to campaign:', error)
            // Don't fail the whole process if tags fail
          }
        }
        
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
        const targetPool = campaignData.value.config_data?.selectedSegment?.value || campaignData.value.config_data?.selectedSegment || null
        
        await call('frappe.client.set_value', {
          doctype: 'Mira Campaign',
          name: campaignData.value.name,
          fieldname: {
            campaign_name: campaignData.value.campaign_name,
            description: campaignData.value.objective,
            target_pool: targetPool,
            condition_filter: JSON.stringify(campaignData.value.conditions),
            start_date: campaignData.value.start_date
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

    // Step 3: Save settings & actions
    if (currentStep.value === 3 && campaignData.value.name) {
      try {
        await call('frappe.client.set_value', {
          doctype: 'Mira Campaign',
          name: campaignData.value.name,
          fieldname: {
            start_date: campaignData.value.start_date
          }
        })
        
        // Save step3 triggers separately if needed
        if (campaignData.value.step3_triggers && campaignData.value.step3_triggers.length > 0) {
          console.log('💾 Saving Step3 triggers:', campaignData.value.step3_triggers)
          
          try {
            // Use same API as timeline triggers but with different trigger types
            const result = await call('mbw_mira.api.campaign_social.save_nurturing_campaign_triggers', {
              campaign_id: campaignData.value.name,
              triggers: campaignData.value.step3_triggers
            })

            if (result.success) {
              console.log('✅ Step3 triggers saved:', result.data)
              toast.success(__('Event triggers saved successfully'))
            } else {
              console.error('❌ Error saving step3 triggers:', result.message)
              toast.error(result.message || __('Failed to save event triggers'))
            }
          } catch (error) {
            console.error('❌ Error saving step3 triggers:', error)
            toast.error(__('Failed to save event triggers'))
          }
        } else {
          console.log('📝 No Step3 triggers to save')
        }
        
        console.log('✅ Settings saved')
      } catch (error) {
        console.error('❌ Error saving settings:', error)
        toast.error(__('Failed to save settings'))
        return
      }
    }

    // Don't show toast for auto-save
    
    // Update initial state after successful save
    initialCampaignData.value = JSON.parse(JSON.stringify(campaignData.value))
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
    console.log('🚀 Finalizing campaign...')
    
    // Step 1: Ensure campaign is saved
    if (!campaignData.value.name) {
      toast.error(__('Campaign must be saved first'))
      return
    }

    console.log('Campaign data:', campaignData.value)
    console.log('📊 Step 2 triggers:', campaignData.value.triggers)
    console.log('📊 Step 3 triggers:', campaignData.value.step3_triggers)

    // Step 2: Update campaign settings (start_date)
    try {
      await call('frappe.client.set_value', {
        doctype: 'Mira Campaign',
        name: campaignData.value.name,
        fieldname: {
          start_date: campaignData.value.start_date
        }
      })
      console.log('✅ Campaign start_date updated')
    } catch (error) {
      console.error('❌ Error updating campaign settings:', error)
    }

    // Step 3: Sync all flows with triggers in one API call
    try {
      console.log('🔄 Syncing flows with triggers...')
      
      // Combine both timeline triggers (Step 2) and event triggers (Step 3)
      const allTriggers = [
        ...(campaignData.value.triggers || []),        // Step 2: Timeline triggers
        ...(campaignData.value.step3_triggers || [])   // Step 3: Event triggers
      ]
      
      console.log('📊 All triggers to sync:', allTriggers)
      
      const result = await call('mbw_mira.api.campaign_flow.sync_campaign_flows', {
        campaign_id: campaignData.value.name,
        triggers: allTriggers
      })
      
      if (result && result.success) {
        console.log(`✅ Flows synced: ${result.created || 0} created, ${result.updated || 0} updated, ${result.deleted || 0} deleted`)
      }
    } catch (error) {
      console.error('❌ Error syncing flows:', error)
    }

    // Step 4: Reload campaign data to get updated flow status
    await loadCampaignData(campaignData.value.name)
    
    // Step 5: Campaign finalized - Reset wizard
    toast.success(__('Campaign saved successfully!'))
    console.log('✅ Campaign finalized')
    
    // Reset wizard to step 1
    currentStep.value = 1
    resetCampaignData()
    
    // Clear unsaved changes flag before closing
    initialCampaignData.value = JSON.parse(JSON.stringify(campaignData.value))
    
    emit('success', { name: campaignData.value.name })
    emit('close')
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
        campaign_tags: [], // Will be loaded separately
        config_data: configData,
        conditions: conditions,
        candidate_count: result.candidate_count || 0,
        channel: result.channel || '',
        type: result.type || 'NURTURING',
        status: result.status || 'DRAFT',
        start_date: result.start_date || null,
        // Landing page data
        ladipage_url: result.ladipage_url || '',
        ladipage_id: result.ladipage_id || '',
        company_info: result.company_info ? JSON.parse(result.company_info) : {},
        job_info: result.job_info ? JSON.parse(result.job_info) : {},
        step3_triggers: [], // TODO: Load step3 triggers from backend
        triggers: [] // Will be loaded separately in Step 2
      }
      
      console.log('✅ Campaign data loaded:', campaignData.value)
      
      // Load campaign tags
      await loadCampaignTags(campaignId)
      
      // Save initial state after loading
      initialCampaignData.value = JSON.parse(JSON.stringify(campaignData.value))
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
    status: 'DRAFT',
    triggers: [],
    start_date: new Date().toISOString().slice(0, 16), // Reset to current time
    step3_triggers: []
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
    // Save initial state for change detection
    initialCampaignData.value = JSON.parse(JSON.stringify(campaignData.value))
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
