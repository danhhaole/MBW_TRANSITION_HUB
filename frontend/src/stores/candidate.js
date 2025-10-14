import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCandidateStore = defineStore('candidate', {
  state: () => ({
    candidates: [],
    currentCandidate: null,
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
    sourceFilter: '',
    skillsFilter: '',
    orderBy: 'modified desc',
    // Statistics
    statistics: {
      total: 0,
      by_status: {},
      by_source: {},
      recent: 0
    },
    // Filter options
    filterOptions: {
      statuses: [],
      sources: [],
      skills: []
    }
  }),

  getters: {
    // Client-side filtered candidates
    filteredCandidates: (state) => {
      let filtered = state.candidates

      if (state.searchText) {
        filtered = filtered.filter(candidate =>
          candidate.full_name?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          candidate.email?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          candidate.phone?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          candidate.skills?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.statusFilter) {
        filtered = filtered.filter(candidate => candidate.status === state.statusFilter)
      }

      if (state.sourceFilter) {
        filtered = filtered.filter(candidate => candidate.source === state.sourceFilter)
      }

      if (state.skillsFilter) {
        filtered = filtered.filter(candidate => 
          candidate.skills?.toLowerCase().includes(state.skillsFilter.toLowerCase())
        )
      }

      return filtered
    },

    // Get candidate by name
    getCandidateByName: (state) => (name) => {
      return state.candidates.find(candidate => candidate.name === name)
    },

    // Candidates by status
    candidatesByStatus: (state) => (status) => {
      return state.candidates.filter(candidate => candidate.status === status)
    },

    // Candidates by source
    candidatesBySource: (state) => (source) => {
      return state.candidates.filter(candidate => candidate.source === source)
    },

    // Recent candidates (last 7 days)
    recentCandidates: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.candidates.filter(candidate => {
        const creationDate = new Date(candidate.creation)
        return creationDate >= sevenDaysAgo
      })
    },

    // Candidates with specific skills
    candidatesWithSkills: (state) => (skills) => {
      if (!skills || skills.length === 0) return state.candidates
      
      return state.candidates.filter(candidate => {
        if (!candidate.skills) return false
        const candidateSkills = candidate.skills.toLowerCase()
        return skills.some(skill => candidateSkills.includes(skill.toLowerCase()))
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

    // Set filters
    setStatusFilter(status) {
      this.statusFilter = status
    },

    setSourceFilter(source) {
      this.sourceFilter = source
    },

    setSkillsFilter(skills) {
      this.skillsFilter = skills
    },

    setOrderBy(orderBy) {
      this.orderBy = orderBy
    },

    // Reset filters
    resetFilters() {
      this.searchText = ''
      this.statusFilter = ''
      this.sourceFilter = ''
      this.skillsFilter = ''
      this.orderBy = 'modified desc'
    },

    // Get candidates with pagination and filters
    async fetchCandidates(options = {}) {
      this.setLoading(true)

      try {
        const {
          filters = {},
          or_filters = undefined,
          fields = ['name', 'full_name', 'email', 'phone', 'skills', 'source', 'status', 'creation', 'modified'],
          order_by = this.orderBy,
          page_length = this.pagination.limit,
          start = (this.pagination.page - 1) * this.pagination.limit
        } = options

        // Build filters
        let enhancedFilters = { ...filters }

        if (this.searchText && this.searchText.trim()) {
          // Use or_filters for search across multiple fields
          or_filters = [
            ['full_name', 'like', `%${this.searchText.trim()}%`],
            ['email', 'like', `%${this.searchText.trim()}%`],
            ['phone', 'like', `%${this.searchText.trim()}%`],
            ['skills', 'like', `%${this.searchText.trim()}%`]
          ]
        }

        if (this.statusFilter) {
          enhancedFilters['status'] = this.statusFilter
        }

        if (this.sourceFilter) {
          enhancedFilters['source'] = this.sourceFilter
        }

        if (this.skillsFilter) {
          enhancedFilters['skills'] = ['like', `%${this.skillsFilter}%`]
        }

        // Fetch candidates
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Contact',
          filters: enhancedFilters,
          or_filters: or_filters,
          fields: fields,
          order_by: order_by,
          limit_start: start,
          limit_page_length: page_length
        })

        // Get total count for pagination
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'Mira Contact',
          filters: enhancedFilters,
          or_filters: or_filters
        })

        // Process candidates to add display fields
        const processedCandidates = (response || []).map(candidate => ({
          ...candidate,
          display_status: this.getStatusDisplay(candidate.status),
          display_source: this.getSourceDisplay(candidate.source),
          avatarText: this.getAvatarText(candidate.full_name),
          formattedCreation: this.formatDate(candidate.creation),
          formattedModified: this.formatDate(candidate.modified),
          relativeCreation: this.formatRelativeDate(candidate.creation),
          skillsList: this.parseSkills(candidate.skills)
        }))

        this.candidates = processedCandidates

        // Update pagination
        this.pagination = {
          page: Math.floor(start / page_length) + 1,
          limit: page_length,
          total: totalCount || 0,
          pages: Math.ceil((totalCount || 0) / page_length),
          has_next: (start + page_length) < (totalCount || 0),
          has_prev: start > 0,
          showing_from: start + 1,
          showing_to: Math.min(start + page_length, totalCount || 0)
        }

        this.setSuccess('Candidates loaded successfully')
        return {
          success: true,
          data: processedCandidates,
          pagination: this.pagination
        }
      } catch (error) {
        console.error('Error fetching candidates:', error)
        this.setError(error.message || 'Failed to fetch candidates')
        return {
          success: false,
          error: error.message || 'Failed to fetch candidates'
        }
      }
    },

    // Get candidate by name
    async fetchCandidateById(name) {
      this.setLoading(true)

      try {
        const response = await call('frappe.client.get', {
          doctype: 'Mira Contact',
          name: name
        })

        if (response) {
          const processedCandidate = {
            ...response,
            display_status: this.getStatusDisplay(response.status),
            display_source: this.getSourceDisplay(response.source),
            avatarText: this.getAvatarText(response.full_name),
            formattedCreation: this.formatDate(response.creation),
            formattedModified: this.formatDate(response.modified),
            relativeCreation: this.formatRelativeDate(response.creation),
            skillsList: this.parseSkills(response.skills)
          }

          this.currentCandidate = processedCandidate
          this.setSuccess('Candidate loaded successfully')

          return {
            success: true,
            data: processedCandidate
          }
        } else {
          throw new Error('Candidate not found')
        }
      } catch (error) {
        console.error('Error fetching candidate:', error)
        this.setError(error.message || 'Failed to fetch candidate')
        return {
          success: false,
          error: error.message || 'Failed to fetch candidate'
        }
      }
    },

    // Create new candidate
    async createCandidate(data) {
      this.setLoading(true)

      try {
        // Validate required fields
        const validationErrors = this.validateCandidate(data, 'create')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for creation
        const preparedData = this.prepareCandidateForSave(data, 'create')

        const docData = {
          doctype: 'Mira Contact',
          ...preparedData
        }

        const response = await call('frappe.client.insert', {
          doc: docData
        })

        if (response) {
          // Add to local state
          const newCandidate = {
            ...response,
            display_status: this.getStatusDisplay(response.status),
            display_source: this.getSourceDisplay(response.source),
            avatarText: this.getAvatarText(response.full_name),
            formattedCreation: this.formatDate(response.creation),
            formattedModified: this.formatDate(response.modified),
            relativeCreation: this.formatRelativeDate(response.creation),
            skillsList: this.parseSkills(response.skills)
          }

          this.candidates.unshift(newCandidate)
          this.currentCandidate = newCandidate

          this.setSuccess('Candidate created successfully')
          return {
            success: true,
            data: newCandidate,
            message: 'Candidate created successfully'
          }
        } else {
          throw new Error('Failed to create candidate')
        }
      } catch (error) {
        console.error('Error creating candidate:', error)
        this.setError(this.parseError(error) || 'Failed to create candidate')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to create candidate'
        }
      }
    },

    // Update candidate
    async updateCandidate(name, data) {
      this.setLoading(true)

      try {
        // Validate required fields
        const validationErrors = this.validateCandidate(data, 'update')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for update
        const preparedData = this.prepareCandidateForSave(data, 'update')

        const response = await call('frappe.client.set_value', {
          doctype: 'Mira Contact',
          name: name,
          fieldname: preparedData
        })

        if (response) {
          // Update local state
          const index = this.candidates.findIndex(c => c.name === name)
          if (index !== -1) {
            this.candidates[index] = {
              ...this.candidates[index],
              ...preparedData,
              display_status: this.getStatusDisplay(preparedData.status),
              display_source: this.getSourceDisplay(preparedData.source),
              avatarText: this.getAvatarText(preparedData.full_name),
              skillsList: this.parseSkills(preparedData.skills)
            }
          }

          if (this.currentCandidate && this.currentCandidate.name === name) {
            this.currentCandidate = {
              ...this.currentCandidate,
              ...preparedData,
              display_status: this.getStatusDisplay(preparedData.status),
              display_source: this.getSourceDisplay(preparedData.source),
              avatarText: this.getAvatarText(preparedData.full_name),
              skillsList: this.parseSkills(preparedData.skills)
            }
          }

          this.setSuccess('Candidate updated successfully')
          return {
            success: true,
            data: response,
            message: 'Candidate updated successfully'
          }
        } else {
          throw new Error('Failed to update candidate')
        }
      } catch (error) {
        console.error('Error updating candidate:', error)
        this.setError(this.parseError(error) || 'Failed to update candidate')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to update candidate'
        }
      }
    },

    // Delete candidate
    async deleteCandidate(name) {
      this.setLoading(true)

      try {
        await call('frappe.client.delete', {
          doctype: 'Mira Contact',
          name: name
        })

        // Remove from local state
        this.candidates = this.candidates.filter(c => c.name !== name)

        if (this.currentCandidate && this.currentCandidate.name === name) {
          this.currentCandidate = null
        }

        this.setSuccess('Candidate deleted successfully')
        return {
          success: true,
          message: 'Candidate deleted successfully'
        }
      } catch (error) {
        console.error('Error deleting candidate:', error)
        this.setError(this.parseError(error) || 'Failed to delete candidate')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to delete candidate'
        }
      }
    },

    // Search candidates
    async searchCandidates(query = "", limit = 10) {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Contact',
          filters: [['full_name', 'like', `%${query}%`]],
          fields: ['name', 'full_name', 'email', 'phone', 'skills', 'source', 'status'],
          limit_page_length: limit
        })

        const processedCandidates = (response || []).map(candidate => ({
          ...candidate,
          display_status: this.getStatusDisplay(candidate.status),
          display_source: this.getSourceDisplay(candidate.source),
          avatarText: this.getAvatarText(candidate.full_name),
          skillsList: this.parseSkills(candidate.skills)
        }))

        return {
          success: true,
          data: processedCandidates
        }
      } catch (error) {
        console.error('Error searching candidates:', error)
        return {
          success: false,
          error: error.message || 'Failed to search candidates'
        }
      }
    },

    // Get statistics
    async fetchStatistics() {
      try {
        // Get statistics by status
        const statusStats = await call('frappe.client.get_list', {
          doctype: 'Mira Contact',
          fields: ['status', 'count(*) as count'],
          group_by: 'status'
        })

        // Get statistics by source
        const sourceStats = await call('frappe.client.get_list', {
          doctype: 'Mira Contact',
          fields: ['source', 'count(*) as count'],
          group_by: 'source'
        })

        // Get total count
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'Mira Contact'
        })

        // Get recent count (last 7 days)
        const sevenDaysAgo = new Date()
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
        const recentCount = await call('frappe.client.get_count', {
          doctype: 'Mira Contact',
          filters: [['creation', '>=', sevenDaysAgo.toISOString().split('T')[0]]]
        })

        const statistics = {
          total: totalCount || 0,
          by_status: {},
          by_source: {},
          recent: recentCount || 0
        }

        // Process status statistics
        if (statusStats && Array.isArray(statusStats)) {
          statusStats.forEach(stat => {
            statistics.by_status[stat.status] = stat.count
          })
        }

        // Process source statistics
        if (sourceStats && Array.isArray(sourceStats)) {
          sourceStats.forEach(stat => {
            statistics.by_source[stat.source] = stat.count
          })
        }

        this.statistics = statistics

        return {
          success: true,
          data: statistics
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
        const [statusOptions, sourceOptions, skillsOptions] = await Promise.all([
          call('frappe.client.get_list', {
            doctype: 'Mira Contact',
            fields: ['status'],
            distinct: true,
            order_by: 'status'
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Contact',
            fields: ['source'],
            distinct: true,
            order_by: 'source'
          }),
          call('frappe.client.get_list', {
            doctype: 'Mira Contact',
            fields: ['skills'],
            distinct: true,
            order_by: 'skills'
          })
        ])

        this.filterOptions = {
          statuses: (statusOptions || []).filter(item => item.status).map(item => ({
            label: item.status,
            value: item.status
          })),
          sources: (sourceOptions || []).filter(item => item.source).map(item => ({
            label: item.source,
            value: item.source
          })),
          skills: (skillsOptions || []).filter(item => item.skills).map(item => ({
            label: item.skills,
            value: item.skills
          }))
        }

        return {
          success: true,
          data: this.filterOptions
        }
      } catch (error) {
        console.error('Error fetching filter options:', error)
        return {
          success: false,
          error: error.message || 'Failed to get filter options'
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

    // Helper methods
    validateCandidate(data, action = 'create') {
      const errors = []

      // Required fields
      if (!data.full_name || !data.full_name.trim()) {
        errors.push('Full name is required')
      }

      if (!data.email || !data.email.trim()) {
        errors.push('Email is required')
      }

      // Business rules
      if (data.full_name && data.full_name.length > 150) {
        errors.push('Full name must be less than 150 characters')
      }

      // Email validation
      if (data.email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(data.email)) {
          errors.push('Invalid email format')
        }
      }

      // Phone validation (if provided)
      if (data.phone && data.phone.trim()) {
        const phoneRegex = /^[\d\s\-\+\(\)]{10,}$/
        if (!phoneRegex.test(data.phone.replace(/\s/g, ''))) {
          errors.push('Invalid phone number format')
        }
      }

      return errors
    },

    prepareCandidateForSave(data, action = 'create') {
      const prepared = { ...data }

      // Trim strings
      if (prepared.full_name) {
        prepared.full_name = prepared.full_name.trim()
      }
      if (prepared.email) {
        prepared.email = prepared.email.trim().toLowerCase()
      }
      if (prepared.phone) {
        prepared.phone = prepared.phone.trim()
      }
      if (prepared.skills) {
        prepared.skills = prepared.skills.trim()
      }

      // Set defaults
      if (action === 'create') {
        prepared.status = prepared.status || 'Active'
        prepared.source = prepared.source || 'Manual'
      }

      return prepared
    },

    getStatusDisplay(status) {
      const statusMap = {
        'Active': 'Active',
        'Inactive': 'Inactive',
        'Shortlisted': 'Shortlisted',
        'Interviewed': 'Interviewed',
        'Hired': 'Hired',
        'Rejected': 'Rejected'
      }
      return statusMap[status] || status || 'Unknown'
    },

    getSourceDisplay(source) {
      const sourceMap = {
        'Manual': 'Manual Entry',
        'LinkedIn': 'LinkedIn',
        'JobBoard': 'Job Board',
        'Referral': 'Referral',
        'Website': 'Website',
        'Other': 'Other'
      }
      return sourceMap[source] || source || 'Unknown'
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
    },

    parseSkills(skillsStr) {
      if (!skillsStr) return []
      return skillsStr.split(',').map(skill => skill.trim()).filter(skill => skill)
    },

    // Process skills for display (legacy compatibility)
    processSkills(skillsStr) {
      return this.parseSkills(skillsStr)
    },

    // Convert skills array to string
    skillsToString(skillsArray) {
      if (!skillsArray || !Array.isArray(skillsArray)) return ''
      return skillsArray.join(', ')
    },

    // Validate candidate form (legacy compatibility)
    validateCandidateForm(data) {
      const errors = {}
      
      if (!data.full_name || !data.full_name.trim()) {
        errors.full_name = 'Full name is required'
      }
      
      if (!data.email || !data.email.trim()) {
        errors.email = 'Email is required'
      } else {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        if (!emailRegex.test(data.email)) {
          errors.email = 'Invalid email format'
        }
      }
      
      if (data.phone && data.phone.length > 20) {
        errors.phone = 'Phone number must be less than 20 characters'
      }
      
      return {
        isValid: Object.keys(errors).length === 0,
        errors
      }
    },

    parseError(error) {
      if (typeof error === 'string') return error

      if (error.messages && Array.isArray(error.messages)) {
        return error.messages[0] || error.message
      }

      if (error.exception && typeof error.exception === 'string') {
        // Extract meaningful error from Frappe exception
        const match = error.exception.match(/Title: (.+)/)
        if (match) return match[1]
      }

      return error.message || 'An error occurred'
    }
  }
})

// Export utility functions for backward compatibility
export const processSkills = (skillsStr) => {
  const store = useCandidateStore()
  return store.parseSkills(skillsStr)
}

export const skillsToString = (skillsArray) => {
  const store = useCandidateStore()
  return store.skillsToString(skillsArray)
}

export const validateCandidateForm = (data) => {
  const store = useCandidateStore()
  return store.validateCandidateForm(data)
}

export const formatCandidateStatus = (status) => {
  const store = useCandidateStore()
  return store.getStatusDisplay(status)
}

export const getAvatarText = (fullName) => {
  const store = useCandidateStore()
  return store.getAvatarText(fullName)
}

export const getStatusChipColor = (status) => {
  const statusColors = {
    'ACTIVE': 'green',
    'INACTIVE': 'gray',
    'PENDING': 'yellow',
    'BLACKLISTED': 'red'
  }
  return statusColors[status] || 'gray'
}

export const calculateEngagementScore = (candidate) => {
  // Simple engagement score calculation
  let score = 0
  
  if (candidate.email) score += 20
  if (candidate.phone) score += 20
  if (candidate.skills && candidate.skills.length > 0) score += 30
  if (candidate.experience_years && candidate.experience_years > 0) score += 30
  
  return Math.min(score, 100)
}
