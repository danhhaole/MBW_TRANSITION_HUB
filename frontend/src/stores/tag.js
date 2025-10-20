import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useTagStore = defineStore('tag', {
  state: () => ({
    tags: [],
    currentTag: null,
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
      total: 0
    }
  }),

  getters: {
    filteredTags: (state) => {
      let filtered = [...state.tags]
      
      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        filtered = filtered.filter(tag => 
          tag.title?.toLowerCase().includes(search) ||
          tag.name?.toLowerCase().includes(search)
        )
      }
      
      if (state.filters.owner) {
        filtered = filtered.filter(tag => tag.owner === state.filters.owner)
      }
      
      return filtered
    },

    getTagByName: (state) => (name) => {
      return state.tags.find(tag => tag.name === name)
    },

    tagsByOrder: (state) => {
      return [...state.tags].sort((a, b) => (a.order || 0) - (b.order || 0))
    },

    recentTags: (state) => {
      const sevenDaysAgo = new Date()
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
      
      return state.tags.filter(tag => {
        const createdAt = new Date(tag.creation)
        return createdAt >= sevenDaysAgo
      })
    }
  },

  actions: {
    async fetchTags(options = {}) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          doctype: 'Mira Tag',
          fields: [
            'name', 'title', 'color', 'order',
            'owner', 'creation', 'modified'
          ],
          limit_page_length: options.limit || this.pagination.limit,
          limit_start: options.page ? (options.page - 1) * (options.limit || this.pagination.limit) : 0,
          order_by: options.order_by || '`order` asc'
        }

        // Add filters
        if (options.filters) {
          params.filters = options.filters
        }

        if (this.filters.search) {
          params.or_filters = [
            ['title', 'like', `%${this.filters.search}%`],
            ['name', 'like', `%${this.filters.search}%`]
          ]
        }

        if (this.filters.owner) {
          params.filters = { ...params.filters, owner: this.filters.owner }
        }

        const [listResult, countResult] = await Promise.all([
          call('frappe.client.get_list', params),
          call('frappe.client.get_count', {
            doctype: 'Mira Tag',
            filters: params.filters,
            or_filters: params.or_filters
          })
        ])

        if (listResult && Array.isArray(listResult)) {
          // Enhance data with display fields
          this.tags = listResult.map(tag => ({
            ...tag,
            formatted_created_at: this.formatDate(tag.creation),
            formatted_modified: this.formatRelativeDate(tag.modified)
          }))

          // Update pagination
          this.pagination.total = countResult || 0
          this.pagination.page = options.page || 1
          this.pagination.limit = options.limit || this.pagination.limit
          this.pagination.showing_from = this.pagination.total > 0 ? ((this.pagination.page - 1) * this.pagination.limit) + 1 : 0
          this.pagination.showing_to = Math.min(this.pagination.page * this.pagination.limit, this.pagination.total)
          this.pagination.has_next = this.pagination.showing_to < this.pagination.total
          this.pagination.has_prev = this.pagination.page > 1

          return { success: true, data: this.tags }
        }

        return { success: false, message: 'No data received' }
      } catch (error) {
        console.error('Error fetching tags:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchTagById(id) {
      this.loading = true
      this.error = null
      
      try {
        const tagResult = await call('frappe.client.get', {
          doctype: 'Mira Tag',
          name: id
        })

        if (tagResult && tagResult.name) {
          // Enhance data with display fields
          const enhancedTag = {
            ...tagResult,
            display_status: this.getStatusDisplay(tagResult.status),
            status_color: this.getStatusColor(tagResult.status),
            formatted_created_at: this.formatDate(tagResult.created_at || tagResult.creation),
            formatted_modified: this.formatRelativeDate(tagResult.modified)
          }

          this.currentTag = enhancedTag
          return { success: true, data: enhancedTag }
        }

        return { success: false, message: 'Tag not found' }
      } catch (error) {
        console.error('Error fetching tag:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createTag(tagData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateTag(tagData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        const preparedData = this.prepareTagForSave(tagData)
        
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Tag',
            ...preparedData
          }
        })

        if (result && result.name) {
          // Refresh tags list
          await this.fetchTags()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to create tag' }
      } catch (error) {
        console.error('Error creating tag:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateTag(name, tagData) {
      this.loading = true
      this.error = null
      
      try {
        const validationResult = this.validateTag(tagData)
        if (!validationResult.isValid) {
          throw new Error(validationResult.message)
        }

        // Prepare complete tag data
        const completeTagData = {
          title: tagData.title?.trim(),
          color: tagData.color || '#3B82F6',
          order: tagData.order || 0
        }
        
        // Update with complete data in one call
        const result = await call('frappe.client.set_value', {
          doctype: 'Mira Tag',
          name: name,
          fieldname: completeTagData
        })

        if (result) {
          // Refresh tags list
          await this.fetchTags()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to update tag' }
      } catch (error) {
        console.error('Error updating tag:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteTag(tagId) {
      this.loading = true
      this.error = null
      
      try {
        const result = await call('frappe.client.delete', {
          doctype: 'Mira Tag',
          name: tagId
        })

        if (result === undefined) {
          // Remove from local state
          this.tags = this.tags.filter(tag => tag.name !== tagId)
          
          // Update pagination
          this.pagination.total = Math.max(0, this.pagination.total - 1)
          
          return { success: true }
        }

        return { success: false, message: 'Failed to delete tag' }
      } catch (error) {
        console.error('Error deleting tag:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async duplicateTag(tagId) {
      this.loading = true
      this.error = null
      
      try {
        // First get the original tag
        const originalTag = await call('frappe.client.get', {
          doctype: 'Mira Tag',
          name: tagId
        })

        if (!originalTag) {
          throw new Error('Original tag not found')
        }

        // Prepare duplicate data
        const duplicateData = {
          title: `${originalTag.title} (Copy)`,
          color: originalTag.color,
          order: this.getNextOrder() // Sử dụng max order + 1 thay vì order hiện tại + 1
        }

        // Create the duplicate
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Tag',
            ...duplicateData
          }
        })

        if (result && result.name) {
          // Refresh tags list
          await this.fetchTags()
          return { success: true, data: result }
        }

        return { success: false, message: 'Failed to duplicate tag' }
      } catch (error) {
        console.error('Error duplicating tag:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async searchTags(searchText) {
      this.filters.search = searchText
      return await this.fetchTags({ page: 1 })
    },

    async fetchStatistics() {
      try {
        const totalResult = await call('frappe.client.get_count', { doctype: 'Mira Tag' })

        this.statistics = {
          total: totalResult || 0
        }

        return this.statistics
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return this.statistics
      }
    },

    async getTag(name) {
      try {
        const result = await call('frappe.client.get', {
          doctype: 'Mira Tag',
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

        return { success: false, error: 'Tag not found' }
      } catch (error) {
        console.error('Error fetching tag:', error)
        return { 
          success: false, 
          error: this.parseError(error) || 'Failed to fetch tag details'
        }
      }
    },

    // Helper methods
    validateTag(tagData) {
      if (!tagData.title || tagData.title.trim().length === 0) {
        return { isValid: false, message: 'Tag title is required' }
      }

      if (tagData.title.length > 100) {
        return { isValid: false, message: 'Tag title must be less than 100 characters' }
      }

      return { isValid: true }
    },

    prepareTagForSave(tagData) {
      return {
        title: tagData.title?.trim(),
        color: tagData.color || '#3B82F6',
        order: tagData.order !== undefined ? tagData.order : this.getNextOrder()
      }
    },

    getNextOrder() {
      if (this.tags.length === 0) return 1
      const maxOrder = Math.max(...this.tags.map(tag => tag.order || 0))
      return maxOrder + 1
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
