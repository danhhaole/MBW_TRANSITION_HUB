<template>
  <div class="job-external-sharing">
    <!-- Header Section -->
    <div class="header-section">
      <div class="flex items-center justify-between">
        <div class="header-content">
          <h3 class="header-title">{{__('Share Job Posting')}}</h3>
          <p class="header-subtitle">{{__('Share your job across connected platforms')}}</p>
        </div>
        <Button 
          variant="outline" 
          size="sm" 
          @click="refreshConnections" 
          :loading="loading"
          class="refresh-button"
        >
          <template #prefix>
            <FeatherIcon name="refresh-cw" class="w-4 h-4" />
          </template>
          {{__('Refresh')}}
        </Button>
      </div>
    </div>

    <!-- Job Info Card -->
    <div class="job-info-card">
      <div class="flex items-start gap-3">
        <div class="job-icon">
          <FeatherIcon name="briefcase" class="w-5 h-5 text-blue-600" />
        </div>
        <div class="flex-1">
          <h4 class="job-title">{{ jobTitle }}</h4>
          <p class="job-description">{{ jobDescription ? truncateText(jobDescription, 120) : __('No description provided') }}</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-section">
      <div class="loading-header">
        <div class="loading-skeleton loading-title"></div>
        <div class="loading-skeleton loading-subtitle"></div>
      </div>
      <div class="loading-grid">
        <div v-for="i in 3" :key="`loading-${i}`" class="loading-card">
          <div class="loading-skeleton loading-card-header"></div>
          <div class="loading-skeleton loading-card-content"></div>
          <div class="loading-skeleton loading-card-button"></div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-section">
      <div class="error-icon">
        <FeatherIcon name="alert-circle" class="w-12 h-12 text-red-500" />
      </div>
      <h4 class="error-title">{{__('Connection Failed')}}</h4>
      <p class="error-message">{{ error }}</p>
      <Button @click="refreshConnections" variant="outline" class="error-retry">
        <template #prefix>
          <FeatherIcon name="refresh-cw" class="w-4 h-4" />
        </template>
        {{__('Try Again')}}
      </Button>
    </div>

    <!-- Connected Platforms -->
    <div v-else class="platforms-section">
      <!-- No Connected Platforms State -->
      <div v-if="connectedPlatforms.length === 0" class="empty-state">
        <FeatherIcon name="wifi-off" class="w-12 h-12 text-gray-400 mb-4 mx-auto" />
        <h4 class="empty-title">{{__('No Connected Platforms')}}</h4>
        <p class="empty-message">{{__('You need to connect to at least one platform before you can share job postings. Please go to Settings to set up your connections.')}}</p>
        <Button 
          variant="solid" 
          @click="goToSettings"
          class="mt-4"
        >
          <template #prefix>
            <FeatherIcon name="settings" class="w-4 h-4" />
          </template>
          {{__('Go to Settings')}}
        </Button>
      </div>

      <!-- Connected Platforms Grid -->
      <div v-else class="connected-platforms">
        <div class="section-header">
          <h4 class="section-title">{{__('Connected Platforms')}}</h4>
          <span class="platform-count">{{ connectedPlatforms.length }} {{ connectedPlatforms.length !== 1 ? __('platforms') : __('platform') }}</span>
        </div>

        <div class="platforms-grid">
          <div 
            v-for="connection in connectedPlatforms" 
            :key="`platform-${connection.connection_id}`"
            class="platform-card platform-connected"
          >
            <!-- Platform Header -->
            <div class="platform-header">
              <div class="platform-icon-wrapper">
                <FeatherIcon 
                  :name="getPlatformIconName(connection.platform_type)" 
                  class="platform-icon" 
                  :class="getPlatformIconColor(connection.platform_type)" 
                />
              </div>
              <div class="platform-info">
                <h5 class="platform-name">{{ connection.platform_name || connection.platform_type }}</h5>
                <Badge 
                  variant="solid" 
                  theme="green" 
                  size="sm"
                  class="platform-status"
                >
                  {{__('Connected')}}
                </Badge>
              </div>
            </div>

            <!-- Connection Details -->
            <div class="connection-details">
              <div v-if="connection.account_name" class="connection-info">
                <FeatherIcon name="user" class="w-4 h-4 text-gray-400" />
                <span class="connection-text">{{ connection.account_name }}</span>
              </div>
              <div v-if="connection.last_sync" class="connection-info">
                <FeatherIcon name="clock" class="w-4 h-4 text-gray-400" />
                <span class="connection-text">{{__('Last sync')}} {{ formatRelativeTime(connection.last_sync) }}</span>
              </div>
            </div>

            <!-- Last Shared Info -->
            <div v-if="getLastShared(connection.platform_type)" class="last-shared-info">
              <div class="shared-header">
                <FeatherIcon name="share-2" class="w-4 h-4 text-gray-400" />
                <span class="shared-label">{{__('Last posted')}} {{ formatRelativeTime(getLastShared(connection.platform_type).shared_at || getLastShared(connection.platform_type).modified) }}</span>
              </div>
              <div v-if="getLastShared(connection.platform_type).status" class="share-status">
                <Badge 
                  variant="outline" :theme="getShareStatusVariant(getLastShared(connection.platform_type).status)"
                  size="sm"
                >
                  {{ getLastShared(connection.platform_type).status }}
                </Badge>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="platform-actions">
              <Button 
                size="sm" 
                variant="solid" 
                theme="blue"
                @click="shareJob(connection)" 
                :loading="posting[connection.platform_type]"
                class="share-button"
              >
                <template #prefix>
                  <FeatherIcon name="share-2" class="w-4 h-4" />
                </template>
                {{ getLastShared(connection.platform_type) ? __('Post Again') : __('Post Job') }}
              </Button>

              <div class="secondary-actions">
                <Button 
                  size="sm" 
                  variant="ghost" 
                  @click="viewSharedPost(connection.platform_type)"
                  v-if="getLastShared(connection.platform_type)?.external_url"
                  class="action-button"
                  :title="__('View Posted Job')"
                >
                  <FeatherIcon name="external-link" class="w-4 h-4" />
                </Button>

                <Button 
                  size="sm" 
                  variant="ghost" 
                  @click="viewSharingHistory(connection)"
                  class="action-button"
                  :title="__('View History')"
                >
                  <FeatherIcon name="clock" class="w-4 h-4" />
                </Button>

                <Dropdown :options="getConnectionActions(connection)">
                  <template #default="{ open }">
                    <Button size="sm" variant="ghost" @click="open" class="action-button">
                      <FeatherIcon name="more-vertical" class="w-4 h-4" />
                    </Button>
                  </template>
                </Dropdown>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Share Dialog -->
    <Dialog v-model="showShareDialog" :options="{
      title: `${__('Post to')} ${selectedConnection?.platform_name || selectedConnection?.platform_type}`,
      size: '5xl'
    }">
      <template #body-content>
        <ShareConfigDialog 
          v-if="selectedConnection" 
          :connection="selectedConnection" 
          :job="jobData"
          :jobUrl="getJobUrl()"
          :jobImageUrl="getJobImageUrl()"
          :is-submitting="submittingShare || (posting[selectedConnection.platform_type] || false)"
          @submit="submitShare"
          @cancel="showShareDialog = false"
        />
      </template>
    </Dialog>

    <!-- History Dialog -->
    <Dialog v-model="showHistoryDialog" :options="{
      title: __('Posting History'),
      size: '3xl'
    }">
      <template #body-content>
        <SharingHistoryDialog 
          v-if="selectedConnection" 
          :connection="selectedConnection" 
          :job-id="jobId" 
        />
      </template>
      <template #actions>
        <Button @click="showHistoryDialog = false" variant="ghost">
          {{__('Close')}}
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, defineProps, defineEmits } from 'vue'
import {
  Button,
  Badge,
  Dialog,
  Dropdown,
  FeatherIcon,
  call
} from 'frappe-ui'
import useToast from '@/composables/useToast'

