import { createResource } from 'frappe-ui'

/**
 * Candidate Repository
 * Xử lý tất cả các API calls liên quan đến Candidate
 */

// Get paginated candidates with filters and search
export const getCandidates = (params = {}) => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.get_candidates_paginated',
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
        data: response.data || [],
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

// Get candidate statistics
export const getCandidateStats = () => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.get_candidate_stats',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch().catch(error => {
    console.error('Error fetching candidate stats:', error)
    return {}
  })
}

// Search candidates for autocomplete
export const searchCandidates = (query, limit = 10) => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.search_candidates',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({
    query,
    limit
  }).then(response => {
    return Array.isArray(response) ? response : []
  }).catch(error => {
    console.error('Error searching candidates:', error)
    return []
  })
}

// Get candidate by ID/name
export const getCandidateByName = (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.get_candidate_by_name',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ name }).catch(error => {
    console.error('Error fetching candidate by name:', error)
    throw error
  })
}

// Create new candidate
export const createCandidate = (candidateData) => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.create_candidate',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ data: candidateData }).catch(error => {
    console.error('Error creating candidate:', error)
    throw error
  })
}

// Update candidate
export const updateCandidate = (name, candidateData) => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.update_candidate',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({
    name,
    data: candidateData
  }).catch(error => {
    console.error('Error updating candidate:', error)
    throw error
  })
}

// Delete candidate
export const deleteCandidate = (name) => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.delete_candidate',
    method: 'POST',
    auto: false
  })
  
  return resource.fetch({ name }).catch(error => {
    console.error('Error deleting candidate:', error)
    throw error
  })
}

// Get filter options (statuses, sources, skills)
export const getFilterOptions = () => {
  const resource = createResource({
    url: 'mbw_mira.api.candidate.get_filter_options',
    method: 'GET',
    auto: false
  })
  
  return resource.fetch().then(response => {
    return {
      statuses: response?.statuses || [],
      sources: response?.sources || [],
      skills: response?.skills || []
    }
  }).catch(error => {
    console.error('Error fetching filter options:', error)
    return {
      statuses: [],
      sources: [],
      skills: []
    }
  })
}

export default {
  getCandidates,
  getCandidateStats,
  searchCandidates,
  getCandidateByName,
  createCandidate,
  updateCandidate,
  deleteCandidate,
  getFilterOptions
} 