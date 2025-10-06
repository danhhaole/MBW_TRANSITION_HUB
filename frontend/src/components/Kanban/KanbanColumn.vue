<template>
    <div class="kanban-column">
      <!-- Loading State -->
      <template v-if="isLoading">
        <div class="column-header-skeleton">
          <div class="flex items-center gap-3 mb-3">
            <div class="w-2 h-8 bg-gray-200 rounded animate-pulse"></div>
            <div class="flex-1">
              <div class="w-32 h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
              <div class="w-24 h-3 bg-gray-200 rounded animate-pulse"></div>
            </div>
            <div class="w-6 h-6 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div class="flex gap-2">
            <div class="w-16 h-6 bg-gray-200 rounded-full animate-pulse"></div>
            <div class="w-12 h-6 bg-gray-200 rounded-full animate-pulse"></div>
          </div>
        </div>
        
        <div class="column-content-skeleton">
          <div v-for="n in 3" :key="n" class="candidate-skeleton">
            <div class="flex items-start gap-3 mb-3">
              <div class="w-8 h-8 bg-gray-200 rounded-full animate-pulse"></div>
              <div class="flex-1">
                <div class="w-24 h-4 bg-gray-200 rounded animate-pulse mb-1"></div>
                <div class="w-32 h-3 bg-gray-200 rounded animate-pulse"></div>
              </div>
              <div class="w-12 h-5 bg-gray-200 rounded animate-pulse"></div>
            </div>
            <div class="space-y-2">
              <div class="w-full h-3 bg-gray-200 rounded animate-pulse"></div>
              <div class="w-3/4 h-3 bg-gray-200 rounded animate-pulse"></div>
            </div>
          </div>
        </div>
      </template>
  
      <!-- Normal Content -->
      <template v-else>
        <!-- Column Header -->
        <div class="column-header">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-1">
                <div 
                  class="w-2 h-8 rounded-sm flex-shrink-0" 
                  :style="{ backgroundColor: getStepColor() }"
                ></div>
                <div class="flex-1 min-w-0">
                  <h3 class="font-semibold text-gray-900 text-sm truncate">
                    {{ step.step_name }}
                  </h3>
                  <div class="text-xs text-gray-500 mt-1 flex items-center gap-2">
                    <span class="font-medium">{{ candidates.length }}</span>
                    <span>{{ __('candidates') }}</span>
                    <span class="px-2 py-0.5 rounded-full text-xs bg-gray-100 text-gray-600">
                      {{ step.stage_name }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Menu Button -->
            <div class="flex-shrink-0">
              <Dropdown :options="stepActions" placement="bottom-end">
                <Button 
                  variant="ghost" 
                  size="sm" 
                  class="text-gray-500 hover:text-gray-700"
                  @mousedown.stop
                >
                  <FeatherIcon name="more-horizontal" class="h-4 w-4" />
                </Button>
              </Dropdown>
            </div>
          </div>
          
          <!-- Step Badges -->
          <!-- <div class="flex items-center gap-2 flex-wrap">
            <span class="step-badge" :class="getTriggerBadgeClass()">
              <FeatherIcon :name="getTriggerIcon()" class="h-3 w-3" />
              <span class="text-xs">{{ getTriggerLabel() }}</span>
            </span>
            <span v-if="step.action" class="step-badge bg-indigo-50 text-indigo-700 border border-indigo-200">
              <FeatherIcon :name="getActionIcon()" class="h-3 w-3" />
              <span class="text-xs">{{ getActionLabel() }}</span>
            </span>
            <span v-if="step.condition" class="step-badge bg-amber-50 text-amber-700 border border-amber-200">
              <FeatherIcon name="filter" class="h-3 w-3" />
              <span class="text-xs">{{ __('Conditional') }}</span>
            </span>
            <span v-if="step.duration_hours" class="step-badge bg-orange-50 text-orange-700 border border-orange-200">
              <FeatherIcon name="clock" class="h-3 w-3" />
              <span class="text-xs">{{ getDurationText() }}</span>
            </span>
          </div> -->
        </div>
  
        <!-- Candidates Container with Fixed Height -->
        <div class="column-content">
          <Draggable
            :list="candidates"
            group="candidates"
            item-key="name"
            class="candidates-list"
            @end="onCandidateMove"
            :data-step-key="step.step_key"
            ghost-class="candidate-ghost"
            chosen-class="candidate-chosen"
            drag-class="candidate-drag"
          >
            <template #item="{ element: candidate }">
              <CandidateCard
                :candidate="candidate"
                :available-steps="availableSteps"
                @view="$emit('viewCandidate', candidate)"
                @edit="$emit('editCandidate', candidate)"
                @view-cv="$emit('viewCV', candidate)"
                @send-email="$emit('sendEmail', candidate)"
                @schedule-interview="$emit('scheduleInterview', candidate)"
                @move-to-step="handleMoveToStep"
              />
            </template>
          </Draggable>
  
          <!-- Empty State -->
          <!-- <div v-if="!candidates.length" class="empty-state">
            <div class="text-center py-8">
              <FeatherIcon name="inbox" class="h-8 w-8 mx-auto mb-2 text-gray-300" />
              <p class="text-sm text-gray-500 mb-4">{{ __('No candidates in this step') }}</p>
              <Button 
                variant="outline" 
                size="sm"
                @click="$emit('addCandidate')"
                class="border-dashed"
              >
                <template #prefix>
                  <FeatherIcon name="plus" class="h-4 w-4" />
                </template>
                {{ __('Add Candidate') }}
              </Button>
            </div>
          </div> -->
        </div>
      </template>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  import { Button, Dropdown, FeatherIcon } from 'frappe-ui'
  import Draggable from 'vuedraggable'
  import CandidateCard from './CandidateCard.vue'
  
  // Props
  const props = defineProps({
    step: { type: Object, default: () => ({}) },
    candidates: { type: Array, default: () => [] },
    availableSteps: { type: Array, default: () => [] },
    isLoading: { type: Boolean, default: false }
  })
  
  // Emits
  const emit = defineEmits([
    'addCandidate',
    'viewCandidate', 
    'editCandidate',
    'viewCV',
    'sendEmail',
    'scheduleInterview',
    'candidateMoved',
    'stepAction',
    'moveToStep'
  ])
  
  // Computed
  const stepActions = computed(() => [
    {
      group: __('Candidate Actions'),
      hideLabel: true,
      items: [
        { 
          label: __('Add Candidate'), 
          icon: 'user-plus', 
          onClick: () => emit('addCandidate') 
        },
        // { 
        //   label: __('Import Candidates'), 
        //   icon: 'upload', 
        //   onClick: () => emit('stepAction', 'import', props.step) 
        // }
      ]
    },
    {
      group: __('Step Management'),
      hideLabel: true,
      items: [
        { 
          label: __('Automations'), 
          icon: 'settings', 
          onClick: () => emit('stepAction', 'edit', props.step) 
        },
        // { 
        //   label: __('View Statistics'),  
        //   icon: 'bar-chart-3', 
        //   onClick: () => emit('stepAction', 'stats', props.step) 
        // }
      ]
    }
  ])
  
  // Helper functions
  const getStepColor = () => {
    // Get color from JSON data with priority order
    return props.step?.color || 
           props.step?.step_color || 
           props.step?.stage_color || 
           '#2563eb' // FrappeUI default blue
  }
  
  const getTriggerBadgeClass = () => {
    const trigger = props.step?.trigger || 'manual'
    const baseClass = 'step-badge'
    
    switch (trigger) {
      case 'scheduled':
        return `${baseClass} badge-green`
    //   case 'webhook':
    //     return `${baseClass} badge-purple`
      case 'manual':
      default:
        return `${baseClass} badge-gray`
    }
  }
  
  const getTriggerIcon = () => {
    const trigger = props.step?.trigger || 'manual'
    const icons = {
      'scheduled': 'zap',
      'manual': 'user',
    //   'webhook': 'link'
    }
    return icons[trigger] || 'circle'
  }
  
  const getTriggerLabel = () => {
    const trigger = props.step?.trigger || 'manual'
    const labels = {
      'scheduled': __('Auto'),
      'manual': __('Manual'),
      'webhook': __('API')
    }
    return labels[trigger] || trigger
  }
  
  const getActionIcon = () => {
    const actionType = props.step?.action?.type
    const icons = {
      'send_email': 'mail',
      'create_task': 'clipboard',
      'automatic_scoring': 'star',
      'send_test': 'file-text',
      'send_offer_letter': 'file-check'
    }
    return icons[actionType] || 'play'
  }
  
  const getActionLabel = () => {
    const actionType = props.step?.action?.type
    const labels = {
      'send_email': __('Email'),
      'create_task': __('Task'),
      'automatic_scoring': __('Score'),
      'send_test': __('Test'),
      'send_offer_letter': __('Offer')
    }
    return labels[actionType] || actionType
  }
  
  const getDurationText = () => {
    const hours = props.step?.duration_hours
    if (!hours) return ''
    
    if (hours < 1) return `${hours * 60}m`
    if (hours === 1) return '1h'
    if (hours < 24) return `${hours}h`
    const days = Math.floor(hours / 24)
    return `${days}d`
  }
  
  // Event handlers
  const onCandidateMove = (event) => {
    const candidateId = event.item.dataset.candidateId
    const fromStepKey = event.from.dataset.stepKey
    const toStepKey = event.to.dataset.stepKey
    
    if (fromStepKey !== toStepKey) {
      // Find candidate data safely
      //const candidate = props.candidates.find(c => c.name === candidateId)
      //if (candidate) {
        emit('candidateMoved', {
          candidateId,
          //candidate: candidate,
          fromStep: fromStepKey,
          toStep: toStepKey,
          fromStepName: props.step?.step_name || 'Unknown Step',
          toStepName: props.step?.step_name || 'Unknown Step',
          fromStage: props.step?.stage_name || 'Unknown Stage',
          toStage: props.step?.stage_name || 'Unknown Stage',
          oldIndex: event.oldIndex,
          newIndex: event.newIndex
        })
    //   } else {
    //     console.warn('Candidate not found for move:', candidateId)
    //   }
    }
  }
  
  const handleMoveToStep = (moveData) => {
    
    emit('moveToStep', moveData)
  }
  </script>
  
  <style scoped>
  .kanban-column {
    height: 100%;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
  }
  
  .column-header-skeleton {
    padding: 16px;
    border-bottom: 1px solid #f3f4f6;
    background-color: #f9fafb;
  }
  
  .column-content-skeleton {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
  }
  
  .candidate-skeleton {
    background-color: #f9fafb;
    border-radius: 8px;
    padding: 16px;
  }
  
  .column-header {
    padding: 16px;
    border-bottom: 1px solid #f3f4f6;
    background-color: #f9fafb;
    flex-shrink: 0;
  }
  
  .column-content {
    flex: 1;
    padding: 12px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: calc(100% - 120px);
  }
  
  .candidates-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
    overflow-y: auto;
  }
  
  .step-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 500;
    border-radius: 6px;
    transition: all 0.15s ease;
  }
  
  .badge-green {
    background-color: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
  }
  
  .badge-purple {
    background-color: #faf5ff;
    color: #7c2d12;
    border: 1px solid #ddd6fe;
  }
  
  .badge-gray {
    background-color: #f9fafb;
    color: #374151;
    border: 1px solid #e5e7eb;
  }
  
  .empty-state {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  /* Drag states with FrappeUI colors */
  .candidate-ghost {
    opacity: 0.4;
    background-color: #f9fafb;
    border-color: #d1d5db;
    transform: rotate(2deg) scale(0.98);
  }
  
  .candidate-chosen {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    border-color: #6b7280;
    transform: scale(1.05);
    z-index: 1000;
  }
  
  .candidate-drag {
    opacity: 0.8;
    transform: rotate(1deg);
  }
  
  /* Scrollbar styling - FrappeUI style */
  .candidates-list::-webkit-scrollbar {
    width: 6px;
  }
  
  .candidates-list::-webkit-scrollbar-track {
    background-color: #f3f4f6;
    border-radius: 3px;
  }
  
  .candidates-list::-webkit-scrollbar-thumb {
    background-color: #d1d5db;
    border-radius: 3px;
  }
  
  .candidates-list::-webkit-scrollbar-thumb:hover {
    background-color: #9ca3af;
  }
  
  /* Loading animation */
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
    .column-header {
      padding: 12px;
    }
    
    .column-content {
      padding: 8px;
    }
    
    .candidates-list {
      gap: 8px;
    }
  }
  </style>