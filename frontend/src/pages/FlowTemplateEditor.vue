<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b border-gray-200 sticky top-0 z-10">
      <div class="max-w-full mx-5 px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Left: Back button and Title -->
          <div class="flex items-center space-x-4">
            <Button
              variant="ghost"
              @click="handleBack"
            >
              <template #prefix>
                <FeatherIcon name="arrow-left" class="h-4 w-4" />
              </template>
              {{ __('Back') }}
            </Button>
            
            <div class="h-8 w-px bg-gray-300"></div>
            
            <div>
              <h1 class="text-xl font-semibold text-gray-900">
                {{ isEditMode ? __('Edit Flow Template') : __('Create Flow Template') }}
              </h1>
              <p class="text-sm text-gray-500">
                {{ isEditMode ? templateData.name_template : __('Create a new flow template') }}
              </p>
            </div>
          </div>

          <!-- Right: Actions -->
          <div class="flex items-center space-x-3">
            <!-- Use Template button (only in edit mode) -->
            <Button
              v-if="isEditMode"
              variant="outline"
              @click="handleUseTemplate"
              :loading="usingTemplate"
            >
              <template #prefix>
                <FeatherIcon name="play" class="h-4 w-4" />
              </template>
              {{ __('Use Template') }}
            </Button>
            
            <!-- Save/Update button -->
            <Button
              theme="blue"
              :loading="saving"
              @click="handleSave"
            >
              <template #prefix>
                <FeatherIcon name="save" class="h-4 w-4" />
              </template>
              {{ isEditMode ? __('Update Template') : __('Create Template') }}
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column: Form -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Basic Information -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h2 class="text-lg font-semibold text-gray-900 mb-4">
              {{ __('Basic Information') }}
            </h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('Template Name') }} <span class="text-red-500">*</span>
                </label>
                <FormControl
                  v-model="templateData.name_template"
                  type="text"
                  :placeholder="__('Enter template name...')"
                />
                <p v-if="errors.name_template" class="text-xs text-red-500 mt-1">
                  {{ errors.name_template }}
                </p>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('Alias') }}
                </label>
                <FormControl
                  v-model="templateData.alias"
                  type="text"
                  :placeholder="__('URL-friendly identifier')"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  {{ __('Description') }}
                </label>
                <textarea
                  v-model="templateData.description"
                  rows="3"
                  :placeholder="__('Describe this template...')"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ __('Type') }} <span class="text-red-500">*</span>
                  </label>
                  <Select
                    v-model="templateData.type"
                    :options="typeOptions"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ __('Scope') }} <span class="text-red-500">*</span>
                  </label>
                  <Select
                    v-model="templateData.scope_type"
                    :options="scopeOptions"
                  />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ __('Channel') }} <span class="text-red-500">*</span>
                  </label>
                  <Select
                    v-model="templateData.channel"
                    :options="channelOptions"
                  />
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">
                    {{ __('Target Type') }}
                  </label>
                  <Select
                    v-model="templateData.target_type"
                    :options="targetTypeOptions"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Triggers Section -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">
                {{ __('Triggers') }}
              </h2>
              <Button
                variant="outline"
                size="sm"
                @click="showAddTrigger = true"
              >
                <template #prefix>
                  <FeatherIcon name="plus" class="h-4 w-4" />
                </template>
                {{ __('Add Trigger') }}
              </Button>
            </div>

            <div v-if="triggers.length > 0" class="space-y-3">
              <div
                v-for="(trigger, index) in triggers"
                :key="`trigger-${index}`"
                class="group relative p-4 border border-gray-200 rounded-lg hover:border-blue-300 transition-colors"
              >
                <!-- Action Buttons -->
                <div class="absolute top-3 right-3 flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    @click="editTrigger(index)"
                    class="w-8 h-8 bg-green-500 text-white rounded-full hover:bg-green-600 flex items-center justify-center"
                    title="Edit"
                  >
                    <FeatherIcon name="edit-2" class="h-4 w-4" />
                  </button>
                  <button
                    @click="removeTrigger(index)"
                    class="w-8 h-8 bg-red-500 text-white rounded-full hover:bg-red-600 flex items-center justify-center"
                    title="Delete"
                  >
                    <FeatherIcon name="trash-2" class="h-4 w-4" />
                  </button>
                </div>
                
                <div class="flex items-start space-x-3">
                  <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <FeatherIcon name="zap" class="h-5 w-5 text-blue-600" />
                  </div>
                  <div class="flex-1 pr-20">
                    <h4 class="text-sm font-medium text-gray-900">{{ trigger.trigger_name }}</h4>
                    <p class="text-xs text-gray-500 mt-1">{{ trigger.description }}</p>
                    
                    <!-- Config Summary -->
                    <div v-if="trigger.configuration_json" class="mt-2 p-2 bg-blue-50 rounded text-xs">
                      <div class="text-gray-700">
                        <span class="font-medium">Config:</span>
                        {{ getTriggerConfigSummary(trigger.configuration_json) }}
                      </div>
                    </div>
                    
                    <div class="flex items-center space-x-4 mt-2 text-xs text-gray-400">
                      <span>{{ trigger.trigger_type }}</span>
                      <span v-if="trigger.status">• {{ trigger.status }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-8 text-gray-500">
              <FeatherIcon name="zap" class="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p class="text-sm">{{ __('No triggers added yet') }}</p>
              <p class="text-xs mt-1">{{ __('Click "Add Trigger" to get started') }}</p>
            </div>
          </div>

          <!-- Actions Section -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-gray-900">
                {{ __('Actions') }}
              </h2>
              <Button
                variant="outline"
                size="sm"
                @click="showAddAction = true"
              >
                <template #prefix>
                  <FeatherIcon name="plus" class="h-4 w-4" />
                </template>
                {{ __('Add Action') }}
              </Button>
            </div>

            <div v-if="actions.length > 0" class="space-y-3">
              <div
                v-for="(action, index) in actions"
                :key="`action-${index}`"
                class="group relative p-4 border border-gray-200 rounded-lg hover:border-purple-300 transition-colors"
              >
                <!-- Action Buttons -->
                <div class="absolute top-3 right-3 flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    @click="viewAction(index)"
                    class="w-8 h-8 bg-blue-500 text-white rounded-full hover:bg-blue-600 flex items-center justify-center"
                    title="View"
                  >
                    <FeatherIcon name="eye" class="h-4 w-4" />
                  </button>
                  <button
                    @click="editAction(index)"
                    class="w-8 h-8 bg-green-500 text-white rounded-full hover:bg-green-600 flex items-center justify-center"
                    title="Edit"
                  >
                    <FeatherIcon name="edit-2" class="h-4 w-4" />
                  </button>
                  <button
                    @click="removeAction(index)"
                    class="w-8 h-8 bg-red-500 text-white rounded-full hover:bg-red-600 flex items-center justify-center"
                    title="Delete"
                  >
                    <FeatherIcon name="trash-2" class="h-4 w-4" />
                  </button>
                </div>
                
                <div class="flex items-start space-x-3">
                  <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <FeatherIcon name="send" class="h-5 w-5 text-purple-600" />
                  </div>
                  <div class="flex-1 pr-24">
                    <h4 class="text-sm font-medium text-gray-900">{{ action.action_name }}</h4>
                    <p class="text-xs text-gray-500 mt-1">{{ action.action_type }}</p>
                    <div class="flex items-center space-x-4 mt-2 text-xs text-gray-400">
                      <span>{{ action.channel_type }}</span>
                      <span v-if="action.status">• {{ action.status }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-8 text-gray-500">
              <FeatherIcon name="send" class="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p class="text-sm">{{ __('No actions added yet') }}</p>
              <p class="text-xs mt-1">{{ __('Click "Add Action" to get started') }}</p>
            </div>
          </div>
        </div>

        <!-- Right Column: Settings & Preview -->
        <div class="space-y-6">
          <!-- Thumbnail -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-900 mb-4">
              {{ __('Thumbnail') }}
            </h3>
            
            <div v-if="templateData.thumbnail" class="mb-3">
              <img
                :src="templateData.thumbnail"
                alt="Thumbnail"
                class="w-full h-32 object-cover rounded-lg border border-gray-200"
              />
              <Button
                variant="outline"
                theme="red"
                size="sm"
                class="mt-2 w-full"
                @click="templateData.thumbnail = ''"
              >
                <template #prefix>
                  <FeatherIcon name="trash-2" class="w-3 h-3" />
                </template>
                {{ __('Remove') }}
              </Button>
            </div>

            <FileUploader
              v-else
              :fileTypes="['image/*']"
              :validateFile="validateThumbnailFile"
              @success="handleFileUploadSuccess"
            >
              <template #default="{ openFileSelector, uploading, progress }">
                <div 
                  @click="openFileSelector()"
                  class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors cursor-pointer"
                >
                  <div v-if="uploading">
                    <FeatherIcon name="loader" class="w-6 h-6 mx-auto text-blue-500 animate-spin mb-2" />
                    <p class="text-xs text-gray-600">{{ __('Uploading...') }} {{ progress }}%</p>
                  </div>
                  <div v-else>
                    <FeatherIcon name="image" class="w-8 h-8 mx-auto text-gray-400 mb-2" />
                    <p class="text-xs text-gray-700 font-medium">
                      {{ __('Upload thumbnail') }}
                    </p>
                    <p class="text-xs text-gray-400 mt-1">
                      {{ __('PNG, JPG (max 5MB)') }}
                    </p>
                  </div>
                </div>
              </template>
            </FileUploader>
          </div>

          <!-- Settings -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-900 mb-4">
              {{ __('Settings') }}
            </h3>
            <div class="space-y-3">
              <label class="flex items-center">
                <Checkbox
                  size="sm"
                  :value="false"
                  v-model="templateData.is_default"
                 
                />
                
                <span class="ml-2 text-sm text-gray-700">{{ __('Default Template') }}</span>
              </label>

              <label class="flex items-center">
                <Checkbox
                  size="sm"
                  :value="false"
                  v-model="templateData.is_premium"
                 
                />
                <span class="ml-2 text-sm text-gray-700">{{ __('Premium') }}</span>
              </label>

              <label class="flex items-center">
                <Checkbox
                  size="sm"
                  :value="false"
                  v-model="templateData.is_suggestion"
                   
                />
                <span class="ml-2 text-sm text-gray-700">{{ __('Show as Suggestion') }}</span>
              </label>
            </div>
          </div>

          <!-- Statistics (Edit mode only) -->
          <div v-if="isEditMode" class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 class="text-sm font-semibold text-gray-900 mb-4">
              {{ __('Statistics') }}
            </h3>
            
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __('Usage Count') }}</span>
                <span class="font-medium">{{ templateData.usage_count || 0 }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ __('Flows Created') }}</span>
                <span class="font-medium">{{ templateData.flow_total || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Trigger Modal -->
    <Dialog 
      v-model="isAddTriggerOpen" 
      :options="{ 
        title: editingTriggerIndex !== null ? __('Edit Trigger') : __('Add Trigger'), 
        size: showTriggerConfig ? '3xl' : 'md' 
      }"
    >
      <template #body-content>
        <!-- Step 1: Select Trigger Type -->
        <div v-if="!showTriggerConfig" class="space-y-4" @click.stop>
          <FormControl
            v-model="triggerSearch"
            type="text"
            :placeholder="__('Search trigger')"
          />
          
          <div class="max-h-96 overflow-y-auto space-y-2">
            <div
              v-for="trigger in filteredTriggerOptions"
              :key="trigger.id"
              class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
              @click.stop="selectTriggerType(trigger)"
            >
              <h4 class="text-sm font-medium text-gray-900">{{ trigger.name }}</h4>
              <p class="text-xs text-gray-500">{{ trigger.description }}</p>
            </div>
          </div>
        </div>

        <!-- Step 2: Configure Trigger -->
        <div v-else class="space-y-4" @click.stop>
          <TriggerEditor
            :content="currentTriggerConfig"
            @update:content="updateTriggerConfig"
            :readonly="false"
          />
        </div>
      </template>

      <template #actions v-if="showTriggerConfig">
        <div class="flex justify-end space-x-3">
          <Button
            variant="outline"
            @click="cancelTriggerConfig"
          >
            {{ __('Back') }}
          </Button>
          <Button
            theme="blue"
            @click="saveTrigger"
          >
            {{ __('Save Trigger') }}
          </Button>
        </div>
      </template>
    </Dialog>

    <!-- ✅ Action Picker Dialog -->
    <Dialog
      v-model="showAddAction"
      :options="{ title: __('Add Action'), size: 'lg' }"
    >
      <template #body-content>
        <div class="space-y-4">
          <!-- Search -->
          <div class="relative">
            <input
              v-model="actionSearch"
              type="text"
              :placeholder="__('Search actions...')"
              class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
            />
            <FeatherIcon name="search" class="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
          </div>

          <!-- Action List -->
          <div class="grid grid-cols-1 gap-3 max-h-96 overflow-y-auto">
            <div
              v-for="action in filteredActionOptions"
              :key="action.value"
              class="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
              @click="handleSelectAction(action)"
            >
              <h4 class="text-sm font-medium text-gray-900">{{ action.label }}</h4>
              <p class="text-xs text-gray-500 mt-1">{{ action.description }}</p>
            </div>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Edit/View Action Modal -->
    <Dialog 
      v-model="isEditActionOpen" 
      :options="{ 
        title: isViewMode ? __('View Action') : (editingActionIndex !== null ? __('Edit Action') : __('Add Action')), 
        size: '3xl' 
      }"
    >
      <template #body-content>
        <div class="space-y-6" @click.stop>
          <!-- Email Editor -->
          <div v-if="selectedActionType?.action_type === 'EMAIL'">
            <EmailEditor
              :content="currentActionContent"
              @update:content="updateActionContent"
              :readonly="isViewMode"
            />
          </div>

          <!-- SMS Editor -->
          <div v-else-if="selectedActionType?.action_type === 'SMS'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">SMS Content</label>
              <textarea
                v-model="currentActionContent.message"
                rows="4"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                :readonly="isViewMode"
                placeholder="Enter SMS message..."
              />
            </div>
          </div>

          <!-- Zalo Editor -->
          <div v-else-if="selectedActionType?.action_type === 'ZALO'">
            <ZaloEditor
              :content="currentActionContent"
              @update:content="updateActionContent"
              :readonly="isViewMode"
            />
          </div>

          <!-- Add Tag -->
          <div v-else-if="selectedActionType?.action_type === 'ADD_TAG'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tag Name</label>
              <input
                v-model="currentActionContent.tag_name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                :readonly="isViewMode"
                placeholder="Enter tag name..."
              />
            </div>
          </div>

          <!-- Remove Tag -->
          <div v-else-if="selectedActionType?.action_type === 'REMOVE_TAG'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tag Name</label>
              <input
                v-model="currentActionContent.tag_name"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                :readonly="isViewMode"
                placeholder="Enter tag name to remove..."
              />
            </div>
          </div>

          <!-- Smart Delay -->
          <div v-else-if="selectedActionType?.action_type === 'SMART_DELAY'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Duration</label>
              <input
                v-model="currentActionContent.duration"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                :readonly="isViewMode"
                placeholder="e.g., 1 day, 2 hours..."
              />
            </div>
          </div>

          <!-- Add Custom Field -->
          <div v-else-if="selectedActionType?.action_type === 'ADD_CUSTOM_FIELD'">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Field Name</label>
                <input
                  v-model="currentActionContent.field_name"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  :readonly="isViewMode"
                  placeholder="Enter field name..."
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Field Value</label>
                <input
                  v-model="currentActionContent.field_value"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  :readonly="isViewMode"
                  placeholder="Enter field value..."
                />
              </div>
            </div>
          </div>

          <!-- Start Flow -->
          <div v-else-if="selectedActionType?.action_type === 'START_FLOW'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Flow ID</label>
              <input
                v-model="currentActionContent.flow_id"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                :readonly="isViewMode"
                placeholder="Enter flow ID..."
              />
            </div>
          </div>

          <!-- Subscribe to Sequence -->
          <div v-else-if="selectedActionType?.action_type === 'SUBSCRIBE_TO_SEQUENCE'">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Sequence ID</label>
              <input
                v-model="currentActionContent.sequence_id"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                :readonly="isViewMode"
                placeholder="Enter sequence ID..."
              />
            </div>
          </div>

          <!-- Additional Actions (only for messaging actions) -->
          <div v-if="!isViewMode && ['EMAIL', 'SMS', 'ZALO'].includes(selectedActionType?.action_type)">
            <AdditionalActions
              :interaction-type="getInteractionType()"
              :model-value="currentAdditionalActions"
              @update:model-value="updateAdditionalActions"
            />
          </div>
        </div>
      </template>
      
      <template #actions>
        <div class="flex justify-end space-x-3">
          <Button
            variant="outline"
            @click="isEditActionOpen = false"
          >
            {{ isViewMode ? __('Close') : __('Cancel') }}
          </Button>
          <Button
            v-if="!isViewMode"
            theme="blue"
            @click="saveAction"
          >
            {{ __('Save Action') }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, FormControl, Select, Dialog, FeatherIcon, FileUploader, Checkbox } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { useFlowTemplateStore } from '@/stores/flowTemplate'
