import { call } from 'frappe-ui'

/**
 * Repository for CandidateDataSource API
 */

// Get all active data sources for campaign wizard
export const getDataSources = () => {
  return call('mbw_mira.mbw_mira.candidatedatasource.candidatedatasource.get_data_sources')
}

// Test connection to a data source
export const testConnection = (name) => {
  return call('mbw_mira.mbw_mira.candidatedatasource.candidatedatasource.test_connection', {
    name
  })
}

// Sync data from a data source
export const syncData = (name) => {
  return call('mbw_mira.mbw_mira.candidatedatasource.candidatedatasource.sync_data', {
    name
  })
}

// Named export for service usage
export const candidateDataSourceRepository = {
  getDataSources,
  testConnection,
  syncData
}

// Default export for backward compatibility
export default candidateDataSourceRepository 