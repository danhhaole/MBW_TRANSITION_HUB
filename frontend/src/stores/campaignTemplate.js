import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCampaignTemplateStore = defineStore('campaignTemplate', {
  state: () => ({
    templates: [],
    currentTemplate: null,
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
    typeFilter: 'all',
    activeFilter: 'all',
    // Form state
    formData: null,
    fieldLayout: [],
    meta: null,
    // Statistics
    statistics: {
      total: 0,
      active: 0,
      inactive: 0,
      by_type: {}
    }
  }),

  getters: {
    // Client-side filtered templates
    filteredTemplates: (state) => {
      let filtered = state.templates

      if (state.searchText) {
        filtered = filtered.filter(template => 
          template.template_name?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          template.description?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.typeFilter && state.typeFilter !== 'all') {
        filtered = filtered.filter(template => template.campaign_type === state.typeFilter)
      }

      if (state.activeFilter && state.activeFilter !== 'all') {
        const isActive = state.activeFilter === 'active'
        filtered = filtered.filter(template => Boolean(template.is_active) === isActive)
      }

      return filtered
    },

    // Get template by name
    getTemplateByName: (state) => (name) => {
      return state.templates.find(template => template.name === name)
    },

    // Active templates only
    activeTemplates: (state) => {
      return state.templates.filter(template => template.is_active)
    },

    // Templates by type
    templatesByType: (state) => (type) => {
      return state.templates.filter(template => template.campaign_type === type)
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
    setTypeFilter(type) {
      this.typeFilter = type
    },

    setActiveFilter(active) {
      this.activeFilter = active
    },

    // Reset filters
    resetFilters() {
      this.searchText = ''
      this.typeFilter = 'all'
      this.activeFilter = 'all'
    },

    // Get templates list with pagination and filters
    async fetchTemplates(options = {}) {
      this.setLoading(true)
      
      try {
        const {
          filters = {},
          fields = ['*'],
          order_by = 'modified desc',
          page_length = this.pagination.limit,
          start = (this.pagination.page - 1) * this.pagination.limit
        } = options

        // Build filters
        let enhancedFilters = { ...filters }
        
        if (this.searchText && this.searchText.trim()) {
          enhancedFilters['template_name'] = ['like', `%${this.searchText.trim()}%`]
        }

        if (this.typeFilter && this.typeFilter !== 'all') {
          enhancedFilters['campaign_type'] = this.typeFilter
        }

        if (this.activeFilter && this.activeFilter !== 'all') {
          enhancedFilters['is_active'] = this.activeFilter === 'active' ? 1 : 0
        }

        // Fetch templates
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Campaign Template',
          fields: fields,
          filters: enhancedFilters,
          order_by: order_by,
          limit_page_length: page_length,
          limit_start: start
        })

        // Get total count for pagination
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'Mira Campaign Template',
          filters: enhancedFilters
        })

        // Process templates to add display fields
        const processedTemplates = (response || []).map(template => ({
          ...template,
          display_status: template.is_active ? 'Active' : 'Inactive',
          type_display: this.getCampaignTypeDisplay(template.campaign_type)
        }))

        this.templates = processedTemplates
        
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

        this.setSuccess('Templates loaded successfully')
        return {
          success: true,
          data: processedTemplates,
          pagination: this.pagination
        }
      } catch (error) {
        console.error('Error fetching templates:', error)
        this.setError(error.message || 'Failed to fetch campaign templates')
        return {
          success: false,
          error: error.message || 'Failed to fetch campaign templates'
        }
      }
    },

    // Get template by ID
    async fetchTemplateById(name) {
      this.setLoading(true)
      
      try {
        const response = await call('frappe.client.get', {
          doctype: 'Mira Campaign Template',
          name: name
        })

        if (response) {
          const processedTemplate = {
            ...response,
            display_status: response.is_active ? 'Active' : 'Inactive',
            type_display: this.getCampaignTypeDisplay(response.campaign_type)
          }

          this.currentTemplate = processedTemplate
          this.setSuccess('Template loaded successfully')
          
          return {
            success: true,
            data: processedTemplate
          }
        } else {
          throw new Error('Template not found')
        }
      } catch (error) {
        console.error('Error fetching template:', error)
        this.setError(error.message || 'Failed to fetch campaign template')
        return {
          success: false,
          error: error.message || 'Failed to fetch campaign template'
        }
      }
    },

    // Create new template
    async createTemplate(data) {
      this.setLoading(true)
      
      try {
        // Validate required fields
        const validationErrors = this.validateTemplate(data, 'create')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for creation
        const preparedData = this.prepareTemplateForSave(data, 'create')
        
        const docData = {
          doctype: 'Mira Campaign Template',
          ...preparedData
        }

        const response = await call('frappe.client.insert', {
          doc: docData
        })

        if (response) {
          // Add to local state
          const newTemplate = {
            ...response,
            display_status: response.is_active ? 'Active' : 'Inactive',
            type_display: this.getCampaignTypeDisplay(response.campaign_type)
          }
          
          this.templates.unshift(newTemplate)
          this.currentTemplate = newTemplate
          
          this.setSuccess('Campaign template created successfully')
          return {
            success: true,
            data: newTemplate
          }
        } else {
          throw new Error('Failed to create template')
        }
      } catch (error) {
        console.error('Error creating template:', error)
        this.setError(this.parseError(error) || 'Failed to create campaign template')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to create campaign template'
        }
      }
    },

    // Update template
    async updateTemplate(name, data) {
      this.setLoading(true)
      
      try {
        // Validate required fields
        const validationErrors = this.validateTemplate(data, 'update')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for update
        const preparedData = this.prepareTemplateForSave(data, 'update')

        const response = await call('frappe.client.set_value', {
          doctype: 'Mira Campaign Template',
          name: name,
          fieldname: preparedData
        })

        if (response) {
          // Update local state
          const index = this.templates.findIndex(t => t.name === name)
          if (index !== -1) {
            this.templates[index] = {
              ...this.templates[index],
              ...preparedData,
              display_status: preparedData.is_active ? 'Active' : 'Inactive',
              type_display: this.getCampaignTypeDisplay(preparedData.campaign_type)
            }
          }

          if (this.currentTemplate && this.currentTemplate.name === name) {
            this.currentTemplate = {
              ...this.currentTemplate,
              ...preparedData,
              display_status: preparedData.is_active ? 'Active' : 'Inactive',
              type_display: this.getCampaignTypeDisplay(preparedData.campaign_type)
            }
          }

          this.setSuccess('Campaign template updated successfully')
          return {
            success: true,
            data: response
          }
        } else {
          throw new Error('Failed to update template')
        }
      } catch (error) {
        console.error('Error updating template:', error)
        this.setError(this.parseError(error) || 'Failed to update campaign template')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to update campaign template'
        }
      }
    },

    // Delete template
    async deleteTemplate(name) {
      this.setLoading(true)
      
      try {
        await call('frappe.client.delete', {
          doctype: 'Mira Campaign Template',
          name: name
        })

        // Remove from local state
        this.templates = this.templates.filter(t => t.name !== name)
        
        if (this.currentTemplate && this.currentTemplate.name === name) {
          this.currentTemplate = null
        }

        this.setSuccess('Campaign template deleted successfully')
        return {
          success: true
        }
      } catch (error) {
        console.error('Error deleting template:', error)
        this.setError(this.parseError(error) || 'Failed to delete campaign template')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to delete campaign template'
        }
      }
    },

    // Get form data with field layout
    async fetchFormData(name = null) {
      this.setLoading(true)
      
      try {
        // Get metadata
        const metaResponse = await call('frappe.desk.form.load.getdoctype', {
          doctype: 'Mira Campaign Template'
        })

        let docData = null
        
        // If name provided, get document data
        if (name) {
          const docResponse = await this.fetchTemplateById(name)
          if (docResponse.success) {
            docData = docResponse.data
          }
        }

        // Create field layout from metadata
        let fieldLayout = []
        if (metaResponse?.docs?.[0]) {
          fieldLayout = this.createFieldLayout(metaResponse.docs[0].fields)
        }

        this.formData = docData
        this.fieldLayout = fieldLayout
        this.meta = metaResponse?.docs?.[0] || null

        this.setSuccess('Form data loaded successfully')
        return {
          success: true,
          data: {
            doc: docData,
            fieldLayout: fieldLayout,
            meta: this.meta
          }
        }
      } catch (error) {
        console.error('Error fetching form data:', error)
        this.setError(error.message || 'Failed to fetch form data')
        return {
          success: false,
          error: error.message || 'Failed to fetch form data'
        }
      }
    },

    // Get statistics
    async fetchStatistics() {
      try {
        const [totalCount, activeCount] = await Promise.all([
          call('frappe.client.get_count', {
            doctype: 'Mira Campaign Template'
          }),
          call('frappe.client.get_count', {
            doctype: 'Mira Campaign Template',
            filters: { is_active: 1 }
          })
        ])

        // Get type statistics
        const typeStats = await this.fetchTypeStatistics()

        this.statistics = {
          total: totalCount || 0,
          active: activeCount || 0,
          inactive: (totalCount || 0) - (activeCount || 0),
          by_type: typeStats
        }

        return {
          success: true,
          data: this.statistics
        }
      } catch (error) {
        console.error('Error fetching statistics:', error)
        return {
          success: false,
          error: error.message || 'Failed to fetch statistics'
        }
      }
    },

    // Get type statistics
    async fetchTypeStatistics() {
      try {
        const templates = await call('frappe.client.get_list', {
          doctype: 'Mira Campaign Template',
          fields: ['campaign_type', 'is_active'],
          limit_page_length: 999
        })

        const stats = {}
        if (templates && Array.isArray(templates)) {
          templates.forEach(template => {
            const type = template.campaign_type
            if (!stats[type]) {
              stats[type] = { total: 0, active: 0 }
            }
            stats[type].total++
            if (template.is_active) {
              stats[type].active++
            }
          })
        }

        return stats
      } catch (error) {
        console.error('Error getting type statistics:', error)
        return {}
      }
    },

    // Search templates
    async searchTemplates(searchTerm, options = {}) {
      this.setSearchText(searchTerm)
      return await this.fetchTemplates(options)
    },

    // Get filter options for specific field
    async fetchFilterOptions(fieldname) {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Campaign Template',
          fields: [fieldname],
          distinct: true,
          order_by: fieldname
        })

        const options = response
          ?.filter(item => item[fieldname])
          ?.map(item => ({
            label: item[fieldname],
            value: item[fieldname]
          })) || []

        return {
          success: true,
          data: options
        }
      } catch (error) {
        console.error('Error fetching filter options:', error)
        return {
          success: false,
          error: error.message || 'Failed to get filter options',
          data: []
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
    validateTemplate(data, action = 'create') {
      const errors = []

      // Required fields
      if (!data.template_name || !data.template_name.trim()) {
        errors.push('Template name is required')
      }

      if (!data.campaign_type || !data.campaign_type.trim()) {
        errors.push('Campaign type is required')
      }

      // Business rules
      if (data.template_name && data.template_name.length > 150) {
        errors.push('Template name must be less than 150 characters')
      }

      // Validate campaign type
      const validTypes = ['Email', 'SMS', 'Ads', 'Social Media', 'Direct Mail']
      if (data.campaign_type && !validTypes.includes(data.campaign_type)) {
        errors.push('Invalid campaign type')
      }

      return errors
    },

    prepareTemplateForSave(data, action = 'create') {
      const prepared = { ...data }

      // Trim strings
      if (prepared.template_name) {
        prepared.template_name = prepared.template_name.trim()
      }
      if (prepared.description) {
        prepared.description = prepared.description.trim()
      }

      // Set defaults
      if (action === 'create') {
        prepared.is_active = prepared.is_active !== undefined ? prepared.is_active : 1
      }

      return prepared
    },

    getCampaignTypeDisplay(type) {
      const typeMap = {
        'Email': 'Email Campaign',
        'SMS': 'SMS Campaign', 
        'Ads': 'Advertisement Campaign',
        'Social Media': 'Social Media Campaign',
        'Direct Mail': 'Direct Mail Campaign'
      }
      return typeMap[type] || type
    },

    createFieldLayout(fields) {
      if (!fields || !Array.isArray(fields)) return []

      // Filter visible fields
      const visibleFields = fields.filter(field => 
        !field.hidden && 
        field.fieldtype !== 'Section Break' && 
        field.fieldtype !== 'Column Break' &&
        field.fieldtype !== 'Tab Break'
      )

      // Create layout structure
      return [
        {
          label: '',
          name: 'main_tab',
          sections: [
            {
              label: 'Thông tin cơ bản',
              name: 'basic_info',
              columns: [
                {
                  label: '',
                  name: 'col1',
                  fields: visibleFields.map(field => ({
                    fieldname: field.fieldname,
                    fieldtype: field.fieldtype,
                    label: field.label,
                    options: field.options,
                    reqd: field.reqd,
                    description: field.description,
                    depends_on: field.depends_on,
                    visible: true,
                    read_only: field.read_only
                  }))
                }
              ]
            }
          ]
        }
      ]
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
