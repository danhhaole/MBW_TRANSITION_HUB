<template>
    <div 
      class="candidate-card"
      :data-candidate-id="candidate.name"
      @click="$emit('view')"
      @mousedown.stop
    >
      <!-- Candidate Header -->
      <div class="candidate-header">
        <div class="flex items-start gap-3 flex-1 min-w-0">
          <!-- Avatar -->
          <Avatar
            :image="candidate.can_avatar"
            :label="candidate.can_full_name"
            size="sm"
            class="candidate-avatar"
          />
          
          <!-- Basic Info -->
          <div class="flex-1 min-w-0">
            <h4 class="candidate-name">
              {{ candidate.can_full_name || __('Unnamed Candidate') }}
            </h4>
            <p class="candidate-email">
              {{ candidate.can_email }}
            </p>
          </div>
        </div>
        
        <!-- Status Badge -->
        <div class="status-badge">
          {{ candidate.status || 'New' }}
        </div>
      </div>
  
      <!-- Candidate Details -->
      <div class="candidate-details">
        <!-- Application Date -->
        <div v-if="candidate.can_application_date" class="detail-item">
          <FeatherIcon name="calendar" class="detail-icon" />
          <span class="detail-text">
            {{ __('Applied') }} {{ formatTimeAgo(candidate.can_application_date) }}
          </span>
        </div>
  
        <!-- Source -->
        <div v-if="candidate.candidatesource_id" class="detail-item">
          <FeatherIcon name="users" class="detail-icon" />
          <span class="detail-text">
            {{ candidate.candidatesource_id }}
          </span>
        </div>
  
        <!-- Phone -->
        <div v-if="candidate.can_phone" class="detail-item">
          <FeatherIcon name="phone" class="detail-icon" />
          <span class="detail-text">
            {{ candidate.can_phone }}
          </span>
        </div>
  
        <!-- Score Progress -->
        <div v-if="candidate.overall_score" class="detail-item">
          <FeatherIcon name="star" class="detail-icon" />
          <div class="score-container">
            <div class="score-bar">
              <div 
                class="score-fill"
                :class="getScoreColorClass(candidate.overall_score)"
                :style="`width: ${candidate.overall_score}%`"
              ></div>
            </div>
            <span class="score-text">
              {{ candidate.overall_score }}%
            </span>
          </div>
        </div>
      </div>
  
      <!-- Quick Actions -->
      <div class="candidate-actions">
        <div class="actions-row">
          <div class="action-buttons-left">
            <!-- View CV -->
            <Button
              v-if="candidate.can_cv_file"
              variant="ghost"
              size="sm"
              @click.stop="$emit('viewCV')"
              :title="__('View CV')"
              class="action-button"
            >
              <FeatherIcon name="file-text" class="h-3 w-3" />
            </Button>
            
            <!-- Send Email -->
            <Button
              variant="ghost"
              size="sm"
              @click.stop="$emit('sendEmail')"
              :title="__('Send Email')"
              class="action-button"
            >
              <FeatherIcon name="mail" class="h-3 w-3" />
            </Button>
            
            <!-- Schedule Interview -->
            <Button
              variant="ghost"
              size="sm"
              @click.stop="$emit('scheduleInterview')"
              :title="__('Schedule Interview')"
              class="action-button"
            >
              <FeatherIcon name="calendar" class="h-3 w-3" />
            </Button>
  
            <!-- Move to Step -->
            <Button
              variant="ghost"
              size="sm"
              @click.stop="showMoveModal = true"
              :title="__('Move to Step')"
              class="action-button"
            >
              <FeatherIcon name="move" class="h-3 w-3" />
            </Button>
          </div>
          
          <div class="action-buttons-right">
            <!-- Edit Candidate -->
            <Button
              variant="ghost"
              size="sm"
              @click.stop="$emit('edit')"
              :title="__('Edit Candidate')"
              class="action-button"
            >
              <FeatherIcon name="edit" class="h-3 w-3" />
            </Button>
            
            <!-- More Actions -->
            <Dropdown :options="candidateActions" placement="bottom-end">
              <Button 
                variant="ghost" 
                size="sm" 
                @click.stop 
                @mousedown.stop
                class="action-button"
              >
                <FeatherIcon name="more-horizontal" class="h-3 w-3" />
              </Button>
            </Dropdown>
          </div>
        </div>
      </div>
  
      <!-- Move to Step Modal -->
      <Dialog v-model="showMoveModal" :options="{ title: __('Move Candidate to Step'), size: 'md' }">
        <template #body-content>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Search Steps') }}
              </label>
              <div class="relative">
                <FeatherIcon name="search" class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                <input
                  type="text"
                  v-model="stepSearchQuery"
                  :placeholder="__('Search by step name or stage...')"
                  class="search-input"
                />
              </div>
            </div>
  
            <div class="max-h-64 overflow-y-auto border border-gray-200 rounded-lg">
              <div v-if="filteredSteps.length === 0" class="p-4 text-center text-gray-500">
                {{ __('No steps found') }}
              </div>
              
              <div 
                v-for="step in filteredSteps" 
                :key="step.step_key"
                class="step-option"
                @click="selectStep(step)"
              >
                <div class="flex items-center gap-3">
                  <div 
                    class="w-3 h-3 rounded-full flex-shrink-0"
                    :style="{ backgroundColor: step.color }"
                  ></div>
                  <div class="flex-1 min-w-0">
                    <div class="text-base text-gray-900">{{ step.step_name }}</div>
                    <div class="text-sm text-gray-500">{{ step.stage_name }}</div>
                  </div>
                  <div class="text-xs px-2 py-1 bg-gray-100 rounded">
                    {{ step.trigger || 'manual' }}
                  </div>
                </div>
              </div>
            </div>
  
            <div v-if="selectedStep" class="selected-step-preview">
              <h4 class="font-medium text-gray-900 mb-2">{{ __('Moving to:') }}</h4>
              <div class="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                <div 
                  class="w-4 h-4 rounded-full"
                  :style="{ backgroundColor: selectedStep.color }"
                ></div>
                <div class="flex-1">
                  <div class="text-base text-blue-900">{{ selectedStep.step_name }}</div>
                  <div class="text-sm text-blue-700">{{ selectedStep.stage_name }}</div>
                </div>
              </div>
            </div>
          </div>
        </template>
        
        <template #actions>
          <div class="flex gap-3">
            <Button variant="outline" @click="cancelMove">
              {{ __('Cancel') }}
            </Button>
            <Button 
              variant="solid" 
              @click="confirmMove"
              :disabled="!selectedStep"
            >
              {{ __('Move Candidate') }}
            </Button>
          </div>
        </template>
      </Dialog>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { Button, Avatar, Dropdown, FeatherIcon, Dialog } from 'frappe-ui'
  
  // Props
  const props = defineProps({
    candidate: { type: Object, required: true },
    availableSteps: { type: Array, default: () => [] }
  })
  
  // Emits
  const emit = defineEmits([
    'view',
    'edit', 
    'viewCV',
    'sendEmail',
    'scheduleInterview',
    'moveToStep'
  ])
  
  // Reactive state
  const showMoveModal = ref(false)
  const stepSearchQuery = ref('')
  const selectedStep = ref(null)
  
  // Computed
  const candidateActions = computed(() => [
    {
      group: __('Actions'),
      hideLabel: true,
      items: [
        { 
          label: __('View Profile'), 
          icon: 'user', 
          onClick: () => emit('view') 
        },
        { 
          label: __('Add Note'), 
          icon: 'message-circle', 
          onClick: () => emit('addNote') 
        },
        { 
          label: __('Download CV'), 
          icon: 'download', 
          onClick: () => emit('downloadCV') 
        },
        { 
          label: __('Delete'), 
          icon: 'trash-2', 
          onClick: () => emit('delete'),
          class: 'text-red-600'
        }
      ]
    }
  ])
  
  const filteredSteps = computed(() => {
    if (!stepSearchQuery.value.trim()) {
      return props.availableSteps
    }
    
    const query = stepSearchQuery.value.toLowerCase()
    return props.availableSteps.filter(step => 
      step.step_name?.toLowerCase().includes(query) ||
      step.stage_name?.toLowerCase().includes(query)
    )
  })
  
  // Helper functions
  const getScoreColorClass = (score) => {
    if (score >= 80) return 'bg-emerald-500'
    if (score >= 60) return 'bg-blue-500'
    if (score >= 40) return 'bg-amber-500'
    return 'bg-red-500'
  }
  
  const formatTimeAgo = (dateString) => {
    if (!dateString) return ''
    
    const date = new Date(dateString)
    const now = new Date()
    const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
    
    if (diffInDays === 0) return __('today')
    if (diffInDays === 1) return __('yesterday')
    if (diffInDays < 7) return __(`${diffInDays} days ago`)
    if (diffInDays < 30) return __(`${Math.floor(diffInDays / 7)} weeks ago`)
    return __(`${Math.floor(diffInDays / 30)} months ago`)
  }
  
  // Move functionality
  const selectStep = (step) => {
    selectedStep.value = step
  }
  
  const confirmMove = () => {
    if (selectedStep.value) {
      emit('moveToStep', {
        candidate: props.candidate,
        targetStep: selectedStep.value,
        fromStep: props.candidate.current_step || props.candidate.step_id,
        toStep: selectedStep.value.step_key
      })
      
      // Reset and close modal
      cancelMove()
    }
  }
  
  const cancelMove = () => {
    showMoveModal.value = false
    selectedStep.value = null
    stepSearchQuery.value = ''
  }
  </script>
  
  <style scoped>
  .candidate-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  
  .candidate-card:hover {
    border-color: #d1d5db;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
  }
  
  .candidate-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 12px;
  }
  
  .candidate-avatar {
    flex-shrink: 0;
    border: 2px solid #f3f4f6;
    border-radius: 50%;
  }
  
  .candidate-name {
    font-weight: 600;
    color: #111827;
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .candidate-email {
    font-size: 12px;
    color: #6b7280;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-top: 2px;
  }
  
  .status-badge {
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 6px;
    background-color: #f3f4f6;
    color: #374151;
    font-weight: 500;
    flex-shrink: 0;
  }
  
  .candidate-details {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-bottom: 12px;
  }
  
  .detail-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
  }
  
  .detail-icon {
    width: 12px;
    height: 12px;
    color: #9ca3af;
    flex-shrink: 0;
  }
  
  .detail-text {
    color: #6b7280;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .score-container {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
  }
  
  .score-bar {
    flex: 1;
    background-color: #e5e7eb;
    border-radius: 9999px;
    height: 6px;
  }
  
  .score-fill {
    height: 6px;
    border-radius: 9999px;
    transition: all 0.3s ease;
  }
  
  .score-text {
    font-size: 12px;
    font-weight: 600;
    color: #374151;
  }
  
  .candidate-actions {
    padding-top: 12px;
    border-top: 1px solid #f3f4f6;
    opacity: 0;
    transition: opacity 0.2s ease;
  }
  
  .candidate-card:hover .candidate-actions {
    opacity: 1;
  }
  
  .actions-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  .action-buttons-left,
  .action-buttons-right {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  
  .action-button {
    color: #6b7280;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.15s ease;
  }
  
  .action-button:hover {
    color: #374151;
    background-color: #f3f4f6;
  }
  
  /* Score colors */
  .bg-emerald-500 {
    background-color: #10b981;
  }
  
  .bg-blue-500 {
    background-color: #3b82f6;
  }
  
  .bg-amber-500 {
    background-color: #f59e0b;
  }
  
  .bg-red-500 {
    background-color: #ef4444;
  }
  
  /* Mobile optimizations */
  @media (max-width: 768px) {
    .candidate-actions {
      opacity: 1;
    }
    
    .candidate-card {
      padding: 12px;
    }
  }
  
  /* Search input styling */
  .search-input {
    width: 100%;
    padding: 4px 12px 4px 36px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.15s ease;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  /* Step option styling */
  .step-option {
    padding: 12px;
    border-bottom: 1px solid #f3f4f6;
    cursor: pointer;
    transition: background-color 0.15s ease;
  }
  
  .step-option:hover {
    background-color: #f9fafb;
  }
  
  .step-option:last-child {
    border-bottom: none;
  }
  
  /* Selected step preview */
  .selected-step-preview {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid #e5e7eb;
  }
  
  /* Accessibility - reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .candidate-card,
    .candidate-actions,
    .score-fill,
    .search-input,
    .step-option {
      transition: none;
    }
    
    .candidate-card:hover {
      transform: none;
    }
  }
  </style>