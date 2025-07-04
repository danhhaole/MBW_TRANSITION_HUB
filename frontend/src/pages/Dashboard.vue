<template>
    <v-container fluid class="pa-6">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-h3 font-weight-bold text-slate-800 mb-2">Dashboard Tổng quan</h1>
            <p class="text-subtitle-1 text-medium-emphasis">Chào mừng trở lại! Đây là tình hình các hoạt động của bạn
                hôm nay.</p>
        </div>

        <v-row>
            <!-- Main Content -->
            <v-col cols="12" lg="8">
                <!-- My Tasks Section -->
                <v-card class="mb-6" elevation="1">
                    <v-card-title>
                        <v-icon class="mr-2">mdi-clipboard-check</v-icon>
                        Tác vụ của tôi ({{ tasks.length }})
                    </v-card-title>

                    <v-card-text>
                        <div v-if="tasks.length === 0" class="text-center py-8">
                            <v-icon size="64" color="success">mdi-party-popper</v-icon>
                            <p class="text-h6 mt-4 text-medium-emphasis">Chúc mừng! Bạn đã hoàn thành tất cả các tác vụ.
                            </p>
                        </div>

                        <v-list v-else lines="two">
                            <v-list-item v-for="task in tasks" :key="task.id" class="mb-2" rounded="lg" border>
                                <template v-slot:prepend>
                                    <v-avatar color="grey-lighten-3">
                                        <v-icon v-if="task.type === 'MANUAL_CALL'">mdi-phone</v-icon>
                                        <v-icon v-else>mdi-clipboard-text</v-icon>
                                    </v-avatar>
                                </template>

                                <v-list-item-title>
                                    {{ task.title }}: <strong>{{ task.candidate }}</strong>
                                </v-list-item-title>
                                <v-list-item-subtitle>
                                    Chiến dịch: {{ task.campaign }}
                                </v-list-item-subtitle>

                                <template v-slot:append>
                                    <div class="text-right">
                                        <v-chip :color="task.dueDate === 'Hôm nay' ? 'error' : 'warning'" size="small"
                                            variant="flat" class="mb-2">
                                            {{ task.dueDate }}
                                        </v-chip>
                                        <br>
                                        <v-btn color="primary" size="small" variant="flat" @click="openTaskModal(task)">
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
                        <v-row>
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
                        <v-list lines="two">
                            <v-list-item v-for="campaign in completedCampaigns" :key="campaign.id" class="mb-2"
                                rounded="lg">
                                <template v-slot:prepend>
                                    <v-avatar color="blue-lighten-4">
                                        <v-icon color="blue">mdi-check</v-icon>
                                    </v-avatar>
                                </template>

                                <v-list-item-title class="font-weight-medium">
                                    {{ campaign.name }}
                                </v-list-item-title>
                                <v-list-item-subtitle>
                                    {{ campaign.stats.newApplicants }} ứng viên mới
                                </v-list-item-subtitle>
                            </v-list-item>
                        </v-list>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <!-- Task Update Modal -->
        <TaskUpdateModal v-model="taskModal" :task="selectedTask" @update:completed="handleTaskCompleted" />
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import CampaignCard from '@/components/campaign/CampaignCard.vue'
import TaskUpdateModal from '@/components/shared/TaskUpdateModal.vue'

// Reactive data
const tasks = ref([])
const activeCampaigns = ref([])
const completedCampaigns = ref([])
const taskModal = ref(false)
const selectedTask = ref(null)

// API Resources
const dashboardResource = createResource({
    url: 'mbw_mira.api.test_data.get_test_dashboard_data', // Use test data for now
    method: 'GET',
    auto: false,
    onSuccess: (data) => {
        console.log(data)
        if (data) {
            tasks.value = data.tasks || []
            activeCampaigns.value = data.activeCampaigns || []
            completedCampaigns.value = data.completedCampaigns || []
        }
    }
})

const updateTaskResource = createResource({
    url: 'mbw_mira.api.test_data.test_update_task', // Use test API for now
    method: 'POST'
})

// Methods
const openTaskModal = (task) => {
    selectedTask.value = task
    taskModal.value = true
}

const handleTaskCompleted = async (taskData) => {
    try {
        await updateTaskResource.submit(taskData)
        await refreshData()
        taskModal.value = false
    } catch (error) {
        console.error('Error updating task:', error)
    }
}

const refreshData = async () => {
    await dashboardResource.fetch()
    const data = dashboardResource.data
    if (data) {
        tasks.value = data.tasks || []
        activeCampaigns.value = data.activeCampaigns || []
        completedCampaigns.value = data.completedCampaigns || []
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