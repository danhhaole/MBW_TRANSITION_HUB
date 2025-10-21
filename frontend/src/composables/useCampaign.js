import { ref, computed, reactive } from 'vue'
import { debounce } from 'lodash'
import { useCampaignStore } from '@/stores/campaign'
import { storeToRefs } from 'pinia'

// Composable chính cho quản lý campaigns với pagination
export const useCampaignList = () => {
  const campaignStore = useCampaignStore()
  
  // Sử dụng store state với reactivity
  const { 
    campaigns, 
    loading, 
    error, 
    pagination,
    searchText,
    statusFilter,
    typeFilter,
    activeFilter,
    filteredCampaigns,
    statistics
  } = storeToRefs(campaignStore)

  // Load danh sách campaigns với pagination
  const loadCampaigns = async (options = {}) => {
    try {
      const requestOptions = {
        page: pagination.value.page,
        limit: pagination.value.limit,
        searchText: searchText.value,
        status: statusFilter.value,
        type: typeFilter.value,
        isActive: activeFilter.value !== 'all' ? (activeFilter.value === 'active' ? 1 : 0) : undefined,
        ...options
      }
      await campaignStore.getFilteredCampaigns(requestOptions)
    } catch (err) {
      console.error('Failed to load campaigns:', err)
    }
  }

  // Pagination functions
  const goToPage = async (page) => {
    campaignStore.pagination.page = page
    await loadCampaigns()
  }
  
  const changeItemsPerPage = async (limit) => {
    campaignStore.pagination.limit = limit
    campaignStore.pagination.page = 1 // Reset to first page
    await loadCampaigns()
  }

  // Refresh data
  const refreshCampaigns = () => {
    campaignStore.pagination.page = 1 // Reset to first page when filtering
    loadCampaigns()
  }

  // Set filter và reload
  const setStatusFilter = (status) => {
    // Nếu truyền vào là event object thì lấy value
    if (status && status.target) status = status.target.value
    campaignStore.setStatusFilter(status)
    refreshCampaigns()
  }

  const setTypeFilter = (type) => {
    if (type && type.target) type = type.target.value
    campaignStore.setTypeFilter(type)
    refreshCampaigns()
  }

  const setActiveFilter = (active) => {
    if (active && active.target) active = active.target.value
    campaignStore.setActiveFilter(active)
    refreshCampaigns()
  }

  const setSearchText = debounce((text) => {
    campaignStore.setSearchText(text)
    refreshCampaigns()
  }, 500)

  // Load statistics
  const loadStatistics = async () => {
    try {
      await campaignStore.fetchStatistics()
    } catch (err) {
      console.error('Failed to load statistics:', err)
    }
  }

  // Smart load campaigns with statistics for initial load
  const smartLoadCampaigns = async (options = {}) => {
    try {
      const result = await campaignStore.getFilteredCampaigns({
        page: pagination.value.page,
        limit: pagination.value.limit,
        searchText: searchText.value,
        status: statusFilter.value,
        type: typeFilter.value,
        isActive: activeFilter.value !== 'all' ? (activeFilter.value === 'active' ? 1 : 0) : undefined,
        ...options
      })
      
      // Only calculate statistics for initial load (no filters, page 1)
      const isInitialLoad = (!options.page || options.page === 1) && 
                           !searchText.value && 
                           statusFilter.value === 'all' && 
                           typeFilter.value === 'all' && 
                           activeFilter.value === 'all'
      
      if (result && result.count !== undefined && isInitialLoad) {
        // Calculate statistics from loaded data for initial load
        if (result.data) {
          const statusCounts = { active: 0, draft: 0, paused: 0, archived: 0 }
          result.data.forEach(campaign => {
            const displayStatus = campaignStore.getCampaignStatusByDate(
              campaign.start_date, 
              campaign.end_date, 
              campaign.status,
              campaign.is_active
            ).toLowerCase()
            
            if (statusCounts.hasOwnProperty(displayStatus)) {
              statusCounts[displayStatus]++
            }
          })
          
          // Update statistics in store
          campaignStore.statistics = {
            total: result.count,
            ...statusCounts
          }
        }
      }
      
      return result
    } catch (err) {
      console.error('Failed to load campaigns:', err)
    }
  }

  return {
    campaigns,
    filteredCampaigns,
    loading,
    error,
    searchText,
    statusFilter,
    typeFilter,
    activeFilter,
    pagination,
    statistics,
    loadCampaigns,
    smartLoadCampaigns,
    loadStatistics,
    refreshCampaigns,
    goToPage,
    changeItemsPerPage,
    setStatusFilter,
    setTypeFilter,
    setActiveFilter,
    setSearchText
  }
}

