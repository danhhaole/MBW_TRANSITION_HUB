<template>
  <div>
    <!-- Debug/Admin Toggle -->
    <v-row v-if="showDebugToggle" class="mb-4">
      <v-col cols="12">
        <v-card variant="outlined" class="pa-4">
          <div class="d-flex align-center justify-space-between">
            <div>
              <h4 class="text-h6">Debug Mode</h4>
              <p class="text-caption text-medium-emphasis mb-0">Show detailed segment data structure</p>
            </div>
            <v-switch 
              v-model="showDebugView"
              color="primary"
              hide-details
              @change="toggleDebugView"
            />
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Debug View - Full Data Structure -->
    <v-row v-if="showDebugView" class="mb-4">
      <v-col cols="12">
        <v-card variant="outlined" class="pa-4">
          <div class="d-flex align-center justify-space-between mb-4">
            <h4 class="text-h6">Segment Data Structure</h4>
            <v-btn 
              icon="mdi-close" 
              size="small" 
              variant="text"
              @click="showDebugView = false"
            />
          </div>
          
          <v-expansion-panels multiple>
            <v-expansion-panel
              v-for="(segment, index) in segments"
              :key="segment.name"
              :title="`${segment.title || segment.name} - Debug Data`"
              :value="index"
            >
              <template v-slot:text>
                <div class="debug-data-container">
                  <v-row>
                    <!-- Basic Fields -->
                    <v-col cols="12" md="6">
                      <v-card variant="tonal" class="pa-3 mb-3">
                        <h6 class="text-subtitle-1 mb-2">Basic Information</h6>
                        <div class="debug-field-group">
                          <div class="debug-field">
                            <strong>Name:</strong> {{ segment.name }}
                          </div>
                          <div class="debug-field">
                            <strong>Title:</strong> {{ segment.title }}
                          </div>
                          <div class="debug-field">
                            <strong>Description:</strong> {{ segment.description || 'N/A' }}
                          </div>
                          <div class="debug-field">
                            <strong>Type:</strong> 
                            <v-chip size="small" :color="getTypeColor(segment.type)">
                              {{ getTypeLabel(segment.type) }}
                            </v-chip>
                          </div>
                          <div class="debug-field">
                            <strong>Candidate Count:</strong> {{ segment.candidate_count || 0 }}
                          </div>
                          <div class="debug-field">
                            <strong>Owner ID:</strong> {{ segment.owner_id || 'N/A' }}
                          </div>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Timestamps -->
                    <v-col cols="12" md="6">
                      <v-card variant="tonal" class="pa-3 mb-3">
                        <h6 class="text-subtitle-1 mb-2">Timestamps</h6>
                        <div class="debug-field-group">
                          <div class="debug-field">
                            <strong>Created:</strong> {{ formatDate(segment.creation) }}
                          </div>
                          <div class="debug-field">
                            <strong>Modified:</strong> {{ formatDate(segment.modified) }}
                          </div>
                          <div class="debug-field">
                            <strong>Relative Time:</strong> {{ formatRelativeTime(segment.modified) }}
                          </div>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Criteria JSON -->
                    <v-col cols="12">
                      <v-card variant="tonal" class="pa-3 mb-3">
                        <h6 class="text-subtitle-1 mb-2">Criteria JSON</h6>
                        <div class="debug-field">
                          <pre class="debug-json">{{ formatCriteria(segment.criteria) }}</pre>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Top Skills -->
                    <v-col cols="12" md="6">
                      <v-card variant="tonal" class="pa-3 mb-3">
                        <h6 class="text-subtitle-1 mb-2">Top Skills ({{ segment.topSkills?.length || 0 }})</h6>
                        <div v-if="segment.topSkills && segment.topSkills.length > 0" class="debug-field-group">
                          <div class="d-flex flex-wrap ga-1">
                            <v-chip 
                              v-for="skill in segment.topSkills"
                              :key="skill"
                              size="small"
                              color="primary"
                              variant="tonal"
                            >
                              {{ skill }}
                            </v-chip>
                          </div>
                        </div>
                        <div v-else class="text-caption text-medium-emphasis">
                          No skills data available
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Team Members -->
                    <v-col cols="12" md="6">
                      <v-card variant="tonal" class="pa-3 mb-3">
                        <h6 class="text-subtitle-1 mb-2">Team Members ({{ segment.teamMembers?.length || 0 }})</h6>
                        <div v-if="segment.teamMembers && segment.teamMembers.length > 0" class="debug-field-group">
                          <div 
                            v-for="(member, memberIndex) in segment.teamMembers" 
                            :key="memberIndex"
                            class="debug-member-card"
                          >
                            <div class="d-flex align-center mb-2">
                              <v-avatar 
                                size="32" 
                                :color="getAvatarColor(member.candidate_name || member.name)"
                                class="mr-2"
                              >
                                <span class="text-caption white--text">
                                  {{ getAvatarText(member.candidate_name || member.name) }}
                                </span>
                              </v-avatar>
                              <div>
                                <div class="text-body-2 font-weight-medium">
                                  {{ member.candidate_name || member.name }}
                                </div>
                                <div class="text-caption text-medium-emphasis">
                                  {{ member.email || 'N/A' }}
                                </div>
                              </div>
                            </div>
                            <div class="debug-field-group ml-10">
                              <div class="debug-field">
                                <strong>Phone:</strong> {{ member.phone || 'N/A' }}
                              </div>
                              <div class="debug-field">
                                <strong>Status:</strong> {{ member.status || 'N/A' }}
                              </div>
                              <div class="debug-field">
                                <strong>Added:</strong> {{ member.added_at || 'N/A' }}
                              </div>
                            </div>
                          </div>
                        </div>
                        <div v-else class="text-caption text-medium-emphasis">
                          No team members data available
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Raw Data -->
                    <v-col cols="12">
                      <v-card variant="tonal" class="pa-3">
                        <div class="d-flex align-center justify-space-between mb-2">
                          <h6 class="text-subtitle-1">Raw JSON Data</h6>
                          <v-btn 
                            size="small" 
                            variant="text"
                            @click="copyToClipboard(segment)"
                          >
                            Copy JSON
                          </v-btn>
                        </div>
                        <pre class="debug-json">{{ JSON.stringify(segment, null, 2) }}</pre>
                      </v-card>
                    </v-col>
                  </v-row>
                </div>
              </template>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Segment Cards -->
      <v-col 
        v-for="segment in segments" 
        :key="segment.name"
        cols="12" 
        md="4" 
        lg="4"
      >
        <v-card 
          class="segment-card h-100"
          variant="default"
          :loading="loading"
          style="border-radius: 12px; overflow: hidden;"
        >
          <!-- Header with solid color -->
          <div 
            class="pa-4 text-white d-flex justify-space-between align-center"
            :style="getHeaderStyle(segment.type)"
          >
            <div class="flex-grow-1">
              <h3 class="text-h6 font-weight-bold mb-2">{{ segment.title }}</h3>
              <div class="text-body-2 opacity-90">
                {{ segment.candidate_count || 0 }} candidates
              </div>
            </div>
          </div>

          <!-- Content -->
          <v-card-text class="pa-4">
            <!-- Last Updated -->
            <div class="d-flex align-center mb-4">
              <v-icon size="16" color="grey">mdi-clock-outline</v-icon>
              <span class="text-caption text-medium-emphasis ml-2">
                Last updated: {{ formatRelativeTime(segment.modified) }}
              </span>
            </div>

            <!-- Top Skills -->
            <div class="mb-4">
              <div class="text-caption text-medium-emphasis mb-2">Top Skills</div>
              <div class="d-flex flex-wrap ga-1" v-if="segment.topSkills && segment.topSkills.length > 0">
                <v-chip 
                  v-for="skill in segment.topSkills.slice(0, 3)"
                  :key="skill"
                  size="x-small" 
                  color="primary"
                  variant="tonal"
                  class="ma-1"
                >
                  {{ skill }}
                </v-chip>
                <v-chip 
                  v-if="segment.topSkills.length > 3"
                  size="x-small" 
                  color="grey"
                  variant="tonal"
                  class="ma-1"
                >
                  +{{ segment.topSkills.length - 3 }}
                </v-chip>
              </div>
              <div v-else class="text-caption text-medium-emphasis">
                No skills data available
              </div>
            </div>

            <!-- Engagement Rate -->
            <div class="mb-4">
              <div class="text-caption text-medium-emphasis mb-2">Engagement Rate</div>
              <div class="d-flex align-center">
                <v-progress-linear
                  :model-value="getEngagementRate(segment)"
                  height="6"
                  rounded
                  :color="getEngagementColor(getEngagementRate(segment))"
                  class="flex-grow-1 mr-3"
                />
                <span class="text-body-2 font-weight-medium">
                  {{ getEngagementRate(segment) }}%
                </span>
              </div>
            </div>

            <!-- Team Members -->
            <div class="d-flex align-center justify-space-between mb-4">
              <div class="d-flex align-center">
                <v-avatar 
                  v-for="(member, index) in segment.teamMembers?.slice(0, 3) || []" 
                  :key="index"
                  size="32" 
                  :color="getAvatarColor(member.candidate_name || member.name)"
                  class="mr-1"
                  style="border: 2px solid white;"
                  :title="member.candidate_name || member.name"
                >
                  <span class="text-caption white--text">
                    {{ getAvatarText(member.candidate_name || member.name) }}
                  </span>
                </v-avatar>
                <v-chip 
                  v-if="segment.candidate_count > 3"
                  size="small"
                  variant="outlined"
                  class="ml-1"
                >
                  +{{ segment.candidate_count - 3 }}
                </v-chip>
                <div v-if="!segment.teamMembers || segment.teamMembers.length === 0" class="text-caption text-medium-emphasis">
                  No candidates yet
                </div>
              </div>
              
              <v-btn
                color="primary"
                variant="text"
                size="small"
                @click="$emit('view-details', segment)"
                class="text-none"
              >
                Manage
              </v-btn>
            </div>
          </v-card-text>


        </v-card>
      </v-col>

      <!-- Create New Pool Card -->
      <v-col cols="12" md="4" lg="4">
        <v-card 
          class="create-card h-100 d-flex align-center justify-center"
          variant="outlined"
          style="border-style: dashed; cursor: pointer; min-height: 260px; border-radius: 12px;"
          @click="$emit('create')"
        >
          <div class="text-center pa-6">
            <div class="d-flex justify-center mb-4">
              <v-icon size="48" color="primary" class="opacity-60">mdi-plus-circle-outline</v-icon>
            </div>
            <h3 class="text-h6 mb-2 font-weight-medium">Create New Pool</h3>
            <p class="text-body-2 text-medium-emphasis">
              Define a new talent segment
            </p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { calculateEngagementRate, formatDate, getSegmentTypeColor } from '@/services/talentSegmentService'
