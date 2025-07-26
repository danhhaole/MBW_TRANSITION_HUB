// Universal repository sử dụng hàm chung từ common.py

import { call } from "frappe-ui"

class UniversalRepository {
  constructor(doctype) {
    this.doctype = doctype
  }

  /**
   * getList(options)
   * options:
   *   - filters: object (chỉ truyền các field thực sự tồn tại trong doctype)
   *   - or_filters: mảng các điều kiện OR, ví dụ: [[field, operator, value], ...]
   *   - fields, order_by, group_by, start, page_length: như Frappe doc
   * Lưu ý: Không truyền field lạ vào filters, không nhét search_text vào filters!
   */
  async getList(options = {}) {
    try {
      const {
        filters = {},
        or_filters = {},
        fields = null,
        order_by = 'modified desc',
        group_by = '',
        page_length = 20,
        start = 0
      } = options

      const data = await call('frappe.client.get_list', {
        doctype: this.doctype,
        filters,
        or_filters,
        fields,
        order_by,
        group_by,
        limit_start: start,
        limit_page_length: page_length
      })
      // Lấy tổng số bản ghi cho phân trang
      const total = await call('frappe.client.get_count', {
        doctype: this.doctype,
        filters
      })

      return {
        data: data || [],
        pagination: {
          total: total || 0,
          page: Math.floor(start / page_length) + 1,
          limit: page_length,
          pages: Math.ceil((total || 0) / page_length),
          has_next: (start + page_length) < total,
          has_prev: start > 0,
          showing_from: start + 1,
          showing_to: Math.min(start + page_length, total)
        }
      }
    } catch (error) {
      console.error(`Error getting list for ${this.doctype}:`, error)
      throw error
    }
  }

  async getFormData(name = null) {
    try {
      return await call('frappe.client.get', {
        doctype: this.doctype,
        name
      })
    } catch (error) {
      console.error(`Error getting form data for ${this.doctype}:`, error)
      throw error
    }
  }

  async save(data, name = null) {
    try {
      if (name) {
        // Nếu data là object nhiều field thì truyền fieldname là object
        // Nếu chỉ update 1 field thì truyền fieldname là string, value là giá trị
        let setValueParams = {
          doctype: this.doctype,
          name
        }
        if (typeof data === 'object' && !Array.isArray(data)) {
          setValueParams.fieldname = data
        } else {
          // Nếu data là [fieldname, value]
          setValueParams.fieldname = data[0]
          setValueParams.value = data[1]
        }
        return await call('frappe.client.set_value', setValueParams)
      } else {
        // create
        return await call('frappe.client.insert', {
          doc: {
            doctype: this.doctype,
            ...data
          }
        })
      }
    } catch (error) {
      console.error(`Error saving ${this.doctype}:`, error)
      throw error
    }
  }

  async delete(name) {
    try {
      return await call('frappe.client.delete', {
        doctype: this.doctype,
        name
      })
    } catch (error) {
      console.error(`Error deleting ${this.doctype}:`, error)
      throw error
    }
  }

  async getFilterOptions(field) {
    try {
      return await call('frappe.client.get_list', {
        doctype: this.doctype,
        fields: [field],
        distinct: true
      })
    } catch (error) {
      console.error(`Error getting filter options for ${this.doctype}.${field}:`, error)
      throw error
    }
  }
}

// Tạo instances cho tất cả doctype
export const candidateSegmentRepository = new UniversalRepository('TalentProfilesSegment')
export const candidateCampaignRepository = new UniversalRepository('TalentProfilesCampaign')
export const actionRepository = new UniversalRepository('Action')
export const interactionRepository = new UniversalRepository('Interaction')
export const emailLogRepository = new UniversalRepository('EmailLog')
export const talentSegmentRepository = new UniversalRepository('TalentSegment')
export const candidateRepository = new UniversalRepository('TalentProfiles')
export const campaignRepository = new UniversalRepository('Campaign')
export const campaignStepRepository = new UniversalRepository('CampaignStep')
export const userRepository = new UniversalRepository('User')
export const candidateDataSourceRepository = new UniversalRepository('CandidateDataSource')

export default UniversalRepository