import EmailEditor from '@/components/campaign/content-editors/EmailEditor.vue'
import ZaloEditor from '@/components/campaign/content-editors/ZaloEditor.vue'
import TriggerEditor from '@/components/campaign/content-editors/TriggerEditor.vue'
import AdditionalActions from '@/components/campaign/AdditionalActions.vue'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const templateStore = useFlowTemplateStore()

// State
const saving = ref(false)
const usingTemplate = ref(false)
const errors = ref({})
const showAddTrigger = ref(false)
const showAddAction = ref(false)  // ✅ Action picker dialog
const showEditAction = ref(false)
const triggerSearch = ref('')
const actionSearch = ref('')  // ✅ Search for actions
const editingActionIndex = ref(null)
const editingTriggerIndex = ref(null)
const currentActionContent = ref(null)
const currentAdditionalActions = ref({})  // Object, not Array
const currentTriggerConfig = ref(null)
const showTriggerConfig = ref(false)
const selectedTriggerType = ref(null)
const selectedActionType = ref(null)  // ✅ Selected action type
const isViewMode = ref(false)

const templateData = ref({
  name_template: '',
  alias: '',
  description: '',
  thumbnail: '',
  type: 'FLOW',
  order_no: 999,
  is_default: false,
  is_premium: false,
  is_suggestion: false,
  scope_type: 'PRIVATE',
  channel: '',
  target_type: '',
  flow_parent_id: '',
  usage_count: 0,
  flow_total: 0
})

