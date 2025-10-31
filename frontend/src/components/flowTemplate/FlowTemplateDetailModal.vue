<template>
  <Dialog
    v-model="isOpen"
    :options="{
      title: template?.name_template || __('Template Details'),
      size: 'xl',
    }"
  >
    <template #body-content>
      <div v-if="template" class="space-y-6">
        <!-- Template Header with Thumbnail -->
        <div class="flex items-start space-x-6">
          <!-- Thumbnail -->
          <div class="flex-shrink-0">
            <img
              :src="template.thumbnail_url"
              :alt="template.name_template"
              class="w-48 h-32 object-cover rounded-lg border border-gray-200"
            />
          </div>

          <!-- Template Info -->
          <div class="flex-1">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="text-xl font-semibold text-gray-900">
                  {{ template.name_template }}
                </h3>
                <p v-if="template.alias" class="text-sm text-gray-500 mt-1">
                  {{ template.alias }}
                </p>
              </div>
              <div class="flex items-center space-x-2">
                <Badge
                  :theme="template.type_badge_color"
                  :label="template.display_type"
                />
                <Badge
                  v-if="template.is_default"
                  theme="green"
                  :label="__('System Template')"
                />
                <Badge
                  v-if="template.is_premium"
                  theme="purple"
                  :label="__('Premium')"
                />
              </div>
            </div>

            <!-- Description -->
            <p class="text-gray-700 text-sm leading-relaxed">
              {{ template.description || __('No description available') }}
            </p>

            <!-- Meta Info -->
            <div class="flex items-center space-x-4 mt-4 text-xs text-gray-500">
              <div class="flex items-center">
                <FeatherIcon name="calendar" class="w-3 h-3 mr-1" />
                {{ __('Created') }}: {{ template.formatted_created_at }}
              </div>
              <div class="flex items-center">
                <FeatherIcon name="users" class="w-3 h-3 mr-1" />
                {{ __('Used') }}: {{ template.usage_count || 0 }} {{ __('times') }}
              </div>
            </div>
          </div>
        </div>

        <!-- Template Details -->
        <div class="border-t border-gray-200 pt-6">
          <h4 class="text-sm font-semibold text-gray-900 mb-4">{{ __('Template Details') }}</h4>
          
          <div class="grid grid-cols-2 gap-4">
            <!-- Flow Type -->
            <div v-if="template.flow_type" class="bg-gray-50 rounded-lg p-3">
              <div class="text-xs text-gray-500 mb-1">{{ __('Flow Type') }}</div>
              <div class="text-sm font-medium text-gray-900">{{ template.flow_type }}</div>
            </div>

            <!-- Channel -->
            <div v-if="template.channel" class="bg-gray-50 rounded-lg p-3">
              <div class="text-xs text-gray-500 mb-1">{{ __('Channel') }}</div>
              <div class="flex items-center text-sm font-medium text-gray-900">
                <FeatherIcon :name="getChannelIcon(template.channel)" class="w-4 h-4 mr-2" />
                {{ template.channel }}
              </div>
            </div>

            <!-- Target Type -->
            <div v-if="template.target_type" class="bg-gray-50 rounded-lg p-3">
              <div class="text-xs text-gray-500 mb-1">{{ __('Target Type') }}</div>
              <div class="text-sm font-medium text-gray-900">{{ template.target_type }}</div>
            </div>

            <!-- Scope -->
            <div class="bg-gray-50 rounded-lg p-3">
              <div class="text-xs text-gray-500 mb-1">{{ __('Scope') }}</div>
              <div class="text-sm font-medium text-gray-900">{{ template.display_scope }}</div>
            </div>
          </div>
        </div>

        <!-- Scenario Description -->
        <div class="border-t border-gray-200 pt-6">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">{{ __('Scenario Description') }}</h4>
          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div class="flex items-start">
              <FeatherIcon name="info" class="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
              <div class="ml-3">
                <h5 class="text-sm font-medium text-blue-900 mb-2">{{ __('Use Case') }}</h5>
                <p class="text-sm text-blue-800 leading-relaxed">
                  {{ template.description || __('This template helps you automate your workflow efficiently.') }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Triggers (if available) -->
        <div v-if="template.template_triggers && template.template_triggers.length > 0" class="border-t border-gray-200 pt-6">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">{{ __('Triggers') }}</h4>
          <div class="space-y-2">
            <div
              v-for="(trigger, index) in template.template_triggers"
              :key="index"
              class="flex items-center p-3 bg-green-50 border border-green-200 rounded-lg"
            >
              <FeatherIcon name="zap" class="w-4 h-4 text-green-600 mr-3" />
              <span class="text-sm text-green-900">{{ trigger.trigger_type || __('Trigger') }}</span>
            </div>
          </div>
        </div>

        <!-- Actions (if available) -->
        <div v-if="template.template_actions && template.template_actions.length > 0" class="border-t border-gray-200 pt-6">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">{{ __('Actions') }}</h4>
          <div class="space-y-2">
            <div
              v-for="(action, index) in template.template_actions"
              :key="index"
              class="flex items-center p-3 bg-purple-50 border border-purple-200 rounded-lg"
            >
              <FeatherIcon name="send" class="w-4 h-4 text-purple-600 mr-3" />
              <span class="text-sm text-purple-900">{{ action.action_type || __('Action') }}</span>
            </div>
          </div>
        </div>

        <!-- CTA URL (if available) -->
        <div v-if="template.is_has_url_cta && template.url_cta" class="border-t border-gray-200 pt-6">
          <h4 class="text-sm font-semibold text-gray-900 mb-3">{{ __('Additional Resources') }}</h4>
          <a
            :href="template.url_cta"
            target="_blank"
            class="inline-flex items-center text-sm text-blue-600 hover:text-blue-700"
          >
            <FeatherIcon name="external-link" class="w-4 h-4 mr-2" />
            {{ __('View Documentation') }}
          </a>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else class="flex items-center justify-center py-12">
        <FeatherIcon name="loader" class="w-8 h-8 text-gray-400 animate-spin" />
      </div>
    </template>

    <template #actions>
      <div class="flex justify-between w-full">
        <Button
          variant="outline"
          theme="gray"
          @click="closeModal"
        >
          {{ __('Cancel') }}
        </Button>
        <Button
          theme="blue"
          @click="handleUseTemplate"
          :loading="loading"
        >
          <template #prefix>
            <FeatherIcon name="check" class="w-4 h-4" />
          </template>
          {{ __('Use Template') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, Badge, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  template: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['close', 'use-template'])

// Local state
const isOpen = ref(props.show)

// Watch for prop changes
watch(() => props.show, (newValue) => {
  isOpen.value = newValue
})

watch(isOpen, (newValue) => {
  if (!newValue) {
    closeModal()
  }
})

// Methods
const closeModal = () => {
  isOpen.value = false
  emit('close')
}

const handleUseTemplate = () => {
  emit('use-template', props.template)
}

const getChannelIcon = (channel) => {
  const iconMap = {
    'Email': 'mail',
    'SMS': 'message-square',
    'Zalo': 'message-circle',
    'Messenger': 'facebook'
  }
  return iconMap[channel] || 'send'
}
</script>
