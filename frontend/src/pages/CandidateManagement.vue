<template>
  <div class="candidate-management-page">
    <!-- Header Section -->
    <div class="page-header bg-white pa-6 mb-6 elevation-1">
      <div class="d-flex align-center justify-space-between">
        <div>
          <h1 class="text-h4 font-weight-bold text-primary mb-2">
            <v-icon class="mr-3" size="36">mdi-account-group</v-icon>
            Quản lý ứng viên
          </h1>
          <p class="text-body-1 text-medium-emphasis mb-0">
            Quản lý và theo dõi thông tin ứng viên trong hệ thống
          </p>
        </div>
        
        <div class="d-flex align-center">
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-plus"
            size="large"
            @click="openCreateModal"
          >
            Thêm ứng viên
          </v-btn>
        </div>
      </div>
    </div>


    <!-- Filters and Controls -->
    <v-card class="mb-6" variant="default">
      <v-card-text class="pa-4">
        <v-row align="center">
          <!-- Search -->
          <v-col cols="12" md="4">
            <v-text-field
              v-model="filters.search"
              label="Tìm kiếm ứng viên"
              variant="outlined"
              density="compact"
              prepend-inner-icon="mdi-magnify"
              clearable
              hide-details
              @input="debouncedSearch"
            />
          </v-col>
          
          <!-- Status Filter -->
          <v-col cols="12" md="2" sm="6">
            <v-select
              v-model="filters.status"
              label="Trạng thái"
              variant="outlined"
              density="compact"
              :items="statusFilterOptions"
              item-title="label"
              item-value="value"
              clearable
              hide-details
              @update:model-value="updateStatus"
            />
          </v-col>
          
          <!-- Source Filter -->
          <v-col cols="12" md="2" sm="6">
            <v-select
              v-model="filters.source"
              label="Nguồn"
              variant="outlined"
              density="compact"
              :items="sourceFilterOptions"
              item-title="label"
              item-value="value"
              clearable
              hide-details
              @update:model-value="updateSource"
            />
          </v-col>
          
          <!-- Skills Filter -->
          <v-col cols="12" md="2" sm="6">
            <v-select
              v-model="filters.skills"
              label="Kỹ năng"
              variant="outlined"
              density="compact"
              :items="skillFilterOptions"
              item-title="label"
              item-value="value"
              multiple
              clearable
              hide-details
              @update:model-value="updateSkills"
            />
          </v-col>
          
          <!-- Clear Filters -->
          <v-col cols="12" md="2" sm="6" class="d-flex justify-end">
            <v-btn
              v-if="hasFilters"
              variant="text"
              color="error"
              size="small"
              @click="clearFilters"
            >
              Xóa bộ lọc
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- Loading State -->
    <div v-if="loading && candidates.length === 0" class="text-center pa-8">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      />
      <p class="text-body-1 text-medium-emphasis mt-4">
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
      <v-card
        v-if="pagination.total > 0"
        class="d-flex align-center justify-space-between pa-4 mt-4"
        variant="default"
      >
        <!-- Items per page selector -->
        <div class="d-flex align-center">
          <span class="text-body-2 mr-2">Số items mỗi trang:</span>
          <v-select
            :model-value="pagination.limit"
            :items="itemsPerPageOptions"
            @update:model-value="changeItemsPerPage"
            density="compact"
            variant="outlined"
            hide-details
            style="width: 80px;"
          />
        </div>

        <!-- Page info -->
        <div class="text-body-2 text-medium-emphasis">
          Hiển thị {{ pagination.showing_from }} đến {{ pagination.showing_to }} 
          trong tổng số {{ pagination.total }} ứng viên
        </div>

        <!-- Page navigation -->
        <div class="d-flex align-center">
          <v-btn
            :disabled="!pagination.has_prev"
            variant="text"
            size="small"
            @click="goToPage(1)"
          >
            <v-icon>mdi-page-first</v-icon>
          </v-btn>
          
          <v-btn
            :disabled="!pagination.has_prev"
            variant="text"
            size="small"
            @click="goToPage(pagination.page - 1)"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>

          <span class="mx-3 text-body-2">
            Trang {{ pagination.page }} / {{ pagination.pages }}
          </span>

          <v-btn
            :disabled="!pagination.has_next"
            variant="text"
            size="small"
            @click="goToPage(pagination.page + 1)"
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
          
          <v-btn
            :disabled="!pagination.has_next"
            variant="text"
            size="small"
            @click="goToPage(pagination.pages)"
          >
            <v-icon>mdi-page-last</v-icon>
          </v-btn>
        </div>
      </v-card>
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
    <v-dialog
      v-model="deleteDialog.show"
      max-width="500px"
      persistent
    >
      <v-card>
        <v-card-title class="text-h5 text-error">
          <v-icon class="mr-2">mdi-delete-alert</v-icon>
          Xác nhận xóa
        </v-card-title>
        
        <v-card-text>
          <p class="mb-2">
            Bạn có chắc chắn muốn xóa ứng viên này không?
          </p>
          <div class="bg-grey-lighten-4 pa-3 rounded">
            <strong>{{ deleteDialog.candidate?.full_name }}</strong><br>
            {{ deleteDialog.candidate?.email }}
          </div>
          <p class="text-caption text-error mt-2 mb-0">
            Hành động này không thể hoàn tác.
          </p>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer />
          <v-btn
            variant="outlined"
            @click="deleteDialog.show = false"
            :disabled="deleteDialog.loading"
          >
            Hủy
          </v-btn>
          <v-btn
            color="error"
            variant="flat"
            @click="confirmDelete"
            :loading="deleteDialog.loading"
          >
            Xóa
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Toast notifications handled by ToastContainer -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCandidate } from '@/composables/useCandidate'
import { useToast } from '@/composables/useToast'
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
  { label: 'Tất cả', value: '' },
  { label: 'Mới', value: 'NEW' },
  { label: 'Đã tìm thấy', value: 'SOURCED' },
  { label: 'Đang chăm sóc', value: 'NURTURING' },
  { label: 'Đã tương tác', value: 'ENGAGED' },
  { label: 'Đã lưu trữ', value: 'ARCHIVED' }
])

const sourceFilterOptions = computed(() => {
  const defaultOptions = [
    { label: 'Tất cả', value: '' },
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
  try {
    if (!filterOptions.value || typeof filterOptions.value !== 'object') {
      return []
    }
    
    const skills = filterOptions.value.skills || []
    return Array.isArray(skills) ? skills : []
  } catch (err) {
    console.error('Error in skillFilterOptions:', err)
    return []
  }
})

const itemsPerPageOptions = [
  { title: '12', value: 12 },
  { title: '24', value: 24 },
  { title: '36', value: 36 },
  { title: '48', value: 48 }
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
.candidate-management-page {
  min-height: 100vh;
  background-color: rgb(var(--v-theme-background));
}

.page-header {
  border-radius: 12px;
  border: 1px solid rgb(var(--v-theme-outline-variant));
}

.stats-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-radius: 12px;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
}

/* Custom scrollbar */
:deep(.v-data-table__wrapper) {
  scrollbar-width: thin;
}

:deep(.v-data-table__wrapper::-webkit-scrollbar) {
  height: 8px;
}

:deep(.v-data-table__wrapper::-webkit-scrollbar-track) {
  background: rgb(var(--v-theme-surface-variant));
}

:deep(.v-data-table__wrapper::-webkit-scrollbar-thumb) {
  background: rgb(var(--v-theme-outline-variant));
  border-radius: 4px;
}
</style> 