const triggers = ref([])
const actions = ref([])

// Computed
const isEditMode = computed(() => !!route.params.id)

const isAddTriggerOpen = computed({
  get: () => showAddTrigger.value,
  set: (value) => {
    showAddTrigger.value = value
  }
})

const isEditActionOpen = computed({
  get: () => showEditAction.value,
  set: (value) => {
    showEditAction.value = value
  }
})

// Options
const typeOptions = [
  { label: 'Flow', value: 'FLOW' },
  { label: 'Sequence', value: 'SEQUENCE' },
  { label: 'Campaign', value: 'CAMPAIGN' }
]

const scopeOptions = [
  { label: 'Private', value: 'PRIVATE' },
  { label: 'Team', value: 'TEAM' },
  { label: 'Organization', value: 'ORGANIZATION' },
  { label: 'Public', value: 'PUBLIC' }
]

const channelOptions = [
  { label: 'Email', value: 'Email' },
  { label: 'SMS', value: 'SMS' },
  { label: 'Zalo', value: 'Zalo' },
  { label: 'Messenger', value: 'Messenger' }
]

const targetTypeOptions = [
  { label: 'Talent', value: 'Talent' },
  { label: 'Talent Pool', value: 'Talent Pool' },
  { label: 'Applicant', value: 'Applicant' }
]

