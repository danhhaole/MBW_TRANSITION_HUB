<template>
  <v-container fluid class="pa-6">
    <!-- Back Button -->
    <div class="mb-4">
      <v-btn
        variant="text"
        prepend-icon="mdi-arrow-left"
        @click="$router.back()"
        class="text-none"
      >
        Back to Talent Pools
      </v-btn>
    </div>

    <!-- Header -->
    <div class="d-flex align-center justify-space-between mb-6">
      <div class="d-flex align-center">
        <v-avatar size="40" color="primary" class="mr-3">
          <v-icon color="white">mdi-code-tags</v-icon>
        </v-avatar>
        <div>
          <h1 class="text-h5 font-weight-bold mb-1">{{ segmentTitle }}</h1>
          <div class="text-body-2 text-medium-emphasis">
            {{ candidateCount }} candidates • Created on {{ formatCreationDate(creationDate) }}
          </div>
        </div>
      </div>
      
      <div class="d-flex align-center">
        <v-btn
          variant="outlined"
          prepend-icon="mdi-download"
          class="mr-2"
          @click="exportData"
        >
          Export
        </v-btn>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn
              v-bind="props"
              variant="outlined"
              append-icon="mdi-chevron-down"
            >
              More
            </v-btn>
          </template>
          <v-list density="compact">
            <v-list-item @click="editSegment">
              <template v-slot:prepend>
                <v-icon size="18">mdi-pencil</v-icon>
              </template>
              <v-list-item-title>Edit Pool</v-list-item-title>
            </v-list-item>
            <v-list-item @click="duplicateSegment">
              <template v-slot:prepend>
                <v-icon size="18">mdi-content-copy</v-icon>
              </template>
              <v-list-item-title>Duplicate</v-list-item-title>
            </v-list-item>
            <v-divider />
            <v-list-item @click="deleteSegment" class="text-error">
              <template v-slot:prepend>
                <v-icon size="18" color="error">mdi-delete</v-icon>
              </template>
              <v-list-item-title>Delete Pool</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>

    <!-- Stats Cards -->
    <v-row class="mb-6">
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="primary" class="h-100">
          <v-card-text class="pa-4">
            <div class="text-caption text-medium-emphasis mb-1">Total Candidates</div>
            <div class="text-h4 font-weight-bold mb-2">{{ candidateCount }}</div>
            <div class="text-caption text-success">
              <v-icon size="14" class="mr-1">mdi-trending-up</v-icon>
              +{{ newCandidatesThisMonth }} this month
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="success" class="h-100">
          <v-card-text class="pa-4">
            <div class="text-caption text-medium-emphasis mb-1">Engagement Rate</div>
            <div class="text-h4 font-weight-bold mb-2">{{ engagementRate }}%</div>
            <div class="text-caption text-success">
              <v-icon size="14" class="mr-1">mdi-trending-up</v-icon>
              +{{ engagementChange }}% from last month
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="purple" class="h-100">
          <v-card-text class="pa-4">
            <div class="text-caption text-medium-emphasis mb-1">Active Campaigns</div>
            <div class="text-h4 font-weight-bold mb-2">{{ activeCampaigns }}</div>
            <div class="text-caption text-warning">
              <v-icon size="14" class="mr-1">mdi-clock-outline</v-icon>
              {{ pendingApprovals }} pending approval
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="3">
        <v-card variant="tonal" color="orange" class="h-100">
          <v-card-text class="pa-4">
            <div class="text-caption text-medium-emphasis mb-1">Avg. Response Time</div>
            <div class="text-h4 font-weight-bold mb-2">{{ avgResponseTime }} days</div>
            <div class="text-caption text-success">
              <v-icon size="14" class="mr-1">mdi-trending-down</v-icon>
              {{ responseTimeChange }} days from last month
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Action Buttons -->
    <div class="d-flex flex-wrap ga-3 mb-6">
      <v-btn
        color="purple"
        variant="elevated"
        prepend-icon="mdi-plus"
        @click="createCampaign"
      >
        Create Campaign
      </v-btn>
      
      <v-btn
        color="blue"
        variant="elevated"
        prepend-icon="mdi-account-plus"
        @click="addCandidates"
      >
        Add Candidates
      </v-btn>
      
      <v-btn
        color="green"
        variant="elevated"
        prepend-icon="mdi-calendar-clock"
        @click="scheduleNurturing"
      >
        Schedule Nurturing
      </v-btn>
      
      <v-btn
        color="purple"
        variant="elevated"
        prepend-icon="mdi-chart-line"
        @click="viewAnalytics"
      >
        Analytics
      </v-btn>
    </div>

    <!-- Candidates Table -->
    <v-card variant="outlined">
      <v-card-title class="d-flex align-center justify-space-between pa-4">
        <span class="text-h6">Candidates in this Pool</span>
        <div class="d-flex align-center">
          <v-text-field
            v-model="candidateSearch"
            placeholder="Search candidates..."
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            density="compact"
            hide-details
            style="max-width: 300px;"
            class="mr-2"
          />
          <v-btn
            variant="outlined"
            prepend-icon="mdi-filter"
            @click="showFilters = !showFilters"
          >
            Filter
          </v-btn>
        </div>
      </v-card-title>

      <!-- Filters (Collapsible) -->
      <v-expand-transition>
        <div v-show="showFilters" class="pa-4 border-b">
          <v-row dense>
            <v-col cols="12" md="3">
              <v-select
                v-model="statusFilter"
                :items="statusOptions"
                label="Status"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="skillFilter"
                :items="skillOptions"
                label="Skills"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="engagementFilter"
                :items="engagementOptions"
                label="Engagement"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-btn
                variant="text"
                @click="clearFilters"
                class="mt-1"
              >
                Clear Filters
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </v-expand-transition>

      <v-data-table
        :headers="candidateHeaders"
        :items="filteredCandidates"
        :loading="loadingCandidates"
        :search="candidateSearch"
        item-key="id"
        class="elevation-0"
        :items-per-page="10"
        loading-text="Loading candidates..."
        no-data-text="No candidates found"
      >
        <!-- Candidate column -->
        <template v-slot:item.candidate="{ item }">
          <div class="d-flex align-center">
            <v-avatar size="40" :color="getAvatarColor(item.name)" class="mr-3">
              <span class="text-body-2 text-white">
                {{ getAvatarText(item.name) }}
              </span>
            </v-avatar>
            <div>
              <div class="font-weight-medium">{{ item.name }}</div>
              <div class="text-caption text-medium-emphasis">{{ item.email }}</div>
            </div>
          </div>
        </template>

        <!-- Skills column -->
        <template v-slot:item.skills="{ item }">
          <div class="d-flex flex-wrap ga-1">
            <v-chip
              v-for="skill in item.skills"
              :key="skill"
              size="x-small"
              :color="getSkillColor(skill)"
              variant="tonal"
            >
              {{ skill }}
            </v-chip>
          </div>
        </template>

        <!-- Last Contact column -->
        <template v-slot:item.lastContact="{ item }">
          <div class="text-body-2">{{ formatRelativeTime(item.lastContact) }}</div>
        </template>

        <!-- Engagement column -->
        <template v-slot:item.engagement="{ item }">
          <div class="d-flex align-center" style="min-width: 120px;">
            <v-progress-linear
              :model-value="item.engagement"
              height="8"
              rounded
              :color="getEngagementColor(item.engagement)"
              class="flex-grow-1 mr-2"
            />
            <span class="text-body-2 font-weight-medium">{{ item.engagement }}%</span>
          </div>
        </template>

        <!-- Status column -->
        <template v-slot:item.status="{ item }">
          <v-chip
            size="small"
            :color="getStatusColor(item.status)"
            variant="tonal"
          >
            {{ item.status }}
          </v-chip>
        </template>

        <!-- Actions column -->
        <template v-slot:item.actions="{ item }">
          <div class="d-flex align-center">
            <v-btn
              color="blue"
              variant="text"
              size="small"
              @click="viewCandidate(item)"
              class="mr-1"
            >
              View
            </v-btn>
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn
                  v-bind="props"
                  variant="text"
                  icon="mdi-dots-vertical"
                  size="small"
                />
              </template>
              <v-list density="compact">
                <v-list-item @click="viewCandidate(item)">
                  <template v-slot:prepend>
                    <v-icon size="18">mdi-eye</v-icon>
                  </template>
                  <v-list-item-title>View Profile</v-list-item-title>
                </v-list-item>
                <v-list-item @click="contactCandidate(item)">
                  <template v-slot:prepend>
                    <v-icon size="18">mdi-email</v-icon>
                  </template>
                  <v-list-item-title>Send Message</v-list-item-title>
                </v-list-item>
                <v-list-item @click="addToCampaign(item)">
                  <template v-slot:prepend>
                    <v-icon size="18">mdi-plus-circle</v-icon>
                  </template>
                  <v-list-item-title>Add to Campaign</v-list-item-title>
                </v-list-item>
                <v-divider />
                <v-list-item @click="removeFromPool(item)" class="text-error">
                  <template v-slot:prepend>
                    <v-icon size="18" color="error">mdi-delete</v-icon>
                  </template>
                  <v-list-item-title>Remove from Pool</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </template>

        <!-- Bottom pagination -->
        <template v-slot:bottom="{ page, pageCount, itemsPerPage, itemsLength, updateOptions }">
          <div class="d-flex justify-space-between align-center pa-4">
            <div class="text-body-2 text-medium-emphasis">
              Showing {{ Math.min((page - 1) * itemsPerPage + 1, itemsLength) }} to {{ Math.min(page * itemsPerPage, itemsLength) }} of {{ itemsLength }} candidates
            </div>
            <v-pagination
              :model-value="page"
              @update:model-value="(newPage) => updateOptions({ page: newPage })"
              :length="pageCount"
              :total-visible="7"
              size="small"
              variant="outlined"
            />
          </div>
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

