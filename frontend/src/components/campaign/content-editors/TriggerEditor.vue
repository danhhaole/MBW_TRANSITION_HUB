<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="border-b border-gray-200 pb-4">
      <div class="flex items-center space-x-2 mb-2">
        <FeatherIcon name="zap" class="h-5 w-5 text-purple-600" />
        <h3 class="text-lg font-medium text-gray-900">Cấu hình Trigger</h3>
      </div>
      <p class="text-sm text-gray-500">Thiết lập điều kiện kích hoạt flow</p>
    </div>

    <!-- Trigger Name & Description (Read-only) -->
    <div class="space-y-4">

    </div>

    <!-- Connected Account Selection -->
    <div class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        <FeatherIcon name="user" class="inline h-4 w-4 mr-1" />
        Chọn tài khoản đã liên kết
      </label>
      <div class="relative">
        <select
          v-model="localContent.connected_account"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          @change="updateContent"
        >
          <option value="">Chọn tài khoản...</option>
          <option value="zalo_account_1">Zalo Business - Công ty ABC</option>
          <option value="zalo_account_2">Zalo Business - Shop XYZ</option>
          <option value="facebook_account_1">Facebook Page - Fanpage DEF</option>
        </select>
        <div class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none">
          <FeatherIcon name="chevron-down" class="h-4 w-4 text-gray-400" />
        </div>
      </div>
    </div>

    <!-- Sequence Selection (only for sequence triggers) -->
    <div v-if="isSequenceTrigger()" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        <FeatherIcon name="list" class="inline h-4 w-4 mr-1" />
        Chọn Sequence
      </label>
      <select
        v-model="localContent.sequence_id"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
        @change="updateContent"
      >
        <option value="">Chọn sequence...</option>
        <option value="seq_1">Sequence Chào mừng khách hàng mới</option>
        <option value="seq_2">Sequence Khuyến mãi cuối tuần</option>
        <option value="seq_3">Sequence Chăm sóc khách hàng VIP</option>
      </select>
    </div>

    <!-- Channel Selection (only for new subscriber trigger) -->
    <div v-if="isNewSubscriberTrigger()" class="space-y-3">
      <label class="block text-sm font-medium text-gray-700">
        <FeatherIcon name="radio" class="inline h-4 w-4 mr-1" />
        Kênh áp dụng (tùy chọn)
      </label>
      <div class="flex flex-wrap gap-3">
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="zalo"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">Zalo</span>
        </label>
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="facebook"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">Facebook</span>
        </label>
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="email"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">Email</span>
        </label>
        <label class="inline-flex items-center">
          <input
            v-model="localContent.channels"
            type="checkbox"
            value="sms"
            class="rounded border-gray-300 text-blue-600 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
            @change="updateContent"
          />
          <span class="ml-2 text-sm text-gray-700">SMS</span>
        </label>
      </div>
    </div>

    <!-- Advanced Conditions - Always show for all trigger types -->
    <div class="space-y-4">
      <div class="border-t border-gray-200 pt-4">
        <label class="block text-sm font-medium text-gray-700 mb-3">
          <FeatherIcon name="filter" class="inline h-4 w-4 mr-1" />
          Điều kiện kích hoạt
        </label>
        <p class="text-xs text-gray-500 mb-4">
          Kích hoạt khi đáp ứng các điều kiện sau
        </p>
        
        <!-- Condition Groups -->
        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <div class="space-y-3">
            <div v-for="(condition, index) in localContent.Conditional_Split" :key="index" 
                 class="bg-white border border-gray-200 rounded-lg p-3">
              <div class="flex items-center space-x-2">
                <select
                  v-model="condition.field"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                  @change="updateContent"
                >
                  <option value="">Chọn trường...</option>
                  <option value="ho_ten">Họ tên</option>
                  <option value="email">Email</option>
                  <option value="phone">Số điện thoại</option>
                  <option value="age">Tuổi</option>
                  <option value="gender">Giới tính</option>
                  <option value="location">Địa điểm</option>
                  <option value="source">Nguồn đăng ký</option>
                  <option value="tag">Tag</option>
                </select>
                
                <select
                  v-model="condition.operator"
                  class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                  @change="updateContent"
                >
                  <option value="equals">Là</option>
                  <option value="not_equals">Không là</option>
                  <option value="contains">Chứa</option>
                  <option value="not_contains">Không chứa</option>
                  <option value="starts_with">Bắt đầu bằng</option>
                  <option value="ends_with">Kết thúc bằng</option>
                  <option value="greater_than">Lớn hơn</option>
                  <option value="less_than">Nhỏ hơn</option>
                  <option value="is_empty">Trống</option>
                  <option value="is_not_empty">Không trống</option>
                </select>
                
                <input
                  v-if="!['is_empty', 'is_not_empty'].includes(condition.operator)"
                  v-model="condition.value"
                  type="text"
                  :placeholder="getFieldPlaceholder(condition.field)"
                  class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 text-sm"
                  @input="updateContent"
                />
                
                <button
                  @click="removeCondition(index)"
                  class="text-red-500 hover:text-red-700 p-1 rounded"
                  title="Xóa điều kiện"
                >
                  <FeatherIcon name="trash-2" class="h-4 w-4" />
                </button>
              </div>
              
              <!-- Condition Preview -->
              <div v-if="condition.field && condition.operator" class="mt-2 text-xs text-gray-600 bg-blue-50 px-2 py-1 rounded">
                {{ getConditionPreview(condition) }}
              </div>
            </div>
            
            <!-- Add Condition Button -->
            <button
              @click="addCondition"
              class="w-full inline-flex items-center justify-center px-3 py-2 border border-dashed border-gray-300 rounded-md text-sm font-medium text-gray-600 bg-white hover:bg-gray-50 hover:border-gray-400"
            >
              <FeatherIcon name="plus" class="h-4 w-4 mr-1" />
              Thêm điều kiện
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Preview Summary -->
    <div v-if="localContent.trigger_type" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div class="flex items-start space-x-2">
        <FeatherIcon name="info" class="h-4 w-4 text-blue-600 mt-0.5" />
        <div>
          <h4 class="text-sm font-medium text-blue-900">Tóm tắt cấu hình</h4>
          <p class="text-sm text-blue-700 mt-1">
            {{ getTriggerSummary() }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  content: { type: Object, default: () => ({}) },
  readonly: { type: Boolean, default: false }
})

