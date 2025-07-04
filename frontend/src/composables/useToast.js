import { ref } from 'vue'

// Global toast state
const toasts = ref([])
let toastId = 0

export const useToast = () => {
  // Show toast notification
  const showToast = (message, type = 'info', timeout = 4000) => {
    const id = ++toastId
    const toast = {
      id,
      message,
      type,
      visible: true
    }
    
    toasts.value.push(toast)
    
    // Auto remove after timeout
    if (timeout > 0) {
      setTimeout(() => {
        removeToast(id)
      }, timeout)
    }
    
    return id
  }

  // Remove specific toast
  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  // Clear all toasts
  const clearToasts = () => {
    toasts.value = []
  }

  // Shorthand methods
  const showSuccess = (message, timeout = 3000) => showToast(message, 'success', timeout)
  const showError = (message, timeout = 5000) => showToast(message, 'error', timeout)
  const showWarning = (message, timeout = 4000) => showToast(message, 'warning', timeout)
  const showInfo = (message, timeout = 4000) => showToast(message, 'info', timeout)

  return {
    toasts,
    showToast,
    removeToast,
    clearToasts,
    showSuccess,
    showError,
    showWarning,
    showInfo
  }
} 