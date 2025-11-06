<template>
  <div class="flow-graph-v2">
    <VueFlow
      v-model:nodes="nodes"
      v-model:edges="edges"
      :default-viewport="{ zoom: 0.8 }"
      :min-zoom="0.2"
      :max-zoom="4"
      fit-view-on-init
      @node-click="handleNodeClick"
    >
      <!-- Background pattern -->
      <Background pattern-color="#e2e8f0" :gap="16" />

      <!-- Controls (zoom, fit view, etc.) -->
      <Controls />

      <!-- Minimap -->
      <MiniMap />

      <!-- Custom Node Templates -->
      <template #node-trigger="{ data }">
        <div class="custom-node trigger-node">
          <div class="node-header">
            <div class="node-icon trigger-icon">
              <FeatherIcon name="zap" class="w-4 h-4" />
            </div>
            <div class="node-content">
              <div class="node-title">{{ data.title }}</div>
              <div class="node-subtitle">{{ data.subtitle }}</div>
            </div>
          </div>
        </div>
      </template>

      <template #node-action="{ data }">
        <div class="custom-node action-node" :class="`action-${data.actionType?.toLowerCase()}`">
          <div class="node-header">
            <div class="node-icon action-icon">
              <FeatherIcon :name="getActionIcon(data.actionType)" class="w-4 h-4" />
            </div>
            <div class="node-content">
              <div class="node-title">{{ data.title }}</div>
              <div class="node-subtitle">{{ data.subtitle }}</div>
            </div>
          </div>
        </div>
      </template>
    </VueFlow>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { VueFlow, Position, useVueFlow } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { Controls } from '@vue-flow/controls'
import { MiniMap } from '@vue-flow/minimap'
import { FeatherIcon } from 'frappe-ui'
import { useLayout } from './useLayout'

