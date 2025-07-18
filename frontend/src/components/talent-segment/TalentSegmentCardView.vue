<template>
  <div>
    <!-- Main Content -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3 mb-8">
      <!-- Pool Card -->
      <div v-for="segment in segments" :key="segment.name"
        class="bg-white rounded-lg  overflow-hidden border border-gray-200 transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-lg cursor-pointer flex flex-col">
        <!-- Card Header -->
        <div class="px-4 py-3 text-black bg-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="font-semibold truncate">{{ segment.title }}</h3>
            <!-- <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-white bg-opacity-20 text-black">
              {{ segment.candidate_count || 0 }} candidates
            </span> -->
          </div>
        </div>

        <!-- Card Body -->
        <div class="px-4 py-3 flex-1 flex flex-col">
          <!-- Last Updated -->
          <div class="flex items-center mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 mr-2" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span class="text-sm text-gray-600">
              {{ __('Last updated: ') }}{{ formatRelativeTime(segment.modified) }}
            </span>
          </div>

          <!-- Top Skills - Always show this section -->
          <div class="mb-3">
            <div class="text-xs text-gray-500 mb-1">{{ __('Top Skills') }}</div>
            <div class="flex flex-wrap gap-1 min-h-[24px]">
              <template v-if="segment.topSkills && segment.topSkills.length">
                <span v-for="skill in segment.topSkills.slice(0, 3)" :key="skill"
                  class="inline-block bg-[#e0e7ff] text-[#4338ca] font-medium text-xs px-2 py-1 rounded-full">
                  {{ skill }}
                </span>
              </template>
              <template v-else>
                <span class="text-xs text-gray-400 italic mt-2">{{ __('No information') }}</span>
              </template>
            </div>
          </div>

          <!-- Engagement Rate -->
          <div class="mb-3">
            <div class="text-xs text-gray-500 mb-1">{{ __('Engagement Rate') }}</div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-2 mr-2">
                <div :class="getProgressBarClass(getEngagementRate(segment))"
                  class="h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${getEngagementRate(segment)}%` }"></div>
              </div>
              <span class="text-xs font-medium text-gray-700">{{ getEngagementRate(segment) }}%</span>
            </div>
          </div>

          <!-- Footer section - always at bottom -->
          <div class="mt-auto">
            <!-- Action Buttons and Recent Candidates - Same line -->
            <div class="flex items-center justify-between pt-2 border-t border-gray-100">
              <!-- Left side: Avatar Stack -->
              <div class="flex items-center">
                <div class="flex -space-x-2" v-if="segment.teamMembers && segment.teamMembers.length">
                  <div v-for="(candidate, index) in segment.teamMembers.slice(0, 3)" :key="index"
                    :class="getAvatarClass(index)"
                    class="h-7 w-7 rounded-full flex items-center justify-center text-white text-xs font-medium">
                    {{ getAvatarText(candidate.candidate_name || candidate.name) }}
                  </div>
                  <div v-if="segment.candidate_count > 3"
                    class="h-7 w-7 rounded-full bg-gray-300 flex items-center justify-center text-gray-700 text-xs font-medium">
                    +{{ segment.candidate_count - 3 }}
                  </div>
                </div>
                <div v-else class="text-xs text-gray-400 italic">
                  {{ __('No candidates yet') }}
                </div>
              </div>
              
              <!-- Right side: Action Buttons -->
              <div class="flex space-x-2">
                <Button variant="ghost" theme="gray" size="sm" @click="$emit('view-details', segment)">
                  {{ __('Manage') }}
                </Button>

                <Dropdown :options="getDropdownOptions(segment)" placement="bottom-end">
                  <Button variant="ghost" theme="gray" size="sm">
                    <template #icon>
                      <FeatherIcon name="more-horizontal" class="h-4 w-4" />
                    </template>
                  </Button>
                </Dropdown>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create New Pool Card -->
      <div
        class="bg-white rounded-lg  overflow-hidden border-2 border-dashed border-gray-300 flex items-center justify-center h-64 transition-all duration-300 hover:border-blue-500 cursor-pointer hover:bg-gray-50"
        @click="$emit('create')">
        <div class="text-center p-6">
          <div class="h-12 w-12 rounded-full bg-blue-100 flex items-center justify-center mx-auto mb-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('Create New Pool') }}</h3>
          <p class="text-sm text-gray-500">{{ __('Define a new talent segment') }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, h } from 'vue'
import { Button, Dropdown, FeatherIcon } from 'frappe-ui'
import { calculateEngagementRate, formatDate, getSegmentTypeColor } from '@/services/talentSegmentService'
import { processSkills } from '@/services/candidateService'

// Translation helper function


// Props
const props = defineProps({
  segments: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  showDebugToggle: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['view-details', 'edit', 'delete', 'create'])

// Helper functions
const getEngagementRate = (segment) => {
  return calculateEngagementRate(segment.candidate_count || 0)
}

const getProgressBarClass = (rate) => {
  if (rate >= 70) return 'bg-green-500'
  if (rate >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getAvatarClass = (index) => {
  const colors = [
    'bg-green-500',
    'bg-yellow-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-blue-500'
  ]
  return colors[index % colors.length]
}

const getAvatarText = (name) => {
  if (!name) return ''
  return name.split(' ').map(word => word[0]).join('').toUpperCase().substring(0, 2)
}

const formatRelativeTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'just now'
  if (diffInHours === 1) return '1 hour ago'
  if (diffInHours < 24) return `${diffInHours} hours ago`
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays === 1) return '1 day ago'
  if (diffInDays < 7) return `${diffInDays} days ago`
  
  return formatDate(dateString)
}

const getDropdownOptions = (segment) => {
  return [
    {
      group: __('Actions'),
      items: [
        {
          label: __('Edit'),
          icon: () => h(FeatherIcon, { name: "edit", class: "h-4 w-4" }),
          onClick: () => emit('edit', segment)
        },
        {
          label: __('View Details'),
          icon: () => h(FeatherIcon, { name: "eye", class: "h-4 w-4" }),
          onClick: () => emit('view-details', segment)
        },
      ],
    },
    {
      group: __('Danger'),
      items: [
        {
          label: __('Delete'),
          icon: () => h(FeatherIcon, { name: "trash-2", class: "h-4 w-4" }),
          onClick: () => emit('delete', segment)
        },
      ],
    },
  ]
}
</script>

<style scoped>
/* Card hover effects */
.transition-all {
  transition: all 0.3s ease;
}

/* Loading animation */
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