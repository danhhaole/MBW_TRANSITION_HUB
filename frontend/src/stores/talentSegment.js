import { defineStore } from 'pinia'
import { call, createResource } from 'frappe-ui'

export const useTalentSegmentStore = defineStore('talentSegment', {
  state: () => ({
    // Main data
    talentSegments: [],
    currentTalentSegment: null,
    
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
    typeFilter: '',
    orderBy: 'modified desc',
    
    // Statistics
    statistics: {
      total: 0,
      by_type: {},
      recent: 0
    },
    
    // Filter options
    filterOptions: {
      types: ['DYNAMIC', 'MANUAL']
    },
    
    // Talent Pool data for segments
    segmentTalents: {},
    talentWithPool: [],
    talentPoolPagination: {
      page: 1,
      limit: 20,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    }
  }),

  getters: {
    // Client-side filtered talent segments
    filteredTalentSegments: (state) => {
      let filtered = [...state.talentSegments]
      
      // Search filter
      if (state.searchText) {
        const searchLower = state.searchText.toLowerCase()
        filtered = filtered.filter(segment => 
          segment.title?.toLowerCase().includes(searchLower) ||
          segment.description?.toLowerCase().includes(searchLower)
        )
      }
      
      // Type filter
      if (state.typeFilter && state.typeFilter !== 'all') {
        filtered = filtered.filter(segment => segment.type === state.typeFilter)
      }
      
      return filtered
    },
    
    // Get talent segment by name
    getTalentSegmentByName: (state) => (name) => {
      return state.talentSegments.find(segment => segment.name === name)
    },
    
    // Talent segments by type
    talentSegmentsByType: (state) => (type) => {
      return state.talentSegments.filter(segment => segment.type === type)
    },
    
    // Dynamic segments
    dynamicSegments: (state) => {
      return state.talentSegments.filter(segment => segment.type === 'DYNAMIC')
    },
    
    // Manual segments
    manualSegments: (state) => {
      return state.talentSegments.filter(segment => segment.type === 'MANUAL')
    },
    
    // Recent talent segments (last 7 days)
    recentTalentSegments: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.talentSegments.filter(segment => {
        if (!segment.creation) return false
        const creationDate = new Date(segment.creation)
        return creationDate >= sevenDaysAgo
      })
    },
    
    // Get talents for specific segment
    getSegmentTalents: (state) => (segmentId) => {
      return state.segmentTalents[segmentId] || []
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
    
    setTypeFilter(type) {
      this.typeFilter = type
    },
    
    setOrderBy(orderBy) {
      this.orderBy = orderBy
    },
    
    resetFilters() {
      this.searchText = ''
      this.typeFilter = ''
      this.orderBy = 'modified desc'
    },
    
    // Main CRUD operations
    async fetchTalentSegments(options = {}) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        const {
          page = this.pagination.page,
          limit = this.pagination.limit,
          searchText = this.searchText,
          type = this.typeFilter,
          orderBy = this.orderBy
        } = options
        
        const start = (page - 1) * limit
        let filters = {}
        
        if (type && type !== 'all') {
          filters.type = type
        }
        
        let queryOptions = {
          filters,
          fields: ['name', 'title', 'description', 'type', 'candidate_count', 'owner_id', 'creation', 'modified', 'criteria'],
          order_by: orderBy,
          limit_start: start,
          limit_page_length: limit
        }
        
        if (searchText) {
          queryOptions.or_filters = [
            ['title', 'like', `%${searchText}%`],
            ['description', 'like', `%${searchText}%`]
          ]
        }
        
        const [data, total] = await Promise.all([
          call('frappe.client.get_list', {
            doctype: 'Mira Segment',
            ...queryOptions
          }),
          call('frappe.client.get_count', {
            doctype: 'Mira Segment',
            filters: queryOptions.filters,
            or_filters: queryOptions.or_filters
          })
        ])
        
        // Enhance data with display fields
        const enhancedData = (data || []).map(segment => ({
          ...segment,
          display_type: this.getTypeDisplay(segment.type),
          type_color: this.getSegmentTypeColor(segment.type),
          formatted_creation: this.formatDate(segment.creation),
          formatted_modified: this.formatRelativeDate(segment.modified),
          engagement_rate: this.calculateEngagementRate(segment.candidate_count || 0)
        }))
        
        this.talentSegments = enhancedData
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
    
    async fetchTalentSegmentById(name) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        const data = await call('frappe.client.get', {
          doctype: 'Mira Segment',
          name
        })
        
        if (data) {
          // Enhance data with display fields
          const enhancedData = {
            ...data,
            display_type: this.getTypeDisplay(data.type),
            type_color: this.getSegmentTypeColor(data.type),
            formatted_creation: this.formatDate(data.creation),
            formatted_modified: this.formatRelativeDate(data.modified),
            engagement_rate: this.calculateEngagementRate(data.candidate_count || 0)
          }
          
          this.currentTalentSegment = enhancedData
          this.setLoading(false)
          return enhancedData
        }
        
        throw new Error('Talent segment not found')
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async createTalentSegment(data) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        // Validate data
        const validation = this.validateTalentSegment(data, 'create')
        if (!validation.isValid) {
          throw new Error(Object.values(validation.errors).join(', '))
        }
        
        // Prepare data for save
        const preparedData = this.prepareTalentSegmentForSave(data, 'create')
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Segment',
            ...preparedData
          }
        })
        
        if (result) {
          // Add to local state
          const enhancedData = {
            ...result,
            display_type: this.getTypeDisplay(result.type),
            type_color: this.getSegmentTypeColor(result.type),
            formatted_creation: this.formatDate(result.creation),
            formatted_modified: this.formatRelativeDate(result.modified),
            engagement_rate: this.calculateEngagementRate(result.candidate_count || 0)
          }
          
          this.talentSegments.unshift(enhancedData)
          this.currentTalentSegment = enhancedData
          this.setSuccess('Talent segment created successfully')
          this.setLoading(false)
          return enhancedData
        }
        
        throw new Error('Failed to create talent segment')
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async updateTalentSegment(name, data) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        // Validate data
        const validation = this.validateTalentSegment(data, 'update')
        if (!validation.isValid) {
          throw new Error(Object.values(validation.errors).join(', '))
        }
        
        // Prepare data for save
        const preparedData = this.prepareTalentSegmentForSave(data, 'update')
        
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira Segment',
          name,
          fieldname: preparedData
        })
        
        if (result) {
          // Update local state
          const index = this.talentSegments.findIndex(segment => segment.name === name)
          if (index !== -1) {
            const enhancedData = {
              ...this.talentSegments[index],
              ...result,
              display_type: this.getTypeDisplay(result.type || this.talentSegments[index].type),
              type_color: this.getSegmentTypeColor(result.type || this.talentSegments[index].type),
              formatted_modified: this.formatRelativeDate(result.modified || new Date().toISOString()),
              engagement_rate: this.calculateEngagementRate(result.candidate_count || this.talentSegments[index].candidate_count || 0)
            }
            
            this.talentSegments[index] = enhancedData
            
            if (this.currentTalentSegment?.name === name) {
              this.currentTalentSegment = enhancedData
            }
          }
          
          this.setSuccess('Talent segment updated successfully')
          this.setLoading(false)
          return result
        }
        
        throw new Error('Failed to update talent segment')
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async deleteTalentSegment(name) {
      this.setLoading(true)
      this.clearMessages()
      
      try {
        await call('frappe.client.delete', {
          doctype: 'Mira Segment',
          name
        })
        
        // Remove from local state
        this.talentSegments = this.talentSegments.filter(segment => segment.name !== name)
        
        if (this.currentTalentSegment?.name === name) {
          this.currentTalentSegment = null
        }
        
        // Remove from segment talents cache
        delete this.segmentTalents[name]
        
        this.setSuccess('Talent segment deleted successfully')
        this.setLoading(false)
        return true
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async searchTalentSegments(query = "", limit = 10) {
      try {
        const or_filters = [
          ['title', 'like', `%${query}%`],
          ['description', 'like', `%${query}%`]
        ]
        
        const data = await call('frappe.client.get_list', {
          doctype: 'Mira Segment',
          filters: {},
          or_filters,
          fields: ['name', 'title', 'description', 'type', 'candidate_count'],
          order_by: 'modified desc',
          limit_page_length: limit
        })
        
        return (data || []).map(segment => ({
          ...segment,
          display_type: this.getTypeDisplay(segment.type),
          type_color: this.getSegmentTypeColor(segment.type)
        }))
      } catch (error) {
        console.error('Search talent segments error:', error)
        return []
      }
    },
    
    // Talent Pool management
    async fetchSegmentTalents(segmentId, options = {}) {
      this.setLoading(true)
      
      try {
        const { page = 1, limit = 20 } = options
        const start = (page - 1) * limit
        
        const [data, total] = await Promise.all([
          call('frappe.client.get_list', {
            doctype: 'Mira Talent Pool',
            fields: ['talent_id', 'added_at', 'added_by'],
            filters: { segment_id: segmentId },
            limit_start: start,
            limit_page_length: limit
          }),
          call('frappe.client.get_count', {
            doctype: 'Mira Talent Pool',
            filters: { segment_id: segmentId }
          })
        ])
        
        const talents = data || []
        this.segmentTalents[segmentId] = talents
        
        this.talentPoolPagination = {
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
        return { data: talents, pagination: this.talentPoolPagination }
      } catch (error) {
        this.setError(this.parseError(error))
        this.setLoading(false)
        throw error
      }
    },
    
    async addTalentToSegment(segmentId, talentId) {
      try {
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Talent Pool',
            segment_id: segmentId,
            talent_id: talentId,
            added_at: new Date().toISOString(),
            added_by: 'Administrator' // TODO: get current user
          }
        })
        
        // Update local cache
        if (this.segmentTalents[segmentId]) {
          this.segmentTalents[segmentId].push({
            talent_id: talentId,
            added_at: new Date().toISOString(),
            added_by: 'Administrator'
          })
        }
        
        this.setSuccess('Talent added to segment successfully')
        return result
      } catch (error) {
        this.setError(this.parseError(error))
        throw error
      }
    },
    
    async removeTalentFromSegment(segmentId, talentId) {
      try {
        // Find the talent pool record
        const segments = await call('frappe.client.get_list', {
          doctype: 'Mira Talent Pool',
          fields: ['name'],
          filters: { segment_id: segmentId, talent_id: talentId }
        })
        
        if (segments && segments.length > 0) {
          await call('frappe.client.delete', {
            doctype: 'Mira Talent Pool',
            name: segments[0].name
          })
          
          // Update local cache
          if (this.segmentTalents[segmentId]) {
            this.segmentTalents[segmentId] = this.segmentTalents[segmentId].filter(
              talent => talent.talent_id !== talentId
            )
          }
          
          this.setSuccess('Talent removed from segment successfully')
          return { success: true }
        } else {
          throw new Error('Talent not found in segment')
        }
      } catch (error) {
        this.setError(this.parseError(error))
        throw error
      }
    },
    
    async fetchTalentWithPool(options = {}) {
      try {
        const { page = 1, limit = 20, searchText } = options
        
        // Create resource if not exists
        const talentWithPoolResource = createResource({
          url: 'mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.get_talent_with_pool',
          method: 'GET',
          auto: false
        })
        
        const response = await talentWithPoolResource.fetch({
          page,
          page_size: limit,
          search_text: searchText
        })
        
        if (response && response.data) {
          this.talentWithPool = response.data
          this.talentPoolPagination = {
            page: response.page || 1,
            limit: response.page_size || 20,
            total: response.total || 0,
            pages: response.total_pages || 1,
            has_next: (response.page || 1) < (response.total_pages || 1),
            has_prev: (response.page || 1) > 1,
            showing_from: ((response.page || 1) - 1) * (response.page_size || 20) + 1,
            showing_to: Math.min((response.page || 1) * (response.page_size || 20), response.total || 0)
          }
          
          return { data: response.data, pagination: this.talentPoolPagination }
        }
        
        throw new Error('Failed to fetch talent with pool')
      } catch (error) {
        this.setError(this.parseError(error))
        throw error
      }
    },
    
    // Statistics
    async fetchStatistics() {
      try {
        const [totalCount, typeStats, recentCount] = await Promise.all([
          call('frappe.client.get_count', {
            doctype: 'Mira Segment'
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Segment',
            fields: ['type', 'count(name) as count'],
            group_by: 'type',
            as_dict: true
          }),
          call('frappe.client.get_count', {
            doctype: 'Mira Segment',
            filters: [['creation', '>=', this.formatDate(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000))]]
          })
        ])
        
        const by_type = {}
        if (typeStats && Array.isArray(typeStats)) {
          typeStats.forEach(stat => {
            by_type[stat.type] = stat.count
          })
        }
        
        this.statistics = {
          total: totalCount || 0,
          by_type,
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
    validateTalentSegment(data, action = 'create') {
      const errors = {}
      
      if (!data.title || !data.title.trim()) {
        errors.title = 'Talent segment name is required'
      } else if (data.title.length < 3) {
        errors.title = 'Talent segment name must be at least 3 characters'
      } else if (data.title.length > 200) {
        errors.title = 'Talent segment name must be less than 200 characters'
      }

      if (data.description && data.description.length > 1000) {
        errors.description = 'Description must be less than 1000 characters'
      }

      if (!data.type) {
        errors.type = 'Talent segment type is required'
      }

      // Validate criteria if it's JSON
      if (data.criteria) {
        try {
          if (typeof data.criteria === 'string') {
            JSON.parse(data.criteria)
          }
        } catch (e) {
          errors.criteria = 'Criteria must be a valid JSON'
        }
      }
      
      return {
        isValid: Object.keys(errors).length === 0,
        errors
      }
    },
    
    prepareTalentSegmentForSave(data, action = 'create') {
      const prepared = { ...data }
      
      // Clean string fields
      if (prepared.title) {
        prepared.title = prepared.title.trim()
      }
      if (prepared.description) {
        prepared.description = prepared.description.trim()
      }
      
      // Handle criteria JSON
      if (prepared.criteria && typeof prepared.criteria === 'object') {
        prepared.criteria = JSON.stringify(prepared.criteria)
      }
      
      return prepared
    },
    
    getTypeDisplay(type) {
      const typeMap = {
        'DYNAMIC': 'Dynamic',
        'MANUAL': 'Manual'
      }
      return typeMap[type] || type
    },
    
    getSegmentTypeColor(type) {
      const colorMap = {
        'DYNAMIC': {
          gradient: 'from-blue-500 to-indigo-600',
          bg: 'bg-blue-100',
          text: 'text-blue-800',
          border: 'border-blue-100'
        },
        'MANUAL': {
          gradient: 'from-green-500 to-teal-500', 
          bg: 'bg-green-100',
          text: 'text-green-800',
          border: 'border-green-100'
        }
      }
      
      return colorMap[type] || colorMap['MANUAL']
    },
    
    calculateEngagementRate(candidateCount, totalInteractions = 0) {
      if (!candidateCount || candidateCount === 0) return 0
      
      // Simplified engagement rate calculation
      const baseRate = Math.min(candidateCount / 100 * 70, 95) // Base rate from 0-95%
      const randomFactor = Math.random() * 20 - 10 // Random from -10% to +10%
      
      return Math.max(0, Math.min(100, Math.round(baseRate + randomFactor)))
    },
    
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US')
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
