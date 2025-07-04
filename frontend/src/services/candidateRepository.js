import { createResource } from 'frappe-ui'

// Get paginated candidates
export const getCandidatesResource = createResource({
  url: 'mbw_mira.api.candidate.get_candidates_paginated',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return {
        candidates: data.candidates || [],
        pagination: data.pagination || {}
      }
    }
    return { candidates: [], pagination: {} }
  }
})

// Get candidate stats
export const getCandidateStatsResource = createResource({
  url: 'mbw_mira.api.candidate.get_candidate_stats',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.stats || {}
    }
    return {}
  }
})

// Search candidates
export const searchCandidatesResource = createResource({
  url: 'mbw_mira.api.candidate.search_candidates',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.candidates || []
    }
    return []
  }
})

// Get candidate by name
export const getCandidateResource = createResource({
  url: 'mbw_mira.api.candidate.get_candidate_by_name',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.candidate || null
    }
    return null
  }
})

// Create candidate
export const createCandidateResource = createResource({
  url: 'mbw_mira.api.candidate.create_candidate',
  method: 'POST',
  transform: (data) => {
    if (data?.success) {
      return data.candidate || null
    }
    throw new Error(data?.error || 'Failed to create candidate')
  }
})

// Update candidate
export const updateCandidateResource = createResource({
  url: 'mbw_mira.api.candidate.update_candidate',
  method: 'POST',
  transform: (data) => {
    if (data?.success) {
      return data.candidate || null
    }
    throw new Error(data?.error || 'Failed to update candidate')
  }
})

// Delete candidate
export const deleteCandidateResource = createResource({
  url: 'mbw_mira.api.candidate.delete_candidate',
  method: 'POST',
  transform: (data) => {
    if (data?.success) {
      return { success: true }
    }
    throw new Error(data?.error || 'Failed to delete candidate')
  }
})

// Get filter options
export const getFilterOptionsResource = createResource({
  url: 'mbw_mira.api.candidate.get_candidate_filter_options',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.options || {}
    }
    return { status: [], source: [], skills: [] }
  }
}) 