const emit = defineEmits(['update:content'])

// Local content with default structure
const localContent = ref({
  name: '',
  description: '',
  connected_account: '',
  trigger_type: '',
  sequence_id: '',
  channels: [],
  Conditional_Split: [],
  ...props.content
})

// Watch for external content changes
watch(() => props.content, (newContent) => {
  localContent.value = {
    name: '',
    description: '',
    connected_account: '',
    trigger_type: '',
    sequence_id: '',
    channels: [],
    Conditional_Split: [],
    ...newContent
  }
}, { deep: true, immediate: true })

// Update content
const updateContent = () => {
  emit('update:content', { ...localContent.value })
}

// Helper methods to check trigger type
const isSequenceTrigger = () => {
  return localContent.value.trigger_type === 'subscribe_sequence' || 
         localContent.value.trigger_type === 'unsubscribe_sequence'
}

const isNewSubscriberTrigger = () => {
  return localContent.value.trigger_type === 'new_subscriber_all'
}

// Add condition
const addCondition = () => {
  localContent.value.Conditional_Split.push({
    field: '',
    operator: 'equals',
    value: ''
  })
  updateContent()
}

// Remove condition
const removeCondition = (index) => {
  localContent.value.Conditional_Split.splice(index, 1)
  updateContent()
}

// Get field placeholder
const getFieldPlaceholder = (field) => {
  const placeholders = {
    ho_ten: 'VD: Minh, Nguyễn Văn A',
    email: 'VD: minh@example.com',
    phone: 'VD: 0123456789',
    age: 'VD: 25',
    gender: 'VD: Nam, Nữ',
    location: 'VD: Hà Nội, TP.HCM',
    source: 'VD: Facebook, Website',
    tag: 'VD: VIP, Khách hàng mới'
  }
  return placeholders[field] || 'Nhập giá trị...'
}

// Get condition preview
const getConditionPreview = (condition) => {
  if (!condition.field || !condition.operator) return ''
  
  const fieldNames = {
    ho_ten: 'Họ tên',
    email: 'Email',
    phone: 'Số điện thoại',
    age: 'Tuổi',
    gender: 'Giới tính',
    location: 'Địa điểm',
    source: 'Nguồn đăng ký',
    tag: 'Tag'
  }
  
  const operatorNames = {
    equals: 'là',
    not_equals: 'không là',
    contains: 'chứa',
    not_contains: 'không chứa',
    starts_with: 'bắt đầu bằng',
    ends_with: 'kết thúc bằng',
    greater_than: 'lớn hơn',
    less_than: 'nhỏ hơn',
    is_empty: 'trống',
    is_not_empty: 'không trống'
  }
  
  const fieldName = fieldNames[condition.field] || condition.field
  const operatorName = operatorNames[condition.operator] || condition.operator
  
  if (['is_empty', 'is_not_empty'].includes(condition.operator)) {
    return `${fieldName} ${operatorName}`
  }
  
  return `${fieldName} ${operatorName} "${condition.value || '...'}"`
}

// Get trigger summary
const getTriggerSummary = () => {
  const triggerTypes = {
    subscribe_sequence: 'Kích hoạt khi khách hàng đăng ký sequence',
    unsubscribe_sequence: 'Kích hoạt khi khách hàng hủy đăng ký sequence',
    new_subscriber_all: 'Kích hoạt khi có khách hàng mới đăng ký'
  }
  
  let summary = triggerTypes[localContent.value.trigger_type] || ''
  
  if (localContent.value.sequence_id && (localContent.value.trigger_type === 'subscribe_sequence' || localContent.value.trigger_type === 'unsubscribe_sequence')) {
    summary += ` "${localContent.value.sequence_id}"`
  }
  
  if (localContent.value.channels && localContent.value.channels.length > 0) {
    summary += ` từ kênh: ${localContent.value.channels.join(', ')}`
  }
  
  if (localContent.value.Conditional_Split && localContent.value.Conditional_Split.length > 0) {
    summary += ` khi ${localContent.value.Conditional_Split.map(c => getConditionPreview(c)).join(' và ')}`
  }
  
  return summary
}
</script>
