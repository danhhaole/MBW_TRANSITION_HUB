<template>
  <v-card elevation="2" rounded="lg" class="campaign-card">
    <v-card-text class="pb-0">
      <div class="d-flex justify-space-between align-start mb-4">
        <h3 class="text-h6 font-weight-bold">{{ campaign.name }}</h3>
        <v-chip 
          :color="campaign.status === 'active' ? 'success' : 'primary'"
          size="small"
          variant="flat"
        >
          {{ campaign.status === 'active' ? 'Đang chạy' : 'Hoàn thành' }}
        </v-chip>
      </div>

      <v-row class="mt-4">
        <!-- Donut Chart -->
        <v-col cols="6" class="d-flex justify-center align-center">
          <div class="position-relative">
            <!-- SVG Donut Chart -->
            <svg width="96" height="96" viewBox="0 0 96 96" class="donut-chart">
              <!-- Background circle -->
              <circle
                cx="48"
                cy="48"
                r="40"
                fill="transparent"
                stroke="#e5e7eb"
                stroke-width="8"
              />
              <!-- Open rate circle -->
              <circle
                cx="48"
                cy="48"
                r="40"
                fill="transparent"
                stroke="#3b82f6"
                stroke-width="8"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="openRateOffset"
                transform="rotate(-90 48 48)"
                stroke-linecap="round"
                class="progress-circle"
              />
              <!-- Inner background circle -->
              <circle
                cx="48"
                cy="48"
                r="28"
                fill="transparent"
                stroke="#e5e7eb"
                stroke-width="8"
              />
              <!-- Click rate circle -->
              <circle
                cx="48"
                cy="48"
                r="28"
                fill="transparent"
                stroke="#6366f1"
                stroke-width="8"
                :stroke-dasharray="innerCircumference"
                :stroke-dashoffset="clickRateOffset"
                transform="rotate(-90 48 48)"
                stroke-linecap="round"
                class="progress-circle"
              />
            </svg>
            
            <!-- Center text -->
            <div class="donut-center">
              <div class="text-h5 font-weight-bold">{{ campaign.stats.newApplicants }}</div>
              <div class="text-caption text-medium-emphasis">ứng tuyển</div>
            </div>
          </div>
        </v-col>

        <!-- Stats -->
        <v-col cols="6">
          <div class="stats-container">
            <div class="stat-item mb-2">
              <div class="text-caption text-medium-emphasis">Ứng viên mục tiêu</div>
              <div class="text-h6 font-weight-bold">{{ campaign.stats.candidates }}</div>
            </div>
            <div class="stat-item mb-2">
              <div class="text-caption text-medium-emphasis">Tỷ lệ mở</div>
              <div class="text-subtitle-1 font-weight-bold text-blue">{{ campaign.stats.openRate }}%</div>
            </div>
            <div class="stat-item">
              <div class="text-caption text-medium-emphasis">Tỷ lệ nhấp</div>
              <div class="text-subtitle-1 font-weight-bold text-indigo">{{ campaign.stats.clickRate }}%</div>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-card-text>

    <v-divider class="mx-4"></v-divider>
    
    <v-card-actions>
      <v-btn 
        variant="text" 
        color="primary" 
        block
        @click="viewDetails"
      >
        Xem chi tiết luồng
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  campaign: {
    type: Object,
    required: true
  }
})

// Computed properties for donut chart
const circumference = computed(() => 2 * Math.PI * 40) // outer circle radius = 40
const innerCircumference = computed(() => 2 * Math.PI * 28) // inner circle radius = 28

const openRateOffset = computed(() => {
  const progress = props.campaign.stats.openRate / 100
  return circumference.value - (progress * circumference.value)
})

const clickRateOffset = computed(() => {
  const progress = props.campaign.stats.clickRate / 100
  return innerCircumference.value - (progress * innerCircumference.value)
})

// Methods
const viewDetails = () => {
  // Navigate to campaign detail page
  console.log('View campaign details:', props.campaign.id)
}
</script>

<style scoped>
.campaign-card {
  height: 100%;
  transition: transform 0.2s ease-in-out;
}

.campaign-card:hover {
  transform: translateY(-2px);
}

.donut-chart {
  display: block;
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-circle {
  transition: stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.stats-container {
  padding-left: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.text-blue {
  color: #3b82f6;
}

.text-indigo {
  color: #6366f1;
}
</style> 