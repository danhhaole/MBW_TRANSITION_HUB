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
                {{ hasAnyContent ? __("Edit Email Template") : __("Create Email Template") }}
              </p>
              <p class="text-xs text-gray-500 mt-1">
                {{ __("Click to open email template editor") }}
              </p>
            </div>
          </div>

          <!-- Content Preview -->
          <div v-if="hasAnyContent" class="mt-4 bg-white rounded border">
            <div class="text-xs text-gray-500 mb-2 px-3 pt-3">{{ __("Preview:") }}</div>
            <div class="email-preview-wrapper" style="max-width: 100%; max-height: 600px; overflow-y: auto; overflow-x: hidden; border: 1px solid #e5e7eb; border-radius: 8px; background: #f4f4f4; padding: 8px;">
              <iframe
                ref="previewIframe"
                :srcdoc="previewHtml"
                style="width: 100%; min-height: 400px; border: none; background: #ffffff; border-radius: 4px; display: block;"
                frameborder="0"
                scrolling="yes"
              ></iframe>
            </div>
          </div>
        </div>
      </div>

      <!-- Attachments and Actions Footer -->
      <div class="pt-4 mt-4 border-t">
        <div class="flex justify-between items-center">
          <!-- Left Side: File Attachments -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __("File Attachments") }}
            </label>
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

          <!-- Right Side: Action Slot -->
          <div>
            <slot name="actions"></slot>
          </div>
        </div>

        <!-- Uploaded Files List -->
        <div v-if="localContent.attachments && localContent.attachments.length > 0" class="mt-4 space-y-2">
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
        title: __('Create Email Template'),
        size: '7xl'
      }"
    >
      <template #body-content>
        <div class="space-y-6">
          <!-- Template Options -->
          <div class="flex items-center justify-between">
            <h4 class="text-lg font-semibold"></h4>
            <div class="flex space-x-2">
              <Button
                :label="__('Use Template')"
                icon-left="layout"
                variant="outline"
                @click="useTemplate"
              />
            </div>
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

            <EmailBuilder
              ref="emailBuilderEditor"
              v-model="dialogContent"
              :initial-content="getInitialContentForEditor"
              :initial-css="dialogCss"
              height="600px"
              @ready="onEditorReady"
              @css-change="handleCssChange"
            />

            <!-- OLD Unlayer Editor - COMMENTED OUT -->
            <!--
            <UnlayerEmailEditor
              ref="unlayerEditor"
              v-model="dialogContent"
              min-height="600px"
              @ready="onEditorReady"
            />
            -->
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
import EmailBuilder from '@/components/Settings/MiraEmailTemplate/EmailBuilder/EmailBuilder.vue'
import {
  convertEmailBuilderToHtml,
  convertHtmlToEmailBuilder,
  isEmailBuilderFormat,
  isHtmlFormat
} from '@/utils/emailBuilderConverter.js'
import { getDefaultEmailTemplate, getDefaultEmailTemplateCss } from '@/utils/emailTemplates'
// OLD IMPORT - COMMENTED OUT
// import UnlayerEmailEditor from '@/components/Settings/MiraEmailTemplate/UnlayerEmailEditor.vue'

