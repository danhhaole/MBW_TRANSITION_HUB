<template>
  <div class="flow-graph-view">
    <!-- Canvas container -->
    <div ref="canvasContainer" class="canvas-container">
      <svg
        ref="svgCanvas"
        class="flow-canvas"
        :width="canvasWidth"
        :height="canvasHeight"
        @mousedown="handleCanvasMouseDown"
        @mousemove="handleCanvasMouseMove"
        @mouseup="handleCanvasMouseUp"
        @wheel="handleWheel"
      >
        <!-- Define arrow markers -->
        <defs>
          <marker
            id="arrowhead"
            markerWidth="10"
            markerHeight="10"
            refX="9"
            refY="3"
            orient="auto"
          >
            <polygon points="0 0, 10 3, 0 6" fill="#94a3b8" />
          </marker>
        </defs>

        <!-- Transform group for pan and zoom -->
        <g :transform="`translate(${panX}, ${panY}) scale(${zoom})`">
          <!-- Connections (edges) -->
          <g class="connections">
            <path
              v-for="edge in edges"
              :key="edge.id"
              :d="edge.path"
              class="edge"
              stroke="#94a3b8"
              stroke-width="2"
              fill="none"
              marker-end="url(#arrowhead)"
            />
          </g>

          <!-- Nodes (triggers and actions) -->
          <g class="nodes">
            <g
              v-for="node in nodes"
              :key="node.id"
              :transform="`translate(${node.x}, ${node.y})`"
              class="node"
              :class="{ selected: selectedNodeId === node.id }"
              @click="handleNodeClick(node)"
            >
              <!-- Node background -->
              <rect
                :width="node.width"
                :height="node.height"
                :rx="8"
                :class="[
                  'node-bg',
                  node.type === 'trigger' ? 'trigger-node' : 'action-node',
                  node.actionType ? `action-${node.actionType.toLowerCase()}` : ''
                ]"
              />

              <!-- Icon -->
              <foreignObject
                :x="12"
                :y="12"
                width="32"
                height="32"
              >
                <div class="node-icon" :class="`icon-${node.type}`">
                  <FeatherIcon :name="getNodeIcon(node)" class="w-5 h-5" />
                </div>
              </foreignObject>

              <!-- Text content -->
              <foreignObject
                :x="52"
                :y="8"
                :width="node.width - 64"
                :height="node.height - 16"
              >
                <div class="node-content">
                  <div class="node-title">{{ node.title }}</div>
                  <div class="node-subtitle">{{ node.subtitle }}</div>
                </div>
              </foreignObject>
            </g>
          </g>
        </g>
      </svg>
    </div>

    <!-- Controls -->
    <div class="graph-controls">
      <button @click="zoomIn" class="control-btn" title="Zoom In">
        <FeatherIcon name="zoom-in" class="w-4 h-4" />
      </button>
      <button @click="zoomOut" class="control-btn" title="Zoom Out">
        <FeatherIcon name="zoom-out" class="w-4 h-4" />
      </button>
      <button @click="resetView" class="control-btn" title="Reset View">
        <FeatherIcon name="maximize" class="w-4 h-4" />
      </button>
      <div class="zoom-level">{{ Math.round(zoom * 100) }}%</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { FeatherIcon } from 'frappe-ui'

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

// Canvas state
const canvasContainer = ref(null)
const svgCanvas = ref(null)
const canvasWidth = ref(2400)  // Increased canvas width
const canvasHeight = ref(1600) // Increased canvas height

// Pan and zoom
const panX = ref(0)
const panY = ref(0)
const zoom = ref(1)
const isPanning = ref(false)
const lastMouseX = ref(0)
const lastMouseY = ref(0)

// Node dimensions
const NODE_WIDTH = 280
const NODE_HEIGHT = 70
const VERTICAL_SPACING = 150  // Increased spacing between nodes vertically
const HORIZONTAL_SPACING = 200
const LEVEL_SPACING = 400     // Increased spacing between levels (Trigger → Action → Child)

// Selected node
const selectedNodeId = computed(() => {
  if (!props.selectedItem) return null
  return `${props.selectedItem.type}-${props.selectedItem.index}`
})

