<template>
  <v-autocomplete
    v-model="selectedValue"
    :items="options"
    :loading="loading"
    :search="searchText"
    @update:search="handleSearch"
    :placeholder="placeholder"
    :label="label"
    :variant="variant"
    :clearable="true"
    item-value="value"
    item-title="label"
    hide-no-data
  >
    <!-- Khi đã chọn: chỉ hiển thị label -->
    <template #selection="{ item }">
      <span>{{ item.raw.label || item.raw.value }}</span>
    </template>

    <!-- Trong dropdown: hiển thị label + description -->
    <template #item="{ props: itemProps, item }">
      <v-list-item v-bind="itemProps">
        <v-list-item-title>{{ item.raw.label || item.raw.value }}</v-list-item-title>
        <v-list-item-subtitle v-if="item.raw.description && item.raw.description !== item.raw.value">
          {{ item.raw.description }}
        </v-list-item-subtitle>
      </v-list-item>
    </template>
  </v-autocomplete>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  doctype: { type: String, required: true },
  modelValue: { type: String, default: '' },
  label: { type: String, default: '' },
  placeholder: { type: String, default: 'Tìm kiếm...' },
  variant: { type: String, default: 'outlined' },
  filters: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:modelValue'])

const searchText = ref('')
const loading = ref(false)
const options = ref([])

const selectedValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const handleSearch = (query) => {
  searchText.value = query || ''
  searchOptions(query || '')
}

const searchOptions = async (query = '') => {
  if (!props.doctype) return
  loading.value = true
  
  try {
    const response = await call('frappe.desk.search.search_link', {
      doctype: props.doctype,
      txt: query,
      filters: props.filters,
      page_length: 20,
    })

    // Loại bỏ duplicate
    const seen = new Set()
    options.value = response.filter(item => {
      if (seen.has(item.value)) return false
      seen.add(item.value)
      return true
    })

  } catch (error) {
    console.error('Error:', error)
    options.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => searchOptions(''))
watch(() => props.doctype, () => searchOptions(''))
</script> 