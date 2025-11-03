<template>
  <div class="flex h-full flex-col gap-6 p-8 text-ink-gray-8">
    <!-- Header -->
    <div class="flex justify-between">
      <div class="flex gap-1 -ml-4 w-9/12">
        <Button
          variant="ghost"
          icon-left="chevron-left"
          :label="__(template.template_name || template.name)"
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
          :label="__('Update')"
          icon-left="check"
          variant="solid"
          :disabled="!dirty"
          :loading="templates.setValue.loading"
          @click="updateTemplate"
        />
      </div>
    </div>

    <!-- Fields -->
    <div class="flex flex-1 flex-col gap-4 overflow-y-auto">
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
      <div>
        <div class="mb-1.5 flex items-center justify-between">
          <label class="text-base text-ink-gray-5">
            {{ __('Message') }}
            <span class="text-ink-red-3">*</span>
          </label>
          <Autocomplete
            v-model="selectedMessageField"
            :options="subjectFieldAutocompleteOptions"
            :placeholder="__('Search fields...')"
            class="w-48"
          >
            <template #target="{ togglePopover }">
              <Button
                :label="__('Insert')"
                icon-left="plus-circle"
                variant="outline"
                size="sm"
                @click="togglePopover"
              />
            </template>
          </Autocomplete>
        </div>
        <TextEditor
          ref="content"
          editor-class="!prose-sm max-w-full overflow-auto min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-[--surface-gray-2] bg-surface-gray-2 placeholder-ink-gray-4 hover:border-outline-gray-modals hover:bg-surface-gray-3 hover:shadow-sm focus:bg-surface-white focus:border-outline-gray-4 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-outline-gray-3 text-ink-gray-8 transition-colors"
          :bubbleMenu="true"
          :fixed-menu="true"
          :content="template.message"
          @change="(val) => (template.message = val)"
          :placeholder="
            __(
              'Dear {{ full_name }}, \n\nWelcome to our platform! \n\nBest regards, \nThe Team',
            )
          "
        />
        <p class="text-xs text-ink-gray-4 mt-1">
          {{ __('Click insert to insert talent fields') }}
        </p>
      </div>
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
import {
  TextEditor,
  FormControl,
  Switch,
  Button,
  Autocomplete,
  FeatherIcon,
} from 'frappe-ui'
import { computed, inject, onMounted, ref, watch } from 'vue'
import EmailPreview from './EmailPreview.vue'
import { useToast } from '@/composables/useToast'

const props = defineProps({
  templateData: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['updateStep'])
const errorMessage = ref('')
const toast = useToast()

const templates = inject('templates')
const template = ref({})
const content = ref(null)
const subjectRef = ref(null)
const showPreview = ref(false)
const selectedField = ref(null)
const selectedMessageField = ref(null)

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

// Watch for message field selection
watch(selectedMessageField, (newValue) => {
  if (newValue) {
    insertFieldToMessage(newValue)
    // Reset selection after insert
    setTimeout(() => {
      selectedMessageField.value = null
    }, 100)
  }
})

const updateTemplate = async () => {
  errorMessage.value = ''
  if (!template.value.template_name) {
    errorMessage.value = __('Template Name is required')
    return
  }
  if (!template.value.subject) {
    errorMessage.value = __('Subject is required')
    return
  }
  if (!template.value.message) {
    errorMessage.value = __('Message is required')
    return
  }

  const values = {
    name: props.templateData.name,
    template_name: template.value.template_name,
    template_type: template.value.template_type,
    subject: template.value.subject,
    message: template.value.message,
    is_active: template.value.is_active ? 1 : 0,
    default_template: template.value.default_template ? 1 : 0,
    auto_send: template.value.auto_send ? 1 : 0,
  }

  templates.setValue.submit(values, {
    onSuccess: () => {
      emit('updateStep', 'template-list')
      toast.success('Template updated successfully')
    },
    onError: (error) => {
      errorMessage.value =
        error.messages?.[0] || 'Failed to update template'
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

const dirty = computed(() => {
  return (
    template.value.template_name !== props.templateData.template_name ||
    template.value.template_type !== props.templateData.template_type ||
    template.value.subject !== props.templateData.subject ||
    template.value.message !== props.templateData.message ||
    Boolean(template.value.is_active) !== Boolean(props.templateData.is_active) ||
    Boolean(template.value.default_template) !== Boolean(props.templateData.default_template) ||
    Boolean(template.value.auto_send) !== Boolean(props.templateData.auto_send)
  )
})

onMounted(() => {
  template.value = { ...props.templateData }
  // Convert to boolean for switches
  template.value.is_active = Boolean(template.value.is_active)
  template.value.default_template = Boolean(template.value.default_template)
  template.value.auto_send = Boolean(template.value.auto_send)
})
</script>
