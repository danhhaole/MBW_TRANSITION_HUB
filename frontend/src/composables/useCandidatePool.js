import { ref, reactive, computed, watch } from 'vue'
import candidatePoolService from '@/services/candidatePoolService'

/**
 * Composable for CandidatePool - READ ONLY
 * Quản lý state và cung cấp các chức năng chỉ xem cho CandidatePool
 */

// Simple debounce function
function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

export function useCandidatePool() {
  // State
  const candidatePools = ref([])
  const loading = ref(false)
  const error = ref(null)
  const stats = ref({})
  const filterOptions = ref({})

  // Filters
  const filters = reactive({
    search: '',
    status: '',
  })

  // Pagination
  const pagination = reactive({
    page: 1,
    limit: 12,
    total: 0,
    pages: 0,
    has_next: false,
    has_prev: false,
    showing_from: 0,
    showing_to: 0
  })

  // Computed
  const hasData = computed(() => candidatePools.value.length > 0)
  const isEmpty = computed(() => !loading.value && candidatePools.value.length === 0)
  const hasFilters = computed(() => {
    return filters.search || filters.status
  })

  // Methods
  const fetchCandidatePools = async (params = {}) => {
    loading.value = true
    error.value = null

    try {
      const queryParams = {
        page: pagination.page,
        limit: pagination.limit,
        search: filters.search,
        status: filters.status,
        order_by: "modified desc",
        ...params
      }

      const response = await candidatePoolService.getCandidatePoolsWithDetails(queryParams)

      if (response.success) {
        candidatePools.value = response.candidate_pools || []
        
        if (response.pagination) {
          Object.assign(pagination, response.pagination)
        }
      } else {
        error.value = response.error || 'Có lỗi xảy ra khi tải dữ liệu'
        candidatePools.value = []
      }
    } catch (err) {
      error.value = err.message || 'Có lỗi xảy ra khi tải dữ liệu'
      candidatePools.value = []
      console.error('Error fetching candidate pools:', err)
    } finally {
      loading.value = false
    }
  }

  const getCandidatePool = async (name) => {
    loading.value = true
    error.value = null

    try {
      const response = await candidatePoolService.getCandidatePoolDetail(name)
      
      if (response.success) {
        return response.candidate_pool
      } else {
        error.value = response.error || 'Không tìm thấy candidate pool'
        return null
      }
    } catch (err) {
      error.value = err.message || 'Có lỗi xảy ra khi tải chi tiết'
      console.error('Error fetching candidate pool:', err)
      return null
    } finally {
      loading.value = false
    }
  }

  const fetchStats = async () => {
    try {
      const response = await candidatePoolService.getCandidatePoolStatistics()
      
      if (response.success) {
        stats.value = response.stats || {}
      } else {
        console.error('Error fetching stats:', response.error)
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const fetchFilterOptions = async () => {
    try {
      const response = await candidatePoolService.getCandidatePoolFilterOptions()
      
      if (response.success) {
        filterOptions.value = response.filter_options || {}
      } else {
        console.error('Error fetching filter options:', response.error)
      }
    } catch (err) {
      console.error('Error fetching filter options:', err)
    }
  }

  const searchCandidatePools = async (query = '', limit = 10) => {
    try {
      const response = await candidatePoolService.searchCandidatePoolsWithDetails(query, limit)
      
      if (response.success) {
        return response.candidate_pools || []
      } else {
        console.error('Error searching candidate pools:', response.error)
        return []
      }
    } catch (err) {
      console.error('Error searching candidate pools:', err)
      return []
    }
  }

  // Pagination methods
  const goToPage = (page) => {
    if (page >= 1 && page <= pagination.pages) {
      pagination.page = page
      fetchCandidatePools()
    }
  }

  const changeItemsPerPage = (newLimit) => {
    pagination.limit = newLimit
    pagination.page = 1
    fetchCandidatePools()
  }

  // Filter methods
  const updateSearch = debounce((searchText) => {
    filters.search = searchText
    pagination.page = 1
    fetchCandidatePools()
  }, 500)

  const updateStatus = (status) => {
    filters.status = status
    pagination.page = 1
    fetchCandidatePools()
  }

  const clearFilters = () => {
    filters.search = ''
    filters.status = ''
    pagination.page = 1
    fetchCandidatePools()
  }

  // Initialize data
  const initialize = async () => {
    await Promise.all([
      fetchCandidatePools(),
      fetchStats(),
      fetchFilterOptions()
    ])
  }

  return {
    // State
    candidatePools,
    loading,
    error,
    pagination,
    filters,
    stats,
    filterOptions,

    // Computed
    hasData,
    isEmpty,
    hasFilters,

    // Methods
    fetchCandidatePools,
    getCandidatePool,
    fetchStats,
    fetchFilterOptions,
    searchCandidatePools,

    // Pagination
    goToPage,
    changeItemsPerPage,

    // Filters
    updateSearch,
    updateStatus,
    clearFilters,

    // Initialize
    initialize,
  }
}

export default useCandidatePool 