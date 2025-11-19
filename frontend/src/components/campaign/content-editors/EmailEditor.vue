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
    />

    <!-- Email Template Editor Dialog -->
    <Dialog
      v-model="showTemplateDialog"
      :options="{
        title: __('Email Template Editor'),
        size: '7xl'
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

          <!-- Unlayer Email Editor -->
          <div class="relative">
            <!-- Loading Overlay -->
            <div 
              v-if="editorLoading" 
              class="absolute inset-0 bg-white/80 backdrop-blur-sm z-50 flex items-center justify-center rounded-lg"
            >
              <div class="text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-3"></div>
                <p class="text-sm text-gray-600 font-medium">{{ __('Loading email editor...') }}</p>
              </div>
            </div>
            
            <UnlayerEmailEditor
              ref="unlayerEditor"
              v-model="dialogContent"
              min-height="600px"
              @ready="onEditorReady"
            />
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
import { FeatherIcon, Dialog, Button, FileUploader, FormControl, Autocomplete } from 'frappe-ui'
import { useToast } from '../../../composables/useToast'
import EmailTemplateSelectorModal from '@/components/Modals/EmailTemplateSelectorModal.vue'
import { showSettings, activeSettingsPage } from '@/composables/settings'
import UnlayerEmailEditor from '@/components/Settings/MiraEmailTemplate/UnlayerEmailEditor.vue'

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
const unlayerEditor = ref(null)
const selectedDialogField = ref(null)
const editorLoading = ref(false)
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

// Open template editor dialog
const openTemplateEditor = () => {
  if (props.readonly) return
  
  editorLoading.value = true
  
  // Load existing design if available
  if (localContent.value.email_content) {
    try {
      // Parse if it's JSON string, otherwise use as is
      const design = typeof localContent.value.email_content === 'string' 
        ? JSON.parse(localContent.value.email_content)
        : localContent.value.email_content
      
      // Validate it's a proper Unlayer design
      if (design && design.body && Array.isArray(design.body.rows)) {
        dialogContent.value = design
      } else {
        console.warn('Email content is not valid Unlayer format, starting with empty canvas')
        dialogContent.value = null
      }
    } catch (e) {
      console.warn('Failed to parse email_content as JSON, starting with empty canvas:', e)
      dialogContent.value = null
      toast.info(__('Starting with blank canvas. Previous content was in old format.'))
    }
  } else {
    dialogContent.value = null
  }
  
  showTemplateDialog.value = true
}

// Save template from dialog
const saveTemplate = async () => {
  if (!unlayerEditor.value) {
    toast.error(__('Editor not ready'))
    return
  }
  
  try {
    // Export design from Unlayer
    const design = await unlayerEditor.value.saveDesign()
    
    // Save as JSON string for backend
    localContent.value.email_content = JSON.stringify(design)
    
    showTemplateDialog.value = false
    toast.success(__('Email template saved successfully'))
  } catch (error) {
    console.error('Failed to save template:', error)
    toast.error(__('Failed to save template'))
  }
}

// Generate content with AI (fake for now)
const generateWithAI = async () => {
  toast.info(__('AI generation will be available soon'))
  aiGenerating.value = false
}

// Use predefined template - open selector modal
const useTemplate = () => {
  // Temporarily close editor dialog to prevent modal conflicts
  showTemplateDialog.value = false
  
  // Open selector modal
  nextTick(() => {
    showTemplateSelectorModal.value = true
  })
}

// Apply selected template
const applyTemplate = (template) => {
  editorLoading.value = true
  
  if (template.subject) {
    localContent.value.email_subject = template.subject
  }
  
  let templateApplied = false
  
  // Use email_design_json field (Unlayer design) instead of message (HTML export)
  if (template.email_design_json) {
    try {
      // Parse template design JSON if it's string
      const design = typeof template.email_design_json === 'string'
        ? JSON.parse(template.email_design_json)
        : template.email_design_json
      
      // Validate it's a proper Unlayer design (must have body.rows)
      if (design && design.body && Array.isArray(design.body.rows)) {
        dialogContent.value = design
        templateApplied = true
      } else {
        console.warn('Template is not valid Unlayer format (missing body.rows)')
      }
    } catch (e) {
      console.warn('Template email_design_json is not valid JSON:', e)
    }
  }
  
  // If template couldn't be applied (old format or missing design JSON)
  if (!templateApplied) {
    dialogContent.value = null
    toast.warning(__('This template does not have a valid design. Please create a new design with the visual editor.'))
    editorLoading.value = false
  }
  
  showTemplateSelectorModal.value = false
  
  // Ensure editor dialog stays open
  nextTick(() => {
    showTemplateDialog.value = true
  })
  
  if (templateApplied) {
    toast.success(__('Template applied successfully'))
  }
}

// Open template settings
const openTemplateSettings = () => {
  // Close both modals
  showTemplateSelectorModal.value = false
  showTemplateDialog.value = false
  
  // Open settings dialog and set active page to Email Templates
  nextTick(() => {
    showSettings.value = true
    activeSettingsPage.value = 'Email Templates'
  })
}

// Get preview content (export HTML from Unlayer design)
const getPreviewContent = (content) => {
  if (!content) return ''
  
  try {
    // If content is Unlayer design JSON, extract text preview
    const design = typeof content === 'string' ? JSON.parse(content) : content
    
    if (design.body && design.body.rows) {
      // Extract text from Unlayer design structure
      let previewText = ''
      design.body.rows.forEach(row => {
        row.columns?.forEach(column => {
          column.contents?.forEach(contentItem => {
            if (contentItem.type === 'text' && contentItem.values?.text) {
              // Strip HTML tags for preview
              const div = document.createElement('div')
              div.innerHTML = contentItem.values.text
              previewText += div.textContent + ' '
            }
          })
        })
      })
      
      // Limit preview length
      if (previewText.length > 200) {
        return previewText.substring(0, 200) + '...'
      }
      return previewText || '<p>Email template created with visual editor</p>'
    }
  } catch (e) {
    // If parsing fails, treat as plain text/HTML
    console.warn('Failed to parse content as Unlayer design:', e)
  }
  
  // Fallback for non-JSON content
  if (content.length > 200) {
    return content.substring(0, 200) + '...'
  }
  return content
}

// Editor ready callback
const onEditorReady = (editor) => {
  // Hide loading indicator when editor is fully ready
  setTimeout(() => {
    editorLoading.value = false
  }, 100)
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
  
  toast.info(__(`Copy this variable: {{ ${option.value} }} and paste it in the editor`))
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
