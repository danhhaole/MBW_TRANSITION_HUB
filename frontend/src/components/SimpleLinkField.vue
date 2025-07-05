<template>
  <div class="simple-link-field">
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
      :menu-props="{ maxHeight: '300px' }"
    >
      <!-- Khi đã chọn - chỉ hiển thị label -->
      <template #selection="{ item }">
        <span>{{ item.raw.label || item.raw.value }}</span>
      </template>

      <!-- Trong dropdown - hiển thị label + description -->
      <template #item="{ props: itemProps, item }">
        <v-list-item v-bind="itemProps">
          <v-list-item-title>{{ item.raw.label || item.raw.value }}</v-list-item-title>
          <v-list-item-subtitle v-if="item.raw.description && item.raw.description !== item.raw.value">
            {{ item.raw.description }}
          </v-list-item-subtitle>
        </v-list-item>
      </template>
    </v-autocomplete>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { call } from 'frappe-ui'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Tìm kiếm...',
  },
  variant: {
    type: String,
    default: 'outlined',
  },
  filters: {
    type: Array,
    default: () => [],
  },
})

const emit = defineEmits(['update:modelValue'])

const searchText = ref('')
const loading = ref(false)
const rawOptions = ref([])

const selectedValue = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// Chỉ loại bỏ duplicate, giữ nguyên format
const options = computed(() => {
  return rawOptions.value
})

const handleSearch = async (query) => {
  searchText.value = query || ''
  await searchOptions(query || '')
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

    // Transform dữ liệu - loại bỏ duplicate
    const seen = new Set()
    const uniqueData = response.filter(item => {
      const key = item.value
      if (seen.has(key)) {
        return false
      }
      seen.add(key)
      return true
    })

    rawOptions.value = uniqueData

  } catch (error) {
    console.error('Error fetching link options:', error)
    rawOptions.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  searchOptions('')
})

watch(() => props.doctype, () => {
  searchOptions('')
})
</script>

<style scoped>
.simple-link-field {
  width: 100%;
}
</style> 