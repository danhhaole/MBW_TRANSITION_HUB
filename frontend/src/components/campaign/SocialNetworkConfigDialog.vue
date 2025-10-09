<template>
  <Dialog
    v-model="show"
    :options="{ title: __('Social Network Configuration'), size: 'lg' }"
  >
    <template #body-content>
      <div class=" space-y-4">
        <!-- Loading State -->
        <div v-if="isDataLoading" class="flex items-center justify-center py-8">
          <div class="flex items-center space-x-3">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span class="text-sm text-gray-600">
              {{ __('Loading data...') }}
            </span>
          </div>
        </div>
        
        <!-- Form Content -->
        <div v-show="!isDataLoading" class="space-y-4">
        <!-- Modal Header with Close Button -->

        <!-- Select Social Page -->
        <FormControl
          type="select"
          :label="__('Select Social Page')"
          v-model="configData.page_id"
          :options="socialPageOptions"
          :placeholder="loadingPages ? __('Loading pages...') : __('Select a page...')"
          :loading="loadingPages"
          :key="socialPageOptions.length"
        />

        <!-- Schedule -->
        <FormControl
          type="datetime-local"
          :label="__('Time Post News')"
          v-model="configData.scheduled_at"
          :min="minScheduledAt"
          :step="60"
        />

        <!-- Job Opening -->
        <FormControl
          type="select"
          :label="__('Job Opening (optional)')"
          v-model="configData.job_opening"
          :options="jobOpeningOptions"
          :placeholder="loadingJobOpenings ? __('Loading job openings...') : __('Select a job opening...')"
          :loading="loadingJobOpenings"
          :key="jobOpeningOptions.length"
          @change="handleJobOpeningChange"
        />

        <!-- Template Content -->
        <!-- <FormControl
          type="textarea"
          :label="__('Template Content')"
          v-model="configData.template_content"
          :placeholder="__('Enter template content for this step...')"
          :rows="4"
        >
      </FormControl> -->
      <TextEditor
      ref="content"
				variant="outline"
				:class="'w-full'"
        :bubbleMenu="true"
				:fixedMenu="true"
        :placeholder="__('Enter your template content...')"
        :content="configData.template_content"
        @change="configData.template_content = $event"
        editor-class="!prose-sm !w-full overflow-auto !max-w-full min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
/>

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
            <FormControl
              type="text"
              :label="__('Image URL')"
              v-model="configData.image"
              :placeholder="__('https://...')"
              size="sm"
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
        </div> <!-- End Form Content -->
        
      </div>
    </template>
    <template #actions>
      <div class="flex items-center justify-end gap-2">
      
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
          :loading="saving || isDataLoading"
          :disabled="saving || isDataLoading"
        >
          {{ buttonText }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch, nextTick } from "vue";
import { Dialog, Button, FeatherIcon, FormControl, TextEditor, call } from "frappe-ui";
import ImageUploader from "@/components/Controls/ImageUploader.vue";
import { useCampaignSocialStore } from "@/stores/campaignSocial";
import { useRouter } from "vue-router";

