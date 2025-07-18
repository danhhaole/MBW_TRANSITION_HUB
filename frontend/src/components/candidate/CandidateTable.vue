<template>
  <div class="candidate-table-container">
    <!-- Table Header -->
    <div class="bg-white border-b border-gray-200 px-6 py-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-medium text-gray-900">{{ __('Candidate List') }}</h2>
        <slot name="toolbar-actions" />
      </div>
    </div>

    <!-- Table Content -->
    <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5">
      <table class="min-w-full divide-y divide-gray-300">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Candidate') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Position') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Skills') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Source') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Last Interaction') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Engagement Score') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Actions') }}</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <!-- Loading State -->
          <tr v-if="loading" v-for="n in 5" :key="n" class="animate-pulse">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 bg-gray-300 rounded-full"></div>
                <div class="ml-4">
                  <div class="h-4 bg-gray-300 rounded w-24"></div>
                  <div class="h-3 bg-gray-300 rounded w-32 mt-1"></div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="h-4 bg-gray-300 rounded w-20"></div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex space-x-1">
                <div class="h-6 bg-gray-300 rounded w-16"></div>
                <div class="h-6 bg-gray-300 rounded w-12"></div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="h-6 bg-gray-300 rounded w-16"></div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="h-4 bg-gray-300 rounded w-20"></div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="h-4 bg-gray-300 rounded w-16"></div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="h-6 bg-gray-300 rounded w-20"></div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right">
              <div class="h-8 bg-gray-300 rounded w-16 ml-auto"></div>
            </td>
          </tr>

          <!-- Empty State -->
          <tr v-else-if="candidates.length === 0">
            <td colspan="8" class="px-6 py-12 text-center">
              <svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
              </svg>
              <h3 class="text-lg font-medium text-gray-900 mb-2">
                {{ hasFilters ? 'Không tìm thấy ứng viên' : 'Chưa có ứng viên nào' }}
              </h3>
              <p class="text-gray-500 mb-4">
                {{ hasFilters 
                  ? 'Thử thay đổi bộ lọc để tìm thấy ứng viên phù hợp.' 
                  : 'Bắt đầu bằng cách thêm ứng viên đầu tiên.' 
                }}
              </p>
              <button
                v-if="!hasFilters"
                @click="$emit('create-candidate')"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                </svg>
                Thêm ứng viên
              </button>
              <button
                v-else
                @click="$emit('clear-filters')"
                class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Xóa bộ lọc
              </button>
            </td>
          </tr>

          <!-- Candidate Rows -->
          <tr v-else v-for="candidate in candidates" :key="candidate.name" class="hover:bg-gray-50">
            <!-- Candidate Column -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <Avatar
                    :shape="'circle'"
                    :image="candidate.avatar"
                    :label="getAvatarText(candidate.full_name)"
                    size="sm"
                  />
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">{{ candidate.full_name }}</div>
                  <div class="text-sm text-gray-500">{{ candidate.email }}</div>
                  <div v-if="candidate.phone" class="text-sm text-gray-500">{{ candidate.phone }}</div>
                </div>
              </div>
            </td>

            <!-- Headline Column -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm text-gray-900">{{ candidate.headline || '-' }}</div>
            </td>

            <!-- Skills Column -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex flex-wrap gap-1 max-w-xs">
                <span
                  v-for="skill in getTopSkills(candidate.skills)"
                  :key="skill"
                  class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ skill }}
                </span>
                <span
                  v-if="candidate.skills && candidate.skills.length > 2"
                  class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                >
                  +{{ candidate.skills.length - 2 }}
                </span>
              </div>
            </td>

            <!-- Source Column -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                v-if="candidate.source"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyan-100 text-cyan-800"
              >
                {{ candidate.source }}
              </span>
              <span v-else class="text-gray-500">-</span>
            </td>

            <!-- Last Interaction Column -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ formatRelativeTime(candidate.last_interaction) }}
            </td>

            <!-- Engagement Column -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-16 bg-gray-200 rounded-full h-2 mr-2">
                  <div
                    :class="[
                      'h-2 rounded-full',
                      getEngagementColorClass(calculateEngagementScore(candidate))
                    ]"
                    :style="{ width: `${calculateEngagementScore(candidate)}%` }"
                  ></div>
                </div>
                <span class="text-sm font-medium text-gray-900">
                  {{ calculateEngagementScore(candidate) }}%
                </span>
              </div>
            </td>

            <!-- Status Column -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                  getStatusClasses(candidate.status)
                ]"
              >
                {{ formatCandidateStatus(candidate.status).text }}
              </span>
            </td>

            <!-- Actions Column -->
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex items-center justify-end space-x-2">
                <button
                  @click="$emit('view-candidate', candidate)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Xem
                </button>
                <div class="relative inline-block text-left">
                  <button
                    @click="toggleDropdown(candidate.name)"
                    class="text-gray-400 hover:text-gray-600 p-1"
                  >
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z"/>
                    </svg>
                  </button>
                  
                  <!-- Dropdown menu -->
                  <div
                    v-if="activeDropdown === candidate.name"
                    class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10"
                  >
                    <div class="py-1">
                      <button
                        @click="handleAction('edit', candidate)"
                        class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                      >
                        <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                        Chỉnh sửa
                      </button>
                      <button
                        @click="handleAction('duplicate', candidate)"
                        class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                      >
                        <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>
                        </svg>
                        Sao chép
                      </button>
                      <hr class="my-1">
                      <button
                        @click="handleAction('delete', candidate)"
                        class="flex items-center px-4 py-2 text-sm text-red-700 hover:bg-red-50 w-full text-left"
                      >
                        <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                        Xóa
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Custom Pagination -->
    <div
      v-if="pagination.total > 0"
      class="flex items-center justify-between p-4 mt-4 bg-white border border-gray-200 rounded-lg"
    >
      <!-- Items per page selector -->
      <div class="flex items-center">
        <span class="text-sm mr-2">Số hàng mỗi trang:</span>
        <FormControl
          type="select"
          :value="pagination.limit"
          :options="itemsPerPageOptions"
          @change="$emit('items-per-page-change', $event.target.value)"
          class="w-20"
        />
      </div>

      <!-- Page info -->
      <div class="text-sm text-gray-600">
        Hiển thị {{ pagination.showing_from }} đến {{ pagination.showing_to }} 
        trong tổng số {{ pagination.total }} ứng viên
      </div>

      <!-- Page navigation -->
      <div class="flex items-center space-x-2">
        <Button
          :disabled="!pagination.has_prev"
          variant="ghost"
          size="sm"
          @click="$emit('page-change', 1)"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M15.707 15.707a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414l5-5a1 1 0 111.414 1.414L11.414 9H17a1 1 0 110 2h-5.586l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd"/>
          </svg>
        </Button>
        
        <Button
          :disabled="!pagination.has_prev"
          variant="ghost"
          size="sm"
          @click="$emit('page-change', pagination.page - 1)"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
        </Button>

        <!-- Page numbers -->
        <div class="flex items-center space-x-1">
          <template v-for="page in visiblePages" :key="page">
            <Button
              v-if="page === '...'"
              variant="ghost"
              size="sm"
              disabled
            >
              ...
            </Button>
            <Button
              v-else
              :variant="page === pagination.page ? 'solid' : 'ghost'"
              size="sm"
              @click="$emit('page-change', page)"
            >
              {{ page }}
            </Button>
          </template>
        </div>

        <Button
          :disabled="!pagination.has_next"
          variant="ghost"
          size="sm"
          @click="$emit('page-change', pagination.page + 1)"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
          </svg>
        </Button>
        
        <Button
          :disabled="!pagination.has_next"
          variant="ghost"
          size="sm"
          @click="$emit('page-change', pagination.pages)"
        >
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10.293 15.707a1 1 0 010-1.414L14.586 10l-4.293-4.293a1 1 0 111.414-1.414l5 5a1 1 0 010 1.414l-5 5a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
            <path fill-rule="evenodd" d="M3 10a1 1 0 011-1h10.586l-4.293-4.293a1 1 0 111.414-1.414l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
          </svg>
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Button, FormControl, Avatar } from 'frappe-ui'
import {
  calculateEngagementScore,
  formatCandidateStatus,
  formatRelativeTime,
  getAvatarText,
  getStatusChipColor,
  getEngagementColor
} from '@/utils/candidateHelpers'