// Route params
const route = useRoute()
const segmentId = route.params.id

// State
const loadingCandidates = ref(false)
const candidateSearch = ref('')
const showFilters = ref(false)
const statusFilter = ref('all')
const skillFilter = ref('all')
const engagementFilter = ref('all')

// Static data (replace with API calls)
const segmentTitle = ref('Software Developers')
const candidateCount = ref(248)
const creationDate = ref('2023-05-15')
const newCandidatesThisMonth = ref(12)
const engagementRate = ref(78)
const engagementChange = ref(5)
const activeCampaigns = ref(3)
const pendingApprovals = ref(1)
const avgResponseTime = ref(2.4)
const responseTimeChange = ref(-0.5)

// Sample candidates data
const candidates = ref([
  {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@example.com',
    skills: ['React', 'Node.js', 'TypeScript'],
    lastContact: '2024-01-10',
    engagement: 85,
    status: 'Active'
  },
  {
    id: 2,
    name: 'Tran Nguyen',
    email: 'tran.nguyen@example.com',
    skills: ['React', 'Vue.js', 'AWS'],
    lastContact: '2024-01-03',
    engagement: 65,
    status: 'Nurturing'
  },
  {
    id: 3,
    name: 'Kim Lee',
    email: 'kim.lee@example.com',
    skills: ['React Native', 'Node.js', 'GraphQL'],
    lastContact: '2024-01-12',
    engagement: 90,
    status: 'Active'
  }
])