const router = useRouter();

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
    default: '',
  },
  mode: {
    type: String,
    default: 'wizard', // 'wizard' or 'detail'
  },
  campaignId: {
    type: String,
    default: null,
  },
  campaignSocialId: {
    type: String,
    default: null,
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

// Store
const campaignSocialStore = useCampaignSocialStore();

// Reactive state
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

const saving = ref(false);
const forceShowForm = ref(false);

// Fallback timeout to show form after 5 seconds
let loadingTimeout = null;

// Computed loading state
const isDataLoading = computed(() => {
  if (forceShowForm.value) {
    console.log('🔴 Force showing form due to timeout');
    return false;
  }
  
  const loading = props.loadingPages || props.loadingJobOpenings;
  console.log('🔍 isDataLoading computed:', {
    loadingPages: props.loadingPages,
    loadingJobOpenings: props.loadingJobOpenings,
    result: loading
  });
  return loading;
});

// Computed to check if data is ready
const isDataReady = computed(() => {
  return !isDataLoading.value && 
         (socialPageOptions.value.length > 0 || jobOpeningOptions.value.length > 0);
});

// Computed button text based on mode
const buttonText = computed(() => {
  if (saving.value) {
    return props.mode === 'detail' ? __("Saving...") : __("Creating...");
  }
  if (isDataLoading.value) {
    return __("Loading...");
  }
  return props.mode === 'detail' ? __("Save") : __("Continue");
});

// Local config data
const configData = ref({
  page_id: "",
  scheduled_at: "",
  job_opening: "",
  image: "",
  template_content: "",
});

// Reactive options for FormControl selects
const socialPageOptions = ref([]);
const jobOpeningOptions = ref([]);

// Update socialPageOptions when props.socialPages changes
const updateSocialPageOptions = () => {
  console.log('🔍 Updating socialPageOptions...');
  console.log('props.socialPages:', props.socialPages);
  console.log('props.socialPages length:', props.socialPages?.length);
  
  if (!props.socialPages || props.socialPages.length === 0) {
    console.log('❌ No socialPages or empty array');
    socialPageOptions.value = [];
    return;
  }
  
  const options = props.socialPages.map(page => {
    console.log('🔄 Processing page:', page);
    return {
      label: `${page.account_name} (${page.account_type})`,
      value: page.external_account_id
    };
  });
  
  console.log('✅ Final socialPageOptions:', options);
  socialPageOptions.value = options;
};

// Update jobOpeningOptions when props.jobOpeningsList changes
const updateJobOpeningOptions = () => {
  console.log('🔍 Updating jobOpeningOptions...');
  console.log('props.jobOpeningsList:', props.jobOpeningsList);
  console.log('props.jobOpeningsList length:', props.jobOpeningsList?.length);
  
  if (!props.jobOpeningsList || props.jobOpeningsList.length === 0) {
    console.log('❌ No jobOpeningsList or empty array');
    jobOpeningOptions.value = [];
    return;
  }
  
  const options = props.jobOpeningsList.map(job => {
    console.log('🔄 Processing job:', job);
    return {
      label: `${job.job_title} ${job.job_code ? `(${job.job_code})` : ''}`,
      value: job.name
    };
  });
  
  console.log('✅ Final jobOpeningOptions:', options);
  jobOpeningOptions.value = options;
};

// Get selected job opening details
const selectedJobOpening = computed(() => {
  if (!configData.value.job_opening || !props.jobOpeningsList) {
    return null;
  }
  return props.jobOpeningsList.find(job => job.name === configData.value.job_opening);
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

const handleJobOpeningChange = async () => {
  console.log('🔍 Job Opening Change Debug:');
  console.log('configData.value.job_opening:', configData.value.job_opening);
  console.log('selectedJobOpening.value:', selectedJobOpening.value);
  console.log('current template_content:', configData.value.template_content);
  
  // Auto-generate template content when job opening is selected
  if (selectedJobOpening.value && !configData.value.template_content?.trim()) {
    const jobName = selectedJobOpening.value.name;
    console.log('📝 Fetching job details for:', jobName);
    
    try {
      // Call API to get job opening details
      const jobDetails = await call('frappe.client.get', {
        doctype: 'JobOpening',
        name: jobName,
        fields: ['name', 'job_title', 'job_code', 'description', 'requirements', 'benefits', 'job_url_cms']
      });
      
      console.log('✅ Job details fetched:', jobDetails);
      
      // Generate template with full job details
      const template = generateJobTemplateFromDetails(jobDetails);
      configData.value.template_content = template;
      console.log('✅ Template generated from details:', template);
    } catch (error) {
      console.error('❌ Error fetching job details:', error);
      // Fallback to basic template
      const job = selectedJobOpening.value;
      const template = generateJobTemplate(job);
      configData.value.template_content = template;
      console.log('⚠️ Using fallback template:', template);
    }
  } else {
    console.log('⚠️ Template not generated. Reasons:');
    console.log('- selectedJobOpening exists:', !!selectedJobOpening.value);
    console.log('- template_content is empty:', !configData.value.template_content?.trim());
  }
  
  updateSocialConfig();
  emit("job-opening-change", configData.value.job_opening);
};

// Generate template content from full job details
const generateJobTemplateFromDetails = (jobDetails) => {
  const { job_title, job_code, description, requirements, benefits, job_url_cms } = jobDetails;

  // 🔹 Lấy base URL từ router (ví dụ http://ats.local:8080)
  const baseUrl = window.location.origin; // hoặc router.resolve("/") nếu muốn route-base
  // 🔹 Xác định path job base trong hệ thống
  const jobBasePath = "/mbw_mira/jobs";
  // 🔹 Làm sạch slug
  const slug = (job_url_cms || "").replace(/^\/+|\/+$/g, "");
  // 🔹 Ghép full URL
  const fullJobUrl = `${baseUrl}${jobBasePath}/${slug}`;

  // 🔹 Xây template HTML
  let template = `
    🚀 <strong>Cơ hội việc làm hấp dẫn:</strong> ${job_title}<br><br>
  `;

  if (job_code) {
    template += `💼 <strong>Mã công việc:</strong> ${job_code}<br><br>`;
  }

  if (description) {
    template += `📝 <strong>Mô tả công việc:</strong><br>${description}<br><br>`;
  }

  if (requirements) {
    template += `🎯 <strong>Yêu cầu:</strong><br>${requirements}<br><br>`;
  }

  if (benefits) {
    template += `🎁 <strong>Phúc lợi:</strong><br>${benefits}<br><br>`;
  }

  template += `
    ✨ Tham gia đội ngũ của chúng tôi và phát triển sự nghiệp cùng những cơ hội tuyệt vời!<br><br>
    📩 <strong>Apply ngay tại:</strong> <a href="${fullJobUrl}" target="_blank">${fullJobUrl}</a><br><br>
    #JobOpening #${job_title.replace(/\s+/g, "")} #Hiring #WorkWithUs
  `;

  return template.trim();
};


// Generate basic template content for job opening (fallback)
const generateJobTemplate = (job) => {
  const templates = [
    `🚀 Cơ hội việc làm hấp dẫn: ${job.job_title}\n\n` +
    `📍 Vị trí: ${job.job_title}\n` +
    `💼 Mã công việc: ${job.job_code || 'N/A'}\n\n` +
    `✨ Tham gia đội ngũ của chúng tôi và phát triển sự nghiệp cùng những cơ hội tuyệt vời!\n\n` +
    `🚀 Môi trường năng động, đồng nghiệp thân thiện, cơ hội thăng tiến rõ ràng!\n\n` +
    `📩 Apply ngay!\n\n` +
    `#JobOpening #${job.job_title.replace(/\s+/g, '')} #Hiring #WorkWithUs`,
    
    `🎆 Tuyển dụng: ${job.job_title}\n\n` +
    `📅 Mã JD: ${job.job_code || 'N/A'}\n` +
    `📍 Vị trí đầy tiềm năng và hấp dẫn!\n\n` +
    `🌟 Bạn sẽ được làm việc trong môi trường chuyên nghiệp, học hỏi và phát triển kỹ năng.\n\n` +
    `🚀 Môi trường năng động, đồng nghiệp thân thiện, cơ hội thăng tiến rõ ràng!\n\n` +
    `📩 Apply ngay!\n\n` +
    `#JobOpening #${job.job_title.replace(/\s+/g, '')} #Hiring #WorkWithUs`,
    
    `💼 VIỆC LÀM HOT: ${job.job_title}\n\n` +
    `🌟 Bạn đang tìm kiếm cơ hội mới? Đây chính là dành cho bạn!\n\n` +
    `📌 Vị trí: ${job.job_title}\n` +
    `🏷️ Mã: ${job.job_code || 'Updating...'}\n\n` +
    `🚀 Môi trường năng động, đồng nghiệp thân thiện, cơ hội thăng tiến rõ ràng!\n\n` +
    `📩 Apply ngay!\n\n` +
    `#JobOpening #${job.job_title.replace(/\s+/g, '')} #Hiring #WorkWithUs`
  ];
  
  // Random template để tạo sự đa dạng
  return templates[Math.floor(Math.random() * templates.length)];
};

const updateSocialConfig = () => {
  // Don't emit if we're updating from props to prevent recursion
  if (!isUpdatingFromProps) {
    emit("update:socialConfig", { ...configData.value });
  }
};

const handleConfirm = async () => {
  if (!props.campaignId) {
    // If no campaign ID, just emit the config (for wizard mode)
    updateSocialConfig();
    emit("confirm", { ...configData.value });
    show.value = false;
    return;
  }

  saving.value = true;
  try {
    const socialData = {
      campaign_id: props.campaignId,
      social_page_id: configData.value.page_id,
      social_page_name: props.socialPages.find(
        (p) => p.external_account_id === configData.value.page_id
      )?.account_name || '',
      post_schedule_time: configData.value.scheduled_at || null,
      template_content: configData.value.template_content || '',
      social_media_images: configData.value.image || ''
    };

    let result;
    if (props.campaignSocialId) {
      // Update existing CampaignSocial
      result = await campaignSocialStore.updateCampaignSocial(
        props.campaignSocialId,
        socialData
      );
      console.log('✅ CampaignSocial updated:', props.campaignSocialId);
    } else {
      // Create new CampaignSocial
      result = await campaignSocialStore.createCampaignSocial(socialData);
      console.log('✅ CampaignSocial created:', result.name);
    }

    updateSocialConfig();
    emit("confirm", { ...configData.value, campaignSocialId: result.name });
    show.value = false;
  } catch (error) {
    console.error('❌ Error saving CampaignSocial:', error);
    alert(__('Failed to save social configuration. Please try again.'));
  } finally {
    saving.value = false;
  }
};

const handleCancel = () => {
  show.value = false;
  emit("cancel");
};

// Watch for prop changes (prevent recursive updates)
let isUpdatingFromProps = false;
watch(
  () => props.socialConfig,
  (newConfig) => {
    if (newConfig && !isUpdatingFromProps) {
      isUpdatingFromProps = true;
      configData.value = { ...newConfig };
      // Use nextTick to reset flag after update
      nextTick(() => {
        isUpdatingFromProps = false;
      });
    }
  },
  { immediate: true, deep: true }
);

// Watch for socialPages changes and update options
watch(
  () => props.socialPages,
  (newPages) => {
    console.log('🔄 socialPages changed:', newPages);
    updateSocialPageOptions();
    console.log('🔄 socialPageOptions updated:', socialPageOptions.value);
  },
  { immediate: true, deep: true }
);

// Watch for jobOpeningsList changes and update options
watch(
  () => props.jobOpeningsList,
  (newJobs) => {
    console.log('🔄 jobOpeningsList changed:', newJobs);
    updateJobOpeningOptions();
    console.log('🔄 jobOpeningOptions updated:', jobOpeningOptions.value);
  },
  { immediate: true, deep: true }
);

// Watch for config changes and emit updates (with debounce to prevent recursion)
let updateTimeout = null;
watch(
  configData,
  (newConfig) => {
    // Debounce to prevent recursive updates
    if (updateTimeout) {
      clearTimeout(updateTimeout);
    }
    updateTimeout = setTimeout(() => {
      updateSocialConfig();
    }, 100);
  },
  { deep: true }
);

// Watch for show changes to set default scheduled time and timeout
watch(show, (newShow) => {
  if (newShow) {
    // Reset force show form
    forceShowForm.value = false;
    
    // Set default scheduled time
    if (!configData.value.scheduled_at) {
      const now = new Date();
      const plus30m = new Date(now.getTime() + 30 * 60 * 1000);
      const year = plus30m.getFullYear();
      const month = String(plus30m.getMonth() + 1).padStart(2, '0');
      const day = String(plus30m.getDate()).padStart(2, '0');
      const hours = String(plus30m.getHours()).padStart(2, '0');
      const minutes = String(plus30m.getMinutes()).padStart(2, '0');
      configData.value.scheduled_at = `${year}-${month}-${day}T${hours}:${minutes}`;
    }
    
    // Set timeout to force show form after 5 seconds
    loadingTimeout = setTimeout(() => {
      console.log('⏰ Loading timeout reached, forcing form to show');
      forceShowForm.value = true;
    }, 5000);
  } else {
    // Clear timeout when modal closes
    if (loadingTimeout) {
      clearTimeout(loadingTimeout);
      loadingTimeout = null;
    }
    forceShowForm.value = false;
  }
});

console.log('🔍 SocialNetworkConfigDialog Props Debug:');
console.log('socialPages:', props.socialPages);
console.log('jobOpeningsList:', props.jobOpeningsList);
console.log('loadingPages:', props.loadingPages);
console.log('loadingJobOpenings:', props.loadingJobOpenings);
console.log('socialPageOptions:', socialPageOptions.value);
console.log('jobOpeningOptions:', jobOpeningOptions.value);
</script>
