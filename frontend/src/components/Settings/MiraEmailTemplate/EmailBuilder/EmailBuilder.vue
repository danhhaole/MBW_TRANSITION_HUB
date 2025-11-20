<template>
  <div class="email-builder-wrapper">
    <!-- Toolbar -->
    <div class="toolbar">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-sm font-medium text-gray-700">Email Design</span>
          <span class="text-xs text-gray-500">{{ blocks.length }} blocks</span>
        </div>
        <div class="flex items-center gap-2">
          <!-- Email Settings Button -->
          <Button
            label="Email Settings"
            icon="settings"
            :variant="showEmailSettings ? 'solid' : 'outline'"
            size="sm"
            @click="toggleEmailSettings"
          />
          <!-- Preview Button -->
          <Button
            label="Preview"
            icon="eye"
            variant="solid"
            size="sm"
            @click="showPreview = true"
          />
        </div>
      </div>
    </div>

    <div class="main-container flex flex-1">
      <!-- Left Sidebar -->
      <Sidebar ref="sidebarRef" />

      <!-- Center Canvas -->
      <Canvas
        ref="canvasRef"
        :blocks="blocks"
        :selected-index="selectedBlockIndex"
        :email-settings="emailSettings"
        @select="selectBlock"
        @delete="removeBlock"
        @duplicate="duplicateBlock"
        @select-nested="selectNestedBlock"
      />

      <!-- Right Properties Panel -->
      <Properties
        :block="selectedBlock"
        :show-email-settings="showEmailSettings"
        :email-settings="emailSettings"
        @close="deselectBlock"
        @change="onChange"
        @update-email-settings="updateEmailSettings"
        @set-email-align="setEmailAlign"
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
import Sortable from 'sortablejs'
import Sidebar from './Sidebar.vue'
import Canvas from './Canvas.vue'
import Properties from './Properties.vue'
import { defaultBlockProps } from './blocks'
import { blocksToMJML, renderHTML } from './utils'
import mjml2html from 'mjml-browser'

const props = defineProps({
  modelValue: {
    type: [String, Object],
    default: null
  },
  height: {
    type: String,
    default: '700px'
  }
})

const emit = defineEmits(['update:modelValue', 'ready'])

// Refs
const sidebarRef = ref(null)
const canvasRef = ref(null)

// Sortable instances
let contentSortable = null
let layout2Sortable = null
let layout3Sortable = null
let canvasSortable = null

// State
const blocks = ref([])
const selectedBlockIndex = ref(null)
const selectedNestedBlock = ref(null) // { blockId, columnIndex, child }

// Preview state
const showPreview = ref(false)
const selectedDevice = ref('desktop')

// Email settings state
const showEmailSettings = ref(false)
const emailSettings = ref({
  backgroundColor: '#ffffff',
  contentWidth: 600,
  contentAlign: 'center',
  fontFamily: 'Arial, sans-serif'
})

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

const previewHtml = computed(() => {
  // Check if modelValue is already MJML string
  if (typeof props.modelValue === 'string' && props.modelValue.trim().startsWith('<mjml>')) {
    try {
      return renderHTML([]) // Use renderHTML with empty array to get the MJML converted
    } catch (error) {
      // If that fails, try to render the MJML directly
      try {
        const { html } = mjml2html(props.modelValue)
        return html
      } catch (mjmlError) {
        console.error('MJML render error:', mjmlError)
        return '<p style="text-align: center; padding: 40px; color: #f00;">Error rendering MJML</p>'
      }
    }
  }
  
  // Ensure blocks is an array
  const blocksArray = Array.isArray(blocks.value) ? blocks.value : []
  
  if (blocksArray.length === 0) {
    return '<p style="text-align: center; padding: 40px; color: #999;">No content to preview</p>'
  }
  
  try {
    const mjml = blocksToMJML(blocksArray, emailSettings.value)
    const { html } = mjml2html(mjml)
    return html
  } catch (error) {
    console.error('Preview render error:', error)
    return '<p style="text-align: center; padding: 40px; color: #f00;">Error rendering preview</p>'
  }
})

