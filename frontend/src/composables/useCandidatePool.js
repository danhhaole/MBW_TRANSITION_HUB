import { ref, reactive, computed, watch } from 'vue'
import { useCandidatePoolStore } from '@/stores/candidatePool.js'

/**
 * Composable for Mira Talent - READ ONLY
 * Quản lý state và cung cấp các chức năng chỉ xem cho Mira Talent
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
  // Store
  const candidatePoolStore = useCandidatePoolStore()
  
  // State (using store state)
  const candidatePools = computed(() => candidatePoolStore.candidatePools)
  const loading = computed(() => candidatePoolStore.loading)
  const error = computed(() => candidatePoolStore.error)
  const stats = computed(() => candidatePoolStore.statistics)
  const filterOptions = computed(() => candidatePoolStore.filterOptions)

  // Filters (using store state)
  const filters = reactive({
    search: candidatePoolStore.searchText,
    status: candidatePoolStore.statusFilter,
  })

  // Pagination (using store state)
  const pagination = computed(() => candidatePoolStore.pagination)

  // Computed
  const hasData = computed(() => candidatePools.value.length > 0)
  const isEmpty = computed(() => !loading.value && candidatePools.value.length === 0)
  const hasFilters = computed(() => {
    return filters.search || filters.status
  })

  // Methods
  const fetchCandidatePools = async (params = {}) => {
    try {
      const queryParams = {
        page: pagination.value.page,
        limit: pagination.value.limit,
        search: filters.search,
        status: filters.status,
        order_by: "modified desc",
        ...params
      }

      const response = await candidatePoolStore.fetchCandidatePools(queryParams)

      // Store handles all state updates internally
      if (!response.success) {
        console.error('Failed to fetch candidate pools:', response.error)
      }
    } catch (err) {
      console.error('Error fetching candidate pools:', err)
    }
  }

  const getCandidatePool = async (name) => {
    try {
      const response = await candidatePoolStore.fetchCandidatePoolById(name)
      
      if (response.success) {
        return response.candidate_pool
      } else {
        console.error('Error fetching candidate pool:', response.error)
        return null
      }
    } catch (err) {
      console.error('Error fetching candidate pool:', err)
      return null
    }
  }

  const fetchStats = async () => {
    try {
      const response = await candidatePoolStore.fetchStatistics()
      
      if (!response.success) {
        console.error('Error fetching stats:', response.error)
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const fetchFilterOptions = async () => {
    try {
      const response = await candidatePoolStore.fetchFilterOptions()
      
      if (!response.success) {
        console.error('Error fetching filter options:', response.error)
      }
    } catch (err) {
      console.error('Error fetching filter options:', err)
    }
  }

  const searchCandidatePools = async (query = '', limit = 10) => {
    try {
      const response = await candidatePoolStore.searchCandidatePools(query, limit)
      
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
    if (page >= 1 && page <= pagination.value.pages) {
      candidatePoolStore.setPagination(page)
      fetchCandidatePools()
    }
  }

  const changeItemsPerPage = (newLimit) => {
    candidatePoolStore.setPagination(1, newLimit)
    fetchCandidatePools()
  }

  // Filter methods
  const updateSearch = debounce((searchText) => {
    filters.search = searchText
    candidatePoolStore.setSearchText(searchText)
    candidatePoolStore.setPagination(1)
    fetchCandidatePools()
  }, 500)

  const updateStatus = (status) => {
    filters.status = status
    candidatePoolStore.setStatusFilter(status)
    candidatePoolStore.setPagination(1)
    fetchCandidatePools()
  }

  const clearFilters = () => {
    filters.search = ''
    filters.status = ''
    candidatePoolStore.resetFilters()
    candidatePoolStore.setPagination(1)
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