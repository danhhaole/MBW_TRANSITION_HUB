<template>
  <Dialog :show="show" @close="$emit('close')" :options="{ title: 'Sequence Preview', size: 'xl' }">
    <div v-if="sequence" class="space-y-6">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div>
          <h3 class="text-lg font-medium text-gray-900">{{ sequence.title }}</h3>
          <p v-if="sequence.purpose" class="text-sm text-gray-600 mt-1">{{ sequence.purpose }}</p>
        </div>
        <Badge
          :variant="getStatusVariant(sequence.status)"
          :label="sequence.display_status"
        />
      </div>

      <!-- Basic Info -->
      <div class="grid grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
          <div class="flex items-center">
            <div class="w-3 h-3 rounded-full mr-2" :class="getStatusColorClass(sequence.status)"></div>
            <span class="text-sm text-gray-900">{{ sequence.display_status }}</span>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Enrollment Source</label>
          <p class="text-sm text-gray-900">{{ sequence.enrollment_source || 'Not specified' }}</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Total Steps</label>
          <div class="flex items-center">
            <FeatherIcon name="layers" class="w-4 h-4 mr-2 text-gray-400" />
            <span class="text-sm text-gray-900">{{ sequence.steps_count }} steps</span>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Enrollments</label>
          <div class="flex items-center">
            <FeatherIcon name="users" class="w-4 h-4 mr-2 text-gray-400" />
            <span class="text-sm text-gray-900">{{ sequence.enrollment_count || 0 }} people enrolled</span>
          </div>
        </div>
      </div>

      <!-- Steps Preview -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-3">Sequence Steps</label>
        <div v-if="parsedSteps.length > 0" class="space-y-3">
          <div
            v-for="(step, index) in parsedSteps"
            :key="index"
            class="border border-gray-200 rounded-lg p-4 bg-gray-50"
          >
            <div class="flex items-start justify-between">
              <div class="flex items-start">
                <div class="flex-shrink-0 w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                  <span class="text-xs font-medium text-blue-600">{{ index + 1 }}</span>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-gray-900">
                    {{ getStepTitle(step) }}
                  </h4>
                  <p v-if="step.delay_from_previous" class="text-xs text-gray-500 mt-1">
                    <FeatherIcon name="clock" class="w-3 h-3 inline mr-1" />
                    Delay: {{ step.delay_from_previous }}
                  </p>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <Badge
                  v-if="step.channel"
                  :label="step.channel"
                  variant="gray"
                  size="sm"
                />
                <Badge
                  v-if="step.action_if_replied"
                  :label="step.action_if_replied"
                  variant="blue"
                  size="sm"
                />
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8 text-gray-500">
          <FeatherIcon name="inbox" class="w-8 h-8 mx-auto mb-2 text-gray-400" />
          <p>No steps configured</p>
        </div>
      </div>

      <!-- Metadata -->
      <div class="border-t border-gray-200 pt-4">
        <div class="grid grid-cols-2 gap-6 text-sm">
          <div>
            <label class="block font-medium text-gray-700 mb-1">Created At</label>
            <p class="text-gray-600">{{ sequence.formatted_created_at }}</p>
          </div>
          <div>
            <label class="block font-medium text-gray-700 mb-1">Last Modified</label>
            <p class="text-gray-600">{{ sequence.formatted_modified }}</p>
          </div>
          <div>
            <label class="block font-medium text-gray-700 mb-1">Owner</label>
            <p class="text-gray-600">{{ sequence.owner_id || 'Not specified' }}</p>
          </div>
          <div>
            <label class="block font-medium text-gray-700 mb-1">Sequence ID</label>
            <p class="text-gray-600 font-mono text-xs">{{ sequence.name }}</p>
          </div>
        </div>
      </div>
    </div>

    <template #actions>
      <div class="flex justify-end space-x-3">
        <Button variant="outline" theme="gray" @click="$emit('close')">
          Close
        </Button>
        <Button variant="solid" theme="gray" @click="editSequence">
          <FeatherIcon name="edit" class="w-4 h-4 mr-2" />
          Edit Sequence
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Dialog, Button, Badge, FeatherIcon } from 'frappe-ui'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  sequence: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close'])
const router = useRouter()

// Computed
const parsedSteps = computed(() => {
  if (!props.sequence?.steps) return []
  
  try {
    const steps = typeof props.sequence.steps === 'string' 
      ? JSON.parse(props.sequence.steps) 
      : props.sequence.steps
    return Array.isArray(steps) ? steps : []
  } catch (error) {
    console.error('Error parsing steps:', error)
    return []
  }
})

// Methods
const getStatusVariant = (status) => {
  const variantMap = {
    'Active': 'success',
    'Draft': 'gray',
    'Paused': 'warning',
    'Completed': 'blue'
  }
  return variantMap[status] || 'gray'
}

const getStatusColorClass = (status) => {
  const colorMap = {
    'Active': 'bg-green-500',
    'Draft': 'bg-gray-500',
    'Paused': 'bg-yellow-500',
    'Completed': 'bg-blue-500'
  }
  return colorMap[status] || 'bg-gray-500'
}

const getStepTitle = (step) => {
  if (step.template_id) {
    return `Send Template: ${step.template_id}`
  }
  if (step.channel) {
    return `Send via ${step.channel}`
  }
  if (step.related_action) {
    return step.related_action
  }
  return `Step ${step.step_order || 'N/A'}`
}

const editSequence = () => {
  emit('close')
  router.push({ name: 'SequenceEditor', params: { id: props.sequence.name } })
}
</script>