// Composable cho CRUD operations
export const useCampaignCRUD = () => {
  const campaignStore = useCampaignStore()
  
  // Sử dụng store state với reactivity
  const { loading, error, success } = storeToRefs(campaignStore)

  // Tạo mới campaign
  const createCampaign = async (formData) => {
    try {
      await campaignStore.submitNewCampaign(formData)
      return true
    } catch (err) {
      return false
    }
  }

  // Cập nhật campaign (giữ nguyên logic cũ)
  const updateCampaign = async (name, formData) => {
    try {
      await campaignStore.updateCampaignData(name, formData)
      return true
    } catch (err) {
      return false
    }
  }

  // Cập nhật campaign basic info (cho modal)
  const updateCampaignBasic = async (name, formData) => {
    try {
      await campaignStore.updateCampaignBasicInfo(name, formData)
      return true
    } catch (err) {
      return false
    }
  }

  // Xóa campaign
  const deleteCampaign = async (name, campaignName) => {
    try {
      await campaignStore.removeCampaign(name, campaignName)
      return true
    } catch (err) {
      return false
    }
  }

  // Reset state
  const resetState = () => {
    campaignStore.resetState()
  }

  return {
    loading,
    error,
    success,
    createCampaign,
    updateCampaign,
    updateCampaignBasic,
    deleteCampaign,
    resetState
  }
}

// Composable cho form management
export const useCampaignForm = (initialData = null) => {
  const campaignStore = useCampaignStore()
  
  // Sử dụng store state cho options
  const { users, talentSegments, jobOpenings, loadingOptions } = storeToRefs(campaignStore)

  const form = ref({
    campaign_name: initialData?.campaign_name || '',
    description: initialData?.description || '',
    is_active: initialData?.is_active || 1,
    owner_id: initialData?.owner_id || null,
    start_date: initialData?.start_date || null,
    end_date: initialData?.end_date || null,
    type: initialData?.type || 'NURTURING',
    status: initialData?.status || 'DRAFT',
    target_segment: initialData?.target_segment || null,
    job_opening: initialData?.job_opening || null
  })

  const formErrors = ref({})
  const isValid = ref(false)

  // Validation rules theo Vuetify
  const campaignNameRules = [
    (v) => !!v || 'Tên chiến dịch là bắt buộc',
    (v) => (v && v.length >= 3) || 'Tên chiến dịch phải có ít nhất 3 ký tự',
    (v) => (v && v.length <= 200) || 'Tên chiến dịch không được quá 200 ký tự'
  ]

  const dateRules = [
    (v) => {
      if (!v) return true
      const date = new Date(v)
      return !isNaN(date.getTime()) || 'Ngày không hợp lệ'
    }
  ]

  const endDateRules = [
    ...dateRules,
    (v) => {
      if (!v || !form.value.start_date) return true
      const startDate = new Date(form.value.start_date)
      const endDate = new Date(v)
      return endDate > startDate || 'Ngày kết thúc phải sau ngày bắt đầu'
    }
  ]

  // Type options
  const typeOptions = [
    { label: 'Nuôi dưỡng', value: 'NURTURING' },
    { label: 'Thu hút', value: 'ATTRACTION' }
  ]

  // Status options  
  const statusOptions = [
    { label: 'Nháp', value: 'DRAFT' },
    { label: 'Hoạt động', value: 'ACTIVE' },
    { label: 'Tạm dừng', value: 'PAUSED' },
    { label: 'Lưu trữ', value: 'ARCHIVED' }
  ]

  // Active options
  const activeOptions = [
    { label: 'Kích hoạt', value: 1 },
    { label: 'Vô hiệu hóa', value: 0 }
  ]

  // Load options data từ store
  const loadOptions = async () => {
    await campaignStore.loadOptions()
  }

  // Validate form sử dụng store method
  const validateForm = () => {
    const errors = campaignStore.validateCampaignForm(form.value)
    formErrors.value = errors
    isValid.value = Object.keys(errors).length === 0
    return isValid.value
  }

  // Reset form
  const resetForm = () => {
    form.value = {
      campaign_name: '',
      description: '',
      is_active: 1,
      owner_id: null,
      start_date: null,
      end_date: null,
      type: 'NURTURING',
      status: 'DRAFT',
      target_segment: null,
      job_opening: null
    }
    formErrors.value = {}
    isValid.value = false
  }

  // Set form data
  const setFormData = (data) => {
    form.value = {
      campaign_name: data.campaign_name || '',
      description: data.description || '',
      is_active: data.is_active || 1,
      owner_id: data.owner_id || null,
      start_date: data.start_date || null,
      end_date: data.end_date || null,
      type: data.type || 'NURTURING',
      status: data.status || 'DRAFT',
      target_segment: data.target_segment || null,
      job_opening: data.job_opening || null
    }
  }

  return {
    form,
    formErrors,
    isValid,
    users,
    talentSegments,
    loadingOptions,
    campaignNameRules,
    dateRules,
    endDateRules,
    typeOptions,
    statusOptions,
    activeOptions,
    loadOptions,
    validateForm,
    resetForm,
    setFormData,
    jobOpenings
  }
}

// Composable cho single campaign detail
export const useCampaignDetail = () => {
  const campaignStore = useCampaignStore()
  
  // Sử dụng store state với reactivity
  const { currentCampaign: campaign, loading, error } = storeToRefs(campaignStore)

  const loadCampaign = async (name) => {
    try {
      await campaignStore.getCampaignDetails(name)
    } catch (err) {
      console.error('Failed to load campaign:', err)
    }
  }

  return {
    campaign,
    loading,
    error,
    loadCampaign
  }
} 