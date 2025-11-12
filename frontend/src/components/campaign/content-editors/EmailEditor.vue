<template>
  <div class="email-editor space-y-6">


    <!-- Email Form -->
    <div class="space-y-6">
      <!-- Subject -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __("Email Subject") }} <span class="text-red-500">*</span>
        </label>
        <!-- <input
          v-model="localContent.email_subject"
          type="text"
          :placeholder="__('Enter email subject line...')"
          :disabled="readonly"
          class="block w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
        />   -->
        <FormControl 
          v-model="localContent.email_subject"
          :disabled="readonly"
          :placeholder="__('Enter email subject line...')"
          :type="'text'"
          class="block w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          :class="{ 'bg-gray-100 cursor-not-allowed': readonly }"
        />
        <p class="mt-1 text-xs text-gray-500">
          {{ __("Keep it concise and compelling (recommended: 30-50 characters)") }}
        </p>
      </div>

      <!-- Email Template Editor -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __("Email Content") }} <span class="text-red-500">*</span>
        </label>
        
        <div class="border border-gray-300 rounded-lg p-4 bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors"
             @click="openTemplateEditor"
             :class="{ 'cursor-not-allowed bg-gray-200': readonly }">
          <div class="flex items-center justify-center py-8">
            <div class="text-center">
              <FeatherIcon name="edit-3" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p class="text-gray-600 font-medium">
                {{ localContent.email_content ? __("Edit Email Template") : __("Create Email Template") }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {{ __("Click to open email template editor") }}
              </p>
            </div>
          </div>
          
          <!-- Content Preview -->
          <div v-if="localContent.email_content" class="mt-4 p-3 bg-white rounded border">
            <div class="text-xs text-gray-500 mb-2">{{ __("Preview:") }}</div>
            <div 
              class="prose prose-sm max-w-none text-gray-700 line-clamp-3 overflow-hidden"
              v-html="getPreviewContent(localContent.email_content)"
            >
            </div>
          </div>
        </div>
      </div>

      <!-- File Attachments -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
          {{ __("File Attachments") }}
        </label>
        
        <!-- Uploaded Files List -->
        <div v-if="localContent.attachments && localContent.attachments.length > 0" class="mb-4 space-y-2">
          <div
            v-for="(file, index) in localContent.attachments"
            :key="index"
            class="flex items-center justify-between p-3 bg-gray-50 border border-gray-200 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <FeatherIcon name="file" class="h-5 w-5 text-gray-500" />
              <div class="min-w-0">
                <a :href="file.file_url" target="_blank"
                   class="text-sm font-medium text-gray-900 hover:text-blue-600 underline block truncate">
                  {{ file.file_name }}
                </a>
                <div class="text-xs text-gray-500 mt-1">
                  {{ formatFileSize(file.file_size) }}
                </div>
              </div>
            </div>
            <button
              v-if="!readonly"
              @click="removeAttachment(index)"
              class="text-red-500 hover:text-red-700 p-1"
              type="button"
            >
              <FeatherIcon name="x" class="h-4 w-4" />
            </button>
          </div>
        </div>

        <!-- File Uploader -->
        <FileUploader
          v-if="!readonly"
          :fileTypes="['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']"
          :upload-args="{
            doctype: 'Mira Campaign',
            docname: 'temp',
            private: false,
          }"
          @success="handleFileUploadSuccess"
          @error="handleFileUploadError"
        >
          <template v-slot="{ openFileSelector }">
            <button
              @click="openFileSelector()"
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              type="button"
            >
              <FeatherIcon name="paperclip" class="h-4 w-4 mr-2" />
              {{ __("Add File Attachment") }}
            </button>
          </template>
        </FileUploader>
      </div>
    </div>

    <!-- Email Template Selector Modal -->
    <EmailTemplateSelectorModal
      v-model="showTemplateSelectorModal"
      doctype="Mira Campaign"
      @apply="applyTemplate"
      @openSettings="openTemplateSettings"
      @close="handleSelectorClose"
    />

    <!-- Email Template Editor Dialog -->
    <Dialog
      v-model="showTemplateDialog"
      :options="{
        title: __('Email Template Editor'),
        size: 'xl'
      }"
    >
      <template #body-content>
        <div class="space-y-6">
          <!-- Template Options -->
          <div class="flex items-center justify-between">
            <h4 class="text-lg font-semibold">{{ __("Create Email Template") }}</h4>
            <div class="flex space-x-2">
              <Button
                :label="__('Generate with AI')"
                icon-left="zap"
                variant="outline"
                :loading="aiGenerating"
                @click="generateWithAI"
              />
              <Button
                :label="__('Use Template')"
                icon-left="layout"
                variant="outline"
                @click="useTemplate"
              />
            </div>
          </div>

          <!-- Insert Fields Autocomplete -->
          <div class="flex items-center justify-between mb-2">
            <label class="text-sm font-medium text-gray-700">
              {{ __("Insert Fields") }}
            </label>
            <Autocomplete
              v-model="selectedDialogField"
              :options="fieldAutocompleteOptions"
              :placeholder="__('Search fields...')"
              class="w-64"
            >
              <template #target="{ togglePopover }">
                <Button
                  :label="__('Insert Field')"
                  icon-left="plus-circle"
                  variant="outline"
                  size="sm"
                  @click="togglePopover"
                />
              </template>
            </Autocomplete>
          </div>

          <!-- Rich Text Editor -->
          <div>
            <TextEditor
              ref="dialogTextarea"
              editor-class="prose-sm min-h-[20rem] border rounded-lg border-gray-300 p-3"
              :content="dialogContent"
              :placeholder="emailPlaceholder"
              @change="(val) => dialogContent = val"
              :bubbleMenu="true"
              :fixedMenu="true"
            />
            <div class="flex justify-between items-center mt-2">
              <p class="text-xs text-gray-500">
                {{ __("Use variables like [Candidate Name], [Job Title], [Company]") }}
              </p>
              <span class="text-xs text-gray-500">
                {{ getTextLength(dialogContent) }} {{ __("characters") }}
              </span>
            </div>
          </div>
        </div>
      </template>
      
      <template #actions>

        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" theme="gray" @click="showTemplateDialog = false">
            {{ __("Cancel") }}
          </Button>
          <Button variant="solid" theme="gray" @click="saveTemplate">
          {{ __("Save Template") }}
        </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import { FeatherIcon, Dialog, Button, FileUploader, TextEditor, FormControl, Autocomplete } from 'frappe-ui'
