import { ref, computed } from 'vue'
import { debounce } from 'lodash'
import { useCampaignStepStore } from '@/stores/campaignStep'
import { storeToRefs } from 'pinia'

// Composable chính cho quản lý campaign steps với pagination
export const useCampaignStepList = () => {
  const campaignStepStore = useCampaignStepStore()
  
  // Sử dụng store state với reactivity
  const { 
    campaignSteps, 
    loading, 
    error, 
    pagination,
    searchText,
    campaignFilter,
    actionTypeFilter,
    orderBy,
    filteredCampaignSteps
  } = storeToRefs(campaignStepStore)

  // Debounced search function
  const debouncedSearch = debounce(async (searchTerm) => {
    await campaignStepStore.getFilteredCampaignSteps({
      search: searchTerm,
      campaign: campaignFilter.value,
      action_type: actionTypeFilter.value,
      order_by: orderBy.value,
      page: 1,
      limit: pagination.value.limit
    })
  }, 300)

  // Load campaign steps with current filters
  const loadCampaignSteps = async (options = {}) => {
    const params = {
      search: searchText.value,
      campaign: campaignFilter.value,
      action_type: actionTypeFilter.value,
      order_by: orderBy.value,
      page: pagination.value.page,
      limit: pagination.value.limit,
      ...options
    }
    
    return await campaignStepStore.getFilteredCampaignSteps(params)
  }

  // Refresh data
  const refreshCampaignSteps = async () => {
    await loadCampaignSteps({ page: 1 })
  }

  // Search function
  const searchCampaignSteps = (searchTerm) => {
    campaignStepStore.setSearchText(searchTerm)
    debouncedSearch(searchTerm)
  }

  // Pagination functions
  const goToPage = async (page) => {
    await loadCampaignSteps({ page })
  }

  const nextPage = async () => {
    if (pagination.value.has_next) {
      await goToPage(pagination.value.page + 1)
    }
  }

  const prevPage = async () => {
    if (pagination.value.has_prev) {
      await goToPage(pagination.value.page - 1)
    }
  }

  const changeItemsPerPage = async (limit) => {
    await loadCampaignSteps({ page: 1, limit })
  }

  // Filter functions
  const setCampaignFilter = async (campaign) => {
    campaignStepStore.setCampaignFilter(campaign)
    await loadCampaignSteps({ page: 1 })
  }

  const setActionTypeFilter = async (actionType) => {
    campaignStepStore.setActionTypeFilter(actionType)
    await loadCampaignSteps({ page: 1 })
  }

  const setOrderBy = async (orderBy) => {
    campaignStepStore.setOrderBy(orderBy)
    await loadCampaignSteps({ page: 1 })
  }

  return {
    // State
    campaignSteps,
    loading,
    error,
    pagination,
    searchText,
    campaignFilter,
    actionTypeFilter,
    orderBy,
    filteredCampaignSteps,
    
    // Actions
    loadCampaignSteps,
    refreshCampaignSteps,
    searchCampaignSteps,
    goToPage,
    nextPage,
    prevPage,
    changeItemsPerPage,
    setCampaignFilter,
    setActionTypeFilter,
    setOrderBy
  }
}

// Composable cho CRUD operations
export const useCampaignStepCRUD = () => {
  const campaignStepStore = useCampaignStepStore()
  
  // Sử dụng store state với reactivity
  const { loading, error, success } = storeToRefs(campaignStepStore)

  // Tạo mới campaign step
  const createCampaignStep = async (formData) => {
    try {
      await campaignStepStore.createCampaignStep(formData)
      return true
    } catch (err) {
      return false
    }
  }

  // Cập nhật campaign step
  const updateCampaignStep = async (name, formData) => {
    try {
      await campaignStepStore.updateCampaignStep(name, formData)
      return true
    } catch (err) {
      return false
    }
  }

  // Xóa campaign step
  const deleteCampaignStep = async (name) => {
    try {
      await campaignStepStore.deleteCampaignStep(name)
      return true
    } catch (err) {
      return false
    }
  }

  // Cập nhật chỉ step order (lightweight)
  const updateStepOrder = async (name, stepOrder) => {
    try {
      await campaignStepStore.updateStepOrder(name, stepOrder)
      return true
    } catch (err) {
      return false
    }
  }

  // Reset state
  const resetState = () => {
    campaignStepStore.resetState()
  }

  return {
    loading,
    error,
    success,
    createCampaignStep,
    updateCampaignStep,
    deleteCampaignStep,
    updateStepOrder,
    resetState
  }
}

