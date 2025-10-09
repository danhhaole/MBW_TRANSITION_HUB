<template>
  <Dialog
    v-model="show"
    :options="dialogOptions"
    :disableOutsideClickToClose="true"
  >
    <template #body>
      <div class="bg-white">
        <!-- Header -->
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-900">
            {{ editingStep ? __("Edit Step") : __("Add New Step") }}
          </h2>
          <Button
            theme="gray"
            variant="ghost"
            class="w-7 h-7"
            @click="handleCancel"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </Button>
        </div>

        <!-- Step Form Content -->
        <div class="p-6">
          <!-- Template Step Selection -->
          <div class="mb-6 p-4 bg-gray-50 rounded-lg border">
            <h3 class="text-sm font-medium text-gray-900 mb-3">
              {{ __("Use Template Step (Optional)") }}
            </h3>
            
            <Link
              v-model="selectedTemplateStepName"
              :label="__('Template Step')"
              :placeholder="__('Select a template step...')"
              doctype="CampaignTemplateStep"
              :fields="['campaign_step_name', 'action_type', 'delay_in_days']"
              @change="onTemplateStepChange"
              @update:modelValue="onTemplateStepChange"
            />
            
            <!-- Selected Template Step Info -->
            <div v-if="selectedTemplateStep" class="mt-3 p-3 bg-blue-50 rounded border border-blue-200">
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-medium text-sm text-blue-900">
                    {{ selectedTemplateStep.campaign_step_name }}
                  </div>
                  <div class="text-xs text-blue-600">
                    {{ selectedTemplateStep.action_type }} • {{ __("Delay:") }} {{ selectedTemplateStep.delay_in_days }} {{ __("days") }}
                  </div>
                </div>
                <Button
                  theme="gray"
                  variant="ghost"
                  size="sm"
                  @click="clearTemplateStep"
                >
                  {{ __("Clear") }}
                </Button>
              </div>
            </div>
          </div>
          
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <!-- Step Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __("Step Name") }}
                <span class="text-red-500">*</span>
              </label>
              <input
                v-model="formData.campaign_step_name"
                type="text"
                :placeholder="__('Enter step name...')"
                :disabled="loading"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': errors.campaign_step_name }"
              />
              <div
                v-if="errors.campaign_step_name"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.campaign_step_name }}
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <!-- Action Type -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Action Type") }}
                  <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="formData.action_type"
                  :disabled="loading"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{ 'border-red-500': errors.action_type }"
                >
                  <option
                    v-for="option in actionTypeOptions"
                    :key="option.value"
                    :value="option.value"
                    :disabled="option.disabled"
                  >
                    {{ option.label }}
                  </option>
                </select>
                <div
                  v-if="errors.action_type"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ errors.action_type }}
                </div>
              </div>

              <!-- Step Order -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Step Order") }}
                  <span class="text-red-500">*</span>
                </label>
                <input
                  v-model.number="formData.step_order"
                  type="number"
                  min="1"
                  max="999"
                  :placeholder="__('Order...')"
                  :disabled="true"
                  readonly
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                  :class="{ 'border-red-500': errors.step_order }"
                />
                <div v-if="errors.step_order" class="mt-1 text-sm text-red-600">
                  {{ errors.step_order }}
                </div>
              </div>
            </div>

            <!-- Delay -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __("Delay (Days)") }}
              </label>
              <input
                v-model.number="formData.delay_in_days"
                type="number"
                min="0"
                max="365"
                :placeholder="__('0 for immediate execution')"
                :disabled="loading"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': errors.delay_in_days }"
              />
              <p class="mt-1 text-sm text-gray-500">
                {{ __("Number of days to wait before executing this step") }}
              </p>
              <div
                v-if="errors.delay_in_days"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.delay_in_days }}
              </div>
            </div>

            <!-- Template Content -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __("Template Content") }}
              </label>
              <textarea
                v-model="formData.template_content"
                rows="4"
                :placeholder="__('Enter template content...')"
                :disabled="loading"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-500': errors.template_content }"
              />
              <p class="mt-1 text-sm text-gray-500">
                {{ __("Email/SMS template content or task description") }}
              </p>
              <div
                v-if="errors.template_content"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.template_content }}
              </div>
            </div>

            <!-- Action Config -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __("Action Configuration") }}
              </label>
              <textarea
                v-model="formData.action_config_string"
                rows="3"
                :placeholder="__('Enter JSON configuration...')"
                :disabled="loading"
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm font-mono text-sm"
                :class="{ 'border-red-500': errors.action_config_string }"
              />
              <p class="mt-1 text-sm text-gray-500">
                {{ __("JSON configuration for the action (optional)") }}
              </p>
              <div
                v-if="errors.action_config_string"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.action_config_string }}
              </div>
            </div>
          </form>
        </div>

        <!-- Footer Actions -->
        <div class="flex justify-end space-x-3 p-6 border-t border-gray-200">
          <Button
            type="button"
            variant="outline"
            theme="gray"
            @click="handleCancel"
            :disabled="loading"
          >
            {{ __("Cancel") }}
          </Button>
          <Button
            type="submit"
            variant="solid"
            theme="gray"
            @click="handleSubmit"
            :loading="loading"
            :disabled="loading"
          >
            {{ editingStep ? __("Update Step") : __("Add Step") }}
          </Button>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { Dialog, Button, FeatherIcon, call } from "frappe-ui";
