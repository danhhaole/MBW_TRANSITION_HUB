import { ref, computed, reactive } from 'vue'
import { debounce } from 'lodash'
import { 
  getFilteredCampaigns, 
  getCampaignDetails, 
  submitNewCampaign, 
  updateCampaignData, 
  removeCampaign,
  formatCampaignDate,
  getCampaignStatusByDate,
  getUserOptions,
  getTalentSegmentOptions,
  getJobOpeningOptions
} from '@/services/campaignService'
import { getCampaigns } from '@/repositories/campaignRepository'

// Composable chính cho quản lý campaigns với pagination
export const useCampaignList = () => {
  const campaigns = ref([])
  const loading = ref(false)
  const error = ref(null)
  const searchText = ref('')
  const statusFilter = ref('all')
  const typeFilter = ref('all')
  const activeFilter = ref('all')
  
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

  // Computed để filter campaigns (client-side backup)
  const filteredCampaigns = computed(() => {
    let filtered = campaigns.value

    if (searchText.value) {
      filtered = filtered.filter(campaign => 
        campaign.campaign_name.toLowerCase().includes(searchText.value.toLowerCase()) ||
        campaign.description?.toLowerCase().includes(searchText.value.toLowerCase())
      )
    }

    if (statusFilter.value && statusFilter.value !== 'all') {
      filtered = filtered.filter(campaign => campaign.status === statusFilter.value)
    }

    if (typeFilter.value && typeFilter.value !== 'all') {
      filtered = filtered.filter(campaign => campaign.type === typeFilter.value)
    }

    if (activeFilter.value !== 'all') {
      const isActive = activeFilter.value === 'active'
      filtered = filtered.filter(campaign => campaign.is_active === (isActive ? 1 : 0))
    }

    return filtered
  })

  // Load danh sách campaigns với pagination
  const loadCampaigns = async (options = {}) => {
    loading.value = true
    error.value = null
    
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
      const response = await getFilteredCampaigns(requestOptions)
      if (response && Array.isArray(response.data) && response.data.length > 0) {
        campaigns.value = response.data.map(campaign => ({
          ...campaign,
          displayStatus: getCampaignStatusByDate(
            campaign.start_date, 
            campaign.end_date, 
            campaign.status,
            campaign.is_active
          ),
          formattedStartDate: formatCampaignDate(campaign.start_date),
          formattedEndDate: formatCampaignDate(campaign.end_date)
        }))
        // Update pagination info
        pagination.value = {
          ...pagination.value,
          ...response.pagination
        }
      } else {
        error.value = response && response.message ? response.message : 'Không có dữ liệu'
        campaigns.value = []
      }
    } catch (err) {
      error.value = err.message || 'Có lỗi xảy ra khi tải campaigns'
      console.error('Failed to load campaigns:', err)
      campaigns.value = []
    } finally {
      loading.value = false
    }
  }

  // Pagination functions
  const goToPage = async (page) => {
    pagination.value.page = page
    await loadCampaigns()
  }
  
  const changeItemsPerPage = async (limit) => {
    pagination.value.limit = limit
    pagination.value.page = 1 // Reset to first page
    await loadCampaigns()
  }

  // Refresh data
  const refreshCampaigns = () => {
    pagination.value.page = 1 // Reset to first page when filtering
    loadCampaigns()
  }

  // Set filter và reload
  const setStatusFilter = (status) => {
    // Nếu truyền vào là event object thì lấy value
    if (status && status.target) status = status.target.value
    statusFilter.value = status
    refreshCampaigns()
  }

  const setTypeFilter = (type) => {
    if (type && type.target) type = type.target.value
    typeFilter.value = type
    refreshCampaigns()
  }

  const setActiveFilter = (active) => {
    if (active && active.target) active = active.target.value
    activeFilter.value = active
    refreshCampaigns()
  }

  const setSearchText = debounce((text) => {
    searchText.value = text
    refreshCampaigns()
  }, 400)

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
    loadCampaigns,
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
  const loading = ref(false)
  const error = ref(null)
  const success = ref(false)

  // Tạo mới campaign
  const createCampaign = async (formData) => {
    loading.value = true
    error.value = null
    success.value = false

    try {
      await submitNewCampaign(formData)
      success.value = true
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Cập nhật campaign
  const updateCampaign = async (name, formData) => {
    loading.value = true
    error.value = null
    success.value = false

    try {
      await updateCampaignData(name, formData)
      success.value = true
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  // Xóa campaign
  const deleteCampaign = async (name, campaignName) => {
    loading.value = true
    error.value = null

    try {
      await removeCampaign(name, campaignName)
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
    createCampaign,
    updateCampaign,
    deleteCampaign,
    resetState
  }
}

// Composable cho form management
export const useCampaignForm = (initialData = null) => {
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
  const users = ref([])
  const talentSegments = ref([])
  const loadingOptions = ref(false)
  const jobOpenings = ref([])

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

  // Load options data
  const loadOptions = async () => {
    loadingOptions.value = true
    try {
      const [usersData, segmentsData, jobOpeningsData] = await Promise.all([
        getUserOptions(),
        getTalentSegmentOptions(),
        getJobOpeningOptions()
      ])
      
      users.value = usersData.map(user => ({
        label: user.full_name || user.name,
        value: user.name,
        subtitle: user.email
      }))
      
      talentSegments.value = segmentsData.map(segment => ({
        label: segment.title || segment.name,
        value: segment.name
      }))

      jobOpenings.value = jobOpeningsData.map(j => ({
        label: j.job_title || j.name,
        value: j.name
      }))
    } catch (error) {
      console.error('Failed to load options:', error)
    } finally {
      loadingOptions.value = false
    }
  }

  // Validate form
  const validateForm = () => {
    formErrors.value = {}
    
    // Check campaign_name
    if (!form.value.campaign_name || !form.value.campaign_name.trim()) {
      formErrors.value.campaign_name = 'Tên chiến dịch là bắt buộc'
    } else if (form.value.campaign_name.length < 3) {
      formErrors.value.campaign_name = 'Tên chiến dịch phải có ít nhất 3 ký tự'
    }

    // Check dates
    if (form.value.start_date && form.value.end_date) {
      const startDate = new Date(form.value.start_date)
      const endDate = new Date(form.value.end_date)
      if (startDate >= endDate) {
        formErrors.value.end_date = 'Ngày kết thúc phải sau ngày bắt đầu'
      }
    }

    isValid.value = Object.keys(formErrors.value).length === 0
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
  const campaign = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const loadCampaign = async (name) => {
    loading.value = true
    error.value = null

    try {
      const data = await getCampaignDetails(name)
      campaign.value = {
        ...data,
        displayStatus: getCampaignStatusByDate(
          data.start_date, 
          data.end_date, 
          data.status,
          data.is_active
        ),
        formattedStartDate: formatCampaignDate(data.start_date),
        formattedEndDate: formatCampaignDate(data.end_date)
      }
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return {
    campaign,
    loading,
    error,
    loadCampaign
  }
} 