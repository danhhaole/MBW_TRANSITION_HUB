<template>
  <v-container fluid class="pa-4">
    <!-- Debug info -->
    <div v-if="!loading && campaigns?.length === 0" class="text-center pa-8">
      <v-alert type="info" text="Không có campaign nào để hiển thị" />
    </div>
    
    <v-row v-if="!loading && campaigns?.length > 0">
      <v-col
        v-for="campaign in campaigns"
        :key="campaign.name"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card class="h-100 campaign-card">
          <!-- Card Header với background màu -->
          <div 
            class="pa-3 d-flex justify-space-between align-center"
            :class="getHeaderClass(campaign.status)"
          >
            <span class="font-medium" :class="getHeaderTextClass(campaign.status)">
              {{ campaign.type === 'NURTURING' ? 'Nuôi dưỡng' : 'Thu hút' }}
            </span>
            <v-chip
              :color="getStatusColor(campaign.displayStatus || campaign.status)"
              :class="getStatusChipClass(campaign.status)"
              size="x-small"
            >
              {{ getStatusText(campaign.displayStatus || campaign.status) }}
            </v-chip>
          </div>

          <!-- Card Content -->
          <v-card-text class="pa-4">
            <h3 class="text-h6 font-weight-semibold text-grey-darken-3 mb-2">
              {{ campaign.campaign_name }}
            </h3>
            <p class="text-body-2 text-grey-darken-1 mb-4">
              {{ campaign.description || 'Tuyển dụng cho vị trí quan trọng trong công ty.' }}
            </p>

            <!-- Progress section -->
            <div class="mb-4">
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="text-caption text-grey-darken-1">Tiến độ</span>
                <span class="text-caption font-medium" :class="getProgressTextClass(campaign)">
                  {{ getCampaignSteps(campaign) }}
                </span>
              </div>
              
              <!-- Progress bar với design giống HTML -->
              <div class="progress-container mb-4">
                <div 
                  class="progress-bar"
                  :style="{ width: getCampaignProgress(campaign) + '%' }"
                  :class="getProgressBarClass(campaign)"
                ></div>
              </div>

              <!-- Timeline info -->
              <div class="d-flex justify-space-between align-center text-caption mb-4">
                <div class="d-flex align-center">
                  <v-icon size="16" color="grey-lighten-1" class="mr-1">mdi-calendar</v-icon>
                  <span class="text-grey-darken-1">{{ campaign.formattedStartDate || 'Chưa xác định' }}</span>
                </div>
                
                <!-- Owner avatars -->
                <div class="d-flex" style="margin-left: -8px;">
                  <v-avatar
                    v-if="campaign.owner_id"
                    size="24"
                    :color="getOwnerColor(campaign.owner_id)"
                    class="border-2 border-white"
                    style="margin-left: -8px;"
                  >
                    <span class="text-caption font-medium text-white">
                      {{ getInitials(campaign.owner_id) }}
                    </span>
                  </v-avatar>
                  <v-avatar
                    v-if="campaign.target_segment"
                    size="24"
                    color="purple-lighten-3"
                    class="border-2 border-white"
                    style="margin-left: -8px;"
                  >
                    <span class="text-caption font-medium text-purple-darken-2">
                      {{ getInitials(campaign.target_segment) }}
                    </span>
                  </v-avatar>
                  <v-avatar
                    v-if="getTeamCount(campaign) > 2"
                    size="24"
                    color="green-lighten-3"
                    class="border-2 border-white"
                    style="margin-left: -8px;"
                  >
                    <span class="text-caption font-medium text-green-darken-2">
                      +{{ getTeamCount(campaign) - 2 }}
                    </span>
                  </v-avatar>
                </div>
              </div>
            </div>
          </v-card-text>

          <!-- Card Footer -->
          <v-divider />
          <div class="pa-3 bg-grey-lighten-5 d-flex justify-space-between align-center">
            <v-btn
              variant="text"
              size="small"
              color="grey-darken-1"
              class="text-caption"
              @click="$emit('view', campaign)"
            >
              <v-icon size="16" class="mr-1">mdi-eye</v-icon>
              Chi tiết
            </v-btn>
            
            <v-btn
              variant="text"
              size="small"
              color="primary"
              class="text-caption font-medium"
              @click="$emit('view', campaign)"
            >
              Xem timeline →
            </v-btn>
          </div>
        </v-card>
      </v-col>

      <!-- Add new card -->
      <v-col cols="12" sm="6" md="4" lg="3">
        <v-card 
          class="h-100 d-flex align-center justify-center create-card"
          variant="outlined"
          style="border-style: dashed;"
          @click="$emit('create')"
        >
          <div class="text-center pa-8">
            <div class="mx-auto mb-3 d-flex align-center justify-center">
              <v-avatar size="48" color="primary" variant="tonal">
                <v-icon size="24" color="primary">mdi-plus</v-icon>
              </v-avatar>
            </div>
            <h3 class="text-h6 font-weight-semibold text-grey-darken-3 mb-1">
              Tạo yêu cầu mới
            </h3>
            <p class="text-body-2 text-grey-darken-1">
              Bắt đầu một yêu cầu tuyển dụng mới
            </p>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Loading Skeleton -->
    <v-row v-if="loading">
      <v-col
        v-for="n in 8"
        :key="n"
        cols="12"
        sm="6"
        md="4"
        lg="3"
      >
        <v-card>
          <v-skeleton-loader type="card" />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  campaigns: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

