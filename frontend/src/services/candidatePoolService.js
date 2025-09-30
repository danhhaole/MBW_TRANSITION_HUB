import candidatePoolRepository from '@/repositories/candidatePoolRepository'

/**
 * Service for Mira Talent - READ ONLY
 * Xử lý business logic cho Mira Talent
 */

// Format candidate pool status with color
export const formatCandidatePoolStatus = (status) => {
  const statusConfig = {
    'Shortlisted': { text: __('Shortlisted'), color: 'info' },
    'Offered': { text: __('Offered'), color: 'warning' },
    'Hired': { text: __('Hired'), color: 'success' },
    'Rejected': { text: __('Rejected'), color: 'error' }
  }
  
  return statusConfig[status] || { text: status || __('Unknown'), color: 'gray' }
}

// Calculate evaluation score color
export const getEvaluationScoreColor = (score) => {
  if (!score || score === 0) return 'gray'
  if (score >= 80) return 'green'
  if (score >= 60) return 'blue'
  if (score >= 40) return 'yellow'
  return 'red'
}

// Get avatar text for applicant
export const getAvatarText = (name) => {
  if (!name) return '??'
  return name
    .split(' ')
    .map(word => word.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

// Format date for display
export const formatDate = (dateStr) => {
  if (!dateStr) return __('Not set')
  const date = new Date(dateStr)
  return date.toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// Format relative date
export const formatRelativeDate = (dateStr) => {
  if (!dateStr) return __('Never')
  
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return __('Today')
  if (diffDays === 1) return __('Yesterday')
  if (diffDays < 7) return `${diffDays} ${__('days ago')}`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} ${__('weeks ago')}`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} ${__('months ago')}`
  return `${Math.floor(diffDays / 365)} ${__('years ago')}`
}

// Get candidate pools with enhanced data
export const getCandidatePoolsWithDetails = async (params = {}) => {
  try {
    const response = await candidatePoolRepository.getCandidatePools(params)
    
    if (response?.success) {
      const candidatePools = response.candidate_pools || []
      
      // Enhance data with formatting
      const enhancedPools = candidatePools.map(pool => ({
        ...pool,
        statusInfo: formatCandidatePoolStatus(pool.status),
        scoreColor: getEvaluationScoreColor(pool.evaluation_score),
        formattedShortlistDate: formatDate(pool.shortlist_date),
        formattedHiredDate: formatDate(pool.hired_date),
        relativeModified: formatRelativeDate(pool.modified),
        avatarText: getAvatarText(pool.applicant_name || pool.applicant_id)
      }))
      
      return {
        success: true,
        candidate_pools: enhancedPools,
        pagination: response.pagination
      }
    }
    
    return response
  } catch (error) {
    console.error('Error in getCandidatePoolsWithDetails:', error)
    return {
      success: false,
      error: error.message || 'Unknown error'
    }
  }
}

// Get candidate pool statistics
export const getCandidatePoolStatistics = async () => {
  try {
    const response = await candidatePoolRepository.getCandidatePoolStats()
    
    if (response?.success) {
      const stats = response.stats || {}
      
      // Calculate percentages
      const total = stats.total || 0
      const enhancedStats = {
        ...stats,
        shortlistedPercentage: total > 0 ? Math.round((stats.shortlisted / total) * 100) : 0,
        offeredPercentage: total > 0 ? Math.round((stats.offered / total) * 100) : 0,
        hiredPercentage: total > 0 ? Math.round((stats.hired / total) * 100) : 0,
        rejectedPercentage: total > 0 ? Math.round((stats.rejected / total) * 100) : 0,
        recentPercentage: total > 0 ? Math.round((stats.recent / total) * 100) : 0
      }
      
      return {
        success: true,
        stats: enhancedStats
      }
    }
    
    return response
  } catch (error) {
    console.error('Error in getCandidatePoolStatistics:', error)
    return {
      success: false,
      error: error.message || 'Unknown error'
    }
  }
}

// Search candidate pools with enhanced data
export const searchCandidatePoolsWithDetails = async (query = "", limit = 10) => {
  try {
    const response = await candidatePoolRepository.searchCandidatePools(query, limit)
    
    if (response?.success) {
      const candidatePools = response.candidate_pools || []
      
      // Enhance data with formatting
      const enhancedPools = candidatePools.map(pool => ({
        ...pool,
        statusInfo: formatCandidatePoolStatus(pool.status),
        scoreColor: getEvaluationScoreColor(pool.evaluation_score),
        avatarText: getAvatarText(pool.applicant_name || pool.applicant_id)
      }))
      
      return {
        success: true,
        candidate_pools: enhancedPools
      }
    }
    
    return response
  } catch (error) {
    console.error('Error in searchCandidatePoolsWithDetails:', error)
    return {
      success: false,
      error: error.message || 'Unknown error'
    }
  }
}

// Get candidate pool detail by name
export const getCandidatePoolDetail = async (name) => {
  try {
    const response = await candidatePoolRepository.getCandidatePoolByName(name)
    
    if (response?.success) {
      const pool = response.candidate_pool || {}
      
      // Enhance data with formatting
      const enhancedPool = {
        ...pool,
        statusInfo: formatCandidatePoolStatus(pool.status),
        scoreColor: getEvaluationScoreColor(pool.evaluation_score),
        formattedShortlistDate: formatDate(pool.shortlist_date),
        formattedHiredDate: formatDate(pool.hired_date),
        relativeModified: formatRelativeDate(pool.modified),
        avatarText: getAvatarText(pool.applicant_name || pool.applicant_id)
      }
      
      return {
        success: true,
        candidate_pool: enhancedPool
      }
    }
    
    return response
  } catch (error) {
    console.error('Error in getCandidatePoolDetail:', error)
    return {
      success: false,
      error: error.message || 'Unknown error'
    }
  }
}

// Get filter options
export const getCandidatePoolFilterOptions = async () => {
  try {
    const response = await candidatePoolRepository.getCandidatePoolFilterOptions()
    return response
  } catch (error) {
    console.error('Error in getCandidatePoolFilterOptions:', error)
    return {
      success: false,
      error: error.message || 'Unknown error'
    }
  }
}

export default {
  formatCandidatePoolStatus,
  getEvaluationScoreColor,
  getAvatarText,
  formatDate,
  formatRelativeDate,
  getCandidatePoolsWithDetails,
  getCandidatePoolStatistics,
  searchCandidatePoolsWithDetails,
  getCandidatePoolDetail,
  getCandidatePoolFilterOptions
} 