const availableTriggers = [
  {
    id: 'on_create',
    name: 'On Create',
    description: 'Trigger when creating a new record',
    icon: 'plus-circle',
    event_type: 'ON_CREATE'
  },
  {
    id: 'on_update',
    name: 'On Update',
    description: 'Trigger when updating a record',
    icon: 'edit',
    event_type: 'ON_UPDATE'
  },
  {
    id: 'on_tag_added',
    name: 'On Tag Added',
    description: 'Trigger when a tag is added',
    icon: 'tag',
    event_type: 'ON_TAG_ADDED'
  },
  {
    id: 'on_status_changed',
    name: 'On Status Changed',
    description: 'Trigger when status changes',
    icon: 'refresh-cw',
    event_type: 'ON_STATUS_CHANGED'
  },
  {
    id: 'on_sequence_completed',
    name: 'On Sequence Completed',
    description: 'Trigger when sequence completes',
    icon: 'check-circle',
    event_type: 'ON_SEQUENCE_COMPLETED'
  },
  {
    id: 'on_scheduled_time',
    name: 'On Scheduled Time',
    description: 'Trigger at scheduled time',
    icon: 'clock',
    event_type: 'ON_SCHEDULED_TIME'
  }
]

// ✅ Available actions list (copied from FlowEditor)
const availableActions = [
  {
    label: 'Send Email',
    value: 'send_email',
    description: 'Send email to customer',
    action_type: 'EMAIL',
    parameters: {
      channel: 'Email',
      template_id: '',
      email_content: {
        email_subject: '',
        email_content: '',
        attachments: [],
      },
    },
  },
  {
    label: 'Send SMS',
    value: 'send_sms',
    description: 'Send SMS to customer',
    action_type: 'SMS',
    parameters: {
      channel: 'SMS',
      template_id: '',
      sms_content: {
        message: '',
      },
    },
  },
  {
    label: 'Send Zalo',
    value: 'send_zalo',
    description: 'Send Zalo message to customer',
    action_type: 'ZALO',
    parameters: {
      channel: 'Zalo',
      template_id: '',
      zalo_content: {
        blocks: [
          {
            id: 1,
            type: 'text',
            text_content: '',
          },
        ],
      },
    },
  },
  {
    label: 'Smart Delay',
    value: 'smart_delay',
    description: 'Wait for a certain amount of time before the next action',
    action_type: 'SMART_DELAY',
    parameters: { duration: '1 day' },
  },
  {
    label: 'Add Tag',
    value: 'add_tag',
    description: 'Add tag to customer',
    action_type: 'ADD_TAG',
    parameters: { tag_name: '' },
  },
  {
    label: 'Remove Tag',
    value: 'remove_tag',
    description: 'Remove tag from customer',
    action_type: 'REMOVE_TAG',
    parameters: { tag_name: '' },
  },
  {
    label: 'Add Custom Field',
    value: 'add_custom_field',
    description: 'Add custom field to customer',
    action_type: 'ADD_CUSTOM_FIELD',
    parameters: { field_name: '', field_value: '' },
  },
  {
    label: 'Start Flow',
    value: 'start_flow',
    description: 'Start another flow',
    action_type: 'START_FLOW',
    parameters: { flow_id: '' },
  },
  {
    label: 'Subscribe to Sequence',
    value: 'subscribe_to_sequence',
    description: 'Subscribe customer to sequence',
    action_type: 'SUBSCRIBE_TO_SEQUENCE',
    parameters: { sequence_id: '' },
  },
]

