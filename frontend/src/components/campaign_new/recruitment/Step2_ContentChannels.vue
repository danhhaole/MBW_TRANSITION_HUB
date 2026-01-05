<!-- Recruitment Content & Channels - Similar to Attraction but with Email -->
<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-2">
        {{ __('Content & Channels') }}
      </h3>
      <p class="text-sm text-gray-600">
        {{ __('Create content for recruitment campaign across multiple channels') }}
      </p>
      <div
        v-if="campaignObjective"
        class="mt-3 flex items-start rounded-md bg-blue-50 px-3 py-2 text-sm text-blue-800 border border-blue-200 w-full"
      >
        <FeatherIcon name="target" class="h-4 w-4 mr-2 mt-0.5 flex-shrink-0 text-blue-600" />
        <div class="flex-1 min-w-0">
          <span class="font-semibold mr-2">
            {{ __('Campaign Objective') }}:
          </span>
          <span class="text-blue-900">
            {{ campaignObjective }}
          </span>
        </div>
      </div>
    </div>

    <!-- Landing Page Selector (Section 2.1) -->
    <LandingPageSelector
      v-model:ladipage-url="localLadipageUrl"
      v-model:ladipage-id="localLadipageId"
      :campaign-id="props.name"
      :campaign-name="campaignName"
      :company-info="companyInfo"
      :job-info="jobInfo"
      :doctype="doctype"
    />

    <!-- Channel Selection with Add Button -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('Posting Channels') }}
        </h4>

        <!-- Add Channel Dropdown (only show if there are available channels) -->
        <Dropdown v-if="availableChannelOptions.length > 0" :options="availableChannelOptions">
          <template v-slot="{ open }">
            <Button variant="solid" size="sm" :theme="'gray'">
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Add Channel') }}
              <template #suffix>
                <FeatherIcon
                  :name="open ? 'chevron-up' : 'chevron-down'"
                  class="h-4 w-4"
                />
              </template>
            </Button>
          </template>
        </Dropdown>

        <!-- All channels added message -->
        <div v-else class="text-xs text-gray-500 flex items-center">
          <FeatherIcon name="check-circle" class="h-4 w-4 text-green-600 mr-1" />
          {{ __('All channels added') }}
        </div>
      </div>

      <!-- Selected Channels List (Empty State) -->
      <div v-if="localSelectedChannels.length === 0" class="text-center py-8 border-2 border-dashed border-gray-200 rounded-lg">
        <FeatherIcon name="share-2" class="h-10 w-10 text-gray-400 mx-auto mb-3" />
        <p class="text-sm text-gray-600 mb-1">{{ __('No channels added yet') }}</p>
        <p class="text-xs text-gray-500">{{ __('Click "Add Channel" to start posting') }}</p>
      </div>

      <!-- No channel selected warning -->
      <div v-if="localSelectedChannels.length === 0 && showError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
        <div class="flex items-start">
          <FeatherIcon name="alert-circle" class="h-4 w-4 text-red-600 mt-0.5 mr-2 flex-shrink-0" />
          <p class="text-sm text-red-800">
            {{ __('Please add at least one channel to continue') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Channel Content Editors (Collapsible) -->
    <div class="space-y-4">
      <!-- Email Editor (Collapsible) -->
      <div v-if="isEmailSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('email')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-red-500 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="mail" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('Email Campaign') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localEmailContent.subject ? __('Content added') : __('Click to add content') }}
              </p>
            </div>
            <FeatherIcon
              :name="expandedEditors.email ? 'chevron-up' : 'chevron-down'"
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('email')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        <div v-if="expandedEditors.email" class="p-6 space-y-4">
          <!-- Schedule Time for Email -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center mb-3">
              <FeatherIcon name="clock" class="h-4 w-4 text-gray-600 mr-2" />
              <label class="text-sm font-medium text-gray-700">
                {{ __('Email Send Time') }}
              </label>
            </div>
            <FormControl
              type="datetime-local"
              :model-value="localEmailContent.schedule_time"
              :placeholder="__('Leave empty to send immediately')"
              @update:model-value="updateEmailScheduleTime($event)"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ localEmailContent.schedule_time ? __('Will send at scheduled time') : __('Will send immediately when campaign starts') }}
            </p>
          </div>

          <!-- Content Editor -->
          <EmailContentEditor
            :content="localEmailContent"
            @update:content="updateEmailContent"
            @saved="handleEmailSaved"
          >
            <template #actions>
              <Button @click="openTestEmailModal" variant="solid" theme="blue" size="sm">
                <template #prefix>
                  <FeatherIcon name="send" class="h-4 w-4" />
                </template>
                {{ __('Send Email To Check') }}
              </Button>
            </template>
          </EmailContentEditor>
        </div>
      </div>

    <!-- Test Email Dialog -->
    <Dialog
      v-model="showTestEmailModal"
      :options="{
        title: __('Test Email Configuration'),
        size: '5xl'
      }"
    >
      <template #body-content>
        <div class="space-y-4">
          <div class="space-y-1">
            <label class="block text-sm font-medium text-gray-700">
              {{ __('Email') }} <span class="text-red-500">*</span>
            </label>
            <FormControl
              type="email"
              v-model="testEmailAddress"
              :placeholder="__('Enter email address')"
            />
          </div>
          <label class="block text-sm font-medium text-gray-700">
            {{ __('Content') }}
          </label>
          <div class="overflow-hidden">
            <iframe
              ref="testEmailPreviewIframe"
              class="w-full h-80 bg-white border-0 test-email-preview-iframe"
              :srcdoc="testEmailPreviewHtml"
              scrolling="auto"
              style="border: none; outline: none;"
              @load="onPreviewIframeLoad"
            ></iframe>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" theme="gray" @click="showTestEmailModal = false">
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            theme="blue"
            @click="confirmSendTestEmail"
            :disabled="!isTestEmailValid || isSendingEmail"
            :loading="isSendingEmail"
          >
            {{ isSendingEmail ? __('Sending...') : __('Send Email') }}
          </Button>
        </div>
      </template>
    </Dialog>

      <!-- Facebook Editor (Collapsible) -->
      <div v-if="isFacebookSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('facebook')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-blue-500 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="facebook" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('Facebook Post') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localFacebookContent.content ? __('Content added') : __('Click to add content') }}
              </p>
            </div>
            <FeatherIcon
              :name="expandedEditors.facebook ? 'chevron-up' : 'chevron-down'"
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('facebook')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        <div v-if="expandedEditors.facebook" class="p-6 space-y-4">
          <!-- Schedule Time for Facebook -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center mb-3">
              <FeatherIcon name="clock" class="h-4 w-4 text-gray-600 mr-2" />
              <label class="text-sm font-medium text-gray-700">
                {{ __('Post Schedule Time') }}
              </label>
            </div>
            <FormControl
              type="datetime-local"
              :model-value="localFacebookContent.schedule_time"
              :placeholder="__('Leave empty to post immediately')"
              @update:model-value="updateFacebookContent('schedule_time', $event)"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ localFacebookContent.schedule_time ? __('Will post at scheduled time') : __('Will post immediately when campaign starts') }}
            </p>
          </div>

          <!-- Content Editor -->
          <FacebookContentEditor
            :content="localFacebookContent.content"
            :image="localFacebookContent.image"
            :page-id="localFacebookContent.page_id"
            :page-options="facebookPages"
            :show-page-selector="true"
            :show-link-input="false"
            :placeholder="__('Write your job post content here...')"
            :share-page-data="sharePageData"
            @update:content="updateFacebookContent('content', $event)"
            @update:image="updateFacebookContent('image', $event)"
            @update:page-id="updateFacebookContent('page_id', $event)"
          />

          <!-- Test Share Job Posting Button -->
          <div class="mt-4 pt-4 border-t border-gray-200">
            <Button
              @click="testShareJobPosting"
              :loading="testingShare"
              variant="outline"
              size="sm"
              class="w-full"
            >
              <template #prefix>
                <FeatherIcon name="send" class="h-4 w-4" />
              </template>
              {{ __('Test Share Job to Facebook') }}
            </Button>
            <p class="text-xs text-gray-500 mt-2 text-center">
              {{ __('This will post the current content to your selected Facebook page') }}
            </p>
          </div>
        </div>
      </div>

      <!-- Zalo Editor (Collapsible) -->
      <div v-if="isZaloSelected" class="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div class="px-6 py-4 flex items-center justify-between border-b border-gray-200">
          <button
            @click="toggleEditor('zalo')"
            class="flex items-center flex-1 hover:opacity-80 transition-opacity"
          >
            <div class="w-10 h-10 rounded-lg bg-blue-600 text-white flex items-center justify-center mr-3">
              <FeatherIcon name="message-square" class="h-5 w-5" />
            </div>
            <div class="text-left flex-1">
              <h4 class="text-sm font-semibold text-gray-900">
                {{ __('Zalo Post') }}
              </h4>
              <p class="text-xs text-gray-500">
                {{ localZaloContent.content ? __('Content added') : __('Click to add content') }}
              </p>
            </div>
            <FeatherIcon
              :name="expandedEditors.zalo ? 'chevron-up' : 'chevron-down'"
              class="h-5 w-5 text-gray-400 mr-3"
            />
          </button>
          <button
            @click="removeChannel('zalo')"
            class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded transition-colors"
            :title="__('Remove channel')"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </button>
        </div>
        <div v-if="expandedEditors.zalo" class="p-6 space-y-4">
          <!-- Schedule Time for Zalo -->
          <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
            <div class="flex items-center mb-3">
              <FeatherIcon name="clock" class="h-4 w-4 text-gray-600 mr-2" />
              <label class="text-sm font-medium text-gray-700">
                {{ __('Post Schedule Time') }}
              </label>
            </div>
            <FormControl
              type="datetime-local"
              :model-value="localZaloContent.schedule_time"
              :placeholder="__('Leave empty to post immediately')"
              @update:model-value="updateZaloScheduleTime($event)"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ localZaloContent.schedule_time ? __('Will post at scheduled time') : __('Will post immediately when campaign starts') }}
            </p>
          </div>

          <!-- Content Editor -->
          <ZaloContentEditor
            :content="localZaloContent"
            :share-page-data="sharePageData"
            :oa-options="zaloAccounts"
            :show-oa-selector="true"
            @update:content="updateZaloContent"
            @update:oa-id="updateZaloOaId"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useToast } from '@/composables/useToast'
