<template>
  <Dialog v-model="show" :title="title">
    <div class="space-y-4">
      <!-- Title -->
      <FormControl
        type="text"
        label="Title"
        v-model="form.title"
        :error="formErrors.title"
        required
      />

      <!-- Description -->
      <FormControl
        type="textarea"
        label="Description"
        v-model="form.description"
        :error="formErrors.description"
      />

      <!-- Route -->
      <FormControl
        type="text"
        label="Route"
        v-model="form.route"
        :error="formErrors.route"
        required
      />

      <!-- Campaign -->
      <FormControl
        type="select"
        label="Campaign"
        v-model="form.campaign"
        :options="campaignOptions"
        :error="formErrors.campaign"
      />

      <!-- Status -->
      <FormControl
        type="select"
        label="Status"
        v-model="form.status"
        :options="store.statusOptions"
        :error="formErrors.status"
        required
      />

      <!-- Content -->
      <FormControl
        type="textarea"
        label="Content"
        v-model="form.content"
        :error="formErrors.content"
        rows="10"
      />
    </div>

    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" theme="gray" @click="show = false">
          {{ __('Cancel') }}
        </Button>
        <Button variant="solid" theme="gray" @click="handleSubmit" :loading="store.loading">
          {{ __('Save') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {  Button } from 'frappe-ui'
import { useLadiPageStore } from '@/stores/ladiPage'
import Dialog from 'frappe-ui/src/components/Dialog/Dialog.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  page: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'saved'])

// Initialize store
const store = useLadiPageStore()

// Form state
const form = ref({
  title: '',
  description: '',
  route: '',
  campaign: null,
  status: 'Draft',
  content: ''
})

const formErrors = ref({})

// Computed
const show = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const title = computed(() => props.page ? __('Edit Ladi Page') : __('Create Ladi Page'))

// Campaign options
const campaignOptions = ref([])
const loadCampaignOptions = async () => {
  try {
    const options = await store.fetchCampaignOptions()
    campaignOptions.value = options
  } catch (error) {
    console.error('Error loading campaign options:', error)
  }
}

// Reset form
const resetForm = () => {
  form.value = {
    title: '',
    description: '',
    route: '',
    campaign: null,
    status: 'Draft',
    content: ''
  }
  formErrors.value = {}
}

// Validate form
const validateForm = () => {
  const errors = {}

  if (!form.value.title?.trim()) {
    errors.title = __('Title is required')
  }

  if (!form.value.route?.trim()) {
    errors.route = __('Route is required')
  }

  if (!form.value.status) {
    errors.status = __('Status is required')
  }

  formErrors.value = errors
  return Object.keys(errors).length === 0
}

// Handle submit
const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    if (props.page) {
      await store.updateLadiPage(props.page.name, form.value)
    } else {
      await store.createLadiPage(form.value)
    }
    emit('saved')
    resetForm()
    show.value = false
  } catch (error) {
    console.error('Error saving Ladi page:', error)
    // Error will be handled by store and shown via toast
  }
}

// Watch for page prop changes to populate form
watch(() => props.page, (newPage) => {
  if (newPage) {
    form.value = {
      title: newPage.title || '',
      description: newPage.description || '',
      route: newPage.route || '',
      campaign: newPage.campaign || null,
      status: newPage.status || 'Draft',
      content: newPage.content || ''
    }
  } else {
    resetForm()
  }
}, { immediate: true })

// Initialize
loadCampaignOptions()
</script>