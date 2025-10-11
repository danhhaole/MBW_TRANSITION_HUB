import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCandidatePoolStore = defineStore('candidatePool', {
  state: () => ({
    candidatePools: [],
    currentCandidatePool: null,
    loading: false,
    error: null,
    success: false,
    // Pagination state
    pagination: {
      page: 1,
      limit: 12,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    },
    // Filter state
    searchText: '',
    statusFilter: '',
    orderBy: 'modified desc',
    // Statistics
    statistics: {
      total: 0,
      shortlisted: 0,
      offered: 0,
      hired: 0,
      rejected: 0,
      recent: 0,
      shortlistedPercentage: 0,
      offeredPercentage: 0,
      hiredPercentage: 0,
      rejectedPercentage: 0,
      recentPercentage: 0
    },
    // Filter options
    filterOptions: {
      statuses: [],
      jobOpenings: [],
      departments: []
    }
  }),

  getters: {
    // Client-side filtered candidate pools
    filteredCandidatePools: (state) => {
      let filtered = state.candidatePools

      if (state.searchText) {
        filtered = filtered.filter(pool =>
          pool.applicant_name?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          pool.applicant_id?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          pool.job_opening?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.statusFilter) {
        filtered = filtered.filter(pool => pool.status === state.statusFilter)
      }

      return filtered
    },

    // Get candidate pool by name
    getCandidatePoolByName: (state) => (name) => {
      return state.candidatePools.find(pool => pool.name === name)
    },

    // Candidate pools by status
    candidatePoolsByStatus: (state) => (status) => {
      return state.candidatePools.filter(pool => pool.status === status)
    },

    // Shortlisted candidates
    shortlistedCandidates: (state) => {
      return state.candidatePools.filter(pool => pool.status === 'Shortlisted')
    },

    // Offered candidates
    offeredCandidates: (state) => {
      return state.candidatePools.filter(pool => pool.status === 'Offered')
    },

    // Hired candidates
    hiredCandidates: (state) => {
      return state.candidatePools.filter(pool => pool.status === 'Hired')
    },

    // Recent candidates (last 7 days)
    recentCandidates: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.candidatePools.filter(pool => {
        const modifiedDate = new Date(pool.modified)
        return modifiedDate >= sevenDaysAgo
      })
    }
  },

  actions: {
    // Set loading state
    setLoading(loading) {
      this.loading = loading
      if (loading) {
        this.error = null
        this.success = false
      }
    },

    // Set error state
    setError(error) {
      this.error = error
      this.loading = false
      this.success = false
    },

    // Set success state
    setSuccess(message = 'Operation completed successfully') {
      this.success = message
      this.error = null
      this.loading = false
    },

    // Clear messages
    clearMessages() {
      this.error = null
      this.success = false
    },

    // Set search text
    setSearchText(text) {
      this.searchText = text
    },

    // Set status filter
    setStatusFilter(status) {
      this.statusFilter = status
    },

    // Set order by
    setOrderBy(orderBy) {
      this.orderBy = orderBy
    },

    // Reset filters
    resetFilters() {
      this.searchText = ''
      this.statusFilter = ''
      this.orderBy = 'modified desc'
    },

    // Get candidate pools with pagination and filters
    async fetchCandidatePools(options = {}) {
      this.setLoading(true)

      try {
        const {
          page = this.pagination.page,
          limit = this.pagination.limit,
          search = this.searchText,
          status = this.statusFilter,
          order_by = this.orderBy
        } = options

        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pools_paginated', {
          page,
          limit,
          search,
          status,
          order_by
        })

        if (response?.success) {
          const candidatePools = response.candidate_pools || []
          
          // Enhance data with formatting
          const enhancedPools = candidatePools.map(pool => ({
            ...pool,
            statusInfo: this.formatCandidatePoolStatus(pool.status),
            scoreColor: this.getEvaluationScoreColor(pool.evaluation_score),
            formattedShortlistDate: this.formatDate(pool.shortlist_date),
            formattedHiredDate: this.formatDate(pool.hired_date),
            relativeModified: this.formatRelativeDate(pool.modified),
            avatarText: this.getAvatarText(pool.applicant_name || pool.applicant_id)
          }))

          this.candidatePools = enhancedPools

          // Update pagination
          this.pagination = {
            page: page,
            limit: limit,
            total: response.pagination?.total || 0,
            pages: response.pagination?.pages || 1,
            has_next: response.pagination?.has_next || false,
            has_prev: response.pagination?.has_prev || false,
            showing_from: response.pagination?.showing_from || 0,
            showing_to: response.pagination?.showing_to || 0
          }

          this.setSuccess('Candidate pools loaded successfully')
          return {
            success: true,
            candidate_pools: enhancedPools,
            pagination: this.pagination
          }
        } else {
          throw new Error(response?.error || 'Failed to fetch candidate pools')
        }
      } catch (error) {
        console.error('Error fetching candidate pools:', error)
        this.setError(error.message || 'Failed to fetch candidate pools')
        return {
          success: false,
          error: error.message || 'Failed to fetch candidate pools'
        }
      }
    },

    // Get candidate pool by name
    async fetchCandidatePoolById(name) {
      this.setLoading(true)

      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pool_by_name', {
          name
        })

        if (response?.success) {
          const pool = response.candidate_pool || {}
          
          // Enhance data with formatting
          const enhancedPool = {
            ...pool,
            statusInfo: this.formatCandidatePoolStatus(pool.status),
            scoreColor: this.getEvaluationScoreColor(pool.evaluation_score),
            formattedShortlistDate: this.formatDate(pool.shortlist_date),
            formattedHiredDate: this.formatDate(pool.hired_date),
            relativeModified: this.formatRelativeDate(pool.modified),
            avatarText: this.getAvatarText(pool.applicant_name || pool.applicant_id)
          }

          this.currentCandidatePool = enhancedPool
          this.setSuccess('Candidate pool loaded successfully')

          return {
            success: true,
            candidate_pool: enhancedPool
          }
        } else {
          throw new Error(response?.error || 'Candidate pool not found')
        }
      } catch (error) {
        console.error('Error fetching candidate pool:', error)
        this.setError(error.message || 'Failed to fetch candidate pool')
        return {
          success: false,
          error: error.message || 'Failed to fetch candidate pool'
        }
      }
    },

    // Search candidate pools
    async searchCandidatePools(query = "", limit = 10) {
      this.setLoading(true)

      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.search_candidate_pools', {
          query,
          limit
        })

        if (response?.success) {
          const candidatePools = response.candidate_pools || []
          
          // Enhance data with formatting
          const enhancedPools = candidatePools.map(pool => ({
            ...pool,
            statusInfo: this.formatCandidatePoolStatus(pool.status),
            scoreColor: this.getEvaluationScoreColor(pool.evaluation_score),
            avatarText: this.getAvatarText(pool.applicant_name || pool.applicant_id)
          }))

          this.setSuccess('Search completed successfully')
          return {
            success: true,
            candidate_pools: enhancedPools
          }
        } else {
          throw new Error(response?.error || 'Search failed')
        }
      } catch (error) {
        console.error('Error searching candidate pools:', error)
        this.setError(error.message || 'Failed to search candidate pools')
        return {
          success: false,
          error: error.message || 'Failed to search candidate pools'
        }
      }
    },

    // Get statistics
    async fetchStatistics() {
      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pool_stats')

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

          this.statistics = enhancedStats

          return {
            success: true,
            stats: enhancedStats
          }
        } else {
          throw new Error(response?.error || 'Failed to fetch statistics')
        }
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return {
          success: false,
          error: error.message || 'Failed to fetch statistics'
        }
      }
    },

    // Get filter options
    async fetchFilterOptions() {
      try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.get_candidate_pool_filter_options')

        if (response?.success) {
          this.filterOptions = response.filter_options || {}
          return {
            success: true,
            filter_options: this.filterOptions
          }
        } else {
          throw new Error(response?.error || 'Failed to fetch filter options')
        }
      } catch (error) {
        console.error('Error fetching filter options:', error)
        return {
          success: false,
          error: error.message || 'Failed to fetch filter options'
        }
      }
    },

    // Set pagination
    setPagination(page, limit = null) {
      this.pagination.page = page
      if (limit) {
        this.pagination.limit = limit
      }
    },

    // Helper methods for data formatting
    formatCandidatePoolStatus(status) {
      const statusConfig = {
        'Shortlisted': { text: 'Shortlisted', color: 'info' },
        'Offered': { text: 'Offered', color: 'warning' },
        'Hired': { text: 'Hired', color: 'success' },
        'Rejected': { text: 'Rejected', color: 'error' }
      }
      
      return statusConfig[status] || { text: status || 'Unknown', color: 'gray' }
    },

    getEvaluationScoreColor(score) {
      if (!score || score === 0) return 'gray'
      if (score >= 80) return 'green'
      if (score >= 60) return 'blue'
      if (score >= 40) return 'yellow'
      return 'red'
    },

    getAvatarText(name) {
      if (!name) return '??'
      return name
        .split(' ')
        .map(word => word.charAt(0))
        .join('')
        .toUpperCase()
        .slice(0, 2)
    },

    formatDate(dateStr) {
      if (!dateStr) return 'Not set'
      const date = new Date(dateStr)
      return date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      })
    },

    formatRelativeDate(dateStr) {
      if (!dateStr) return 'Never'
      
      const date = new Date(dateStr)
      const now = new Date()
      const diffTime = Math.abs(now - date)
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

      if (diffDays === 0) return 'Today'
      if (diffDays === 1) return 'Yesterday'
      if (diffDays < 7) return `${diffDays} days ago`
      if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
      if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
      return `${Math.floor(diffDays / 365)} years ago`
    }
  }
})
