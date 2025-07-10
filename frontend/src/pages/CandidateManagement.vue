<template>
  <div class="candidate-management-page container mx-auto w-full min-h-screen pt-10 bg-gray-50">
    <!-- Header Section -->
    <div class="bg-white rounded-lg border border-gray-200 p-6 mb-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-blue-600 mb-2 flex items-center">
            <svg class="w-8 h-8 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
            </svg>
            Quản lý ứng viên
          </h1>
          <p class="text-gray-600 mb-0">
            Quản lý và theo dõi thông tin ứng viên trong hệ thống
          </p>
        </div>
        
        <div class="flex items-center">
          <button
            @click="openCreateModal"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
            Thêm ứng viên
          </button>
        </div>
      </div>
    </div>


    <!-- Filters and Controls -->
    <div class="bg-white rounded-lg border border-gray-200 mb-6">
      <div class="p-4">
        <div class="grid grid-cols-1 md:grid-cols-6 gap-4 items-center">
          <!-- Search -->
          <div class="md:col-span-2">
            <FormControl
              v-model="filters.search"
              type="text"
              placeholder="Tìm kiếm ứng viên..."
              :prefix-icon="'search'"
              @input="debouncedSearch"
            />
          </div>
          
          <!-- Status Filter -->
          <div>
            <FormControl
              v-model="filters.status"
              type="select"
              
              :options="statusFilterOptions"
              @change="updateStatus(filters.status)"
            />
          </div>
          
          <!-- Source Filter -->
          <div>
            <FormControl
              v-model="filters.source"
              type="select"
              
              :options="sourceFilterOptions"
              @change="updateSource(filters.source)"
            />
          </div>
          
          <!-- Skills Filter -->
          <!-- <div>
            <FormControl
              v-model="filters.skills"
              type="autocomplete"
              placeholder="Chọn kỹ năng..."
              :options="skillFilterOptions"
              multiple
              :allow-custom="true"
              @change="updateSkills(filters.skills)"
            />
          </div> -->
          
          <!-- Clear Filters -->
          <div class="flex justify-end">
            <button
              v-if="hasFilters"
              @click="clearFilters"
              class="text-sm text-red-600 hover:text-red-800 font-medium px-3 py-2 rounded-lg hover:bg-red-50 transition-colors duration-200"
            >
              Xóa bộ lọc
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && candidates.length === 0" class="text-center py-12">
      <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-4">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
      <p class="text-gray-600">
        Đang tải danh sách ứng viên...
      </p>
    </div>

    <!-- Content Views -->
    <div v-else>
      <!-- Card View -->
      <CandidateCardView
        :candidates="candidates"
        :loading="loading"
        :has-filters="hasFilters"
        @view-candidate="openViewModal"
        @edit-candidate="openEditModal"
        @delete-candidate="handleDeleteCandidate"
        @duplicate-candidate="handleDuplicateCandidate"
        @create-candidate="openCreateModal"
        @clear-filters="clearFilters"
      />

      <!-- Pagination -->
      <div
        v-if="pagination.total > 0"
        class="bg-white rounded-lg border border-gray-200 p-4 mt-6 flex items-center justify-between"
      >
        <!-- Items per page selector -->
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-700">Số items mỗi trang:</span>
          <div class="w-20">
            <FormControl
              :model-value="pagination.limit"
              type="select"
              :options="itemsPerPageOptions"
              @change="changeItemsPerPage"
            />
          </div>
        </div>

        <!-- Page info -->
        <div class="text-sm text-gray-600">
          Hiển thị {{ pagination.showing_from }} đến {{ pagination.showing_to }} 
          trong tổng số {{ pagination.total }} ứng viên
        </div>

        <!-- Page navigation -->
        <div class="flex items-center space-x-1">
          <button
            :disabled="!pagination.has_prev"
            @click="goToPage(1)"
            class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>
            </svg>
          </button>
          
          <button
            :disabled="!pagination.has_prev"
            @click="goToPage(pagination.page - 1)"
            class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>

          <span class="mx-3 text-sm text-gray-700">
            Trang {{ pagination.page }} / {{ pagination.pages }}
          </span>

          <button
            :disabled="!pagination.has_next"
            @click="goToPage(pagination.page + 1)"
            class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </button>
          
          <button
            :disabled="!pagination.has_next"
            @click="goToPage(pagination.pages)"
            class="p-2 text-gray-500 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- View Modal -->
    <CandidateViewModal
      v-model="viewModal.show"
      :candidate="viewModal.candidate"
      :loading="viewModal.loading"
      :error="viewModal.error"
      @edit-candidate="openEditModal"
      @delete-candidate="handleDeleteCandidate"
      @duplicate-candidate="handleDuplicateCandidate"
    />

    <!-- Edit Modal -->
    <CandidateEditModal
      v-model="editModal.show"
      :candidate="editModal.candidate"
      :loading="editModal.loading"
      :saving="editModal.saving"
      :filter-options="filterOptions || {}"
      @save-candidate="handleSaveCandidate"
      @cancel="editModal.show = false"
    />

    <!-- Delete Confirmation Dialog -->
    <div
      v-if="deleteDialog.show"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50 flex items-center justify-center"
    >
      <div class="bg-white rounded-lg max-w-md w-full mx-4">
        <div class="p-6">
          <div class="flex items-center mb-4">
            <div class="flex-shrink-0">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-lg font-medium text-gray-900">Xác nhận xóa</h3>
            </div>
          </div>
          
          <div class="mb-4">
            <p class="text-sm text-gray-500 mb-3">
              Bạn có chắc chắn muốn xóa ứng viên này không?
            </p>
            <div class="bg-gray-50 p-3 rounded-lg">
              <div class="font-medium text-gray-900">{{ deleteDialog.candidate?.full_name }}</div>
              <div class="text-sm text-gray-500">{{ deleteDialog.candidate?.email }}</div>
            </div>
            <p class="text-xs text-red-600 mt-2">
              Hành động này không thể hoàn tác.
            </p>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button
              @click="deleteDialog.show = false"
              :disabled="deleteDialog.loading"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              Hủy
            </button>
            <button
              @click="confirmDelete"
              :disabled="deleteDialog.loading"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 flex items-center"
            >
              <span v-if="deleteDialog.loading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
              Xóa
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast notifications handled by ToastContainer -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCandidate } from '@/composables/useCandidate'
import { useToast } from '@/composables/useToast'
import { FormControl } from 'frappe-ui'
import {
  CandidateCardView,
  CandidateViewModal,
  CandidateEditModal
} from '@/components/candidate'