// Table headers
const candidateHeaders = [
  { title: 'CANDIDATE', key: 'candidate', sortable: true, width: '25%' },
  { title: 'SKILLS', key: 'skills', sortable: false, width: '20%' },
  { title: 'LAST CONTACT', key: 'lastContact', sortable: true, width: '15%' },
  { title: 'ENGAGEMENT', key: 'engagement', sortable: true, width: '15%' },
  { title: 'STATUS', key: 'status', sortable: true, width: '12%' },
  { title: 'ACTIONS', key: 'actions', sortable: false, width: '13%', align: 'center' }
]

// Filter options
const statusOptions = [
  { title: 'All Statuses', value: 'all' },
  { title: 'Active', value: 'Active' },
  { title: 'Nurturing', value: 'Nurturing' },
  { title: 'Inactive', value: 'Inactive' }
]

const skillOptions = [
  { title: 'All Skills', value: 'all' },
  { title: 'React', value: 'React' },
  { title: 'Node.js', value: 'Node.js' },
  { title: 'TypeScript', value: 'TypeScript' },
  { title: 'Vue.js', value: 'Vue.js' }
]

const engagementOptions = [
  { title: 'All Levels', value: 'all' },
  { title: 'High (80%+)', value: 'high' },
  { title: 'Medium (50-79%)', value: 'medium' },
  { title: 'Low (<50%)', value: 'low' }
]