const props = defineProps({
  content: { type: Object, default: () => ({}) },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:content', 'save', 'preview'])

const localContent = ref({
  email_subject: '',
  email_content: '',        // Legacy field (for backward compatibility)
  block_content: '',        // EmailBuilder format for editing
  template_content: '',     // HTML format for campaign storage/rendering
  mjml_content: '',         // MJML format for email services
  css_content: '',          // CSS content for styling
  attachments: [],
  ...props.content
})

const showTemplateDialog = ref(false)
const showTemplateSelectorModal = ref(false)
const dialogContent = ref('')
// IMPORTANT: Initialize dialogCss from localContent.css_content if available
const dialogCss = ref(localContent.value.css_content || '')
const aiGenerating = ref(false)
const emailBuilderEditor = ref(null)
// OLD REF - COMMENTED OUT
// const unlayerEditor = ref(null)
const selectedDialogField = ref(null)
const editorLoading = ref(false)
const previewIframe = ref(null)
const toast = useToast()

const __ = (text) => text

// Computed property to get initial content for EmailBuilder
const getInitialContentForEditor = computed(() => {
  // Priority 1: Use dialogContent if it's a string (HTML)
  if (typeof dialogContent.value === 'string' && dialogContent.value.trim() !== '') {
    return dialogContent.value
  }
  
  // Priority 2: Convert dialogContent object to HTML if it exists
  if (typeof dialogContent.value === 'object' && dialogContent.value !== null) {
    // IMPORTANT: Extract CSS from object if available and set dialogCss
    if (dialogContent.value.css && dialogContent.value.css.trim() !== '') {
      dialogCss.value = dialogContent.value.css
    }
    
    // IMPORTANT: If object has html field and blocks is empty, use html directly
    if (dialogContent.value.html && dialogContent.value.html.trim() !== '') {
      const blocksCount = dialogContent.value.blocks?.length || 0
      if (blocksCount === 0) {
        return dialogContent.value.html
      }
    }
    
    // Try to convert from blocks if blocks exist
    try {
      const htmlFormat = convertEmailBuilderToHtml(dialogContent.value)
      const html = htmlFormat.html || ''
      if (html && html.trim() !== '' && !html.includes('No content')) {
        return html
      } else if (dialogContent.value.html && dialogContent.value.html.trim() !== '') {
        return dialogContent.value.html
      }
    } catch (e) {
      if (dialogContent.value.html && dialogContent.value.html.trim() !== '') {
        return dialogContent.value.html
      }
    }
  }
  
  // Priority 3: Fallback to localContent.template_content
  const fallback = localContent.value.template_content || ''
  if (fallback && fallback.trim() !== '') {
    return fallback
  }
  
  return ''
})

// Check if there's any content to preview
const hasAnyContent = computed(() => {
  return !!(
    localContent.value.block_content?.trim() ||
    localContent.value.template_content?.trim() ||
    localContent.value.email_content?.trim()
  )
})

// Get content for preview (prioritize block_content)
const getContentForPreview = () => {
  return localContent.value.block_content ||
         localContent.value.template_content ||
         localContent.value.email_content ||
         ''
}

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

  // IMPORTANT: Load CSS first from localContent.css_content to ensure it's available
  if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
    dialogCss.value = localContent.value.css_content
  }

  // Check if template_content has actual HTML elements (not just CSS/meta)
  const hasHtmlElements = (content) => {
    if (!content) return false
    // Remove CSS, meta, and whitespace, then check if there's actual HTML content
    const cleanContent = content
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<meta[^>]*>/gi, '')
      .replace(/\s+/g, ' ')
      .trim()
    return cleanContent.length > 100 && /<[^>]+>/.test(cleanContent)
  }

  if (localContent.value.block_content && localContent.value.block_content.trim()) {
    try {
      const blockData = JSON.parse(localContent.value.block_content)
      
      // IMPORTANT: Load block_content even if blocks is empty, as long as it has html or css
      const hasBlocks = blockData?.blocks && Array.isArray(blockData.blocks) && blockData.blocks.length > 0
      const hasHtml = blockData?.html && blockData.html.trim() !== ''
      const hasCss = blockData?.css && blockData.css.trim() !== ''
      
      if (hasBlocks || hasHtml || hasCss) {
        // IMPORTANT: Always load CSS from blockData.css first (highest priority)
        if (blockData.css && blockData.css.trim() !== '') {
          dialogCss.value = blockData.css
          if (!localContent.value.css_content || localContent.value.css_content.trim() === '') {
            localContent.value.css_content = blockData.css
          }
        } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
          dialogCss.value = localContent.value.css_content
          blockData.css = localContent.value.css_content
          localContent.value.block_content = JSON.stringify(blockData)
        }
        
        // IMPORTANT: Use blockData.html if available, otherwise use blockData object
        if (hasHtml) {
          dialogContent.value = blockData.html
        } else {
          dialogContent.value = blockData
        }
        
        // IMPORTANT: Ensure CSS is set from blockData if available
        if (blockData.css && blockData.css.trim() !== '') {
          dialogCss.value = blockData.css
        } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
          dialogCss.value = localContent.value.css_content
        }
        
        showTemplateDialog.value = true
        return
      }
    } catch (e) {
      console.error('[EmailEditor] Error parsing block_content:', e)
    }
  }

  // Fallback to JSON formats
  const contentToLoad = localContent.value.block_content || localContent.value.email_content

  if (contentToLoad) {
    try {
      // Check if it's JSON format first
      if (typeof contentToLoad === 'string' && contentToLoad.trim().startsWith('{')) {
        const design = JSON.parse(contentToLoad)

        // Extract HTML content from blocks if available
        if (design.blocks && design.blocks.length > 0) {
          const htmlBlock = design.blocks.find(block => block.type === 'html' && block.props && block.props.content)
          if (htmlBlock && htmlBlock.props.content) {
            dialogContent.value = htmlBlock.props.content

            // Get CSS - Priority: css_content > extract from HTML
            let finalCss = localContent.value.css_content || ''
            if (!finalCss && localContent.value.template_content) {
              const cssMatch = localContent.value.template_content.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
              if (cssMatch && cssMatch[1]) {
                finalCss = cssMatch[1].trim()
              }
            }
            if (!finalCss && htmlBlock.props.content) {
              const htmlCssMatch = htmlBlock.props.content.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
              if (htmlCssMatch && htmlCssMatch[1]) {
                finalCss = htmlCssMatch[1].trim()
              }
            }
            dialogCss.value = finalCss
            showTemplateDialog.value = true
            return
          }
        }

        // Check for EmailBuilder format
        if (design && design.blocks && Array.isArray(design.blocks)) {
          // Priority 1: Use design.css if available
          if (design.css && design.css.trim() !== '') {
            dialogCss.value = design.css
          } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
            dialogCss.value = localContent.value.css_content
          }

          // If design.html exists, use it for GrapesJS
          if (design.html && design.html.trim() !== '') {
            dialogContent.value = design.html
            if (design.css && design.css.trim() !== '') {
              dialogCss.value = design.css
            } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
              dialogCss.value = localContent.value.css_content
            }
          }
          // If blocks exist, extract HTML content
          else if (design.blocks.length > 0) {
            const htmlContent = design.blocks
              .filter(block => block.type === 'html' && block.props && block.props.content)
              .map(block => block.props.content)
              .join('')

            if (htmlContent) {
              dialogContent.value = htmlContent

              // Get CSS
              let finalCss = localContent.value.css_content || ''
              if (!finalCss && localContent.value.template_content) {
                const cssMatch = localContent.value.template_content.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
                if (cssMatch && cssMatch[1]) {
                  finalCss = cssMatch[1].trim()
                }
              }
              if (!finalCss && htmlContent) {
                const htmlCssMatch = htmlContent.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
                if (htmlCssMatch && htmlCssMatch[1]) {
                  finalCss = htmlCssMatch[1].trim()
                }
              }
              if (finalCss && finalCss.trim() !== '' && !dialogCss.value) {
                dialogCss.value = finalCss
              }
            }
          }
          // If no blocks and no design.html, set dialogContent to design object
          else if (!design.html) {
            dialogContent.value = design
            if (design.css && design.css.trim() !== '') {
              dialogCss.value = design.css
            } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
              dialogCss.value = localContent.value.css_content
            }
          }
        }
        // OLD: Validate it's a proper Unlayer design (backward compatibility)
        else if (design && design.body && Array.isArray(design.body.rows)) {
          dialogContent.value = design
          toast.info(__('Loading legacy email format. Consider recreating with new editor.'))
        } else {
          dialogContent.value = null
        }
      }
      // Handle HTML format - convert to EmailBuilder
      else if (isHtmlFormat(contentToLoad)) {
        const converted = convertHtmlToEmailBuilder(contentToLoad)
        dialogContent.value = converted
        
        if (converted && converted.css && converted.css.trim() !== '') {
          dialogCss.value = converted.css
        } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
          dialogCss.value = localContent.value.css_content
        }
      } else {
        dialogContent.value = null
        toast.info(__('Starting with blank canvas. Previous content was in old format.'))
      }
    } catch (error) {
      console.error('[EmailEditor] Error parsing content:', error)
      dialogContent.value = null
    }
  } else {
    // IMPORTANT: If no block_content or email_content, use template_content if available
    if (localContent.value.template_content && localContent.value.template_content.trim() !== '') {
      dialogContent.value = localContent.value.template_content
    } else {
      // No content found - load default template for new email
      const defaultTemplate = getDefaultEmailTemplate()
      const defaultCss = getDefaultEmailTemplateCss()
      
      dialogContent.value = defaultTemplate
      dialogCss.value = defaultCss
      
      localContent.value.template_content = defaultTemplate
      localContent.value.css_content = defaultCss
    }
  }

  // IMPORTANT: Ensure CSS is always set - check multiple sources
  // Priority 1: dialogContent object css field (if dialogContent is object)
  if (typeof dialogContent.value === 'object' && dialogContent.value !== null) {
    if (dialogContent.value.css && dialogContent.value.css.trim() !== '') {
      dialogCss.value = dialogContent.value.css
    }
  }
  
  // Priority 2: localContent.css_content (fallback)
  if (!dialogCss.value && localContent.value.css_content && localContent.value.css_content.trim() !== '') {
    dialogCss.value = localContent.value.css_content
  }

  showTemplateDialog.value = true
}

