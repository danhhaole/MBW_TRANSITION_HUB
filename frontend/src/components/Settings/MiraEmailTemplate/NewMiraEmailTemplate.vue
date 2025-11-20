<template>
  <div class="flex h-full flex-col gap-6 p-8 text-ink-gray-8">
    <!-- Header -->
    <div class="flex justify-between" v-show="!isFullscreen">
      <div class="flex gap-1 -ml-4 w-9/12">
        <Button
          variant="ghost"
          icon-left="chevron-left"
          :label="
            templateData?.name ? __('Duplicate Template') : __('New Template')
          "
          size="md"
          @click="() => emit('updateStep', 'template-list')"
          class="cursor-pointer hover:bg-transparent focus:bg-transparent focus:outline-none focus:ring-0 focus:ring-offset-0 focus-visible:none active:bg-transparent active:outline-none active:ring-0 active:ring-offset-0 active:text-ink-gray-5 font-semibold text-xl hover:opacity-70 !pr-0 !max-w-96 !justify-start"
        />
      </div>
      <div class="flex item-center space-x-4 w-3/12 justify-end">
        <div class="flex items-center space-x-2">
          <Switch size="sm" v-model="template.is_active" />
          <span class="text-sm text-ink-gray-7">{{ __('Active') }}</span>
        </div>
        <Button
          :label="__('Preview')"
          icon-left="eye"
          variant="outline"
          @click="showPreview = true"
        />
        <Button
          :label="templateData?.name ? __('Duplicate') : __('Create')"
          icon-left="plus"
          variant="solid"
          @click="createTemplate"
          :loading="templates.insert.loading"
        />
      </div>
    </div>

    <!-- Fields -->
    <div class="space-y-4" v-show="!isFullscreen">
      <div class="flex sm:flex-row flex-col gap-4">
        <div class="flex-1">
          <FormControl
            size="md"
            v-model="template.template_name"
            :placeholder="__('Welcome Email')"
            :label="__('Template Name')"
            :required="true"
          />
        </div>
        <div class="flex-1">
          <FormControl
            type="select"
            size="md"
            v-model="template.template_type"
            :label="__('Template Type')"
            :options="[
              {
                label: __('Confirm Email'),
                value: 'confirm-email',
              },
              {
                label: __('Invited Email'),
                value: 'invited-email',
              },
              {
                label: __('Reject Email'),
                value: 'reject-email',
              },
              {
                label: __('Other Email'),
                value: 'other-email',
              },
            ]"
            :placeholder="__('Select Type')"
          />
        </div>
      </div>
      <div>
        <div class="mb-1.5 flex items-center justify-between">
          <label class="text-base text-ink-gray-5">
            {{ __('Subject') }}
            <span class="text-ink-red-3">*</span>
          </label>
        </div>
        <div class="flex gap-2">
          <FormControl
            ref="subjectRef"
            size="md"
            v-model="template.subject"
            :placeholder="__('Welcome to our platform, {{ full_name }}')"
            :required="true"
            class="flex-1"
          />
          <Autocomplete
            v-model="selectedField"
            :options="subjectFieldAutocompleteOptions"
            :placeholder="__('Search fields...')"
            class="w-48"
          >
            <template #target="{ togglePopover }">
              <Button
                :label="__('Insert')"
                icon-left="plus-circle"
                variant="outline"
                size="md"
                @click="togglePopover"
              />
            </template>
          </Autocomplete>
        </div>
        <p class="text-xs text-ink-gray-4 mt-1">
          {{ __('Click insert to insert talent fields') }}
        </p>
      </div>
      <div class="flex gap-4">
        <div class="flex items-center space-x-2">
          <Switch size="sm" v-model="template.default_template" />
          <span class="text-sm text-ink-gray-7">{{ __('Default Template') }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <Switch size="sm" v-model="template.auto_send" />
          <span class="text-sm text-ink-gray-7">{{ __('Auto Send') }}</span>
        </div>
      </div>
    </div>

    <!-- Email Design Section - Always visible -->
    <div>
      <div class="mb-1.5 flex items-center justify-between">
        <label class="text-base text-ink-gray-5" v-show="!isFullscreen">
          {{ __('Email Design') }}
          <span class="text-ink-red-3">*</span>
        </label>
        <div class="flex items-center gap-2" :class="isFullscreen ? 'w-full justify-end' : ''">
          <!-- Merge Tags Autocomplete -->
          <Autocomplete
            :options="mergeTagsAutocompleteOptions"
            v-model="selectedMergeTag"
            placeholder="Insert merge tag..."
            :class="isFullscreen ? 'w-80' : 'w-64'"
          >
            <template #prefix>
              <FeatherIcon name="code" class="h-4 w-4 text-gray-500" />
            </template>
          </Autocomplete>
          
          <!-- Fullscreen Toggle Button -->
          <Button
            :label="isFullscreen ? __('Exit Fullscreen') : __('Fullscreen')"
            :icon-left="isFullscreen ? 'minimize-2' : 'maximize-2'"
            variant="outline"
            size="sm"
            @click="isFullscreen = !isFullscreen"
          />
        </div>
      </div>
      <!-- Email Builder -->
      <EmailBuilder
        ref="emailBuilderRef"
        v-model="emailDesignJson"
        :height="isFullscreen ? 'calc(100vh - 250px)' : '400px'"
        @ready="onEmailBuilderReady"
      />
      <p class="text-xs text-ink-gray-4 mt-2" v-show="!isFullscreen">
        {{ __('Drag blocks from the sidebar to design your email. Click merge tags above to copy and paste into content.') }}
      </p>
    </div>
    
    <!-- Email Preview Dialog -->
    <EmailPreview
      v-model="showPreview"
      :templateData="template"
    />
    
    <div v-if="errorMessage">
      <div class="rounded-md bg-red-50 p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <FeatherIcon name="alert-circle" class="h-5 w-5 text-red-400" />
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-800">{{ __(errorMessage) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { TextEditor, FormControl, Switch, Button, Autocomplete, FeatherIcon } from 'frappe-ui'
import { inject, onMounted, ref, computed, watch } from 'vue'
import EmailPreview from './EmailPreview.vue'
import EmailBuilder from './EmailBuilder/EmailBuilder.vue'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  templateData: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['updateStep'])
const errorMessage = ref('')
const toast = useToast()

