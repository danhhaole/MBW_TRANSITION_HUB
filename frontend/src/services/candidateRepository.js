import { createResource } from 'frappe-ui'

// Get paginated talent profiles
export const getCandidatesResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.get_prospects_paginated',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return {
        candidates: data.talent_profiles || [],
        pagination: data.pagination || {}
      }
    }
    return { candidates: [], pagination: {} }
  }
})

// Get talent profile statistics
export const getCandidateStatsResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.get_talent_profile_stats',
  method: 'GET',
  transform: (data) => data?.stats || {}
})

// Search talent profiles
export const searchCandidatesResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.search_talent_profiles',
  method: 'GET',
  transform: (data) => data?.talent_profiles || []
})

// Get single talent profile
export const getCandidateResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.get_talent_profile_by_name',
  method: 'GET',
  transform: (data) => data?.talent_profile || null
})

// Create talent profile
export const createCandidateResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.create_talent_profile',
  method: 'POST',
  transform: (data) => data?.talent_profile || null
})

// Update talent profile
export const updateCandidateResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.update_talent_profile',
  method: 'POST',
  transform: (data) => data?.talent_profile || null
})

// Delete talent profile
export const deleteCandidateResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.delete_talent_profile',
  method: 'DELETE',
  transform: (data) => data?.success || false
})

// Get filter options
export const getFilterOptionsResource = createResource({
  url: 'mbw_mira.mbw_mira.mira_contact.mira_contact.get_talent_profile_filter_options',
  method: 'GET',
  transform: (data) => data?.options || { status: [], source: [], skills: [] }
}) 