<template>
  <Dialog v-model="show" :options="{ size: '4xl', title: __('Candidate Pool Details') }">
    <template #body-content>
      <div class="candidate-pool-view-modal">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600">{{ __('Loading candidate pool details...') }}</span>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-8">
          <div class="text-red-600 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Error Loading Data') }}</h3>
          <p class="text-gray-600">{{ error }}</p>
        </div>

        <!-- Content -->
        <div v-else-if="candidatePool" class="space-y-6">
          <!-- Header Section -->
          <div class="bg-gray-50 rounded-lg p-6">
            <div class="flex items-start justify-between">
              <div class="flex items-center space-x-4">
                <Avatar :shape="'circle'" :label="candidatePool.avatarText" size="xl" />
                <div>
                  <h2 class="text-2xl font-bold text-gray-900">
                    {{ candidatePool.applicant_name || candidatePool.applicant_id }}
                  </h2>
                  <p class="text-gray-600">{{ candidatePool.applicant_email }}</p>
                  <p class="text-gray-600">{{ candidatePool.applicant_position }}</p>
                </div>
              </div>
              <div class="text-right">
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                  :class="getStatusClasses(candidatePool.statusInfo.color)">
                  {{ candidatePool.statusInfo.text }}
                </span>
                <div class="mt-2 text-sm text-gray-500">
                  {{ __('Last updated') }}: {{ candidatePool.relativeModified }}
                </div>
              </div>
            </div>
          </div>

          <!-- Main Content Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Basic Information -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  {{ __('Applicant Information') }}
                </h3>
                <div class="space-y-3">
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Full Name') }}:</span>
                    <span class="font-medium">{{ candidatePool.applicant_name || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Email') }}:</span>
                    <span class="font-medium">{{ candidatePool.applicant_email || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Phone') }}:</span>
                    <span class="font-medium">{{ candidatePool.applicant_phone || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Position') }}:</span>
                    <span class="font-medium">{{ candidatePool.applicant_position || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2">
                    <span class="text-gray-600">{{ __('Location') }}:</span>
                    <span class="font-medium">{{ candidatePool.applicant_location || '-' }}</span>
                  </div>
                </div>
              </div>

              <!-- Timeline Information -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ __('Timeline') }}
                </h3>
                <div class="space-y-3">
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Shortlist Date') }}:</span>
                    <span class="font-medium">{{ candidatePool.formattedShortlistDate }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Hired Date') }}:</span>
                    <span class="font-medium">{{ candidatePool.formattedHiredDate }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">{{ __('Created') }}:</span>
                    <span class="font-medium">{{ formatDate(candidatePool.creation) }}</span>
                  </div>
                  <div class="flex justify-between py-2">
                    <span class="text-gray-600">{{ __('Modified') }}:</span>
                    <span class="font-medium">{{ formatDate(candidatePool.modified) }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Evaluation Information -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  {{ __('Evaluation') }}
                </h3>
                <div class="space-y-4">
                  <!-- Evaluation Score -->
                  <div>
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-gray-600">{{ __('Score') }}:</span>
                      <span class="font-bold text-lg">
                        {{ candidatePool.evaluation_score ? candidatePool.evaluation_score.toFixed(1) : '-' }}
                        <span v-if="candidatePool.evaluation_score" class="text-sm text-gray-500">/100</span>
                      </span>
                    </div>
                    <div v-if="candidatePool.evaluation_score" class="w-full bg-gray-200 rounded-full h-3">
                      <div class="h-3 rounded-full transition-all duration-300"
                        :class="getScoreBarColor(candidatePool.scoreColor)"
                        :style="`width: ${Math.min(candidatePool.evaluation_score, 100)}%`">
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Skills Information -->
              <div v-if="candidatePool.applicant_skills" class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  {{ __('Skills') }}
                </h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="skill in processSkills(candidatePool.applicant_skills)" :key="skill"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ skill }}
                  </span>
                </div>
              </div>

              <!-- Notes Section -->
              <div v-if="candidatePool.notes || candidatePool.interview_feedback" class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  {{ __('Notes & Feedback') }}
                </h3>
                <div class="space-y-4">
                  <div v-if="candidatePool.interview_feedback">
                    <h4 class="font-medium text-gray-900 mb-2">{{ __('Interview Feedback') }}:</h4>
                    <p class="text-gray-700 bg-gray-50 p-3 rounded-md">{{ candidatePool.interview_feedback }}</p>
                  </div>
                  <div v-if="candidatePool.notes">
                    <h4 class="font-medium text-gray-900 mb-2">{{ __('Notes') }}:</h4>
                    <p class="text-gray-700 bg-gray-50 p-3 rounded-md">{{ candidatePool.notes }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- No Data State -->
        <div v-else class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No Data Available') }}</h3>
          <p class="text-gray-600">{{ __('No candidate pool information found.') }}</p>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end">
        <Button variant="outline" theme="gray" @click="handleClose">
          {{ __('Close') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed, watch } from 'vue'
import { Dialog, Button, Avatar } from 'frappe-ui'
import { processSkills } from '../../services/candidateService'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  candidatePool: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'close'])

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Helper methods
const getStatusClasses = (color) => {
  switch (color) {
    case 'success':
      return 'bg-green-100 text-green-800'
    case 'warning':
      return 'bg-yellow-100 text-yellow-800'
    case 'error':
      return 'bg-red-100 text-red-800'
    case 'info':
      return 'bg-blue-100 text-blue-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const getScoreBarColor = (color) => {
  switch (color) {
    case 'green':
      return 'bg-green-500'
    case 'blue':
      return 'bg-blue-500'
    case 'yellow':
      return 'bg-yellow-500'
    case 'red':
      return 'bg-red-500'
    default:
      return 'bg-gray-500'
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return __('Not set')
  const date = new Date(dateStr)
  return date.toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Methods
const handleClose = () => {
  emit('close')
  show.value = false
}

// Watch for modal close
watch(() => show.value, (newValue) => {
  if (!newValue) {
    emit('close')
  }
})
</script>

<style scoped>
.candidate-pool-view-modal {
  max-height: 80vh;
  overflow-y: auto;
}

/* Custom scrollbar */
.candidate-pool-view-modal::-webkit-scrollbar {
  width: 6px;
}

.candidate-pool-view-modal::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.candidate-pool-view-modal::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.candidate-pool-view-modal::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style> 