const selectedBlock = computed(() => {
  // If nested block selected, show its properties
  if (selectedNestedBlock.value) {
    return selectedNestedBlock.value.child
  }
  // Otherwise show parent block
  if (selectedBlockIndex.value !== null) {
    return blocks.value[selectedBlockIndex.value]
  }
  return null
})

// Initialize SortableJS
onMounted(async () => {
  await nextTick()
  
  const sortableConfig = {
    group: {
      name: 'email-blocks',
      pull: 'clone',
      put: false
    },
    sort: false,
    animation: 150,
    // Don't remove anything - Sortable handles clones automatically
  }

  // Content blocks
  if (sidebarRef.value?.contentList) {
    contentSortable = Sortable.create(sidebarRef.value.contentList, sortableConfig)
  }

  // Layout blocks
  if (sidebarRef.value?.layout2Col) {
    layout2Sortable = Sortable.create(sidebarRef.value.layout2Col, sortableConfig)
  }
  if (sidebarRef.value?.layout3Col) {
    layout3Sortable = Sortable.create(sidebarRef.value.layout3Col, sortableConfig)
  }

  // Canvas (drop zone)
  if (canvasRef.value?.canvasContainer) {
    canvasSortable = Sortable.create(canvasRef.value.canvasContainer, {
      group: {
        name: 'email-blocks',
        pull: false,
        put: true
      },
      animation: 150,
      handle: '.email-block',
      ghostClass: 'sortable-ghost',
      dragClass: 'sortable-drag',
      onAdd: (evt) => {
        const blockType = evt.item.dataset.type
        if (blockType) {
          addBlock(blockType, evt.newIndex)
          evt.item.parentNode.removeChild(evt.item)
          
          // Setup nested sortables for layout columns
          setTimeout(() => setupNestedSortables(), 100)
        }
      },
      onUpdate: (evt) => {
        const movedBlock = blocks.value.splice(evt.oldIndex, 1)[0]
        blocks.value.splice(evt.newIndex, 0, movedBlock)
        onChange()
      }
    })
  }
  
  // Setup nested sortables initially
  setupNestedSortables()

  emit('ready', {
    getHtml: () => renderHTML(blocks.value),
    getBlocks: () => blocks.value,
    getMJML: () => blocksToMJML(blocks.value),
  })

  console.log('✅ [EmailBuilder] Ready')
})

// Reinitialize sortables (useful after DOM changes)
function reinitializeSortables() {
  // Destroy existing sortables
  if (contentSortable) contentSortable.destroy()
  if (layout2Sortable) layout2Sortable.destroy()
  if (layout3Sortable) layout3Sortable.destroy()
  if (canvasSortable) canvasSortable.destroy()
  
  // Wait for DOM update then reinitialize
  nextTick(() => {
    const sortableConfig = {
      group: {
        name: 'email-blocks',
        pull: 'clone',
        put: false
      },
      sort: false,
      animation: 150,
    }

    // Recreate sortables
    if (sidebarRef.value?.contentList) {
      contentSortable = Sortable.create(sidebarRef.value.contentList, sortableConfig)
    }
    if (sidebarRef.value?.layout2Col) {
      layout2Sortable = Sortable.create(sidebarRef.value.layout2Col, sortableConfig)
    }
    if (sidebarRef.value?.layout3Col) {
      layout3Sortable = Sortable.create(sidebarRef.value.layout3Col, sortableConfig)
    }
    
    if (canvasRef.value?.canvasContainer) {
      canvasSortable = Sortable.create(canvasRef.value.canvasContainer, {
        group: {
          name: 'email-blocks',
          pull: false,
          put: true
        },
        animation: 150,
        handle: '.email-block',
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        onAdd: (evt) => {
          const blockType = evt.item.dataset.type
          if (blockType) {
            addBlock(blockType, evt.newIndex)
            evt.item.remove()
          }
        }
      })
    }
  })
}

