import { ref, computed, watch } from 'vue'
import { call } from 'frappe-ui'

export function useLinkField(props) {
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

  // Hàm tìm kiếm options
  const searchOptions = async (query = '') => {
    if (!props.doctype) return

    loading.value = true
    
    try {
      // Sử dụng get_list để có thể custom fields
      let fields = ['name']
      let searchFields = ['name']
      
      // Lấy meta để biết có title_field không
      const metaResponse = await call('frappe.client.get_meta', {
        doctype: props.doctype
      })
      
      const meta = metaResponse
      
      // Thêm title field nếu có
      if (meta.title_field) {
        fields.push(meta.title_field)
      }
      
      // Thêm search fields nếu có
      if (meta.search_fields) {
        const searchFieldsList = meta.search_fields.split(',').map(f => f.trim())
        fields = [...fields, ...searchFieldsList]
        searchFields = [...searchFields, ...searchFieldsList]
      }
      
      // Loại bỏ duplicate fields
      fields = [...new Set(fields)]
      
      // Tạo or_filters cho search
      let orFilters = []
      if (query) {
        searchFields.forEach(field => {
          orFilters.push([props.doctype, field, 'like', `%${query}%`])
        })
      }

      const response = await call('frappe.client.get_list', {
        doctype: props.doctype,
        fields: fields,
        filters: parsedFilters.value,
        or_filters: orFilters,
        limit_page_length: 20,
        order_by: 'name asc'
      })

      console.log(`API Response for ${props.doctype}:`, response)
      console.log('Meta:', meta)

      // Transform dữ liệu
      let allData = response.map((item) => {
        let displayLabel = item.name
        let description = ''
        
        // Tạo description từ các field khác
        if (meta.title_field && item[meta.title_field] && item[meta.title_field] !== item.name) {
          description = item[meta.title_field]
        } else {
          // Tìm field đầu tiên khác name để làm description
          const descriptionFields = fields.filter(f => f !== 'name' && item[f] && item[f] !== item.name)
          if (descriptionFields.length > 0) {
            description = item[descriptionFields[0]]
          }
        }
        
        // Nếu vẫn không có description hoặc giống name, dùng doctype-specific logic
        if (!description || description === item.name) {
          description = getDefaultDescription(props.doctype, item)
        }
        
        return {
          label: displayLabel,
          value: item.name,
          description: description || displayLabel,
          raw: item
        }
      })

      // Loại bỏ duplicate dựa trên value
      const uniqueData = allData.filter((item, index, self) => 
        index === self.findIndex(t => t.value === item.value)
      )

      // Thêm option "@me" cho User doctype nếu không hideMe
      if (!props.hideMe && props.doctype === 'User') {
        const hasMe = uniqueData.some(item => item.value === '@me')
        if (!hasMe) {
          uniqueData.unshift({
            label: '@me',
            value: '@me',
            description: 'Current User',
            raw: { name: '@me' }
          })
        }
      }

      options.value = uniqueData
    } catch (error) {
      console.error('Error fetching link options:', error)
      options.value = []
    } finally {
      loading.value = false
    }
  }

  // Hàm tạo description mặc định cho từng doctype
  const getDefaultDescription = (doctype, item) => {
    switch (doctype) {
      case 'User':
        return item.full_name || item.email || item.name
      case 'Customer':
        return item.customer_name || item.name
      case 'Supplier':
        return item.supplier_name || item.name
      case 'Company':
        return item.company_name || item.name
      case 'Item':
        return item.item_name || item.name
      case 'Project':
        return item.project_name || item.name
      case 'Campaign':
        return item.campaign_name || item.description || item.name
      default:
        return item.title || item.description || item.name
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