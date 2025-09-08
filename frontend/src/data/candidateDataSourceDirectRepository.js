import { call } from 'frappe-ui'

const DOCTYPE = 'CandidateDataSource'

// Tận dụng get_list_data từ common.py
export const getDataSourceList = async (filters = {}, page = 1, limit = 20, orderBy = 'modified desc') => {
  try {
    const start = (page - 1) * limit
    
    const response = await call('mbw_mira.api.common.get_list_data', {
      doctype: DOCTYPE,
      filters: filters,
      order_by: orderBy,
      page_length: limit,
      start: start,
              fields: ['name', 'source_name', 'source_type', 'status', 'notes', 'modified']
    })

    return response
  } catch (error) {
    console.error('Error fetching data source list:', error)
    return {
      success: false,
      error: error.message,
      data: [],
      pagination: {
        page: 1, limit: limit, total: 0, pages: 0,
        has_next: false, has_prev: false, showing_from: 0, showing_to: 0
      }
    }
  }
}

// Tận dụng get_form_data từ common.py  
export const getDataSourceFormData = async (id = null) => {
  try {
    const response = await call('mbw_mira.api.common.get_form_data', {
      doctype: DOCTYPE,
      name: id
    })
    return response
  } catch (error) {
    console.error('Error fetching form data:', error)
    return { success: false, error: error.message }
  }
}

// Tận dụng save_doc từ common.py
export const saveDataSource = async (data, id = null) => {
  try {
    const response = await call('mbw_mira.api.common.save_doc', {
      doctype: DOCTYPE,
      data: data,
      name: id
    })
    return response
  } catch (error) {
    console.error('Error saving data source:', error)
    return { success: false, error: error.message }
  }
}

// Tận dụng delete_doc từ common.py
export const deleteDataSource = async (id) => {
  try {
    const response = await call('mbw_mira.api.common.delete_doc', {
      doctype: DOCTYPE,
      name: id
    })
    return response
  } catch (error) {
    console.error(`Error deleting data source ${id}:`, error)
    return { success: false, error: error.message }
  }
}

// Tận dụng get_filter_options từ common.py
export const getDataSourceFilterOptions = async (field) => {
  try {
    const response = await call('mbw_mira.api.common.get_filter_options', {
      doctype: DOCTYPE,
      field: field
    })
    return response
  } catch (error) {
    console.error(`Error fetching filter options for ${field}:`, error)
    return { success: false, options: [] }
  }
}

// Các function đặc biệt cho CandidateDataSource
export const testDataSourceConnection = async (id) => {
  try {
    const response = await call('mbw_mira.mbw_mira.candidatedatasource.candidatedatasource.test_connection', {
      name: id
    })
    return response
  } catch (error) {
    console.error(`Error testing connection for ${id}:`, error)
    return { success: false, error: error.message }
  }
}

export const syncDataSourceData = async (id) => {
  try {
    const response = await call('mbw_mira.mbw_mira.candidatedatasource.candidatedatasource.sync_data', {
      name: id
    })
    return response
  } catch (error) {
    console.error(`Error syncing data for ${id}:`, error)
    return { success: false, error: error.message }
  }
}

export const getDataSourceFieldMeta = async () => {
  try {
    const response = await call('frappe.client.get_meta', {
      doctype: DOCTYPE
    })
    return { success: true, data: response }
  } catch (error) {
    console.error('Error fetching field metadata:', error)
    return { success: false, error: error.message }
  }
} 