// Setup nested sortables for layout columns
function setupNestedSortables() {
  if (!canvasRef.value?.canvasContainer) return
  
  // Find all layout columns
  const layoutColumns = canvasRef.value.canvasContainer.querySelectorAll('.layout-column')
  
  layoutColumns.forEach((columnEl) => {
    // Skip if already initialized
    if (columnEl.dataset.sortableInitialized) return
    columnEl.dataset.sortableInitialized = 'true'
    
    const columnIndex = parseInt(columnEl.dataset.column)
    const blockEl = columnEl.closest('.email-block')
    const blockId = blockEl?.dataset.id
    
    if (!blockId) return
    
    const block = blocks.value.find(b => b.id == blockId)
    if (!block || !block.children) return
    
    Sortable.create(columnEl, {
      group: 'email-blocks',
      animation: 150,
      ghostClass: 'sortable-ghost',
      onAdd: (evt) => {
        const blockType = evt.item.dataset.type
        if (blockType && block.children[columnIndex]) {
          // Check if column already has an element
          if (block.children[columnIndex].length > 0) {
            // Replace existing element instead of adding
            const newChild = {
              id: Date.now(),
              type: blockType,
              props: { ...defaultBlockProps[blockType] }
            }
            block.children[columnIndex] = [newChild] // Replace with single element
          } else {
            // Add to empty column
            const newChild = {
              id: Date.now(),
              type: blockType,
              props: { ...defaultBlockProps[blockType] }
            }
            block.children[columnIndex].push(newChild)
          }
          evt.item.parentNode.removeChild(evt.item)
          onChange()
        }
      },
      onUpdate: (evt) => {
        // Since we only allow 1 element per column, onUpdate shouldn't happen
        // But handle it gracefully if it does
        if (block.children[columnIndex] && block.children[columnIndex].length <= 1) {
          const movedChild = block.children[columnIndex].splice(evt.oldIndex, 1)[0]
          block.children[columnIndex].splice(evt.newIndex, 0, movedChild)
          onChange()
        }
      }
    })
  })
}

onBeforeUnmount(() => {
  if (contentSortable) contentSortable.destroy()
  if (layout2Sortable) layout2Sortable.destroy()
  if (layout3Sortable) layout3Sortable.destroy()
  if (canvasSortable) canvasSortable.destroy()
})

// Add block
function addBlock(type, index = null) {
  const newBlock = {
    id: Date.now(),
    type,
    props: { ...defaultBlockProps[type] }
  }

  // Layout blocks can have nested children
  if (type.startsWith('col-')) {
    const colCount = type.startsWith('col-2') ? 2 : 3
    newBlock.children = Array.from({ length: colCount }, () => [])
  }

  if (index !== null) {
    blocks.value.splice(index, 0, newBlock)
  } else {
    blocks.value.push(newBlock)
  }
  
  onChange()
}

// Remove block
function removeBlock(index) {
  blocks.value.splice(index, 1)
  selectedBlockIndex.value = null
  onChange()
}

// Duplicate block
function duplicateBlock(index) {
  const originalBlock = blocks.value[index]
  // Deep clone the block
  const clonedBlock = JSON.parse(JSON.stringify(originalBlock))
  // Generate new unique ID
  clonedBlock.id = Date.now() + Math.random()
  // Insert right after the original block
  blocks.value.splice(index + 1, 0, clonedBlock)
  // Select the new block
  selectedBlockIndex.value = index + 1
  onChange()
}

// Select block (parent)
function selectBlock(index) {
  selectedBlockIndex.value = index
  selectedNestedBlock.value = null // Clear nested selection
  showEmailSettings.value = false // Turn off Email Settings when selecting block
}

// Select nested block (child inside layout)
function selectNestedBlock(data) {
  selectedNestedBlock.value = data
  selectedBlockIndex.value = null // Clear parent selection
  showEmailSettings.value = false // Turn off Email Settings when selecting nested block
}

