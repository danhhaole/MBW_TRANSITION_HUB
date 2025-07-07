<template>
    <v-container fluid class="pa-6">
        <!-- Header -->
        <div class="mb-8">
            <div class="d-flex justify-space-between align-center">
                <div>
                    <h1 class="text-h3 font-weight-bold text-slate-800 mb-2">Dashboard Tổng quan</h1>
                    <p class="text-subtitle-1 text-medium-emphasis">Chào mừng trở lại! Đây là tình hình các hoạt động của bạn
                        hôm nay.</p>
                </div>
                <v-btn
                    color="primary"
                    variant="outlined"
                    prepend-icon="mdi-refresh"
                    @click="refreshData"
                    :loading="loading"
                >
                    Làm mới
                </v-btn>
            </div>
        </div>

        <v-row>
            <!-- Summary Stats -->
            <v-col cols="12" class="mb-4">
                <v-row>
                    <v-col cols="12" sm="6" md="3">
                        <v-card elevation="1" class="text-center pa-4">
                            <v-icon size="32" color="primary" class="mb-2">mdi-clipboard-check</v-icon>
                            <div class="text-h5 font-weight-bold">{{ tasks.length }}</div>
                            <div class="text-body-2 text-medium-emphasis">Tác vụ đang chờ</div>
                        </v-card>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                        <v-card elevation="1" class="text-center pa-4">
                            <v-icon size="32" color="success" class="mb-2">mdi-bullhorn</v-icon>
                            <div class="text-h5 font-weight-bold">{{ activeCampaigns.length }}</div>
                            <div class="text-body-2 text-medium-emphasis">Chiến dịch hoạt động</div>
                        </v-card>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                        <v-card elevation="1" class="text-center pa-4">
                            <v-icon size="32" color="info" class="mb-2">mdi-check-circle</v-icon>
                            <div class="text-h5 font-weight-bold">{{ completedCampaigns.length }}</div>
                            <div class="text-body-2 text-medium-emphasis">Hoàn thành gần đây</div>
                        </v-card>
                    </v-col>
                    <v-col cols="12" sm="6" md="3">
                        <v-card elevation="1" class="text-center pa-4">
                            <v-icon size="32" color="warning" class="mb-2">mdi-clock-alert</v-icon>
                            <div class="text-h5 font-weight-bold">{{ urgentTasks.length }}</div>
                            <div class="text-body-2 text-medium-emphasis">Tác vụ cấp bách</div>
                        </v-card>
                    </v-col>
                </v-row>
            </v-col>

            <!-- Main Content -->
            <v-col cols="12" lg="8">
                <!-- My Tasks Section -->
                <v-card class="mb-6" elevation="1">
                    <v-card-title>
                        <v-icon class="mr-2">mdi-clipboard-check</v-icon>
                        Tác vụ của tôi ({{ tasks.length }})
                    </v-card-title>

                    <v-card-text>
                        <div v-if="loading" class="text-center py-8">
                            <v-progress-circular indeterminate color="primary" class="mb-4"></v-progress-circular>
                            <p class="text-body-2 text-medium-emphasis">Đang tải dữ liệu...</p>
                        </div>

                        <div v-else-if="tasks.length === 0" class="text-center py-8">
                            <v-icon size="64" color="success">mdi-party-popper</v-icon>
                            <p class="text-h6 mt-4 text-medium-emphasis">Chúc mừng! Bạn đã hoàn thành tất cả các tác vụ.
                            </p>
                        </div>

                        <v-list v-else lines="two">
                            <v-list-item v-for="task in tasks" :key="task.id" class="mb-2" rounded="lg" border>
                                <template v-slot:prepend>
                                    <v-avatar :color="getTaskColor(task.dueDate)">
                                        <v-icon v-if="task.status === 'PENDING_MANUAL'">mdi-account-check</v-icon>
                                        <v-icon v-else-if="task.status === 'SCHEDULED'">mdi-calendar-clock</v-icon>
                                        <v-icon v-else-if="task.status === 'EXECUTED'">mdi-check-circle</v-icon>
                                        <v-icon v-else-if="task.status === 'FAILED'">mdi-alert-circle</v-icon>
                                        <v-icon v-else>mdi-clipboard-text</v-icon>
                                    </v-avatar>
                                </template>

                                <v-list-item-title>
                                    {{ task.title }}: <strong>{{ task.candidate }}</strong>
                                </v-list-item-title>
                                <v-list-item-subtitle>
                                    Chiến dịch: {{ task.campaign }}
                                    <v-chip 
                                      v-if="task.status === 'PENDING_MANUAL'" 
                                      color="warning" 
                                      size="x-small" 
                                      variant="tonal"
                                      class="ml-2"
                                    >
                                      Chờ xác nhận
                                    </v-chip>
                                    <v-chip 
                                      v-else-if="task.status === 'SCHEDULED'" 
                                      color="info" 
                                      size="x-small" 
                                      variant="tonal"
                                      class="ml-2"
                                    >
                                      Đã lên lịch
                                    </v-chip>
                                </v-list-item-subtitle>

                                <template v-slot:append>
                                    <div class="text-right">
                                        <v-chip 
                                          :color="getDueDateColor(task.dueDate)" 
                                          size="small"
                                          variant="flat" 
                                          class="mb-2"
                                        >
                                            {{ task.dueDate }}
                                        </v-chip>
                                        <br>
                                        <v-btn 
                                          color="primary" 
                                          size="small" 
                                          variant="flat" 
                                          @click="openTaskModal(task)"
                                          :loading="loading"
                                        >
                                            Cập nhật
                                        </v-btn>
                                    </div>
                                </template>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>

                <!-- Active Campaigns Section -->
                <v-card elevation="1">
                    <v-card-title>
                        <v-icon class="mr-2">mdi-bullhorn</v-icon>
                        Các chiến dịch đang hoạt động
                    </v-card-title>

                    <v-card-text>
                        <div v-if="loading" class="text-center py-8">
                            <v-progress-circular indeterminate color="primary" class="mb-4"></v-progress-circular>
                            <p class="text-body-2 text-medium-emphasis">Đang tải chiến dịch...</p>
                        </div>

                        <div v-else-if="activeCampaigns.length === 0" class="text-center py-8">
                            <v-icon size="64" color="grey-lighten-1">mdi-bullhorn-outline</v-icon>
                            <p class="text-body-1 text-medium-emphasis mt-4">Chưa có chiến dịch nào đang hoạt động</p>
                        </div>

                        <v-row v-else>
                            <v-col v-for="campaign in activeCampaigns" :key="campaign.id" cols="12" md="6">
                                <CampaignCard :campaign="campaign" />
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>

            <!-- Sidebar -->
            <v-col cols="12" lg="4">
                <v-card elevation="1">
                    <v-card-title>
                        <v-icon class="mr-2">mdi-check-circle</v-icon>
                        Đã hoàn thành gần đây
                    </v-card-title>

                    <v-card-text>
                        <div v-if="loading" class="text-center py-8">
                            <v-progress-circular indeterminate color="primary" size="24" class="mb-4"></v-progress-circular>
                            <p class="text-caption text-medium-emphasis">Đang tải...</p>
                        </div>

                        <div v-else-if="completedCampaigns.length === 0" class="text-center py-8">
                            <v-icon size="48" color="grey-lighten-1">mdi-check-circle-outline</v-icon>
                            <p class="text-body-2 text-medium-emphasis mt-2">Chưa có chiến dịch nào hoàn thành gần đây</p>
                        </div>

                        <v-list v-else lines="two">
                            <v-list-item v-for="campaign in completedCampaigns" :key="campaign.id" class="mb-2"
                                rounded="lg">
                                <template v-slot:prepend>
                                    <v-avatar color="green-lighten-4">
                                        <v-icon color="green">mdi-check</v-icon>
                                    </v-avatar>
                                </template>

                                <v-list-item-title class="font-weight-medium">
                                    {{ campaign.name }}
                                </v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ campaign.stats.newApplicants }} tác vụ đã hoàn thành
                                </v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Task Update Modal -->
        <TaskUpdateModal v-model="taskModal" :task="selectedTask" @update:completed="handleTaskCompleted" />

        <!-- Toast Container -->
        <ToastContainer 
            :show="showToast" 
            :message="toastMessage"
            :type="toastType"
            @close="closeToast"
        />
    </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { createResource } from 'frappe-ui'
