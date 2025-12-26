<template>
  <div class="grapesjs-email-editor-container">
    <!-- Merge Fields Button -->
    <div v-if="showMergeFieldsButton" class="merge-fields-button-container">
      <button @click="showMergeFieldsModal = true" class="merge-fields-button" title="Search merge fields">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        Search Fields
      </button>
    </div>

    <!-- Editor Container -->
    <div ref="editorContainer" class="flex-1 border" />

    <!-- Merge Fields Modal -->
    <div v-if="showMergeFieldsModal" class="merge-fields-modal-overlay" @click="showMergeFieldsModal = false">
      <div class="merge-fields-modal" @click.stop>
        <div class="modal-header">
          <h3>Search Merge Fields</h3>
          <button @click="showMergeFieldsModal = false" class="close-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="modal-content">
          <div class="search-container">
            <input v-model="searchTerm" type="text" placeholder="Type to search merge fields..." class="search-input" ref="searchInput" @keyup.enter="insertFirstResult" />
          </div>
          <div class="merge-fields-grid">
            <div v-for="field in filteredMergeFields" :key="field.name" class="merge-field-item" @click="insertMergeField(field)">
              <div class="field-name">{{ field.name }}</div>
              <div class="field-variable">{{ field.jinja_variable }}</div>
            </div>
          </div>
          <div v-if="filteredMergeFields.length === 0" class="no-results">
            No merge fields found for "{{ searchTerm }}"
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { createToast } from "@/utils"
import { createResource, call } from 'frappe-ui'
import { getDefaultEmailTemplate } from '@/utils/emailTemplates'

// Import GrapesJS and plugins
import grapesjs from 'grapesjs'
import pluginWebpage from 'grapesjs-preset-webpage'
import pluginExport from 'grapesjs-plugin-export'
import pluginNavbar from 'grapesjs-navbar'
import pluginCustomCode from 'grapesjs-custom-code'
import pluginFlexbox from 'grapesjs-blocks-flexbox'
import pluginForms from 'grapesjs-plugin-forms'
import pluginCountdown from 'grapesjs-component-countdown'
import pluginTabs from 'grapesjs-tabs'
import pluginStyleBG from 'grapesjs-style-bg'
import pluginLorySlider from 'grapesjs-lory-slider'
import pluginParserPostcss from 'grapesjs-parser-postcss'
import pluginNewsLetter from 'grapesjs-preset-newsletter'
import pluginStyleFilter from 'grapesjs-style-filter'
import pluginStyleGradient from 'grapesjs-style-gradient'
import pluginImageEditor from 'grapesjs-tui-image-editor'
import 'grapesjs/dist/css/grapes.min.css'

const props = defineProps({
  modelValue: {
    type: [String, Object],
    default: ''
  },
  initialCss: {
    type: String,
    default: ''
  },
  mergeFields: {
    type: Array,
    default: () => []
  },
  templateType: {
    type: String,
    default: ''
  },
  showMergeFields: {
    type: Boolean,
    default: true
  },
  autoLoadMergeFields: {
    type: Boolean,
    default: false
  },
  editorConfig: {
    type: Object,
    default: () => ({})
  },
  height: {
    type: String,
    default: '700px'
  }
})

const emit = defineEmits([
  'update:modelValue',
  'content-change',
  'css-change',
  'editor-ready',
  'editor-destroyed',
  'merge-fields-loaded'
])

const editorContainer = ref(null)
const internalMergeFields = ref([])
const showMergeFieldsModal = ref(false)
const searchTerm = ref('')
let editor = null
let isUpdatingFromProps = false

