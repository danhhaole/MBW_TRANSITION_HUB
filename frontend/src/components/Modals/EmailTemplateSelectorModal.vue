<template>
  <Dialog
    v-model="show"
    :options="{ title: __('Email Templates'), size: '4xl' }"
  >
    <template #body-content>
      <div class="flex items-center gap-3 mb-2">
        <TextInput
          ref="searchInput"
          v-model="search"
          type="text"
          :placeholder="__('Search templates...')"
          class="flex-1"
        >
          <template #prefix>
            <FeatherIcon name="search" class="h-4 w-4 text-gray-500" />
          </template>
        </TextInput>
        <Button
          :label="__('Create')"
          icon-left="plus"
          variant="solid"
          @click.stop="openSettings"
        />
      </div>
      <div
        v-if="filteredTemplates.length"
        class="mt-2 grid max-h-[560px] sm:grid-cols-3 grid-cols-1 gap-2 overflow-y-auto"
      >
        <div
          v-for="template in filteredTemplates"
          :key="template.name"
          class="flex h-80 cursor-pointer flex-col gap-2 rounded-lg border p-3 hover:bg-gray-100 transition-colors"
          @click.stop="handleTemplateClick(template)"
        >
          <div class="flex items-center justify-between border-b pb-2">
            <div class="text-base font-semibold truncate">
              {{ template.template_name || template.name }}
            </div>
            <div class="flex gap-1">
              <span v-if="template.is_active" class="px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded">
                {{ __('Active') }}
              </span>
              <span v-if="template.default_template" class="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded">
                {{ __('Default') }}
              </span>
            </div>
          </div>
          <div v-if="template.subject" class="text-sm text-gray-600 truncate">
            <span class="font-medium">{{ __('Subject:') }}</span> {{ template.subject }}
          </div>
          <div v-if="template.template_type" class="text-xs text-gray-500 truncate">
            <span class="font-medium">{{ __('Type:') }}</span> {{ getTypeLabel(template.template_type) }}
          </div>
          
          <!-- Preview: Visual thumbnail of email design -->
          <div class="flex-1 overflow-hidden">
            <!-- Visual Preview (if has HTML message) -->
            <div 
              v-if="template.message && template.message.length > 50" 
              class="relative h-full w-full bg-white border rounded overflow-hidden"
            >
              <!-- Stats overlay -->
              <div 
                v-if="template.email_design_json"
                class="absolute top-1 left-1 flex gap-1 z-10"
              >
                <span class="px-1.5 py-0.5 text-[10px] bg-black/70 text-white rounded flex items-center gap-0.5">
                  <FeatherIcon name="image" class="w-2.5 h-2.5" />
                  {{ getDesignStats(template.email_design_json).images }}
                </span>
                <span class="px-1.5 py-0.5 text-[10px] bg-black/70 text-white rounded flex items-center gap-0.5">
                  <FeatherIcon name="type" class="w-2.5 h-2.5" />
                  {{ getDesignStats(template.email_design_json).texts }}
                </span>
                <span class="px-1.5 py-0.5 text-[10px] bg-black/70 text-white rounded flex items-center gap-0.5">
                  <FeatherIcon name="mouse-pointer" class="w-2.5 h-2.5" />
                  {{ getDesignStats(template.email_design_json).buttons }}
                </span>
              </div>
              
              <!-- HTML Preview (scaled, top portion only) -->
              <div class="w-full h-full overflow-hidden relative bg-gray-50/50">
                <iframe
                  :srcdoc="getPreviewHtml(template)"
                  class="w-full border-0 pointer-events-none origin-top-left"
                  style="width: 600px; height: 1200px; transform: scale(0.42); transform-origin: top left;"
                  sandbox="allow-same-origin"
                  loading="lazy"
                />
              </div>
            </div>
            
            <!-- Fallback: Stats + Text (if no HTML but has design) -->
            <div v-else-if="template.email_design_json" class="text-sm text-gray-600 space-y-2">
              <div class="flex items-center gap-2 text-xs">
                <span class="flex items-center gap-1">
                  <FeatherIcon name="image" class="w-3 h-3" />
                  {{ getDesignStats(template.email_design_json).images }} {{ __('images') }}
                </span>
                <span class="flex items-center gap-1">
                  <FeatherIcon name="type" class="w-3 h-3" />
                  {{ getDesignStats(template.email_design_json).texts }} {{ __('texts') }}
                </span>
                <span class="flex items-center gap-1">
                  <FeatherIcon name="mouse-pointer" class="w-3 h-3" />
                  {{ getDesignStats(template.email_design_json).buttons }} {{ __('buttons') }}
                </span>
              </div>
              <div class="text-xs text-gray-500 line-clamp-4">
                {{ getDesignPreviewText(template.email_design_json) }}
              </div>
            </div>
            
            <!-- No content -->
            <div v-else class="text-sm text-gray-400 italic flex items-center justify-center h-full">
              <div class="text-center">
                <FeatherIcon name="mail" class="w-8 h-8 mx-auto mb-2 text-gray-300" />
                <div>{{ __('No preview available') }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="mt-2">
        <div class="flex h-56 flex-col items-center justify-center">
          <FeatherIcon name="inbox" class="h-12 w-12 text-gray-400 mb-3" />
          <div class="text-lg font-medium text-gray-700">
            {{ __('No templates found') }}
          </div>
          <div class="text-sm text-gray-500 mt-1">
            {{ search ? __('Try a different search term') : __('Create your first email template') }}
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { createListResource } from 'frappe-ui'
import { ref, computed, nextTick, watch, onMounted } from 'vue'

const props = defineProps({
  doctype: {
    type: String,
    default: '',
  },
})

const show = defineModel()
const searchInput = ref('')

const emit = defineEmits(['apply', 'openSettings', 'close'])

const search = ref('')

const templates = createListResource({
  type: 'list',
  doctype: 'Mira Email Template',
  cache: ['MiraEmailTemplates', props.doctype],
  fields: [
    'name',
    'template_name',
    'template_type',
    'subject',
    'message',
    'html_content',
    'css_content',
    'email_design_json',
    'is_active',
    'default_template',
  ],
  filters: { is_active: 1 },
  orderBy: 'modified desc',
  pageLength: 99999,
})

onMounted(() => {
  if (templates.data == null) {
    templates.fetch()
  }
})

const filteredTemplates = computed(() => {
  if (!templates.data) return []
  
  return templates.data.filter((template) => {
    if (!search.value) return true
    
    const searchLower = search.value.toLowerCase()
    return (
      template.template_name?.toLowerCase().includes(searchLower) ||
      template.subject?.toLowerCase().includes(searchLower) ||
      template.name?.toLowerCase().includes(searchLower)
    )
  })
})

const getTypeLabel = (type) => {
  const labels = {
    'confirm-email': 'Confirm Email',
    'invited-email': 'Invited Email',
    'reject-email': 'Reject Email',
    'other-email': 'Other Email',
  }
  return labels[type] || type
}

const getPreviewText = (html) => {
  if (!html) return ''
  
  // Create a temporary div to parse HTML
  const temp = document.createElement('div')
  temp.innerHTML = html
  
  // Get text content (strips HTML tags)
  const text = temp.textContent || temp.innerText || ''
  
  // Clean up extra whitespace and newlines
  return text
    .replace(/\s+/g, ' ')
    .trim()
}

// Get preview HTML with CSS injected
const getPreviewHtml = (template) => {
  // Priority: html_content > message
  let htmlContent = template.html_content || template.message || ''
  const cssContent = template.css_content || ''
  
  if (!htmlContent) return ''
  
  // Remove script tags to avoid sandbox errors (we only need visual preview)
  htmlContent = htmlContent.replace(/<script[\s\S]*?<\/script>/gi, '')
  htmlContent = htmlContent.replace(/<script[^>]*>/gi, '')
  
  // Clean up HTML - remove <body> tags if present (we'll wrap it properly)
  const hasBodyTag = htmlContent.includes('<body')
  if (hasBodyTag) {
    // Extract content inside <body> tags
    const bodyMatch = htmlContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
    if (bodyMatch && bodyMatch[1]) {
      htmlContent = bodyMatch[1]
    } else {
      // Remove <body> opening tag if no closing tag
      htmlContent = htmlContent.replace(/<body[^>]*>/i, '')
    }
  }
  
  // Build complete HTML document with CSS
  let fullHtml = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Preview</title>`
  
  // Inject CSS into <head>
  if (cssContent && cssContent.trim() !== '') {
    fullHtml += `
  <style>
${cssContent}
  </style>`
  }
  
  fullHtml += `
</head>
<body style="margin: 0; padding: 0;">
${htmlContent}
</body>
</html>`
  
  return fullHtml
}

// Get stats from Unlayer design JSON
const getDesignStats = (jsonString) => {
  try {
    const design = typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString
    const counters = design.counters || {}
    
    return {
      images: counters.u_content_image || 0,
      texts: counters.u_content_text || 0,
      buttons: counters.u_content_button || 0,
      rows: counters.u_row || 0
    }
  } catch (e) {
    return { images: 0, texts: 0, buttons: 0, rows: 0 }
  }
}

// Extract preview text from Unlayer design JSON
const getDesignPreviewText = (jsonString) => {
  try {
    const design = typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString
    const textContents = []
    
    // Walk through design body to find text contents
    const rows = design.body?.rows || []
    rows.forEach(row => {
      row.columns?.forEach(column => {
        column.contents?.forEach(content => {
          if (content.type === 'text' && content.values?.text) {
            // Strip HTML tags from text
            const temp = document.createElement('div')
            temp.innerHTML = content.values.text
            const text = (temp.textContent || temp.innerText || '').trim()
            if (text && !text.startsWith('{{')) { // Skip merge tags
              textContents.push(text)
            }
          }
        })
      })
    })
    
    return textContents.slice(0, 3).join(' • ') || 'Email template design'
  } catch (e) {
    return 'Email template design'
  }
}

const handleTemplateClick = (template) => {
  console.log('🖱️ [EmailTemplateSelectorModal] Template clicked:', {
    templateName: template.template_name || template.name,
    templateId: template.name,
    hasHtmlContent: !!template.html_content,
    htmlContentLength: template.html_content?.length || 0,
    hasCssContent: !!template.css_content,
    cssContentLength: template.css_content?.length || 0,
    hasMessage: !!template.message,
    messageLength: template.message?.length || 0,
    hasBlockContent: !!template.block_content,
    blockContentLength: template.block_content?.length || 0,
    hasEmailDesignJson: !!template.email_design_json,
    emailDesignJsonLength: template.email_design_json?.length || 0,
    subject: template.subject,
    templateType: template.template_type,
    fullTemplate: template
  })
  
  console.log('📤 [EmailTemplateSelectorModal] Emitting apply event with template')
  emit('apply', template)
}

const openSettings = () => {
  show.value = false
  emit('openSettings')
}

watch(show, (value) => {
  if (value) {
    nextTick(() => searchInput.value?.el?.focus())
  } else {
    // Emit close event to parent
    emit('close')
  }
})
</script>