// Import components
import ShareConfigDialog from './ShareConfiguration.vue'
import SharingHistoryDialog from './SharingHistory.vue'
import { useRouter, useRoute } from "vue-router";
const route = useRoute();
const router = useRouter();
const { success: toastSuccess, error: toastError } = useToast()

// Props
const props = defineProps({
  jobId: {
    type: String,
    required: true
  },
  jobTitle: {
    type: String,
    required: true
  },
  jobDescription: {
    type: String,
    default: ''
  },
  job: {
    type: Object,
    default: () => ({})
  },
  tenantName: {
    type: String,
    required: true
  },
  userEmail: {
    type: String,
    required: true
  }
})

// Emits
const emit = defineEmits(['connection-updated', 'job-shared'])

// Reactive data
const loading = ref(true)
const error = ref(null)
const connections = ref([])
const sharingHistory = ref({})
const posting = ref({})

// Dialog states
const showShareDialog = ref(false)
const showHistoryDialog = ref(false)
const selectedConnection = ref(null)

// Form data
const submittingShare = ref(false)

// Computed - Only show connected platforms
const connectedPlatforms = computed(() => {
  return connections.value.filter(conn => 
    conn.connection_status === 'Connected'
  )
})

// Computed
const jobData = computed(() => ({
  id: props.jobId,
  title: props.jobTitle,
  description: props.jobDescription,
  job: props.job,
  name: props.jobId,
  slug: props.job.job_url_cms
}))

