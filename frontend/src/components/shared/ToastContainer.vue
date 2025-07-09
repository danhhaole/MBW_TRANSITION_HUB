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
                      <v-card
              class="toast-card elevation-8"
              :class="`toast-${toast.type}`"
            >
              <v-card-text class="pa-4">
                <div class="d-flex align-center">
                  <v-icon
                    :icon="getToastIcon(toast.type)"
                    :color="getToastIconColor(toast.type)"
                    class="mr-3"
                    size="20"
                  />
                  
                  <div class="flex-grow-1">
                    <p class="mb-0 text-body-2 font-weight-medium toast-text">
                      {{ toast.message }}
                    </p>
                  </div>
                  
                  <v-btn
                    icon="mdi-close"
                    variant="text"
                    size="small"
                    color="grey-darken-1"
                    @click="removeToast(toast.id)"
                    class="ml-2 toast-close-btn"
                  />
                </div>
              </v-card-text>
            
            <!-- Progress bar -->
            <div
              v-if="toast.timeout > 0"
              class="toast-progress"
              :class="`toast-progress-${toast.type}`"
              :style="{ 
                animation: `toast-progress ${toast.timeout}ms linear`
              }"
            />
          </v-card>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useToast } from '@/composables/useToast'

// Composable
const { toasts, removeToast } = useToast()

// Methods
const getToastIcon = (type) => {
  const icons = {
    success: 'mdi-check-circle',
    error: 'mdi-alert-circle',
    warning: 'mdi-alert',
    info: 'mdi-information'
  }
  return icons[type] || 'mdi-information'
}

const getToastIconColor = (type) => {
  const colors = {
    success: 'success',
    error: 'error', 
    warning: 'warning',
    info: 'info'
  }
  return colors[type] || 'info'
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
  border-radius: 12px !important;
  backdrop-filter: blur(10px);
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
  background: #f1f8e9;
  border: 1px solid #4caf50;
  color: #2e7d32;
}

.toast-success .toast-text {
  color: #2e7d32 !important;
}

.toast-success .toast-close-btn {
  color: #2e7d32 !important;
}

.toast-progress-success {
  background: #4caf50;
}

/* Error toast */
.toast-error .toast-card {
  background: #ffebee;
  border: 1px solid #f44336;
  color: #c62828;
}

.toast-error .toast-text {
  color: #c62828 !important;
}

.toast-error .toast-close-btn {
  color: #c62828 !important;
}

.toast-progress-error {
  background: #f44336;
}

/* Warning toast */
.toast-warning .toast-card {
  background: #fff8e1;
  border: 1px solid #ff9800;
  color: #ef6c00;
}

.toast-warning .toast-text {
  color: #ef6c00 !important;
}

.toast-warning .toast-close-btn {
  color: #ef6c00 !important;
}

.toast-progress-warning {
  background: #ff9800;
}

/* Info toast */
.toast-info .toast-card {
  background: #e3f2fd;
  border: 1px solid #2196f3;
  color: #1565c0;
}

.toast-info .toast-text {
  color: #1565c0 !important;
}

.toast-info .toast-close-btn {
  color: #1565c0 !important;
}

.toast-progress-info {
  background: #2196f3;
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