const filteredTriggerOptions = computed(() => {
  if (!triggerSearch.value) return availableTriggers
  return availableTriggers.filter(trigger =>
    trigger.name.toLowerCase().includes(triggerSearch.value.toLowerCase()) ||
    trigger.description.toLowerCase().includes(triggerSearch.value.toLowerCase())
  )
})

const filteredActionOptions = computed(() => {
  if (!actionSearch.value) return availableActions
  return availableActions.filter(action =>
    action.label.toLowerCase().includes(actionSearch.value.toLowerCase()) ||
    action.description.toLowerCase().includes(actionSearch.value.toLowerCase())
  )
})

// Methods
const handleBack = () => {
  router.push('/flow-templates')
}

const handleUseTemplate = async () => {
  try {
    usingTemplate.value = true
    
    // Call store action to create flow from template
    const result = await templateStore.useTemplate(
      templateData.value.name,
      `${templateData.value.name_template} - ${new Date().toLocaleString()}`
    )
    
    if (result.success) {
      toast.success(result.message || __('Flow created successfully from template!'))
      
      // Navigate to flow editor
      router.push(`/flows/${result.flow_name}/edit`)
    } else {
      toast.error(result.error || __('Failed to create flow from template'))
    }
  } catch (error) {
    console.error('Error using template:', error)
    toast.error(__('An error occurred while creating flow'))
  } finally {
    usingTemplate.value = false
  }
}

const validateForm = () => {
  errors.value = {}
  
  if (!templateData.value.name_template?.trim()) {
    errors.value.name_template = 'Template name is required'
  }
  
  if (!templateData.value.type) {
    errors.value.type = 'Type is required'
  }
  
  if (!templateData.value.channel) {
    errors.value.channel = 'Channel is required'
  }
  
  return Object.keys(errors.value).length === 0
}

