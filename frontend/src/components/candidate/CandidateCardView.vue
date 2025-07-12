<template>
  <div>
    <!-- Candidate Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Loading State -->
      <template v-if="loading">
        <div
          v-for="n in 6"
          :key="n"
          class="bg-white border border-gray-200 rounded-lg shadow-sm p-4 min-h-[320px]"
        >
          <!-- Skeleton Loader -->
          <div class="animate-pulse">
            <div class="flex items-center mb-4">
              <div class="w-11 h-11 bg-gray-300 rounded-full mr-3"></div>
              <div class="flex-1">
                <div class="h-4 bg-gray-300 rounded mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-3/4"></div>
              </div>
            </div>
            <div class="space-y-3">
              <div class="h-3 bg-gray-200 rounded"></div>
              <div class="h-3 bg-gray-200 rounded w-5/6"></div>
              <div class="flex space-x-2">
                <div class="h-6 bg-gray-200 rounded w-16"></div>
                <div class="h-6 bg-gray-200 rounded w-12"></div>
              </div>
              <div class="h-2 bg-gray-200 rounded"></div>
              <div class="flex justify-between items-center">
                <div class="h-6 bg-gray-200 rounded w-20"></div>
                <div class="h-8 bg-gray-200 rounded w-24"></div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Candidate Cards -->
      <div
        v-for="candidate in candidates"
        :key="candidate.name"
        class="candidate-card bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer transform hover:-translate-y-1 min-h-[320px]"
        @click="$emit('view-candidate', candidate)"
      >
        <div class="p-4 h-full flex flex-col">
          <!-- Header with Avatar and Basic Info -->
          <div class="flex items-center mb-4">
            <div class="mr-3 flex-shrink-0">
              <Avatar
                :shape="'circle'"
                :image="candidate.avatar"
                :label="getAvatarText(candidate.full_name)"
                size="md"
              />
            </div>
            
            <div class="flex-1 min-w-0">
              <h3 class="text-base font-medium text-gray-900 truncate">
                {{ candidate.full_name }}
              </h3>
              <p class="text-sm text-gray-500 truncate">
                {{ candidate.headline || __('No information available') }}
              </p>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="mb-4 space-y-1">
            <div class="flex items-center text-sm text-gray-600">
              <svg class="w-3.5 h-3.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
              </svg>
              <span class="truncate">{{ candidate.email }}</span>
            </div>
            <div class="flex items-center text-sm text-gray-600">
              <svg class="w-3.5 h-3.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
              </svg>
              <span>{{ getLocation(candidate) }}</span>
            </div>
          </div>

          <!-- Skills -->
          <div class="mb-4">
            <div class="text-xs text-gray-500 mb-2">Kỹ năng</div>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="skill in getTopSkills(candidate.skills, 2)"
                :key="skill"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
              >
                {{ skill }}
              </span>
              <span
                v-if="processSkills(candidate.skills).length > 2"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-600 border border-gray-200"
              >
                +{{ processSkills(candidate.skills).length - 2 }}
              </span>
            </div>
          </div>

          <!-- Talent Pools -->
          <div class="mb-4">
            <div class="text-xs text-gray-500 mb-2">Talent Pools</div>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="pool in getTalentPools(candidate).slice(0, 1)"
                :key="pool"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-cyan-50 text-cyan-700"
              >
                {{ pool }}
              </span>
            </div>
          </div>

          <!-- Engagement Score -->
          <div class="mb-4">
            <div class="text-xs text-gray-500 mb-2">Điểm tương tác</div>
            <div class="flex items-center">
              <div class="flex-1 mr-2">
                <div class="w-full bg-gray-200 rounded-full h-1.5">
                  <div
                    class="h-1.5 rounded-full transition-all duration-300"
                    :class="getEngagementBarColor(calculateEngagementScore(candidate))"
                    :style="`width: ${calculateEngagementScore(candidate)}%`"
                  ></div>
                </div>
              </div>
              <span class="text-xs font-medium text-gray-700">
                {{ calculateEngagementScore(candidate) }}%
              </span>
            </div>
          </div>

          <!-- Footer with Status and Actions -->
          <div class="flex justify-between items-center mt-auto">
            <span
              class="inline-flex items-center px-2 py-1 rounded text-xs font-medium"
              :class="getStatusClasses(candidate.status)"
            >
              {{ formatCandidateStatus(candidate.status).text }}
            </span>
            
            <div class="flex items-center space-x-1">
              <button
                class="text-blue-600 hover:text-blue-800 text-xs font-medium px-2 py-1 rounded hover:bg-blue-50 transition-colors"
                @click.stop="$emit('view-candidate', candidate)"
              >
                {{ __('View Details') }}
              </button>
              <div class="relative" v-if="false">
                <button
                  class="p-1 text-gray-400 hover:text-gray-600 rounded hover:bg-gray-100 transition-colors"
                  @click.stop="toggleDropdown(candidate.name)"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
                  </svg>
                </button>
                
                <!-- Dropdown Menu -->
                <div
                  v-if="dropdownOpen === candidate.name"
                  class="absolute right-0 top-full mt-1 w-40 bg-white border border-gray-200 rounded-md shadow-lg z-50"
                >
                  <div class="py-1">
                    <button
                      class="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                      @click.stop="$emit('edit-candidate', candidate); dropdownOpen = null"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      {{ __('Edit') }}
                    </button>
                    <button
                      class="flex items-center w-full px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                      @click.stop="$emit('duplicate-candidate', candidate); dropdownOpen = null"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      {{ __('Duplicate') }}
                    </button>
                    <div class="border-t border-gray-100"></div>
                    <button
                      class="flex items-center w-full px-3 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                      @click.stop="$emit('delete-candidate', candidate); dropdownOpen = null"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                      {{ __('Delete') }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div
      v-if="!loading && candidates.length === 0"
      class="flex flex-col items-center justify-center py-12 px-4 text-center"
      style="min-height: 300px;"
    >
      <svg class="w-16 h-16 text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        {{ hasFilters ? __('No candidates found') : __('No candidates yet') }}
      </h3>
      <p class="text-sm text-gray-500 max-w-sm mb-6">
        {{ hasFilters 
          ? __('Try changing filters to find suitable candidates.') 
          : __('Start by adding your first candidate.') 
        }}
      </p>
      <button
        v-if="!hasFilters"
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors"
        @click="$emit('create-candidate')"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        {{ __('Add Candidate') }}
      </button>
      <button
        v-else
        class="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-50 transition-colors"
        @click="$emit('clear-filters')"
      >
        {{ __('Clear Filters') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Avatar } from 'frappe-ui'
import {
  calculateEngagementScore,
  formatCandidateStatus,
  getAvatarText,
  getStatusChipColor,
  getEngagementColor,
  processSkills
} from '../../services/candidateService'

// Translation helper function
const __ = (text) => text

// Props
const props = defineProps({
  candidates: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  hasFilters: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits([
  'view-candidate',
  'edit-candidate',
  'delete-candidate',
  'duplicate-candidate',
  'create-candidate',
  'clear-filters'
])

// State
const dropdownOpen = ref(null)

// Helper functions
const getTopSkills = (skills, limit) => {
  const skillsArray = processSkills(skills)
  return skillsArray.slice(0, limit || 3)
}

const getTalentPools = (candidate) => {
  // Mock talent pools based on skills or source
  const pools = []
  
  if (candidate.skills) {
    const skills = processSkills(candidate.skills)
    if (skills.some(skill => ['React', 'Vue.js', 'Angular', 'JavaScript'].includes(skill))) {
      pools.push('Frontend Experts')
    }
    if (skills.some(skill => ['Node.js', 'Python', 'Java', 'AWS'].includes(skill))) {
      pools.push('Software Developers')
    }
    if (skills.some(skill => ['React Native', 'Flutter', 'iOS', 'Android'].includes(skill))) {
      pools.push('Mobile Developers')
    }
    if (skills.some(skill => ['AWS', 'DevOps', 'Docker', 'Kubernetes'].includes(skill))) {
      pools.push('Cloud Engineers')
    }
  }
  
  // Default pool if no specific match
  if (pools.length === 0) {
    pools.push('Software Developers')
  }
  
  return pools
}

const getLocation = (candidate) => {
  // Mock location data - in real app this would come from candidate profile
  const locations = ['Ho Chi Minh City', 'Ha Noi', 'Da Nang', 'Can Tho']
  return candidate.location || locations[Math.floor(Math.random() * locations.length)]
}

const getStatusClasses = (status) => {
  const statusConfig = formatCandidateStatus(status)
  const baseClasses = ''
  
  switch (statusConfig.color) {
    case 'success':
      return 'bg-green-50 text-green-700'
    case 'warning':
      return 'bg-yellow-50 text-yellow-700'
    case 'error':
      return 'bg-red-50 text-red-700'
    case 'info':
      return 'bg-blue-50 text-blue-700'
    case 'purple':
      return 'bg-purple-50 text-purple-700'
    default:
      return 'bg-gray-50 text-gray-700'
  }
}

const getEngagementBarColor = (score) => {
  if (score >= 80) return 'bg-green-500'
  if (score >= 60) return 'bg-blue-500'
  if (score >= 40) return 'bg-yellow-500'
  if (score >= 20) return 'bg-orange-500'
  return 'bg-red-500'
}

const toggleDropdown = (candidateId) => {
  dropdownOpen.value = dropdownOpen.value === candidateId ? null : candidateId
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    dropdownOpen.value = null
  }
}

// Add event listener for clicking outside
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.candidate-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  cursor: pointer;
}

.candidate-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style> 