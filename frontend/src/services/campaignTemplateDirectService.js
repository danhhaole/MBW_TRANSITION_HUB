import { campaignTemplateDirectRepository } from '@/repositories/campaignTemplateDirectRepository.js'
import { campaignTemplateStepDirectRepository } from '@/repositories/campaignTemplateStepDirectRepository.js'

/**
 * Direct Service for CampaignTemplate
 * Không sử dụng UniversalService pattern
 * Xử lý business logic và validation riêng
 */
class CampaignTemplateDirectService {
  constructor() {
    this.repository = campaignTemplateDirectRepository
    this.stepRepository = campaignTemplateStepDirectRepository
  }

  /**
   * Lấy danh sách templates với enhanced features
   */
  async getList(options = {}) {
    try {
      // Build advanced filters
      const enhancedOptions = this.buildSearchFilters(options)
      
      const result = await this.repository.getList(enhancedOptions)
      
      if (result.success) {
        // Post-process data để thêm số lượng steps
        const processedData = await this.processTemplateList(result.data)
        
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
        error: error.message || 'Failed to fetch campaign templates'
      }
    }
  }

  /**
   * Process template list để thêm thông tin bổ sung
   */
  async processTemplateList(templates) {
    if (!templates || !Array.isArray(templates)) return []

    // Lấy số lượng steps cho từng template
    const processPromises = templates.map(async (template) => {
      try {
        const stepCount = await this.stepRepository.getCountByTemplate(template.name)
        return {
          ...template,
          step_count: stepCount,
          display_status: template.is_active ? 'Active' : 'Inactive',
          type_display: this.getCampaignTypeDisplay(template.campaign_type)
        }
      } catch (error) {
        console.error(`Error processing template ${template.name}:`, error)
        return {
          ...template,
          step_count: 0,
          display_status: template.is_active ? 'Active' : 'Inactive',
          type_display: this.getCampaignTypeDisplay(template.campaign_type)
        }
      }
    })

    return await Promise.all(processPromises)
  }

  /**
   * Build search filters
   */
  buildSearchFilters(options = {}) {
    const { search_text, filters = {}, ...otherOptions } = options
    
    let enhancedFilters = { ...filters }

    // Add text search
    if (search_text && search_text.trim()) {
      enhancedFilters['template_name'] = ['like', `%${search_text.trim()}%`]
    }

    return {
      ...otherOptions,
      filters: enhancedFilters
    }
  }

  /**
   * Lấy chi tiết template với steps
   */
  async getById(name) {
    try {
      // Lấy thông tin template
      const templateResult = await this.repository.getById(name)
      
      if (!templateResult.success) {
        return templateResult
      }

      // Lấy danh sách steps
      const stepsResult = await this.stepRepository.getStepsByTemplate(name)
      
      const processedTemplate = {
        ...templateResult.data,
        display_status: templateResult.data.is_active ? 'Active' : 'Inactive',
        type_display: this.getCampaignTypeDisplay(templateResult.data.campaign_type),
        steps: stepsResult.success ? stepsResult.data : [],
        step_count: stepsResult.success ? stepsResult.data.length : 0
      }
      
      return {
        success: true,
        data: processedTemplate
      }
    } catch (error) {
      console.error('Service error in getById:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch campaign template'
      }
    }
  }

  /**
   * Tạo template mới với validation
   */
  async create(data) {
    try {
      // Advanced validation
      const validationErrors = this.validateTemplate(data, 'create')
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        }
      }

      // Prepare data cho creation
      const preparedData = this.prepareTemplateForSave(data, 'create')
      
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
        error: error.message || 'Failed to create campaign template'
      }
    }
  }

  /**
   * Cập nhật template
   */
  async update(name, data) {
    try {
      // Advanced validation
      const validationErrors = this.validateTemplate(data, 'update')
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        }
      }

      // Prepare data cho update
      const preparedData = this.prepareTemplateForSave(data, 'update')
      
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
        error: error.message || 'Failed to update campaign template'
      }
    }
  }

  /**
   * Xóa template với validation
   */
  async delete(name) {
    try {
      // Check nếu template đang được sử dụng
      const usageCheck = await this.checkTemplateUsage(name)
      if (usageCheck.inUse) {
        return {
          success: false,
          error: `Cannot delete template. It is being used by: ${usageCheck.usedBy.join(', ')}`
        }
      }

      // Xóa tất cả steps trước
      const deleteStepsResult = await this.stepRepository.deleteByTemplate(name)
      if (!deleteStepsResult.success) {
        return {
          success: false,
          error: 'Failed to delete template steps: ' + deleteStepsResult.error
        }
      }

      // Xóa template
      const result = await this.repository.delete(name)
      
      if (result.success) {
        await this.logActivity('delete', null, name)
      }
      
      return result
    } catch (error) {
      console.error('Service error in delete:', error)
      return {
        success: false,
        error: error.message || 'Failed to delete campaign template'
      }
    }
  }

  /**
   * Validate template data
   */
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
  }

  /**
   * Prepare data for save
   */
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
  }

  /**
   * Check template usage (placeholder - implement based on business needs)
   */
  async checkTemplateUsage(templateName) {
    try {
      // TODO: Check if template is used in campaigns or other places
      // For now, just return not in use
      return {
        inUse: false,
        usedBy: []
      }
    } catch (error) {
      console.error('Error checking template usage:', error)
      return {
        inUse: false,
        usedBy: []
      }
    }
  }

  /**
   * Log activity (placeholder)
   */
  async logActivity(action, data, name = null) {
    try {
      // TODO: Implement activity logging
      console.log(`Template ${action}:`, name || data?.name, data)
    } catch (error) {
      console.error('Error logging activity:', error)
    }
  }

  /**
   * Get display text cho campaign type
   */
  getCampaignTypeDisplay(type) {
    const typeMap = {
      'Email': 'Email Campaign',
      'SMS': 'SMS Campaign', 
      'Ads': 'Advertisement Campaign',
      'Social Media': 'Social Media Campaign',
      'Direct Mail': 'Direct Mail Campaign'
    }
    return typeMap[type] || type
  }

  /**
   * Get statistics cho dashboard
   */
  async getStatistics() {
    try {
      const [totalCount, activeCount, typeStats] = await Promise.all([
        this.repository.getCount(),
        this.repository.getCount({ is_active: 1 }),
        this.getTypeStatistics()
      ])

      return {
        success: true,
        data: {
          total: totalCount,
          active: activeCount,
          inactive: totalCount - activeCount,
          by_type: typeStats
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

  /**
   * Get statistics by type
   */
  async getTypeStatistics() {
    try {
      const templates = await this.repository.getList({
        fields: ['campaign_type', 'is_active'],
        page_length: 999
      })

      if (!templates.success) return {}

      const stats = {}
      templates.data.forEach(template => {
        const type = template.campaign_type
        if (!stats[type]) {
          stats[type] = { total: 0, active: 0 }
        }
        stats[type].total++
        if (template.is_active) {
          stats[type].active++
        }
      })

      return stats
    } catch (error) {
      console.error('Error getting type statistics:', error)
      return {}
    }
  }

  /**
   * Search templates
   */
  async search(searchTerm, options = {}) {
    try {
      const searchOptions = {
        ...options,
        search_text: searchTerm
      }

      return await this.getList(searchOptions)
    } catch (error) {
      console.error('Service error in search:', error)
      return {
        success: false,
        error: error.message || 'Search failed'
      }
    }
  }
}

// Create instance
export const campaignTemplateDirectService = new CampaignTemplateDirectService() 