const template = ref({
  template_name: '',
  template_type: 'other-email',
  subject: '',
  message: '',
  is_active: false,
  default_template: false,
  auto_send: false,
})

const subjectRef = ref(null)
const showPreview = ref(false)
const isFullscreen = ref(false)
const selectedField = ref(null)
const selectedMergeTag = ref(null)
const emailBuilderRef = ref(null)
const emailDesignJson = ref(null)
// OLD REF - COMMENTED OUT
// const unlayerEditorRef = ref(null)

// Mira Talent & Campaign fields for insertion - grouped for better UX
const talentFieldsGrouped = [
  {
    group: 'Campaign Info',
    items: [
      { fieldname: 'campaign_name', label: 'Campaign Name' },
      { fieldname: 'campaign_type', label: 'Campaign Type' },
      { fieldname: 'campaign_description', label: 'Campaign Description' },
    ]
  },
  {
    group: 'Personal Info',
    items: [
      { fieldname: 'full_name', label: 'Full Name' },
      { fieldname: 'email', label: 'Email' },
      { fieldname: 'phone', label: 'Phone' },
      { fieldname: 'gender', label: 'Gender' },
      { fieldname: 'date_of_birth', label: 'Date of Birth' },
      { fieldname: 'current_city', label: 'City/Address' },
    ]
  },
  {
    group: 'Professional',
    items: [
      { fieldname: 'latest_title', label: 'Latest Title' },
      { fieldname: 'latest_company', label: 'Latest Company' },
      { fieldname: 'skills', label: 'Skills' },
      { fieldname: 'total_years_of_experience', label: 'Years of Experience' },
      { fieldname: 'highest_education', label: 'Highest Education' },
    ]
  },
  {
    group: 'Career Preferences',
    items: [
      { fieldname: 'desired_role', label: 'Desired Role' },
      { fieldname: 'domain_expertise', label: 'Domain Expertise' },
      { fieldname: 'current_salary', label: 'Current Salary' },
      { fieldname: 'expected_salary', label: 'Expected Salary' },
      { fieldname: 'preferred_work_model', label: 'Work Model' },
      { fieldname: 'availability_date', label: 'Availability Date' },
    ]
  },
  {
    group: 'Status & Social',
    items: [
      { fieldname: 'current_status', label: 'Current Status' },
      { fieldname: 'cultural_fit', label: 'Cultural Fit' },
      { fieldname: 'internal_rating', label: 'Internal Rating' },
      { fieldname: 'priority_level', label: 'Priority' },
      { fieldname: 'linkedin_profile', label: 'LinkedIn Profile' },
      { fieldname: 'facebook_profile', label: 'Facebook Profile' },
      { fieldname: 'zalo_profile', label: 'Zalo Profile' },
    ]
  },
]

// Merge tags autocomplete options - grouped for better organization
const mergeTagsAutocompleteOptions = computed(() => {
  return talentFieldsGrouped.map(group => ({
    group: group.group,
    items: group.items.map(field => ({
      label: field.label,
      value: field.fieldname,
    }))
  }))
})

// Flatten for badge display
const talentFields = ref(
  talentFieldsGrouped.flatMap(group => group.items)
)

