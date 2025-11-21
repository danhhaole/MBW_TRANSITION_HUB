<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900">Log Hoạt động Hệ thống & Nội bộ</h2>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Loading activities...</span>
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
                      Trigger: {{ activity.trigger_type }}
                    </span>
                    <span v-if="activity.score_change" class="flex items-center">
                      <FeatherIcon name="trending-up" class="w-3 h-3 mr-1" />
                      Score: {{ activity.score_change > 0 ? '+' : '' }}{{ activity.score_change }}
                    </span>
                    <span v-if="activity.source">
                      Source: {{ activity.source }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
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

// Fetch activities when component mounts
onMounted(() => {
  fetchActivities()
})

// Watch for talent changes
watch(() => props.talent?.name, (newVal) => {
  if (newVal) {
    fetchActivities()
  }
})

const fetchActivities = async () => {
  if (!props.talent?.name) return
  
  loading.value = true
  try {
    const response = await call('mbw_mira.api.interaction.get_talent_activity_logs', {
      talent_id: props.talent.name,
      limit: 50
    })
    
    if (response && response.activities) {
      activities.value = response.activities
    }
  } catch (error) {
    console.error('Error fetching activities:', error)
  } finally {
    loading.value = false
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
