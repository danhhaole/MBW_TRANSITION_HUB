<template>
  <div :style="{ padding: block.props.padding + 'px' }">
    <!-- 1 Column Layout -->
    <div v-if="block.type === 'col-1'" class="layout-column-container">
      <div class="layout-column border-2 border-dashed border-gray-300 rounded p-4 min-h-[100px]" :data-column="0">
        <div v-if="!block.children || !block.children[0] || block.children[0].length === 0" class="text-center text-gray-400 text-xs py-4">
          Drop content here (100%)
        </div>
        <div v-else>
          <div 
            v-for="child in block.children[0]" 
            :key="child.id" 
            class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all"
            @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: 0, child })"
          >
            <component :is="getChildComponent(child.type)" :block="child" />
          </div>
        </div>
      </div>
    </div>

    <!-- 2 Columns 50/50 -->
    <div v-else-if="block.type === 'col-2-50-50'" class="layout-column-container grid grid-cols-2 gap-4">
      <div v-for="colIdx in 2" :key="colIdx" class="layout-column border-2 border-dashed border-gray-300 rounded p-4 min-h-[100px]" :data-column="colIdx - 1">
        <div v-if="!block.children || !block.children[colIdx - 1] || block.children[colIdx - 1].length === 0" class="text-center text-gray-400 text-xs py-4">
          50%
        </div>
        <div v-else>
          <div 
            v-for="child in block.children[colIdx - 1]" 
            :key="child.id" 
            class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all"
            @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: colIdx - 1, child })"
          >
            <component :is="getChildComponent(child.type)" :block="child" />
          </div>
        </div>
      </div>
    </div>

    <!-- 2 Columns 33/67 -->
    <div v-else-if="block.type === 'col-2-33-67'" class="layout-column-container grid grid-cols-3 gap-4">
      <div class="layout-column border-2 border-dashed border-gray-300 rounded p-4 min-h-[100px]" :data-column="0">
        <div v-if="!block.children || !block.children[0] || block.children[0].length === 0" class="text-center text-gray-400 text-xs py-4">33%</div>
        <div v-else><div v-for="child in block.children[0]" :key="child.id" class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all" @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: 0, child })"><component :is="getChildComponent(child.type)" :block="child" /></div></div>
      </div>
      <div class="layout-column col-span-2 border-2 border-dashed border-gray-300 rounded p-4 min-h-[100px]" :data-column="1">
        <div v-if="!block.children || !block.children[1] || block.children[1].length === 0" class="text-center text-gray-400 text-xs py-4">67%</div>
        <div v-else><div v-for="child in block.children[1]" :key="child.id" class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all" @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: 1, child })"><component :is="getChildComponent(child.type)" :block="child" /></div></div>
      </div>
    </div>

    <!-- 2 Columns 67/33 -->
    <div v-else-if="block.type === 'col-2-67-33'" class="layout-column-container grid grid-cols-3 gap-4">
      <div class="layout-column col-span-2 border-2 border-dashed border-gray-300 rounded p-4 min-h-[100px]" :data-column="0">
        <div v-if="!block.children || !block.children[0] || block.children[0].length === 0" class="text-center text-gray-400 text-xs py-4">67%</div>
        <div v-else><div v-for="child in block.children[0]" :key="child.id" class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all" @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: 0, child })"><component :is="getChildComponent(child.type)" :block="child" /></div></div>
      </div>
      <div class="layout-column border-2 border-dashed border-gray-300 rounded p-4 min-h-[100px]" :data-column="1">
        <div v-if="!block.children || !block.children[1] || block.children[1].length === 0" class="text-center text-gray-400 text-xs py-4">33%</div>
        <div v-else><div v-for="child in block.children[1]" :key="child.id" class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all" @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: 1, child })"><component :is="getChildComponent(child.type)" :block="child" /></div></div>
      </div>
    </div>

    <!-- 3 Columns -->
    <div v-else-if="block.type === 'col-3-33-33-33'" class="layout-column-container grid grid-cols-3 gap-2">
      <div v-for="colIdx in 3" :key="colIdx" class="layout-column border-2 border-dashed border-gray-300 rounded p-3 min-h-[100px]" :data-column="colIdx - 1">
        <div v-if="!block.children || !block.children[colIdx - 1] || block.children[colIdx - 1].length === 0" class="text-center text-gray-400 text-xs py-4">
          33.33%
        </div>
        <div v-else>
          <div 
            v-for="child in block.children[colIdx - 1]" 
            :key="child.id" 
            class="nested-block mb-2 p-2 border border-transparent hover:border-blue-400 rounded cursor-pointer transition-all"
            @click.stop="$emit('select-nested', { blockId: block.id, columnIndex: colIdx - 1, child })"
          >
            <component :is="getChildComponent(child.type)" :block="child" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { blockComponents } from './index.js'

defineProps({
  block: {
    type: Object,
    required: true
  }
})

defineEmits(['select-nested'])

function getChildComponent(type) {
  return blockComponents[type] || blockComponents.text
}
</script>

<style scoped>
.layout-column {
  background: #fafafa;
}
.layout-column:hover {
  border-color: #3b82f6 !important;
  background: #eff6ff;
}
</style>
