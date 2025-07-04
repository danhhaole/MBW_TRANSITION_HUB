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
          <div class="d-flex align-center gap-3 mb-4">
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
            </div>
          </div>
        </div>

        <!-- Outcome Selection -->
        <div class="mb-4">
          <v-label class="text-subtitle-1 font-weight-medium mb-3">
            Cập nhật kết quả:
          </v-label>
          <div class="d-flex flex-wrap gap-2 mb-4">
            <v-chip
              v-for="outcome in outcomeOptions"
              :key="outcome.value"
              :color="selectedOutcome === outcome.value ? 'primary' : 'default'"
              :variant="selectedOutcome === outcome.value ? 'flat' : 'outlined'"
              clickable
              @click="selectedOutcome = outcome.value"
            >
              {{ outcome.label }}
            </v-chip>
          </div>
        </div>

        <!-- Notes -->
        <div class="mb-4">
          <v-textarea
            v-model="notes"
            label="Ghi chú chi tiết"
            placeholder="Nhập ghi chú về cuộc gọi hoặc tác vụ..."
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
          :disabled="!selectedOutcome"
          :loading="loading"
          @click="completeTask"
        >
          Hoàn thành tác vụ
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  task: Object
})

const emit = defineEmits(['update:modelValue', 'update:completed'])

// Reactive data
const selectedOutcome = ref('')
const notes = ref('')
const loading = ref(false)

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Outcome options based on task type
const outcomeOptions = computed(() => {
  if (props.task?.type === 'MANUAL_CALL') {
    return [
      { value: 'answered', label: 'Đã trả lời' },
      { value: 'no_answer', label: 'Không nghe máy' },
      { value: 'voicemail', label: 'Để lại lời nhắn' },
      { value: 'wrong_number', label: 'Sai số' },
      { value: 'interested', label: 'Quan tâm' },
      { value: 'not_interested', label: 'Không quan tâm' }
    ]
  } else {
    return [
      { value: 'completed', label: 'Đã hoàn thành' },
      { value: 'reviewed', label: 'Đã review' },
      { value: 'approved', label: 'Đã duyệt' },
      { value: 'rejected', label: 'Từ chối' },
      { value: 'needs_revision', label: 'Cần sửa đổi' }
    ]
  }
})

// Methods
const closeModal = () => {
  resetForm()
  dialog.value = false
}

const resetForm = () => {
  selectedOutcome.value = ''
  notes.value = ''
  loading.value = false
}

const completeTask = async () => {
  if (!selectedOutcome.value || !props.task) return

  loading.value = true
  
  try {
    const taskData = {
      taskId: props.task.id,
      outcome: selectedOutcome.value,
      notes: notes.value,
      completedAt: new Date().toISOString()
    }

    emit('update:completed', taskData)
  } catch (error) {
    console.error('Error completing task:', error)
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
</script>

<style scoped>
.bg-primary {
  background-color: rgb(var(--v-theme-primary)) !important;
}
</style> 