import UniversalRepository from './universalRepository.js'

// Repository for CandidateDataSource doctype
class CandidateDataSourceRepository extends UniversalRepository {
  constructor() {
    super('CandidateDataSource')
  }

  // Get list with default fields for CandidateDataSource
  async getList(options = {}) {
    const defaultFields = [
      'name', 'source_name', 'source_type', 'api_base_url', 'auth_method', 
      'status', 'last_sync_at', 'sync_frequency_minutes', 'last_error', 
      'notes', 'created_by', 'is_active', 'modified', 'creation'
    ]
    
    return await super.getList({
      fields: defaultFields,
      ...options
    })
  }

  // Get form data for create/edit with field metadata
  async getFormData(name = null) {
    return await super.getFormData(name)
  }
}

export const candidateDataSourceRepository = new CandidateDataSourceRepository() 