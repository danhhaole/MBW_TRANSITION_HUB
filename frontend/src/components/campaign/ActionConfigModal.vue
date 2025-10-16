<template>
  <div class="space-y-6 p-6">
    <!-- Action Type Selection -->
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">
        {{ __("Chọn sự kiện") }}
      </label>
      <select
        v-model="localAction.type"
        class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      >
        <option value="">{{ __("Chọn sự kiện...") }}</option>
        <option value="add_tag">{{ __("Thêm Tag") }}</option>
        <option value="remove_tag">{{ __("Xóa Tag") }}</option>
        <option value="send_email">{{ __("Gửi thông báo email") }}</option>
        <option value="unsubscribe">{{ __("Hủy theo dõi") }}</option>
        <option value="next_scenario">{{ __("Thực hiện kịch bản tiếp theo") }}</option>
      </select>
    </div>

    <!-- Action Configuration -->
    <div v-if="localAction.type" class="border-t pt-4">
      <!-- Add Tag Configuration -->
      <div v-if="localAction.type === 'add_tag'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Thêm Tag") }}</h4>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Chọn tag hoặc tạo mới") }}
          </label>
          <div class="flex space-x-2">
            <select
              v-model="localAction.data.tag_id"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="">{{ __("Chọn tag có sẵn...") }}</option>
              <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
                {{ tag.name }}
              </option>
            </select>
          </div>
        </div>
        
        <!-- Or create new tag -->
        <div class="text-center text-sm text-gray-500">
          {{ __("hoặc") }}
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Tạo tag mới") }}
          </label>
          <div class="flex space-x-2">
            <input
              v-model="localAction.data.new_tag_name"
              type="text"
              :placeholder="__('Tên tag mới (vd: Webinar MBWN DMS 2110)')"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <Button variant="outline" size="sm">
              <div class="flex items-center space-x-2">
                <FeatherIcon name="plus" class="h-4 w-4 mr-1" />
                {{ __("Tạo") }}
              </div>
            </Button>
          </div>
        </div>
        
        <p class="text-xs text-gray-500">
          {{ __("Tag sẽ được thêm vào danh mục và gán cho ứng viên") }}
        </p>
      </div>

      <!-- Send Email Configuration -->
      <div v-else-if="localAction.type === 'send_email'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Gửi thông báo email") }}</h4>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Tên người gửi") }}
          </label>
          <input
            v-model="localAction.data.sender_name"
            type="text"
            :placeholder="__('Tên người gửi')"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Email nhận phản hồi") }}
          </label>
          <input
            v-model="localAction.data.reply_email"
            type="email"
            :placeholder="__('vd: abc@gmail.com')"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Gửi đến (tối đa 5 địa chỉ email)") }}
          </label>
          <input
            v-model="localAction.data.recipients"
            type="text"
            :placeholder="__('vd: abc@gmail.com')"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Chủ đề") }}
          </label>
          <input
            v-model="localAction.data.subject"
            type="text"
            :placeholder="__('Chủ đề')"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Nội dung") }}
          </label>
          <textarea
            v-model="localAction.data.content"
            rows="4"
            :placeholder="__('Nội dung')"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          ></textarea>
        </div>
      </div>

      <!-- Remove Tag Configuration -->
      <div v-else-if="localAction.type === 'remove_tag'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Xóa Tag") }}</h4>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Chọn tag cần xóa") }}
          </label>
          <select
            v-model="localAction.data.tag_id"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">{{ __("Chọn tag...") }}</option>
            <option v-for="tag in availableTags" :key="tag.id" :value="tag.id">
              {{ tag.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Unsubscribe Configuration -->
      <div v-else-if="localAction.type === 'unsubscribe'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Hủy theo dõi") }}</h4>
        <div class="flex items-center space-x-2">
          <input
            v-model="localAction.data.send_confirmation"
            type="checkbox"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
          />
          <label class="text-sm text-gray-700">
            {{ __("Gửi email xác nhận hủy theo dõi") }}
          </label>
        </div>
      </div>

      <!-- Next Scenario Configuration -->
      <div v-else-if="localAction.type === 'next_scenario'" class="space-y-4">
        <h4 class="text-sm font-medium text-gray-900">{{ __("Thực hiện kịch bản tiếp theo") }}</h4>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Chọn kịch bản") }}
          </label>
          <select
            v-model="localAction.data.scenario_id"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">{{ __("Chọn kịch bản...") }}</option>
            <option v-for="scenario in availableScenarios" :key="scenario.id" :value="scenario.id">
              {{ scenario.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Độ trễ thực hiện") }}
          </label>
          <div class="flex space-x-2">
            <input
              v-model="localAction.data.delay_value"
              type="number"
              min="0"
              class="w-20 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
            <select
              v-model="localAction.data.delay_unit"
              class="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            >
              <option value="minutes">{{ __("Phút") }}</option>
              <option value="hours">{{ __("Giờ") }}</option>
              <option value="days">{{ __("Ngày") }}</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-end space-x-3 pt-4 border-t">
      <Button variant="ghost" @click="$emit('cancel')">
        {{ __("Đóng") }}
      </Button>
      <Button variant="solid" @click="handleSave" :disabled="!isValid">
        {{ __("Lưu") }}
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  action: {
    type: Object,
    required: true
  },
  interactionType: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['save', 'cancel'])

// Translation helper
const __ = (text) => text

// Local action state
const localAction = ref({
  trigger: props.action.trigger,
  type: props.action.type || '',
  data: { ...props.action.data } || {}
})

// Mock data
const availableTags = ref([
  { id: '1', name: 'Webinar MBWN DMS 2110' },
  { id: '2', name: 'Interested in React' },
  { id: '3', name: 'Senior Developer' }
])

const availableScenarios = ref([
  { id: '1', name: 'Follow-up Email Sequence' },
  { id: '2', name: 'Interview Invitation' },
  { id: '3', name: 'Technical Assessment' }
])

// Validation
const isValid = computed(() => {
  if (!localAction.value.type) return false
  
  switch (localAction.value.type) {
    case 'add_tag':
      return !!(localAction.value.data.tag_id || localAction.value.data.new_tag_name)
    case 'remove_tag':
      return !!localAction.value.data.tag_id
    case 'send_email':
      return !!(localAction.value.data.sender_name && localAction.value.data.reply_email)
    case 'next_scenario':
      return !!localAction.value.data.scenario_id
    case 'unsubscribe':
      return true
    default:
      return false
  }
})

// Methods
const handleSave = () => {
  if (isValid.value) {
    emit('save', localAction.value)
  }
}

// Initialize default values
watch(() => localAction.value.type, (newType) => {
  if (newType && !localAction.value.data) {
    localAction.value.data = {}
  }
  
  // Set default values for specific types
  if (newType === 'next_scenario' && !localAction.value.data.delay_unit) {
    localAction.value.data.delay_unit = 'minutes'
    localAction.value.data.delay_value = 0
  }
}, { immediate: true })
</script>
