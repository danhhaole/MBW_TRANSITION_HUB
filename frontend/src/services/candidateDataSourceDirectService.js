import { candidateDataSourceDirectRepository } from '@/repositories/candidateDataSourceDirectRepository.js'
import { call } from 'frappe-ui'

/**
 * Direct Service for CandidateDataSource
 * Không sử dụng UniversalService pattern
 * Xử lý business logic và validation riêng
 */
class CandidateDataSourceDirectService {
  constructor() {
    this.repository = candidateDataSourceDirectRepository
  }

  /**
   * Lấy danh sách data sources với enhanced features
   */
  async getList(options = {}) {
    try {
      // Build advanced filters
      const enhancedOptions = this.buildSearchFilters(options)
      
      const result = await this.repository.getList(enhancedOptions)
      
      if (result.success) {
        // Post-process data nếu cần
        const processedData = this.processDataSourceList(result.data)
        
        return {
          success: true,
          data: {
            data: processedData,
            total: result.pagination.total,
            ...result.pagination
          }
        }
      }
      
      return result
    } catch (error) {
      console.error('Service error in getList:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch data sources'
      }
    }
  }

  /**
   * Build search filters từ query parameters
   */
  buildSearchFilters(options) {
    const { filters = {}, search_text, ...otherOptions } = options
    let enhancedFilters = { ...filters }

    // Xử lý search text - tìm trong multiple fields
    if (search_text && search_text.trim()) {
      const searchTerm = search_text.trim()
      enhancedFilters['$or'] = [
        { 'source_name': ['like', `%${searchTerm}%`] },
        { 'source_type': ['like', `%${searchTerm}%`] },
        { 'api_base_url': ['like', `%${searchTerm}%`] },
        { 'notes': ['like', `%${searchTerm}%`] }
      ]
    }

    return {
      ...otherOptions,
      filters: enhancedFilters
    }
  }

  /**
   * Process data source list - thêm computed fields
   */
  processDataSourceList(dataSources) {
    return dataSources.map(source => ({
      ...source,
      // Thêm computed fields
      display_status: this.getDisplayStatus(source),
      connection_status: this.getConnectionStatus(source),
      last_sync_formatted: this.formatLastSync(source.last_sync_at),
      type_display: this.getTypeDisplay(source.source_type)
    }))
  }

  /**
   * Lấy chi tiết data source
   */
  async getById(name) {
    try {
      const result = await this.repository.getById(name)
      
      if (result.success && result.data) {
        // Process single data source
        const processedData = this.processDataSource(result.data)
        
        return {
          success: true,
          data: processedData
        }
      }
      
      return result
    } catch (error) {
      console.error('Service error in getById:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch data source'
      }
    }
  }

  /**
   * Process single data source
   */
  processDataSource(source) {
    return {
      ...source,
      display_status: this.getDisplayStatus(source),
      connection_status: this.getConnectionStatus(source),
      last_sync_formatted: this.formatLastSync(source.last_sync_at),
      type_display: this.getTypeDisplay(source.source_type),
      auth_method_display: this.getAuthMethodDisplay(source.auth_method)
    }
  }

  /**
   * Tạo data source mới với validation
   */
  async create(data) {
    try {
      // Advanced validation
      const validationErrors = this.validateDataSource(data, 'create')
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        }
      }

      // Prepare data cho creation
      const preparedData = this.prepareDataForSave(data, 'create')
      
      const result = await this.repository.create(preparedData)
      
      if (result.success) {
        // Log activity hoặc trigger events nếu cần
        await this.logActivity('create', result.data)
      }
      
