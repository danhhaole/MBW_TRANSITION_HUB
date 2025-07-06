import * as campaignStepRepository from '@/repositories/campaignStepRepository'

/**
 * Campaign Step Service
 * Business logic layer cho Campaign Step management
 */

// Get filtered and paginated campaign steps
export const getFilteredCampaignSteps = async (params = {}) => {
  try {
    const response = await campaignStepRepository.getCampaignSteps(params)
    return response
  } catch (error) {
    console.error('Error in getFilteredCampaignSteps:', error)
    throw new Error('Không thể tải danh sách bước chiến dịch')
  }
}

// Get campaign step details
export const getCampaignStepDetails = async (name) => {
  try {
    if (!name) throw new Error('Campaign step name is required')
    
    const campaignStep = await campaignStepRepository.getCampaignStepByName(name)
    if (!campaignStep) throw new Error('Campaign step not found')
    
    return campaignStep
  } catch (error) {
    console.error('Error in getCampaignStepDetails:', error)
    throw new Error('Không thể tải thông tin bước chiến dịch')
  }
}

// Create new campaign step
export const createNewCampaignStep = async (campaignStepData) => {
  try {
    // Validate required fields
    if (!campaignStepData.campaign_step_name?.trim()) {
      throw new Error('Tên bước chiến dịch là bắt buộc')
    }
    if (!campaignStepData.campaign?.trim()) {
      throw new Error('Chiến dịch là bắt buộc')
    }
    if (!campaignStepData.action_type?.trim()) {
      throw new Error('Loại hành động là bắt buộc')
    }
    
    // Validate step order
    if (campaignStepData.step_order && campaignStepData.step_order < 1) {
      throw new Error('Thứ tự bước phải lớn hơn 0')
    }
    
    // Validate delay
    if (campaignStepData.delay_in_days && campaignStepData.delay_in_days < 0) {
      throw new Error('Số ngày chờ không được âm')
    }
    
    const result = await campaignStepRepository.createCampaignStep(campaignStepData)
    
    if (!result.success) {
      throw new Error(result.error || 'Không thể tạo bước chiến dịch')
    }
    
    return result
  } catch (error) {
    console.error('Error in createNewCampaignStep:', error)
    throw error
  }
}

// Update campaign step
export const updateCampaignStep = async (name, campaignStepData) => {
  try {
    if (!name) throw new Error('Campaign step name is required')
    
    // Validate required fields
    if (!campaignStepData.campaign_step_name?.trim()) {
      throw new Error('Tên bước chiến dịch là bắt buộc')
    }
    if (!campaignStepData.campaign?.trim()) {
      throw new Error('Chiến dịch là bắt buộc')
    }
    if (!campaignStepData.action_type?.trim()) {
      throw new Error('Loại hành động là bắt buộc')
    }
    
    // Validate step order
    if (campaignStepData.step_order && campaignStepData.step_order < 1) {
      throw new Error('Thứ tự bước phải lớn hơn 0')
    }
    
    // Validate delay
    if (campaignStepData.delay_in_days && campaignStepData.delay_in_days < 0) {
      throw new Error('Số ngày chờ không được âm')
    }
    
    const result = await campaignStepRepository.updateCampaignStep(name, campaignStepData)
    
    if (!result.success) {
      throw new Error(result.error || 'Không thể cập nhật bước chiến dịch')
    }
    
    return result
  } catch (error) {
    console.error('Error in updateCampaignStep:', error)
    throw error
  }
}

// Delete campaign step
export const deleteCampaignStep = async (name) => {
  try {
    if (!name) throw new Error('Campaign step name is required')
    
    const result = await campaignStepRepository.deleteCampaignStep(name)
    
    if (!result.success) {
      throw new Error(result.error || 'Không thể xóa bước chiến dịch')
    }
    
    return result
  } catch (error) {
    console.error('Error in deleteCampaignStep:', error)
    throw error
  }
}

// Get campaign step statistics
export const getCampaignStepStats = async () => {
  try {
    const stats = await campaignStepRepository.getCampaignStepStats()
    return stats
  } catch (error) {
    console.error('Error in getCampaignStepStats:', error)
    return {}
  }
}

// Search campaign steps
export const searchCampaignSteps = async (query, limit = 10) => {
  try {
    if (!query?.trim()) return []
    
    const results = await campaignStepRepository.searchCampaignSteps(query, limit)
    return results
  } catch (error) {
    console.error('Error in searchCampaignSteps:', error)
    return []
  }
}

