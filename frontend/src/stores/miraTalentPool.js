import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useMiraTalentPoolStore = defineStore('miraTalentPool', {
  state: () => ({
    // Main data
    talentPools: [],
    currentTalentPool: null,
    
    // Loading and error states
    loading: false,
    error: null,
    success: false,
    
    // Pagination state
    pagination: {
      page: 1,
      limit: 20,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    },
    
    // Filter state
    searchText: '',
    campaignFilter: '',
    segmentFilter: '',
    statusFilter: '',
    orderBy: 'modified desc',
    
    // Statistics
    statistics: {
      total: 0,
      by_status: {},
      by_campaign: {},
      by_segment: {},
      recent: 0
    },
    
    // Filter options
    filterOptions: {
      campaigns: [],
      segments: [],
      statuses: ['Applied', 'Shortlisted', 'Interviewed', 'Offered', 'Hired', 'Rejected']
    }
  }),

  getters: {
    // Client-side filtered talent pools
    filteredTalentPools: (state) => {
      let filtered = [...state.talentPools]
      
      // Search filter
      if (state.searchText) {
        const searchLower = state.searchText.toLowerCase()
        filtered = filtered.filter(pool => 
          pool.talent_id?.toLowerCase().includes(searchLower) ||
          pool.campaign_id?.toLowerCase().includes(searchLower) ||
          pool.segment_id?.toLowerCase().includes(searchLower) ||
          pool.notes?.toLowerCase().includes(searchLower)
        )
      }
      
      // Campaign filter
      if (state.campaignFilter) {
        filtered = filtered.filter(pool => pool.campaign_id === state.campaignFilter)
      }
      
      // Segment filter
      if (state.segmentFilter) {
        filtered = filtered.filter(pool => pool.segment_id === state.segmentFilter)
      }
      
      // Status filter
      if (state.statusFilter) {
        filtered = filtered.filter(pool => pool.application_status === state.statusFilter)
      }
      
      return filtered
    },
    
    // Get talent pool by name
    getTalentPoolByName: (state) => (name) => {
      return state.talentPools.find(pool => pool.name === name)
    },
    
    // Talent pools by campaign
    talentPoolsByCampaign: (state) => (campaignId) => {
      return state.talentPools.filter(pool => pool.campaign_id === campaignId)
    },
    
    // Talent pools by segment
    talentPoolsBySegment: (state) => (segmentId) => {
      return state.talentPools.filter(pool => pool.segment_id === segmentId)
    },
    
    // Talent pools by status
    talentPoolsByStatus: (state) => (status) => {
      return state.talentPools.filter(pool => pool.application_status === status)
    },
    
    // Recent talent pools (last 7 days)
    recentTalentPools: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.talentPools.filter(pool => {
        if (!pool.application_date) return false
        const applicationDate = new Date(pool.application_date)
        return applicationDate >= sevenDaysAgo
      })
    }
  },

  actions: {
    // Loading and error management
    setLoading(loading) {
      this.loading = loading
    },
    
    setError(error) {
      this.error = error
      this.success = false
    },
    
    setSuccess(message = 'Operation completed successfully') {
      this.success = message
      this.error = null
    },
    
    clearMessages() {
      this.error = null
      this.success = false
    },
    
    // Filter management
    setSearchText(text) {
      this.searchText = text
    },
    
    setCampaignFilter(campaign) {
      this.campaignFilter = campaign
    },
    
    setSegmentFilter(segment) {
      this.segmentFilter = segment
    },
    
    setStatusFilter(status) {
      this.statusFilter = status
    },
    
    setOrderBy(orderBy) {
      this.orderBy = orderBy
    },
    
    resetFilters() {
      this.searchText = ''
      this.campaignFilter = ''
      this.segmentFilter = ''
      this.statusFilter = ''
      this.orderBy = 'modified desc'
    },
    
    // Main CRUD operations
    async fetchTalentPools(options = {}) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        const {
          page = this.pagination.page,
          limit = this.pagination.limit,
          searchText = this.searchText,
          campaignFilter = this.campaignFilter,
          segmentFilter = this.segmentFilter,
          statusFilter = this.statusFilter,
          orderBy = this.orderBy
        } = options
        
        const start = (page - 1) * limit
        let filters = {}
        
        if (campaignFilter) {
          filters.campaign_id = campaignFilter
        }
        
        if (segmentFilter) {
          filters.segment_id = segmentFilter
        }
        
        if (statusFilter) {
          filters.application_status = statusFilter
        }
        
        let queryOptions = {
          filters,
          fields: [
            'name', 'talent_id', 'campaign_id', 'segment_id', 
            'application_status', 'result', 'score', 'application_date', 
            'notes', 'creation', 'modified'
          ],
          order_by: orderBy,
          limit_start: start,
          limit_page_length: limit
        }
        
        if (searchText) {
          queryOptions.or_filters = [
            ['talent_id', 'like', `%${searchText}%`],
            ['campaign_id', 'like', `%${searchText}%`],
            ['segment_id', 'like', `%${searchText}%`],
            ['notes', 'like', `%${searchText}%`]
          ]
        }
        
        const [data, total] = await Promise.all([
          call('frappe.client.get_list', {
            doctype: 'Mira Talent Pool',
            ...queryOptions
          }),
          call('frappe.client.get_count', {
            doctype: 'Mira Talent Pool',
            filters: queryOptions.filters,
            or_filters: queryOptions.or_filters
          })
        ])
        
        // Enhance data with display fields
        const enhancedData = (data || []).map(pool => ({
          ...pool,
          display_status: this.getStatusDisplay(pool.application_status),
          formatted_application_date: this.formatDate(pool.application_date),
          formatted_creation: this.formatDate(pool.creation),
          formatted_modified: this.formatRelativeDate(pool.modified),
          score_percentage: pool.score ? Math.round(pool.score) : 0
        }))
        
        this.talentPools = enhancedData
        this.pagination = {
          page,
          limit,
          total: total || 0,
          pages: Math.ceil((total || 0) / limit),
          has_next: (start + limit) < total,
          has_prev: start > 0,
          showing_from: start + 1,
          showing_to: Math.min(start + limit, total)
        }
        
        this.setLoading(false)
        return { data: enhancedData, pagination: this.pagination }
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async fetchTalentPoolById(name) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        const data = await call('frappe.client.get', {
          doctype: 'Mira Talent Pool',
          name
        })
        
        if (data) {
          // Enhance data with display fields
          const enhancedData = {
            ...data,
            display_status: this.getStatusDisplay(data.application_status),
            formatted_application_date: this.formatDate(data.application_date),
            formatted_creation: this.formatDate(data.creation),
            formatted_modified: this.formatRelativeDate(data.modified),
            score_percentage: data.score ? Math.round(data.score) : 0
          }
          
          this.currentTalentPool = enhancedData
          this.setLoading(false)
          return enhancedData
        }
        
        throw new Error('Talent pool not found')
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async createTalentPool(data) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        // Validate data
        const validation = this.validateTalentPool(data, 'create')
        if (!validation.isValid) {
          throw new Error(Object.values(validation.errors).join(', '))
        }
        
        // Prepare data for save
        const preparedData = this.prepareTalentPoolForSave(data, 'create')
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Talent Pool',
            ...preparedData
          }
        })
        
        if (result) {
          // Add to local state
          const enhancedData = {
            ...result,
            display_status: this.getStatusDisplay(result.application_status),
            formatted_application_date: this.formatDate(result.application_date),
            formatted_creation: this.formatDate(result.creation),
            formatted_modified: this.formatRelativeDate(result.modified),
            score_percentage: result.score ? Math.round(result.score) : 0
          }
          
          this.talentPools.unshift(enhancedData)
          this.currentTalentPool = enhancedData
          this.setSuccess('Talent pool created successfully')
          this.setLoading(false)
          return enhancedData
        }
        
        throw new Error('Failed to create talent pool')
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async updateTalentPool(name, data) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        // Validate data
        const validation = this.validateTalentPool(data, 'update')
        if (!validation.isValid) {
          throw new Error(Object.values(validation.errors).join(', '))
        }
        
        // Prepare data for save
        const preparedData = this.prepareTalentPoolForSave(data, 'update')
        
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira Talent Pool',
          name,
          fieldname: preparedData
        })
        
        if (result) {
          // Update local state
          const index = this.talentPools.findIndex(pool => pool.name === name)
          if (index !== -1) {
            const enhancedData = {
              ...this.talentPools[index],
              ...result,
              display_status: this.getStatusDisplay(result.application_status || this.talentPools[index].application_status),
              formatted_modified: this.formatRelativeDate(result.modified || new Date().toISOString()),
              score_percentage: (result.score || this.talentPools[index].score) ? Math.round(result.score || this.talentPools[index].score) : 0
            }
            
            this.talentPools[index] = enhancedData
            
            if (this.currentTalentPool?.name === name) {
              this.currentTalentPool = enhancedData
            }
          }
          
          this.setSuccess('Talent pool updated successfully')
          this.setLoading(false)
          return result
        }
        
        throw new Error('Failed to update talent pool')
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async deleteTalentPool(name) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        await call('frappe.client.delete', {
          doctype: 'Mira Talent Pool',
          name
        })
        
        // Remove from local state
        this.talentPools = this.talentPools.filter(pool => pool.name !== name)
        
        if (this.currentTalentPool?.name === name) {
          this.currentTalentPool = null
        }
        
        this.setSuccess('Talent pool deleted successfully')
        this.setLoading(false)
        return true
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async searchTalentPools(query = "", limit = 10) {
      try {
        const or_filters = [
          ['talent_id', 'like', `%${query}%`],
          ['campaign_id', 'like', `%${query}%`],
          ['segment_id', 'like', `%${query}%`],
          ['notes', 'like', `%${query}%`]
        ]
        
        const data = await call('frappe.client.get_list', {
          doctype: 'Mira Talent Pool',
          filters: {},
          or_filters,
          fields: ['name', 'talent_id', 'campaign_id', 'segment_id', 'application_status', 'score'],
          order_by: 'modified desc',
          limit_page_length: limit
        })
        
        return (data || []).map(pool => ({
          ...pool,
          display_status: this.getStatusDisplay(pool.application_status),
          score_percentage: pool.score ? Math.round(pool.score) : 0
        }))
      } catch (error) {
        console.error('Search talent pools error:', error)
        return []
      }
    },
    
    // Filter options
    async fetchFilterOptions() {
      try {
        const [campaigns, segments] = await Promise.all([
          call('frappe.client.get_list', {
            doctype: 'Campaign',
            fields: ['name', 'campaign_name'],
            order_by: 'campaign_name asc',
            limit_page_length: 1000
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Segment',
            fields: ['name', 'title'],
            limit_page_length: 1000
          })
        ])
        
        this.filterOptions.campaigns = (campaigns || []).map(c => ({
          label: c.campaign_name || c.name,
          value: c.name
        }))
        
        this.filterOptions.segments = (segments || []).map(s => ({
          label: s.title || s.name,
          value: s.name
        }))
        
        return this.filterOptions
      } catch (error) {
        console.error('Fetch filter options error:', error)
        return this.filterOptions
      }
    },
    
    // Statistics
    async fetchStatistics() {
      try {
        const [totalCount, statusStats, campaignStats, segmentStats, recentCount] = await Promise.all([
          call('frappe.client.get_count', {
            doctype: 'Mira Talent Pool'
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Talent Pool',
            fields: ['application_status', 'count(name) as count'],
            group_by: 'application_status',
            as_dict: true
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Talent Pool',
            fields: ['campaign_id', 'count(name) as count'],
            group_by: 'campaign_id',
            as_dict: true
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Talent Pool',
            fields: ['segment_id', 'count(name) as count'],
            group_by: 'segment_id',
            as_dict: true
          }),
          call('frappe.client.get_count', {
            doctype: 'Mira Talent Pool',
            filters: [['application_date', '>=', this.formatDate(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000))]]
          })
        ])
        
        const by_status = {}
        if (statusStats && Array.isArray(statusStats)) {
          statusStats.forEach(stat => {
            by_status[stat.application_status] = stat.count
          })
        }
        
        const by_campaign = {}
        if (campaignStats && Array.isArray(campaignStats)) {
          campaignStats.forEach(stat => {
            by_campaign[stat.campaign_id] = stat.count
          })
        }
        
        const by_segment = {}
        if (segmentStats && Array.isArray(segmentStats)) {
          segmentStats.forEach(stat => {
            by_segment[stat.segment_id] = stat.count
          })
        }
        
        this.statistics = {
          total: totalCount || 0,
          by_status,
          by_campaign,
          by_segment,
          recent: recentCount || 0
        }
        
        return this.statistics
      } catch (error) {
        console.error('Fetch statistics error:', error)
        return this.statistics
      }
    },
    
    // Pagination
    setPagination(page, limit = null) {
      this.pagination.page = page
      if (limit) {
        this.pagination.limit = limit
      }
    },
    
    // Helper methods
    validateTalentPool(data, action = 'create') {
      const errors = {}
      
      if (!data.talent_id || !data.talent_id.trim()) {
        errors.talent_id = 'Talent ID is required'
      }
      
      if (!data.campaign_id || !data.campaign_id.trim()) {
        errors.campaign_id = 'Campaign ID is required'
      }
      
      if (!data.segment_id || !data.segment_id.trim()) {
        errors.segment_id = 'Segment ID is required'
      }
      
      if (data.score && (isNaN(data.score) || data.score < 0 || data.score > 100)) {
        errors.score = 'Score must be a number between 0 and 100'
      }
      
      return {
        isValid: Object.keys(errors).length === 0,
        errors
      }
    },
    
    prepareTalentPoolForSave(data, action = 'create') {
      const prepared = { ...data }
      
      // Clean string fields
      if (prepared.talent_id) {
        prepared.talent_id = prepared.talent_id.trim()
      }
      if (prepared.campaign_id) {
        prepared.campaign_id = prepared.campaign_id.trim()
      }
      if (prepared.segment_id) {
        prepared.segment_id = prepared.segment_id.trim()
      }
      if (prepared.notes) {
        prepared.notes = prepared.notes.trim()
      }
      
      // Convert score to number
      if (prepared.score) {
        prepared.score = parseFloat(prepared.score)
      }
      
      return prepared
    },
    
    getStatusDisplay(status) {
      const statusMap = {
        'Applied': 'Applied',
        'Shortlisted': 'Shortlisted',
        'Interviewed': 'Interviewed',
        'Offered': 'Offered',
        'Hired': 'Hired',
        'Rejected': 'Rejected'
      }
      return statusMap[status] || status
    },
    
    formatDate(dateStr) {
      if (!dateStr) return ''
      try {
        const date = new Date(dateStr)
        return date.toLocaleDateString('vi-VN')
      } catch {
        return dateStr
      }
    },
    
    formatRelativeDate(dateStr) {
      if (!dateStr) return ''
      
      const date = new Date(dateStr)
      const now = new Date()
      const diffInMs = now - date
      const diffInHours = diffInMs / (1000 * 60 * 60)
      const diffInDays = diffInHours / 24
      
      if (diffInHours < 1) {
        return 'Just now'
      } else if (diffInHours < 24) {
        return `${Math.floor(diffInHours)} hours ago`
      } else if (diffInDays < 7) {
        return `${Math.floor(diffInDays)} days ago`
      } else {
        return this.formatDate(dateStr)
      }
    },
    
    parseError(error) {
      if (typeof error === 'string') {
        return error
      }
      
      if (error?.message) {
        return error.message
      }
      
      if (error?.exc_type && error?.exc) {
        return `${error.exc_type}: ${error.exc}`
      }
      
      return 'An unexpected error occurred'
    }
  }
})
