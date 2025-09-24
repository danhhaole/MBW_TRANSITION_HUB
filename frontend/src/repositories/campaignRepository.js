import { call } from 'frappe-ui'

// Lấy danh sách campaigns với filter, phân trang, tìm kiếm nhiều trường dùng or_filters
export const getCampaigns = async (options = {}) => {
  const {
    filters = {},
    or_filters = undefined,
    fields = ['name', 'campaign_name', 'description', 'is_active', 'owner_id', 'start_date', 'end_date', 'type', 'status', 'target_segment', 'creation', 'modified', 'current', 'total', 'job_opening'],
    order_by = 'modified desc',
    page_length = 20,
    start = 0
  } = options
  const data = await call('frappe.client.get_list', {
    doctype: 'Campaign',
    filters,
    or_filters,
    fields,
    order_by,
    limit_start: start,
    limit_page_length: page_length
  })
  const total = await call('frappe.client.get_count', {
    doctype: 'Campaign',
    filters
  })
  return {
    data: data || [],
    pagination: {
      total: total || 0,
      page: Math.floor(start / page_length) + 1,
      limit: page_length,
      pages: Math.ceil((total || 0) / page_length),
      has_next: (start + page_length) < total,
      has_prev: start > 0,
      showing_from: start + 1,
      showing_to: Math.min(start + page_length, total)
    }
  }
}

// Lấy thống kê campaigns
export const getCampaignStats = async () => {
  const result = await call('frappe.client.get_list', {
    doctype: 'Campaign',
    fields: ['name', 'campaign_name', 'description', 'is_active', 'owner_id', 'start_date', 'end_date', 'type', 'status', 'target_segment', 'creation', 'modified', 'current', 'total', 'job_opening'],
    filters: { enabled: 1 },
    order_by: 'full_name asc'
  })
  
  return result
}

// Lấy chi tiết campaign
export const getCampaignByName = async (name) => {
  return await call('frappe.client.get', {
    doctype: 'Campaign',
    name
  })
}

// Tạo mới campaign
export const createCampaign = async (data) => {
  return await call('frappe.client.insert', {
    doc: {
      doctype: 'Campaign',
      ...data
    }
  })
}

// Cập nhật campaign
export const updateCampaign = async (name, data) => {
  return await call('frappe.client.set_value', {
    doctype: 'Campaign',
    name,
    fieldname: data
  })
}

// Xóa campaign
export const deleteCampaign = async (name) => {
  return await call('frappe.client.delete', {
    doctype: 'Campaign',
    name
  })
}

// Tìm kiếm campaigns theo nhiều trường (or_filters)
export const searchCampaigns = async (searchText) => {
  const or_filters = [
    ['campaign_name', 'like', `%${searchText}%`],
    ['description', 'like', `%${searchText}%`]
  ]
  return await getCampaigns({ or_filters })
}

// Lấy danh sách users cho Owner ID
export const getUsers = async () => {
  return await call('frappe.client.get_list', {
    doctype: 'User',
    fields: ['name', 'full_name', 'email'],
    filters: { enabled: 1 },
    order_by: 'full_name asc'
  })
}

// Lấy danh sách TalentSegment
export const getTalentSegments = async () => {
  return await call('frappe.client.get_list', {
    doctype: 'TalentSegment',
    fields: ['name', 'title'],
    order_by: 'title asc'
  })
}

// Thêm: Lấy danh sách Job Opening
export const getJobOpenings = async () => {
  return await call('frappe.client.get_list', {
    doctype: 'JobOpening',
    fields: ['name', 'job_title'],
    order_by: 'modified desc'
  })
} 