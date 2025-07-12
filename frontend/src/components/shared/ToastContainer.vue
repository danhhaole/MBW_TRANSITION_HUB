<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast" tag="div">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'toast-item',
            `toast-${toast.type}`,
            { 'toast-visible': toast.visible }
          ]"
        >
          <div
            class="toast-card shadow-lg"
            :class="`toast-${toast.type}`"
          >
            <div class="p-4">
              <div class="flex items-center">
                <div
                  v-html="getToastIcon(toast.type)"
                  :class="[
                    'w-5 h-5 mr-3 flex-shrink-0',
                    getToastIconColor(toast.type)
                  ]"
                />
                
                <div class="flex-grow">
                  <p class="mb-0 text-sm font-medium toast-text">
                    {{ toast.message }}
                  </p>
                </div>
                
                <button
                  @click="removeToast(toast.id)"
                  class="ml-2 toast-close-btn p-1 rounded-full hover:bg-black hover:bg-opacity-10 transition-colors duration-200"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          
            <!-- Progress bar -->
            <div
              v-if="toast.timeout > 0"
              class="toast-progress"
              :class="`toast-progress-${toast.type}`"
              :style="{ 
                animation: `toast-progress ${toast.timeout}ms linear`
              }"
            />
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

// Composable
const { toasts, removeToast } = useToast()

// Icon SVG strings
const icons = {
  success: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
  </svg>`,
  
  error: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
  </svg>`,
  
  warning: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
  </svg>`,
  
  info: `<svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
  </svg>`
}

// Methods
const getToastIcon = (type) => {
  return icons[type] || icons.info
}

const getToastIconColor = (type) => {
  const colors = {
    success: 'text-green-600',
    error: 'text-red-600', 
    warning: 'text-orange-600',
    info: 'text-blue-600'
  }
  return colors[type] || 'text-blue-600'
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
  max-width: 400px;
  width: 100%;
  pointer-events: none;
}

@media (max-width: 768px) {
  .toast-container {
    top: 16px;
    right: 16px;
    left: 16px;
    max-width: none;
  }
}

.toast-item {
  pointer-events: all;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}

.toast-card {
  @apply rounded-xl backdrop-blur-sm border;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.toast-progress {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  width: 100%;
  opacity: 0.7;
}

/* Animations */
@keyframes toast-progress {
  from {
    width: 100%;
  }
  to {
    width: 0%;
  }
}

.toast-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.95);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.95);
}

.toast-move {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Toast styles with better contrast */
.toast-success .toast-card {
  @apply bg-green-50 border-green-200 text-green-800;
}

.toast-success .toast-text {
  @apply text-green-800;
}

.toast-success .toast-close-btn {
  @apply text-green-800 hover:bg-green-100;
}

.toast-progress-success {
  @apply bg-green-500;
}

/* Error toast */
.toast-error .toast-card {
  @apply bg-red-50 border-red-200 text-red-800;
}

.toast-error .toast-text {
  @apply text-red-800;
}

.toast-error .toast-close-btn {
  @apply text-red-800 hover:bg-red-100;
}

.toast-progress-error {
  @apply bg-red-500;
}

/* Warning toast */
.toast-warning .toast-card {
  @apply bg-orange-50 border-orange-200 text-orange-800;
}

.toast-warning .toast-text {
  @apply text-orange-800;
}

.toast-warning .toast-close-btn {
  @apply text-orange-800 hover:bg-orange-100;
}

.toast-progress-warning {
  @apply bg-orange-500;
}

/* Info toast */
.toast-info .toast-card {
  @apply bg-blue-50 border-blue-200 text-blue-800;
}

.toast-info .toast-text {
  @apply text-blue-800;
}

.toast-info .toast-close-btn {
  @apply text-blue-800 hover:bg-blue-100;
}

.toast-progress-info {
  @apply bg-blue-500;
}

/* Hover effects */
.toast-item:hover .toast-card {
  transform: translateY(-2px);
  transition: transform 0.2s ease;
}

.toast-item:hover .toast-progress {
  animation-play-state: paused;
}
</style> 