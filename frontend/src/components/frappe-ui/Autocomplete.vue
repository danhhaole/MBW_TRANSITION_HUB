<template>
  <div class="autocomplete-wrapper">
    <Combobox
      v-model="selectedValue"
      :multiple="multiple"
      nullable
      v-slot="{ open: isComboboxOpen }"
    >
      <Popover
        class="w-full"
        v-model:show="showOptions"
        ref="rootRef"
        :placement="placement"
      >
        <template
          #target="{ open: openPopover, togglePopover, close: closePopover }"
        >
          <slot
            name="target"
            v-bind="{
              open: openPopover,
              close: closePopover,
              togglePopover,
              isOpen: isComboboxOpen,
            }"
          >
            <div class="w-full space-y-1.5">
              <label v-if="props.label" class="block text-xs text-gray-500">
                {{ props.label }}
              </label>
              <button
                class="flex h-8 w-full items-center justify-between gap-2 rounded bg-gray-100 px-3 py-1.5 transition-colors hover:bg-gray-200 border border-transparent focus:border-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300"
                :class="{ 'bg-gray-200': isComboboxOpen }"
                @click="togglePopover"
              >
                <div class="flex items-center overflow-hidden">
                  <slot name="prefix" />
                  <span
                    class="truncate text-sm leading-5 text-gray-800"
                    v-if="displayValue"
                  >
                    {{ displayValue }}
                  </span>
                  <span class="text-sm leading-5 text-gray-400" v-else>
                    {{ placeholder || 'Chọn một tùy chọn' }}
                  </span>
                  <slot name="suffix" />
                </div>
                <FeatherIcon
                  name="chevron-down"
                  class="h-4 w-4 text-gray-500"
                  aria-hidden="true"
                />
              </button>
            </div>
          </slot>
        </template>
        <template #body="{ isOpen, togglePopover }">
          <div v-show="isOpen" class="relative">
            <div
              class="mt-1 rounded-lg bg-white text-sm shadow-lg border border-gray-200"
              :class="bodyClasses"
            >
              <ComboboxOptions
                class="max-h-60 overflow-y-auto px-2 pb-2"
                :class="{ 'pt-2': hideSearch }"
                static
              >
                <div
                  v-if="!hideSearch"
                  class="sticky top-0 z-10 flex items-stretch space-x-2 bg-white py-2"
                >
                  <div class="relative w-full">
                    <ComboboxInput
                      ref="searchInput"
                      class="w-full rounded border border-gray-300 px-3 py-1.5 text-sm focus:bg-gray-100 hover:bg-gray-50 text-gray-800"
                      type="text"
                      :value="query"
                      @change="query = $event.target.value"
                      autocomplete="off"
                      placeholder="Tìm kiếm"
                    />
                    <div
                      class="absolute right-0 top-0 inline-flex h-8 w-8 items-center justify-center"
                    >
                      <LoadingIndicator
                        v-if="loading"
                        class="h-4 w-4 text-gray-500"
                      />
                      <button v-else @click="clearAll">
                        <FeatherIcon name="x" class="h-4 w-4 text-gray-600" />
                      </button>
                    </div>
                  </div>
                </div>
                <div v-if="groups.length === 0 && !loading" class="px-3 py-2 text-sm text-gray-500">
                  Không có tùy chọn nào
                </div>
                <div
                  v-for="group in groups"
                  :key="group.key"
                  v-show="group.items.length > 0"
                >
                  <div
                    v-if="group.group && !group.hideLabel"
                    class="sticky top-10 truncate bg-white px-3 py-1.5 text-xs font-medium text-gray-500"
                  >
                    {{ group.group }}
                  </div>
                  <ComboboxOption
                    as="template"
                    v-for="(option, idx) in group.items.slice(0, 50)"
                    :key="idx"
                    :value="option"
                    :disabled="option.disabled"
                    v-slot="{ active, selected }"
                  >
                    <li
                      :class="[
                        'flex cursor-pointer items-center justify-between rounded px-3 py-1.5 text-sm',
                        {
                          'bg-gray-100': active,
                          'opacity-50': option.disabled,
                        },
                      ]"
                    >
                      <div class="flex flex-1 gap-2 overflow-hidden">
                        <div
                          v-if="$slots['item-prefix'] || props.multiple"
                          class="flex flex-shrink-0"
                        >
                          <slot
                            name="item-prefix"
                            v-bind="{ active, selected, option }"
                          >
                            <FeatherIcon
                              name="check"
                              v-if="isOptionSelected(option)"
                              class="h-4 w-4 text-gray-600"
                            />
                            <div v-else class="h-4 w-4" />
                          </slot>
                        </div>
                        <div class="flex-1 truncate">
                          <span class="block text-gray-700 font-medium">
                            {{ option.value || '' }} <!-- Hiển thị value trên -->
                          </span>
                          <span class="block text-xs text-gray-500" v-if="option.title">
                            {{ option.title || '' }} <!-- Hiển thị title dưới -->
                          </span>
                        </div>
                      </div>
                    </li>
                  </ComboboxOption>
                </div>
              </ComboboxOptions>
              <div
                v-if="$slots.footer || props.showFooter || multiple"
                class="border-t border-gray-200 p-2"
              >
                <slot name="footer" v-bind="{ togglePopover }">
                  <div v-if="multiple" class="flex items-center justify-end">
                    <Button
                      v-if="!areAllOptionsSelected"
                      label="Chọn tất cả"
                      @click.stop="selectAll"
                    />
                    <Button
                      v-if="areAllOptionsSelected"
                      label="Xóa tất cả"
                      @click.stop="clearAll"
                    />
                  </div>
                  <div v-else class="flex items-center justify-end">
                    <Button label="Xóa" @click.stop="clearAll" />
                  </div>
                </slot>
              </div>
            </div>
          </div>
        </template>
      </Popover>
    </Combobox>
  </div>
