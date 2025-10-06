<template>
  <div class="recruitment-kanban">
    <!-- View Toggle Header -->
    <div class="view-toggle-header">
      <!-- Stage Summary Bar (Main Header) -->
      <div class="stage-summary-bar">
        <div class="flex items-center justify-between">
          <!-- <div class="flex items-center gap-6">
            <div class="stage-list">
              <div 
                v-for="stage in stageSummaries" 
                :key="stage.stage_name"
                class="stage-summary-item"
                :style="{ '--stage-color': stage.color }"
              >
                <div class="stage-indicator"></div>
                <div class="stage-info">
                  <span class="stage-name">{{ stage.stage_name }}</span>
                  <span class="stage-count">{{ stage.candidate_count }}</span>
                </div>
              </div>
            </div>
            
            <div class="total-summary">
              <div class="total-candidates">
                <span class="total-number">{{ activeCandidates.length }}</span>
                <span class="total-label">{{__("Total")}}</span>
              </div>
            </div>
          </div> -->
          
          <div class="flex items-center gap-3">
            <!-- Loading indicator for view preference -->
            <div v-if="viewPreferences.isLoading.value" class="view-loading">
              <svg class="h-4 w-4 animate-spin text-gray-400" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            
            <!-- View Toggle Buttons -->
            <div class="view-toggle-group">
              <button 
                @click="viewPreferences.setPreference('kanban')"
                :class="['view-toggle-btn', { 'active': viewPreferences.currentView.value === 'kanban' }]"
                title="Kanban View"
                :disabled="viewPreferences.isLoading.value"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/>
                </svg>
                <span class="hidden sm:inline">{{__("Kanban")}}</span>
              </button>
              <button 
                @click="viewPreferences.setPreference('list')"
                :class="['view-toggle-btn', { 'active': viewPreferences.currentView.value === 'list' }]"
                title="List View"
                :disabled="viewPreferences.isLoading.value"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16"/>
                </svg>
                <span class="hidden sm:inline">{{__("List")}}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Views -->
    <div class="view-content">
      <!-- Kanban View -->
      <KanbanBoard
        v-if="viewPreferences.currentView.value === 'kanban'"
        :step-columns="stepColumns"
        :stage-summaries="stageSummaries"
        :candidates="activeCandidates"
        :is-loading="isLoading"
        @add-candidate-to-step="handleAddCandidateToStep"
        @view-candidate="handleViewCandidate"
        @edit-candidate="handleEditCandidate"
        @view-cv="handleViewCV"
        @send-email="handleSendEmail"
        @schedule-interview="handleScheduleInterview"
        @candidate-moved="handleCandidateMoved"
        @step-action="handleStepAction"
        @move-to-step="handleMoveToStep"
      />

      <!-- List View -->
      <CandidateListView
        v-if="viewPreferences.currentView.value === 'list'"
        :candidates="activeCandidates"
        :step-columns="stepColumns"
        :stage-summaries="stageSummaries"
        :is-loading="isLoading"
        @view-candidate="handleViewCandidate"
        @edit-candidate="handleEditCandidate"
        @view-cv="handleViewCV"
        @send-email="handleSendEmail"
        @schedule-interview="handleScheduleInterview"
        @move-to-step="handleMoveToStep"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useViewPreferences } from '@/composables/useViewPreferences'
import KanbanBoard from './KanbanBoard.vue'
import CandidateListView from './CandidateListView.vue'

// Props
const props = defineProps({
  jobId: { type: String, default: '' },
  recruitmentProcess: { type: Array, default: () => [] },
  candidates: { type: Array, default: () => [] },
  useTestData: { type: Boolean, default: false }
})

