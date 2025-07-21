import { createResource } from 'frappe-ui'

/**
 * TalentProfiles Repository
 * Xử lý tất cả các API calls liên quan đến TalentProfiles
 */

// Get paginated talent profiles with filters and search
export const getCandidates = (params = {}) => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.get_talent_profiles_paginated',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({
    page: params.page || 1,
    limit: params.limit || 10,
    search: params.search || '',
    filters: params.filters || {}
  }).then(response => {
    // Handle response structure
    if (response && typeof response === 'object') {
      return {
        data: response.talent_profiles || [],
        pagination: response.pagination || {
          page: 1,
          limit: 10,
          total: 0,
          pages: 0,
          has_next: false,
          has_prev: false,
          showing_from: 0,
          showing_to: 0
        }
      }
    }
    
    // Fallback for unexpected response format
    return {
      data: Array.isArray(response) ? response : [],
      pagination: {
        page: params.page || 1,
        limit: params.limit || 10,
        total: Array.isArray(response) ? response.length : 0,
        pages: 1,
        has_next: false,
        has_prev: false,
        showing_from: 1,
        showing_to: Array.isArray(response) ? response.length : 0
      }
    }
  }).catch(error => {
    console.error('Error fetching candidates:', error)
    throw error
  })
}

// Get talent profile statistics
export const getCandidateStats = () => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.get_talent_profile_stats',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch().then(response => {
    if (response && response.success) {
      return response.stats
    }
    return {}
  }).catch(error => {
    console.error('Error fetching stats:', error)
    return {}
  })
}

// Search talent profiles for autocomplete
export const searchCandidates = (query, limit = 10) => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.search_talent_profiles',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch({ query, limit }).then(response => {
    if (response && response.success) {
      return response.talent_profiles || []
    }
    return []
  }).catch(error => {
    console.error('Error searching candidates:', error)
    return []
  })
}

// Get single talent profile by name
export const getCandidate = (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.get_talent_profile_by_name',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch({ name }).then(response => {
    if (response && response.success) {
      return response.talent_profile
    }
    return null
  }).catch(error => {
    console.error('Error fetching candidate:', error)
    throw error
  })
}

// Create new talent profile
export const createCandidate = (candidateData) => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.create_talent_profile',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ data: candidateData }).then(response => {
    if (response && response.success) {
      return response.talent_profile
    }
    throw new Error(response?.error || 'Failed to create talent profile')
  }).catch(error => {
    console.error('Error creating candidate:', error)
    throw error
  })
}

// Update talent profile
export const updateCandidate = (name, candidateData) => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.update_talent_profile',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ name, data: candidateData }).then(response => {
    if (response && response.success) {
      return response.talent_profile
    }
    throw new Error(response?.error || 'Failed to update talent profile')
  }).catch(error => {
    console.error('Error updating candidate:', error)
    throw error
  })
}

// Delete talent profile
export const deleteCandidate = (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.delete_talent_profile',
    method: 'DELETE',
    auto: false
  })
  
  return resource.fetch({ name }).then(response => {
    if (response && response.success) {
      return true
    }
    throw new Error(response?.error || 'Failed to delete talent profile')
  }).catch(error => {
    console.error('Error deleting candidate:', error)
    throw error
  })
}

// Get filter options
export const getFilterOptions = () => {
  const resource = createResource({
    url: 'mbw_mira.api.talentprofiles.get_talent_profile_filter_options',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch().then(response => {
    if (response && response.success) {
      return response.options
    }
    return {
      status: [],
      source: [],
      skills: []
    }
  }).catch(error => {
    console.error('Error fetching filter options:', error)
    return {
      status: [],
      source: [],
      skills: []
    }
  })
}

// Resource exports for composables
export const getCandidatesResource = createResource({
  url: 'mbw_mira.api.talentprofiles.get_talent_profiles_paginated',
  method: 'POST',
  auto: false
})

export const getCandidateStatsResource = createResource({
  url: 'mbw_mira.api.talentprofiles.get_talent_profile_stats',
  method: 'GET',
  auto: false
})

export const searchCandidatesResource = createResource({
  url: 'mbw_mira.api.talentprofiles.search_talent_profiles',
  method: 'GET',
  auto: false
})

export const getCandidateResource = createResource({
  url: 'mbw_mira.api.talentprofiles.get_talent_profile_by_name',
  method: 'GET',
  auto: false
})

export const createCandidateResource = createResource({
  url: 'mbw_mira.api.talentprofiles.create_talent_profile',
  method: 'POST',
  auto: false
})

export const updateCandidateResource = createResource({
  url: 'mbw_mira.api.talentprofiles.update_talent_profile',
  method: 'POST',
  auto: false
})

export const deleteCandidateResource = createResource({
  url: 'mbw_mira.api.talentprofiles.delete_talent_profile',
  method: 'DELETE',
  auto: false
})

export const getFilterOptionsResource = createResource({
  url: 'mbw_mira.api.talentprofiles.get_talent_profile_filter_options',
  method: 'GET',
  auto: false
}) 