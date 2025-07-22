<template>
  <div v-if="show" class="fixed z-50 inset-0 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="handleClose"></div>
      
      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
      
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <form @submit.prevent="handleSubmit">
          <!-- Header -->
          <div class="bg-white pt-5 pb-4 sm:py-6 sm:pb-4">
            <div class="flex items-center justify-between">
              <h3 class="text-lg px-5 leading-6 font-medium text-gray-900">
                {{ isEdit ? __('Edit Campaign Template') : __('Create Campaign Template') }}
              </h3>
              <Button
                variant="ghost"
                size="sm"
                @click="handleClose"
                class="px-6"
              >
                <template #icon>
                  <FeatherIcon name="x" class="w-6 h-6" />
                </template>
              </Button>
            </div>
            
            <!-- Tabs -->
            <div class="mt-4" v-if="tabs.length > 0">
              <Tabs
                v-model="activeTabIndex"
                :tabs="tabs"
              />
            </div>
          </div>

          <!-- Form Content -->
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 max-h-[70vh] overflow-y-auto">
            <!-- Template Info Tab -->
            <div v-if="activeTab === 'template'" class="grid grid-cols-1 gap-6">
              <!-- Template Name -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Template Name') }}
                  <span class="text-red-500">*</span>
                </label>
                <TextInput
                  v-model="formData.template_name"
                  type="text"
                  :placeholder="__('Enter template name...')"
                  :disabled="loading"
                  class="w-full"
                />
                <div v-if="errors.template_name" class="mt-1 text-sm text-red-600">
                  {{ errors.template_name }}
                </div>
              </div>

              <!-- Campaign Type -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Campaign Type') }}
                  <span class="text-red-500">*</span>
                </label>
                <FormControl
                  type="select"
                  v-model="formData.campaign_type"
                  :options="campaignTypeOptions"
                  :disabled="loading"
                  class="w-full"
                />
                <div v-if="errors.campaign_type" class="mt-1 text-sm text-red-600">
                  {{ errors.campaign_type }}
                </div>
              </div>

              <!-- Description -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Description') }}
                </label>
                <textarea
                  v-model="formData.description"
                  rows="3"
                  :placeholder="__('Enter template description...')"
                  :disabled="loading"
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                />
                <div v-if="errors.description" class="mt-1 text-sm text-red-600">
                  {{ errors.description }}
                </div>
              </div>

              <!-- Is Active -->
              <div class="flex items-center">
                <input
                  v-model="formData.is_active"
                  type="checkbox"
                  :disabled="loading"
                  class="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                />
                <label class="ml-2 block text-sm text-gray-900">
                  {{ __('Active') }}
                </label>
              </div>
            </div>

            <!-- Steps Tab -->
            <div v-if="activeTab === 'steps'" class="space-y-4">
              <!-- Steps Header -->
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="text-lg font-medium text-gray-900">{{ __('Template Steps') }}</h3>
                  <p class="text-sm text-gray-500">{{ __('Define the steps for this campaign template') }}</p>
                </div>
                <Button
                  type="button"
                  variant="solid"
                  theme="gray"
                  @click.stop="handleAddStep"
                >
                  <template #prefix>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
                    </svg>
                  </template>
                  {{ __('Add Step') }}
                </Button>
              </div>

              <!-- Steps List -->
              <div v-if="stepsLoading" class="flex justify-center py-4">
                <div class="flex items-center text-gray-600">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ __('Loading steps...') }}
                </div>
              </div>

              <div v-else-if="templateSteps.length === 0" class="text-center py-6 bg-gray-50 rounded-lg">
                <div class="text-gray-400 mb-2">
                  <svg class="mx-auto h-8 w-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
                <p class="text-gray-500 text-sm">{{ __('No steps defined yet. Click "Add Step" to get started.') }}</p>
              </div>

              <div v-else class="space-y-2">
                <div
                  v-for="(step, index) in templateSteps"
                  :key="step.name"
                >
                  <!-- Normal Step Display -->
                  <div
                    v-if="!editingStep || editingStep.name !== step.name"
                    class="bg-gray-50 border border-gray-200 rounded-lg p-4 hover:bg-gray-100 transition-colors"
                  >
                    <div class="flex items-center justify-between">
                      <div class="flex-1">
                        <div class="flex items-center space-x-3">
                          <span class="flex items-center justify-center w-6 h-6 bg-indigo-100 text-indigo-800 text-xs font-medium rounded-full">
                            {{ step.step_order }}
                          </span>
                          <div>
                            <h4 class="text-sm font-medium text-gray-900">{{ step.campaign_step_name }}</h4>
                            <div class="flex items-center space-x-2 text-xs text-gray-500">
                              <span>{{ step.action_type }}</span>
                              <span v-if="step.delay_in_days > 0">• {{ step.delay_in_days }} {{ __('days delay') }}</span>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="flex items-center space-x-1">
                        <!-- Move Up -->
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          @click.stop="handleMoveStep(step, 'up')"
                          :disabled="index === 0"
                          :title="__('Move up')"
                        >
                          <template #icon>
                            <FeatherIcon name="chevron-up" class="w-4 h-4" />
                          </template>
                        </Button>
                        <!-- Move Down -->
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          @click.stop="handleMoveStep(step, 'down')"
                          :disabled="index === templateSteps.length - 1"
                          :title="__('Move down')"
                        >
                          <template #icon>
                            <FeatherIcon name="chevron-down" class="w-4 h-4" />
                          </template>
                        </Button>
                        <div class="border-l border-gray-300 h-4 mx-1"></div>
                        <!-- Copy -->
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          @click.stop="handleCopyStep(step)"
                          :title="__('Copy step')"
                        >
                          <template #icon>
                            <FeatherIcon name="copy" class="w-4 h-4" />
                          </template>
                        </Button>
                        <!-- Edit -->
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          @click.stop="handleEditStep(step)"
                          :title="__('Edit step')"
                        >
                          <template #icon>
                            <FeatherIcon name="edit-2" class="w-4 h-4" />
                          </template>
                        </Button>
                        <!-- Delete -->
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          @click.stop="handleDeleteStep(step)"
                          :title="__('Delete step')"
                        >
                          <template #icon>
                            <FeatherIcon name="trash-2" class="w-4 h-4" />
                          </template>
                        </Button>
                      </div>
                    </div>
                  </div>

                  <!-- Inline Edit Step Form -->
                  <div
                    v-else
                    class="bg-blue-50 border border-blue-200 rounded-lg p-4"
                  >
                    <div class="flex items-center justify-between mb-4">
                      <h4 class="text-lg font-medium text-gray-900">
                        {{ __('Edit Step') }}
                      </h4>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        @click.stop="handleStepCancel"
                      >
                        <template #icon>
                          <FeatherIcon name="x" class="w-4 h-4" />
                        </template>
                      </Button>
                    </div>

                    <div class="space-y-4">
                      <div class="grid grid-cols-2 gap-4">
                        <!-- Step Name -->
                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">
                            {{ __('Step Name') }}
                            <span class="text-red-500">*</span>
                          </label>
                          <TextInput
                            v-model="stepFormData.campaign_step_name"
                            type="text"
                            :placeholder="__('Enter step name...')"
                            :disabled="stepFormLoading"
                            class="w-full"
                          />
                          <div v-if="stepFormErrors.campaign_step_name" class="mt-1 text-sm text-red-600">
                            {{ stepFormErrors.campaign_step_name }}
                          </div>
                        </div>

                        <!-- Action Type -->
                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">
                            {{ __('Action Type') }}
                            <span class="text-red-500">*</span>
                          </label>
                          <FormControl
                            type="select"
                            v-model="stepFormData.action_type"
                            :options="actionTypeOptions"
                            :disabled="stepFormLoading"
                            class="w-full"
                          />
                          <div v-if="stepFormErrors.action_type" class="mt-1 text-sm text-red-600">
                            {{ stepFormErrors.action_type }}
                          </div>
                        </div>
                      </div>

                                          <!-- Delay Days -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        {{ __('Delay (Days)') }}
                      </label>
                      <TextInput
                        v-model.number="stepFormData.delay_in_days"
                        type="number"
                        min="0"
                        max="365"
                        :placeholder="__('0 for immediate execution')"
                        :disabled="stepFormLoading"
                        class="w-full"
                      />
                      <p class="mt-1 text-xs text-gray-500">
                        {{ __('Number of days to wait before executing this step') }}
                      </p>
                      <div v-if="stepFormErrors.delay_in_days" class="mt-1 text-sm text-red-600">
                        {{ stepFormErrors.delay_in_days }}
                      </div>
                    </div>

                      <!-- Template Content -->
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                          {{ __('Template Content') }}
                        </label>
                        <textarea
                          v-model="stepFormData.template_content"
                          rows="3"
                          :placeholder="__('Enter template content for this step...')"
                          :disabled="stepFormLoading"
                          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        />
                        <div v-if="stepFormErrors.template_content" class="mt-1 text-sm text-red-600">
                          {{ stepFormErrors.template_content }}
                        </div>
                      </div>

                      <!-- Action Config -->
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                          {{ __('Action Configuration') }}
                        </label>
                        <textarea
                          v-model="stepFormData.action_config_string"
                          rows="3"
                          :placeholder="__('Enter JSON configuration...')"
                          :disabled="stepFormLoading"
                          class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm font-mono text-sm"
                        />
                        <p class="mt-1 text-xs text-gray-500">
                          {{ __('JSON configuration for the action (optional)') }}
                        </p>
                        <div v-if="stepFormErrors.action_config" class="mt-1 text-sm text-red-600">
                          {{ stepFormErrors.action_config }}
                        </div>
                      </div>

                      <!-- Step Order (Info Only) -->
                      <div class="bg-gray-50 p-3 rounded-md border border-gray-200">
                        <div class="flex items-center space-x-3">
                          <div class="flex-shrink-0">
                            <div class="w-6 h-6 bg-indigo-100 text-indigo-800 text-xs font-medium rounded-full flex items-center justify-center">
                              {{ stepFormData.step_order }}
                            </div>
                          </div>
                          <div class="flex-1">
                            <p class="text-sm font-medium text-gray-900">{{ __('Step Order') }}</p>
                            <p class="text-xs text-gray-500">{{ __('Use Move Up/Down buttons to reorder steps') }}</p>
                          </div>
                        </div>
                      </div>

                      <!-- Form Actions -->
                      <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
                        <Button
                          type="button"
                          variant="outline"
                          theme="gray"
                          @click.stop="handleStepCancel"
                          :disabled="stepFormLoading"
                        >
                          {{ __('Cancel') }}
                        </Button>
                        <Button
                          type="button"
                          variant="solid"
                          theme="gray"
                          @click.stop="handleStepSubmit"
                          :loading="stepFormLoading"
                          :disabled="stepFormLoading"
                        >
                          {{ stepFormLoading ? __('Saving...') : __('Update Step') }}
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Inline Add Step Form -->
              <div v-if="showStepForm && !editingStep" class="mt-6 border-t border-gray-200 pt-6">
                <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div class="flex items-center justify-between mb-4">
                    <h4 class="text-lg font-medium text-gray-900">
                      {{ __('Add New Step') }}
                    </h4>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      @click.stop="handleStepCancel"
                    >
                      <template #icon>
                        <FeatherIcon name="x" class="w-4 h-4" />
                      </template>
                    </Button>
                  </div>

                  <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                      <!-- Step Name -->
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                          {{ __('Step Name') }}
                          <span class="text-red-500">*</span>
                        </label>
                        <TextInput
                          v-model="stepFormData.campaign_step_name"
                          type="text"
                          :placeholder="__('Enter step name...')"
                          :disabled="stepFormLoading"
                          class="w-full"
                        />
                        <div v-if="stepFormErrors.campaign_step_name" class="mt-1 text-sm text-red-600">
                          {{ stepFormErrors.campaign_step_name }}
                        </div>
                      </div>

                      <!-- Action Type -->
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                          {{ __('Action Type') }}
                          <span class="text-red-500">*</span>
                        </label>
                        <FormControl
                          type="select"
                          v-model="stepFormData.action_type"
                          :options="actionTypeOptions"
                          :disabled="stepFormLoading"
                          class="w-full"
                        />
                        <div v-if="stepFormErrors.action_type" class="mt-1 text-sm text-red-600">
                          {{ stepFormErrors.action_type }}
                        </div>
                      </div>
                    </div>

                                          <!-- Delay Days -->
                      <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                          {{ __('Delay (Days)') }}
                        </label>
                        <TextInput
                          v-model.number="stepFormData.delay_in_days"
                          type="number"
                          min="0"
                          max="365"
                          :placeholder="__('0 for immediate execution')"
                          :disabled="stepFormLoading"
                          class="w-full"
                        />
                        <p class="mt-1 text-xs text-gray-500">
                          {{ __('Number of days to wait before executing this step') }}
                        </p>
                        <div v-if="stepFormErrors.delay_in_days" class="mt-1 text-sm text-red-600">
                          {{ stepFormErrors.delay_in_days }}
                        </div>
                      </div>

                    <!-- Template Content -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        {{ __('Template Content') }}
                      </label>
                      <textarea
                        v-model="stepFormData.template_content"
                        rows="3"
                        :placeholder="__('Enter template content for this step...')"
                        :disabled="stepFormLoading"
                        class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                      <div v-if="stepFormErrors.template_content" class="mt-1 text-sm text-red-600">
                        {{ stepFormErrors.template_content }}
                      </div>
                    </div>

                    <!-- Action Config -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">
                        {{ __('Action Configuration') }}
                      </label>
                      <textarea
                        v-model="stepFormData.action_config_string"
                        rows="3"
                        :placeholder="__('Enter JSON configuration...')"
                        :disabled="stepFormLoading"
                        class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm font-mono text-sm"
                      />
                      <p class="mt-1 text-xs text-gray-500">
                        {{ __('JSON configuration for the action (optional)') }}
                      </p>
                      <div v-if="stepFormErrors.action_config" class="mt-1 text-sm text-red-600">
                        {{ stepFormErrors.action_config }}
                      </div>
                    </div>

                    <!-- Step Order (Info Only) -->
                    <div class="bg-green-50 p-3 rounded-md border border-green-200">
                      <div class="flex items-center space-x-3">
                        <div class="flex-shrink-0">
                          <div class="w-6 h-6 bg-green-100 text-green-800 text-xs font-medium rounded-full flex items-center justify-center">
                            {{ stepFormData.step_order }}
                          </div>
                        </div>
                        <div class="flex-1">
                          <p class="text-sm font-medium text-gray-900">{{ __('Step Order') }}</p>
                          <p class="text-xs text-gray-500">{{ __('Will be positioned as step #' + stepFormData.step_order) }}</p>
                        </div>
                      </div>
                    </div>

                    <!-- Form Actions -->
                    <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
                      <Button
                        type="button"
                        variant="outline"
                        theme="gray"
                        @click.stop="handleStepCancel"
                        :disabled="stepFormLoading"
                      >
                        {{ __('Cancel') }}
                      </Button>
                      <Button
                        type="button"
                        variant="solid"
                        theme="gray"
                        @click.stop="handleStepSubmit"
                        :loading="stepFormLoading"
                        :disabled="stepFormLoading"
                      >
                        {{ stepFormLoading ? __('Saving...') : __('Add Step') }}
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Error Message -->
            <div v-if="submitError" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <div class="flex">
                <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">
                    {{ __('Error saving template') }}
                  </h3>
                  <div class="mt-1 text-sm text-red-700">
                    {{ submitError }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <Button
              type="submit"
              variant="solid"
              theme="gray"
              :loading="loading"
              :disabled="loading"
            >
              {{ loading ? __('Saving...') : (isEdit ? __('Update Template') : __('Create Template')) }}
            </Button>
            <Button
              variant="outline"
              theme="gray"
              @click="handleClose"
              :disabled="loading"
              class="sm:mr-3"
            >
              {{ __('Cancel') }}
            </Button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick } from 'vue'