// Router
const router = useRouter()

// Composables
const {
  candidates,
  loading,
  error,
  pagination,
  filters,
  filterOptions,
  stats,
  hasData,
  isEmpty,
  
  fetchCandidates,
  getCandidate,
  createCandidate,
  updateCandidate,
  deleteCandidate,
  
  goToPage,
  changeItemsPerPage,
  updateSearch,
  updateStatus,
  updateSource,
  updateSkills,
  clearFilters,
  
  initialize
} = useCandidate()

const { showToast, showSuccess, showError } = useToast()

// Debug logs removed

// Local state (removed currentView since we only have card view)

// Modal states
const viewModal = ref({
  show: false,
  candidate: null,
  loading: false,
  error: null
})

const editModal = ref({
  show: false,
  candidate: null,
  loading: false,
  saving: false
})

const deleteDialog = ref({
  show: false,
  candidate: null,
  loading: false
})

// Removed snackbar state - using useToast instead

// Computed
const hasCandidates = computed(() => hasData.value)
const hasFilters = computed(() => {
  return filters.search || 
         filters.status || 
         filters.source || 
         (filters.skills && filters.skills.length > 0)
})

const statusFilterOptions = computed(() => [
  { label: 'Tất cả trạng thái', value: '' },
  { label: 'Mới', value: 'NEW' },
  { label: 'Đã tìm thấy', value: 'SOURCED' },
  { label: 'Đang chăm sóc', value: 'NURTURING' },
  { label: 'Đã tương tác', value: 'ENGAGED' },
  { label: 'Đã lưu trữ', value: 'ARCHIVED' }
])