// Load merge fields from API
const loadMergeFields = async () => {
  if (!props.autoLoadMergeFields || !props.templateType) {
    return
  }

  try {
    const response = await createResource({
      url: "mbw_mira.mbw_mira.doctype.mira_merge_field_list.mira_merge_field_list.get_merge_fields",
      params: { template_type: props.templateType },
      auto: true,
      onSuccess: (data) => {
        console.log('Merge fields loaded: 1233444544', data)
        internalMergeFields.value = data?.map((item) => ({
          name: item.name,
          jinja_variable: item.jinja_variable,
        })) || []
        emit('merge-fields-loaded', internalMergeFields.value)
      },
    })
  } catch (error) {
    console.error("Error loading merge fields:", error)
  }
}

// Initialize editor
const initEditor = async () => {
  let csrf_token = ''
  if (window.csrf_token && window.csrf_token !== '{{ csrf_token }}') {
    csrf_token = window.csrf_token
  }

  // Load merge fields first if auto-load is enabled
  if (props.autoLoadMergeFields) {
    await loadMergeFields()
  }

  // Destroy existing editor if any
  if (editor) {
    editor.destroy()
    editor = null
  }

  // Wait for container to be available
  await nextTick()

  if (!editorContainer.value) {
    console.error('Editor container not found')
    return
  }

  // Get initial content
  let initialContent = ''
  if (typeof props.modelValue === 'string') {
    initialContent = props.modelValue
  } else if (props.modelValue && props.modelValue.html) {
    initialContent = props.modelValue.html
  }

  // Default configuration
  const defaultConfig = {
    container: editorContainer.value,
    plugins: [
      pluginWebpage,
      pluginExport,
      pluginNavbar,
      pluginCustomCode,
      pluginFlexbox,
      pluginForms,
      pluginCountdown,
      pluginTabs,
      pluginNewsLetter,
      pluginStyleFilter,
      pluginStyleGradient,
      pluginImageEditor,
    ],
    pluginsOpts: {
      [pluginWebpage]: {},
      [pluginExport]: {},
      [pluginNavbar]: {},
      [pluginCustomCode]: {},
      [pluginFlexbox]: {},
      [pluginForms]: {},
      [pluginCountdown]: {},
      [pluginTabs]: {},
      [pluginNewsLetter]: {
        modalTitleImport: 'Import HTML',
        modalTitleExport: 'Export HTML',
        importPlaceholder: '<table>...</table>',
        inlineCss: true,
      },
      [pluginStyleFilter]: {},
      [pluginStyleGradient]: {},
      [pluginImageEditor]: {},
    },
    // Load existing content - only use default if explicitly no content provided
    components: initialContent || '',
    style: props.initialCss || '',
    // Disable storage to prevent caching
    storageManager: false,
    // Device manager options
    deviceManager: {
      devices: [
        {
          name: 'Desktop',
          width: '',
        },
        {
          name: 'Tablet',
          width: '768px',
          widthMedia: '992px',
        },
        {
          name: 'Mobile',
          width: '320px',
          widthMedia: '480px',
        },
      ],
    },
    // Enable panels for device manager - use built-in device panel
    panels: {
      defaults: [
        {
          id: 'devices-c',
          el: '.panel__devices',
          buttons: [
            {
              id: 'device-desktop',
              label: '<i class="fa fa-desktop"></i>',
              command: 'set-device-desktop',
              active: true,
              togglable: false,
            },
            {
              id: 'device-tablet',
              label: '<i class="fa fa-tablet"></i>',
              command: 'set-device-tablet',
              togglable: false,
            },
            {
              id: 'device-mobile',
              label: '<i class="fa fa-mobile"></i>',
              command: 'set-device-mobile',
              togglable: false,
            },
          ],
        },
      ],
    },
    // Set project type to email
    project: {
      type: 'email',
      assets: [],
    },
    // Canvas options - minimal for email
    canvas: {
      styles: [
        'https://unpkg.com/grapesjs/dist/css/grapes.min.css'
      ]
    },
    // Asset manager
    assetManager: {
      embedAsBase64: false,
      upload: "/api/method/mbw_mira.api.upload_image",
      headers: {
        'X-Frappe-CSRF-Token': csrf_token
      },
      uploadName: 'files',
    },
    // Undo manager
    undoManager: {
      trackSelection: false,
    },
  }

  // Merge with custom config
  const finalConfig = { ...defaultConfig, ...props.editorConfig }

  editor = grapesjs.init(finalConfig)

  // Content will be loaded in the 'load' event handler

  // Add device commands
  editor.Commands.add('set-device-desktop', {
    run: (editor) => {
      editor.setDevice('Desktop')
    }
  })

  editor.Commands.add('set-device-tablet', {
    run: (editor) => {
      editor.setDevice('Tablet')
    }
  })

  editor.Commands.add('set-device-mobile', {
    run: (editor) => {
      editor.setDevice('Mobile')
    }
  })

  // Add merge field blocks after editor loads
  editor.on('load', () => {
    if (props.showMergeFields) {
      addMergeFieldBlocks()
    }

    // Load merge fields if auto-load is enabled
    if (props.autoLoadMergeFields) {
      loadMergeFields()
    }

    // Load initial content after editor is fully loaded
    if (initialContent && initialContent.trim() !== '') {
      // Clean HTML content for GrapesJS
      let cleanContent = initialContent

      // First, try to extract body content
      const bodyMatch = cleanContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
      if (bodyMatch) {
        cleanContent = bodyMatch[1]
      } else {
        // If no body tag, remove only problematic tags
        cleanContent = cleanContent.replace(/<!DOCTYPE[^>]*>/gi, '')
        cleanContent = cleanContent.replace(/<html[^>]*>/gi, '')
        cleanContent = cleanContent.replace(/<\/html>/gi, '')
        cleanContent = cleanContent.replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
        cleanContent = cleanContent.replace(/<meta\s+charset[^>]*>/gi, '')
      }

      // Remove empty lines and trim
      cleanContent = cleanContent.replace(/^\s*[\r\n]/gm, '').trim()

      if (cleanContent && cleanContent.trim() !== '') {
        try {
          editor.setComponents(cleanContent)

          // Load CSS if available
          if (props.initialCss && props.initialCss.trim() !== '') {
            editor.setStyle(props.initialCss)
            // IMPORTANT: Inject CSS directly into iframe immediately
            injectCssIntoIframe(props.initialCss)
          }
        } catch (error) {
          console.error('[GrapesJS] Error loading content:', error)
          editor.setComponents(getDefaultEmailTemplate())
        }
      }
    }

    // IMPORTANT: Always inject CSS into iframe after editor load
    if (props.initialCss && props.initialCss.trim() !== '') {
      setTimeout(() => {
        injectCssIntoIframe(props.initialCss)
      }, 300)
    }

    // Emit ready event
    emit('editor-ready', editor)
  })

  // Listen for component selection - ensure CSS is injected
  editor.on('component:selected', () => {
    if (props.initialCss && props.initialCss.trim() !== '') {
      injectCssIntoIframe(props.initialCss)
    }
  })

  // Listen for content changes
  editor.on('component:update', () => {
    if (props.initialCss && props.initialCss.trim() !== '') {
      injectCssIntoIframe(props.initialCss)
    }
    if (!isUpdatingFromProps) {
      emitContentChange()
    }
  })

  editor.on('style:update', () => {
    if (!isUpdatingFromProps) {
      emitCssChange()
      // IMPORTANT: Always use props.initialCss (from css_content)
      if (props.initialCss && props.initialCss.trim() !== '') {
        injectCssIntoIframe(props.initialCss)
      } else {
        injectCssIntoIframe(editor.getCss())
      }
    }
  })

  // Listen for when blocks/components are added - ensure CSS is injected
  editor.on('component:add', () => {
    if (props.initialCss && props.initialCss.trim() !== '') {
      setTimeout(() => {
        injectCssIntoIframe(props.initialCss)
      }, 100)
    }
  })

  const am = editor.AssetManager
  editor.on('asset:upload:response', (response) => {
    am.add(response.message)
  })
}

