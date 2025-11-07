<template>
  <div class="space-y-6">
    <!-- Show warning if no interaction method selected -->
    <div v-if="!interactionMethod" class="text-center py-12">
      <FeatherIcon name="alert-triangle" class="h-8 w-8 text-yellow-600 mx-auto mb-2" />
      <h4 class="text-lg font-medium text-yellow-900 mb-2">
        {{ __("No interaction method selected") }}
      </h4>
      <p class="text-yellow-700">
        {{ __("Please go back to Step 1 to select an interaction method") }}
      </p>
    </div>

    <!-- Flow Timeline (copy 100% từ SequenceEditor) -->
    <div v-else class="relative">
      <!-- Initial Delay (Before first flow) -->
      <div v-if="parsedFlows.length > 0" class="relative text-center mb-12">
        <!-- Đường nối nửa đầu -->
        <div
          class="absolute left-1/2 top-full translate-x-[-50%] w-px h-12 border-l-2 border-dashed border-gray-300 z-0"
        ></div>
        <!-- Display Initial Delay -->
        <div
          @click="editInitialDelay"
          class="inline-flex items-center space-x-2 bg-white text-black px-4 py-2 rounded-full text-sm font-medium cursor-pointer hover:bg-blue-100 transition-colors"
        >
          <FeatherIcon name="play" class="w-4 h-4" />
          <span>{{ __('Send after ') }}{{ initialDelay || '1 Ngày' }}</span>
        </div>
      </div>

      <!-- Flows List -->
      <div v-if="parsedFlows.length > 0" class="relative">
        <div
          v-for="(flow, index) in parsedFlows"
          :key="index"
          class="relative mb-16"
        >
          <!-- Timeline connector to next flow -->

          <!-- Delay Indicator on Timeline -->
          <div
            v-if="index > 0"
            class="absolute left-0 -top-12 flex items-center justify-center w-full z-10"
          >
            <!-- Display Delay -->
            <div
              @click="editDelay(index)"
              class="inline-flex items-center space-x-2 bg-white text-black px-4 py-2 rounded-full text-sm font-medium cursor-pointer hover:bg-orange-100 transition-colors"
            >
              <FeatherIcon name="clock" class="w-4 h-4" />
              <span>{{ __('Wait ') }}{{ flow.delay || '1 day' }}
                {{ __('then continue') }}</span
              >
            </div>
          </div>

          <!-- Flow Block -->
          <div
            class="bg-white rounded-lg shadow-sm border transition-all duration-200 relative z-10"
          >
            <!-- Flow Number Circle - Positioned at center -->
            <div
              class="absolute bg-white -left-12 top-6 w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium border border-solid border-blue-500 z-20 shadow-sm"
              :class="getFlowIconClass()"
            >
              {{ index + 1 }}
            </div>

            <!-- Flow Header (Collapsed View) -->
            <div
              class="p-6 pl-12 hover:bg-gray-50 transition-colors group relative"
              @mouseenter="hoveredFlow = index"
              @mouseleave="hoveredFlow = -1"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4 flex-1">
                  <!-- Flow Info -->
                  <div class="flex-1">
                    <!-- Editable Title -->
                    <div class="flex items-center group">
                      <FeatherIcon
                        :name="getFlowIcon()"
                        class="w-4 h-4 mr-2 flex-shrink-0"
                      />
                      
                      <!-- Display mode -->
                      <h3
                        v-if="editingTitleIndex !== index"
                        class="font-medium text-gray-900 flex items-center"
                      >
                        {{ getFlowTitle(flow) }}
                        <button
                          @click="startEditTitle(index, flow)"
                          class="ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
                        >
                          <FeatherIcon
                            name="edit"
                            class="w-4 h-4 text-black hover:text-blue-600"
                          />
                        </button>
                      </h3>
                      
                      <!-- Edit mode -->
                      <div
                        v-else
                        class="flex items-center space-x-2 flex-1"
                      >
                        <input
                          v-model="editingTitleValue"
                          @keyup.enter="saveFlowTitle(index)"
                          @keyup.esc="cancelEditTitle"
                          class="flex-1 px-2 py-1 border border-blue-500 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                          autofocus
                        />
                        <button
                          @click="saveFlowTitle(index)"
                          class="p-1 text-green-600 hover:bg-green-50 rounded"
                        >
                          <FeatherIcon name="check" class="w-4 h-4" />
                        </button>
                        <button
                          @click="cancelEditTitle"
                          class="p-1 text-red-600 hover:bg-red-50 rounded"
                        >
                          <FeatherIcon name="x" class="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    
                    <p class="text-sm text-gray-500 mt-1">
                      {{ getFlowDescription(flow) }}
                    </p>
                  </div>
                </div>

                <!-- Actions Menu (Show on hover, hide when editing) -->
                <div
                  v-if="hoveredFlow === index && expandedFlow !== index"
                  class="absolute -right-[120px] top-1/2 transform -translate-y-1/2 bg-gray-50 p-2 flex flex-col space-y-1 z-20"
                >
                  <button
                    @click="editFlow(index)"
                    class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
                  >
                    <FeatherIcon name="edit" class="w-4 h-4 mr-2" />
                    {{ __('Edit') }}
                  </button>
                  <button
                    @click="duplicateFlow(index)"
                    class="flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-md transition-colors"
                  >
                    <FeatherIcon name="copy" class="w-4 h-4 mr-2" />
                    {{ __('Duplicate') }}
                  </button>
                  <button
                    @click="confirmDeleteFlow(index)"
                    class="flex items-center px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md transition-colors"
                  >
                    <FeatherIcon name="trash-2" class="w-4 h-4 mr-2" />
                    {{ __('Delete') }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Flow Content Editor (Expanded View) -->
            <div
              v-if="expandedFlow === index"
              class="border-t border-gray-100"
            >
              <div class="p-6 space-y-6">
                <!-- Email Editor -->
                <div v-if="interactionMethod === 'EMAIL'">
                  <EmailEditor
                    :content="getFlowContent(flow)"
                    @update:content="updateFlowContent(index, $event)"
                  />
                </div>

                <!-- Text Content Editor for SMS/Messenger/Zalo -->
                <div
                  v-else-if="
                    interactionMethod === 'ZALO_ZNS' ||
                    interactionMethod === 'ZALO_CARE'
                  "
                >
                  <ZaloEditor
                    :content="getFlowContent(flow)"
                    @update:content="updateFlowContent(index, $event)"
                  />
                </div>

                <!-- Basic fields for all types -->
                <div class="space-y-4 border-t border-gray-100 pt-6">
                  <div>
                    <label
                      class="block text-sm font-medium text-gray-700 mb-2"
                    >
                      {{ __('Template ID') }}
                    </label>
                    <input
                      v-model="flow.template_id"
                      type="text"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :placeholder="__('Enter template ID')"
                    />
                  </div>

                  <div>
                    <label
                      class="block text-sm font-medium text-gray-700 mb-2"
                    >
                      {{ __('Action if Replied') }}
                    </label>
                    <select
                      v-model="flow.action_if_replied"
                      class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="Continue">Continue</option>
                      <option value="Stop Sequence">Stop Sequence</option>
                    </select>
                  </div>
                </div>

                <!-- Additional Actions -->
                <div class="border-t border-gray-100 pt-6">
                  <AdditionalActions
                    :interaction-type="interactionMethod"
                    :model-value="flow.content?.additional_actions || {}"
                    @update:model-value="updateFlowAdditionalActions(index, $event)"
                  />
                </div>
              </div>

              <!-- Action Buttons -->
              <div
                class="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-end space-x-3"
              >
                <Button variant="outline" theme="gray" @click="cancelEdit">
                  {{ __('Cancel') }}
                </Button>
                <Button
                  variant="solid"
                  theme="gray"
                  @click="saveFlowContent(index)"
                >
                  {{ __('Save Changes') }}
                </Button>
              </div>
            </div>

            <!-- Dòng nối (gạch gạch gạch) -->
            <div
              v-if="index < parsedFlows.length - 1"
              class="absolute left-1/2 top-full translate-x-[-50%] w-px h-16 border-l-2 border-dashed border-gray-300 z-0"
            ></div>
          </div>
        </div>
      </div>

      <!-- Add Flow Button -->
      <div class="text-center relative">
        <!-- Timeline line extends to button -->

        <div
          class="border-2 border-dashed border-gray-300 rounded-lg p-8 bg-gray-50 hover:bg-gray-100 transition-colors"
        >
          <Button
            variant="outline"
            theme="blue"
            @click="addFlow"
            class="w-full py-3"
          >
            <div class="flex items-center justify-center">
              <FeatherIcon name="plus" class="w-5 h-5 mr-2" />
              {{ __('Add Flow') }}
            </div>
          </Button>
        </div>
      </div>
    </div>

    <!-- Delay Edit Modal -->
    <DelayEditModal
      :show="showDelayModal"
      :current-delay="currentEditingDelay"
      :is-initial="editingDelayIndex === 0"
      @save="saveDelayFromModal"
      @cancel="cancelDelayEdit"
      @update:show="showDelayModal = $event"
    />

    <!-- Delete Confirmation Dialog -->
    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      @click.self="cancelDelete"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <div class="flex items-start mb-4">
          <div class="flex-shrink-0">
            <FeatherIcon name="alert-triangle" class="w-6 h-6 text-red-600" />
          </div>
          <div class="ml-3 flex-1">
            <h3 class="text-lg font-medium text-gray-900">
              {{ __('Delete Flow') }}
            </h3>
            <p class="mt-2 text-sm text-gray-500">
              {{ __('Are you sure you want to delete this flow? This action cannot be undone.') }}
            </p>
          </div>
        </div>
        <div class="flex justify-end space-x-3 mt-6">
          <Button
            variant="outline"
            @click="cancelDelete"
          >
            {{ __('Cancel') }}
          </Button>
          <Button
            variant="solid"
            theme="red"
            @click="removeFlow"
          >
            <div class="flex items-center">
              <FeatherIcon name="trash-2" class="w-4 h-4 mr-2" />
              {{ __('Delete') }}
            </div>
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, FeatherIcon } from 'frappe-ui'
import DelayEditModal from '@/components/sequence/DelayEditModal.vue'
import EmailEditor from './content-editors/EmailEditor.vue'
import ZaloEditor from './content-editors/ZaloEditor.vue'
import AdditionalActions from './AdditionalActions.vue'

