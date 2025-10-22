<template>
  <Dialog v-model="show" :options="{ size: '4xl', title: 'Talent Details' }">
    <template #body-content>
      <div class="talent-view-modal">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span class="ml-3 text-gray-600">Loading talent details...</span>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-8">
          <div class="text-red-600 mb-4">
            <FeatherIcon name="alert-circle" class="w-12 h-12 mx-auto" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">Error Loading Data</h3>
          <p class="text-gray-600">{{ error }}</p>
        </div>

        <!-- Content -->
        <div v-else-if="talent" class="space-y-6">
          <!-- Header Section -->
          <div class="bg-gray-50 rounded-lg p-6">
            <div class="flex items-start justify-between">
              <div class="flex items-center space-x-4">
                <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-white text-xl font-bold">
                  {{ getInitials(talent.full_name) }}
                </div>
                <div>
                  <h2 class="text-2xl font-bold text-gray-900">
                    {{ talent.full_name }}
                  </h2>
                  <p class="text-gray-600">{{ talent.email }}</p>
                  <p class="text-gray-600">{{ talent.phone }}</p>
                </div>
              </div>
              <div class="text-right">
                <Badge :theme="getStatusTheme(talent.current_status)">
                  {{ talent.current_status || 'Unknown' }}
                </Badge>
                <div class="mt-2 text-sm text-gray-500">
                  Last updated: {{ formatRelativeDate(talent.modified) }}
                </div>
              </div>
            </div>
          </div>

          <!-- Main Content Grid -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Basic Information -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="user" class="w-5 h-5 inline mr-2" />
                  Basic Information
                </h3>
                <div class="space-y-3">
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Full Name:</span>
                    <span class="font-medium">{{ talent.full_name || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Gender:</span>
                    <span class="font-medium">{{ talent.gender || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Date of Birth:</span>
                    <span class="font-medium">{{ formatDate(talent.date_of_birth) || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Email:</span>
                    <span class="font-medium">{{ talent.email || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Phone:</span>
                    <span class="font-medium">{{ talent.phone || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2">
                    <span class="text-gray-600">Experience:</span>
                    <span class="font-medium">{{ formatExperience(talent.experience_years) }}</span>
                  </div>
                </div>
              </div>

              <!-- Location Information -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="map-pin" class="w-5 h-5 inline mr-2" />
                  Location
                </h3>
                <div class="space-y-3">
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Current Location:</span>
                    <span class="font-medium">{{ talent.current_location || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2">
                    <span class="text-gray-600">Preferred Location:</span>
                    <span class="font-medium">{{ talent.preferred_location || '-' }}</span>
                  </div>
                </div>
              </div>

              <!-- Social Profiles -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="globe" class="w-5 h-5 inline mr-2" />
                  Social Profiles
                </h3>
                <div class="space-y-3">
                  <div v-if="talent.linkedin_profile" class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">LinkedIn:</span>
                    <a :href="talent.linkedin_profile" target="_blank" class="font-medium text-blue-600 hover:text-blue-800">
                      View Profile
                    </a>
                  </div>
                  <div v-if="talent.facebook_profile" class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Facebook:</span>
                    <a :href="talent.facebook_profile" target="_blank" class="font-medium text-blue-600 hover:text-blue-800">
                      View Profile
                    </a>
                  </div>
                  <div v-if="talent.zalo_profile" class="flex justify-between py-2">
                    <span class="text-gray-600">Zalo:</span>
                    <span class="font-medium">{{ talent.zalo_profile }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Skills Information -->
              <div v-if="talent.skills" class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="zap" class="w-5 h-5 inline mr-2" />
                  Skills
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge v-for="skill in processSkills(talent.skills)" :key="skill" theme="blue" variant="subtle">
                    {{ skill }}
                  </Badge>
                </div>
              </div>

              <!-- Tags -->
              <div v-if="talent.tags" class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="tag" class="w-5 h-5 inline mr-2" />
                  Tags
                </h3>
                <div class="flex flex-wrap gap-2">
                  <Badge v-for="tag in processTags(talent.tags)" :key="tag" theme="green" variant="subtle">
                    {{ tag }}
                  </Badge>
                </div>
              </div>

              <!-- Source Information -->
              <div class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="info" class="w-5 h-5 inline mr-2" />
                  Additional Info
                </h3>
                <div class="space-y-3">
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Source:</span>
                    <span class="font-medium">{{ talent.source || '-' }}</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Status:</span>
                    <Badge :theme="getStatusTheme(talent.current_status)">
                      {{ talent.current_status || 'Unknown' }}
                    </Badge>
                  </div>
                  <div v-if="talent.resume" class="flex justify-between py-2 border-b border-gray-100">
                    <span class="text-gray-600">Resume:</span>
                    <a :href="talent.resume" target="_blank" class="font-medium text-blue-600 hover:text-blue-800">
                      <FeatherIcon name="download" class="w-4 h-4 inline mr-1" />
                      Download
                    </a>
                  </div>
                  <div class="flex justify-between py-2">
                    <span class="text-gray-600">Created:</span>
                    <span class="font-medium">{{ formatDate(talent.creation) }}</span>
                  </div>
                </div>
              </div>

              <!-- Notes -->
              <div v-if="talent.notes" class="bg-white border border-gray-200 rounded-lg p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">
                  <FeatherIcon name="file-text" class="w-5 h-5 inline mr-2" />
                  Notes
                </h3>
                <div class="text-gray-700 whitespace-pre-wrap">{{ talent.notes }}</div>
              </div>
            </div>
          </div>

          <!-- Experience & Education (if available) -->
          <div v-if="talent.experience || talent.education" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Work Experience -->
            <div v-if="talent.experience" class="bg-white border border-gray-200 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">
                <FeatherIcon name="briefcase" class="w-5 h-5 inline mr-2" />
                Work Experience
              </h3>
              <div class="text-sm text-gray-600">
                <pre class="whitespace-pre-wrap font-sans">{{ formatJSON(talent.experience) }}</pre>
              </div>
            </div>

            <!-- Education -->
            <div v-if="talent.education" class="bg-white border border-gray-200 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">
                <FeatherIcon name="book" class="w-5 h-5 inline mr-2" />
                Education
              </h3>
              <div class="text-sm text-gray-600">
                <pre class="whitespace-pre-wrap font-sans">{{ formatJSON(talent.education) }}</pre>
              </div>
            </div>
          </div>

          <!-- Certifications & Languages (if available) -->
          <div v-if="talent.certifications || talent.languages" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Certifications -->
            <div v-if="talent.certifications" class="bg-white border border-gray-200 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">
                <FeatherIcon name="award" class="w-5 h-5 inline mr-2" />
                Certifications
              </h3>
              <div class="text-sm text-gray-600">
                <pre class="whitespace-pre-wrap font-sans">{{ formatJSON(talent.certifications) }}</pre>
              </div>
            </div>

            <!-- Languages -->
            <div v-if="talent.languages" class="bg-white border border-gray-200 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">
                <FeatherIcon name="globe" class="w-5 h-5 inline mr-2" />
                Languages
              </h3>
              <div class="text-sm text-gray-600">
                <pre class="whitespace-pre-wrap font-sans">{{ formatJSON(talent.languages) }}</pre>
              </div>
            </div>
          </div>
        </div>

        <!-- No Data State -->
        <div v-else class="text-center py-8">
          <div class="text-gray-400 mb-4">
            <FeatherIcon name="user-x" class="w-12 h-12 mx-auto" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">No Data Available</h3>
          <p class="text-gray-600">No talent information found.</p>
        </div>
      </div>
    </template>

    <template #actions>
      <div class="flex justify-end">
        <Button variant="outline" theme="gray" @click="handleClose">
          Close
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed, watch } from 'vue'
import { Dialog, Button, Badge, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  talent: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'close'])

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Helper methods
const getInitials = (name) => {
  if (!name) return 'T'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getStatusTheme = (status) => {
  switch (status) {
    case 'Active':
      return 'green'
    case 'Passive':
      return 'yellow'
    case 'Not Interested':
      return 'red'
    case 'Hired':
      return 'blue'
    default:
      return 'gray'
  }
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

const formatRelativeDate = (dateStr) => {
  if (!dateStr) return '-'
  try {
    const date = new Date(dateStr)
    const now = new Date()
    const diffInSeconds = Math.floor((now - date) / 1000)
    
    if (diffInSeconds < 60) return 'Just now'
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`
    if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)} days ago`
    
    return formatDate(dateStr)
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

const processSkills = (skillsStr) => {
  if (!skillsStr) return []
  
  // If it's already an array, return it
  if (Array.isArray(skillsStr)) {
    return skillsStr.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
  }
  
  // Convert to string if it's not
  const str = String(skillsStr)
  
  // Handle JSON array format like "['Linux', 'Firewall', 'Security Policies']"
  try {
    // Try to parse as JSON first
    const parsed = JSON.parse(str)
    if (Array.isArray(parsed)) {
      return parsed.map(skill => String(skill).trim()).filter(skill => skill.length > 0)
    }
  } catch (e) {
    // If not valid JSON, continue to other formats
  }
  
  // Handle Python-like array format ['item1', 'item2', 'item3']
  if (str.startsWith('[') && str.endsWith(']')) {
    try {
      // Remove brackets and split by comma, then clean up quotes
      const content = str.slice(1, -1)
      const items = content.split(',').map(item => {
        return item.trim().replace(/^['"]|['"]$/g, '') // Remove quotes
      }).filter(item => item.length > 0)
      return items
    } catch (e) {
      console.warn('Failed to parse array-like string:', str)
    }
  }
  
  // Handle comma-separated string
  return str.split(',').map(skill => skill.trim()).filter(skill => skill.length > 0)
}

const processTags = (tagsStr) => {
  if (!tagsStr) return []
  return tagsStr.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)
}

const formatJSON = (jsonStr) => {
  if (!jsonStr) return '-'
  try {
    const parsed = JSON.parse(jsonStr)
    return JSON.stringify(parsed, null, 2)
  } catch (error) {
    return jsonStr
  }
}

// Methods
const handleClose = () => {
  emit('close')
  show.value = false
}

// Watch for modal close
watch(() => show.value, (newValue) => {
  if (!newValue) {
    emit('close')
  }
})
</script>

<style scoped>
.talent-view-modal {
  max-height: 80vh;
  overflow-y: auto;
}

/* Custom scrollbar */
.talent-view-modal::-webkit-scrollbar {
  width: 6px;
}

.talent-view-modal::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 3px;
}

.talent-view-modal::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

.talent-view-modal::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
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
</style>
