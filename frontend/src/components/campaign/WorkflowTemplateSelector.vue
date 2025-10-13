<template>
  <div class="workflow-template-selector">
    <div class="flex h-full">
      <!-- Left side - Template selection -->
      <div class="w-1/2 p-6 border-r border-gray-200">
        <h3 class="text-lg font-semibold mb-4">Choose your template</h3>
        
        <div class="grid grid-cols-2 gap-4">
          <!-- Template cards -->
          <div
            v-for="template in templates"
            :key="template.id"
            class="template-card border-2 rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-lg"
            :class="[
              selectedTemplate?.id === template.id 
                ? 'border-blue-500 bg-blue-50' 
                : 'border-gray-200 hover:border-gray-300',
              template.color
            ]"
            @click="selectTemplate(template)"
            @mouseenter="previewTemplate = template"
            @mouseleave="previewTemplate = selectedTemplate"
          >
            <div class="flex flex-col items-center text-center">
              <div 
                class="w-12 h-12 rounded-lg flex items-center justify-center mb-3"
                :class="template.iconBg"
              >
                <FeatherIcon :name="template.icon" class="h-6 w-6 text-white" />
              </div>
              <h4 class="font-medium text-gray-900 mb-1">{{ template.name }}</h4>
              <p class="text-xs text-gray-600">{{ template.description }}</p>
            </div>
          </div>

          <!-- Start from scratch option -->
          <div
            class="template-card border-2 border-dashed border-gray-300 rounded-lg p-4 cursor-pointer transition-all duration-200 hover:border-gray-400 hover:bg-gray-50"
            @click="selectTemplate(null)"
          >
            <div class="flex flex-col items-center text-center">
              <div class="w-12 h-12 rounded-lg bg-gray-100 flex items-center justify-center mb-3">
                <FeatherIcon name="plus" class="h-6 w-6 text-gray-400" />
              </div>
              <h4 class="font-medium text-gray-900 mb-1">Start from scratch</h4>
              <p class="text-xs text-gray-600">Create your own workflow</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right side - Preview -->
      <div class="w-1/2 p-6 bg-gradient-to-br from-purple-100 to-purple-200">
        <div v-if="previewTemplate" class="h-full">
          <h4 class="text-lg font-semibold mb-4 text-gray-900">
            {{ previewTemplate.name }} Preview
          </h4>
          
          <!-- Preview workflow -->
          <div class="bg-white rounded-lg p-4 h-full overflow-y-auto">
            <div class="space-y-3">
              <div
                v-for="(step, index) in previewTemplate.steps"
                :key="index"
                class="flex items-center p-3 bg-gray-50 rounded-lg"
              >
                <div class="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <span class="text-sm font-medium text-blue-600">{{ index + 1 }}</span>
                </div>
                <div class="flex-1">
                  <div class="flex items-center mb-1">
                    <FeatherIcon :name="step.icon" class="h-4 w-4 mr-2 text-gray-600" />
                    <span class="font-medium text-gray-900">{{ step.name }}</span>
                  </div>
                  <p class="text-xs text-gray-600">{{ step.description }}</p>
                  <div v-if="step.timing" class="text-xs text-blue-600 mt-1">
                    {{ step.timing }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Empty state -->
        <div v-else class="h-full flex items-center justify-center">
          <div class="text-center text-gray-500">
            <div class="w-16 h-16 bg-purple-200 rounded-full flex items-center justify-center mx-auto mb-4">
              <FeatherIcon name="eye" class="h-8 w-8 text-purple-400" />
            </div>
            <p>Hover over a template to see preview</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="flex justify-between items-center p-6 border-t border-gray-200 bg-gray-50">
      <Button variant="outline" theme="gray" @click="$emit('back')">
        Back
      </Button>
      
      <Button 
        variant="solid" 
        theme="blue" 
        @click="continueWithTemplate"
        :disabled="!selectedTemplate && !isCustom"
      >
        {{ selectedTemplate ? 'Use This Template' : 'Create Custom Workflow' }}
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'

// Props
const props = defineProps({
  modelValue: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'continue', 'back'])

// State
const selectedTemplate = ref(props.modelValue)
const previewTemplate = ref(props.modelValue)

// Computed
const isCustom = computed(() => selectedTemplate.value === null)

// Mock templates data
const templates = [
  {
    id: 'value-ladder',
    name: 'Value Ladder',
    description: 'For trust building relationships',
    icon: 'trending-up',
    iconBg: 'bg-blue-500',
    color: 'border-blue-200',
    steps: [
      {
        name: 'Welcome Email',
        description: 'Personalized welcome message',
        icon: 'mail',
        timing: 'Immediate'
      },
      {
        name: 'Value Content',
        description: 'Share industry insights',
        icon: 'book-open',
        timing: 'After 2 days'
      },
      {
        name: 'LinkedIn Connection',
        description: 'Connect on LinkedIn',
        icon: 'linkedin',
        timing: 'After 5 days'
      },
      {
        name: 'Follow-up Email',
        description: 'Check interest and next steps',
        icon: 'mail',
        timing: 'After 7 days'
      }
    ]
  },
  {
    id: 'thermal',
    name: 'Thermal',
    description: 'For event-driven outreach',
    icon: 'thermometer',
    iconBg: 'bg-purple-500',
    color: 'border-purple-200',
    steps: [
      {
        name: 'Event Invitation',
        description: 'Invite to upcoming event',
        icon: 'calendar',
        timing: 'Immediate'
      },
      {
        name: 'Reminder Email',
        description: 'Event reminder with details',
        icon: 'bell',
        timing: '1 day before event'
      },
      {
        name: 'Follow-up Survey',
        description: 'Post-event feedback',
        icon: 'clipboard',
        timing: '1 day after event'
      }
    ]
  },
  {
    id: '1-touch',
    name: '1 Touch',
    description: 'For simple, direct engagement',
    icon: 'hand',
    iconBg: 'bg-pink-500',
    color: 'border-pink-200',
    steps: [
      {
        name: 'Direct Outreach',
        description: 'Single personalized message',
        icon: 'send',
        timing: 'Immediate'
      }
    ]
  },
  {
    id: 'social-selling',
    name: 'Social Selling',
    description: 'For LinkedIn-first prospects',
    icon: 'users',
    iconBg: 'bg-indigo-500',
    color: 'border-indigo-200',
    steps: [
      {
        name: 'LinkedIn View Profile',
        description: 'View their LinkedIn profile',
        icon: 'eye',
        timing: 'Immediate'
      },
      {
        name: 'Like Recent Post',
        description: 'Engage with their content',
        icon: 'heart',
        timing: 'After 1 day'
      },
      {
        name: 'Connection Request',
        description: 'Send personalized connection',
        icon: 'user-plus',
        timing: 'After 3 days'
      },
      {
        name: 'LinkedIn Message',
        description: 'Start conversation',
        icon: 'message-circle',
        timing: 'After connection accepted'
      }
    ]
  },
  {
    id: 'direct-action',
    name: 'Direct Action',
    description: 'For time-sensitive prospects',
    icon: 'zap',
    iconBg: 'bg-yellow-500',
    color: 'border-yellow-200',
    steps: [
      {
        name: 'Urgent Email',
        description: 'Time-sensitive opportunity',
        icon: 'clock',
        timing: 'Immediate'
      },
      {
        name: 'Phone Call',
        description: 'Direct phone follow-up',
        icon: 'phone',
        timing: 'Same day'
      },
      {
        name: 'Final Email',
        description: 'Last chance offer',
        icon: 'mail',
        timing: 'After 2 days'
      }
    ]
  }
]

// Methods
const selectTemplate = (template) => {
  selectedTemplate.value = template
  previewTemplate.value = template
  emit('update:modelValue', template)
}

const continueWithTemplate = () => {
  emit('continue', {
    template: selectedTemplate.value,
    isCustom: isCustom.value
  })
}
</script>

<style scoped>
.workflow-template-selector {
  height: 600px;
  display: flex;
  flex-direction: column;
}

.template-card:hover {
  transform: translateY(-2px);
}
</style>