// Computed
const filteredCandidates = computed(() => {
  let filtered = candidates.value

  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(c => c.status === statusFilter.value)
  }

  if (skillFilter.value !== 'all') {
    filtered = filtered.filter(c => c.skills.includes(skillFilter.value))
  }

  if (engagementFilter.value !== 'all') {
    if (engagementFilter.value === 'high') {
      filtered = filtered.filter(c => c.engagement >= 80)
    } else if (engagementFilter.value === 'medium') {
      filtered = filtered.filter(c => c.engagement >= 50 && c.engagement < 80)
    } else if (engagementFilter.value === 'low') {
      filtered = filtered.filter(c => c.engagement < 50)
    }
  }

  return filtered
})

// Helper functions
const formatCreationDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatRelativeTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffInDays === 0) return 'today'
  if (diffInDays === 1) return '1 day ago'
  if (diffInDays < 7) return `${diffInDays} days ago`
  if (diffInDays < 14) return '1 week ago'
  return `${Math.floor(diffInDays / 7)} weeks ago`
}

const getAvatarColor = (name) => {
  const colors = ['primary', 'secondary', 'accent', 'info', 'warning', 'error', 'success']
  const hash = name.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const getAvatarText = (name) => {
  return name.split(' ').map(word => word[0]).join('').toUpperCase().substring(0, 2)
}

const getSkillColor = (skill) => {
  const skillColors = {
    'React': 'blue',
    'Node.js': 'green',
    'TypeScript': 'blue',
    'Vue.js': 'green',
    'AWS': 'orange',
    'GraphQL': 'pink',
    'React Native': 'purple'
  }
  return skillColors[skill] || 'grey'
}

const getEngagementColor = (engagement) => {
  if (engagement >= 80) return 'success'
  if (engagement >= 50) return 'warning'
  return 'error'
}

const getStatusColor = (status) => {
  const statusColors = {
    'Active': 'success',
    'Nurturing': 'warning',
    'Inactive': 'grey'
  }
  return statusColors[status] || 'grey'
}

// Event handlers
const exportData = () => {
  console.log('Export data')
}

const editSegment = () => {
  console.log('Edit segment')
}

const duplicateSegment = () => {
  console.log('Duplicate segment')
}

const deleteSegment = () => {
  console.log('Delete segment')
}

const createCampaign = () => {
  console.log('Create campaign')
}

const addCandidates = () => {
  console.log('Add candidates')
}

const scheduleNurturing = () => {
  console.log('Schedule nurturing')
}

const viewAnalytics = () => {
  console.log('View analytics')
}

const viewCandidate = (candidate) => {
  console.log('View candidate:', candidate)
}

const contactCandidate = (candidate) => {
  console.log('Contact candidate:', candidate)
}

const addToCampaign = (candidate) => {
  console.log('Add to campaign:', candidate)
}

const removeFromPool = (candidate) => {
  console.log('Remove from pool:', candidate)
}

const clearFilters = () => {
  statusFilter.value = 'all'
  skillFilter.value = 'all'
  engagementFilter.value = 'all'
}

// Initialize
onMounted(() => {
  // Load segment data based on segmentId
  console.log('Loading segment:', segmentId)
})
</script>

<style scoped>
/* Custom styling */
.border-b {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

/* Avatar text color fix */
.v-avatar .white--text {
  color: white !important;
}

/* Stats cards styling */
.v-card.v-card--variant-tonal {
  background-color: rgba(var(--v-theme-surface), 0.04);
}

/* Progress bar styling */
:deep(.v-progress-linear) {
  border-radius: 4px;
}

/* Table styling */
:deep(.v-data-table) {
  border-radius: 0;
}

:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
  text-transform: uppercase;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* Action buttons */
.v-btn {
  text-transform: none;
  font-weight: 500;
}

/* Pagination styling */
:deep(.v-pagination) {
  justify-content: center;
}
</style> 