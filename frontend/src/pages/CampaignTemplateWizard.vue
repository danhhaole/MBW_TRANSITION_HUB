<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-full mx-5 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Left: Back button and Title -->
          <div class="flex items-center space-x-4">
            <Button variant="ghost" @click="handleBack">
              <template #prefix>
                <FeatherIcon name="arrow-left" class="h-4 w-4" />
              </template>
              {{ __('Back') }}
            </Button>
            
            <div class="h-8 w-px bg-gray-300"></div>
            
            <div>
              <h1 class="text-xl font-semibold text-gray-900">
                {{ isEditMode ? __('Edit Campaign Template') : __('Create Campaign Template') }}
              </h1>
              <p class="text-sm text-gray-500">
                {{ __('Step {0} of {1}', [currentStep, totalSteps]) }}
              </p>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="flex items-center space-x-3">
            <!-- Save Draft Button -->
            <Button 
              v-if="templateData.name && templateData.name !== 'template'"
              variant="outline" 
              @click="saveDraft" 
              :loading="saving"
            >
              {{ __('Save Draft') }}
            </Button>
            
            <Button v-if="currentStep > 1" variant="outline" @click="prevStep">
              {{ __('Previous') }}
            </Button>
            
            <Button v-if="currentStep < totalSteps" theme="blue" @click="nextStep" :disabled="!canProceed">
              {{ __('Save & Continue') }}
            </Button>
            
            <Button v-else theme="blue" @click="finalizeTemplate" :loading="finalizing">
              {{ isEditMode ? __('Update Template') : __('Create Template') }}
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-full mx-5 px-4 sm:px-6 lg:px-8">
        <div class="py-4">
          <div class="flex items-center justify-between mb-2">
            <div class="flex space-x-4">
              <div 
                v-for="(step, index) in steps" 
                :key="step.id"
                class="flex items-center cursor-pointer"
                @click="handleStepClick(index + 1)"
              >
                <div 
                  :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors',
                    currentStep > index + 1 
                      ? 'bg-green-500 text-white hover:bg-green-600' 
                      : currentStep === index + 1 
                        ? 'bg-blue-500 text-white' 
                        : 'bg-gray-200 text-gray-500 hover:bg-gray-300'
                  ]"
                >
                  <FeatherIcon 
                    v-if="currentStep > index + 1" 
                    name="check" 
                    class="w-4 h-4" 
                  />
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <span 
                  :class="[
                    'ml-2 text-sm font-medium transition-colors',
                    currentStep >= index + 1 ? 'text-gray-900 hover:text-blue-600' : 'text-gray-500'
                  ]"
                >
                  {{ step.title }}
                </span>
                <FeatherIcon 
                  v-if="index < steps.length - 1" 
                  name="chevron-right" 
                  class="w-4 h-4 mx-4 text-gray-400" 
                />
              </div>
            </div>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-500 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Area -->
    <div class="flex-1 overflow-y-auto">
      <div class="max-w-4xl mx-auto px-6 py-8">
        
        <!-- Loading State -->
        <div v-if="loading" class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600">{{ __('Loading template...') }}</span>
        </div>
        
        <!-- Step 1: Template Information -->
        <div v-else-if="currentStep === 1" class="space-y-6">
          <!-- Quick Templates -->
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-6">{{ __('Choose Template Type') }}</h2>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div 
                v-for="quickTemplate in quickTemplates" 
                :key="quickTemplate.id"
                @click="selectQuickTemplate(quickTemplate)"
                :class="[
                  'border-2 rounded-lg p-4 cursor-pointer transition-all',
                  selectedQuickTemplate?.id === quickTemplate.id 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                ]"
              >
                <div class="flex items-center mb-3">
                  <div :class="['w-10 h-10 rounded-lg flex items-center justify-center', quickTemplate.color]">
                    <FeatherIcon :name="quickTemplate.icon" class="w-5 h-5 text-white" />
                  </div>
                  <div class="ml-3">
                    <h4 class="text-sm font-medium text-gray-900">{{ quickTemplate.name }}</h4>
                    <p class="text-xs text-gray-500">{{ quickTemplate.type }}</p>
                  </div>
                </div>
                <p class="text-xs text-gray-600">{{ quickTemplate.description }}</p>
              </div>
            </div>
          </div>

          <!-- Template Step 1 Component -->
          <TemplateStep1
            :template-name="templateData.template_name"
            :template-description="templateData.template_description"
            :campaign-type="templateData.campaign_type"
            :campaign-name="templateData.campaign_name"
            :description="templateData.objective"
            :target-pool="templateData.target_pool"
            :config-data="templateData.config_data"
            :conditions="templateData.conditions"
            :candidate-count="templateData.candidate_count"
            :campaign-tags="templateData.campaign_tags"
            :scope-type="templateData.scope_type"
            :is-default="templateData.is_default"
            :is-premium="templateData.is_premium"
            :is-suggestion="templateData.is_suggestion"
            :show-error="false"
            @update:template-name="templateData.template_name = $event; if (!templateData.campaign_name) templateData.campaign_name = $event"
            @update:template-description="templateData.template_description = $event"
            @update:campaign-type="templateData.campaign_type = $event; onCampaignTypeChange()"
            @update:campaign-name="templateData.campaign_name = $event"
            @update:description="templateData.objective = $event"
            @update:target-pool="templateData.target_pool = $event"
            @update:config-data="templateData.config_data = $event"
            @update:conditions="templateData.conditions = $event"
            @update:candidate-count="templateData.candidate_count = $event"
            @update:campaign-tags="templateData.campaign_tags = $event"
            @update:scope-type="templateData.scope_type = $event; console.log('🔧 Scope type updated:', $event)"
            @update:is-default="templateData.is_default = $event"
            @update:is-premium="templateData.is_premium = $event"
            @update:is-suggestion="templateData.is_suggestion = $event"
          />
        </div>

        <!-- Step 2: Content Templates -->
        <div v-else-if="currentStep === 2" class="space-y-6">
          
          <!-- ATTRACTION Content -->
          <AttractionStep2
            v-if="templateData.campaign_type === 'ATTRACTION'"
            :selected-channels="templateData.selected_channels"
            :facebook-content="templateData.facebook_content"
            :zalo-content="templateData.zalo_content"
            :campaign-name="templateData.campaign_name"
            :name="templateData.name"
            :ladipage-url="templateData.ladipage_url"
            :ladipage-id="templateData.ladipage_id"
            :show-error="false"
            doctype="Mira Campaign Template"
            @update:selected-channels="templateData.selected_channels = $event"
            @update:facebook-content="templateData.facebook_content = $event"
            @update:zalo-content="templateData.zalo_content = $event"
            @update:ladipage-url="templateData.ladipage_url = $event"
            @update:ladipage-id="templateData.ladipage_id = $event"
          />

          <!-- NURTURING Content -->
          <NurturingStep2
            v-else-if="templateData.campaign_type === 'NURTURING'"
            :triggers="templateData.triggers"
            :campaign-name="templateData.campaign_name"
            :name="templateData.name"
            :ladipage-url="templateData.ladipage_url"
            :ladipage-id="templateData.ladipage_id"
            doctype="Mira Campaign Template"
            @update:triggers="templateData.triggers = $event"
            @update:ladipage-url="templateData.ladipage_url = $event"
            @update:ladipage-id="templateData.ladipage_id = $event"
          />

          <!-- RECRUITMENT Content -->
          <RecruitmentStep2
            v-else-if="templateData.campaign_type === 'RECRUITMENT'"
            :selected-channels="templateData.selected_channels"
            :email-content="templateData.email_content"
            :facebook-content="templateData.facebook_content"
            :zalo-content="templateData.zalo_content"
            :campaign-name="templateData.campaign_name"
            :name="templateData.name"
            :ladipage-url="templateData.ladipage_url"
            :ladipage-id="templateData.ladipage_id"
            :show-error="false"
            doctype="Mira Campaign Template"
            @update:selected-channels="templateData.selected_channels = $event"
            @update:email-content="templateData.email_content = $event"
            @update:facebook-content="templateData.facebook_content = $event"
            @update:zalo-content="templateData.zalo_content = $event"
            @update:ladipage-url="templateData.ladipage_url = $event"
            @update:ladipage-id="templateData.ladipage_id = $event"
          />
        </div>

        <!-- Step 3: Settings & Triggers -->
        <div v-else-if="currentStep === 3" class="space-y-6">
          
          <!-- ATTRACTION Settings -->
          <AttractionStep3
            v-if="templateData.campaign_type === 'ATTRACTION'"
            :start-date="templateData.start_date"
            :triggers="templateData.step3_triggers"
            @update:start-date="templateData.start_date = $event"
            @update:triggers="templateData.step3_triggers = $event"
          />

          <!-- NURTURING Settings -->
          <NurturingStep3
            v-else-if="templateData.campaign_type === 'NURTURING'"
            :start-date="templateData.start_date"
            :triggers="templateData.step3_triggers"
            @update:start-date="templateData.start_date = $event"
            @update:triggers="templateData.step3_triggers = $event"
          />

          <!-- RECRUITMENT Settings -->
          <RecruitmentStep3
            v-else-if="templateData.campaign_type === 'RECRUITMENT'"
            :start-date="templateData.start_date"
            :triggers="templateData.step3_triggers"
            @update:start-date="templateData.start_date = $event"
            @update:triggers="templateData.step3_triggers = $event"
          />
        </div>


      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Button, FormControl, Select, FeatherIcon, call } from 'frappe-ui'
