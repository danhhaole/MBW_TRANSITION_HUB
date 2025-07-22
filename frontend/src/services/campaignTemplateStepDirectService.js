import { campaignTemplateStepDirectRepository } from '@/repositories/campaignTemplateStepDirectRepository.js'

/**
 * Direct Service for CampaignTemplateStep
 * Không sử dụng UniversalService pattern
 * Xử lý business logic và validation riêng
 */
class CampaignTemplateStepDirectService {
  constructor() {
    this.repository = campaignTemplateStepDirectRepository
  }

  /**
   * Lấy danh sách steps với enhanced features
   */
  async getList(options = {}) {
    try {
      // Build advanced filters
      const enhancedOptions = this.buildSearchFilters(options)
      
      const result = await this.repository.getList(enhancedOptions)
      
      if (result.success) {
        // Post-process data
        const processedData = this.processStepList(result.data)
        
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
        error: error.message || 'Failed to fetch template steps'
      }
    }
  }

  /**
   * Lấy các step theo template
   */
  async getStepsByTemplate(templateName, options = {}) {
    try {
      const result = await this.repository.getStepsByTemplate(templateName, options)
      
      if (result.success) {
        // Post-process data
        const processedData = this.processStepList(result.data)
        
        return {
          success: true,
          data: processedData
        }
      }
      
      return result
    } catch (error) {
      console.error('Service error in getStepsByTemplate:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch template steps'
      }
    }
  }

  /**
   * Process step list để thêm thông tin bổ sung
   */
  processStepList(steps) {
    if (!steps || !Array.isArray(steps)) return []

    return steps.map(step => ({
      ...step,
      action_type_display: this.getActionTypeDisplay(step.action_type),
      delay_display: this.getDelayDisplay(step.delay_in_days),
      has_content: !!(step.template_content && step.template_content.trim()),
      has_config: !!(step.action_config && Object.keys(step.action_config).length > 0)
    }))
  }

  /**
   * Build search filters
   */
  buildSearchFilters(options = {}) {
    const { search_text, filters = {}, ...otherOptions } = options
    
    let enhancedFilters = { ...filters }

    // Add text search
    if (search_text && search_text.trim()) {
      enhancedFilters['campaign_step_name'] = ['like', `%${search_text.trim()}%`]
    }

    return {
      ...otherOptions,
      filters: enhancedFilters
    }
  }

  /**
   * Lấy chi tiết step
   */
  async getById(name) {
    try {
      const result = await this.repository.getById(name)
      
      if (result.success && result.data) {
        // Process single step
        const processedStep = this.processStep(result.data)
        
        return {
          success: true,
          data: processedStep
        }
      }
      
      return result
    } catch (error) {
      console.error('Service error in getById:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch template step'
      }
    }
  }

  /**
   * Process single step
   */
  processStep(step) {
    return {
      ...step,
      action_type_display: this.getActionTypeDisplay(step.action_type),
      delay_display: this.getDelayDisplay(step.delay_in_days),
      has_content: !!(step.template_content && step.template_content.trim()),
      has_config: !!(step.action_config && Object.keys(step.action_config).length > 0)
    }
  }

  /**
   * Tạo step mới với validation
   */
  async create(data) {
    try {
      // Advanced validation
      const validationErrors = this.validateStep(data, 'create')
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        }
      }

      // Auto-assign step order nếu không có
      if (!data.step_order) {
        const nextOrder = await this.getNextStepOrder(data.template)
        data.step_order = nextOrder
      }

      // Prepare data cho creation
      const preparedData = this.prepareStepForSave(data, 'create')
      
      const result = await this.repository.create(preparedData)
      
      if (result.success) {
        // Log activity
        await this.logActivity('create', result.data)
      }
      
