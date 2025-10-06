// Đảm bảo đã import frappe client
import { call } from 'frappe-ui'

/**
 * Mira Contact Repository
 * Xử lý tất cả các API calls liên quan đến Mira Contact
 */

// Lấy danh sách talent profiles (get_list)
export const getCandidates = async (options = {}) => {
  const {
    filters = {},
    or_filters = undefined,
    fields = ['name', 'full_name', 'email', 'phone_number', 'skills', 'source', 'creation', 'modified'],
    order_by = 'modified desc',
    page_length = 12,
    start = 0
  } = options
  const data = await call('frappe.client.get_list', {
    doctype: 'Mira Contact',
    filters,
    or_filters,
    fields,
    order_by,
    limit_start: start,
    limit_page_length: page_length
  })
  const total = await call('frappe.client.get_count', {
    doctype: 'Mira Contact',
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

// Lấy thống kê talent profile (ví dụ get_list với aggregate hoặc custom logic nếu cần)
export const getCandidateStats = async () => {
  // Nếu có endpoint riêng thì giữ lại, nếu không thì dùng get_list hoặc custom frappe.client.call
  // Ví dụ: lấy tổng số theo status
  return await call('frappe.client.get_list', {
    doctype: 'Mira Contact',
    fields: ['status'],
    group_by: 'status'
  })
}

// Search talent profiles for autocomplete
export const searchCandidates = async (query, limit = 10) => {
  return await call('frappe.client.get_list', {
    doctype: 'Mira Contact',
    filters: [['full_name', 'like', `%${query}%`]],
    limit_page_length: limit
  })
}

// Get single talent profile by name
export const getCandidate = async (name) => {
  return await call('frappe.client.get', {
    doctype: 'Mira Contact',
    name
  })
}

// Create new talent profile
export const createCandidate = async (candidateData) => {
  return await call('frappe.client.insert', {
    doc: {
      doctype: 'Mira Contact',
      ...candidateData
    }
  })
}

// Update talent profile
export const updateCandidate = async (name, candidateData) => {
  return await call('frappe.client.set_value', {
    doctype: 'Mira Contact',
    name,
    fieldname: candidateData
  })
}

// Delete talent profile
export const deleteCandidate = async (name) => {
  return await call('frappe.client.delete', {
    doctype: 'Mira Contact',
    name
  })
}

// Get filter options (ví dụ lấy distinct các trường)
export const getFilterOptions = async () => {
  return {
    status: await call('frappe.client.get_list', { doctype: 'Mira Contact', fields: ['status'], distinct: true }),
    source: await call('frappe.client.get_list', { doctype: 'Mira Contact', fields: ['source'], distinct: true }),
    skills: await call('frappe.client.get_list', { doctype: 'Mira Contact', fields: ['skills'], distinct: true })
  }
} 