import { Button, TextInput, FormControl, FeatherIcon, Tabs } from 'frappe-ui'
import { campaignTemplateDirectService } from '@/services/campaignTemplateDirectService.js'
import { campaignTemplateStepDirectService } from '@/services/campaignTemplateStepDirectService.js'
import { useToast } from '@/composables/useToast.js'

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  template: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'saved', 'step-changed'])

// Toast
const { showSuccess, showError } = useToast()

// i18n fallback
const __ = (text) => text

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const isEdit = computed(() => !!props.template)

// Tabs configuration
const tabs = computed(() => {
  const tabsArray = [
    {
      label: __('Template Info'),
      name: 'template'
    }
  ]
  
  // Only show steps tab if template exists or is being edited
  if (isEdit.value || savedTemplate.value) {
    tabsArray.push({
      label: templateSteps.value.length > 0 
        ? `${__('Template Steps')} (${templateSteps.value.length})`
        : __('Template Steps'),
      name: 'steps'
    })
  }
  
  return tabsArray
})

// For backward compatibility
const activeTab = computed(() => tabs.value[activeTabIndex.value]?.name || 'template')

// Reactive data
const loading = ref(false)
const submitError = ref('')
const errors = reactive({})
const activeTabIndex = ref(0)
const savedTemplate = ref(null)
const templateSteps = ref([])
const stepsLoading = ref(false)