const sourceFilterOptions = computed(() => {
  const defaultOptions = [
    { label: 'Tất cả nguồn', value: '' },
    { label: 'Thủ công', value: 'MANUAL' },
    { label: 'LinkedIn', value: 'LINKEDIN' },
    { label: 'Website', value: 'WEBSITE' },
    { label: 'Giới thiệu', value: 'REFERRAL' },
    { label: 'Job Board', value: 'JOB_BOARD' }
  ]
  
  try {
    if (!filterOptions.value || typeof filterOptions.value !== 'object') {
      return defaultOptions
    }
    
    const apiOptions = filterOptions.value.source || []
    if (Array.isArray(apiOptions)) {
      return [...defaultOptions, ...apiOptions]
    }
    return defaultOptions
  } catch (err) {
    console.error('Error in sourceFilterOptions:', err)
    return defaultOptions
  }
})

const skillFilterOptions = computed(() => {
  return [
    // Programming Languages
    { label: 'JavaScript', value: 'javascript' },
    { label: 'TypeScript', value: 'typescript' },
    { label: 'Python', value: 'python' },
    { label: 'Java', value: 'java' },
    { label: 'C#', value: 'csharp' },
    { label: 'C++', value: 'cpp' },
    { label: 'PHP', value: 'php' },
    { label: 'Go', value: 'go' },
    { label: 'Rust', value: 'rust' },
    { label: 'Ruby', value: 'ruby' },
    { label: 'Swift', value: 'swift' },
    { label: 'Kotlin', value: 'kotlin' },
    
    // Frontend Frameworks
    { label: 'React', value: 'react' },
    { label: 'Vue.js', value: 'vuejs' },
    { label: 'Angular', value: 'angular' },
    { label: 'Next.js', value: 'nextjs' },
    { label: 'Nuxt.js', value: 'nuxtjs' },
    { label: 'Svelte', value: 'svelte' },
    
    // Backend Frameworks
    { label: 'Node.js', value: 'nodejs' },
    { label: 'Express.js', value: 'expressjs' },
    { label: 'Django', value: 'django' },
    { label: 'Flask', value: 'flask' },
    { label: 'Spring Boot', value: 'springboot' },
    { label: 'Laravel', value: 'laravel' },
    { label: 'ASP.NET', value: 'aspnet' },
    { label: 'FastAPI', value: 'fastapi' },
    
    // Databases
    { label: 'MySQL', value: 'mysql' },
    { label: 'PostgreSQL', value: 'postgresql' },
    { label: 'MongoDB', value: 'mongodb' },
    { label: 'Redis', value: 'redis' },
    { label: 'SQLite', value: 'sqlite' },
    { label: 'Oracle', value: 'oracle' },
    { label: 'SQL Server', value: 'sqlserver' },
    
    // Cloud & DevOps
    { label: 'AWS', value: 'aws' },
    { label: 'Azure', value: 'azure' },
    { label: 'Google Cloud', value: 'gcp' },
    { label: 'Docker', value: 'docker' },
    { label: 'Kubernetes', value: 'kubernetes' },
    { label: 'Jenkins', value: 'jenkins' },
    { label: 'CI/CD', value: 'cicd' },
    { label: 'Terraform', value: 'terraform' },
    
    // Tools & Technologies
    { label: 'Git', value: 'git' },
    { label: 'Linux', value: 'linux' },
    { label: 'Agile', value: 'agile' },
    { label: 'Scrum', value: 'scrum' },
    { label: 'REST API', value: 'restapi' },
    { label: 'GraphQL', value: 'graphql' },
    { label: 'Microservices', value: 'microservices' },
    { label: 'Machine Learning', value: 'ml' },
    { label: 'Data Science', value: 'datascience' },
    { label: 'AI', value: 'ai' },
  ]
})

