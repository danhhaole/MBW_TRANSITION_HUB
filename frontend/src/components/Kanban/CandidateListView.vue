<template>
    <div class="candidate-list-container">
      <!-- Filters and Search Header -->
      <div class="list-header">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <!-- Search -->
            <div class="relative">
              <FeatherIcon name="search" class="search-icon" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search candidates..."
                class="search-input"
              />
            </div>
            
            <!-- Stage Filter -->
            <FormControl
              type="select"
              v-model="selectedStage"
              :options="stageOptions"
              placeholder="All Stages"
              class="filter-control"
            />
            
            <!-- Step Filter -->
            <FormControl
              type="select"
              v-model="selectedStep"
              :options="stepOptions"
              placeholder="All Steps"
              class="filter-control"
            />
          </div>
          
          <div class="flex items-center gap-3">
            <!-- Results count -->
            <span class="results-count">
              {{ filteredCandidates.length }} of {{ candidates.length }}
            </span>
            
            <!-- Page size selector -->
            <FormControl
              type="select"
              v-model="pageSize"
              :options="pageSizeOptions"
              class="page-size-control"
            />
            
            <!-- Export button -->
            <Button variant="outline" @click="exportToCSV" class="export-btn">
              <template #prefix>
                <FeatherIcon name="download" class="h-4 w-4" />
              </template>
              {{__("Export")}}
            </Button>
          </div>
        </div>
      </div>
  
      <!-- Grid Content -->
      <div class="grid-container">
        <!-- Loading state -->
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-content">
            <LoadingIndicator />
            <span class="loading-text">{{__("Loading candidates...")}}</span>
          </div>
        </div>
  
        <!-- Grid Header -->
        <div v-else class="grid-header">
          <div class="grid-row header-row">
            <div class="grid-cell header-cell" @click="sortBy('can_full_name')">
              <span>Candidate</span>
              <FeatherIcon 
                v-if="sortField === 'can_full_name'" 
                :name="sortOrder === 'asc' ? 'chevron-up' : 'chevron-down'" 
                class="sort-icon"
              />
            </div>
            <div class="grid-cell header-cell" @click="sortBy('can_email')">
              <span>{{__("Contact")}}</span>
              <FeatherIcon 
                v-if="sortField === 'can_email'" 
                :name="sortOrder === 'asc' ? 'chevron-up' : 'chevron-down'" 
                class="sort-icon"
              />
            </div>
            <div class="grid-cell header-cell" @click="sortBy('current_stage')">
              <span>{{__("Status")}}</span>
              <FeatherIcon 
                v-if="sortField === 'current_stage'" 
                :name="sortOrder === 'asc' ? 'chevron-up' : 'chevron-down'" 
                class="sort-icon"
              />
            </div>
            <div class="grid-cell header-cell" @click="sortBy('can_application_date')">
              <span>{{__("Applied")}}</span>
              <FeatherIcon 
                v-if="sortField === 'can_application_date'" 
                :name="sortOrder === 'asc' ? 'chevron-up' : 'chevron-down'" 
                class="sort-icon"
              />
            </div>
            <div class="grid-cell header-cell">
              <span>{{__("Score")}}</span>
            </div>
            <div class="grid-cell header-cell">
              <span>{{__("Actions")}}</span>
            </div>
          </div>
        </div>
  
        <!-- Grid Body -->
        <div v-if="!isLoading" class="grid-body">
          <div 
            v-for="candidate in paginatedCandidates" 
            :key="candidate.name"
            class="grid-row candidate-row"
            @click="handleRowClick(candidate)"
          >
            <!-- Candidate Info -->
            <div class="grid-cell candidate-cell">
              <div class="candidate-info">
                <Avatar 
                  :image="candidate.can_avatar" 
                  :label="getInitials(candidate.can_full_name)"
                  size="md"
                  class="candidate-avatar"
                />
                <div class="candidate-details">
                  <div class="candidate-name">{{ candidate.can_full_name }}</div>
                  <div v-if="candidate.can_last_workplace" class="candidate-company">
                    {{ candidate.can_last_workplace }}
                  </div>
                </div>
              </div>
            </div>
  
            <!-- Contact Info -->
            <div class="grid-cell contact-cell">
              <div class="contact-info">
                <div class="contact-email">
                  <FeatherIcon name="mail" class="contact-icon" />
                  <a :href="`mailto:${candidate.can_email}`" class="contact-link">
                    {{ candidate.can_email }}
                  </a>
                </div>
                <div v-if="candidate.can_phone" class="contact-phone">
                  <FeatherIcon name="phone" class="contact-icon" />
                  <a :href="`tel:${candidate.can_phone}`" class="contact-link">
                    {{ candidate.can_phone }}
                  </a>
                </div>
              </div>
            </div>
  
            <!-- Status Info -->
            <div class="grid-cell status-cell">
              <div class="status-info">
                <Badge 
                  :label="getCurrentStageName(candidate)"
                  :color="getBadgeColor(getStageColor(candidate))"
                  size="md"
                  class="status-badge"
                />
                <div class="step-info">
                  {{ getCurrentStepName(candidate) }}
                </div>
              </div>
            </div>
  
            <!-- Application Date -->
            <div class="grid-cell date-cell">
              <div class="date-info">
                <div class="date-value">{{ formatDate(candidate.can_application_date) }}</div>
                <div class="date-relative">{{ getRelativeDate(candidate.can_application_date) }}</div>
              </div>
            </div>
  
            <!-- Score -->
            <div class="grid-cell score-cell">
              <div v-if="candidate.match_score" class="score-container">
                <div class="score-value" :class="getScoreClass(candidate.match_score)">
                  {{ candidate.match_score }}%
                </div>
                <div class="score-bar">
                  <div 
                    class="score-fill" 
                    :class="getScoreClass(candidate.match_score)"
                    :style="{ width: `${candidate.match_score}%` }"
                  ></div>
                </div>
              </div>
              <span v-else class="text-gray-500">-</span>
            </div>
  
            <!-- Actions -->
            <div class="grid-cell actions-cell" @click.stop>
              <div class="action-buttons">
                <Button 
                  variant="ghost" 
                  @click="$emit('viewCandidate', candidate)"
                  class="action-btn"
                  title="View Details"
                >
                  <FeatherIcon name="eye" class="h-4 w-4" />
                </Button>
                
                <Button 
                  variant="ghost" 
                  @click="$emit('editCandidate', candidate)"
                  class="action-btn"
                  title="Edit"
                >
                  <FeatherIcon name="edit" class="h-4 w-4" />
                </Button>
                
                <Button 
                  variant="ghost" 
                  @click="$emit('sendEmail', candidate)"
                  class="action-btn"
                  title="Send Email"
                >
                  <FeatherIcon name="mail" class="h-4 w-4" />
                </Button>
                
                <Dropdown :options="getMoveOptions(candidate)" class="move-dropdown">
                  <template #default>
                    <Button variant="ghost" class="action-btn" title="Move to Step">
                      <FeatherIcon name="move" class="h-4 w-4" />
                    </Button>
                  </template>
                </Dropdown>
              </div>
            </div>
          </div>
  
          <!-- Empty State -->
          <div v-if="filteredCandidates.length === 0" class="empty-state">
            <div class="empty-content">
              <FeatherIcon name="users" class="empty-icon" />
              <h3 class="empty-title">No candidates found</h3>
              <p class="empty-description">
                {{ searchQuery || selectedStage || selectedStep ? 'Try adjusting your filters' : 'No candidates available for this job' }}
              </p>
              <Button v-if="searchQuery || selectedStage || selectedStep" variant="outline" @click="clearFilters">
                {{__("Clear Filters")}}
              </Button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Pagination Footer -->
      <div v-if="!isLoading && filteredCandidates.length > 0" class="pagination-footer">
        <div class="pagination-info">
          {{__("Showing")}} {{ (currentPage - 1) * pageSize + 1 }} to {{ Math.min(currentPage * pageSize, filteredCandidates.length) }} {{__("of")}} {{ filteredCandidates.length }} {{__("results")}}
        </div>
        
        <div class="pagination-controls">
          <Button 
            variant="outline"
            @click="currentPage = 1" 
            :disabled="currentPage === 1"
            size="sm"
          >
            <FeatherIcon name="chevrons-left" class="h-4 w-4" />
          </Button>
          
          <Button 
            variant="outline"
            @click="currentPage--" 
            :disabled="currentPage === 1"
            size="sm"
          >
            <FeatherIcon name="chevron-left" class="h-4 w-4" />
          </Button>
          
          <span class="pagination-current">{{ currentPage }} of {{ totalPages }}</span>
          
          <Button 
            variant="outline"
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            size="sm"
          >
            <FeatherIcon name="chevron-right" class="h-4 w-4" />
          </Button>
          
          <Button 
            variant="outline"
            @click="currentPage = totalPages" 
            :disabled="currentPage === totalPages"
            size="sm"
          >
            <FeatherIcon name="chevrons-right" class="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch } from 'vue'
  import { 
    Button, 
    FormControl, 
    Badge, 
    Avatar, 
    Dropdown, 
    FeatherIcon, 
    LoadingIndicator 
  } from 'frappe-ui'
  
  // Props
  const props = defineProps({
    candidates: { type: Array, default: () => [] },
    stepColumns: { type: Array, default: () => [] },
    stageSummaries: { type: Array, default: () => [] },
    isLoading: { type: Boolean, default: false }
  })
  
  // Emits
  const emit = defineEmits([
    'viewCandidate',
    'editCandidate', 
    'viewCV',
    'sendEmail',
    'scheduleInterview',
    'moveToStep'
  ])
  
  // Reactive state
  const searchQuery = ref('')
  const selectedStage = ref('')
  const selectedStep = ref('')
  const sortField = ref('can_application_date')
  const sortOrder = ref('desc')
  const currentPage = ref(1)
  const pageSize = ref(25)
  
  // Options for dropdowns
  const stageOptions = computed(() => [
    { label: __('All Stages'), value: '' },
    ...props.stageSummaries.map(stage => ({
      label: `${stage.stage_name} (${stage.candidate_count})`,
      value: stage.stage_name
    }))
  ])
  
  const stepOptions = computed(() => [
    { label: __('All Steps'), value: '' },
    ...props.stepColumns.map(step => ({
      label: step.step_name,
      value: step.step_key
    }))
  ])
  
  const pageSizeOptions = [
    { label: '25', value: 25 },
    { label: '50', value: 50 },
    { label: '100', value: 100 }
  ]
  
  // Computed properties
  const filteredCandidates = computed(() => {
    let filtered = [...props.candidates]
    
    // Search filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      filtered = filtered.filter(candidate => 
        candidate.can_full_name?.toLowerCase().includes(query) ||
        candidate.can_email?.toLowerCase().includes(query) ||
        candidate.can_phone?.includes(query) ||
        candidate.can_last_workplace?.toLowerCase().includes(query)
      )
    }
    
    // Stage filter
    if (selectedStage.value) {
      filtered = filtered.filter(candidate => 
        getCurrentStageName(candidate) === selectedStage.value
      )
    }
    
    // Step filter
    if (selectedStep.value) {
      filtered = filtered.filter(candidate => 
        candidate.step_id === selectedStep.value ||
        candidate.current_step === selectedStep.value ||
        candidate.recruitment_step === selectedStep.value
      )
    }
    
    // Sort
    if (sortField.value) {
      filtered.sort((a, b) => {
        let aVal = a[sortField.value]
        let bVal = b[sortField.value]
        
        // Handle dates
        if (sortField.value.includes('date')) {
          aVal = new Date(aVal || 0)
          bVal = new Date(bVal || 0)
        }
        
        // Handle strings
        if (typeof aVal === 'string') {
          aVal = aVal.toLowerCase()
          bVal = bVal?.toLowerCase() || ''
        }
        
        if (sortOrder.value === 'asc') {
          return aVal > bVal ? 1 : -1
        } else {
          return aVal < bVal ? 1 : -1
        }
      })
    }
    
    return filtered
  })
  
  const paginatedCandidates = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return filteredCandidates.value.slice(start, end)
  })
  
  const totalPages = computed(() => {
    return Math.ceil(filteredCandidates.value.length / pageSize.value)
  })
  
  // Methods
  const sortBy = (field) => {
    if (sortField.value === field) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
      sortField.value = field
      sortOrder.value = 'asc'
    }
  }
  
  const getInitials = (name) => {
    if (!name) return '??'
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
  }
  
  const getCurrentStageName = (candidate) => {
    const step = props.stepColumns.find(s => 
      s.step_key === candidate.step_id ||
      s.step_key === candidate.current_step ||
      s.step_key === candidate.recruitment_step
    )
    return step?.stage_name || 'Unknown'
  }
  
  const getCurrentStepName = (candidate) => {
    const step = props.stepColumns.find(s => 
      s.step_key === candidate.step_id ||
      s.step_key === candidate.current_step ||
      s.step_key === candidate.recruitment_step
    )
    return step?.step_name || 'Unknown'
  }
  
  const getStageColor = (candidate) => {
    const stageName = getCurrentStageName(candidate)
    const stage = props.stageSummaries.find(s => s.stage_name === stageName)
    return stage?.color || '#6b7280'
  }
  
  const getBadgeColor = (hexColor) => {
    // Convert hex to badge color names
    const colorMap = {
      '#2563eb': 'blue',
      '#7c3aed': 'purple', 
      '#dc2626': 'red',
      '#059669': 'green',
      '#ea580c': 'orange',
      '#0891b2': 'cyan'
    }
    return colorMap[hexColor] || 'gray'
  }
  
  const getScoreClass = (score) => {
    if (score >= 80) return 'score-high'
    if (score >= 60) return 'score-medium'
    return 'score-low'
  }
  
  const formatDate = (date) => {
    if (!date) return '-'
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    })
  }
  
  const getRelativeDate = (date) => {
    if (!date) return ''
    const now = new Date()
    const diffTime = Math.abs(now - new Date(date))
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays === 1) return 'Yesterday'
    if (diffDays < 7) return `${diffDays} days ago`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
    return `${Math.floor(diffDays / 30)} months ago`
  }
  
  const getMoveOptions = (candidate) => {
    return props.stepColumns.map(step => ({
      label: `${step.step_name} (${step.stage_name})`,
      onClick: () => moveToStep(candidate, step),
      disabled: isCurrentStep(candidate, step)
    }))
  }
  
  const isCurrentStep = (candidate, step) => {
    return candidate.step_id === step.step_key ||
           candidate.current_step === step.step_key ||
           candidate.recruitment_step === step.step_key
  }
  
  const moveToStep = (candidate, targetStep) => {
    emit('moveToStep', {
      candidate: candidate,
      toStep: targetStep.step_key,
      targetStep: targetStep
    })
  }
  
  const handleRowClick = (candidate) => {
    emit('viewCandidate', candidate)
  }
  
  const clearFilters = () => {
    searchQuery.value = ''
    selectedStage.value = ''
    selectedStep.value = ''
  }
  
  const exportToCSV = () => {
    const headers = [__('Name'), __('Email'), __('Phone'), __('Current Stage'), __('Current Step'), __('Applied Date'), __('Score')]
    const rows = filteredCandidates.value.map(candidate => [
      candidate.can_full_name || '',
      candidate.can_email || '',
      candidate.can_phone || '',
      getCurrentStageName(candidate),
      getCurrentStepName(candidate),
      formatDate(candidate.can_application_date),
      candidate.match_score || ''
    ])
    
    const csvContent = [headers, ...rows]
      .map(row => row.map(field => `"${field}"`).join(','))
      .join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.setAttribute('hidden', '')
    a.setAttribute('href', url)
    a.setAttribute('download', `candidates-${new Date().toISOString().split('T')[0]}.csv`)
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }
  
  // Watchers
  watch([searchQuery, selectedStage, selectedStep], () => {
    currentPage.value = 1
  })
  
  watch(pageSize, () => {
    currentPage.value = 1
  })
  </script>
  
  <style scoped>
  .candidate-list-container {
    @apply h-full flex flex-col bg-white border border-gray-200 rounded-lg;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
  }
  
  .list-header {
    @apply flex-shrink-0 p-4 border-b border-gray-200 bg-gray-50;
  }
  
  .search-input {
    @apply w-64 pl-9 pr-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
  }
  
  .search-icon {
    @apply absolute left-3 top-2.5 h-4 w-4 text-gray-400;
  }
  
  .filter-control {
    @apply w-40;
  }
  
  .page-size-control {
    @apply w-20;
  }
  
  .results-count {
    @apply text-sm text-gray-600 font-medium;
  }
  
  .grid-container {
    @apply flex-1 flex flex-col overflow-hidden;
  }
  
  .loading-overlay {
    @apply flex-1 flex items-center justify-center;
  }
  
  .loading-content {
    @apply flex items-center gap-3 text-gray-600;
  }
  
  .loading-text {
    @apply text-sm font-medium;
  }
  
  .grid-header {
    @apply flex-shrink-0 bg-gray-50 border-b border-gray-200;
  }
  
  .grid-body {
    @apply flex-1 overflow-y-auto;
  }
  
  .grid-row {
    @apply grid grid-cols-6 gap-4 px-4 py-3;
  }
  
  .header-row {
    @apply py-3;
  }
  
  .candidate-row {
    @apply border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors;
  }
  
  .grid-cell {
    @apply flex items-center;
  }
  
  .header-cell {
    @apply text-xs font-semibold text-gray-700 uppercase tracking-wider cursor-pointer hover:text-gray-900 flex items-center gap-2;
  }
  
  .sort-icon {
    @apply h-4 w-4 text-gray-400;
  }
  
  .candidate-info {
    @apply flex items-center gap-3;
  }
  
  .candidate-details {
    @apply min-w-0 flex-1;
  }
  
  .candidate-name {
    @apply text-sm font-semibold text-gray-900 truncate;
  }
  
  .candidate-company {
    @apply text-xs text-gray-500 truncate;
  }
  
  .contact-info {
    @apply space-y-1;
  }
  
  .contact-email,
  .contact-phone {
    @apply flex items-center gap-2 text-sm;
  }
  
  .contact-icon {
    @apply h-3 w-3 text-gray-400 flex-shrink-0;
  }
  
  .contact-link {
    @apply text-blue-600 hover:text-blue-800 truncate;
  }
  
  .status-info {
    @apply space-y-1;
  }
  
  .step-info {
    @apply text-xs text-gray-500;
  }
  
  .date-info {
    @apply text-sm;
  }
  
  .date-value {
    @apply font-medium text-gray-900;
  }
  
  .date-relative {
    @apply text-xs text-gray-500;
  }
  
  .score-container {
    @apply space-y-1;
  }
  
  .score-value {
    @apply text-sm font-semibold;
  }
  
  .score-high {
    @apply text-green-700;
  }
  
  .score-medium {
    @apply text-yellow-700;
  }
  
  .score-low {
    @apply text-red-700;
  }
  
  .score-bar {
    @apply w-16 h-1.5 bg-gray-200 rounded-full overflow-hidden;
  }
  
  .score-fill {
    @apply h-full transition-all duration-300;
  }
  
  .score-fill.score-high {
    @apply bg-green-500;
  }
  
  .score-fill.score-medium {
    @apply bg-yellow-500;
  }
  
  .score-fill.score-low {
    @apply bg-red-500;
  }
  
  .action-buttons {
    @apply flex items-center gap-1;
  }
  
  .action-btn {
    @apply p-1.5;
  }
  
  .empty-state {
    @apply flex-1 flex items-center justify-center p-8;
  }
  
  .empty-content {
    @apply text-center space-y-4;
  }
  
  .empty-icon {
    @apply h-12 w-12 text-gray-300 mx-auto;
  }
  
  .empty-title {
    @apply text-lg font-semibold text-gray-900;
  }
  
  .empty-description {
    @apply text-sm text-gray-500 max-w-sm;
  }
  
  .pagination-footer {
    @apply flex-shrink-0 flex items-center justify-between px-4 py-3 border-t border-gray-200 bg-white;
  }
  
  .pagination-info {
    @apply text-sm text-gray-700;
  }
  
  .pagination-controls {
    @apply flex items-center gap-2;
  }
  
  .pagination-current {
    @apply px-3 text-sm font-medium text-gray-900;
  }
  </style>