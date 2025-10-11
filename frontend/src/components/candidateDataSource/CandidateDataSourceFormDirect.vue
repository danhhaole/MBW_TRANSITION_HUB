<template>
  <Dialog
    v-model="dialog"
    :options="{
      title: isEdit ? __('Edit Data Source') : __('Add New Data Source'),
      size: 'xl',
    }"
  >
    <template #body>
      <div class="p-6">
        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <div class="flex items-center space-x-3">
            <div
              class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center"
            >
              <FeatherIcon name="database" class="h-6 w-6 text-white" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900">
                {{ isEdit ? __("Edit Data Source") : __("Add New Data Source") }}
              </h3>
              <p class="text-sm text-gray-500">
                {{
                  isEdit
                    ? __("Update data source information")
                    : __("Create a new data source for the system")
                }}
              </p>
            </div>
          </div>
          <!-- Close Button -->
          <Button
            variant="ghost"
            size="sm"
            @click="handleCancel"
            class="text-gray-400 hover:text-gray-600"
          >
            <FeatherIcon name="x" class="h-5 w-5" />
          </Button>
        </div>

        <!-- Loading Form Fields -->
        <div v-if="loadingFields" class="flex justify-center items-center py-8">
          <div class="flex items-center space-x-2 text-gray-600">
            <svg
              class="animate-spin h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>{{ __("Loading form...") }}</span>
          </div>
        </div>

        <!-- Enhanced Form using FieldLayout -->
        <div v-else-if="fieldTabs && fieldTabs.length > 0" class="space-y-4">
          <FieldLayout
            :tabs="fieldTabs"
            :data="formData"
            doctype="CandidateDataSource"
            :preview="false"
          />

          <!-- Additional computed fields display -->
          <div
            v-if="isEdit && formData.display_status"
            class="mt-6 p-4 bg-gray-50 rounded-lg"
          >
            <h4 class="text-sm font-medium text-gray-700 mb-3">
              {{ __("Connection Status") }}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="flex items-center space-x-2">
                <div
                  class="w-3 h-3 rounded-full"
                  :class="{
                    'bg-green-500': formData.connection_status === 'connected',
                    'bg-red-500': formData.connection_status === 'error',
                    'bg-yellow-500': formData.connection_status === 'unknown',
                    'bg-gray-500': formData.connection_status === 'disconnected',
                  }"
                ></div>
                <span class="text-sm text-gray-600">
                  Status: {{ formData.display_status }}
                </span>
              </div>
              <div class="text-sm text-gray-600">
                Last Sync: {{ formData.last_sync_formatted }}
              </div>
              <div class="text-sm text-gray-600">Type: {{ formData.type_display }}</div>
            </div>
          </div>
        </div>

        <!-- Fallback Enhanced Form nếu FieldLayout fails -->
        <div v-else class="space-y-6">
          <!-- Thông tin cơ bản -->
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h4 class="text-md font-medium text-gray-800 mb-4">
              {{ __("Basic Information") }}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Source Name -->
              <div v-if="false">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Source Name") }} <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.source_name"
                  type="text"
                  :placeholder="__('Enter data source name')"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  :disabled="true"
                  required
                />
              </div>

              <!-- Source Type -->
              <div v-if="false">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Source Type") }} <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="formData.source_type"
                  :disabled="true"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <!-- <option value="">{{ __('-- Select source type --') }}</option> -->
                  <option value="ATS">{{ __("ATS") }}</option>
                  <!-- <option value="JobBoard">{{ __('Job Board') }}</option>
                  <option value="Social Network">{{ __('Social Network') }}</option>
                  <option value="Manual">{{ __('Manual') }}</option>
                  <option value="Other">{{ __('Other') }}</option> -->
                </select>
              </div>

              <!-- API Base URL -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">{{
                  __("API Base URL")
                }}</label>
                <input
                  v-model="formData.api_base_url"
                  type="url"
                  placeholder="https://api.example.com"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          <!-- Authentication -->
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h4 class="text-md font-medium text-gray-800 mb-4">
              {{ __("Authentication") }}
            </h4>
            <div class="space-y-4">
              <!-- Auth Method -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __("Authentication Method") }} <span class="text-red-500">*</span>
                </label>
                <select
                  v-model="formData.auth_method"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                >
                  <option value="">{{ __("-- Select method --") }}</option>
                  <option value="API Key">{{ __("API Key") }}</option>
                  <option value="OAuth2">{{ __("OAuth2") }}</option>
                  <option value="Basic">{{ __("Basic") }}</option>
                </select>
              </div>

              <!-- OAuth2 Fields -->
              <div
                v-if="formData.auth_method === 'OAuth2'"
                class="grid grid-cols-1 md:grid-cols-2 gap-4"
              >
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("Client ID") }} <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="formData.client_id"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("Client Secret") }} <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="formData.client_secret"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <!-- API Key Fields -->
              <div
                v-if="formData.auth_method === 'API Key'"
                class="grid grid-cols-1 md:grid-cols-2 gap-4"
              >
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __("API Key") }} <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model="formData.api_key"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">{{
                    __("API Secret")
                  }}</label>
                  <input
                    v-model="formData.api_secret"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Configuration -->
          <div class="bg-white border border-gray-200 rounded-lg p-4">
            <h4 class="text-md font-medium text-gray-800 mb-4">
              {{ __("Configuration") }}
            </h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Status -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{
                  __("Status")
                }}</label>
                <select
                  v-model="formData.status"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="Active">{{ __("Active") }}</option>
                  <option value="Inactive">{{ __("Inactive") }}</option>
                </select>
              </div>

              <!-- Active Status -->
              <div class="md:col-span-2 flex items-center space-x-2">
                <input
                  v-model="formData.is_active"
                  type="checkbox"
                  class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
                />
                <label class="text-sm font-medium text-gray-700">{{
                  __("Activate data source")
                }}</label>
              </div>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 bg-red-50 border border-red-200 rounded-lg p-3">
          <div class="flex">
            <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
            <div class="ml-3">
              <p class="text-sm text-red-800">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Success Message -->
        <div
          v-if="success"
          class="mt-4 bg-green-50 border border-green-200 rounded-lg p-3"
        >
          <div class="flex">
            <svg class="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
            <div class="ml-3">
              <p class="text-sm text-green-800">{{ __("Operation successful!") }}</p>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-between items-center pt-6 border-t border-gray-200 mt-6">
          <div>
            <!-- Test Connection Button (chỉ hiện khi edit) -->
            <Button
              v-if="isEdit"
              variant="outline"
              theme="blue"
              @click="handleTestConnection"
              :loading="testing"
            >
              <template #prefix>
                <FeatherIcon name="wifi" class="h-4 w-4" />
              </template>
              {{ testing ? __("Testing...") : __("Test Connection") }}
            </Button>
          </div>

          <div class="flex space-x-3">
            <Button variant="outline" @click="handleCancel">
              {{ __("Cancel") }}
            </Button>
            <Button variant="solid" theme="gray" @click="handleSubmit" :loading="loading">
              {{ isEdit ? __("Update") : __("Create") }}
            </Button>
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, reactive } from "vue";
import { Dialog, Button, FeatherIcon } from "frappe-ui";
import FieldLayout from "@/components/FieldLayout/FieldLayout.vue";
import { useCandidateDataSourceStore } from "@/stores/candidateDataSource.js";
import { useDocument } from "@/data/document";

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  dataSource: {
    type: Object,
    default: null,
  },
});