      return result
    } catch (error) {
      console.error('Service error in create:', error)
      return {
        success: false,
        error: error.message || 'Failed to create data source'
      }
    }
  }

  /**
   * Cập nhật data source
   */
  async update(name, data) {
    try {
      // Advanced validation
      const validationErrors = this.validateDataSource(data, 'update')
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        }
      }

      // Prepare data cho update
      const preparedData = this.prepareDataForSave(data, 'update')
      
      const result = await this.repository.update(name, preparedData)
      
      if (result.success) {
        // Log activity
        await this.logActivity('update', result.data, name)
      }
      
      return result
    } catch (error) {
      console.error('Service error in update:', error)
      return {
        success: false,
        error: error.message || 'Failed to update data source'
      }
    }
  }

  /**
   * Xóa data source với validation
   */
  async delete(name) {
    try {
      // Check nếu data source đang được sử dụng
      const usageCheck = await this.checkDataSourceUsage(name)
      if (usageCheck.inUse) {
        return {
          success: false,
          error: `Cannot delete data source. It is being used by: ${usageCheck.usedBy.join(', ')}`
        }
      }

      const result = await this.repository.delete(name)
      
      if (result.success) {
        await this.logActivity('delete', null, name)
      }
      
      return result
    } catch (error) {
      console.error('Service error in delete:', error)
      return {
        success: false,
        error: error.message || 'Failed to delete data source'
      }
    }
  }

  /**
   * Validate data source data
   */
  validateDataSource(data, action = 'create') {
    const errors = []

    // Required fields
    if (!data.source_name?.trim()) {
      errors.push('Source Name is required')
    }

    if (!data.source_type) {
      errors.push('Source Type is required')
    }

    if (!data.auth_method) {
      errors.push('Auth Method is required')
    }

    // Business rules validation
    if (data.source_name && data.source_name.length > 200) {
      errors.push('Source name cannot exceed 200 characters')
    }

    // Auth method specific validation
    if (data.auth_method === 'OAuth2') {
      if (!data.client_id?.trim()) {
        errors.push('Client ID is required for OAuth2')
      }
      if (!data.client_secret?.trim()) {
        errors.push('Client Secret is required for OAuth2')
      }
    }

    if (data.auth_method === 'API Key') {
      if (!data.api_key?.trim()) {
        errors.push('API Key is required for API Key authentication')
      }
    }

    // URL validation
    if (data.api_base_url && data.api_base_url.trim()) {
      try {
        new URL(data.api_base_url)
      } catch {
        errors.push('Invalid API Base URL format')
      }
    }

    // Sync frequency validation
    if (data.sync_frequency_minutes && 
        (isNaN(data.sync_frequency_minutes) || data.sync_frequency_minutes < 1)) {
      errors.push('Sync frequency must be a positive number')
    }

    return errors
  }

  /**
   * Prepare data trước khi save
   */
  prepareDataForSave(data, action) {
    const prepared = { ...data }

    // Set defaults
    if (action === 'create') {
      prepared.status = prepared.status || 'Active'
      prepared.is_active = prepared.is_active !== false ? 1 : 0
      prepared.sync_frequency_minutes = prepared.sync_frequency_minutes || 60
    }

    // Clean up data
    if (prepared.is_active === true) prepared.is_active = 1
    if (prepared.is_active === false) prepared.is_active = 0

    // Remove computed fields
    delete prepared.display_status
    delete prepared.connection_status
    delete prepared.last_sync_formatted
    delete prepared.type_display
    delete prepared.auth_method_display

    return prepared
  }

  /**
   * Lấy form data với metadata
   */
  async getFormData(name = null) {
    try {
      return await this.repository.getFormData(name)
    } catch (error) {
      console.error('Service error in getFormData:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch form data'
      }
    }
  }

  /**
   * Test connection cho data source
   */
  async testConnection(name) {
    try {
      // Gọi custom API method cho test connection
      const response = await call('mbw_mira.api.candidate_data_source.test_connection', {
        name: name
      })

      return {
        success: true,
        data: response,
        message: response?.message || 'Connection test completed'
      }
    } catch (error) {
      console.error('Service error in testConnection:', error)
      return {
        success: false,
        error: error.message || 'Connection test failed'
      }
    }
  }

  /**
   * Sync data từ source
   */
  async syncData(name) {
    try {
      // Gọi custom API method cho sync data
      const response = await call('mbw_mira.api.candidate_data_source.sync_data', {
        name: name
      })

      return {
        success: true,
        data: response,
        message: response?.message || 'Data sync completed'
      }
    } catch (error) {
      console.error('Service error in syncData:', error)
      return {
        success: false,
        error: error.message || 'Data sync failed'
      }
    }
  }

  /**
   * Check nếu data source đang được sử dụng
   */
  async checkDataSourceUsage(name) {
    try {
      // Check trong Campaign
      const campaignUsage = await call('frappe.client.get_count', {
        doctype: 'Campaign',
        filters: { source: name }
      })

      // Check trong TalentPool
      const talentPoolUsage = await call('frappe.client.get_count', {
        doctype: 'TalentPool',
        filters: { source: name }
      })

      const usedBy = []
      if (campaignUsage > 0) usedBy.push(`${campaignUsage} campaigns`)
      if (talentPoolUsage > 0) usedBy.push(`${talentPoolUsage} talent pools`)

      return {
        inUse: usedBy.length > 0,
        usedBy: usedBy
      }
    } catch (error) {
      console.error('Error checking data source usage:', error)
      return { inUse: false, usedBy: [] }
    }
  }

  /**
   * Log activity cho audit trail
   */
  async logActivity(action, data, name = null) {
    try {
      // Implement activity logging nếu cần
      console.log(`Data Source ${action}:`, { name, data })
    } catch (error) {
      console.error('Error logging activity:', error)
    }
  }

  // Helper methods cho display formatting
  getDisplayStatus(source) {
    if (!source.is_active) return 'Inactive'
    if (source.last_error) return 'Error'
    if (source.last_sync_at) return 'Active'
    return 'Not Synced'
  }

  getConnectionStatus(source) {
    if (!source.is_active) return 'disconnected'
    if (source.last_error) return 'error'
    if (source.last_sync_at) return 'connected'
    return 'unknown'
  }

  formatLastSync(lastSync) {
    if (!lastSync) return 'Never'
    return new Date(lastSync).toLocaleString('vi-VN')
  }

  getTypeDisplay(type) {
    const typeMap = {
      'ATS': 'Applicant Tracking System',
      'JobBoard': 'Job Board Platform',
      'SocialNetwork': 'Social Network',
      'Manual': 'Manual Entry',
      'Other': 'Other Source'
    }
    return typeMap[type] || type
  }

  getAuthMethodDisplay(method) {
    const methodMap = {
      'API Key': 'API Key Authentication',
      'OAuth2': 'OAuth 2.0',
      'Basic': 'Basic Authentication'
    }
    return methodMap[method] || method
  }

  /**
   * Get statistics cho dashboard
   */
  async getStatistics() {
    try {
      const [totalCount, activeCount, errorCount] = await Promise.all([
        this.repository.getCount(),
        this.repository.getCount({ is_active: 1 }),
        this.repository.getCount({ last_error: ['!=', ''] })
      ])

      return {
        success: true,
        data: {
          total: totalCount,
          active: activeCount,
          inactive: totalCount - activeCount,
          errors: errorCount
        }
      }
    } catch (error) {
      console.error('Service error in getStatistics:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch statistics'
      }
    }
  }
}

// Export singleton instance
export const candidateDataSourceDirectService = new CandidateDataSourceDirectService()
export default CandidateDataSourceDirectService 