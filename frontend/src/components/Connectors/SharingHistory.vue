<template>
  <div class="sharing-history-dialog">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center">
        <component 
          :is="getPlatformIcon(connection.platform_type)" 
          class="w-6 h-6 mr-3"
          :class="getPlatformColor(connection.platform_type)"
        />
        <div>
          <h4 class="font-medium text-gray-900">{{ connection.platform_name }}</h4>
          <p class="text-sm text-gray-600">{{ connection.account_name }}</p>
        </div>
      </div>
      
      <Button
        variant="ghost"
        size="sm"
        @click="refreshHistory"
        :loading="loading"
      >
        <template #prefix>
          <FeatherIcon name="refresh-cw" class="w-4 h-4" />
        </template>
        {{__('Refresh')}}
      </Button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="animate-pulse">
        <div class="h-24 bg-gray-100 rounded-lg"></div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="!history.length" class="text-center py-12">
      <FeatherIcon name="clock" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{__('No sharing history')}}</h3>
      <p class="text-gray-600 mb-4">{{__('This job hasn\'t been shared to')}} {{ connection.platform_name }} {{__('yet.')}}</p>
      <Button
        variant="solid"
        @click="$emit('share-now')"
      >
        {{__('Share Job Now')}}
      </Button>
    </div>

    <!-- History list -->
    <div v-else class="space-y-4">
      <!-- Filters -->
      <div class="flex items-center space-x-4 pb-4 border-b">
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">{{__('Status:')}}</label>
          <select
            v-model="filterStatus"
            class="text-sm border border-gray-300 rounded px-2 py-1 focus:ring-2 focus:ring-blue-500"
          >
            <option value="">{{__('All')}}</option>
            <option value="success">{{__('Success')}}</option>
            <option value="pending">{{__('Pending')}}</option>
            <option value="failed">{{__('Failed')}}</option>
          </select>
        </div>
        
        <div class="flex items-center space-x-2">
          <label class="text-sm font-medium text-gray-700">{{__('Time:')}}</label>
          <select
            v-model="filterTime"
            class="text-sm border border-gray-300 rounded px-2 py-1 focus:ring-2 focus:ring-blue-500"
          >
            <option value="">{{__('All time')}}</option>
            <option value="today">{{__('Today')}}</option>
            <option value="week">{{__('This week')}}</option>
            <option value="month">{{__('This month')}}</option>
          </select>
        </div>
      </div>

      <!-- History items -->
      <div class="max-h-96 overflow-y-auto space-y-3">
        <div
          v-for="item in filteredHistory"
          :key="item.id"
          class="border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center space-x-2">
              <Badge 
                :variant="getStatusVariant(item.status)"
                size="sm"
              >
                {{ __(getStatusLabel(item.status)) }}
              </Badge>
              <span class="text-sm text-gray-600">
                {{ formatDateTime(item.shared_at) }}
              </span>
            </div>
            
            <Dropdown :options="getItemActions(item)" v-if="item.status === 'success'">
              <template #default="{ open }">
                <Button
                  variant="ghost"
                  size="sm"
                  @click="open"
                >
                  <FeatherIcon name="more-vertical" class="w-4 h-4" />
                </Button>
              </template>
            </Dropdown>
          </div>

          <!-- Share details -->
          <div class="space-y-2">
            <div class="text-sm">
              <span class="font-medium text-gray-700">{{__('Message:')}}</span>
              <p class="text-gray-900 mt-1 line-clamp-3">{{ item.message }}</p>
            </div>

            <!-- Platform specific details -->
            <div class="text-xs text-gray-600 space-y-1">
              <div v-if="item.target_page_name" class="flex items-center">
                <FeatherIcon name="users" class="w-3 h-3 mr-1" />
                {{__('Shared to:')}} {{ item.target_page_name }}
              </div>
              
              <div v-if="item.scheduled_time && item.status === 'pending'" class="flex items-center">
                <FeatherIcon name="clock" class="w-3 h-3 mr-1" />
                {{__('Scheduled for:')}} {{ formatDateTime(item.scheduled_time) }}
              </div>
              
              <div v-if="item.external_post_id" class="flex items-center">
                <FeatherIcon name="hash" class="w-3 h-3 mr-1" />
                {{__('Post ID:')}} {{ item.external_post_id }}
              </div>
            </div>

            <!-- Engagement metrics (if available) -->
            <div v-if="item.engagement" class="flex items-center space-x-4 text-xs text-gray-600 pt-2 border-t">
              <div v-if="item.engagement.likes" class="flex items-center">
                <FeatherIcon name="heart" class="w-3 h-3 mr-1" />
                {{ item.engagement.likes }} {{__('likes')}}
              </div>
              <div v-if="item.engagement.shares" class="flex items-center">
                <FeatherIcon name="share" class="w-3 h-3 mr-1" />
                {{ item.engagement.shares }} {{__('shares')}}
              </div>
              <div v-if="item.engagement.comments" class="flex items-center">
                <FeatherIcon name="message-circle" class="w-3 h-3 mr-1" />
                {{ item.engagement.comments }} {{__('comments')}}
              </div>
              <div v-if="item.engagement.clicks" class="flex items-center">
                <FeatherIcon name="mouse-pointer" class="w-3 h-3 mr-1" />
                {{ item.engagement.clicks }} {{__('clicks')}}
              </div>
            </div>

            <!-- Error details (if failed) -->
            <div v-if="item.status === 'failed' && item.error_message" class="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs">
              <div class="flex items-start">
                <FeatherIcon name="alert-circle" class="w-3 h-3 text-red-500 mr-1 mt-0.5 flex-shrink-0" />
                <span class="text-red-700">{{ item.error_message }}</span>
              </div>
              <div v-if="item.retry_count > 0" class="mt-1 text-red-600">
                {{__('Retried')}} {{ item.retry_count }} {{__('times')}}
              </div>
            </div>
          </div>

          <!-- Action buttons for failed items -->
          <div v-if="item.status === 'failed'" class="flex space-x-2 mt-3 pt-3 border-t">
            <Button
              size="sm"
              variant="outline"
              @click="retryShare(item)"
              :loading="retrying[item.id]"
            >
              <template #prefix>
                <FeatherIcon name="refresh-cw" class="w-3 h-3" />
              </template>
              {{__('Retry')}}
            </Button>
            
            <Button
              size="sm"
              variant="ghost"
              @click="editAndRetry(item)"
            >
              <template #prefix>
                <FeatherIcon name="edit" class="w-3 h-3" />
              </template>
              {{__('Edit & Retry')}}
            </Button>
          </div>

          <!-- Action buttons for pending scheduled items -->
          <div v-if="item.status === 'pending' && item.scheduled_time" class="flex space-x-2 mt-3 pt-3 border-t">
            <Button
              size="sm"
              variant="outline"
              @click="cancelScheduled(item)"
              :loading="canceling[item.id]"
            >
              <template #prefix>
                <FeatherIcon name="x" class="w-3 h-3" />
              </template>
              {{__('Cancel')}}
            </Button>
            
            <Button
              size="sm"
              variant="ghost"
              @click="editScheduled(item)"
            >
              <template #prefix>
                <FeatherIcon name="edit" class="w-3 h-3" />
              </template>
              {{__('Edit Schedule')}}
            </Button>
          </div>
        </div>
      </div>

      <!-- Summary stmira -->
      <div class="pt-4 border-t bg-gray-50 rounded-lg p-3 mt-6">
        <h5 class="font-medium text-gray-900 mb-2">{{__('Summary')}}</h5>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center text-sm">
          <div>
            <div class="font-semibold text-lg text-green-600">{{ successCount }}</div>
            <div class="text-gray-600">{{__('Successful')}}</div>
          </div>
          <div>
            <div class="font-semibold text-lg text-yellow-600">{{ pendingCount }}</div>
            <div class="text-gray-600">{{__('Pending')}}</div>
          </div>
          <div>
            <div class="font-semibold text-lg text-red-600">{{ failedCount }}</div>
            <div class="text-gray-600">{{__('Failed')}}</div>
          </div>
          <div>
            <div class="font-semibold text-lg text-blue-600">{{ totalEngagement }}</div>
            <div class="text-gray-600">{{__('Total Engagement')}}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="flex justify-end space-x-3 pt-6 border-t">
      <Button
        variant="ghost"
        @click="$emit('close')"
      >
        {{__('Close')}}
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, onMounted } from 'vue'
import { Button, Badge, Dropdown, FeatherIcon, call } from 'frappe-ui'
import useToast from '@/composables/useToast'