// Step inline form state
const showStepForm = ref(false)
const editingStep = ref(null)
const stepFormLoading = ref(false)
const stepFormErrors = reactive({})
const stepFormData = reactive({
  campaign_step_name: '',
  action_type: '',
  step_order: 1,
  delay_in_days: 0,
  template_content: '',
  action_config_string: ''
})

const formData = reactive({
  template_name: '',
  campaign_type: '',
  description: '',
  is_active: true
})

// Campaign type options
const campaignTypeOptions = [
  { label: __('Select campaign type...'), value: '', disabled: true },
  { label: __('Email Campaign'), value: 'Email' },
  { label: __('SMS Campaign'), value: 'SMS' },
  { label: __('Advertisement Campaign'), value: 'Ads' },
  { label: __('Social Media Campaign'), value: 'Social Media' },
  { label: __('Direct Mail Campaign'), value: 'Direct Mail' }
]

// Action type options for steps
const actionTypeOptions = [
  { label: __('Select action type...'), value: '', disabled: true },
  { label: __('Send Email'), value: 'SEND_EMAIL' },
  { label: __('Send SMS'), value: 'SEND_SMS' },
  { label: __('Manual Call'), value: 'MANUAL_CALL' },
  { label: __('Manual Task'), value: 'MANUAL_TASK' }
]