import { FeatherIcon, Button, Dropdown, FormControl, Dialog, call } from 'frappe-ui'
import EmailContentEditor from '../molecules/EmailContentEditor.vue'
import FacebookContentEditor from '../molecules/FacebookContentEditor.vue'
import ZaloContentEditor from '../molecules/ZaloContentEditor.vue'
import LandingPageSelector from '../molecules/LandingPageSelector.vue'
import { getDefaultEmailTemplate } from '@/utils/emailTemplates'

const props = defineProps({
  selectedChannels: {
    type: Array,
    default: () => []
  },
  emailContent: {
    type: Object,
    default: () => ({ subject: '', body: '' })
  },
  campaignObjective: {
    type: String,
    default: ''
  },
  facebookContent: {
    type: Object,
    default: () => ({ content: '', image: null, page_id: null })
  },
  zaloContent: {
    type: Object,
    default: () => ({ content: '', image: null })
  },
  campaignName: {
    type: String,
    default: ''
  },
  name: {
    type: String,
    default: ''
  },
  ladipageUrl: {
    type: String,
    default: ''
  },
  ladipageId: {
    type: String,
    default: ''
  },
  companyInfo: {
    type: Object,
    default: () => ({})
  },
  jobInfo: {
    type: Object,
    default: () => ({})
  },
  showError: {
    type: Boolean,
    default: false
  },
  doctype: {
    type: String,
    default: 'Mira Campaign' // 'Mira Campaign' or 'Mira Campaign Template'
  }
})