// Helper methods
const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const getPlatformIconName = (platformId) => {
  const iconMap = {
    facebook: 'facebook',
    zalo: 'message-square',
    cal_com: 'calendar',
    topcv: 'briefcase',
    linkedin: 'linkedin',
    twitter: 'twitter'
  }
  return iconMap[platformId.toLowerCase()] || 'globe'
}

const getPlatformIconColor = (platformId) => {
  const colorMap = {
    facebook: 'text-blue-600',
    zalo: 'text-blue-500',
    cal_com: 'text-orange-600',
    topcv: 'text-purple-600',
    linkedin: 'text-blue-700',
    twitter: 'text-blue-400'
  }
  return colorMap[platformId.toLowerCase()] || 'text-gray-600'
}

const formatRelativeTime = (dateString) => {
  if (!dateString) return __('unknown')
  
  const date = new Date(dateString)
  const now = new Date()
  const diffInSeconds = Math.floor((now - date) / 1000)
  
  if (diffInSeconds < 60) return __('just now')
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}${__('m ago')}`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}${__('h ago')}`
  return `${Math.floor(diffInSeconds / 86400)}${__('d ago')}`
}

const getShareStatusVariant = (status) => {
  
  switch (status?.toLowerCase()) {
    case 'published':
    case 'success':
      return 'success'
    case 'pending':
      return 'warning'
    case 'failed':
    case 'error':
      return 'red'
    default:
      return 'subtle'
  }
}

// Helper methods for job URLs and images
const getJobUrl = () => {
  return `${window.location.origin}/jobs/${props.job.job_url_cms}`
}

const getJobImageUrl = () => {
  return `${window.location.origin}/assets/images/job-default.jpg`
}

// Methods
const refreshConnections = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await call('mbw_mira.api.external_connections.get_connection_info', {
      tenant_name: props.tenantName,
      user_email: props.userEmail
    })

    if (response.status === 'success' && Array.isArray(response.data)) {
      connections.value = response.data
    } else if (Array.isArray(response)) {
      connections.value = response
    } else {
      connections.value = []
    }

    await loadSharingHistory()
    
  } catch (err) {
    console.error('Error loading connections:', err)
    error.value = `Failed to load connections: ${err.message || 'Unknown error'}`
    connections.value = []
  } finally {
    loading.value = false
  }
}

