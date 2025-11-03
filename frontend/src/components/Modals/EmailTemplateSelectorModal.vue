<template>
  <Dialog
    v-model="show"
    :options="{ title: __('Email Templates'), size: '4xl' }"
  >
    <template #body-content>
      <div class="flex items-center gap-3 mb-2">
        <TextInput
          ref="searchInput"
          v-model="search"
          type="text"
          :placeholder="__('Search templates...')"
          class="flex-1"
        >
          <template #prefix>
            <FeatherIcon name="search" class="h-4 w-4 text-gray-500" />
          </template>
        </TextInput>
        <Button
          :label="__('Create')"
          icon-left="plus"
          variant="solid"
          @click.stop="openSettings"
        />
      </div>
      <div
        v-if="filteredTemplates.length"
        class="mt-2 grid max-h-[560px] sm:grid-cols-3 gris-cols-1 gap-2 overflow-y-auto"
      >
        <div
          v-for="template in filteredTemplates"
          :key="template.name"
          class="flex h-56 cursor-pointer flex-col gap-2 rounded-lg border p-3 hover:bg-gray-100 transition-colors"
          @click.stop="emit('apply', template)"
        >
          <div class="flex items-center justify-between border-b pb-2">
            <div class="text-base font-semibold truncate">
              {{ template.template_name || template.name }}
            </div>
            <div class="flex gap-1">
              <span v-if="template.is_active" class="px-2 py-0.5 text-xs bg-green-100 text-green-700 rounded">
                {{ __('Active') }}
              </span>
              <span v-if="template.default_template" class="px-2 py-0.5 text-xs bg-blue-100 text-blue-700 rounded">
                {{ __('Default') }}
              </span>
            </div>
          </div>
          <div v-if="template.subject" class="text-sm text-gray-600 truncate">
            <span class="font-medium">{{ __('Subject:') }}</span> {{ template.subject }}
          </div>
          <div v-if="template.template_type" class="text-xs text-gray-500">
            <span class="font-medium">{{ __('Type:') }}</span> {{ getTypeLabel(template.template_type) }}
          </div>
          <TextEditor
            v-if="template.message"
            :content="template.message"
            :editable="false"
            editor-class="!prose-sm max-w-none !text-sm text-gray-600 focus:outline-none"
            class="flex-1 overflow-hidden"
          />
        </div>
      </div>
      <div v-else class="mt-2">
        <div class="flex h-56 flex-col items-center justify-center">
          <FeatherIcon name="inbox" class="h-12 w-12 text-gray-400 mb-3" />
          <div class="text-lg font-medium text-gray-700">
            {{ __('No templates found') }}
          </div>
          <div class="text-sm text-gray-500 mt-1">
            {{ search ? __('Try a different search term') : __('Create your first email template') }}
          </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { TextEditor, createListResource } from 'frappe-ui'
import { ref, computed, nextTick, watch, onMounted } from 'vue'

const props = defineProps({
  doctype: {
    type: String,
    default: '',
  },
})

const show = defineModel()
const searchInput = ref('')

const emit = defineEmits(['apply', 'openSettings', 'close'])

const search = ref('')

const templates = createListResource({
  type: 'list',
  doctype: 'Mira Email Template',
  cache: ['MiraEmailTemplates', props.doctype],
  fields: [
    'name',
    'template_name',
    'template_type',
    'subject',
    'message',
    'is_active',
    'default_template',
  ],
  filters: { is_active: 1 },
  orderBy: 'modified desc',
  pageLength: 99999,
})

onMounted(() => {
  if (templates.data == null) {
    templates.fetch()
  }
})

const filteredTemplates = computed(() => {
  if (!templates.data) return []
  
  return templates.data.filter((template) => {
    if (!search.value) return true
    
    const searchLower = search.value.toLowerCase()
    return (
      template.template_name?.toLowerCase().includes(searchLower) ||
      template.subject?.toLowerCase().includes(searchLower) ||
      template.name?.toLowerCase().includes(searchLower)
    )
  })
})

const getTypeLabel = (type) => {
  const labels = {
    'confirm-email': 'Confirm Email',
    'invited-email': 'Invited Email',
    'reject-email': 'Reject Email',
    'other-email': 'Other Email',
  }
  return labels[type] || type
}

const openSettings = () => {
  show.value = false
  emit('openSettings')
}

watch(show, (value) => {
  if (value) {
    nextTick(() => searchInput.value?.el?.focus())
  } else {
    // Emit close event to parent
    emit('close')
  }
})
</script>