// Save template from dialog
async function saveTemplate() {
  console.log('💾 [EmailEditor] ========== SAVE TEMPLATE START ==========')
  
  if (!emailBuilderEditor.value) {
    toast.error(__('Editor not ready'));
    return;
  }

  try {
    const editorInstance = emailBuilderEditor.value.editor || emailBuilderEditor.value;

    // Log current CSS state
    console.log('🎨 [EmailEditor] Current CSS state before save:')
    console.log('   dialogCss.value exists:', !!dialogCss.value)
    console.log('   dialogCss.value length:', dialogCss.value?.length || 0)
    console.log('   dialogCss.value preview:', dialogCss.value?.substring(0, 200) + '...')
    console.log('   localContent.value.css_content exists:', !!localContent.value.css_content)
    console.log('   localContent.value.css_content length:', localContent.value.css_content?.length || 0)
    console.log('   localContent.value.css_content preview:', localContent.value.css_content?.substring(0, 200) + '...')

    if (!editorInstance) {
      if (dialogContent.value) {
        const htmlFormat = convertEmailBuilderToHtml(dialogContent.value);
        const finalCss = dialogCss.value || localContent.value.css_content || htmlFormat.css || ''
        
        console.log('🎨 [EmailEditor] Path 1: No editorInstance, using dialogContent')
        console.log('   finalCss source:', dialogCss.value ? 'dialogCss (PRIORITY 1)' : (localContent.value.css_content ? 'localContent.css_content (PRIORITY 2)' : (htmlFormat.css ? 'htmlFormat.css (PRIORITY 3)' : 'empty')))
        console.log('   finalCss length:', finalCss.length)
        console.log('   dialogCss.value length:', dialogCss.value?.length || 0)
        console.log('   localContent.value.css_content length:', localContent.value.css_content?.length || 0)
        console.log('   htmlFormat.css length:', htmlFormat.css?.length || 0)
        
        // Ensure CSS is in block_content
        let blockData = dialogContent.value
        if (typeof blockData === 'object' && blockData !== null) {
          blockData = { ...blockData, css: finalCss, html: htmlFormat.html || blockData.html || '' }
        }
        
        localContent.value = {
          ...localContent.value,
          template_content: htmlFormat.html,
          css_content: finalCss,
          block_content: JSON.stringify(blockData)
        };
        
        console.log('✅ [EmailEditor] Saved css_content (Path 1), length:', finalCss.length)
        console.log('   Saved to localContent.value.css_content:', !!localContent.value.css_content)
        console.log('   Saved to block_content.css:', blockData.css ? 'yes' : 'no')
      } else {
        throw new Error('Editor not available');
      }
    } else {
      const hasGetHtml = typeof editorInstance.getHtml === 'function';
      const hasGetCss = typeof editorInstance.getCss === 'function';

      if (!hasGetHtml || !hasGetCss) {
        const exportData = editorInstance.exportHtml ? editorInstance.exportHtml() : null;
        if (exportData) {
          // IMPORTANT: Priority dialogCss (contains CSS from imported template) > localContent.css_content > exportData.css
          const finalCss = dialogCss.value || localContent.value.css_content || exportData.css || ''
          
          console.log('🎨 [EmailEditor] Path 2: Using exportHtml')
          console.log('   finalCss source:', dialogCss.value ? 'dialogCss (PRIORITY 1)' : (localContent.value.css_content ? 'localContent.css_content (PRIORITY 2)' : (exportData.css ? 'exportData.css (PRIORITY 3)' : 'empty')))
          console.log('   finalCss length:', finalCss.length)
          console.log('   dialogCss.value length:', dialogCss.value?.length || 0)
          console.log('   localContent.value.css_content length:', localContent.value.css_content?.length || 0)
          console.log('   exportData.css length:', exportData.css?.length || 0)
          
          // Ensure CSS is in exportData
          exportData.css = finalCss
          
          localContent.value = {
            ...localContent.value,
            template_content: exportData.html,
            css_content: finalCss,
            block_content: JSON.stringify(exportData)
          };
          
          console.log('✅ [EmailEditor] Saved css_content (Path 2), length:', finalCss.length)
          console.log('   Saved to localContent.value.css_content:', !!localContent.value.css_content)
          console.log('   Saved to exportData.css:', !!exportData.css)
        } else {
          throw new Error('No valid export method found');
        }
      } else {
        const html = editorInstance.getHtml();
        const editorCss = editorInstance.getCss ? editorInstance.getCss() : '';
        const design = editorInstance.getProjectData ? editorInstance.getProjectData() : dialogContent.value || { blocks: [] };

        // IMPORTANT: Compare old CSS vs new CSS from editor
        const oldCss = localContent.value.css_content || ''
        const oldCssLength = oldCss.length
        const newCssFromEditor = editorCss || ''
        const newCssFromEditorLength = newCssFromEditor.length
        const dialogCssLength = dialogCss.value?.length || 0
        
        console.log('🔄 [EmailEditor] ========== CSS COMPARISON ==========')
        console.log('   Old CSS (localContent.value.css_content):')
        console.log('     - Length:', oldCssLength)
        console.log('     - Preview:', oldCss.substring(0, 200) + '...')
        console.log('   New CSS from editor (getCss()):')
        console.log('     - Length:', newCssFromEditorLength)
        console.log('     - Preview:', newCssFromEditor.substring(0, 200) + '...')
        console.log('   dialogCss.value (current dialog CSS):')
        console.log('     - Length:', dialogCssLength)
        console.log('     - Preview:', dialogCss.value?.substring(0, 200) + '...')
        console.log('   CSS changed:', oldCss !== newCssFromEditor && newCssFromEditorLength > 0)
        console.log('   dialogCss changed:', dialogCss.value !== newCssFromEditor && newCssFromEditorLength > 0)

        // IMPORTANT: Priority CSS from editor (newest) > dialogCss (from template) > localContent (old) > design
        // This ensures we always save the latest CSS that user edited in GrapesJS
        let finalCss = ''
        if (newCssFromEditor && newCssFromEditor.trim() !== '') {
          // PRIORITY 1: Use CSS from editor (getCss()) - this is the latest CSS user edited
          finalCss = newCssFromEditor
          console.log('🎨 [EmailEditor] Path 3: Using NEW CSS from editor.getCss() (PRIORITY 1), length:', finalCss.length)
          console.log('   ✅ Using NEW CSS from editor (user edited)')
        } else if (dialogCss.value && dialogCss.value.trim() !== '') {
          // PRIORITY 2: Use dialogCss (CSS from imported template or initial load)
          finalCss = dialogCss.value
          console.log('🎨 [EmailEditor] Path 3: Using dialogCss.value (PRIORITY 2), length:', finalCss.length)
          console.log('   ⚠️ Using dialogCss (may be old CSS from template)')
        } else if (oldCss && oldCss.trim() !== '') {
          // PRIORITY 3: Use old CSS from localContent (fallback)
          finalCss = oldCss
          console.log('🎨 [EmailEditor] Path 3: Using localContent.value.css_content (PRIORITY 3), length:', finalCss.length)
          console.log('   ⚠️ Using OLD CSS from localContent (fallback)')
        } else if (design && design.css && design.css.trim() !== '') {
          // PRIORITY 4: Use CSS from design object
          finalCss = design.css
          console.log('🎨 [EmailEditor] Path 3: Using design.css (PRIORITY 4), length:', finalCss.length)
        } else {
          console.log('⚠️ [EmailEditor] Path 3: No CSS found from any source')
        }
        
        console.log('🎨 [EmailEditor] Path 3: Final CSS determined')
        console.log('   finalCss length:', finalCss.length)
        console.log('   finalCss preview:', finalCss.substring(0, 200) + '...')
        console.log('   CSS will be saved:', finalCss !== oldCss ? '✅ YES (CSS changed)' : '⚠️ NO (same as old CSS)')
        console.log('🔄 [EmailEditor] ========== END CSS COMPARISON ==========')

        // Check if design has blocks - if not, convert HTML to block_content
        const hasBlocks = design && design.blocks && Array.isArray(design.blocks) && design.blocks.length > 0
        if (!hasBlocks && html && html.trim() !== '') {
          console.log('🔄 [EmailEditor] Path 3a: No blocks, converting HTML to block_content')
          try {
            const converted = convertHtmlToEmailBuilder(html)
            const cssToSave = finalCss || converted.css || ''
            const blockContentToSave = {
              ...converted,
              css: cssToSave,
              html: html
            }
            
            localContent.value = {
              ...localContent.value,
              template_content: html,
              block_content: JSON.stringify(blockContentToSave),
              css_content: cssToSave
            }
            
            console.log('✅ [EmailEditor] Saved css_content (Path 3a - converted), length:', cssToSave.length)
          } catch (error) {
            console.log('⚠️ [EmailEditor] Path 3a: Conversion failed, using fallback')
            // Fallback: create minimal block_content
            const blockContentToSave = {
              blocks: [],
              emailSettings: {
                backgroundColor: '#ffffff',
                contentWidth: 600,
                contentAlign: 'left',
                fontFamily: 'Arial, sans-serif'
              },
              css: finalCss,
              html: html
            }
            
            localContent.value = {
              ...localContent.value,
              template_content: html,
              block_content: JSON.stringify(blockContentToSave),
              css_content: finalCss
            }
            
            console.log('✅ [EmailEditor] Saved css_content (Path 3a - fallback), length:', finalCss.length)
          }
        } else {
          console.log('🔄 [EmailEditor] Path 3b: Design has blocks or is valid object')
          // Design has blocks or is valid object - ensure CSS is saved
          let blockContentToSave = design
          if (design && typeof design === 'object') {
            blockContentToSave = {
              ...design,
              css: finalCss || design.css || '',
              html: html || design.html || ''
            }
          } else {
            blockContentToSave = {
              blocks: [],
              emailSettings: {
                backgroundColor: '#ffffff',
                contentWidth: 600,
                contentAlign: 'left',
                fontFamily: 'Arial, sans-serif'
              },
              css: finalCss,
              html: html || ''
            }
          }

          localContent.value = {
            ...localContent.value,
            template_content: html,
            block_content: JSON.stringify(blockContentToSave),
            css_content: finalCss
          }
          
          console.log('✅ [EmailEditor] Saved css_content (Path 3b), length:', finalCss.length)
          console.log('   Saved to localContent.value.css_content:', !!localContent.value.css_content)
          console.log('   Saved to blockContentToSave.css:', blockContentToSave.css ? 'yes' : 'no')
        }
      }
    }

    // Log final saved state
    console.log('💾 [EmailEditor] Final saved state:')
    console.log('   localContent.value.css_content exists:', !!localContent.value.css_content)
    console.log('   localContent.value.css_content length:', localContent.value.css_content?.length || 0)
    console.log('   localContent.value.css_content preview:', localContent.value.css_content?.substring(0, 200) + '...')
    console.log('   localContent.value.block_content exists:', !!localContent.value.block_content)
    
    // Check if CSS is in block_content
    if (localContent.value.block_content) {
      try {
        const blockData = typeof localContent.value.block_content === 'string'
          ? JSON.parse(localContent.value.block_content)
          : localContent.value.block_content
        console.log('   block_content.css exists:', !!blockData.css)
        console.log('   block_content.css length:', blockData.css?.length || 0)
      } catch (e) {
        console.log('   block_content parse error:', e.message)
      }
    }

    editorLoading.value = true;

    console.log('📤 [EmailEditor] Emitting saved event with css_content length:', localContent.value.css_content?.length || 0)
    console.log('   block_content length:', localContent.value.block_content?.length || 0)
    console.log('   template_content length:', localContent.value.template_content?.length || 0)
    console.log('   template_content preview:', localContent.value.template_content?.substring(0, 200) + '...')
    
    // IMPORTANT: Force trigger reactivity by creating new object reference
    localContent.value = { ...localContent.value }
    
    emit('saved', { ...localContent.value });
    emit('update:content', { ...localContent.value });

    // IMPORTANT: Force update preview iframe after saving to show the latest saved content
    // Use multiple nextTick to ensure DOM and computed properties are updated
    nextTick(() => {
      nextTick(() => {
        if (previewIframe.value) {
          const newPreviewHtml = previewHtml.value
          previewIframe.value.srcdoc = newPreviewHtml
          console.log('✅ [EmailEditor] Preview iframe updated after save')
          console.log('   Preview HTML length:', newPreviewHtml?.length || 0)
          console.log('   Preview HTML preview:', newPreviewHtml?.substring(0, 200) + '...')
          console.log('   template_content in preview:', newPreviewHtml?.includes(localContent.value.template_content?.substring(0, 50) || ''))
        }
      })
    })

    console.log('✅ [EmailEditor] ========== SAVE TEMPLATE SUCCESS ==========')
    toast.success(__('Template saved successfully'));
    showTemplateDialog.value = false;

  } catch (error) {
    console.error('[EmailEditor] Error saving template:', error);
    toast.error(__('Failed to save template: ') + (error.message || 'Unknown error'));
  } finally {
    editorLoading.value = false;
  }
}
// Load current content into the editor
const loadContentIntoEditor = () => {
  if (localContent.value.block_content) {
    try {
      const blockData = typeof localContent.value.block_content === 'string'
        ? JSON.parse(localContent.value.block_content)
        : localContent.value.block_content;

      // Set the HTML content
      if (blockData.html) {
        dialogContent.value = blockData.html;
      }

      // Set the CSS content - Priority: blockData.css > localContent.css_content > extract from HTML
      let finalCss = ''
      
      if (blockData.css && blockData.css.trim() !== '') {
        finalCss = blockData.css;
      } else if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
        finalCss = localContent.value.css_content;
      } else if (blockData.html) {
        const htmlCssMatch = blockData.html.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
        if (htmlCssMatch && htmlCssMatch[1]) {
          finalCss = htmlCssMatch[1].trim();
        }
      } else if (localContent.value.template_content) {
        const templateCssMatch = localContent.value.template_content.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
        if (templateCssMatch && templateCssMatch[1]) {
          finalCss = templateCssMatch[1].trim();
        }
      }
      
      if (finalCss && finalCss.trim() !== '') {
        dialogCss.value = finalCss;
        localContent.value.css_content = finalCss;
      }

      // Update editor directly if available
      if (emailBuilderEditor.value) {
        if (blockData.html) {
          emailBuilderEditor.value.setComponents(blockData.html);
        }
        if (finalCss && finalCss.trim() !== '') {
          emailBuilderEditor.value.setStyle(finalCss);
        }
      }
    } catch (error) {
      console.error('[EmailEditor] Error parsing block_content:', error);
    }
  } else if (localContent.value.template_content) {
    dialogContent.value = localContent.value.template_content;
    
    // Extract CSS from template_content if available
    if (localContent.value.template_content) {
      const templateCssMatch = localContent.value.template_content.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
      if (templateCssMatch && templateCssMatch[1]) {
        const extractedCss = templateCssMatch[1].trim();
        dialogCss.value = extractedCss;
        if (!localContent.value.css_content) {
          localContent.value.css_content = extractedCss;
        }
      }
    }
    
    // Also check css_content field
    if (localContent.value.css_content && localContent.value.css_content.trim() !== '') {
      dialogCss.value = localContent.value.css_content;
    }
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
  console.log('📥 [EmailEditor] ========== APPLY TEMPLATE START ==========')
  console.log('📥 [EmailEditor] Template name:', template.template_name || template.name)
  console.log('📥 [EmailEditor] Template CSS sources:')
  console.log('   template.css_content exists:', !!template.css_content)
  console.log('   template.css_content length:', template.css_content?.length || 0)
  console.log('   template.block_content exists:', !!template.block_content)
  console.log('   template.email_design_json exists:', !!template.email_design_json)
  console.log('   template.html_content exists:', !!template.html_content)
  
  editorLoading.value = true

  if (template.subject) {
    localContent.value.email_subject = template.subject
  }

  let templateApplied = false
  let finalCss = '' // CSS to use for this template

  // Priority 1: Check for block_content (EmailBuilder format stored directly)
  if (template.block_content) {
    try {
      const blockData = typeof template.block_content === 'string'
        ? JSON.parse(template.block_content)
        : template.block_content

      if (blockData && (blockData.blocks || blockData.html)) {
        // Get CSS - Priority: template.css_content > blockData.css
        if (template.css_content && template.css_content.trim() !== '') {
          finalCss = template.css_content
          console.log('🎨 [EmailEditor] Priority 1: Using template.css_content, length:', finalCss.length)
        } else if (blockData.css && blockData.css.trim() !== '') {
          finalCss = blockData.css
          console.log('🎨 [EmailEditor] Priority 1: Using blockData.css, length:', finalCss.length)
        } else {
          console.log('⚠️ [EmailEditor] Priority 1: No CSS found in template or blockData')
        }
        
        // Force left alignment
        if (!blockData.emailSettings) {
          blockData.emailSettings = {
            backgroundColor: '#ffffff',
            contentWidth: 600,
            contentAlign: 'left',
            fontFamily: 'Arial, sans-serif'
          }
        } else {
          blockData.emailSettings.contentAlign = 'left'
        }

        // Ensure CSS is in blockData
        blockData.css = finalCss

        // Convert and save all formats
        const htmlFormat = convertEmailBuilderToHtml(blockData)
        localContent.value.template_content = template.html_content || htmlFormat.html || template.message || ''
        localContent.value.mjml_content = htmlFormat.mjml || ''
        localContent.value.css_content = finalCss
        localContent.value.block_content = JSON.stringify(blockData)

        dialogContent.value = blockData.html || blockData
        // IMPORTANT: Always set dialogCss even if finalCss is empty (to clear old CSS)
        dialogCss.value = finalCss
        
        console.log('✅ [EmailEditor] Priority 1: Applied template from block_content')
        console.log('   Set localContent.value.css_content, length:', finalCss.length)
        console.log('   Set dialogCss.value, length:', dialogCss.value.length)
        templateApplied = true
      }
    } catch (e) {
      console.error('[EmailEditor] Failed to parse block_content:', e)
    }
  }

  // Priority 2: Use email_design_json field (EmailBuilder or Unlayer design)
  if (!templateApplied && template.email_design_json) {
    try {
      const design = typeof template.email_design_json === 'string'
        ? JSON.parse(template.email_design_json)
        : template.email_design_json

      // Check for EmailBuilder format first
      if (design && design.blocks && Array.isArray(design.blocks) && design.blocks.length > 0) {
        // Get CSS - Priority: template.css_content > design.css
        if (template.css_content && template.css_content.trim() !== '') {
          finalCss = template.css_content
          console.log('🎨 [EmailEditor] Priority 2: Using template.css_content, length:', finalCss.length)
        } else if (design.css && design.css.trim() !== '') {
          finalCss = design.css
          console.log('🎨 [EmailEditor] Priority 2: Using design.css, length:', finalCss.length)
        } else {
          console.log('⚠️ [EmailEditor] Priority 2: No CSS found in template or design')
        }
        
        // Force left alignment
        if (!design.emailSettings) {
          design.emailSettings = {
            backgroundColor: '#ffffff',
            contentWidth: 600,
            contentAlign: 'left',
            fontFamily: 'Arial, sans-serif'
          }
        } else {
          design.emailSettings.contentAlign = 'left'
        }

        // Ensure CSS is in design
        design.css = finalCss

        // Convert and save all formats
        const htmlFormat = convertEmailBuilderToHtml(design)
        localContent.value.template_content = template.html_content || htmlFormat.html || template.message || ''
        localContent.value.mjml_content = htmlFormat.mjml || ''
        localContent.value.css_content = finalCss
        localContent.value.block_content = JSON.stringify(design)

        dialogContent.value = design.html || design
        // IMPORTANT: Always set dialogCss even if finalCss is empty (to clear old CSS)
        dialogCss.value = finalCss
        
        console.log('✅ [EmailEditor] Priority 2: Applied template from email_design_json')
        console.log('   Set localContent.value.css_content, length:', finalCss.length)
        console.log('   Set dialogCss.value, length:', dialogCss.value.length)
        templateApplied = true
      }
      // OLD: Validate it's a proper Unlayer design (must have body.rows)
      else if (design && design.body && Array.isArray(design.body.rows)) {
        // Get CSS from template
        if (template.css_content && template.css_content.trim() !== '') {
          finalCss = template.css_content
        }
        
        // Convert Unlayer to EmailBuilder format
        const converted = convertHtmlToEmailBuilder(design.body?.rows?.[0]?.columns?.[0]?.contents?.[0]?.values?.text || '')

        // Force left alignment
        if (!converted.emailSettings) {
          converted.emailSettings = {
            backgroundColor: '#ffffff',
            contentWidth: 600,
            contentAlign: 'left',
            fontFamily: 'Arial, sans-serif'
          }
        } else {
          converted.emailSettings.contentAlign = 'left'
        }

        // Ensure CSS is in converted
        converted.css = finalCss

        // Convert and save all formats
        const htmlFormat = convertEmailBuilderToHtml(converted)
        localContent.value.template_content = template.html_content || htmlFormat.html || template.message || ''
        localContent.value.mjml_content = htmlFormat.mjml || ''
        localContent.value.css_content = finalCss
        localContent.value.block_content = JSON.stringify(converted)

        dialogContent.value = converted.html || converted
        // IMPORTANT: Always set dialogCss even if finalCss is empty (to clear old CSS)
        dialogCss.value = finalCss
        
        templateApplied = true
        toast.info(__('Applied legacy template format. Converted to new format.'))
      }
    } catch (e) {
      console.error('[EmailEditor] Failed to parse email_design_json:', e)
    }
  }

  // Priority 3: If template has html_content or message, use it directly
  if (!templateApplied && (template.html_content || template.message)) {
    try {
      const htmlContent = template.html_content || template.message || ''
      
      // Get CSS - Priority: template.css_content > extract from HTML
      if (template.css_content && template.css_content.trim() !== '') {
        finalCss = template.css_content
        console.log('🎨 [EmailEditor] Priority 3: Using template.css_content, length:', finalCss.length)
      } else if (htmlContent) {
        // Try to extract CSS from <style> tags in HTML
        const styleMatch = htmlContent.match(/<style[^>]*>([\s\S]*?)<\/style>/gi)
        if (styleMatch && styleMatch.length > 0) {
          finalCss = styleMatch.map(match => {
            const contentMatch = match.match(/<style[^>]*>([\s\S]*?)<\/style>/i)
            return contentMatch ? contentMatch[1] : ''
          }).join('\n')
          console.log('🎨 [EmailEditor] Priority 3: Extracted CSS from HTML, length:', finalCss.length)
        } else {
          console.log('⚠️ [EmailEditor] Priority 3: No CSS found in template or HTML')
        }
      }

      // Use HTML content directly
      dialogContent.value = htmlContent

      // Set all content fields
      localContent.value.template_content = htmlContent
      localContent.value.css_content = finalCss
      
      // Create minimal block_content with CSS
      const minimalBlockContent = {
        blocks: [],
        emailSettings: {
          backgroundColor: '#ffffff',
          contentWidth: 600,
          contentAlign: 'left',
          fontFamily: 'Arial, sans-serif'
        },
        css: finalCss,
        html: htmlContent
      }
      localContent.value.block_content = JSON.stringify(minimalBlockContent)

      // Convert to MJML format if needed (optional)
      try {
        const converted = convertHtmlToEmailBuilder(htmlContent)
        const htmlFormat = convertEmailBuilderToHtml(converted)
        localContent.value.mjml_content = htmlFormat.mjml || ''
      } catch (e) {
        localContent.value.mjml_content = ''
      }

      // IMPORTANT: Always set dialogCss even if finalCss is empty (to clear old CSS)
      dialogCss.value = finalCss
      
      console.log('✅ [EmailEditor] Priority 3: Applied template from html_content')
      console.log('   Set localContent.value.css_content, length:', finalCss.length)
      console.log('   Set dialogCss.value, length:', dialogCss.value.length)
      templateApplied = true
    } catch (e) {
      console.error('[EmailEditor] Failed to process html_content:', e)
    }
  }

  // If template couldn't be applied (truly no design data)
  if (!templateApplied) {
    if (localContent.value.template_content && localContent.value.template_content.trim() !== '') {
      dialogContent.value = localContent.value.template_content
    } else {
      dialogContent.value = null
    }
    toast.warning(__('This template does not have a valid design. Please create a new design with the visual editor.'))
    editorLoading.value = false
  } else {
    // IMPORTANT: Ensure dialogCss is set from finalCss before opening dialog
    if (finalCss && finalCss.trim() !== '') {
      dialogCss.value = finalCss
      console.log('[EmailEditor] Template applied, CSS length:', finalCss.length)
    }
  }

  showTemplateSelectorModal.value = false

  // IMPORTANT: Emit update:content immediately after applying template
  // This ensures parent component receives the updated block_content, template_content, and css_content
  if (templateApplied) {
    console.log('📤 [EmailEditor] Emitting update:content after template applied')
    console.log('   block_content exists:', !!localContent.value.block_content)
    console.log('   block_content length:', localContent.value.block_content?.length || 0)
    console.log('   template_content exists:', !!localContent.value.template_content)
    console.log('   template_content length:', localContent.value.template_content?.length || 0)
    console.log('   css_content exists:', !!localContent.value.css_content)
    console.log('   css_content length:', localContent.value.css_content?.length || 0)
    
    // IMPORTANT: Force emit update:content to ensure parent receives the new template
    // Use nextTick to ensure all updates are complete
    nextTick(() => {
      emit('update:content', { ...localContent.value })
      
      // IMPORTANT: Force preview iframe to update immediately
      if (previewIframe.value) {
        nextTick(() => {
          if (previewIframe.value) {
            previewIframe.value.srcdoc = previewHtml.value
            console.log('✅ [EmailEditor] Preview iframe updated after template applied')
          }
        })
      }
    })
  }

  // Ensure editor dialog stays open
  nextTick(() => {
    showTemplateDialog.value = true
    
    // IMPORTANT: Update editor with new CSS and content after template is applied
    if (templateApplied && emailBuilderEditor.value) {
      nextTick(() => {
        // Update CSS in editor
        if (finalCss && finalCss.trim() !== '') {
          try {
            const editor = emailBuilderEditor.value
            if (editor && typeof editor.setStyle === 'function') {
              editor.setStyle(finalCss)
            }
          } catch (error) {
            console.error('[EmailEditor] Error setting CSS after template apply:', error)
          }
        }
        
        // Update content in editor if needed
        if (dialogContent.value) {
          try {
            const editor = emailBuilderEditor.value
            if (editor && typeof editor.setComponents === 'function') {
              const htmlContent = typeof dialogContent.value === 'string' 
                ? dialogContent.value 
                : (dialogContent.value.html || '')
              if (htmlContent) {
                editor.setComponents(htmlContent)
              }
            }
          } catch (error) {
            console.error('[EmailEditor] Error setting content after template apply:', error)
          }
        }
      })
    }
  })

  if (templateApplied) {
    console.log('✅ [EmailEditor] Template applied successfully')
    console.log('📥 [EmailEditor] Final state after apply:')
    console.log('   localContent.value.css_content length:', localContent.value.css_content?.length || 0)
    console.log('   dialogCss.value length:', dialogCss.value?.length || 0)
    console.log('   localContent.value.block_content exists:', !!localContent.value.block_content)
    toast.success(__('Template applied successfully'))
  } else {
    console.log('⚠️ [EmailEditor] Template was not applied')
  }
  
  console.log('📥 [EmailEditor] ========== APPLY TEMPLATE END ==========')
  editorLoading.value = false
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

// Strip MJML-generated tables and extract clean text content
// When user has old MJML-generated HTML, this extracts readable text by removing table structure
const stripMJMLTables = (html) => {
  if (!html) return ''

  try {
    // If it looks like HTML with tables (MJML output), extract text content
    if (html.includes('<table') || html.includes('<td')) {
      // Create a temp DOM element
      const div = document.createElement('div')
      div.innerHTML = html

      // Get all text nodes, preserving some structure
      let text = ''
      const nodes = div.querySelectorAll('*')

      for (const node of nodes) {
        // Skip script and style tags
        if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE') continue

        // Get text from divs, p tags, and table cells
        if (['DIV', 'P', 'TD', 'TH', 'SPAN'].includes(node.tagName)) {
          const nodeText = node.textContent?.trim()
          if (nodeText && !text.includes(nodeText)) {
            text += nodeText + '\n'
          }
        }
      }

      // If we extracted text, return it formatted; otherwise return original
      return text.trim() || html
    }

    return html
  } catch (error) {
    console.warn('Error stripping MJML tables:', error)
    return html
  }
}

// Get default email template (same as NewMiraEmailTemplate.vue)

// Get preview content (extract from EmailBuilder blocks or Unlayer design)
const getPreviewContent = (content) => {
  if (!content) return ''

  try {
    const design = typeof content === 'string' ? JSON.parse(content) : content

    // NEW: Handle EmailBuilder format
    if (design.blocks && Array.isArray(design.blocks)) {
      let previewHtml = ''
      design.blocks.forEach(block => {
        if (block.type === 'text' && block.props?.content) {
          // Wrap each block in paragraph tag để xuống dòng
          previewHtml += '<p>' + block.props.content + '</p>'
        }
        // Handle nested blocks in layout columns
        if (block.children && Array.isArray(block.children)) {
          block.children.forEach(column => {
            if (Array.isArray(column)) {
              column.forEach(childBlock => {
                if (childBlock.type === 'text' && childBlock.props?.content) {
                  previewHtml += '<p>' + childBlock.props.content + '</p>'
                }
              })
            }
          })
        }
      })

      // Limit preview length một cách đơn giản bằng textContent nếu quá dài
      if (previewHtml.length > 2000) {
        const div = document.createElement('div')
        div.innerHTML = previewHtml
        const text = div.textContent || ''
        return text.substring(0, 200) + '...'
      }
      return previewHtml || '<p>Email template created with EmailBuilder</p>'
    }

    // OLD: Handle Unlayer design format (for backward compatibility)
    if (design.body && design.body.rows) {
      let previewText = ''
      design.body.rows.forEach(row => {
        row.columns?.forEach(column => {
          column.contents?.forEach(contentItem => {
            if (contentItem.type === 'text' && contentItem.values?.text) {
              const div = document.createElement('div')
              div.innerHTML = contentItem.values.text
              previewText += div.textContent + ' '
            }
          })
        })
      })

      if (previewText.length > 200) {
        return previewText.substring(0, 200) + '...'
      }
      return previewText || '<p>Email template created with visual editor</p>'
    }
  } catch (e) {
    console.warn('Failed to parse content as design JSON:', e)
  }

  // Fallback for non-JSON content
  if (content.length > 200) {
    return content.substring(0, 200) + '...'
  }
  return content
}

// Get preview with CSS injected - Convert to computed property for reactivity
const previewHtml = computed(() => {
  const content = getContentForPreview()
  let htmlContent = ''
  
  // Priority 1: Use template_content directly (already HTML with full structure)
  if (localContent.value.template_content) {
    htmlContent = localContent.value.template_content
  } 
  // Priority 2: Extract from block_content or email_content
  else if (content) {
    htmlContent = getPreviewContent(content)
    // If getPreviewContent returns empty or too short, try to use content as HTML directly
    if ((!htmlContent || htmlContent.length < 50) && typeof content === 'string' && !content.startsWith('{')) {
      htmlContent = content
    }
  }
  
  // Get CSS content - use default CSS if not available
  let cssContent = localContent.value.css_content || ''
  if (!cssContent || cssContent.trim() === '') {
    cssContent = getDefaultEmailTemplateCss()
  }
  
  // IMPORTANT: Create complete HTML document for iframe preview (like Step2_ContentTimeline)
  if (htmlContent && htmlContent.trim() !== '') {
    // Check if HTML already has full document structure
    const hasDoctype = htmlContent.trim().startsWith('<!DOCTYPE') || htmlContent.trim().startsWith('<!doctype')
    const hasHtmlTag = htmlContent.includes('<html') || htmlContent.includes('<HTML')
    const hasHeadTag = htmlContent.includes('<head') || htmlContent.includes('<HEAD')
    const hasBodyTag = htmlContent.includes('<body') || htmlContent.includes('<BODY')
    
    // If already a complete HTML document, just inject CSS into head
    if (hasDoctype && hasHtmlTag && hasHeadTag) {
      // Remove existing style tags to avoid duplicates
      let cleanHtml = htmlContent.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      
      // Inject CSS into head
      const headEndMatch = cleanHtml.match(/<\/head>/i)
      if (headEndMatch) {
        const cssStyleTag = cssContent ? `\n  <style type="text/css">${cssContent}</style>` : ''
        cleanHtml = cleanHtml.replace(/<\/head>/i, `${cssStyleTag}\n</head>`)
      } else {
        // If no </head> tag, try to inject before </html> or at end
        const htmlEndMatch = cleanHtml.match(/<\/html>/i)
        if (htmlEndMatch) {
          const cssStyleTag = cssContent ? `\n  <style type="text/css">${cssContent}</style>` : ''
          cleanHtml = cleanHtml.replace(/<\/html>/i, `${cssStyleTag}\n</html>`)
        } else {
          // Just prepend CSS as style tag
          const cssStyleTag = cssContent ? `<style type="text/css">${cssContent}</style>\n` : ''
          cleanHtml = cssStyleTag + cleanHtml
        }
      }
      
      return cleanHtml
    }
    
    // Otherwise, extract body content and create full HTML document
    // Remove existing <style> tags from HTML to avoid duplicates
    let cleanHtml = htmlContent.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    
    // Extract body content if HTML has <body> tag
    let bodyContent = cleanHtml
    if (cleanHtml.includes('<body')) {
      const bodyMatch = cleanHtml.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
      if (bodyMatch && bodyMatch[1]) {
        bodyContent = bodyMatch[1]
      } else {
        // If <body> tag exists but no closing tag, extract everything after <body>
        const bodyStart = cleanHtml.indexOf('<body')
        if (bodyStart !== -1) {
          const bodyTagEnd = cleanHtml.indexOf('>', bodyStart) + 1
          bodyContent = cleanHtml.substring(bodyTagEnd)
        }
      }
    }
    
    // Remove <meta>, <title>, and other head tags from body content
    bodyContent = bodyContent
      .replace(/<meta[^>]*>/gi, '')
      .replace(/<title[^>]*>[\s\S]*?<\/title>/gi, '')
      .replace(/<link[^>]*>/gi, '')
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .trim()
    
    // Create complete HTML document with CSS in <head> for iframe preview
    // IMPORTANT: Reset styles FIRST (low priority), then css_content (high priority)
    // This ensures css_content styles override reset styles and browser defaults
    const fullHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <style type="text/css" id="email-reset-styles">
    /* Minimal reset styles - only override browser defaults, NOT email CSS */
    /* These styles have LOW priority - CSS from css_content will override them */
    html, body { 
      margin: 0; 
      padding: 0; 
      background-color: #f4f4f4; 
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
  ${cssContent ? `<style type="text/css" id="email-css-content">${cssContent}</style>` : ''}
</head>
<body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: Arial, sans-serif;">
  ${bodyContent}
</body>
</html>`
    
    return fullHtml
  }
  
  // Return HTML without CSS if no HTML available, but still strip MJML tables
  const fallbackContent = htmlContent ? stripMJMLTables(htmlContent) : stripMJMLTables(getPreviewContent(content))
  if (fallbackContent && cssContent) {
    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>${cssContent}</style>
</head>
<body style="margin: 0; padding: 0; background: #ffffff; font-family: Arial, sans-serif;">
  ${fallbackContent}
</body>
</html>`
  }
  return fallbackContent || ''
})

// Handle CSS change from EmailBuilder (similar to EmailBuilder.vue)
const handleCssChange = (newCss) => {
  console.log('🎨 [EmailEditor] CSS changed from editor:')
  console.log('   Old dialogCss.value length:', dialogCss.value?.length || 0)
  console.log('   New CSS length:', newCss?.length || 0)
  console.log('   CSS changed:', dialogCss.value !== newCss)
  
  if (newCss && newCss.trim() !== '') {
    // IMPORTANT: Update dialogCss when CSS changes from editor
    // This ensures we save the latest CSS from GrapesJS editor
    dialogCss.value = newCss
    console.log('✅ [EmailEditor] Updated dialogCss.value with new CSS from editor')
  }
}

// Editor ready callback
const onEditorReady = (editor) => {
  // Hide loading indicator when editor is fully ready
  setTimeout(() => {
    editorLoading.value = false
    
    // IMPORTANT: Apply CSS when editor is ready if dialogCss is set
    if (dialogCss.value && dialogCss.value.trim() !== '') {
      try {
        if (emailBuilderEditor.value && typeof emailBuilderEditor.value.setStyle === 'function') {
          emailBuilderEditor.value.setStyle(dialogCss.value)
        }
      } catch (error) {
        console.error('[EmailEditor] Error applying CSS on editor ready:', error)
      }
    }
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

// Watch dialogCss to update editor when CSS changes (e.g., after applying template)
watch(dialogCss, (newCss) => {
  if (newCss && newCss.trim() !== '' && emailBuilderEditor.value) {
    nextTick(() => {
      try {
        if (emailBuilderEditor.value && typeof emailBuilderEditor.value.setStyle === 'function') {
          emailBuilderEditor.value.setStyle(newCss)
        }
      } catch (error) {
        console.error('[EmailEditor] Error updating CSS from dialogCss watch:', error)
      }
    })
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
  console.log('🔄 [EmailEditor] localContent changed - emitting update:content')
  console.log('   email_subject:', newContent.email_subject)
  console.log('   email_subject type:', typeof newContent.email_subject)
  console.log('   email_subject length:', newContent.email_subject?.length || 0)
  console.log('   attachments count:', newContent.attachments?.length || 0)
  console.log('   Full newContent keys:', Object.keys(newContent))
  
  emit('update:content', newContent)
  
  // IMPORTANT: Update dialogCss when localContent.css_content changes
  if (newContent.css_content && newContent.css_content.trim() !== '') {
    if (dialogCss.value !== newContent.css_content) {
      dialogCss.value = newContent.css_content
    }
  }
  
  // Force iframe to update when content changes (especially after save)
  if (previewIframe.value) {
    nextTick(() => {
    nextTick(() => {
      if (previewIframe.value) {
          const newPreviewHtml = previewHtml.value
          previewIframe.value.srcdoc = newPreviewHtml
          console.log('🔄 [EmailEditor] Preview iframe updated from localContent watch')
          console.log('   Preview HTML length:', newPreviewHtml?.length || 0)
          console.log('   template_content in preview:', newPreviewHtml?.includes(newContent.template_content?.substring(0, 50) || ''))
      }
      })
    })
  }
}, { deep: true })

watch(() => props.content, (newContent) => {
  if (!newContent) return
  
  console.log('🔄 [EmailEditor] Props content changed')
  console.log('   newContent.email_subject:', newContent?.email_subject)
  console.log('   newContent.email_subject type:', typeof newContent?.email_subject)
  console.log('   newContent.email_subject length:', newContent?.email_subject?.length || 0)
  console.log('   current localContent.email_subject:', localContent.value.email_subject)
  console.log('   template_content length:', newContent?.template_content?.length || 0)
  console.log('   block_content length:', newContent?.block_content?.length || 0)
  console.log('   css_content length:', newContent?.css_content?.length || 0)
  
  // IMPORTANT: Force trigger reactivity by creating new object
  // IMPORTANT: Preserve email_subject if newContent.email_subject is empty string or undefined
  // This prevents overwriting user input when props are updated from parent
  // Only preserve if current localContent has a non-empty email_subject AND newContent doesn't have a valid one
  const currentEmailSubject = localContent.value.email_subject || ''
  const newEmailSubject = newContent.email_subject || ''
  const shouldPreserveEmailSubject = currentEmailSubject.trim() !== '' && newEmailSubject.trim() === ''
  const preservedEmailSubject = shouldPreserveEmailSubject 
    ? currentEmailSubject
    : newEmailSubject
  
  localContent.value = { 
    ...localContent.value, 
    ...newContent,
    // IMPORTANT: Preserve email_subject if newContent doesn't have a valid value
    email_subject: preservedEmailSubject,
    // Ensure css_content is always a string, not undefined
    css_content: newContent?.css_content !== undefined ? newContent.css_content : (localContent.value.css_content || ''),
    // Explicitly ensure all fields are updated
    block_content: newContent?.block_content !== undefined ? newContent.block_content : localContent.value.block_content,
    template_content: newContent?.template_content !== undefined ? newContent.template_content : localContent.value.template_content
  }
  
  console.log('✅ [EmailEditor] Updated localContent from props')
  console.log('   preserved email_subject:', localContent.value.email_subject)
  console.log('   email_subject preserved:', shouldPreserveEmailSubject)
  console.log('   localContent.template_content length:', localContent.value.template_content?.length || 0)
  
  // Force iframe to update when props content changes (especially after save)
  if (previewIframe.value) {
    nextTick(() => {
    nextTick(() => {
      if (previewIframe.value) {
          const newPreviewHtml = previewHtml.value
          previewIframe.value.srcdoc = newPreviewHtml
          console.log('✅ [EmailEditor] Preview iframe updated from props.content watch')
          console.log('   Preview HTML length:', newPreviewHtml?.length || 0)
          console.log('   Preview HTML preview:', newPreviewHtml?.substring(0, 200) + '...')
          console.log('   template_content in preview:', newPreviewHtml?.includes(localContent.value.template_content?.substring(0, 50) || ''))
      }
      })
    })
  }
}, { deep: true, immediate: false })

// Watch previewHtml computed property to update iframe
watch(previewHtml, (newHtml) => {
  if (previewIframe.value && newHtml) {
    previewIframe.value.srcdoc = newHtml
    console.log('🔄 [EmailEditor] Preview iframe updated from watch, HTML length:', newHtml?.length || 0)
  }
}, { immediate: true })

</script>

