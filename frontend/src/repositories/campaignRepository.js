import { call } from 'frappe-ui'

// Lấy danh sách campaigns với pagination
export const getCampaigns = async (options = {}) => {
  try {
    const {
      page = 1,
      limit = 10,
      search = "",
      status_filter = "all",
      type_filter = "all", 
      active_filter = "all",
      order_by = "modified desc"
    } = options
    
    const result = await call('mbw_mira.api.campaign.get_campaigns_paginated', {
      page,
      limit,
      search,
      status_filter,
      type_filter,
      active_filter,
      order_by
    })
    
    return result
  } catch (error) {
    console.error('Error getting campaigns:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy danh sách campaigns',
      error,
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
}

// Lấy thống kê campaigns
export const getCampaignStats = async () => {
  try {
    const result = await call('mbw_mira.api.campaign.get_campaign_stats')
    return result
  } catch (error) {
    console.error('Error getting campaign stats:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy thống kê campaigns',
      error 
    }
  }
}

// Lấy chi tiết campaign theo name
export const getCampaignByName = async (name) => {
  try {
    const result = await call('frappe.client.get', {
      doctype: 'Campaign',
      name: name
    })
    return { success: true, message: result, data: result }
  } catch (error) {
    console.error('Error getting campaign by name:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy thông tin campaign',
      error 
    }
  }
}

// Tạo mới campaign
export const createCampaign = async (data) => {
  try {
    const doc = await call('frappe.client.insert', {
      doc: {
        doctype: 'Campaign',
        ...data
      }
    })
    return { success: true, message: doc, data: doc }
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
  try {
    const result = await call('frappe.client.set_value', {
      doctype: 'Campaign',
      name: name,
      fieldname: data
    })
    return { success: true, message: result, data: result }
  } catch (error) {
    console.error('Error updating campaign:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi cập nhật campaign',
      error 
    }
  }
}

// Xóa campaign
export const deleteCampaign = async (name) => {
  try {
    const result = await call('frappe.client.delete', {
      doctype: 'Campaign',
      name: name
    })
    return { success: true, message: result, data: result }
  } catch (error) {
    console.error('Error deleting campaign:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi xóa campaign',
      error 
    }
  }
}

// Tìm kiếm campaigns nhanh (autocomplete)
export const searchCampaigns = async (searchText, limit = 10) => {
  try {
    const result = await call('mbw_mira.api.campaign.search_campaigns', {
      query: searchText,
      limit
    })
    return result
  } catch (error) {
    console.error('Error searching campaigns:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi tìm kiếm campaigns',
      error,
      data: []
    }
  }
}

// Lấy danh sách Users cho Owner ID
export const getUsers = async () => {
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'User',
      fields: ['name', 'full_name', 'email'],
      filters: { enabled: 1 },
      order_by: 'full_name asc'
    })
    return { success: true, message: result, data: result }
  } catch (error) {
    console.error('Error getting users:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy danh sách users',
      error 
    }
  }
}

// Lấy danh sách TalentSegment
export const getTalentSegments = async () => {
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'TalentSegment',
      fields: ['name', 'title'],
      order_by: 'title asc'
    })
    return { success: true, message: result, data: result }
  } catch (error) {
    console.error('Error getting talent segments:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy danh sách talent segments',
      error 
    }
  }
} 