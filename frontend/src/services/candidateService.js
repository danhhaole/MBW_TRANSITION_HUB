import * as candidateRepository from '@/repositories/candidateRepository'

/**
 * Candidate Service
 * Business logic layer cho Candidate management
 */

// Get filtered and paginated candidates
export const getFilteredCandidates = async (params = {}) => {
  try {
    const response = await candidateRepository.getCandidates(params)
    return response
  } catch (error) {
    console.error('Error in getFilteredCandidates:', error)
    throw new Error('Không thể tải danh sách ứng viên')
  }
}

// Get candidate details
export const getCandidateDetails = async (name) => {
  try {
    if (!name) throw new Error('Candidate name is required')
    
    const candidate = await candidateRepository.getCandidateByName(name)
    if (!candidate) throw new Error('Candidate not found')
    
    return candidate
  } catch (error) {
    console.error('Error in getCandidateDetails:', error)
    throw new Error('Không thể tải thông tin ứng viên')
  }
}

// Create new candidate
export const createNewCandidate = async (candidateData) => {
  try {
    // Validate required fields
    if (!candidateData.full_name?.trim()) {
      throw new Error('Tên đầy đủ là bắt buộc')
    }
    if (!candidateData.email?.trim()) {
      throw new Error('Email là bắt buộc')
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(candidateData.email)) {
      throw new Error('Email không hợp lệ')
    }
    
    // Process skills
    if (candidateData.skills && typeof candidateData.skills === 'string') {
      candidateData.skills = candidateData.skills.split(',').map(s => s.trim()).filter(s => s)
    }
    
    const newCandidate = await candidateRepository.createCandidate(candidateData)
    return newCandidate
  } catch (error) {
    console.error('Error in createNewCandidate:', error)
    throw error
  }
}

// Update candidate details
export const updateCandidateDetails = async (name, candidateData) => {
  try {
    if (!name) throw new Error('Candidate name is required')
    
    // Validate email if provided
    if (candidateData.email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(candidateData.email)) {
        throw new Error('Email không hợp lệ')
      }
    }
    
    // Process skills
    if (candidateData.skills && typeof candidateData.skills === 'string') {
      candidateData.skills = candidateData.skills.split(',').map(s => s.trim()).filter(s => s)
    }
    
    const updatedCandidate = await candidateRepository.updateCandidate(name, candidateData)
    return updatedCandidate
  } catch (error) {
    console.error('Error in updateCandidateDetails:', error)
    throw error
  }
}

// Delete candidate
export const deleteCandidateById = async (name) => {
  try {
    if (!name) throw new Error('Candidate name is required')
    
    await candidateRepository.deleteCandidate(name)
    return { success: true, message: 'Ứng viên đã được xóa thành công' }
  } catch (error) {
    console.error('Error in deleteCandidateById:', error)
    throw new Error('Không thể xóa ứng viên')
  }
}

// Search candidates
export const searchCandidatesService = async (query, limit = 10) => {
  try {
    if (!query?.trim()) return []
    
    const candidates = await candidateRepository.searchCandidates(query, limit)
    return candidates
  } catch (error) {
    console.error('Error in searchCandidatesService:', error)
    return []
  }
}

// Get filter options
export const getFilterOptionsService = async () => {
  try {
    const options = await candidateRepository.getFilterOptions()
    return options
  } catch (error) {
    console.error('Error in getFilterOptionsService:', error)
    return {
      statuses: [],
      sources: [],
      skills: []
    }
  }
}

// Get candidate statistics
export const getCandidateStatsService = async () => {
  try {
    const stats = await candidateRepository.getCandidateStats()
    return stats
  } catch (error) {
    console.error('Error in getCandidateStatsService:', error)
    return {}
  }
}

// Helper Functions

// Calculate engagement score based on various factors
export const calculateEngagementScore = (candidate) => {
  let score = 0
  
  // Base score for having complete profile
  if (candidate.full_name) score += 20
  if (candidate.email) score += 20
  if (candidate.phone) score += 10
  if (candidate.location) score += 10
  if (candidate.current_position) score += 15
  
  // Skills score
  const skills = processSkills(candidate.skills)
  if (skills.length > 0) score += Math.min(skills.length * 5, 25)
  
  // Experience score
  if (candidate.experience_years) {
    if (candidate.experience_years >= 5) score += 10
    else if (candidate.experience_years >= 2) score += 5
  }
  
  return Math.min(score, 100)
}

// Format talent pool status for display
export const formatCandidateStatus = (status) => {
  const statusMap = {
    'Active': { text: 'Hoạt động', color: 'green' },
    'Inactive': { text: 'Không hoạt động', color: 'grey' }
  }
  
  return statusMap[status] || { text: status, color: 'grey' }
}

