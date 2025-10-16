import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useMiraFlowStore = defineStore('miraFlow', {
  state: () => ({
    flows: [],
    currentFlow: null,
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
      archived: 0
    }
  }),

  getters: {
    filteredFlows: (state) => {
      let filtered = [...state.flows]
      
      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        filtered = filtered.filter(flow => 
          flow.title?.toLowerCase().includes(search) ||
          flow.description?.toLowerCase().includes(search) ||
          flow.tags?.toLowerCase().includes(search)
        )
      }
      
      if (state.filters.status) {
        filtered = filtered.filter(flow => flow.status === state.filters.status)
      }
      
      if (state.filters.owner) {
        filtered = filtered.filter(flow => flow.owner_id === state.filters.owner)
      }
      
      return filtered
    },

    getFlowByName: (state) => (name) => {
      return state.flows.find(flow => flow.name === name)
    },

    flowsByStatus: (state) => (status) => {
      return state.flows.filter(flow => flow.status === status)
    },

    activeFlows: (state) => {
      return state.flows.filter(flow => flow.status === 'Active')
    },

    recentFlows: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.flows.filter(flow => {
        const createdAt = new Date(flow.created_at || flow.creation)
        return createdAt >= sevenDaysAgo
      })
    }
  },

  actions: {
    async fetchFlows(options = {}) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          doctype: 'Mira flow',
          fields: [
            'name', 'title', 'description', 'status', 'tags', 
            'owner_id', 'created_at', 'creation', 'modified'
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
            ['description', 'like', `%${this.filters.search}%`],
            ['tags', 'like', `%${this.filters.search}%`]
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
            doctype: 'Mira flow',
            filters: params.filters,
            or_filters: params.or_filters
          })
        ])

        if (listResult && Array.isArray(listResult)) {
          // Enhance data with display fields
          this.flows = listResult.map(flow => ({
            ...flow,
            display_status: this.getStatusDisplay(flow.status),
            status_color: this.getStatusColor(flow.status),
            formatted_created_at: this.formatDate(flow.created_at || flow.creation),
            formatted_modified: this.formatRelativeDate(flow.modified)
          }))

          // Update pagination
          this.pagination.total = countResult || 0
          this.pagination.page = options.page || 1
          this.pagination.limit = options.limit || this.pagination.limit
          this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
          this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
          this.pagination.has_next = this.pagination.showing_to < this.pagination.total
          this.pagination.has_prev = this.pagination.page > 1

          return { success: true, data: this.flows }
        }

        return { success: false, message: 'No data received' }
      } catch (error) {
        console.error('Error fetching flows:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchFlowById(id) {
      this.loading = true
      this.error = null
      
      try {
        const result = await call('frappe.client.get', {
          doctype: 'Mira flow',
          name: id
        })

        if (result && result.name) {
          // Enhance data with display fields
          const enhancedFlow = {
            ...result,
            display_status: this.getStatusDisplay(result.status),
            status_color: this.getStatusColor(result.status),
            formatted_created_at: this.formatDate(result.created_at || result.creation),
            formatted_modified: this.formatRelativeDate(result.modified)
          }

          this.currentFlow = enhancedFlow
          return { success: true, data: enhancedFlow }
        }

        return { success: false, message: 'Flow not found' }
      } catch (error) {
        console.error('Error fetching flow:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createFlow(flowData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateFlow(flowData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        const preparedData = this.prepareFlowForSave(flowData)
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira flow',
            ...preparedData
          }
        })

        if (result && result.name) {
          // Refresh flows list
          await this.fetchFlows()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to create flow' }
      } catch (error) {
        console.error('Error creating flow:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateFlow(name, flowData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateFlow(flowData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        const preparedData = this.prepareFlowForSave(flowData)
        
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira flow',
          name: name,
          fieldname: preparedData
        })

        if (result) {
          // Refresh flows list
          await this.fetchFlows()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to update flow' }
      } catch (error) {
        console.error('Error updating flow:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteFlow(flowId) {
      this.loading = true
      this.error = null
      
      try {
        const result = await call('frappe.client.delete', {
          doctype: 'Mira flow',
          name: flowId
        })

        if (result === undefined) {
          // Remove from local state
          this.flows = this.flows.filter(flow => flow.name !== flowId)
          
          // Update pagination
          this.pagination.total = Math.max(0, this.pagination.total - 1)
          
          return { success: true }
        }

        return { success: false, message: 'Failed to delete flow' }
      } catch (error) {
        console.error('Error deleting flow:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async duplicateFlow(flowId) {
      this.loading = true
      this.error = null
      
      try {
        // First get the original flow
        const originalFlow = await call('frappe.client.get', {
          doctype: 'Mira flow',
          name: flowId
        })

        if (!originalFlow) {
          throw new Error('Original flow not found')
        }

        // Prepare duplicate data
        const duplicateData = {
          title: `${originalFlow.title} (Copy)`,
          description: originalFlow.description,
          status: 'Draft', // Always create as draft
          tags: originalFlow.tags,
        }

        // Create the duplicate
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira flow',
            ...duplicateData
          }
        })

        if (result && result.name) {
          // Refresh flows list
          await this.fetchFlows()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to duplicate flow' }
      } catch (error) {
        console.error('Error duplicating flow:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async searchFlows(searchText) {
      this.filters.search = searchText
      return await this.fetchFlows({ page: 1 })
    },

    async fetchStatistics() {
      try {
        const [totalResult, activeResult, draftResult, pausedResult, archivedResult] = await Promise.all([
          call('frappe.client.get_count', { doctype: 'Mira flow' }),
          call('frappe.client.get_count', { doctype: 'Mira flow', filters: { status: 'Active' } }),
          call('frappe.client.get_count', { doctype: 'Mira flow', filters: { status: 'Draft' } }),
          call('frappe.client.get_count', { doctype: 'Mira flow', filters: { status: 'Paused' } }),
          call('frappe.client.get_count', { doctype: 'Mira flow', filters: { status: 'Archived' } })
        ])

        this.statistics = {
          total: totalResult || 0,
          active: activeResult || 0,
          draft: draftResult || 0,
          paused: pausedResult || 0,
          archived: archivedResult || 0
        }

        return this.statistics
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return this.statistics
      }
    },

    // Helper methods
    validateFlow(flowData) {
      if (!flowData.title || flowData.title.trim().length === 0) {
        return { isValid: false, message: 'Flow title is required' }
      }

      if (flowData.title.length > 200) {
        return { isValid: false, message: 'Flow title must be less than 200 characters' }
      }

      return { isValid: true }
    },

    prepareFlowForSave(flowData) {
      return {
        title: flowData.title?.trim(),
        description: flowData.description?.trim() || '',
        status: flowData.status || 'Draft',
        tags: flowData.tags?.trim() || '',
        owner_id: flowData.owner_id,
        triggers: flowData.triggers || JSON.stringify({}),
        actions: flowData.actions || JSON.stringify([])
      }
    },

    getStatusDisplay(status) {
      const statusMap = {
        'Active': 'Đang hoạt động',
        'Draft': 'Bản nháp',
        'Paused': 'Tạm dừng',
        'Archived': 'Đã lưu trữ'
      }
      return statusMap[status] || status
    },

    getStatusColor(status) {
      const colorMap = {
        'Active': 'green',
        'Draft': 'gray',
        'Paused': 'yellow',
        'Archived': 'red'
      }
      return colorMap[status] || 'gray'
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
