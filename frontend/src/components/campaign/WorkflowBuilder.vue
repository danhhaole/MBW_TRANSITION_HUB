<template>
  <div class="workflow-builder h-full flex flex-col">
    <!-- Header -->
    <div class="flex justify-between items-center p-6 border-b border-gray-200">
      <div>
        <h3 class="text-lg font-semibold">Your Workflow</h3>
        <p class="text-sm text-gray-600 mt-1">
          {{ selectedTemplate ? `Based on ${selectedTemplate.name} template` : 'Custom workflow' }}
        </p>
      </div>
      
      <div class="flex space-x-2">
        <Button variant="outline" theme="gray" size="sm" @click="$emit('back-to-templates')">
          <FeatherIcon name="arrow-left" class="h-4 w-4 mr-1" />
          Back to templates
        </Button>
        <Button variant="outline" theme="blue" size="sm" @click="previewWorkflow">
          <FeatherIcon name="eye" class="h-4 w-4 mr-1" />
          Preview
        </Button>
      </div>
    </div>

    <!-- Workflow Steps -->
    <div class="flex-1 p-6 overflow-y-auto">
      <div class="max-w-4xl mx-auto">
        <!-- Steps List -->
        <div class="space-y-4">
          <div
            v-for="(step, index) in workflowSteps"
            :key="step.id"
            class="workflow-step border rounded-lg p-4 bg-white hover:shadow-md transition-shadow"
            :class="step.type === 'condition' ? 'border-purple-200 bg-purple-50' : 'border-gray-200'"
          >
            <div class="flex items-center justify-between">
              <!-- Step number and info -->
              <div class="flex items-center flex-1">
                <div 
                  class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center mr-4"
                  :class="step.type === 'condition' ? 'bg-purple-100' : 'bg-blue-100'"
                >
                  <span 
                    class="text-sm font-medium"
                    :class="step.type === 'condition' ? 'text-purple-600' : 'text-blue-600'"
                  >
                    {{ index + 1 }}
                  </span>
                </div>
                
                <div class="flex items-center flex-1">
                  <FeatherIcon :name="step.icon" class="h-5 w-5 mr-3 text-gray-600" />
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-900">{{ step.name }}</h4>
                    <p class="text-sm text-gray-600">{{ step.description }}</p>
                  </div>
                </div>
              </div>

              <!-- Timing and actions -->
              <div class="flex items-center space-x-4">
                <div v-if="step.timing || step.type !== 'condition'" class="text-sm">
                  <span class="text-gray-500">
                    {{ step.type === 'condition' ? 'Check after' : 'Send after' }}
                  </span>
                  <input
                    v-model="step.delay"
                    type="number"
                    min="0"
                    class="w-16 mx-2 px-2 py-1 border border-gray-300 rounded text-center"
                  />
                  <select
                    v-model="step.delayUnit"
                    class="px-2 py-1 border border-gray-300 rounded text-sm"
                  >
                    <option value="minutes">minutes</option>
                    <option value="hours">hours</option>
                    <option value="days">days</option>
                    <option value="weeks">weeks</option>
                  </select>
                </div>

                <div class="flex space-x-2">
                  <Button
                    variant="ghost"
                    theme="gray"
                    size="sm"
                    @click="editStep(step, index)"
                  >
                    <FeatherIcon name="edit-2" class="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    theme="red"
                    size="sm"
                    @click="deleteStep(index)"
                    :disabled="workflowSteps.length === 1"
                  >
                    <FeatherIcon name="trash-2" class="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>

            <!-- Condition Branches -->
            <div v-if="step.type === 'condition' && step.branches" class="mt-4 pl-12">
              <div class="grid grid-cols-2 gap-4">
                <!-- Yes Branch -->
                <div class="border border-green-200 rounded-lg p-3 bg-green-50">
                  <div class="flex items-center justify-between mb-2">
                    <h5 class="text-sm font-medium text-green-800">Yes</h5>
                    <Button
                      variant="ghost"
                      theme="green"
                      size="sm"
                      @click="addBranchStep(index, 'yes')"
                    >
                      <FeatherIcon name="plus" class="h-3 w-3" />
                    </Button>
                  </div>
                  <div v-if="step.branches.yes.length === 0" class="text-xs text-green-600">
                    No steps added yet
                  </div>
                  <div v-else class="space-y-1">
                    <div
                      v-for="(branchStep, branchIndex) in step.branches.yes"
                      :key="branchStep.id"
                      class="text-xs bg-white rounded p-2 border border-green-200"
                    >
                      <div class="flex items-center">
                        <FeatherIcon :name="branchStep.icon" class="h-3 w-3 mr-1" />
                        <span class="font-medium">{{ branchStep.name }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- No Branch -->
                <div class="border border-red-200 rounded-lg p-3 bg-red-50">
                  <div class="flex items-center justify-between mb-2">
                    <h5 class="text-sm font-medium text-red-800">No</h5>
                    <Button
                      variant="ghost"
                      theme="red"
                      size="sm"
                      @click="addBranchStep(index, 'no')"
                    >
                      <FeatherIcon name="plus" class="h-3 w-3" />
                    </Button>
                  </div>
                  <div v-if="step.branches.no.length === 0" class="text-xs text-red-600">
                    No steps added yet
                  </div>
                  <div v-else class="space-y-1">
                    <div
                      v-for="(branchStep, branchIndex) in step.branches.no"
                      :key="branchStep.id"
                      class="text-xs bg-white rounded p-2 border border-red-200"
                    >
                      <div class="flex items-center">
                        <FeatherIcon :name="branchStep.icon" class="h-3 w-3 mr-1" />
                        <span class="font-medium">{{ branchStep.name }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Regular Conditions (if any) -->
            <div v-else-if="step.conditions && step.conditions.length > 0" class="mt-3 pl-12">
              <div class="text-xs text-gray-500 mb-2">Conditions:</div>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="condition in step.conditions"
                  :key="condition.id"
                  class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full"
                >
                  {{ condition.name }}
                </span>
              </div>
            </div>
          </div>
        </div>


        <!-- Add Step Button -->
        <div class="mt-6 text-center relative">
          <Button
            variant="outline"
            theme="blue"
            @click="toggleAddMenu"
          >
            <FeatherIcon name="plus" class="h-4 w-4 mr-2" />
            Add new
          </Button>

          <!-- Dropdown Menu -->
          <div v-if="showAddMenu" class="absolute top-full mt-2 left-1/2 transform -translate-x-1/2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
            <!-- Actions Section -->
            <div class="p-2">
              <div class="text-xs font-medium text-gray-500 px-2 py-1 mb-1">Actions</div>
              
              <div class="relative group">
                <div class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer">
                  <FeatherIcon name="mail" class="h-4 w-4 mr-2 text-gray-600" />
                  <span class="text-sm">Email</span>
                  <FeatherIcon name="chevron-right" class="h-4 w-4 ml-auto text-gray-400" />
                </div>
                
                <!-- Email Submenu -->
                <div class="absolute left-full top-0 ml-1 w-40 bg-white border border-gray-200 rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <div class="p-1">
                    <div
                      v-for="action in emailActions"
                      :key="action.type"
                      class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer text-sm"
                      @click="addStepFromMenu(action)"
                    >
                      <FeatherIcon :name="action.icon" class="h-3 w-3 mr-2 text-gray-600" />
                      {{ action.name }}
                    </div>
                  </div>
                </div>
              </div>
              
              <div
                class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer"
                @click="addStepFromMenu({ type: 'linkedin_connection', name: 'LinkedIn', icon: 'linkedin' })"
              >
                <FeatherIcon name="linkedin" class="h-4 w-4 mr-2 text-gray-600" />
                <span class="text-sm">LinkedIn</span>
              </div>
              
              <div
                class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer"
                @click="addStepFromMenu({ type: 'phone_call', name: 'Call', icon: 'phone' })"
              >
                <FeatherIcon name="phone" class="h-4 w-4 mr-2 text-gray-600" />
                <span class="text-sm">Call</span>
              </div>
            </div>

            <div class="border-t border-gray-100"></div>

            <!-- Conditions Section -->
            <div class="p-2">
              <div class="text-xs font-medium text-gray-500 px-2 py-1 mb-1">Conditions</div>
              
              <div
                class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer"
                @click="addConditionFromMenu({ type: 'is_connected', name: 'Is Connected', icon: 'user-check' })"
              >
                <FeatherIcon name="user-check" class="h-4 w-4 mr-2 text-gray-600" />
                <span class="text-sm">Is Connected</span>
              </div>
              
              <div
                class="flex items-center p-2 rounded hover:bg-gray-50 cursor-pointer"
                @click="addConditionFromMenu({ type: 'custom_condition', name: 'Condition', icon: 'git-branch' })"
              >
                <FeatherIcon name="git-branch" class="h-4 w-4 mr-2 text-gray-600" />
                <span class="text-sm">Condition</span>
              </div>
            </div>
          </div>

          <!-- Backdrop to close dropdown -->
          <div v-if="showAddMenu" class="fixed inset-0 z-40" @click="closeAddMenu"></div>
        </div>
      </div>
    </div>

    <!-- Footer Actions -->
    <div class="flex justify-between items-center p-6 border-t border-gray-200 bg-gray-50">
      <Button variant="outline" theme="gray" @click="$emit('back')">
        Back
      </Button>
      
      <div class="flex space-x-3">
        <Button variant="outline" theme="gray" @click="saveDraft">
          Save Draft
        </Button>
        <Button variant="solid" theme="blue" @click="continueToNext">
          Continue
        </Button>
      </div>
    </div>

    <!-- Edit Step Modal -->
    <EditStepModal
      v-if="showEditStepModal"
      v-model="showEditStepModal"
      :step="editingStep"
      @save-step="saveStep"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import EditStepModal from './EditStepModal.vue'

// Props
const props = defineProps({
  selectedTemplate: {
    type: Object,
    default: null
  },
  isCustom: {
    type: Boolean,
    default: false
  }
})

// Emits
const emit = defineEmits(['back', 'back-to-templates', 'continue', 'save-draft'])

// State
const workflowSteps = ref([])
const showAddMenu = ref(false)
const previewAction = ref(null)
const showEditStepModal = ref(false)
const editingStep = ref(null)
const editingIndex = ref(-1)

// Email actions for the sidebar
const emailActions = [
  {
    type: 'personalized_email',
    name: 'Personalized',
    icon: 'mail',
    description: 'Send personalized email with dynamic content'
  },
  {
    type: 'templated_email', 
    name: 'Templated',
    icon: 'file-text',
    description: 'Send email using predefined template'
  },
  {
    type: 'custom_email',
    name: 'Custom email',
    icon: 'edit',
    description: 'Send custom email with specific content'
  }
]

// Initialize workflow from template
onMounted(() => {
  if (props.selectedTemplate && props.selectedTemplate.steps) {
    workflowSteps.value = props.selectedTemplate.steps.map((step, index) => ({
      id: `step-${index + 1}`,
      name: step.name,
      description: step.description,
      icon: step.icon,
      type: getStepType(step.name),
      delay: extractDelay(step.timing),
      delayUnit: extractDelayUnit(step.timing),
      timing: step.timing,
      conditions: [],
      config: {}
    }))
  } else {
    // Start with one default step
    workflowSteps.value = [{
      id: 'step-1',
      name: 'Personalized Email',
      description: 'Send a personalized welcome email',
      icon: 'mail',
      type: 'email',
      delay: 0,
      delayUnit: 'days',
      timing: 'Immediate',
      conditions: [],
      config: {}
    }]
  }
})

// Helper functions
const getStepType = (stepName) => {
  if (stepName.toLowerCase().includes('email')) return 'email'
  if (stepName.toLowerCase().includes('linkedin')) return 'linkedin'
  if (stepName.toLowerCase().includes('call') || stepName.toLowerCase().includes('phone')) return 'call'
  if (stepName.toLowerCase().includes('sms')) return 'sms'
  return 'email'
}

const extractDelay = (timing) => {
  if (!timing || timing === 'Immediate') return 0
  const match = timing.match(/(\d+)/)
  return match ? parseInt(match[1]) : 1
}

const extractDelayUnit = (timing) => {
  if (!timing || timing === 'Immediate') return 'days'
  if (timing.includes('minute')) return 'minutes'
  if (timing.includes('hour')) return 'hours'
  if (timing.includes('day')) return 'days'
  if (timing.includes('week')) return 'weeks'
  return 'days'
}

// Methods
const toggleAddMenu = () => {
  showAddMenu.value = !showAddMenu.value
  console.log('🔄 Toggle add menu:', showAddMenu.value)
}

const closeAddMenu = () => {
  showAddMenu.value = false
  previewAction.value = null
}

const addStepFromMenu = (action) => {
  console.log('🔄 Adding step from menu:', action)
  addStep({
    name: action.name,
    description: action.description || `Send ${action.name.toLowerCase()}`,
    type: action.type,
    icon: action.icon
  })
  closeAddMenu()
}

const addConditionFromMenu = (condition) => {
  console.log('🔄 Adding condition from menu:', condition)
  addCondition({
    name: condition.name,
    description: condition.description || `Check ${condition.name.toLowerCase()}`,
    type: condition.type,
    delay: 1,
    delayUnit: 'days',
    config: {}
  })
  closeAddMenu()
}

const addStep = (stepData) => {
  const newStep = {
    id: `step-${workflowSteps.value.length + 1}`,
    ...stepData,
    delay: 1,
    delayUnit: 'days',
    conditions: [],
    config: {},
    branches: null // For conditions
  }
  workflowSteps.value.push(newStep)
  showAddStepModal.value = false
}

const addCondition = (conditionData) => {
  const newCondition = {
    id: `condition-${workflowSteps.value.length + 1}`,
    type: 'condition',
    name: conditionData.name,
    description: conditionData.description,
    icon: 'git-branch',
    delay: conditionData.delay || 1,
    delayUnit: conditionData.delayUnit || 'days',
    conditions: [],
    config: conditionData.config || {},
    branches: {
      yes: [],
      no: []
    }
  }
  workflowSteps.value.push(newCondition)
  showAddConditionModal.value = false
}

const editStep = (step, index) => {
  editingStep.value = { ...step }
  editingIndex.value = index
  showEditStepModal.value = true
}

const saveStep = (stepData) => {
  if (editingIndex.value >= 0) {
    workflowSteps.value[editingIndex.value] = {
      ...workflowSteps.value[editingIndex.value],
      ...stepData
    }
  }
  showEditStepModal.value = false
  editingStep.value = null
  editingIndex.value = -1
}

const deleteStep = (index) => {
  if (workflowSteps.value.length > 1) {
    workflowSteps.value.splice(index, 1)
  }
}

const addBranchStep = (conditionIndex, branch) => {
  // For now, add a simple email step to the branch
  const newBranchStep = {
    id: `branch-${Date.now()}`,
    name: 'Templated Email',
    description: 'Send follow-up email',
    icon: 'mail',
    type: 'templated_email',
    delay: 1,
    delayUnit: 'days',
    config: {}
  }
  
  workflowSteps.value[conditionIndex].branches[branch].push(newBranchStep)
  console.log(`Added step to ${branch} branch of condition ${conditionIndex}`)
}

const previewWorkflow = () => {
  // TODO: Show preview modal
  console.log('Preview workflow:', workflowSteps.value)
}

const saveDraft = () => {
  emit('save-draft', {
    steps: workflowSteps.value,
    template: props.selectedTemplate
  })
}

const continueToNext = () => {
  emit('continue', {
    steps: workflowSteps.value,
    template: props.selectedTemplate
  })
}
</script>

<style scoped>
.workflow-step {
  transition: all 0.2s ease;
}

.workflow-step:hover {
  border-color: #e5e7eb;
}
</style>
