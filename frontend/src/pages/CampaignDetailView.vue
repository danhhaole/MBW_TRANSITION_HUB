<template>
  <div class="campaign-detail-view">
    <!-- Header with Campaign Info -->
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
              {{ campaign.campaign_name || 'Loading...' }}
            </h1>
            <div class="d-flex align-center flex-wrap">
              <v-chip 
                :color="getStatusColor(campaign.status)"
                variant="tonal"
                class="mr-2 mb-2"
              >
                {{ campaign.status }}
              </v-chip>
              <span class="text-body-2 text-medium-emphasis mr-4">
                Created: {{ formatDate(campaign.creation) }}
              </span>
              <span class="text-body-2 text-medium-emphasis">
                Modified: {{ formatDate(campaign.modified) }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="d-flex align-center">
          <v-btn
            color="primary"
            variant="outlined"
            prepend-icon="mdi-pencil"
            @click="editCampaign"
            class="mr-2"
          >
            Edit Campaign
          </v-btn>
          <v-btn
            color="error"
            variant="outlined"
            prepend-icon="mdi-delete"
            @click="deleteCampaign"
          >
            Delete
          </v-btn>
        </div>
      </div>
    </div>

    <!-- Campaign Details Card -->
    <v-card class="mb-6" variant="outlined">
      <v-card-title>
        <v-icon class="mr-2">mdi-information</v-icon>
        Campaign Information
      </v-card-title>
      <v-card-text>
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <strong>Campaign Name:</strong>
              <p class="mb-0">{{ campaign.campaign_name || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Description:</strong>
              <p class="mb-0">{{ campaign.description || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Status:</strong>
              <v-chip 
                :color="getStatusColor(campaign.status)"
                variant="tonal"
                size="small"
              >
                {{ campaign.status }}
              </v-chip>
            </div>
            <div class="mb-3">
              <strong>Type:</strong>
              <v-chip 
                :color="getTypeColor(campaign.type)"
                variant="tonal"
                size="small"
              >
                {{ campaign.type }}
              </v-chip>
            </div>
          </div>
          <div class="col-md-6">
            <div class="mb-3">
              <strong>Start Date:</strong>
              <p class="mb-0">{{ formatDate(campaign.start_date) || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>End Date:</strong>
              <p class="mb-0">{{ formatDate(campaign.end_date) || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Created By:</strong>
              <p class="mb-0">{{ campaign.owner_id || 'N/A' }}</p>
            </div>
            <div class="mb-3">
              <strong>Target Segment:</strong>
              <div class="d-flex align-center">
                <v-chip 
                  v-if="targetSegment"
                  color="purple"
                  variant="tonal"
                  size="small"
                  class="mr-2"
                  @click="viewTargetSegment"
                  style="cursor: pointer;"
                >
                  {{ targetSegment.title }}
                </v-chip>
                <span v-else class="text-body-2">N/A</span>
              </div>
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
        <v-tab value="steps">
          <v-icon class="mr-2">mdi-chart-timeline-variant</v-icon>
          Campaign Steps ({{ campaignSteps.length }})
        </v-tab>
        <v-tab value="candidates">
          <v-icon class="mr-2">mdi-account-multiple</v-icon>
          Assigned Candidates ({{ candidateCampaigns.length }})
        </v-tab>
        <v-tab value="actions">
          <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
          Actions ({{ actions.length }})
        </v-tab>
        <v-tab value="analytics">
          <v-icon class="mr-2">mdi-chart-line</v-icon>
          Analytics
        </v-tab>
      </v-tabs>

      <v-window v-model="activeTab">
        <!-- Campaign Steps Tab -->
        <v-window-item value="steps">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Campaign Steps</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="openStepModal()"
              >
                Add Step
              </v-btn>
            </div>
            
            <!-- Campaign Steps List -->
            <v-data-table
              :headers="stepHeaders"
              :items="campaignSteps"
              :loading="loadingSteps"
              item-value="name"
              class="elevation-1"
            >
              <template #item.step_order="{ item }">
                <v-chip color="primary" variant="outlined" size="small">
                  Step {{ item.step_order }}
                </v-chip>
              </template>
              
              <template #item.action_type="{ item }">
                <v-chip 
                  :color="getActionTypeColor(item.action_type)"
                  variant="tonal"
                  size="small"
                >
                  {{ item.action_type }}
                </v-chip>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-pencil"
                  size="small"
                  variant="text"
                  @click="openStepModal(item)"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="deleteStep(item)"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Candidate Campaigns Tab -->
        <v-window-item value="candidates">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Assigned Candidates</h3>
              <div class="d-flex align-center">
                <v-btn
                  v-if="campaign.target_segment && availableCandidates.length > 0"
                  color="success"
                  variant="outlined"
                  prepend-icon="mdi-account-group"
                  @click="assignAllFromSegment"
                  class="mr-2"
                  :loading="assigningAll"
                >
                  Assign All from Segment ({{ availableCandidates.length }})
                </v-btn>
                <v-btn
                  color="primary"
                  prepend-icon="mdi-plus"
                  @click="openCandidateModal()"
                >
                  Assign Candidate
                </v-btn>
              </div>
            </div>
            
            <!-- Candidate Campaigns List -->
            <v-data-table
              :headers="candidateHeaders"
              :items="candidateCampaigns"
              :loading="loadingCandidates"
              item-value="name"
              class="elevation-1"
            >
              <template #item.candidate_id="{ item }">
                <div class="d-flex align-center">
                  <v-avatar size="32" color="primary" class="mr-2">
                    <span class="text-caption">{{ item.candidate_id?.charAt(0) }}</span>
                  </v-avatar>
                  <div>
                    <div class="font-weight-medium">{{ item.candidate_id }}</div>
                    <div class="text-caption text-medium-emphasis">Candidate</div>
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
                <v-chip color="info" variant="outlined" size="small">
                  Step {{ item.current_step_order }}
                </v-chip>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-play"
                  size="small"
                  variant="text"
                  color="success"
                  @click="startCandidateCampaign(item)"
                  v-if="item.status === 'Draft' || item.status === 'Paused'"
                />
                <v-btn
                  icon="mdi-pause"
                  size="small"
                  variant="text"
                  color="warning"
                  @click="pauseCandidateCampaign(item)"
                  v-if="item.status === 'Active'"
                />
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewCandidateDetails(item)"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="unassignCandidate(item)"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Actions Tab -->
        <v-window-item value="actions">
          <div class="pa-6">
            <div class="d-flex justify-space-between align-center mb-4">
              <h3 class="text-h6">Campaign Actions</h3>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="openActionModal()"
              >
                Add Action
              </v-btn>
            </div>
            
            <!-- Actions List -->
            <v-data-table
              :headers="actionHeaders"
              :items="actions"
              :loading="loadingActions"
              item-value="name"
              class="elevation-1"
            >
              <template #item.status="{ item }">
                <v-chip 
                  :color="getActionStatusColor(item.status)"
                  variant="tonal"
                  size="small"
                >
                  {{ item.status }}
                </v-chip>
              </template>
              
              <template #item.scheduled_at="{ item }">
                <div class="text-body-2">
                  {{ formatDateTime(item.scheduled_at) }}
                </div>
              </template>
              
              <template #item.executed_at="{ item }">
                <div class="text-body-2">
                  {{ formatDateTime(item.executed_at) }}
                </div>
              </template>
              
              <template #item.actions="{ item }">
                <v-btn
                  icon="mdi-eye"
                  size="small"
                  variant="text"
                  @click="viewActionDetails(item)"
                />
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  variant="text"
                  color="error"
                  @click="deleteAction(item)"
                />
              </template>
            </v-data-table>
          </div>
        </v-window-item>

        <!-- Analytics Tab -->
        <v-window-item value="analytics">
          <div class="pa-6">
            <h3 class="text-h6 mb-4">Campaign Analytics</h3>
            
            <!-- Stats Cards -->
            <div class="row mb-6">
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-primary">{{ campaignSteps.length }}</div>
                  <div class="text-body-2 text-medium-emphasis">Total Steps</div>
                </v-card>
              </div>
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-success">{{ candidateCampaigns.length }}</div>
                  <div class="text-body-2 text-medium-emphasis">Assigned Candidates</div>
                </v-card>
              </div>
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-warning">{{ getActiveCandidates() }}</div>
                  <div class="text-body-2 text-medium-emphasis">Active Candidates</div>
                </v-card>
              </div>
              <div class="col-md-3 col-6 mb-4">
                <v-card class="pa-4 text-center">
                  <div class="text-h4 font-weight-bold text-info">{{ getCompletedCandidates() }}</div>
                  <div class="text-body-2 text-medium-emphasis">Completed</div>
                </v-card>
              </div>
            </div>
            
            <!-- Chart placeholder -->
            <v-card class="pa-6">
              <h4 class="text-h6 mb-4">Campaign Progress</h4>
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

    <!-- Step Modal -->
    <v-dialog v-model="showStepModal" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          {{ stepFormData.name ? 'Edit' : 'Add' }} Campaign Step
        </v-card-title>
        <v-card-text>
          <v-form ref="stepForm" v-model="stepFormValid">
            <v-text-field
              v-model="stepFormData.campaign_step_name"
              label="Step Name *"
              :rules="[v => !!v || 'Step name is required']"
              required
            />
            <v-text-field
              v-model="stepFormData.step_order"
              label="Step Order *"
              type="number"
              :rules="[v => !!v || 'Step order is required']"
              required
            />
            <v-select
              v-model="stepFormData.action_type"
              :items="stepTypeOptions"
              label="Action Type *"
              :rules="[v => !!v || 'Action type is required']"
              required
            />
            <v-text-field
              v-model="stepFormData.delay_in_days"
              label="Delay in Days"
              type="number"
              min="0"
            />
            <v-textarea
              v-model="stepFormData.template"
              label="Template"
              rows="3"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeStepModal">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="savingStep"
            :disabled="!stepFormValid"
            @click="saveStep"
          >
            {{ stepFormData.name ? 'Update' : 'Save' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Candidate Assignment Modal -->
    <v-dialog v-model="showCandidateModal" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          Assign Candidate to Campaign
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
            <v-select
              v-model="candidateFormData.status"
              :items="statusOptions"
              label="Status *"
              :rules="[v => !!v || 'Status is required']"
              required
            />
            <v-text-field
              v-model="candidateFormData.current_step_order"
              label="Starting Step"
              type="number"
              value="1"
              min="1"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="grey" variant="text" @click="closeCandidateModal">
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            :loading="savingCandidate"
            :disabled="!candidateFormValid"
            @click="assignCandidate"
          >
            Assign
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Edit Campaign Modal -->
    <campaign-form
      v-model="showEditCampaignModal"
      :campaign="campaign"
      @success="handleCampaignUpdated"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  campaignService, 
  campaignStepService, 
  candidateCampaignService,
  candidateService,
  candidateSegmentService,
  talentSegmentService,
  actionService
} from '../services/universalService'
import CampaignForm from '@/components/campaign/CampaignForm.vue'
import moment from 'moment'

const route = useRoute()
const router = useRouter()

// State
const activeTab = ref('steps')
const loading = ref(false)
const loadingSteps = ref(false)
const loadingCandidates = ref(false)
const loadingActions = ref(false)

// Campaign data
const campaign = reactive({})
const targetSegment = ref(null)
const campaignSteps = ref([])
const candidateCampaigns = ref([])
const actions = ref([])
const availableCandidates = ref([])

// Modals
const showStepModal = ref(false)
const showCandidateModal = ref(false)
const showEditCampaignModal = ref(false)
const stepFormValid = ref(false)
const candidateFormValid = ref(false)
const savingStep = ref(false)
const savingCandidate = ref(false)
const assigningAll = ref(false)

// Form data
const stepFormData = reactive({
  name: '',
  campaign_step_name: '',
  step_order: '',
  action_type: '',
  delay_in_days: 0,
  template: '',
  campaign: route.params.id
})

const candidateFormData = reactive({
  candidate_id: '',
  campaign_id: route.params.id,
  status: 'ACTIVE',
  current_step_order: 1
})

// Options
const stepTypeOptions = [
  { title: 'Send Email', value: 'SEND_EMAIL' },
  { title: 'Send SMS', value: 'SEND_SMS' },
  { title: 'Manual Call', value: 'MANUAL_CALL' },
  { title: 'Manual Task', value: 'MANUAL_TASK' }
]

const statusOptions = [
  { title: 'Active', value: 'ACTIVE' },
  { title: 'Paused', value: 'PAUSED' },
  { title: 'Completed', value: 'COMPLETED' },
  { title: 'Cancelled', value: 'CANCELLED' }
]

// Table headers
const stepHeaders = [
  { title: 'Step Order', key: 'step_order' },
  { title: 'Step Name', key: 'campaign_step_name' },
  { title: 'Action Type', key: 'action_type' },
  { title: 'Delay (Days)', key: 'delay_in_days' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const candidateHeaders = [
  { title: 'Candidate', key: 'candidate_id' },
  { title: 'Status', key: 'status' },
  { title: 'Current Step', key: 'current_step_order' },
  { title: 'Enrolled At', key: 'enrolled_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

const actionHeaders = [
  { title: 'Campaign Step', key: 'campaign_step' },
  { title: 'Status', key: 'status' },
  { title: 'Scheduled At', key: 'scheduled_at' },
  { title: 'Executed At', key: 'executed_at' },
  { title: 'Actions', key: 'actions', sortable: false }
]

// Methods
const loadCampaign = async () => {
  loading.value = true
  try {
    const result = await campaignService.getFormData(route.params.id)
    if (result.success) {
      Object.assign(campaign, result.data)
      // Load target segment if exists
      if (campaign.target_segment) {
        await loadTargetSegment()
      }
    }
  } catch (error) {
    console.error('Error loading campaign:', error)
  } finally {
    loading.value = false
  }
}

const loadTargetSegment = async () => {
  if (!campaign.target_segment) return
  
  try {
    const result = await talentSegmentService.getFormData(campaign.target_segment)
    if (result.success) {
      targetSegment.value = result.data
    }
  } catch (error) {
    console.error('Error loading target segment:', error)
  }
}

const loadCampaignSteps = async () => {
  loadingSteps.value = true
  try {
    const result = await campaignStepService.getList({
      filters: { campaign: route.params.id },
      fields: ['name', 'campaign_step_name', 'step_order', 'action_type', 'delay_in_days']
    })
    if (result.success) {
      campaignSteps.value = result.data
    }
  } catch (error) {
    console.error('Error loading campaign steps:', error)
  } finally {
    loadingSteps.value = false
  }
}

const loadCandidateCampaigns = async () => {
  loadingCandidates.value = true
  try {
    const result = await candidateCampaignService.getList({
      filters: { campaign_id: route.params.id },
      fields: ['name', 'candidate_id', 'status', 'current_step_order', 'enrolled_at']
    })
    if (result.success) {
      candidateCampaigns.value = result.data
    }
  } catch (error) {
    console.error('Error loading candidate campaigns:', error)
  } finally {
    loadingCandidates.value = false
  }
}

const loadActions = async () => {
  loadingActions.value = true
  try {
    // Load actions for this campaign through CandidateCampaign
    const candidateCampaignsResult = await candidateCampaignService.getList({
      filters: { campaign_id: route.params.id },
      fields: ['name']
    })
    
    if (candidateCampaignsResult.success && candidateCampaignsResult.data.length > 0) {
      const candidateCampaignIds = candidateCampaignsResult.data.map(cc => cc.name)
      
      const result = await actionService.getList({
        filters: { candidate_campaign_id: ['in', candidateCampaignIds] },
        fields: ['name', 'campaign_step', 'status', 'scheduled_at', 'executed_at']
      })
      
      if (result.success) {
        actions.value = result.data
      }
    } else {
      actions.value = []
    }
  } catch (error) {
    console.error('Error loading actions:', error)
    actions.value = []
  } finally {
    loadingActions.value = false
  }
}

const loadAvailableCandidates = async () => {
  try {
    if (!campaign.target_segment) {
      // If no target segment, show all candidates
      const result = await candidateService.getList({
        fields: ['name', 'candidate_name'],
        page_length: 1000
      })
      if (result.success) {
        availableCandidates.value = result.data.map(item => ({
          title: item.candidate_name || item.name,
          value: item.name
        }))
      }
    } else {
      // Get candidates from target segment through CandidateSegment
      const candidateSegmentResult = await candidateSegmentService.getList({
        filters: { segment_id: campaign.target_segment },
        fields: ['candidate_id']
      })
      
      if (candidateSegmentResult.success && candidateSegmentResult.data.length > 0) {
        const candidateIds = candidateSegmentResult.data.map(cs => cs.candidate_id)
        
        // Get candidates already in this campaign
        const existingCandidateCampaigns = await candidateCampaignService.getList({
          filters: { campaign_id: route.params.id },
          fields: ['candidate_id']
        })
        
        const existingCandidateIds = existingCandidateCampaigns.success 
          ? existingCandidateCampaigns.data.map(cc => cc.candidate_id)
          : []
        
        // Filter out candidates already in campaign
        const availableCandidateIds = candidateIds.filter(
          id => !existingCandidateIds.includes(id)
        )
        
        if (availableCandidateIds.length > 0) {
          const candidateResult = await candidateService.getList({
            filters: { name: ['in', availableCandidateIds] },
            fields: ['name', 'candidate_name']
          })
          
          if (candidateResult.success) {
            availableCandidates.value = candidateResult.data.map(item => ({
              title: item.candidate_name || item.name,
              value: item.name
            }))
          }
        } else {
          availableCandidates.value = []
        }
      } else {
        availableCandidates.value = []
      }
    }
  } catch (error) {
    console.error('Error loading candidates:', error)
  }
}

// Step methods
const openStepModal = (step = null) => {
  if (step) {
    Object.assign(stepFormData, step)
  } else {
    Object.keys(stepFormData).forEach(key => {
      stepFormData[key] = ''
    })
    stepFormData.campaign = route.params.id
  }
  showStepModal.value = true
}

const closeStepModal = () => {
  showStepModal.value = false
  Object.keys(stepFormData).forEach(key => {
    stepFormData[key] = ''
  })
}

const saveStep = async () => {
  if (!stepFormValid.value) return

  savingStep.value = true
  try {
    const result = await campaignStepService.save(stepFormData, stepFormData.name)
    if (result.success) {
      closeStepModal()
      loadCampaignSteps()
    }
  } catch (error) {
    console.error('Error saving step:', error)
  } finally {
    savingStep.value = false
  }
}

const deleteStep = async (step) => {
  if (confirm('Are you sure you want to delete this step?')) {
    try {
      const result = await campaignStepService.delete(step.name)
      if (result.success) {
        loadCampaignSteps()
      }
    } catch (error) {
      console.error('Error deleting step:', error)
    }
  }
}

// Candidate methods
const openCandidateModal = async () => {
  Object.keys(candidateFormData).forEach(key => {
    candidateFormData[key] = ''
  })
  candidateFormData.campaign_id = route.params.id
  candidateFormData.status = 'ACTIVE'
  candidateFormData.current_step_order = 1
  
  // Reload available candidates to get most up-to-date list
  await loadAvailableCandidates()
  
  showCandidateModal.value = true
}

const closeCandidateModal = () => {
  showCandidateModal.value = false
}

const assignCandidate = async () => {
  if (!candidateFormValid.value) return

  savingCandidate.value = true
  try {
    const result = await candidateCampaignService.save(candidateFormData)
    if (result.success) {
      closeCandidateModal()
      loadCandidateCampaigns()
    }
  } catch (error) {
    console.error('Error assigning candidate:', error)
  } finally {
    savingCandidate.value = false
  }
}

const startCandidateCampaign = async (item) => {
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

const pauseCandidateCampaign = async (item) => {
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

const unassignCandidate = async (item) => {
  if (confirm('Are you sure you want to unassign this candidate?')) {
    try {
      const result = await candidateCampaignService.delete(item.name)
      if (result.success) {
        loadCandidateCampaigns()
      }
    } catch (error) {
      console.error('Error unassigning candidate:', error)
    }
  }
}

const viewCandidateDetails = (item) => {
  router.push(`/candidates/${item.candidate_id}`)
}

// Assign all candidates from segment
const assignAllFromSegment = async () => {
  if (!confirm(`Are you sure you want to assign all ${availableCandidates.value.length} candidates from the target segment to this campaign?`)) {
    return
  }
  
  assigningAll.value = true
  try {
    // Create CandidateCampaign records for all available candidates
    const promises = availableCandidates.value.map(candidate => 
      candidateCampaignService.save({
        candidate_id: candidate.value,
        campaign_id: route.params.id,
        status: 'ACTIVE',
        current_step_order: 1,
        enrolled_at: moment().format("YYYY-MM-DD HH:mm:ss")
      })
    )
    
    await Promise.all(promises)
    
    // Reload data
    await loadCandidateCampaigns()
    await loadAvailableCandidates()
    
    console.log('Successfully assigned all candidates from segment')
  } catch (error) {
    console.error('Error assigning all candidates:', error)
  } finally {
    assigningAll.value = false
  }
}

// Action methods
const openActionModal = () => {
  // Implementation for action modal
}

const viewActionDetails = (action) => {
  // Implementation for viewing action details
}

const deleteAction = async (action) => {
  if (confirm('Are you sure you want to delete this action?')) {
    try {
      const result = await actionService.delete(action.name)
      if (result.success) {
        loadActions()
      }
    } catch (error) {
      console.error('Error deleting action:', error)
    }
  }
}

// Utility methods
const getStatusColor = (status) => {
  const colors = {
    'ACTIVE': 'success',
    'PAUSED': 'warning',
    'COMPLETED': 'primary',
    'CANCELLED': 'error',
    'DRAFT': 'grey',
    'ARCHIVED': 'grey'
  }
  return colors[status] || 'grey'
}

const getTypeColor = (type) => {
  const colors = {
    'NURTURING': 'purple',
    'ATTRACTION': 'blue'
  }
  return colors[type] || 'grey'
}

const getStepTypeColor = (type) => {
  const colors = {
    'SEND_EMAIL': 'blue',
    'SEND_SMS': 'green',
    'MANUAL_CALL': 'orange',
    'MANUAL_TASK': 'purple'
  }
  return colors[type] || 'grey'
}

const getActionTypeColor = (type) => {
  const colors = {
    'SEND_EMAIL': 'blue',
    'SEND_SMS': 'green',
    'MANUAL_CALL': 'orange',
    'MANUAL_TASK': 'purple'
  }
  return colors[type] || 'grey'
}

const getActionStatusColor = (status) => {
  const colors = {
    'SCHEDULED': 'info',
    'EXECUTED': 'success',
    'SKIPPED': 'warning',
    'FAILED': 'error',
    'PENDING_MANUAL': 'orange'
  }
  return colors[status] || 'grey'
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

const getActiveCandidates = () => {
  return candidateCampaigns.value.filter(item => item.status === 'ACTIVE').length
}

const getCompletedCandidates = () => {
  return candidateCampaigns.value.filter(item => item.status === 'COMPLETED').length
}

const editCampaign = () => {
  // Ensure we have loaded campaign data before opening modal
  if (Object.keys(campaign).length === 0) {
    console.warn('Campaign data not loaded yet')
    return
  }
  // Open edit modal with current campaign data
  showEditCampaignModal.value = true
}

const handleCampaignUpdated = async () => {
  console.log('Campaign updated successfully')
  // Reload campaign data
  await loadCampaign()
}

const deleteCampaign = async () => {
  if (confirm('Are you sure you want to delete this campaign?')) {
    try {
      const result = await campaignService.delete(route.params.id)
      if (result.success) {
        router.push('/campaigns')
      }
    } catch (error) {
      console.error('Error deleting campaign:', error)
    }
  }
}

const viewTargetSegment = () => {
  if (targetSegment.value) {
    router.push(`/talent-segments/${targetSegment.value.name}/detail`)
  }
}

// Lifecycle
onMounted(async () => {
  await loadCampaign()
  await loadCampaignSteps()
  await loadCandidateCampaigns()
  await loadActions()
  await loadAvailableCandidates()
})
</script>

<style scoped>
.campaign-detail-view {
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