// Subject field autocomplete options - grouped
const subjectFieldAutocompleteOptions = computed(() => {
  return talentFieldsGrouped.map(group => ({
    group: group.group,
    items: group.items.map(field => ({
      label: field.label,
      value: field.fieldname,
      description: `{{ ${field.fieldname} }}`,
    }))
  }))
})

// Watch for subject field selection
watch(selectedField, (newValue) => {
  if (newValue) {
    insertFieldToSubject(newValue)
    // Reset selection after insert
    setTimeout(() => {
      selectedField.value = null
    }, 100)
  }
})

// Watch for merge tag selection - copy to clipboard
watch(selectedMergeTag, (newValue) => {
  if (newValue) {
    const tag = `{{ ${newValue.value} }}`
    navigator.clipboard.writeText(tag).then(() => {
      toast.success(`Copied: ${tag}`)
      // Reset selection after copy
      setTimeout(() => {
        selectedMergeTag.value = null
      }, 100)
    }).catch(() => {
      toast.error('Failed to copy merge tag')
    })
  }
})


const templates = inject('templates')

const onUnlayerReady = (editor) => {
  console.log('Unlayer editor ready in new template')
  
  // If switching to advanced editor with existing HTML but no design JSON
  if (template.value.message && !emailDesignJson.value) {
    const basicDesign = createUnlayerDesignFromHtml(template.value.message)
    // Deep clone to remove Vue reactivity
    const plainDesign = JSON.parse(JSON.stringify(basicDesign))
    editor.loadDesign(plainDesign)
    toast.info('Converted HTML content to Advanced editor')
  }
}


const createTemplate = async () => {
  errorMessage.value = ''
  if (!template.value.template_name) {
    errorMessage.value = __('Template Name is required')
    return
  }
  if (!template.value.subject) {
    errorMessage.value = __('Subject is required')
    return
  }
  
  // Save design from EmailBuilder
  if (!emailBuilderRef.value) {
    errorMessage.value = __('Email editor not ready')
    return
  }
  
  try {
    const exportData = emailBuilderRef.value.exportHtml()
    const blocks = emailBuilderRef.value.getBlocks()
    const mjml = emailBuilderRef.value.getMJML()
    
    // Store blocks, HTML and MJML
    emailDesignJson.value = { blocks, emailSettings: exportData.emailSettings }
    template.value.message = exportData.html
    template.value.email_design_json = JSON.stringify(emailDesignJson.value)
  } catch (error) {
    console.error('Error saving design:', error)
    errorMessage.value = __('Failed to save email design')
    return
  }
  
  if (!template.value.message) {
    errorMessage.value = __('Message is required')
    return
  }

  const submitData = {
    template_name: template.value.template_name,
    template_type: template.value.template_type,
    subject: template.value.subject,
    message: template.value.message,
    email_design_json: template.value.email_design_json || null,
    is_active: template.value.is_active ? 1 : 0,
    default_template: template.value.default_template ? 1 : 0,
    auto_send: template.value.auto_send ? 1 : 0,
  }

  templates.insert.submit(submitData, {
    onSuccess: () => {
      emit('updateStep', 'template-list')
      toast.success('Template created successfully')
    },
    onError: (error) => {
      errorMessage.value =
        error.messages?.[0] || 'Failed to create template'
    },
  })
}

function insertFieldToSubject(option) {
  if (!option) return
  
  const fieldPlaceholder = `{{ ${option.value} }}`
  const input = subjectRef.value?.$el?.querySelector('input')
  
  if (input) {
    const start = input.selectionStart || 0
    const end = input.selectionEnd || 0
    const text = template.value.subject || ''
    template.value.subject = text.substring(0, start) + fieldPlaceholder + text.substring(end)
    // Set cursor position after inserted text
    setTimeout(() => {
      input.selectionStart = input.selectionEnd = start + fieldPlaceholder.length
      input.focus()
    }, 0)
  } else {
    template.value.subject = (template.value.subject || '') + fieldPlaceholder
  }
  
  toast.success(`Inserted field: ${option.label}`)
}

function insertFieldToMessage(option) {
  if (!option) return
  
  const fieldPlaceholder = `{{ ${option.value} }}`
  
  // Insert into Rich Text Editor
  if (content.value?.editor) {
    content.value.editor.commands.insertContent(fieldPlaceholder)
  } else {
    template.value.message += fieldPlaceholder
  }
  
  toast.success(`Inserted field: ${option.label}`)
}

// EmailBuilder ready callback
function onEmailBuilderReady(builderMethods) {
  console.log('🎉 [NewTemplate] EmailBuilder ready callback')
  // EmailBuilder is ready to use
}

onMounted(() => {
  if (props.templateData?.name) {
    Object.assign(template.value, props.templateData)
    template.value.template_name = template.value.template_name + ' - Copy'
    template.value.is_active = false
    template.value.default_template = false
  }
})
</script>