// Translation helper function


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
  pagination: {
    type: Object,
    default: () => ({
      page: 1,
      limit: 25,
      total: 0,
      pages: 0,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
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
  'clear-filters',
  'page-change',
  'items-per-page-change'
])

// Table headers
const headers = [
  {
    title: 'Candidate',
    key: 'candidate',
    align: 'start',
    sortable: false,
    width: '300px'
  },
  {
    title: 'Position',
    key: 'headline',
    align: 'start',
    sortable: false,
    width: '200px'
  },
  {
    title: 'Skills',
    key: 'skills',
    align: 'start',
    sortable: false,
    width: '200px'
  },
  {
    title: 'Source',
    key: 'source',
    align: 'start',
    sortable: false,
    width: '120px'
  },
  {
    title: 'Last Interaction',
    key: 'last_interaction',
    align: 'start',
    sortable: false,
    width: '140px'
  },
  {
    title: 'Engagement Score',
    key: 'engagement',
    align: 'start',
    sortable: false,
    width: '140px'
  },
  {
    title: 'Status',
    key: 'status',
    align: 'start',
    sortable: false,
    width: '120px'
  },
  {
    title: 'Actions',
    key: 'actions',
    align: 'end',
    sortable: false,
    width: '120px'
  }
]

// Items per page options
const itemsPerPageOptions = [
  { title: '10', value: 10 },
  { title: '25', value: 25 },
  { title: '50', value: 50 },
  { title: '100', value: 100 }
]

// Computed
const visiblePages = computed(() => {
  const current = props.pagination.page
  const total = props.pagination.pages
  const delta = 2 // Number of pages to show on each side of current page
  
  if (total <= 7) {
    // Show all pages if total is small
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  const pages = []
  
  // Always show first page
  pages.push(1)
  
  if (current - delta > 2) {
    pages.push('...')
  }
  
  // Show pages around current
  const start = Math.max(2, current - delta)
  const end = Math.min(total - 1, current + delta)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  if (current + delta < total - 1) {
    pages.push('...')
  }
  
  // Always show last page
  if (total > 1) {
    pages.push(total)
  }
  
  return pages
})

// Helper functions
const getTopSkills = (skills) => {
  if (!skills || !Array.isArray(skills)) return []
  return skills.slice(0, 2) // Show only 2 skills in table
}
</script>

<style scoped>
.candidate-table-container {
  width: 100%;
}

/* Custom table styling */
table {
  border-radius: 12px;
}

/* Hover effects */
tbody tr:hover {
  background-color: #f9fafb;
}

/* Custom scrollbar */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #e5e7eb #f9fafb;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f9fafb;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}
</style> 