// Methods
const resetForm = () => {
  formData.template_name = ''
  formData.campaign_type = ''
  formData.description = ''
  formData.is_active = true
  
  // Clear errors
  Object.keys(errors).forEach(key => {
    delete errors[key]
  })
  
  submitError.value = ''
  activeTabIndex.value = 0
  savedTemplate.value = null
  templateSteps.value = []
  showStepForm.value = false
  resetStepForm()
}

const setFormData = (template) => {
  if (template) {
    formData.template_name = template.template_name || ''
    formData.campaign_type = template.campaign_type || ''
    formData.description = template.description || ''
    // Fix: Handle both number (1/0) and boolean values for is_active
    formData.is_active = template.is_active === 1 || template.is_active === true
    savedTemplate.value = template
    
    // Load steps if template exists
    if (template.name) {
      loadTemplateSteps(template.name)
    }
  }
}

const loadTemplateSteps = async (templateName) => {
  if (!templateName) return
  
  stepsLoading.value = true
  try {
    const result = await campaignTemplateStepDirectService.getStepsByTemplate(templateName)
    if (result.success) {
      templateSteps.value = result.data || []
    } else {
      console.error('Error loading template steps:', result.error)
      templateSteps.value = []
    }
  } catch (err) {
    console.error('Error loading template steps:', err)
    templateSteps.value = []
  } finally {
    stepsLoading.value = false
  }
}