// Build nodes from flow data with proper hierarchy layout
const nodes = computed(() => {
  const result = []
  const triggers = props.flowData.triggers || []
  const actions = props.flowData.actions || []

  // Separate parent and child actions
  const parentActions = actions.filter(a => !a.parent_action_id)
  const childActions = actions.filter(a => a.parent_action_id)

  // Level 1: Triggers (leftmost)
  const triggerStartY = 150  // More top padding
  const triggerStartX = 100  // More left padding
  triggers.forEach((trigger, index) => {
    result.push({
      id: `trigger-${index}`,
      type: 'trigger',
      title: trigger._ui_name || trigger.trigger_type || 'Trigger',
      subtitle: trigger._ui_description || getTriggerTypeLabel(trigger.trigger_type),
      x: triggerStartX,
      y: triggerStartY + (index * VERTICAL_SPACING),
      width: NODE_WIDTH,
      height: NODE_HEIGHT,
      data: trigger,
      index: index,
      level: 1
    })
  })

  // Level 2: Parent Actions (middle)
  const parentActionStartY = 150  // Same as trigger start
  parentActions.forEach((action, pIndex) => {
    const realIndex = actions.indexOf(action)
    result.push({
      id: `action-${realIndex}`,
      type: 'action',
      actionType: action.action_type,
      title: action._ui_name || getActionTypeLabel(action.action_type),
      subtitle: action._ui_description || getActionDescription(action),
      x: triggerStartX + LEVEL_SPACING,
      y: parentActionStartY + (pIndex * VERTICAL_SPACING),
      width: NODE_WIDTH,
      height: NODE_HEIGHT,
      data: action,
      index: realIndex,
      parentActionId: null,
      level: 2
    })
  })

  // Level 3: Child Actions (rightmost) - grouped by parent
  const childActionStartY = 150
  let childYOffset = 0
  
  parentActions.forEach((parentAction, pIndex) => {
    const parentRealIndex = actions.indexOf(parentAction)
    const children = childActions.filter(c => c.parent_action_id === parentAction.name)
    
    if (children.length > 0) {
      // Position children relative to their parent
      const parentNode = result.find(n => n.id === `action-${parentRealIndex}`)
      const parentY = parentNode ? parentNode.y : childActionStartY
      
      children.forEach((child, cIndex) => {
        const realIndex = actions.indexOf(child)
        result.push({
          id: `action-${realIndex}`,
          type: 'action',
          actionType: child.action_type,
          title: child._ui_name || getActionTypeLabel(child.action_type),
          subtitle: child._ui_description || getActionDescription(child),
          x: triggerStartX + (LEVEL_SPACING * 2),
          y: parentY + (cIndex * VERTICAL_SPACING),
          width: NODE_WIDTH,
          height: NODE_HEIGHT,
          data: child,
          index: realIndex,
          parentActionId: child.parent_action_id,
          level: 3
        })
      })
    }
  })

  return result
})

// Build edges (connections)
const edges = computed(() => {
  const result = []
  const triggers = props.flowData.triggers || []
  const actions = props.flowData.actions || []

  // Connect triggers to actions
  triggers.forEach((trigger, triggerIndex) => {
    // Find parent actions (actions without parent_action_id)
    const parentActions = actions.filter(a => !a.parent_action_id)
    
    parentActions.forEach((action, actionIndex) => {
      const realActionIndex = actions.indexOf(action)
      const triggerNode = nodes.value.find(n => n.id === `trigger-${triggerIndex}`)
      const actionNode = nodes.value.find(n => n.id === `action-${realActionIndex}`)

      if (triggerNode && actionNode) {
        result.push({
          id: `edge-t${triggerIndex}-a${realActionIndex}`,
          from: triggerNode.id,
          to: actionNode.id,
          path: createEdgePath(triggerNode, actionNode)
        })
      }
    })
  })

  // Connect parent actions to child actions
  actions.forEach((action, index) => {
    if (action.parent_action_id) {
      const parentIndex = actions.findIndex(a => a.name === action.parent_action_id)
      if (parentIndex !== -1) {
        const parentNode = nodes.value.find(n => n.id === `action-${parentIndex}`)
        const childNode = nodes.value.find(n => n.id === `action-${index}`)

        if (parentNode && childNode) {
          result.push({
            id: `edge-a${parentIndex}-a${index}`,
            from: parentNode.id,
            to: childNode.id,
            path: createEdgePath(parentNode, childNode, true)
          })
        }
      }
    }
  })

  return result
})

// Create SVG path for edge with smooth curves
const createEdgePath = (fromNode, toNode, isCurved = false) => {
  const x1 = fromNode.x + fromNode.width
  const y1 = fromNode.y + fromNode.height / 2
  const x2 = toNode.x
  const y2 = toNode.y + toNode.height / 2

  // Always use smooth bezier curves for better visual
  const dx = x2 - x1
  const controlPointOffset = Math.abs(dx) * 0.5
  
  // Horizontal control points for smooth S-curve
  const cx1 = x1 + controlPointOffset
  const cy1 = y1
  const cx2 = x2 - controlPointOffset
  const cy2 = y2

  return `M ${x1} ${y1} C ${cx1} ${cy1}, ${cx2} ${cy2}, ${x2} ${y2}`
}