import { useCampaignTemplateStore } from '@/stores/campaignTemplate'
import { useToast } from '@/composables/useToast'
import Link from '@/components/Controls/Link.vue'

// Import template components
import TemplateStep1 from '@/components/campaign_template/TemplateStep1.vue'

// Import Step2 components (original)
import AttractionStep2 from '@/components/campaign_new/attraction/Step2_ContentChannels.vue'
import RecruitmentStep2 from '@/components/campaign_new/recruitment/Step2_ContentChannels.vue'
import NurturingStep2 from '@/components/campaign_new/nurturing/Step2_ContentTimeline.vue'

// Import Step3 components (original)
import AttractionStep3 from '@/components/campaign_new/attraction/Step3_Settings.vue'
import RecruitmentStep3 from '@/components/campaign_new/recruitment/Step3_Settings.vue'
import NurturingStep3 from '@/components/campaign_new/nurturing/Step3_Settings.vue'


// Composables
const router = useRouter()
const route = useRoute()
const templateStore = useCampaignTemplateStore()
const toast = useToast()

// Reactive state
const currentStep = ref(1)
const totalSteps = 3
const loading = ref(false)
const saving = ref(false)
const finalizing = ref(false)
const selectedQuickTemplate = ref(null)
const hasUnsavedChanges = ref(false)

