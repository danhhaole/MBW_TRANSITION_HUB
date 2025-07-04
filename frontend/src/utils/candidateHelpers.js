// Helper functions for candidate components

export const calculateEngagementScore = (candidate) => {
  if (!candidate) return 0
  
  let score = 20 // Base score
  
  // Add points for complete profile
  if (candidate.full_name) score += 10
  if (candidate.email) score += 10
  if (candidate.phone) score += 10
  if (candidate.headline) score += 10
  if (candidate.skills && candidate.skills.length > 0) score += 15
  if (candidate.cv_original_url) score += 10
  if (candidate.ai_summary) score += 15
  
  return Math.min(100, score)
}

export const formatCandidateStatus = (status) => {
  const statusMap = {
    'NEW': { text: 'Mới', color: 'blue' },
    'SOURCED': { text: 'Đã tìm thấy', color: 'orange' },
    'NURTURING': { text: 'Đang chăm sóc', color: 'purple' },
    'ENGAGED': { text: 'Đã tương tác', color: 'green' },
    'ARCHIVED': { text: 'Đã lưu trữ', color: 'grey' }
  }
  
  return statusMap[status] || { text: status, color: 'grey' }
}

export const getAvatarColor = (name) => {
  if (!name) return 'grey'
  
  const colors = [
    'red', 'pink', 'purple', 'deep-purple', 'indigo', 
    'blue', 'light-blue', 'cyan', 'teal', 'green',
    'light-green', 'lime', 'yellow', 'amber', 'orange',
    'deep-orange', 'brown', 'blue-grey'
  ]
  
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  
  return colors[Math.abs(hash) % colors.length]
}

export const getAvatarText = (name) => {
  if (!name) return '?'
  
  const words = name.trim().split(' ')
  if (words.length >= 2) {
    return (words[0][0] + words[words.length - 1][0]).toUpperCase()
  }
  return name.charAt(0).toUpperCase()
}

export const getStatusChipColor = (status) => {
  return formatCandidateStatus(status).color
}

export const getEngagementColor = (score) => {
  if (score >= 80) return 'green'
  if (score >= 60) return 'orange'
  if (score >= 40) return 'yellow'
  return 'red'
}

export const validateCandidateForm = (candidate) => {
  const errors = {}
  
  if (!candidate.full_name?.trim()) {
    errors.full_name = 'Họ tên là bắt buộc'
  }
  
  if (!candidate.email?.trim()) {
    errors.email = 'Email là bắt buộc'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(candidate.email)) {
    errors.email = 'Email không hợp lệ'
  }
  
  if (candidate.phone && !/^[\+]?[0-9\-\(\)\s]+$/.test(candidate.phone)) {
    errors.phone = 'Số điện thoại không hợp lệ'
  }
  
  if (candidate.cv_original_url && !/^https?:\/\/.+/.test(candidate.cv_original_url)) {
    errors.cv_original_url = 'URL CV không hợp lệ'
  }
  
  return errors
}

export const processSkills = (skills) => {
  if (!skills) return []
  
  if (Array.isArray(skills)) {
    return skills.filter(skill => skill && skill.trim())
  }
  
  if (typeof skills === 'string') {
    try {
      const parsed = JSON.parse(skills)
      return Array.isArray(parsed) ? parsed : []
    } catch {
      return skills.split(',').map(s => s.trim()).filter(s => s)
    }
  }
  
  return []
}

export const formatDate = (date) => {
  if (!date) return '-'
  
  try {
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).format(new Date(date))
  } catch {
    return date
  }
}

export const formatRelativeTime = (date) => {
  if (!date) return '-'
  
  try {
    const now = new Date()
    const target = new Date(date)
    const diffMs = now - target
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return 'Hôm nay'
    if (diffDays === 1) return 'Hôm qua'
    if (diffDays < 7) return `${diffDays} ngày trước`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} tuần trước`
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} tháng trước`
    return `${Math.floor(diffDays / 365)} năm trước`
  } catch {
    return date
  }
} 