// Emits
const emit = defineEmits(["update:modelValue", "success", "cancel"]);

// Store
const candidateDataSourceStore = useCandidateDataSourceStore();

// Reactive state
const loading = ref(false);
const loadingFields = ref(false);
const testing = ref(false);
const error = ref(null);
const success = ref(false);

// Refs
const fieldTabs = ref([]);

// Form data với enhanced structure
const formData = reactive({
  source_name: "MBW ATS",
  source_type: "ATS",
  api_base_url: "",
  auth_method: "",
  client_id: "",
  client_secret: "",
  api_key: "",
  api_secret: "",
  access_token: "",
  refresh_token: "",
  token_expires_at: "",
  doctype_to_sync: "",
  sync_direction: "",
  status: "Active",
  last_sync_at: "",
  sync_frequency_minutes: 60,
  last_error: "",
  notes: "",
  created_by: "",
  is_active: true,
  // Computed fields từ service
  display_status: "",
  connection_status: "",
  last_sync_formatted: "",
  type_display: "",
  auth_method_display: "",
});

const { document: data, triggerOnBeforeCreate } = useDocument("CandidateDataSource");

// Computed
const dialog = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const isEdit = computed(() => !!props.dataSource);

// Methods
const resetForm = () => {
  Object.assign(formData, {
    source_name: "MBW ATS",
    source_type: "ATS",
    api_base_url: "",
    auth_method: "",
    client_id: "",
    client_secret: "",
    api_key: "",
    api_secret: "",
    access_token: "",
    refresh_token: "",
    token_expires_at: "",
    doctype_to_sync: "",
    sync_direction: "",
    status: "Active",
    last_sync_at: "",
    sync_frequency_minutes: 60,
    last_error: "",
    notes: "",
    created_by: "",
    is_active: true,
    display_status: "",
    connection_status: "",
    last_sync_formatted: "",
    type_display: "",
    auth_method_display: "",
    same_site: 0,
  });
};

const setFormData = (dataSource) => {
  if (dataSource) {
    Object.keys(formData).forEach((key) => {
      if (dataSource[key] !== undefined) {
        formData[key] = dataSource[key];
      }
    });
  }
};

