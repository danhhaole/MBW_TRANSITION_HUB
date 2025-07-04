<template>
  <div>
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
          variant="outlined"
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
              <div class="d-flex flex-wrap ga-1">
                <v-chip 
                  v-for="skill in getTopSkills(segment)"
                  :key="skill"
                  size="x-small" 
                  color="primary"
                  variant="tonal"
                  class="ma-1"
                >
                  {{ skill }}
                </v-chip>
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
                  v-for="(member, index) in getTeamMembers(segment)" 
                  :key="index"
                  size="32" 
                  :color="getAvatarColor(member.name)"
                  class="mr-1"
                  style="border: 2px solid white;"
                >
                  <span class="text-caption white--text">
                    {{ getAvatarText(member.name) }}
                  </span>
                </v-avatar>
                <v-chip 
                  v-if="getExtraCount(segment) > 0"
                  size="small"
                  variant="outlined"
                  class="ml-1"
                >
                  +{{ getExtraCount(segment) }}
                </v-chip>
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
import { computed } from 'vue'
import { calculateEngagementRate, formatDate, getSegmentTypeColor } from '@/services/talentSegmentService'

// Props
const props = defineProps({
  segments: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['view-details', 'edit', 'delete', 'create'])

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
  // Sample skills based on segment type and name
  const skillSets = {
    'Software Developers': ['React', 'Node.js', 'TypeScript'],
    'UX/UI Designers': ['Figma', 'UI Design', 'User Research'],
    'Product Managers': ['Agile', 'Product Strategy', 'Roadmapping'],
    'Data Scientists': ['Python', 'Machine Learning', 'SQL']
  }
  return skillSets[segment.title] || ['JavaScript', 'React', 'Vue.js']
}

const getTeamMembers = (segment) => {
  // Sample team members - in real app this would come from API
  return [
    { name: 'John Doe' },
    { name: 'Jane Smith' },
    { name: 'Alice Brown' }
  ]
}

const getExtraCount = (segment) => {
  // Calculate extra members beyond the 3 shown
  const totalMembers = (segment.candidate_count || 0) / 10 // Rough estimate
  return Math.max(0, Math.floor(totalMembers) - 3)
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
</style> 