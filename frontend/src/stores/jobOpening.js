import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useJobOpeningStore = defineStore('jobOpening', {
  state: () => ({
    jobOpenings: [],
    currentJobOpening: null,
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
    statusFilter: '',
    departmentFilter: '',
    locationFilter: '',
    orderBy: 'modified desc',
    // Statistics
    statistics: {
      total: 0,
      by_status: {},
      by_department: {},
      recent: 0
    },
    // Filter options
    filterOptions: {
      statuses: [],
      departments: [],
      locations: []
    }
  }),

  getters: {
    // Client-side filtered job openings
    filteredJobOpenings: (state) => {
      let filtered = state.jobOpenings

      if (state.searchText) {
        filtered = filtered.filter(job =>
          job.job_title?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          job.job_code?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          job.department_name?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.statusFilter) {
        filtered = filtered.filter(job => job.approval_status === state.statusFilter)
      }

      if (state.departmentFilter) {
        filtered = filtered.filter(job => job.department_name === state.departmentFilter)
      }

      if (state.locationFilter) {
        filtered = filtered.filter(job => job.location_name === state.locationFilter)
      }

      return filtered
    },

    // Get job opening by name
    getJobOpeningByName: (state) => (name) => {
      return state.jobOpenings.find(job => job.name === name)
    },

    // Job openings by status
    jobOpeningsByStatus: (state) => (status) => {
      return state.jobOpenings.filter(job => job.approval_status === status)
    },

    // Active job openings
    activeJobOpenings: (state) => {
      return state.jobOpenings.filter(job => job.approval_status === 'Approved')
    },

    // Recent job openings (last 7 days)
    recentJobOpenings: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.jobOpenings.filter(job => {
        const creationDate = new Date(job.creation)
        return creationDate >= sevenDaysAgo
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

    // Set filters
    setSearchText(text) {
      this.searchText = text
    },

    setStatusFilter(status) {
      this.statusFilter = status
    },

    setDepartmentFilter(department) {
      this.departmentFilter = department
    },

    setLocationFilter(location) {
      this.locationFilter = location
    },

    setOrderBy(orderBy) {
      this.orderBy = orderBy
    },

    // Reset filters
    resetFilters() {
      this.searchText = ''
      this.statusFilter = ''
      this.departmentFilter = ''
      this.locationFilter = ''
      this.orderBy = 'modified desc'
    },

    // Get job openings with pagination and filters
    async fetchJobOpenings(options = {}) {
      this.setLoading(true)

      try {
        const {
          filters = {},
          or_filters = undefined,
          fields = [
            'name', 'job_title', 'job_code', 'department_name', 'location_name', 'owner_id',
            'number_of_openings', 'posting_date', 'closing_date', 'approval_status', 'total_applicants',
            'creation', 'modified'
          ],
          order_by = this.orderBy,
          page_length = this.pagination.limit,
          start = (this.pagination.page - 1) * this.pagination.limit
        } = options

        // Build filters
        let enhancedFilters = { ...filters }

        if (this.searchText && this.searchText.trim()) {
          or_filters = [
            ['job_title', 'like', `%${this.searchText.trim()}%`],
            ['job_code', 'like', `%${this.searchText.trim()}%`],
            ['department_name', 'like', `%${this.searchText.trim()}%`]
          ]
        }

        if (this.statusFilter) {
          enhancedFilters['approval_status'] = this.statusFilter
        }

        if (this.departmentFilter) {
          enhancedFilters['department_name'] = this.departmentFilter
        }

        if (this.locationFilter) {
          enhancedFilters['location_name'] = this.locationFilter
        }

        // Fetch job openings
        const response = await call('frappe.client.get_list', {
          doctype: 'JobOpening',
          filters: enhancedFilters,
          or_filters: or_filters,
          fields: fields,
          order_by: order_by,
          limit_start: start,
          limit_page_length: page_length
        })

        // Get total count for pagination
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'JobOpening',
          filters: enhancedFilters,
          or_filters: or_filters
        })

        // Process job openings to add display fields
        const processedJobOpenings = (response || []).map(job => ({
          ...job,
          display_status: this.getStatusDisplay(job.approval_status),
          formattedPostingDate: this.formatDate(job.posting_date),
          formattedClosingDate: this.formatDate(job.closing_date),
          formattedCreation: this.formatDate(job.creation),
          relativeCreation: this.formatRelativeDate(job.creation),
          isExpired: this.isJobExpired(job.closing_date)
        }))

        this.jobOpenings = processedJobOpenings

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

        this.setSuccess('Job openings loaded successfully')
        return {
          success: true,
          data: processedJobOpenings,
          pagination: this.pagination
        }
      } catch (error) {
        console.error('Error fetching job openings:', error)
        this.setError(error.message || 'Failed to fetch job openings')
        return {
          success: false,
          error: error.message || 'Failed to fetch job openings'
        }
      }
    },

    // Get job opening by name
    async fetchJobOpeningById(name) {
      this.setLoading(true)

      try {
        const response = await call('frappe.client.get', {
          doctype: 'JobOpening',
          name: name
        })

        if (response) {
          const processedJobOpening = {
            ...response,
            display_status: this.getStatusDisplay(response.approval_status),
            formattedPostingDate: this.formatDate(response.posting_date),
            formattedClosingDate: this.formatDate(response.closing_date),
            formattedCreation: this.formatDate(response.creation),
            relativeCreation: this.formatRelativeDate(response.creation),
            isExpired: this.isJobExpired(response.closing_date)
          }

          this.currentJobOpening = processedJobOpening
          this.setSuccess('Job opening loaded successfully')

          return {
            success: true,
            data: processedJobOpening
          }
        } else {
          throw new Error('Job opening not found')
        }
      } catch (error) {
        console.error('Error fetching job opening:', error)
        this.setError(error.message || 'Failed to fetch job opening')
        return {
          success: false,
          error: error.message || 'Failed to fetch job opening'
        }
      }
    },

    // Create new job opening
    async createJobOpening(data) {
      this.setLoading(true)

      try {
        // Validate required fields
        const validationErrors = this.validateJobOpening(data, 'create')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for creation
        const preparedData = this.prepareJobOpeningForSave(data, 'create')

        const docData = {
          doctype: 'JobOpening',
          ...preparedData
        }

        const response = await call('frappe.client.insert', {
          doc: docData
        })

        if (response) {
          // Add to local state
          const newJobOpening = {
            ...response,
            display_status: this.getStatusDisplay(response.approval_status),
            formattedPostingDate: this.formatDate(response.posting_date),
            formattedClosingDate: this.formatDate(response.closing_date),
            formattedCreation: this.formatDate(response.creation),
            relativeCreation: this.formatRelativeDate(response.creation),
            isExpired: this.isJobExpired(response.closing_date)
          }

          this.jobOpenings.unshift(newJobOpening)
          this.currentJobOpening = newJobOpening

          this.setSuccess('Job opening created successfully')
          return {
            success: true,
            data: newJobOpening,
            message: 'Job opening created successfully'
          }
        } else {
          throw new Error('Failed to create job opening')
        }
      } catch (error) {
        console.error('Error creating job opening:', error)
        this.setError(this.parseError(error) || 'Failed to create job opening')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to create job opening'
        }
      }
    },

    // Update job opening
    async updateJobOpening(name, data) {
      this.setLoading(true)

      try {
        // Validate required fields
        const validationErrors = this.validateJobOpening(data, 'update')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for update
        const preparedData = this.prepareJobOpeningForSave(data, 'update')

        const response = await call('frappe.client.set_value', {
          doctype: 'JobOpening',
          name: name,
          fieldname: preparedData
        })

        if (response) {
          // Update local state
          const index = this.jobOpenings.findIndex(j => j.name === name)
          if (index !== -1) {
            this.jobOpenings[index] = {
              ...this.jobOpenings[index],
              ...preparedData,
              display_status: this.getStatusDisplay(preparedData.approval_status),
              formattedPostingDate: this.formatDate(preparedData.posting_date),
              formattedClosingDate: this.formatDate(preparedData.closing_date),
              isExpired: this.isJobExpired(preparedData.closing_date)
            }
          }

          if (this.currentJobOpening && this.currentJobOpening.name === name) {
            this.currentJobOpening = {
              ...this.currentJobOpening,
              ...preparedData,
              display_status: this.getStatusDisplay(preparedData.approval_status),
              formattedPostingDate: this.formatDate(preparedData.posting_date),
              formattedClosingDate: this.formatDate(preparedData.closing_date),
              isExpired: this.isJobExpired(preparedData.closing_date)
            }
          }

          this.setSuccess('Job opening updated successfully')
          return {
            success: true,
            data: response,
            message: 'Job opening updated successfully'
          }
        } else {
          throw new Error('Failed to update job opening')
        }
      } catch (error) {
        console.error('Error updating job opening:', error)
        this.setError(this.parseError(error) || 'Failed to update job opening')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to update job opening'
        }
      }
    },

    // Delete job opening
    async deleteJobOpening(name) {
      this.setLoading(true)

      try {
        await call('frappe.client.delete', {
          doctype: 'JobOpening',
          name: name
        })

        // Remove from local state
        this.jobOpenings = this.jobOpenings.filter(j => j.name !== name)

        if (this.currentJobOpening && this.currentJobOpening.name === name) {
          this.currentJobOpening = null
        }

        this.setSuccess('Job opening deleted successfully')
        return {
          success: true,
          message: 'Job opening deleted successfully'
        }
      } catch (error) {
        console.error('Error deleting job opening:', error)
        this.setError(this.parseError(error) || 'Failed to delete job opening')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to delete job opening'
        }
      }
    },

    // Search job openings
    async searchJobOpenings(query = "", limit = 10) {
      try {
        const filters = [
          ['job_title', 'like', `%${query}%`]
        ]

        const response = await call('frappe.client.get_list', {
          doctype: 'JobOpening',
          filters: filters,
          fields: ['name', 'job_title', 'job_code', 'department_name', 'location_name', 'approval_status'],
          limit_page_length: limit
        })

        const processedJobOpenings = (response || []).map(job => ({
          ...job,
          display_status: this.getStatusDisplay(job.approval_status)
        }))

        return {
          success: true,
          data: processedJobOpenings
        }
      } catch (error) {
        console.error('Error searching job openings:', error)
        return {
          success: false,
          error: error.message || 'Failed to search job openings'
        }
      }
    },

    // Get statistics
    async fetchStatistics() {
      try {
        // Get statistics by status
        const statusStats = await call('frappe.client.get_list', {
          doctype: 'JobOpening',
          fields: ['approval_status', 'count(*) as count'],
          group_by: 'approval_status'
        })

        // Get statistics by department
        const departmentStats = await call('frappe.client.get_list', {
          doctype: 'JobOpening',
          fields: ['department_name', 'count(*) as count'],
          group_by: 'department_name'
        })

        // Get total count
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'JobOpening'
        })

        // Get recent count (last 7 days)
        const sevenDaysAgo = new Date()
        sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
        const recentCount = await call('frappe.client.get_count', {
          doctype: 'JobOpening',
          filters: [['creation', '>=', sevenDaysAgo.toISOString().split('T')[0]]]
        })

        const statistics = {
          total: totalCount || 0,
          by_status: {},
          by_department: {},
          recent: recentCount || 0
        }

        // Process status statistics
        if (statusStats && Array.isArray(statusStats)) {
          statusStats.forEach(stat => {
            statistics.by_status[stat.approval_status] = stat.count
          })
        }

        // Process department statistics
        if (departmentStats && Array.isArray(departmentStats)) {
          departmentStats.forEach(stat => {
            statistics.by_department[stat.department_name] = stat.count
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
        const [statusOptions, departmentOptions, locationOptions] = await Promise.all([
          call('frappe.client.get_list', {
            doctype: 'JobOpening',
            fields: ['approval_status'],
            distinct: true,
            order_by: 'approval_status'
          }),
          call('frappe.client.get_list', {
            doctype: 'JobOpening',
            fields: ['department_name'],
            distinct: true,
            order_by: 'department_name'
          }),
          call('frappe.client.get_list', {
            doctype: 'JobOpening',
            fields: ['location_name'],
            distinct: true,
            order_by: 'location_name'
          })
        ])

        this.filterOptions = {
          statuses: (statusOptions || []).filter(item => item.approval_status).map(item => ({
            label: item.approval_status,
            value: item.approval_status
          })),
          departments: (departmentOptions || []).filter(item => item.department_name).map(item => ({
            label: item.department_name,
            value: item.department_name
          })),
          locations: (locationOptions || []).filter(item => item.location_name).map(item => ({
            label: item.location_name,
            value: item.location_name
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
    validateJobOpening(data, action = 'create') {
      const errors = []

      // Required fields
      if (!data.job_title || !data.job_title.trim()) {
        errors.push('Job title is required')
      }

      // Business rules
      if (data.job_title && data.job_title.length > 200) {
        errors.push('Job title must be less than 200 characters')
      }

      if (data.number_of_openings && (isNaN(data.number_of_openings) || data.number_of_openings < 1)) {
        errors.push('Number of openings must be a positive number')
      }

      // Date validation
      if (data.posting_date && data.closing_date) {
        const postingDate = new Date(data.posting_date)
        const closingDate = new Date(data.closing_date)
        if (closingDate <= postingDate) {
          errors.push('Closing date must be after posting date')
        }
      }

      return errors
    },

    prepareJobOpeningForSave(data, action = 'create') {
      const prepared = { ...data }

      // Trim strings
      if (prepared.job_title) {
        prepared.job_title = prepared.job_title.trim()
      }
      if (prepared.job_code) {
        prepared.job_code = prepared.job_code.trim()
      }
      if (prepared.department_name) {
        prepared.department_name = prepared.department_name.trim()
      }
      if (prepared.location_name) {
        prepared.location_name = prepared.location_name.trim()
      }

      // Set defaults
      if (action === 'create') {
        prepared.approval_status = prepared.approval_status || 'Draft'
        prepared.number_of_openings = prepared.number_of_openings || 1
      }

      return prepared
    },

    getStatusDisplay(status) {
      const statusMap = {
        'Draft': 'Draft',
        'Approved': 'Approved',
        'Rejected': 'Rejected',
        'Closed': 'Closed',
        'On Hold': 'On Hold'
      }
      return statusMap[status] || status || 'Unknown'
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

    isJobExpired(closingDate) {
      if (!closingDate) return false
      const today = new Date()
      const closing = new Date(closingDate)
      return closing < today
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