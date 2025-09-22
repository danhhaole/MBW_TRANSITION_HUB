import { inject } from 'vue'

/**
 * Composable để sử dụng toast notifications
 * Cung cấp các method tiện lợi để hiển thị thông báo
 */
export function useToast() {
	// Fallback toast object nếu chưa được setup
	const fallbackToast = {
		success: (message) => console.log('Toast Success:', message),
		error: (message) => console.error('Toast Error:', message),
		warning: (message) => console.warn('Toast Warning:', message),
		info: (message) => console.info('Toast Info:', message),
		promise: (promise, messages) => promise,
		remove: () => { },
		removeAll: () => { }
	}

	// Lấy toast từ window hoặc sử dụng fallback
	const toast = window.customToast || window.toast || fallbackToast

	return {
		// Basic toast methods
		success: (message, options) => toast.success(message, options),
		error: (message, options) => toast.error(message, options),
		warning: (message, options) => toast.warning(message, options),
		info: (message, options) => toast.info(message, options),

		// Promise toast for async operations
		promise: (promise, messages, options) => toast.promise(promise, messages, options),

		// Utility methods
		remove: (toastId) => toast.remove(toastId),
		removeAll: () => toast.removeAll(),

		// Convenience methods với các message patterns thường dùng
		showSuccess: (action = 'Operation') => toast.success(`${action} ${__('completed successfully')}`),
		showError: (action = 'Operation', error = 'Unknown error') => {
			const errorMessage = typeof error === 'string' ? error : error.message || 'Unknown error'
			toast.error(`${action} failed: ${errorMessage}`)
		},
		showLoading: (message = 'Loading...') => toast.info(message, { duration: 999999 }),

		// CRUD operation helpers
		showCreateSuccess: (itemName = 'Item') => toast.success(`${itemName} ${__('created successfully')}`),
		showUpdateSuccess: (itemName = 'Item') => toast.success(`${itemName} ${__('updated successfully')}`),
		showDeleteSuccess: (itemName = 'Item') => toast.success(`${itemName} ${__('deleted successfully')}`),
		showLoadSuccess: (itemName = 'Data') => toast.success(`${itemName} ${__('loaded successfully')}`),

		showCreateError: (itemName = 'Item', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toast.error(`${__('Failed to create')} ${itemName}: ${errorMessage}`)
		},
		showUpdateError: (itemName = 'Item', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toast.error(`${__('Failed to update')} ${itemName}: ${errorMessage}`)
		},
		showDeleteError: (itemName = 'Item', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toast.error(`${__('Failed to delete')} ${itemName}: ${errorMessage}`)
		},
		showLoadError: (itemName = 'Data', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Unknown error'
			toast.error(`${__('Failed to load')} ${itemName}: ${errorMessage}`)
		},

		// API operation helpers
		showApiSuccess: (operation = 'API call') => toast.success(`${operation} ${__('completed successfully')}`),
		showApiError: (operation = 'API call', error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'API error'
			toast.error(`${operation} failed: ${errorMessage}`)
		},

		// Validation helpers
		showValidationError: (message = 'Please check your input') => toast.warning(message),
		showPermissionError: (action = 'perform this action') => {
			toast.error(`${__('You don have permission to')} ${action}`)
		},

		// Network helpers
		showNetworkError: () => toast.error(__('Network error. Please check your connection')),
		showTimeoutError: () => toast.error(__('Request timed out. Please try again')),

		// Form helpers
		showFormError: (fieldName) => toast.error(`Please check the ${fieldName} field`),
		showFormSuccess: (formName = 'Form') => toast.success(`${formName} ${__('submitted successfully')}`),

		// File operation helpers
		showFileUploadSuccess: (fileName) => toast.success(`File "${fileName}" ${__('uploaded successfully')}`),
		showFileUploadError: (fileName, error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Upload failed'
			toast.error(`${__('Failed to upload')} "${fileName}": ${errorMessage}`)
		},

		// Authentication helpers
		showLoginSuccess: () => toast.success(__('Logged in successfully')),
		showLogoutSuccess: () => toast.success(__('Logged out successfully')),
		showAuthError: () => toast.error(__('Authentication failed. Please try again')),

		// Settings helpers
		showSettingsSaved: () => toast.success(__('Settings saved successfully')),
		showSettingsError: (error) => {
			const errorMessage = typeof error === 'string' ? error : error?.message || 'Settings error'
			toast.error(`${__('Failed to save settings')}: ${errorMessage}`)
		}
	}
}

// Export default
export default useToast
