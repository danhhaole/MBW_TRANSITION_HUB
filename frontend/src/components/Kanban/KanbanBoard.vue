<template>
    <div class="kanban-board h-full">
      <!-- Stage Summary Bar -->
      <!-- <div class="stage-summary">
        <div class="flex items-center gap-6 overflow-x-auto p-4">
          <template v-if="isLoading">
            <div v-for="n in 4" :key="n" class="stage-summary-skeleton">
              <div class="w-3 h-3 bg-gray-200 rounded-full animate-pulse"></div>
              <div class="space-y-1">
                <div class="w-24 h-4 bg-gray-200 rounded animate-pulse"></div>
                <div class="w-16 h-3 bg-gray-200 rounded animate-pulse"></div>
              </div>
              <div class="w-8 h-6 bg-gray-200 rounded animate-pulse"></div>
            </div>
          </template>
          
          <template v-else>
            <div 
              v-for="stageSummary in stageSummaries" 
              :key="stageSummary.stage_name"
              class="stage-summary-item"
            >
              <div 
                class="w-3 h-3 rounded-full" 
                :style="{ backgroundColor: stageSummary.color }"
              ></div>
              <div class="flex flex-col">
                <span class="text-sm font-semibold text-gray-900">
                  {{ stageSummary.stage_name }}
                </span>
                <span class="text-xs text-gray-500">
                  {{ stageSummary.step_count }} {{ __('steps') }}
                </span>
              </div>
              <div class="ml-3 px-2 py-1 bg-gray-100 rounded-md">
                <span class="text-sm font-bold text-gray-700">
                  {{ stageSummary.candidate_count }}
                </span>
              </div>
            </div>
          </template>
        </div>
      </div> -->
  
      <!-- Kanban Columns Container -->
      <div 
        class="kanban-container"
        ref="kanbanBoard"
        @mousedown="startPan"
        @mousemove="handlePan"
        @mouseup="endPan"
        @mouseleave="endPan"
        @wheel="handleWheel"
        :class="{ 'cursor-grabbing': isPanning, 'cursor-grab': !isPanning }"
      >
        <div 
          class="kanban-scroll-area"
          :style="{ 
            transform: `translateX(${translateX}px)`,
            width: `${containerWidth}px`
          }"
          ref="kanbanContainer"
        >
          <template v-if="isLoading">
            <div v-for="n in 5" :key="n" class="kanban-column-wrapper">
              <KanbanColumn :is-loading="true" />
            </div>
          </template>
          
          <template v-else>
            <div 
              v-for="step in stepColumns" 
              :key="step.step_key"
              class="kanban-column-wrapper"
            >
              <KanbanColumn
                :step="step"
                :candidates="getStepCandidates(step.step_key)"
                :available-steps="stepColumns"
                @add-candidate="$emit('addCandidateToStep', step)"
                @view-candidate="$emit('viewCandidate', $event)"
                @edit-candidate="$emit('editCandidate', $event)"
                @view-cv="$emit('viewCV', $event)"
                @send-email="$emit('sendEmail', $event)"
                @schedule-interview="$emit('scheduleInterview', $event)"
                @candidate-moved="handleCandidateMove"
                @step-action="handleStepAction"
                @move-to-step="handleMoveToStep"
              />
            </div>
          </template>
        </div>
      </div>
  
      <!-- Scroll Indicator -->
      <div v-if="showScrollIndicator" class="scroll-indicator">
        <div class="flex items-center gap-2 bg-black bg-opacity-75 text-white text-xs px-3 py-2 rounded-lg">
          <FeatherIcon name="move" class="h-3 w-3" />
          <span>{{ __('Drag to scroll horizontally') }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
  import { FeatherIcon } from 'frappe-ui'
  import KanbanColumn from './KanbanColumn.vue'
  
  // Props
  const props = defineProps({
    stepColumns: { type: Array, default: () => [] },
    stageSummaries: { type: Array, default: () => [] },
    candidates: { type: Array, default: () => [] },
    isLoading: { type: Boolean, default: false }
  })
  
  // Emits
  const emit = defineEmits([
    'addCandidateToStep',
    'viewCandidate', 
    'editCandidate',
    'viewCV',
    'sendEmail',
    'scheduleInterview',
    'candidateMoved',
    'stepAction',
    'moveToStep'
  ])
  
  // Reactive state
  const isPanning = ref(false)
  const startX = ref(0)
  const startTranslateX = ref(0)
  const translateX = ref(0)
  const containerWidth = ref(0)
  const kanbanBoard = ref(null)
  const kanbanContainer = ref(null)
  const showScrollIndicator = ref(false)
  const scrollIndicatorTimeout = ref(null)
  
  // Pan variables
  const panVelocity = ref(0)
  const lastPanX = ref(0)
  const panTimeStamp = ref(0)
  const animationFrameId = ref(null)
  const isAnimating = ref(false)
  
  // Helper functions
  const getStepCandidates = (stepKey) => {
    // console.log(stepKey,props.candidates)
    return props.candidates.filter(candidate => 
      candidate.step_id === stepKey 
      // ||
      // candidate.recruitment_step === stepKey
    )
  }
  
  const calculateContainerWidth = () => {
    if (!props.stepColumns || props.stepColumns.length === 0) return
    
    const columnWidth = 320
    const gap = 16
    const padding = 32
    
    containerWidth.value = (props.stepColumns.length * columnWidth) + 
                          ((props.stepColumns.length - 1) * gap) + 
                          padding
  }
  
  // Pan functionality
  const startPan = (event) => {
    if (event.target.closest('.kanban-column-content') || 
        event.target.closest('.dropdown') || 
        event.target.closest('button')) {
      return
    }
    
    isPanning.value = true
    startX.value = event.clientX
    startTranslateX.value = translateX.value
    lastPanX.value = event.clientX
    panTimeStamp.value = performance.now()
    panVelocity.value = 0
    
    if (animationFrameId.value) {
      cancelAnimationFrame(animationFrameId.value)
      animationFrameId.value = null
      isAnimating.value = false
    }
    
    showScrollIndicator.value = true
    clearTimeout(scrollIndicatorTimeout.value)
    
    if (kanbanContainer.value) {
      kanbanContainer.value.classList.add('panning')
    }
  }
  
  const handlePan = (event) => {
    if (!isPanning.value) return
    
    event.preventDefault()
    
    const currentTime = performance.now()
    const deltaX = event.clientX - startX.value
    const newTranslateX = startTranslateX.value + deltaX
    
    const timeDiff = currentTime - panTimeStamp.value
    if (timeDiff > 0) {
      panVelocity.value = (event.clientX - lastPanX.value) / timeDiff
    }
    
    lastPanX.value = event.clientX
    panTimeStamp.value = currentTime
    
    const boardWidth = kanbanBoard.value?.clientWidth || 0
    const maxTranslate = 0
    const minTranslate = Math.min(0, boardWidth - containerWidth.value)
    
    if (newTranslateX > maxTranslate) {
      translateX.value = maxTranslate + (newTranslateX - maxTranslate) * 0.2
    } else if (newTranslateX < minTranslate) {
      translateX.value = minTranslate + (newTranslateX - minTranslate) * 0.2
    } else {
      translateX.value = newTranslateX
    }
  }
  
  const endPan = () => {
    if (!isPanning.value) return
    
    isPanning.value = false
    
    if (kanbanContainer.value) {
      kanbanContainer.value.classList.remove('panning')
    }
    
    const boardWidth = kanbanBoard.value?.clientWidth || 0
    const maxTranslate = 0
    const minTranslate = Math.min(0, boardWidth - containerWidth.value)
    
    if (Math.abs(panVelocity.value) > 0.1) {
      startMomentumScroll(panVelocity.value * 200)
    } else {
      snapToBoundaries(maxTranslate, minTranslate)
    }
    
    scrollIndicatorTimeout.value = setTimeout(() => {
      showScrollIndicator.value = false
    }, 1500)
  }
  
  const startMomentumScroll = (initialVelocity) => {
    if (isAnimating.value) return
    
    isAnimating.value = true
    let velocity = initialVelocity
    const friction = 0.95
    const minVelocity = 0.5
    
    const boardWidth = kanbanBoard.value?.clientWidth || 0
    const maxTranslate = 0
    const minTranslate = Math.min(0, boardWidth - containerWidth.value)
    
    const animate = () => {
      if (Math.abs(velocity) < minVelocity) {
        isAnimating.value = false
        snapToBoundaries(maxTranslate, minTranslate)
        return
      }
      
      velocity *= friction
      const newTranslateX = translateX.value + velocity
      
      if (newTranslateX > maxTranslate) {
        translateX.value = maxTranslate
        velocity *= -0.3
      } else if (newTranslateX < minTranslate) {
        translateX.value = minTranslate
        velocity *= -0.3
      } else {
        translateX.value = newTranslateX
      }
      
      animationFrameId.value = requestAnimationFrame(animate)
    }
    
    animationFrameId.value = requestAnimationFrame(animate)
  }
  
  const snapToBoundaries = (maxTranslate, minTranslate) => {
    const currentTranslate = translateX.value
    let targetTranslate = currentTranslate
    
    if (currentTranslate > maxTranslate) {
      targetTranslate = maxTranslate
    } else if (currentTranslate < minTranslate) {
      targetTranslate = minTranslate
    }
    
    if (targetTranslate !== currentTranslate) {
      animateToPosition(targetTranslate)
    }
  }
  
  const animateToPosition = (targetPosition) => {
    if (isAnimating.value) return
    
    isAnimating.value = true
    const startPosition = translateX.value
    const distance = targetPosition - startPosition
    const duration = 300
    const startTime = performance.now()
    
    const animate = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easeOut = 1 - Math.pow(1 - progress, 3)
      
      translateX.value = startPosition + (distance * easeOut)
      
      if (progress < 1) {
        animationFrameId.value = requestAnimationFrame(animate)
      } else {
        isAnimating.value = false
      }
    }
    
    animationFrameId.value = requestAnimationFrame(animate)
  }
  
  const handleWheel = (event) => {
    if (Math.abs(event.deltaX) > Math.abs(event.deltaY)) {
      event.preventDefault()
      
      if (animationFrameId.value) {
        cancelAnimationFrame(animationFrameId.value)
        animationFrameId.value = null
        isAnimating.value = false
      }
      
      const deltaX = event.deltaX
      const sensitivity = 1.2
      const newTranslateX = translateX.value - (deltaX * sensitivity)
      
      const boardWidth = kanbanBoard.value?.clientWidth || 0
      const maxTranslate = 0
      const minTranslate = Math.min(0, boardWidth - containerWidth.value)
      
      if (newTranslateX > maxTranslate) {
        translateX.value = maxTranslate + (newTranslateX - maxTranslate) * 0.1
        setTimeout(() => animateToPosition(maxTranslate), 100)
      } else if (newTranslateX < minTranslate) {
        translateX.value = minTranslate + (newTranslateX - minTranslate) * 0.1
        setTimeout(() => animateToPosition(minTranslate), 100)
      } else {
        translateX.value = newTranslateX
      }
    }
  }
  
  // Event handlers
  const handleCandidateMove = (moveData) => {
    // Find step data safely
    const fromStepData = props.stepColumns.find(s => s.step_key === moveData.fromStep)
    const toStepData = props.stepColumns.find(s => s.step_key === moveData.toStep)
    
    // Enhanced move data with step information
    const enhancedMoveData = {
      ...moveData,
      fromStepData: fromStepData || null,
      toStepData: toStepData || null,
      fromStepName: fromStepData?.step_name || 'Unknown Step',
      toStepName: toStepData?.step_name || 'Unknown Step',
      fromStage: fromStepData?.stage_name || 'Unknown Stage', 
      toStage: toStepData?.stage_name || 'Unknown Stage'
    }
    
    emit('candidateMoved', enhancedMoveData)
  }
  
  const handleStepAction = (action, step) => {
    emit('stepAction', action, step)
  }
  
  const handleMoveToStep = (moveData) => {
    // Process move to step request
    const enhancedMoveData = {
      ...moveData,
      fromStepData: props.stepColumns.find(s => s.step_key === moveData.fromStep),
      toStepData: moveData.targetStep
    }
    
    emit('moveToStep', enhancedMoveData)
  }
  
  // Cleanup
  const cleanupAnimations = () => {
    if (animationFrameId.value) {
      cancelAnimationFrame(animationFrameId.value)
      animationFrameId.value = null
    }
    isAnimating.value = false
    
    if (scrollIndicatorTimeout.value) {
      clearTimeout(scrollIndicatorTimeout.value)
    }
  }
  
  // Watchers
  watch(() => props.stepColumns, () => {
    nextTick(() => {
      calculateContainerWidth()
    })
  }, { immediate: true })
  
  // Lifecycle
  onMounted(() => {
    window.addEventListener('resize', calculateContainerWidth)
    nextTick(() => {
      calculateContainerWidth()
    })
  })
  
  onUnmounted(() => {
    window.removeEventListener('resize', calculateContainerWidth)
    cleanupAnimations()
  })
  
  // Expose methods
  defineExpose({
    animateToPosition,
    cleanupAnimations
  })
  </script>
  
  <style scoped>
  .kanban-board {
    display: flex;
    flex-direction: column;
    background-color: #f9fafb;
    overflow: hidden;
    height: 100%;
  }
  
  .stage-summary {
    position: sticky;
    top: 0;
    z-index: 10;
    background: rgba(255, 255, 255, 0.95);
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(8px);
  }
  
  .stage-summary-skeleton {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: fit-content;
  }
  
  .stage-summary-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    min-width: fit-content;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.2s ease;
  }
  
  .stage-summary-item:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .kanban-container {
    flex: 1;
    overflow: hidden;
    user-select: none;
    transform: translateZ(0);
    backface-visibility: hidden;
    perspective: 1000px;
  }
  
  .kanban-container.cursor-grab {
    cursor: grab;
    cursor: -webkit-grab;
  }
  
  .kanban-container.cursor-grabbing {
    cursor: grabbing;
    cursor: -webkit-grabbing;
    filter: brightness(0.98);
  }
  
  .kanban-scroll-area {
    display: flex;
    gap: 16px;
    padding: 16px;
    min-height: 100%;
    min-width: fit-content;
    will-change: transform;
    transform: translateZ(0);
    backface-visibility: hidden;
    transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  }
  
  .kanban-scroll-area.panning {
    transition: none;
    transform: translateZ(0);
  }
  
  .kanban-column-wrapper {
    min-width: 320px;
    width: 320px;
    flex-shrink: 0;
    height: calc(100vh - 140px);
  }
  
  .scroll-indicator {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 50;
    pointer-events: none;
    animation: smoothFadeIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    backdrop-filter: blur(12px);
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }
  
  @keyframes smoothFadeIn {
    0% {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.8) translateY(10px);
    }
    100% {
      opacity: 1;
      transform: translate(-50%, -50%) scale(1) translateY(0px);
    }
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 1;
    }
    50% {
      opacity: 0.5;
    }
  }
  
  .animate-pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  }
  
  /* Mobile responsive */
  @media (max-width: 768px) {
    .kanban-column-wrapper {
      min-width: 288px;
      width: 288px;
    }
    
    .scroll-indicator {
      display: none;
    }
    
    .kanban-container {
      cursor: default;
      touch-action: pan-x;
    }
  }
  
  /* Reduced motion accessibility */
  @media (prefers-reduced-motion: reduce) {
    .kanban-scroll-area {
      transition: none !important;
    }
    
    @keyframes smoothFadeIn {
      0%, 100% {
        opacity: 1;
        transform: translate(-50%, -50%);
      }
    }
  }
  </style>