</template>

<script setup>
import {
  Combobox,
  ComboboxInput,
  ComboboxOption,
  ComboboxOptions,
} from '@headlessui/vue'
import { computed, nextTick, ref, watch } from 'vue'
import {LoadingIndicator, Popover, Button, FeatherIcon , call, debounce } from 'frappe-ui'

const props = defineProps({
  modelValue: {
    default: undefined,
  },
  options: {
    default: () => [],
  },
  multiple: {
    type: Boolean,
    default: false,
  },
  hideSearch: {
    type: Boolean,
    default: false,
  },
  label: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  showFooter: {
    type: Boolean,
    default: false,
  },
  bodyClasses: {
    type: [String, Array],
    default: '',
  },
  placement: {
    type: String,
    default: 'bottom-start',
  },
  doctype: {
    type: String,
    default: '',
  },
  filters: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue', 'update:query', 'change'])

const searchInput = ref()
const showOptions = ref(false)
const query = ref('')
const options = ref([])
const loading = ref(false)
const searchFields = ref(['title']) // Mặc định dựa trên dữ liệu của bạn

const fetchSearchFields = async () => {
  if (!props.doctype) {
    console.log('Không có doctype, sử dụng trường mặc định:', searchFields.value)
    return
  }
  console.log('Đang lấy trường tìm kiếm cho doctype:', props.doctype)
  try {
    const response = await call('frappe.client.get', {
      doctype: 'DocType',
      name: props.doctype,
      fields: ['search_fields'],
    })
    if (response.search_fields) {
      searchFields.value = response.search_fields.split(',').map(field => field.trim())
    } else {
      searchFields.value = ['title'] // Mặc định là 'title'
      console.log('Không có search_fields trong doctype, mặc định là:', searchFields.value)
    }
  } catch (error) {
    console.error('Lỗi khi lấy trường tìm kiếm:', error)
    searchFields.value = ['title']
  }
  console.log('Trường tìm kiếm hiện tại:', searchFields.value)
}

const fetchOptions = debounce(async (searchQuery) => {
  if (!searchQuery || !props.doctype) {
    options.value = []
    console.log('Không có truy vấn hoặc doctype, xóa options')
    return
  }
  loading.value = true
  try {
    console.log('Đang lấy options với trường:', searchFields.value, 'cho truy vấn:', searchQuery)
    const response = await call('frappe.desk.search.search_link', {
      doctype: props.doctype,
      txt: searchQuery,
      filters: props.filters || {},
      query: 'frappe.desk.search.search_link',
      reference_doctype: props.doctype,
      fields: searchFields.value,
    })
    console.log('Phản hồi options:', response)
    options.value = response.results.map((item) => {
      const labelField = searchFields.value[0] || 'title'
      const option = {
        label: item[labelField] || item.title || '',
        value: item.name || item.value || '', // Sử dụng 'value' từ dữ liệu
        title: item.title || '', // Giữ title để hiển thị
        ...item,
      }
      console.log('Option đã xử lý:', option)
      return option
    })
  } catch (error) {
    console.error('Lỗi khi lấy options:', error)
    options.value = []
  } finally {
    loading.value = false
  }
}, 300)

const getExtendedInfo = (option) => {
  if (!option || !option.value) {
    return ''
  }
  return `Mã: ${option.value}`
}

watch(
  () => props.doctype,
  (newDoctype) => {
    if (newDoctype) {
      fetchSearchFields()
    }
  },
  { immediate: true }
)

watch(query, (newQuery) => {
  console.log('Truy vấn thay đổi:', newQuery)
  fetchOptions(newQuery)
})

watch(showOptions, (newValue) => {
  console.log('Hiển thị options:', newValue)
})

const groups = computed(() => {
  console.log('Tính toán groups, options:', options.value, 'props.options:', props.options)
  if (!options.value.length && !props.options.length) return []
  if (props.options.length) {
    return [
      {
        key: 0,
        group: '',
        items: filterOptions(sanitizeOptions(props.options)),
        hideLabel: true,
      },
    ]
  }
  return [
    {
      key: 0,
      group: '',
      items: filterOptions(sanitizeOptions(options.value)),
      hideLabel: true,
    },
  ]
})

const allOptions = computed(() => {
  const opts = groups.value.flatMap((group) => group.items)
  console.log('Tất cả options:', opts)
  return opts
})

const sanitizeOptions = (options) => {
  if (!options) return []
  return options.map((option) => {
    return typeof option === 'object' && option !== null
      ? { label: option.title || option.label || '', value: option.value || option.name || '', title: option.title || '', ...option }
      : { label: option.toString(), value: option }
  })
}

const filterOptions = (options) => {
  if (!query.value) return options
  const filtered = options.filter((option) => {
    return (
      (option.label || '').toLowerCase().includes(query.value.trim().toLowerCase()) ||
      (option.value || '')
        .toString()
        .toLowerCase()
        .includes(query.value.trim().toLowerCase()) ||
      (option.title || '').toLowerCase().includes(query.value.trim().toLowerCase())
    )
  })
  console.log('Options đã lọc:', filtered)
  return filtered
}

const selectedValue = computed({
  get() {
    if (!props.multiple) {
      const opt = findOption(props.modelValue) || makeOption(props.modelValue)
      console.log('Giá trị đã chọn (single):', opt)
      return opt
    }
    const values = props.modelValue || []
    const opts = typeof values[0] === 'object' && values[0] !== null
      ? values
      : values.map((v) => findOption(v) || makeOption(v))
    console.log('Giá trị đã chọn (multiple):', opts)
    return opts
  },
  set(val) {
    console.log('Đặt giá trị đã chọn:', val)
    query.value = ''
    if (val && !props.multiple) showOptions.value = false
    emit('update:modelValue', val)
  },
})

const findOption = (option) => {
  if (!option) return option
  const value = typeof option === 'object' && option !== null ? option.value : option
  return allOptions.value.find((o) => o.value === value)
}

const makeOption = (option) => {
  return typeof option === 'object' && option !== null
    ? { label: option.title || option.label || '', value: option.value || option.name || '', title: option.title || '', ...option }
    : { label: option, value: option }
}

const getLabel = (option) => {
  if (typeof option === 'object' && option !== null) {
    return option.label || option.title || option.value
  }
  return option
}

const displayValue = computed(() => {
  if (!selectedValue.value) return ''
  if (!props.multiple) {
    return getLabel(selectedValue.value)
  }
  return selectedValue.value.map((v) => getLabel(v)).join(', ')
})

const isOptionSelected = (option) => {
  if (!selectedValue.value) return false
  const value = typeof option === 'object' && option !== null ? option.value : option
  if (!props.multiple) {
    return selectedValue.value === value
  }
  return selectedValue.value.find((v) =>
    typeof v === 'object' && v !== null ? v.value === value : v === value
  )
}

const areAllOptionsSelected = computed(() => {
  if (!props.multiple) return false
  return allOptions.value.length === (selectedValue.value || []).length
})

const selectAll = () => {
  selectedValue.value = allOptions.value
}

const clearAll = () => {
  selectedValue.value = props.multiple ? [] : undefined
}

const isOption = (option) => {
  return typeof option === 'object' && option !== null
}

const isOptionGroup = (option) => {
  return typeof option === 'object' && option !== null && 'items' in option && 'group' in option
}

watch(
  () => query.value,
  () => {
    emit('update:query', query.value)
  }
)

watch(
  () => showOptions.value,
  () => {
    if (showOptions.value) {
      nextTick(() => {
        if (searchInput.value?.$el) {
          searchInput.value.$el.focus()
          console.log('Đã focus vào input tìm kiếm')
        }
      })
    }
  }
)

const rootRef = ref()

const togglePopover = () => {
  showOptions.value = !showOptions.value
  console.log('Đã toggle popover, showOptions:', showOptions.value)
}

defineExpose({
  rootRef,
  togglePopover,
})
</script>

<style scoped>
.autocomplete-wrapper {
  position: relative;
}
</style>