const handleAddStep = async () => {
  if (!savedTemplate.value && !isEdit.value) {
    showError(__('Please save the template first before adding steps'))
    return
  }
  
  // Reset and show inline step form
  resetStepForm()
  editingStep.value = null
  
  // Auto-assign next step order
  try {
    const nextOrder = await getNextStepOrder()
    stepFormData.step_order = nextOrder
  } catch (error) {
    console.error('Error getting next step order:', error)
    stepFormData.step_order = templateSteps.value.length + 1
  }
  
  showStepForm.value = true
  
  // Auto-scroll to add step form after it renders
  await nextTick()
  const addStepForm = document.querySelector('.bg-green-50.border-green-200')
  if (addStepForm) {
    addStepForm.scrollIntoView({ 
      behavior: 'smooth', 
      block: 'start' 
    })
    
    // Auto-focus on first input field
    const firstInput = addStepForm.querySelector('input[type="text"]')
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 300) // Wait for scroll to complete
    }
  }
}

const handleEditStep = async (step) => {
  // Set form data and show inline step form (replace the step item)
  resetStepForm()
  editingStep.value = step
  setStepFormData(step)
  // No need to set showStepForm, it's handled by v-if in template
  
  // Auto-focus on first input field after form renders
  await nextTick()
  const editForm = document.querySelector('.bg-blue-50.border-blue-200')
  if (editForm) {
    const firstInput = editForm.querySelector('input[type="text"]')
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100)
    }
  }
}