const loadSharingHistory = async () => {
  try {
    const response = await call('mbw_mira.api.external_connections.get_job_sharing_history', {
      job_id: props.jobId
    })

    sharingHistory.value = {}
    
    let historyData = []
    if (response && typeof response === 'object') {
      if (response.status === 'success' && Array.isArray(response.data)) {
        historyData = response.data
      } else if (Array.isArray(response)) {
        historyData = response
      }
    }

    if (historyData.length > 0) {
      const historyByPlatform = {}
      historyData.forEach(item => {
        if (item.platform_type) {
          if (!historyByPlatform[item.platform_type]) {
            historyByPlatform[item.platform_type] = { latest: null, all: [] }
          }
          historyByPlatform[item.platform_type].all.push(item)

          const currentDate = new Date(item.shared_at || item.created)
          const latestDate = historyByPlatform[item.platform_type].latest ? 
            new Date(historyByPlatform[item.platform_type].latest.shared_at || 
                    historyByPlatform[item.platform_type].latest.created) : null

          if (!latestDate || currentDate > latestDate) {
            historyByPlatform[item.platform_type].latest = item
          }
        }
      })
      sharingHistory.value = historyByPlatform
    }
  } catch (err) {
    console.warn('Error loading sharing history:', err)
    sharingHistory.value = {}
  }
}

const getLastShared = (platformId) => {
  return sharingHistory.value[platformId]?.latest || null
}

const getConnectionActions = (connection) => {
  return [
    {
      label: __('View History'),
      icon: 'clock',
      onClick: () => viewSharingHistory(connection)
    },
    {
      label: __('Connection Settings'),
      icon: 'settings',
      onClick: () => goToConnectionSettings(connection)
    }
  ]
}

const shareJob = async (connection) => {
  selectedConnection.value = connection
  showShareDialog.value = true
}

const viewSharedPost = (platformId) => {
  const lastShared = getLastShared(platformId)
  if (lastShared?.external_url) {
    window.open(lastShared.external_url, '_blank')
  }
}

const viewSharingHistory = (connection) => {
  selectedConnection.value = connection
  showHistoryDialog.value = true
}

const goToSettings = () => {
  // Navigate to settings page or emit event
  router.push({
												name: 'Connectors'
											});
}

const goToConnectionSettings = (connection) => {
  // Navigate to specific connection settings
  router.push({
												name: 'Connectors'
											});
}

const submitShare = async (shareData) => {
  if (!selectedConnection.value) return

  try {
    submittingShare.value = true
    posting.value[selectedConnection.value.platform_type] = true

    const response = await call('mbw_mira.api.external_connections.share_job_posting', {
      connection_id: selectedConnection.value.connection_id,
      job_id: props.jobId,
      ...shareData
    })
    
    if (response.status === "success") {
      toastSuccess(`${__('Success')}: ${__('Job posted to')} ${selectedConnection.value.platform_name}`)

      showShareDialog.value = false
      await loadSharingHistory()
      emit('job-shared', {
        platform: selectedConnection.value.platform_type,
        jobId: props.jobId
      })
    } else if (response.status === "error") {
      toastError(`${__('Posting Failed')}: ${response.message || __('Failed to post job')}`)
    }
  } catch (error) {
    console.error('Error sharing job:', error)
    toastError(`${__('Network Error')}: ${error.message || __('Failed to connect to server')}`)
  } finally {
    submittingShare.value = false
    if (selectedConnection.value) {
      posting.value[selectedConnection.value.platform_type] = false
    }
  }
}

// Lifecycle
onMounted(() => {
  refreshConnections()
})
</script>

<style scoped>
.job-external-sharing {
  @apply max-w-6xl mx-auto p-6 space-y-6;
}

/* Header Section */
.header-section {
  @apply bg-gradient-to-r from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-100;
}

.header-content {
  @apply flex-1;
}

.header-title {
  @apply text-2xl font-bold text-gray-900 mb-1;
}

.header-subtitle {
  @apply text-gray-600 text-sm;
}

.refresh-button {
  @apply transition-all duration-200 hover:scale-105;
}

/* Job Info Card */
.job-info-card {
  @apply bg-white rounded-xl p-6 border border-gray-200 shadow-sm;
}

.job-icon {
  @apply w-12 h-12 rounded-lg bg-blue-50 flex items-center justify-center flex-shrink-0;
}

.job-title {
  @apply font-semibold text-gray-900 text-lg mb-2;
}

