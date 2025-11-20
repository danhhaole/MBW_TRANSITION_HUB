<template>
  <div class="space-y-6">
    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-blue-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100">
            <FeatherIcon name="briefcase" class="w-6 h-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-blue-600">{{ __('Total Interactions (Open/Click)')}}</p>
            <p class="text-2xl font-bold text-blue-900">{{ totalInteractions }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-green-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100">
            <FeatherIcon name="check-circle" class="w-6 h-6 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-green-600">{{ __('Time to MQL (Days)')}}</p>
            <p class="text-2xl font-bold text-green-900">{{ engagementTimeline }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-purple-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100">
            <FeatherIcon name="star" class="w-6 h-6 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-purple-600">{{ __('Engagement Score')}}</p>
            <p class="text-2xl font-bold text-purple-900">{{ engagementScore }}/100</p>
          </div>
        </div>
      </div>

      <div class="bg-orange-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100">
            <FeatherIcon name="clock" class="w-6 h-6 text-orange-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-orange-600">{{ __('Last Interaction Date')}}</p>
            <p class="text-xl font-bold text-orange-900">{{ lastInteractionDate }}</p> 
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Chart -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Performance Overview</h3>
      <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
        <div class="text-center">
          <FeatherIcon name="bar-chart-2" class="w-12 h-12 text-gray-400 mx-auto mb-2" />
          <p class="text-gray-500">Performance chart will be implemented here</p>
        </div>
      </div>
    </div>

    <!-- Recent Activity Summary -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
      <!-- <div class="space-y-4">
        <div class="flex items-center space-x-4">
          <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">Applied to Senior Developer position</p>
            <p class="text-xs text-gray-500">2 hours ago</p>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="w-2 h-2 bg-green-500 rounded-full"></div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">Completed technical interview</p>
            <p class="text-xs text-gray-500">1 day ago</p>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">Profile updated</p>
            <p class="text-xs text-gray-500">3 days ago</p>
          </div>
        </div>
      </div> -->
    </div>

    <!-- Skills Assessment -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Skills Assessment') }}</h3>
      <div class="space-y-3">
        <!-- Hard Skills -->
        <div class="text-sm">
          <span class="font-medium text-gray-900">{{ __('Hard Skills') }}:</span>
          <span class="text-gray-600 ml-2">{{ talent.hard_skills || __('None') }}</span>
        </div>
        
        <!-- Soft Skills -->
        <div class="text-sm">
          <span class="font-medium text-gray-900">{{ __('Soft Skills') }}:</span>
          <span class="text-gray-600 ml-2">{{ talent.soft_skills || __('None') }}</span>
        </div>
        
        <!-- Domain Expertise -->
        <div class="text-sm">
          <span class="font-medium text-gray-900">{{ __('Domain Expertise') }}:</span>
          <span class="text-gray-600 ml-2">{{ talent.domain_expertise || __('None') }}</span>
        </div>
        
        <!-- Cultural Fit -->
        <div class="text-sm">
          <span class="font-medium text-gray-900">{{ __('Cultural Fit') }}:</span>
          <span class="text-gray-600 ml-2">{{ talent.cultural_fit || __('None') }}</span>
        </div>
        
        <!-- Internal Rating -->
        <div class="text-sm">
          <span class="font-medium text-gray-900">{{ __('Internal Rating') }}:</span>
          <span class="text-gray-600 ml-2">{{ talent.internal_rating || __('None') }}</span>
        </div>
        
        <!-- Availability Date & Expected Salary -->
        <div class="text-sm">
          <span class="font-medium text-gray-900">{{ __('Availability Date') }}:</span>
          <span class="text-gray-600 ml-2">{{ formatDate(talent.availability_date) }}</span>
          <span class="text-gray-400 mx-2">|</span>
          <span class="font-medium text-gray-900">{{ __('Expected Salary') }}:</span>
          <span class="text-gray-600 ml-2">{{ formatCurrency(talent.expected_salary) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { FeatherIcon, call } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})

const totalInteractions = ref(0)
const engagementTimeline = ref(0)
const engagementScore = ref(0)

// Helper for internationalization
const __ = (text) => text

// Helper function to format currency
const formatCurrency = (amount) => {
  if (!amount) return __('None')
  const num = parseFloat(amount)
  if (isNaN(num)) return __('None')
  
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(num)
}

// Helper function to format date
const formatDate = (dateStr) => {
  if (!dateStr) return __('None')
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (error) {
    return __('None')
  }
}

// Computed để lấy talent ID
const talentId = computed(() => props.talent?.name)

// Computed để format last interaction date
const lastInteractionDate = computed(() => {
  const lastDate = props.talent?.last_interaction_date
  if (!lastDate) return __('Not yet interacted')
  
  try {
    const date = new Date(lastDate)
    return date.toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch (error) {
    return __('Not yet interacted')
  }
})

// Function để đếm interactions
const fetchInteractionCount = async () => {
  if (!talentId.value) return
  
  try {
    // Sử dụng frappe.client.get_list để query interactions
    const interactions = await call('frappe.client.get_list', {
      doctype: 'Mira Interaction',
      filters: {
        talent_id: talentId.value,
        interaction_type: ['in', ['EMAIL_OPENED', 'ON_LINK_CLICK', 'ZALO_CLICK']]
      },
      fields: ['name'],
      limit_page_length: 0 // Lấy tất cả records để đếm
    })
    
    totalInteractions.value = interactions ? interactions.length : 0
  } catch (error) {
    console.error('Error fetching interaction count:', error)
    totalInteractions.value = 0
  }
}

// Function để lấy engagement summary
const fetchEngagementSummary = async () => {
  if (!talentId.value) return
  
  try {
    // Lấy engagement summary cho talent
    const summaries = await call('frappe.client.get_list', {
      doctype: 'Mira Engagement Summary',
      filters: {
        talent_id: talentId.value
      },
      fields: ['engagement_timeline', 'total_score'],
      limit_page_length: 1,
      order_by: 'creation desc' // Lấy record mới nhất
    })
    
    if (summaries && summaries.length > 0) {
      const summary = summaries[0]
      engagementTimeline.value = summary.engagement_timeline || 0
      engagementScore.value = summary.total_score || 0
    } else {
      engagementTimeline.value = 0
      engagementScore.value = 0
    }
  } catch (error) {
    console.error('Error fetching engagement summary:', error)
    engagementTimeline.value = 0
    engagementScore.value = 0
  }
}

// Fetch data khi component mount
onMounted(() => {
  fetchInteractionCount()
  fetchEngagementSummary()
})

// Watch talent changes để update count
watch(talentId, (newTalentId) => {
  if (newTalentId) {
    fetchInteractionCount()
    fetchEngagementSummary()
  }
}, { immediate: true })
</script>
