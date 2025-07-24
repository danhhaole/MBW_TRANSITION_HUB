// Universal service sử dụng repository chung
import {
	candidateSegmentRepository,
	candidateCampaignRepository,
	actionRepository,
	interactionRepository,
	emailLogRepository,
	talentSegmentRepository,
	candidateRepository,
	campaignRepository,
	campaignStepRepository,
	userRepository,
	candidateDataSourceRepository,
} from '../repositories/universalRepository'

class UniversalService {
	constructor(repository) {
		this.repository = repository
	}

	async getList(options = {}) {
		try {
			const result = await this.repository.getList(options)

			console.log('result', result)

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
export const campaignService = new UniversalService(campaignRepository)
export const campaignStepService = new UniversalService(campaignStepRepository)
export const userService = new UniversalService(userRepository)
export const candidateDataSourceService = new UniversalService(candidateDataSourceRepository)

export default UniversalService