console.log('[Step2_ContentChannels] props.campaignObjective:', props.campaignObjective)

const emit = defineEmits([
  'update:selectedChannels',
  'update:emailContent',
  'update:facebookContent',
  'update:zaloContent',
  'update:ladipageUrl',
  'update:ladipageId'
])

// Local computed properties for two-way binding
const localSelectedChannels = computed({
  get: () => props.selectedChannels,
  set: (value) => emit('update:selectedChannels', value)
})

const localEmailContent = computed({
  get: () => props.emailContent,
  set: (value) => emit('update:emailContent', value)
})

const localFacebookContent = computed({
  get: () => props.facebookContent,
  set: (value) => emit('update:facebookContent', value)
})

const localZaloContent = computed({
  get: () => props.zaloContent,
  set: (value) => emit('update:zaloContent', value)
})

const localLadipageUrl = computed({
  get: () => props.ladipageUrl,
  set: (value) => emit('update:ladipageUrl', value)
})

const localLadipageId = computed({
  get: () => props.ladipageId,
  set: (value) => emit('update:ladipageId', value)
})

// Share page data for short link generation
const sharePageData = computed(() => {
  if (!localLadipageUrl.value) return null
  return {
    url: localLadipageUrl.value,
    campaignName: props.campaignName,
    // Dùng campaignId (props.name) cho utm_campaign, vẫn hiển thị campaignName
    campaignId: props.name
  }
})


// Facebook pages from Mira External Connection
const facebookPages = ref([])
const loadingPages = ref(false)
const testingShare = ref(false)

// Zalo OA accounts from Mira External Connection
const zaloAccounts = ref([])
const loadingZaloAccounts = ref(false)

// Channel options - Include Email for recruitment
const allChannelOptions = [
  {
    label: __('Email'),
    value: 'email',
    icon: 'mail',
    onClick: () => addChannel('email')
  },
  {
    label: __('Facebook'),
    value: 'facebook',
    icon: 'facebook',
    onClick: () => addChannel('facebook')
  },
  {
    label: __('Zalo'),
    value: 'zalo',
    icon: 'message-square',
    onClick: () => addChannel('zalo')
  }
]

// Available channel options (not yet selected)
const availableChannelOptions = computed(() => {
  return allChannelOptions.filter(option =>
    !localSelectedChannels.value.includes(option.value)
  )
})
const toast = useToast()
// Channel selection helpers
const isEmailSelected = computed(() => localSelectedChannels.value.includes('email'))
const isFacebookSelected = computed(() => localSelectedChannels.value.includes('facebook'))
const isZaloSelected = computed(() => localSelectedChannels.value.includes('zalo'))

// Expanded editors state
const expandedEditors = ref({
  email: true,
  facebook: true,
  zalo: true
})

// Get default email template (same as Step2_ContentTimeline.vue)

// Channel management
const addChannel = (channelType) => {
  if (!localSelectedChannels.value.includes(channelType)) {
    localSelectedChannels.value = [...localSelectedChannels.value, channelType]
    // Auto-expand the editor when adding
    expandedEditors.value[channelType] = true
    
    // Initialize default email template when adding email channel
    if (channelType === 'email') {
      const defaultTemplate = getDefaultEmailTemplate()
      // Only initialize if emailContent is empty or doesn't have template_content
      if (!localEmailContent.value || !localEmailContent.value.template_content || localEmailContent.value.template_content.trim() === '') {
        localEmailContent.value = {
          email_subject: '',
          email_content: '',
          block_content: '',
          template_content: defaultTemplate.trim(), // Set default template content
          mjml_content: '',
          css_content: '', // Initialize css_content as empty string
          attachments: [],
          schedule_time: null
        }
        console.log('✅ [Step2_ContentChannels] Initialized default email template with css_content')
      }
    }
  }
}

const removeChannel = (channelType) => {
  localSelectedChannels.value = localSelectedChannels.value.filter(ch => ch !== channelType)
  expandedEditors.value[channelType] = false
}

// Content update handlers
const updateEmailContent = (content) => {
  console.log('📧 [Step2_ContentChannels] ========== updateEmailContent called ==========')
  console.log('   incoming content.email_subject:', content?.email_subject)
  console.log('   incoming content.email_subject type:', typeof content?.email_subject)
  console.log('   incoming content.email_subject length:', content?.email_subject?.length || 0)
  console.log('   current localEmailContent.value.email_subject:', localEmailContent.value.email_subject)
  
  // IMPORTANT: Preserve email_subject if incoming content.email_subject is empty string or undefined
  // This prevents overwriting user input when EmailEditor emits update:content
  // Only preserve if current localEmailContent has a non-empty email_subject AND incoming content doesn't have a valid one
  const currentEmailSubject = localEmailContent.value.email_subject || ''
  const newEmailSubject = content.email_subject || ''
  const shouldPreserveEmailSubject = currentEmailSubject.trim() !== '' && newEmailSubject.trim() === ''
  const preservedEmailSubject = shouldPreserveEmailSubject 
    ? currentEmailSubject
    : newEmailSubject
  
  // IMPORTANT: Merge content to preserve existing fields (like nurturing campaign)
  // Simply merge - preserve all existing fields including email_subject and attachments
  localEmailContent.value = {
    ...localEmailContent.value,
    ...content,
    // IMPORTANT: Preserve email_subject if incoming content doesn't have a valid value
    email_subject: preservedEmailSubject
  }
  
  console.log('✅ [Step2_ContentChannels] Updated localEmailContent')
  console.log('   preserved email_subject:', localEmailContent.value.email_subject)
  console.log('   email_subject preserved:', shouldPreserveEmailSubject)
  console.log('   attachments count:', localEmailContent.value.attachments?.length || 0)
  console.log('   template_content length:', localEmailContent.value.template_content?.length || 0)
  console.log('   block_content length:', localEmailContent.value.block_content?.length || 0)
  console.log('   css_content length:', localEmailContent.value.css_content?.length || 0)
  
  // ✅ IMPORTANT: Emit to parent so wizard receives updated content with all fields
  emit('update:email-content', { ...localEmailContent.value })
  console.log('📤 [Step2_ContentChannels] Emitted update:email-content to parent')
  console.log('   emitted email_subject:', localEmailContent.value.email_subject)
  console.log('📧 [Step2_ContentChannels] ========== END updateEmailContent ==========')
}