// Deselect block
function deselectBlock() {
  selectedBlockIndex.value = null
  selectedNestedBlock.value = null
  // Don't turn off Email Settings here - let user keep it open if they want
}

// On change
function onChange() {
  const blocksArray = Array.isArray(blocks.value) ? blocks.value : []
  const html = renderHTML(blocksArray)
  
  emit('update:modelValue', {
    html,
    blocks: blocksArray,
    mjml: blocksToMJML(blocksArray)
  })
}

// Load existing design
watch(() => props.modelValue, (newValue) => {
  console.log('[EmailBuilder] Loading modelValue:', newValue)
  
  if (!newValue) {
    blocks.value = []
    return
  }
  
  try {
    // Handle different data formats
    let data = newValue
    
    // If it's a string, try to parse as JSON first
    if (typeof newValue === 'string') {
      // Check if it's MJML string (starts with <mjml>)
      if (newValue.trim().startsWith('<mjml>')) {
        console.log('[EmailBuilder] Detected MJML string, initializing empty blocks')
        blocks.value = []
        return
      }
      
      // Try to parse as JSON
      try {
        data = JSON.parse(newValue)
      } catch (parseError) {
        console.log('[EmailBuilder] String is not JSON, treating as raw string')
        blocks.value = []
        return
      }
    }
    
    console.log('[EmailBuilder] Parsed data:', data)
    
    // If data is array directly (old format), use it
    if (Array.isArray(data)) {
      blocks.value = data
      console.log('[EmailBuilder] Set blocks from array:', blocks.value)
    }
    // If data has blocks property (new format), use blocks
    else if (data && data.blocks && Array.isArray(data.blocks)) {
      blocks.value = data.blocks
      console.log('[EmailBuilder] Set blocks from data.blocks:', blocks.value)
    }
    // Otherwise, initialize empty
    else {
      blocks.value = []
      console.log('[EmailBuilder] Set blocks to empty array - unknown format')
    }
    
    console.log('[EmailBuilder] Final blocks value:', blocks.value, 'isArray:', Array.isArray(blocks.value))
    
    // Re-setup nested sortables after loading
    if (blocks.value.length > 0) {
      setTimeout(() => setupNestedSortables(), 200)
    }
  } catch (error) {
    console.error('Error loading email design:', error)
    blocks.value = []
  }
}, { immediate: true })

// Watch blocks changes to re-setup nested sortables
watch(() => blocks.value.length, () => {
  setTimeout(() => setupNestedSortables(), 100)
})

// Email settings methods
function updateEmailSettings(updates = {}) {
  Object.assign(emailSettings.value, updates)
  onChange()
}

function setEmailAlign(align) {
  emailSettings.value.contentAlign = align
  onChange()
}

function toggleEmailSettings() {
  showEmailSettings.value = !showEmailSettings.value
  // Deselect any block when showing email settings
  if (showEmailSettings.value) {
    selectedBlockIndex.value = null
    selectedNestedBlock.value = null
  }
}

// Expose methods
defineExpose({
  getHtml: () => {
    const blocksArray = Array.isArray(blocks.value) ? blocks.value : []
    return renderHTML(blocksArray)
  },
  getBlocks: () => blocks.value,
  getMJML: () => {
    const blocksArray = Array.isArray(blocks.value) ? blocks.value : []
    return blocksToMJML(blocksArray, emailSettings.value)
  },
  setBlocks: (newBlocks) => {
    blocks.value = Array.isArray(newBlocks) ? newBlocks : []
    onChange()
  },
  exportHtml: () => {
    const blocksArray = Array.isArray(blocks.value) ? blocks.value : []
    const mjml = blocksToMJML(blocksArray, emailSettings.value)
    return {
      html: mjml2html(mjml).html,
      blocks: blocksArray,
      mjml: mjml,
      emailSettings: emailSettings.value
    }
  },
  reinitializeSortables
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