// Format date for display
export const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const options = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  
  return date.toLocaleDateString('vi-VN', options)
}

// Format relative time (e.g., "2 hours ago")
export const formatRelativeTime = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'vừa xong'
  if (diffInHours === 1) return '1 giờ trước'
  if (diffInHours < 24) return `${diffInHours} giờ trước`
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays === 1) return '1 ngày trước'
  if (diffInDays < 7) return `${diffInDays} ngày trước`
  
  const diffInWeeks = Math.floor(diffInDays / 7)
  if (diffInWeeks === 1) return '1 tuần trước'
  if (diffInWeeks < 4) return `${diffInWeeks} tuần trước`
  
  return formatDate(dateString)
}

// Get avatar color based on name
export const getAvatarColor = (name) => {
  const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
  const hash = name?.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0) || 0
  return colors[Math.abs(hash) % colors.length]
}

// Get avatar text from name
export const getAvatarText = (name) => {
  if (!name) return ''
  return name.split(' ').map(word => word[0]).join('').toUpperCase().substring(0, 2)
}

// Get status chip color
export const getStatusChipColor = (status) => {
  const colorMap = {
    'Active': 'green',
    'Inactive': 'grey'
  }
  return colorMap[status] || 'grey'
}

// Validate talent pool form data
export const validateCandidateForm = (data) => {
  const errors = {}
  
  if (!data.full_name?.trim()) {
    errors.full_name = 'Tên đầy đủ là bắt buộc'
  }
  
  if (!data.email?.trim()) {
    errors.email = 'Email là bắt buộc'
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(data.email)) {
      errors.email = 'Email không hợp lệ'
    }
  }
  
  if (data.phone && !/^[+\d\s\-()]+$/.test(data.phone)) {
    errors.phone = 'Số điện thoại không hợp lệ'
  }
  
  if (data.experience_years && (isNaN(data.experience_years) || data.experience_years < 0)) {
    errors.experience_years = 'Số năm kinh nghiệm không hợp lệ'
  }

  console.log(errors)
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  }
}

const tryParseWeirdJsonArray = (s) => {
  // chỉ xử lý khi mở đầu bằng [ hoặc { để tránh split thường
  if (!/^\s*[\[{]/.test(s)) return null
  try {
    // API trả về ['a','b'] -> đổi ' thành "
    const fixed = s.replace(/'/g, '"')
    const parsed = JSON.parse(fixed)
    return parsed
  } catch {
    return null
  }
}

// Process skills array/string for display (returns array)
export const processSkills = (skills) => {
  if (!skills) return []

  const clean = (arr) =>
    arr
      .filter(v => v != null && v !== '')
      .map(v => String(v).trim().replace(/^['"]|['"]$/g, '')) // bỏ quote đầu/cuối
      .filter(v => v && v !== '[object Object]')

  // Case A: Array
  if (Array.isArray(skills)) {
    // Mảng bị vỡ từ chuỗi JSON: ["['react'", "'test'", "'abc']"]
    if (skills.length && /^\s*\[/.test(String(skills[0]))) {
      try {
        const joined = skills.join(',')                  // "['react','test','abc']"
        const fixed  = joined.replace(/'/g, '"')         // '["react","test","abc"]'
        const parsed = JSON.parse(fixed)
        return clean(parsed)
      } catch { /* fallthrough */ }
    }
    return clean(skills)
  }

  // Case B: String
  if (typeof skills === 'string') {
    const s = skills.trim()
    try {
      const parsed = JSON.parse(s) // chuẩn: ["react","test"]
      if (Array.isArray(parsed)) return clean(parsed)
    } catch { /* ignore */ }
    return clean(s.split(','))
  }

  // Case C: Object
  if (typeof skills === 'object') return clean(Object.values(skills))

  return []
}



// Convert skills array to string for backend storage (returns string)
export const skillsToString = (skills) =>
  processSkills(skills).join(', ')

// Get engagement color based on score
export const getEngagementColor = (score) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  if (score >= 40) return 'orange'
  return 'error'
}

export default {
  getFilteredCandidates,
  getCandidateDetails,
  createNewCandidate,
  updateCandidateDetails,
  deleteCandidateById,
  searchCandidatesService,
  getFilterOptionsService,
  getCandidateStatsService,
  calculateEngagementScore,
  formatCandidateStatus,
  formatDate,
  formatRelativeTime,
  getAvatarColor,
  getAvatarText,
  getStatusChipColor,
  validateCandidateForm,
  processSkills,
  skillsToString,
  getEngagementColor
} 