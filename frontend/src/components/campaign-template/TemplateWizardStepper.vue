<template>
  <div class="bg-gray-50 border-b border-gray-200 px-6 py-4">
    <div class="max-w-4xl mx-auto">
      <div class="flex items-center justify-center">
        <template v-for="(step, index) in steps" :key="step.number">
          <div
            class="flex flex-col items-center min-w-[120px] transition-all duration-300"
            :class="[
              getStepClass(step.number),
              canClickStep(step.number) ? 'cursor-pointer hover:scale-105' : ''
            ]"
            @click="handleStepClick(step.number)"
          >
            <!-- Step Icon/Number -->
            <div
              class="w-10 h-10 rounded-full border-2 flex items-center justify-center font-semibold transition-all duration-300 mb-2"
              :class="getStepIconClass(step.number)"
            >
              <FeatherIcon
                v-if="step.number < currentStep"
                name="check"
                class="h-4 w-4"
              />
              <span v-else-if="step.number === steps.length && currentStep === steps.length">🎉</span>
              <span v-else>{{ step.number }}</span>
            </div>
            
            <!-- Step Label -->
            <span
              class="text-sm font-medium text-center transition-all duration-300"
              :class="getStepLabelClass(step.number)"
            >
              {{ __(step.label) }}
            </span>
            
            <!-- Step Description (optional) -->
            <span
              v-if="step.description"
              class="text-xs text-center mt-1 transition-all duration-300"
              :class="getStepDescriptionClass(step.number)"
            >
              {{ __(step.description) }}
            </span>
          </div>
          
          <!-- Connector Line -->
          <div
            v-if="index < steps.length - 1"
            class="flex-grow h-0.5 mx-4 transition-all duration-400"
            :class="step.number < currentStep ? 'bg-blue-500' : 'bg-gray-300'"
          ></div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  steps: {
    type: Array,
    required: true,
    validator: (steps) => {
      return steps.every(step => 
        typeof step.number === 'number' && 
        typeof step.label === 'string'
      )
    }
  },
  currentStep: {
    type: Number,
    required: true
  }
})

// Emits
const emit = defineEmits(['step-click'])

// Translation helper
const __ = (text) => text

// Step styling functions
const getStepClass = (stepNumber) => {
  return stepNumber === props.currentStep ? 'scale-105' : ''
}

const getStepIconClass = (stepNumber) => {
  if (stepNumber < props.currentStep) {
    // Completed step - clickable
    return 'bg-blue-500 border-blue-500 text-white hover:bg-blue-600'
  } else if (stepNumber === props.currentStep) {
    // Current step - clickable
    return 'bg-blue-100 border-blue-500 text-blue-600 hover:bg-blue-200'
  } else {
    // Future step - not clickable
    return 'bg-gray-100 border-gray-300 text-gray-400'
  }
}

const getStepLabelClass = (stepNumber) => {
  if (stepNumber < props.currentStep) {
    // Completed step
    return 'text-blue-600'
  } else if (stepNumber === props.currentStep) {
    // Current step
    return 'text-blue-700 font-semibold'
  } else {
    // Future step
    return 'text-gray-500'
  }
}

const getStepDescriptionClass = (stepNumber) => {
  if (stepNumber < props.currentStep) {
    // Completed step
    return 'text-blue-500'
  } else if (stepNumber === props.currentStep) {
    // Current step
    return 'text-blue-600'
  } else {
    // Future step
    return 'text-gray-400'
  }
}

// Check if step can be clicked (completed steps or current step)
const canClickStep = (stepNumber) => {
  return stepNumber <= props.currentStep
}

// Handle step click
const handleStepClick = (stepNumber) => {
  if (canClickStep(stepNumber)) {
    emit('step-click', stepNumber)
  }
}
</script>

<style scoped>
/* Add smooth transitions for step animations */
.transition-all {
  transition: all 0.3s ease-in-out;
}

/* Hover effects for better UX */
.flex.flex-col.items-center:hover {
  transform: translateY(-1px);
}
</style>
