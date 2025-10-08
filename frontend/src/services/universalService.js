// Universal service sử dụng repository chung
import {
	candidateSegmentRepository,
	candidateCampaignRepository,
	actionRepository,
	interactionRepository,
	emailLogRepository,
	talentSegmentRepository,
	candidateRepository,
	userRepository,
	candidateDataSourceRepository,
	jobOpeningRepository,
} from '../repositories/universalRepository'
import { call } from 'frappe-ui'

class UniversalService {
	constructor(repository) {
		this.repository = repository
	}

	async getList(options = {}) {
		try {
			const result = await this.repository.getList(options)

			console.log('>>>>>>>>result: ', result)

			// Backend trả về direct response với success flag
			if (result && result.data && result.data.length > 0) {
				return {
					success: true,
					data: result.data || [],
					pagination: result.pagination || {},
				}
			} else {
				return {
					success: false,
					error: result.error || 'Unknown error',
					data: [],
					pagination: {},
				}
			}
		} catch (error) {
			console.error('Service error:', error)
			return {
				success: false,
				error: error.message || 'Network error',
				data: [],
				pagination: {},
			}
		}
	}

	async getFormData(name = null) {
		try {
			const result = await this.repository.getFormData(name)

			console.log('result', result)

			if (result) {
				return {
					success: true,
					data: result || {},
				}
			} else {
				return {
					success: false,
					error: result.error || 'Unknown error',
					data: {},
				}
			}
		} catch (error) {
			console.error('Service error:', error)
			return {
				success: false,
				error: error.message || 'Network error',
				data: {},
			}
		}
	}

	async save(data, name = null) {
		try {
			const result = await this.repository.save(data, name)

			console.log('result', result)

			if (result) {
				return {
					success: true,
					data: result,
					message: 'Saved successfully',
				}
			} else {
				return {
					success: false,
					error: 'Unknown error',
					data: {},
				}
			}
		} catch (error) {
			console.error('Service error:', error)
			return {
				success: false,
				error: error.message || 'Network error',
				data: {},
			}
		}
	}

	async delete(name) {
		try {
			const result = await this.repository.delete(name)

			console.log('result', result)

			return {
				success: true,
				message: 'Deleted successfully',
			}
		} catch (error) {
			console.error('Service error:', error)
			return {
				success: false,
				error: error.message || 'Network error',
			}
		}
	}

	async getFilterOptions(field) {
		try {
			const result = await this.repository.getFilterOptions(field)

			if (result && result.success) {
				return {
					success: true,
					options: result.options || [],
				}
			} else {
				return {
					success: false,
					error: result.error || 'Unknown error',
					options: [],
				}
			}
		} catch (error) {
			console.error('Service error:', error)
			return {
				success: false,
				error: error.message || 'Network error',
				options: [],
			}
		}
	}
}

// Tạo service instances cho tất cả doctype
export const candidateSegmentService = new UniversalService(candidateSegmentRepository)
export const candidateCampaignService = new UniversalService(candidateCampaignRepository)
export const actionService = new UniversalService(actionRepository)
export const interactionService = new UniversalService(interactionRepository)
export const emailLogService = new UniversalService(emailLogRepository)
export const talentSegmentService = new UniversalService(talentSegmentRepository)
export const candidateService = new UniversalService(candidateRepository)
export const userService = new UniversalService(userRepository)
export const candidateDataSourceService = new UniversalService(candidateDataSourceRepository)
export const jobOpeningService = new UniversalService(jobOpeningRepository)

export const getCampaignOptions = async () => {
  const data = await call('frappe.client.get_list', {
    doctype: 'Campaign',
    fields: ['name', 'campaign_name'],
    order_by: 'campaign_name asc',
    limit_page_length: 1000
  })
  return (data || []).map(c => ({ label: c.campaign_name || c.name, value: c.name }))
}

export const getSegmentOptions = async () => {
  const data = await call('frappe.client.get_list', {
    doctype: 'Mira Segment',
    fields: ['name', 'title'],
    limit_page_length: 1000
  })
  return (data || []).map(s => ({ label: s.title || s.name, value: s.name }))
}

export const applicantPoolService = {
  async getList(options = {}) {
    const {
      filters = {},
      or_filters = undefined,
      fields = [
        'name', 'talent_id', 'campaign_id', 'segment_id', 'application_status', 'result', 'score', 'application_date', 'notes'
      ],
      order_by = 'modified desc',
      page_length = 20,
      start = 0
    } = options
    const data = await call('frappe.client.get_list', {
      doctype: 'ApplicantPool',
      filters,
      or_filters,
      fields,
      order_by,
      start,
      page_length
    })
    const total = await call('frappe.client.get_count', {
      doctype: 'ApplicantPool',
      filters
    })
    return {
      data: data || [],
      total: total || 0
    }
  },
  async getFormData(name) {
    return await call('frappe.client.get', {
      doctype: 'ApplicantPool',
      name
    })
  },
  async update(name, data) {
    return await call('frappe.client.set_value', {
      doctype: 'ApplicantPool',
      name,
      fieldname: data
    })
  },
  async delete(name) {
    return await call('frappe.client.delete', {
      doctype: 'ApplicantPool',
      name
    })
  },
}

export default UniversalService

// New service functions for talent segment operations
export const findTalentProfilesBySegment = async (segmentId, minScore = 50) => {
	try {
		const result = await call('mbw_mira.mbw_mira.doctype.mira_segment.mira_segment.find_talentprofile_by_segment', {
			segment_id: segmentId,
			min_score: Number(minScore)
		})
		
		console.log('findTalentProfilesBySegment result:', result)
		
		if (result && Array.isArray(result)) {
			return {
				success: true,
				data: result,
				count: result.length
			}
		} else {
			return {
				success: false,
				error: 'Invalid response format',
				data: [],
				count: 0
			}
		}
	} catch (error) {
		console.error('Error finding talent profiles by segment:', error)
		return {
			success: false,
			error: error.message || 'Network error',
			data: [],
			count: 0
		}
	}
}

export const bulkInsertSegments = async (segmentData) => {
	try {
		// Gửi dữ liệu trực tiếp thay vì wrap trong object data
		const result = await call('mbw_mira.mbw_mira.doctype.talentprofilessegment.talentprofilessegment.bulk_insert_segments', segmentData)
		
		console.log('bulkInsertSegments result:', result)
		
		if (result && result.status === 'completed') {
			return {
				success: true,
				data: result,
				total: result.total,
				results: result.results
			}
		} else {
			return {
				success: false,
				error: result?.message || 'Bulk insert failed',
				data: result,
				total: 0,
				results: []
			}
		}
	} catch (error) {
		console.error('Error bulk inserting segments:', error)
		return {
			success: false,
			error: error.message || 'Network error',
			data: {},
			total: 0,
			results: []
		}
	}
}
