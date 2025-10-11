import { ref, computed, reactive, watch } from 'vue'
import { useMiraTalentPoolStore } from '@/stores/miraTalentPool.js'
import { debounce } from 'lodash'

export function useMiraTalentPool() {
  const miraTalentPoolStore = useMiraTalentPoolStore()
  
  // Computed properties from store
  const talentPools = computed(() => miraTalentPoolStore.talentPools)
  const selectedTalentPool = computed(() => miraTalentPoolStore.currentTalentPool)
  const loading = computed(() => miraTalentPoolStore.loading)
  const error = computed(() => miraTalentPoolStore.error)
  const success = computed(() => miraTalentPoolStore.success)
  const stats = computed(() => miraTalentPoolStore.statistics)
  const filterOptions = computed(() => miraTalentPoolStore.filterOptions)
  const pagination = computed(() => miraTalentPoolStore.pagination)

  // Filter state
  const filters = reactive({
    search: miraTalentPoolStore.searchText || '',
    campaign: miraTalentPoolStore.campaignFilter || '',
    segment: miraTalentPoolStore.segmentFilter || '',
    status: miraTalentPoolStore.statusFilter || ''
  })

  // Computed
  const filteredTalentPools = computed(() => miraTalentPoolStore.filteredTalentPools)
  const hasData = computed(() => talentPools.value.length > 0)
  const isEmpty = computed(() => !loading.value && talentPools.value.length === 0)
  const hasFilters = computed(() => {
    return filters.search || filters.campaign || filters.segment || filters.status
  })

  // Debounced search
  const debouncedSearch = debounce(() => {
    miraTalentPoolStore.setPagination(1)
    fetchTalentPools()
  }, 500)
  
  watch(() => filters.search, debouncedSearch)

  // API Methods
  const fetchTalentPools = async (params = {}) => {
    const options = {
      page: params.page || pagination.value.page,
      limit: params.limit || pagination.value.limit,
      searchText: filters.search,
      campaignFilter: filters.campaign,
      segmentFilter: filters.segment,
      statusFilter: filters.status,
      orderBy: params.orderBy || miraTalentPoolStore.orderBy
    }
    
    return await miraTalentPoolStore.fetchTalentPools(options)
  }

  const fetchStats = async () => {
    return await miraTalentPoolStore.fetchStatistics()
  }

  const fetchFilterOptions = async () => {
    return await miraTalentPoolStore.fetchFilterOptions()
  }

  const searchTalentPoolsAPI = async (query = '', limit = 10) => {
    return await miraTalentPoolStore.searchTalentPools(query, limit)
  }

  const getTalentPoolAPI = async (name) => {
    return await miraTalentPoolStore.fetchTalentPoolById(name)
  }

  const createTalentPoolAPI = async (talentPoolData) => {
    return await miraTalentPoolStore.createTalentPool(talentPoolData)
  }

  const updateTalentPoolAPI = async (name, talentPoolData) => {
    return await miraTalentPoolStore.updateTalentPool(name, talentPoolData)
  }

  const deleteTalentPoolAPI = async (name) => {
    return await miraTalentPoolStore.deleteTalentPool(name)
  }

  // Pagination methods
  const goToPage = (page) => {
    miraTalentPoolStore.setPagination(page)
    fetchTalentPools()
  }

  const nextPage = () => {
    if (pagination.value.has_next) {
      goToPage(pagination.value.page + 1)
    }
  }

  const previousPage = () => {
    if (pagination.value.has_prev) {
      goToPage(pagination.value.page - 1)
    }
  }

  const changeItemsPerPage = (newLimit) => {
    miraTalentPoolStore.setPagination(1, newLimit)
    fetchTalentPools()
  }

  // Filter methods
  const updateSearch = debounce((searchText) => {
    filters.search = searchText
    miraTalentPoolStore.setSearchText(searchText)
    miraTalentPoolStore.setPagination(1)
    fetchTalentPools()
  }, 400)

  const updateCampaign = (campaign) => {
    filters.campaign = campaign
    miraTalentPoolStore.setCampaignFilter(campaign)
    miraTalentPoolStore.setPagination(1)
    fetchTalentPools()
  }

  const updateSegment = (segment) => {
    filters.segment = segment
    miraTalentPoolStore.setSegmentFilter(segment)
    miraTalentPoolStore.setPagination(1)
    fetchTalentPools()
  }

  const updateStatus = (status) => {
    filters.status = status
    miraTalentPoolStore.setStatusFilter(status)
    miraTalentPoolStore.setPagination(1)
    fetchTalentPools()
  }

  const clearFilters = () => {
    filters.search = ''
    filters.campaign = ''
    filters.segment = ''
    filters.status = ''
    miraTalentPoolStore.resetFilters()
    fetchTalentPools()
  }

  // Initialize
  const initialize = async () => {
    await Promise.all([
      fetchTalentPools(),
      fetchStats(),
      fetchFilterOptions()
    ])
  }

  // Legacy methods for backward compatibility
  const loadData = async (params = {}) => {
    return await fetchTalentPools(params)
  }

  const handleSearch = () => {
    updateSearch(filters.search)
  }

  const clearSearch = () => {
    filters.search = ''
    updateSearch('')
  }

  // Utility methods
  const formatDate = (dateString) => {
    return miraTalentPoolStore.formatDate(dateString)
  }

  const getStatusDisplay = (status) => {
    return miraTalentPoolStore.getStatusDisplay(status)
  }

  const getPaginationRange = () => {
    const totalPages = pagination.value.pages || 1
    const currentPage = pagination.value.page || 1
    const range = []
    
    if (totalPages <= 5) {
      for (let i = 1; i <= totalPages; i++) range.push(i)
    } else {
      if (currentPage <= 3) {
        range.push(1, 2, 3, 4, "...", totalPages)
      } else if (currentPage >= totalPages - 2) {
        range.push(1, "...", totalPages - 3, totalPages - 2, totalPages - 1, totalPages)
      } else {
        range.push(
          1,
          "...",
          currentPage - 1,
          currentPage,
          currentPage + 1,
          "...",
          totalPages
        )
      }
    }
    return range
  }

  return {
    // State
    talentPools,
    selectedTalentPool,
    loading,
    error,
    success,
    stats,
    filterOptions,
    pagination,
    filters,

    // Computed
    filteredTalentPools,
    hasData,
    isEmpty,
    hasFilters,

    // API Methods
    fetchTalentPools,
    searchTalentPoolsAPI,
    getTalentPoolAPI,
    createTalentPoolAPI,
    updateTalentPoolAPI,
    deleteTalentPoolAPI,
    fetchStats,
    fetchFilterOptions,

    // Pagination
    goToPage,
    nextPage,
    previousPage,
    changeItemsPerPage,

    // Filters
    updateSearch,
    updateCampaign,
    updateSegment,
    updateStatus,
    clearFilters,

    // Legacy methods (for backward compatibility)
    loadData,
    handleSearch,
    clearSearch,

    // Utilities
    formatDate,
    getStatusDisplay,
    getPaginationRange,
    
    // Initialize
    initialize
  }
}

export default useMiraTalentPool
