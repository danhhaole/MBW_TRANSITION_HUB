// Universal repository sử dụng hàm chung từ common.py

import { call } from "frappe-ui"

class UniversalRepository {
  constructor(doctype) {
    this.doctype = doctype
  }

  async getList(options = {}) {
    try {
      const params = {
        doctype: this.doctype,
        filters: options.filters || {},
        order_by: options.order_by || 'modified desc',
        page_length: options.page_length || 20,
        start: options.start || 0,
        fields: options.fields || null
      }
      
      const response = await call('mbw_mira.api.common.get_list_data', params)
      
      return response
    } catch (error) {
      console.error(`Error getting list for ${this.doctype}:`, error)
      throw error
    }
  }

  async getFormData(name = null) {
    try {
      const response = await call('mbw_mira.api.common.get_form_data', {
        doctype: this.doctype,
        name
      })
      
      return response
    } catch (error) {
      console.error(`Error getting form data for ${this.doctype}:`, error)
      throw error
    }
  }

  async save(data, name = null) {
    try {
      const response = await call('mbw_mira.api.common.save_doc', {
        doctype: this.doctype,
        data: data,
        name
      })
      
      return response
    } catch (error) {
      console.error(`Error saving ${this.doctype}:`, error)
      throw error
    }
  }

  async delete(name) {
    try {
      const response = await call('mbw_mira.api.common.delete_doc', {
        doctype: this.doctype,
        name
      })
      
      return response
    } catch (error) {
      console.error(`Error deleting ${this.doctype}:`, error)
      throw error
    }
  }

  async getFilterOptions(field) {
    try {
      const response = await call('mbw_mira.api.common.get_filter_options', {
        doctype: this.doctype,
        field
      })
      
      return response
    } catch (error) {
      console.error(`Error getting filter options for ${this.doctype}.${field}:`, error)
      throw error
    }
  }
}

// Tạo instances cho tất cả doctype
export const candidateSegmentRepository = new UniversalRepository('CandidateSegment')
export const candidateCampaignRepository = new UniversalRepository('CandidateCampaign')
export const actionRepository = new UniversalRepository('Action')
export const interactionRepository = new UniversalRepository('Interaction')
export const emailLogRepository = new UniversalRepository('EmailLog')
export const talentSegmentRepository = new UniversalRepository('TalentSegment')
export const candidateRepository = new UniversalRepository('Candidate')
export const campaignRepository = new UniversalRepository('Campaign')
export const campaignStepRepository = new UniversalRepository('CampaignStep')
export const userRepository = new UniversalRepository('User')

export default UniversalRepository