.job-description {
  @apply text-gray-600 text-sm leading-relaxed;
}

/* Loading States */
.loading-section {
  @apply space-y-6;
}

.loading-header {
  @apply space-y-3;
}

.loading-grid {
  @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6;
}

.loading-card {
  @apply bg-white rounded-xl p-6 border border-gray-200 space-y-4;
}

.loading-skeleton {
  @apply animate-pulse bg-gray-200 rounded;
}

.loading-title {
  @apply h-6 w-48;
}

.loading-subtitle {
  @apply h-4 w-32;
}

.loading-card-header {
  @apply h-5 w-24;
}

.loading-card-content {
  @apply h-16 w-full;
}

.loading-card-button {
  @apply h-8 w-20;
}

/* Error States */
.error-section {
  @apply text-center py-12 bg-white rounded-xl border border-red-200;
}

.error-title {
  @apply text-xl font-semibold text-red-900 mb-2;
}

.error-message {
  @apply text-red-700 mb-6 max-w-md mx-auto;
}

.error-retry {
  @apply transition-all duration-200 hover:scale-105;
}

/* Empty State */
.empty-state {
  @apply text-center py-12 bg-white rounded-xl border border-gray-200;
}

.empty-title {
  @apply text-xl font-semibold text-gray-900 mb-2;
}

.empty-message {
  @apply text-gray-600 max-w-md mx-auto mb-6;
}

/* Connected Platforms */
.connected-platforms {
  @apply bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm;
}

.section-header {
  @apply flex items-center justify-between p-6 bg-gray-50 border-b border-gray-200;
}

.section-title {
  @apply text-lg font-semibold text-gray-900;
}

.platform-count {
  @apply text-sm text-gray-500;
}

/* Platforms Grid */
.platforms-grid {
  @apply p-6 grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6;
}

/* Platform Card */
.platform-card {
  @apply bg-white rounded-xl border border-gray-200 p-6 space-y-4 transition-all duration-200 hover:shadow-md hover:border-gray-300;
}

.platform-connected {
  @apply border-green-200 bg-green-50/30;
}

/* Platform Header */
.platform-header {
  @apply flex items-start gap-3;
}

.platform-icon-wrapper {
  @apply w-10 h-10 rounded-lg bg-gray-50 flex items-center justify-center flex-shrink-0;
}

.platform-icon {
  @apply w-5 h-5;
}

.platform-info {
  @apply flex-1 min-w-0;
}

.platform-name {
  @apply font-semibold text-gray-900 mb-1;
}

.platform-status {
  @apply inline-flex;
}

/* Connection Details */
.connection-details {
  @apply space-y-2;
}

.connection-info {
  @apply flex items-center gap-2 text-xs text-gray-500;
}

.connection-text {
  @apply flex-1;
}

/* Last Shared Info */
.last-shared-info {
  @apply bg-white rounded-lg p-3 border border-gray-100 space-y-2;
}

.shared-header {
  @apply flex items-center gap-2 text-xs text-gray-500;
}

.shared-label {
  @apply flex-1;
}

.share-status {
  @apply flex justify-end;
}

/* Platform Actions */
.platform-actions {
  @apply flex items-center gap-3;
}

.share-button {
  @apply flex-1 transition-all duration-200 hover:scale-105;
}

.secondary-actions {
  @apply flex items-center gap-1;
}

.action-button {
  @apply transition-all duration-200 hover:scale-110;
}

/* Animation */
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

/* Responsive */
@media (max-width: 768px) {
  .job-external-sharing {
    @apply p-4 space-y-4;
  }
  
  .header-section {
    @apply p-4;
  }
  
  .job-info-card {
    @apply p-4;
  }
  
  .section-header {
    @apply p-4;
  }
  
  .platforms-grid {
    @apply p-4 grid-cols-1 gap-4;
  }
  
  .platform-card {
    @apply p-4;
  }
  
  .platform-actions {
    @apply flex-col gap-2;
  }
  
  .share-button {
    @apply w-full;
  }
  
  .secondary-actions {
    @apply w-full justify-center;
  }
}
</style>