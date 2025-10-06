<template>
  <div class="candidate-detail-view">
    <!-- Header with Candidate Info -->
    <div class="page-header bg-white pa-6 mb-6 elevation-1">
      <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-btn
            icon="mdi-arrow-left"
            variant="text"
            @click="$router.go(-1)"
            class="mr-3"
          />
          <div class="d-flex align-center">
            <v-avatar size="60" color="primary" class="mr-4">
              <span class="text-h5">{{ candidate.candidate_name?.charAt(0) }}</span>
            </v-avatar>
            <div>
              <h1 class="text-h4 font-weight-bold text-primary mb-2">
                {{ candidate.candidate_name || 'Loading...' }}
              </h1>
              <div class="d-flex align-center flex-wrap">
                <v-chip 
                  :color="getStatusColor(candidate.status)"
                  variant="tonal"
                  class="mr-2 mb-2"
                >
                  {{ candidate.status }}
                </v-chip>
                <span class="text-body-2 text-medium-emphasis mr-4">
                  {{ candidate.email }}
                </span>
                <span class="text-body-2 text-medium-emphasis">
                  {{ candidate.phone }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="d-flex align-center">
          <v-btn
            color="primary"
            variant="outlined"
            prepend-icon="mdi-pencil"
            @click="editCandidate"
            class="mr-2"
          >
            Edit Profile
          </v-btn>
          <v-btn
            color="error"
            variant="outlined"
            prepend-icon="mdi-delete"
            @click="deleteCandidate"
          >
            Delete
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Candidate Details Card -->
    <v-card class="mb-6" variant="outlined">
      <v-card-title>
        <v-icon class="mr-2">mdi-account-circle</v-icon>
        Candidate Information
      </v-card-title>
      <v-card-text>
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <strong>Full Name:</strong>
              <p class="mb-0">{{ candidate.candidate_name || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Email:</strong>
              <p class="mb-0">{{ candidate.email || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Phone:</strong>
              <p class="mb-0">{{ candidate.phone || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Status:</strong>
              <v-chip 
                :color="getStatusColor(candidate.status)"
                variant="tonal"
                size="small"
              >
                {{ candidate.status }}
              </v-chip>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <strong>Position:</strong>
              <p class="mb-0">{{ candidate.position || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Experience:</strong>
              <p class="mb-0">{{ candidate.experience || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Location:</strong>
              <p class="mb-0">{{ candidate.location || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Created:</strong>
              <p class="mb-0">{{ formatDate(candidate.creation) || 'N/A' }}</p>
            </div>
          </div>
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
        <v-tab value="campaigns">
          <v-icon class="mr-2">mdi-bullseye-arrow</v-icon>
          Active Campaigns ({{ candidateCampaigns.length }})
        </v-tab>
        <v-tab value="segments">
          <v-icon class="mr-2">mdi-group</v-icon>
          Segments ({{ candidateSegments.length }})
        </v-tab>
        <v-tab value="interactions">
          <v-icon class="mr-2">mdi-message-text</v-icon>
          Interactions ({{ interactions.length }})
        </v-tab>
        <v-tab value="emails">
          <v-icon class="mr-2">mdi-email</v-icon>
          Email History ({{ emailLogs.length }})
        </v-tab>
        <v-tab value="documents">
          <v-icon class="mr-2">mdi-file-document</v-icon>
          Documents
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- Campaigns Tab -->
        <v-window-item value="campaigns">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Active Campaigns</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="openCampaignModal()"
              >
                Assign to Campaign
              </v-btn>
            </div>
            
            <!-- Campaign List -->
            <v-data-table
              :headers="campaignHeaders"
              :items="candidateCampaigns"
              :loading="loadingCampaigns"
              item-value="name"
              class="elevation-1"
            >
              <template #item.campaign_id="{ item }">
                <div class="d-flex align-center">
                  <v-icon color="primary" class="mr-2">mdi-bullseye-arrow</v-icon>
                  <div>
                    <div class="font-weight-medium">{{ item.campaign_name }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.campaign_id }}</div>
                  </div>
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
              
              <template #item.current_step_order="{ item }">
                <div class="d-flex align-center">
                  <v-progress-circular
                    :model-value="getStepProgress(item)"
                    color="primary"
                    size="24"
                    width="3"
                    class="mr-2"
                  />
                  <span>Step {{ item.current_step_order }}</span>
                </div>
              </template>
              
              <template #item.next_action_at="{ item }">
                <div class="text-body-2">
                  {{ formatDate(item.next_action_at) }}
                  <v-chip 
                    v-if="isOverdue(item.next_action_at)"
                    color="error"
                    variant="tonal"
                    size="x-small"
                    class="ml-1"
                  >
                    Overdue
                  </v-chip>
                </div>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-play"
                  size="small"
                  variant="text"
                  color="success"
                  @click="startCampaign(item)"
                  v-if="item.status === 'PAUSED'"
                />
                <v-btn
                  icon="mdi-pause"
                  size="small"
                  variant="text"
                  color="warning"
                  @click="pauseCampaign(item)"
                  v-if="item.status === 'ACTIVE'"
                />
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewCampaignDetails(item)"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="removeCampaign(item)"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Segments Tab -->
        <v-window-item value="segments">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Candidate Segments</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="openSegmentModal()"
              >
                Add to Segment
              </v-btn>
            </div>
            
            <!-- Segments List -->
            <v-data-table
              :headers="segmentHeaders"
              :items="candidateSegments"
              :loading="loadingSegments"
              item-value="name"
              class="elevation-1"
            >
              <template #item.title="{ item }">
                <div class="d-flex align-center">
                  <v-icon color="success" class="mr-2">mdi-group</v-icon>
                  <div>
                    <div class="font-weight-medium">{{ item.title }}</div>
                    <div class="text-caption text-medium-emphasis">{{ item.description }}</div>
                  </div>
                </div>
              </template>
              
              <template #item.type="{ item }">
                <v-chip 
                  :color="getTypeColor(item.type)"
                  variant="tonal"
                  size="small"
                >
                  {{ item.type }}
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
                  @click="viewSegmentDetails(item)"
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

        <!-- Interactions Tab -->
        <v-window-item value="interactions">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Mira Interaction History</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="openInteractionModal()"
              >
                Add Mira Interaction
              </v-btn>
            </div>
            
            <!-- Interactions Timeline -->
            <div v-if="interactions.length > 0">
              <v-timeline side="end" class="pa-4">
                <v-timeline-item
                  v-for="interaction in interactions"
                  :key="interaction.name"
                  :dot-color="getInteractionColor(interaction.interaction_type)"
                  size="small"
                >
                  <template #icon>
                    <v-icon size="16">{{ getInteractionIcon(interaction.interaction_type) }}</v-icon>
                  </template>
                  
                  <v-card class="mb-3" variant="outlined">
                    <v-card-text class="pb-2">
                      <div class="d-flex align-center justify-space-between mb-2">
                        <div class="d-flex align-center">
                          <v-chip 
                            :color="getInteractionColor(interaction.interaction_type)"
                            variant="tonal"
                            size="small"
                            class="mr-2"
                          >
                            {{ formatInteractionType(interaction.interaction_type) }}
                          </v-chip>
                          <span class="text-caption text-medium-emphasis">
                            {{ formatDateTime(interaction.creation) }}
                          </span>
                        </div>
                        <v-btn
                          icon="mdi-delete"
                          size="small"
                          variant="text"
                          color="error"
                          @click="deleteInteraction(interaction)"
                        />
                      </div>
                      
                      <div v-if="interaction.description" class="text-body-2 text-medium-emphasis">
                        {{ interaction.description }}
                      </div>
                      
                      <div v-if="interaction.url" class="mt-2">
                        <v-chip
                          color="info"
                          variant="outlined"
                          size="x-small"
                          prepend-icon="mdi-link"
                        >
                          Link clicked
                        </v-chip>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-timeline-item>
              </v-timeline>
            </div>
            
            <!-- Empty state -->
            <div v-else class="text-center pa-8">
              <v-icon size="64" color="grey-lighten-1">mdi-message-text-outline</v-icon>
              <p class="text-body-1 text-medium-emphasis mt-4">
                No interactions recorded yet
              </p>
            </div>
          </div>
        </v-window-item>

        <!-- Email History Tab -->
        <v-window-item value="emails">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Email History</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-email-send"
                @click="composeEmail()"
              >
                Send Email
              </v-btn>
            </div>
            
            <!-- Email List -->
            <v-data-table
              :headers="emailHeaders"
              :items="emailLogs"
              :loading="loadingEmails"
              item-value="name"
              class="elevation-1"
            >
              <template #item.subject="{ item }">
                <div>
                  <div class="font-weight-medium">{{ item.subject }}</div>
                  <div class="text-caption text-medium-emphasis">{{ item.content?.substring(0, 50) }}...</div>
                </div>
              </template>
              
              <template #item.status="{ item }">
                <v-chip 
                  :color="getEmailStatusColor(item.status)"
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
                  @click="viewEmailDetails(item)"
                />
                <v-btn
                  icon="mdi-reply"
                  size="small"
                  variant="text"
                  @click="replyEmail(item)"
                  v-if="item.email_status === 'Sent'"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Documents Tab -->
        <v-window-item value="documents">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Documents</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-upload"
                @click="uploadDocument()"
              >
                Upload Document
              </v-btn>
            </div>
            
            <!-- Documents Grid -->
            <div class="row">
              <div class="col-md-4 col-sm-6 mb-4" v-for="doc in documents" :key="doc.id">
                <v-card>
                  <v-card-text class="text-center pa-6">
                    <v-icon size="48" color="primary">{{ getDocumentIcon(doc.type) }}</v-icon>
                    <h4 class="text-body-1 font-weight-medium mt-2">{{ doc.name }}</h4>
                    <p class="text-caption text-medium-emphasis">{{ formatFileSize(doc.size) }}</p>
                  </v-card-text>
                  <v-card-actions class="justify-center">
                    <v-btn size="small" variant="text" @click="downloadDocument(doc)">
                      Download
                    </v-btn>
                    <v-btn size="small" variant="text" color="error" @click="deleteDocument(doc)">
                      Delete
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </div>
              
              <!-- Empty state -->
              <div v-if="documents.length === 0" class="col-12 text-center pa-8">
                <v-icon size="64" color="grey-lighten-1">mdi-file-document-outline</v-icon>
                <p class="text-body-1 text-medium-emphasis mt-4">
                  No documents uploaded yet
                </p>
              </div>
            </div>
          </div>
        </v-window-item>
      </v-window>
    </v-card>

    <!-- Campaign Assignment Modal -->
    <v-dialog v-model="showCampaignModal" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          Assign to Campaign
        </v-card-title>
        <v-card-text>
          <v-form ref="campaignForm" v-model="campaignFormValid">
            <v-select
              v-model="campaignFormData.campaign_id"
              :items="availableCampaigns"
              label="Select Campaign *"
              :rules="[v => !!v || 'Campaign is required']"
              required
            />
            <v-select
              v-model="campaignFormData.status"
              :items="statusOptions"
              label="Status *"
              :rules="[v => !!v || 'Status is required']"
              required
            />
            <v-text-field
              v-model="campaignFormData.current_step_order"
              label="Starting Step"
              type="number"
              value="1"
              min="1"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeCampaignModal">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="savingCampaign"
            :disabled="!campaignFormValid"
            @click="assignToCampaign"
          >
            Assign
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Segment Assignment Modal -->
    <v-dialog v-model="showSegmentModal" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          Add to Segment
        </v-card-title>
        <v-card-text>
          <v-form ref="segmentForm" v-model="segmentFormValid">
            <v-select
              v-model="segmentFormData.segment_id"
              :items="availableSegments"
              label="Select Segment *"
              :rules="[v => !!v || 'Segment is required']"
              required
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeSegmentModal">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="savingSegment"
            :disabled="!segmentFormValid"
            @click="addToSegment"
          >
            Add
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  candidateService, 
  candidateCampaignService,
  candidateSegmentService,
  talentSegmentService,
  interactionService,
  emailLogService
} from '../services/universalService'
import { useCampaignStore } from '@/stores/campaign'

const route = useRoute()
const router = useRouter()

// Campaign store
const campaignStore = useCampaignStore()

// State
const activeTab = ref('campaigns')
const loading = ref(false)
const loadingCampaigns = ref(false)
const loadingSegments = ref(false)
const loadingInteractions = ref(false)
const loadingEmails = ref(false)

// Data
const candidate = reactive({})
const candidateCampaigns = ref([])
const candidateSegments = ref([])
const interactions = ref([])
const emailLogs = ref([])
const documents = ref([])

// Available options
const availableCampaigns = ref([])
const availableSegments = ref([])

// Modals
const showCampaignModal = ref(false)
const showSegmentModal = ref(false)
const campaignFormValid = ref(false)
const segmentFormValid = ref(false)
const savingCampaign = ref(false)
const savingSegment = ref(false)

// Form data
const campaignFormData = reactive({
  candidate_id: route.params.id,
  campaign_id: '',
  status: 'ACTIVE',
  current_step_order: 1
})

const segmentFormData = reactive({
  candidate_id: route.params.id,
  segment_id: ''
})

// Options
const statusOptions = [
  { title: 'Active', value: 'ACTIVE' },
  { title: 'Paused', value: 'PAUSED' },
  { title: 'Completed', value: 'COMPLETED' },
  { title: 'Cancelled', value: 'CANCELLED' }
]

// Table headers
const campaignHeaders = [
  { title: 'Campaign', key: 'campaign_id' },
  { title: 'Status', key: 'status' },
  { title: 'Progress', key: 'current_step_order' },
  { title: 'Next Action', key: 'next_action_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const segmentHeaders = [
  { title: 'Segment', key: 'title' },
  { title: 'Type', key: 'type' },
  { title: 'Added At', key: 'added_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const emailHeaders = [
  { title: 'Subject', key: 'subject' },
  { title: 'Status', key: 'status' },
  { title: 'Sent Date', key: 'creation' },
  { title: 'Actions', key: 'actions', sortable: false }
]

// Methods
const loadCandidate = async () => {
  loading.value = true
  try {
    const result = await candidateService.getFormData(route.params.id)
    if (result.success) {
      Object.assign(candidate, result.data)
    }
  } catch (error) {
    console.error('Error loading candidate:', error)
  } finally {
    loading.value = false
  }
}

const loadCandidateCampaigns = async () => {
  loadingCampaigns.value = true
  try {
    const result = await candidateCampaignService.getList({
      filters: { candidate_id: route.params.id },
      fields: ['name', 'campaign_id', 'campaign_name', 'status', 'current_step_order', 'next_action_at']
    })
    if (result.success) {
      candidateCampaigns.value = result.data
    }
  } catch (error) {
    console.error('Error loading candidate campaigns:', error)
  } finally {
    loadingCampaigns.value = false
  }
}

const loadCandidateSegments = async () => {
  loadingSegments.value = true
  try {
    // First, get all CandidateSegment records for this candidate
    const candidateSegmentResult = await candidateSegmentService.getList({
      filters: { candidate_id: route.params.id },
      fields: ['name', 'segment_id', 'added_at', 'added_by']
    })
    
    if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
      // Get segment IDs from the relationship
      const segmentIds = candidateSegmentResult.data.map(cs => cs.segment_id)
      
      // Then get the actual segment data
      const segmentResult = await talentSegmentService.getList({
        filters: { name: ['in', segmentIds] },
        fields: ['name', 'title', 'description', 'type', 'candidate_count']
      })
      
      if (segmentResult.success) {
        // Merge the data - add relationship info to segment data
        candidateSegments.value = segmentResult.data.map(segment => {
          const segmentRelation = candidateSegmentResult.data.find(cs => cs.segment_id === segment.name)
          return {
            ...segment,
            added_at: segmentRelation?.added_at,
            added_by: segmentRelation?.added_by,
            candidate_segment_id: segmentRelation?.name
          }
        })
      }
    } else {
      candidateSegments.value = []
    }
  } catch (error) {
    console.error('Error loading candidate segments:', error)
    candidateSegments.value = []
  } finally {
    loadingSegments.value = false
  }
}

const loadInteractions = async () => {
  loadingInteractions.value = true
  try {
    const result = await interactionService.getList({
      filters: { candidate_id: route.params.id },
      fields: ['name', 'interaction_type', 'description', 'url', 'creation'],
      order_by: 'creation desc'
    })
    if (result.success) {
      interactions.value = result.data
    }
  } catch (error) {
    console.error('Error loading interactions:', error)
  } finally {
    loadingInteractions.value = false
  }
}

const loadEmailLogs = async () => {
  loadingEmails.value = true
  try {
    // Since EmailLog doctype doesn't have candidate_id field,
    // we might need to filter by recipients containing the candidate's email
    const candidateEmail = candidate.email || candidate.candidate_email
    let filters = {}
    
    if (candidateEmail) {
      // Filter by recipients containing the candidate's email
      filters.recipients = ['like', `%${candidateEmail}%`]
    } else {
      // If no email available, return empty result
      emailLogs.value = []
      loadingEmails.value = false
      return
    }
    
    const result = await emailLogService.getList({
      filters: filters,
      fields: ['name', 'subject', 'content', 'status', 'creation'],
      order_by: 'creation desc'
    })
    if (result.success) {
      emailLogs.value = result.data
    }
  } catch (error) {
    console.error('Error loading email logs:', error)
  } finally {
    loadingEmails.value = false
  }
}

const loadAvailableCampaigns = async () => {
  try {
    const result = await campaignStore.getFilteredCampaigns({
      limit: 1000,
      page: 1
    })
    if (result && result.data) {
      availableCampaigns.value = result.data.map(item => ({
        label: item.campaign_name || item.name,
        value: item.name
      }))
    } else {
      availableCampaigns.value = []
    }
  } catch (error) {
    console.error('Error loading campaigns:', error)
    availableCampaigns.value = []
  }
}

const loadAvailableSegments = async () => {
  try {
    const result = await talentSegmentService.getList({
      fields: ['name', 'segment_name'],
      page_length: 1000
    })
    if (result.success) {
      availableSegments.value = result.data.map(item => ({
        title: item.segment_name || item.name,
        value: item.name
      }))
    }
  } catch (error) {
    console.error('Error loading segments:', error)
  }
}

// Campaign methods
const openCampaignModal = () => {
  Object.keys(campaignFormData).forEach(key => {
    if (key !== 'candidate_id') {
      campaignFormData[key] = ''
    }
  })
  campaignFormData.status = 'ACTIVE'
  campaignFormData.current_step_order = 1
  showCampaignModal.value = true
}

const closeCampaignModal = () => {
  showCampaignModal.value = false
}

const assignToCampaign = async () => {
  if (!campaignFormValid.value) return

  savingCampaign.value = true
  try {
    const result = await candidateCampaignService.save(campaignFormData)
    if (result.success) {
      closeCampaignModal()
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error assigning to campaign:', error)
  } finally {
    savingCampaign.value = false
  }
}

// Segment methods
const openSegmentModal = () => {
  segmentFormData.segment_id = ''
  showSegmentModal.value = true
}

const closeSegmentModal = () => {
  showSegmentModal.value = false
}

const addToSegment = async () => {
  if (!segmentFormValid.value) return

  savingSegment.value = true
  try {
    const result = await candidateSegmentService.save(segmentFormData)
    if (result.success) {
      closeSegmentModal()
      loadCandidateSegments()
    }
  } catch (error) {
    console.error('Error adding to segment:', error)
  } finally {
    savingSegment.value = false
  }
}

// Utility methods
const getStatusColor = (status) => {
  const colors = {
    'ACTIVE': 'success',
    'PAUSED': 'warning',
    'COMPLETED': 'primary',
    'CANCELLED': 'error',
    'Active': 'success',
    'Inactive': 'grey'
  }
  return colors[status] || 'grey'
}

const getStepProgress = (item) => {
  // Calculate progress based on current step (assuming max 10 steps)
  return (item.current_step_order / 10) * 100
}

const isOverdue = (date) => {
  if (!date) return false
  return new Date(date) < new Date()
}

const getInteractionColor = (type) => {
  const colors = {
    'EMAIL_SENT': 'blue',
    'EMAIL_DELIVERED': 'green',
    'EMAIL_BOUNCED': 'error',
    'EMAIL_OPENED': 'info',
    'EMAIL_CLICKED': 'success',
    'EMAIL_UNSUBSCRIBED': 'warning',
    'EMAIL_REPLIED': 'purple',
    'PAGE_VISITED': 'cyan',
    'FORM_SUBMITTED': 'teal',
    'DOWNLOAD_TRIGGERED': 'orange',
    'CHAT_STARTED': 'indigo',
    'CHAT_MESSAGE_SENT': 'indigo',
    'CHAT_COMPLETED': 'green',
    'CALL_MISSED': 'warning',
    'CALL_COMPLETED': 'success',
    'SMS_SENT': 'blue',
    'SMS_DELIVERED': 'green',
    'SMS_REPLIED': 'purple',
    'APPLICATION_SUBMITTED': 'primary',
    'DOCUMENT_UPLOADED': 'orange',
    'TEST_STARTED': 'info',
    'TEST_COMPLETED': 'success',
    'INTERVIEW_CONFIRMED': 'success',
    'INTERVIEW_RESCHEDULED': 'warning'
  }
  return colors[type] || 'grey'
}

const getInteractionIcon = (type) => {
  const icons = {
    'EMAIL_SENT': 'mdi-email-send',
    'EMAIL_DELIVERED': 'mdi-email-check',
    'EMAIL_BOUNCED': 'mdi-email-alert',
    'EMAIL_OPENED': 'mdi-email-open',
    'EMAIL_CLICKED': 'mdi-cursor-pointer',
    'EMAIL_UNSUBSCRIBED': 'mdi-email-remove',
    'EMAIL_REPLIED': 'mdi-reply',
    'PAGE_VISITED': 'mdi-web',
    'FORM_SUBMITTED': 'mdi-form-select',
    'DOWNLOAD_TRIGGERED': 'mdi-download',
    'CHAT_STARTED': 'mdi-chat',
    'CHAT_MESSAGE_SENT': 'mdi-message-text',
    'CHAT_COMPLETED': 'mdi-chat-outline',
    'CALL_MISSED': 'mdi-phone-missed',
    'CALL_COMPLETED': 'mdi-phone',
    'SMS_SENT': 'mdi-message',
    'SMS_DELIVERED': 'mdi-message-check',
    'SMS_REPLIED': 'mdi-message-reply',
    'APPLICATION_SUBMITTED': 'mdi-file-document-edit',
    'DOCUMENT_UPLOADED': 'mdi-file-upload',
    'TEST_STARTED': 'mdi-clipboard-text',
    'TEST_COMPLETED': 'mdi-clipboard-check',
    'INTERVIEW_CONFIRMED': 'mdi-calendar-check',
    'INTERVIEW_RESCHEDULED': 'mdi-calendar-edit'
  }
  return icons[type] || 'mdi-information'
}

const formatInteractionType = (type) => {
  const labels = {
    'EMAIL_SENT': 'Email Sent',
    'EMAIL_DELIVERED': 'Email Delivered',
    'EMAIL_BOUNCED': 'Email Bounced',
    'EMAIL_OPENED': 'Email Opened',
    'EMAIL_CLICKED': 'Link Clicked',
    'EMAIL_UNSUBSCRIBED': 'Unsubscribed',
    'EMAIL_REPLIED': 'Email Replied',
    'PAGE_VISITED': 'Page Visited',
    'FORM_SUBMITTED': 'Form Submitted',
    'DOWNLOAD_TRIGGERED': 'Download',
    'CHAT_STARTED': 'Chat Started',
    'CHAT_MESSAGE_SENT': 'Chat Message',
    'CHAT_COMPLETED': 'Chat Ended',
    'CALL_MISSED': 'Call Missed',
    'CALL_COMPLETED': 'Call Completed',
    'SMS_SENT': 'SMS Sent',
    'SMS_DELIVERED': 'SMS Delivered',
    'SMS_REPLIED': 'SMS Replied',
    'APPLICATION_SUBMITTED': 'Application Submitted',
    'DOCUMENT_UPLOADED': 'Document Uploaded',
    'TEST_STARTED': 'Test Started',
    'TEST_COMPLETED': 'Test Completed',
    'INTERVIEW_CONFIRMED': 'Interview Confirmed',
    'INTERVIEW_RESCHEDULED': 'Interview Rescheduled'
  }
  return labels[type] || type.replace(/_/g, ' ')
}

const getEmailStatusColor = (status) => {
  const colors = {
    'Success': 'success',
    'Failed': 'error',
    'Fallback': 'warning'
  }
  return colors[status] || 'grey'
}

const getDocumentIcon = (type) => {
  const icons = {
    'pdf': 'mdi-file-pdf-box',
    'doc': 'mdi-file-word-box',
    'xls': 'mdi-file-excel-box',
    'image': 'mdi-file-image-box'
  }
  return icons[type] || 'mdi-file-document-box'
}

const getTypeColor = (type) => {
  const colors = {
    'DYNAMIC': 'blue',
    'MANUAL': 'green'
  }
  return colors[type] || 'grey'
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
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

const formatFileSize = (size) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB'
  return (size / (1024 * 1024)).toFixed(1) + ' MB'
}

// Action methods
const startCampaign = async (item) => {
  try {
    const result = await candidateCampaignService.save(
      { ...item, status: 'ACTIVE' },
      item.name
    )
    if (result.success) {
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error starting campaign:', error)
  }
}

const pauseCampaign = async (item) => {
  try {
    const result = await candidateCampaignService.save(
      { ...item, status: 'PAUSED' },
      item.name
    )
    if (result.success) {
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error pausing campaign:', error)
  }
}

const viewCampaignDetails = (item) => {
  router.push(`/campaigns/${item.campaign_id}`)
}

const removeCampaign = async (item) => {
  if (confirm('Are you sure you want to remove this candidate from the campaign?')) {
    try {
      const result = await candidateCampaignService.delete(item.name)
      if (result.success) {
        loadCandidateCampaigns()
      }
    } catch (error) {
      console.error('Error removing campaign:', error)
    }
  }
}

const viewSegmentDetails = (item) => {
  router.push(`/talent-segments/${item.name}/detail`)
}

const removeFromSegment = async (item) => {
  if (confirm('Are you sure you want to remove this candidate from the segment?')) {
    try {
      // Delete the CandidateSegment relationship
      const result = await candidateSegmentService.delete(item.candidate_segment_id)
      if (result.success) {
        loadCandidateSegments()
      }
    } catch (error) {
      console.error('Error removing from segment:', error)
    }
  }
}

const editCandidate = () => {
  router.push(`/candidates/${route.params.id}/edit`)
}

const deleteCandidate = async () => {
  if (confirm('Are you sure you want to delete this candidate?')) {
    try {
      const result = await candidateService.delete(route.params.id)
      if (result.success) {
        router.push('/candidates')
      }
    } catch (error) {
      console.error('Error deleting candidate:', error)
    }
  }
}

// Placeholder methods for future implementation
const openInteractionModal = () => {
  // Implementation for interaction modal
}

const deleteInteraction = async (interaction) => {
  if (confirm('Are you sure you want to delete this interaction?')) {
    try {
      const result = await interactionService.delete(interaction.name)
      if (result.success) {
        loadInteractions()
      }
    } catch (error) {
      console.error('Error deleting interaction:', error)
    }
  }
}

const composeEmail = () => {
  // Implementation for compose email
}

const viewEmailDetails = (item) => {
  // Implementation for view email details
}

const replyEmail = (item) => {
  // Implementation for reply email
}

const uploadDocument = () => {
  // Implementation for upload document
}

const downloadDocument = (doc) => {
  // Implementation for download document
}

const deleteDocument = (doc) => {
  // Implementation for delete document
}

// Lifecycle
onMounted(async () => {
  await loadCandidate()
  await loadCandidateCampaigns()
  await loadCandidateSegments()
  await loadInteractions()
  await loadEmailLogs()
  await loadAvailableCampaigns()
  await loadAvailableSegments()
})
</script>

<style scoped>
.candidate-detail-view {
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

.v-timeline {
  max-height: 600px;
  overflow-y: auto;
}
</style>
