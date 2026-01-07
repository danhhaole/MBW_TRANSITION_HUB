<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900">{{ __('System & Internal Activity Log') }}</h2>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">{{ __('Loading activities...') }}</span>
      </div>
    </div>

    <!-- Activities List -->
    <div v-else-if="activities.length > 0" class="bg-white rounded-lg border border-gray-200">
      <div class="divide-y divide-gray-200">
        <div v-for="activity in activities" :key="activity.name" class="p-4 hover:bg-gray-50 transition-colors">
          <div class="flex items-start space-x-3">
            <!-- Icon -->
            <div class="flex-shrink-0">
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center"
                :class="getActivityIconClass(activity.activity_type)"
              >
                <FeatherIcon :name="getActivityIcon(activity.activity_type)" class="w-4 h-4" />
              </div>
            </div>
            
            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <!-- Date and Activity Type -->
                  <div class="flex items-center space-x-2 mb-1">
                    <span class="text-sm font-medium text-blue-600">
                      {{ formatDate(activity.date || activity.creation) }}
                    </span>
                    <span class="text-xs text-gray-400">•</span>
                    <span class="text-xs text-gray-500">
                      {{ activity.activity_type }}
                    </span>
                  </div>
                  
                  <!-- Subject/Description -->
                  <p class="text-sm text-gray-900" v-if="activity.subject">
                    {{ activity.subject }}
                  </p>
                  <div 
                    v-if="activity.description" 
                    class="text-sm text-gray-600 mt-1"
                    v-html="activity.description"
                  ></div>
                  
                  <!-- Additional Info -->
                  <div class="flex items-center space-x-3 mt-2 text-xs text-gray-500">
                    <span v-if="activity.trigger_type">
                      {{ __('Trigger') }}: {{ activity.trigger_type }}
                    </span>
                    <span v-if="activity.score_change" class="flex items-center">
                      <FeatherIcon name="trending-up" class="w-3 h-3 mr-1" />
                      {{ __('Score') }}: {{ activity.score_change > 0 ? '+' : '' }}{{ activity.score_change }}
                    </span>
                    <span v-if="activity.source">
                      {{ __('Source') }}: {{ activity.source }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total > pagination.limit" class="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-500">
          {{ __('Showing') }} {{ (pagination.page - 1) * pagination.limit + 1 }} - {{ Math.min(pagination.page * pagination.limit, pagination.total) }} of {{ pagination.total }}
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="prevPage"
            :disabled="pagination.page === 1"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ __('Previous') }}
          </button>
          <span class="text-sm text-gray-600">
            {{ __('Page') }} {{ pagination.page }} of {{ Math.ceil(pagination.total / pagination.limit) }}
          </span>
          <button
            @click="nextPage"
            :disabled="pagination.page * pagination.limit >= pagination.total"
            class="px-3 py-1 text-sm border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ __('Next') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white rounded-lg border border-gray-200 p-12 text-center">
      <FeatherIcon name="activity" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">No Activities Yet</h3>
      <p class="text-gray-500">Activity logs will appear here when actions are performed.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { FeatherIcon, call } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})

const activities = ref([])
const loading = ref(false)
const pagination = ref({
  page: 1,
  limit: 20,
  total: 0
})

// Fetch activities when component mounts
onMounted(() => {
  fetchActivities()
})

// Watch for talent changes
watch(() => props.talent?.name, (newVal) => {
  if (newVal) {
    pagination.value.page = 1
    fetchActivities()
  }
})

const fetchActivities = async () => {
  if (!props.talent?.name) return
  
  loading.value = true
  try {
    const result = await call('frappe.client.get_list', {
      doctype: 'Talent Activity Log',
      filters: {
        talent_id: props.talent.name
      },
      fields: ['name', 'activity_type', 'subject', 'description', 'date', 'creation', 'trigger_type', 'score_change', 'source'],
      order_by: 'creation desc',
      limit_start: (pagination.value.page - 1) * pagination.value.limit,
      limit_page_length: pagination.value.limit
    })
    
    if (result && Array.isArray(result)) {
      activities.value = result
      
      // Get total count for pagination
      const count = await call('frappe.client.get_count', {
        doctype: 'Talent Activity Log',
        filters: {
          talent_id: props.talent.name
        }
      })
      pagination.value.total = count || 0
    }
  } catch (error) {
    console.error('Error fetching activities:', error)
  } finally {
    loading.value = false
  }
}

const nextPage = () => {
  if (pagination.value.page * pagination.value.limit < pagination.value.total) {
    pagination.value.page++
    fetchActivities()
  }
}

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    fetchActivities()
  }
}

const getActivityIcon = (activityType) => {
  const icons = {
    'Created': 'user-plus',
    'Updated Status': 'edit',
    'Added to Pool': 'users',
    'Engagement Score Updated': 'trending-up',
    'Email Sent': 'mail',
    'SMS Sent': 'message-square',
    'Link Clicked': 'mouse-pointer',
    'Opened Email': 'mail-open',
    'Message Sent': 'send',
    'Note Added': 'file-text',
    'System Update': 'settings'
  }
  return icons[activityType] || 'activity'
}

const getActivityIconClass = (activityType) => {
  const classes = {
    'Created': 'bg-blue-100 text-blue-600',
    'Updated Status': 'bg-purple-100 text-purple-600',
    'Added to Pool': 'bg-green-100 text-green-600',
    'Engagement Score Updated': 'bg-yellow-100 text-yellow-600',
    'Email Sent': 'bg-indigo-100 text-indigo-600',
    'SMS Sent': 'bg-pink-100 text-pink-600',
    'Link Clicked': 'bg-orange-100 text-orange-600',
    'Opened Email': 'bg-teal-100 text-teal-600',
    'Message Sent': 'bg-cyan-100 text-cyan-600',
    'Note Added': 'bg-gray-100 text-gray-600',
    'System Update': 'bg-slate-100 text-slate-600'
  }
  return classes[activityType] || 'bg-gray-100 text-gray-600'
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return dateStr
  }
}
</script>
