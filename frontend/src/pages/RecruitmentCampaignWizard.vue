<template>
  <div v-if="show" class="fixed inset-0 bg-white z-[9] flex flex-col">
    <!-- Header with CampaignWizardHeader -->
    <CampaignWizardHeader
      :campaign-name="campaignData.campaign_name"
      :current-step="currentStep"
      :total-steps="totalSteps"
      :can-proceed="canProceed"
      :saving="saving"
      :finalizing="finalizing"
      :is-edit-mode="false"
      :show-save-as-template="!!campaignData.name"
      :saving-as-template="savingAsTemplate"
      @exit="closeWizard"
      @back="prevStep"
      @save="saveDraft"
      @save-and-continue="nextStep"
      @finalize="finalizeCampaign"
      @save-as-template="handleSaveAsTemplate"
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
          :objective="campaignData.description"
          :campaign-id="campaignData.name"
          :campaign-tags="campaignData.campaign_tags"
          :config-data="campaignData.config_data"
          :conditions="campaignData.conditions"
          :candidate-count="campaignData.candidate_count"
          :show-error="showValidationError"
          :start-date="campaignData.start_date"
          @update:campaign-name="campaignData.campaign_name = $event"
          @update:objective="campaignData.description = $event"
          @update:campaign-tags="campaignData.campaign_tags = $event"
          @update:config-data="campaignData.config_data = $event"
          @update:conditions="campaignData.conditions = $event"
          @update:candidate-count="campaignData.candidate_count = $event"
          @update:start-date="campaignData.start_date = $event"
          @validate="handleValidate"
          @change="handleConditionsChange"
        />

        <!-- Step 2: Content & Channels -->
        <CampaignStep2
          v-else-if="currentStep === 2"
          :selected-channels="campaignData.selected_channels"
          :email-content="campaignData.email_content"
          :facebook-content="campaignData.facebook_content"
          :zalo-content="campaignData.zalo_content"
          :campaign-name="campaignData.campaign_name"
          :name="campaignData.name"
          :ladipage-url="campaignData.ladipage_url"
          :ladipage-id="campaignData.ladipage_id"
          :company-info="campaignData.company_info"
          :job-info="campaignData.job_info"
          :show-error="showValidationError"
          @update:selected-channels="campaignData.selected_channels = $event"
          @update:email-content="campaignData.email_content = $event"
          @update:facebook-content="campaignData.facebook_content = $event"
          @update:zalo-content="campaignData.zalo_content = $event"
          @update:ladipage-url="campaignData.ladipage_url = $event"
          @update:ladipage-id="campaignData.ladipage_id = $event"
        />

        <!-- Step 3: Settings & Triggers -->
        <CampaignStep3
          v-else-if="currentStep === 3"
          :start-date="campaignData.start_date"
          :triggers="campaignData.triggers"
          @update:start-date="campaignData.start_date = $event"
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

    <!-- Save as Template Modal -->
    <SaveAsTemplateModal
      v-model="showSaveAsTemplateModal"
      :campaign="{ name: campaignData.name, campaign_name: campaignData.campaign_name, type: campaignData.type }"
      @saved="handleTemplateSaved"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FeatherIcon, Button, call } from 'frappe-ui'
import moment from 'moment'
import CampaignWizardHeader from '@/components/campaign/CampaignWizardHeader.vue'
import CampaignWizardStepper from '@/components/campaign/CampaignWizardStepper.vue'
import CampaignStep1 from '@/components/campaign_new/recruitment/Step1_CampaignInfo.vue'
import CampaignStep2 from '@/components/campaign_new/recruitment/Step2_ContentChannels.vue'
import CampaignStep3 from '@/components/campaign_new/recruitment/Step3_Settings.vue'
import { SaveAsTemplateModal } from '@/components/campaign'
import { useCampaignStore } from '@/stores/campaign'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  campaignType: {
    type: String,
    default: 'RECRUITMENT'
  },
  editCampaignId: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['close', 'success', 'campaign-created'])

// Composables
const campaignStore = useCampaignStore()
const toast = useToast()

// State
const currentStep = ref(1)
const saving = ref(false)
const finalizing = ref(false)
const savingAsTemplate = ref(false)
const showSaveAsTemplateModal = ref(false)
const showValidationError = ref(false)
const loadingTriggers = ref(false)

