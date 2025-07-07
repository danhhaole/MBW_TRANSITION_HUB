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
      item-value="value"
      item-title="label"
      :menu-props="{ maxHeight: '300px' }"
      persistent-search
      open-on-clear
      eager
    >
      <template #item="{ props, item }">
        <v-list-item v-bind="props">
          <template #prepend>
            <slot name="item-prefix" :option="item" />
          </template>
          <v-list-item-title class="text-body-2">
            {{ item.description }}
          </v-list-item-title>
          <v-list-item-subtitle class="text-caption">
            {{ item.value }}
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
import { createResource } from 'frappe-ui'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  displayField: {
    type: String,
    default: null,
    // Ví dụ: 'full_name' cho User, 'customer_name' cho Customer
  },
  searchField: {
    type: String,
    default: null,
  },
  mode: {
    type: String,
    default: 'auto', // 'auto', 'custom', 'simple'
    validator: (value) => ['auto', 'custom', 'simple'].includes(value)
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

// Reactive state
const autocomplete = ref(null)
const searchText = ref('')
const options = ref([])
const loading = ref(false)

// Computed để lọc options có kết quả
const filteredOptions = computed(() => {
  return options.value.filter(item => {
    if (!searchText.value) return true
    return filterSearch(item, searchText.value)
  })
})

// Parse filters với eval support
const parsedFilters = computed(() => {
  if (!Array.isArray(props.filters)) {
    return props.filters || []
  }
  
  return props.filters.map((f) => {
    if (Array.isArray(f) && typeof f[3] === 'string' && f[3].startsWith('eval:')) {
      // Cắt bỏ 'eval:' và trim path, vd "doc.country_id"
      const path = f[3].slice(5).trim().split('.')
      // Lấy giá trị từ props.doc theo đường dẫn
      let val = props[path[0]] // Đầu tiên: props["doc"]
      for (let i = 1; i < path.length; i++) {
        val = val?.[path[i]]
      }
      return [f[0], f[1], f[2], val]
    }
    return f
  })
})

// Computed để xử lý giá trị với selectedValue
const selectedValue = computed({
  get: () => {
    return props.modelValue || null
  },
  set: (val) => {
    emit('update:modelValue', val || '')
    emit('change', val || '')
  }
})

// Debounce function
let debounceTimer = null
const debounce = (func, delay) => {
  return (...args) => {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => func.apply(this, args), delay)
  }
}


// Hàm search duy nhất
const searchOptions = async (query = '') => {
  if (!props.doctype) return

  loading.value = true
  
  try {
    const resource = createResource({
      url: 'mbw_mira.api.link_search.search_link_custom',
      method: 'POST',
      auto: false
    })
    
    const response = await resource.fetch({
      doctype: props.doctype,
      txt: query,
      filters: parsedFilters.value,
      page_length: 20,
      searchfield: props.searchField,
      display_field: props.displayField,
      ignore_user_permissions: true
    })

    console.log('Search Response:', response)

    console.log('API Response:', response)
    
    // Transform data - dùng description làm label chính
    options.value = response.map(item => ({
      value: item.value,
      label: item.description,  // Hiển thị description làm label chính
      description: item.value   // Value làm description phụ
    }))

    // Thêm option "@me" cho User doctype nếu không hideMe và đang search rỗng
    if (!query && !props.hideMe && props.doctype === 'User') {
      const hasMe = options.value.some(item => item.value === '@me')
      if (!hasMe) {
        options.value.unshift({
          value: '@me',
          label: '@me',
          description: 'Current User'
        })
      }
    }

  } catch (error) {
    console.error('Error searching:', error)
    options.value = []
  } finally {
    loading.value = false
  }
}

// Debounced search function
const debouncedSearch = debounce(searchOptions, 300)

// Custom filter function cho local search
const filterSearch = (item, query, itemText) => {
  if (!query) return true

  const searchQuery = query.toLowerCase().trim()
  const label = (item.label || '').toLowerCase()
  const description = (item.description || '').toLowerCase()
  const value = (item.value || '').toLowerCase()

  // Tìm trong tất cả các trường
  return label.includes(searchQuery) || 
         description.includes(searchQuery) || 
         value.includes(searchQuery)
}

// Xử lý tìm kiếm - kết hợp cả server và client search
const handleSearch = (query) => {
  searchText.value = query || ''
  
  // Nếu query quá ngắn, chỉ search local
  if (!query || query.length < 2) {
    return
  }

  // Ngược lại thì search server
  debouncedSearch(query)
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
  selectedValue.value = null
  searchText.value = ''
}

// Khởi tạo
onMounted(() => {
  searchOptions('')
})

// Watch thay đổi doctype, displayField và filters
watch([() => props.doctype, () => props.displayField, () => props.mode, parsedFilters], () => {
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

/* Ẩn subtitle trong selection input */
.link-field :deep(.v-field__input .v-list-item-subtitle) {
  display: none !important;
}

/* Chỉ hiển thị title trong selection */
.link-field :deep(.v-field__input .v-list-item-title) {
  display: block !important;
}

/* Xóa background khi không có selection */
.link-field :deep(.v-field__input) {
  background: transparent !important;
}

/* Style cho dropdown items */
.link-field :deep(.v-list-item-title) {
  font-weight: 500 !important;
}

.link-field :deep(.v-list-item-subtitle) {
  opacity: 0.8;
  margin-top: 2px;
}

/* Đảm bảo placeholder hiển thị đúng */
.link-field :deep(.v-field__input input::placeholder) {
  opacity: 0.6;
}
</style> 