      return result
    } catch (error) {
      console.error('Service error in create:', error)
      return {
        success: false,
        error: error.message || 'Failed to create template step'
      }
    }
  }

  /**
   * Cập nhật step
   */
  async update(name, data) {
    try {
      // Advanced validation
      const validationErrors = this.validateStep(data, 'update')
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        }
      }

      // Prepare data cho update
      const preparedData = this.prepareStepForSave(data, 'update')
      
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
        error: error.message || 'Failed to update template step'
      }
    }
  }

  /**
   * Xóa step với reorder
   */
  async delete(name) {
    try {
      // Get step info trước khi xóa
      const stepResult = await this.repository.getById(name)
      if (!stepResult.success) {
        return stepResult
      }

      const step = stepResult.data
      const templateName = step.template
      const deletedOrder = step.step_order

      // Xóa step
      const result = await this.repository.delete(name)
      
      if (result.success) {
        // Reorder các steps còn lại
        await this.reorderStepsAfterDelete(templateName, deletedOrder)
        await this.logActivity('delete', null, name)
      }
      
      return result
    } catch (error) {
      console.error('Service error in delete:', error)
      return {
        success: false,
        error: error.message || 'Failed to delete template step'
      }
    }
  }

  /**
   * Reorder steps sau khi xóa
   */
  async reorderStepsAfterDelete(templateName, deletedOrder) {
    try {
      // Get all steps for template with higher order
      const stepsResult = await this.repository.getStepsByTemplate(templateName, {
        filters: {
          step_order: ['>', deletedOrder]
        }
      })

      if (stepsResult.success && stepsResult.data.length > 0) {
        // Update orders
        const stepUpdates = stepsResult.data.map(step => ({
          name: step.name,
          step_order: step.step_order - 1
        }))

        await this.repository.reorderSteps(templateName, stepUpdates)
      }
    } catch (error) {
      console.error('Error reordering steps after delete:', error)
    }
  }

  /**
   * Get next step order cho template
   */
  async getNextStepOrder(templateName) {
    try {
      const stepsResult = await this.repository.getStepsByTemplate(templateName)
      
      if (!stepsResult.success || !stepsResult.data.length) {
        return 1
      }

      const maxOrder = Math.max(...stepsResult.data.map(step => step.step_order || 0))
      return maxOrder + 1
    } catch (error) {
      console.error('Error getting next step order:', error)
      return 1
    }
  }

  /**
   * Validate step data
   */
  validateStep(data, action = 'create') {
    const errors = []

    // Required fields
    if (!data.template || !data.template.trim()) {
      errors.push('Template is required')
    }

    if (!data.campaign_step_name || !data.campaign_step_name.trim()) {
      errors.push('Step name is required')
    }

    if (!data.action_type || !data.action_type.trim()) {
      errors.push('Action type is required')
    }

    // Business rules
    if (data.campaign_step_name && data.campaign_step_name.length > 150) {
      errors.push('Step name must be less than 150 characters')
    }

    if (data.step_order && (data.step_order < 1 || data.step_order > 999)) {
      errors.push('Step order must be between 1 and 999')
    }

    if (data.delay_in_days && (data.delay_in_days < 0 || data.delay_in_days > 365)) {
      errors.push('Delay must be between 0 and 365 days')
    }

    // Validate action type
    const validActionTypes = ['SEND_EMAIL', 'SEND_SMS', 'MANUAL_CALL', 'MANUAL_TASK']
    if (data.action_type && !validActionTypes.includes(data.action_type)) {
      errors.push('Invalid action type')
    }

    // Validate action config if present
    if (data.action_config) {
      try {
        if (typeof data.action_config === 'string') {
          JSON.parse(data.action_config)
        }
      } catch (e) {
        errors.push('Invalid action config JSON format')
      }
    }

    return errors
  }

  /**
   * Prepare data for save
   */
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
      prepared.delay_in_days = prepared.delay_in_days !== undefined ? prepared.delay_in_days : 0
    }

    // Handle JSON fields
    if (prepared.action_config && typeof prepared.action_config === 'string') {
      try {
        prepared.action_config = JSON.parse(prepared.action_config)
      } catch (e) {
        // Keep as string if invalid JSON
      }
    }

    return prepared
  }

  /**
   * Log activity (placeholder)
   */
  async logActivity(action, data, name = null) {
    try {
      // TODO: Implement activity logging
      console.log(`Template Step ${action}:`, name || data?.name, data)
    } catch (error) {
      console.error('Error logging activity:', error)
    }
  }

  /**
   * Get display text cho action type
   */
  getActionTypeDisplay(actionType) {
    const actionTypeMap = {
      'SEND_EMAIL': 'Send Email',
      'SEND_SMS': 'Send SMS',
      'MANUAL_CALL': 'Manual Call',
      'MANUAL_TASK': 'Manual Task'
    }
    return actionTypeMap[actionType] || actionType
  }

  /**
   * Get display text cho delay
   */
  getDelayDisplay(delayInDays) {
    if (!delayInDays || delayInDays === 0) {
      return 'Immediate'
    }
    
    if (delayInDays === 1) {
      return '1 day'
    }
    
    return `${delayInDays} days`
  }

  /**
   * Move step up/down in order
   */
  async moveStep(stepName, direction) {
    try {
      const stepResult = await this.repository.getById(stepName)
      if (!stepResult.success) {
        return stepResult
      }

      const step = stepResult.data
      const currentOrder = step.step_order
      const templateName = step.template

      // Calculate new order
      const newOrder = direction === 'up' ? currentOrder - 1 : currentOrder + 1

      // Check if there's a step at the target position
      const targetStepsResult = await this.repository.getStepsByTemplate(templateName, {
        filters: { step_order: newOrder }
      })

      if (!targetStepsResult.success) {
        return targetStepsResult
      }

      const targetStep = targetStepsResult.data[0]
      if (!targetStep) {
        return {
          success: false,
          error: `Cannot move step ${direction}`
        }
      }

      // Swap orders
      const updatePromises = [
        this.repository.update(stepName, { step_order: newOrder }),
        this.repository.update(targetStep.name, { step_order: currentOrder })
      ]

      const results = await Promise.all(updatePromises)
      const failedUpdates = results.filter(result => !result.success)

      if (failedUpdates.length > 0) {
        return {
          success: false,
          error: 'Failed to move step'
        }
      }

      return {
        success: true,
        message: `Step moved ${direction} successfully`
      }
    } catch (error) {
      console.error('Service error in moveStep:', error)
      return {
        success: false,
        error: error.message || 'Failed to move step'
      }
    }
  }

  /**
   * Duplicate step
   */
  async duplicateStep(stepName) {
    try {
      const stepResult = await this.repository.getById(stepName)
      if (!stepResult.success) {
        return stepResult
      }

      const originalStep = stepResult.data
      
      // Create duplicate data
      const duplicateData = {
        template: originalStep.template,
        campaign_step_name: `${originalStep.campaign_step_name} (Copy)`,
        action_type: originalStep.action_type,
        delay_in_days: originalStep.delay_in_days,
        template_content: originalStep.template_content,
        action_config: originalStep.action_config
      }

      // Get next step order
      const nextOrder = await this.getNextStepOrder(originalStep.template)
      duplicateData.step_order = nextOrder

      return await this.create(duplicateData)
    } catch (error) {
      console.error('Service error in duplicateStep:', error)
      return {
        success: false,
        error: error.message || 'Failed to duplicate step'
      }
    }
  }
}

// Create instance
export const campaignTemplateStepDirectService = new CampaignTemplateStepDirectService() 