<template>
    <v-dialog
      v-model="dialog"
      max-width="800px"
    >
      <v-card v-if="campaign" class="rounded-xl">
        <v-card-title class="pa-6">
          <div class="d-flex align-center">
            <v-avatar
              size="40"
              :color="getTypeColor(campaign.type)"
              class="mr-3"
              variant="tonal"
            >
              <v-icon color="white">{{ getTypeIcon(campaign.type) }}</v-icon>
            </v-avatar>
            <div>
              <h2 class="text-h5 font-weight-bold">{{ campaign.campaign_name }}</h2>
              <div class="d-flex align-center mt-1">
                <v-chip
                  :color="getStatusColor(campaign.displayStatus || campaign.status)"
                  variant="tonal"
                  size="small"
                  class="mr-2"
                >
                  {{ __(getStatusText(campaign.displayStatus || campaign.status)) }}
                </v-chip>
                <v-chip
                  :color="getTypeColor(campaign.type)"
                  variant="outlined"
                  size="small"
                  class="mr-2"
                >
                  {{ __(getTypeText(campaign.type)) }}
                </v-chip>
                <v-chip
                  :color="campaign.is_active ? 'success' : 'error'"
                  variant="tonal"
                  size="small"
                >
                  {{ campaign.is_active ? __('Active') : __('Inactive') }}
                </v-chip>
              </div>
            </div>
          </div>
        </v-card-title>
  
        <v-divider />
  
        <v-card-text class="pa-6">
          <v-row>
            <v-col cols="12" md="6">
              <!-- Thông tin cơ bản -->
              <div class="mb-4">
                <p class="text-subtitle-2 text-grey-darken-1 mb-1">Mô tả</p>
                <p class="text-body-1">{{ campaign.description || 'Không có mô tả' }}</p>
              </div>
              
              <div class="mb-4">
                <p class="text-subtitle-2 text-grey-darken-1 mb-1">Phân khúc mục tiêu</p>
                <v-chip
                  v-if="campaign.target_segment"
                  color="info"
                  variant="outlined"
                  size="small"
                >
                  {{ campaign.target_segment }}
                </v-chip>
                <span v-else class="text-grey">Chưa xác định</span>
              </div>
  
              <!-- Tiến độ -->
              <div class="mb-4">
                <p class="text-subtitle-2 text-grey-darken-1 mb-1">Tiến độ</p>
                <v-progress-linear
                  :model-value="getCampaignProgress(campaign)"
                  :color="getProgressColor(campaign)"
                  height="8"
                  rounded
                  class="mb-1"
                />
                <div class="d-flex justify-space-between">
                  <span class="text-caption">{{ campaign.formattedStartDate }}</span>
                  <span class="text-caption">{{ campaign.formattedEndDate }}</span>
                </div>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <!-- Thông tin thời gian và người phụ trách -->
              <v-list density="compact">
                <v-list-subheader class="text-subtitle-2 text-grey-darken-1">
                  Thông tin chi tiết
                </v-list-subheader>
  
                <v-list-item prepend-icon="mdi-calendar-start">
                  <v-list-item-title>Ngày bắt đầu</v-list-item-title>
                  <v-list-item-subtitle>{{ campaign.formattedStartDate }}</v-list-item-subtitle>
                </v-list-item>
  
                <v-list-item prepend-icon="mdi-calendar-end">
                  <v-list-item-title>Ngày kết thúc</v-list-item-title>
                  <v-list-item-subtitle>{{ campaign.formattedEndDate }}</v-list-item-subtitle>
                </v-list-item>
  
                <v-list-item prepend-icon="mdi-account">
                  <v-list-item-title>Chủ sở hữu</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ campaign.owner_id || 'Chưa phân công' }}
                  </v-list-item-subtitle>
                </v-list-item>
  
                <v-list-item prepend-icon="mdi-account-circle">
                  <v-list-item-title>Người tạo</v-list-item-title>
                  <v-list-item-subtitle>{{ campaign.owner }}</v-list-item-subtitle>
                </v-list-item>
  
                <v-list-item prepend-icon="mdi-clock-outline">
                  <v-list-item-title>Ngày tạo</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(campaign.creation) }}</v-list-item-subtitle>
                </v-list-item>
  
                <v-list-item prepend-icon="mdi-update">
                  <v-list-item-title>Cập nhật lần cuối</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(campaign.modified) }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
        </v-card-text>
  
        <v-divider />
  
        <v-card-actions class="pa-6">
          <v-spacer />
          <v-btn
            variant="outlined"
            @click="dialog = false"
          >
            {{ __('Close') }}
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            @click="$emit('edit')"
          >
            {{ __('Edit') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script setup>
  import { computed } from 'vue'

  // Translation helper function
  const __ = (text) => text
  
  // Props
  const props = defineProps({
    modelValue: {
      type: Boolean,
      default: false
    },
    campaign: {
      type: Object,
      default: null
    }
  })
  
  // Emits
  const emit = defineEmits(['update:modelValue', 'edit'])
  
  // Computed
  const dialog = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
  })
  
  // Helper functions
  const getTypeIcon = (type) => {
    const icons = {
      'NURTURING': 'mdi-heart',
      'ATTRACTION': 'mdi-magnet'
    }
    return icons[type] || 'mdi-help'
  }
  
  const getStatusColor = (status) => {
    const colors = {
      'DRAFT': 'grey',
      'ACTIVE': 'success',
      'PAUSED': 'warning',
      'ARCHIVED': 'info'
    }
    return colors[status] || 'grey'
  }
  
  const getStatusText = (status) => {
    const texts = {
      'DRAFT': 'Draft',
      'ACTIVE': 'Active',
      'PAUSED': 'Paused',
      'ARCHIVED': 'Archived'
    }
    return texts[status] || status
  }
  
  const getTypeColor = (type) => {
    const colors = {
      'NURTURING': 'primary',
      'ATTRACTION': 'secondary'
    }
    return colors[type] || 'grey'
  }
  
  const getTypeText = (type) => {
    const texts = {
      'NURTURING': 'Nurturing',
      'ATTRACTION': 'Attraction'
    }
    return texts[type] || type
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
  
  const getProgressColor = (campaign) => {
    const progress = getCampaignProgress(campaign)
    if (progress === 0) return 'grey'
    if (progress < 30) return 'error'
    if (progress < 70) return 'warning'
    return 'success'
  }
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date)
  }
  </script>