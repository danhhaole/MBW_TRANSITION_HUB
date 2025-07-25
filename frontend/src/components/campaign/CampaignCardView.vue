<template>
  <div class="p-6">
    <!-- No campaigns message -->
    <div v-if="!loading && campaigns?.length === 0" class="text-center py-12">
      <div class="mx-auto flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full mb-4">
        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No campaigns to display') }}</h3>
      <p class="text-gray-500">{{ __('Create your first campaign') }}</p>
    </div>
    
    <div v-if="!loading && campaigns?.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <!-- Campaign Cards -->
      <div
        v-for="campaign in campaigns"
        :key="campaign.name"
        class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden campaign-card group hover:shadow-md transition-all duration-300"
      >
        <!-- Card Header -->
        <div 
          class="px-4 py-3 flex justify-between items-center"
          :class="getHeaderClass(campaign.status)"
        >
          <span class="text-sm font-medium" :class="getHeaderTextClass(campaign.status)">
            {{ campaign.type === 'NURTURING' ? __('Nurturing') : __('Attraction') }}
          </span>
          <span
            :class="getStatusChipClass(campaign.status)"
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
          >
            {{ getStatusText(campaign.displayStatus || campaign.status) }}
          </span>
        </div>

        <!-- Card Content -->
        <div class="p-4">
          <h3 class="text-lg font-semibold text-gray-900 mb-2 truncate">
            {{ campaign.campaign_name }}
          </h3>
          <p class="text-sm text-gray-600 mb-4 line-clamp-2 truncate">
            {{ campaign.description || __('Recruiting for important positions in the company.') }}
          </p>

          <!-- Progress section -->
          <div class="mb-4">
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs text-gray-500">{{ __('Progress') }}</span>
              <span class="text-xs font-medium" :class="getProgressTextClass(campaign)">
                {{ campaign.total > 0 ? __('Step') : 'Steps' }} {{ campaign.current || 0 }}/{{ campaign.total || 0 }}
              </span>
            </div>
            <!-- Progress bar -->
            <div class="progress-container mb-4">
              <div 
                class="progress-bar transition-all duration-300 ease-out"
                :style="{ width: getCampaignPercent(campaign) + '%' }"
                :class="getProgressBarClass(campaign)"
              ></div>
            </div>
          </div>
        </div>

        <!-- Card Footer -->
        <div class="border-t border-gray-100 bg-gray-50 px-4 py-3 flex justify-between items-center">
          <button
            @click="$emit('view', campaign)"
            class="inline-flex items-center text-xs text-gray-600 hover:text-gray-900 transition-colors duration-200"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            </svg>
            {{ __('Details') }}
          </button>
          
          <button
            @click="$emit('view', campaign)"
            class="text-xs font-medium text-blue-600 hover:text-blue-800 transition-colors duration-200"
          >
            {{ __('View timeline') }} →
          </button>
        </div>
      </div>

      <!-- Add new card -->
      <div 
        class="bg-white rounded-lg border-2 border-dashed border-gray-300 hover:border-blue-400 cursor-pointer transition-all duration-300 flex items-center justify-center h-full create-card group"
        @click="$emit('create')"
      >
        <div class="text-center p-8">
          <div class="mx-auto mb-4 flex items-center justify-center w-12 h-12 rounded-full bg-blue-100 group-hover:bg-blue-200 transition-colors duration-300">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">
            {{ __('Create New Request') }}
          </h3>
          <p class="text-sm text-gray-600">
            {{ __('Start a new recruitment request') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div
        v-for="n in 8"
        :key="n"
        class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden"
      >
        <!-- Header skeleton -->
        <div class="h-12 bg-gray-100 animate-pulse"></div>
        <!-- Content skeleton -->
        <div class="p-4 space-y-3">
          <div class="h-6 bg-gray-200 rounded animate-pulse"></div>
          <div class="h-4 bg-gray-200 rounded animate-pulse"></div>
          <div class="h-4 bg-gray-200 rounded w-3/4 animate-pulse"></div>
          <div class="space-y-2">
            <div class="h-3 bg-gray-200 rounded animate-pulse"></div>
            <div class="h-2 bg-gray-200 rounded animate-pulse"></div>
          </div>
          <div class="flex justify-between items-center">
            <div class="h-4 bg-gray-200 rounded w-20 animate-pulse"></div>
            <div class="flex -space-x-1">
              <div class="w-6 h-6 bg-gray-200 rounded-full animate-pulse"></div>
              <div class="w-6 h-6 bg-gray-200 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
        <!-- Footer skeleton -->
        <div class="h-12 bg-gray-50 border-t border-gray-100 flex items-center justify-between px-4">
          <div class="h-4 bg-gray-200 rounded w-16 animate-pulse"></div>
          <div class="h-4 bg-gray-200 rounded w-20 animate-pulse"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Translation helper function


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
    'DRAFT': 'bg-gray-100',
    'ACTIVE': 'bg-blue-50',
    'PAUSED': 'bg-yellow-50',
    'ARCHIVED': 'bg-gray-100'
  }
  return classes[status] || 'bg-gray-100'
}

const getHeaderTextClass = (status) => {
  const classes = {
    'DRAFT': 'text-gray-600',
    'ACTIVE': 'text-blue-700',
    'PAUSED': 'text-yellow-700',
    'ARCHIVED': 'text-gray-600'
  }
  return classes[status] || 'text-gray-600'
}

const getStatusChipClass = (status) => {
  const classes = {
    'DRAFT': 'bg-gray-100 text-gray-800',
    'ACTIVE': 'bg-blue-100 text-blue-800',
    'PAUSED': 'bg-yellow-100 text-yellow-800',
    'ARCHIVED': 'bg-green-100 text-green-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getStatusText = (status) => {
  const texts = {
    'DRAFT': __('Draft'),
    'ACTIVE': __('In Progress'),
    'PAUSED': __('Paused'),
    'ARCHIVED': __('Completed')
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
  return `${currentStep}/${totalSteps} ${__('steps')}`
}

const getProgressBarClass = (campaign) => {
  const progress = getCampaignProgress(campaign)
  if (progress === 0) return 'bg-gray-300'
  if (progress < 30) return 'bg-blue-500'
  if (progress < 70) return 'bg-yellow-500'
  return 'bg-green-500'
}

const getProgressTextClass = (campaign) => {
  const progress = getCampaignProgress(campaign)
  if (progress === 0) return 'text-gray-500'
  if (progress < 30) return 'text-blue-600'
  if (progress < 70) return 'text-yellow-600'
  return 'text-green-600'
}

const getInitials = (name) => {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
}

const getOwnerColor = (owner) => {
  const colors = ['bg-blue-400', 'bg-purple-400', 'bg-green-400', 'bg-orange-400', 'bg-red-400', 'bg-indigo-400']
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

function getCampaignPercent(campaign) {
  if (!campaign.total || campaign.total === 0) return 0
  return Math.round(((campaign.current || 0) / campaign.total) * 100)
}
</script>

<style scoped>
.campaign-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.campaign-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.create-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.create-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.progress-container {
  height: 6px;
  background-color: #e5e7eb;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style> 