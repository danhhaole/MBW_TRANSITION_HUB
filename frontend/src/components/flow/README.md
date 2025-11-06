# Flow Graph View Components

Các component để hiển thị flow dạng graph với quan hệ giữa triggers và actions.

## Components

### 1. FlowGraphView.vue
Component chính để hiển thị flow dạng graph (flowchart).

**Features:**
- ✅ Hiển thị triggers và actions dạng nodes
- ✅ Hiển thị quan hệ giữa triggers → actions
- ✅ Hiển thị quan hệ parent-child giữa actions
- ✅ Pan (kéo canvas)
- ✅ Zoom (scroll wheel hoặc buttons)
- ✅ Click để select node
- ✅ Màu sắc khác nhau cho từng loại action

**Props:**
```javascript
{
  flowData: {
    type: Object,
    required: true,
    default: () => ({ triggers: [], actions: [] })
  },
  selectedItem: {
    type: Object,
    default: null
  }
}
```

**Events:**
```javascript
@node-click="handleNodeClick"  // Click vào node
@node-select="handleNodeSelect" // Select node (emit { type, index })
```

**Usage:**
```vue
<FlowGraphView
  :flow-data="flowData"
  :selected-item="selectedItem"
  @node-select="handleNodeSelect"
/>
```

---

### 2. FlowViewToggle.vue
Component wrapper với switch để toggle giữa List View và Graph View.

**Features:**
- ✅ Switch toggle (Frappe UI)
- ✅ List view (slot)
- ✅ Graph view (FlowGraphView)
- ✅ Emit view change event

**Props:**
```javascript
{
  flowData: Object,
  selectedItem: Object,
  defaultView: String // 'list' or 'graph'
}
```

**Events:**
```javascript
@node-click="handleNodeClick"
@node-select="handleNodeSelect"
@view-change="handleViewChange" // 'list' or 'graph'
```

**Usage:**
```vue
<FlowViewToggle
  :flow-data="flowData"
  :selected-item="selectedItem"
  default-view="graph"
  @node-select="handleNodeSelect"
  @view-change="handleViewChange"
>
  <template #list-view>
    <!-- Your existing list view content -->
    <div>List view content here</div>
  </template>
</FlowViewToggle>
```

---

### 3. FlowGraphDemo.vue
Component demo để test và xem cách sử dụng.

**Usage:**
```javascript
// In router or page
import FlowGraphDemo from '@/components/flow/FlowGraphDemo.vue'
```

---

## Integration vào FlowEditor

### Bước 1: Import components
```vue
<script setup>
import FlowViewToggle from '@/components/flow/FlowViewToggle.vue'
</script>
```

### Bước 2: Wrap existing content
```vue
<template>
  <div class="flow-editor">
    <FlowViewToggle
      :flow-data="flowData"
      :selected-item="selectedItem"
      default-view="list"
      @node-select="handleNodeSelect"
    >
      <template #list-view>
        <!-- Existing FlowEditor content -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Left: Triggers & Actions List -->
          <!-- Right: Configuration Panel -->
        </div>
      </template>
    </FlowViewToggle>
  </div>
</template>
```

### Bước 3: Handle node selection
```javascript
const handleNodeSelect = (item) => {
  // item = { type: 'trigger' | 'action', index: number }
  selectedItem.value = item
}
```

---

## Data Format

### Flow Data Structure
```javascript
{
  triggers: [
    {
      trigger_type: 'ON_CREATE',
      _ui_name: 'Trigger Name',
      _ui_description: 'Description',
      target_type: 'Talent',
      status: 'ACTIVE'
    }
  ],
  actions: [
    {
      action_type: 'EMAIL',
      _ui_name: 'Action Name',
      _ui_description: 'Description',
      action_parameters: '{"email_subject": "..."}',
      parent_action_id: null, // or parent action name
      order: 0
    }
  ]
}
```

---

## Customization

### Node Colors
Edit trong `FlowGraphView.vue`:

```css
.action-email {
  fill: #dbeafe;
  stroke: #3b82f6;
}

.action-sms {
  fill: #e0e7ff;
  stroke: #6366f1;
}

/* Add more action types */
```

### Node Icons
Edit function `getNodeIcon()`:

```javascript
const getNodeIcon = (node) => {
  const iconMap = {
    'EMAIL': 'mail',
    'SMS': 'message-square',
    // Add more mappings
  }
  return iconMap[node.actionType] || 'circle'
}
```

### Layout
Adjust spacing constants:

```javascript
const NODE_WIDTH = 280
const NODE_HEIGHT = 60
const VERTICAL_SPACING = 120
const HORIZONTAL_SPACING = 350
```

---

## TODO / Future Enhancements

- [ ] Auto-layout algorithm (dagre, elk, etc.)
- [ ] Minimap
- [ ] Export to image
- [ ] Undo/Redo
- [ ] Drag & drop nodes
- [ ] Add/delete nodes from graph
- [ ] Edge labels
- [ ] Conditional branches visualization
- [ ] Animation khi thêm/xóa nodes

---

## Dependencies

- Vue 3
- Frappe UI (Switch, FeatherIcon)
- SVG (native)

No external graph libraries required! 🎉
