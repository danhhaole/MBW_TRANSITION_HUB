<template>
  <div class="email-builder-wrapper">
    <!-- GrapesJS Email Editor -->
    <div class="main-container flex-1">
      <GrapesJSEmailEditor
        ref="grapesJSEditor"
        :model-value="initialContent || modelValue"
        :initial-css="effectiveInitialCss"
        :merge-fields="mergeFields"
        :template-type="templateType"
        :show-merge-fields="showMergeFields"
        :auto-load-merge-fields="autoLoadMergeFields"
        :editor-config="editorConfig"
        :height="editorHeight"
        @update:model-value="handleEditorUpdate"
        @content-change="handleContentChange"
        @css-change="handleCssChange"
        @editor-ready="handleEditorReady"
        @editor-destroyed="handleEditorDestroyed"
        @merge-fields-loaded="handleMergeFieldsLoaded"
      />
    </div>

    <!-- Preview Dialog -->
    <div v-if="showPreview" class="preview-overlay" @click="showPreview = false">
      <div class="preview-dialog" @click.stop>
        <div class="preview-header">
          <div class="flex items-center gap-2">
            <h3 class="text-lg font-semibold">Email Preview</h3>
            <div class="flex border border-gray-300 rounded-md overflow-hidden ml-4">
              <button
                v-for="device in devices"
                :key="device.value"
                @click="selectedDevice = device.value"
                :class="[
                  'px-3 py-1.5 text-xs font-medium transition-colors',
                  selectedDevice === device.value
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                ]"
              >
                <FeatherIcon :name="device.icon" class="w-4 h-4" />
              </button>
            </div>
          </div>
          <Button
            icon="x"
            variant="ghost"
            @click="showPreview = false"
          />
        </div>
        <div class="preview-body">
          <div
            class="preview-frame"
            :style="{ maxWidth: deviceWidth }"
          >
            <div v-html="previewHtml" class="preview-content"></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import GrapesJSEmailEditor from './GrapesJSEmailEditor.vue'

const props = defineProps({
  modelValue: {
    type: [String, Object],
    default: null
  },
  height: {
    type: String,
    default: '700px'
  },
  // GrapesJS specific props
  initialContent: {
    type: String,
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
  }
})

const emit = defineEmits(['update:modelValue', 'ready', 'content-change', 'css-change', 'editor-ready', 'editor-destroyed', 'merge-fields-loaded'])
// Computed property to ensure we always have a string for initialCss
const effectiveInitialCss = computed(() => {
  return props.initialCss || ''
})
// Watch for changes to initialCss and update the editor if needed
watch(() => props.initialCss, (newCss) => {
  if (newCss && newCss.trim() !== '') {
    console.log('🎨 [EmailBuilder] initialCss changed, updating editor...')
    const editor = grapesJSEditor.value
    if (editor) {
      // Use nextTick to ensure the editor is ready
      nextTick(() => {
        try {
          editor.setStyle(newCss)
          console.log('✅ [EmailBuilder] Updated editor with new CSS')
        } catch (error) {
          console.error('❌ [EmailBuilder] Error updating CSS:', error)
        }
      })
    }
  }
})

// Refs
const grapesJSEditor = ref(null)

// Preview state
const showPreview = ref(false)
const selectedDevice = ref('desktop')
const currentContent = ref('')

// Device configurations
const devices = [
  { value: 'desktop', label: 'Desktop', icon: 'monitor', width: '100%' },
  { value: 'tablet', label: 'Tablet', icon: 'tablet', width: '768px' },
  { value: 'mobile', label: 'Mobile', icon: 'smartphone', width: '375px' }
]

const deviceWidth = computed(() => {
  const device = devices.find(d => d.value === selectedDevice.value)
  return device ? device.width : '100%'
})

const editorHeight = computed(() => {
  return `calc(${props.height} - 60px)` // Subtract toolbar height
})

const previewHtml = computed(() => {
  if (!currentContent.value) {
    return '<p style="text-align: center; padding: 40px; color: #999;">No content to preview</p>'
  }

  return currentContent.value
})

// Event handlers for GrapesJS editor
const handleEditorUpdate = (value) => {
  currentContent.value = value.html || ''
  emit('update:modelValue', value)
}

const handleContentChange = (html) => {
  currentContent.value = html
  emit('content-change', html)
}

const handleCssChange = (css) => {
  emit('css-change', css)
}

const handleEditorReady = (editor) => {
  emit('editor-ready', editor)
  emit('ready', {
    getHtml: () => grapesJSEditor.value?.getHtml() || '',
    getBlocks: () => [],
    getMJML: () => '',
    exportHtml: () => grapesJSEditor.value?.exportHtml() || {}
  })
}

const handleEditorDestroyed = () => {
  emit('editor-destroyed')
}

const handleMergeFieldsLoaded = (fields) => {
  emit('merge-fields-loaded', fields)
}

// Lifecycle
onMounted(async () => {
  console.log('✅ [EmailBuilder] Ready with GrapesJS')
  console.log('🎨 [EmailBuilder] Initial CSS received:', props.initialCss?.length || 0, 'characters')
  console.log('🎨 [EmailBuilder] Initial CSS preview:', props.initialCss?.substring(0, 200) + '...')
  console.log('🎨 [EmailBuilder] Initial CSS full value:', props.initialCss)
  console.log('📄 [EmailBuilder] Initial content received:', props.initialContent?.length || 0, 'characters')
  console.log('📄 [EmailBuilder] Initial content preview:', props.initialContent?.substring(0, 200) + '...')
})

onBeforeUnmount(() => {
  // Cleanup handled by GrapesJS editor component
})

// Expose methods for external use
defineExpose({
  getHtml: () => grapesJSEditor.value?.getHtml() || '',
  getCss: () => grapesJSEditor.value?.getCss() || '',
  getBlocks: () => grapesJSEditor.value?.getBlocks() || [],
  getMJML: () => grapesJSEditor.value?.getMJML() || '',
  setBlocks: () => {},
  exportHtml: () => grapesJSEditor.value?.exportHtml() || {
    html: '',
    css: '',
    blocks: [],
    mjml: '',
    emailSettings: {}
  },
  reinitializeSortables: () => {}
})
</script>

<style scoped>
.email-builder-wrapper {
  height: v-bind(height);
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

/* Main flex container */
.main-container {
  flex: 1;
  min-height: 0;
}

/* Toolbar */
.toolbar {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  background: #fafafa;
  flex-shrink: 0;
}

/* Preview Overlay */
.preview-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.preview-dialog {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 1200px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.preview-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: #f5f5f5;
  display: flex;
  justify-content: center;
}

.preview-frame {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  width: 100%;
  transition: max-width 0.3s ease;
  margin: 0 auto;
}

.preview-content {
  padding: 20px;
  min-height: 400px;
}

/* Sortable styles */
:deep(.sortable-ghost) {
  opacity: 0.4;
  background: #dbeafe !important;
  border: 2px dashed #3b82f6 !important;
}

:deep(.sortable-drag) {
  opacity: 0.9;
  cursor: grabbing !important;
}
</style>