const itemsPerPageOptions = [
  { label: '12', value: 12 },
  { label: '24', value: 24 },
  { label: '36', value: 36 },
  { label: '48', value: 48 }
]

// Methods - removed showSnackbar, using useToast instead

const openCreateModal = () => {
  editModal.value = {
    show: true,
    candidate: null,
    loading: false,
    saving: false
  }
}

const openViewModal = (candidate) => {
  // Navigate to candidate detail view instead of opening modal
  router.push(`/candidates/${candidate.name}`)
}

const openEditModal = (candidate) => {
  editModal.value = {
    show: true,
    candidate: candidate,
    loading: false,
    saving: false
  }
}

const handleDeleteCandidate = (candidate) => {
  deleteDialog.value = {
    show: true,
    candidate: candidate,
    loading: false
  }
}

// Prevent double delete
let isDeleting = false

const confirmDelete = async () => {
  // Prevent double delete
  if (isDeleting) {
    console.log('Already deleting, ignoring duplicate call')
    return
  }
  
  try {
    isDeleting = true
    deleteDialog.value.loading = true
    await deleteCandidate(deleteDialog.value.candidate.name)
    
    deleteDialog.value.show = false
    viewModal.value.show = false
    
    showSuccess('Ứng viên đã được xóa thành công')
  } catch (err) {
    showError(`Lỗi khi xóa ứng viên: ${err.message}`)
  } finally {
    deleteDialog.value.loading = false
    isDeleting = false
  }
}

// Prevent double save
let isSaving = false

const handleSaveCandidate = async (candidateData) => {
  console.log('handleSaveCandidate called with:', candidateData)
  
  // Prevent double save
  if (isSaving) {
    console.log('Already saving, ignoring duplicate call')
    return
  }
  
  try {
    isSaving = true
    editModal.value.saving = true
    console.log('Setting saving to true')
    console.log(editModal.value.candidate)  
    
    if (editModal.value.candidate) {
      // Update existing candidate
      console.log('Updating candidate:', editModal.value.candidate.name)
      await updateCandidate(editModal.value.candidate.name, candidateData)
      showSuccess('Ứng viên đã được cập nhật thành công')
    } else {
      // Create new candidate
      console.log('Creating new candidate')
      await createCandidate(candidateData)
      showSuccess('Ứng viên mới đã được tạo thành công')
    }
    
    console.log('Closing modal')
    editModal.value.show = false
  } catch (err) {
    console.error('Error in handleSaveCandidate:', err)
    showError(`Lỗi khi lưu ứng viên: ${err.message}`)
  } finally {
    console.log('Setting saving to false')
    editModal.value.saving = false
    isSaving = false
  }
}

const handleDuplicateCandidate = (candidate) => {
  // Create a copy without the unique fields
  const duplicateData = {
    ...candidate,
    full_name: `${candidate.full_name} (Bản sao)`,
    email: `copy_${Date.now()}_${candidate.email}`,
    name: undefined // Let system generate new name
  }
  
  editModal.value = {
    show: true,
    candidate: duplicateData,
    loading: false,
    saving: false
  }
}

// Removed export function since we don't have table view

// Debounced search
let searchTimeout = null
const debouncedSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  searchTimeout = setTimeout(() => {
    updateSearch(filters.search)
  }, 500)
}

// Removed view watching since we only have card view

// Initialize on mount
onMounted(async () => {
  try {
    await initialize()
  } catch (err) {
    showError(`Lỗi khi tải dữ liệu: ${err.message}`)
  }
})
</script>

<style scoped>


/* Custom scrollbar */
.candidate-management-page ::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.candidate-management-page ::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.candidate-management-page ::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

.candidate-management-page ::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Smooth transitions */
.candidate-management-page button {
  transition: all 0.2s ease-in-out;
}

.candidate-management-page input,
.candidate-management-page select {
  transition: all 0.2s ease-in-out;
}

/* Loading animation */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style> 