const handleDeleteStep = async (step) => {
  if (!confirm(__('Are you sure you want to delete this step?'))) return
  
  try {
    const result = await campaignTemplateStepDirectService.delete(step.name)
    if (result.success) {
      showSuccess(__('Step deleted successfully'))
      // Reload steps
      loadTemplateSteps(savedTemplate.value?.name || props.template?.name)
      // Emit step changed event to parent
      emit('step-changed')
    } else {
      showError(result.error || __('Failed to delete step'))
    }
  } catch (err) {
    console.error('Error deleting step:', err)
    showError(__('An error occurred while deleting step'))
  }
}

const handleMoveStep = async (step, direction) => {
  try {
    const result = await campaignTemplateStepDirectService.moveStep(step.name, direction)
    if (result.success) {
      showSuccess(result.message || __('Step moved successfully'))
      // Reload steps to reflect new order
      loadTemplateSteps(savedTemplate.value?.name || props.template?.name)
      // Emit step changed event to parent
      emit('step-changed')
    } else {
      showError(result.error || __('Failed to move step'))
    }
  } catch (err) {
    console.error('Error moving step:', err)
    showError(__('An error occurred while moving step'))
  }
}

const handleCopyStep = async (step) => {
  try {
    const templateName = savedTemplate.value?.name || props.template?.name
    
    // Create copy data with modified name and put at the end
    const copyData = {
      template: templateName,
      campaign_step_name: `${step.campaign_step_name} (Copy)`,
      action_type: step.action_type,
      step_order: templateSteps.value.length + 1, // Put at the end
      delay_in_days: step.delay_in_days || 0,
      template_content: step.template_content || '',
      action_config: step.action_config || null
    }
    
    const result = await campaignTemplateStepDirectService.create(copyData)
    if (result.success) {
      showSuccess(__('Step copied successfully'))
      // Reload steps to reflect new step
      loadTemplateSteps(templateName)
      // Emit step changed event to parent
      emit('step-changed')
    } else {
      showError(result.error || __('Failed to copy step'))
    }
  } catch (err) {
    console.error('Error copying step:', err)
    showError(__('An error occurred while copying step'))
  }
}