// Template data
const templateData = ref({
  // Basic Info
  template_name: '',
  template_description: '',
  campaign_type: 'ATTRACTION',
  campaign_name: '', // for CampaignBasicInfo
  name: 'template', // campaign ID for components
  objective: '',
  campaign_tags: [],
  
  // ATTRACTION specific
  target_pool: '',
  
  // NURTURING & RECRUITMENT specific
  config_data: {},
  conditions: [],
  candidate_count: 0,
  
  // Schedule
  start_date: null,
  
  // Step 2 Content & Channels - for components
  selected_channels: [],
  facebook_content: {},
  zalo_content: {},
  email_content: {},
  
  // Landing Page
  ladipage_url: '',
  ladipage_id: '',
  
  // Step 2 Triggers (for NURTURING)
  triggers: [],
  
  // Step 3 Triggers & Settings
  step3_triggers: [],
  is_premium: false,
  is_suggestion: false,
  is_default: false,
  start_date_strategy: 'immediate',
  scope_type: 'PUBLIC'
})

// Steps
const steps = [
  { id: 1, title: __('Template Info') },
  { id: 2, title: __('Content') },
  { id: 3, title: __('Settings') }
]

// Quick Templates
const quickTemplates = [
  {
    id: 'attraction_social',
    name: __('Social Media Attraction'),
    type: 'ATTRACTION',
    description: __('Ready-to-use social media posts for attracting candidates'),
    icon: 'users',
    color: 'bg-blue-500',
    channels: ['facebook', 'zalo'],
    content: {
      facebook: '🚀 Join our amazing team! We\'re looking for talented individuals...',
      zalo: 'Chào bạn! 👋 Chúng tôi đang tìm kiếm những tài năng xuất sắc...'
    }
  },
  {
    id: 'nurturing_email',
    name: __('Email Nurturing'),
    type: 'NURTURING',
    description: __('Email sequences for nurturing candidate relationships'),
    icon: 'mail',
    color: 'bg-green-500',
    channels: ['email'],
    content: {
      email: 'Hi there! Thanks for your interest in our company...'
    }
  },
  {
    id: 'recruitment_direct',
    name: __('Direct Recruitment'),
    type: 'RECRUITMENT',
    description: __('Direct outreach templates for active recruitment'),
    icon: 'target',
    color: 'bg-purple-500',
    channels: ['email', 'zalo'],
    content: {
      email: 'We\'re actively hiring for [Position Name]!...',
      zalo: '🎯 Tuyển dụng vị trí [Tên vị trí]!...'
    }
  }
]

