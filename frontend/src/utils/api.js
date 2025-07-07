import { createResource } from 'frappe-ui'

/**
 * Tạo resource với xử lý CSRF token nhất quán
 * @param {Object} config - Configuration cho resource
 * @returns {Object} - Frappe UI resource với CSRF handling
 */
export const createApiResource = (config) => {
  const defaultConfig = {
    auto: false,
    ...config
  }
  
  return createResource(defaultConfig)
}

/**
 * Wrapper function để thực hiện API call với error handling nhất quán
 * @param {Function} apiCall - Function thực hiện API call
 * @param {string} errorMessage - Error message mặc định
 * @returns {Object} - Kết quả API call với format nhất quán
 */
export const executeApiCall = async (apiCall, errorMessage = 'Có lỗi xảy ra') => {
  try {
    const result = await apiCall()
    return {
      success: true,
      data: result,
      message: 'Thành công'
    }
  } catch (error) {
    console.error('API Error:', error)
    
    // Xử lý lỗi CSRF đặc biệt
    if (error.exc_type === 'CSRFTokenError' || error.message?.includes('CSRF')) {
      return {
        success: false,
        error,
        message: 'Lỗi bảo mật. Vui lòng refresh trang và thử lại.',
        needsRefresh: true
      }
    }
    
    return {
      success: false,
      error,
      message: error.messages?.[0] || errorMessage
    }
  }
}

/**
 * API call cho Frappe client methods với retry logic
 * @param {Object} params - Parameters cho API call
 * @returns {Promise} - Promise với kết quả API
 */
export const frappeClientCall = async (params) => {
  const resource = createApiResource({
    url: params.url,
    method: params.method || 'POST'
  })
  
  const executeCall = async () => {
    return await resource.fetch(params.data || {})
  }
  
  return executeApiCall(executeCall, params.errorMessage)
}

/**
 * Retry API call nếu gặp lỗi CSRF
 * @param {Function} apiCall - Function thực hiện API call
 * @param {number} maxRetries - Số lần retry tối đa
 * @returns {Promise} - Promise với kết quả API
 */
export const retryApiCall = async (apiCall, maxRetries = 1) => {
  let lastError = null
  
  for (let i = 0; i <= maxRetries; i++) {
    try {
      const result = await apiCall()
      return result
    } catch (error) {
      lastError = error
      
      // Chỉ retry nếu là lỗi CSRF và còn lần retry
      if ((error.exc_type === 'CSRFTokenError' || error.message?.includes('CSRF')) && i < maxRetries) {
        // Đợi một chút trước khi retry
        await new Promise(resolve => setTimeout(resolve, 500))
        continue
      }
      
      // Throw error nếu không phải CSRF hoặc đã hết lần retry
      throw error
    }
  }
  
  throw lastError
} 