// Composable cho form management
export const useCampaignStepForm = (initialData = null) => {
  const campaignStepStore = useCampaignStepStore()

  const form = ref({
    campaign_step_name: initialData?.campaign_step_name || '',
    description: initialData?.description || '',
    campaign: initialData?.campaign || '',
    action_type: initialData?.action_type || '',
    step_order: initialData?.step_order || 1,
    is_active: initialData?.is_active !== undefined ? initialData.is_active : 1,
    delay_days: initialData?.delay_days || 0,
    template_content: initialData?.template_content || ''
  })

  const formErrors = ref({})
  const isValid = ref(false)
  const campaignOptions = ref([])
  const loadingOptions = ref(false)

  // Validation rules theo Vuetify
  const stepNameRules = [
    (v) => !!v || 'Tên bước là bắt buộc',
    (v) => (v && v.length >= 3) || 'Tên bước phải có ít nhất 3 ký tự',
    (v) => (v && v.length <= 200) || 'Tên bước không được quá 200 ký tự'
  ]

  const campaignRules = [
    (v) => !!v || 'Chiến dịch là bắt buộc'
  ]

  const actionTypeRules = [
    (v) => !!v || 'Loại hành động là bắt buộc'
  ]

  const stepOrderRules = [
    (v) => v === '' || v === null || (!isNaN(v) && v >= 1) || 'Thứ tự bước phải là số dương'
  ]

  const delayDaysRules = [
    (v) => v === '' || v === null || (!isNaN(v) && v >= 0) || 'Số ngày trễ phải là số không âm'
  ]

  // Action type options
  const actionTypeOptions = [
    { label: 'Gửi Email', value: 'EMAIL' },
    { label: 'Gửi SMS', value: 'SMS' },
    { label: 'Gọi điện', value: 'CALL' },
    { label: 'Cuộc họp', value: 'MEETING' },
    { label: 'Nhiệm vụ', value: 'TASK' },
    { label: 'Ghi chú', value: 'NOTE' },
    { label: 'Theo dõi', value: 'FOLLOW_UP' }
  ]

  // Active options
  const activeOptions = [
    { label: 'Kích hoạt', value: 1 },
    { label: 'Vô hiệu hóa', value: 0 }
  ]

  // Load campaign options
  const loadCampaignOptions = async () => {
    loadingOptions.value = true
    try {
      const options = await campaignStepStore.getCampaignOptions()
      campaignOptions.value = options
    } catch (error) {
      console.error('Failed to load campaign options:', error)
    } finally {
      loadingOptions.value = false
    }
  }

  // Validate form sử dụng store method
  const validateForm = () => {
    const errors = campaignStepStore.validateCampaignStepForm(form.value)
    formErrors.value = errors
    isValid.value = Object.keys(errors).length === 0
    return isValid.value
  }

  // Reset form
  const resetForm = () => {
    form.value = {
      campaign_step_name: '',
      description: '',
      campaign: '',
      action_type: '',
      step_order: 1,
      is_active: 1,
      delay_days: 0,
      template_content: ''
    }
    formErrors.value = {}
    isValid.value = false
  }

  // Set form data
  const setFormData = (data) => {
    form.value = {
      campaign_step_name: data.campaign_step_name || '',
      description: data.description || '',
      campaign: data.campaign || '',
      action_type: data.action_type || '',
      step_order: data.step_order || 1,
      is_active: data.is_active !== undefined ? data.is_active : 1,
      delay_days: data.delay_days || 0,
      template_content: data.template_content || ''
    }
  }

  return {
    form,
    formErrors,
    isValid,
    campaignOptions,
    loadingOptions,
    stepNameRules,
    campaignRules,
    actionTypeRules,
    stepOrderRules,
    delayDaysRules,
    actionTypeOptions,
    activeOptions,
    loadCampaignOptions,
    validateForm,
    resetForm,
    setFormData
  }
}

// Composable cho single campaign step detail
export const useCampaignStepDetail = () => {
  const campaignStepStore = useCampaignStepStore()
  
  // Sử dụng store state với reactivity
  const { currentCampaignStep: campaignStep, loading, error } = storeToRefs(campaignStepStore)

  const loadCampaignStep = async (name) => {
    try {
      await campaignStepStore.getCampaignStepDetails(name)
    } catch (err) {
      console.error('Failed to load campaign step:', err)
    }
  }

  return {
    campaignStep,
    loading,
    error,
    loadCampaignStep
  }
}