import { processSkills } from '@/services/candidateService'

// Props
const props = defineProps({
  segments: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  showDebugToggle: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['view-details', 'edit', 'delete', 'create'])

// Debug state
const showDebugView = ref(false)

// Methods
const toggleDebugView = () => {
  // Optional: emit event to parent component
  emit('debug-toggle', showDebugView.value)
}

// Helper functions
const getHeaderStyle = (type) => {
  const colors = ['#4F46E5', '#EC4899', '#10B981', '#F59E0B'] // Blue, Pink, Green, Orange
  const index = type === 'DYNAMIC' ? 0 : Math.floor(Math.random() * colors.length)
  return `background-color: ${colors[index]}`
}

const getTypeColor = (type) => {
  return type === 'DYNAMIC' ? 'blue' : 'green'
}

const getTypeLabel = (type) => {
  return type === 'DYNAMIC' ? 'Tự động (AI)' : 'Thủ công'
}

const getEngagementRate = (segment) => {
  return calculateEngagementRate(segment.candidate_count || 0)
}

const getEngagementColor = (rate) => {
  if (rate >= 70) return 'success'
  if (rate >= 40) return 'warning'
  return 'error'
}

const getAvatarColor = (name) => {
  const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
  const hash = name?.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0) || 0
  return colors[Math.abs(hash) % colors.length]
}

