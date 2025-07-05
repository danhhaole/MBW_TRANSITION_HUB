import { ref, computed, watch } from 'vue'
import { call } from 'frappe-ui'

export function useLinkFieldCustom(props) {
  const options = ref([])
  const loading = ref(false)
  const searchText = ref('')

  // Parse filters tương tự như component gốc
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

  // Debounce function
  let debounceTimer = null
  const debounce = (func, delay) => {
    return (...args) => {
      clearTimeout(debounceTimer)
      debounceTimer = setTimeout(() => func.apply(this, args), delay)
    }
  }

  // Hàm tìm kiếm options sử dụng API custom
  const searchOptions = async (query = '') => {
    if (!props.doctype) return

    loading.value = true
    
    try {
      const response = await call('mbw_mira.api.link_search.search_link_custom', {
        doctype: props.doctype,
        txt: query,
        display_field: props.displayField, // Field để hiển thị làm description
        filters: parsedFilters.value,
        page_length: 20,
        searchfield: props.searchField,
        ignore_user_permissions: true,
      })

      console.log(`Custom API Response for ${props.doctype}:`, response)

      // Transform dữ liệu từ API custom
      let allData = response.map((item) => ({
        label: item.label || item.value,
        value: item.value,
        description: item.description || '',
        raw: item
      }))

      // Thêm option "@me" cho User doctype nếu không hideMe
      if (!props.hideMe && props.doctype === 'User') {
        const hasMe = allData.some(item => item.value === '@me')
        if (!hasMe) {
          allData.unshift({
            label: '@me',
            value: '@me',
            description: 'Current User',
            raw: { value: '@me', label: '@me', description: 'Current User' }
          })
        }
      }

      options.value = allData
    } catch (error) {
      console.error('Error fetching custom link options:', error)
      options.value = []
    } finally {
      loading.value = false
    }
  }

  // Debounced search function
  const debouncedSearch = debounce(searchOptions, 300)

  // Watch parsedFilters để tự động reload khi filters thay đổi
  watch(parsedFilters, () => {
    searchOptions(searchText.value)
  }, { deep: true })

  return {
    options,
    loading,
    searchOptions: debouncedSearch,
    parsedFilters,
  }
} 