import CampaignCard from '@/components/campaign/CampaignCard.vue'
import TaskUpdateModal from '@/components/shared/TaskUpdateModal.vue'
import { ToastContainer } from '@/components/shared'
import { 
  campaignService, 
  candidateCampaignService, 
  actionService,
  candidateService 
} from '../services/universalService'

// Reactive data
const tasks = ref([])
const activeCampaigns = ref([])
const completedCampaigns = ref([])
const taskModal = ref(false)
const selectedTask = ref(null)
const loading = ref(false)

// Toast state
const toastMessage = ref('')
const toastType = ref('success')
const showToast = ref(false)

// Computed properties
const urgentTasks = computed(() => {
  return tasks.value.filter(task => 
    (task.dueDate === 'Hôm nay' || task.dueDate === 'Quá hạn') && 
    task.status === 'PENDING_MANUAL'
  )
})

// Load Tasks from Action doctype
const loadTasks = async () => {
  try {
    const result = await actionService.getList({
      filters: { 
        status: ['in', ['PENDING_MANUAL', 'SCHEDULED']]
      },
      fields: ['name', 'status', 'scheduled_at', 'executed_at', 'candidate_campaign_id', 'campaign_step', 'assignee_id'],
      order_by: 'scheduled_at asc',
      page_length: 10
    })

    if (result.success) {
      // Transform actions to tasks format
      const actionsWithDetails = await Promise.all(
        result.data.map(async (action) => {
          // Get candidate campaign details
          const ccResult = await candidateCampaignService.getFormData(action.candidate_campaign_id)
          if (ccResult.success) {
            const candidateResult = await candidateService.getFormData(ccResult.data.candidate_id)
            const campaignResult = await campaignService.getFormData(ccResult.data.campaign_id)
            
            return {
              id: action.name,
              title: getActionTitle(action.status),
              type: action.status,
              candidate: candidateResult.success ? candidateResult.data.candidate_name || candidateResult.data.full_name : 'Unknown',
              campaign: campaignResult.success ? campaignResult.data.campaign_name : 'Unknown',
              dueDate: formatDueDate(action.scheduled_at),
              status: action.status,
              description: `${getActionTitle(action.status)} cho chiến dịch ${campaignResult.success ? campaignResult.data.campaign_name : 'Unknown'}`,
              candidateCampaignId: action.candidate_campaign_id
            }
          }
          return null
        })
      )
      
      tasks.value = actionsWithDetails.filter(task => task !== null)
    }
  } catch (error) {
    console.error('Error loading tasks:', error)
    tasks.value = []
  }
}

