import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useSequenceStore = defineStore('sequence', {
  state: () => ({
    sequences: [],
    currentSequence: null,
    loading: false,
    error: null,
    pagination: {
      page: 1,
      limit: 20,
      total: 0,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    },
    filters: {
      search: '',
      status: '',
      owner: ''
    },
    statistics: {
      total: 0,
      active: 0,
      draft: 0,
      paused: 0,
      completed: 0
    }
  }),

  getters: {
    filteredSequences: (state) => {
      let filtered = [...state.sequences]
      
      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        filtered = filtered.filter(sequence => 
          sequence.title?.toLowerCase().includes(search) ||
          sequence.name?.toLowerCase().includes(search) ||
          sequence.purpose?.toLowerCase().includes(search)
        )
      }
      
      if (state.filters.status) {
        filtered = filtered.filter(sequence => sequence.status === state.filters.status)
      }
      
      if (state.filters.owner) {
        filtered = filtered.filter(sequence => sequence.owner_id === state.filters.owner)
      }
      
      return filtered
    },

    getSequenceByName: (state) => (name) => {
      return state.sequences.find(sequence => sequence.name === name)
    },

    sequencesByStatus: (state) => (status) => {
      return state.sequences.filter(sequence => sequence.status === status)
    },

    recentSequences: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.sequences.filter(sequence => {
        const createdAt = new Date(sequence.created_at || sequence.creation)
        return createdAt >= sevenDaysAgo
      })
    }
  },

  actions: {
    async fetchSequences(options = {}) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          doctype: 'Mira Sequence',
          fields: [
            'name', 'title', 'purpose', 'status', 'enrollment_count',
            'owner_id', 'created_at', 'steps', 'enrollment_source',
            'creation', 'modified'
          ],
          limit_page_length: options.limit || this.pagination.limit,
          limit_start: options.page ? (options.page - 1) * (options.limit || this.pagination.limit) : 0,
          order_by: options.order_by || 'modified desc'
        }

        // Add filters
        if (options.filters) {
          params.filters = options.filters
        }

        if (this.filters.search) {
          params.or_filters = [
            ['title', 'like', `%${this.filters.search}%`],
            ['name', 'like', `%${this.filters.search}%`],
            ['purpose', 'like', `%${this.filters.search}%`]
          ]
        }

        if (this.filters.status) {
          params.filters = { ...params.filters, status: this.filters.status }
        }

        if (this.filters.owner) {
          params.filters = { ...params.filters, owner_id: this.filters.owner }
        }

        const [listResult, countResult] = await Promise.all([
          call('frappe.client.get_list', params),
          call('frappe.client.get_count', {
            doctype: 'Mira Sequence',
            filters: params.filters,
            or_filters: params.or_filters
          })
        ])

        if (listResult && Array.isArray(listResult)) {
          // Enhance data with display fields
          this.sequences = listResult.map(sequence => ({
            ...sequence,
            display_status: this.getStatusDisplay(sequence.status),
            status_color: this.getStatusColor(sequence.status),
            steps_count: this.getStepsCount(sequence.steps),
            formatted_created_at: this.formatDate(sequence.created_at || sequence.creation),
            formatted_modified: this.formatRelativeDate(sequence.modified)
          }))

          // Update pagination
          this.pagination.total = countResult || 0
          this.pagination.page = options.page || 1
          this.pagination.limit = options.limit || this.pagination.limit
          this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
          this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
          this.pagination.has_next = this.pagination.showing_to < this.pagination.total
          this.pagination.has_prev = this.pagination.page > 1

          return { success: true, data: this.sequences }
        }

        return { success: false, message: 'No data received' }
      } catch (error) {
        console.error('Error fetching sequences:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchSequenceById(id) {
      this.loading = true
      this.error = null
      
      try {
        const sequenceResult = await call('frappe.client.get', {
          doctype: 'Mira Sequence',
          name: id
        })

        if (sequenceResult && sequenceResult.name) {
          // Enhance data with display fields
          const enhancedSequence = {
            ...sequenceResult,
            display_status: this.getStatusDisplay(sequenceResult.status),
            status_color: this.getStatusColor(sequenceResult.status),
            steps_count: this.getStepsCount(sequenceResult.steps),
            formatted_created_at: this.formatDate(sequenceResult.created_at || sequenceResult.creation),
            formatted_modified: this.formatRelativeDate(sequenceResult.modified)
          }

          this.currentSequence = enhancedSequence
          return { success: true, data: enhancedSequence }
        }

        return { success: false, message: 'Sequence not found' }
      } catch (error) {
        console.error('Error fetching sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createSequence(sequenceData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateSequence(sequenceData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        const preparedData = this.prepareSequenceForSave(sequenceData)
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Sequence',
            ...preparedData
          }
        })

        if (result && result.name) {
          // Refresh sequences list
          await this.fetchSequences()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to create sequence' }
      } catch (error) {
        console.error('Error creating sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateSequence(name, sequenceData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateSequence(sequenceData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        // Prepare complete sequence data
        const completeSequenceData = {
          title: sequenceData.title?.trim(),
          purpose: sequenceData.purpose?.trim() || '',
          status: sequenceData.status || 'Draft',
          enrollment_source: sequenceData.enrollment_source?.trim() || '',
          steps: sequenceData.steps || '[]'
        }
        
        // Update with complete data in one call
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira Sequence',
          name: name,
          fieldname: completeSequenceData
        })

        if (result) {
          // Refresh sequences list
          await this.fetchSequences()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to update sequence' }
      } catch (error) {
        console.error('Error updating sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteSequence(sequenceId) {
      this.loading = true
      this.error = null
      
      try {
        // Check if sequence can be deleted (not Active)
        const sequence = this.getSequenceByName(sequenceId)
        if (sequence && sequence.status === 'Active') {
          throw new Error('Không thể xóa sequence đang hoạt động. Vui lòng tạm dừng sequence trước khi xóa.')
        }

        const result = await call('frappe.client.delete', {
          doctype: 'Mira Sequence',
          name: sequenceId
        })

        if (result === undefined) {
          // Remove from local state
          this.sequences = this.sequences.filter(sequence => sequence.name !== sequenceId)
          
          // Update pagination
          this.pagination.total = Math.max(0, this.pagination.total - 1)
          
          return { success: true }
        }

        return { success: false, message: 'Failed to delete sequence' }
      } catch (error) {
        console.error('Error deleting sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async duplicateSequence(sequenceId) {
      this.loading = true
      this.error = null
      
      try {
        // First get the original sequence
        const originalSequence = await call('frappe.client.get', {
          doctype: 'Mira Sequence',
          name: sequenceId
        })

        if (!originalSequence) {
          throw new Error('Original sequence not found')
        }

        // Prepare duplicate data
        const duplicateData = {
          title: `${originalSequence.title} (Copy)`,
          purpose: originalSequence.purpose,
          status: 'Draft', // Always create duplicates as Draft
          enrollment_source: originalSequence.enrollment_source,
          steps: originalSequence.steps
        }

        // Create the duplicate
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Sequence',
            ...duplicateData
          }
        })

        if (result && result.name) {
          // Refresh sequences list
          await this.fetchSequences()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to duplicate sequence' }
      } catch (error) {
        console.error('Error duplicating sequence:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async searchSequences(searchText) {
      this.filters.search = searchText
      return await this.fetchSequences({ page: 1 })
    },

    async fetchStatistics() {
      try {
        const [totalResult, statusResults] = await Promise.all([
          call('frappe.client.get_count', { doctype: 'Mira Sequence' }),
          call('frappe.client.get_list', {
            doctype: 'Mira Sequence',
            fields: ['status'],
            limit_page_length: 1000
          })
        ])

        // Count by status
        const statusCounts = { active: 0, draft: 0, paused: 0, completed: 0 }
        if (statusResults && Array.isArray(statusResults)) {
          statusResults.forEach(item => {
            const status = item.status?.toLowerCase()
            if (statusCounts.hasOwnProperty(status)) {
              statusCounts[status]++
            }
          })
        }

        this.statistics = {
          total: totalResult || 0,
          ...statusCounts
        }

        return this.statistics
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return this.statistics
      }
    },

    async getSequence(name) {
      try {
        const result = await call('frappe.client.get', {
          doctype: 'Mira Sequence',
          name: name
        })

        if (result) {
          return {
            success: true,
            data: {
              ...result,
              display_status: this.getStatusDisplay(result.status),
              status_color: this.getStatusColor(result.status),
              steps_count: this.getStepsCount(result.steps),
              formatted_created_at: this.formatDate(result.created_at || result.creation),
              formatted_modified: this.formatRelativeDate(result.modified)
            }
          }
        }

        return { success: false, error: 'Sequence not found' }
      } catch (error) {
        console.error('Error fetching sequence:', error)
        return { 
          success: false, 
          error: this.parseError(error) || 'Failed to fetch sequence details'
        }
      }
    },

    // Helper methods
    validateSequence(sequenceData) {
      if (!sequenceData.title || sequenceData.title.trim().length === 0) {
        return { isValid: false, message: 'Tên sequence là bắt buộc' }
      }

      if (sequenceData.title.length > 200) {
        return { isValid: false, message: 'Tên sequence không được vượt quá 200 ký tự' }
      }

      const validStatuses = ['Active', 'Draft', 'Paused', 'Completed']
      if (sequenceData.status && !validStatuses.includes(sequenceData.status)) {
        return { isValid: false, message: 'Trạng thái không hợp lệ' }
      }

      return { isValid: true }
    },

    prepareSequenceForSave(sequenceData) {
      return {
        title: sequenceData.title?.trim(),
        purpose: sequenceData.purpose?.trim() || '',
        status: sequenceData.status || 'Draft',
        enrollment_source: sequenceData.enrollment_source?.trim() || '',
        steps: sequenceData.steps || '[]'
      }
    },

    getStatusDisplay(status) {
      const statusMap = {
        'Active': 'Hoạt động',
        'Draft': 'Nháp',
        'Paused': 'Tạm dừng',
        'Completed': 'Hoàn thành'
      }
      return statusMap[status] || status
    },

    getStatusColor(status) {
      const colorMap = {
        'Active': 'green',
        'Draft': 'gray',
        'Paused': 'yellow',
        'Completed': 'blue'
      }
      return colorMap[status] || 'gray'
    },

    getStepsCount(stepsJson) {
      try {
        if (!stepsJson) return 0
        const steps = typeof stepsJson === 'string' ? JSON.parse(stepsJson) : stepsJson
        return Array.isArray(steps) ? steps.length : 0
      } catch (error) {
        return 0
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('vi-VN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (error) {
        return dateString
      }
    },

    formatRelativeDate(dateString) {
      if (!dateString) return ''
      
      try {
        const date = new Date(dateString)
        const now = new Date()
        const diffInSeconds = Math.floor((now - date) / 1000)
        
        if (diffInSeconds < 60) return 'Vừa xong'
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} phút trước`
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} giờ trước`
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} ngày trước`
        
        return this.formatDate(dateString)
      } catch (error) {
        return dateString
      }
    },

    parseError(error) {
      if (typeof error === 'string') return error
      if (error?.message) return error.message
      if (error?.exc_type && error?.exc) return `${error.exc_type}: ${error.exc}`
      return 'An unexpected error occurred'
    },

    // Filter methods
    setSearch(searchText) {
      this.filters.search = searchText
    },

    setStatusFilter(status) {
      this.filters.status = status
    },

    setOwnerFilter(owner) {
      this.filters.owner = owner
    },

    clearFilters() {
      this.filters = {
        search: '',
        status: '',
        owner: ''
      }
    }
  }
})
