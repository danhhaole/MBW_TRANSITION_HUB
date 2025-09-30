import { call } from 'frappe-ui'

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
export const getTalentSegmentCandidates = async (segmentId, filters = {}) => {
  const data = await call('frappe.client.get_list', {
    doctype: 'Mira Talent Pool',
    fields: ['talent_id', 'added_at', 'added_by', 'match_score'],
    filters: { segment_id: segmentId, ...filters },
    order_by: 'added_at desc',
    page_length: 50
  })
  return { data }
}

// Thêm ứng viên vào phân khúc
export const addCandidateToSegment = async (segmentId, candidateId) => {
  return await call('frappe.client.insert', {
    doc: {
      doctype: 'Mira Talent Pool',
      segment_id: segmentId,
      talent_id: candidateId,
      added_at: new Date().toISOString(),
      added_by: 'Administrator' // TODO: lấy user hiện tại nếu cần
    }
  })
}

// Xóa ứng viên khỏi phân khúc
export const removeCandidateFromSegment = async (segmentId, candidateId) => {
  // Tìm record Mira Talent Pool
  const segments = await call('frappe.client.get_list', {
    doctype: 'Mira Talent Pool',
    fields: ['name'],
    filters: { segment_id: segmentId, talent_id: candidateId }
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