// Load Active Campaigns
const loadActiveCampaigns = async () => {
  try {
    const result = await campaignService.getList({
      filters: { status: 'ACTIVE' },
      fields: ['name', 'campaign_name', 'description', 'status', 'creation'],
      order_by: 'creation desc',
      page_length: 6
    })

    if (result.success) {
      // Get stats for each campaign
      const campaignsWithStats = await Promise.all(
        result.data.map(async (campaign) => {
          const ccResult = await candidateCampaignService.getList({
            filters: { campaign_id: campaign.name },
            fields: ['status', 'creation'],
            page_length: 1000
          })
          
          let stats = { total: 0, active: 0, completed: 0, newApplicants: 0 }
          if (ccResult.success) {
            stats.total = ccResult.data.length
            stats.active = ccResult.data.filter(cc => cc.status === 'ACTIVE').length
            stats.completed = ccResult.data.filter(cc => cc.status === 'COMPLETED').length
            // Use total count as newApplicants (total candidates in campaign)
            stats.newApplicants = stats.total
          }

          return {
            id: campaign.name,
            name: campaign.campaign_name,
            description: campaign.description,
            status: campaign.status.toLowerCase(),
            stats: {
              ...stats,
              candidates: stats.total, // Total candidates in campaign
              openRate: stats.total > 0 ? (stats.active / stats.total * 100).toFixed(1) : 0,
              clickRate: stats.total > 0 ? (stats.completed / stats.total * 100).toFixed(1) : 0
            }
          }
        })
      )
      
      activeCampaigns.value = campaignsWithStats
    }
  } catch (error) {
    console.error('Error loading active campaigns:', error)
    activeCampaigns.value = []
  }
}