console.log('CampaignCardView - campaigns:', props.campaigns)
console.log('CampaignCardView - campaigns length:', props.campaigns?.length)

// Emits
defineEmits(['edit', 'view', 'delete', 'create'])

// Helper functions
const getHeaderClass = (status) => {
  const classes = {
    'DRAFT': 'bg-grey-lighten-4',
    'ACTIVE': 'bg-blue-lighten-5',
    'PAUSED': 'bg-yellow-lighten-5',
    'ARCHIVED': 'bg-grey-lighten-4'
  }
  return classes[status] || 'bg-grey-lighten-4'
}

const getHeaderTextClass = (status) => {
  const classes = {
    'DRAFT': 'text-grey-darken-2',
    'ACTIVE': 'text-blue-darken-2',
    'PAUSED': 'text-yellow-darken-3',
    'ARCHIVED': 'text-grey-darken-2'
  }
  return classes[status] || 'text-grey-darken-2'
}

const getStatusColor = (status) => {
  const colors = {
    'DRAFT': 'grey',
    'ACTIVE': 'blue',
    'PAUSED': 'yellow-darken-1',
    'ARCHIVED': 'green'
  }
  return colors[status] || 'grey'
}

const getStatusChipClass = (status) => {
  const classes = {
    'DRAFT': 'text-grey-darken-3',
    'ACTIVE': 'text-blue-darken-3',
    'PAUSED': 'text-yellow-darken-4',
    'ARCHIVED': 'text-green-darken-3'
  }
  return classes[status] || 'text-grey-darken-3'
}

const getStatusText = (status) => {
  const texts = {
    'DRAFT': 'Nháp',
    'ACTIVE': 'Đang tiến hành',
    'PAUSED': 'Tạm dừng',
    'ARCHIVED': 'Hoàn thành'
  }
  return texts[status] || status
}

const getCampaignProgress = (campaign) => {
  if (!campaign.start_date || !campaign.end_date) return 0
  
  const now = new Date()
  const start = new Date(campaign.start_date)
  const end = new Date(campaign.end_date)
  
  if (now < start) return 0
  if (now > end) return 100
  
  const total = end - start
  const current = now - start
  return Math.round((current / total) * 100)
}

const getCampaignSteps = (campaign) => {
  const progress = getCampaignProgress(campaign)
  const totalSteps = 5
  const currentStep = Math.ceil((progress / 100) * totalSteps)
  return `${currentStep}/${totalSteps} bước`
}

const getProgressBarClass = (campaign) => {
  const progress = getCampaignProgress(campaign)
  if (progress === 0) return 'bg-grey'
  if (progress < 30) return 'bg-blue-darken-1'
  if (progress < 70) return 'bg-yellow-darken-1'
  return 'bg-green'
}

const getProgressTextClass = (campaign) => {
  const progress = getCampaignProgress(campaign)
  if (progress === 0) return 'text-grey-darken-2'
  if (progress < 30) return 'text-blue-darken-2'
  if (progress < 70) return 'text-yellow-darken-3'
  return 'text-green-darken-2'
}

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

const getOwnerColor = (owner) => {
  const colors = ['blue-lighten-3', 'purple-lighten-3', 'green-lighten-3', 'orange-lighten-3']
  const hash = owner.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const getTeamCount = (campaign) => {
  let count = 0
  if (campaign.owner_id) count++
  if (campaign.target_segment) count++
  return count + 2 // Simulate additional team members
}
</script>

<style scoped>
.campaign-card {
  transition: all 0.3s ease;
}

.campaign-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}

.create-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.create-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.1);
  border-color: rgb(var(--v-theme-primary)) !important;
}

.progress-container {
  height: 6px;
  background-color: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}
</style> 