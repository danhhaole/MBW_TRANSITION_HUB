<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
    <!-- Loading state -->
    <div v-if="loading" class="p-8 text-center">
      <svg class="animate-spin h-8 w-8 text-gray-500 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="text-gray-500">{{ __('Loading talent pools...') }}</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="!segments.length" class="p-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-300 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
      </svg>
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No talent pools found') }}</h3>
      <p class="text-gray-500 mb-4">{{ __('Get started by creating your first talent pool') }}</p>
      <Button variant="solid" theme="gray" @click="$emit('create')">
        <template #prefix>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
        </template>
        {{ __('Create Talent Pool') }}
      </Button>
    </div>

    <!-- Table view -->
    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __('Talent Pool') }}
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __('Type') }}
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __('Candidates') }}
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __('Status') }}
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ __('Last Updated') }}
            </th>
            <th scope="col" class="relative px-6 py-3">
              <span class="sr-only">{{ __('Actions') }}</span>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <!-- Create button row -->
          <tr v-if="hasCreateButton" class="hover:bg-gray-50">
            <td colspan="6" class="px-6 py-4">
              <div class="flex items-center justify-center">
                <Button variant="outline" theme="gray" @click="$emit('create')" class="flex items-center">
                  <template #prefix>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                    </svg>
                  </template>
                  {{ __('Create New Talent Pool') }}
                </Button>
              </div>
            </td>
          </tr>

          <!-- Segment rows -->
          <tr v-for="segment in segments" :key="segment.name" class="hover:bg-gray-50" v-show="!segment.isCreateButton">
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">
                    {{ segment.title }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ segment.description || __('No description') }}
                  </div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getBadgeClass(segment.type)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ segment.type }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ segment.candidate_count || 0 }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span :class="getStatusBadgeClass(segment.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                {{ segment.status || 'Active' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ formatLastUpdated(segment.modified) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex items-center space-x-2">
                <Button variant="ghost" theme="gray" size="sm" @click="$emit('view-details', segment)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                </Button>
                <Button variant="ghost" theme="gray" size="sm" @click="$emit('edit', segment)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </Button>
                <Button variant="ghost" theme="red" size="sm" @click="$emit('delete', segment)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </Button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Button } from 'frappe-ui'

// Props
const props = defineProps({
  segments: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['view-details', 'edit', 'delete', 'create'])

// Computed
const hasCreateButton = computed(() => {
  return props.segments.some(segment => segment.isCreateButton)
})

// Utility functions
const formatLastUpdated = (dateStr) => {
  if (!dateStr) return 'Never'
  const date = new Date(dateStr)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 1) return '1 day ago'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return `${Math.floor(diffDays / 30)} months ago`
}

const getBadgeClass = (type) => {
  const badges = {
    'DYNAMIC': 'bg-blue-100 text-blue-800',
    'MANUAL': 'bg-purple-100 text-purple-800',
    'default': 'bg-green-100 text-green-800'
  }
  return badges[type] || badges.default
}

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    'Active': 'bg-green-100 text-green-800',
    'Inactive': 'bg-gray-100 text-gray-800',
    'Draft': 'bg-yellow-100 text-yellow-800',
    'default': 'bg-gray-100 text-gray-800'
  }
  return statusClasses[status] || statusClasses.default
}

const getAvatarClass = (name) => {
  const colors = [
    'bg-green-500',
    'bg-yellow-500',
    'bg-purple-500',
    'bg-pink-500',
    'bg-blue-500'
  ]
  // Use name hash to get consistent color
  const hash = name.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const getInitials = (name) => {
  if (!name) return '??'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}
</script> 