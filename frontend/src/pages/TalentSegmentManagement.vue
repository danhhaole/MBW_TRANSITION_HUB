<!--
  TalentSegmentManagement.vue
  
  Debug Mode:
  - Enable by adding ?debug=true to URL
  - Or use keyboard shortcut: Ctrl+Shift+D
  - Enables detailed data structure view in segment cards
  - Shows all segment fields, criteria JSON, and raw data
  - Useful for debugging and admin review
-->
<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>

    <!-- Main Content -->
    <div class="container mx-auto px-6 py-6">
      <!-- Actions Bar -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <!-- Search -->
        <div class="relative">
          <input v-model="searchQuery" type="text" placeholder="Search pools..."
            class="w-80 pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            :class="{ 'animate-pulse': isSearching }" @input="handleSearch">
          <svg xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <button v-if="searchQuery" @click="clearSearch"
            class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Create Button -->
        <Button variant="solid" theme="gray" @click="showCreateForm = true" :loading="loading" class="px-6 py-5">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
          </template>
          {{ __('Create Pool') }}
        </Button>
      </div>

      <!-- Loading State -->
      <div v-if="loading && !segments.length" class="flex flex-col items-center justify-center py-12">
        <svg class="animate-spin h-12 w-12 text-blue-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none"
          viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
          </path>
        </svg>
        <div class="text-gray-600">Đang tải dữ liệu...</div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!loading && !segments.length" class="text-center py-16">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 text-gray-300 mx-auto mb-4" fill="none"
          viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1"
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z">
          </path>
        </svg>
        <h3 class="text-xl font-medium text-gray-900 mb-2">Chưa có talent pool nào</h3>
        <p class="text-gray-500 mb-6">Tạo talent pool đầu tiên để bắt đầu quản lý ứng viên</p>
        <Button variant="solid" theme="blue" @click="showCreateForm = true">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
          </template>
          Create Your First Pool
        </Button>
      </div>

      <!-- Segments Grid -->
      <div v-else>
        <!-- Use TalentSegmentCardView Component -->
        <TalentSegmentCardView 
          :segments="paginatedSegments"
          :loading="loading"
          @view-details="handleViewDetails"
          @edit="handleEdit"
          @delete="handleDelete"
          @create="showCreateForm = true"
        />

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-8">
          <div class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6 rounded-lg shadow">
            <div class="flex-1 flex justify-between sm:hidden">
              <Button variant="outline" theme="gray" @click="previousPage" :disabled="pagination.currentPage <= 1">
                Previous
              </Button>
              <Button variant="outline" theme="gray" @click="nextPage" :disabled="pagination.currentPage >= totalPages">
                Next
              </Button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p class="text-sm text-gray-700">
                  Showing
                  <span class="font-medium">{{ (pagination.currentPage - 1) * pagination.pageSize + 1 }}</span>
                  to
                  <span class="font-medium">{{ Math.min(pagination.currentPage * pagination.pageSize, filteredSegments.length) }}</span>
                  of
                  <span class="font-medium">{{ filteredSegments.length }}</span>
                  results
                </p>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md  -space-x-px" aria-label="Pagination">
                  <!-- Previous Button -->
                  <button @click="previousPage" :disabled="pagination.currentPage <= 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>

                  <!-- Page Numbers -->
                  <button v-for="page in visiblePages" :key="page" @click="goToPage(page)" :class="[
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                    page === pagination.currentPage
                      ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                  ]">
                    {{ page }}
                  </button>

                  <!-- Next Button -->
                  <button @click="nextPage" :disabled="pagination.currentPage >= totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clip-rule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Success/Error Toast -->
      <div v-if="toast.show" :class="[
        'fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transform transition-all duration-300',
        toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]">
        <div class="flex items-center">
          <svg v-if="toast.type === 'success'" class="h-5 w-5 mr-2" fill="none" stroke="currentColor"
            viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <svg v-else class="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          <span>{{ toast.message }}</span>
        </div>
      </div>
    </div>

    <!-- Create/Edit Dialog -->
    <Dialog v-model="showCreateForm" :options="createDialogOptions">
      <template #body>
        <div class="bg-white px-4 pb-6 pt-5 sm:px-6">
          <div class="mb-5 flex items-center justify-between">
            <div>
              <h3 class="text-2xl font-semibold leading-6 text-gray-900">
                {{ editingSegment ? 'Edit Talent Pool' : 'Create New Talent Pool' }}
              </h3>
            </div>
            <div class="flex items-center gap-1">
              <Button variant="ghost" class="w-7" @click="handleFormClose">
                <FeatherIcon name="x" class="h-4 w-4" />
              </Button>
            </div>
          </div>
          <div class="max-h-[70vh] overflow-y-auto">
            <TalentSegmentForm :segment="editingSegment" @success="handleFormSuccess" @cancel="handleFormClose" />
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Delete Confirmation Dialog -->
    <Dialog v-model="showDeleteDialog" :options="deleteDialogOptions">
      <template #body>
        <div class="bg-white px-4 pb-6 pt-5 sm:px-6">
          <div class="mb-5 flex items-center justify-between">
            <div>
              <h3 class="text-2xl font-semibold leading-6 text-gray-900">
                Confirm Delete
              </h3>
            </div>
            <div class="flex items-center gap-1">
              <Button variant="ghost" class="w-7" @click="showDeleteDialog = false">
                <FeatherIcon name="x" class="h-4 w-4" />
              </Button>
            </div>
          </div>
          <div>
            <div class="sm:flex sm:items-start">
              <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100 sm:mx-0 sm:h-10 sm:w-10">
                <svg class="h-6 w-6 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                <h3 class="text-lg leading-6 font-medium text-gray-900">Delete Talent Pool</h3>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    Are you sure you want to delete "{{ deletingSegment?.title }}"? This action cannot be undone.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="px-4 pb-7 pt-4 sm:px-6">
          <div class="space-y-2 flex justify-end gap-3">
            <Button variant="outline" theme="gray" @click="showDeleteDialog = false" :disabled="loading">
              Cancel
            </Button>
            <Button variant="solid" theme="red" @click="confirmDelete" :loading="loading">
              Delete
            </Button>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useTalentSegment } from '@/composables/useTalentSegment'
