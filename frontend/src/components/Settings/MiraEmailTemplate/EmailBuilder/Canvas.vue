<template>
  <div class="canvas-container flex-1 bg-gray-50 overflow-y-auto">
    <div class="p-6">
      <div 
        class="max-w-3xl mx-auto shadow-sm rounded-lg border min-h-[500px]"
        :style="{ backgroundColor: emailSettings?.backgroundColor || '#ffffff' }"
      >
        <div 
          ref="canvasContainer" 
          class="p-4 min-h-[400px]"
          :class="{ 'border-2 border-dashed border-gray-300 rounded': blocks.length === 0 && !isDraggingOver }"
          @dragenter="isDraggingOver = true"
          @dragleave="handleDragLeave"
          @drop="isDraggingOver = false"
        >
          <!-- Email Blocks -->
          <div
            v-for="(block, index) in blocks"
            :key="block.id"
            :data-id="block.id"
            class="email-block group relative border-2 border-transparent hover:border-blue-300 transition-all cursor-move mb-3 rounded bg-white"
            :class="{ 'border-blue-500 bg-blue-50': selectedIndex === index }"
            @click="$emit('select', index)"
          >
            <!-- Drag Handle -->
            <div class="absolute left-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-50 cursor-move">
              <FeatherIcon name="menu" class="w-4 h-4 text-gray-400" />
            </div>

            <!-- Block Content -->
            <div class="pl-8 pr-10">
              <component 
                :is="getBlockComponent(block.type)" 
                :block="block"
                @select-nested="$emit('select-nested', $event)"
              />
            </div>

            <!-- Action Buttons -->
            <div class="!absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <!-- Drag Handle -->
              <Button
                icon="move"
                variant="subtle"
                size="sm"
                class="cursor-move"
                title="Drag to reorder"
              />
              <!-- Duplicate Button -->
              <Button
                @click.stop="$emit('duplicate', index)"
                icon="copy"
                variant="subtle"
                size="sm"
                title="Duplicate"
              />
              <!-- Delete Button -->
              <Button
                @click.stop="$emit('delete', index)"
                icon="x"
                variant="solid"
                theme="red"
                size="sm"
                title="Delete"
              />
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="blocks.length === 0 && !isDraggingOver" class="text-center py-16 text-gray-400">
            <FeatherIcon name="mouse-pointer" class="w-16 h-16 mx-auto mb-4 text-gray-300" />
            <p class="text-sm">Drag blocks from the left sidebar here</p>
          </div>
          
          <!-- Dragging Over State -->
          <div v-if="blocks.length === 0 && isDraggingOver" class="text-center py-16 text-blue-400">
            <FeatherIcon name="download" class="w-16 h-16 mx-auto mb-4" />
            <p class="text-sm font-medium">Drop here to add block</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import { blockComponents } from './blocks'

defineProps({
  blocks: {
    type: Array,
    default: () => []
  },
  selectedIndex: {
    type: Number,
    default: null
  },
  emailSettings: {
    type: Object,
    default: () => ({})
  }
})

defineEmits(['select', 'delete', 'duplicate', 'select-nested'])

const canvasContainer = ref(null)
const isDraggingOver = ref(false)

// Handle drag leave - only set false when leaving canvas container
function handleDragLeave(e) {
  // Check if we're leaving the canvas container itself
  if (e.target === canvasContainer.value) {
    isDraggingOver.value = false
  }
}

function getBlockComponent(type) {
  return blockComponents[type] || blockComponents.text
}

defineExpose({
  canvasContainer
})
</script>

<style scoped>
.canvas-container {
  height: 100%;
  max-height: 100%;
}

.email-block {
  position: relative;
  transition: all 0.2s;
}
</style>
