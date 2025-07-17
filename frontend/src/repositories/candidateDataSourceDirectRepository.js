import { createResource, call } from 'frappe-ui'

/**
 * Direct Repository for CandidateDataSource
 * Không sử dụng UniversalRepository pattern
 * Gọi trực tiếp Frappe API endpoints
 */
class CandidateDataSourceDirectRepository {
  constructor() {
    this.doctype = 'CandidateDataSource'
  }

  /**
   * Lấy danh sách CandidateDataSource với pagination và filters
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
        error: error.message || 'Failed to fetch data sources',
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
   * Lấy chi tiết một CandidateDataSource
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
        error: error.message || 'Failed to fetch data source',
        data: null
      }
    }
  }

  /**
   * Tạo mới CandidateDataSource
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
        message: 'Data source created successfully'
      }
    } catch (error) {
      console.error('Error in create:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to create data source',
        data: null
      }
    }
  }

  /**
   * Cập nhật CandidateDataSource
   */
  async update(name, data) {
    try {
      const response = await call('frappe.client.set_value', {
        doctype: this.doctype,
        name: name,
        values: data
      })

      return {
        success: true,
        data: response || null,
        message: 'Data source updated successfully'
      }
    } catch (error) {
      console.error('Error in update:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to update data source',
        data: null
      }
    }
  }

  /**
   * Xóa CandidateDataSource
   */
  async delete(name) {
    try {
      await call('frappe.client.delete', {
        doctype: this.doctype,
        name: name
      })

      return {
        success: true,
        message: 'Data source deleted successfully'
      }
    } catch (error) {
      console.error('Error in delete:', error)
      return {
        success: false,
        error: this.parseError(error) || 'Failed to delete data source'
      }
    }
  }

  /**
   * Lấy field metadata cho form
   */
  async getFieldMeta() {
    try {
      const response = await call('frappe.desk.form.load.getdoctype', {
        doctype: this.doctype,
        with_parent: 1
      })

      if (response && response.docs && response.docs.length > 0) {
        const meta = response.docs.find(doc => doc.name === this.doctype)
        return {
          success: true,
          data: meta || null
        }
      }

      return {
        success: false,
        error: 'No metadata found',
        data: null
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
   * Parse error messages từ Frappe
   */
  parseError(error) {
    if (error.messages && Array.isArray(error.messages)) {
      return error.messages.join(', ')
    }
    if (error.message) {
      return error.message
    }
    if (typeof error === 'string') {
      return error
    }
    return null
  }

  /**
   * Search data sources
   */
  async search(searchTerm, options = {}) {
    try {
      const filters = {
        ...options.filters,
        'source_name': ['like', `%${searchTerm}%`]
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

// Export singleton instance
export const candidateDataSourceDirectRepository = new CandidateDataSourceDirectRepository()
export default CandidateDataSourceDirectRepository 