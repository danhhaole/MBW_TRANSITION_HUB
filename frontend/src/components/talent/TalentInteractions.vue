<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900">{{ __('Marketing & Personal Interaction History')}}</h2>
      <p class="text-sm text-gray-600 mt-1">{{ __('Filter by Email Sent, Email Opened, Link Clicked, Recruiter Messages.')}}</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">{{ __('Loading interactions...') }}</span>
      </div>
    </div>

    <!-- Interactions List -->
    <div v-else-if="interactions.length > 0" class="bg-white rounded-lg border border-gray-200">
      <div class="divide-y divide-gray-200">
        <div v-for="interaction in interactions" :key="interaction.name" class="p-4 hover:bg-gray-50 transition-colors">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <!-- Interaction Type and Details -->
              <div class="flex items-center space-x-2 mb-2">
                <span class="font-semibold text-gray-900">{{ getInteractionLabel(interaction.interaction_type) }}:</span>
                <span class="text-gray-700">
                  <template v-if="interaction.campaign_name">
                    {{ __('Campaign') }}: '{{ interaction.campaign_name }}'
                  </template>
                  <template v-else-if="interaction.action">
                    {{ interaction.action }}
                  </template>
                  <template v-else>
                    {{ interaction.interaction_type }}
                  </template>
                </span>
              </div>

              <!-- Platform Info -->
              <div v-if="interaction.platform" class="text-sm text-gray-600 mb-1">
                {{ __('Platform') }}: {{ interaction.platform }}
                <span v-if="interaction.social_page_name"> - {{ interaction.social_page_name }}</span>
              </div>

              <!-- URL if available -->
              <div v-if="interaction.url" class="text-sm text-gray-600 mb-1">
                {{ __('URL') }}: <a :href="interaction.url" target="_blank" class="text-blue-600 hover:underline">{{ interaction.url }}</a>
              </div>

              <!-- Channel -->
              <div v-if="interaction.channel" class="text-xs text-gray-500">
                {{ __('Channel') }}: {{ interaction.channel }}
              </div>
            </div>

            <!-- Date -->
            <div class="text-right ml-4">
              <p class="text-sm font-medium text-gray-900">{{ formatDate(interaction.creation) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white rounded-lg border border-gray-200 p-12 text-center">
      <FeatherIcon name="inbox" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No Interactions Yet') }}</h3>
      <p class="text-gray-500">{{ __('Email and marketing interactions will appear here.') }}</p>
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

const interactions = ref([])
const loading = ref(false)

// Fetch interactions when component mounts
onMounted(() => {
  fetchInteractions()
})

// Watch for talent changes
watch(() => props.talent?.name, (newVal) => {
  if (newVal) {
    fetchInteractions()
  }
})

const fetchInteractions = async () => {
  if (!props.talent?.name) return
  
  loading.value = true
  try {
    const response = await call('mbw_mira.api.interaction.get_talent_email_interactions', {
      talent_id: props.talent.name
    })
    
    if (response && response.interactions) {
      interactions.value = response.interactions
    }
  } catch (error) {
    console.error('Error fetching interactions:', error)
  } finally {
    loading.value = false
  }
}

const getInteractionLabel = (type) => {
  const labels = {
    'EMAIL_SENT': 'Email Sent',
    'EMAIL_OPENED': 'Email Opened',
    'ON_LINK_CLICK': 'Link Clicked',
    'EMAIL_DELIVERED': 'Email Delivered',
    'EMAIL_BOUNCED': 'Email Bounced',
    'EMAIL_UNSUBSCRIBED': 'Email Unsubscribed',
    'EMAIL_REPLIED': 'Email Replied'
  }
  return labels[type] || type
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
