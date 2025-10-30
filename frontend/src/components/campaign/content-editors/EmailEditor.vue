<template>
  <div class="email-editor space-y-6">
    <!-- Header -->
    <div class="text-center py-4">
      <div class="bg-blue-100 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
        <FeatherIcon name="mail" class="h-8 w-8 text-blue-600" />
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-2">{{ __("Email Campaign Editor") }}</h3>
      <p class="text-gray-600">{{ __("Create engaging email content for your campaign") }}</p>
    </div>

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
            <div class="text-sm text-gray-700 line-clamp-3">
              {{ localContent.email_content.substring(0, 150) }}{{ localContent.email_content.length > 150 ? '...' : '' }}
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
                variant="outline"
                @click="generateWithAI"
                :loading="aiGenerating"
              >
              <div class="flex items-center">

                  <FeatherIcon name="zap" class="h-4 w-4 mr-2" />
                  {{ __("Generate with AI") }}
              </div>
              </Button>
              <Button
                variant="outline"
                @click="useTemplate"
              >
              <div class="flex items-center">

                <FeatherIcon name="layout" class="h-4 w-4 mr-2" />
                {{ __("Use Template") }}
              </div>
              </Button>
            </div>
          </div>

          <!-- Variable Buttons -->
          <div class="flex flex-wrap gap-2 p-3 bg-gray-50 rounded-lg">
            <span class="text-xs font-medium text-gray-700 mr-2">{{ __("Variables:") }}</span>
            <button
              v-for="variable in variables"
              :key="variable.key"
              @click="insertVariableInDialog(variable.value)"
              class="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
              type="button"
            >
              {{ variable.label }}
            </button>
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
import { ref, watch, nextTick } from 'vue'
import { FeatherIcon, Dialog, Button, FileUploader, TextEditor, FormControl } from 'frappe-ui'
import { useToast } from '../../../composables/useToast'

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
const dialogContent = ref('')
const aiGenerating = ref(false)
const dialogTextarea = ref(null)
const toast = useToast()

const __ = (text) => text

const variables = [
  { key: 'name', label: __('Name'), value: '[Candidate Name]' },
  { key: 'job', label: __('Job Title'), value: '[Job Title]' },
  { key: 'company', label: __('Company'), value: '[Company]' }
]

const emailPlaceholder = `Hello [Candidate Name],

We hope this email finds you well. We have an exciting opportunity at [Company] that we believe would be a perfect fit for your skills and experience.

Position: [Job Title]
Location: Ho Chi Minh City
Type: Full-time

We would love to discuss this opportunity with you further. Are you available for a brief call this week?

Best regards,
HR Team
[Company]`

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
  
  const aiContent = `Hello [Candidate Name],

I hope this message finds you well. I'm reaching out because we have an exciting opportunity at [Company] that perfectly matches your background and expertise.

We're currently looking for a talented [Job Title] to join our dynamic team. Based on your experience and skills, I believe this role could be an excellent fit for your career growth.

Here's what makes this opportunity special:
• Competitive salary and comprehensive benefits
• Flexible working arrangements
• Opportunity to work with cutting-edge technology
• Collaborative and innovative work environment
• Clear career progression path

I'd love to schedule a brief call to discuss this opportunity in more detail. Are you available for a 15-minute conversation this week?

Looking forward to hearing from you.

Best regards,
[Your Name]
HR Team - [Company]`

  dialogContent.value = aiContent
  aiGenerating.value = false
}

// Use predefined template
const useTemplate = () => {
  dialogContent.value = emailPlaceholder
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