// Function to inject CSS directly into the iframe
const injectCssIntoIframe = (css) => {
  // Priority: Always use props.initialCss (from css_content) if available
  const cssToInject = (props.initialCss && props.initialCss.trim() !== '') ? props.initialCss : css
  
  if (!editor || !cssToInject || cssToInject.trim() === '') {
    return
  }
  
  try {
    const canvas = editor.Canvas
    if (!canvas) return
    
    const iframe = canvas.getFrameEl()
    if (!iframe || !iframe.contentDocument) return
    
    const iframeDoc = iframe.contentDocument
    const iframeHead = iframeDoc.head || iframeDoc.getElementsByTagName('head')[0]
    if (!iframeHead) return
    
    // Remove existing custom style tag if any
    let styleTag = iframeDoc.getElementById('gjs-custom-style')
    if (!styleTag) {
      styleTag = iframeDoc.createElement('style')
      styleTag.id = 'gjs-custom-style'
      iframeHead.appendChild(styleTag)
    }
    
    // Update style content
    styleTag.textContent = cssToInject
  } catch (error) {
    console.error('[GrapesJS] Error injecting CSS:', error)
  }
}

// Get default email template

// Add merge field blocks
const addMergeFieldBlocks = () => {
  if (!editor) return

  editor.Panels.addButton('options', {
    id: 'open-merge-tag',
    className: 'fa fa-tags',
    command: 'open-merge-tag-popup',
    attributes: {
      title: 'Chèn Merge Tag'
    }
  })

  // Use internal merge fields if auto-load is enabled, otherwise use props
  const fieldsToUse = props.autoLoadMergeFields ? internalMergeFields.value : props.mergeFields

  if (!fieldsToUse.length) return

  editor.Commands.add('open-merge-tag-popup', {
    run(editor) {
      const modal = editor.Modal
      const content = document.createElement('div')

      content.innerHTML = `
        <style>
          .merge-tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 10px;
          }

          .merge-tag-chip {
            background-color: #cce5ff;
            color: #004085;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            border: 1px solid #b8daff;
            cursor: pointer;
            white-space: nowrap;
            transition: background-color 0.2s;
          }

          .merge-tag-chip:hover {
            background-color: #b8daff;
          }
        </style>

        <div class="merge-tag-list" id="merge-tag-list"></div>
      `

      const listEl = content.querySelector('#merge-tag-list')

      fieldsToUse.forEach(tag => {
        const btn = document.createElement('button')
        btn.className = 'merge-tag-chip'
        btn.innerText = tag.name
        btn.onclick = () => {
          const selected = editor.getSelected()
          const insertText = tag.jinja_variable

          if (selected?.is('text') || selected?.is('paragraph')) {
            const current = selected.components().map(comp => comp.toHTML()).join('')
            selected.components(current + insertText)
          } else {
            editor.RichTextEditor?.insertHTML?.(insertText)
          }

          modal.close()
        }

        listEl.appendChild(btn)
      })

      modal.setTitle('🔗 Chèn Merge Tag')
      modal.setContent(content)
      modal.open()
    }
  })
}