const props = defineProps({
  flowData: {
    type: Object,
    required: true,
    default: () => ({ triggers: [], actions: [] })
  },
  selectedItem: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['node-click', 'node-select'])

const { layout } = useLayout()
const { fitView } = useVueFlow()

// Build raw nodes (without positions - will be calculated by Dagre)
const rawNodes = computed(() => {
  const result = []
  const triggers = props.flowData.triggers || []
  const actions = props.flowData.actions || []

  // ✅ Filter only active/enabled actions (not disabled)
  const activeActions = actions.filter(a => {
    // Check if action is disabled/inactive
    if (a.disabled === true || a.status === 'INACTIVE' || a.is_active === false) {
      return false
    }
    return true
  })

  // ✅ Build action hierarchy (support multi-level nesting)
  const parentActions = activeActions.filter(a => !a.parent_action_id)
  
  // Get all descendants of an action (recursive)
  const getDescendants = (parentId, level = 1) => {
    const directChildren = activeActions.filter(a => a.parent_action_id === parentId)
    let allDescendants = []
    
    directChildren.forEach(child => {
      allDescendants.push({ action: child, level })
      // Recursively get children of this child
      const grandChildren = getDescendants(child.name, level + 1)
      allDescendants = allDescendants.concat(grandChildren)
    })
    
    return allDescendants
  }

  // Level 1: Triggers
  triggers.forEach((trigger, index) => {
    result.push({
      id: `trigger-${index}`,
      type: 'trigger',
      position: { x: 0, y: 0 },  // ✅ Will be calculated by Dagre
      width: 280,
      height: 70,
      data: {
        title: trigger._ui_name || trigger.trigger_type || 'Trigger',
        subtitle: trigger._ui_description || getTriggerTypeLabel(trigger.trigger_type),
        index: index,
        itemType: 'trigger'
      },
      // sourcePosition & targetPosition will be set by Dagre
    })
  })

  // Level 2: Parent Actions
  parentActions.forEach((action, pIndex) => {
    const realIndex = activeActions.indexOf(action)
    result.push({
      id: `action-${realIndex}`,
      type: 'action',
      position: { x: 0, y: 0 },  // ✅ Will be calculated by Dagre
      width: 280,
      height: 70,
      data: {
        title: action._ui_name || getActionTypeLabel(action.action_type),
        subtitle: action._ui_description || getActionDescription(action),
        actionType: action.action_type,
        index: realIndex,
        itemType: 'action'
      },
      // sourcePosition & targetPosition will be set by Dagre
    })
  })

  // Level 3+: All child actions (flatten hierarchy for Dagre)
  const allChildren = activeActions.filter(a => a.parent_action_id)
  
  allChildren.forEach((child) => {
    const realIndex = activeActions.indexOf(child)
    result.push({
      id: `action-${realIndex}`,
      type: 'action',
      position: { x: 0, y: 0 },  // ✅ Will be calculated by Dagre
      width: 280,
      height: 70,
      data: {
        title: child._ui_name || getActionTypeLabel(child.action_type),
        subtitle: child._ui_description || getActionDescription(child),
        actionType: child.action_type,
        index: realIndex,
        itemType: 'action'
      },
      // sourcePosition & targetPosition will be set by Dagre
    })
  })

  return result
})

// ✅ Apply auto-layout to nodes
const nodes = computed(() => {
  if (rawNodes.value.length === 0 || edges.value.length === 0) {
    return rawNodes.value
  }
  
  // Apply Dagre layout
  return layout(rawNodes.value, edges.value, 'TB')  // ✅ TB = Top to Bottom (DỌC)
})

// Convert connections to Vue Flow edges
const edges = computed(() => {
  const result = []
  const triggers = props.flowData.triggers || []
  const actions = props.flowData.actions || []
  
  // ✅ Filter only active actions (same as nodes)
  const activeActions = actions.filter(a => {
    if (a.disabled === true || a.status === 'INACTIVE' || a.is_active === false) {
      return false
    }
    return true
  })
  
  const parentActions = activeActions.filter(a => !a.parent_action_id)
  const childActions = activeActions.filter(a => a.parent_action_id)

  // Trigger -> Parent Actions
  triggers.forEach((trigger, triggerIndex) => {
    parentActions.forEach((action) => {
      const actionIndex = activeActions.indexOf(action)
      result.push({
        id: `e-t${triggerIndex}-a${actionIndex}`,
        source: `trigger-${triggerIndex}`,
        target: `action-${actionIndex}`,
        type: 'default',  // ✅ Bezier curve (tròn)
        animated: false,
        markerEnd: {
          type: 'arrowclosed',
          color: '#94a3b8',
        },
        style: { stroke: '#94a3b8', strokeWidth: 2 }
      })
    })
  })

  // ✅ All Parent -> Child connections (support multi-level)
  childActions.forEach((child) => {
    const parentIndex = activeActions.findIndex(a => a.name === child.parent_action_id)
    const childIndex = activeActions.indexOf(child)
    
    if (parentIndex !== -1) {
      // ✅ Get trigger event from parent's additional_actions
      const parent = activeActions[parentIndex]
      let triggerLabel = ''
      
      if (parent.action_parameters) {
        try {
          const params = JSON.parse(parent.action_parameters)
          const additionalActions = params.additional_actions || {}
          
          // Find which trigger event this child belongs to
          for (const [triggerKey, actionConfig] of Object.entries(additionalActions)) {
            if (actionConfig.action_id === child.name) {
              triggerLabel = getTriggerEventLabel(triggerKey)
              break
            }
          }
        } catch (e) {
          console.error('Error parsing action_parameters:', e)
        }
      }
      
      result.push({
        id: `e-a${parentIndex}-a${childIndex}`,
        source: `action-${parentIndex}`,
        target: `action-${childIndex}`,
        type: 'default',  // ✅ Bezier curve (tròn)
        animated: true,
        label: triggerLabel,  // ✅ Show trigger event on edge
        labelStyle: { fill: '#3b82f6', fontWeight: 600, fontSize: 11 },
        labelBgStyle: { fill: '#eff6ff', fillOpacity: 1 },
        labelBgPadding: [6, 3],
        labelBgBorderRadius: 3,
        labelShowBg: true,
        labelPosition: 0.1,  // ✅ Position label near source
        markerEnd: {
          type: 'arrowclosed',
          color: '#3b82f6',
        },
        style: { stroke: '#3b82f6', strokeWidth: 2 }
      })
    }
  })

  return result
})

// Event handlers
const handleNodeClick = (event) => {
  const node = event.node
  if (node.data) {
    emit('node-select', {
      type: node.data.itemType,
      index: node.data.index
    })
  }
}

// Helper functions
const getTriggerTypeLabel = (type) => {
  const labels = {
    'ON_CREATE': 'When Created',
    'ON_UPDATE': 'When Updated',
    'ON_TAG_ADDED': 'When Tag Added',
  }
  return labels[type] || type
}

const getActionTypeLabel = (type) => {
  const labels = {
    'EMAIL': 'Send Email',
    'SMS': 'Send SMS',
    'ZALO': 'Send Zalo',
    'ADD_TAG': 'Add Tag',
    'REMOVE_TAG': 'Remove Tag',
  }
  return labels[type] || type
}

const getActionDescription = (action) => {
  if (action.action_type === 'EMAIL') {
    try {
      const params = JSON.parse(action.action_parameters || '{}')
      return params.email_content?.email_subject || 'Email Action'
    } catch (e) {
      return 'Email Action'
    }
  }
  return action.action_type
}

const getActionIcon = (type) => {
  const iconMap = {
    'EMAIL': 'mail',
    'SMS': 'message-square',
    'ZALO': 'message-circle',
    'ADD_TAG': 'tag',
    'REMOVE_TAG': 'x',
    'SMART_DELAY': 'clock',
    'START_FLOW': 'play',
    'UNSUBSCRIBE': 'user-x',
  }
  return iconMap[type] || 'circle'
}

const getTriggerEventLabel = (triggerKey) => {
  const labels = {
    'email_open': '📧 Email Opened',
    'link_click': '🔗 Link Clicked',
    'send_success': '✅ Send Success',
    'send_failed': '❌ Send Failed',
    'email_reply': '↩️ Email Reply',
    'email_bounce': '⚠️ Email Bounce',
    'sms_delivered': '✅ SMS Delivered',
    'sms_failed': '❌ SMS Failed',
  }
  return labels[triggerKey] || triggerKey
}
</script>

<style scoped>
.flow-graph-v2 {
  width: 100%;
  height: 100%;
  background: #f8fafc;
}

/* Custom Node Styles */
.custom-node {
  padding: 12px 16px;
  border-radius: 8px;
  border: 2px solid;
  background: white;
  min-width: 280px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.custom-node:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.node-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.node-icon {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.trigger-icon {
  background: #fef3c7;
  color: #f59e0b;
}

.action-icon {
  background: #dbeafe;
  color: #3b82f6;
}

.node-content {
  flex: 1;
  min-width: 0;
}

.node-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.node-subtitle {
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 2px;
}

/* Trigger Node */
.trigger-node {
  border-color: #fbbf24;
  background: #fffbeb;
}

/* Action Node Variants */
.action-node {
  border-color: #e2e8f0;
}

.action-email {
  border-color: #3b82f6;
  background: #eff6ff;
}

.action-email .action-icon {
  background: #dbeafe;
  color: #3b82f6;
}

.action-sms {
  border-color: #6366f1;
  background: #eef2ff;
}

.action-sms .action-icon {
  background: #e0e7ff;
  color: #6366f1;
}

.action-zalo {
  border-color: #8b5cf6;
  background: #f5f3ff;
}

.action-zalo .action-icon {
  background: #ddd6fe;
  color: #8b5cf6;
}

.action-add_tag {
  border-color: #10b981;
  background: #f0fdf4;
}

.action-add_tag .action-icon {
  background: #d1fae5;
  color: #10b981;
}

.action-remove_tag {
  border-color: #ef4444;
  background: #fef2f2;
}

.action-remove_tag .action-icon {
  background: #fee2e2;
  color: #ef4444;
}
</style>
