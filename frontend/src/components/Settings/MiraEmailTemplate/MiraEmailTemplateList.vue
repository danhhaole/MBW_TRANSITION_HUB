<template>
  <div class="flex h-full flex-col gap-6 p-6 text-ink-gray-8">
    <!-- Header -->
    <div class="flex justify-between px-2 pt-2">
      <div class="flex flex-col gap-1 w-9/12">
        <h2 class="flex gap-2 text-xl font-semibold leading-none h-5">
          {{ __('Email Templates') }}
        </h2>
        <p class="text-p-base text-ink-gray-6">
          {{ __('Manage email templates for campaigns and communications') }}
        </p>
      </div>
      <div class="flex item-center space-x-2 w-3/12 justify-end">
        <Button
          :label="__('New')"
          icon-left="plus"
          variant="solid"
          @click="emit('updateStep', 'new-template')"
        />
      </div>
    </div>

    <!-- Loading state -->
    <div
      v-if="templates.loading"
      class="flex mt-28 justify-between w-full h-full"
    >
      <Button
        :loading="templates.loading"
        variant="ghost"
        class="w-full"
        size="2xl"
      />
    </div>

    <!-- Empty State -->
    <div
      v-if="!templates.loading && !templates.data?.length"
      class="flex justify-between w-full h-full"
    >
      <div
        class="text-ink-gray-4 border border-dashed rounded w-full flex items-center justify-center"
      >
        {{ __('No email templates found') }}
      </div>
    </div>

    <!-- Search & Filters -->
    <div
      v-if="!templates.loading && templates.data?.length"
      class="flex flex-col gap-2 mb-4 px-2"
    >
      <div class="flex items-center gap-3">
        <TextInput
          ref="searchRef"
          v-model="search"
          :placeholder="__('Search by name or subject...')"
          class="flex-1"
          :debounce="300"
        >
          <template #prefix>
            <FeatherIcon name="search" class="h-4 w-4 text-ink-gray-6" />
          </template>
        </TextInput>
        <FormControl
          type="select"
          v-model="currentType"
          :options="typeOptions"
          class="w-48"
          :placeholder="__('Filter by type')"
        />
        <FormControl
          type="select"
          v-model="currentStatus"
          :options="statusOptions"
          class="w-40"
          :placeholder="__('Filter by status')"
        />
      </div>
      <div class="flex items-center justify-between text-sm text-ink-gray-5">
        <div>
          {{ __('Showing {0} of {1} templates', [templatesList.length, templates.data.length]) }}
        </div>
        <button
          v-if="search || currentType !== 'All' || currentStatus !== 'All'"
          @click="clearFilters"
          class="text-blue-600 hover:text-blue-700 font-medium"
        >
          {{ __('Clear filters') }}
        </button>
      </div>
    </div>

    <!-- Email template list -->
    <div
      class="flex flex-col overflow-hidden"
      v-if="!templates.loading && templates.data?.length"
    >
      <!-- No results from filter -->
      <div
        v-if="templatesList.length === 0"
        class="flex flex-col items-center justify-center py-12 text-center"
      >
        <FeatherIcon name="search" class="h-12 w-12 text-ink-gray-4 mb-3" />
        <p class="text-base font-medium text-ink-gray-7 mb-1">
          {{ __('No templates found') }}
        </p>
        <p class="text-sm text-ink-gray-5 mb-4">
          {{ __('Try adjusting your search or filters') }}
        </p>
        <Button
          :label="__('Clear filters')"
          variant="outline"
          @click="clearFilters"
        />
      </div>

      <!-- Template list -->
      <div v-else class="flex flex-col">
        <div class="flex items-center py-2 px-4 text-sm text-ink-gray-5">
          <div class="w-4/12">{{ __('Template Name') }}</div>
          <div class="w-2/12">{{ __('Type') }}</div>
          <div class="w-3/12">{{ __('Subject') }}</div>
          <div class="w-1/12">{{ __('Active') }}</div>
          <div class="w-1/12">{{ __('Default') }}</div>
          <div class="w-1/12"></div>
        </div>
        <div class="h-px border-t mx-4 border-outline-gray-modals" />
        <ul class="overflow-y-auto px-2">
        <template v-for="(template, i) in templatesList" :key="template.name">
          <li
            class="flex items-center justify-between p-3 cursor-pointer hover:bg-surface-menu-bar rounded"
            @click="() => emit('updateStep', 'edit-template', { ...template })"
          >
            <div class="flex flex-col w-4/12 pr-5">
              <div class="text-p-base font-medium text-ink-gray-7 truncate">
                {{ template.template_name || template.name }}
              </div>
              <div class="text-p-sm text-ink-gray-5 truncate">
                {{ formatDate(template.created_time) }}
              </div>
            </div>
            <div class="text-base text-ink-gray-6 w-2/12">
              <Badge
                :label="getTypeLabel(template.template_type)"
                variant="subtle"
                theme="blue"
              />
            </div>
            <div class="text-sm text-ink-gray-6 w-3/12 truncate pr-2">
              {{ template.subject || '-' }}
            </div>
            <div class="flex items-center w-1/12">
              <Switch
                size="sm"
                v-model="template.is_active"
                @update:model-value="toggleActive(template)"
                @click.stop
              />
            </div>
            <div class="flex items-center w-1/12">
              <Switch
                size="sm"
                v-model="template.default_template"
                @update:model-value="toggleDefault(template)"
                @click.stop
              />
            </div>
            <div class="w-1/12 flex justify-end">
              <Dropdown
                :options="getDropdownOptions(template)"
                placement="right"
                :button="{
                  icon: 'more-horizontal',
                  variant: 'ghost',
                  onblur: (e) => {
                    e.stopPropagation()
                    confirmDelete = false
                  },
                }"
                @click.stop
              />
            </div>
          </li>
          <div
            v-if="templatesList.length !== i + 1"
            class="h-px border-t mx-2 border-outline-gray-modals"
          />
        </template>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  TextInput,
  FormControl,
  Switch,
  Dropdown,
  FeatherIcon,
  Badge,
  Button,
} from 'frappe-ui'
import { ref, computed, inject } from 'vue'
import { useToast } from '@/composables/useToast'