// Computed
const isEditMode = computed(() => !!route.params.id)

const campaignTypeOptions = [
  { label: __('Attraction'), value: 'ATTRACTION' },
  { label: __('Nurturing'), value: 'NURTURING' },
  { label: __('Recruitment'), value: 'RECRUITMENT' }
]

// Channel options by campaign type
const attractionChannels = [
  { label: __('Facebook'), value: 'facebook' },
  { label: __('Zalo'), value: 'zalo' },
  { label: __('QR Code'), value: 'qr' }
]

const nurturingChannels = [
  { label: __('Email'), value: 'email' },
  { label: __('SMS'), value: 'sms' },
  { label: __('Zalo'), value: 'zalo' }
]

const recruitmentChannels = [
  { label: __('Email'), value: 'email' },
  { label: __('Facebook'), value: 'facebook' },
  { label: __('Zalo'), value: 'zalo' }
]

// Other options
const startDateOptions = [
  { label: __('Immediate'), value: 'immediate' },
  { label: __('Next Business Day'), value: 'next_business_day' },
  { label: __('Custom Date'), value: 'custom' },
  { label: __('User Defined'), value: 'user_defined' }
]

const scopeOptions = [
  { label: __('Private'), value: 'PRIVATE' },
  { label: __('Team'), value: 'TEAM' },
  { label: __('Organization'), value: 'ORGANIZATION' },
  { label: __('Public'), value: 'PUBLIC' }
]

// Trigger Types
const nurturingTriggerTypes = [
  { label: __('Time Based'), value: 'time_based' },
  { label: __('Email Opened'), value: 'email_opened' },
  { label: __('Link Clicked'), value: 'link_clicked' },
  { label: __('Profile Updated'), value: 'profile_updated' }
]

const attractionTriggerTypes = [
  { label: __('Form Submitted'), value: 'form_submitted' },
  { label: __('Page Visited'), value: 'page_visited' },
  { label: __('QR Scanned'), value: 'qr_scanned' },
  { label: __('Social Engagement'), value: 'social_engagement' }
]

const recruitmentTriggerTypes = [
  { label: __('Application Submitted'), value: 'application_submitted' },
  { label: __('Interview Scheduled'), value: 'interview_scheduled' },
  { label: __('Assessment Completed'), value: 'assessment_completed' },
  { label: __('Reference Check'), value: 'reference_check' }
]

const nurturingStep3TriggerTypes = [
  { label: __('Engagement Score'), value: 'engagement_score' },
  { label: __('Inactivity Period'), value: 'inactivity_period' },
  { label: __('Job Match'), value: 'job_match' }
]

// Actions
const attractionActions = [
  { label: __('Send Welcome Email'), value: 'send_welcome_email' },
  { label: __('Add to Talent Pool'), value: 'add_to_talent_pool' },
  { label: __('Schedule Follow-up'), value: 'schedule_followup' }
]

const nurturingActions = [
  { label: __('Send Nurturing Email'), value: 'send_nurturing_email' },
  { label: __('Update Engagement Score'), value: 'update_engagement_score' },
  { label: __('Notify Recruiter'), value: 'notify_recruiter' }
]

const recruitmentActions = [
  { label: __('Send Interview Invite'), value: 'send_interview_invite' },
  { label: __('Update Application Status'), value: 'update_application_status' },
  { label: __('Send Assessment'), value: 'send_assessment' }
]

const jobStageOptions = [
  { label: __('Application'), value: 'application' },
  { label: __('Screening'), value: 'screening' },
  { label: __('Interview'), value: 'interview' },
  { label: __('Assessment'), value: 'assessment' },
  { label: __('Reference'), value: 'reference' },
  { label: __('Offer'), value: 'offer' }
]

const canProceed = computed(() => {
  if (currentStep.value === 1) {
    const hasBasicInfo = templateData.value.template_name && 
                        templateData.value.template_description &&
                        templateData.value.campaign_type &&
                        templateData.value.campaign_name &&
                        
                        templateData.value.scope_type
    
    console.log('🔍 Validation check:', {
      template_name: templateData.value.template_name,
      template_description: templateData.value.template_description,
      campaign_type: templateData.value.campaign_type,
      campaign_name: templateData.value.campaign_name,
      objective: templateData.value.objective,
      scope_type: templateData.value.scope_type,
      canProceed: hasBasicInfo
    })
    
    return hasBasicInfo
  }
  
  if (currentStep.value === 2) {
    // For templates, channels are optional
    return true
  }
  
  if (currentStep.value === 3) {
    return true
  }
  
  return false
})

