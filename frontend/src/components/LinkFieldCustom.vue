<template>
  <div class="link-field-custom">
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
      :custom-filter="customFilter"
      hide-no-data
      :menu-props="{ maxHeight: '300px' }"
    >
      <template #selection="{ item }">
        <!-- Chỉ hiển thị label khi đã chọn -->
        <span>{{ item.label }}</span>
      </template>

      <template #chip="{ props: chipProps, item }">
        <v-chip v-bind="chipProps">
          {{ item.label }}
        </v-chip>
      </template>

      <template #prepend-inner>
        <slot name="prefix" />
      </template>

      <template #item="{ props: itemProps, item }">
        <v-list-item v-bind="itemProps">
          <template #prepend>
            <slot name="item-prefix" :option="item" />
          </template>
          <v-list-item-title>
            <slot name="item-label" :option="item">
              {{ item.label }}
            </slot>
          </v-list-item-title>
          <v-list-item-subtitle v-if="item.description && item.description !== item.label">
            {{ item.description }}
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
import { useLinkFieldCustom } from '@/composables/useLinkFieldCustom'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  displayField: {
    type: String,
    default: null,
    // Ví dụ: 'full_name' cho User, 'customer_name' cho Customer, 'item_name' cho Item
  },
  searchField: {
    type: String,
    default: null,
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

// Sử dụng composable custom
const {
  options,
  loading,
  searchOptions,
  parsedFilters
} = useLinkFieldCustom(props)

// Tạo displayOptions để hiển thị trong dropdown
const displayOptions = computed(() => {
  const result = options.value.map(opt => ({
    value: opt.value,
    display: opt.label, // Chỉ hiển thị label trong dropdown
    raw: opt // Giữ nguyên data gốc
  }));
  
  console.log('Original options:', options.value);
  console.log('Display options:', result);
  
  return result;
});

const selectedValue = computed({
  get: () => {
    return props.modelValue || '';
  },
  set: (val) => {
    console.log('Setting value:', val);
    emit('update:modelValue', val);
    emit('change', val);
  }
});

// Watch để đồng bộ selectedValue với currentValue
watch(selectedValue, (newVal) => {
  if (newVal !== props.modelValue) {
    emit('update:modelValue', newVal);
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
  selectedValue.value = null;
  searchText.value = ''
}

// Khởi tạo
onMounted(() => {
  searchOptions('')
})

// Watch thay đổi doctype và filters
watch([() => props.doctype, () => props.displayField, parsedFilters], () => {
  searchOptions(searchText.value)
}, { deep: true })

// Watch để debug displayOptions
watch(displayOptions, (newVal) => {
  console.log('DisplayOptions changed:', newVal);
}, { deep: true });

const handleItemSelect = (item) => {
  console.log('Item selected:', item);
  selectedValue.value = item;
};

const getLabelFromValue = (value) => {
  const found = options.value.find(opt => opt.value === value);
  return found ? found.label : value;
};

const getItemTitle = (item) => {
  return item.label;
};

const getItemLabel = (item) => {
  return item.label;
};

const customFilter = (item, query) => {
  // Implement custom filter logic here
  return item.label.toLowerCase().includes(query.toLowerCase());
};
</script>

<style scoped>
.link-field-custom {
  width: 100%;
}

.v-label {
  color: rgb(var(--v-theme-on-surface));
  font-size: 0.875rem;
  font-weight: 400;
}

/* Ẩn subtitle trong selection input */
.link-field-custom :deep(.v-field__input .v-list-item-subtitle) {
  display: none !important;
}

/* Chỉ hiển thị title trong selection */
.link-field-custom :deep(.v-field__input .v-list-item-title) {
  display: block !important;
}
</style> 