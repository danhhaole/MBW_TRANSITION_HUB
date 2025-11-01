import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useFlowTemplateStore = defineStore('flowTemplate', {
  state: () => ({
    templates: [],
    currentTemplate: null,
    loading: false,
    error: null,
    pagination: {
      page: 1,
      limit: 12, // Card layout typically shows 12 items per page
      total: 0,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    },
    filters: {
      search: '',
      type: '', // FLOW, SEQUENCE, CAMPAIGN
      scope_type: '', // PRIVATE, TEAM, ORGANIZATION, PUBLIC
      channel: '', // Email, SMS, Zalo, Messenger
      is_default: null
    },
    statistics: {
      total: 0,
      system_templates: 0,
      my_templates: 0,
      by_type: {
        flow: 0,
        sequence: 0,
        campaign: 0
      }
    }
  }),

  getters: {
    filteredTemplates: (state) => {
      let filtered = [...state.templates]
      
      if (state.filters.search) {
        const search = state.filters.search.toLowerCase()
        filtered = filtered.filter(template => 
          template.name_template?.toLowerCase().includes(search) ||
          template.description?.toLowerCase().includes(search) ||
          template.alias?.toLowerCase().includes(search)
        )
      }
      
      if (state.filters.type) {
        filtered = filtered.filter(template => template.type === state.filters.type)
      }
      
      if (state.filters.scope_type) {
        filtered = filtered.filter(template => template.scope_type === state.filters.scope_type)
      }
      
      if (state.filters.channel) {
        filtered = filtered.filter(template => template.channel === state.filters.channel)
      }
      
      if (state.filters.is_default !== null) {
        filtered = filtered.filter(template => template.is_default === state.filters.is_default)
      }
      
      return filtered
    },

    systemTemplates: (state) => {
      return state.templates.filter(template => template.is_default === 1)
    },

    myTemplates: (state) => {
      return state.templates.filter(template => template.is_default === 0)
    },

    getTemplateByName: (state) => (name) => {
      return state.templates.find(template => template.name === name)
    },

    templatesByType: (state) => (type) => {
      return state.templates.filter(template => template.type === type)
    }
  },

  actions: {
    async fetchTemplates(options = {}) {
      this.loading = true
      this.error = null
      
      try {
        const params = {
          doctype: 'Mira Flow Template',
          page: options.page || this.pagination.page,
          page_size: options.limit || this.pagination.limit,
          fields: [
            'name', 'name_template', 'alias', 'description', 'thumbnail',
            'type', 'order_no', 'is_default', 'is_premium', 'is_suggestion',
            'scope_type', 'flow_type', 'channel', 'target_type',
            'flow_parent_id', 'configuration_json',
            'is_has_url_cta', 'url_cta',
            'flow_total', 'version', 'usage_count', 'last_used_at',
            'owner_id', 'creator_id', 'created_at', 'updated_at',
            'creation', 'modified', 'is_delete'
          ],
          filters: {}
        }

        // Add filters
        if (this.filters.search) {
          params.search = this.filters.search
        }

        if (this.filters.type) {
          params.filters.type = this.filters.type
        }

        if (this.filters.scope_type) {
          params.filters.scope_type = this.filters.scope_type
        }

        if (this.filters.channel) {
          params.filters.channel = this.filters.channel
        }

        if (this.filters.is_default !== null) {
          params.filters.is_default = this.filters.is_default
        }

        // Add is_delete filter to exclude deleted records
        params.filters.is_delete = 0

        const result = await call('mbw_mira.api.doc.get_list_data', params)

        if (result && result.data) {
          this.templates = result.data.map(template => this.enhanceTemplate(template))
          
          // Update pagination
          this.pagination = {
            page: result.page || 1,
            limit: result.page_size || this.pagination.limit,
            total: result.total || 0,
            has_next: result.has_next || false,
            has_prev: result.has_prev || false,
            showing_from: result.showing_from || 0,
            showing_to: result.showing_to || 0
          }

          return { success: true, data: this.templates, count: result.total }
        }

        return { success: false, error: __('No data returned') }
      } catch (error) {
        console.error('Error fetching flow templates:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchTemplateById(name) {
      this.loading = true
      this.error = null
      
      try {
        const result = await call('frappe.client.get', {
          doctype: 'Mira Flow Template',
          name: name
        })

        if (result) {
          this.currentTemplate = this.enhanceTemplate(result)
          return { success: true, data: this.currentTemplate }
        }

        return { success: false, error: __('Template not found') }
      } catch (error) {
        console.error('Error fetching template details:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async createTemplate(templateData) {
      this.loading = true
      this.error = null
      
      try {
        const result = await call('frappe.client.insert', {
          doc: {
            doctype: 'Mira Flow Template',
            ...templateData
          }
        })

        if (result) {
          const enhancedTemplate = this.enhanceTemplate(result)
          this.templates.unshift(enhancedTemplate)
          this.currentTemplate = enhancedTemplate
          return { success: true, data: enhancedTemplate }
        }

        return { success: false, error: __('Failed to create template') }
      } catch (error) {
        console.error('Error creating template:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async updateTemplate(name, templateData) {
      this.loading = true
      this.error = null
      
      try {
        // First, get the current document to preserve fields like modified
        const currentDoc = await call('frappe.client.get', {
          doctype: 'Mira Flow Template',
          name: name
        })

        if (!currentDoc) {
          return { success: false, error: __('Template not found') }
        }

        // Merge with new data
        const updatedDoc = {
          ...currentDoc,
          ...templateData,
          doctype: 'Mira Flow Template',
          name: name
        }

        // Use save_doc to properly handle child tables
        const result = await call('frappe.client.save', {
          doc: updatedDoc
        })

        if (result) {
          // Update in local state
          const index = this.templates.findIndex(t => t.name === name)
          if (index !== -1) {
            this.templates[index] = this.enhanceTemplate(result)
          }
          
          if (this.currentTemplate?.name === name) {
            this.currentTemplate = this.enhanceTemplate(result)
          }

          return { success: true, data: result }
        }

        return { success: false, error: __('Failed to update template') }
      } catch (error) {
        console.error('Error updating template:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async deleteTemplate(name) {
      this.loading = true
      this.error = null
      
      try {
        await call('frappe.client.delete', {
          doctype: 'Mira Flow Template',
          name: name
        })

        // Remove from local state
        this.templates = this.templates.filter(t => t.name !== name)
        
        if (this.currentTemplate?.name === name) {
          this.currentTemplate = null
        }

        return { success: true }
      } catch (error) {
        console.error('Error deleting template:', error)
        this.error = this.parseError(error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async fetchStatistics() {
      try {
        const result = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Flow Template',
          page: 1,
          page_size: 1000, // Get all for statistics
          fields: ['name', 'type', 'is_default'],
          filters: { is_delete: 0 }
        })

        if (result && result.data) {
          const templates = result.data
          
          this.statistics = {
            total: templates.length,
            system_templates: templates.filter(t => t.is_default === 1).length,
            my_templates: templates.filter(t => t.is_default === 0).length,
            by_type: {
              flow: templates.filter(t => t.type === 'FLOW').length,
              sequence: templates.filter(t => t.type === 'SEQUENCE').length,
              campaign: templates.filter(t => t.type === 'CAMPAIGN').length
            }
          }

          return { success: true, data: this.statistics }
        }

        return { success: false, error: __('Failed to fetch statistics') }
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return { success: false, error: this.parseError(error) }
      }
    },

    async useTemplate(templateName) {
      // This will be implemented later to create a flow from template
      // For now, just return the template data
      try {
        const result = await this.fetchTemplateById(templateName)
        if (result.success) {
          return { success: true, data: result.data }
        }
        return result
      } catch (error) {
        console.error('Error using template:', error)
        return { success: false, error: this.parseError(error) }
      }
    },

    // Helper methods
    enhanceTemplate(template) {
      return {
        ...template,
        display_type: this.getTypeDisplay(template.type),
        display_scope: this.getScopeDisplay(template.scope_type),
        type_badge_color: this.getTypeBadgeColor(template.type),
        scope_badge_color: this.getScopeBadgeColor(template.scope_type),
        formatted_created_at: this.formatDate(template.created_at || template.creation),
        formatted_updated_at: this.formatDate(template.updated_at || template.modified),
        thumbnail_url: template.thumbnail || this.getDefaultThumbnail(template.type)
      }
    },

    getTypeDisplay(type) {
      const typeMap = {
        'FLOW': __('Flow'),
        'SEQUENCE': __('Sequence'),
        'CAMPAIGN': __('Campaign')
      }
      return typeMap[type] || type
    },

    getScopeDisplay(scopeType) {
      const scopeMap = {
        'PRIVATE': __('Private'),
        'TEAM': __('Team'),
        'ORGANIZATION': __('Organization'),
        'PUBLIC': __('Public')
      }
      return scopeMap[scopeType] || scopeType
    },

    getTypeBadgeColor(type) {
      const colorMap = {
        'FLOW': 'blue',
        'SEQUENCE': 'green',
        'CAMPAIGN': 'purple'
      }
      return colorMap[type] || 'gray'
    },

    getScopeBadgeColor(scopeType) {
      const colorMap = {
        'PRIVATE': 'gray',
        'TEAM': 'blue',
        'ORGANIZATION': 'green',
        'PUBLIC': 'purple'
      }
      return colorMap[scopeType] || 'gray'
    },

    getDefaultThumbnail(type) {
      // Return default thumbnail based on type
      const thumbnailMap = {
        'FLOW': '/assets/mbw_mira/images/flow-default.svg',
        'SEQUENCE': '/assets/mbw_mira/images/sequence-default.svg',
        'CAMPAIGN': '/assets/mbw_mira/images/campaign-default.svg'
      }
      return thumbnailMap[type] || '/assets/mbw_mira/images/template-default.svg'
    },

    formatDate(dateString) {
      if (!dateString) return ''
      
      const date = new Date(dateString)
      return date.toLocaleDateString('vi-VN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    },

    parseError(error) {
      if (typeof error === 'string') return error
      if (error.message) return error.message
      if (error.exc) {
        try {
          const exc = JSON.parse(error.exc)
          return exc.message || exc.exc || __('An error occurred')
        } catch {
          return error.exc
        }
      }
      return __('An unexpected error occurred')
    },

    // Filter methods
    setSearch(search) {
      this.filters.search = search
    },

    setTypeFilter(type) {
      this.filters.type = type
    },

    setScopeFilter(scopeType) {
      this.filters.scope_type = scopeType
    },

    setChannelFilter(channel) {
      this.filters.channel = channel
    },

    setDefaultFilter(isDefault) {
      this.filters.is_default = isDefault
    },

    clearFilters() {
      this.filters = {
        search: '',
        type: '',
        scope_type: '',
        channel: '',
        is_default: null
      }
    }
  }
})
