<template>
  <div class="talent-segment-detail-view">
    <!-- Header with Talent Segment Info -->
    <div class="page-header bg-white pa-6 mb-6 elevation-1">
      <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            @click="$router.go(-1)"
            class="mr-3"
          />
          <div>
            <h1 class="text-h4 font-weight-bold text-primary mb-2">
              {{ talentSegment.title || 'Loading...' }}
            </h1>
            <div class="d-flex align-center flex-wrap">
              <v-chip 
                :color="getTypeColor(talentSegment.type)"
                variant="tonal"
                class="mr-2 mb-2"
              >
                {{ talentSegment.type }}
              </v-chip>
              <span class="text-body-2 text-medium-emphasis mr-4">
                Created: {{ formatDate(talentSegment.creation) }}
              </span>
              <span class="text-body-2 text-medium-emphasis">
                Modified: {{ formatDate(talentSegment.modified) }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="d-flex align-center">
          <v-btn
            color="primary"
            variant="outlined"
            prepend-icon="mdi-pencil"
            @click="editTalentSegment"
            class="mr-2"
          >
            Edit Segment
          </v-btn>
          <v-btn
            color="error"
            variant="outlined"
            prepend-icon="mdi-delete"
            @click="deleteTalentSegment"
          >
            Delete
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Talent Segment Details Card -->
    <v-card class="mb-6" variant="outlined">
      <v-card-title>
        <v-icon class="mr-2">mdi-account-group</v-icon>
        Talent Segment Information
      </v-card-title>
      <v-card-text>
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <strong>Title:</strong>
              <p class="mb-0">{{ talentSegment.title || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Description:</strong>
              <p class="mb-0">{{ talentSegment.description || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Type:</strong>
              <v-chip 
                :color="getTypeColor(talentSegment.type)"
                variant="tonal"
                size="small"
              >
                {{ talentSegment.type }}
              </v-chip>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <strong>Owner:</strong>
              <p class="mb-0">{{ talentSegment.owner_id || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Candidate Count:</strong>
              <v-chip color="info" variant="tonal" size="small">
                {{ talentSegment.candidate_count || 0 }} candidates
              </v-chip>
            </div>
            <div class="mb-3">
              <strong>Created By:</strong>
              <p class="mb-0">{{ talentSegment.owner || 'N/A' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Criteria (if available) -->
        <div v-if="talentSegment.criteria" class="mt-4">
          <strong>Criteria:</strong>
          <v-card variant="outlined" class="mt-2">
            <v-card-text>
              <pre class="text-body-2">{{ formatCriteria(talentSegment.criteria) }}</pre>
            </v-card-text>
          </v-card>
        </div>
      </v-card-text>
    </v-card>

    <!-- Tabbed Content -->
    <v-card>
      <v-tabs 
        v-model="activeTab" 
        bg-color="primary"
        color="white"
        slider-color="white"
      >
        <v-tab value="candidates">
          <v-icon class="mr-2">mdi-account-multiple</v-icon>
          Candidates ({{ candidates.length }})
        </v-tab>
        <v-tab value="campaigns">
          <v-icon class="mr-2">mdi-chart-timeline-variant</v-icon>
          Related Campaigns
        </v-tab>
        <v-tab value="analytics">
          <v-icon class="mr-2">mdi-chart-line</v-icon>
          Analytics
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- Candidates Tab -->
        <v-window-item value="candidates">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Candidates in this Segment</h3>
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
                  color="primary"
                  prepend-icon="mdi-plus"
                  @click="openAddCandidateModal()"
                >
                  Add Candidate
                </v-btn>
              </div>
            </div>
            
            <!-- Candidates List -->
            <v-data-table
              :headers="candidateHeaders"
              :items="candidates"
              :loading="loadingCandidates"
              :search="candidateSearch"
              item-value="name"
              class="elevation-1"
            >
              <template #item.candidate="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" color="primary" class="mr-2">
                    <span class="text-caption">{{ item.candidate_name?.charAt(0) }}</span>
                  </v-avatar>
                  <div>
                    <div class="font-weight-medium">{{ item.candidate_name }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.email }}</div>
                  </div>
                </div>
              </template>
              
              <template #item.skills="{ item }">
                <div class="d-flex flex-wrap ga-1">
                  <v-chip
                    v-for="skill in processSkills(item.skills)"
                    :key="skill"
                    size="x-small"
                    :color="getSkillColor(skill)"
                    variant="tonal"
                  >
                    {{ skill }}
                  </v-chip>
                </div>
              </template>
              
              <template #item.last_contact="{ item }">
                <div class="text-body-2">
                  {{ formatDateTime(item.last_contact) }}
                </div>
              </template>
              
              <template #item.status="{ item }">
                <v-chip 
                  :color="getStatusColor(item.status)"
                  variant="tonal"
                  size="small"
                >
                  {{ item.status }}
                </v-chip>
              </template>
              
              <template #item.added_at="{ item }">
                <div class="text-body-2">
                  {{ formatDateTime(item.added_at) }}
                </div>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewCandidateDetails(item)"
                />
                <v-btn
                  icon="mdi-email"
                  size="small"
                  variant="text"
                  color="primary"
                  @click="contactCandidate(item)"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="removeFromSegment(item)"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Related Campaigns Tab -->
        <v-window-item value="campaigns">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Related Campaigns</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="showCampaignWizard = true"
              >
                Create Campaign
              </v-btn>
            </div>
            
            <!-- Related Campaigns List -->
            <v-data-table
              :headers="campaignHeaders"
              :items="relatedCampaigns"
              :loading="loadingCampaigns"
              item-value="name"
              class="elevation-1"
            >
              <template #item.campaign_name="{ item }">
                <div class="font-weight-medium">{{ item.campaign_name }}</div>
              </template>
              
              <template #item.status="{ item }">
                <v-chip 
                  :color="getStatusColor(item.status)"
                  variant="tonal"
                  size="small"
                >
                  {{ item.status }}
                </v-chip>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewCampaignDetails(item)"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Analytics Tab -->
        <v-window-item value="analytics">
          <div class="pa-6">
            <h3 class="text-h6 mb-4">Segment Analytics</h3>
            
            <!-- Stats Cards -->
            <div class="row mb-6">
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-primary">{{ talentSegment.candidate_count || 0 }}</div>
                  <div class="text-body-2 text-medium-emphasis">Total Candidates</div>
                </v-card>
              </div>
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-success">{{ getActiveCandidates() }}</div>
                  <div class="text-body-2 text-medium-emphasis">Active Candidates</div>
                </v-card>
              </div>
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-warning">{{ relatedCampaigns.length }}</div>
                  <div class="text-body-2 text-medium-emphasis">Related Campaigns</div>
                </v-card>
              </div>
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-info">{{ getEngagementRate() }}%</div>
                  <div class="text-body-2 text-medium-emphasis">Engagement Rate</div>
                </v-card>
              </div>
            </div>
            
            <!-- Chart placeholder -->
            <v-card class="pa-6">
              <h4 class="text-h6 mb-4">Segment Analytics</h4>
              <div class="text-center pa-8">
                <v-icon size="64" color="grey-lighten-1">mdi-chart-line</v-icon>
                <p class="text-body-1 text-medium-emphasis mt-4">
                  Analytics charts will be implemented here
                </p>
              </div>
            </v-card>
          </div>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- Add Candidate Modal -->
    <v-dialog v-model="showAddCandidateModal" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          Add Candidate to Segment
        </v-card-title>
        <v-card-text>
          <v-form ref="candidateForm" v-model="candidateFormValid">
            <v-select
              v-model="candidateFormData.candidate_id"
              :items="availableCandidates"
              label="Select Candidate *"
              :rules="[v => !!v || 'Candidate is required']"
              required
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeAddCandidateModal">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="savingCandidate"
            :disabled="!candidateFormValid"
            @click="addCandidateToSegment"
          >
            Add
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Campaign Wizard -->
    <campaign-wizard
      v-model="showCampaignWizard"
      :preselected-segment="route.params.id"
      @success="handleCampaignCreated"
    />

    <!-- Edit Talent Segment Modal -->
    <talent-segment-form
      v-model="showEditTalentSegmentModal"
      :segment="Object.keys(talentSegment).length > 0 ? talentSegment : null"
      @success="handleTalentSegmentUpdated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  talentSegmentService,
  candidateSegmentService,
  candidateCampaignService,
  candidateService,
  campaignService
} from '../services/universalService'
import { processSkills } from '../services/candidateService'
import { usersStore } from '@/stores/users'
import CampaignWizard from '@/components/campaign/CampaignWizard.vue'
import TalentSegmentForm from '@/components/talent-segment/TalentSegmentForm.vue'
import moment from 'moment'


const { getUser } = usersStore()
console.log(getUser())
const route = useRoute()
const router = useRouter()

// State
const activeTab = ref('candidates')
const loading = ref(false)
const loadingCandidates = ref(false)
const loadingCampaigns = ref(false)

// Data
const talentSegment = reactive({})
const candidates = ref([])
const relatedCampaigns = ref([])
const availableCandidates = ref([])

// Modals
const showAddCandidateModal = ref(false)
const showCampaignWizard = ref(false)
const showEditTalentSegmentModal = ref(false)
const candidateFormValid = ref(false)
const savingCandidate = ref(false)

// Search
const candidateSearch = ref('')

// Form data
const candidateFormData = reactive({
  candidate_id: '',
  segment_id: route.params.id
})

// Table headers
const candidateHeaders = [
  { title: 'Candidate', key: 'candidate', sortable: true },
  { title: 'Skills', key: 'skills', sortable: false },
  { title: 'Last Contact', key: 'last_contact', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Added At', key: 'added_at', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

const campaignHeaders = [
  { title: 'Campaign Name', key: 'campaign_name', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Start Date', key: 'start_date', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

// Methods
const loadTalentSegment = async () => {
  loading.value = true
  try {
    const result = await talentSegmentService.getFormData(route.params.id)
    if (result.success) {
      Object.assign(talentSegment, result.data)
    }
  } catch (error) {
    console.error('Error loading talent segment:', error)
  } finally {
    loading.value = false
  }
}

const loadCandidates = async () => {
  loadingCandidates.value = true
  try {
    // First, get all CandidateSegment records for this segment
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: route.params.id },
      fields: ['name', 'candidate_id', 'added_at', 'added_by']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      // Get candidate IDs from the relationship
      const candidateIds = candidateSegmentResult.data.map(cs => cs.candidate_id)
      
      // Then get the actual candidate data
      const candidateResult = await candidateService.getList({
        filters: { name: ['in', candidateIds] },
        fields: ['name', 'candidate_name', 'email', 'skills', 'last_contact', 'status']
      })
      
      if (candidateResult.success) {
        // Merge the data - add segment relationship info to candidate data
        candidates.value = candidateResult.data.map(candidate => {
          const segmentRelation = candidateSegmentResult.data.find(cs => cs.candidate_id === candidate.name)
          return {
            ...candidate,
            added_at: segmentRelation?.added_at,
            added_by: segmentRelation?.added_by,
            candidate_segment_id: segmentRelation?.name
          }
        })
      }
    } else {
      candidates.value = []
    }
  } catch (error) {
    console.error('Error loading candidates:', error)
    candidates.value = []
  } finally {
    loadingCandidates.value = false
  }
}

const loadRelatedCampaigns = async () => {
  loadingCampaigns.value = true
  try {
    // First get candidates in this segment
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { segment_id: route.params.id },
      fields: ['candidate_id']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      const candidateIds = candidateSegmentResult.data.map(cs => cs.candidate_id)
      
      // Then get campaigns that have these candidates through CandidateCampaign
      const candidateCampaignResult = await candidateCampaignService.getList({
        filters: { candidate_id: ['in', candidateIds] },
        fields: ['campaign_id']
      })
      
      if (candidateCampaignResult.success && candidateCampaignResult.data.length > 0) {
        const campaignIds = [...new Set(candidateCampaignResult.data.map(cc => cc.campaign_id))]
        
        // Get the actual campaign data
        const campaignResult = await campaignService.getList({
          filters: { name: ['in', campaignIds] },
          fields: ['name', 'campaign_name', 'status', 'start_date']
        })
        
        if (campaignResult.success) {
          relatedCampaigns.value = campaignResult.data
        }
      }
    } else {
      relatedCampaigns.value = []
    }
  } catch (error) {
    console.error('Error loading related campaigns:', error)
    relatedCampaigns.value = []
  } finally {
    loadingCampaigns.value = false
  }
}

const loadAvailableCandidates = async () => {
  try {
    // Get all candidates
    const allCandidatesResult = await candidateService.getList({
      fields: ['name', 'candidate_name'],
      page_length: 1000
    })
    
    if (allCandidatesResult.success) {
      // Get candidates already in this segment
      const existingCandidateSegments = await candidateSegmentService.getList({
        filters: { segment_id: route.params.id },
        fields: ['candidate_id']
      })
      
      const existingCandidateIds = existingCandidateSegments.success 
        ? existingCandidateSegments.data.map(cs => cs.candidate_id)
        : []
      
      // Filter out candidates already in the segment
      const availableCandidatesData = allCandidatesResult.data.filter(
        candidate => !existingCandidateIds.includes(candidate.name)
      )
      
      availableCandidates.value = availableCandidatesData.map(item => ({
        title: item.candidate_name || item.name,
        value: item.name
      }))
    }
  } catch (error) {
    console.error('Error loading candidates:', error)
  }
}

// Candidate methods
const openAddCandidateModal = () => {
  candidateFormData.candidate_id = ''
  showAddCandidateModal.value = true
}

const closeAddCandidateModal = () => {
  showAddCandidateModal.value = false
}

const addCandidateToSegment = async () => {
  if (!candidateFormValid.value) return

  savingCandidate.value = true
  try {
    // Create a new CandidateSegment relationship
    const candidateSegmentData = {
      candidate_id: candidateFormData.candidate_id,
      segment_id: route.params.id,
      added_at: moment().format("YYYY-MM-DD HH:mm:ss"),
      added_by: getUser()?.name || 'Administrator'
    }
    
    const result = await candidateSegmentService.save(candidateSegmentData)
    if (result.success) {
      closeAddCandidateModal()
      await loadCandidates()
      // Update the segment's candidate count
      await loadTalentSegment()
    }
  } catch (error) {
    console.error('Error adding candidate:', error)
  } finally {
    savingCandidate.value = false
  }
}

const viewCandidateDetails = (candidate) => {
  router.push(`/candidates/${candidate.name}`)
}

const contactCandidate = (candidate) => {
  // Implementation for contacting candidate
  console.log('Contact candidate:', candidate)
}

const removeFromSegment = async (candidate) => {
  if (confirm('Are you sure you want to remove this candidate from the segment?')) {
    try {
      // Delete the CandidateSegment relationship
      if (candidate.candidate_segment_id) {
        const result = await candidateSegmentService.delete(candidate.candidate_segment_id)
        if (result.success) {
          await loadCandidates()
          // Update the segment's candidate count
          await loadTalentSegment()
        }
      }
    } catch (error) {
      console.error('Error removing candidate:', error)
    }
  }
}

// Assign all candidates from segment
const handleCampaignCreated = async (event) => {
  console.log('Campaign created successfully:', event)
  // Reload related campaigns
  await loadRelatedCampaigns()
}

const handleTalentSegmentUpdated = async () => {
  console.log('Talent segment updated successfully')
  // Reload talent segment data
  await loadTalentSegment()
}

const createCampaignFromSegment = () => {
  // This method is kept for backward compatibility but now opens wizard
  showCampaignWizard.value = true
}

const viewCampaignDetails = (campaign) => {
  router.push(`/campaigns/${campaign.name}`)
}

// Utility methods
const getTypeColor = (type) => {
  const colors = {
    'DYNAMIC': 'blue',
    'MANUAL': 'green'
  }
  return colors[type] || 'grey'
}

const getStatusColor = (status) => {
  const colors = {
    'ACTIVE': 'success',
    'PAUSED': 'warning',
    'COMPLETED': 'primary',
    'CANCELLED': 'error',
    'Draft': 'grey'
  }
  return colors[status] || 'grey'
}

const getSkillColor = (skill) => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'error']
  const hash = skill.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const formatDateTime = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const formatCriteria = (criteria) => {
  if (!criteria) return ''
  try {
    return JSON.stringify(JSON.parse(criteria), null, 2)
  } catch {
    return criteria
  }
}

const getActiveCandidates = () => {
  return candidates.value.filter(item => item.status === 'ACTIVE').length
}

const getEngagementRate = () => {
  // Calculate engagement rate based on candidates data
  if (candidates.value.length === 0) return 0
  const activeCount = getActiveCandidates()
  return Math.round((activeCount / candidates.value.length) * 100)
}

const editTalentSegment = () => {
  // Ensure we have loaded segment data before opening modal
  if (Object.keys(talentSegment).length === 0) {
    console.warn('Talent segment data not loaded yet')
    return
  }
  // Open edit modal with current segment data
  showEditTalentSegmentModal.value = true
}

const deleteTalentSegment = async () => {
  if (confirm('Are you sure you want to delete this talent segment?')) {
    try {
      const result = await talentSegmentService.delete(route.params.id)
      if (result.success) {
        router.push('/talent-segments')
      }
    } catch (error) {
      console.error('Error deleting talent segment:', error)
    }
  }
}

// Lifecycle
onMounted(async () => {
  await loadTalentSegment()
  await loadCandidates()
  await loadRelatedCampaigns()
  await loadAvailableCandidates()
})
</script>

<style scoped>
.talent-segment-detail-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  border-radius: 8px;
}

.v-card {
  border-radius: 8px;
}

.v-chip {
  font-weight: 500;
}

.v-data-table {
  border-radius: 8px;
}
</style>