// Step form methods
const resetStepForm = () => {
  stepFormData.campaign_step_name = ''
  stepFormData.action_type = ''
  stepFormData.step_order = 1
  stepFormData.delay_in_days = 0
  stepFormData.template_content = ''
  stepFormData.action_config_string = ''
  
  // Clear errors
  Object.keys(stepFormErrors).forEach(key => {
    delete stepFormErrors[key]
  })
  
  editingStep.value = null
}

const setStepFormData = (step) => {
  if (step) {
    stepFormData.campaign_step_name = step.campaign_step_name || ''
    stepFormData.action_type = step.action_type || ''
    stepFormData.step_order = step.step_order || 1
    stepFormData.delay_in_days = step.delay_in_days || 0
    stepFormData.template_content = step.template_content || ''
    
    // Handle JSON config
    if (step.action_config) {
      if (typeof step.action_config === 'object') {
        stepFormData.action_config_string = JSON.stringify(step.action_config, null, 2)
      } else {
        stepFormData.action_config_string = step.action_config
      }
    } else {
      stepFormData.action_config_string = ''
    }
  }
}

const getNextStepOrder = async () => {
  const templateName = savedTemplate.value?.name || props.template?.name
  if (!templateName) return 1
  
  try {
    const result = await campaignTemplateStepDirectService.getNextStepOrder(templateName)
    return result || templateSteps.value.length + 1
  } catch (error) {
    return templateSteps.value.length + 1
  }
}

const validateStepForm = () => {
  // Clear previous errors
  Object.keys(stepFormErrors).forEach(key => {
    delete stepFormErrors[key]
  })

  let isValid = true

  // Required fields
  if (!stepFormData.campaign_step_name || !stepFormData.campaign_step_name.trim()) {
    stepFormErrors.campaign_step_name = __('Step name is required')
    isValid = false
  } else if (stepFormData.campaign_step_name.length > 150) {
    stepFormErrors.campaign_step_name = __('Step name must be less than 150 characters')
    isValid = false
  }

  if (!stepFormData.action_type || !stepFormData.action_type.trim()) {
    stepFormErrors.action_type = __('Action type is required')
    isValid = false
  }

  // Step order is auto-managed, no validation needed

  if (stepFormData.delay_in_days < 0 || stepFormData.delay_in_days > 365) {
    stepFormErrors.delay_in_days = __('Delay must be between 0 and 365 days')
    isValid = false
  }

  // Validate JSON config if provided
  if (stepFormData.action_config_string && stepFormData.action_config_string.trim()) {
    try {
      JSON.parse(stepFormData.action_config_string)
    } catch (e) {
      stepFormErrors.action_config = __('Invalid JSON format')
      isValid = false
    }
  }

  return isValid
}