// Handle email saved event - ensure css_content is saved and auto-save to doctype
const handleEmailSaved = async (content) => {
  console.log('💾 [Step2_ContentChannels] ========== EMAIL SAVED EVENT ==========')
  console.log('   Received content keys:', Object.keys(content || {}))
  console.log('   email_subject:', content?.email_subject)
  console.log('   email_subject type:', typeof content?.email_subject)
  console.log('   email_subject length:', content?.email_subject?.length || 0)
  console.log('   email_subject value:', JSON.stringify(content?.email_subject))
  console.log('   attachments count:', content?.attachments?.length || 0)
  console.log('   attachments:', content?.attachments)
  console.log('   css_content exists:', !!content?.css_content)
  console.log('   css_content length:', content?.css_content?.length || 0)
  console.log('   template_content exists:', !!content?.template_content)
  console.log('   template_content length:', content?.template_content?.length || 0)
  console.log('   block_content exists:', !!content?.block_content)
  console.log('   block_content length:', content?.block_content?.length || 0)
  console.log('   mjml_content exists:', !!content?.mjml_content)
  console.log('   mjml_content length:', content?.mjml_content?.length || 0)
  console.log('   Full content object:', JSON.stringify(content, null, 2))
  
  // IMPORTANT: Use content from saved event directly (it has the latest data from EmailEditor)
  // Priority: content fields (from saved event) > localEmailContent.value fields (old)
  const finalCssContent = (content.css_content !== undefined && content.css_content !== null && content.css_content.trim() !== '')
    ? content.css_content
    : (localEmailContent.value.css_content || '')
  
  const finalBlockContent = (content.block_content !== undefined && content.block_content !== null && content.block_content.trim() !== '')
    ? content.block_content
    : (localEmailContent.value.block_content || '')
  
  const finalTemplateContent = (content.template_content !== undefined && content.template_content !== null && content.template_content.trim() !== '')
    ? content.template_content
    : (localEmailContent.value.template_content || '')
  
  // IMPORTANT: Update localEmailContent directly with saved content (like nurturing campaign)
  // This preserves ALL fields including email_subject and attachments
  localEmailContent.value = { ...content }
  
  console.log('✅ [Step2_ContentChannels] Updated localEmailContent with saved content:')
  console.log('   email_subject:', localEmailContent.value.email_subject)
  console.log('   attachments count:', localEmailContent.value.attachments?.length || 0)
  console.log('   css_content length:', localEmailContent.value.css_content?.length || 0)
  console.log('   template_content length:', localEmailContent.value.template_content?.length || 0)
  console.log('   block_content length:', localEmailContent.value.block_content?.length || 0)
  
  // IMPORTANT: Emit to parent with FULL content including all fields (like nurturing campaign)
  // Simply use content directly - it has ALL fields including email_subject and attachments
  const contentToEmit = { ...content }
  
  // IMPORTANT: Emit update:email-content to parent
  // This will update props.emailContent in parent, which will flow back to EmailContentEditor
  emit('update:email-content', contentToEmit)
  console.log('📤 [Step2_ContentChannels] Emitted update:email-content to parent')
  console.log('📤 [Step2_ContentChannels] Emitted to parent:')
  console.log('   email_subject:', contentToEmit.email_subject)
  console.log('   attachments count:', contentToEmit.attachments?.length || 0)
  console.log('   css_content length:', contentToEmit.css_content?.length || 0)
  console.log('   block_content length:', contentToEmit.block_content?.length || 0)
  console.log('   template_content length:', contentToEmit.template_content?.length || 0)
  
  
  // Auto-save to doctype if campaign is already created
  if (props.name && props.doctype === 'Mira Campaign') {
    try {
      console.log('💾 [Step2_ContentChannels] Auto-saving to Mira Campaign Social...')
      console.log('   Campaign ID:', props.name)
      
      // IMPORTANT: Use content directly (like nurturing campaign does)
      // Extract sender_account value if it's an object
      const emailContentToSave = {
        ...content,
        sender_account: typeof content.sender_account === 'object'
          ? content.sender_account?.value
          : content.sender_account
      }
      
      // Prepare social posts array (only email for now)
      // IMPORTANT: Include ALL fields exactly like nurturing campaign does
      const socialPosts = [{
        platform: 'Email',
        subject: emailContentToSave.email_subject || '',
        template_content: emailContentToSave.template_content || emailContentToSave.email_content || '',
        block_content: emailContentToSave.block_content || '',  // IMPORTANT: Include block_content
        mjml_content: emailContentToSave.mjml_content || '',
        css_content: emailContentToSave.css_content || '',  // IMPORTANT: Include css_content
        sender_account: emailContentToSave.sender_account || null,
        status: 'Pending',
        post_schedule_time: emailContentToSave.schedule_time || null
      }]
      
      console.log('📧 [Step2_ContentChannels] Social posts to save:')
      console.log('   platform:', socialPosts[0].platform)
      console.log('   subject:', socialPosts[0].subject)
      console.log('   css_content exists:', !!socialPosts[0].css_content)
      console.log('   css_content length:', socialPosts[0].css_content?.length || 0)
      console.log('   css_content preview:', socialPosts[0].css_content?.substring(0, 200) + '...')
      console.log('   template_content exists:', !!socialPosts[0].template_content)
      console.log('   template_content length:', socialPosts[0].template_content?.length || 0)
      console.log('   block_content exists:', !!socialPosts[0].block_content)
      console.log('   block_content length:', socialPosts[0].block_content?.length || 0)
      console.log('   block_content preview:', socialPosts[0].block_content?.substring(0, 200) + '...')
      console.log('   mjml_content exists:', !!socialPosts[0].mjml_content)
      console.log('   mjml_content length:', socialPosts[0].mjml_content?.length || 0)
      
      const result = await call('mbw_mira.api.campaign_social.save_campaign_social_posts', {
        campaign_id: props.name,
        posts: socialPosts  // Use 'posts' parameter to match API
      })
      
      console.log('📥 [Step2_ContentChannels] API response:', result)
      
      if (result && result.success) {
        console.log('✅ [Step2_ContentChannels] Template saved to Mira Campaign Social successfully')
        console.log('   Saved css_content length:', socialPosts[0].css_content?.length || 0)
        console.log('   Saved block_content length:', socialPosts[0].block_content?.length || 0)
        console.log('   Saved template_content length:', socialPosts[0].template_content?.length || 0)
        toast.success(__('Template saved to campaign'))
      } else {
        console.error('❌ [Step2_ContentChannels] Failed to save:', result?.message || result?.error)
        toast.error(__('Failed to auto-save template: ') + (result?.message || result?.error || 'Unknown error'))
      }
    } catch (error) {
      console.error('❌ [Step2_ContentChannels] Error auto-saving template:', error)
      console.error('   Error details:', JSON.stringify(error, null, 2))
      toast.error(__('Failed to auto-save template: ') + (error.message || 'Unknown error'))
    }
  } else {
    console.log('⚠️ [Step2_ContentChannels] Skipping auto-save:')
    console.log('   props.name:', props.name)
    console.log('   props.doctype:', props.doctype)
  }
  
  console.log('💾 [Step2_ContentChannels] ========== END EMAIL SAVED EVENT ==========')
}

