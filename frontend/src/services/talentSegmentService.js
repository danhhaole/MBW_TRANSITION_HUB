import { 
  getTalentSegments, 
  getTalentSegmentByName, 
  createTalentSegment, 
  updateTalentSegment, 
  deleteTalentSegment,
  searchTalentSegments,
  getTalentSegmentCandidates,
  addCandidateToSegment,
  removeCandidateFromSegment
} from '@/repositories/talentSegmentRepository'
import { getUsers } from '@/repositories/campaignRepository'

// Lấy danh sách phân khúc với filter
export const getFilteredTalentSegments = async (filterOptions = {}) => {
  try {
    const { type, searchText } = filterOptions
    
    let filters = {}
    if (type && type !== 'all') {
      filters.type = type
    }
    
    let response
    if (searchText) {
      response = await searchTalentSegments(searchText)
      // Áp dụng thêm filters nếu có
      if (response.success && response.data && type !== 'all') {
        response.data = response.data.filter(segment => {
          return type === 'all' || segment.type === type
        })
      }
    } else {
      response = await getTalentSegments(filters)
    }

    console.log('Service response:', response)
    
    if (response.success) {
      return response.data || []
    } else {
      throw new Error(response.message || 'Không thể tải danh sách phân khúc')
    }
  } catch (error) {
    console.error('Failed to get talent segments:', error)
    throw new Error('Không thể tải danh sách phân khúc')
  }
}

// Lấy chi tiết phân khúc
export const getTalentSegmentDetails = async (name) => {
  try {
    const response = await getTalentSegmentByName(name)
    if (response.success) {
      return response.data
    } else {
      throw new Error(response.message || 'Không thể tải thông tin phân khúc')
    }
  } catch (error) {
    console.error('Failed to get talent segment details:', error)
    throw new Error('Không thể tải thông tin phân khúc')
  }
}

// Tạo phân khúc mới
export const createNewTalentSegment = async (segmentData) => {
  try {
    const response = await createTalentSegment(segmentData)
    if (response.success) {
      return response.data
    } else {
      throw new Error(response.message || 'Không thể tạo phân khúc')
    }
  } catch (error) {
    console.error('Failed to create talent segment:', error)
    throw new Error('Không thể tạo phân khúc')
  }
}

// Cập nhật phân khúc
export const updateTalentSegmentDetails = async (name, updateData) => {
  try {
    const response = await updateTalentSegment(name, updateData)
    if (response.success) {
      return response.data
    } else {
      throw new Error(response.message || 'Không thể cập nhật phân khúc')
    }
  } catch (error) {
    console.error('Failed to update talent segment:', error)
    throw new Error('Không thể cập nhật phân khúc')
  }
}

// Xóa phân khúc
export const deleteTalentSegmentById = async (name) => {
  try {
    const response = await deleteTalentSegment(name)
    if (response.success) {
      return true
    } else {
      throw new Error(response.message || 'Không thể xóa phân khúc')
    }
  } catch (error) {
    console.error('Failed to delete talent segment:', error)
    throw new Error('Không thể xóa phân khúc')
  }
}

// Lấy danh sách ứng viên trong phân khúc
export const getSegmentCandidates = async (segmentId, filterOptions = {}) => {
  try {
    const response = await getTalentSegmentCandidates(segmentId, filterOptions)
    if (response.success) {
      return response.data || []
    } else {
      throw new Error(response.message || 'Không thể tải danh sách ứng viên')
    }
  } catch (error) {
    console.error('Failed to get segment candidates:', error)
    throw new Error('Không thể tải danh sách ứng viên')
  }
}

// Thêm ứng viên vào phân khúc
export const addCandidateToTalentSegment = async (segmentId, candidateId) => {
  try {
    const response = await addCandidateToSegment(segmentId, candidateId)
    if (response.success) {
      return response.data
    } else {
      throw new Error(response.message || 'Không thể thêm ứng viên')
    }
  } catch (error) {
    console.error('Failed to add candidate to segment:', error)
    throw new Error('Không thể thêm ứng viên')
  }
}

// Xóa ứng viên khỏi phân khúc
export const removeCandidateFromTalentSegment = async (segmentId, candidateId) => {
  try {
    const response = await removeCandidateFromSegment(segmentId, candidateId)
    if (response.success) {
      return true
    } else {
      throw new Error(response.message || 'Không thể xóa ứng viên')
    }
  } catch (error) {
    console.error('Failed to remove candidate from segment:', error)
    throw new Error('Không thể xóa ứng viên')
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
    return 'Vừa xong'
  } else if (diffInHours < 24) {
    return `${Math.floor(diffInHours)} giờ trước`
  } else if (diffInDays < 7) {
    return `${Math.floor(diffInDays)} ngày trước`
  } else {
    return date.toLocaleDateString('vi-VN')
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
    errors.title = 'Tên phân khúc là bắt buộc'
  } else if (formData.title.length < 3) {
    errors.title = 'Tên phân khúc phải có ít nhất 3 ký tự'
  } else if (formData.title.length > 200) {
    errors.title = 'Tên phân khúc không được quá 200 ký tự'
  }

  if (formData.description && formData.description.length > 1000) {
    errors.description = 'Mô tả không được quá 1000 ký tự'
  }

  if (!formData.type) {
    errors.type = 'Loại phân khúc là bắt buộc'
  }

  // Validate criteria nếu là JSON
  if (formData.criteria) {
    try {
      if (typeof formData.criteria === 'string') {
        JSON.parse(formData.criteria)
      }
    } catch (e) {
      errors.criteria = 'Tiêu chí phải là JSON hợp lệ'
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

export default {
  getFilteredTalentSegments,
  getTalentSegmentDetails,
  createNewTalentSegment,
  updateTalentSegmentDetails,
  deleteTalentSegmentById,
  getSegmentCandidates,
  addCandidateToTalentSegment,
  removeCandidateFromTalentSegment,
  getUserOptions,
  calculateEngagementRate,
  formatDate,
  getSegmentTypeColor,
  validateTalentSegmentForm
} 