const handleStepSubmit = async () => {
  if (!validateStepForm()) {
    return
  }

  stepFormLoading.value = true

  try {
    const templateName = savedTemplate.value?.name || props.template?.name
    const data = {
      template: templateName,
      campaign_step_name: stepFormData.campaign_step_name.trim(),
      action_type: stepFormData.action_type,
      step_order: stepFormData.step_order,
      delay_in_days: stepFormData.delay_in_days,
      template_content: stepFormData.template_content ? stepFormData.template_content.trim() : '',
    }

    // Handle action config
    if (stepFormData.action_config_string && stepFormData.action_config_string.trim()) {
      try {
        data.action_config = JSON.parse(stepFormData.action_config_string)
      } catch (e) {
        data.action_config = stepFormData.action_config_string
      }
    }

    let result

    if (editingStep.value) {
      // Update existing step
      result = await campaignTemplateStepDirectService.update(editingStep.value.name, data)
    } else {
      // Create new step
      result = await campaignTemplateStepDirectService.create(data)
    }

    if (result.success) {
      showSuccess(result.message || (editingStep.value ? __('Step updated successfully') : __('Step added successfully')))

      // Hide form and reload steps
      showStepForm.value = false
      editingStep.value = null
      resetStepForm()
      
      // Reload steps list
      loadTemplateSteps(templateName)
      
      // Emit step changed event to parent
      emit('step-changed')
    } else {
      // Handle validation errors from server
      if (result.error.includes('campaign_step_name')) {
        stepFormErrors.campaign_step_name = result.error
      } else if (result.error.includes('action_type')) {
        stepFormErrors.action_type = result.error
      } else {
        showError(result.error)
      }
    }
  } catch (err) {
    console.error('Error submitting step form:', err)
    showError(__('An error occurred while saving step'))
  } finally {
    stepFormLoading.value = false
  }
}

const handleStepCancel = () => {
  showStepForm.value = false
  editingStep.value = null
  resetStepForm()
}

const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => {
    delete errors[key]
  })

  let isValid = true

  // Required fields
  if (!formData.template_name || !formData.template_name.trim()) {
    errors.template_name = __('Template name is required')
    isValid = false
  } else if (formData.template_name.length > 150) {
    errors.template_name = __('Template name must be less than 150 characters')
    isValid = false
  }

  if (!formData.campaign_type || !formData.campaign_type.trim()) {
    errors.campaign_type = __('Campaign type is required')
    isValid = false
  }

  if (formData.description && formData.description.length > 500) {
    errors.description = __('Description must be less than 500 characters')
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  submitError.value = ''

  try {
    const data = {
      template_name: formData.template_name.trim(),
      campaign_type: formData.campaign_type,
      description: formData.description ? formData.description.trim() : '',
      is_active: formData.is_active ? 1 : 0
    }

    let result

    if (isEdit.value) {
      // Update existing template
      result = await campaignTemplateDirectService.update(props.template.name, data)
    } else {
      // Create new template
      result = await campaignTemplateDirectService.create(data)
    }

    if (result.success) {
      showSuccess(result.message || (isEdit.value ? __('Template updated successfully') : __('Template created successfully')))

      // Update saved template for new creations
      if (!isEdit.value) {
        savedTemplate.value = result.data
        activeTabIndex.value = 1 // Switch to steps tab
        
        // Don't close modal, switch to steps tab
        emit('saved', result.data)
        return
      } else {
        // For edits, reload steps and close modal
        if (result.data?.name) {
          loadTemplateSteps(result.data.name)
        }
        show.value = false
        emit('saved', result.data)
      }
    } else {
      // Handle validation errors from server
      if (result.error.includes('template_name')) {
        errors.template_name = result.error
      } else if (result.error.includes('campaign_type')) {
        errors.campaign_type = result.error
      } else {
        submitError.value = result.error
      }
    }
  } catch (err) {
    console.error('Error submitting form:', err)
    submitError.value = __('An error occurred while saving template')
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  if (!loading.value) {
    show.value = false
  }
}



// Watchers
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue) {
      // Reset form when opening
      resetForm()
      
      // Set form data if editing
      if (props.template) {
        nextTick(() => {
          setFormData(props.template)
        })
      }
    }
  },
  { immediate: true }
)

watch(
  () => props.template,
  (newTemplate) => {
    if (newTemplate && props.modelValue) {
      setFormData(newTemplate)
    }
  }
)
</script>

<style scoped>
/* Add any component-specific styles here */
</style> 