const updateEmailScheduleTime = (scheduleTime) => {
  localEmailContent.value = {
    ...localEmailContent.value,
    schedule_time: scheduleTime
  }
}

const updateFacebookContent = (field, value) => {
  localFacebookContent.value = {
    ...localFacebookContent.value,
    [field]: value
  }
}

const updateZaloContent = (content) => {
  localZaloContent.value = content
}

const updateZaloOaId = (oaId) => {
  localZaloContent.value = {
    ...localZaloContent.value,
    oa_id: oaId
  }
}

const updateZaloScheduleTime = (scheduleTime) => {
  localZaloContent.value = {
    ...localZaloContent.value,
    schedule_time: scheduleTime
  }
}

// Helper function to strip HTML tags and convert to plain text with line breaks
const stripHtmlTags = (html) => {
  if (!html) return ''
  
  // Replace block-level HTML elements with newlines BEFORE stripping tags
  let text = html
    // Replace closing block tags with double newline (paragraph breaks)
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<\/div>/gi, '\n\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<\/h[1-6]>/gi, '\n\n')
    // Replace BR tags with single newline
    .replace(/<br\s*\/?>/gi, '\n')
    // Replace list items with bullet points
    .replace(/<li[^>]*>/gi, '\n• ')
  
  // Now strip all remaining HTML tags
  const tmp = document.createElement('div')
  tmp.innerHTML = text
  text = tmp.textContent || tmp.innerText || ''
  
  // Clean up excessive newlines (more than 2 consecutive)
  text = text.replace(/\n{3,}/g, '\n\n')
  
  // Trim each line but preserve the newlines
  text = text
    .split('\n')
    .map(line => line.trim())
    .join('\n')
  
  // Remove leading/trailing whitespace from the entire text
  return text.trim()
}