// Props
const props = defineProps({
  connection: {
    type: Object,
    required: true
  },
  jobId: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['close', 'share-now', 'retry-share', 'edit-share'])

// Reactive data
const loading = ref(true)
const history = ref([])
const filterStatus = ref('')
const filterTime = ref('')
const retrying = ref({})
const canceling = ref({})
const { success: toastSuccess, error: toastError } = useToast()

// Computed
const filteredHistory = computed(() => {
  let filtered = history.value

  // Filter by status
  if (filterStatus.value) {
    filtered = filtered.filter(item => item.status === filterStatus.value)
  }

  // Filter by time
  if (filterTime.value) {
    const now = new Date()
    const cutoff = new Date()
    
    switch (filterTime.value) {
      case 'today':
        cutoff.setHours(0, 0, 0, 0)
        break
      case 'week':
        cutoff.setDate(now.getDate() - 7)
        break
      case 'month':
        cutoff.setMonth(now.getMonth() - 1)
        break
    }
    
    filtered = filtered.filter(item => new Date(item.shared_at) >= cutoff)
  }

  return filtered.sort((a, b) => new Date(b.shared_at) - new Date(a.shared_at))
})

const successCount = computed(() => 
  history.value.filter(item => item.status === 'success').length
)

const pendingCount = computed(() => 
  history.value.filter(item => item.status === 'pending').length
)

const failedCount = computed(() => 
  history.value.filter(item => item.status === 'failed').length
)

const totalEngagement = computed(() => {
  return history.value.reduce((total, item) => {
    if (!item.engagement) return total
    return total + (item.engagement.likes || 0) + 
                  (item.engagement.shares || 0) + 
                  (item.engagement.comments || 0) + 
                  (item.engagement.clicks || 0)
  }, 0)
})

// Methods
const refreshHistory = async () => {
  try {
    loading.value = true
    const response = await call('mbw_mira.api.external_connections.get_job_sharing_history', {
      connection_id: props.connection.name,
      job_id: props.jobId
    })
    
    history.value = response || []
  } catch (error) {
    console.error('Error loading history:', error)
    toastError(`${__('Error')}: ${__('Failed to load sharing history')}`)
  } finally {
    loading.value = false
  }
}

const getPlatformIcon = (platformType) => {
  return 'FeatherIcon' // You can customize based on platform
}

const getPlatformColor = (platformType) => {
  const colors = {
    facebook: 'text-blue-600',
    zalooa: 'text-blue-500',
    cal_com: 'text-gray-600',
    topcv: 'text-orange-600'
  }
  return colors[platformType] || 'text-gray-600'
}

const getStatusVariant = (status) => {
  const variants = {
    success: 'solid',
    pending: 'outline',
    failed: 'subtle'
  }
  return variants[status] || 'subtle'
}

const getStatusLabel = (status) => {
  const labels = {
    success: __('Success'),
    pending: __('Pending'),
    failed: __('Failed')
  }
  return labels[status] || status
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const getItemActions = (item) => {
  const actions = []
  
  if (item.external_url) {
    actions.push({
      label: __('View Post'),
      icon: 'external-link',
      onClick: () => window.open(item.external_url, '_blank')
    })
  }
  
  if (item.status === 'success') {
    actions.push({
      label: __('Share Again'),
      icon: 'share',
      onClick: () => shareAgain(item)
    })
  }
  
  return actions
}

const retryShare = async (item) => {
  try {
    retrying.value[item.id] = true
    
    await call('mbw_mira.api.external_connections.retry_share', {
      share_id: item.id
    })
    
    toastSuccess(`${__('Success')}: ${__('Share retry initiated')}`)
    
    await refreshHistory()
  } catch (error) {
    console.error('Error retrying share:', error)
    toastError(`${__('Error')}: ${__('Failed to retry share')}`)
  } finally {
    retrying.value[item.id] = false
  }
}

const editAndRetry = (item) => {
  emit('edit-share', item)
}

const shareAgain = (item) => {
  emit('retry-share', item)
}

const cancelScheduled = async (item) => {
  try {
    canceling.value[item.id] = true
    
    await call('mbw_mira.api.external_connections.cancel_scheduled_share', {
      share_id: item.id
    })
    
    toastSuccess(`${__('Success')}: ${__('Scheduled share cancelled')}`)
    
    await refreshHistory()
  } catch (error) {
    console.error('Error cancelling share:', error)
    toastError(`${__('Error')}: ${__('Failed to cancel share')}`)
  } finally {
    canceling.value[item.id] = false
  }
}

const editScheduled = (item) => {
  emit('edit-share', item)
}

// Lifecycle
onMounted(() => {
  refreshHistory()
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style>