const emit = defineEmits(['updateStep'])

const templates = inject('templates')
const toast = useToast()

const search = ref('')
const currentType = ref('All')
const currentStatus = ref('All')
const confirmDelete = ref(false)

const typeOptions = [
  { label: __('All Types'), value: 'All' },
  { label: __('Confirm Email'), value: 'confirm-email' },
  { label: __('Invited Email'), value: 'invited-email' },
  { label: __('Reject Email'), value: 'reject-email' },
  { label: __('Other Email'), value: 'other-email' },
]

const statusOptions = [
  { label: __('All Status'), value: 'All' },
  { label: __('Active'), value: 'active' },
  { label: __('Inactive'), value: 'inactive' },
  { label: __('Default'), value: 'default' },
]

function clearFilters() {
  search.value = ''
  currentType.value = 'All'
  currentStatus.value = 'All'
}

const templatesList = computed(() => {
  let list = templates.data || []

  // Search filter
  if (search.value) {
    list = list.filter(
      (template) =>
        template.template_name
          .toLowerCase()
          .includes(search.value.toLowerCase()) ||
        template.subject?.toLowerCase().includes(search.value.toLowerCase()),
    )
  }

  // Type filter
  if (currentType.value !== 'All') {
    list = list.filter(
      (template) => template.template_type === currentType.value,
    )
  }

  // Status filter
  if (currentStatus.value !== 'All') {
    if (currentStatus.value === 'active') {
      list = list.filter((template) => template.is_active)
    } else if (currentStatus.value === 'inactive') {
      list = list.filter((template) => !template.is_active)
    } else if (currentStatus.value === 'default') {
      list = list.filter((template) => template.default_template)
    }
  }

  return list
})

function toggleActive(template) {
  templates.setValue.submit(
    {
      name: template.name,
      is_active: template.is_active ? 1 : 0,
    },
    {
      onSuccess: () => {
        toast.success(
          template.is_active
            ? 'Template activated successfully'
            : 'Template deactivated successfully',
        )
      },
      onError: (error) => {
        toast.error(error.messages?.[0] || 'Failed to update template')
        template.is_active = !template.is_active
      },
    },
  )
}

function toggleDefault(template) {
  templates.setValue.submit(
    {
      name: template.name,
      default_template: template.default_template ? 1 : 0,
    },
    {
      onSuccess: () => {
        toast.success('Default template updated successfully')
      },
      onError: (error) => {
        toast.error(error.messages?.[0] || 'Failed to update template')
        template.default_template = !template.default_template
      },
    },
  )
}

function deleteTemplate(template) {
  confirmDelete.value = false
  templates.delete.submit(template.name, {
    onSuccess: () => {
      toast.success('Template deleted successfully')
    },
    onError: (error) => {
      toast.error(error.messages?.[0] || 'Failed to delete template')
    },
  })
}

function getDropdownOptions(template) {
  let options = [
    {
      label: __('Duplicate'),
      icon: 'copy',
      onClick: () => emit('updateStep', 'new-template', { ...template }),
    },
    {
      label: __('Delete'),
      icon: 'trash-2',
      onClick: (e) => {
        e.preventDefault()
        e.stopPropagation()
        confirmDelete.value = true
      },
      condition: () => !confirmDelete.value,
    },
    {
      label: __('Confirm Delete'),
      icon: 'trash-2',
      theme: 'red',
      onClick: () => deleteTemplate(template),
      condition: () => confirmDelete.value,
    },
  ]

  return options
}

function getTypeLabel(type) {
  const typeMap = {
    'confirm-email': 'Confirm',
    'invited-email': 'Invited',
    'reject-email': 'Reject',
    'other-email': 'Other',
  }
  return typeMap[type] || type || 'Other'
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}
</script>
