<template>
  <div class="container mx-auto px-4 py-8 max-w-7xl">
    <!-- Header Section -->
    <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
      <!-- Header with filters -->
      <div class="flex flex-wrap items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-gray-800">{{ __('Recruitment Campaign List') }}</h2>
        
        <div class="flex items-center space-x-4 mt-4 sm:mt-0">
          <!-- Search -->
          <div class="relative">
            <input 
              type="text" 
              :value="searchText"
              @input="handleSearch($event.target.value)"
              :placeholder="__('Search...')" 
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
          </div>
          
          <!-- Filter -->
          <div class="relative">
            <select 
              :value="statusFilter"
              @change="handleFilterChange($event.target.value)"
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none"
            >
              <option value="all">Tất cả trạng thái</option>
              <option value="ACTIVE">Đang hoạt động</option>
              <option value="PAUSED">Tạm dừng</option>
              <option value="ARCHIVED">Lưu trữ</option>
              <option value="DRAFT">Nháp</option>
            </select>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z"></path>
            </svg>
          </div>
          
          <!-- Refresh Button -->
          <button 
            @click="handleRefresh"
            :disabled="loading"
            class="px-4 py-2 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" :class="{'animate-spin': loading}" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Làm mới
          </button>
          
          <!-- Add New Button -->
          <button 
            @click="$emit('create')"
            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            Tạo mới
          </button>
        </div>
      </div>
    </div>

    <!-- Table Content -->
    <div class="bg-white rounded-xl shadow-lg p-6">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-4 text-gray-600">Đang tải dữ liệu...</p>
      </div>

      <!-- Table -->
      <div v-else-if="campaigns?.length > 0" class="overflow-x-auto">
        <table class="min-w-full bg-white rounded-lg overflow-hidden">
          <thead class="bg-gray-100">
            <tr>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Tên chiến dịch</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Trạng thái</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Tiến độ</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Ngày tạo</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Người phụ trách</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">Hành động</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="campaign in campaigns" 
              :key="campaign.name || campaign.id"
              class="hover:bg-gray-50"
            >
              <!-- Campaign Name -->
              <td class="py-4 px-4">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <div class="font-medium text-gray-800">{{ campaign.campaign_name || campaign.name }}</div>
                    <div class="text-xs text-gray-500">{{ campaign.description || 'Tuyển dụng' }}</div>
                  </div>
                </div>
              </td>

              <!-- Status -->
              <td class="py-4 px-4">
                <span :class="getStatusBadgeClass(campaign.status)" class="text-xs px-2 py-1 rounded-full">
                  {{ getStatusText(campaign.status) }}
                </span>
              </td>

              <!-- Progress -->
              <td class="py-4 px-4">
                <div class="flex items-center">
                  <div class="w-20 h-2 bg-gray-200 rounded-full mr-2">
                    <div 
                      class="h-full rounded-full"
                      :class="getProgressBarClass(campaign.status)"
                      :style="`width: ${getProgress(campaign)}%`"
                    ></div>
                  </div>
                  <span class="text-xs font-medium text-gray-700">{{ getProgress(campaign) }}%</span>
                </div>
              </td>

              <!-- Date -->
              <td class="py-4 px-4 text-sm text-gray-700">
                {{ formatDate(campaign.start_date || campaign.creation) }}
              </td>

              <!-- Assignees -->
              <td class="py-4 px-4">
                <div class="flex -space-x-2">
                  <div 
                    v-if="campaign.owner_id" 
                    class="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center border-2 border-white"
                  >
                    <span class="text-xs font-medium text-blue-700">{{ getInitials(campaign.owner_id) }}</span>
                  </div>
                  <div 
                    v-if="campaign.target_segment" 
                    class="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center border-2 border-white"
                  >
                    <span class="text-xs font-medium text-purple-700">{{ getInitials(campaign.target_segment) }}</span>
                  </div>
                </div>
              </td>

              <!-- Actions -->
              <td class="py-4 px-4">
                <div class="flex space-x-2">
                  <button 
                    @click="handleView(campaign)"
                    class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                  >
                    Xem timeline
                  </button>
                  <div class="relative">
                    <button 
                      @click="toggleDropdown(campaign.name || campaign.id)"
                      class="text-gray-600 hover:text-gray-800 text-sm"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z"></path>
                      </svg>
                    </button>
                    <!-- Dropdown Menu -->
                    <div 
                      v-if="dropdownOpen === (campaign.name || campaign.id)"
                      class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10 border border-gray-200"
                    >
                      <div class="py-1">
                        <button 
                          @click="handleEdit(campaign); closeDropdown()"
                          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        >
                          <span class="flex items-center">
                            <span class="mr-2">✏️</span>
                            Chỉnh sửa
                          </span>
                        </button>
                        <button 
                          @click="handleView(campaign); closeDropdown()"
                          class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                        >
                          <span class="flex items-center">
                            <span class="mr-2">👁️</span>
                            Xem chi tiết
                          </span>
                        </button>
                        <div class="border-t border-gray-100"></div>
                        <button 
                          @click="handleDelete(campaign); closeDropdown()"
                          class="block px-4 py-2 text-sm text-red-700 hover:bg-red-50 w-full text-left"
                        >
                          <span class="flex items-center">
                            <span class="mr-2">🗑️</span>
                            Xóa
                          </span>
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

      <!-- No Data State -->
      <div v-else class="text-center py-12">
        <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Không có chiến dịch nào</h3>
        <p class="text-gray-500 mb-4">Bắt đầu tạo chiến dịch tuyển dụng đầu tiên của bạn</p>
        <button 
          @click="$emit('create')"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
        >
          Tạo chiến dịch mới
        </button>
      </div>

      <!-- Pagination -->
      <div v-if="campaigns?.length > 0 && pagination.total > 0" class="flex items-center justify-between mt-6 pt-6 border-t border-gray-200">
        <div class="text-sm text-gray-600">
          Hiển thị {{ pagination.showing_from || 1 }}-{{ pagination.showing_to || campaigns.length }} của {{ pagination.total || campaigns.length }} chiến dịch
        </div>
        <div class="flex space-x-1">
          <button 
            @click="handlePageChange(1)"
            :disabled="pagination.page === 1"
            class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          
          <template v-for="page in getPaginationRange()" :key="page">
            <button
              v-if="page === '...'"
              class="px-3 py-1 text-gray-500"
              disabled
            >
              ...
            </button>
            <button
              v-else
              @click="handlePageChange(page)"
              :class="pagination.page === page ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
              class="px-3 py-1 rounded-md"
            >
              {{ page }}
            </button>
          </template>
          
          <button 
            @click="handlePageChange(pagination.page + 1)"
            :disabled="pagination.page >= pagination.pages"
            class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Dialog } from 'frappe-ui'