import Link from "@/components/Controls/Link.vue";

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  editingStep: {
    type: Object,
    default: null,
  },
  campaignSteps: {
    type: Array,
    default: () => [],
  },
  draftCampaign: {
    type: Object,
    default: null,
  },
});

// Emits
const emit = defineEmits([
  "update:modelValue",
  "submit",
  "cancel",
]);

// Translation helper
const __ = (text) => text;

// Reactive state
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const loading = ref(false);
const errors = ref({});

// Form data
const formData = ref({
  campaign: "",
  campaign_step_name: "",
  action_type: "",
  step_order: 1,
  delay_in_days: 0,
  template_content: "",
  action_config_string: "",
  image: "",
  scheduled_at: "",
});

// Template step selection state
const selectedTemplateStep = ref(null);
const selectedTemplateStepName = ref("");

// Action type options
const actionTypeOptions = [
  { label: __("Select action type..."), value: "", disabled: true },
  { label: __("Send Email"), value: "SEND_EMAIL" },
  { label: __("Send SMS"), value: "SEND_SMS" },
  { label: __("Manual Call"), value: "MANUAL_CALL" },
  { label: __("Manual Task"), value: "MANUAL_TASK" },
];

// Dialog options
const dialogOptions = computed(() => ({
  title: props.editingStep ? __("Edit Step") : __("Add New Step"),
  size: "lg",
}));

// Methods
const resetForm = () => {
  formData.value = {
    campaign: "",
    campaign_step_name: "",
    action_type: "",
    step_order: props.campaignSteps.length + 1,
    delay_in_days: 0,
    template_content: "",
    action_config_string: "",
    image: "",
    scheduled_at: "",
  };
  errors.value = {};
  // Reset template step selection
  selectedTemplateStep.value = null;
  selectedTemplateStepName.value = "";
};

// Template step functions
const onTemplateStepChange = async (stepName) => {
  console.log('🔍 Template step selected:', stepName);
  
  if (!stepName) {
    selectedTemplateStep.value = null;
    return;
  }
  
  try {
    console.log('📡 Loading template step data...');
    const response = await call('frappe.client.get_doc', {
      doctype: 'CampaignTemplateStep',
      name: stepName
    });
    
    console.log('📋 Template step data received:', response);
    
    if (response) {
      selectedTemplateStep.value = response;
      
      // Fill form with template step data
      formData.value.campaign_step_name = response.campaign_step_name;
      formData.value.action_type = response.action_type;
      formData.value.delay_in_days = response.delay_in_days || 0;
      formData.value.template_content = response.template_content || "";
      
      console.log('✅ Form data filled:', {
        name: formData.value.campaign_step_name,
        type: formData.value.action_type,
        delay: formData.value.delay_in_days,
        content: formData.value.template_content
      });
      
      // Handle action_config (JSON field)
      if (response.action_config) {
        try {
          formData.value.action_config_string = typeof response.action_config === 'string' 
            ? response.action_config 
            : JSON.stringify(response.action_config, null, 2);
        } catch (e) {
          formData.value.action_config_string = "";
        }
      }
    }
  } catch (error) {
    console.error('❌ Error loading template step:', error);
    selectedTemplateStep.value = null;
  }
};

