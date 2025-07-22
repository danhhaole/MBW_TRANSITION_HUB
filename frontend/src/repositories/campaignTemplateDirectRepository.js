import { call } from 'frappe-ui'

/**
 * Direct Repository for CampaignTemplate
 * Không sử dụng UniversalRepository pattern
 * Gọi trực tiếp Frappe API endpoints
 */
class CampaignTemplateDirectRepository {
  constructor() {
    this.doctype = 'CampaignTemplate'
  }

  /**
   * Lấy danh sách CampaignTemplate với pagination và filters
   */
  async getList(options = {}) {
    try {
      const {
        filters = {},
        fields = ['*'],
        order_by = 'modified desc',
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
        error: error.message || 'Failed to fetch campaign templates',
        data: [],
        pagination: {}
      }
    }
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
   * Lấy chi tiết một CampaignTemplate
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
        error: error.message || 'Failed to fetch campaign template',
        data: null
      }
    }
  }

  /**
   * Tạo mới CampaignTemplate
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
        message: 'Campaign template created successfully'
      }
    } catch (error) {
      console.error('Error in create:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to create campaign template',
        data: null
      }
    }
  }

  /**
   * Cập nhật CampaignTemplate
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
        message: 'Campaign template updated successfully'
      }
    } catch (error) {
      console.error('Error in update:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to update campaign template',
        data: null
      }
    }
  }

  /**
   * Xóa CampaignTemplate
   */
  async delete(name) {
    try {
      await call('frappe.client.delete', {
        doctype: this.doctype,
        name: name
      })

      return {
        success: true,
        message: 'Campaign template deleted successfully'
      }
    } catch (error) {
      console.error('Error in delete:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to delete campaign template'
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
  }

  /**
   * Search templates
   */
  async search(searchTerm, options = {}) {
    try {
      const filters = {
        ...options.filters,
        'template_name': ['like', `%${searchTerm}%`]
      }

      return await this.getList({
        ...options,
        filters
      })
    } catch (error) {
      console.error('Error in search:', error)
      return {
        success: false,
        error: error.message || 'Search failed',
        data: [],
        pagination: {}
      }
    }
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
export const campaignTemplateDirectRepository = new CampaignTemplateDirectRepository() 