// Load Completed Campaigns (recently completed)
const loadCompletedCampaigns = async () => {
  try {
    // Get recently executed actions to show completed campaigns
    const actionsResult = await actionService.getList({
      filters: { status: 'EXECUTED' },
      fields: ['name', 'executed_at', 'candidate_campaign_id'],
      order_by: 'executed_at desc',
      page_length: 20
    })

    if (actionsResult.success) {
      // Group by campaign and get campaign details
      const campaignMap = new Map()
      
      for (const action of actionsResult.data) {
        const ccResult = await candidateCampaignService.getFormData(action.candidate_campaign_id)
        if (ccResult.success) {
          const campaignId = ccResult.data.campaign_id
          if (!campaignMap.has(campaignId)) {
            const campaignResult = await campaignService.getFormData(campaignId)
            if (campaignResult.success) {
              campaignMap.set(campaignId, {
                id: campaignId,
                name: campaignResult.data.campaign_name,
                completedTasks: 1,
                lastCompleted: action.executed_at
              })
            }
          } else {
            campaignMap.get(campaignId).completedTasks++
          }
        }
      }
      
      // Convert to array and sort by last completed
      const campaigns = Array.from(campaignMap.values())
        .sort((a, b) => new Date(b.lastCompleted) - new Date(a.lastCompleted))
        .slice(0, 5)
        .map(campaign => ({
          id: campaign.id,
          name: campaign.name,
          stats: {
            newApplicants: campaign.completedTasks // Show completed tasks as "new applicants"
          }
        }))
      
      completedCampaigns.value = campaigns
    }
  } catch (error) {
    console.error('Error loading completed campaigns:', error)
    completedCampaigns.value = []
  }
}

// Update task using frappe.client.set_value
const updateTaskResource = createResource({
  url: 'frappe.client.set_value',
  method: 'POST'
})

// Helper functions
const showToastMessage = (message, type = 'success') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
}

const closeToast = () => {
  showToast.value = false
  toastMessage.value = ''
}

const getActionTitle = (actionStatus) => {
  const titles = {
    'SCHEDULED': 'Đã lên lịch',
    'EXECUTED': 'Đã hoàn thành',
    'SKIPPED': 'Đã bỏ qua',
    'FAILED': 'Thất bại',
    'PENDING_MANUAL': 'Chờ xác nhận'
  }
  return titles[actionStatus] || 'Tác vụ'
}

const formatDueDate = (dueDate) => {
  if (!dueDate) return 'Không xác định'
  
  const due = new Date(dueDate)
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  // Reset time for date comparison
  due.setHours(0, 0, 0, 0)
  today.setHours(0, 0, 0, 0)
  tomorrow.setHours(0, 0, 0, 0)
  
  if (due.getTime() === today.getTime()) {
    return 'Hôm nay'
  } else if (due.getTime() === tomorrow.getTime()) {
    return 'Ngày mai'
  } else if (due < today) {
    return 'Quá hạn'
  } else {
    return due.toLocaleDateString('vi-VN', { 
      day: '2-digit', 
      month: '2-digit'
    })
  }
}

const getDueDateColor = (dueDate) => {
  switch (dueDate) {
    case 'Hôm nay':
    case 'Quá hạn':
      return 'error'
    case 'Ngày mai':
      return 'warning'
    default:
      return 'info'
  }
}

