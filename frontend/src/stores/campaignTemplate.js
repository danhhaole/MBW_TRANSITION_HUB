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
      system_templates: 0,
      my_templates: 0,
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
          page = this.pagination.page,
          limit = this.pagination.limit,
          searchText = this.searchText,
          typeFilter = this.typeFilter,
          activeFilter = this.activeFilter,
          scopeFilter = null
        } = options

        // Build filters
        let filters = {}
        
        if (typeFilter && typeFilter !== 'all') {
          filters['campaign_type'] = typeFilter
        }

        if (activeFilter && activeFilter !== 'all') {
          filters['is_active'] = activeFilter === 'active' ? 1 : 0
        }

        // Add scope_type filter if provided
        if (scopeFilter) {
          filters['scope_type'] = scopeFilter
        }

        // Build or_filters for search
        let or_filters = undefined
        if (searchText && searchText.trim()) {
          or_filters = [
            ['template_name', 'like', `%${searchText.trim()}%`],
            ['description', 'like', `%${searchText.trim()}%`]
          ]
        }

        // Use get_list_data API which returns both data and count
        const result = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Campaign Template',
          fields: ['*'],
          filters: filters,
          or_filters: or_filters,
          limit_page_length: limit,
          limit_start: (page - 1) * limit,
          order_by: 'modified desc'
        })
        
        if (result && result.success && Array.isArray(result.data)) {
          // Process templates to add display fields
          const processedTemplates = result.data.map(template => ({
            ...template,
            display_status: template.is_active ? 'Active' : 'Inactive',
            type_display: this.getCampaignTypeDisplay(template.campaign_type)
          }))

          this.templates = processedTemplates
          
          // Update pagination info with correct total count
          const total = result.count || 0
          this.pagination = {
            page,
            limit,
            total,
            pages: Math.ceil(total / limit),
            has_next: page * limit < total,
            has_prev: page > 1,
            showing_from: total > 0 ? (page - 1) * limit + 1 : 0,
            showing_to: Math.min(page * limit, total)
          }

          this.setSuccess('Templates loaded successfully')
          return {
            success: true,
            data: processedTemplates,
            pagination: this.pagination,
            count: result.count
          }
        } else {
          throw new Error('API returned invalid response')
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
          // Save social contents if any
          if (data.selected_channels && data.selected_channels.length > 0) {
            await this.saveSocialContents(response.name, data)
          }
          
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

    // Use template to create campaign
    async useTemplate(templateName, campaignName) {
      this.setLoading(true)
      
      try {
        const response = await call('mbw_mira.api.campaign_template.use_template', {
          template_name: templateName,
          campaign_name: campaignName
        })

        if (response) {
          this.setSuccess('Campaign created successfully from template')
          return {
            success: true,
            data: response,
            campaign_name: response.name,
            message: 'Campaign created successfully from template!'
          }
        } else {
          throw new Error('Failed to create campaign from template')
        }
      } catch (error) {
        console.error('Error using template:', error)
        this.setError(this.parseError(error) || 'Failed to create campaign from template')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to create campaign from template'
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
        // Use get_list_data to get all templates with count
        const result = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Campaign Template',
          fields: ['campaign_type', 'is_active', 'scope_type'],
          limit_page_length: 9999
        })

        console.log('📊 fetchStatistics result:', result)

        if (result && result.success && Array.isArray(result.data)) {
          const templates = result.data
          let activeCount = 0
          let systemTemplates = 0
          let myTemplates = 0
          const typeStats = {}

          templates.forEach(template => {
            if (template.is_active) activeCount++
            
            // Count by scope_type for tabs
            if (template.scope_type === 'PUBLIC' || template.scope_type === 'ORGANIZATION') {
              systemTemplates++
            } else if (template.scope_type === 'PRIVATE') {
              myTemplates++
            }
            
            const type = template.campaign_type
            if (type) {
              if (!typeStats[type]) {
                typeStats[type] = { total: 0, active: 0 }
              }
              typeStats[type].total++
              if (template.is_active) {
                typeStats[type].active++
              }
            }
          })

          this.statistics = {
            total: result.count || templates.length,
            active: activeCount,
            inactive: (result.count || templates.length) - activeCount,
            system_templates: systemTemplates,
            my_templates: myTemplates,
            by_type: typeStats
          }
          
          console.log('📊 Updated statistics:', this.statistics)
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

    // Search templates
    async searchTemplates(searchTerm, options = {}) {
      this.setSearchText(searchTerm)
      return await this.fetchTemplates(options)
    },

    // Get filter options for specific field
    async fetchFilterOptions(fieldname) {
      try {
        const result = await call('mbw_mira.api.doc.get_list_data', {
          doctype: 'Mira Campaign Template',
          fields: [fieldname],
          limit_page_length: 9999
        })

        const uniqueValues = new Set()
        if (result && result.success && Array.isArray(result.data)) {
          result.data.forEach(item => {
            if (item[fieldname]) {
              uniqueValues.add(item[fieldname])
            }
          })
        }

        const options = Array.from(uniqueValues).sort().map(value => ({
          label: value,
          value: value
        }))

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

    // Use template to create a new campaign
    async useTemplate(templateId, campaignName = null, startDate = null, targetPool = null) {
      this.setLoading(true)
      
      try {
        const result = await call('mbw_mira.api.campaign_from_template.create_campaign_from_template', {
          template_id: templateId,
          campaign_name: campaignName,
          start_date: startDate,
          target_pool: targetPool
        })
        
        if (result && result.success) {
          this.setSuccess('Campaign created from template')
          return {
            success: true,
            message: result.message,
            campaign_id: result.data?.campaign_id,
            campaign_name: result.data?.campaign_id, // Use ID for routing
            data: result.data
          }
        } else {
          throw new Error(result?.error || 'Failed to create campaign from template')
        }
      } catch (error) {
        console.error('Error using template:', error)
        this.setError(error.message || 'Failed to create campaign from template')
        return {
          success: false,
          error: error.message || 'Failed to create campaign from template'
        }
      }
    },

    // Get template preview before using
    async getTemplatePreview(templateId) {
      try {
        const result = await call('mbw_mira.api.campaign_from_template.get_template_preview', {
          template_id: templateId
        })
        
        if (result && result.success) {
          return {
            success: true,
            data: result.data
          }
        } else {
          throw new Error(result?.error || 'Failed to get template preview')
        }
      } catch (error) {
        console.error('Error getting template preview:', error)
        return {
          success: false,
          error: error.message || 'Failed to get template preview'
        }
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
      const validTypes = ['ATTRACTION', 'NURTURING', 'RECRUITMENT']
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

      // Build configuration_json from campaign info fields
      const configFields = ['objective', 'target_pool', 'config_data', 'conditions', 'candidate_count']
      const config = prepared.configuration || {}
      
      // Get values from campaign_info nested structure or flat structure
      const campaignInfo = prepared.campaign_info || {}
      
      configFields.forEach(field => {
        const value = campaignInfo[field] || prepared[field]
        if (value !== undefined && value !== null && value !== '') {
          config[field] = value
        }
      })
      
      // Store configuration as JSON string
      if (Object.keys(config).length > 0) {
        prepared.configuration_json = JSON.stringify(config)
      }
      
      // Remove fields that don't exist in doctype
      delete prepared.objective
      delete prepared.target_pool
      delete prepared.config_data
      delete prepared.conditions
      delete prepared.candidate_count
      delete prepared.campaign_info
      delete prepared.content_channels
      delete prepared.campaign_settings
      delete prepared.configuration
      delete prepared.selected_channels
      delete prepared.facebook_content
      delete prepared.zalo_content
      delete prepared.email_content
      delete prepared.sms_content
      delete prepared.social_contents_raw
      delete prepared.campaign_tags
      delete prepared.template_description

      return prepared
    },

    getCampaignTypeDisplay(type) {
      const typeMap = {
        'ATTRACTION': 'Attraction Campaign',
        'NURTURING': 'Nurturing Campaign', 
        'RECRUITMENT': 'Recruitment Campaign'
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
    },

    // Save social contents for template
    async saveSocialContents(templateId, templateData) {
      try {
        const socialContents = []
        const selectedChannels = templateData.selected_channels || []
        
        // Process each selected channel
        for (const channel of selectedChannels) {
          let contentData = {
            platform: this.getPlatformName(channel),
            channel_type: channel,
            is_active: 1
          }
          
          // Get content based on channel
          if (channel === 'facebook' && templateData.facebook_content) {
            contentData.template_content = templateData.facebook_content.content || ''
            contentData.social_media_images = templateData.facebook_content.image || null
            contentData.page_id = templateData.facebook_content.page_id || null
            contentData.connection_id = templateData.facebook_content.connection_id || null
          } else if (channel === 'zalo' && templateData.zalo_content) {
            contentData.template_content = templateData.zalo_content.content || ''
            contentData.social_media_images = templateData.zalo_content.image || null
            contentData.page_id = templateData.zalo_content.page_id || null
            contentData.connection_id = templateData.zalo_content.connection_id || null
          } else if (channel === 'email' && templateData.email_content) {
            contentData.template_content = templateData.email_content.body || templateData.email_content.content || ''
            contentData.subject = templateData.email_content.subject || ''
            contentData.mjml_content = templateData.email_content.mjml_content || null
            contentData.block_content = templateData.email_content.block_content || null
          }
          
          if (contentData.template_content) {
            socialContents.push(contentData)
          }
        }
        
        // Also check for content without selected channels (e.g., direct content input)
        if (selectedChannels.length === 0) {
          // Check Facebook content
          if (templateData.facebook_content?.content) {
            socialContents.push({
              platform: 'Facebook',
              channel_type: 'facebook',
              is_active: 1,
              template_content: templateData.facebook_content.content,
              social_media_images: templateData.facebook_content.image || null,
              page_id: templateData.facebook_content.page_id || null,
              connection_id: templateData.facebook_content.connection_id || null
            })
          }
          
          // Check Zalo content
          if (templateData.zalo_content?.content) {
            socialContents.push({
              platform: 'Zalo',
              channel_type: 'zalo',
              is_active: 1,
              template_content: templateData.zalo_content.content,
              social_media_images: templateData.zalo_content.image || null,
              page_id: templateData.zalo_content.page_id || null,
              connection_id: templateData.zalo_content.connection_id || null
            })
          }
          
          // Check Email content
          if (templateData.email_content?.body || templateData.email_content?.content) {
            socialContents.push({
              platform: 'Email',
              channel_type: 'email',
              is_active: 1,
              template_content: templateData.email_content.body || templateData.email_content.content || '',
              subject: templateData.email_content.subject || '',
              mjml_content: templateData.email_content.mjml_content || null,
              block_content: templateData.email_content.block_content || null
            })
          }
        }
        
        // Bulk save social contents
        if (socialContents.length > 0) {
          console.log('💾 Saving social contents:', socialContents)
          await call('mbw_mira.mbw_mira.doctype.mira_campaign_template_social.api.bulk_save_template_social_contents', {
            template_id: templateId,
            contents_data: socialContents
          })
        }
      } catch (error) {
        console.error('Error saving social contents:', error)
        // Don't throw error to avoid breaking template creation
      }
    },

    // Helper method to get platform name
    getPlatformName(channel) {
      const platformMap = {
        'facebook': 'Facebook',
        'zalo': 'Zalo', 
        'email': 'Email',
        'sms': 'SMS'
      }
      return platformMap[channel] || channel
    },

    // Load template with social contents for editing
    async loadTemplateWithSocialContents(templateId) {
      try {
        console.log('🔍 Loading template with social contents:', templateId)
        const response = await call(
          'mbw_mira.mbw_mira.doctype.mira_campaign_template_social.api.get_template_with_social_contents',
          { template_id: templateId }
        )
        
        console.log('📦 API Response:', response)
        
        // Handle Frappe response wrapper (response.message or direct response)
        const result = response?.message || response
        
        if (result?.success) {
          console.log('✅ Template data loaded:', result.data)
          return result.data
        } else {
          console.error('❌ Error loading template:', result?.error)
          return null
        }
      } catch (error) {
        console.error('❌ Error loading template with social contents:', error)
        return null
      }
    },

    // Get social contents for a template
    async getSocialContents(templateId) {
      try {
        const response = await call(
          'mbw_mira.mbw_mira.doctype.mira_campaign_template_social.api.get_template_social_contents',
          { template_id: templateId }
        )
        
        // Handle Frappe response wrapper
        const result = response?.message || response
        
        if (result?.success) {
          return {
            raw: result.data,
            formatted: result.formatted,
            selectedChannels: result.selected_channels
          }
        }
        return null
      } catch (error) {
        console.error('Error getting social contents:', error)
        return null
      }
    },

    // Save template flows (triggers)
    async saveTemplateFlows(templateId, triggers) {
      try {
        console.log('💾 Saving template flows:', templateId, triggers)
        const response = await call(
          'mbw_mira.api.campaign_template_flow.sync_template_flows',
          { 
            campaign_template_id: templateId,
            triggers: triggers
          }
        )
        
        const result = response?.message || response
        console.log('📦 Save flows response:', result)
        
        return result
      } catch (error) {
        console.error('Error saving template flows:', error)
        return { success: false, error: error.message }
      }
    },

    // Get template flows (triggers)
    async getTemplateFlows(templateId) {
      try {
        console.log('🔍 Getting template flows:', templateId)
        const response = await call(
          'mbw_mira.api.campaign_template_flow.get_template_flows',
          { campaign_template_id: templateId }
        )
        
        const result = response?.message || response
        console.log('📦 Get flows response:', result)
        
        if (result?.success) {
          return result.data || []
        }
        return []
      } catch (error) {
        console.error('Error getting template flows:', error)
        return []
      }
    }
  }
})
