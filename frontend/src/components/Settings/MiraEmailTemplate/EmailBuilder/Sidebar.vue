<template>
  <div class="sidebar-container w-64 border-r bg-gray-50 overflow-y-auto">
    <div class="sidebar-content p-3">
      <!-- Content Section -->
      <div class="mb-4">
        <div 
          class="flex items-center gap-2 cursor-pointer py-2 mb-2"
          @click="contentExpanded = !contentExpanded"
        >
          <FeatherIcon 
            :name="contentExpanded ? 'chevron-down' : 'chevron-right'" 
            class="w-3 h-3 text-gray-500" 
          />
          <span class="text-xs font-semibold text-gray-700 uppercase">Content</span>
        </div>
        
        <div v-show="contentExpanded" ref="contentList" class="grid grid-cols-3 gap-2">
          <div
            v-for="block in contentBlocks"
            :key="block.type"
            :data-type="block.type"
            class="block-item flex flex-col items-center justify-center p-3 border border-gray-200 rounded cursor-move bg-white hover:border-blue-400 hover:shadow-sm transition-all"
          >
            <FeatherIcon :name="block.icon" class="w-5 h-5 text-gray-600 mb-1" />
            <div class="text-xs text-center text-gray-700">{{ block.name }}</div>
          </div>
        </div>
      </div>

      <!-- Layout Section -->
      <div class="mb-4">
        <div 
          class="flex items-center gap-2 cursor-pointer py-2 mb-2"
          @click="layoutExpanded = !layoutExpanded"
        >
          <FeatherIcon 
            :name="layoutExpanded ? 'chevron-down' : 'chevron-right'" 
            class="w-3 h-3 text-gray-500" 
          />
          <span class="text-xs font-semibold text-gray-700 uppercase">Layout</span>
        </div>
        
        <div v-show="layoutExpanded" class="space-y-3">
          <!-- 2 Columns -->
          <div>
            <div class="text-xs text-gray-500 mb-1">2 columns</div>
            <div ref="layout2Col" class="space-y-1">
              <div :data-type="'col-2-50-50'" class="layout-item border border-gray-200 rounded p-2 cursor-move bg-white hover:border-blue-400 hover:shadow-sm transition-all">
                <div class="grid grid-cols-2 gap-1">
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">50%</div>
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">50%</div>
                </div>
              </div>
              <div :data-type="'col-2-33-67'" class="layout-item border border-gray-200 rounded p-2 cursor-move bg-white hover:border-blue-400 hover:shadow-sm transition-all">
                <div class="grid grid-cols-3 gap-1">
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">33%</div>
                  <div class="col-span-2 text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">67%</div>
                </div>
              </div>
              <div :data-type="'col-2-67-33'" class="layout-item border border-gray-200 rounded p-2 cursor-move bg-white hover:border-blue-400 hover:shadow-sm transition-all">
                <div class="grid grid-cols-3 gap-1">
                  <div class="col-span-2 text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">67%</div>
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">33%</div>
                </div>
              </div>
            </div>
          </div>

          <!-- 3 Columns -->
          <div>
            <div class="text-xs text-gray-500 mb-1">3 columns</div>
            <div ref="layout3Col">
              <div :data-type="'col-3-33-33-33'" class="layout-item border border-gray-200 rounded p-2 cursor-move bg-white hover:border-blue-400 hover:shadow-sm transition-all">
                <div class="grid grid-cols-3 gap-1">
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">33.33%</div>
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">33.33%</div>
                  <div class="text-center text-xs text-gray-600 py-1 border border-dashed border-gray-300 rounded">33.33%</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const contentExpanded = ref(true)
const layoutExpanded = ref(true)

const contentBlocks = [
  { type: 'text', name: 'Text', icon: 'type' },
  { type: 'image', name: 'Image', icon: 'image' },
  { type: 'button', name: 'Button', icon: 'square' },
  { type: 'divider', name: 'Divider', icon: 'minus' },
  { type: 'spacer', name: 'Spacer', icon: 'move-vertical' },
]

// Expose refs for SortableJS
const contentList = ref(null)
const layout2Col = ref(null)
const layout3Col = ref(null)

defineExpose({
  contentList,
  layout2Col,
  layout3Col
})
</script>

<style scoped>
.sidebar-container {
  height: 100%;
  max-height: 100%;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: auto;
}

/* Custom scrollbar */
.sidebar-container::-webkit-scrollbar {
  width: 6px;
}

.sidebar-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.sidebar-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.sidebar-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.block-item,
.layout-item {
  user-select: none;
  min-height: 60px;
}

.block-item:hover,
.layout-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