const getTaskColor = (dueDate) => {
  switch (dueDate) {
    case 'Hôm nay':
    case 'Quá hạn':
      return 'error'
    case 'Ngày mai':
      return 'warning'
    default:
      return 'grey-lighten-3'
  }
}

// Methods
const openTaskModal = (task) => {
  selectedTask.value = task
  taskModal.value = true
}

const handleTaskCompleted = async (taskData) => {
  try {
    loading.value = true
    
    // Update action status based on the selected action
    await updateTaskResource.submit({
      doctype: 'Action',
      name: taskData.taskId,
      fieldname: 'status',
      value: taskData.action
    })
    
    // Update appropriate datetime field based on action
    if (taskData.action === 'EXECUTED') {
      // Set executed_at to current time in Frappe format
      const now = new Date()
      const frappeFormat = now.getFullYear() + '-' + 
                          String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                          String(now.getDate()).padStart(2, '0') + ' ' + 
                          String(now.getHours()).padStart(2, '0') + ':' + 
                          String(now.getMinutes()).padStart(2, '0') + ':' + 
                          String(now.getSeconds()).padStart(2, '0')
      
      await updateTaskResource.submit({
        doctype: 'Action',
        name: taskData.taskId,
        fieldname: 'executed_at',
        value: frappeFormat
      })
    } else if (taskData.action === 'SCHEDULED' && taskData.scheduledDate) {
      // Set scheduled_at to the specified date in Frappe format
      const scheduledDateTime = new Date(taskData.scheduledDate)
      const frappeFormat = scheduledDateTime.getFullYear() + '-' + 
                          String(scheduledDateTime.getMonth() + 1).padStart(2, '0') + '-' + 
                          String(scheduledDateTime.getDate()).padStart(2, '0') + ' ' + 
                          String(scheduledDateTime.getHours()).padStart(2, '0') + ':' + 
                          String(scheduledDateTime.getMinutes()).padStart(2, '0') + ':' + 
                          String(scheduledDateTime.getSeconds()).padStart(2, '0')
      
      await updateTaskResource.submit({
        doctype: 'Action',
        name: taskData.taskId,
        fieldname: 'scheduled_at',
        value: frappeFormat
      })
    }
    
    // Store notes in the result field as JSON if provided
    if (taskData.notes) {
      const now = new Date()
      const frappeFormat = now.getFullYear() + '-' + 
                          String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                          String(now.getDate()).padStart(2, '0') + ' ' + 
                          String(now.getHours()).padStart(2, '0') + ':' + 
                          String(now.getMinutes()).padStart(2, '0') + ':' + 
                          String(now.getSeconds()).padStart(2, '0')
      
      await updateTaskResource.submit({
        doctype: 'Action',
        name: taskData.taskId,
        fieldname: 'result',
        value: JSON.stringify({ 
          notes: taskData.notes, 
          action: taskData.action,
          updated_by: 'user',
          updated_at: frappeFormat
        })
      })
    }
     // Show success message
    const actionMessages = {
      'EXECUTED': 'Tác vụ đã được hoàn thành',
      'SCHEDULED': 'Tác vụ đã được lên lịch',
      'SKIPPED': 'Tác vụ đã được bỏ qua',
      'FAILED': 'Tác vụ đã được đánh dấu thất bại'
    }
    
    showToastMessage(actionMessages[taskData.action] || 'Tác vụ đã được cập nhật', 'success')
    
    // Refresh data
    await refreshData()
    
  } catch (error) {
    console.error('Error updating task:', error)
    showToastMessage('Không thể cập nhật tác vụ. Vui lòng thử lại.', 'error')
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadTasks(),
      loadActiveCampaigns(), 
      loadCompletedCampaigns()
    ])
  } catch (error) {
    console.error('Error refreshing data:', error)
    showToastMessage('Không thể tải dữ liệu. Vui lòng thử lại.', 'error')
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  refreshData()
})

</script>

<style scoped>
.text-slate-800 {
    color: rgb(30, 41, 59);
}
</style>