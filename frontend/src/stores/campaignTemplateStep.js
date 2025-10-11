import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCampaignTemplateStepStore = defineStore('campaignTemplateStep', {
  state: () => ({
    steps: [],
    currentStep: null,
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
    templateFilter: '',
    actionTypeFilter: '',
    // Form state
    formData: null,
    fieldLayout: [],
    meta: null,
    // Template-specific steps cache
    stepsByTemplate: {}
  }),

  getters: {
    // Client-side filtered steps
    filteredSteps: (state) => {
      let filtered = state.steps

      if (state.searchText) {
        filtered = filtered.filter(step => 
          step.campaign_step_name?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          step.template_content?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.templateFilter) {
        filtered = filtered.filter(step => step.template === state.templateFilter)
      }

      if (state.actionTypeFilter) {
        filtered = filtered.filter(step => step.action_type === state.actionTypeFilter)
      }

      return filtered
    },

    // Get step by name
    getStepByName: (state) => (name) => {
      return state.steps.find(step => step.name === name)
    },

    // Get steps by template name
    getStepsByTemplate: (state) => (templateName) => {
      return state.stepsByTemplate[templateName] || []
    },

    // Steps by action type
    stepsByActionType: (state) => (actionType) => {
      return state.steps.filter(step => step.action_type === actionType)
    },

    // Get next step order for template
    getNextStepOrder: (state) => (templateName) => {
      const templateSteps = state.stepsByTemplate[templateName] || []
      if (templateSteps.length === 0) return 1
      
      const maxOrder = Math.max(...templateSteps.map(step => step.step_order || 0))
      return maxOrder + 1
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
    setTemplateFilter(template) {
      this.templateFilter = template
    },

    setActionTypeFilter(actionType) {
      this.actionTypeFilter = actionType
    },

    // Reset filters
    resetFilters() {
      this.searchText = ''
      this.templateFilter = ''
      this.actionTypeFilter = ''
    },

    // Get steps list with pagination and filters
    async fetchSteps(options = {}) {
      this.setLoading(true)
      
      try {
        const {
          filters = {},
          fields = ['*'],
          order_by = 'step_order asc',
          page_length = this.pagination.limit,
          start = (this.pagination.page - 1) * this.pagination.limit
        } = options

        // Build filters
        let enhancedFilters = { ...filters }
        
        if (this.searchText && this.searchText.trim()) {
          enhancedFilters['campaign_step_name'] = ['like', `%${this.searchText.trim()}%`]
        }

        if (this.templateFilter) {
          enhancedFilters['template'] = this.templateFilter
        }

        if (this.actionTypeFilter) {
          enhancedFilters['action_type'] = this.actionTypeFilter
        }

        // Fetch steps
        const response = await call('frappe.client.get_list', {
          doctype: 'CampaignTemplateStep',
          fields: fields,
          filters: enhancedFilters,
          order_by: order_by,
          limit_page_length: page_length,
          limit_start: start
        })

        // Get total count for pagination
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'CampaignTemplateStep',
          filters: enhancedFilters
        })

        // Process steps to add display fields
        const processedSteps = (response || []).map(step => ({
          ...step,
          display_action_type: this.getActionTypeDisplay(step.action_type),
          delay_display: step.delay_in_days > 0 ? `${step.delay_in_days} days` : 'Immediate'
        }))

        this.steps = processedSteps
        
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

        this.setSuccess('Steps loaded successfully')
        return {
          success: true,
          data: processedSteps,
          pagination: this.pagination
        }
      } catch (error) {
        console.error('Error fetching steps:', error)
        this.setError(error.message || 'Failed to fetch template steps')
        return {
          success: false,
          error: error.message || 'Failed to fetch template steps'
        }
      }
    },

    // Get steps by template
    async fetchStepsByTemplate(templateName, options = {}) {
      this.setLoading(true)
      
      try {
        const filters = {
          template: templateName,
          ...options.filters
        }
        
        const response = await call('frappe.client.get_list', {
          doctype: 'CampaignTemplateStep',
          fields: ['*'],
          filters: filters,
          order_by: 'step_order asc'
        })

        // Process steps
        const processedSteps = (response || []).map(step => ({
          ...step,
          display_action_type: this.getActionTypeDisplay(step.action_type),
          delay_display: step.delay_in_days > 0 ? `${step.delay_in_days} days` : 'Immediate'
        }))

        // Cache steps by template
        this.stepsByTemplate[templateName] = processedSteps

        this.setSuccess('Template steps loaded successfully')
        return {
          success: true,
          data: processedSteps
        }
      } catch (error) {
        console.error('Error fetching template steps:', error)
        this.setError(error.message || 'Failed to fetch template steps')
        return {
          success: false,
          error: error.message || 'Failed to fetch template steps'
        }
      }
    },

    // Get step by ID
    async fetchStepById(name) {
      this.setLoading(true)
      
      try {
        const response = await call('frappe.client.get', {
          doctype: 'CampaignTemplateStep',
          name: name
        })

        if (response) {
          const processedStep = {
            ...response,
            display_action_type: this.getActionTypeDisplay(response.action_type),
            delay_display: response.delay_in_days > 0 ? `${response.delay_in_days} days` : 'Immediate'
          }

          this.currentStep = processedStep
          this.setSuccess('Step loaded successfully')
          
          return {
            success: true,
            data: processedStep
          }
        } else {
          throw new Error('Step not found')
        }
      } catch (error) {
        console.error('Error fetching step:', error)
        this.setError(error.message || 'Failed to fetch template step')
        return {
          success: false,
          error: error.message || 'Failed to fetch template step'
        }
      }
    },

    // Create new step
    async createStep(data) {
      this.setLoading(true)
      
      try {
        // Validate required fields
        const validationErrors = this.validateStep(data, 'create')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for creation
        const preparedData = this.prepareStepForSave(data, 'create')
        
        const docData = {
          doctype: 'CampaignTemplateStep',
          ...preparedData
        }

        const response = await call('frappe.client.insert', {
          doc: docData
        })

        if (response) {
          // Add to local state
          const newStep = {
            ...response,
            display_action_type: this.getActionTypeDisplay(response.action_type),
            delay_display: response.delay_in_days > 0 ? `${response.delay_in_days} days` : 'Immediate'
          }
          
          this.steps.push(newStep)
          this.currentStep = newStep

          // Update template cache
          if (response.template) {
            if (!this.stepsByTemplate[response.template]) {
              this.stepsByTemplate[response.template] = []
            }
            this.stepsByTemplate[response.template].push(newStep)
            // Sort by step_order
            this.stepsByTemplate[response.template].sort((a, b) => (a.step_order || 0) - (b.step_order || 0))
          }
          
          this.setSuccess('Template step created successfully')
          return {
            success: true,
            data: newStep,
            message: 'Template step created successfully'
          }
        } else {
          throw new Error('Failed to create step')
        }
      } catch (error) {
        console.error('Error creating step:', error)
        this.setError(this.parseError(error) || 'Failed to create template step')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to create template step'
        }
      }
    },

    // Update step
    async updateStep(name, data) {
      this.setLoading(true)
      
      try {
        // Validate required fields
        const validationErrors = this.validateStep(data, 'update')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for update
        const preparedData = this.prepareStepForSave(data, 'update')

        const response = await call('frappe.client.set_value', {
          doctype: 'CampaignTemplateStep',
          name: name,
          fieldname: preparedData
        })

        if (response) {
          // Update local state
          const index = this.steps.findIndex(s => s.name === name)
          if (index !== -1) {
            this.steps[index] = {
              ...this.steps[index],
              ...preparedData,
              display_action_type: this.getActionTypeDisplay(preparedData.action_type),
              delay_display: preparedData.delay_in_days > 0 ? `${preparedData.delay_in_days} days` : 'Immediate'
            }
          }

          if (this.currentStep && this.currentStep.name === name) {
            this.currentStep = {
              ...this.currentStep,
              ...preparedData,
              display_action_type: this.getActionTypeDisplay(preparedData.action_type),
              delay_display: preparedData.delay_in_days > 0 ? `${preparedData.delay_in_days} days` : 'Immediate'
            }
          }

          // Update template cache
          const templateName = preparedData.template || this.currentStep?.template
          if (templateName && this.stepsByTemplate[templateName]) {
            const stepIndex = this.stepsByTemplate[templateName].findIndex(s => s.name === name)
            if (stepIndex !== -1) {
              this.stepsByTemplate[templateName][stepIndex] = {
                ...this.stepsByTemplate[templateName][stepIndex],
                ...preparedData,
                display_action_type: this.getActionTypeDisplay(preparedData.action_type),
                delay_display: preparedData.delay_in_days > 0 ? `${preparedData.delay_in_days} days` : 'Immediate'
              }
            }
          }

          this.setSuccess('Template step updated successfully')
          return {
            success: true,
            data: response,
            message: 'Template step updated successfully'
          }
        } else {
          throw new Error('Failed to update step')
        }
      } catch (error) {
        console.error('Error updating step:', error)
        this.setError(this.parseError(error) || 'Failed to update template step')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to update template step'
        }
      }
    },

    // Delete step
    async deleteStep(name) {
      this.setLoading(true)
      
      try {
        await call('frappe.client.delete', {
          doctype: 'CampaignTemplateStep',
          name: name
        })

        // Remove from local state
        const stepToDelete = this.steps.find(s => s.name === name)
        this.steps = this.steps.filter(s => s.name !== name)
        
        if (this.currentStep && this.currentStep.name === name) {
          this.currentStep = null
        }

        // Update template cache
        if (stepToDelete?.template && this.stepsByTemplate[stepToDelete.template]) {
          this.stepsByTemplate[stepToDelete.template] = this.stepsByTemplate[stepToDelete.template].filter(s => s.name !== name)
        }

        this.setSuccess('Template step deleted successfully')
        return {
          success: true,
          message: 'Template step deleted successfully'
        }
      } catch (error) {
        console.error('Error deleting step:', error)
        this.setError(this.parseError(error) || 'Failed to delete template step')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to delete template step'
        }
      }
    },

    // Delete all steps by template
    async deleteStepsByTemplate(templateName) {
      this.setLoading(true)
      
      try {
        // Get all steps for this template
        const templateSteps = this.stepsByTemplate[templateName] || []
        
        if (templateSteps.length > 0) {
          // Delete each step
          const deletePromises = templateSteps.map(step => 
            call('frappe.client.delete', {
              doctype: 'CampaignTemplateStep',
              name: step.name
            })
          )
          
          await Promise.all(deletePromises)
          
          // Remove from local state
          this.steps = this.steps.filter(s => s.template !== templateName)
          
          // Clear template cache
          delete this.stepsByTemplate[templateName]
        }

        this.setSuccess('All template steps deleted successfully')
        return {
          success: true,
          message: 'All template steps deleted successfully'
        }
      } catch (error) {
        console.error('Error deleting template steps:', error)
        this.setError(this.parseError(error) || 'Failed to delete template steps')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to delete template steps'
        }
      }
    },

    // Move step up/down
    async moveStep(stepName, direction) {
      this.setLoading(true)
      
      try {
        const step = this.steps.find(s => s.name === stepName)
        if (!step) {
          throw new Error('Step not found')
        }

        const templateSteps = this.stepsByTemplate[step.template] || []
        const currentIndex = templateSteps.findIndex(s => s.name === stepName)
        
        if (currentIndex === -1) {
          throw new Error('Step not found in template')
        }

        let targetIndex
        if (direction === 'up') {
          if (currentIndex === 0) {
            throw new Error('Cannot move first step up')
          }
          targetIndex = currentIndex - 1
        } else {
          if (currentIndex === templateSteps.length - 1) {
            throw new Error('Cannot move last step down')
          }
          targetIndex = currentIndex + 1
        }

        // Swap step orders
        const currentStep = templateSteps[currentIndex]
        const targetStep = templateSteps[targetIndex]
        
        const currentOrder = currentStep.step_order
        const targetOrder = targetStep.step_order

        // Update both steps
        await Promise.all([
          this.updateStep(currentStep.name, { step_order: targetOrder }),
          this.updateStep(targetStep.name, { step_order: currentOrder })
        ])

        // Refresh template steps to get updated order
        await this.fetchStepsByTemplate(step.template)

        this.setSuccess('Step moved successfully')
        return {
          success: true,
          message: 'Step moved successfully'
        }
      } catch (error) {
        console.error('Error moving step:', error)
        this.setError(this.parseError(error) || 'Failed to move step')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to move step'
        }
      }
    },

    // Get count by template
    async getCountByTemplate(templateName) {
      try {
        const count = await call('frappe.client.get_count', {
          doctype: 'CampaignTemplateStep',
          filters: { template: templateName }
        })
        return count || 0
      } catch (error) {
        console.error('Error getting step count:', error)
        return 0
      }
    },

    // Get next step order for template
    async getNextStepOrderForTemplate(templateName) {
      try {
        const templateSteps = this.stepsByTemplate[templateName]
        if (templateSteps && templateSteps.length > 0) {
          const maxOrder = Math.max(...templateSteps.map(step => step.step_order || 0))
          return maxOrder + 1
        }
        
        // If not cached, fetch from API
        const steps = await call('frappe.client.get_list', {
          doctype: 'CampaignTemplateStep',
          fields: ['step_order'],
          filters: { template: templateName },
          order_by: 'step_order desc',
          limit_page_length: 1
        })
        
        if (steps && steps.length > 0) {
          return (steps[0].step_order || 0) + 1
        }
        
        return 1
      } catch (error) {
        console.error('Error getting next step order:', error)
        return 1
      }
    },

    // Get form data with field layout
    async fetchFormData(name = null) {
      this.setLoading(true)
      
      try {
        // Get metadata
        const metaResponse = await call('frappe.desk.form.load.getdoctype', {
          doctype: 'CampaignTemplateStep'
        })

        let docData = null
        
        // If name provided, get document data
        if (name) {
          const docResponse = await this.fetchStepById(name)
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

    // Search steps
    async searchSteps(searchTerm, options = {}) {
      this.setSearchText(searchTerm)
      return await this.fetchSteps(options)
    },

    // Get filter options for specific field
    async fetchFilterOptions(fieldname) {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'CampaignTemplateStep',
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
    validateStep(data, action = 'create') {
      const errors = []

      // Required fields
      if (!data.campaign_step_name || !data.campaign_step_name.trim()) {
        errors.push('Step name is required')
      }

      if (!data.action_type || !data.action_type.trim()) {
        errors.push('Action type is required')
      }

      if (!data.template || !data.template.trim()) {
        errors.push('Template is required')
      }

      // Business rules
      if (data.campaign_step_name && data.campaign_step_name.length > 150) {
        errors.push('Step name must be less than 150 characters')
      }

      if (data.delay_in_days < 0 || data.delay_in_days > 365) {
        errors.push('Delay must be between 0 and 365 days')
      }

      // Validate action type
      const validTypes = ['SEND_EMAIL', 'SEND_SMS', 'MANUAL_CALL', 'MANUAL_TASK']
      if (data.action_type && !validTypes.includes(data.action_type)) {
        errors.push('Invalid action type')
      }

      return errors
    },

    prepareStepForSave(data, action = 'create') {
      const prepared = { ...data }

      // Trim strings
      if (prepared.campaign_step_name) {
        prepared.campaign_step_name = prepared.campaign_step_name.trim()
      }
      if (prepared.template_content) {
        prepared.template_content = prepared.template_content.trim()
      }

      // Set defaults
      if (action === 'create') {
        prepared.delay_in_days = prepared.delay_in_days || 0
        prepared.step_order = prepared.step_order || 1
      }

      // Handle action_config JSON
      if (prepared.action_config && typeof prepared.action_config === 'string') {
        try {
          prepared.action_config = JSON.parse(prepared.action_config)
        } catch (e) {
          // Keep as string if not valid JSON
        }
      }

      return prepared
    },

    getActionTypeDisplay(type) {
      const typeMap = {
        'SEND_EMAIL': 'Send Email',
        'SEND_SMS': 'Send SMS',
        'MANUAL_CALL': 'Manual Call',
        'MANUAL_TASK': 'Manual Task'
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
              label: 'Thông tin bước',
              name: 'step_info',
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
