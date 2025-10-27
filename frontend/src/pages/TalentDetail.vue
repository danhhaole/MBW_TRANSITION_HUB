<template>
  <div class="min-h-screen bg-gray-50">
    <!-- <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader> -->

    <div class="talent-detail-page w-full min-h-screen bg-gray-50">
      <!-- Loading State -->
      <Loading v-if="loading && !talent" text="Loading talent details..." />

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-8">
        <div class="text-red-600 mb-4">
          <FeatherIcon name="alert-circle" class="w-12 h-12 mx-auto" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Error Loading Talent</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <Button variant="outline" theme="blue" @click="handleRefresh">
          <template #prefix>
            <FeatherIcon name="refresh-cw" class="h-4 w-4" />
          </template>
          Try Again
        </Button>
      </div>

      <!-- Main Content -->
      <div v-else-if="talent" class="flex">
        <!-- Left Sidebar - Talent Information -->
        <div class="w-80 flex-shrink-0 bg-white border-r border-gray-200">
          <div class="sticky top-0 h-screen overflow-y-auto">
            <!-- Back Navigation -->
            <div class="p-4 border-gray-200">
              <button
                @click="goBack"
                class="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors"
              >
                <FeatherIcon name="arrow-left" class="w-4 h-4" />
                <span class="font-medium">Back to Talent List</span>
              </button>
            </div>

            <!-- Talent Header -->
            <div class="p-6">
              <!-- Action Dropdown -->
              <div class="flex justify-end mb-4">
                <Dropdown :options="actionOptions" placement="bottom-end">
                  <template #default="{ open }">
                    <Button variant="ghost" theme="gray" class="p-2">
                      <FeatherIcon name="more-horizontal" class="w-4 h-4" />
                    </Button>
                  </template>
                </Dropdown>
              </div>

              <!-- Avatar and Basic Info -->
              <div class="text-center mb-6">
                <div class="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
                  {{ getInitials(talent.full_name) }}
                </div>
                <h1 class="text-xl font-bold text-gray-900 mb-1">{{ talent.full_name }}</h1>
                <p class="text-gray-600 mb-2">{{ talent.email }}</p>
                <Badge v-if="talent.status" :theme="getStatusColor(talent.status)" variant="subtle">
                  {{ talent.status }}
                </Badge>
              </div>

              <!-- Contact Information -->
              <div class="space-y-4">
                <h3 class="text-sm font-medium text-gray-900 uppercase tracking-wide">Contact Information</h3>
                
                <div v-if="talent.mobile_no" class="flex items-center space-x-3">
                  <FeatherIcon name="phone" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.mobile_no }}</span>
                </div>
                
                <div v-if="talent.email" class="flex items-center space-x-3">
                  <FeatherIcon name="mail" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.email }}</span>
                </div>
                
                <div v-if="talent.location" class="flex items-center space-x-3">
                  <FeatherIcon name="map-pin" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.location }}</span>
                </div>
              </div>

              <!-- Professional Information -->
              <div class="space-y-4 mt-6">
                <h3 class="text-sm font-medium text-gray-900 uppercase tracking-wide">Professional</h3>
                
                <div v-if="talent.current_city" class="flex items-center space-x-3">
                  <FeatherIcon name="briefcase" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.current_city }}</span>
                </div>
                
                <div v-if="talent.latest_company" class="flex items-center space-x-3">
                  <FeatherIcon name="building" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.latest_company }}</span>
                </div>
                
                <div v-if="talent.total_years_of_experience" class="flex items-center space-x-3">
                  <FeatherIcon name="clock" class="w-4 h-4 text-gray-400" />
                  <span class="text-sm text-gray-700">{{ talent.total_years_of_experience }} years experience</span>
                </div>
              </div>


              <!-- Social Links -->
              <!-- <div class="space-y-4 mt-6">
                <h3 class="text-sm font-medium text-gray-900 uppercase tracking-wide">Social</h3>
                
                <div v-if="talent.linkedin_profile" class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2">
                    <FeatherIcon name="linkedin" class="w-4 h-4 text-blue-600" />
                    <span class="text-sm text-gray-700">{{ talent.linkedin_profile }}</span>
                  </div>
                </div>
                
                <div v-if="talent.facebook_profile" class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2">
                    <FeatherIcon name="facebook" class="w-4 h-4 text-blue-600" />
                    <span class="text-sm text-gray-700">{{ talent.facebook_profile }}</span>
                  </div>
                </div>
                
                <div v-if="talent.zalo_profile" class="flex items-center space-x-3">
                  <div class="flex items-center space-x-2">
                    <FeatherIcon name="message-circle" class="w-4 h-4 text-green-600" />
                    <span class="text-sm text-gray-700">{{ talent.zalo_profile }}</span>
                  </div>
                </div>
              </div> -->

              <!-- Tags -->
              <div class="mt-6">
                <TalentTagPicker
                  v-if="talent"
                  :docname="talent.name"
                  doctype="Mira Talent"
                  v-model="talent._user_tags"
                  :isTalentView="true"
                />
              </div>
            </div>

            <!-- Additional Information -->
            <div class="border-t border-gray-200">
              <div class="p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-4 flex items-center">
                  <FeatherIcon name="info" class="w-4 h-4 mr-2" />
                  Additional Information
                </h3>
                
                <div class="space-y-3 text-sm">
                  <div v-if="talent.gender" class="flex justify-between">
                    <span class="text-gray-600">Gender:</span>
                    <span class="font-medium">{{ talent.gender }}</span>
                  </div>
                  <div v-if="talent.date_of_birth" class="flex justify-between">
                    <span class="text-gray-600">Date of Birth:</span>
                    <span class="font-medium">{{ formatDate(talent.date_of_birth) }}</span>
                  </div>
                  <div v-if="talent.experience_years" class="flex justify-between">
                    <span class="text-gray-600">Experience:</span>
                    <span class="font-medium">{{ formatExperience(talent.experience_years) }}</span>
                  </div>
                  <div v-if="talent.source" class="flex justify-between">
                    <span class="text-gray-600">Source:</span>
                    <span class="font-medium">{{ talent.source }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Created:</span>
                    <span class="font-medium">{{ formatDate(talent.creation) }}</span>
                  </div>
                </div>
              </div>

              <!-- Skills -->
              <div v-if="talent.skills" class="border-t border-gray-200 p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-3 flex items-center">
                  <FeatherIcon name="zap" class="w-4 h-4 mr-2" />
                  Skills
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge
                    v-for="skill in processSkills(talent.skills)"
                    :key="skill"
                    theme="blue"
                    variant="subtle"
                    class="text-xs"
                  >
                    {{ skill }}
                  </Badge>
                </div>
              </div>

              <!-- Social Profiles -->
              <div v-if="talent.linkedin_profile || talent.facebook_profile || talent.zalo_profile" class="border-t border-gray-200 p-4">
                <h3 class="text-sm font-medium text-gray-900 mb-3 flex items-center">
                  <FeatherIcon name="globe" class="w-4 h-4 mr-2" />
                  Social Profiles
                </h3>
                <div class="space-y-2">
                  <div v-if="talent.linkedin_profile" class="flex items-center space-x-2">
                    <FeatherIcon name="linkedin" class="w-4 h-4 text-blue-600" />
                    <a :href="talent.linkedin_profile" target="_blank" class="text-sm text-blue-600 hover:text-blue-800">
                      LinkedIn Profile
                    </a>
                  </div>
                  <div v-if="talent.facebook_profile" class="flex items-center space-x-2">
                    <FeatherIcon name="facebook" class="w-4 h-4 text-blue-600" />
                    <a :href="talent.facebook_profile" target="_blank" class="text-sm text-blue-600 hover:text-blue-800">
                      Facebook Profile
                    </a>
                  </div>
                  <div v-if="talent.zalo_profile" class="flex items-center space-x-2">
                    <FeatherIcon name="message-circle" class="w-4 h-4 text-green-600" />
                    <span class="text-sm text-gray-700">{{ talent.zalo_profile }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Content - Tabs -->
        <div class="flex-1 bg-white flex flex-col">
          <!-- Sticky Tab Navigation -->
          <div class="sticky top-0 z-10 bg-white border-b border-gray-200">
            <nav class="flex space-x-8 px-6" aria-label="Tabs">
              <button
                v-for="(tab, index) in tabs"
                :key="tab.name"
                @click="tabIndex = index"
                :class="[
                  'py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center space-x-2',
                  tabIndex === index
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                <component :is="tab.icon" />
                <span>{{ tab.label }}</span>
                <Badge v-if="tab.count > 0" theme="gray" variant="subtle" class="text-xs">
                  {{ tab.count }}
                </Badge>
              </button>
            </nav>
          </div>

          <!-- Tab Content -->
          <div class="flex-1 overflow-y-auto">
            <div class="p-6">
              <div class="container mx-auto max-w-6xl">
                <!-- Summary Tab -->
                <TalentSummary v-if="tabs[tabIndex]?.content === 'summary'" :talent="talent" />
                
                <!-- Interactions Tab -->
                <TalentInteractions v-else-if="tabs[tabIndex]?.content === 'interactions'" :talent="talent" />
                
                <!-- Applications Tab -->
                <TalentApplications v-else-if="tabs[tabIndex]?.content === 'applications'" :talent="talent" />
                
                <!-- Activities Tab -->
                <TalentActivities v-else-if="tabs[tabIndex]?.content === 'activities'" :talent="talent" />
                
                <!-- Notes Tab -->
                <TalentNotes v-else-if="tabs[tabIndex]?.content === 'notes'" :talent="talent" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>


</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTalentDetailStore } from '@/stores/talentDetail'
import { useToast } from '@/composables/useToast'
import { Button, Badge, Dropdown, FeatherIcon, Breadcrumbs, Tabs } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import TalentSummary from '@/components/talent/TalentSummary.vue'
import TalentInteractions from '@/components/talent/TalentInteractions.vue'
import TalentApplications from '@/components/talent/TalentApplications.vue'
import TalentActivities from '@/components/talent/TalentActivities.vue'
import TalentNotes from '@/components/talent/TalentNotes.vue'
import TalentTagPicker from '@/components/TalentTagPicker.vue'
import { useActiveTabManager } from "@/composables/useActiveTabManager";
// Router
const route = useRoute()
const router = useRouter()

// Store
const talentDetailStore = useTalentDetailStore()

// Composables
const { showSuccess, showError } = useToast()

// Reactive data
const talentName = computed(() => route.params.id)

// Computed from store
const talent = computed(() => talentDetailStore.talent)
const loading = computed(() => talentDetailStore.loading)
const error = computed(() => talentDetailStore.error)
const activities = computed(() => talentDetailStore.formattedActivities)
const attachments = computed(() => talentDetailStore.attachments)

// Computed for stats
const activityCount = computed(() => talentDetailStore.activityCount)
const commentCount = computed(() => talentDetailStore.commentCount)
const attachmentCount = computed(() => talentDetailStore.attachmentCount)

const recentActivities = computed(() => activities.value.slice(0, 5))

// Breadcrumbs
const breadcrumbs = computed(() => [
  { label: 'Talent', route: { name: 'Talent' } },
  { label: talent.value?.full_name || 'Detail', route: { name: 'TalentDetail', params: { id: talentName.value } } }
])


// Main tabs configuration for Frappe UI Tabs
const tabs = computed(() => [
  {
    label: 'Summary',
    name: 'summary',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'bar-chart-2' }),
    count: 0,
    content: 'summary'
  },
  {
    label: 'Interactions',
    name: 'interactions',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'users' }),
    count: 0,
    content: 'interactions'
  },
  {
    label: 'Applications',
    name: 'applications',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'briefcase' }),
    count: 0,
    content: 'applications'
  },
  {
    label: 'Activities',
    name: 'activities',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'activity' }),
    count: activityCount.value,
    content: 'activities'
  },
  {
    label: 'Notes',
    name: 'notes',
    icon: h(FeatherIcon, { class: 'w-4 h-4', name: 'message-circle' }),
    count: commentCount.value,
    content: 'notes'
  }
])

