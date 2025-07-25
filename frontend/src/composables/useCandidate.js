import { ref, reactive, computed, watch } from 'vue'
import {
  getCandidates,
  getCandidateStats,
  searchCandidates,
  getCandidate,
  createCandidate,
  updateCandidate,
  deleteCandidate,
  getFilterOptions
} from '@/repositories/candidateRepository'
import { debounce } from 'lodash'

/**
 * Talent Pool Composable
 * Quản lý state và logic cho TalentPool management
 */
export function useCandidate() {
  // State
  const candidates = ref([])
  const selectedCandidate = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const stats = ref({})
  const filterOptions = ref({ 
    status: [], 
    source: [], 
    skills: [] 
  })
  
  // Pagination state
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
  
  // Filter state
  const filters = reactive({
    search: '',
    status: '',
    source: '',
    skills: []
  })
  
  // Computed
  const hasData = computed(() => candidates.value.length > 0)
  const isEmpty = computed(() => !loading.value && candidates.value.length === 0)
  
  // Debounced search
  const debouncedSearch = debounce(() => {
    pagination.page = 1
    fetchCandidates()
  }, 500)
  watch(() => filters.search, debouncedSearch)
  
  // Methods
  const fetchCandidates = async () => {
    try {
      loading.value = true
      error.value = null
      const options = {
        filters: {
          status: filters.status || undefined,
          source: filters.source || undefined
        },
        or_filters: filters.search ? [
          ['full_name', 'like', `%${filters.search}%`],
          ['email', 'like', `%${filters.search}%`]
        ] : undefined,
        page_length: pagination.limit,
        start: (pagination.page - 1) * pagination.limit,
        order_by: 'modified desc'
      }
      const result = await getCandidates(options)

      console.log('result', result)
      candidates.value = result.data || []
      if (result.pagination) {
        Object.assign(pagination, result.pagination)
      }
    } catch (err) {
      error.value = err.message || 'Failed to fetch talent pools'
      console.error('Error fetching talent pools:', err)
    } finally {
      loading.value = false
    }
  }
  
  const fetchStats = async () => {
    try {
      const statsResult = await getCandidateStats()
      if (statsResult) {
        stats.value = statsResult
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }
  
  const fetchFilterOptions = async () => {
    try {
      const data = await getFilterOptions()
      filterOptions.value = {
        status: Array.isArray(data.status) ? data.status : [],
        source: Array.isArray(data.source) ? data.source : [],
        skills: Array.isArray(data.skills) ? data.skills : []
      }
    } catch (err) {
      console.error('Error fetching filter options:', err)
      filterOptions.value = { 
        status: [], 
        source: [], 
        skills: [] 
      }
    }
  }
  
  const searchCandidates = async (query, limit = 10) => {
    try {
      await searchCandidates.fetch({ query, limit })
      return searchCandidates.data || []
    } catch (err) {
      console.error('Error searching candidates:', err)
      return []
    }
  }
  
  const getCandidate = async (name) => {
    try {
      loading.value = true
      error.value = null
      
      await getCandidate.fetch({ name })
      
      if (getCandidate.data) {
        selectedCandidate.value = getCandidate.data
        return getCandidate.data
      }
      return null
    } catch (err) {
      error.value = err.message || 'Failed to fetch talent pool'
      console.error('Error fetching talent pool:', err)
      return null
    } finally {
      loading.value = false
    }
  }
  
  const createCandidateAPI = async (candidateData) => {
    try {
      loading.value = true
      error.value = null
      const result = await createCandidate(candidateData)
      if (result) {
        candidates.value.unshift(result)
        pagination.total += 1
        await fetchStats()
        return result
      }
      return null
    } catch (err) {
      error.value = err.message || 'Failed to create talent pool'
      console.error('Error creating talent pool:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const updateCandidateAPI = async (name, candidateData) => {
    try {
      loading.value = true
      error.value = null
      const result = await updateCandidate(name, candidateData)
      if (result) {
        const index = candidates.value.findIndex(c => c.name === name)
        if (index !== -1) {
          candidates.value[index] = result
        }
        if (selectedCandidate.value?.name === name) {
          selectedCandidate.value = result
        }
        await fetchStats()
        return result
      }
      return null
    } catch (err) {
      error.value = err.message || 'Failed to update talent pool'
      console.error('Error updating talent pool:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const deleteCandidate = async (name) => {
    try {
      loading.value = true
      error.value = null
      await deleteCandidate(name)
      candidates.value = candidates.value.filter(c => c.name !== name)
      if (selectedCandidate.value?.name === name) {
        selectedCandidate.value = null
      }
      pagination.total -= 1
      await fetchStats()
      return true
    } catch (err) {
      error.value = err.message || 'Failed to delete talent pool'
      console.error('Error deleting talent pool:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  // Pagination methods
  const goToPage = (page) => {
    if (page >= 1 && page <= pagination.pages) {
      pagination.page = page
      fetchCandidates()
    }
  }
  
  const nextPage = () => {
    if (pagination.has_next) {
      pagination.page++
      fetchCandidates()
    }
  }
  
  const previousPage = () => {
    if (pagination.has_prev) {
      pagination.page--
      fetchCandidates()
    }
  }
  
  const changeItemsPerPage = (newLimit) => {
    pagination.limit = newLimit
    pagination.page = 1
    fetchCandidates()
  }
  
  // Filter methods
  const updateSearch = debounce((searchText) => {
    filters.search = searchText
    pagination.page = 1
    fetchCandidates()
  }, 400)

  const updateStatus = (status) => {
    if (status && status.target) status = status.target.value
    filters.status = status
    pagination.page = 1
    fetchCandidates()
  }

  const updateSource = (source) => {
    if (source && source.target) source = source.target.value
    filters.source = source
    pagination.page = 1
    fetchCandidates()
  }
  
  const updateSkills = (skills) => {
    filters.skills = skills
    pagination.page = 1
    fetchCandidates()
  }
  
  const clearFilters = () => {
    filters.search = ''
    filters.status = ''
    filters.source = ''
    filters.skills = []
    pagination.page = 1
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
    searchCandidates,
    getCandidate,
    createCandidateAPI,
    updateCandidateAPI,
    deleteCandidate,
    
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