const props = defineProps({
  interactionMethod: {
    type: String,
    default: ''
  },
  modelValue: {
    type: Array,
    default: () => []
  },
  campaignId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:model-value'])

// Reactive state (copy từ SequenceEditor)
const expandedFlow = ref(-1)
const editingTitleIndex = ref(-1)
const editingTitleValue = ref('')
const hoveredFlow = ref(-1)
const showDelayModal = ref(false)
const editingDelayIndex = ref(-1)
const currentEditingDelay = ref('')
const initialDelay = ref('1 Ngày')
const showDeleteConfirm = ref(false)
const flowToDelete = ref(null)

// Computed
const parsedFlows = computed({
  get: () => props.modelValue || [],
  set: (value) => emit('update:model-value', value)
})

// Methods (copy từ SequenceEditor, đổi step -> flow)
const getFlowIcon = () => {
  const iconMap = {
    EMAIL: 'mail',
    ZALO_ZNS: 'message-square',
    ZALO_CARE: 'message-circle',
  }
  return iconMap[props.interactionMethod] || 'send'
}

const getFlowIconClass = () => {
  const classMap = {
    EMAIL: 'text-blue-600 border-blue-500',
    ZALO_ZNS: 'text-blue-600 border-blue-500',
    ZALO_CARE: 'text-blue-600 border-blue-500',
  }
  return classMap[props.interactionMethod] || 'text-gray-600 border-gray-500'
}

const getFlowTitle = (flow) => {
  return flow.name || `Flow ${parsedFlows.value.indexOf(flow) + 1}`
}

const getFlowDescription = (flow) => {
  if (flow.template_id) {
    return `Using template: ${flow.template_id}`
  }
  return flow.description || `Send a ${props.interactionMethod.toLowerCase()} message to the contact`
}

const getFlowContent = (flow) => {
  if (!flow.content) return {}
  
  if (props.interactionMethod === 'EMAIL') {
    return {
      email_subject: flow.content.email_subject || '',
      email_content: flow.content.email_content || '',
      attachments: flow.content.attachments || [],
    }
  } else {
    // For Zalo
    return {
      blocks: flow.content.blocks || [
        {
          id: 1,
          type: 'text',
          text_content: flow.content.message_content || '',
        },
      ],
    }
  }
}

const updateFlowContent = (index, content) => {
  const updatedFlows = [...parsedFlows.value]
  const flow = updatedFlows[index]
  
  if (!flow.content) {
    flow.content = {}
  }
  
  // Update email content
  if (content.email_subject !== undefined || content.email_content !== undefined || content.attachments !== undefined) {
    if (content.email_subject !== undefined) {
      flow.content.email_subject = content.email_subject
    }
    if (content.email_content !== undefined) {
      flow.content.email_content = content.email_content
    }
    if (content.attachments !== undefined) {
      flow.content.attachments = content.attachments
    }
  }
  
  // Update Zalo blocks
  if (content.blocks !== undefined) {
    flow.content.blocks = content.blocks
  }
  
  parsedFlows.value = updatedFlows
}

const updateFlowAdditionalActions = (index, actions) => {
  const updatedFlows = [...parsedFlows.value]
  const flow = updatedFlows[index]
  
  if (!flow.content) {
    flow.content = {}
  }
  
  // actions is already the additional_actions object
  flow.content.additional_actions = actions
  
  parsedFlows.value = updatedFlows
}

const addFlow = () => {
  const newFlow = {
    id: Date.now(),
    name: `Flow ${parsedFlows.value.length + 1}`,
    description: '',
    content: {},
    delay: '1 day',
    template_id: '',
    action_if_replied: 'Continue'
  }
  parsedFlows.value = [...parsedFlows.value, newFlow]
}

const duplicateFlow = (index) => {
  const flowToDuplicate = parsedFlows.value[index]
  const duplicated = {
    ...JSON.parse(JSON.stringify(flowToDuplicate)),
    id: Date.now(),
    name: flowToDuplicate.name + ' (Copy)'
  }
  parsedFlows.value = [
    ...parsedFlows.value.slice(0, index + 1),
    duplicated,
    ...parsedFlows.value.slice(index + 1)
  ]
}

const confirmDeleteFlow = (index) => {
  flowToDelete.value = index
  showDeleteConfirm.value = true
}

const removeFlow = () => {
  if (flowToDelete.value !== null) {
    parsedFlows.value = parsedFlows.value.filter((_, i) => i !== flowToDelete.value)
    showDeleteConfirm.value = false
    flowToDelete.value = null
  }
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
  flowToDelete.value = null
}

const startEditTitle = (index, flow) => {
  editingTitleIndex.value = index
  editingTitleValue.value = flow.name || 'New Flow'
}

const cancelEditTitle = () => {
  editingTitleIndex.value = -1
  editingTitleValue.value = ''
}

const saveFlowTitle = (index) => {
  const updatedFlows = [...parsedFlows.value]
  updatedFlows[index].name = editingTitleValue.value.trim() || `Flow ${index + 1}`
  parsedFlows.value = updatedFlows
  cancelEditTitle()
}

const editDelay = (index) => {
  editingDelayIndex.value = index
  const flow = parsedFlows.value[index]
  currentEditingDelay.value = flow.delay || '1 day'
  showDelayModal.value = true
}

const editInitialDelay = () => {
  editingDelayIndex.value = 0
  currentEditingDelay.value = initialDelay.value
  showDelayModal.value = true
}

const saveDelayFromModal = (newDelay) => {
  if (editingDelayIndex.value === 0) {
    // Initial delay
    initialDelay.value = newDelay
    
    if (parsedFlows.value.length > 0) {
      const updatedFlows = [...parsedFlows.value]
      updatedFlows[0].delay = newDelay
      parsedFlows.value = updatedFlows
    }
  } else {
    // Flow delay
    const updatedFlows = [...parsedFlows.value]
    updatedFlows[editingDelayIndex.value].delay = newDelay
    parsedFlows.value = updatedFlows
  }
  showDelayModal.value = false
  editingDelayIndex.value = -1
}

const cancelDelayEdit = () => {
  showDelayModal.value = false
  editingDelayIndex.value = -1
  currentEditingDelay.value = ''
}

const editFlow = (index) => {
  expandedFlow.value = index
  hoveredFlow.value = -1
}

const cancelEdit = () => {
  expandedFlow.value = -1
}

const saveFlowContent = () => {
  expandedFlow.value = -1
}
</script>
