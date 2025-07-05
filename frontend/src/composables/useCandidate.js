import { ref, reactive, computed, watch } from 'vue'
import {
  getCandidatesResource,
  getCandidateStatsResource,
  searchCandidatesResource,
  getCandidateResource,
  createCandidateResource,
  updateCandidateResource,
  deleteCandidateResource,
  getFilterOptionsResource
} from '../services/candidateRepository'

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

/**
 * Candidate Composable
 * Quản lý state và logic cho Candidate management
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
  
  // Watch search changes
  watch(() => filters.search, debouncedSearch)
  
  // Methods
  const fetchCandidates = async () => {
    try {
      loading.value = true
      error.value = null
      
      const params = {
        page: pagination.page,
        limit: pagination.limit,
        search: filters.search,
        status: filters.status,
        source: filters.source,
        skills: JSON.stringify(filters.skills),
        order_by: 'modified desc'
      }
      
      await getCandidatesResource.fetch(params)
      
      if (getCandidatesResource.data) {
        const result = getCandidatesResource.data
        candidates.value = result.candidates || []
        
        // Update pagination
        if (result.pagination) {
          Object.assign(pagination, result.pagination)
        }
      }
    } catch (err) {
      error.value = err.message || 'Failed to fetch candidates'
      console.error('Error fetching candidates:', err)
    } finally {
      loading.value = false
    }
  }
  
  const fetchStats = async () => {
    try {
      await getCandidateStatsResource.fetch()
      if (getCandidateStatsResource.data) {
        stats.value = getCandidateStatsResource.data
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }
  
  const fetchFilterOptions = async () => {
    try {
      await getFilterOptionsResource.fetch()
      if (getFilterOptionsResource.data) {
        const data = getFilterOptionsResource.data
        filterOptions.value = {
          status: Array.isArray(data.status) ? data.status : [],
          source: Array.isArray(data.source) ? data.source : [],
          skills: Array.isArray(data.skills) ? data.skills : []
        }
      }
    } catch (err) {
      console.error('Error fetching filter options:', err)
      // Keep default empty arrays
      filterOptions.value = { 
        status: [], 
        source: [], 
        skills: [] 
      }
    }
  }
  
  const searchCandidates = async (query, limit = 10) => {
    try {
      await searchCandidatesResource.fetch({ query, limit })
      return searchCandidatesResource.data || []
    } catch (err) {
      console.error('Error searching candidates:', err)
      return []
    }
  }
  
  const getCandidate = async (name) => {
    try {
      loading.value = true
      error.value = null
      
      await getCandidateResource.fetch({ name })
      
      if (getCandidateResource.data) {
        selectedCandidate.value = getCandidateResource.data
        return getCandidateResource.data
      }
      return null
    } catch (err) {
      error.value = err.message || 'Failed to fetch candidate'
      console.error('Error fetching candidate:', err)
      return null
    } finally {
      loading.value = false
    }
  }
  
  const createCandidate = async (candidateData) => {
    try {
      loading.value = true
      error.value = null
      
      await createCandidateResource.fetch({ data: candidateData })
      
      if (createCandidateResource.data) {
        // Add to local list instead of refetching
        candidates.value.unshift(createCandidateResource.data)
        
        // Update pagination
        pagination.total += 1
        
        // Only fetch stats to update counts
        await fetchStats()
        return createCandidateResource.data
      }
      return null
    } catch (err) {
      error.value = err.message || 'Failed to create candidate'
      console.error('Error creating candidate:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const updateCandidate = async (name, candidateData) => {
    try {
      loading.value = true
      error.value = null
      
      await updateCandidateResource.fetch({ name, data: candidateData })
      
      if (updateCandidateResource.data) {
        // Update in local list
        const index = candidates.value.findIndex(c => c.name === name)
        if (index !== -1) {
          candidates.value[index] = updateCandidateResource.data
        }
        
        // Update selected candidate if it's the same
        if (selectedCandidate.value?.name === name) {
          selectedCandidate.value = updateCandidateResource.data
        }
        
        await fetchStats()
        return updateCandidateResource.data
      }
      return null
    } catch (err) {
      error.value = err.message || 'Failed to update candidate'
      console.error('Error updating candidate:', err)
      throw err
    } finally {
      loading.value = false
    }
  }
  
  const deleteCandidate = async (name) => {
    try {
      loading.value = true
      error.value = null
      
      await deleteCandidateResource.fetch({ name })
      
      // Remove from local list
      candidates.value = candidates.value.filter(c => c.name !== name)
      
      // Clear selected if it's the deleted one
      if (selectedCandidate.value?.name === name) {
        selectedCandidate.value = null
      }
      
      // Update pagination
      pagination.total -= 1
      
      // Only fetch stats to update counts
      await fetchStats()
      
      return true
    } catch (err) {
      error.value = err.message || 'Failed to delete candidate'
      console.error('Error deleting candidate:', err)
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
  const updateSearch = (searchText) => {
    filters.search = searchText
    // debouncedSearch will be triggered by the watcher
  }
  
  const updateStatus = (status) => {
    filters.status = status
    pagination.page = 1
    fetchCandidates()
  }
  
  const updateSource = (source) => {
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
    createCandidate,
    updateCandidate,
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