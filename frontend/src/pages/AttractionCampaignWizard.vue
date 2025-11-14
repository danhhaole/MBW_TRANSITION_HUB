<template>
  <div v-if="show" class="fixed inset-0 bg-white z-[9] flex flex-col">
    <!-- Header - Reuse existing component -->
    <CampaignWizardHeader
      :campaign-name="campaignData.campaign_name || __('New Attraction Campaign')"
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
          :description="campaignData.description"
          :target-pool="campaignData.target_pool"
          :campaign-id="campaignData.name"
          :campaign-tags="campaignData.campaign_tags"
          :start-date="campaignData.start_date"
          :show-error="showValidationError"
          @update:campaign-name="campaignData.campaign_name = $event"
          @update:description="campaignData.description = $event"
          @update:target-pool="campaignData.target_pool = $event"
          @update:campaign-tags="campaignData.campaign_tags = $event"
          @update:start-date="campaignData.start_date = $event"
        />

        <!-- Step 2: Content & Channels -->
        <CampaignStep2
          v-else-if="currentStep === 2"
          :selected-channels="campaignData.selected_channels"
          :facebook-content="campaignData.facebook_content"
          :zalo-content="campaignData.zalo_content"
          :qr-content="campaignData.qr_content"
          :ladipage-url="campaignData.ladipage_url"
          :ladipage-id="campaignData.ladipage_id"
          :page-data="campaignData.page_data"
          :campaign-name="campaignData.campaign_name"
          :name="campaignData.name"
          :show-error="showValidationError"
          @update:selected-channels="campaignData.selected_channels = $event"
          @update:facebook-content="campaignData.facebook_content = $event"
          @update:zalo-content="campaignData.zalo_content = $event"
          @update:qr-content="campaignData.qr_content = $event"
          @update:landing-page="campaignData.landing_page = $event"
          @update:page-data="campaignData.page_data = $event"
          @update:ladipage-url="campaignData.ladipage_url = $event"
          @update:ladipage-id="campaignData.ladipage_id = $event"
        />

        <!-- Step 3: Settings -->
        <CampaignStep3
          v-else-if="currentStep === 3"
          :triggers="campaignData.triggers"
          :start-date="campaignData.start_date"
          :show-error="showValidationError"
          @update:triggers="campaignData.triggers = $event"
          @update:start-date="campaignData.start_date = $event"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { call } from 'frappe-ui'
import CampaignWizardHeader from '@/components/campaign/CampaignWizardHeader.vue'
import CampaignWizardStepper from '@/components/campaign/CampaignWizardStepper.vue'
import CampaignStep1 from '@/components/campaign_new/attraction/Step1_CampaignInfo.vue'
import CampaignStep2 from '@/components/campaign_new/attraction/Step2_ContentChannels.vue'
import CampaignStep3 from '@/components/campaign_new/attraction/Step3_Settings.vue'
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
    default: 'ATTRACTION'
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
const showValidationError = ref(false)

const campaignData = ref({
  campaign_name: '',
  description: '',
  target_pool: '',
  campaign_tags: [],
  start_date: '', // Let CampaignSchedule handle default behavior
  // Step 2: Content & Channels
  selected_channels: [],
  landing_page: '',
  page_data: null,
  ladipage_url: '',
  ladipage_id: '',
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
    schedule_time: null
  },
  qr_content: {
    utm_campaign: '',
    utm_source: 'qr_code',
    utm_medium: 'qr',
    qr_data: null
  },
  // Step 3: Settings
  triggers: [],
  // Meta
  type: props.campaignType, // 'ATTRACTION'
  status: 'Draft',
  flow_id: null // Will be set after creating Mira Flow
})

// Steps configuration
const steps = ref([
  { title: __('Campaign Info'), key: 'info' },
  { title: __('Content & Channels'), key: 'content' },
  { title: __('Settings'), key: 'settings' }
])

const totalSteps = computed(() => steps.value.length)

