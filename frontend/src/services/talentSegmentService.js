import { 
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
} from '@/repositories/talentSegmentRepository'
import { getUsers } from '@/repositories/campaignRepository'

// Lấy danh sách phân khúc với filter
export const getFilteredTalentSegments = async (filterOptions = {}) => {
  try {
    const { type, searchText, page = 1, limit = 20 } = filterOptions
    let filters = {}
    if (type && type !== 'all') {
      filters.type = type
    }
    let options = {
      filters,
      page_length: limit,
      start: (page - 1) * limit
    }
    if (searchText) {
      options.or_filters = [
        ['title', 'like', `%${searchText}%`],
        ['description', 'like', `%${searchText}%`]
      ]
    }
    const response = await getTalentSegments(options)
    console.log('response', response)
    if (response && Array.isArray(response.data)) {
      return response
    } else {
      throw new Error('Failed to get talent segments')
    }
  } catch (error) {
    console.error('Failed to get talent segments:', error)
    throw new Error('Failed to get talent segments')
  }
}

// Lấy chi tiết phân khúc
export const getTalentSegmentDetails = async (name) => {
  try {
    const response = await getTalentSegmentByName(name)
    if (response && response.data) {
      return response.data
    } else {
      throw new Error('Failed to get talent segment details')
    }
  } catch (error) {
    console.error('Failed to get talent segment details:', error)
    throw new Error('Failed to get talent segment details')
  }
}

// Tạo phân khúc mới
export const createNewTalentSegment = async (segmentData) => {
  try {
    const response = await createTalentSegment(segmentData)
    if (response && response.data) {
      return response.data
    } else {
      throw new Error('Failed to create talent segment')
    }
  } catch (error) {
    console.error('Failed to create talent segment:', error)
    throw new Error('Failed to create talent segment')
  }
}

// Cập nhật phân khúc
export const updateTalentSegmentDetails = async (name, updateData) => {
  try {
    const response = await updateTalentSegment(name, updateData)
    if (response && response.data) {
      return response.data
    } else {
      throw new Error('Failed to update talent segment')
    }
  } catch (error) {
    console.error('Failed to update talent segment:', error)
    throw new Error('Failed to update talent segment')
  }
}

// Xóa phân khúc
export const deleteTalentSegmentById = async (name) => {
  try {
    const response = await deleteTalentSegment(name)
    if (response) {
      return true
    } else {
      throw new Error('Failed to delete talent segment')
    }
  } catch (error) {
    console.error('Failed to delete talent segment:', error)
    throw new Error('Failed to delete talent segment')
  }
}

// Lấy danh sách ứng viên trong phân khúc
export const getSegmentTalent = async (segmentId, filterOptions = {}) => {
  try {
    const response = await getTalentSegmentTalent(segmentId, filterOptions)
    if (response && response.data) {
      return response.data
    } else {
        throw new Error('Failed to get segment Talent')
    }
  } catch (error) {
    throw new Error('Failed to get segment Talent')
  }
}

// Thêm ứng viên vào phân khúc
export const addTalentToSegment = async (segmentId, talentId) => {
  try {
    await addCandidateToSegment(segmentId, talentId)
    return { success: true }
  } catch (error) {
    console.error('Failed to add talent to segment:', error)
    throw error
  }
}

// Xóa ứng viên khỏi phân khúc
export const removeTalentFromSegment = async (segmentId, talentId) => {
  try {
    const result = await removeCandidateFromSegment(segmentId, talentId)
    if (!result.success) {
      throw new Error(result.message || 'Failed to remove talent from segment')
    }
    return result
  } catch (error) {
    console.error('Failed to remove talent from segment:', error)
    throw error
  }
}

// Lấy danh sách users
export const getUserOptions = async () => {
  try {
    const response = await getUsers()
    return response.success ? (response.data || []) : []
  } catch (error) {
    console.error('Failed to get users:', error)
    return []
  }
}

// Format engagement rate để hiển thị
export const calculateEngagementRate = (candidateCount, totalInteractions = 0) => {
  if (!candidateCount || candidateCount === 0) return 0
  
  // Giả định công thức tính engagement rate
  // Trong thực tế có thể phức tạp hơn
  const baseRate = Math.min(candidateCount / 100 * 70, 95) // Base rate từ 0-95%
  const randomFactor = Math.random() * 20 - 10 // Random từ -10% đến +10%
  
  return Math.max(0, Math.min(100, Math.round(baseRate + randomFactor)))
}

// Format ngày hiển thị
export const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const now = new Date()
  const diffInMs = now - date
  const diffInHours = diffInMs / (1000 * 60 * 60)
  const diffInDays = diffInHours / 24
  
  if (diffInHours < 1) {
    return 'Just now'
  } else if (diffInHours < 24) {
    return `${Math.floor(diffInHours)} hours ago`
  } else if (diffInDays < 7) {
    return `${Math.floor(diffInDays)} days ago`
  } else {
    return date.toLocaleDateString('en-US')
  }
}

// Lấy màu sắc cho từng loại phân khúc
export const getSegmentTypeColor = (type) => {
  const colorMap = {
    'DYNAMIC': {
      gradient: 'from-blue-500 to-indigo-600',
      bg: 'bg-blue-100',
      text: 'text-blue-800',
      border: 'border-blue-100'
    },
    'MANUAL': {
      gradient: 'from-green-500 to-teal-500', 
      bg: 'bg-green-100',
      text: 'text-green-800',
      border: 'border-green-100'
    }
  }
  
  return colorMap[type] || colorMap['MANUAL']
}

// Validate dữ liệu form
export const validateTalentSegmentForm = (formData) => {
  const errors = {}
  
  if (!formData.title || !formData.title.trim()) {
    errors.title = 'Talent segment name is required'
  } else if (formData.title.length < 3) {
    errors.title = 'Talent segment name must be at least 3 characters'
  } else if (formData.title.length > 200) {
    errors.title = 'Talent segment name must be less than 200 characters'
  }

  if (formData.description && formData.description.length > 1000) {
    errors.description = 'Description must be less than 1000 characters'
  }

  if (!formData.type) {
    errors.type = 'Talent segment type is required'
  }

  // Validate criteria nếu là JSON
  if (formData.criteria) {
    try {
      if (typeof formData.criteria === 'string') {
        JSON.parse(formData.criteria)
      }
    } catch (e) {
      errors.criteria = 'Criteria must be a valid JSON'
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

// Lấy danh sách talent với thông tin pool
export const getTalentListWithPool = async (options = {}) => {
  try {
    const { page = 1, limit = 20, searchText } = options
    
    // Gọi API để lấy dữ liệu
    const response = await getTalentWithPool.fetch({
      page,
      page_size: limit,
      search_text: searchText
    })
    
    if (response && response.data) {
      return {
        data: response.data.map(talent => ({
          ...talent,
          // Format dữ liệu nếu cần
        })),
        pagination: response.pagination
      }
    } else {
      throw new Error('Failed to get talent list with pool')
    }
  } catch (error) {
    console.error('Failed to get talent list with pool:', error)
    throw error
  }
}

export default {
  getFilteredTalentSegments,
  getTalentSegmentDetails,
  createNewTalentSegment,
  updateTalentSegmentDetails,
  deleteTalentSegmentById,
  getSegmentTalent,
  addCandidateToTalentSegment,
  removeCandidateFromTalentSegment,
  getTalentListWithPool,
  getUserOptions,
  calculateEngagementRate,
  formatDate,
  getSegmentTypeColor,
  validateTalentSegmentForm
} 