import { createResource } from 'frappe-ui'

// Lấy danh sách TalentSegment với filter
export const getTalentSegments = async (filters = {}) => {
  try {
    const resource = createResource({
      url: 'frappe.client.get_list',
      method: 'POST',
      auto: false
    })
    
    const params = {
      doctype: 'TalentSegment',
      fields: ['name', 'title', 'description', 'type', 'candidate_count', 'owner_id', 'creation', 'modified', "criteria"],
      order_by: 'modified desc',
      limit_page_length: 50
    }

    if (Object.keys(filters).length > 0) {
      params.filters = filters
    }

    const result = await resource.fetch(params)
    return { success: true, message: 'Lấy danh sách phân khúc thành công', data: result }
  } catch (error) {
    console.error('Error getting talent segments:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy danh sách phân khúc',
      error 
    }
  }
}

// Lấy chi tiết TalentSegment
export const getTalentSegmentByName = async (name) => {
  try {
    const resource = createResource({
      url: 'frappe.client.get',
      method: 'POST',
      auto: false
    })
    
    const result = await resource.fetch({
      doctype: 'TalentSegment',
      name: name
    })
    return { success: true, message: 'Lấy thông tin phân khúc thành công', data: result }
  } catch (error) {
    console.error('Error getting talent segment:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Không tìm thấy phân khúc',
      error 
    }
  }
}

// Tạo TalentSegment mới
export const createTalentSegment = async (data) => {
  try {
    const resource = createResource({
      url: 'frappe.client.insert',
      method: 'POST',
      auto: false
    })
    
    const result = await resource.fetch({
      doc: {
        doctype: 'TalentSegment',
        ...data
      }
    })
    return { success: true, message: 'Tạo phân khúc thành công', data: result }
  } catch (error) {
    console.error('Error creating talent segment:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi tạo phân khúc',
      error 
    }
  }
}

// Cập nhật TalentSegment
export const updateTalentSegment = async (name, data) => {
  try {
    const resource = createResource({
      url: 'frappe.client.set_value',
      method: 'POST',
      auto: false
    })
    
    const result = await resource.fetch({
      doctype: 'TalentSegment',
      name: name,
      fieldname: data
    })
    return { success: true, message: 'Cập nhật phân khúc thành công', data: result }
  } catch (error) {
    console.error('Error updating talent segment:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi cập nhật phân khúc',
      error 
    }
  }
}

// Xóa TalentSegment
export const deleteTalentSegment = async (name) => {
  try {
    const resource = createResource({
      url: 'frappe.client.delete',
      method: 'POST',
      auto: false
    })
    
    await resource.fetch({
      doctype: 'TalentSegment',
      name: name
    })
    return { success: true, message: 'Xóa phân khúc thành công' }
  } catch (error) {
    console.error('Error deleting talent segment:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi xóa phân khúc',
      error 
    }
  }
}

// Tìm kiếm TalentSegment
export const searchTalentSegments = async (searchText) => {
  try {
    const resource = createResource({
      url: 'frappe.client.get_list',
      method: 'POST',
      auto: false
    })
    
    const result = await resource.fetch({
      doctype: 'TalentSegment',
      fields: ['name', 'criteria', 'title', 'description', 'type', 'candidate_count', 'owner_id', 'creation', 'modified'],
      filters: [
        ['title', 'like', `%${searchText}%`],
        // ['description', 'like', `%${searchText}%`]
      ],
      order_by: 'modified desc',
      limit_page_length: 50
    })
    return { success: true, message: 'Tìm kiếm thành công', data: result }
  } catch (error) {
    console.error('Error searching talent segments:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi tìm kiếm',
      error 
    }
  }
}

// Lấy danh sách ứng viên trong phân khúc
export const getTalentSegmentCandidates = async (segmentId, filters = {}) => {
  try {
    const resource = createResource({
      url: 'frappe.client.get_list',
      method: 'POST',
      auto: false
    })
    
    const params = {
      doctype: 'TalentProfilesSegment',
      fields: ['talent_id', 'added_at', 'added_by'],
      filters: { segment_id: segmentId },
      order_by: 'added_at desc',
      limit_page_length: 50
    }

    if (Object.keys(filters).length > 0) {
      params.filters = { ...params.filters, ...filters }
    }

    const result = await resource.fetch(params)
    
    // Lấy thông tin chi tiết ứng viên nếu có kết quả
    if (result && result.length > 0) {
      const candidateIds = result.map(item => item.talent_id)
      const candidateResource = createResource({
        url: 'frappe.client.get_list',
        method: 'POST',
        auto: false
      })
      
      const candidates = await candidateResource.fetch({
        doctype: 'TalentProfiles',
        fields: ['name', 'full_name', 'email', 'phone', 'skills', 'status'],
        filters: [['name', 'in', candidateIds]]
      })
      
      // Kết hợp thông tin
      const combinedData = result.map(segmentCandidate => {
        const candidate = candidates.find(c => c.name === segmentCandidate.talent_id)
        return {
          ...segmentCandidate,
          candidate: candidate
        }
      })
      
      return { success: true, message: 'Lấy danh sách ứng viên thành công', data: combinedData }
    }

    return { success: true, message: 'Lấy danh sách ứng viên thành công', data: [] }
  } catch (error) {
    console.error('Error getting talent segment candidates:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi lấy danh sách ứng viên',
      error 
    }
  }
}

// Thêm ứng viên vào phân khúc
export const addCandidateToSegment = async (segmentId, candidateId) => {
  try {
    const resource = createResource({
      url: 'frappe.client.insert',
      method: 'POST',
      auto: false
    })
    
    const result = await resource.fetch({
      doc: {
        doctype: 'TalentProfilesSegment',
        segment_id: segmentId,
        talent_id: candidateId,
        added_at: new Date().toISOString(),
        added_by: 'Administrator' // TODO: Get current user
      }
    })
    return { success: true, message: 'Thêm ứng viên vào phân khúc thành công', data: result }
  } catch (error) {
    console.error('Error adding candidate to segment:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi thêm ứng viên',
      error 
    }
  }
}

// Xóa ứng viên khỏi phân khúc
export const removeCandidateFromSegment = async (segmentId, candidateId) => {
  try {
    // Tìm record TalentProfilesSegment
    const resource = createResource({
      url: 'frappe.client.get_list',
      method: 'POST',
      auto: false
    })
    
    const segments = await resource.fetch({
      doctype: 'TalentProfilesSegment',
      fields: ['name'],
      filters: {
        segment_id: segmentId,
        talent_id: candidateId
      }
    })

    if (segments && segments.length > 0) {
      const deleteResource = createResource({
        url: 'frappe.client.delete',
        method: 'POST',
        auto: false
      })
      
      await deleteResource.fetch({
        doctype: 'TalentProfilesSegment',
        name: segments[0].name
      })
      return { success: true, message: 'Xóa ứng viên khỏi phân khúc thành công' }
    } else {
      return { success: false, message: 'Không tìm thấy ứng viên trong phân khúc' }
    }
  } catch (error) {
    console.error('Error removing candidate from segment:', error)
    return { 
      success: false, 
      message: error.messages?.[0] || 'Có lỗi xảy ra khi xóa ứng viên',
      error 
    }
  }
} 