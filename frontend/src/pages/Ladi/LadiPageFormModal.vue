<template>
  <Dialog v-model="show" :options="{ size: 'lg' }">
    <template #body-title>
      <h3 class="flex items-center gap-2 text-2xl font-semibold leading-6 text-ink-gray-9">
        <div>{{ title }}</div>
      </h3>
    </template>
    <template #body-content>
      <div class="space-y-4">
        <!-- Title -->
        <FormControl
          type="text"
          :label="__('Page Title')"
          v-model="form.title"
          :error="formErrors.title"
          required
        />

        <!-- Route -->
        <FormControl
          type="text"
          :label="__('Slug')"
          v-model="form.route"
          :error="formErrors.route"
          required
        />

        <!-- Campaign -->
        <FormControl
          type="select"
          :label="__('Campaign')"
          v-model="form.campaign"
          :options="campaignOptions"
          :error="formErrors.campaign"
        />

        <!-- Published -->
        <FormControl
          type="checkbox"
          :label="__('Published')"
          v-model="form.published"
          :error="formErrors.published"
        />
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" theme="gray" @click="show = false">
          {{ __('Cancel') }}
        </Button>
        <Button variant="solid" theme="gray" @click="handleSubmit" :loading="store.loading">
          {{ __('Save') }}
        </Button>
        <Button 
          v-if="!isEdit" 
          variant="solid" 
          theme="blue" 
          @click="handleSubmitAndEdit" 
          :loading="store.loading"
        >
          {{ __('Save & Edit') }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Button, FormControl } from 'frappe-ui'
import { Dialog } from 'frappe-ui'
import { useLadiPageStore } from '@/stores/ladiPage'

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

// Initialize store and router
const store = useLadiPageStore()
const router = useRouter()

// Form state
const form = ref({
  title: '',
  route: '',
  campaign: null,
  published: false
})

const formErrors = ref({})

// Computed
const show = defineModel()
const title = computed(() => props.page ? __('Edit Ladi Page') : __('Create Ladi Page'))
const isEdit = computed(() => !!props.page)

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
    route: '',
    campaign: null,
    published: false
  }
  formErrors.value = {}
}

// Validate form
const validateForm = () => {
  const errors = {}

  if (!form.value.title?.trim()) {
    errors.title = __('Page Title is required')
  }

  if (!form.value.route?.trim()) {
    errors.route = __('Route is required')
  }

  formErrors.value = errors
  return Object.keys(errors).length === 0
}

// Handle submit
const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    let pageName
    if (props.page) {
      await store.updateLadiPage(props.page.name, form.value)
      pageName = props.page.name
    } else {
      const response = await store.createLadiPage(form.value)
      pageName = response.name
    }
    emit('saved')
    resetForm()
    show.value = false
    return pageName
  } catch (error) {
    console.error('Error saving Ladi page:', error)
    // Error will be handled by store and shown via toast
  }
}

// Handle submit and edit
const handleSubmitAndEdit = async () => {
  const pageName = await handleSubmit()
  if (pageName) {
    router.push({ name: 'ladi-page-editor', params: { id: pageName } })
  }
}

// Watch for page prop changes to populate form
watch(() => props.page, (newPage) => {
  if (newPage) {
    form.value = {
      title: newPage.title || '',
      route: newPage.route || '',
      campaign: newPage.campaign || null,
      published: newPage.published || false
    }
  } else {
    resetForm()
  }
}, { immediate: true })

// Initialize
loadCampaignOptions()
</script>