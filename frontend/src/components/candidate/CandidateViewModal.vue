<template>
  <Dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :options="{
      title: __('Candidate Details'),
      size: 'lg'
    }"
  >
    <template #body>
      <div class="p-6">
        <!-- Loading State -->
        <div v-if="loading" class="space-y-4">
          <div class="animate-pulse">
            <div class="h-4 bg-gray-300 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div class="h-4 bg-gray-300 rounded mb-2"></div>
            <div class="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-8">
          <div class="text-red-500 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
          </div>
          <p class="text-gray-600">{{ __(error) }}</p>
        </div>

        <!-- Content -->
        <div v-else-if="candidate" class="space-y-6">
          <!-- Header with Avatar -->
          <div class="flex items-center space-x-4 pb-6 border-b border-gray-200">
            <Avatar
              :shape="'circle'"
              :image="null"
              :label="getAvatarText(candidate.full_name)"
              size="lg"
            />
            
            <div class="flex-1">
              <h2 class="text-2xl font-semibold text-gray-900 mb-1">
                {{ candidate.full_name }}
              </h2>
              <div class="text-gray-600">
                {{ candidate.position || __('No position information available') }}
              </div>
              <div class="mt-2 flex items-center space-x-4">
                <span 
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getStatusClass(candidate.status)"
                >
                  {{ formatCandidateStatus(candidate.status) }}
                </span>
                <span class="text-sm text-gray-500">
                  {{ formatDate(candidate.creation) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Contact Information -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
              </svg>
              Thông tin liên hệ
            </h3>
            
            <div class="bg-gray-50 rounded-lg p-4 space-y-3">
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
                <span class="text-gray-900">{{ candidate.email }}</span>
              </div>
              
              <div v-if="candidate.phone" class="flex items-center">
                <svg class="w-4 h-4 mr-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                </svg>
                <span class="text-gray-900">{{ candidate.phone }}</span>
              </div>
              
              <div v-if="candidate.location" class="flex items-center">
                <svg class="w-4 h-4 mr-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                </svg>
                <span class="text-gray-900">{{ candidate.location }}</span>
              </div>
              
              <div v-if="candidate.experience_years" class="flex items-center">
                <svg class="w-4 h-4 mr-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
                </svg>
                <span class="text-gray-900">{{ candidate.experience_years }} năm kinh nghiệm</span>
              </div>
              
              <div class="flex items-center">
                <svg class="w-4 h-4 mr-3 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd"/>
                </svg>
                <span class="text-gray-900">{{ candidate.source || 'Không xác định' }}</span>
              </div>
            </div>
          </div>

          <!-- Skills -->
          <div v-if="candidateSkills && candidateSkills.length > 0">
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
              </svg>
              Kỹ năng
            </h3>
            
            <div class="flex flex-wrap gap-2">
              <span
                v-for="skill in candidateSkills"
                :key="skill"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
              >
                {{ skill }}
              </span>
            </div>
          </div>

          <!-- Notes -->
          <div v-if="candidate.notes">
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd"/>
              </svg>
              Ghi chú
            </h3>
            
            <div class="bg-gray-50 rounded-lg p-4">
              <p class="text-gray-700 leading-relaxed">{{ candidate.notes }}</p>
            </div>
          </div>
            


          <!-- Metadata -->
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
              </svg>
              Thông tin hệ thống
            </h3>
            
            <div class="bg-gray-50 rounded-lg p-4 space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600">Ngày tạo:</span>
                <span class="text-gray-900">{{ formatDate(candidate.creation) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Cập nhật lần cuối:</span>
                <span class="text-gray-900">{{ formatDate(candidate.modified) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">ID:</span>
                <span class="text-gray-900 font-mono text-sm">{{ candidate.name }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- No Data State -->
        <div v-else class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <svg class="w-12 h-12 mx-auto" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
          </div>
          <p class="text-gray-500">Không có dữ liệu ứng viên</p>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button
          variant="outline"
          @click="$emit('update:modelValue', false)"
        >
          {{ __('Close') }}
        </Button>
        <Button
          v-if="candidate"
          variant="solid"
          @click="$emit('edit-candidate', candidate)"
        >
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
          </svg>
          {{ __('Edit') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed } from 'vue'
import { Dialog, Button, Avatar } from 'frappe-ui'
import {
  formatCandidateStatus,
  getAvatarText,
  processSkills
} from '@/stores/candidate'

// Translation helper function


// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  candidate: {
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
const emit = defineEmits([
  'update:modelValue',
  'edit-candidate',
  'delete-candidate',
  'duplicate-candidate'
])

const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    return new Date(dateString).toLocaleDateString('vi-VN')
  } catch {
    return dateString
  }
}

// Computed
const candidateSkills = computed(() => {
  if (!props.candidate?.skills) return []
  
  // Handle JSON skills from TalentPool
  let skills = props.candidate.skills
  if (typeof skills === 'string') {
    try {
      skills = JSON.parse(skills)
    } catch (e) {
      // If not JSON, treat as comma-separated string
      skills = skills.split(',').map(s => s.trim()).filter(s => s)
    }
  }
  
  if (Array.isArray(skills)) {
    return skills
  } else if (typeof skills === 'object' && skills !== null) {
    return Object.values(skills)
  }
  
  return []
})

// Methods
const getStatusClass = (status) => {
  const statusClasses = {
    'Active': 'bg-green-100 text-green-800',
    'Inactive': 'bg-gray-100 text-gray-800'
  }
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}
</script>

<style scoped>
/* Custom scrollbar for content areas */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: #e5e7eb #f9fafb;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f9fafb;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}
</style>