const getAvatarText = (name) => {
  if (!name) return ''
  return name.split(' ').map(word => word[0]).join('').toUpperCase().substring(0, 2)
}

const formatRelativeTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'just now'
  if (diffInHours === 1) return '1 hour ago'
  if (diffInHours < 24) return `${diffInHours} hours ago`
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays === 1) return '1 day ago'
  if (diffInDays < 7) return `${diffInDays} days ago`
  
  return formatDate(dateString)
}

const getTopSkills = (segment) => {
  // Return actual top skills from segment data
  return segment.topSkills || []
}

const getTeamMembers = (segment) => {
  // Return actual team members from segment data
  return segment.teamMembers || []
}

const getExtraCount = (segment) => {
  // Calculate extra members beyond the 3 shown
  return Math.max(0, (segment.candidate_count || 0) - 3)
}

const formatCriteria = (criteria) => {
  if (!criteria) return 'No criteria set'
  
  try {
    if (typeof criteria === 'string') {
      return JSON.stringify(JSON.parse(criteria), null, 2)
    }
    return JSON.stringify(criteria, null, 2)
  } catch (e) {
    return criteria
  }
}

const copyToClipboard = async (segment) => {
  try {
    await navigator.clipboard.writeText(JSON.stringify(segment, null, 2))
    // Could emit a success event or show a snackbar
    console.log('Segment data copied to clipboard')
  } catch (err) {
    console.error('Failed to copy to clipboard:', err)
  }
}
</script>