import { useToast } from '../../../composables/useToast'
import EmailTemplateSelectorModal from '@/components/Modals/EmailTemplateSelectorModal.vue'
import { showSettings, activeSettingsPage } from '@/composables/settings'

const props = defineProps({
  content: { type: Object, default: () => ({}) },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:content', 'save', 'preview'])

const localContent = ref({
  email_subject: '',
  email_content: '',
  attachments: [],
  ...props.content
})

const showTemplateDialog = ref(false)
const showTemplateSelectorModal = ref(false)
const dialogContent = ref('')
const aiGenerating = ref(false)
const dialogTextarea = ref(null)
const selectedDialogField = ref(null)
const toast = useToast()

const __ = (text) => text

// Talent & Campaign fields for insertion - grouped
const talentFieldsGrouped = [
  {
    group: 'Campaign Info',
    items: [
      { fieldname: 'campaign_name', label: 'Campaign Name' },
      { fieldname: 'campaign_type', label: 'Campaign Type' },
      { fieldname: 'campaign_description', label: 'Campaign Description' },
    ]
  },
  {
    group: 'Personal Info',
    items: [
      { fieldname: 'full_name', label: 'Full Name' },
      { fieldname: 'email', label: 'Email' },
      { fieldname: 'phone', label: 'Phone' },
      { fieldname: 'gender', label: 'Gender' },
      { fieldname: 'date_of_birth', label: 'Date of Birth' },
      { fieldname: 'current_city', label: 'City/Address' },
    ]
  },
  {
    group: 'Professional',
    items: [
      { fieldname: 'latest_title', label: 'Latest Title' },
      { fieldname: 'latest_company', label: 'Latest Company' },
      { fieldname: 'skills', label: 'Skills' },
      { fieldname: 'total_years_of_experience', label: 'Years of Experience' },
      { fieldname: 'highest_education', label: 'Highest Education' },
    ]
  },
  {
    group: 'Career Preferences',
    items: [
      { fieldname: 'desired_role', label: 'Desired Role' },
      { fieldname: 'domain_expertise', label: 'Domain Expertise' },
      { fieldname: 'current_salary', label: 'Current Salary' },
      { fieldname: 'expected_salary', label: 'Expected Salary' },
      { fieldname: 'preferred_work_model', label: 'Work Model' },
      { fieldname: 'availability_date', label: 'Availability Date' },
    ]
  },
  {
    group: 'Status & Social',
    items: [
      { fieldname: 'current_status', label: 'Current Status' },
      { fieldname: 'cultural_fit', label: 'Cultural Fit' },
      { fieldname: 'internal_rating', label: 'Internal Rating' },
      { fieldname: 'priority_level', label: 'Priority' },
      { fieldname: 'linkedin_profile', label: 'LinkedIn Profile' },
      { fieldname: 'facebook_profile', label: 'Facebook Profile' },
      { fieldname: 'zalo_profile', label: 'Zalo Profile' },
    ]
  },
]

// Field autocomplete options for dialog
const fieldAutocompleteOptions = computed(() => {
  return talentFieldsGrouped.map(group => ({
    group: group.group,
    items: group.items.map(field => ({
      label: field.label,
      value: field.fieldname,
      description: `{{ ${field.fieldname} }}`,
    }))
  }))
})

const emailPlaceholder = `<p>Hello {{ full_name }},</p>
<p>We hope this email finds you well. We have an exciting opportunity at {{ latest_company }} that we believe would be a perfect fit for your skills and experience.</p>
<p><strong>Position:</strong> {{ latest_title }}<br>
<strong>Location:</strong> Ho Chi Minh City<br>
<strong>Type:</strong> Full-time</p>
<p>We would love to discuss this opportunity with you further. Are you available for a brief call this week?</p>
<p>Best regards,<br>
HR Team<br>
{{ latest_company }}</p>`

// Open template editor dialog
const openTemplateEditor = () => {
  if (props.readonly) return
  
  dialogContent.value = localContent.value.email_content || ''
  showTemplateDialog.value = true
}

// Save template from dialog
const saveTemplate = () => {
  localContent.value.email_content = dialogContent.value
  showTemplateDialog.value = false
}

// Generate content with AI (fake for now)
const generateWithAI = async () => {
  aiGenerating.value = true
  
  // Simulate AI generation
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  const aiContent = `<p>Hello {{ full_name }},</p>

<p>I hope this message finds you well. I'm reaching out because we have an exciting opportunity at {{ latest_company }} that perfectly matches your background and expertise.</p>

<p>We're currently looking for a talented {{ latest_title }} to join our dynamic team. Based on your experience and skills, I believe this role could be an excellent fit for your career growth.</p>

<p><strong>Here's what makes this opportunity special:</strong></p>
<ul>
<li>Competitive salary and comprehensive benefits</li>
<li>Flexible working arrangements</li>
<li>Opportunity to work with cutting-edge technology</li>
<li>Collaborative and innovative work environment</li>
<li>Clear career progression path</li>
</ul>

<p>I'd love to schedule a brief call to discuss this opportunity in more detail. Are you available for a 15-minute conversation this week?</p>

<p>Looking forward to hearing from you.</p>

<p>Best regards,<br>
{{ full_name }}<br>
HR Team - {{ latest_company }}</p>`

  dialogContent.value = aiContent
  aiGenerating.value = false
}

// Use predefined template - open selector modal
const useTemplate = () => {
  showTemplateSelectorModal.value = true
}

// Apply selected template
const applyTemplate = (template) => {
  if (template.subject) {
    localContent.value.email_subject = template.subject
  }
  if (template.message) {
    dialogContent.value = template.message
  }
  showTemplateSelectorModal.value = false
  
  // Ensure editor dialog stays open
  nextTick(() => {
    showTemplateDialog.value = true
  })
  
  toast.success(__('Template applied successfully'))
}

// Open template settings
const openTemplateSettings = () => {
  // Open settings dialog and set active page to Email Templates
  showSettings.value = true
  activeSettingsPage.value = 'Email Templates'
}

// Handle selector modal close
const handleSelectorClose = () => {
  // Ensure editor dialog stays open when selector closes
  nextTick(() => {
    showTemplateDialog.value = true
  })
}

// Get preview content (strip HTML for preview or limit length)
const getPreviewContent = (content) => {
  if (!content) return ''
  // Limit content length for preview
  if (content.length > 200) {
    return content.substring(0, 200) + '...'
  }
  return content
}

// Watch for field selection in dialog
watch(selectedDialogField, (newValue) => {
  if (newValue) {
    insertFieldToDialog(newValue)
    // Reset selection after insert
    setTimeout(() => {
      selectedDialogField.value = null
    }, 100)
  }
})

// Insert field to dialog editor
const insertFieldToDialog = (option) => {
  if (!option) return
  
  const fieldPlaceholder = `{{ ${option.value} }}`
  
  // For TextEditor, we need to insert HTML content
  if (dialogTextarea.value?.editor) {
    dialogTextarea.value.editor.chain().focus().insertContent(fieldPlaceholder).run()
  } else {
    // Fallback: append to content
    dialogContent.value += fieldPlaceholder
  }
  
  toast.success(`Inserted field: ${option.label}`)
}

// Insert variable in dialog textarea
const insertVariableInDialog = (variable) => {
  if (!dialogTextarea.value) return
  
  // For TextEditor, we need to insert HTML content
  const editor = dialogTextarea.value.editor
  if (editor) {
    editor.chain().focus().insertContent(variable).run()
  } else {
    // Fallback: append to content
    dialogContent.value = (dialogContent.value || '') + variable
  }
}

// Get text length from HTML content
const getTextLength = (htmlContent) => {
  if (!htmlContent) return 0
  // Strip HTML tags to get text length
  const div = document.createElement('div')
  div.innerHTML = htmlContent
  return div.textContent?.length || 0
}

// Handle file upload success
const handleFileUploadSuccess = (file) => {
  // Validate file size (10MB = 10 * 1024 * 1024 bytes)
  const maxSize = 10 * 1024 * 1024
  if (file.file_size > maxSize) {
    toast.error(__('File size must be less than 10MB'))
    return
  }
  
  if (!localContent.value.attachments) {
    localContent.value.attachments = []
  }
  
  localContent.value.attachments.push({
    file_name: file.file_name,
    file_url: file.file_url,
    file_size: file.file_size
  })
}

// Handle file upload error
const handleFileUploadError = (error) => {
  console.error('File upload error:', error)
  toast.error(__('Failed to upload file. Please try again.'))
}

// Remove attachment
const removeAttachment = (index) => {
  localContent.value.attachments.splice(index, 1)
}

// Format file size
const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

watch(localContent, (newContent) => {
  emit('update:content', newContent)
}, { deep: true })

watch(() => props.content, (newContent) => {
  localContent.value = { ...localContent.value, ...newContent }
}, { deep: true })
</script>
