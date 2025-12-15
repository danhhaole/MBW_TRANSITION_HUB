import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useBlacklistStore = defineStore('blacklist', {
  state: () => ({
    blacklists: [],
    currentBlacklist: null,
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
      owner: ''
    },
    statistics: {
      total: 0
    }
  }),

  getters: {
    filteredBlacklists: (state) => {
      let filtered = [...state.blacklists]
      
      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        filtered = filtered.filter(blacklist => 
          blacklist.email?.toLowerCase().includes(search) ||
          blacklist.tag?.toLowerCase().includes(search) ||
          blacklist.name?.toLowerCase().includes(search)
        )
      }
      
      if (state.filters.owner) {
        filtered = filtered.filter(blacklist => blacklist.owner === state.filters.owner)
      }
      
      return filtered
    },

    getBlacklistByName: (state) => (name) => {
      return state.blacklists.find(blacklist => blacklist.name === name)
    }
  },

  actions: {
    async fetchBlacklists(options = {}) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          doctype: 'Mira BlackList',
          fields: [
            'name', 'email', 'tag',
            'owner', 'creation', 'modified'
          ],
          limit_page_length: options.limit || this.pagination.limit,
          limit_start: options.page ? (options.page - 1) * (options.limit || this.pagination.limit) : 0,
          order_by: options.order_by || 'creation desc'
        }

        // Add filters
        if (options.filters) {
          params.filters = options.filters
        }

        if (this.filters.search) {
          params.or_filters = [
            ['email', 'like', `%${this.filters.search}%`],
            ['tag', 'like', `%${this.filters.search}%`],
            ['name', 'like', `%${this.filters.search}%`]
          ]
        }

        if (this.filters.owner) {
          params.filters = { ...params.filters, owner: this.filters.owner }
        }

        // Try the new combined API first, fallback to old API if it fails
        let result
        try {
          result = await call('mbw_mira.api.doc.get_list_data', params)
          
          if (result && result.success && Array.isArray(result.data)) {
            // Enhance data with display fields
            this.blacklists = result.data.map(blacklist => ({
              ...blacklist,
              formatted_created_at: this.formatDate(blacklist.creation),
              formatted_modified: this.formatRelativeDate(blacklist.modified)
            }))

            // Update pagination
            this.pagination.total = result.count || 0
            this.pagination.page = options.page || 1
            this.pagination.limit = options.limit || this.pagination.limit
            this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
            this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
            this.pagination.has_next = this.pagination.showing_to < this.pagination.total
            this.pagination.has_prev = this.pagination.page > 1

            return { success: true, data: this.blacklists, count: result.count }
          } else {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed, falling back to old API:', newApiError.message)
          
          // Fallback to old separate API calls
          const [listResult, countResult] = await Promise.all([
            call('frappe.client.get_list', params),
            call('frappe.client.get_count', {
              doctype: 'Mira BlackList',
              filters: params.filters,
              or_filters: params.or_filters
            })
          ])

          if (listResult && Array.isArray(listResult)) {
            // Enhance data with display fields
            this.blacklists = listResult.map(blacklist => ({
              ...blacklist,
              formatted_created_at: this.formatDate(blacklist.creation),
              formatted_modified: this.formatRelativeDate(blacklist.modified)
            }))

            // Update pagination
            this.pagination.total = countResult || 0
            this.pagination.page = options.page || 1
            this.pagination.limit = options.limit || this.pagination.limit
            this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
            this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
            this.pagination.has_next = this.pagination.showing_to < this.pagination.total
            this.pagination.has_prev = this.pagination.page > 1

            return { success: true, data: this.blacklists, count: countResult }
          }
        }

        return { success: false, message: 'No data received' }
      } catch (error) {
        console.error('Error fetching blacklists:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createBlacklist(blacklistData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateBlacklist(blacklistData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        const preparedData = this.prepareBlacklistForSave(blacklistData)
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira BlackList',
            ...preparedData
          }
        })

        if (result && result.name) {
          // Refresh blacklists list
          await this.fetchBlacklists()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to create blacklist' }
      } catch (error) {
        console.error('Error creating blacklist:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateBlacklist(name, blacklistData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateBlacklist(blacklistData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        // Prepare complete blacklist data
        const completeBlacklistData = {
          email: blacklistData.email?.trim(),
          tag: blacklistData.tag?.trim() || ''
        }
        
        // Update with complete data in one call
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira BlackList',
          name: name,
          fieldname: completeBlacklistData
        })

        if (result) {
          // Refresh blacklists list
          await this.fetchBlacklists()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to update blacklist' }
      } catch (error) {
        console.error('Error updating blacklist:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteBlacklist(blacklistId) {
      this.loading = true
      this.error = null
      
      try {
        const result = await call('frappe.client.delete', {
          doctype: 'Mira BlackList',
          name: blacklistId
        })

        if (result === undefined) {
          // Remove from local state
          this.blacklists = this.blacklists.filter(blacklist => blacklist.name !== blacklistId)
          
          // Update pagination
          this.pagination.total = Math.max(0, this.pagination.total - 1)
          
          return { success: true }
        }

        return { success: false, message: 'Failed to delete blacklist' }
      } catch (error) {
        console.error('Error deleting blacklist:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async getBlacklist(name) {
      try {
        const result = await call('frappe.client.get', {
          doctype: 'Mira BlackList',
          name: name
        })

        if (result) {
          return {
            success: true,
            data: {
              ...result,
              formatted_created_at: this.formatDate(result.creation),
              formatted_modified: this.formatRelativeDate(result.modified)
            }
          }
        }

        return { success: false, error: 'Blacklist not found' }
      } catch (error) {
        console.error('Error fetching blacklist:', error)
        return { 
          success: false, 
          error: this.parseError(error) || 'Failed to fetch blacklist details'
        }
      }
    },

    async fetchStatistics() {
      try {
        // Try new API first
        try {
          const result = await call('mbw_mira.api.doc.get_list_data', {
            doctype: 'Mira BlackList',
            fields: ['name'],
            limit_page_length: 1
          })

          if (result && result.success) {
            this.statistics = {
              total: result.count || 0
            }
            return this.statistics
          } else {
            throw new Error('New API returned invalid response')
          }
        } catch (newApiError) {
          console.warn('New API failed for statistics, falling back to old API:', newApiError.message)
          
          // Fallback to old API
          const totalResult = await call('frappe.client.get_count', { doctype: 'Mira BlackList' })
          this.statistics = {
            total: totalResult || 0
          }
          return this.statistics
        }
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return this.statistics
      }
    },

    // Helper methods
    validateBlacklist(blacklistData) {
      if (!blacklistData.email || blacklistData.email.trim().length === 0) {
        return { isValid: false, message: 'Email is required' }
      }

      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(blacklistData.email)) {
        return { isValid: false, message: 'Invalid email format' }
      }

      return { isValid: true }
    },

    prepareBlacklistForSave(blacklistData) {
      return {
        email: blacklistData.email?.trim(),
        tag: blacklistData.tag?.trim() || ''
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

    setOwnerFilter(owner) {
      this.filters.owner = owner
    },

    clearFilters() {
      this.filters = {
        search: '',
        owner: ''
      }
    }
  }
})
