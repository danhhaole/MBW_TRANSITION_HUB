<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 campaign-card hover:shadow-md transition-all duration-300">
    <div class="flex justify-between items-start mb-6">
      <h3 class="text-lg font-bold text-gray-900">{{ campaign.name }}</h3>
      <span 
        :class="campaign.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'"
        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
      >
        {{ campaign.status === 'active' ? __('Running') : __('Completed') }}
      </span>
    </div>

    <div class="grid grid-cols-2 gap-6 mt-4">
      <!-- Donut Chart -->
      <div class="flex flex-col justify-center items-center">
        <div class="relative donut-container">
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
            <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          <div class="floating-icon click-icon" v-if="campaign.stats.clickRate > 0">
            <svg class="w-3 h-3 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path>
            </svg>
          </div>
        </div>
        
        <!-- Label below chart -->
        <div class="chart-label-simple">
         {{ __('Applications Count') }}
        </div>
      </div>

      <!-- Stats -->
      <div class="stats-container">
        <div class="stat-item mb-3">
          <div class="stat-header">
            <svg class="w-4 h-4 text-gray-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <span class="text-xs text-gray-600">{{ __('Target Candidates') }}</span>
          </div>
          <div class="stat-value text-gray-900">{{ formatNumber(campaign.stats.candidates || campaign.stats.total || 0) }}</div>
        </div>
        
        <div class="stat-item mb-3">
          <div class="stat-header">
            <svg class="w-4 h-4 text-blue-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
            <span class="text-xs text-gray-600">{{ __('Open Rate') }}</span>
          </div>
          <div class="stat-value text-blue-600">
            {{ campaign.stats.openRate }}%
            <div class="w-full bg-gray-200 rounded-full h-1 mt-1" style="opacity: 0.7">
              <div 
                class="bg-blue-600 h-1 rounded-full transition-all duration-300"
                :style="{ width: campaign.stats.openRate + '%' }"
              ></div>
            </div>
          </div>
        </div>
        
        <div class="stat-item">
          <div class="stat-header">
            <svg class="w-4 h-4 text-indigo-600 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path>
            </svg>
            <span class="text-xs text-gray-600">{{ __('Click Rate') }}</span>
          </div>
          <div class="stat-value text-indigo-600">
            {{ campaign.stats.clickRate }}%
            <div class="w-full bg-gray-200 rounded-full h-1 mt-1" style="opacity: 0.7">
              <div 
                class="bg-indigo-600 h-1 rounded-full transition-all duration-300"
                :style="{ width: campaign.stats.clickRate + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 mt-6 pt-4">
      <button 
        class="w-full text-center text-blue-600 hover:text-blue-800 font-medium text-sm transition-colors duration-200"
        @click="viewDetails"
      >
        {{ __('View Workflow Details') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Translation helper function
const __ = (text) => text

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