// Emit content change
const emitContentChange = () => {
  if (editor) {
    const html = editor.getHtml()
    const css = editor.getCss()

    emit('content-change', html)
    emit('update:modelValue', {
      html,
      css,
      blocks: [], // GrapesJS doesn't use blocks like the custom builder
      mjml: '' // Could be implemented if needed
    })
  }
}

// Emit CSS change
const emitCssChange = () => {
  if (editor) {
    const css = editor.getCss()
    console.log('📦 [GrapesJS] Emitting CSS content:121212121 12121212', css)
    emit('css-change', css)
  }
}

// Public methods
const getHtml = () => {
  console.log('🔍 [GrapesJS] getHtml() called, editor exists:', !!editor)
  const html = editor ? editor.getHtml() : ''
  console.log('🔍 [GrapesJS] HTML length:', html.length)
  return html
}

const getCss = () => {
  console.log('🔍 [GrapesJS] getCss() called, editor exists:', !!editor)
  const css = editor ? editor.getCss() : ''
  console.log('🔍 [GrapesJS] CSS length:', css.length)
  return css
}

const setComponents = (components) => {
  if (editor) {
    editor.setComponents(components)
  }
}

const setStyle = (css) => {
  if (editor) {
    editor.setStyle(css)
  }
}

const destroy = () => {
  if (editor) {
    editor.destroy()
    editor = null
    emit('editor-destroyed')
  }
}

