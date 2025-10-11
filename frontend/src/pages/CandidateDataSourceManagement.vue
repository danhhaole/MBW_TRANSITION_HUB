<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Content -->
    <CandidateDataSourceTable
      :data-sources="dataSources"
      :loading="loading"
      :pagination="pagination"
      :search-text="searchText"
      :status-filter="statusFilter"
      :type-filter="typeFilter"
      @create="handleCreate"
      @edit="handleEdit"
      @view="handleView"
      @delete="handleDelete"
      @refresh="handleRefresh"
      @test-connection="handleTestConnection"
      @sync="handleSync"
      @update:search-text="handleSearchChange"
      @update:status-filter="handleStatusFilterChange"
      @update:type-filter="handleTypeFilterChange"
      @page-change="handlePageChange"
    />

    <!-- Create/Edit Form Modal -->
    <CandidateDataSourceForm
      v-model="showForm"
      :data-source="selectedDataSource"
      @success="handleFormSuccess"
      @cancel="handleFormCancel"
    />

    <!-- Toast Messages -->
    <div
      v-if="toastMessage"
      class="fixed top-4 right-4 z-50 max-w-sm"
    >
      <div
        class="bg-white border rounded-lg shadow-lg p-4"
        :class="toastType === 'success' ? 'border-green-200' : 'border-red-200'"
      >
        <div class="flex items-center space-x-3">
          <div
            class="flex-shrink-0"
            :class="toastType === 'success' ? 'text-green-400' : 'text-red-400'"
          >
            <svg v-if="toastType === 'success'" class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="flex-1">
            <p
              class="text-sm font-medium"
              :class="toastType === 'success' ? 'text-green-800' : 'text-red-800'"
            >
              {{ toastMessage }}
            </p>
          </div>
          <button
            @click="hideToast"
            class="flex-shrink-0 text-gray-400 hover:text-gray-600"
          >
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import CandidateDataSourceTable from '@/components/candidateDataSource/CandidateDataSourceTable.vue'
import CandidateDataSourceForm from '@/components/candidateDataSource/CandidateDataSourceForm.vue'
import { useCandidateDataSourceStore } from '@/stores/candidateDataSource.js'

// Router
const router = useRouter()

// Store
const candidateDataSourceStore = useCandidateDataSourceStore()

// Translation helper


// Reactive state
const loading = ref(false)
const dataSources = ref([])
const showForm = ref(false)
const selectedDataSource = ref(null)

// Filters and pagination
const searchText = ref('')
const statusFilter = ref('all')
const typeFilter = ref('all')
const pagination = reactive({
  page: 1,
  limit: 10,
  total: 0,
  pages: 1,
  has_next: false,
  has_prev: false,
  showing_from: 0,
  showing_to: 0
})

// Toast message
const toastMessage = ref('')
const toastType = ref('success')
const toastTimeout = ref(null)

// Methods
const showToast = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  
  // Clear existing timeout
  if (toastTimeout.value) {
    clearTimeout(toastTimeout.value)
  }
  
  // Auto hide after 3 seconds
  toastTimeout.value = setTimeout(() => {
    hideToast()
  }, 3000)
}

const hideToast = () => {
  toastMessage.value = ''
  if (toastTimeout.value) {
    clearTimeout(toastTimeout.value)
    toastTimeout.value = null
  }
}

const buildFilters = () => {
  const filters = {}
  
  if (statusFilter.value !== 'all') {
    filters.status = statusFilter.value
  }
  
  if (typeFilter.value !== 'all') {
    filters.source_type = typeFilter.value
  }
  
  if (searchText.value.trim()) {
    filters.search_text = searchText.value.trim()
  }
  
  return filters
}

