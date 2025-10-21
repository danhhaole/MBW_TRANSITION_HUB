import { ref, reactive, computed, watch } from 'vue'
import { useJobOpeningStore } from '@/stores/jobOpening.js'
import { useToast } from '@/composables/useToast'
import { debounce } from 'lodash'

/**
 * Job Opening Composable
 * Quản lý state và logic cho Job Opening management
 */
export function useJobOpening() {
  // Store
  const jobOpeningStore = useJobOpeningStore()
  
  // Toast
  const toast = useToast()
  
  // State (using store state)
  const jobOpenings = computed(() => jobOpeningStore.jobOpenings)
  const selectedJobOpening = computed(() => jobOpeningStore.currentJobOpening)
  const loading = computed(() => jobOpeningStore.loading)
  const error = computed(() => jobOpeningStore.error)
  const stats = computed(() => jobOpeningStore.statistics)
  const filterOptions = computed(() => jobOpeningStore.filterOptions)

  // Pagination state (using store state)
  const pagination = computed(() => jobOpeningStore.pagination)

  // Filter state (using store state)
  const filters = reactive({
    search: jobOpeningStore.searchText,
    status: jobOpeningStore.statusFilter,
    department: jobOpeningStore.departmentFilter,
    location: jobOpeningStore.locationFilter
  })

  // Computed
  const hasData = computed(() => jobOpenings.value.length > 0)
  const isEmpty = computed(() => !loading.value && jobOpenings.value.length === 0)
  const hasFilters = computed(() => {
    return filters.search || filters.status || filters.department || filters.location
  })

  // Debounced search
  const debouncedSearch = debounce(() => {
    jobOpeningStore.setPagination(1)
    fetchJobOpenings()
  }, 500)
  watch(() => filters.search, debouncedSearch)

  // Methods
  const fetchJobOpenings = async (params = {}) => {
    try {
      const options = {
        filters: {
          approval_status: filters.status || undefined,
          department_name: filters.department || undefined,
          location_name: filters.location || undefined
        },
        or_filters: filters.search ? [
          ['job_title', 'like', `%${filters.search}%`],
          ['job_code', 'like', `%${filters.search}%`],
          ['department_name', 'like', `%${filters.search}%`]
        ] : [],
        page_length: pagination.value.limit,
        page: pagination.value.page,
        order_by: 'modified desc',
        ...params
      }
      const result = await jobOpeningStore.fetchJobOpenings(options)

      if (!result.success) {
        toast.error(result.error || 'Failed to load job openings')
      }
      
      return result
    } catch (err) {
      console.error('Error fetching job openings:', err)
      toast.error('Failed to load job openings')
    }
  }

  const fetchStats = async () => {
    try {
      const result = await jobOpeningStore.fetchStatistics()
      if (!result.success) {
        toast.error(result.error || 'Failed to load statistics')
      }
      return result
    } catch (err) {
      console.error('Error fetching stats:', err)
      toast.error('Failed to load statistics')
    }
  }

  const fetchFilterOptions = async () => {
    try {
      const result = await jobOpeningStore.fetchFilterOptions()
      if (!result.success) {
        toast.error(result.error || 'Failed to load filter options')
      }
      return result
    } catch (err) {
      console.error('Error fetching filter options:', err)
      toast.error('Failed to load filter options')
    }
  }

  const searchJobOpeningsAPI = async (query = '', limit = 10) => {
    try {
      const result = await jobOpeningStore.searchJobOpenings(query, limit)
      return result.data || []
    } catch (err) {
      console.error('Error searching job openings:', err)
      return []
    }
  }

  const getJobOpeningAPI = async (name) => {
    try {
      const result = await jobOpeningStore.fetchJobOpeningById(name)
      return result.data || null
    } catch (err) {
      console.error('Error fetching job opening:', err)
      return null
    }
  }

  const createJobOpeningAPI = async (jobOpeningData) => {
    try {
      const result = await jobOpeningStore.createJobOpening(jobOpeningData)
      if (result.success) {
        toast.success('Job opening created successfully')
        await fetchStats()
        return result.data
      }
      toast.error(result.error || 'Failed to create job opening')
      throw new Error(result.error)
    } catch (err) {
      console.error('Error creating job opening:', err)
      toast.error('Failed to create job opening')
      throw err
    }
  }

  const updateJobOpeningAPI = async (name, jobOpeningData) => {
    try {
      const result = await jobOpeningStore.updateJobOpening(name, jobOpeningData)
      if (result.success) {
        toast.success('Job opening updated successfully')
        await fetchStats()
        return result.data
      }
      toast.error(result.error || 'Failed to update job opening')
      throw new Error(result.error)
    } catch (err) {
      console.error('Error updating job opening:', err)
      toast.error('Failed to update job opening')
      throw err
    }
  }

  const deleteJobOpeningAPI = async (name) => {
    try {
      const result = await jobOpeningStore.deleteJobOpening(name)
      if (result.success) {
        toast.success('Job opening deleted successfully')
        await fetchStats()
        return true
      }
      toast.error(result.error || 'Failed to delete job opening')
      throw new Error(result.error)
    } catch (err) {
      console.error('Error deleting job opening:', err)
      toast.error('Failed to delete job opening')
      throw err
    }
  }

  // Pagination methods
  const goToPage = (page) => {
    if (page >= 1 && page <= pagination.value.pages) {
      jobOpeningStore.setPagination(page)
      fetchJobOpenings()
    }
  }

  const nextPage = () => {
    if (pagination.value.has_next) {
      jobOpeningStore.setPagination(pagination.value.page + 1)
      fetchJobOpenings()
    }
  }

  const previousPage = () => {
    if (pagination.value.has_prev) {
      jobOpeningStore.setPagination(pagination.value.page - 1)
      fetchJobOpenings()
    }
  }

  const changeItemsPerPage = (newLimit) => {
    jobOpeningStore.setPagination(1, newLimit)
    fetchJobOpenings()
  }

  // Filter methods
  const updateSearch = debounce((searchText) => {
    filters.search = searchText
    jobOpeningStore.setSearchText(searchText)
    jobOpeningStore.setPagination(1)
    fetchJobOpenings()
  }, 500)

  const updateStatus = (status) => {
    if (status && status.target) status = status.target.value
    filters.status = status
    jobOpeningStore.setStatusFilter(status)
    jobOpeningStore.setPagination(1)
    fetchJobOpenings()
  }

  const updateDepartment = (department) => {
    if (department && department.target) department = department.target.value
    filters.department = department
    jobOpeningStore.setDepartmentFilter(department)
    jobOpeningStore.setPagination(1)
    fetchJobOpenings()
  }

  const updateLocation = (location) => {
    if (location && location.target) location = location.target.value
    filters.location = location
    jobOpeningStore.setLocationFilter(location)
    jobOpeningStore.setPagination(1)
    fetchJobOpenings()
  }

  const clearFilters = () => {
    filters.search = ''
    filters.status = ''
    filters.department = ''
    filters.location = ''
    jobOpeningStore.resetFilters()
    jobOpeningStore.setPagination(1)
    fetchJobOpenings()
  }

  // Initialize data
  const initialize = async () => {
    await Promise.all([
      fetchJobOpenings(),
      fetchStats(),
      fetchFilterOptions()
    ])
  }

  return {
    // State
    jobOpenings,
    selectedJobOpening,
    loading,
    error,
    stats,
    filterOptions,
    pagination,
    filters,

    // Computed
    hasData,
    isEmpty,
    hasFilters,

    // Methods
    fetchJobOpenings,
    fetchStats,
    fetchFilterOptions,
    searchJobOpeningsAPI,
    getJobOpeningAPI,
    createJobOpeningAPI,
    updateJobOpeningAPI,
    deleteJobOpeningAPI,

    // Pagination
    goToPage,
    nextPage,
    previousPage,
    changeItemsPerPage,

    // Filters
    updateSearch,
    updateStatus,
    updateDepartment,
    updateLocation,
    clearFilters,

    // Initialize
    initialize
  }
}

export default useJobOpening