const clearTemplateStep = () => {
  selectedTemplateStep.value = null;
  selectedTemplateStepName.value = "";
  // Don't clear form data, let user keep what they want
};

// Watch for template step name changes
watch(selectedTemplateStepName, (newValue) => {
  console.log('👀 Watcher: selectedTemplateStepName changed to:', newValue);
  if (newValue && newValue !== selectedTemplateStep.value?.name) {
    onTemplateStepChange(newValue);
  }
});

const setFormData = (step) => {
  formData.value = {
    campaign: props.draftCampaign?.data?.name || props.draftCampaign?.name || "",
    campaign_step_name: step.campaign_step_name || "",
    action_type: step.action_type || "",
    step_order: step.step_order || props.campaignSteps.length + 1,
    delay_in_days: step.delay_in_days || 0,
    template_content: step.template_content || "",
    action_config_string: step.action_config_string || "",
    image: step.image || "",
    scheduled_at: step.scheduled_at || "",
  };
};

const validateForm = () => {
  errors.value = {};

  if (!formData.value.campaign_step_name?.trim()) {
    errors.value.campaign_step_name = __("Step name is required");
  }

  if (!formData.value.action_type) {
    errors.value.action_type = __("Action type is required");
  }

  if (
    !Number.isFinite(formData.value.step_order) ||
    formData.value.step_order < 1
  ) {
    errors.value.step_order = __("Step order must be a positive number");
  }

  if (
    formData.value.delay_in_days !== null &&
    formData.value.delay_in_days !== undefined &&
    (!Number.isFinite(formData.value.delay_in_days) ||
      formData.value.delay_in_days < 0)
  ) {
    errors.value.delay_in_days = __("Delay must be a non-negative number");
  }

  if (formData.value.action_config_string?.trim()) {
    try {
      JSON.parse(formData.value.action_config_string);
    } catch {
      errors.value.action_config_string = __("Invalid JSON format");
    }
  }

  return Object.keys(errors.value).length === 0;
};

const handleSubmit = () => {
  if (!validateForm()) return;

  loading.value = true;

  try {
    const stepData = {
      campaign: props.draftCampaign?.data?.name || props.draftCampaign?.name,
      campaign_step_name: formData.value.campaign_step_name.trim(),
      action_type: formData.value.action_type,
      delay_in_days: formData.value.delay_in_days,
      template_content: formData.value.template_content?.trim() || "",
      image: formData.value.image || "",
      action_config: formData.value.action_config_string?.trim()
        ? (() => {
            try {
              return JSON.parse(formData.value.action_config_string);
            } catch {
              return formData.value.action_config_string;
            }
          })()
        : null,
    };

    if (
      Number.isFinite(formData.value.step_order) &&
      formData.value.step_order > 0
    ) {
      stepData.step_order = formData.value.step_order;
    }

    emit("submit", {
      stepData,
      isEditing: !!props.editingStep,
      editingStepId: props.editingStep?.id,
    });

    show.value = false;
    resetForm();
  } finally {
    loading.value = false;
  }
};

const handleCancel = () => {
  show.value = false;
  resetForm();
  emit("cancel");
};

// Watch for editing step changes
watch(
  () => props.editingStep,
  (newStep) => {
    if (newStep) {
      setFormData(newStep);
    } else {
      resetForm();
    }
  },
  { immediate: true }
);

// Watch for show changes to reset form
watch(show, (newShow) => {
  if (newShow && !props.editingStep) {
    resetForm();
  }
});
</script>
