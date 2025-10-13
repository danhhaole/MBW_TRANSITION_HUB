import { defineStore } from 'pinia'
import { call } from 'frappe-ui'

export const useCandidateDataSourceStore = defineStore('candidateDataSource', {
  state: () => ({
    dataSources: [],
    currentDataSource: null,
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
    sourceTypeFilter: '',
    statusFilter: '',
    // Form state
    formData: null,
    fieldLayout: [],
    meta: null,
    // Statistics
    statistics: {
      total: 0,
      by_type: {},
      by_status: {}
    }
  }),

  getters: {
    // Client-side filtered data sources
    filteredDataSources: (state) => {
      let filtered = state.dataSources

      if (state.searchText) {
        filtered = filtered.filter(source =>
          source.source_name?.toLowerCase().includes(state.searchText.toLowerCase()) ||
          source.description?.toLowerCase().includes(state.searchText.toLowerCase())
        )
      }

      if (state.sourceTypeFilter) {
        filtered = filtered.filter(source => source.source_type === state.sourceTypeFilter)
      }

      if (state.statusFilter) {
        filtered = filtered.filter(source => source.status === state.statusFilter)
      }

      return filtered
    },

    // Get data source by name
    getDataSourceByName: (state) => (name) => {
      return state.dataSources.find(source => source.name === name)
    },

    // Active data sources only
    activeDataSources: (state) => {
      return state.dataSources.filter(source => source.status === 'Active')
    },

    // Data sources by type
    dataSourcesByType: (state) => (type) => {
      return state.dataSources.filter(source => source.source_type === type)
    },

    // External connection data sources
    externalConnectionSources: (state) => {
      return state.dataSources.filter(source => 
        source.source_type === 'External Connection' && source.status === 'Active'
      )
    },

    // File upload data sources
    fileUploadSources: (state) => {
      return state.dataSources.filter(source => 
        source.source_type === 'File Upload' && source.status === 'Active'
      )
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
    setSourceTypeFilter(type) {
      this.sourceTypeFilter = type
    },

    setStatusFilter(status) {
      this.statusFilter = status
    },

    // Reset filters
    resetFilters() {
      this.searchText = ''
      this.sourceTypeFilter = ''
      this.statusFilter = ''
    },

    // Get data sources list with pagination and filters
    async fetchDataSources(options = {}) {
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
          enhancedFilters['source_name'] = ['like', `%${this.searchText.trim()}%`]
        }

        if (this.sourceTypeFilter) {
          enhancedFilters['source_type'] = this.sourceTypeFilter
        }

        if (this.statusFilter) {
          enhancedFilters['status'] = this.statusFilter
        }

        // Fetch data sources
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Data Source',
          fields: fields,
          filters: enhancedFilters,
          order_by: order_by,
          limit_page_length: page_length,
          limit_start: start
        })

        // Get total count for pagination
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'Mira Data Source',
          filters: enhancedFilters
        })

        // Process data sources to add display fields
        const processedDataSources = (response || []).map(source => ({
          ...source,
          display_status: this.getStatusDisplay(source.status),
          display_type: this.getSourceTypeDisplay(source.source_type),
          connection_info: this.getConnectionInfo(source)
        }))

        this.dataSources = processedDataSources

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

        this.setSuccess('Data sources loaded successfully')
        return {
          success: true,
          data: processedDataSources,
          pagination: this.pagination
        }
      } catch (error) {
        console.error('Error fetching data sources:', error)
        this.setError(error.message || 'Failed to fetch candidate data sources')
        return {
          success: false,
          error: error.message || 'Failed to fetch candidate data sources'
        }
      }
    },

    // Get data source by ID
    async fetchDataSourceById(name) {
      this.setLoading(true)

      try {
        const response = await call('frappe.client.get', {
          doctype: 'Mira Data Source',
          name: name
        })

        if (response) {
          const processedDataSource = {
            ...response,
            display_status: this.getStatusDisplay(response.status),
            display_type: this.getSourceTypeDisplay(response.source_type),
            connection_info: this.getConnectionInfo(response)
          }

          this.currentDataSource = processedDataSource
          this.setSuccess('Data source loaded successfully')

          return {
            success: true,
            data: processedDataSource
          }
        } else {
          throw new Error('Data source not found')
        }
      } catch (error) {
        console.error('Error fetching data source:', error)
        this.setError(error.message || 'Failed to fetch candidate data source')
        return {
          success: false,
          error: error.message || 'Failed to fetch candidate data source'
        }
      }
    },

    // Create new data source
    async createDataSource(data) {
      this.setLoading(true)

      try {
        // Validate required fields
        const validationErrors = this.validateDataSource(data, 'create')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for creation
        const preparedData = this.prepareDataSourceForSave(data, 'create')

        const docData = {
          doctype: 'Mira Data Source',
          ...preparedData
        }

        const response = await call('frappe.client.insert', {
          doc: docData
        })

        if (response) {
          // Add to local state
          const newDataSource = {
            ...response,
            display_status: this.getStatusDisplay(response.status),
            display_type: this.getSourceTypeDisplay(response.source_type),
            connection_info: this.getConnectionInfo(response)
          }

          this.dataSources.unshift(newDataSource)
          this.currentDataSource = newDataSource

          this.setSuccess('Candidate data source created successfully')
          return {
            success: true,
            data: newDataSource,
            message: 'Candidate data source created successfully'
          }
        } else {
          throw new Error('Failed to create data source')
        }
      } catch (error) {
        console.error('Error creating data source:', error)
        this.setError(this.parseError(error) || 'Failed to create candidate data source')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to create candidate data source'
        }
      }
    },

    // Update data source
    async updateDataSource(name, data) {
      this.setLoading(true)

      try {
        // Validate required fields
        const validationErrors = this.validateDataSource(data, 'update')
        if (validationErrors.length > 0) {
          throw new Error(validationErrors.join(', '))
        }

        // Prepare data for update
        const preparedData = this.prepareDataSourceForSave(data, 'update')

        const response = await call('frappe.client.set_value', {
          doctype: 'Mira Data Source',
          name: name,
          fieldname: preparedData
        })

        if (response) {
          // Update local state
          const index = this.dataSources.findIndex(s => s.name === name)
          if (index !== -1) {
            this.dataSources[index] = {
              ...this.dataSources[index],
              ...preparedData,
              display_status: this.getStatusDisplay(preparedData.status),
              display_type: this.getSourceTypeDisplay(preparedData.source_type),
              connection_info: this.getConnectionInfo(preparedData)
            }
          }

          if (this.currentDataSource && this.currentDataSource.name === name) {
            this.currentDataSource = {
              ...this.currentDataSource,
              ...preparedData,
              display_status: this.getStatusDisplay(preparedData.status),
              display_type: this.getSourceTypeDisplay(preparedData.source_type),
              connection_info: this.getConnectionInfo(preparedData)
            }
          }

          this.setSuccess('Candidate data source updated successfully')
          return {
            success: true,
            data: response,
            message: 'Candidate data source updated successfully'
          }
        } else {
          throw new Error('Failed to update data source')
        }
      } catch (error) {
        console.error('Error updating data source:', error)
        this.setError(this.parseError(error) || 'Failed to update candidate data source')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to update candidate data source'
        }
      }
    },

    // Delete data source
    async deleteDataSource(name) {
      this.setLoading(true)

      try {
        await call('frappe.client.delete', {
          doctype: 'Mira Data Source',
          name: name
        })

        // Remove from local state
        this.dataSources = this.dataSources.filter(s => s.name !== name)

        if (this.currentDataSource && this.currentDataSource.name === name) {
          this.currentDataSource = null
        }

        this.setSuccess('Candidate data source deleted successfully')
        return {
          success: true,
          message: 'Candidate data source deleted successfully'
        }
      } catch (error) {
        console.error('Error deleting data source:', error)
        this.setError(this.parseError(error) || 'Failed to delete candidate data source')
        return {
          success: false,
          error: this.parseError(error) || 'Failed to delete candidate data source'
        }
      }
    },

    // Get form data with field layout
    async fetchFormData(name = null) {
      this.setLoading(true)

      try {
        // Get metadata
        const metaResponse = await call('frappe.desk.form.load.getdoctype', {
          doctype: 'Mira Data Source',
          with_parent: 1
        })

        let docData = null

        // If name provided, get document data
        if (name) {
          const docResponse = await this.fetchDataSourceById(name)
          if (docResponse.success) {
            docData = docResponse.data
          }
        }

        // Create field layout from metadata
        let fieldLayout = []
        if (metaResponse?.docs?.length > 0) {
          const meta = metaResponse.docs.find(doc => doc.name === 'Mira Data Source')
          if (meta) {
            fieldLayout = this.createFieldLayout(meta.fields)
          }
        }

        this.formData = docData
        this.fieldLayout = fieldLayout
        this.meta = metaResponse?.docs?.find(doc => doc.name === 'Mira Data Source') || null

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

    // Search data sources
    async searchDataSources(searchTerm, options = {}) {
      this.setSearchText(searchTerm)
      return await this.fetchDataSources(options)
    },

    // Get filter options for specific field
    async fetchFilterOptions(fieldname) {
      try {
        const response = await call('frappe.client.get_list', {
          doctype: 'Mira Data Source',
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

    // Get statistics
    async fetchStatistics() {
      try {
        // Get total count
        const totalCount = await call('frappe.client.get_count', {
          doctype: 'Mira Data Source'
        })

        // Get count by type
        const typeStats = await call('frappe.client.get_list', {
          doctype: 'Mira Data Source',
          fields: ['source_type', 'count(*) as count'],
          group_by: 'source_type'
        })

        // Get count by status
        const statusStats = await call('frappe.client.get_list', {
          doctype: 'Mira Data Source',
          fields: ['status', 'count(*) as count'],
          group_by: 'status'
        })

        const statistics = {
          total: totalCount || 0,
          by_type: {},
          by_status: {}
        }

        // Process type statistics
        if (typeStats && Array.isArray(typeStats)) {
          typeStats.forEach(stat => {
            statistics.by_type[stat.source_type] = stat.count
          })
        }

        // Process status statistics
        if (statusStats && Array.isArray(statusStats)) {
          statusStats.forEach(stat => {
            statistics.by_status[stat.status] = stat.count
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

    // Set pagination
    setPagination(page, limit = null) {
      this.pagination.page = page
      if (limit) {
        this.pagination.limit = limit
      }
    },

    // Helper methods
    validateDataSource(data, action = 'create') {
      const errors = []

      // Required fields
      if (!data.source_name || !data.source_name.trim()) {
        errors.push('Source name is required')
      }

      if (!data.source_type || !data.source_type.trim()) {
        errors.push('Source type is required')
      }

      // Business rules
      if (data.source_name && data.source_name.length > 150) {
        errors.push('Source name must be less than 150 characters')
      }

      // Validate source type
      const validTypes = ['External Connection', 'File Upload', 'Manual Entry', 'API Integration']
      if (data.source_type && !validTypes.includes(data.source_type)) {
        errors.push('Invalid source type')
      }

      // External connection specific validation
      if (data.source_type === 'External Connection') {
        if (!data.external_connection) {
          errors.push('External connection is required for External Connection type')
        }
      }

      return errors
    },

    prepareDataSourceForSave(data, action = 'create') {
      const prepared = { ...data }

      // Trim strings
      if (prepared.source_name) {
        prepared.source_name = prepared.source_name.trim()
      }
      if (prepared.description) {
        prepared.description = prepared.description.trim()
      }

      // Set defaults
      if (action === 'create') {
        prepared.status = prepared.status || 'Active'
      }

      // Handle connection_config JSON
      if (prepared.connection_config && typeof prepared.connection_config === 'string') {
        try {
          prepared.connection_config = JSON.parse(prepared.connection_config)
        } catch (e) {
          // Keep as string if not valid JSON
        }
      }

      return prepared
    },

    getStatusDisplay(status) {
      const statusMap = {
        'Active': 'Active',
        'Inactive': 'Inactive',
        'Error': 'Error',
        'Pending': 'Pending'
      }
      return statusMap[status] || status
    },

    getSourceTypeDisplay(type) {
      const typeMap = {
        'External Connection': 'External Connection',
        'File Upload': 'File Upload',
        'Manual Entry': 'Manual Entry',
        'API Integration': 'API Integration'
      }
      return typeMap[type] || type
    },

    getConnectionInfo(source) {
      if (source.source_type === 'External Connection' && source.external_connection) {
        return {
          type: 'external',
          connection: source.external_connection,
          platform: source.platform_type || 'Unknown'
        }
      }
      
      if (source.source_type === 'File Upload') {
        return {
          type: 'file',
          format: source.file_format || 'Unknown',
          last_upload: source.last_upload_date
        }
      }

      return {
        type: 'other',
        info: source.source_type
      }
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
