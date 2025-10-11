import { ref, reactive, computed, watch } from 'vue'
import { useCandidateStore } from '@/stores/candidate.js'
import { debounce } from 'lodash'

/**
 * Talent Pool Composable
 * Quản lý state và logic cho TalentPool management
 */
export function useCandidate() {
  // Store
  const candidateStore = useCandidateStore()
  
  // State (using store state)
  const candidates = computed(() => candidateStore.candidates)
  const selectedCandidate = computed(() => candidateStore.currentCandidate)
  const loading = computed(() => candidateStore.loading)
  const error = computed(() => candidateStore.error)
  const stats = computed(() => candidateStore.statistics)
  const filterOptions = computed(() => candidateStore.filterOptions)
  
  // Pagination state (using store state)
  const pagination = computed(() => candidateStore.pagination)
  
  // Filter state (using store state)
  const filters = reactive({
    search: candidateStore.searchText,
    status: candidateStore.statusFilter,
    source: candidateStore.sourceFilter,
    skills: candidateStore.skillsFilter
  })
  
  // Computed
  const hasData = computed(() => candidates.value.length > 0)
  const isEmpty = computed(() => !loading.value && candidates.value.length === 0)
  
  // Debounced search
  const debouncedSearch = debounce(() => {
    candidateStore.setPagination(1)
    fetchCandidates()
  }, 500)
  watch(() => filters.search, debouncedSearch)
  
  // Methods
  const fetchCandidates = async () => {
    try {
      const options = {
        filters: {
          status: filters.status || undefined,
          source: filters.source || undefined
        },
        or_filters: filters.search ? [
          ['full_name', 'like', `%${filters.search}%`],
          ['email', 'like', `%${filters.search}%`]
        ] : [],
        page_length: pagination.value.limit,
        start: (pagination.value.page - 1) * pagination.value.limit,
        order_by: 'modified desc'
      }
      const result = await candidateStore.fetchCandidates(options)

      console.log('result', result)
      // Store handles all state updates internally
    } catch (err) {
      console.error('Error fetching candidates:', err)
    }
  }
  
  const fetchStats = async () => {
    try {
      const result = await candidateStore.fetchStatistics()
      // Store handles all state updates internally
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }
  
  const fetchFilterOptions = async () => {
    try {
      const result = await candidateStore.fetchFilterOptions()
      // Store handles all state updates internally
    } catch (err) {
      console.error('Error fetching filter options:', err)
    }
  }
  
  const searchCandidatesAPI = async (query, limit = 10) => {
    try {
      const result = await candidateStore.searchCandidates(query, limit)
      return result.data || []
    } catch (err) {
      console.error('Error searching candidates:', err)
      return []
    }
  }
  
  const getCandidateAPI = async (name) => {
    try {
      const result = await candidateStore.fetchCandidateById(name)
      return result.data || null
    } catch (err) {
      console.error('Error fetching candidate:', err)
      return null
    }
  }
  
  const createCandidateAPI = async (candidateData) => {
    try {
      const result = await candidateStore.createCandidate(candidateData)
      if (result.success) {
        await fetchStats()
        return result.data
      }
      throw new Error(result.error)
    } catch (err) {
      console.error('Error creating candidate:', err)
      throw err
    }
  }
  
  const updateCandidateAPI = async (name, candidateData) => {
    try {
      const result = await candidateStore.updateCandidate(name, candidateData)
      if (result.success) {
        await fetchStats()
        return result.data
      }
      throw new Error(result.error)
    } catch (err) {
      console.error('Error updating candidate:', err)
      throw err
    }
  }
  
  const deleteCandidateAPI = async (name) => {
    try {
      const result = await candidateStore.deleteCandidate(name)
      if (result.success) {
        await fetchStats()
        return true
      }
      throw new Error(result.error)
    } catch (err) {
      console.error('Error deleting candidate:', err)
      throw err
    }
  }
  
  // Pagination methods
  const goToPage = (page) => {
    if (page >= 1 && page <= pagination.value.pages) {
      candidateStore.setPagination(page)
      fetchCandidates()
    }
  }
  
  const nextPage = () => {
    if (pagination.value.has_next) {
      candidateStore.setPagination(pagination.value.page + 1)
      fetchCandidates()
    }
  }
  
  const previousPage = () => {
    if (pagination.value.has_prev) {
      candidateStore.setPagination(pagination.value.page - 1)
      fetchCandidates()
    }
  }
  
  const changeItemsPerPage = (newLimit) => {
    candidateStore.setPagination(1, newLimit)
    fetchCandidates()
  }
  
  // Filter methods
  const updateSearch = debounce((searchText) => {
    filters.search = searchText
    candidateStore.setSearchText(searchText)
    candidateStore.setPagination(1)
    fetchCandidates()
  }, 400)

  const updateStatus = (status) => {
    if (status && status.target) status = status.target.value
    filters.status = status
    candidateStore.setStatusFilter(status)
    candidateStore.setPagination(1)
    fetchCandidates()
  }

  const updateSource = (source) => {
    if (source && source.target) source = source.target.value
    filters.source = source
    candidateStore.setSourceFilter(source)
    candidateStore.setPagination(1)
    fetchCandidates()
  }
  
  const updateSkills = (skills) => {
    filters.skills = skills
    candidateStore.setSkillsFilter(skills)
    candidateStore.setPagination(1)
    fetchCandidates()
  }
  
  const clearFilters = () => {
    filters.search = ''
    filters.status = ''
    filters.source = ''
    filters.skills = []
    candidateStore.resetFilters()
    candidateStore.setPagination(1)
    fetchCandidates()
  }
  
  // Initialize
  const initialize = async () => {
    await Promise.all([
      fetchCandidates(),
      fetchStats(),
      fetchFilterOptions()
    ])
  }
  
  return {
    // State
    candidates,
    selectedCandidate,
    loading,
    error,
    stats,
    filterOptions,
    pagination,
    filters,
    
    // Computed
    hasData,
    isEmpty,
    
    // Methods
    fetchCandidates,
    fetchStats,
    fetchFilterOptions,
    searchCandidatesAPI,
    getCandidateAPI,
    createCandidateAPI,
    updateCandidateAPI,
    deleteCandidateAPI,
    
    // Pagination
    goToPage,
    nextPage,
    previousPage,
    changeItemsPerPage,
    
    // Filters
    updateSearch,
    updateStatus,
    updateSource,
    updateSkills,
    clearFilters,
    
    // Initialize
    initialize
  }
} 