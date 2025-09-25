import { call } from 'frappe-ui'

/**
 * Repository for CandidateDataSource API
 */

// Get all active data sources for campaign wizard
export const getDataSources = async () => {
  try {
    const data = await call('frappe.client.get_list', {
      doctype: 'CandidateDataSource',
      fields: [
        'name',
        'source_name',
        'source_title',
        'notes',
        'source_type',
        'is_active'
      ],
      filters: { is_active: 1 },
      order_by: 'modified desc',
      limit_page_length: 200
    })

    return {
      success: true,
      data_sources: Array.isArray(data) ? data : []
    }
  } catch (error) {
    console.error('Error fetching CandidateDataSource list:', error)
    return { success: false, error: error?.message || 'Failed to load data sources' }
  }
}

// Test connection to a data source (not implemented server-side yet)
export const testConnection = async (name) => {
  console.warn('testConnection not implemented for CandidateDataSource. name=', name)
  return { success: false, message: 'Not implemented' }
}

// Sync data from a data source (not implemented server-side yet)
export const syncData = async (name) => {
  console.warn('syncData not implemented for CandidateDataSource. name=', name)
  return { success: false, message: 'Not implemented' }
}

// Named export for service usage
export const candidateDataSourceRepository = {
  getDataSources,
  testConnection,
  syncData
}

// Default export for backward compatibility
export default candidateDataSourceRepository 