// Format steps for CampaignWizardStepper component
const formattedSteps = computed(() => {
  return steps.value.map((step, index) => ({
    number: index + 1,
    label: step.title,
    key: step.key
  }))
})

const isLastStep = computed(() => currentStep.value === totalSteps.value)

// Validation computed
const canProceed = computed(() => {
  if (currentStep.value === 1) {
    return campaignData.value.campaign_name?.trim()
  }
  if (currentStep.value === 2) {
    const result = campaignData.value.selected_channels?.length > 0
    console.log('🔍 canProceed step 2:', result, 'channels:', campaignData.value.selected_channels)
    return result
  }
  return true
})

// Methods
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
  
  // Check if posts changed before saving (only on step 2)
  if (currentStep.value === 2) {
    // Only include content for selected channels
    const currentPosts = {}
    const selectedChannels = campaignData.value.selected_channels || []
    
    if (selectedChannels.includes('facebook')) {
      currentPosts.facebook = campaignData.value.facebook_content
    }
    if (selectedChannels.includes('zalo')) {
      currentPosts.zalo = campaignData.value.zalo_content
    }
    if (selectedChannels.includes('qr_code')) {
      currentPosts.qr_code = campaignData.value.qr_content
    }
    
    console.log('🔍 Change detection:')
    console.log('  Selected channels:', selectedChannels)
    console.log('  Current posts:', currentPosts)
    console.log('  Original posts:', originalPosts.value)
    
    const hasChanges = JSON.stringify(currentPosts) !== JSON.stringify(originalPosts.value)
    console.log('  Has changes:', hasChanges)
    
    if (hasChanges) {
      console.log('📝 Posts changed, saving...')
      await saveDraft()
    } else {
      console.log('⏭️ No changes in posts, skipping save')
    }
  } else {
    // Save draft for other steps
    await saveDraft()
  }
  
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
      const result = await campaignStore.submitNewCampaign({
        campaign_name: campaignData.value.campaign_name,
        description: campaignData.value.description,
        target_pool: campaignData.value.target_pool,
        start_date: campaignData.value.start_date === 'SEND_NOW' ? moment().format('YYYY-MM-DDTHH:mm') : (campaignData.value.start_date || moment().format('YYYY-MM-DDTHH:mm')),
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
        await call('frappe.client.set_value', {
          doctype: 'Mira Campaign',
          name: campaignData.value.name,
          fieldname: {
            campaign_name: campaignData.value.campaign_name,
            description: campaignData.value.description,
            target_pool: campaignData.value.target_pool,
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

    // Don't show toast for auto-save
  } catch (error) {
    console.error('Error saving draft:', error)
    toast.error(__('An error occurred while saving'))
  } finally {
    saving.value = false
  }
}

// Track original posts to detect changes
const originalPosts = ref({})

// Watch selected channels and update original posts accordingly
watch(() => campaignData.value.selected_channels, (newChannels) => {
  console.log('🔄 Selected channels changed:', newChannels)
  
  // Update original posts to only include selected channels
  const newOriginalPosts = {}
  
  if (newChannels.includes('facebook')) {
    newOriginalPosts.facebook = originalPosts.value.facebook || campaignData.value.facebook_content
  }
  if (newChannels.includes('zalo')) {
    newOriginalPosts.zalo = originalPosts.value.zalo || campaignData.value.zalo_content
  }
  if (newChannels.includes('qr_code')) {
    newOriginalPosts.qr_code = originalPosts.value.qr_code || campaignData.value.qr_content
  }
  
  originalPosts.value = newOriginalPosts
  console.log('📝 Updated original posts:', originalPosts.value)
}, { deep: true })

const saveSocialPosts = async () => {
  try {
    console.log('🔄 Saving Social Posts...')
    console.log('📊 Campaign Data:', campaignData.value)
    
    const socialPosts = []
    
    // Facebook post
    if (campaignData.value.selected_channels.includes('facebook')) {
      const fbContent = campaignData.value.facebook_content
      
      socialPosts.push({
        platform: 'Facebook',
        social_page_id: fbContent.page_id,
        social_page_name: getPageName(fbContent.page_id),
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
        template_content: JSON.stringify({
          blocks: zaloContent.blocks
        }),
        status: 'Pending',
        post_schedule_time: zaloContent.schedule_time || null
      })
    }
    
    // QR Code post
    if (campaignData.value.selected_channels.includes('qr_code')) {
      const qrContent = campaignData.value.qr_content
      
      socialPosts.push({
        platform: 'QR',
        template_content: JSON.stringify({
          utm_campaign: qrContent.utm_campaign,
          utm_source: qrContent.utm_source,
          utm_medium: qrContent.utm_medium,
          qr_data: qrContent.qr_data
        }),
        status: 'Pending',
        post_schedule_time: null // QR codes don't have schedule time
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
        facebook: campaignData.value.facebook_content,
        zalo: campaignData.value.zalo_content,
        qr_code: campaignData.value.qr_content
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

// Helper function to get page name
const getPageName = (pageId) => {
  // TODO: Get from actual page options when available
  return pageId ? `Page ${pageId}` : 'Unknown Page'
}

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
    } else {
      console.log('ℹ️ No flows found for campaign')
      campaignData.value.triggers = []
    }
  } catch (error) {
    console.error('❌ Error loading flows:', error)
    campaignData.value.triggers = []
  }
}

const loadCampaignTags = async (campaignId) => {
  try {
    console.log('🏷️ Loading campaign tags:', campaignId)
    
    // Get tags from Frappe's tag system
    const response = await call('frappe.desk.doctype.tag.tag.get_tags', {
      doctype: 'Mira Campaign',
      txt: campaignId
    })
    
    if (response && Array.isArray(response)) {
      // Get tag colors from Mira Tag doctype
      const tagTitles = response.map(tag => tag.tag || tag)
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
      campaignData.value.campaign_tags = response.map(tag => {
        const tagTitle = tag.tag || tag
        return {
          label: tagTitle,
          value: tagTitle,
          color: colorMap[tagTitle] || '#6B7280'
        }
      })
      
      console.log('✅ Campaign tags loaded:', campaignData.value.campaign_tags)
    }
  } catch (error) {
    console.error('❌ Error loading campaign tags:', error)
    // Don't show error toast as tags are optional
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
      facebook: campaignData.value.facebook_content,
      zalo: campaignData.value.zalo_content,
      qr_code: campaignData.value.qr_content
    }
    
    // Map posts back to campaign data
    for (const post of posts) {
      if (post.platform === 'Facebook') {
        campaignData.value.facebook_content = {
          content: post.template_content || '',
          image: post.social_media_images || null,
          page_id: post.social_page_id || null,
          schedule_time: post.post_schedule_time || null
        }
        if (!campaignData.value.selected_channels.includes('facebook')) {
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
            schedule_time: post.post_schedule_time || null
          }
        } catch (e) {
          campaignData.value.zalo_content = {
            blocks: [
              {
                id: Date.now(),
                type: 'text',
                text_content: post.template_content || ''
              }
            ],
            schedule_time: post.post_schedule_time || null
          }
        }
        if (!campaignData.value.selected_channels.includes('zalo')) {
          campaignData.value.selected_channels.push('zalo')
        }
      } else if (post.platform === 'QR') {
        try {
          const content = JSON.parse(post.template_content || '{}')
          campaignData.value.qr_content = {
            utm_campaign: content.utm_campaign || '',
            utm_source: content.utm_source || 'qr_code',
            utm_medium: content.utm_medium || 'qr',
            qr_data: content.qr_data || null
          }
        } catch (e) {
          campaignData.value.qr_content = {
            utm_campaign: '',
            utm_source: 'qr_code',
            utm_medium: 'qr',
            qr_data: null
          }
        }
        if (!campaignData.value.selected_channels.includes('qr_code')) {
          campaignData.value.selected_channels.push('qr_code')
        }
      }
    }
    
    console.log('✅ Social posts loaded into campaign data')
    console.log('📊 Selected channels:', campaignData.value.selected_channels)
    console.log('📘 Facebook content:', campaignData.value.facebook_content)
    console.log('💬 Zalo content:', campaignData.value.zalo_content)
    console.log('📱 QR content:', campaignData.value.qr_content)
  } catch (error) {
    console.error('❌ Error loading social posts:', error)
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
      
      const result = await call('mbw_mira.api.campaign_flow.sync_campaign_flows', {
        campaign_id: campaignData.value.name,
        triggers: campaignData.value.triggers || []
      })
      
      if (result && result.success) {
        console.log(`✅ Flows synced: ${result.created || 0} created, ${result.updated || 0} updated, ${result.deleted || 0} deleted`)
      }
    } catch (error) {
      console.error('❌ Error syncing flows:', error)
    }

    // Step 3: Reload campaign data to get updated flow status
    await loadCampaignData(campaignData.value.name)
    
    // Step 4: Campaign finalized - Reset wizard
    toast.success(__('Campaign saved successfully!'))
    console.log('✅ Campaign finalized')
    
    // Reset wizard to step 1
    currentStep.value = 1
    resetCampaignData()
    
    emit('success', { name: campaignData.value.name })
    emit('close')
  } catch (error) {
    console.error('Error activating campaign:', error)
    toast.error(__('An error occurred while activating campaign'))
  } finally {
    finalizing.value = false
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
  }
})


const loadCampaignData = async (campaignId) => {
  try {
    console.log('📂 Loading campaign data:', campaignId)
    
    const result = await campaignStore.fetchCampaignById(campaignId)
    if (result.success && result.data) {
      const campaign = result.data
      
      // Map campaign data to form structure
      campaignData.value = {
        name: campaign.name,
        campaign_name: campaign.campaign_name || '',
        description: campaign.description || '',
        target_pool: campaign.target_pool || '',
        campaign_tags: [], // Will be loaded from tags
        // Step 2: Content & Channels (will be loaded from social posts)
        selected_channels: [],
        landing_page: '',
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
          schedule_time: null
        },
        // Meta
        type: campaign.type || props.campaignType,
        status: campaign.status || 'Draft',
        start_date: campaign.start_date ? moment(campaign.start_date).format('YYYY-MM-DDTHH:mm') : null,
        flow_id: campaign.flow_id || null,
        ladipage_url: campaign.ladipage_url || '',
        ladipage_id: campaign.ladipage_id || '',
      }
      
      console.log('✅ Campaign data loaded:', campaignData.value)
      
      // Load campaign tags
      await loadCampaignTags(campaignId)
      
      // Load social posts
      await loadSocialPosts(campaignId)
      
      // Load flows (triggers)
      await loadCampaignFlows(campaignId)
    }
  } catch (error) {
    console.error('❌ Error loading campaign:', error)
    toast.error(__('Failed to load campaign data'))
  }
}

const resetCampaignData = () => {
  campaignData.value = {
    campaign_name: '',
    description: '',
    target_pool: '',
    campaign_tags: [],
    start_date: '', // Let CampaignSchedule handle default behavior
    // Step 2: Content & Channels
    selected_channels: [],
    ladipage_url: '',
    ladipage_id: '',
    facebook_content: {
      content: '',
      image: null,
      page_id: null
    },
    zalo_content: {
      content: '',
      image: null
    },
    // Meta
    type: props.campaignType, // 'ATTRACTION'
    status: 'Draft',
    flow_id: null
  }
  currentStep.value = 1
  showValidationError.value = false
}

// Handle step click from stepper
const handleStepClick = (stepNumber) => {
  if (stepNumber <= currentStep.value) {
    currentStep.value = stepNumber
  }
}

// Translation helper

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
