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
        <v-col cols="6" class="d-flex flex-column justify-center align-center">
          <div class="position-relative donut-container">
            <!-- SVG Donut Chart -->
            <svg width="120" height="120" viewBox="0 0 120 120" class="donut-chart">
              <!-- Outer glow/shadow -->
              <defs>
                <filter id="glow">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
                <linearGradient id="openRateGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#60a5fa;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="clickRateGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
                  <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
                </linearGradient>
              </defs>
              
              <!-- Background circle -->
              <circle
                cx="60"
                cy="60"
                r="45"
                fill="transparent"
                stroke="#f3f4f6"
                stroke-width="8"
              />
              
              <!-- Open rate circle -->
              <circle
                cx="60"
                cy="60"
                r="45"
                fill="transparent"
                stroke="url(#openRateGradient)"
                stroke-width="8"
                :stroke-dasharray="circumference"
                :stroke-dashoffset="openRateOffset"
                transform="rotate(-90 60 60)"
                stroke-linecap="round"
                class="progress-circle open-rate-circle"
                filter="url(#glow)"
              />
              
              <!-- Inner background circle -->
              <circle
                cx="60"
                cy="60"
                r="30"
                fill="transparent"
                stroke="#f3f4f6"
                stroke-width="6"
              />
              
              <!-- Click rate circle -->
              <circle
                cx="60"
                cy="60"
                r="30"
                fill="transparent"
                stroke="url(#clickRateGradient)"
                stroke-width="6"
                :stroke-dasharray="innerCircumference"
                :stroke-dashoffset="clickRateOffset"
                transform="rotate(-90 60 60)"
                stroke-linecap="round"
                class="progress-circle click-rate-circle"
                filter="url(#glow)"
              />
            </svg>
            
            <!-- Center content -->
            <div class="donut-center">
              <div class="center-number" :class="getNumberSizeClass(campaign.stats.newApplicants)">
                {{ formatNumber(campaign.stats.newApplicants) }}
              </div>
            </div>
            
            <!-- Floating icons -->
            <div class="floating-icon open-icon" v-if="campaign.stats.openRate > 0">
              <v-icon size="12" color="primary">mdi-email-open</v-icon>
            </div>
            <div class="floating-icon click-icon" v-if="campaign.stats.clickRate > 0">
              <v-icon size="12" color="indigo">mdi-cursor-default-click</v-icon>
            </div>
          </div>
          
          <!-- Label below chart -->
          <div class="chart-label-simple">
           Số lượng ứng tuyển
          </div>
        </v-col>

        <!-- Stats -->
        <v-col cols="6">
          <div class="stats-container">
            <div class="stat-item mb-3">
              <div class="stat-header">
                <v-icon size="16" color="medium-emphasis" class="mr-1">mdi-account-group</v-icon>
                <span class="text-caption text-medium-emphasis">Ứng viên mục tiêu</span>
              </div>
              <div class="stat-value">{{ formatNumber(campaign.stats.candidates || campaign.stats.total || 0) }}</div>
            </div>
            
            <div class="stat-item mb-3">
              <div class="stat-header">
                <v-icon size="16" color="primary" class="mr-1">mdi-email-open</v-icon>
                <span class="text-caption text-medium-emphasis">Tỷ lệ mở</span>
              </div>
              <div class="stat-value text-primary">
                {{ campaign.stats.openRate }}%
                <v-progress-linear 
                  :model-value="campaign.stats.openRate"
                  color="primary"
                  height="4"
                  rounded
                  class="mt-1"
                  style="opacity: 0.7"
                />
              </div>
            </div>
            
            <div class="stat-item">
              <div class="stat-header">
                <v-icon size="16" color="indigo" class="mr-1">mdi-cursor-default-click</v-icon>
                <span class="text-caption text-medium-emphasis">Tỷ lệ nhấp</span>
              </div>
              <div class="stat-value text-indigo">
                {{ campaign.stats.clickRate }}%
                <v-progress-linear 
                  :model-value="campaign.stats.clickRate"
                  color="indigo"
                  height="4"
                  rounded
                  class="mt-1"
                  style="opacity: 0.7"
                />
              </div>
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
const circumference = computed(() => 2 * Math.PI * 45) // outer circle radius = 45
const innerCircumference = computed(() => 2 * Math.PI * 30) // inner circle radius = 30

const openRateOffset = computed(() => {
  const progress = props.campaign.stats.openRate / 100
  return circumference.value - (progress * circumference.value)
})

const clickRateOffset = computed(() => {
  const progress = props.campaign.stats.clickRate / 100
  return innerCircumference.value - (progress * innerCircumference.value)
})

// Helper functions
const formatNumber = (num) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const getNumberSizeClass = (num) => {
  if (num >= 1000000) {
    return 'size-mega'
  } else if (num >= 10000) {
    return 'size-large'
  } else if (num >= 1000) {
    return 'size-medium'
  }
  return 'size-small'
}

// Methods
const viewDetails = () => {
  // Navigate to campaign detail page
  console.log('View campaign details:', props.campaign.id)
}
</script>

<style scoped>
.campaign-card {
  height: 100%;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid transparent;
}

.campaign-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: rgba(99, 102, 241, 0.1);
}

.donut-container {
  position: relative;
  padding: 8px;
}

.donut-chart {
  display: block;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
}

.donut-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  pointer-events: none;
}

.center-number {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  line-height: 1;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Dynamic sizing based on number length */
.center-number.size-small {
  font-size: 2rem;
}

.center-number.size-medium {
  font-size: 1.75rem;
}

.center-number.size-large {
  font-size: 1.5rem;
}

.center-number.size-mega {
  font-size: 1.25rem;
}

.chart-label-simple {
  text-align: center;
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 8px;
}

.progress-circle {
  transition: all 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.open-rate-circle {
  animation: drawCircle 2s ease-out;
}

.click-rate-circle {
  animation: drawCircle 2s ease-out 0.5s both;
}

@keyframes drawCircle {
  from {
    stroke-dashoffset: 283; /* approximately 2 * PI * 45 */
  }
}

.floating-icon {
  position: absolute;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  animation: float 3s ease-in-out infinite;
}

.open-icon {
  top: 10px;
  right: 15px;
  animation-delay: 0s;
}

.click-icon {
  bottom: 10px;
  left: 15px;
  animation-delay: 1.5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}

.stats-container {
  padding-left: 12px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-header {
  display: flex;
  align-items: center;
  opacity: 0.8;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.2;
}

.text-primary {
  color: #3b82f6 !important;
}

.text-indigo {
  color: #6366f1 !important;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .donut-chart {
    width: 100px;
    height: 100px;
  }
  
  .center-number {
    max-width: 70px;
  }
  
  .center-number.size-small {
    font-size: 1.75rem;
  }
  
  .center-number.size-medium {
    font-size: 1.5rem;
  }
  
  .center-number.size-large {
    font-size: 1.25rem;
  }
  
  .center-number.size-mega {
    font-size: 1.1rem;
  }
  
  .chart-label-simple {
    font-size: 0.7rem;
  }
}
</style> 