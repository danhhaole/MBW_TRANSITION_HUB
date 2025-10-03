import { call } from 'frappe-ui'

/**
 * Repository for Mira Talent - READ ONLY
 * Chỉ có chức năng xem, không có CRUD
 */

// Get paginated candidate pools
export const getCandidatePools = (params = {}) => {
  const {
    page = 1,
    limit = 12,
    search = "",
    status = "",
    order_by = "modified desc"
  } = params

  return call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pools_paginated', {
    page,
    limit,
    search,
    status,
    order_by
  })
}

// Get candidate pool statistics
export const getCandidatePoolStats = () => {
  return call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pool_stats')
}

// Search candidate pools
export const searchCandidatePools = (query = "", limit = 10) => {
  return call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.search_candidate_pools', {
    query,
    limit
  })
}

// Get candidate pool by name
export const getCandidatePoolByName = (name) => {
  return call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pool_by_name', {
    name
  })
}

// Get filter options
export const getCandidatePoolFilterOptions = () => {
  return call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pool_filter_options')
}

export default {
  getCandidatePools,
  getCandidatePoolStats,
  searchCandidatePools,
  getCandidatePoolByName,
  getCandidatePoolFilterOptions
} 