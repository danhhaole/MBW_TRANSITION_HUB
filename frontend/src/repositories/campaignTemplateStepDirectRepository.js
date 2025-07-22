import { call } from 'frappe-ui'

/**
 * Direct Repository for CampaignTemplateStep
 * Không sử dụng UniversalRepository pattern
 * Gọi trực tiếp Frappe API endpoints
 */
class CampaignTemplateStepDirectRepository {
  constructor() {
    this.doctype = 'CampaignTemplateStep'
  }

  /**
   * Lấy danh sách CampaignTemplateStep với pagination và filters
   */
  async getList(options = {}) {
    try {
      const {
        filters = {},
        fields = ['*'],
        order_by = 'step_order asc',
        page_length = 20,
        start = 0
      } = options

      const response = await call('frappe.client.get_list', {
        doctype: this.doctype,
        fields: fields,
        filters: filters,
        order_by: order_by,
        limit_page_length: page_length,
        limit_start: start
      })

      // Get total count for pagination
      const totalCount = await this.getCount(filters)

      return {
        success: true,
        data: response || [],
        pagination: {
          total: totalCount,
          page: Math.floor(start / page_length) + 1,
          limit: page_length,
          pages: Math.ceil(totalCount / page_length),
          has_next: (start + page_length) < totalCount,
          has_prev: start > 0,
          showing_from: start + 1,
          showing_to: Math.min(start + page_length, totalCount)
        }
      }
    } catch (error) {
      console.error('Error in getList:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch template steps',
        data: [],
        pagination: {}
      }
    }
  }

  /**
   * Lấy các step theo template
   */
  async getStepsByTemplate(templateName, options = {}) {
    const filters = {
      template: templateName,
      ...options.filters
    }
    
    return await this.getList({
      ...options,
      filters,
      order_by: 'step_order asc'
    })
  }

  /**
   * Lấy số lượng bản ghi với filters
   */
  async getCount(filters = {}) {
    try {
      const response = await call('frappe.client.get_count', {
        doctype: this.doctype,
        filters: filters
      })
      return response || 0
    } catch (error) {
      console.error('Error in getCount:', error)
      return 0
    }
  }

  /**
   * Lấy số lượng steps theo template
   */
  async getCountByTemplate(templateName) {
    return await this.getCount({ template: templateName })
  }

  /**
   * Lấy chi tiết một CampaignTemplateStep
   */
  async getById(name) {
    try {
      const response = await call('frappe.client.get', {
        doctype: this.doctype,
        name: name
      })

      return {
        success: true,
        data: response || null
      }
    } catch (error) {
      console.error('Error in getById:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch template step',
        data: null
      }
    }
  }

  /**
   * Tạo mới CampaignTemplateStep
   */
  async create(data) {
    try {
      const docData = {
        doctype: this.doctype,
        ...data
      }

      const response = await call('frappe.client.insert', {
        doc: docData
      })

      return {
        success: true,
        data: response || null,
        message: 'Template step created successfully'
      }
    } catch (error) {
      console.error('Error in create:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to create template step',
        data: null
      }
    }
  }

  /**
   * Cập nhật CampaignTemplateStep
   */
  async update(name, data) {
    try {
      // Sử dụng set_value để cập nhật trực tiếp mà không cần get trước
      const response = await call('frappe.client.set_value', {
        doctype: this.doctype,
        name: name,
        fieldname: data
      })

      return {
        success: true,
        data: response || null,
        message: 'Template step updated successfully'
      }
    } catch (error) {
      console.error('Error in update:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to update template step',
        data: null
      }
    }
  }

  /**
   * Xóa CampaignTemplateStep
   */
  async delete(name) {
    try {
      await call('frappe.client.delete', {
        doctype: this.doctype,
        name: name
      })

      return {
        success: true,
        message: 'Template step deleted successfully'
      }
    } catch (error) {
      console.error('Error in delete:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to delete template step'
      }
    }
  }