// Get filter options
export const getFilterOptions = async () => {
  try {
    const options = await campaignStepRepository.getCampaignStepFilterOptions()
    return options
  } catch (error) {
    console.error('Error in getFilterOptions:', error)
    return {}
  }
}

// Get steps by campaign
export const getStepsByCampaign = async (campaign) => {
  try {
    if (!campaign) throw new Error('Campaign is required')
    
    const result = await campaignStepRepository.getStepsByCampaign(campaign)
    
    if (!result.success) {
      throw new Error(result.error || 'Không thể tải danh sách bước')
    }
    
    return result.data || []
  } catch (error) {
    console.error('Error in getStepsByCampaign:', error)
    throw error
  }
}

// Reorder campaign steps
export const reorderSteps = async (campaign, stepOrders) => {
  try {
    if (!campaign) throw new Error('Campaign is required')
    if (!stepOrders || !Array.isArray(stepOrders)) {
      throw new Error('Step orders array is required')
    }
    
    const result = await campaignStepRepository.reorderCampaignSteps(campaign, stepOrders)
    
    if (!result.success) {
      throw new Error(result.error || 'Không thể sắp xếp lại thứ tự bước')
    }
    
    return result
  } catch (error) {
    console.error('Error in reorderSteps:', error)
    throw error
  }
}

// Get campaigns for dropdown
export const getCampaignOptions = async () => {
  try {
    const campaigns = await campaignStepRepository.getCampaigns()
    return campaigns
  } catch (error) {
    console.error('Error in getCampaignOptions:', error)
    return []
  }
}

// Get action types
export const getActionTypes = async () => {
  try {
    const actionTypes = await campaignStepRepository.getActionTypes()
    return actionTypes
  } catch (error) {
    console.error('Error in getActionTypes:', error)
    return []
  }
}

// Format campaign step data for display
export const formatCampaignStepData = (campaignStep) => {
  if (!campaignStep) return null
  
  return {
    ...campaignStep,
    action_type_label: getActionTypeLabel(campaignStep.action_type),
    delay_text: formatDelayText(campaignStep.delay_in_days),
    template_preview: campaignStep.template ? 
      (campaignStep.template.length > 100 ? 
        campaignStep.template.substring(0, 100) + '...' : 
        campaignStep.template) : 
      'Không có template'
  }
}

// Get action type label
export const getActionTypeLabel = (actionType) => {
  const actionTypeMap = {
    'SEND_EMAIL': 'Gửi Email',
    'SEND_SMS': 'Gửi SMS',
    'MANUAL_CALL': 'Gọi điện thủ công',
    'MANUAL_TASK': 'Tác vụ thủ công'
  }
  
  return actionTypeMap[actionType] || actionType
}

// Format delay text
export const formatDelayText = (delayInDays) => {
  if (!delayInDays || delayInDays === 0) {
    return 'Ngay lập tức'
  }
  
  if (delayInDays === 1) {
    return '1 ngày'
  }
  
  return `${delayInDays} ngày`
}

// Validate campaign step data
export const validateCampaignStepData = (data) => {
  const errors = []
  
  if (!data.campaign_step_name?.trim()) {
    errors.push('Tên bước chiến dịch là bắt buộc')
  }
  
  if (!data.campaign?.trim()) {
    errors.push('Chiến dịch là bắt buộc')
  }
  
  if (!data.action_type?.trim()) {
    errors.push('Loại hành động là bắt buộc')
  }
  
  if (data.step_order && data.step_order < 1) {
    errors.push('Thứ tự bước phải lớn hơn 0')
  }
  
  if (data.delay_in_days && data.delay_in_days < 0) {
    errors.push('Số ngày chờ không được âm')
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

// Get campaign step form fields
export const getCampaignStepFormFields = () => {
  return [
    {
      name: 'campaign_step_name',
      label: 'Tên bước',
      type: 'text',
      required: true,
      placeholder: 'Nhập tên bước chiến dịch'
    },
    {
      name: 'campaign',
      label: 'Chiến dịch',
      type: 'select',
      required: true,
      options: [] // Will be populated by getCampaignOptions
    },
    {
      name: 'step_order',
      label: 'Thứ tự bước',
      type: 'number',
      required: true,
      min: 1
    },
    {
      name: 'action_type',
      label: 'Loại hành động',
      type: 'select',
      required: true,
      options: [] // Will be populated by getActionTypes
    },
    {
      name: 'delay_in_days',
      label: 'Số ngày chờ',
      type: 'number',
      required: false,
      min: 0,
      defaultValue: 0
    },
    {
      name: 'template',
      label: 'Template',
      type: 'textarea',
      required: false,
      placeholder: 'Nhập template cho bước này'
    }
  ]
}
