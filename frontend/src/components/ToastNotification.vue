<template>
	<!-- Toast Container - Moved to top right -->
	<div
		id="toast-notification-container"
		class="fixed bottom-5 right-5 flex flex-col gap-2 pointer-events-none z-[9999]"
		style="z-index: 2147483647 !important"
	>
		<!-- Toasts will be inserted here dynamically -->
	</div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'

// Toast configurations
const TOAST_DURATION = 5000 // 5 seconds
const TOAST_ANIMATION_DURATION = 300 // 0.3 seconds

// Toast types and their styles
const TOAST_TYPES = {
	success: {
		bg: 'bg-green-500',
		border: 'border-green-600',
		icon: '✓',
	},
	error: {
		bg: 'bg-red-500',
		border: 'border-red-600',
		icon: '✕',
	},
	warning: {
		bg: 'bg-yellow-500',
		border: 'border-yellow-600',
		icon: '⚠',
	},
	info: {
		bg: 'bg-blue-500',
		border: 'border-blue-600',
		icon: 'i',
	},
}

// Create a unique toast
function createToast(message, type = 'info', options = {}) {
	const container = document.getElementById('toast-notification-container')
	if (!container) return null

	const toastId = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
	const toast = document.createElement('div')
	toast.id = toastId

	const typeConfig = TOAST_TYPES[type] || TOAST_TYPES.info
	const duration = options.duration || TOAST_DURATION

	// Toast styling - Updated animation for top-right position
	toast.className = `
	  ${typeConfig.bg} ${typeConfig.border}
	  text-white p-3 rounded-lg shadow-lg border-l-4
	  pointer-events-auto cursor-pointer transform translate-x-full
	  transition-transform duration-300 ease-out max-w-sm min-w-[250px]
	  relative overflow-hidden
	`

	// Toast content
	toast.innerHTML = `
	  <div class="flex items-start justify-between gap-3">
		<div class="flex items-center gap-2 flex-1">
		  <span class="flex-shrink-0 w-5 h-5 rounded-full bg-white bg-opacity-20 flex items-center justify-center text-xs font-bold">
			${typeConfig.icon}
		  </span>
		  <div class="flex-1 text-sm leading-relaxed">${message}</div>
		</div>
		<button
		  class="flex-shrink-0 ml-2 text-white hover:text-gray-200 transition-colors duration-200 text-lg leading-none"
		  onclick="this.closest('[id^=toast-]').style.transform='translateX(100%)'; setTimeout(() => this.closest('[id^=toast-]').remove(), 300)"
		  aria-label="Close"
		>
		  ×
		</button>
	  </div>
	  <div class="absolute bottom-0 left-0 h-1 bg-white bg-opacity-30 transition-all duration-${duration} ease-linear"
		   style="width: 100%; animation: toast-progress ${duration}ms linear;"></div>
	`

	// Add CSS animation for progress bar if not exists - Updated for top-right
	if (!document.querySelector('#toast-progress-style')) {
		const style = document.createElement('style')
		style.id = 'toast-progress-style'
		style.textContent = `
		@keyframes toast-progress {
		  from { width: 100%; }
		  to { width: 0%; }
		}
		@keyframes toast-slide-in-top {
		  from { transform: translateX(100%); opacity: 0; }
		  to { transform: translateX(0); opacity: 1; }
		}
		@keyframes toast-slide-out-top {
		  from { transform: translateX(0); opacity: 1; }
		  to { transform: translateX(100%); opacity: 0; }
		}
	  `
		document.head.appendChild(style)
	}

	// Insert toast at the beginning (top) of container for top-right positioning
	container.insertBefore(toast, container.firstChild)

	// Animate in
	setTimeout(() => {
		toast.style.transform = 'translateX(0)'
	}, 10)

	// Auto remove after duration
	const timeoutId = setTimeout(() => {
		removeToast(toastId)
	}, duration)

	// Store timeout ID for manual removal
	toast.dataset.timeoutId = timeoutId

	return toastId
}

// Remove toast with animation - Updated for top-right
function removeToast(toastId) {
	const toast = document.getElementById(toastId)
	if (!toast) return

	// Clear timeout if exists
	if (toast.dataset.timeoutId) {
		clearTimeout(parseInt(toast.dataset.timeoutId))
	}

	toast.style.animation = 'toast-slide-out-top 0.3s ease-in'
	setTimeout(() => {
		if (toast.parentNode) {
			toast.remove()
		}
	}, TOAST_ANIMATION_DURATION)
}

// Main toast functions
const toast = {
	success: (message, options = {}) => createToast(message, 'success', options),
	error: (message, options = {}) => createToast(message, 'error', options),
	warning: (message, options = {}) => createToast(message, 'warning', options),
	info: (message, options = {}) => createToast(message, 'info', options),

	// Promise toast for async operations
	promise: (promise, messages, options = {}) => {
		const loadingToastId = createToast(
			messages.loading || 'Loading...',
			'info',
			{ duration: 999999 }, // Very long duration for loading
		)

		return promise
			.then((data) => {
				removeToast(loadingToastId)
				createToast(messages.success || 'Success!', 'success', options)
				return data
			})
			.catch((error) => {
				removeToast(loadingToastId)
				createToast(messages.error || 'Error occurred!', 'error', options)
				throw error
			})
	},

	// Remove specific toast
	remove: (toastId) => removeToast(toastId),

	// Remove all toasts
	removeAll: () => {
		const container = document.getElementById('toast-notification-container')
		if (container) {
			container.innerHTML = ''
		}
	},
}

// Setup global toast object when component mounts
onMounted(() => {
	// Make toast available globally
	window.customToast = toast
	window.toast = toast // Also available as window.toast
})

// Cleanup when component unmounts
onUnmounted(() => {
	// Clean up any remaining toasts
	toast.removeAll()
})

// Export for use in script setup
defineExpose({
	toast,
	success: toast.success,
	error: toast.error,
	warning: toast.warning,
	info: toast.info,
	promise: toast.promise,
	remove: toast.remove,
	removeAll: toast.removeAll,
})
</script>

<style scoped>
/* Toast container positioned at top-right */
#toast-notification-container {
	max-height: 80vh;
	overflow-y: auto;
}

/* Custom scrollbar for toast container */
#toast-notification-container::-webkit-scrollbar {
	width: 4px;
}

#toast-notification-container::-webkit-scrollbar-track {
	background: transparent;
}

#toast-notification-container::-webkit-scrollbar-thumb {
	background: rgba(0, 0, 0, 0.2);
	border-radius: 2px;
}
</style>