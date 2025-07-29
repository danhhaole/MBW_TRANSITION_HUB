import { ref, computed } from 'vue'
import { debounce } from 'lodash'
import { getFilteredLadiPages, createLadiPage, updateLadiPage, deleteLadiPage } from '@/services/ladiPageService'

// Composable for list management
export const useLadiPageList = () => {
  const ladiPages = ref([])
  const loading = ref(false)
  const error = ref(null)
  const searchText = ref('')
  const statusFilter = ref('all')
  const campaignFilter = ref('all')

  // Pagination state
  const pagination = ref({
    page: 1,
    limit: 10,
    total: 0,
    pages: 1,
    has_next: false,
    has_prev: false,
    showing_from: 0,
    showing_to: 0
  })

  // Load Ladi pages with pagination and filters
  const loadLadiPages = async (options = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const requestOptions = {
        page: pagination.value.page,
        limit: pagination.value.limit,
        searchText: searchText.value,
        status: statusFilter.value,
        campaign: campaignFilter.value,
        ...options
      }
      const response = await getFilteredLadiPages(requestOptions)
      if (response && Array.isArray(response.data)) {
        ladiPages.value = response.data
        pagination.value = {
          ...pagination.value,
          ...response.pagination
        }
      } else {
        error.value = response?.message || 'No data'
        ladiPages.value = []
      }
    } catch (err) {
      error.value = err.message || 'Error loading Ladi pages'
      console.error('Failed to load Ladi pages:', err)
      ladiPages.value = []
    } finally {
      loading.value = false
    }
  }

  // Pagination functions
  const goToPage = async (page) => {
    pagination.value.page = page
    await loadLadiPages()
  }

  const changeItemsPerPage = async (limit) => {
    pagination.value.limit = limit
    pagination.value.page = 1 // Reset to first page
    await loadLadiPages()
  }

  // Refresh data
  const refreshLadiPages = () => {
    pagination.value.page = 1 // Reset to first page when filtering
    loadLadiPages()
  }

  // Set filters and reload
  const setStatusFilter = (status) => {
    if (status && status.target) status = status.target.value
    statusFilter.value = status
    refreshLadiPages()
  }

  const setCampaignFilter = (campaign) => {
    if (campaign && campaign.target) campaign = campaign.target.value
    campaignFilter.value = campaign 
    refreshLadiPages()
  }

  const setSearchText = debounce((text) => {
    searchText.value = text
    refreshLadiPages()
  }, 400)

  return {
    ladiPages,
    loading,
    error,
    searchText,
    statusFilter,
    campaignFilter,
    pagination,
    loadLadiPages,
    refreshLadiPages,
    goToPage,
    changeItemsPerPage,
    setStatusFilter,
    setCampaignFilter,
    setSearchText
  }
}

// Composable for CRUD operations
export const useLadiPageCRUD = () => {
  const loading = ref(false)
  const error = ref(null)
  const success = ref(false)

  // Create new Ladi page
  const createPage = async (formData) => {
    loading.value = true
    error.value = null
    success.value = false

    try {
      await createLadiPage(formData)
      success.value = true
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Update Ladi page
  const updatePage = async (name, formData) => {
    loading.value = true
    error.value = null
    success.value = false

    try {
      await updateLadiPage(name, formData)
      success.value = true
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Delete Ladi page
  const deletePage = async (name, title) => {
    loading.value = true
    error.value = null

    try {
      await deleteLadiPage(name, title)
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Reset state
  const resetState = () => {
    error.value = null
    success.value = false
    loading.value = false
  }

  return {
    loading,
    error,
    success,
    createPage,
    updatePage,
    deletePage,
    resetState
  }
}