import { Button, Dialog, Dropdown, FeatherIcon } from 'frappe-ui'
import TalentSegmentForm from '@/components/talent-segment/TalentSegmentForm.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { Breadcrumbs } from 'frappe-ui'
import TalentSegmentCardView from '@/components/talent-segment/TalentSegmentCardView.vue'
let title = 'Talent Pools'
const breadcrumbs = [{ label: title, route: { name: 'TalentSegments' } }]

// Composables
const router = useRouter()
const {
  segments,
  selectedSegment,
  loading,
  error,
  success,
  filters,
  isSearching,
  segmentCount,
  loadSegments,
  searchSegments,
  clearSearch: clearSegmentSearch,
  setTypeFilter,
  getSegmentDetails,
  deleteSegment
} = useTalentSegment()

console.log(segments)

// Local state
const currentTab = ref('pools')
const showCreateForm = ref(false)
const showDeleteDialog = ref(false)
const editingSegment = ref(null)
const deletingSegment = ref(null)
const searchQuery = ref('')

// Pagination state
const pagination = ref({
  currentPage: 1,
  itemsPerPage: 9, // 3x3 grid
  total: 0
})

// Toast state
const toast = ref({
  show: false,
  message: '',
  type: 'success'
})

// Navigation tabs
const navigationTabs = [
  { label: 'Dashboard', value: 'dashboard' },
  { label: 'Talent Pools', value: 'pools' },
  { label: 'Candidates', value: 'candidates' },
  { label: 'Campaigns', value: 'campaigns' },
  { label: 'AI Timeline', value: 'ai-timeline' },
  { label: 'Analytics', value: 'analytics' }
]

// Debug mode - can be enabled via query parameter ?debug=true or localStorage
const isDebugMode = computed(() => {
  // Check URL query parameter
  const urlParams = new URLSearchParams(window.location.search)
  if (urlParams.get('debug') === 'true') return true

  // Check localStorage for persistent debug mode
  return localStorage.getItem('talent-segment-debug') === 'true'
})

// Dialog options
const createDialogOptions = computed(() => ({
  title: editingSegment.value ? 'Edit Talent Pool' : 'Create New Talent Pool',
  size: '3xl'
}))

const deleteDialogOptions = computed(() => ({
  title: 'Confirm Delete',
  size: 'sm'
}))

// Pagination computed properties
const totalSegments = computed(() => segments.value.length)
const totalPages = computed(() => Math.ceil(totalSegments.value / pagination.value.itemsPerPage))

const paginatedSegments = computed(() => {
  const start = (pagination.value.currentPage - 1) * pagination.value.itemsPerPage
  const end = start + pagination.value.itemsPerPage
  return segments.value.slice(start, end)
})

const paginationStart = computed(() => {
  return totalSegments.value === 0 ? 0 : (pagination.value.currentPage - 1) * pagination.value.itemsPerPage + 1
})

const paginationEnd = computed(() => {
  const end = pagination.value.currentPage * pagination.value.itemsPerPage
  return Math.min(end, totalSegments.value)
})

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = pagination.value.currentPage
  const delta = 2 // Number of pages to show around current page

  const range = []
  const rangeWithDots = []

  for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
    range.push(i)
  }

  if (current - delta > 2) {
    rangeWithDots.push(1, '...')
  } else {
    rangeWithDots.push(1)
  }

  rangeWithDots.push(...range)

  if (current + delta < total - 1) {
    rangeWithDots.push('...', total)
  } else {
    rangeWithDots.push(total)
  }

  return rangeWithDots.filter((page, index, array) => {
    // Remove duplicates and ensure we don't show 1 twice
    return array.indexOf(page) === index && page !== '...' && page > 0 && page <= total
  })
})

// Pagination methods
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    pagination.value.currentPage = page
  }
}