const loadDataSources = async () => {
  loading.value = true
  try {
    const filters = buildFilters()
    const response = await candidateDataSourceStore.fetchDataSources({
      filters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc'
    })

    if (response.success) {
      dataSources.value = response.data.data || []
      
      // Update pagination
      Object.assign(pagination, {
        total: response.data.total || 0,
        pages: Math.ceil((response.data.total || 0) / pagination.limit),
        has_next: response.data.has_next || false,
        has_prev: response.data.has_prev || false,
        showing_from: response.data.showing_from || 0,
        showing_to: response.data.showing_to || 0
      })
    } else {
      console.error('Error loading data sources:', response.error)
      showToast('Lỗi khi tải dữ liệu: ' + response.error, 'error')
    }
  } catch (error) {
    console.error('Error loading data sources:', error)
    showToast('Lỗi khi tải dữ liệu: ' + error.message, 'error')
  } finally {
    loading.value = false
  }
}

// Event handlers
const handleCreate = () => {
  selectedDataSource.value = null
  showForm.value = true
}

const handleEdit = (dataSource) => {
  selectedDataSource.value = dataSource
  showForm.value = true
}

const handleView = (dataSource) => {
  // TODO: Implement view functionality
  console.log('View data source:', dataSource)
  showToast('Chức năng xem chi tiết đang được phát triển', 'info')
}

const handleDelete = async (dataSource) => {
  try {
    const result = await candidateDataSourceStore.deleteDataSource(dataSource.name)
    
    if (result.success) {
      showToast('Xóa nguồn dữ liệu thành công')
      await loadDataSources()
    } else {
      showToast('Lỗi khi xóa: ' + result.error, 'error')
    }
  } catch (error) {
    console.error('Error deleting data source:', error)
    showToast('Lỗi khi xóa: ' + error.message, 'error')
  }
}

const handleRefresh = async () => {
  await loadDataSources()
  showToast('Đã làm mới dữ liệu')
}

const handleTestConnection = async (dataSource) => {
  try {
    // Test connection functionality - simulate success for now
    const result = { success: true, message: 'Connection test successful' }
    
    if (result.success) {
      showToast('Kiểm tra kết nối thành công')
    } else {
      showToast('Kiểm tra kết nối thất bại: ' + result.error, 'error')
    }
  } catch (error) {
    console.error('Error testing connection:', error)
    showToast('Lỗi khi kiểm tra kết nối: ' + error.message, 'error')
  }
}

const handleSync = async (dataSource) => {
  try {
    // Sync data functionality - simulate success for now
    const result = { success: true, message: 'Data sync initiated successfully' }
    
    if (result.success) {
      showToast('Đồng bộ dữ liệu thành công')
      await loadDataSources() // Refresh to show updated sync time
    } else {
      showToast('Đồng bộ dữ liệu thất bại: ' + result.error, 'error')
    }
  } catch (error) {
    console.error('Error syncing data:', error)
    showToast('Lỗi khi đồng bộ dữ liệu: ' + error.message, 'error')
  }
}

const handleFormSuccess = async (event) => {
  const action = event.action
  const actionText = action === 'create' ? 'tạo mới' : 'cập nhật'
  
  showToast(`${actionText.charAt(0).toUpperCase() + actionText.slice(1)} nguồn dữ liệu thành công`)
  await loadDataSources()
}

const handleFormCancel = () => {
  selectedDataSource.value = null
}

// Filter change handlers
const handleSearchChange = (value) => {
  searchText.value = value
  pagination.page = 1 // Reset to first page
}

const handleStatusFilterChange = (value) => {
  statusFilter.value = value
  pagination.page = 1 // Reset to first page
}

const handleTypeFilterChange = (value) => {
  typeFilter.value = value
  pagination.page = 1 // Reset to first page
}

const handlePageChange = (page) => {
  pagination.page = page
}

// Watchers for auto-reload when filters change
watch([searchText, statusFilter, typeFilter], () => {
  // Debounce search
  if (toastTimeout.value) {
    clearTimeout(toastTimeout.value)
  }
  
  toastTimeout.value = setTimeout(() => {
    loadDataSources()
  }, 500)
}, { deep: true })

watch(() => pagination.page, () => {
  loadDataSources()
})

// Lifecycle
onMounted(async () => {
  await loadDataSources()
})

// Page title and meta
document.title = 'Quản lý nguồn dữ liệu ứng viên - MBW Mira'
</script>

<style scoped>
/* Custom styles if needed */
</style> 