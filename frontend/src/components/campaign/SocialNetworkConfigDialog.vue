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
        
        <!-- Progress Indicator (only in detail mode) -->
        <div v-if="props.mode === 'detail'" class="mb-6">
          <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
            <span>{{ __('Progress') }}</span>
            <span>{{ currentStep }}/2</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${(currentStep / 2) * 100}%` }"
            ></div>
          </div>
        </div>

        <!-- Step 1: Choose Where to Post (only in detail mode) -->
        <div v-if="props.mode === 'detail'" class="space-y-4">
          <label class="block text-sm font-medium text-gray-700">
            {{ __('Step 1: Choose Where to Post') }}
          </label>
          
          <!-- Loading State -->
          <div v-if="loadingInternalConnections" class="flex items-center justify-center py-8">
            <div class="flex items-center space-x-3">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
              <span class="text-sm text-gray-600">{{ __('Loading connections...') }}</span>
            </div>
          </div>
          
          <!-- No Connections -->
          <div v-else-if="!internalExternalConnections.length" class="text-center py-8">
            <div class="text-gray-500 mb-2">{{ __('No social media connections available') }}</div>
            <p class="text-xs text-gray-400">{{ __('Please connect your social media accounts first') }}</p>
          </div>
          
          <!-- External Connections Grid -->
          <div v-else class="grid grid-cols-1 gap-3">
            <div
              v-for="connection in internalExternalConnections"
              :key="connection.name"
              class="border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md"
              :class="configData.external_connection === connection.name ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
              @click="selectConnection(connection)"
            >
              <div class="flex items-center">
                <FeatherIcon
                  :name="getPlatformIcon(connection.platform_type)"
                  class="h-6 w-6 mr-3"
                  :class="configData.external_connection === connection.name ? 'text-blue-600' : 'text-gray-400'"
                />
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-900">
                    {{ connection.tenant_name || connection.name }}
                  </div>
                  <div class="text-xs text-gray-500">
                    {{ connection.platform_type }} • {{ connection.connection_status }}
                  </div>
                </div>
                <div v-if="configData.external_connection === connection.name" class="ml-2">
                  <FeatherIcon name="check-circle" class="h-5 w-5 text-blue-600" />
                </div>
              </div>
            </div>
          </div>
          
          <!-- Social Pages (show when connection selected) -->
          <div v-if="configData.external_connection" class="space-y-3">
            <label class="block text-sm font-medium text-gray-700">
              {{ __('Choose Page/Profile') }}
            </label>
            
            <!-- Loading Pages -->
            <div v-if="loadingInternalPages" class="flex items-center justify-center py-4">
              <div class="flex items-center space-x-2">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                <span class="text-sm text-gray-600">{{ __('Loading pages...') }}</span>
              </div>
            </div>
            
            <!-- No Pages -->
            <div v-else-if="!internalSocialPages.length" class="text-center py-4">
              <div class="text-gray-500 text-sm">{{ __('No pages available for this connection') }}</div>
            </div>
            
            <!-- Social Pages Grid -->
            <div v-else class="grid grid-cols-1 gap-2">
              <div
                v-for="page in internalSocialPages"
                :key="page.external_account_id"
                class="border rounded-lg p-3 cursor-pointer transition-all duration-200 hover:shadow-sm"
                :class="configData.page_id === page.external_account_id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                @click="selectPage(page)"
              >
                <div class="flex items-center">
                  <div class="flex-1">
                    <div class="text-sm font-medium text-gray-900">
                      {{ page.account_name }}
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ page.account_type }}
                    </div>
                  </div>
                  <div v-if="configData.page_id === page.external_account_id" class="ml-2">
                    <FeatherIcon name="check-circle" class="h-4 w-4 text-blue-600" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Choose Page (wizard mode only) -->
        <div v-if="props.mode === 'wizard'" class="space-y-4">
          <label class="block text-sm font-medium text-gray-700">
            {{ __('Choose Page/Profile') }}
          </label>
          
          <!-- Loading Pages -->
          <div v-if="loadingInternalPages" class="flex items-center justify-center py-4">
            <div class="flex items-center space-x-2">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <span class="text-sm text-gray-600">{{ __('Loading pages...') }}</span>
            </div>
          </div>
          
          <!-- No Pages -->
          <div v-else-if="!internalSocialPages.length" class="text-center py-4">
            <div class="text-gray-500 text-sm">{{ __('No pages available for this connection') }}</div>
          </div>
          
          <!-- Social Pages Grid -->
          <div v-else class="grid grid-cols-1 gap-2">
            <div
              v-for="page in internalSocialPages"
              :key="page.external_account_id"
              class="border rounded-lg p-3 cursor-pointer transition-all duration-200 hover:shadow-sm"
              :class="configData.page_id === page.external_account_id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
              @click="selectPage(page)"
            >
              <div class="flex items-center">
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-900">
                    {{ page.account_name }}
                  </div>
                  <div class="text-xs text-gray-500">
                    {{ page.account_type }}
                  </div>
                </div>
                <div v-if="configData.page_id === page.external_account_id" class="ml-2">
                  <FeatherIcon name="check-circle" class="h-4 w-4 text-blue-600" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Post Information -->
        <div v-if="props.mode === 'wizard' ? configData.page_id : (props.mode === 'wizard' || configData.page_id)" class="space-y-4">
          <label class="block text-sm font-medium text-gray-700">
            {{ props.mode === 'wizard' ? __('Post Information') : __('Step 2: Post Information') }}
          </label>
          
          <!-- Schedule -->
          <FormControl
            type="datetime-local"
            :label="__('Schedule Time')"
            v-model="configData.scheduled_at"
            :min="minScheduledAt"
            :step="60"
          />

          <!-- Job Opening (optional) -->
          <FormControl
            type="select"
            :label="__('Job Opening (Optional)')"
            v-model="configData.job_opening"
            :options="jobOpeningOptions"
            :placeholder="loadingJobOpenings ? __('Loading job openings...') : __('Select a job opening...')"
            :loading="loadingJobOpenings"
            :key="jobOpeningOptions.length"
            @change="handleJobOpeningChange"
          />

          <!-- Content -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              {{ __('Post Content') }}
            </label>
            <TextEditor
              ref="content"
              variant="outline"
              :class="'w-full'"
              :bubbleMenu="true"
              :fixedMenu="true"
              :placeholder="__('Enter your post content...')"
              :content="configData.template_content"
              @change="configData.template_content = $event"
              editor-class="!prose-sm !w-full overflow-auto !max-w-full min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
            />
          </div>

          <!-- Image (optional) -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">
              {{ __("Post Image (Optional)") }}
            </label>
            <ImageUploader
              :image_url="configData.image"
              image_type="image/*"
              @upload="handleImageUpload"
              @remove="handleImageRemove"
            />
            <!-- Image URL input -->
            <FormControl
              type="text"
              :label="__('Image URL')"
              v-model="configData.image"
              :placeholder="__('https://...')"
              size="sm"
            />
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
          :disabled="saving || isDataLoading || !canSubmit"
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
const campaignSocialStore = useCampaignSocialStore();

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  socialConfig: {
    type: Object,
    default: () => ({
      external_connection: "",
      page_id: "",
      scheduled_at: "",
      job_opening: "",
      image: "",
      template_content: "",
    }),
  },
  mode: {
    type: String,
    default: 'detail', // 'wizard' or 'detail'
  },
  socialPages: {
    type: Array,
    default: () => [],
  },
  externalConnections: {
    type: Array,
    default: () => [],
  },
  loadingConnections: {
    type: Boolean,
    default: false,
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

// Store (already declared above)

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
  
  // In detail mode, also wait for connections to load
  const connectionsLoading = props.mode === 'detail' ? props.loadingConnections : false;
  const loading = props.loadingPages || props.loadingJobOpenings || connectionsLoading;
  
  console.log('🔍 isDataLoading computed:', {
    mode: props.mode,
    loadingPages: props.loadingPages,
    loadingJobOpenings: props.loadingJobOpenings,
    loadingConnections: props.loadingConnections,
    connectionsLoading,
    result: loading
  });
  return loading;
});

// Computed to check if data is ready
const isDataReady = computed(() => {
  return !isDataLoading.value && 
         (socialPageOptions.value.length > 0 || jobOpeningOptions.value.length > 0);
});

// Computed button text based on mode and whether editing existing record
const buttonText = computed(() => {
  if (saving.value) {
    if (props.campaignSocialId) {
      return __("Saving...");
    } else {
      return __("Creating...");
    }
  }

  console.log('🔴 buttonText computed:', {
    mode: props.mode,
    saving: saving.value,
    campaignSocialId: props.campaignSocialId,
    result: buttonText.value
  });
  
  // Not saving
  if (props.mode === 'wizard' ) {
    return props.campaignSocialId ? __("Update Post") : __("Create Post");
  } else {
    // Detail mode: check if editing existing or creating new
    if (props.campaignSocialId) {
      return __("Save Changes");
    } else {
      return __("Create Post");
    }
  }
});

// Check if form can be submitted
const canSubmit = computed(() => {
  if (props.mode === 'wizard') {
    // Wizard mode: chỉ cần schedule và content
    return configData.value.scheduled_at && configData.value.template_content?.trim();
  } else {
    // Detail mode: cần đầy đủ thông tin
    return configData.value.external_connection && 
           configData.value.page_id && 
           configData.value.scheduled_at &&
           configData.value.template_content?.trim();
  }
});

// Calculate current step for progress indicator (simplified to 2 steps)
const currentStep = computed(() => {
  let step = 0;
  // Step 1: Choose where to post (connection + page)
  if (configData.value.external_connection && configData.value.page_id) step++;
  // Step 2: Post information (schedule + content)
  if (configData.value.scheduled_at && configData.value.template_content?.trim()) step++;
  return step;
});

// Local config data
const configData = ref({
  external_connection: "",
  page_id: "",
  scheduled_at: "",
  job_opening: "",
  image: "",
  template_content: "",
});

// Internal data management (like CampaignWizard)
const internalExternalConnections = ref([]);
const internalSocialPages = ref([]);
const loadingInternalConnections = ref(false);
const loadingInternalPages = ref(false);

// Reactive options for FormControl selects
const externalConnectionOptions = ref([]);
const socialPageOptions = ref([]);
const jobOpeningOptions = ref([]);

// Load external connections (like CampaignWizard)
const loadExternalConnections = async () => {
  try {
    loadingInternalConnections.value = true;
    const response = await call('frappe.client.get_list', {
      doctype: 'Mira External Connection',
      fields: ['name', 'tenant_name', 'platform_type', 'connection_status'],
      filters: [['connection_status', '=', 'Connected']],
      limit_page_length: 100
    });
    internalExternalConnections.value = response || [];
    updateExternalConnectionOptions();
    console.log('✅ SocialNetworkConfigDialog: Loaded external connections:', internalExternalConnections.value.length);
  } catch (error) {
    console.error('❌ SocialNetworkConfigDialog: Error loading external connections:', error);
    internalExternalConnections.value = [];
  } finally {
    loadingInternalConnections.value = false;
  }
};

// Update externalConnectionOptions from internal data
const updateExternalConnectionOptions = () => {
  console.log('🔍 Updating externalConnectionOptions...');
  
  if (!internalExternalConnections.value || internalExternalConnections.value.length === 0) {
    console.log('❌ No internalExternalConnections or empty array');
    externalConnectionOptions.value = [];
    return;
  }
  
  const options = internalExternalConnections.value.map(conn => ({
    label: conn.tenant_name || conn.name,
    value: conn.name
  }));
  
  externalConnectionOptions.value = options;
  console.log('✅ externalConnectionOptions updated:', options);
};

// Load social pages for selected connection (like CampaignWizard)
const loadSocialPages = async () => {
  try {
    loadingInternalPages.value = true;
    internalSocialPages.value = [];
    
    if (!configData.value.external_connection) return;
    
    // Fetch accounts for this connection
    const res = await call("mbw_mira.api.external_connections.get_account_details", {
      connection_id: configData.value.external_connection,
    });
    
    if (res && res.status === "success") {
      const accounts = Array.isArray(res.data) ? res.data : res.data ? [res.data] : [];
      // Only active pages/users; prefer Page
      internalSocialPages.value = accounts.filter((a) => a.connection_status !== "Revoked");
      updateInternalSocialPageOptions();
    }
  } catch (e) {
    console.warn("Failed to load social pages", e);
    internalSocialPages.value = [];
  } finally {
    loadingInternalPages.value = false;
  }
};

// Update socialPageOptions from internal data
const updateInternalSocialPageOptions = () => {
  if (!internalSocialPages.value || internalSocialPages.value.length === 0) {
    socialPageOptions.value = [];
    return;
  }
  
  const options = internalSocialPages.value.map(page => ({
    label: `${page.account_name} (${page.account_type})`,
    value: page.external_account_id
  }));
  
  socialPageOptions.value = options;
  console.log('✅ Internal socialPageOptions updated:', options);
};

// Handle connection selection (card click)
const selectConnection = (connection) => {
  configData.value.external_connection = connection.name;
  configData.value.page_id = ""; // Reset page selection
  loadSocialPages(); // Load pages for selected connection
};

// Handle page selection (card click)
const selectPage = (page) => {
  configData.value.page_id = page.external_account_id;
};

// Get platform icon (like CampaignWizard)
const getPlatformIcon = (platformType) => {
  const iconMap = {
    Facebook: "facebook",
    LinkedIn: "linkedin", 
    Twitter: "twitter",
    Instagram: "instagram",
    Zalo: "message-circle",
    TopCV: "briefcase"
  };
  return iconMap[platformType] || "share-2";
};

// Handle connection change - load social pages for selected connection
const handleConnectionChange = () => {
  console.log('🔄 Connection changed:', configData.value.external_connection);
  
  // Reset page selection when connection changes
  configData.value.page_id = "";
  
  // Load social pages for the selected connection
  if (configData.value.external_connection) {
    loadSocialPages();
  } else {
    socialPageOptions.value = [];
  }
};

// Update socialPageOptions when props.socialPages changes
const updateSocialPageOptions = () => {
  console.log('🔍 Updating socialPageOptions...');
  console.log('props.socialPages:', props.socialPages);
  console.log('props.socialPages length:', props.socialPages?.length);
  console.log('mode:', props.mode);
  
  if (!props.socialPages || props.socialPages.length === 0) {
    console.log('❌ No socialPages or empty array');
    socialPageOptions.value = [];
    return;
  }
  
  // In wizard mode, use all available pages (already filtered by connection)
  // In detail mode, filter by selected connection
  let pagesToUse = props.socialPages;
  
  if (props.mode === 'detail' && configData.value.external_connection) {
    pagesToUse = props.socialPages.filter(page => 
      page.parent_connection === configData.value.external_connection
    );
  }
  
  const options = pagesToUse.map(page => ({
    label: `${page.account_name} (${page.account_type})`,
    value: page.external_account_id
  }));
  
  socialPageOptions.value = options;
  console.log('✅ socialPageOptions updated:', options);
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
        doctype: "Mira Job Opening",
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
  // Wizard mode: không có campaignId, chỉ emit config
  if (props.mode === 'wizard' || !props.campaignId) {
    updateSocialConfig();
    emit("confirm", { ...configData.value });
    show.value = false;
    return;
  }

  saving.value = true;
  try {
    // Find selected connection from internal data
    const selectedConnection = internalExternalConnections.value.find(
      (conn) => conn.name === configData.value.external_connection
    );
    
    // Find selected page from internal data
    const selectedPage = internalSocialPages.value.find(
      (p) => p.external_account_id === configData.value.page_id
    );
    
    const socialData = {
      campaign_id: props.campaignId,
      external_connection: configData.value.external_connection,
      platform: selectedConnection?.platform_type || '',
      social_page_id: configData.value.page_id,
      social_page_name: selectedPage?.account_name || '',
      post_schedule_time: configData.value.scheduled_at || null,
      template_content: configData.value.template_content || '',
      social_media_images: configData.value.image || '',
      job_opening: configData.value.job_opening || '',
      status: 'Pending'
    };

    let result;
    if (props.campaignSocialId) {
      // Update existing Mira Campaign Social
      result = await campaignSocialStore.updateCampaignSocial(
        props.campaignSocialId,
        socialData
      );
      console.log('✅ Mira Campaign Social updated:', props.campaignSocialId);
    } else {
      // Create new Mira Campaign Social
      result = await campaignSocialStore.createCampaignSocial(socialData);
      console.log('✅ Mira Campaign Social created:', result.name);
    }

    updateSocialConfig();
    emit("confirm", { ...configData.value, campaignSocialId: result.name });
    show.value = false;
  } catch (error) {
    console.error('❌ Error saving Mira Campaign Social:', error);
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
      console.log('🔄 SocialConfig changed:', newConfig);
      isUpdatingFromProps = true;
      configData.value = { ...newConfig };
      console.log('✅ ConfigData updated:', configData.value);
      
      // If editing existing record with external_connection, load social pages
      if (newConfig.external_connection && props.mode === 'detail') {
        console.log('🔄 Loading social pages for connection:', newConfig.external_connection);
        loadSocialPages();
      }
      
      // Use nextTick to reset flag after update
      nextTick(() => {
        isUpdatingFromProps = false;
      });
    }
  },
  { immediate: true, deep: true }
);

// Watch for externalConnections changes and update options
watch(
  () => props.externalConnections,
  (newConnections) => {
    console.log('🔄 externalConnections changed:', newConnections);
    updateExternalConnectionOptions();
    console.log('🔄 externalConnectionOptions updated:', externalConnectionOptions.value);
  },
  { immediate: true }
);

// Watch for socialPages changes and update options
watch(
  () => props.socialPages,
  (newPages) => {
    console.log('🔄 socialPages changed:', newPages);
    updateSocialPageOptions();
    console.log('🔄 socialPageOptions updated:', socialPageOptions.value);
  },
  { immediate: true }
);

// Watch for jobOpeningsList changes and update options
watch(
  () => props.jobOpeningsList,
  (newJobs) => {
    console.log('🔄 jobOpeningsList changed:', newJobs);
    updateJobOpeningOptions();
    console.log('🔄 jobOpeningOptions updated:', jobOpeningOptions.value);
  },
  { immediate: true }
);

// Watch for config changes and emit updates (with debounce to prevent recursion)
let updateTimeout = null;
watch(
  configData,
  (newConfig) => {
    // Don't emit if we're updating from props to prevent recursion
    if (isUpdatingFromProps) {
      return;
    }
    
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
    
    // Load external connections when dialog opens (detail mode only)
    if (props.mode === 'detail') {
      loadExternalConnections();
      
      // If editing with existing external_connection, also load social pages
      if (configData.value.external_connection) {
        // Wait a bit for connections to load first
        setTimeout(() => {
          loadSocialPages();
        }, 500);
      }
    } else if (props.mode === 'wizard') {
      // Wizard mode: external_connection should come from selectedDataSource
      // Load social pages directly
      if (configData.value.external_connection) {
        loadSocialPages();
      }
    }
    
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
