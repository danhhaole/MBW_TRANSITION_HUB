<template>
  <div class="space-y-4">
      <!-- Description -->


      <!-- Fields Info -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">

      </div>

      <!-- Existing Configs List -->
      <div v-if="configs.length > 0" class="space-y-3">
        <h5 class="text-sm font-medium text-gray-700">{{ __('Current Configurations') }}</h5>
        <div 
          v-for="(config, index) in configs" 
          :key="index"
          :class="[
            'border rounded-lg p-4',
            editingIndex === index ? 'border-blue-300 bg-blue-50' : 'border-gray-200 bg-gray-50'
          ]"
        >
          <!-- Config Header -->
          <div v-if="editingIndex !== index" class="flex items-center justify-between mb-2">
            <div class="flex items-center">
              <FeatherIcon 
                :name="config.type === 'Email' ? 'mail' : 'globe'" 
                class="h-4 w-4 mr-2"
                :class="config.type === 'Email' ? 'text-blue-600' : 'text-green-600'"
              />
              <span class="text-sm font-medium">
                {{ config.type === 'Email' ? __('Email Notification') : __('API Webhook') }}
              </span>
            </div>
            <div class="flex gap-1">
              <Button
                @click="editConfig(index)"
                variant="ghost"
                size="sm"
                class="text-blue-600 hover:text-blue-700"
              >
                <FeatherIcon name="edit-2" class="h-3 w-3" />
              </Button>
              <Button
                @click="removeConfig(index)"
                variant="ghost"
                size="sm"
                class="text-red-600 hover:text-red-700"
              >
                <FeatherIcon name="trash-2" class="h-3 w-3" />
              </Button>
            </div>
          </div>
          
          <!-- Config Details (View Mode) -->
          <div v-if="editingIndex !== index" class="text-xs text-gray-600 space-y-2">
            <div v-if="config.type === 'Email'">
              <div><strong>{{ __('Email:') }}</strong> {{ config.email }}</div>
            </div>
            <div v-else>
              <div><strong>{{ __('Endpoint:') }}</strong> {{ config.end_point }}</div>
              <div><strong>{{ __('Content Type:') }}</strong> {{ config.content_type }}</div>
              
              <!-- API Headers -->
              <div v-if="config.api_headers && Object.keys(config.api_headers).length > 0">
                <strong>{{ __('Headers:') }}</strong>
                <div class="mt-1 space-y-1">
                  <div 
                    v-for="(value, key) in config.api_headers" 
                    :key="key"
                    class="text-xs bg-white px-2 py-1 rounded border"
                  >
                    <span class="font-medium">{{ key }}:</span> {{ value }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Field Mappings -->
            <!-- <div v-if="config.field_mappings && config.field_mappings.length > 0">
              <strong>{{ __('Field Mappings:') }}</strong>
              <div class="mt-1 space-y-1">
                <div 
                  v-for="(mapping, mappingIndex) in config.field_mappings" 
                  :key="mappingIndex"
                  class="text-xs bg-white px-2 py-1 rounded border flex items-center"
                >
                  <span class="text-blue-600 font-medium">{{ mapping.form_field }}</span>
                  <FeatherIcon name="arrow-right" class="h-3 w-3 mx-2 text-gray-400" />
                  <span class="text-green-600 font-medium">{{ mapping.api_field }}</span>
                </div>
              </div>
            </div> -->
          </div>
          
          <!-- Inline Edit Form -->
          <div v-if="editingIndex === index" class="space-y-4">
            <div class="flex items-center justify-between mb-4">
              <h6 class="text-sm font-medium text-blue-900">
                <FeatherIcon name="edit-2" class="h-4 w-4 mr-2 inline" />
                {{ __('Editing Configuration') }}
              </h6>
              <div class="flex gap-2">
                <Button
                  @click="cancelEdit"
                  variant="ghost"
                  size="sm"
                  class="text-gray-600"
                >
                  {{ __('Cancel') }}
                </Button>
                <Button
                  @click="updateConfig"
                  :disabled="!canAddConfig"
                  variant="solid"
                  size="sm"
                >
                <div class="flex items-center">

                  <FeatherIcon name="save" class="h-3 w-3 mr-1" />
                  {{ __('Save Changes') }}
                </div>
                </Button>
              </div>
            </div>
            
            <!-- Inline Edit Fields (same as new config form) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Configuration Type -->
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Configuration Type') }}
                </label>
                <FormControl
                  v-model="newConfig.type"
                  type="select"
                  :options="configTypeOptions"
                  :placeholder="__('Select configuration type')"
                />
              </div>

              <!-- Email Configuration -->
              <div v-if="newConfig.type === 'Email'" class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  {{ __('Email Address') }}
                </label>
                <FormControl
                  v-model="newConfig.email"
                  type="email"
                  :placeholder="__('Enter email address')"
                />
              </div>

              <!-- API Configuration -->
              <template v-if="newConfig.type === 'API'">
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('API Endpoint') }}
                    <span class="text-xs text-green-600 ml-1">({{ __('Auto-generated') }})</span>
                  </label>
                  <div class="flex items-center gap-2 px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg">
                    <FeatherIcon name="link" class="h-4 w-4 text-gray-500 flex-shrink-0" />
                    <span class="text-sm text-gray-700 break-all">{{ newConfig.end_point || generatedEndpoint }}</span>
                    <Button
                      @click="copyEndpoint"
                      variant="ghost"
                      size="sm"
                      class="ml-auto flex-shrink-0"
                    >
                      <FeatherIcon name="copy" class="h-3 w-3" />
                    </Button>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ __('This endpoint will receive candidate data from landing page form') }}
                  </p>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Content Type') }}
                  </label>
                  <FormControl
                    v-model="newConfig.content_type"
                    type="select"
                    :options="contentTypeOptions"
                  />
                </div>

                <!-- API Headers -->
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('API Headers') }}
                  </label>
                  <div class="space-y-2">
                    <div 
                      v-for="(header, headerIndex) in newConfig.api_headers_list" 
                      :key="headerIndex"
                      class="flex gap-2"
                    >
                      <div class="flex-1">
                        <FormControl
                          v-model="header.key"
                          type="text"
                          :placeholder="__('Header name')"
                        />
                      </div>
                      <div class="flex-1">
                        <FormControl
                          v-model="header.value"
                          type="text"
                          :placeholder="__('Header value')"
                        />
                      </div>
                      <Button
                        @click="removeHeader(headerIndex)"
                        variant="ghost"
                        size="sm"
                        class="text-red-600"
                      >
                        <FeatherIcon name="x" class="h-3 w-3" />
                      </Button>
                    </div>
                    <Button
                      @click="addHeader"
                      variant="outline"
                      size="sm"
                      class="text-blue-600"
                    >
                    <div class="flex items-center">

                      <FeatherIcon name="plus" class="h-3 w-3 mr-1" />
                      {{ __('Add Header') }}
                    </div>
                    </Button>
                  </div>
                </div>

                <!-- Field Mappings -->
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ __('Field Mappings') }}
                    <span class="text-xs text-gray-500 ml-1">({{ __('Template Field → Mira Talent Field') }})</span>
                  </label>
                  
                  <!-- Debug Info -->
                  <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                    <span>Template Fields: {{ templateFields.length }} | Mira Talent Fields: {{ miraTalentFields.length }}</span>
                    <Button
                      @click="loadAllFields"
                      variant="ghost"
                      size="sm"
                      class="text-blue-600 text-xs"
                    >
                      <div class="flex items-center">
                        <FeatherIcon name="refresh-cw" class="h-3 w-3 mr-1" />
                        {{ __('Reload Fields') }}
                      </div>
                    </Button>
                  </div>
                  
                  <!-- Show message if fields not loaded -->
                  <div v-if="templateFields.length === 0 || miraTalentFields.length === 0" class="text-sm text-amber-600 bg-amber-50 p-2 rounded mb-2">
                    {{ templateFields.length === 0 ? 'Loading template fields...' : '' }}
                    {{ miraTalentFields.length === 0 ? 'Loading Mira Talent fields...' : '' }}
                  </div>
                  <div class="space-y-2">
                    <div 
                      v-for="(mapping, visibleIndex) in visibleFieldMappings" 
                      :key="visibleIndex"
                      class="flex gap-2"
                    >
                      <div class="flex-1">
                        <FormControl
                          v-model="newConfig.field_mappings[getOriginalMappingIndex(visibleIndex)].form_field"
                          type="select"
                          :options="templateFieldOptions"
                          :placeholder="__('Select template field')"
                        />
                      </div>
                      <div class="flex items-center px-2">
                        <FeatherIcon name="arrow-right" class="h-3 w-3 text-gray-400" />
                      </div>
                      <div class="flex-1">
                        <FormControl
                          v-model="newConfig.field_mappings[getOriginalMappingIndex(visibleIndex)].api_field"
                          type="select"
                          :options="miraTalentFieldOptions"
                          :placeholder="__('Select Mira Talent field')"
                        />
                      </div>
                      <Button
                        @click="removeMapping(getOriginalMappingIndex(visibleIndex))"
                        variant="ghost"
                        size="sm"
                        class="text-red-600"
                      >
                        <FeatherIcon name="x" class="h-3 w-3" />
                      </Button>
                    </div>
                    
                    <!-- Show message if no visible mappings yet -->
                    <div v-if="visibleFieldMappings.length === 0" class="text-sm text-gray-500 italic p-3 border border-dashed border-gray-300 rounded">
                      {{ __('No field mappings yet. Click "Add Mapping" to create one.') }}
                    </div>
                    
                    <!-- Add Mapping button -->
                    <div class="flex gap-2">
                      <Button
                        @click="addMapping"
                        variant="outline"
                        size="sm"
                        class="text-blue-600"
                      >
                        <div class="flex items-center">
                          <FeatherIcon name="plus" class="h-3 w-3 mr-1" />
                          {{ __('Add Mapping') }}
                        </div>
                      </Button>
                      <Button
                        @click="applyDefaultMappings"
                        variant="outline"
                        size="sm"
                        class="text-green-600"
                        :disabled="templateFields.length === 0"
                      >
                        <div class="flex items-center">
                          <FeatherIcon name="zap" class="h-3 w-3 mr-1" />
                          {{ __('Auto Map') }}
                        </div>
                      </Button>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Add New Config Form (only show when not editing existing) -->
      <div v-if="editingIndex < 0" class="border border-gray-200 rounded-lg p-4">
        <h5 class="text-sm font-medium text-gray-700 mb-3">{{ __('Add New Configuration') }}</h5>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Configuration Type -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Configuration Type') }}
            </label>
            <FormControl
              v-model="newConfig.type"
              type="select"
              :options="configTypeOptions"
              :placeholder="__('Select configuration type')"
            />
          </div>

          <!-- Email Configuration -->
          <div v-if="newConfig.type === 'Email'" class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              {{ __('Email Address') }}
            </label>
            <FormControl
              v-model="newConfig.email"
              type="email"
              :placeholder="__('Enter email address')"
            />
          </div>

          <!-- API Configuration -->
          <template v-if="newConfig.type === 'API'">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('API Endpoint') }}
                <span class="text-xs text-green-600 ml-1">({{ __('Auto-generated') }})</span>
              </label>
              <div class="flex items-center gap-2 px-3 py-2 bg-gray-100 border border-gray-200 rounded-lg">
                <FeatherIcon name="link" class="h-4 w-4 text-gray-500 flex-shrink-0" />
                <span class="text-sm text-gray-700 break-all">{{ newConfig.end_point || generatedEndpoint }}</span>
                <Button
                  @click="copyEndpoint"
                  variant="ghost"
                  size="sm"
                  class="ml-auto flex-shrink-0"
                >
                  <FeatherIcon name="copy" class="h-3 w-3" />
                </Button>
              </div>
              <p class="text-xs text-gray-500 mt-1">
                {{ __('This endpoint will receive candidate data from landing page form') }}
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Content Type') }}
              </label>
              <FormControl
                v-model="newConfig.content_type"
                type="select"
                :options="contentTypeOptions"
              />
            </div>

            <!-- API Headers -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('API Headers') }}
              </label>
              <div class="space-y-2">
                <div 
                  v-for="(header, index) in newConfig.api_headers_list" 
                  :key="index"
                  class="flex gap-2"
                >
                  <div class="flex-1">
                    <FormControl
                      v-model="header.key"
                      type="text"
                      :placeholder="__('Header name')"
                    />
                  </div>
                  <div class="flex-1">
                    <FormControl
                      v-model="header.value"
                      type="text"
                      :placeholder="__('Header value')"
                    />
                  </div>
                  <Button
                    @click="removeHeader(index)"
                    variant="ghost"
                    size="sm"
                    class="text-red-600"
                  >
                    <FeatherIcon name="x" class="h-3 w-3" />
                  </Button>
                </div>
                <Button
                  @click="addHeader"
                  variant="outline"
                  size="sm"
                  class="text-blue-600"
                >
                <div class="flex items-center">
                  <FeatherIcon name="plus" class="h-3 w-3 mr-1" />
                  {{ __('Add Header') }}
                </div>
                </Button>
              </div>
            </div>

            <!-- Field Mappings -->
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                {{ __('Field Mappings') }}
                <span class="text-xs text-gray-500 ml-1">({{ __('Template Field → Mira Talent Field') }})</span>
              </label>
              
              <!-- Debug Info -->
              <div class="flex items-center justify-between text-xs text-gray-500 mb-2">
                <span>Template Fields: {{ templateFields.length }} | Mira Talent Fields: {{ miraTalentFields.length }}</span>
                <Button
                  @click="loadAllFields"
                  variant="ghost"
                  size="sm"
                  class="text-blue-600 text-xs"
                >
                <div class="flex items-center">
                  <FeatherIcon name="refresh-cw" class="h-3 w-3 mr-1" />
                  {{ __('Reload Fields') }}
                </div>
                </Button>
              </div>
              
              <!-- Show message if fields not loaded -->
              <div v-if="templateFields.length === 0 || miraTalentFields.length === 0" class="text-sm text-amber-600 bg-amber-50 p-2 rounded mb-2">
                {{ templateFields.length === 0 ? 'Loading template fields...' : '' }}
                {{ miraTalentFields.length === 0 ? 'Loading Mira Talent fields...' : '' }}
              </div>
              <div class="space-y-2">
                <!-- Show existing mappings (excluding hidden metadata fields) -->
                <div 
                  v-for="(mapping, visibleIndex) in visibleFieldMappings" 
                  :key="visibleIndex"
                  class="flex gap-2"
                >
                  <div class="flex-1">
                    <FormControl
                      v-model="newConfig.field_mappings[getOriginalMappingIndex(visibleIndex)].form_field"
                      type="select"
                      :options="templateFieldOptions"
                      :placeholder="__('Select template field')"
                    />
                  </div>
                  <div class="flex items-center px-2">
                    <FeatherIcon name="arrow-right" class="h-3 w-3 text-gray-400" />
                  </div>
                  <div class="flex-1">
                    <FormControl
                      v-model="newConfig.field_mappings[getOriginalMappingIndex(visibleIndex)].api_field"
                      type="select"
                      :options="miraTalentFieldOptions"
                      :placeholder="__('Select Candidate field')"
                    />
                  </div>
                  <Button
                    @click="removeMapping(getOriginalMappingIndex(visibleIndex))"
                    variant="ghost"
                    size="sm"
                    class="text-red-600"
                  >
                    <FeatherIcon name="x" class="h-3 w-3" />
                  </Button>
                </div>
                
                <!-- Show message if no visible mappings yet -->
                <div v-if="visibleFieldMappings.length === 0" class="text-sm text-gray-500 italic p-3 border border-dashed border-gray-300 rounded">
                  {{ __('No field mappings yet. Click "Add Mapping" to create one.') }}
                </div>
                
                <!-- Add Mapping button -->
                <div class="flex gap-2">
                  <Button
                    @click="addMapping"
                    variant="outline"
                    size="sm"
                    class="text-blue-600"
                  >
                    <div class="flex items-center">
                      <FeatherIcon name="plus" class="h-3 w-3 mr-1" />
                      {{ __('Add Mapping') }}
                    </div>
                  </Button>
                  <Button
                    @click="applyDefaultMappings"
                    variant="outline"
                    size="sm"
                    class="text-green-600"
                    :disabled="templateFields.length === 0"
                  >
                    <div class="flex items-center">
                      <FeatherIcon name="zap" class="h-3 w-3 mr-1" />
                      {{ __('Auto Map') }}
                    </div>
                  </Button>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- Add Button -->
        <div class="flex justify-end mt-4">
          <Button
            @click="addConfig"
            :disabled="!canAddConfig"
            variant="solid"
            size="sm"
          >
          <div class="flex items-center">
            <FeatherIcon name="plus" class="h-3 w-3 mr-1" />
            {{ __('Add Configuration') }}
          </div>
          </Button>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { FeatherIcon, Button, FormControl, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const toast = useToast()

const props = defineProps({
  templateId: {
    type: String,
    default: ''
  },
  formConfigId: {
    type: String,
    default: null
  },
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])


// State
const expanded = ref(false)
const templateFields = ref([]) // Form fields từ template
const miraTalentFields = ref([]) // Mira Talent fields
const configs = ref([...props.modelValue])
const editingIndex = ref(-1) // Index của config đang edit
const templateId = ref(null)

watch(() => props.templateId, (newTemplateId) => {
  templateId.value = newTemplateId;
  console.log('Template ID updated:', templateId.value);
}, { immediate: true });

// New config form
const newConfig = ref({
  type: '',
  email: '',
  end_point: '',
  content_type: 'application/json',
  api_headers_list: [],
  field_mappings: []
})

// Options
const configTypeOptions = [
  { label: 'Email Notification', value: 'Email' },
  { label: 'API Webhook', value: 'API' }
]

const contentTypeOptions = [
  { label: 'JSON (application/json)', value: 'application/json' },
  { label: 'Form Data (application/x-www-form-urlencoded)', value: 'application/x-www-form-urlencoded' },
  { label: 'Multipart (multipart/form-data)', value: 'multipart/form-data' }
]

// Default field mappings - common fields that should be auto-mapped
// Format: { templateFieldPattern: miraTalentFieldname }
// Template fields từ CMS: full_name, primary_email, phone_number, linkedin_url, expected_salary, cv_upload, utm_*
// Mira Talent fields: full_name, email, phone, resume, linkedin_profile, etc.
const DEFAULT_FIELD_MAPPINGS = {
  // Full name variations → full_name
  'full_name': 'full_name',
  'fullname': 'full_name',
  'name': 'full_name',
  'ho_ten': 'full_name',
  'hoten': 'full_name',
  'candidate_name': 'full_name',
  
  // Email variations → email
  'email': 'email',
  'primary_email': 'email',
  'email_address': 'email',
  'candidate_email': 'email',
  
  // Phone variations → phone
  'phone': 'phone',
  'phone_number': 'phone',
  'mobile': 'phone',
  'so_dien_thoai': 'phone',
  'dien_thoai': 'phone',
  'contact_number': 'phone',
  
  // CV/Resume variations → resume
  'cv': 'resume',
  'cv_upload': 'resume',
  'cv_attachment': 'resume',
  'resume': 'resume',
  'file_cv': 'resume',
  'cv_file': 'resume',
  'attachment': 'resume',
  
  // LinkedIn/Other links → linkedin_profile
  'linkedin': 'linkedin_profile',
  'linkedin_url': 'linkedin_profile',
  'other_links': 'linkedin_profile',
  'portfolio': 'linkedin_profile',
  'website': 'linkedin_profile',
  
  // Address → current_city
  'address': 'current_city',
  'dia_chi': 'current_city',
  
  // Profile/Cover letter → notes
  'profile': 'notes',
  'cover_letter': 'notes',
  'thu_xin_viec': 'notes',
  'message': 'notes',
  'introduction': 'notes',
  
  // Last workplace → latest_company
  'last_workplace': 'latest_company',
  'current_company': 'latest_company',
  'company': 'latest_company',
  'cong_ty': 'latest_company',
  
  // Referral → source
  'referral': 'source',
  'nguoi_gioi_thieu': 'source',
  'referred_by': 'source'
}

// System/metadata fields that should be hidden from dropdown selection
// These are auto-included and don't need user selection
const SYSTEM_FIELDS = [
  'form_id', 'page_id', 'form_url', 'custom_field',
  'utm_source', 'utm_medium', 'utm_content', 'utm_campaign'
]

// Computed
const templateFieldOptions = computed(() => {
  // Filter out system fields from template field options
  return templateFields.value
    .filter(field => !SYSTEM_FIELDS.includes(field.fieldname))
    .map(field => ({
      label: field.label || field.fieldname,
      value: field.fieldname
    }))
})

const miraTalentFieldOptions = computed(() => {
  return miraTalentFields.value.map(field => ({
    label: field.label,
    value: field.fieldname
  }))
})

// Auto-generated endpoint URL
const generatedEndpoint = computed(() => {
  const siteUrl = window.location.origin
  const apiPath = '/api/method/mbw_mira.api.v1.talent.create'
  return `${siteUrl}${apiPath}`
})

const canAddConfig = computed(() => {
  if (newConfig.value.type === 'Email') {
    return newConfig.value.email && newConfig.value.email.includes('@')
  } else if (newConfig.value.type === 'API') {
    // Endpoint is auto-generated, just need content_type
    return newConfig.value.content_type
  }
  return false
})

// Hidden metadata fields - these are auto-added but not displayed in UI
// Should match SYSTEM_FIELDS above
const HIDDEN_METADATA_FIELDS = [
  'form_id', 'page_id', 'form_url', 'custom_field',
  'utm_source', 'utm_medium', 'utm_content', 'utm_campaign', 'utm_term'
]

// Filter visible field mappings (hide metadata fields)
const visibleFieldMappings = computed(() => {
  return (newConfig.value.field_mappings || []).filter(
    mapping => !HIDDEN_METADATA_FIELDS.includes(mapping.form_field)
  )
})

// Get the actual index in original array for a visible mapping
const getOriginalMappingIndex = (visibleIndex) => {
  const visibleMappings = visibleFieldMappings.value
  if (visibleIndex >= visibleMappings.length) return -1
  
  const targetMapping = visibleMappings[visibleIndex]
  return newConfig.value.field_mappings.findIndex(
    m => m.form_field === targetMapping.form_field && m.api_field === targetMapping.api_field
  )
}

// Methods
const toggleSection = () => {
  expanded.value = !expanded.value
  if (expanded.value) {
    // Always try to load fields when expanding section
    console.log('🔄 Section expanded, loading fields...')
    loadAllFields()
  }
}

const loadAllFields = async () => {
  await Promise.all([
    loadTemplateFields(),
    loadMiraTalentFields()
  ])
}

const loadTemplateFields = async () => {
  console.log('🔍 loadTemplateFields called - using get_fields_mapping API')
  
  try {
    // Use new get_fields_mapping API (doesn't require template_id)
    const response = await call('mbw_mira.integrations.cms_page.get_fields_mapping')
    
    console.log('📥 Fields mapping API response:', response)
    
    // Handle nested response structure
    let fieldsData = null
    if (response?.message?.message?.status === 'success' && response?.message?.message?.data) {
      fieldsData = response.message.message.data
    } else if (response?.message?.status === 'success' && response?.message?.data) {
      fieldsData = response.message.data
    } else if (response?.status === 'success' && response?.data) {
      fieldsData = response.data
    }
    
    if (fieldsData && Array.isArray(fieldsData)) {
      // Fields already have label, fieldname, fieldtype format
      templateFields.value = fieldsData.map(field => ({
        fieldname: field.fieldname,
        label: field.label || field.fieldname.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        fieldtype: field.fieldtype || 'Data'
      }))
      console.log('✅ Template fields loaded:', templateFields.value)
    } else {
      console.log('⚠️ No template fields found or invalid format')
      // Fallback to common fields
      templateFields.value = [
        { fieldname: 'full_name', label: 'Full Name', fieldtype: 'Data' },
        { fieldname: 'primary_email', label: 'Primary Email', fieldtype: 'Data' },
        { fieldname: 'phone_number', label: 'Phone Number', fieldtype: 'Data' },
        { fieldname: 'linkedin_url', label: 'LinkedIn URL', fieldtype: 'Data' },
        { fieldname: 'cv_upload', label: 'CV Upload', fieldtype: 'Attach' },
        { fieldname: 'date_of_birth', label: 'Date of Birth', fieldtype: 'Date' },
        { fieldname: 'utm_source', label: 'UTM Source', fieldtype: 'Data' },
        { fieldname: 'utm_medium', label: 'UTM Medium', fieldtype: 'Data' },
        { fieldname: 'utm_campaign', label: 'UTM Campaign', fieldtype: 'Data' }
      ]
    }
  } catch (error) {
    console.error('❌ Error loading template fields:', error)
    // Use fallback fields on error
    templateFields.value = [
      { fieldname: 'full_name', label: 'Full Name', fieldtype: 'Data' },
      { fieldname: 'primary_email', label: 'Primary Email', fieldtype: 'Data' },
      { fieldname: 'phone_number', label: 'Phone Number', fieldtype: 'Data' },
      { fieldname: 'linkedin_url', label: 'LinkedIn URL', fieldtype: 'Data' },
      { fieldname: 'cv_upload', label: 'CV Upload', fieldtype: 'Attach' }
    ]
    toast.warning(__('Could not load template fields, using defaults'))
  }
}

const loadMiraTalentFields = async () => {
  try {
    console.log('🔍 Loading Mira Talent fields for mapping')
    
    const response = await call('mbw_mira.integrations.cms_page.get_doctype_fields', {
      doctype: 'Mira Talent'
    })
    
    console.log('📥 Mira Talent fields API response:', response)
    
    if (response?.status === 'success' && response?.data) {
      miraTalentFields.value = response.data
      console.log('✅ Mira Talent fields loaded:', response.data)
    } else {
      console.log('⚠️ Mira Talent API failed, using fallback fields')
      console.log('Response details:', response)
      
      // Fallback to common fields if API fails (using actual Mira Talent field names)
      const fallbackFields = [
        { fieldname: 'full_name', label: 'Full Name', fieldtype: 'Data' },
        { fieldname: 'email', label: 'Email', fieldtype: 'Data' },
        { fieldname: 'phone', label: 'Phone Number', fieldtype: 'Data' },
        { fieldname: 'resume', label: 'CV', fieldtype: 'Attach' },
        { fieldname: 'current_city', label: 'Address', fieldtype: 'Data' },
        { fieldname: 'linkedin_profile', label: 'Other Links', fieldtype: 'Data' },
        { fieldname: 'notes', label: 'Candidate Profile', fieldtype: 'Text' },
        { fieldname: 'latest_company', label: 'Last Workplace', fieldtype: 'Data' },
        { fieldname: 'source', label: 'Referral', fieldtype: 'Data' }
      ]
      
      miraTalentFields.value = fallbackFields
      console.log('⚠️ Using fallback Mira Talent fields:', fallbackFields)
    }
  } catch (error) {
    console.error('❌ Error loading Mira Talent fields:', error)
    console.log('Error details:', error)
    
    // Use fallback fields on error (using actual Mira Talent field names)
    const fallbackFields = [
      { fieldname: 'full_name', label: 'Full Name', fieldtype: 'Data' },
      { fieldname: 'email', label: 'Email', fieldtype: 'Data' },
      { fieldname: 'phone', label: 'Phone Number', fieldtype: 'Data' },
      { fieldname: 'resume', label: 'CV', fieldtype: 'Attach' },
      { fieldname: 'current_city', label: 'Address', fieldtype: 'Data' },
      { fieldname: 'linkedin_profile', label: 'Other Links', fieldtype: 'Data' },
      { fieldname: 'notes', label: 'Candidate Profile', fieldtype: 'Text' },
      { fieldname: 'latest_company', label: 'Last Workplace', fieldtype: 'Data' },
      { fieldname: 'source', label: 'Referral', fieldtype: 'Data' }
    ]
    
    miraTalentFields.value = fallbackFields
    toast.error(__('Failed to load Mira Talent fields, using defaults'))
  }
}

const addHeader = () => {
  newConfig.value.api_headers_list.push({ key: '', value: '' })
}

const removeHeader = (index) => {
  newConfig.value.api_headers_list.splice(index, 1)
}

// Copy endpoint to clipboard
const copyEndpoint = async () => {
  const endpoint = newConfig.value.end_point || generatedEndpoint.value
  
  try {
    await navigator.clipboard.writeText(endpoint)
    toast.success(__('API endpoint copied to clipboard'))
  } catch (err) {
    console.error('Failed to copy:', err)
    // Fallback for older browsers
    const textArea = document.createElement('textarea')
    textArea.value = endpoint
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    
    toast.success(__('API endpoint copied to clipboard'))
  }
}

const addMapping = () => {
  newConfig.value.field_mappings.push({ form_field: '', api_field: '' })
}

const removeMapping = (index) => {
  newConfig.value.field_mappings.splice(index, 1)
}

// Apply default field mappings based on template fields
const applyDefaultMappings = () => {
  if (templateFields.value.length === 0) {
    console.log('⚠️ No template fields loaded yet, cannot apply default mappings')
    return
  }
  
  console.log('🔄 Applying default field mappings...')
  console.log('📋 Available template fields:', templateFields.value.map(f => f.fieldname))
  
  const newMappings = []
  const mappedMiraTalentFields = new Set() // Track which ATS fields are already mapped
  
  // Go through each template field and try to find a matching ATS field
  for (const templateField of templateFields.value) {
    const fieldName = templateField.fieldname.toLowerCase()
    
    // Check if this template field matches any default mapping pattern
    for (const [pattern, miraTalentField] of Object.entries(DEFAULT_FIELD_MAPPINGS)) {
      if (fieldName === pattern || fieldName.includes(pattern) || pattern.includes(fieldName)) {
        // Check if this ATS field is already mapped
        if (!mappedMiraTalentFields.has(miraTalentField)) {
          // Verify the ATS field exists in our available fields
          const miraTalentFieldExists = miraTalentFields.value.some(f => f.fieldname === miraTalentField)
          
          if (miraTalentFieldExists) {
            newMappings.push({
              form_field: templateField.fieldname,
              api_field: miraTalentField
            })
            mappedMiraTalentFields.add(miraTalentField)
            console.log(`✅ Mapped: ${templateField.fieldname} → ${miraTalentField}`)
            break // Move to next template field
          }
        }
      }
    }
  }
  
  if (newMappings.length > 0) {
    newConfig.value.field_mappings = newMappings
    console.log(`🎉 Applied ${newMappings.length} default mappings`)
    
    toast.success(__('🤖 {0} đã tự động được map, vui lòng kiểm tra lại!', [newMappings.length]))
  } else {
    console.log('⚠️ No default mappings could be applied')
    // Add one empty mapping for user to fill
    newConfig.value.field_mappings = [{ form_field: '', api_field: '' }]
  }
}

// Watch for type change to auto-apply default mappings when selecting API
watch(() => newConfig.value.type, async (newType, oldType) => {
  console.log('🔄 Config type changed from:', oldType, 'to:', newType)
  
  if (newType === 'API') {
    // Auto-set endpoint URL
    if (!newConfig.value.end_point) {
      newConfig.value.end_point = generatedEndpoint.value
      console.log('🔗 Auto-set endpoint:', newConfig.value.end_point)
    }
    
    // Load fields if not loaded yet
    if (templateFields.value.length === 0 || miraTalentFields.value.length === 0) {
      console.log('📥 Loading fields before applying default mappings...')
      await loadAllFields()
    }
    
    // Apply default mappings if field_mappings is empty
    if (newConfig.value.field_mappings.length === 0) {
      // Give a small delay to ensure fields are rendered
      setTimeout(() => {
        applyDefaultMappings()
      }, 100)
    }
  }
})

const addConfig = async () => {
  if (!canAddConfig.value) return
  
  const config = prepareConfigData()
  
  // If we have form_config_id, create via API
  if (props.formConfigId) {
    const apiResponse = await createReceiveDataConfig(config)
    if (apiResponse && apiResponse.message && apiResponse.message.status === 'success') {
      // Add the config with ID from API response
      const createdConfig = { ...config }
      if (apiResponse.message.data && apiResponse.message.data.id) {
        createdConfig.id = apiResponse.message.data.id
      }
      
      configs.value.push(createdConfig)
      console.log('➕ Added config via API:', createdConfig)
    } else {
      console.error('❌ Failed to create config via API')
      return
    }
  } else {
    // No form_config_id, just add locally (for new pages)
    configs.value.push(config)
    console.log('➕ Added config locally:', config)
  }
  
  console.log('📋 All configs:', configs.value)
  console.log('📤 Will emit to parent:', configs.value)
  
  // Force emit immediately
  emit('update:modelValue', [...configs.value])
  
  resetNewConfigForm()
  toast.success(__('Configuration added successfully'))
}

const editConfig = (index) => {
  const config = configs.value[index]
  editingIndex.value = index
  
  // Load config data into form
  newConfig.value = {
    type: config.type,
    email: config.email || '',
    end_point: config.end_point || '',
    content_type: config.content_type || 'application/json',
    api_headers_list: config.api_headers ? 
      Object.entries(config.api_headers).map(([key, value]) => ({ key, value })) : [],
    field_mappings: [...(config.field_mappings || [])]
  }
  
  console.log('✏️ Editing config at index:', index, config)
  toast.info(__('Editing configuration'))
}

const updateConfig = async () => {
  if (!canAddConfig.value || editingIndex.value < 0) return
  
  const config = prepareConfigData()
  const existingConfig = configs.value[editingIndex.value]
  
  // If config has ID, update via API
  if (existingConfig.id) {
    config.id = existingConfig.id // Preserve ID
    const apiResponse = await updateReceiveDataConfig(config)
    if (apiResponse && apiResponse.message && apiResponse.message.status === 'success') {
      configs.value[editingIndex.value] = config
      console.log('💾 Updated config via API:', config)
    } else {
      console.error('❌ Failed to update config via API')
      return
    }
  } else {
    // No ID, just update locally
    configs.value[editingIndex.value] = config
    console.log('💾 Updated config locally:', config)
  }
  
  console.log('📋 All configs:', configs.value)
  
  // Force emit immediately
  emit('update:modelValue', [...configs.value])
  
  resetNewConfigForm()
  editingIndex.value = -1
  toast.success(__('Configuration updated successfully'))
}

const cancelEdit = () => {
  resetNewConfigForm()
  editingIndex.value = -1
  toast.info(__('Edit cancelled'))
}

const prepareConfigData = () => {
  const config = { ...newConfig.value }
  
  // Convert headers list to object for API
  if (config.type === 'API' && config.api_headers_list.length > 0) {
    config.api_headers = {}
    config.api_headers_list.forEach(header => {
      if (header.key && header.value) {
        config.api_headers[header.key] = header.value
      }
    })
    delete config.api_headers_list
  }
  
  // Clean up empty mappings
  if (config.field_mappings) {
    config.field_mappings = config.field_mappings.filter(mapping => 
      mapping.form_field && mapping.api_field
    )
  }
  
  return config
}

const removeConfig = async (index) => {
  const config = configs.value[index]
  
  // Confirm dialog
  const confirmed = confirm(__('Are you sure you want to delete this configuration? This action cannot be undone.'))
  if (!confirmed) {
    console.log('🚫 User cancelled delete operation')
    return
  }
  
  console.log('🗑️ Removing config at index:', index, config)
  
  // If config has ID, delete via API
  if (config.id) {
    const apiResponse = await deleteReceiveDataConfig(config.id)
    if (apiResponse && apiResponse.message && apiResponse.message.status === 'success') {
      console.log('✅ Config deleted via API successfully')
    } else {
      console.error('❌ Failed to delete config via API')
      toast.error(__('Failed to delete configuration from server'))
      return // Don't remove from UI if API call failed
    }
  }
  
  // Remove from local array
  configs.value.splice(index, 1)
  console.log('🗑️ Removed config at index:', index)
  console.log('📋 Remaining configs:', configs.value)
  
  // Force emit immediately
  emit('update:modelValue', [...configs.value])
  
  toast.success(__('Configuration deleted successfully'))
}

const resetNewConfigForm = () => {
  newConfig.value = {
    type: '',
    email: '',
    end_point: '',
    content_type: 'application/json',
    api_headers_list: [],
    field_mappings: []
  }
}

// Auto-save config if user has entered data but hasn't clicked Add Configuration or Save Changes
const autoSaveConfigIfNeeded = async () => {
  if (!canAddConfig.value) {
    return false // No valid data to save
  }
  
  // Case 1: User is adding new config but hasn't clicked "Add Configuration"
  if (editingIndex.value < 0) {
    console.log('🔄 Auto-saving new config before submit...')
    await addConfig()
    return true
  }
  
  // Case 2: User is editing existing config but hasn't clicked "Save Changes"
  if (editingIndex.value >= 0) {
    console.log('🔄 Auto-saving edited config before submit...')
    await updateConfig()
    return true
  }
  
  return false // No config was auto-saved
}

// Expose the auto-save function to parent component
defineExpose({
  autoSaveConfigIfNeeded
})

// Watch configs and emit changes
watch(configs, (newConfigs, oldConfigs) => {
  // Prevent infinite loop by checking if configs actually changed
  if (JSON.stringify(newConfigs) !== JSON.stringify(oldConfigs)) {
    console.log('📤 ReceiveDataConfigsManager emitting configs:', newConfigs)
    emit('update:modelValue', newConfigs)
  }
}, { deep: true, flush: 'post' })

// Watch props.modelValue for external changes
watch(() => props.modelValue, (newValue, oldValue) => {
  // Prevent infinite loop by checking if value actually changed
  if (JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    configs.value = [...newValue]
  }
}, { deep: true, flush: 'post' })

// Watch templateId changes to reload fields
watch(() => props.templateId, (newTemplateId, oldTemplateId) => {
  console.log('🔄 templateId changed from', oldTemplateId, 'to', newTemplateId)
  if (newTemplateId && newTemplateId !== oldTemplateId) {
    console.log('🔄 Reloading fields for new template ID:', newTemplateId)
    loadAllFields()
  }
}, { immediate: false })

// API calls for create/update configs
const createReceiveDataConfig = async (config) => {
  if (!props.formConfigId) {
    console.error('❌ No form_config_id available for creating config')
    toast.error(__('Cannot create config: No form configuration ID'))
    return null
  }
  
  try {
    console.log('📤 Creating receive data config:', config)
    console.log('🆔 Using form_config_id:', props.formConfigId)
    
    const response = await call('mbw_mira.integrations.cms_page.create_link_account', {
      form_config_id: props.formConfigId,
      receive_data_config: config
    })
    
    console.log('✅ Create config response:', response)
    return response
  } catch (error) {
    console.error('❌ Error creating config:', error)
    toast.error(__('Failed to create configuration'))
    return null
  }
}

const updateReceiveDataConfig = async (config) => {
  if (!config.id) {
    console.error('❌ No config ID available for updating')
    toast.error(__('Cannot update config: No configuration ID'))
    return null
  }
  
  try {
    console.log('💾 Updating receive data config:', config)
    
    const response = await call('mbw_mira.integrations.cms_page.update_link_account', {
      receive_data_config: config
    })
    
    console.log('✅ Update config response:', response)
    return response
  } catch (error) {
    console.error('❌ Error updating config:', error)
    toast.error(__('Failed to update configuration'))
    return null
  }
}

const deleteReceiveDataConfig = async (configId) => {
  if (!configId) {
    console.error('❌ No config ID available for deleting')
    toast.error(__('Cannot delete config: No configuration ID'))
    return null
  }
  
  try {
    console.log('🗑️ Deleting receive data config with ID:', configId)
    
    const response = await call('mbw_mira.integrations.cms_page.delete_link_account', {
      receive_data_config_id: configId
    })
    
    console.log('✅ Delete config response:', response)
    return response
  } catch (error) {
    console.error('❌ Error deleting config:', error)
    toast.error(__('Failed to delete configuration'))
    return null
  }
}

// Initialize on mount
onMounted(() => {
  console.log('🚀 ReceiveDataConfigsManager mounted with:')
  console.log('- templateId:', props.templateId)
  console.log('- formConfigId:', props.formConfigId)
  console.log('- modelValue:', props.modelValue)
  
  // Always load fields on mount for immediate availability
  loadAllFields()
})
</script>
