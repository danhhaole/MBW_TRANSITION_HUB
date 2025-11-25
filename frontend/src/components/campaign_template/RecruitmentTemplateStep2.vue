<template>
  <div class="space-y-6 animate-fadeIn">
    <!-- Header -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-base font-semibold text-gray-900 mb-2">
        {{ __('Content Templates') }}
      </h3>
      <p class="text-sm text-gray-600">
        {{ __('Create content templates for recruitment campaign across multiple channels') }}
      </p>
    </div>

    <!-- Channel Selection with Add Button -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h4 class="text-sm font-semibold text-gray-900">
          {{ __('Posting Channels') }}
        </h4>
        
        <!-- Add Channel Dropdown -->
        <Dropdown v-if="availableChannelOptions.length > 0" :options="availableChannelOptions">
          <template v-slot="{ open }">
            <Button variant="solid" size="sm" :theme="'gray'">
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
              {{ __('Add Channel') }}
              <template #suffix>
                <FeatherIcon
                  :name="open ? 'chevron-up' : 'chevron-down'"
                  class="h-4 w-4"
                />
              </template>
            </Button>
          </template>
        </Dropdown>
        
        <!-- All channels added message -->
        <div v-else class="text-xs text-gray-500 flex items-center">
          <FeatherIcon name="check" class="h-3 w-3 mr-1" />
          {{ __('All channels added') }}
        </div>
      </div>

      <!-- Selected Channels -->
      <div v-if="localSelectedChannels.length > 0" class="space-y-4">
        <!-- Email Channel -->
        <div v-if="localSelectedChannels.includes('email')" class="border border-purple-200 rounded-lg p-4 bg-purple-50">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center mr-3">
                <FeatherIcon name="mail" class="h-4 w-4 text-white" />
              </div>
              <h5 class="text-sm font-medium text-gray-900">{{ __('Email Template') }}</h5>
            </div>
            <Button variant="ghost" size="sm" theme="red" @click="removeChannel('email')">
              <FeatherIcon name="trash-2" class="h-4 w-4" />
            </Button>
          </div>
          
          <EmailContentEditor
            v-model="localEmailContent"
            :show-error="false"
          />
        </div>

        <!-- Facebook Channel -->
        <div v-if="localSelectedChannels.includes('facebook')" class="border border-blue-200 rounded-lg p-4 bg-blue-50">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
                <FeatherIcon name="facebook" class="h-4 w-4 text-white" />
              </div>
              <h5 class="text-sm font-medium text-gray-900">{{ __('Facebook Post Template') }}</h5>
            </div>
            <Button variant="ghost" size="sm" theme="red" @click="removeChannel('facebook')">
              <FeatherIcon name="trash-2" class="h-4 w-4" />
            </Button>
          </div>
          
          <FacebookContentEditor
            v-model="localFacebookContent"
            :show-error="false"
          />
        </div>

        <!-- Zalo Channel -->
        <div v-if="localSelectedChannels.includes('zalo')" class="border border-green-200 rounded-lg p-4 bg-green-50">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center mr-3">
                <FeatherIcon name="message-circle" class="h-4 w-4 text-white" />
              </div>
              <h5 class="text-sm font-medium text-gray-900">{{ __('Zalo Message Template') }}</h5>
            </div>
            <Button variant="ghost" size="sm" theme="red" @click="removeChannel('zalo')">
              <FeatherIcon name="trash-2" class="h-4 w-4" />
            </Button>
          </div>
          
          <ZaloContentEditor
            v-model="localZaloContent"
            :show-error="false"
          />
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-8 text-gray-500">
        <FeatherIcon name="plus-circle" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
        <p class="text-sm">{{ __('No channels selected') }}</p>
        <p class="text-xs">{{ __('Click "Add Channel" to start creating content templates') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Dropdown, FeatherIcon } from 'frappe-ui'
import EmailContentEditor from '@/components/campaign_new/molecules/EmailContentEditor.vue'
import FacebookContentEditor from '@/components/campaign_new/molecules/FacebookContentEditor.vue'
import ZaloContentEditor from '@/components/campaign_new/molecules/ZaloContentEditor.vue'

const props = defineProps({
  selectedChannels: {
    type: Array,
    default: () => []
  },
  emailContent: {
    type: Object,
    default: () => ({ content: '' })
  },
  facebookContent: {
    type: Object,
    default: () => ({ content: '' })
  },
  zaloContent: {
    type: Object,
    default: () => ({ content: '' })
  }
})

const emit = defineEmits(['update:selectedChannels', 'update:emailContent', 'update:facebookContent', 'update:zaloContent'])

// Local reactive data
const localSelectedChannels = ref([...props.selectedChannels])
const localEmailContent = ref({ ...props.emailContent })
const localFacebookContent = ref({ ...props.facebookContent })
const localZaloContent = ref({ ...props.zaloContent })

// Available channels (Email, Facebook, Zalo - no QR)
const templateChannels = [
  { label: __('Email'), value: 'email', icon: 'mail' },
  { label: __('Facebook'), value: 'facebook', icon: 'facebook' },
  { label: __('Zalo'), value: 'zalo', icon: 'message-circle' }
]

const availableChannelOptions = computed(() => {
  return templateChannels
    .filter(channel => !localSelectedChannels.value.includes(channel.value))
    .map(channel => ({
      label: channel.label,
      icon: channel.icon,
      onClick: () => addChannel(channel.value)
    }))
})

const addChannel = (channelValue) => {
  if (!localSelectedChannels.value.includes(channelValue)) {
    localSelectedChannels.value.push(channelValue)
    emit('update:selectedChannels', localSelectedChannels.value)
  }
}

const removeChannel = (channelValue) => {
  const index = localSelectedChannels.value.indexOf(channelValue)
  if (index > -1) {
    localSelectedChannels.value.splice(index, 1)
    emit('update:selectedChannels', localSelectedChannels.value)
    
    // Clear content when removing channel
    if (channelValue === 'email') {
      localEmailContent.value = { content: '' }
      emit('update:emailContent', localEmailContent.value)
    } else if (channelValue === 'facebook') {
      localFacebookContent.value = { content: '' }
      emit('update:facebookContent', localFacebookContent.value)
    } else if (channelValue === 'zalo') {
      localZaloContent.value = { content: '' }
      emit('update:zaloContent', localZaloContent.value)
    }
  }
}

// Watch for content changes (với immediate: false để tránh recursive)
watch(() => localEmailContent.value, (newValue, oldValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    emit('update:emailContent', newValue)
  }
}, { deep: true, immediate: false })

watch(() => localFacebookContent.value, (newValue, oldValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    emit('update:facebookContent', newValue)
  }
}, { deep: true, immediate: false })

watch(() => localZaloContent.value, (newValue, oldValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    emit('update:zaloContent', newValue)
  }
}, { deep: true, immediate: false })

// Watch for prop changes (chỉ update khi thực sự khác)
watch(() => props.selectedChannels, (newValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(localSelectedChannels.value)) {
    localSelectedChannels.value = [...newValue]
  }
})

watch(() => props.emailContent, (newValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(localEmailContent.value)) {
    localEmailContent.value = { ...newValue }
  }
})

watch(() => props.facebookContent, (newValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(localFacebookContent.value)) {
    localFacebookContent.value = { ...newValue }
  }
})

watch(() => props.zaloContent, (newValue) => {
  if (JSON.stringify(newValue) !== JSON.stringify(localZaloContent.value)) {
    localZaloContent.value = { ...newValue }
  }
})

</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