// Emits
const emit = defineEmits([
  'addCandidate',
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

// View Preferences Composable
const viewPreferences = useViewPreferences({
  storageKey: 'recruitment_view_mode',
  defaultValue: 'kanban',
  validValues: ['kanban', 'list'],
  userProfileField: 'recruitment_view_mode'
})

// Reactive state
const isLoading = ref(true)
const activeCandidates = ref([])

// Helper functions for color management
const colorHelpers = {
  getStageColor(stageName) {
    let process = props.recruitmentProcess
  if(typeof process === "string"){
    process = JSON.parse(process)
  }
    const stage = process.find(s => 
      s.stage_name?.toLowerCase() === stageName?.toLowerCase()
    )
    return stage?.color || stage?.stage_color || '#2563eb'
  },

  getStepColor(step) {
    // Priority 1: Direct color from step
    if (step?.color) return step.color
    if (step?.step_color) return step.step_color
     let process = props.recruitmentProcess
  if(typeof process === "string"){
    process = JSON.parse(process)
  }
    // Priority 2: Find in recruitment process
    if (step?.step_id || step?.step_name) {
      for (const stage of process) {
        if (stage.steps) {
          const foundStep = stage.steps.find(s => 
            s.step_id === step.step_id || 
            s.step_name === step.step_name
          )
          
          if (foundStep?.color) return foundStep.color
          if (foundStep?.step_color) return foundStep.step_color
        }
      }
    }
    
    // Priority 3: Fallback to stage color
    if (step?.stage_name) {
      const stageColor = this.getStageColor(step.stage_name)
      if (stageColor !== '#2563eb') return stageColor
    }
    
    return '#2563eb'
  }
}

// Computed properties
const stepColumns = computed(() => {
  if (!props.recruitmentProcess?.length) return []
  
  const steps = []
  let process = props.recruitmentProcess
  if(typeof process === "string"){
    process = JSON.parse(process)
  }
  process.forEach(stage => {
    if (stage.steps?.length) {
      stage.steps.forEach(step => {
        const stepWithStageInfo = {
          ...step,
          stage_name: stage.stage_name,
          stage_sequence: stage.sequence_id,
          step_key: step.step_id,
          stage_color: stage.color || stage.stage_color
        }
        
        const stepColor = colorHelpers.getStepColor(stepWithStageInfo)
        
        steps.push({
          ...stepWithStageInfo,
          color: stepColor
        })
      })
    }
  })
  
  return steps.sort((a, b) => {
    if (a.stage_sequence !== b.stage_sequence) {
      return a.stage_sequence - b.stage_sequence
    }
    return a.sequence_id - b.sequence_id
  })
})

const stageSummaries = computed(() => {
  if (!props.recruitmentProcess?.length) return []
  let process = props.recruitmentProcess
  if(typeof process === "string"){
    process = JSON.parse(process)
  }
  return process.map(stage => {
    const stageCandidates = activeCandidates.value.filter(candidate => {
      return stepColumns.value
        .filter(step => step.stage_name === stage.stage_name)
        .some(step => candidate.stage_id === step.step_key)
    })
    
    const stageColor = stage.color || stage.stage_color || '#6b7280'
    
    return {
      stage_name: stage.stage_name,
      candidate_count: stageCandidates.length,
      step_count: stage.steps?.length || 0,
      color: stageColor,
      sequence_id: stage.sequence_id
    }
  }).sort((a, b) => a.sequence_id - b.sequence_id)
})

// Event handlers
const eventHandlers = {
  handleAddCandidateToStep(step) {
    emit('addCandidateToStep', step)
  },

  handleViewCandidate(candidate) {
    emit('viewCandidate', candidate)
  },

  handleEditCandidate(candidate) {
    emit('editCandidate', candidate)
  },

  handleViewCV(candidate) {
    emit('viewCV', candidate)
  },

  handleSendEmail(candidate) {
    emit('sendEmail', candidate)
  },

  handleScheduleInterview(candidate) {
    emit('scheduleInterview', candidate)
  },

  handleCandidateMoved(moveData) {
    console.log('=== CANDIDATE MOVED DEBUG ===')
    // console.log('moveData received:', moveData)
    // console.log('activeCandidates',activeCandidates)
    
    if (!moveData.candidateId || !moveData.toStep) {
      console.error('Invalid move data:', moveData)
      return
    }

    // Update local state
    const candidate = activeCandidates.value.find(c => c.name === moveData.candidateId)
    if (candidate) {
      console.log('Candidate found:', candidate.can_full_name)
      candidate.current_step = moveData.toStep
      candidate.step_id = moveData.toStep
      candidate.recruitment_step = moveData.toStep
    } else {
      console.warn('Candidate not found for ID:', moveData.candidateId)
    }

    // Enhance move data with step information
    const fromStepData = stepColumns.value.find(s => s.step_key === moveData.fromStep)
    const toStepData = stepColumns.value.find(s => s.step_key === moveData.toStep)

    const enhancedMoveData = {
      ...moveData,
      candidate: candidate,
      fromStepData: fromStepData || { step_name: 'Unknown Step', stage_name: 'Unknown Stage' },
      toStepData: toStepData || { step_name: 'Unknown Step', stage_name: 'Unknown Stage' },
      fromStepName: fromStepData?.step_name || 'Unknown Step',
      toStepName: toStepData?.step_name || 'Unknown Step', 
      fromStage: fromStepData?.stage_name || 'Unknown Stage',
      toStage: toStepData?.stage_name || 'Unknown Stage'
    }

    console.log('Enhanced move data:', enhancedMoveData)
    console.log('===============================')

    emit('candidateMoved', enhancedMoveData)
  },

  handleStepAction(action, step) {
    emit('stepAction', action, step)
  },

  handleMoveToStep(moveData) {
    console.log('=== MOVE TO STEP REQUEST ===')
    // console.log('moveData:', moveData)
    
    // Update local candidate state
    const candidate = activeCandidates.value.find(c => c.name === moveData.candidate.name)
    if (candidate) {
      candidate.current_step = moveData.toStep
      candidate.step_id = moveData.toStep
      candidate.recruitment_step = moveData.toStep
      
      console.log('Updated candidate local state:', candidate.can_full_name, 'to step:', moveData)
    }
     // Enhance move data with step information
    const fromStepData = stepColumns.value.find(s => s.step_key === moveData.fromStep)
    const toStepData = stepColumns.value.find(s => s.step_key === moveData.toStep)

    const enhancedMoveData = {
      ...moveData,
      candidate: candidate,
      fromStepData: fromStepData || { step_name: 'Unknown Step', stage_name: 'Unknown Stage' },
      toStepData: toStepData || { step_name: 'Unknown Step', stage_name: 'Unknown Stage' },
      fromStepName: fromStepData?.step_name || 'Unknown Step',
      toStepName: toStepData?.step_name || 'Unknown Step', 
      fromStage: fromStepData?.stage_name || 'Unknown Stage',
      toStage: toStepData?.stage_name || 'Unknown Stage'
    }
    
    emit('moveToStep', enhancedMoveData)
  }
}

// Extract event handlers for template
const {
  handleAddCandidateToStep,
  handleViewCandidate,
  handleEditCandidate,
  handleViewCV,
  handleSendEmail,
  handleScheduleInterview,
  handleCandidateMoved,
  handleStepAction,
  handleMoveToStep
} = eventHandlers

// Data management
const dataManagement = {
  updateCandidatesData() {
    if (props.candidates.length > 0) {
      activeCandidates.value = [...props.candidates]
    } else {
      activeCandidates.value = []
    }
  },

  refreshData() {
    isLoading.value = true
    setTimeout(() => {
      isLoading.value = false
    }, 1000)
  }
}

// Watchers
watch([() => props.candidates, stepColumns], () => {
  dataManagement.updateCandidatesData()
}, { immediate: true })

// Watch for job changes to reload view preference
watch(() => props.jobId, () => {
  if (props.jobId) {
    // Quick load from storage when job changes
    viewPreferences.loadPreference()
  }
}, { immediate: false })

// Lifecycle
onMounted(async () => {
  // View preferences are auto-initialized by the composable
  // We just need to wait for component loading
  setTimeout(() => {
    isLoading.value = false
  }, 1500)
})

// Expose methods for external access
defineExpose({
  // View management
  setViewMode: viewPreferences.setPreference,
  getCurrentViewMode: () => viewPreferences.currentView.value,
  resetViewPreference: viewPreferences.resetPreference,
  
  // Data management
  refreshData: dataManagement.refreshData,
  
  // Navigation
  scrollToColumn: (columnIndex) => {
    // Method to scroll to specific column if needed
    console.log('Scroll to column:', columnIndex)
  },
  
  // Preference management
  viewPreferencesConfig: viewPreferences.config,
  syncViewPreference: () => {
    const current = viewPreferences.currentView.value
    viewPreferences.setPreference(current)
  }
})
</script>

<style scoped>
.recruitment-kanban {
  @apply h-full w-full;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.view-toggle-header {
  @apply bg-white border-b border-gray-200 px-6 py-4;
}

.view-toggle-group {
  @apply flex items-center bg-gray-100 rounded-lg p-1;
}

.view-toggle-btn {
  @apply flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 rounded-md transition-all duration-200 hover:text-gray-900;
}

.view-toggle-btn.active {
  @apply bg-white text-blue-600 shadow-sm;
}

.view-toggle-btn:hover:not(.active) {
  @apply bg-gray-50;
}

.view-toggle-btn:disabled {
  @apply opacity-50 cursor-not-allowed;
}

.view-loading {
  @apply flex items-center justify-center w-8 h-8;
}

/* Stage Summary Bar Styles */
.stage-summary-bar {
  @apply p-4 bg-gray-50 rounded-lg border border-gray-200;
}

.stage-list {
  @apply flex items-center gap-4 flex-wrap;
}

.stage-summary-item {
  @apply flex items-center gap-2 px-3 py-2 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors cursor-pointer shadow-sm;
}

.stage-indicator {
  @apply w-3 h-3 rounded-full;
  background-color: var(--stage-color);
}

.stage-info {
  @apply flex items-center gap-2;
}

.stage-name {
  @apply text-sm font-medium text-gray-900;
}

.stage-count {
  @apply text-sm font-bold text-gray-700 bg-gray-100 px-2 py-0.5 rounded-full min-w-[20px] text-center;
}

.total-summary {
  @apply flex items-center;
}

.total-candidates {
  @apply flex items-center gap-2 px-3 py-2 bg-blue-50 border border-blue-200 rounded-lg;
}

.total-number {
  @apply text-lg font-bold text-blue-700;
}

.total-label {
  @apply text-sm font-medium text-blue-600;
}

.view-content {
  @apply flex-1 overflow-hidden;
}
</style>