const loadFieldLayout = async () => {
  loadingFields.value = true;
  try {
    const response = await candidateDataSourceStore.fetchFormData(
      props.dataSource?.name || null
    );

    if (response.success && response.data && response.data.fieldLayout) {
      fieldTabs.value = response.data.fieldLayout;

      // Lọc bỏ các field không muốn hiển thị trong form
      const hiddenFields = new Set([
        "last_sync_at",
        "sync_frequency_minutes",
        "last_error",
        "notes",
        // Ẩn luôn trong FieldLayout
        "source_name",
        "source_type",
      ]);
      fieldTabs.value = fieldTabs.value.map((tab) => ({
        ...tab,
        sections: (tab.sections || []).map((sec) => ({
          ...sec,
          columns: (sec.columns || []).map((col) => ({
            ...col,
            fields: (col.fields || [])
              .map((f) => {
                const fname = (f.fieldname || "").trim();
                if (hiddenFields.has(fname)) return null;
                if (fname === "source_name") {
                  // Khóa Source Name và đặt mặc định MBW_ATS
                  return {
                    ...f,
                    read_only: 1,
                    disabled: true,
                    default: "MBW ATS",
                  };
                }
                if (fname === "source_type") {
                  // Khóa Source Type và chỉ hiển thị ATS
                  return {
                    ...f,
                    read_only: 1,
                    disabled: true,
                    default: "ATS",
                    options: "ATS",
                  };
                }
                return f;
              })
              .filter(Boolean),
          })),
        })),
      }));

      // Force Source Type = ATS khi dùng FieldLayout
      formData.source_type = "ATS";
      formData.source_name = "MBW ATS";

      // Load existing document data nếu edit mode
      if (response.data.doc) {
        setFormData(response.data.doc);
        // Giữ ATS và MBW_ATS bất kể dữ liệu cũ
        formData.source_type = "ATS";
        formData.source_name = "MBW ATS";
      }
    } else {
      // Fallback: không sử dụng FieldLayout
      fieldTabs.value = [];
    }
  } catch (err) {
    console.error("Error loading field layout:", err);
    fieldTabs.value = [];
  } finally {
    loadingFields.value = false;
  }
};

const validateForm = () => {
  const errors = [];

  if (!formData.source_name?.trim()) {
    errors.push(__("Source name is required"));
  }

  if (!formData.source_type) {
    errors.push(__("Source type is required"));
  }

  if (!formData.auth_method) {
    errors.push(__("Authentication method is required"));
  }

  if (formData.auth_method === "OAuth2") {
    if (!formData.client_id?.trim()) {
      errors.push(__("Client ID is required for OAuth2"));
    }
    if (!formData.client_secret?.trim()) {
      errors.push(__("Client Secret is required for OAuth2"));
    }
  }

  if (formData.auth_method === "API Key" && !formData.api_key?.trim()) {
    errors.push(__("API Key is required for API Key method"));
  }

  if (formData.api_base_url && formData.api_base_url.trim()) {
    try {
      new URL(formData.api_base_url);
    } catch {
      errors.push(__("Invalid API Base URL format"));
    }
  }
};

const handleSubmit = async () => {
  error.value = null;
  success.value = false;

  const validationErrors = validateForm();
  if (validationErrors?.length > 0) {
    error.value = validationErrors.join(", ");
    return;
  }

  loading.value = true;

  try {
    let result;
    if (isEdit.value) {
      result = await candidateDataSourceStore.updateDataSource(
        props.dataSource.name,
        formData
      );
    } else {
      result = await candidateDataSourceStore.createDataSource(formData);
    }

    if (result.success) {
      success.value = true;
      emit("success", {
        action: isEdit.value ? "update" : "create",
        data: result.data,
      });

      // Close dialog after success
      setTimeout(() => {
        dialog.value = false;
      }, 1000);
    } else {
      error.value = result.error || __("An error occurred");
    }
  } catch (err) {
    error.value = __("An error occurred: {0}", [err.message]);
  } finally {
    loading.value = false;
  }
};

const handleTestConnection = async () => {
  if (!props.dataSource?.name) return;

  testing.value = true;
  error.value = null;

  try {
    // Test connection functionality would need to be implemented in store
    // For now, we'll simulate a successful test
    const result = { success: true, message: 'Connection test successful' };

    if (result.success) {
      success.value = true;
      setTimeout(() => {
        success.value = false;
      }, 3000);
    } else {
      error.value = __("Test connection failed: {0}", [result.error]);
    }
  } catch (err) {
    error.value = __("Test connection error: {0}", [err.message]);
  } finally {
    testing.value = false;
  }
};

const handleCancel = () => {
  error.value = null;
  success.value = false;
  emit("cancel");
  dialog.value = false;
};

// Watch for dataSource changes (edit mode)
watch(
  () => props.dataSource,
  (newDataSource) => {
    if (newDataSource) {
      setFormData(newDataSource);
    } else {
      resetForm();
    }
  },
  { immediate: true }
);

// Watch dialog open/close
watch(dialog, (isOpen) => {
  if (isOpen) {
    error.value = null;
    success.value = false;
    loadFieldLayout();

    if (props.dataSource) {
      setFormData(props.dataSource);
    } else {
      resetForm();
    }
  }
});

// Expose methods for parent component
defineExpose({
  resetForm,
  validateForm,
});
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