const campaignData = ref({
  campaign_name: '',
  description: '',
  campaign_tags: [],
  config_data: {},
  conditions: [],
  candidate_count: 0,
  channel: '',
  type: props.campaignType, // 'RECRUITMENT'
  status: 'Draft',
  start_date: null, // null = new campaign, datetime = edit mode
  // Landing page data
  ladipage_url: '',
  ladipage_id: '',
  company_info: {},
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

// Format steps for stepper component
const formattedSteps = computed(() => {
  return steps.value.map((step, index) => ({
    ...step,
    label: step.title,
    number: index + 1,
    completed: currentStep.value > index + 1,
    active: currentStep.value === index + 1
  }))
})

const canProceed = computed(() => {
  if (currentStep.value === 1) {
    // Step 1: Basic validation
    const hasBasicInfo = !!(
      campaignData.value.campaign_name?.trim()
    )
    
    return hasBasicInfo
  }
  
  if (currentStep.value === 2) {
    // Step 2: Content & Channels validation (simple like Attraction)
    return campaignData.value.selected_channels?.length > 0
  }
  
  if (currentStep.value === 3) {
    // Step 3: Settings & Triggers - optional validation
    // Triggers are optional, but if present, should be valid
    if (campaignData.value.triggers && campaignData.value.triggers.length > 0) {
      return campaignData.value.triggers.every(trigger => {
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
  campaignData.value.conditions = conditions
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
        description: campaignData.value.description,
        target_pool: targetPool,
        condition_filter: JSON.stringify(campaignData.value.conditions),
        type: campaignData.value.type,
        status: 'DRAFT',
        start_date: campaignData.value.start_date === 'SEND_NOW' ? moment().format('YYYY-MM-DDTHH:mm') : (campaignData.value.start_date || moment().format('YYYY-MM-DDTHH:mm'))
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
            description: campaignData.value.description,
            target_pool: targetPool,
            condition_filter: JSON.stringify(campaignData.value.conditions),
            start_date: campaignData.value.start_date === 'SEND_NOW' ? moment().format('YYYY-MM-DDTHH:mm') : (campaignData.value.start_date || moment().format('YYYY-MM-DDTHH:mm'))
          }
        })
        console.log('✅ Campaign info updated')
      } catch (error) {
        console.error('❌ Error updating campaign info:', error)
        toast.error(__('Failed to update campaign info'))
        return
      }
    }

    // Step 2: Save social posts if on step 2
    if (currentStep.value === 2 && campaignData.value.selected_channels.length > 0) {
      await saveSocialPosts()
    }

    // Step 3: Save settings & actions
    if (currentStep.value === 3 && campaignData.value.name) {
      try {

        
        // Save step3 triggers separately if needed
        if (campaignData.value.triggers && campaignData.value.triggers.length > 0) {
          console.log('💾 Saving Step3 triggers:', campaignData.value.triggers)
          
          try {
            // Use same API as timeline triggers but with different trigger types
            const result = await call('mbw_mira.api.campaign_social.save_nurturing_campaign_triggers', {
              campaign_id: campaignData.value.name,
              triggers: campaignData.value.triggers
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
    console.log('📊 Step 3 triggers:', campaignData.value.triggers)

    // Step 2: Update campaign settings (start_date)


    // Step 3: Sync flows with event triggers (Step 3 only)
    try {
      console.log('🔄 Syncing flows with event triggers...')
      
      // Only sync Step 3 event triggers (Step 2 is content, not triggers)
      const eventTriggers = campaignData.value.triggers || []
      
      console.log('📊 Event triggers to sync:', eventTriggers)
      
      if (eventTriggers.length > 0) {
        const result = await call('mbw_mira.api.campaign_flow.sync_campaign_flows', {
          campaign_id: campaignData.value.name,
          triggers: eventTriggers
        })
        
        if (result && result.success) {
          console.log(`✅ Flows synced: ${result.created || 0} created, ${result.updated || 0} updated, ${result.deleted || 0} deleted`)
        }
      } else {
        console.log('📝 No event triggers to sync')
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
    console.log('📂 Loading recruitment campaign data:', campaignId)
    
    const result = await call('frappe.client.get', {
      doctype: 'Mira Campaign',
      name: campaignId
    })
    
    if (result) {
      // Parse config_data and conditions from JSON strings
      let configData = {}
      let conditions = []
      
      try {
        configData = result.config_data ? JSON.parse(result.config_data) : {}
      } catch (e) {
        console.warn('Failed to parse config_data:', e)
        configData = {}
      }
      
      // If target_pool exists but not in configData, set it
      if (result.target_pool && !configData.selectedSegment) {
        configData.selectedSegment = result.target_pool
      }
      
      try {
        conditions = result.condition_filter ? JSON.parse(result.condition_filter) : []
      } catch (e) {
        console.warn('Failed to parse condition_filter:', e)
        conditions = []
      }

      console.log('Campaign data loaded:', result)
      
      // Update campaign data
      campaignData.value = {
        name: result.name,
        campaign_name: result.campaign_name || '',
        objective: result.description || '',
        campaign_tags: [], // Will be loaded separately
        config_data: configData,
        conditions: conditions,
        candidate_count: result.candidate_count || 0,
        channel: result.channel || '',
        type: result.type || 'RECRUITMENT',
        status: result.status || 'DRAFT',
        start_date: result.start_date ? moment(result.start_date).format('YYYY-MM-DDTHH:mm') : null,
        // Landing page data
        ladipage_url: result.ladipage_url || '',
        ladipage_id: result.ladipage_id || '',
        company_info: result.company_info ? JSON.parse(result.company_info) : {},
        job_info: result.job_info ? JSON.parse(result.job_info) : {},
        // Step 2: Content & Channels (will be loaded from social posts)
        selected_channels: [],
        email_content: {
          email_subject: '',
          email_content: '',        // Legacy field
          block_content: '',        // EmailBuilder format
          template_content: '',     // HTML format
          mjml_content: '',         // MJML format
          attachments: [],
          sender_account: null,
          schedule_time: null
        },
        facebook_content: {
          content: '',
          image: null,
          page_id: null,
          schedule_time: null
        },
        zalo_content: {
          blocks: [
            {
              id: Date.now(),
              type: 'text',
              text_content: ''
            }
          ],
          oa_id: null,
          schedule_time: null
        },
        step3_triggers: [], // TODO: Load step3 triggers from backend
      }
      
      // Load campaign tags
      await loadCampaignTags(campaignId)
      
      // Load social posts
      await loadSocialPosts(campaignData.value.name)
      
      // Load flows (triggers) - TODO: Implement if needed
      await loadCampaignFlows(campaignData.value.name)
      
      console.log('✅ Campaign data loaded:', campaignData.value)
      
      // Save initial state after loading
      initialCampaignData.value = JSON.parse(JSON.stringify(campaignData.value))
    }
  } catch (error) {
    console.error('❌ Error loading campaign:', error)
    toast.error(__('Failed to load campaign data'))
  }
}

// Load existing social posts when editing campaign
const loadSocialPosts = async (campaignId) => {
  try {
    console.log('📂 Loading social posts for campaign:', campaignId)
    
    // Call API to get posts
    const result = await call('mbw_mira.api.campaign_social.get_campaign_social_posts', {
      campaign_id: campaignId
    })
    
    if (!result.success) {
      console.error('❌ Failed to load social posts:', result.message)
      return
    }
    
    const posts = result.data || []
    console.log('📋 Loaded social posts:', posts)
    
    // Store original posts for change detection
    originalPosts.value = {
      email: campaignData.value.email_content,
      facebook: campaignData.value.facebook_content,
      zalo: campaignData.value.zalo_content
    }
    
    // Map posts back to campaign data
    for (const post of posts) {
      if (post.platform === 'Email') {
        campaignData.value.email_content = {
          email_subject: post.subject || '',
          email_content: post.template_content || '',     // HTML format
          block_content: post.block_content || '',        // EmailBuilder format (primary for editing)
          template_content: post.template_content || '',  // HTML format
          mjml_content: post.mjml_content || '',          // MJML format
          attachments: [],
          sender_account: post.sender_account || null,
          schedule_time: post.post_schedule_time || null
        }
        if (!campaignData.value.selected_channels?.includes('email')) {
          campaignData.value.selected_channels = campaignData.value.selected_channels || []
          campaignData.value.selected_channels.push('email')
        }
      } else if (post.platform === 'Facebook') {
        campaignData.value.facebook_content = {
          content: post.template_content || '',
          image: post.social_media_images || null,
          page_id: post.social_page_id || null,
          schedule_time: post.post_schedule_time || null
        }
        if (!campaignData.value.selected_channels?.includes('facebook')) {
          campaignData.value.selected_channels = campaignData.value.selected_channels || []
          campaignData.value.selected_channels.push('facebook')
        }
      } else if (post.platform === 'Zalo') {
        try {
          const content = JSON.parse(post.template_content || '{}')
          campaignData.value.zalo_content = {
            blocks: content.blocks || [
              {
                id: Date.now(),
                type: 'text',
                text_content: ''
              }
            ],
            oa_id: post.social_oa_id || null,
            schedule_time: post.post_schedule_time || null
          }
          if (!campaignData.value.selected_channels?.includes('zalo')) {
            campaignData.value.selected_channels = campaignData.value.selected_channels || []
            campaignData.value.selected_channels.push('zalo')
          }
        } catch (e) {
          console.error('❌ Error parsing zalo content:', e)
        }
      }
    }
    
    console.log('✅ Social posts loaded into campaign data')
    console.log('📊 Selected channels:', campaignData.value.selected_channels)
    console.log('📧 Email content:', campaignData.value.email_content)
    console.log('📘 Facebook content:', campaignData.value.facebook_content)
    console.log('💬 Zalo content:', campaignData.value.zalo_content)
  } catch (error) {
    console.error('❌ Error loading social posts:', error)
  }
}

// Reset campaign data
// Track original posts to detect changes
const originalPosts = ref({})

const saveSocialPosts = async () => {
  try {
    console.log('🔄 Saving Social Posts...')
    console.log('📊 Campaign Data:', campaignData.value)
    
    const socialPosts = []
    
    // Email post (for recruitment)
    if (campaignData.value.selected_channels.includes('email')) {
      const emailContent = campaignData.value.email_content
      
      socialPosts.push({
        platform: 'Email',
        subject: emailContent.email_subject || '',
        template_content: emailContent.template_content || emailContent.email_content || '',  // HTML format
        block_content: emailContent.block_content || '',        // EmailBuilder format
        mjml_content: emailContent.mjml_content || '',          // MJML format
        sender_account: emailContent.sender_account || null,
        status: 'Pending',
        post_schedule_time: emailContent.schedule_time || null
      })
    }
    
    // Facebook post
    if (campaignData.value.selected_channels.includes('facebook')) {
      const fbContent = campaignData.value.facebook_content
      
      socialPosts.push({
        platform: 'Facebook',
        social_page_id: fbContent.page_id,
        template_content: fbContent.content,
        social_media_images: fbContent.image,
        status: 'Pending',
        post_schedule_time: fbContent.schedule_time || null
      })
    }
    
    // Zalo post
    if (campaignData.value.selected_channels.includes('zalo')) {
      const zaloContent = campaignData.value.zalo_content
      
      socialPosts.push({
        platform: 'Zalo',
        social_oa_id: zaloContent.oa_id,
        template_content: JSON.stringify({
          blocks: zaloContent.blocks
        }),
        status: 'Pending',
        post_schedule_time: zaloContent.schedule_time || null
      })
    }
    
    console.log('📋 Social posts to save:', socialPosts)

    // Call API to save posts
    const result = await call('mbw_mira.api.campaign_social.save_campaign_social_posts', {
      campaign_id: campaignData.value.name,
      posts: socialPosts
    })

    if (result.success) {
      console.log('✅ Social posts saved:', result.data)
      toast.success(__('Social posts saved successfully'))
      
      // Update original posts after successful save
      originalPosts.value = {
        email: campaignData.value.email_content,
        facebook: campaignData.value.facebook_content,
        zalo: campaignData.value.zalo_content
      }
      
      return result.data
    } else {
      console.error('❌ Failed to save social posts:', result.message)
      toast.error(result.message || __('Failed to save social posts'))
      throw new Error(result.message)
    }
  } catch (error) {
    console.error('❌ Error saving social posts:', error)
    toast.error(__('An error occurred while saving social posts'))
    throw error
  }
}

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
    start_date: null, // null = new campaign, datetime = edit mode
    // Step 2: Content & Channels
    selected_channels: [],
    email_content: {
      email_subject: '',
      email_content: '',        // Legacy field
      block_content: '',        // EmailBuilder format
      template_content: '',     // HTML format
      mjml_content: '',         // MJML format
      attachments: [],
      sender_account: null,
      schedule_time: null
    },
    facebook_content: {
      content: '',
      image: null,
      page_id: null,
      schedule_time: null
    },
    zalo_content: {
      blocks: [
        {
          id: Date.now(),
          type: 'text',
          text_content: ''
        }
      ],
      oa_id: null,
      schedule_time: null
    },
    step3_triggers: []
  }
  currentStep.value = 1
}

// Handle step click from stepper
const handleStepClick = (stepNumber) => {
  if (stepNumber <= currentStep.value) {
    currentStep.value = stepNumber
    showValidationError.value = false
  }
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

// Load campaign flows and convert to triggers
const loadCampaignFlows = async (campaignId) => {
  try {
    console.log('🔀 Loading flows for campaign:', campaignId)
    
    const result = await call('mbw_mira.api.campaign_flow.get_campaign_flows', {
      campaign_id: campaignId
    })
    
    if (result.success && result.data) {
      campaignData.value.triggers = result.data
      console.log('✅ Loaded triggers from flows:', result.data)
      console.log('📊 Triggers detail:', JSON.stringify(result.data, null, 2))
    } else {
      console.log('ℹ️ No flows found for campaign')
      campaignData.value.triggers = []
    }
  } catch (error) {
    console.error('❌ Error loading flows:', error)
    campaignData.value.triggers = []
  }
}

// Watch for step changes to load flows
watch(currentStep, async (newStep, oldStep) => {
  if (newStep === 3 && oldStep !== 3 && campaignData.value.name) {
    await loadCampaignFlows(campaignData.value.name)
  }
})

const handleSaveAsTemplate = () => {
  if (!campaignData.value.name) {
    toast.error(__('Please save the campaign first'))
    return
  }
  showSaveAsTemplateModal.value = true
}

const handleTemplateSaved = (templateData) => {
  toast.success(__('Campaign saved as template successfully!'))
  console.log('✅ Template created:', templateData)
  showSaveAsTemplateModal.value = false
}

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