const handleSave = async () => {
  if (!validateForm()) {
    toast.error('Please fill in all required fields')
    return
  }
  
  saving.value = true
  
  try {
    const submitData = {
      ...templateData.value,
      is_default: templateData.value.is_default ? 1 : 0,
      is_premium: templateData.value.is_premium ? 1 : 0,
      is_suggestion: templateData.value.is_suggestion ? 1 : 0,
      template_triggers: triggers.value,
      template_actions: actions.value
    }
    
    let result
    if (isEditMode.value) {
      result = await templateStore.updateTemplate(route.params.id, submitData)
    } else {
      result = await templateStore.createTemplate(submitData)
    }
    
    if (result.success) {
      toast.success(isEditMode.value ? 'Template updated successfully' : 'Template created successfully')
      
      // Reload template data to get fresh modified timestamp
      if (isEditMode.value) {
        const reloadResult = await templateStore.fetchTemplateById(route.params.id)
        if (reloadResult.success && reloadResult.data) {
          Object.assign(templateData.value, reloadResult.data)
          
          // Reload triggers
          if (reloadResult.data.template_triggers) {
            triggers.value = reloadResult.data.template_triggers.map(t => ({
              ...t,
              icon: getTriggerIcon(t.trigger_type)
            }))
          }
          
          // Reload actions
          if (reloadResult.data.template_actions) {
            actions.value = reloadResult.data.template_actions
          }
        }
      }
    } else {
      toast.error(result.error || 'Failed to save template')
    }
  } catch (error) {
    console.error('Error saving template:', error)
    toast.error('An error occurred while saving')
  } finally {
    saving.value = false
  }
}

const selectTriggerType = (trigger) => {
  selectedTriggerType.value = trigger
  
  // Initialize trigger config
  currentTriggerConfig.value = {
    name: trigger.name,
    description: trigger.description,
    trigger_type: trigger.event_type,
    connected_account: '',
    sequence_id: '',
    channels: [],
    Conditional_Split: []
  }
  
  showTriggerConfig.value = true
}

const updateTriggerConfig = (newConfig) => {
  console.log('🔄 Updating trigger config:', newConfig)
  if (JSON.stringify(currentTriggerConfig.value) !== JSON.stringify(newConfig)) {
    currentTriggerConfig.value = { ...newConfig }
  }
}

const saveTrigger = () => {
  console.log('💾 Saving trigger with config:', currentTriggerConfig.value)
  
  const triggerData = {
    trigger_name: selectedTriggerType.value.name,
    trigger_type: selectedTriggerType.value.event_type,
    target_type: templateData.value.target_type,
    channel: templateData.value.channel,
    description: selectedTriggerType.value.description,
    icon: selectedTriggerType.value.icon,
    configuration_json: JSON.stringify(currentTriggerConfig.value),
    status: 'ACTIVE',
    order: editingTriggerIndex.value !== null ? triggers.value[editingTriggerIndex.value].order : triggers.value.length,
    is_default: triggers.value.length === 0 ? 1 : 0
  }
  
  console.log('📦 Trigger data to save:', triggerData)
  
  if (editingTriggerIndex.value !== null) {
    triggers.value[editingTriggerIndex.value] = triggerData
  } else {
    triggers.value.push(triggerData)
  }
  
  // Reset state
  isAddTriggerOpen.value = false
  showTriggerConfig.value = false
  selectedTriggerType.value = null
  currentTriggerConfig.value = null
  editingTriggerIndex.value = null
  triggerSearch.value = ''
}

const cancelTriggerConfig = () => {
  showTriggerConfig.value = false
  selectedTriggerType.value = null
  currentTriggerConfig.value = null
}

const editTrigger = (index) => {
  editingTriggerIndex.value = index
  const trigger = triggers.value[index]
  
  // Parse trigger config
  try {
    const config = trigger.configuration_json ? JSON.parse(trigger.configuration_json) : {}
    currentTriggerConfig.value = {
      name: trigger.trigger_name,
      description: trigger.description,
      trigger_type: trigger.trigger_type,
      connected_account: config.connected_account || '',
      sequence_id: config.sequence_id || '',
      channels: config.channels || [],
      Conditional_Split: config.Conditional_Split || []
    }
  } catch (e) {
    console.error('Error parsing trigger config:', e)
    currentTriggerConfig.value = {
      name: trigger.trigger_name,
      description: trigger.description,
      trigger_type: trigger.trigger_type,
      connected_account: '',
      sequence_id: '',
      channels: [],
      Conditional_Split: []
    }
  }
  
  // Find trigger type from options
  selectedTriggerType.value = availableTriggers.find(t => t.event_type === trigger.trigger_type) || {
    name: trigger.trigger_name,
    event_type: trigger.trigger_type,
    description: trigger.description
  }
  
  showTriggerConfig.value = true
  isAddTriggerOpen.value = true
}

const removeTrigger = (index) => {
  triggers.value.splice(index, 1)
}

const getTriggerConfigSummary = (configJson) => {
  if (!configJson) return 'No config'
  
  try {
    const config = JSON.parse(configJson)
    const parts = []
    
    if (config.channels && config.channels.length > 0) {
      parts.push(`Channels: ${config.channels.join(', ')}`)
    }
    
    if (config.sequence_id) {
      parts.push(`Sequence: ${config.sequence_id}`)
    }
    
    if (config.Conditional_Split && config.Conditional_Split.length > 0) {
      parts.push(`${config.Conditional_Split.length} condition(s)`)
    }
    
    return parts.length > 0 ? parts.join(' • ') : 'No conditions'
  } catch (e) {
    console.error('Error parsing config:', e)
    return 'Invalid config'
  }
}

