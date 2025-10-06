<template>
  <Dialog
    v-model="show"
    :options="{ title: __('Social Network Configuration'), size: 'lg' }"
  >
    <template #body>
      <div class="p-6 space-y-4">
        <!-- Modal Header with Close Button -->
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center space-x-2">
            <FeatherIcon name="users" class="h-5 w-5 text-blue-600" />
            <h3 class="text-base font-medium text-gray-900">
              {{ __("Select Page & Schedule") }}
            </h3>
          </div>
          <Button
            theme="gray"
            variant="ghost"
            class="w-7 h-7"
            @click="handleCancel"
          >
            <FeatherIcon name="x" class="h-4 w-4" />
          </Button>
        </div>

        <!-- Select Social Page -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Select Social Page") }}
          </label>
          <select
            v-model="configData.page_id"
            :disabled="loadingPages"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">{{ __("Select a page...") }}</option>
            <option
              v-for="p in socialPages"
              :key="p.external_account_id"
              :value="p.external_account_id"
            >
              {{ p.account_name }} ({{ p.account_type }})
            </option>
          </select>
        </div>

        <!-- Schedule -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Time Post News") }}
          </label>
          <input
            v-model="configData.scheduled_at"
            type="datetime-local"
            :min="minScheduledAt"
            :step="60"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
          <p class="mt-1 text-xs text-gray-500">
            {{ __("Local time") }} ({{ localTzLabel }})
          </p>
        </div>

        <!-- Job Opening -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Job Opening (optional)") }}
          </label>
          <select
            v-model="configData.job_opening"
            :disabled="loadingJobOpenings"
            @change="handleJobOpeningChange"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            <option value="">{{ __("Select a job opening...") }}</option>
            <option v-for="job in jobOpeningsList" :key="job.name" :value="job.name">
              {{ job.job_title }} {{ job.job_code ? `(${job.job_code})` : "" }}
            </option>
          </select>
        </div>

        <!-- Template Content -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Template Content") }}
          </label>
          <textarea
            v-model="configData.template_content"
            rows="4"
            :placeholder="__('Enter template content for this step...')"
            class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          />
          <p class="mt-1 text-sm text-gray-500">
            {{ __("Content template for emails, SMS, or other actions") }}
          </p>
        </div>

        <!-- Image Uploader -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ __("Step Image (optional)") }}
          </label>
          <ImageUploader
            :image_url="configData.image"
            image_type="image/*"
            @upload="handleImageUpload"
            @remove="handleImageRemove"
          />
          <!-- Image URL input -->
          <div class="mt-2">
            <label class="block text-xs font-medium text-gray-500 mb-1">{{
              __("Image URL")
            }}</label>
            <input
              v-model="configData.image"
              type="text"
              placeholder="https://..."
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <!-- Preview -->
          <div v-if="configData.image" class="mt-3">
            <label class="block text-xs font-medium text-gray-500 mb-1">{{
              __("Preview")
            }}</label>
            <img
              :src="configData.image"
              alt="Preview"
              class="max-h-40 rounded border"
            />
          </div>
        </div>

        <!-- Inline Actions -->
        <div class="flex items-center justify-end gap-2 pt-2">
          <Button
            variant="outline"
            theme="gray"
            @click="handleCancel"
          >
            {{ __("Cancel") }}
          </Button>
          <Button 
            variant="solid" 
            theme="gray" 
            @click="handleConfirm"
          >
            {{ __("Continue") }}
          </Button>
        </div>
      </div>
    </template>
    <template #actions>
      <div class="flex items-center gap-2 p-3">
        <Button 
          variant="outline" 
          theme="gray" 
          @click="handleCancel"
        >
          {{ __("Cancel") }}
        </Button>
        <Button 
          variant="solid" 
          theme="gray" 
          @click="handleConfirm"
        >
          {{ __("Continue") }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { Dialog, Button, FeatherIcon } from "frappe-ui";
import ImageUploader from "@/components/Controls/ImageUploader.vue";

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  socialConfig: {
    type: Object,
    default: () => ({
      page_id: "",
      scheduled_at: "",
      job_opening: "",
      image: "",
      template_content: "",
    }),
  },
  socialPages: {
    type: Array,
    default: () => [],
  },
  jobOpeningsList: {
    type: Array,
    default: () => [],
  },
  loadingPages: {
    type: Boolean,
    default: false,
  },
  loadingJobOpenings: {
    type: Boolean,
    default: false,
  },
  minScheduledAt: {
    type: String,
    default: "",
  },
  localTzLabel: {
    type: String,
    default: "",
  },
});

// Emits
const emit = defineEmits([
  "update:modelValue",
  "update:socialConfig",
  "confirm",
  "cancel",
  "job-opening-change",
]);

// Translation helper
const __ = (text) => text;

// Reactive state
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

// Local config data
const configData = ref({
  page_id: "",
  scheduled_at: "",
  job_opening: "",
  image: "",
  template_content: "",
});

// Methods
const handleImageUpload = (url) => {
  configData.value.image = url;
  updateSocialConfig();
};

const handleImageRemove = () => {
  configData.value.image = "";
  updateSocialConfig();
};

const handleJobOpeningChange = () => {
  updateSocialConfig();
  emit("job-opening-change", configData.value.job_opening);
};

const updateSocialConfig = () => {
  emit("update:socialConfig", { ...configData.value });
};

const handleConfirm = async () => {
  updateSocialConfig();
  emit("confirm", { ...configData.value });
  show.value = false;
};

const handleCancel = () => {
  show.value = false;
  emit("cancel");
};

// Watch for prop changes
watch(
  () => props.socialConfig,
  (newConfig) => {
    if (newConfig) {
      configData.value = { ...newConfig };
    }
  },
  { immediate: true, deep: true }
);

// Watch for config changes and emit updates
watch(
  configData,
  (newConfig) => {
    updateSocialConfig();
  },
  { deep: true }
);

// Watch for show changes to set default scheduled time
watch(show, (newShow) => {
  if (newShow && !configData.value.scheduled_at) {
    const now = new Date();
    const plus30m = new Date(now.getTime() + 30 * 60 * 1000);
    const year = plus30m.getFullYear();
    const month = String(plus30m.getMonth() + 1).padStart(2, '0');
    const day = String(plus30m.getDate()).padStart(2, '0');
    const hours = String(plus30m.getHours()).padStart(2, '0');
    const minutes = String(plus30m.getMinutes()).padStart(2, '0');
    configData.value.scheduled_at = `${year}-${month}-${day}T${hours}:${minutes}`;
  }
});
</script>