const nextPage = () => {
  if (pagination.value.currentPage < totalPages.value) {
    pagination.value.currentPage++
  }
}

const previousPage = () => {
  if (pagination.value.currentPage > 1) {
    pagination.value.currentPage--
  }
}

// Search handling
const handleSearch = () => {
  if (searchQuery.value !== filters.searchText) {
    searchSegments(searchQuery.value || '')
    pagination.value.currentPage = 1 // Reset to first page on search
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  clearSegmentSearch()
  pagination.value.currentPage = 1
}

// Utility functions
const formatLastUpdated = (dateStr) => {
  if (!dateStr) return 'Never'
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return '1 day ago'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}

const getDropdownOptions = (segment) => {
  return [
    {
      group: 'Actions',
      items: [
        {
          label: 'Edit',
          icon: () => h(FeatherIcon, { name: "edit", class: "h-4 w-4" }),
          onClick: () => handleEdit(segment)
        },
        {
          label: 'View Details',
          icon: () => h(FeatherIcon, { name: "eye", class: "h-4 w-4" }),
          onClick: () => handleViewDetails(segment)
        },
      ],
    },
    {
      group: 'Danger',
      items: [
        {
          label: 'Delete',
          icon: () => h(FeatherIcon, { name: "trash-2", class: "h-4 w-4" }),
          onClick: () => handleDelete(segment)
        },
      ],
    },
  ]
}

const getGradientClass = (type) => {
  const gradients = {
    'DYNAMIC': 'bg-gradient-to-r from-blue-500 to-indigo-600',
    'MANUAL': 'bg-gradient-to-r from-purple-500 to-pink-500',
    'default': 'bg-gradient-to-r from-green-500 to-teal-500'
  }
  return gradients[type] || gradients.default
}

const getBadgeClass = (type) => {
  const badges = {
    'DYNAMIC': 'bg-blue-100 text-blue-800',
    'MANUAL': 'bg-purple-100 text-purple-800',
    'default': 'bg-green-100 text-green-800'
  }
  return badges[type] || badges.default
}

const getProgressBarClass = (rate) => {
  if (rate >= 70) return 'bg-green-500'
  if (rate >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getAvatarClass = (index) => {
  const colors = [
    'bg-green-500',
    'bg-yellow-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-blue-500'
  ]
  return colors[index % colors.length]
}

const getInitials = (name) => {
  if (!name) return '??'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

// Event handlers
const handleViewDetails = async (segment) => {
  router.push(`/talent-segments/${segment.name}/detail`)
}

const handleEdit = (segment) => {
  editingSegment.value = segment
  showCreateForm.value = true
}

const handleDelete = (segment) => {
  deletingSegment.value = segment
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!deletingSegment.value) return

  const result = await deleteSegment(deletingSegment.value.name)
  if (result) {
    showDeleteDialog.value = false
    deletingSegment.value = null
    showToast('Talent pool đã được xóa thành công', 'success')
  }
}

const handleFormSuccess = async () => {
  showCreateForm.value = false
  editingSegment.value = null
  await loadSegments()
  showToast('Talent pool đã được lưu thành công', 'success')
}

const handleFormClose = () => {
  showCreateForm.value = false
  // Reset editing segment to trigger form reset
  editingSegment.value = null
}

const showToast = (message, type = 'success') => {
  toast.value = {
    show: true,
    message,
    type
  }

  setTimeout(() => {
    toast.value.show = false
  }, 5000)
}

// Keyboard shortcuts
const handleKeyDown = (event) => {
  // Ctrl+Shift+D to toggle debug mode
  if (event.ctrlKey && event.shiftKey && event.key === 'D') {
    event.preventDefault()
    const currentDebug = localStorage.getItem('talent-segment-debug') === 'true'
    localStorage.setItem('talent-segment-debug', !currentDebug ? 'true' : 'false')
    console.log('Debug mode toggled via keyboard:', !currentDebug)
    // Force reactivity update
    window.location.reload()
  }
}

// Watchers
watch(() => filters.searchText, (newValue) => {
  searchQuery.value = newValue
})

watch(() => segments.value.length, () => {
  pagination.value.total = segments.value.length
})

watch(() => [error.value, success.value], ([errorVal, successVal]) => {
  if (errorVal) {
    showToast(errorVal, 'error')
  } else if (successVal) {
    showToast('Thao tác thành công!', 'success')
  }
})

// Reset editingSegment when dialog closes
watch(() => showCreateForm.value, (isOpen) => {
  if (!isOpen) {
    // Reset editing segment when dialog is closed
    editingSegment.value = null
  }
})

// Initialize
onMounted(() => {
  loadSegments()
  // Add keyboard event listener
  document.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  // Remove keyboard event listener
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
/* Custom animation classes */
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-2px);
}

/* Skill badge styling */
.skill-badge {
  background-color: #e0e7ff;
  color: #4338ca;
  border-radius: 9999px;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  display: inline-block;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
}

/* Loading animation */
@keyframes pulse {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: .5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Custom scrollbar */
.overflow-x-auto::-webkit-scrollbar {
  height: 4px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.overflow-x-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>