// ✅ Handle selecting action from picker
const handleSelectAction = (actionOption) => {
  console.log('Selected action:', actionOption)
  
  selectedActionType.value = actionOption
  editingActionIndex.value = null
  isViewMode.value = false
  
  // Initialize content based on action type
  if (actionOption.action_type === 'EMAIL') {
    currentActionContent.value = {
      email_subject: '',
      email_content: '',
      attachments: []
    }
  } else if (actionOption.action_type === 'SMS') {
    currentActionContent.value = {
      message: ''
    }
  } else if (actionOption.action_type === 'ZALO') {
    currentActionContent.value = {
      blocks: [{
        id: Date.now(),
        type: 'text',
        text_content: ''
      }]
    }
  } else if (actionOption.action_type === 'ADD_TAG') {
    currentActionContent.value = {
      tag_name: ''
    }
  } else if (actionOption.action_type === 'REMOVE_TAG') {
    currentActionContent.value = {
      tag_name: ''
    }
  } else if (actionOption.action_type === 'SMART_DELAY') {
    currentActionContent.value = {
      duration: '1 day'
    }
  } else if (actionOption.action_type === 'ADD_CUSTOM_FIELD') {
    currentActionContent.value = {
      field_name: '',
      field_value: ''
    }
  } else if (actionOption.action_type === 'START_FLOW') {
    currentActionContent.value = {
      flow_id: ''
    }
  } else if (actionOption.action_type === 'SUBSCRIBE_TO_SEQUENCE') {
    currentActionContent.value = {
      sequence_id: ''
    }
  } else {
    currentActionContent.value = {}
  }
  
  // Initialize additional actions as empty object
  currentAdditionalActions.value = {}
  
  // Close picker, open editor
  showAddAction.value = false
  isEditActionOpen.value = true
}

const viewAction = (index) => {
  editingActionIndex.value = index
  isViewMode.value = true
  const action = actions.value[index]
  
  // ✅ Set selectedActionType based on action_type
  selectedActionType.value = availableActions.find(a => a.action_type === action.action_type) || null
  
  try {
    const params = JSON.parse(action.action_parameters)
    
    // Load content based on action type
    if (action.action_type === 'EMAIL') {
      currentActionContent.value = params.email_content || params
    } else if (action.action_type === 'SMS') {
      currentActionContent.value = params.sms_content || params
    } else if (action.action_type === 'ZALO') {
      currentActionContent.value = params.zalo_content || params
    } else {
      currentActionContent.value = params
    }
    
    // Load additional_actions - support both Object and Array formats
    const additionalActionsData = params.additional_actions || {}
    
    if (typeof additionalActionsData === 'object' && !Array.isArray(additionalActionsData)) {
      // Already in Object format: {email_open: {...}, link_click: {...}}
      currentAdditionalActions.value = additionalActionsData
    } else if (Array.isArray(additionalActionsData)) {
      // Legacy Array format: [{trigger: 'email_open', ...}] - convert to Object
      const additionalActionsObject = {}
      additionalActionsData.forEach(action => {
        if (action.trigger) {
          additionalActionsObject[action.trigger] = {
            type: action.type || action.trigger,
            data: action.data || {},
            configured: action.configured || false
          }
        }
      })
      currentAdditionalActions.value = additionalActionsObject
    } else {
      currentAdditionalActions.value = {}
    }
  } catch (e) {
    console.error('Error parsing action parameters:', e)
    currentAdditionalActions.value = {}
  }
  
  isEditActionOpen.value = true
}

const editAction = (index) => {
  editingActionIndex.value = index
  isViewMode.value = false
  const action = actions.value[index]
  
  // ✅ Set selectedActionType based on action_type
  selectedActionType.value = availableActions.find(a => a.action_type === action.action_type) || null
  
  try {
    const params = JSON.parse(action.action_parameters)
    
    // Load content based on action type
    if (action.action_type === 'EMAIL') {
      currentActionContent.value = params.email_content || params
    } else if (action.action_type === 'SMS') {
      currentActionContent.value = params.sms_content || params
    } else if (action.action_type === 'ZALO') {
      currentActionContent.value = params.zalo_content || params
    } else {
      currentActionContent.value = params
    }
    
    // Load additional_actions - support both Object and Array formats
    const additionalActionsData = params.additional_actions || {}
    
    if (typeof additionalActionsData === 'object' && !Array.isArray(additionalActionsData)) {
      // Already in Object format: {email_open: {...}, link_click: {...}}
      currentAdditionalActions.value = additionalActionsData
    } else if (Array.isArray(additionalActionsData)) {
      // Legacy Array format: [{trigger: 'email_open', ...}] - convert to Object
      const additionalActionsObject = {}
      additionalActionsData.forEach(action => {
        if (action.trigger) {
          additionalActionsObject[action.trigger] = {
            type: action.type || action.trigger,
            data: action.data || {},
            configured: action.configured || false
          }
        }
      })
      currentAdditionalActions.value = additionalActionsObject
    } else {
      currentAdditionalActions.value = {}
    }
    
    console.log('📖 Loading action for edit:', action)
    console.log('📖 Parsed params:', params)
    console.log('📖 Additional actions loaded:', currentAdditionalActions.value)
  } catch (e) {
    console.error('Error parsing action parameters:', e)
    currentAdditionalActions.value = {}
  }
  
  isEditActionOpen.value = true
}