// Tab index for custom tabs
const tabIndex = ref(0)


// Action dropdown options
const actionOptions = [
  {
    label: 'Edit Talent',
    icon: 'edit',
    onClick: () => editTalent()
  },
  {
    label: 'Delete Talent',
    icon: 'trash-2',
    onClick: () => deleteTalent(),
    class: 'text-red-600'
  }
]

// Methods
const handleRefresh = async () => {
  await talentDetailStore.fetchTalent(talentName.value)
}

const goBack = () => {
  router.push({ name: 'TalentSegments' })
}


const editTalent = () => {
  // TODO: Implement edit functionality
  showSuccess('Edit functionality coming soon')
}

const deleteTalent = () => {
  // TODO: Implement delete functionality
  showError('Delete functionality coming soon')
}

const downloadAttachment = (attachment) => {
  window.open(attachment.file_url, '_blank')
}

// Helper methods
const getInitials = (name) => {
  if (!name) return 'T'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getStatusColor = (status) => {
  switch (status) {
    case 'Active': return 'green'
    case 'Passive': return 'yellow'
    case 'Not Interested': return 'red'
    case 'Hired': return 'blue'
    default: return 'gray'
  }
}

const processSkills = (skillsStr) => {
  if (!skillsStr) return []
  try {
    const parsed = JSON.parse(skillsStr)
    if (Array.isArray(parsed)) {
      return parsed.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
    }
  } catch (e) {
    // Continue to string processing
  }
  
  if (skillsStr.startsWith('[') && skillsStr.endsWith(']')) {
    try {
      const content = skillsStr.slice(1, -1)
      const items = content.split(',').map(item => {
        return item.trim().replace(/^['"]|['"]$/g, '')
      }).filter(item => item.length > 0)
      return items
    } catch (e) {
      console.warn('Failed to parse skills:', skillsStr)
    }
  }
  
  return skillsStr.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0)
}

const processTags = (tagsStr) => {
  if (!tagsStr) return []
  return tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (error) {
    return dateStr
  }
}

const formatExperience = (years) => {
  if (!years) return '-'
  const num = parseFloat(years)
  if (num === 1) return '1 year'
  return `${num} years`
}

const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getActivityDotColor = (type) => {
  switch (type) {
    case 'comment': return 'bg-blue-500'
    case 'changed': return 'bg-yellow-500'
    case 'added': return 'bg-green-500'
    case 'removed': return 'bg-red-500'
    case 'creation': return 'bg-purple-500'
    default: return 'bg-gray-500'
  }
}

const getActivitySummary = (activity) => {
  switch (activity.activity_type) {
    case 'comment': return 'Added a comment'
    case 'changed': return `Changed ${activity.data.field_label}`
    case 'added': return `Added ${activity.data.field_label}`
    case 'removed': return `Removed ${activity.data.field_label}`
    case 'creation': return 'Created this talent'
    default: return activity.activity_type
  }
}

// Lifecycle
onMounted(async () => {
  if (talentName.value) {
    await talentDetailStore.fetchTalent(talentName.value)
  }
})

// Watch for route changes
watch(() => route.params.id, async (newId) => {
  if (newId) {
    talentDetailStore.clearTalent()
    await talentDetailStore.fetchTalent(newId)
  }
})

// Cleanup on unmount
onUnmounted(() => {
  talentDetailStore.clearTalent()
})
</script>

<style scoped>
/* Layout */
.talent-detail-page {
  height: calc(100vh - 60px); /* Adjust based on header height */
}

/* Custom scrollbar for sidebar */
.talent-detail-page ::-webkit-scrollbar {
  width: 6px;
}

.talent-detail-page ::-webkit-scrollbar-track {
  background: #f8fafc;
}

.talent-detail-page ::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.talent-detail-page ::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Sidebar styling */
.talent-detail-page .w-80 {
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.05);
}

/* Tab content container */
.talent-detail-page .container {
  padding-left: 0;
  padding-right: 0;
}

/* Smooth transitions */
.talent-detail-page button {
  transition: all 0.2s ease-in-out;
}

/* Loading animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .talent-detail-page .w-80 {
    width: 280px;
  }
}

@media (max-width: 768px) {
  .talent-detail-page .flex {
    flex-direction: column;
  }
  
  .talent-detail-page .w-80 {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .talent-detail-page .sticky {
    position: relative;
    height: auto;
  }
}
</style>
