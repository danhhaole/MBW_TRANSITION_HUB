<template>
  <div class="link-field">
    <v-label v-if="label" class="mb-2">{{ label }}</v-label>
    
    <v-autocomplete
      ref="autocomplete"
      v-model="selectedValue"
      :items="options"
      :loading="loading"
      :search="searchText"
      @update:search="handleSearch"
      :placeholder="placeholder"
      :size="size"
      :variant="variant"
      :clearable="true"
      item-title="label"
      item-value="value"
      no-filter
      hide-no-data
      :menu-props="{ maxHeight: '300px' }"
    >
      <template #selection="{ item }">
        <!-- Chỉ hiển thị label khi đã chọn -->
        <span>{{ item.raw.label }}</span>
      </template>

      <template #prepend-inner>
        <slot name="prefix" />
      </template>

      <template #item="{ props: itemProps, item }">
        <v-list-item v-bind="itemProps">
          <template #prepend>
            <slot name="item-prefix" :option="item.raw" />
          </template>
          <v-list-item-title>
            <slot name="item-label" :option="item.raw">
              {{ item.raw.label }}
            </slot>
          </v-list-item-title>
          <v-list-item-subtitle v-if="item.raw.description && item.raw.description !== item.raw.label">
            {{ item.raw.description }}
          </v-list-item-subtitle>
        </v-list-item>
      </template>

      <template #append-item>
        <v-divider v-if="onCreate || showClear"></v-divider>
        
        <v-list-item 
          v-if="onCreate && searchText"
          @click="handleCreate"
          class="text-primary"
        >
          <template #prepend>
            <v-icon>mdi-plus</v-icon>
          </template>
          <v-list-item-title>Tạo mới</v-list-item-title>
        </v-list-item>

        <v-list-item 
          v-if="showClear"
          @click="handleClear"
          class="text-error"
        >
          <template #prepend>
            <v-icon>mdi-close</v-icon>
          </template>
          <v-list-item-title>Xóa</v-list-item-title>
        </v-list-item>
      </template>
    </v-autocomplete>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useLinkField } from '@/composables/useLinkField'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  filters: {
    type: [Array, String],
    default: () => [],
  },
  modelValue: {
    type: [String, Object],
    default: '',
  },
  doc: { 
    type: Object, 
    default: () => ({}) 
  },
  hideMe: {
    type: Boolean,
    default: false,
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Tìm kiếm...',
  },
  size: {
    type: String,
    default: 'default',
  },
  variant: {
    type: String,
    default: 'outlined',
  },
  onCreate: {
    type: Function,
    default: null,
  },
  showClear: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

const autocomplete = ref(null)
const searchText = ref('')
const selectedValue = ref('')

// Sử dụng composable để xử lý logic
const {
  options,
  loading,
  searchOptions,
  parsedFilters
} = useLinkField(props)

// Debug log
watch(options, (newOptions) => {
  console.log('Options updated:', newOptions)
}, { deep: true })

// Computed để xử lý giá trị
const currentValue = computed({
  get: () => {
    return props.modelValue || ''
  },
  set: (val) => {
    emit('update:modelValue', val)
    emit('change', val)
  }
})

// Watch để đồng bộ selectedValue với currentValue
watch(currentValue, (newVal) => {
  selectedValue.value = newVal
}, { immediate: true })

// Watch để đồng bộ ngược lại
watch(selectedValue, (newVal) => {
  if (newVal !== currentValue.value) {
    currentValue.value = newVal
  }
})

// Xử lý tìm kiếm
const handleSearch = (query) => {
  searchText.value = query || ''
  searchOptions(query || '')
}

// Xử lý tạo mới
const handleCreate = () => {
  if (props.onCreate && searchText.value) {
    props.onCreate(searchText.value, () => {
      // Callback khi tạo xong
      searchOptions(searchText.value)
    })
  }
}

// Xử lý xóa
const handleClear = () => {
  selectedValue.value = ''
  currentValue.value = ''
  searchText.value = ''
}

// Khởi tạo
onMounted(() => {
  searchOptions('')
})

// Watch thay đổi doctype và filters
watch([() => props.doctype, parsedFilters], () => {
  searchOptions(searchText.value)
}, { deep: true })
</script>

<style scoped>
.link-field {
  width: 100%;
}

.v-label {
  color: rgb(var(--v-theme-on-surface));
  font-size: 0.875rem;
  font-weight: 400;
}
</style> 