import { createResource } from 'frappe-ui'

// Get paginated talent pools
export const getCandidatesResource = createResource({
  url: 'mbw_mira.api.talentpool.get_talent_pools_paginated',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return {
        candidates: data.talent_pools || [],
        pagination: data.pagination || {}
      }
    }
    return { candidates: [], pagination: {} }
  }
})

// Get talent pool stats
export const getCandidateStatsResource = createResource({
  url: 'mbw_mira.api.talentpool.get_talent_pool_stats',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.stats || {}
    }
    return {}
  }
})

// Search talent pools
export const searchCandidatesResource = createResource({
  url: 'mbw_mira.api.talentpool.search_talent_pools',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.talent_pools || []
    }
    return []
  }
})

// Get talent pool by name
export const getCandidateResource = createResource({
  url: 'mbw_mira.api.talentpool.get_talent_pool_by_name',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.talent_pool || null
    }
    return null
  }
})

// Create talent pool
export const createCandidateResource = createResource({
  url: 'mbw_mira.api.talentpool.create_talent_pool',
  method: 'POST',
  transform: (data) => {
    if (data?.success) {
      return data.talent_pool || null
    }
    throw new Error(data?.error || 'Failed to create talent pool')
  }
})

// Update talent pool
export const updateCandidateResource = createResource({
  url: 'mbw_mira.api.talentpool.update_talent_pool',
  method: 'POST',
  transform: (data) => {
    if (data?.success) {
      return data.talent_pool || null
    }
    throw new Error(data?.error || 'Failed to update talent pool')
  }
})

// Delete talent pool
export const deleteCandidateResource = createResource({
  url: 'mbw_mira.api.talentpool.delete_talent_pool',
  method: 'POST',
  transform: (data) => {
    if (data?.success) {
      return { success: true }
    }
    throw new Error(data?.error || 'Failed to delete talent pool')
  }
})

// Get filter options
export const getFilterOptionsResource = createResource({
  url: 'mbw_mira.api.talentpool.get_talent_pool_filter_options',
  method: 'GET',
  transform: (data) => {
    if (data?.success) {
      return data.options || {}
    }
    return { status: [], source: [], skills: [] }
  }
}) 