const updateActionContent = (newContent) => {
  // Only update if content actually changed to prevent infinite loops
  if (JSON.stringify(currentActionContent.value) !== JSON.stringify(newContent)) {
    currentActionContent.value = { ...newContent }
  }
}

const updateAdditionalActions = (newActions) => {
  currentAdditionalActions.value = newActions
}

const getInteractionType = () => {
  if (selectedActionType.value?.action_type === 'EMAIL') return 'EMAIL'
  if (selectedActionType.value?.action_type === 'ZALO') return 'ZALO_CARE'
  if (selectedActionType.value?.action_type === 'SMS') return 'SMS'
  return 'EMAIL'
}

const saveAction = () => {
  console.log('💾 Saving action...')
  console.log('Selected action type:', selectedActionType.value)
  console.log('Current content:', currentActionContent.value)
  console.log('Additional actions:', currentAdditionalActions.value)
  
  if (!selectedActionType.value) {
    toast.error('No action type selected')
    return
  }
  
  // Build parameters object that matches FlowEditor structure
  const parameters = { ...currentActionContent.value }
  
  // Add channel for messaging actions
  if (['EMAIL', 'SMS', 'ZALO'].includes(selectedActionType.value.action_type)) {
    parameters.channel = selectedActionType.value.parameters.channel
    
    // Add content based on action type
    if (selectedActionType.value.action_type === 'EMAIL') {
      parameters.email_content = currentActionContent.value
    } else if (selectedActionType.value.action_type === 'ZALO') {
      parameters.zalo_content = currentActionContent.value
    } else if (selectedActionType.value.action_type === 'SMS') {
      parameters.sms_content = currentActionContent.value
    }
    
    // Add additional actions - keep as Object format (FlowEditor expects Object)
    if (currentAdditionalActions.value && Object.keys(currentAdditionalActions.value).length > 0) {
      parameters.additional_actions = JSON.parse(JSON.stringify(currentAdditionalActions.value))
      console.log('✅ Added additional_actions (Object format):', parameters.additional_actions)
    }
  }
  
  const actionData = {
    action_name: selectedActionType.value.label,
    action_type: selectedActionType.value.action_type,
    channel_type: selectedActionType.value.parameters?.channel || null,
    action_parameters: JSON.stringify(parameters),
    status: 'ACTIVE',
    order: editingActionIndex.value !== null ? actions.value[editingActionIndex.value].order : actions.value.length,
    is_default: actions.value.length === 0 ? 1 : 0
  }
  
  console.log('📦 Action data to save:', actionData)
  console.log('📦 Stringified params:', actionData.action_parameters)
  
  if (editingActionIndex.value !== null) {
    console.log('✏️ Updating action at index:', editingActionIndex.value)
    // ✅ Merge với existing action để giữ lại additional_actions
    const existingAction = actions.value[editingActionIndex.value]
    const mergedAction = {
      ...existingAction,
      ...actionData
    }
    // Use splice to ensure reactivity
    actions.value.splice(editingActionIndex.value, 1, mergedAction)
  } else {
    console.log('➕ Adding new action')
    actions.value.push(actionData)
  }
  
  console.log('✅ Actions array after save:', JSON.parse(JSON.stringify(actions.value)))
  
  isEditActionOpen.value = false
  editingActionIndex.value = null
  currentActionContent.value = null
  currentAdditionalActions.value = {}
}

const removeAction = (index) => {
  actions.value.splice(index, 1)
}

const validateThumbnailFile = (fileObject) => {
  const maxSize = 5 * 1024 * 1024
  if (fileObject.size > maxSize) {
    return 'File size must be less than 5MB'
  }
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
  if (!allowedTypes.includes(fileObject.type)) {
    return 'Only image files are allowed'
  }
  return null
}

const handleFileUploadSuccess = (file) => {
  if (file && file.file_url) {
    templateData.value.thumbnail = file.file_url
  }
}

// Load template data if editing
onMounted(async () => {
  if (isEditMode.value) {
    try {
      const result = await templateStore.fetchTemplateById(route.params.id)
      if (result.success && result.data) {
        Object.assign(templateData.value, result.data)
        
        // Load triggers
        if (result.data.template_triggers) {
          triggers.value = result.data.template_triggers.map(t => ({
            ...t,
            icon: getTriggerIcon(t.trigger_type)
          }))
        }
        
        // Load actions
        if (result.data.template_actions) {
          actions.value = result.data.template_actions
        }
      }
    } catch (error) {
      console.error('Error loading template:', error)
      toast.error('Failed to load template')
    }
  }
})

const getTriggerIcon = (triggerType) => {
  const iconMap = {
    'ON_CREATE': 'plus-circle',
    'ON_UPDATE': 'edit',
    'ON_TAG_ADDED': 'tag',
    'ON_STATUS_CHANGED': 'refresh-cw',
    'ON_SEQUENCE_COMPLETED': 'check-circle',
    'ON_SCHEDULED_TIME': 'clock'
  }
  return iconMap[triggerType] || 'zap'
}
</script>
