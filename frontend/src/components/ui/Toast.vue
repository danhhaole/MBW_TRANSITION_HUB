<template>
  <div class="toast-container">
    <TransitionGroup name="toast" tag="div" class="toast-list">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'toast',
          `toast-${toast.type}`,
          { 'toast-closable': toast.closable }
        ]"
      >
        <div class="toast-content">
          <div class="toast-icon">
            <FeatherIcon v-if="toast.type === 'success'" name="check-circle" class="w-5 h-5" />
            <FeatherIcon v-else-if="toast.type === 'error'" name="x-circle" class="w-5 h-5" />
            <FeatherIcon v-else-if="toast.type === 'warning'" name="alert-triangle" class="w-5 h-5" />
            <FeatherIcon v-else name="info" class="w-5 h-5" />
          </div>
          <div class="toast-message">
            {{ toast.message }}
          </div>
        </div>
        <button
          v-if="toast.closable"
          @click="removeToast(toast.id)"
          class="toast-close"
        >
          <FeatherIcon name="x" class="w-4 h-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { toastState } from '../../composables/useToast'
import { FeatherIcon } from 'frappe-ui'

const toasts = toastState.toasts
const removeToast = toastState.removeToast
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: none;
}

.toast-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 400px;
}

.toast {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  padding: 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  min-width: 320px;
  pointer-events: auto;
  animation: slideIn 0.3s ease-out;
}

.toast-success {
  border-color: #bbf7d0;
  background-color: #f0fdf4;
}

.toast-success .toast-icon {
  color: #16a34a;
}

.toast-error {
  border-color: #fecaca;
  background-color: #fef2f2;
}

.toast-error .toast-icon {
  color: #dc2626;
}

.toast-warning {
  border-color: #fde68a;
  background-color: #fffbeb;
}

.toast-warning .toast-icon {
  color: #d97706;
}

.toast-info {
  border-color: #bfdbfe;
  background-color: #eff6ff;
}

.toast-info .toast-icon {
  color: #2563eb;
}

.toast-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1;
}

.toast-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.toast-message {
  font-size: 14px;
  color: #111827;
  line-height: 1.25;
  word-break: break-word;
}

.toast-close {
  flex-shrink: 0;
  color: #9ca3af;
  padding: 4px;
  margin: -4px;
  border: none;
  background: none;
  cursor: pointer;
  border-radius: 4px;
  transition: color 0.2s;
}

.toast-close:hover {
  color: #4b5563;
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
