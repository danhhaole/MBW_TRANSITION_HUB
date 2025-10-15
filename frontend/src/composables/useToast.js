import { reactive } from 'vue'

// Global toast state
const toastState = reactive({
  toasts: [],
  
  addToast(toast) {
    const id = Date.now() + Math.random()
    const newToast = {
      id,
      type: 'info',
      message: '',
      closable: true,
      duration: 5000,
      ...toast
    }
    
    this.toasts.push(newToast)
    
    // Auto remove after duration
    if (newToast.duration > 0) {
      setTimeout(() => {
        this.removeToast(id)
      }, newToast.duration)
    }
    
    return id
  },
  
  removeToast(id) {
    const index = this.toasts.findIndex(t => t.id === id)
    if (index > -1) {
      this.toasts.splice(index, 1)
    }
  },
  
  removeAll() {
    this.toasts.splice(0)
  }
})

/**
 * Custom toast notifications system
 * Cung cấp các method tiện lợi để hiển thị thông báo
 */
export function useToast() {
	return {
		// Basic toast methods
		success: (message, options = {}) => toastState.addToast({ type: 'success', message, ...options }),
		error: (message, options = {}) => toastState.addToast({ type: 'error', message, ...options }),
		warning: (message, options = {}) => toastState.addToast({ type: 'warning', message, ...options }),
		info: (message, options = {}) => toastState.addToast({ type: 'info', message, ...options }),

		// Utility methods
		remove: (toastId) => toastState.removeToast(toastId),
		removeAll: () => toastState.removeAll(),

		// Convenience methods với các message patterns thường dùng
		showSuccess: (action = 'Operation') => toastState.addToast({ type: 'success', message: `${action} completed successfully` }),
		showError: (action = 'Operation', error = 'Unknown error') => {
			const errorMessage = typeof error === 'string' ? error : error.message || 'Unknown error'
			toastState.addToast({ type: 'error', message: `${action} failed: ${errorMessage}` })
		},
		showLoading: (message = 'Loading...') => toastState.addToast({ type: 'info', message, duration: 0 }),

		// CRUD operation helpers
		showCreateSuccess: (itemName = 'Item') => toastState.addToast({ type: 'success', message: `${itemName} created successfully` }),
		showUpdateSuccess: (itemName = 'Item') => toastState.addToast({ type: 'success', message: `${itemName} updated successfully` }),
		showDeleteSuccess: (itemName = 'Item') => toastState.addToast({ type: 'success', message: `${itemName} deleted successfully` }),
		showLoadSuccess: (itemName = 'Data') => toastState.addToast({ type: 'success', message: `${itemName} loaded successfully` }),

		showCreateError: (itemName = 'Item', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toastState.addToast({ type: 'error', message: `Failed to create ${itemName}: ${errorMessage}` })
		},
		showUpdateError: (itemName = 'Item', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toastState.addToast({ type: 'error', message: `Failed to update ${itemName}: ${errorMessage}` })
		},
		showDeleteError: (itemName = 'Item', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toastState.addToast({ type: 'error', message: `Failed to delete ${itemName}: ${errorMessage}` })
		},
		showLoadError: (itemName = 'Data', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toastState.addToast({ type: 'error', message: `Failed to load ${itemName}: ${errorMessage}` })
		},

		// API operation helpers
		showApiSuccess: (operation = 'API call') => toastState.addToast({ type: 'success', message: `${operation} completed successfully` }),
		showApiError: (operation = 'API call', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'API error'
			toastState.addToast({ type: 'error', message: `${operation} failed: ${errorMessage}` })
		},

		// Validation helpers
		showValidationError: (message = 'Please check your input') => toastState.addToast({ type: 'warning', message }),
		showPermissionError: (action = 'perform this action') => {
			toastState.addToast({ type: 'error', message: `You don't have permission to ${action}` })
		},

		// Network helpers
		showNetworkError: () => toastState.addToast({ type: 'error', message: 'Network error. Please check your connection' }),
		showTimeoutError: () => toastState.addToast({ type: 'error', message: 'Request timed out. Please try again' }),

		// Form helpers
		showFormError: (fieldName) => toastState.addToast({ type: 'error', message: `Please check the ${fieldName} field` }),
		showFormSuccess: (formName = 'Form') => toastState.addToast({ type: 'success', message: `${formName} submitted successfully` }),

		// File operation helpers
		showFileUploadSuccess: (fileName) => toastState.addToast({ type: 'success', message: `File "${fileName}" uploaded successfully` }),
		showFileUploadError: (fileName, error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Upload failed'
			toastState.addToast({ type: 'error', message: `Failed to upload "${fileName}": ${errorMessage}` })
		},

		// Authentication helpers
		showLoginSuccess: () => toastState.addToast({ type: 'success', message: 'Logged in successfully' }),
		showLogoutSuccess: () => toastState.addToast({ type: 'success', message: 'Logged out successfully' }),
		showAuthError: () => toastState.addToast({ type: 'error', message: 'Authentication failed. Please try again' }),

		// Settings helpers
		showSettingsSaved: () => toastState.addToast({ type: 'success', message: 'Settings saved successfully' }),
		showSettingsError: (error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Settings error'
			toastState.addToast({ type: 'error', message: `Failed to save settings: ${errorMessage}` })
		}
	}
}

// Export toast state for components
export { toastState }

// Export default
export default useToast
