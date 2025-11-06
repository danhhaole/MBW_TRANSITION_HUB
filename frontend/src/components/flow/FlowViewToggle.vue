<template>
  <div class="flow-view-toggle">
    <!-- View Toggle Switch -->
    <div class="view-toggle-header">
      <div class="toggle-container">
        <span class="toggle-label" :class="{ active: !isGraphView }">
          <FeatherIcon name="list" class="w-4 h-4" />
          {{ __('List View') }}
        </span>
        <Switch
          v-model="isGraphView"
          class="toggle-switch"
        />
        <span class="toggle-label" :class="{ active: isGraphView }">
          <FeatherIcon name="git-branch" class="w-4 h-4" />
          {{ __('Graph View') }}
        </span>
      </div>
    </div>

    <!-- View Content -->
    <div class="view-content">
      <!-- Graph View -->
      <div v-if="isGraphView" class="graph-view-container">
        <FlowGraphView
          :flow-data="flowData"
          :selected-item="selectedItem"
          @node-click="handleNodeClick"
          @node-select="handleNodeSelect"
        />
      </div>

      <!-- List View (slot for existing content) -->
      <div v-else class="list-view-container">
        <slot name="list-view"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Switch, FeatherIcon } from 'frappe-ui'
import FlowGraphView from './FlowGraphView.vue'

const props = defineProps({
  flowData: {
    type: Object,
    required: true,
    default: () => ({ triggers: [], actions: [] })
  },
  selectedItem: {
    type: Object,
    default: null
  },
  defaultView: {
    type: String,
    default: 'list', // 'list' or 'graph'
    validator: (value) => ['list', 'graph'].includes(value)
  }
})

const emit = defineEmits(['node-click', 'node-select', 'view-change'])

// View state
const isGraphView = ref(props.defaultView === 'graph')

// Watch view changes
watch(isGraphView, (newValue) => {
  emit('view-change', newValue ? 'graph' : 'list')
})

// Event handlers
const handleNodeClick = (node) => {
  emit('node-click', node)
}

const handleNodeSelect = (item) => {
  emit('node-select', item)
}
</script>

<style scoped>
.flow-view-toggle {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.view-toggle-header {
  padding: 16px 20px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-container {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8fafc;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  transition: color 0.2s ease;
  cursor: pointer;
  user-select: none;
}

.toggle-label.active {
  color: #3b82f6;
}

.toggle-switch {
  margin: 0 4px;
}

.view-content {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.graph-view-container,
.list-view-container {
  width: 100%;
  height: 100%;
}

.list-view-container {
  overflow-y: auto;
}
</style>
