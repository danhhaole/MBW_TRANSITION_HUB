import { call } from 'frappe-ui'
import { createResource } from 'frappe-ui'

// Lấy danh sách Mira Segment với filter, phân trang, tìm kiếm nhiều trường dùng or_filters
export const getTalentSegments = async (options = {}) => {
  const {
    filters = {},
    or_filters = undefined,
    fields = ['name', 'title', 'description', 'type', 'candidate_count', 'owner_id', 'creation', 'modified', 'criteria'],
    order_by = 'modified desc',
    page_length = 20,
    start = 0
  } = options
  const data = await call('frappe.client.get_list', {
    doctype: 'Mira Segment',
    filters,
    or_filters,
    fields,
    order_by,
    limit_start: start,
    limit_page_length: page_length
  })
  const total = await call('frappe.client.get_count', {
    doctype: 'Mira Segment',
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

// Lấy chi tiết Mira Segment
export const getTalentSegmentByName = async (name) => {
  return await call('frappe.client.get', {
    doctype: 'Mira Segment',
    name
  })
}

// Tạo Mira Segment mới
export const createTalentSegment = async (data) => {
  return await call('frappe.client.insert', {
    doc: {
      doctype: 'Mira Segment',
      ...data
    }
  })
}

// Cập nhật Mira Segment
export const updateTalentSegment = async (name, data) => {
  return await call('frappe.client.set_value', {
    doctype: 'Mira Segment',
    name,
    fieldname: data
  })
}

// Xóa Mira Segment
export const deleteTalentSegment = async (name) => {
  return await call('frappe.client.delete', {
    doctype: 'Mira Segment',
    name
  })
}

// Tìm kiếm Mira Segment theo nhiều trường (or_filters)
export const searchTalentSegments = async (searchText) => {
  const or_filters = [
    ['title', 'like', `%${searchText}%`],
    ['description', 'like', `%${searchText}%`]
  ]
  return await getTalentSegments({ or_filters })
}

// Lấy danh sách ứng viên trong phân khúc
export const getTalentSegmentTalent = async (segmentId, filters = {}) => {
  const { page = 1, page_size = 20 } = filters
  const start = (page - 1) * page_size
  
  const data = await call('frappe.client.get_list', {
    doctype: 'Mira Talent Pool',
    fields: ['talent_id', 'added_at', 'added_by'],
    filters: { segment_id: segmentId },
    limit_start: start,
    limit_page_length: page_size
  })
  
  const total = await call('frappe.client.get_count', {
    doctype: 'Mira Talent Pool',
    filters: { segment_id: segmentId }
  })
  
  return {
    data: data || [],
    pagination: {
      total: total || 0,
      page: page,
      limit: page_size,
      pages: Math.ceil((total || 0) / page_size),
      has_next: (start + page_size) < total,
      has_prev: start > 0,
      showing_from: start + 1,
      showing_to: Math.min(start + page_size, total)
    }
  }
}

// Lấy danh sách talent với thông tin pool
export const getTalentWithPool = createResource({
  url: 'mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.get_talent_with_pool',
  method: 'GET',
  auto: false,
  onSuccess: (data) => {
    return {
      data: data.data || [],
      pagination: {
        total: data.total || 0,
        page: data.page || 1,
        limit: data.page_size || 20,
        pages: data.total_pages || 1,
        has_next: (data.page || 1) < (data.total_pages || 1),
        has_prev: (data.page || 1) > 1,
        showing_from: ((data.page || 1) - 1) * (data.page_size || 20) + 1,
        showing_to: Math.min((data.page || 1) * (data.page_size || 20), data.total || 0)
      }
    }
  }
})

// Thêm ứng viên vào phân khúc
export const addCandidateToSegment = async (segmentId, talentId) => {
  return await call('frappe.client.insert', {
    doc: {
      doctype: 'Mira Talent Pool',
      segment_id: segmentId,
      talent_id: talentId,
      added_at: new Date().toISOString(),
      added_by: 'Administrator' // TODO: lấy user hiện tại nếu cần
    }
  })
}

// Xóa ứng viên khỏi phân khúc
export const removeCandidateFromSegment = async (segmentId, talentId) => {
  // Tìm record Mira Talent Pool
  const segments = await call('frappe.client.get_list', {
    doctype: 'Mira Talent Pool',
    fields: ['name'],
    filters: { segment_id: segmentId, talent_id: talentId }
  })
  if (segments && segments.length > 0) {
    await call('frappe.client.delete', {
      doctype: 'Mira Talent Pool',
      name: segments[0].name
    })
    return { success: true }
  } else {
    return { success: false, message: 'Không tìm thấy ứng viên trong phân khúc' }
  }
}

export default {
  getTalentSegments,
  getTalentSegmentByName,
  createTalentSegment,
  updateTalentSegment,
  deleteTalentSegment,
  searchTalentSegments,
  getTalentSegmentTalent,
  addCandidateToSegment,
  removeCandidateFromSegment,
  getTalentWithPool
}