const reload = async () => {
  await initEditor()
}

// Computed properties
const totalMergeFields = computed(() => {
  const fieldsToUse = props.autoLoadMergeFields ? internalMergeFields.value : props.mergeFields
  return fieldsToUse.length
})

const showMergeFieldsButton = computed(() => {
  return false // Hidden as we use the toolbar button instead
})

const filteredMergeFields = computed(() => {
  const fieldsToUse = props.autoLoadMergeFields ? internalMergeFields.value : props.mergeFields
  if (!searchTerm.value) return fieldsToUse

  return fieldsToUse.filter(field =>
    field.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    field.jinja_variable.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

// Insert merge field into editor
const insertMergeField = (field) => {
  if (!editor) return

  const fieldName = field.jinja_variable.replace(/[{}]/g, '')
  const component = editor.addComponent({
    type: 'text',
    content: `{{${fieldName}}}`,
    style: {
      'background-color': '#dc3545',
      'padding': '4px 8px',
      'border-radius': '4px',
      'color': '#ffffff',
      'font-weight': '500',
      'font-family': 'Arial, sans-serif',
      'border': '1px solid #c82333',
      'display': 'inline-block',
      'margin': '2px'
    }
  })

  // Add to selected component or at cursor position
  const selected = editor.getSelected()
  if (selected && selected.is('text')) {
    selected.append(component)
  } else {
    editor.addComponent(component)
  }

  showMergeFieldsModal.value = false
  searchTerm.value = ''
}

// Insert first search result
const insertFirstResult = () => {
  if (filteredMergeFields.value.length > 0) {
    insertMergeField(filteredMergeFields.value[0])
  }
}

// Expose public methods
defineExpose({
  getHtml,
  getCss,
  setComponents,
  setStyle,
  destroy,
  reload,
  editor: () => editor,
  getBlocks: () => {
    console.log('🔍 [GrapesJS] getBlocks() called - returning empty array')
    return []
  },
  getMJML: () => {
    console.log('🔍 [GrapesJS] getMJML() called - returning empty string')
    return ''
  },
  exportHtml: () => {
    console.log('🔍 [GrapesJS] exportHtml() called')
    const html = getHtml()
    const css = getCss()
    console.log('🔍 [GrapesJS] Raw HTML:', html.substring(0, 200) + '...')
    console.log('🔍 [GrapesJS] Raw CSS:', css.substring(0, 200) + '...')
    console.log('🔍 [GrapesJS] CSS length:', css.length)
    const result = {
      html,
      css,
      blocks: [],
      mjml: '',
      emailSettings: {}
    }
    console.log('🔍 [GrapesJS] exportHtml() result CSS:', result.css.substring(0, 200) + '...')
    return result
  }
})

// Lifecycle
onMounted(async () => {
  await initEditor()
})

onUnmounted(() => {
  destroy()
})

// Watch for prop changes
watch(() => props.modelValue, (newValue) => {
  if (editor && newValue) {
    isUpdatingFromProps = true

    let content = ''
    if (typeof newValue === 'string') {
      content = newValue
    } else if (newValue && newValue.html) {
      content = newValue.html
    }

    // IMPORTANT: Only update if we have actual content
    // Don't clear editor if content is empty - preserve existing content
    if (content && content.trim() !== '') {
      console.log('🔄 [GrapesJS] Updating components from modelValue, length:', content.length)
      editor.setComponents(content)
    } else {
      console.log('⚠️ [GrapesJS] modelValue is empty, preserving existing editor content')
      // Don't clear - preserve what user has already added
    }

    setTimeout(() => {
      isUpdatingFromProps = false
    }, 100)
  }
})

watch(() => props.initialCss, (newCss) => {
  if (editor && newCss && newCss.trim() !== '') {
    isUpdatingFromProps = true
    try {
      editor.setStyle(newCss)
      // IMPORTANT: Inject CSS directly into iframe immediately when prop changes
      setTimeout(() => {
        injectCssIntoIframe(newCss)
      }, 100)
    } catch (error) {
      console.error('[GrapesJS] Error updating CSS:', error)
    }
    setTimeout(() => {
      isUpdatingFromProps = false
    }, 200)
  }
})

watch(() => props.mergeFields, () => {
  if (editor && props.showMergeFields && !props.autoLoadMergeFields) {
    addMergeFieldBlocks()
  }
})

watch(() => internalMergeFields, () => {
  if (editor && props.showMergeFields && props.autoLoadMergeFields) {
    addMergeFieldBlocks()
  }
}, { deep: true })

// Focus search input when modal opens
watch(() => showMergeFieldsModal, (isOpen) => {
  if (isOpen) {
    nextTick(() => {
      const searchInput = document.querySelector('.search-input')
      if (searchInput) {
        searchInput.focus()
      }
    })
  }
})
</script>

<style scoped>
.grapesjs-email-editor-container {
  height: v-bind(height);
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

/* Merge Fields Button */
.merge-fields-button-container {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
}

.merge-fields-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.merge-fields-button:hover {
  background: #0056b3;
}

/* Modal Styles */
.merge-fields-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.merge-fields-modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-button:hover {
  background: #f3f4f6;
}

.modal-content {
  padding: 24px;
  overflow-y: auto;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.merge-fields-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 12px;
}

.merge-field-item {
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.merge-field-item:hover {
  border-color: #007bff;
  background: #f8faff;
}

.field-name {
  font-weight: 500;
  font-size: 14px;
  color: #374151;
  margin-bottom: 4px;
}

.field-variable {
  font-size: 12px;
  color: #6b7280;
  font-family: 'Courier New', monospace;
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
}

.no-results {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
  font-style: italic;
}

/* GrapesJS Styling */
:deep(.gjs-one-bg) {
  background-color: #2c2c2c;
}

:deep(.gjs-two-color) {
  color: #fff;
}

:deep(.gjs-three-bg) {
  background-color: #007bff;
}

:deep(.gjs-four-color) {
  color: #007bff;
}

:deep(.gjs-pn-btn) {
  border-radius: 4px;
  margin: 2px;
}

:deep(.gjs-pn-btn:hover) {
  background-color: #007bff;
}

:deep(.gjs-frame) {
  border: 2px solid #007bff;
  border-radius: 4px;
  margin: 0 auto;
  display: block;
}

:deep(.gjs-toolbar) {
  background: #2c2c2c;
  border: 1px solid #555;
  border-radius: 4px;
}

:deep(.gjs-toolbar-item) {
  color: #fff;
  padding: 4px 8px;
  border-radius: 2px;
  margin: 1px;
}

:deep(.gjs-toolbar-item:hover) {
  background: #007bff;
}

:deep(.gjs-clm-states),
:deep(.gjs-sm-sector),
:deep(.gjs-sm-properties),
:deep(.gjs-sm-properties select),
:deep(.gjs-sm-properties input),
:deep(.gjs-sm-properties button),
:deep(.gjs-sm-properties textarea),
:deep(.gjs-sm-properties label),
:deep(.gjs-sm-properties *) {
  font-size: 11px;
}

:deep(.gjs-sm-sector),
:deep(.gjs-sm-properties) {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 12px;
}
</style>
