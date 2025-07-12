<template>
  <Dialog
    :model-value="dialog"
    @update:model-value="dialog = $event"
    :options="{
      title: `${__('Update')}: ${task?.title || __('Task')}`,
      size: 'md',
    }"
  >
    <template #body>
      <div class="p-6">
        <!-- Task Info -->
        <div v-if="task" class="mb-6">
          <div class="flex items-center space-x-3 mb-4">
            <Avatar
              :label="task.candidate?.charAt(0)?.toUpperCase() || 'U'"
              size="lg"
              class="bg-blue-100 text-blue-600"
            />
            <div>
              <div class="text-lg font-semibold text-gray-900">{{ task.candidate }}</div>
              <div class="text-sm text-gray-600">
                {{ __('Campaign') }}: {{ task.campaign }}
              </div>
              <div class="text-xs text-gray-500">
                {{ __('Current status') }}: {{ getStatusLabel(task.status) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Action Selection -->
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-3">
            {{ __('Update status') }}:
          </label>
          <div class="flex flex-wrap gap-2 mb-4">
            <button
              v-for="action in actionOptions"
              :key="action.value"
              :class="[
                'inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
                selectedAction === action.value 
                  ? getActionSelectedClass(action.color)
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200 border border-gray-300'
              ]"
              @click="selectedAction = action.value"
            >
              <svg class="w-4 h-4 mr-1.5" :class="getActionIconClass(action.icon)" fill="currentColor" viewBox="0 0 20 20">
                <path v-if="action.icon === 'mdi-check-circle'" fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
                <path v-else-if="action.icon === 'mdi-calendar-clock'" fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/>
                <path v-else-if="action.icon === 'mdi-skip-next'" d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0010 6v2.798l-5.445-3.63z"/>
                <path v-else-if="action.icon === 'mdi-alert-circle'" fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
              </svg>
              {{ action.label }}
            </button>
          </div>
        </div>

        <!-- Schedule Date for SCHEDULED status -->
        <div v-if="selectedAction === 'SCHEDULED'" class="mb-4">
          <FormControl
            v-model="scheduledDate"
            type="datetime-local"
            label="Ngày lên lịch"
            :min="new Date().toISOString().slice(0, 16)"
          />
        </div>

        <!-- Notes -->
        <div class="mb-4">
          <FormControl
            v-model="notes"
            type="textarea"
            label="Ghi chú chi tiết"
            placeholder="Nhập ghi chú về kết quả thực hiện tác vụ..."
            :rows="3"
          />
        </div>
      </div>

      <div class="flex justify-end space-x-3 p-6">
        <Button
          variant="outline"
          @click="closeModal"
        >
          Hủy
        </Button>
        <Button
          :disabled="!selectedAction || (selectedAction === 'SCHEDULED' && !scheduledDate)"
          :loading="loading"
          @click="updateTask"
        >
          {{ getActionButtonText() }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FormControl, Avatar } from 'frappe-ui'
import moment from 'moment'

// Translation helper function
const __ = (text) => text

const props = defineProps({
  modelValue: Boolean,
  task: Object
})

const emit = defineEmits(['update:modelValue', 'update:completed'])

// Reactive data
const selectedAction = ref('')
const scheduledDate = ref('')
const notes = ref('')
const loading = ref(false)

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Action options based on current task status
const actionOptions = computed(() => {
  return [
    { 
      value: 'EXECUTED', 
      label: __('Complete'), 
      color: 'success',
      icon: 'mdi-check-circle'
    },
    { 
      value: 'SCHEDULED', 
      label: __('Schedule'), 
      color: 'info',
      icon: 'mdi-calendar-clock'
    },
    { 
      value: 'SKIPPED', 
      label: __('Skip'), 
      color: 'warning',
      icon: 'mdi-skip-next'
    },
    { 
      value: 'FAILED', 
      label: __('Failed'), 
      color: 'error',
      icon: 'mdi-alert-circle'
    }
  ]
})

// Methods
const getActionSelectedClass = (color) => {
  const colorClasses = {
    success: 'bg-green-100 text-green-800 border border-green-300',
    info: 'bg-blue-100 text-blue-800 border border-blue-300',
    warning: 'bg-yellow-100 text-yellow-800 border border-yellow-300',
    error: 'bg-red-100 text-red-800 border border-red-300'
  }
  return colorClasses[color] || 'bg-blue-100 text-blue-800 border border-blue-300'
}

const getActionIconClass = (icon) => {
  // Return empty class since we're using SVG paths directly
  return ''
}

const closeModal = () => {
  resetForm()
  dialog.value = false
}

const resetForm = () => {
  selectedAction.value = ''
  scheduledDate.value = ''
  notes.value = ''
  loading.value = false
}

const getActionButtonText = () => {
  switch (selectedAction.value) {
    case 'EXECUTED':
      return 'Hoàn thành tác vụ'
    case 'SCHEDULED':
      return 'Lên lịch tác vụ'
    case 'SKIPPED':
      return 'Bỏ qua tác vụ'
    case 'FAILED':
      return 'Đánh dấu thất bại'
    default:
      return 'Cập nhật tác vụ'
  }
}

const getStatusLabel = (status) => {
  const statusLabels = {
    'PENDING_MANUAL': 'Chờ xác nhận',
    'SCHEDULED': 'Đã lên lịch',
    'EXECUTED': 'Đã hoàn thành',
    'SKIPPED': 'Đã bỏ qua',
    'FAILED': 'Thất bại'
  }
  return statusLabels[status] || status
}

const updateTask = async () => {
  if (!selectedAction.value || !props.task) return
  
  // Validate scheduled date if action is SCHEDULED
  if (selectedAction.value === 'SCHEDULED' && !scheduledDate.value) {
    return
  }

  loading.value = true
  
  try {
    const taskData = {
      taskId: props.task.id,
      action: selectedAction.value,
      scheduledDate: scheduledDate.value,
      notes: notes.value,
      updatedAt: moment().format("YYYY-MM-DD HH:mm:ss") // Use moment for consistent date formatting
    }

    // Emit the update event
    emit('update:completed', taskData)
    
    // Close modal immediately after emitting
    dialog.value = false
    
  } catch (error) {
    console.error('Error updating task:', error)
  } finally {
    loading.value = false
  }
}

// Watchers
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    resetForm()
  }
})

watch(() => props.task, (newTask) => {
  if (newTask) {
    resetForm()
  }
})

// Watch for successful updates to close modal
watch(() => dialog.value, (newVal) => {
  if (!newVal) {
    resetForm()
  }
})
</script>

<style scoped>
.task-modal button {
  transition: all 0.2s ease-in-out;
}

.task-modal button:hover {
  transform: translateY(-1px);
}
</style> 