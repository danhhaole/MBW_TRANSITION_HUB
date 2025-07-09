<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <v-card rounded="lg">
      <!-- Header -->
      <v-card-title class="d-flex align-center justify-space-between pa-6 bg-primary">
        <h2 class="text-h5 text-white font-weight-bold">
          Cập nhật: {{ task?.title || 'Tác vụ' }}
        </h2>
        <v-btn 
          icon="mdi-close" 
          variant="text" 
          color="white"
          @click="closeModal"
        ></v-btn>
      </v-card-title>

      <!-- Body -->
      <v-card-text class="pa-6">
        <!-- Task Info -->
        <div v-if="task" class="mb-6">
          <div class="d-flex align-center ga-3 mb-4">
            <v-avatar size="48" color="primary" variant="tonal">
              <span class="text-h6 font-weight-bold">
                {{ task.candidate?.charAt(0)?.toUpperCase() || 'U' }}
              </span>
            </v-avatar>
            <div>
              <div class="text-h6 font-weight-bold">{{ task.candidate }}</div>
              <div class="text-subtitle-2 text-medium-emphasis">
                Chiến dịch: {{ task.campaign }}
              </div>
              <div class="text-caption text-medium-emphasis">
                Trạng thái hiện tại: {{ getStatusLabel(task.status) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Action Selection -->
        <div class="mb-4">
          <v-label class="text-subtitle-1 font-weight-medium mb-3">
            Cập nhật trạng thái:
          </v-label>
          <div class="d-flex ga-1 flex-wrap gap-2 mb-4">
            <v-chip
              v-for="action in actionOptions"
              :key="action.value"
              :color="selectedAction === action.value ? action.color : 'default'"
              :variant="selectedAction === action.value ? 'flat' : 'outlined'"
              clickable
              @click="selectedAction = action.value"
            >
              <v-icon :icon="action.icon" size="small" class="mr-1" />
              {{ action.label }}
            </v-chip>
          </div>
        </div>

        <!-- Schedule Date for SCHEDULED status -->
        <div v-if="selectedAction === 'SCHEDULED'" class="mb-4">
          <v-text-field
            v-model="scheduledDate"
            label="Ngày lên lịch"
            type="datetime-local"
            variant="outlined"
            hide-details
            :min="new Date().toISOString().slice(0, 16)"
          />
        </div>

        <!-- Notes -->
        <div class="mb-4">
          <v-textarea
            v-model="notes"
            label="Ghi chú chi tiết"
            placeholder="Nhập ghi chú về kết quả thực hiện tác vụ..."
            rows="3"
            variant="outlined"
            hide-details
          />
        </div>
      </v-card-text>

      <!-- Footer -->
      <v-card-actions class="pa-6 pt-0">
        <v-spacer />
        <v-btn
          variant="text"
          @click="closeModal"
        >
          Hủy
        </v-btn>
        <v-btn
          color="primary"
          variant="flat"
          :disabled="!selectedAction || (selectedAction === 'SCHEDULED' && !scheduledDate)"
          :loading="loading"
          @click="updateTask"
        >
          {{ getActionButtonText() }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import moment from 'moment'

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
      label: 'Hoàn thành', 
      color: 'success',
      icon: 'mdi-check-circle'
    },
    { 
      value: 'SCHEDULED', 
      label: 'Lên lịch', 
      color: 'info',
      icon: 'mdi-calendar-clock'
    },
    { 
      value: 'SKIPPED', 
      label: 'Bỏ qua', 
      color: 'warning',
      icon: 'mdi-skip-next'
    },
    { 
      value: 'FAILED', 
      label: 'Thất bại', 
      color: 'error',
      icon: 'mdi-alert-circle'
    }
  ]
})

// Methods
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
.bg-primary {
  background-color: rgb(var(--v-theme-primary)) !important;
}
</style> 