const isLastStep = computed(() => currentStep.value === totalSteps)

// Debug validation
watch(() => [
  templateData.value.template_name,
  templateData.value.template_description, 
  templateData.value.campaign_name,
  templateData.value.objective,
  templateData.value.scope_type
], () => {
  console.log('📊 Template data changed:', {
    template_name: templateData.value.template_name,
    template_description: templateData.value.template_description,
    campaign_name: templateData.value.campaign_name,
    objective: templateData.value.objective,
    scope_type: templateData.value.scope_type,
    canProceed: canProceed.value
  })
}, { immediate: true })

// Methods
const nextStep = async () => {
  if (!canProceed.value) return
  
  // Auto-save before proceeding to next step
  if (hasUnsavedChanges.value) {
    console.log('📝 Changes detected, saving before next step...')
    await saveDraft()
  } else {
    console.log('⏭️ No changes detected, skipping save')
  }
  
  if (currentStep.value < totalSteps) {
    currentStep.value++
  } else if (isLastStep.value) {
    // Finalize template on last step
    await finalizeTemplate()
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const handleStepClick = async (stepNumber) => {
  if (stepNumber <= currentStep.value) {
    // Allow going back to previous steps
    currentStep.value = stepNumber
  } else if (stepNumber === currentStep.value + 1 && canProceed.value) {
    // Allow going to next step if current step is valid
    await nextStep()
  }
}

const selectQuickTemplate = (quickTemplate) => {
  selectedQuickTemplate.value = quickTemplate
  templateData.value.template_name = quickTemplate.name
  templateData.value.campaign_name = quickTemplate.name
  templateData.value.campaign_type = quickTemplate.type
  // Don't auto-add channels - let user choose
  templateData.value.selected_channels = []
  
  // Reset content - let user add channels and content manually
  templateData.value.facebook_content = {}
  templateData.value.zalo_content = {}
  templateData.value.email_content = {}
}

const getContentPlaceholder = (channel) => {
  const placeholders = {
    facebook: 'Enter your Facebook post content...',
    zalo: 'Nhập nội dung tin nhắn Zalo...',
    email: 'Enter your email content...',
    sms: 'Enter your SMS content...'
  }
  return placeholders[channel] || 'Enter content...'
}

const getChannelLabel = (channel) => {
  const channelMap = {
    facebook: 'Facebook',
    zalo: 'Zalo',
    email: 'Email',
    sms: 'SMS'
  }
  return channelMap[channel] || channel
}

const saveDraft = async () => {
  saving.value = true
  console.log('💾 saveDraft called, currentStep:', currentStep.value)
  console.log('📦 templateData:', {
    name: templateData.value.name,
    step3_triggers: templateData.value.step3_triggers,
    triggers: templateData.value.triggers
  })
  
  try {
    // Step 1: Save template
    if (!templateData.value.name || templateData.value.name === 'template') {
      // Create new template
      const result = await templateStore.createTemplate({
        template_name: templateData.value.template_name,
        description: templateData.value.template_description,
        campaign_type: templateData.value.campaign_type,
        objective: templateData.value.objective,
        target_pool: templateData.value.target_pool,
        config_data: templateData.value.config_data,
        conditions: templateData.value.conditions,
        candidate_count: templateData.value.candidate_count,
        is_active: false, // Draft mode
        is_premium: templateData.value.is_premium,
        is_suggestion: templateData.value.is_suggestion,
        is_default: templateData.value.is_default,
        scope_type: templateData.value.scope_type
      })

      if (result.success && result.data?.name) {
        templateData.value.name = result.data.name
        toast.success(__('Template created successfully'))
        hasUnsavedChanges.value = false
        
        // Add tags if any were selected before template was created
        if (templateData.value.campaign_tags && templateData.value.campaign_tags.length > 0) {
          console.log('🏷️ Adding tags to newly created template:', templateData.value.campaign_tags)
          try {
            for (const tag of templateData.value.campaign_tags) {
              await call('frappe.desk.doctype.tag.tag.add_tag', {
                tag: tag.value,
                dt: 'Mira Campaign Template',
                dn: templateData.value.name
              })
            }
            console.log('✅ Tags added to template')
          } catch (error) {
            console.error('❌ Error adding tags to template:', error)
            // Don't fail the whole process if tags fail
          }
        }
      } else {
        toast.error(result.error || __('Failed to create template'))
        return
      }
    } else if (currentStep.value === 1) {
      // Update existing template info (Step 1 fields)
      try {
        await call('frappe.client.set_value', {
          doctype: 'Mira Campaign Template',
          name: templateData.value.name,
          fieldname: {
            template_name: templateData.value.template_name,
            description: templateData.value.template_description,
            objective: templateData.value.objective,
            target_pool: templateData.value.target_pool,
            config_data: templateData.value.config_data,
            conditions: templateData.value.conditions,
            candidate_count: templateData.value.candidate_count
          }
        })
        
        // Update tags
        if (templateData.value.campaign_tags && templateData.value.campaign_tags.length > 0) {
          for (const tag of templateData.value.campaign_tags) {
            await call('frappe.desk.doctype.tag.tag.add_tag', {
              tag: tag.value,
              dt: 'Mira Campaign Template',
              dn: templateData.value.name
            })
          }
        }
        
        toast.success(__('Template updated'))
        hasUnsavedChanges.value = false
      } catch (error) {
        console.error('Error updating template:', error)
        toast.error(__('Failed to update template'))
        return
      }
    }

    // Step 2: Save social contents if any (for steps 2+)
    if (currentStep.value >= 2) {
      const hasChannels = templateData.value.selected_channels && templateData.value.selected_channels.length > 0
      const hasContent = templateData.value.facebook_content?.content || 
                        templateData.value.zalo_content?.content || 
                        templateData.value.email_content?.body ||
                        templateData.value.email_content?.content
      
      if (hasChannels || hasContent) {
        console.log('💾 Saving social contents for template:', templateData.value.name)
        await templateStore.saveSocialContents(templateData.value.name, templateData.value)
      }
    }

    // Step 3: Save landing page if any (for steps 2+)
    if (currentStep.value >= 2 && (templateData.value.ladipage_url || templateData.value.ladipage_id)) {
      await call('frappe.client.set_value', {
        doctype: 'Mira Campaign Template',
        name: templateData.value.name,
        fieldname: {
          ladipage_url: templateData.value.ladipage_url,
          ladipage_id: templateData.value.ladipage_id
        }
      })
    }

    // Step 4: Save triggers/flows if any (for step 3)
    // Use step3_triggers which is bound to Step3 components
    const triggersToSave = templateData.value.step3_triggers || templateData.value.triggers || []
    if (currentStep.value >= 3 && triggersToSave.length > 0) {
      console.log('💾 Saving template flows:', triggersToSave)
      await templateStore.saveTemplateFlows(templateData.value.name, triggersToSave)
    }

  } catch (error) {
    console.error('Error saving template:', error)
    toast.error(__('An error occurred while saving template'))
  } finally {
    saving.value = false
  }
}

const finalizeTemplate = async () => {
  finalizing.value = true
  
  try {
    // Save any pending changes first (including triggers)
    await saveDraft()
    
    // Activate the template
    const result = await call('frappe.client.set_value', {
      doctype: 'Mira Campaign Template',
      name: templateData.value.name,
      fieldname: 'is_active',
      value: 1
    })
    
    if (result) {
      toast.success(isEditMode.value ? __('Template updated successfully') : __('Template created successfully'))
      router.push({ name: 'CampaignTemplateManagement' })
    } else {
      toast.error(__('Failed to finalize template'))
    }
  } catch (error) {
    console.error('Error finalizing template:', error)
    toast.error(__('An error occurred while finalizing template'))
  } finally {
    finalizing.value = false
  }
}

const handleBack = () => {
  router.push({ name: 'CampaignTemplateManagement' })
}

// Campaign type change handler
const onCampaignTypeChange = () => {
  // Reset campaign-specific fields when type changes
  templateData.value.selected_channels = []
  templateData.value.triggers = []
  templateData.value.step3_triggers = []
  templateData.value.facebook_content = {}
  templateData.value.zalo_content = {}
  templateData.value.email_content = {}
  templateData.value.ladipage_url = ''
  templateData.value.ladipage_id = ''
  templateData.value.campaign_name = templateData.value.template_name
  // Keep template_description when changing campaign type
  hasUnsavedChanges.value = true
}

// Watch for changes to mark as unsaved
watch(templateData, () => {
  hasUnsavedChanges.value = true
}, { deep: true, immediate: false })


// Content placeholder methods
const getCampaignObjectivePlaceholder = (campaignType) => {
  const placeholders = {
    'ATTRACTION': 'Attract potential candidates through engaging content and targeted outreach. Build brand awareness and generate interest in our company culture and opportunities.',
    'NURTURING': 'Nurture existing leads and candidates through personalized communication. Build relationships and keep candidates engaged throughout the hiring process.',
    'RECRUITMENT': 'Actively recruit qualified candidates for specific positions. Focus on direct outreach and conversion to applications.'
  }
  return placeholders[campaignType] || 'Define the main objective and goals for this campaign template.'
}

const getConditionsPlaceholder = (campaignType) => {
  const placeholders = {
    'NURTURING': 'Define conditions for candidate selection: skills, experience level, location, engagement score, etc.',
    'RECRUITMENT': 'Define job requirements: required skills, experience, education, certifications, location preferences, etc.'
  }
  return placeholders[campaignType] || 'Define target conditions and criteria.'
}

const getFacebookPlaceholder = (campaignType) => {
  const placeholders = {
    'ATTRACTION': '🚀 Join our amazing team! We\'re looking for talented individuals who are passionate about innovation and growth.\n\n✨ What we offer:\n- Competitive salary\n- Flexible working hours\n- Great team culture\n\n#Hiring #JoinUs #CareerOpportunity',
    'RECRUITMENT': '🎯 We\'re actively hiring for [Position Name]!\n\n📋 Requirements:\n- [Skill 1]\n- [Skill 2]\n- [Experience level]\n\n💰 Competitive package + benefits\n📍 [Location]\n\nReady to take the next step in your career?'
  }
  return placeholders[campaignType] || 'Enter your Facebook post content template here...'
}

const getZaloPlaceholder = (campaignType) => {
  const placeholders = {
    'ATTRACTION': 'Chào bạn! 👋\n\nChúng tôi đang tìm kiếm những tài năng xuất sắc để gia nhập đội ngũ. Bạn có muốn khám phá cơ hội nghề nghiệp tuyệt vời tại công ty chúng tôi không?\n\n🌟 Môi trường làm việc chuyên nghiệp\n💰 Mức lương cạnh tranh\n📈 Cơ hội phát triển',
    'RECRUITMENT': '🎯 Tuyển dụng vị trí [Tên vị trí]!\n\n📌 Yêu cầu:\n- [Kỹ năng 1]\n- [Kỹ năng 2]\n- [Kinh nghiệm]\n\n💼 Lương thỏa thuận + phúc lợi hấp dẫn\n📍 [Địa điểm làm việc]\n\nSẵn sàng ứng tuyển ngay?'
  }
  return placeholders[campaignType] || 'Nhập nội dung tin nhắn Zalo mẫu tại đây...'
}

const getEmailPlaceholder = (campaignType) => {
  return 'Subject: [Email Subject]\n\nHi [Candidate Name],\n\nWe are excited to reach out to you regarding an opportunity at our company...\n\nBest regards,\n[Your Name]'
}

// Trigger methods
const addNurturingTrigger = () => {
  templateData.value.triggers.push({
    trigger_type: '',
    delay_days: 1,
    channel: '',
    content: ''
  })
}

const removeNurturingTrigger = (index) => {
  templateData.value.triggers.splice(index, 1)
}

const addAttractionTrigger = () => {
  templateData.value.step3_triggers.push({
    trigger_type: '',
    action: '',
    config: ''
  })
}

const removeAttractionTrigger = (index) => {
  templateData.value.step3_triggers.splice(index, 1)
}

const addNurturingStep3Trigger = () => {
  templateData.value.step3_triggers.push({
    trigger_type: '',
    condition: '',
    action: ''
  })
}

const removeNurturingStep3Trigger = (index) => {
  templateData.value.step3_triggers.splice(index, 1)
}

const addRecruitmentTrigger = () => {
  templateData.value.step3_triggers.push({
    trigger_type: '',
    job_stage: '',
    action: '',
    config: ''
  })
}

const removeRecruitmentTrigger = (index) => {
  templateData.value.step3_triggers.splice(index, 1)
}

// Content placeholders for triggers
const getNurturingContentPlaceholder = (triggerType) => {
  const placeholders = {
    'time_based': 'Hi [Name], it\'s been a while since we last connected. Here are some exciting updates...',
    'email_opened': 'Thanks for opening our email! Here\'s more information about opportunities...',
    'link_clicked': 'We noticed you\'re interested in [Topic]. Here are some related opportunities...'
  }
  return placeholders[triggerType] || 'Enter content template for this trigger...'
}

const getAttractionTriggerPlaceholder = (triggerType) => {
  const placeholders = {
    'form_submitted': '{"form_id": "contact_form", "auto_response": true, "follow_up_delay": 24}',
    'page_visited': '{"page_url": "/careers", "visit_count": 3, "action": "send_email"}',
    'qr_scanned': '{"qr_code_id": "career_qr", "redirect_url": "/apply", "track_source": true}'
  }
  return placeholders[triggerType] || '{"key": "value", "action": "default"}'
}

const getRecruitmentTriggerPlaceholder = (triggerType) => {
  const placeholders = {
    'application_submitted': '{"auto_acknowledge": true, "notify_recruiter": true, "screening_delay": 48}',
    'interview_scheduled': '{"reminder_hours": [24, 2], "preparation_materials": true}',
    'assessment_completed': '{"auto_score": true, "threshold": 70, "next_stage": "interview"}'
  }
  return placeholders[triggerType] || '{"key": "value", "action": "default"}'
}

// Watchers
watch(() => templateData.value.template_name, (newName) => {
  if (newName && !templateData.value.campaign_name) {
    templateData.value.campaign_name = newName
  }
})

// Load template for edit mode
const loadTemplateForEdit = async () => {
  if (!isEditMode.value) return
  
  const templateId = route.params.id
  console.log('🔍 Loading template for edit:', templateId)
  
  loading.value = true
  
  try {
    const data = await templateStore.loadTemplateWithSocialContents(templateId)
    
    console.log('📦 Loaded template data:', data)
    
    if (data) {
      // Map API response to templateData
      templateData.value = {
        ...templateData.value,
        name: data.name,
        template_name: data.template_name || '',
        template_description: data.description || '',
        campaign_type: data.campaign_type || 'ATTRACTION',
        scope_type: data.scope_type || 'PRIVATE',
        is_default: data.is_default || false,
        is_premium: data.is_premium || false,
        is_suggestion: data.is_suggestion || false,
        
        // Campaign Info from configuration
        objective: data.objective || '',
        target_pool: data.target_pool || '',
        campaign_tags: data.campaign_tags || [],
        
        // Landing Page
        ladipage_url: data.ladipage_url || '',
        ladipage_id: data.ladipage_id || '',
        
        // Social Contents
        selected_channels: data.selected_channels || [],
        facebook_content: {
          content: data.facebook_content?.content || '',
          image: data.facebook_content?.image || null,
          page_id: data.facebook_content?.page_id || null,
          connection_id: data.facebook_content?.connection_id || null
        },
        zalo_content: {
          content: data.zalo_content?.content || '',
          image: data.zalo_content?.image || null,
          page_id: data.zalo_content?.page_id || null,
          connection_id: data.zalo_content?.connection_id || null
        },
        email_content: {
          subject: data.email_content?.subject || '',
          body: data.email_content?.body || data.email_content?.content || '',
          content: data.email_content?.content || '',
          mjml_content: data.email_content?.mjml_content || null,
          block_content: data.email_content?.block_content || null
        }
      }
      
      // Also set campaign_name for validation
      templateData.value.campaign_name = data.template_name || ''
      
      console.log('✅ Template data mapped:', templateData.value)
      
      // Load triggers/flows
      const triggers = await templateStore.getTemplateFlows(templateId)
      if (triggers && triggers.length > 0) {
        templateData.value.step3_triggers = triggers
        templateData.value.triggers = triggers // Also set for compatibility
        console.log('✅ Loaded triggers:', triggers)
      }
    } else {
      console.error('❌ Failed to load template data')
      toast.error(__('Failed to load template'))
    }
  } catch (error) {
    console.error('❌ Error loading template:', error)
    toast.error(__('Error loading template'))
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  console.log('🚀 CampaignTemplateWizard mounted')
  console.log('📍 Route params:', route.params)
  console.log('📍 isEditMode:', isEditMode.value)
  
  if (isEditMode.value) {
    // Load template data for editing
    console.log('📝 Edit mode detected, loading template...')
    loadTemplateForEdit()
  } else if (quickTemplates.length > 0) {
    // Initialize with first quick template if creating new
    console.log('➕ Create mode, selecting quick template')
    selectQuickTemplate(quickTemplates[0])
  }
})
</script>
