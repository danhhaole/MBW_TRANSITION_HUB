<template>
  <div class="flow-graph-demo">
    <div class="demo-header">
      <h2 class="text-xl font-semibold">Flow Graph View Demo</h2>
      <p class="text-sm text-gray-600">Toggle between list and graph view</p>
    </div>

    <div class="demo-content">
      <FlowViewToggle
        :flow-data="demoFlowData"
        :selected-item="selectedItem"
        default-view="graph"
        @node-select="handleNodeSelect"
        @view-change="handleViewChange"
      >
        <template #list-view>
          <div class="list-view-demo">
            <div class="section">
              <h3 class="section-title">Triggers</h3>
              <div class="items-list">
                <div
                  v-for="(trigger, index) in demoFlowData.triggers"
                  :key="index"
                  class="list-item"
                  :class="{ selected: isSelected('trigger', index) }"
                  @click="selectItem('trigger', index)"
                >
                  <FeatherIcon name="zap" class="w-5 h-5 text-yellow-500" />
                  <div class="item-content">
                    <div class="item-title">{{ trigger._ui_name }}</div>
                    <div class="item-subtitle">{{ trigger._ui_description }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="section">
              <h3 class="section-title">Actions</h3>
              <div class="items-list">
                <div
                  v-for="(action, index) in demoFlowData.actions"
                  :key="index"
                  class="list-item"
                  :class="{ selected: isSelected('action', index) }"
                  @click="selectItem('action', index)"
                >
                  <FeatherIcon :name="getActionIcon(action)" class="w-5 h-5 text-blue-500" />
                  <div class="item-content">
                    <div class="item-title">{{ action._ui_name }}</div>
                    <div class="item-subtitle">{{ action._ui_description }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </FlowViewToggle>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon } from 'frappe-ui'
import FlowViewToggle from './FlowViewToggle.vue'

// Demo data
const demoFlowData = ref({
  triggers: [
    {
      trigger_type: 'ON_CREATE',
      _ui_name: 'Khi tạo mới',
      _ui_description: 'Lead từ Facebook Lead Ads',
      target_type: 'Talent',
      status: 'ACTIVE'
    },
    {
      trigger_type: 'ON_TAG_ADDED',
      _ui_name: 'Đăng ký mới (FB Ads)',
      _ui_description: 'Đăng ký mới từ FB Ads',
      target_type: 'Talent',
      status: 'ACTIVE'
    }
  ],
  actions: [
    {
      action_type: 'EMAIL',
      _ui_name: 'Hành động',
      _ui_description: 'Thêm Tag',
      action_parameters: JSON.stringify({
        email_content: {
          email_subject: 'Welcome Email',
          email_content: '<p>Welcome to our platform!</p>'
        }
      }),
      order: 0
    },
    {
      action_type: 'EMAIL',
      _ui_name: 'Hợp đồng',
      _ui_description: 'Hợp đồng',
      action_parameters: JSON.stringify({
        email_content: {
          email_subject: 'Contract',
          email_content: '<p>Your contract</p>'
        }
      }),
      order: 1
    },
    {
      action_type: 'ZALO',
      _ui_name: 'Zalo ZNS',
      _ui_description: 'Gửi tin Zalo ZNS',
      action_parameters: JSON.stringify({}),
      order: 2
    },
    {
      action_type: 'ADD_TAG',
      _ui_name: 'Add Tag',
      _ui_description: 'Email Opened Tag',
      action_parameters: JSON.stringify({
        selected_tags: ['tag1']
      }),
      parent_action_id: null,
      order: 3
    }
  ]
})

const selectedItem = ref(null)
const currentView = ref('graph')

const selectItem = (type, index) => {
  selectedItem.value = { type, index }
}

const isSelected = (type, index) => {
  return selectedItem.value?.type === type && selectedItem.value?.index === index
}

const handleNodeSelect = (item) => {
  selectedItem.value = item
  console.log('Selected:', item)
}

const handleViewChange = (view) => {
  currentView.value = view
  console.log('View changed to:', view)
}

const getActionIcon = (action) => {
  const iconMap = {
    'EMAIL': 'mail',
    'SMS': 'message-square',
    'ZALO': 'message-circle',
    'ADD_TAG': 'tag',
    'REMOVE_TAG': 'x'
  }
  return iconMap[action.action_type] || 'circle'
}
</script>

<style scoped>
.flow-graph-demo {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
}

.demo-header {
  padding: 24px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.demo-content {
  flex: 1;
  overflow: hidden;
}

/* List View Styles */
.list-view-demo {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 12px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.list-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.list-item:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.list-item.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.item-content {
  flex: 1;
}

.item-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.item-subtitle {
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}
</style>
