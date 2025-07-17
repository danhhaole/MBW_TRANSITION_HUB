import UniversalService from './universalService.js'
import { candidateDataSourceRepository } from '@/repositories/candidateDataSourceRepository.js'

// Service for CandidateDataSource doctype
class CandidateDataSourceService extends UniversalService {
  constructor() {
    super(candidateDataSourceRepository)
  }

  // Validate CandidateDataSource data before save
  validateData(data) {
    const errors = []

    // Required fields validation
    if (!data.source_name?.trim()) {
      errors.push('Source Name is required')
    }

    if (!data.source_type) {
      errors.push('Source Type is required')
    }

    if (!data.auth_method) {
      errors.push('Auth Method is required')
    }

    // Conditional validation based on auth method
    if (data.auth_method === 'OAuth2') {
      if (!data.client_id?.trim()) {
        errors.push('Client ID is required for OAuth2')
      }
      if (!data.client_secret?.trim()) {
        errors.push('Client Secret is required for OAuth2')
      }
    }

    if (data.auth_method === 'API Key') {
      if (!data.api_key?.trim()) {
        errors.push('API Key is required for API Key authentication')
      }
    }

    // URL validation
    if (data.api_base_url && data.api_base_url.trim()) {
      try {
        new URL(data.api_base_url)
      } catch {
        errors.push('Invalid API Base URL format')
      }
    }

    // Sync frequency validation
    if (data.sync_frequency_minutes && (isNaN(data.sync_frequency_minutes) || data.sync_frequency_minutes < 1)) {
      errors.push('Sync frequency must be a positive number')
    }

    return errors
  }

  // Create CandidateDataSource with validation
  async create(data) {
    const errors = this.validateData(data)
    if (errors.length > 0) {
      return {
        success: false,
        error: errors.join(', ')
      }
    }

    return await super.create(data)
  }

  // Update CandidateDataSource with validation
  async update(name, data) {
    const errors = this.validateData(data)
    if (errors.length > 0) {
      return {
        success: false,
        error: errors.join(', ')
      }
    }

    return await super.update(name, data)
  }

  // Test connection for a data source
  async testConnection(name) {
    try {
      // TODO: Implement actual connection test logic
      // For now, just return success
      return {
        success: true,
        message: 'Connection test successful'
      }
    } catch (error) {
      return {
        success: false,
        error: error.message || 'Connection test failed'
      }
    }
  }

  // Sync data from source
  async syncData(name) {
    try {
      // TODO: Implement actual sync logic
      // For now, just return success
      return {
        success: true,
        message: 'Data sync initiated successfully'
      }
    } catch (error) {
      return {
        success: false,
        error: error.message || 'Data sync failed'
      }
    }
  }
}

export const candidateDataSourceService = new CandidateDataSourceService() 