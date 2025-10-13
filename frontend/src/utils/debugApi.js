import { call } from 'frappe-ui'

export const debugApiCall = async (method, params) => {
  console.log('🔍 Debug API Call:', { method, params })
  
  try {
    console.log('📡 Making API call...')
    const response = await call(method, params)
    
    console.log('✅ API Response received:', {
      response,
      type: typeof response,
      keys: response ? Object.keys(response) : null,
      hasName: response?.name ? true : false,
      hasExcType: response?.exc_type ? true : false
    })
    
    return response
  } catch (error) {
    console.error('❌ API Call Error:', {
      error,
      message: error?.message,
      stack: error?.stack,
      response: error?.response,
      status: error?.status,
      hasExcType: error?.exc_type ? true : false
    })
    
    throw error
  }
}

export const testFrappeConnection = async () => {
  try {
    console.log('🧪 Testing Frappe connection...')
    
    // Test 1: Get current user
    const user = await debugApiCall('frappe.auth.get_logged_user')
    console.log('👤 Current user:', user)
    
    // Test 2: Get system settings
    const settings = await debugApiCall('frappe.client.get_list', {
      doctype: 'System Settings',
      limit_page_length: 1
    })
    console.log('⚙️ System settings test:', settings)
    
    // Test 3: Try to get campaigns
    const campaigns = await debugApiCall('frappe.client.get_list', {
      doctype: 'Mira Campaign',
      limit_page_length: 1
    })
    console.log('📋 Campaigns test:', campaigns)
    
    return true
  } catch (error) {
    console.error('❌ Frappe connection test failed:', error)
    return false
  }
}