// Translation helper function


// Props
const props = defineProps({
  campaigns: {
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
      limit: 10,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
  },
  searchText: {
    type: String,
    default: ''
  },
  statusFilter: {
    type: String,
    default: 'all'
  },
  typeFilter: {
    type: String,
    default: 'all'
  },
  activeFilter: {
    type: String,
    default: 'all'
  },
  refreshTrigger: {
    type: Number,
    default: 0
  }
})

// Emits
const emit = defineEmits([
  'create', 'edit', 'view', 'delete', 'refresh', 
  'update:search-text', 'update:status-filter', 'update:type-filter', 'update:active-filter',
  'page-change', 'items-per-page-change'
])

// Refs
const dropdownOpen = ref(null)

// Methods for UI
const getStatusBadgeClass = (status) => {
  const classes = {
    'DRAFT': 'bg-gray-100 text-gray-800',
    'ACTIVE': 'bg-blue-100 text-blue-800',
    'PAUSED': 'bg-yellow-100 text-yellow-800',
    'ARCHIVED': 'bg-green-100 text-green-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status) => {
  const texts = {
    'DRAFT': 'Draft',
    'ACTIVE': 'Active', 
    'PAUSED': 'Paused',
    'ARCHIVED': 'Archived'
  }
  return texts[status] || status
}

const getProgressBarClass = (status) => {
  const classes = {
    'DRAFT': 'bg-gray-500',
    'ACTIVE': 'bg-blue-500',
    'PAUSED': 'bg-yellow-500',
    'ARCHIVED': 'bg-green-500'
  }
  return classes[status] || 'bg-gray-500'
}

const getProgress = (campaign) => {
  if (!campaign.start_date || !campaign.end_date) {
    // Default progress based on status
    const progressMap = {
      'DRAFT': 10,
      'ACTIVE': 60,
      'PAUSED': 40,
      'ARCHIVED': 100
    }
    return progressMap[campaign.status] || 0
  }
  
  const now = new Date()
  const start = new Date(campaign.start_date)
  const end = new Date(campaign.end_date)
  
  if (now < start) return 0
  if (now > end) return 100
  
  const total = end - start
  const current = now - start
  return Math.round((current / total) * 100)
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    return new Date(dateString).toLocaleDateString('vi-VN')
  } catch {
    return dateString
  }
}

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

const toggleDropdown = (itemId) => {
  dropdownOpen.value = dropdownOpen.value === itemId ? null : itemId
}

const closeDropdown = () => {
  dropdownOpen.value = null
}

const getPaginationRange = () => {
  const totalPages = pagination.value?.pages || 1
  const currentPage = pagination.value?.page || 1
  const range = []
  
  if (totalPages <= 5) {
    for (let i = 1; i <= totalPages; i++) {
      range.push(i)
    }
  } else {
    if (currentPage <= 3) {
      range.push(1, 2, 3, 4, '...', totalPages)
    } else if (currentPage >= totalPages - 2) {
      range.push(1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages)
    } else {
      range.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages)
    }
  }
  
  return range
}

// Event handlers
const handleSearch = (value) => {
  emit('update:search-text', value)
}

const handleFilterChange = (value) => {
  emit('update:status-filter', value)
}

const handleRefresh = () => {
  emit('refresh')
}

const handleEdit = (item) => {
  emit('edit', item)
}

const handleView = (item) => {
  emit('view', item)
}

const handleDelete = (item) => {
  // Using Frappe UI Dialog
  const dialog = new Dialog({
    title: 'Xác nhận xóa',
    message: `Bạn có chắc chắn muốn xóa chiến dịch "${item.campaign_name || item.name}"? Hành động này không thể hoàn tác!`,
    actions: [
      {
        label: 'Hủy bỏ',
        variant: 'ghost'
      },
      {
        label: 'Xóa',
        variant: 'solid',
        theme: 'red',
        onClick: () => {
          emit('delete', item)
          dialog.hide()
        }
      }
    ]
  })
  dialog.show()
}

const handlePageChange = (page) => {
  emit('page-change', page)
}

// Click outside to close dropdown
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.relative')) {
      dropdownOpen.value = null
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
})
</script>

<style scoped>
/* Basic Tailwind CSS styles are handled by classes in template */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