// Test share job posting to Facebook
const testShareJobPosting = async () => {
  if (!localFacebookContent.value.page_id) {
    toast.error(__('Please select a Facebook page first'))
    return
  }

  if (!localFacebookContent.value.content) {
    toast.error(__('Please add content to your Facebook post'))
    return
  }

  testingShare.value = true
  
  try {
    // Find the connection ID for the selected Facebook page
    const selectedPage = facebookPages.value.find(page => page.value === localFacebookContent.value.page_id)
    console.log('Selected Facebook page:', selectedPage)
    if (!selectedPage) {
      throw new Error('Selected Facebook page not found')
    }

    if (!selectedPage.connection_id) {
      throw new Error('Facebook page connection ID not found. Please reconnect your Facebook account.')
    }

    // Extract URL from content (both HTML and plain text) - prioritize short links
    let extractedUrl = null
    let cleanMessage = ''
    
    try {
      const content = localFacebookContent.value.content || ''
      console.log('Original content:', content)
      
      // First, try to extract URL from HTML links (<a href="...">)
      const htmlLinkMatch = content.match(/<a[^>]+href=["']([^"']+)["'][^>]*>/i)
      if (htmlLinkMatch && htmlLinkMatch[1]) {
        extractedUrl = htmlLinkMatch[1]
        console.log('🔗 Found URL in HTML link:', extractedUrl)
      }
      
      // If no HTML link, try plain URL pattern (prioritize short links like is.gd, bit.ly, etc.)
      if (!extractedUrl) {
        // Pattern for short link services (is.gd, bit.ly, tinyurl, etc.) or any URL
        const urlPatterns = [
          /https?:\/\/(?:is\.gd|bit\.ly|tinyurl|t\.co|goo\.gl|ow\.ly|buff\.ly|short\.link)\/[^\s<>"']+/i, // Short links first
          /https?:\/\/[^\s<>"']+/i // Any URL
        ]
        
        for (const pattern of urlPatterns) {
          const urlMatch = content.match(pattern)
          if (urlMatch && urlMatch[0]) {
            extractedUrl = urlMatch[0]
            console.log('🔗 Found URL in content:', extractedUrl)
            break
          }
        }
      }
      
      // Strip HTML tags from content for message body
      cleanMessage = stripHtmlTags(content)
      console.log('Clean message:', cleanMessage)
      
      // If we found a URL in content, use it; otherwise use ladipageUrl
      if (extractedUrl) {
        console.log('✅ Using extracted URL from content:', extractedUrl)
      } else {
        console.log('ℹ️ No URL found in content; will use ladipageUrl:', props.ladipageUrl)
      }
    } catch (e) {
      console.warn('⚠️ Error extracting URL from content:', e)
      cleanMessage = stripHtmlTags(localFacebookContent.value.content)
    }
    
    // Use extracted URL if found, otherwise fallback to ladipageUrl
    const shareUrl = extractedUrl || props.ladipageUrl

    const result = await call('mbw_mira.api.external_connections.share_job_posting', {
      connection_id: selectedPage.connection_id,
      job_id: props.name || 'test_job_id',
      message: cleanMessage,  // Message đã chứa short link (nếu có)
      schedule_type: 'now',
      image_url: localFacebookContent.value.image || '',
      campaign_id: props.name,
      // Chỉ gửi ladipage_url nếu không có URL trong message (để Facebook tự append)
      // Nếu message đã có short link, không cần ladipage_url
      ladipage_url: extractedUrl ? '' : shareUrl, // Empty nếu đã có URL trong message
      platform_type: selectedPage.platform_type || 'facebook',
      scheduled_time: localFacebookContent.value.schedule_time
    })

    if (result.status === 'success') {
      toast.success(__('Job posted to Facebook successfully!'))
      console.log('✅ Facebook post result:', result)
    } else {
      throw new Error(result.message || 'Failed to post to Facebook')
    }
  } catch (error) {
    console.error('❌ Error sharing job to Facebook:', error)
    toast.error(error.message || __('Failed to share job to Facebook'))
  } finally {
    testingShare.value = false
  }
}

const toggleEditor = (channelType) => {
  expandedEditors.value[channelType] = !expandedEditors.value[channelType]
}

// Load Facebook pages
const loadFacebookPages = async () => {
  try {
    loadingPages.value = true
    const result = await call('mbw_mira.api.external_connection.get_facebook_pages')

    if (result.success && result.data) {
      facebookPages.value = result.data.map(page => ({
        label: page.page_name,
        value: page.page_id,
        connection_id: page.connection_name // Use connection_name as connection_id
      }))
      console.log('✅ Loaded Facebook pages:', facebookPages.value)
    }
  } catch (error) {
    console.error('❌ Error loading Facebook pages:', error)
  } finally {
    loadingPages.value = false
  }
}

// Load Zalo OA accounts
const loadZaloAccounts = async () => {
  try {
    loadingZaloAccounts.value = true
    const result = await call('mbw_mira.api.external_connection.get_zalo_accounts')

    if (result.success && result.data) {
      zaloAccounts.value = result.data.map(account => ({
        label: account.oa_name,
        value: account.oa_id,
        oa_id: account.oa_id
      }))
      console.log('✅ Loaded Zalo OA accounts:', zaloAccounts.value)
    }
  } catch (error) {
    console.error('❌ Error loading Zalo accounts:', error)
  } finally {
    loadingZaloAccounts.value = false
  }
}

// Load pages and accounts on mount
onMounted(() => {
  loadFacebookPages()
  loadZaloAccounts()
})

// Test Email Modal state
const showTestEmailModal = ref(false)
const testEmailContent = ref(null)
const testEmailAddress = ref('')
const isSendingEmail = ref(false)
const testEmailPreviewIframe = ref(null)

// Computed property for test email preview HTML to ensure reactivity
const testEmailPreviewHtml = computed(() => {
  if (!testEmailContent.value) {
    return ''
  }
  return getPreviewIframeDoc(testEmailContent.value)
})

// Watch for changes in testEmailContent to force iframe update
watch(() => testEmailContent.value, (newContent) => {
  if (newContent && showTestEmailModal.value) {
    nextTick(() => {
      const iframe = document.querySelector('.test-email-preview-iframe')
      if (iframe && testEmailPreviewHtml.value) {
        iframe.srcdoc = testEmailPreviewHtml.value
      }
    })
  }
}, { deep: true })

const onPreviewIframeLoad = () => {
  // Force iframe to reload CSS by checking if CSS is actually loaded
  const iframe = document.querySelector('.test-email-preview-iframe')
  if (iframe && iframe.contentDocument) {
    const iframeDoc = iframe.contentDocument
    const styleTags = iframeDoc.querySelectorAll('style[id="email-css-content"]')
    if (styleTags.length === 0) {
      console.warn('[Step2_ContentChannels] No CSS style tag found in iframe')
    }
  }
}

const openTestEmailModal = () => {
  testEmailContent.value = localEmailContent.value
  testEmailAddress.value = ''
  showTestEmailModal.value = true
}

const stripHtml = (html) => {
  const div = document.createElement('div')
  div.innerHTML = html
  return div.textContent || div.innerText || ''
}

const getPreviewIframeDoc = (content) => {
  if (!content) {
    return wrapEmailContent('', true, '')
  }
  
  let html = getPreviewHtml(content)
  let cssContent = content?.css_content || ''
  
  // Ensure css_content is a string, not undefined
  if (!cssContent || typeof cssContent !== 'string') {
    cssContent = ''
  }
  
  // Extract body content if needed
  if (html && (html.includes('<html') || html.includes('<HTML') || html.trim().startsWith('<body') || html.trim().startsWith('<BODY'))) {
    // Check if HTML starts with <body> tag directly
    if (html.trim().startsWith('<body') || html.trim().startsWith('<BODY')) {
      const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
      if (bodyMatch && bodyMatch[1]) {
        html = bodyMatch[1]
      } else {
        const bodyStart = html.indexOf('<body')
        if (bodyStart !== -1) {
          const bodyTagEnd = html.indexOf('>', bodyStart) + 1
          html = html.substring(bodyTagEnd)
        }
      }
    }
    // Extract body content if HTML has <body> tag (inside full document)
    else if (html.includes('<body') || html.includes('<BODY')) {
      const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
      if (bodyMatch && bodyMatch[1]) {
        html = bodyMatch[1]
      } else {
        const bodyStart = html.indexOf('<body')
        if (bodyStart !== -1) {
          const bodyTagEnd = html.indexOf('>', bodyStart) + 1
          html = html.substring(bodyTagEnd)
        }
      }
    } else {
      // If HTML has <html> but no <body>, try to extract content after </head> or <html>
      if (html.includes('</head>') || html.includes('</HEAD>')) {
        const headEnd = html.indexOf('</head>') + 7
        html = html.substring(headEnd)
      } else if (html.includes('<html') || html.includes('<HTML')) {
        const htmlStart = html.indexOf('<html')
        if (htmlStart !== -1) {
          const htmlTagEnd = html.indexOf('>', htmlStart) + 1
          html = html.substring(htmlTagEnd)
          html = html.replace(/<\/html>$/i, '').trim()
        }
      }
    }
    
    // Remove any remaining head tags and body tags from extracted content
    html = html
      .replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
      .replace(/<body[^>]*>/gi, '')
      .replace(/<\/body>/gi, '')
      .replace(/<meta[^>]*>/gi, '')
      .replace(/<title[^>]*>[\s\S]*?<\/title>/gi, '')
      .replace(/<link[^>]*>/gi, '')
      .trim()
  }
  
  // Remove existing <style> tags from HTML
  if (html) {
    html = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
  }
  
  // Final cleanup - Remove any remaining <body> tags
  if (html) {
    html = html
      .replace(/<body[^>]*>/gi, '')
      .replace(/<\/body>/gi, '')
      .trim()
  }
  
  // Use wrapEmailContent for preview, passing CSS separately
  return wrapEmailContent(html || '', true, cssContent || '')
}

const getPreviewHtml = (content) => {
  if (!content) return ''
  
  // Priority 1: Use template_content directly (full HTML with structure)
  if (content.template_content) {
    return content.template_content
  }
  
  // Priority 2: Use email_content (legacy format)
  if (content.email_content) {
    // Check if it's JSON format
    if (typeof content.email_content === 'string' && content.email_content.startsWith('{')) {
      try {
        const design = JSON.parse(content.email_content)
        if (design.html) {
          return design.html
        }
      } catch (e) {
        // Not JSON, treat as HTML
        return content.email_content
      }
    }
    return content.email_content
  }
  
  // Priority 3: Extract from block_content (EmailBuilder format)
  if (content.block_content) {
    try {
      const design = typeof content.block_content === 'string' 
        ? JSON.parse(content.block_content) 
        : content.block_content
      
      // If design has html property, use it
      if (design.html) {
        return design.html
      }
      
      // Otherwise, extract from blocks
      let html = ''
      design.blocks?.forEach(block => {
        if (block.type === 'text' && block.props?.content) {
          html += block.props.content
        }
      })
      return html || ''
    } catch (e) {
      // If parsing fails, treat as HTML string
      return typeof content.block_content === 'string' ? content.block_content : ''
    }
  }
  
  return typeof content === 'string' ? content : JSON.stringify(content)
}

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
const isTestEmailValid = computed(() => emailPattern.test(testEmailAddress.value))

const wrapEmailContent = (html, forPreview = false, externalCss = '') => {
  // Priority: Use externalCss if provided, otherwise extract from HTML
  let cssContent = (externalCss && typeof externalCss === 'string') ? externalCss : ''
  let htmlBody = html || ''
  
  // Extract CSS from HTML if no external CSS provided
  if (!cssContent && html) {
    const styleMatch = html.match(/<style[^>]*>([\s\S]*?)<\/style>/gi)
    if (styleMatch && styleMatch.length > 0) {
      cssContent = styleMatch.map(match => {
        const contentMatch = match.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
        return contentMatch ? contentMatch[1] : ''
      }).join('\n')
      htmlBody = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    } else {
      htmlBody = html
    }
  } else if (html) {
    htmlBody = html.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
  }
  
  // Clean up HTML body - remove head tags
  htmlBody = htmlBody
    .replace(/<meta[^>]*>/gi, '')
    .replace(/<title[^>]*>[\s\S]*?<\/title>/gi, '')
    .replace(/<link[^>]*>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .trim()
  
  // Create full HTML document
  if (forPreview) {
    const cssStyleTag = (cssContent && typeof cssContent === 'string' && cssContent.trim().length > 0)
      ? `<style type="text/css" id="email-css-content">${cssContent}</style>`
      : ''
    
    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <style type="text/css" id="email-reset-styles">
    html, body { 
      margin: 0; 
      padding: 0; 
      background-color: #ffffff; 
      width: 100%;
      height: 100%;
    }
    * { 
      box-sizing: border-box; 
    }
    table { 
      border-collapse: collapse; 
      mso-table-lspace: 0pt; 
      mso-table-rspace: 0pt; 
    }
    img { 
      border: 0; 
      height: auto; 
      line-height: 100%; 
      outline: none; 
      text-decoration: none; 
      -ms-interpolation-mode: bicubic; 
    }
    a { 
      text-decoration: none; 
    }
  </style>
  ${cssStyleTag}
</head>
<body style="margin: 0; padding: 0; background-color: #ffffff; font-family: Arial, sans-serif;">
  ${htmlBody}
</body>
</html>`
  } else {
    return `<!DOCTYPE html>
<html>
<head>
  <meta charset='utf-8'>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  ${cssContent ? `<style type="text/css">${cssContent}</style>` : ''}
</head>
<body style="margin:0;padding:0;background-color:#ffffff;">
  ${htmlBody}
</body>
</html>`
  }
}

const sendEmail = async (content, recipient) => {
  isSendingEmail.value = true
  try {
    const subject = content?.email_subject || 'Test Email'
    let rawContent = getPreviewHtml(content)
    
    // Get CSS content from content
    const cssContent = content?.css_content || ''
    console.log('🎨 [sendEmail] CSS content check:')
    console.log('   css_content exists:', !!cssContent)
    console.log('   css_content length:', cssContent?.length || 0)
    
    // Remove existing <style> tags from HTML to avoid duplicates
    if (rawContent) {
      rawContent = rawContent.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    }
    
    // Replace placeholders with actual values (handle both with and without spaces)
    rawContent = rawContent.replace(/\{\{\s*full_name\s*\}\}/g, recipient)

    // Replace localhost URLs and relative paths with production domain
    console.log('🔍 [sendEmail] Before replace:', rawContent.substring(0, 200) + '...')

    // Replace absolute localhost URLs
    rawContent = rawContent.replaceAll('http://localhost:8080', 'https://hireos.fastwork.vn')
    rawContent = rawContent.replaceAll('http://localhost:8000', 'https://hireos.fastwork.vn')
    rawContent = rawContent.replaceAll('http://127.0.0.1:8080', 'https://hireos.fastwork.vn')
    rawContent = rawContent.replaceAll('http://127.0.0.1:8000', 'https://hireos.fastwork.vn')

    // Replace relative paths like /files/... with full domain
    rawContent = rawContent.replace(/src="\/files\//g, 'src="https://hireos.fastwork.vn/files/')
    rawContent = rawContent.replace(/href="\/files\//g, 'href="https://hireos.fastwork.vn/files/')

    console.log('✅ [sendEmail] After replace, content length:', rawContent.length)

    // Check if replacement worked
    if (rawContent.includes('localhost')) {
      console.warn('⚠️ WARNING: localhost still found in content after replacement!')
    }

    // Wrap email content with CSS injected into <head>
    const finalContent = wrapEmailContent(rawContent, false, cssContent) // false = for actual email, cssContent = external CSS

    console.log('✅ [sendEmail] Final content length:', finalContent.length)
    console.log('✅ [sendEmail] CSS in content:', finalContent.includes(cssContent?.substring(0, 50) || ''))

    // Get attachments from content
    const attachments = content?.attachments || []
    console.log('📎 [sendEmail] Attachments:', attachments)
    
    // Pass campaign_id và attachments để update status của Mira Campaign Social
    console.log('📧 [sendEmail] Sending test email with campaign_id:', props.name)
    const result = await call('mbw_mira.api.campaign.send_test_email', {
      recipient: recipient,
      subject,
      content: finalContent,
      campaign_id: props.name || null,  // Pass campaign ID nếu có
      attachments: attachments.length > 0 ? attachments : null  // Pass attachments nếu có
    })
    
    console.log('📧 [sendEmail] Test email result:', result)
    console.log('📧 [sendEmail] Campaign ID used:', props.name)

    if (result && result.status === 'success') {
      toast.success(__('The email has been successfully sent.'))
      showTestEmailModal.value = false
    } else {
      toast.error(__('Failed to send email'))
    }
  } catch (error) {
    console.error('Error sending email:', error)
    let errorMessage = __('Failed to send email')
    if (error.message) {
      errorMessage += `: ${error.message}`
    } else if (error.exc_type) {
      errorMessage += `: ${error.exc_type}`
      if (error.exception) {
        errorMessage += ` - ${error.exception}`
      }
    }
    toast.error(errorMessage)
  } finally {
    isSendingEmail.value = false
  }
}

const confirmSendTestEmail = async () => {
  if (!isTestEmailValid.value) {
    toast.error(__('Please enter a valid email address'))
    return
  }

  const content = testEmailContent.value
  if (!content) return

  const scheduleTime = content.schedule_time ? new Date(content.schedule_time) : null
  const now = new Date()

  if (scheduleTime && scheduleTime > now) {
    const delay = scheduleTime.getTime() - now.getTime()
    toast.info(`Email scheduled to be sent at ${formatScheduleTime(content.schedule_time)}`)
    showTestEmailModal.value = false

    setTimeout(() => {
      sendEmail(content, testEmailAddress.value)
    }, delay)
  } else {
    toast.info(__('Sending email...'))
    await sendEmail(content, testEmailAddress.value)
  }
}

const formatScheduleTime = (scheduleTime) => {
  if (!scheduleTime) return ''
  const date = new Date(scheduleTime)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${day}/${month}/${year} ${hours}:${minutes}`
}

</script>

<style scoped>
/* Add any custom styles here */
</style>