// Get icon for node
const getNodeIcon = (node) => {
  if (node.type === 'trigger') {
    return 'zap'
  }
  
  const iconMap = {
    'EMAIL': 'mail',
    'SMS': 'message-square',
    'ZALO': 'message-circle',
    'ADD_TAG': 'tag',
    'REMOVE_TAG': 'x',
    'SMART_DELAY': 'clock',
    'START_FLOW': 'play',
    'SUBSCRIBE_TO_SEQUENCE': 'list',
    'UN_SUBSCRIBE_TO_SEQUENCE': 'x-circle',
    'ADD_CUSTOM_FIELD': 'plus-square',
  }
  
  return iconMap[node.actionType] || 'circle'
}

// Helper functions
const getTriggerTypeLabel = (type) => {
  const labels = {
    'ON_CREATE': 'When Created',
    'ON_UPDATE': 'When Updated',
    'ON_TAG_ADDED': 'When Tag Added',
    'ON_STATUS_CHANGED': 'When Status Changed',
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
    'SMART_DELAY': 'Smart Delay',
    'START_FLOW': 'Start Flow',
    'SUBSCRIBE_TO_SEQUENCE': 'Subscribe to Sequence',
    'UN_SUBSCRIBE_TO_SEQUENCE': 'Unsubscribe',
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

// Event handlers
const handleNodeClick = (node) => {
  emit('node-click', node)
  emit('node-select', {
    type: node.type,
    index: node.index
  })
}

const handleCanvasMouseDown = (e) => {
  if (e.target === svgCanvas.value || e.target.tagName === 'g') {
    isPanning.value = true
    lastMouseX.value = e.clientX
    lastMouseY.value = e.clientY
    e.preventDefault()
  }
}

const handleCanvasMouseMove = (e) => {
  if (isPanning.value) {
    const dx = e.clientX - lastMouseX.value
    const dy = e.clientY - lastMouseY.value
    panX.value += dx
    panY.value += dy
    lastMouseX.value = e.clientX
    lastMouseY.value = e.clientY
  }
}

const handleCanvasMouseUp = () => {
  isPanning.value = false
}

const handleWheel = (e) => {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  const newZoom = Math.max(0.1, Math.min(2, zoom.value + delta))
  zoom.value = newZoom
}

// Controls
const zoomIn = () => {
  zoom.value = Math.min(2, zoom.value + 0.1)
}

const zoomOut = () => {
  zoom.value = Math.max(0.1, zoom.value - 0.1)
}

const resetView = () => {
  zoom.value = 1
  panX.value = 0
  panY.value = 0
}

// Resize canvas
const updateCanvasSize = () => {
  if (canvasContainer.value) {
    canvasWidth.value = canvasContainer.value.clientWidth
    canvasHeight.value = canvasContainer.value.clientHeight
  }
}

onMounted(() => {
  updateCanvasSize()
  window.addEventListener('resize', updateCanvasSize)
})
</script>

<style scoped>
.flow-graph-view {
  position: relative;
  width: 100%;
  height: 100%;
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
}

.canvas-container {
  width: 100%;
  height: 100%;
  cursor: grab;
}

.canvas-container:active {
  cursor: grabbing;
}

.flow-canvas {
  width: 100%;
  height: 100%;
}

/* Nodes */
.node {
  cursor: pointer;
  transition: all 0.2s ease;
}

.node:hover .node-bg {
  filter: brightness(0.95);
}

.node.selected .node-bg {
  stroke: #3b82f6;
  stroke-width: 3;
}

.node-bg {
  fill: white;
  stroke: #e2e8f0;
  stroke-width: 2;
  transition: all 0.2s ease;
}

.trigger-node {
  fill: #fef3c7;
  stroke: #fbbf24;
}

.action-node {
  fill: white;
}

.action-email {
  fill: #dbeafe;
  stroke: #3b82f6;
}

.action-sms {
  fill: #e0e7ff;
  stroke: #6366f1;
}

.action-zalo {
  fill: #ddd6fe;
  stroke: #8b5cf6;
}

.action-add_tag {
  fill: #d1fae5;
  stroke: #10b981;
}

.action-remove_tag {
  fill: #fee2e2;
  stroke: #ef4444;
}

.node-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.8);
}

.icon-trigger {
  color: #f59e0b;
}

.icon-action {
  color: #3b82f6;
}

.node-content {
  padding: 4px 0;
  overflow: hidden;
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

/* Edges */
.edge {
  transition: stroke 0.2s ease;
}

.edge:hover {
  stroke: #3b82f6;
  stroke-width: 3;
}

/* Controls */
.graph-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  gap: 8px;
  align-items: center;
  background: white;
  padding: 8px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.control-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.control-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.zoom-level {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
  min-width: 45px;
  text-align: center;
}
</style>
