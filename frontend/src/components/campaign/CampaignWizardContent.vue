<template>
  <div class="flex-1 overflow-auto">
    <div class="max-w-4xl mx-auto p-6">
      <!-- Step Content with smooth transitions -->
      <div class="min-h-[500px]">
        <transition name="step-fade" mode="out-in">
          <div :key="currentStep" class="animate-fadeIn">
            <slot :current-step="currentStep" />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
// Props
const props = defineProps({
  currentStep: {
    type: Number,
    required: true
  }
})
</script>

<style scoped>
/* Fade animation for step transitions */
.step-fade-enter-active,
.step-fade-leave-active {
  transition: opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
}

.step-fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.step-fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Fade in animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.4s ease-out;
}

/* Custom scrollbar for better UX */
.overflow-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
