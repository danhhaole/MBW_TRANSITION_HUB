import { ref } from 'vue'

/**
 * Composable để xử lý errors nhất quán
 * @returns {Object} - Object chứa error state và methods
 */
export function useErrorHandler() {
  const error = ref({})
  const showError = ref(false)
  
  /**
   * Hiển thị error với thông tin chi tiết
   * @param {Object} errorData - Error data từ API call
   */
  const handleError = (errorData) => {
    if (!errorData || errorData.success) return
    
    error.value = {
      message: errorData.message || 'Có lỗi xảy ra',
      needsRefresh: errorData.needsRefresh || false,
      error: errorData.error
    }
    showError.value = true
    
    // Log error for debugging
    console.error('Error handled:', errorData)
  }
  
  /**
   * Xóa error hiện tại
   */
  const clearError = () => {
    error.value = {}
    showError.value = false
  }
  
  /**
   * Xử lý CSRF error đặc biệt
   * @param {Object} errorData - CSRF error data
   */
  const handleCSRFError = (errorData) => {
    error.value = {
      message: 'Phiên đăng nhập đã hết hạn. Vui lòng refresh trang và thử lại.',
      needsRefresh: true,
      error: errorData.error
    }
    showError.value = true
  }
  
  /**
   * Wrapper để thực hiện API call với auto error handling
   * @param {Function} apiCall - Async function to execute
   * @param {Object} options - Options cho error handling
   * @returns {Promise} - Promise với kết quả hoặc error
   */
  const executeWithErrorHandling = async (apiCall, options = {}) => {
    const { showErrorToast = true, customErrorMessage } = options
    
    try {
      const result = await apiCall()
      
      // Nếu result có success flag và bằng false
      if (result && typeof result === 'object' && result.success === false) {
        if (showErrorToast) {
          if (customErrorMessage) {
            handleError({ message: customErrorMessage })
          } else {
            handleError(result)
          }
        }
        return result
      }
      
      return result
    } catch (err) {
      const errorData = {
        message: customErrorMessage || err.message || 'Có lỗi xảy ra',
        needsRefresh: err.exc_type === 'CSRFTokenError' || err.message?.includes('CSRF'),
        error: err
      }
      
      if (showErrorToast) {
        handleError(errorData)
      }
      
      throw errorData
    }
  }
  
  return {
    error,
    showError,
    handleError,
    clearError,
    handleCSRFError,
    executeWithErrorHandling
  }
} 