<style scoped>
.segment-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-radius: 12px;
}

.segment-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.create-card {
  transition: all 0.3s ease;
  border-radius: 12px;
}

.create-card:hover {
  transform: translateY(-2px);
  border-color: rgb(var(--v-theme-primary)) !important;
  background-color: rgba(var(--v-theme-primary), 0.04);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom progress bar styling */
.v-progress-linear {
  border-radius: 4px;
}

/* Menu styling */
.v-menu > .v-overlay__content {
  border-radius: 8px;
}

/* Avatar text color fix */
.v-avatar .white--text {
  color: white !important;
}

/* Card content spacing */
.v-card-text {
  padding-top: 16px !important;
  padding-bottom: 0 !important;
}

.v-card-actions {
  padding-top: 0 !important;
}

/* Chip styling */
.v-chip {
  font-weight: 500;
}

/* Icon opacity */
.opacity-75 {
  opacity: 0.75;
}

/* Debug view styles */
.debug-data-container {
  max-height: 600px;
  overflow-y: auto;
}

.debug-field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.debug-field {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 4px 0;
  font-size: 0.875rem;
}

.debug-field strong {
  min-width: 120px;
  color: rgb(var(--v-theme-on-surface));
  font-weight: 600;
}

.debug-json {
  background-color: rgba(var(--v-theme-surface-variant), 0.3);
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
  border-radius: 4px;
  padding: 12px;
  font-family: 'Courier New', monospace;
  font-size: 0.75rem;
  line-height: 1.4;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 300px;
  overflow-y: auto;
}

.debug-member-card {
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 8px;
  background-color: rgba(var(--v-theme-surface), 0.5);
}

.debug-member-card:last-child {
  margin-bottom: 0;
}

/* Expansion panel customization */
.v-expansion-panel-title {
  font-weight: 500;
}

.v-expansion-panel-text {
  padding: 16px !important;
}
</style> 