  /**
   * Xóa tất cả steps của một template
   */
  async deleteByTemplate(templateName) {
    try {
      // Get all steps for this template first
      const stepsResponse = await this.getStepsByTemplate(templateName)
      
      if (stepsResponse.success && stepsResponse.data.length > 0) {
        // Delete each step
        const deletePromises = stepsResponse.data.map(step => 
          this.delete(step.name)
        )
        
        const results = await Promise.all(deletePromises)
        
        // Check if all deletions were successful
        const failedDeletions = results.filter(result => !result.success)
        
        if (failedDeletions.length > 0) {
          return {
            success: false,
            error: `Failed to delete ${failedDeletions.length} steps`
          }
        }
      }

      return {
        success: true,
        message: 'All template steps deleted successfully'
      }
    } catch (error) {
      console.error('Error in deleteByTemplate:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to delete template steps'
      }
    }
  }

  /**
   * Update step orders sau khi thêm/xóa
   */
  async reorderSteps(templateName, stepUpdates) {
    try {
      const updatePromises = stepUpdates.map(({ name, step_order }) => 
        this.update(name, { step_order })
      )
      
      const results = await Promise.all(updatePromises)
      
      // Check if all updates were successful
      const failedUpdates = results.filter(result => !result.success)
      
      if (failedUpdates.length > 0) {
        return {
          success: false,
          error: `Failed to reorder ${failedUpdates.length} steps`
        }
      }

      return {
        success: true,
        message: 'Steps reordered successfully'
      }
    } catch (error) {
      console.error('Error in reorderSteps:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to reorder steps'
      }
    }
  }

  /**
   * Parse error message từ Frappe response
   */
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

  /**
   * Lấy metadata của doctype
   */
  async getFieldMeta() {
    try {
      const response = await call('frappe.desk.form.load.getdoctype', {
        doctype: this.doctype
      })

      return {
        success: true,
        data: response?.docs?.[0] || null
      }
    } catch (error) {
      console.error('Error in getFieldMeta:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch field metadata',
        data: null
      }
    }
  }

  /**
   * Lấy form data với field layout
   */
  async getFormData(name = null) {
    try {
      // Lấy metadata
      const metaResponse = await this.getFieldMeta()
      let docData = null
      
      // Nếu có name thì lấy data của document
      if (name) {
        const docResponse = await this.getById(name)
        if (docResponse.success) {
          docData = docResponse.data
        }
      }

      // Tạo field layout từ metadata
      let fieldLayout = []
      if (metaResponse.success && metaResponse.data) {
        fieldLayout = this.createFieldLayout(metaResponse.data.fields)
      }

      return {
        success: true,
        data: {
          doc: docData,
          fieldLayout: fieldLayout,
          meta: metaResponse.data
        }
      }
    } catch (error) {
      console.error('Error in getFormData:', error)
      return {
        success: false,
        error: error.message || 'Failed to fetch form data',
        data: null
      }
    }
  }

  /**
   * Tạo field layout từ metadata fields
   */
  createFieldLayout(fields) {
    if (!fields || !Array.isArray(fields)) return []

    // Filter và group fields
    const visibleFields = fields.filter(field => 
      !field.hidden && 
      field.fieldtype !== 'Section Break' && 
      field.fieldtype !== 'Column Break' &&
      field.fieldtype !== 'Tab Break'
    )

    // Tạo layout structure
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
  }

  /**
   * Get filter options for specific field
   */
  async getFilterOptions(fieldname) {
    try {
      const response = await call('frappe.client.get_list', {
        doctype: this.doctype,
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
      console.error('Error in getFilterOptions:', error)
      return {
        success: false,
        error: error.message || 'Failed to get filter options',
        data: []
      }
    }
  }
}

// Create instance
export const campaignTemplateStepDirectRepository = new CampaignTemplateStepDirectRepository() 