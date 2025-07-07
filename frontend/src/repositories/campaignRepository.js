import { createApiResource, executeApiCall, frappeClientCall, retryApiCall } from '@/utils/api'

// Lấy danh sách campaigns với pagination
export const getCampaigns = async (options = {}) => {
  const {
    page = 1,
    limit = 10,
    search = "",
    status_filter = "all",
    type_filter = "all", 
    active_filter = "all",
    order_by = "modified desc"
  } = options
  
  const apiCall = async () => {
    const resource = createApiResource({
      url: 'mbw_mira.api.campaign.get_campaigns_paginated',
      method: 'POST'
    })
    
    return await resource.fetch({
      page,
      limit,
      search,
      status_filter,
      type_filter,
      active_filter,
      order_by
    })
  }
  
  const result = await executeApiCall(apiCall, 'Có lỗi xảy ra khi lấy danh sách campaigns')
  
  if (!result.success) {
    return { 
      success: false, 
      message: result.message,
      error: result.error,
      data: [],
      pagination: {
        page: 1,
        limit: 10,
        total: 0,
        pages: 1,
        has_next: false,
        has_prev: false
      }
    }
  }
  
  return result.data
}

// Lấy thống kê campaigns
export const getCampaignStats = async () => {
  const result = await frappeClientCall({
    url: 'mbw_mira.api.campaign.get_campaign_stats',
    method: 'GET',
    errorMessage: 'Có lỗi xảy ra khi lấy thống kê campaigns'
  })
  
  return result
}

// Lấy chi tiết campaign theo name
export const getCampaignByName = async (name) => {
  const result = await frappeClientCall({
    url: 'frappe.client.get',
    method: 'POST',
    data: {
      doctype: 'Campaign',
      name: name
    },
    errorMessage: 'Có lỗi xảy ra khi lấy thông tin campaign'
  })
  
  if (result.success) {
    return { success: true, message: result.data, data: result.data }
  }
  
  return result
}

// Tạo mới campaign
export const createCampaign = async (data) => {
  const apiCall = async () => {
    const resource = createApiResource({
      url: 'frappe.client.insert',
      method: 'POST'
    })
    
    return await resource.fetch({
      doc: {
        doctype: 'Campaign',
        ...data
      }
    })
  }
  
  // Sử dụng retry logic cho create operation
  try {
    const result = await retryApiCall(apiCall, 1)
    return { success: true, message: result, data: result }
  } catch (error) {
    console.error('Error creating campaign:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi tạo campaign',
      error 
    }
  }
}

// Cập nhật campaign
export const updateCampaign = async (name, data) => {
  const result = await frappeClientCall({
    url: 'frappe.client.set_value',
    method: 'POST',
    data: {
      doctype: 'Campaign',
      name: name,
      fieldname: data
    },
    errorMessage: 'Có lỗi xảy ra khi cập nhật campaign'
  })
  
  if (result.success) {
    return { success: true, message: result.data, data: result.data }
  }
  
  return result
}

// Xóa campaign
export const deleteCampaign = async (name) => {
  const result = await frappeClientCall({
    url: 'frappe.client.delete',
    method: 'POST',
    data: {
      doctype: 'Campaign',
      name: name
    },
    errorMessage: 'Có lỗi xảy ra khi xóa campaign'
  })
  
  if (result.success) {
    return { success: true, message: result.data, data: result.data }
  }
  
  return result
}

// Tìm kiếm campaigns nhanh (autocomplete)
export const searchCampaigns = async (searchText, limit = 10) => {
  const apiCall = async () => {
    const resource = createApiResource({
      url: 'mbw_mira.api.campaign.search_campaigns',
      method: 'POST'
    })
    
    return await resource.fetch({
      query: searchText,
      limit
    })
  }
  
  const result = await executeApiCall(apiCall, 'Có lỗi xảy ra khi tìm kiếm campaigns')
  
  if (!result.success) {
    return { 
      success: false, 
      message: result.message,
      error: result.error,
      data: []
    }
  }
  
  return result.data
}

// Lấy danh sách Users cho Owner ID
export const getUsers = async () => {
  const result = await frappeClientCall({
    url: 'frappe.client.get_list',
    method: 'POST',
    data: {
      doctype: 'User',
      fields: ['name', 'full_name', 'email'],
      filters: { enabled: 1 },
      order_by: 'full_name asc'
    },
    errorMessage: 'Có lỗi xảy ra khi lấy danh sách users'
  })
  
  if (result.success) {
    return { success: true, message: result.data, data: result.data }
  }
  
  return result
}

// Lấy danh sách TalentSegment
export const getTalentSegments = async () => {
  const result = await frappeClientCall({
    url: 'frappe.client.get_list',
    method: 'POST',
    data: {
      doctype: 'TalentSegment',
      fields: ['name', 'title'],
      order_by: 'title asc'
    },
    errorMessage: 'Có lỗi xảy ra khi lấy danh sách talent segments'
  })
  
  if (result.success) {
    return { success: true, message: result.data, data: result.data }
  }
  
  return result
} 