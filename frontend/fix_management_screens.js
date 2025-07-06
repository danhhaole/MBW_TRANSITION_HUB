// Script to fix management screens with common patterns
const fs = require('fs')
const path = require('path')

// Helper function to fix loadData method
const fixLoadDataMethod = (content, searchFields = ['name']) => {
  const loadDataRegex = /const loadData = async \(\) => \{[\s\S]*?\}\s*(?=\n\n|\nconst)/g
  
  const searchConditionsCode = searchFields.map(field => 
    `searchConditions.push(['${field}', 'like', \`%\${search.value}%\`])`
  ).join('\n      ')
  
  const newLoadData = `const loadData = async () => {
  loading.value = true
  try {
    // Prepare filters
    const apiFilters = {}
    
    // Add non-empty filters
    Object.keys(filters).forEach(key => {
      if (filters[key] && filters[key] !== '') {
        apiFilters[key] = filters[key]
      }
    })
    
    // Prepare search conditions
    const searchConditions = []
    if (search.value && search.value.trim() !== '') {
      ${searchConditionsCode}
    }
    
    const params = {
      filters: apiFilters,
      page_length: pagination.limit,
      start: (pagination.page - 1) * pagination.limit,
      order_by: 'modified desc',
      fields: ['name', 'modified', 'creation'] // Add specific fields as needed
    }
    
    // Add search conditions if any
    if (searchConditions.length > 0) {
      params.filters.search_text = searchConditions
    }

    const result = await service.getList(params) // Replace 'service' with actual service name
    
    if (result.success) {
      items.value = result.data || []
      Object.assign(pagination, result.pagination)
      
      // Update stats if needed
      stats.total = result.pagination.total || 0
    } else {
      console.error('Error loading data:', result.error)
      items.value = []
    }
  } catch (error) {
    console.error('Error loading data:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}`

  return content.replace(loadDataRegex, newLoadData)
}

// Helper function to fix applyFilters method
const fixApplyFilters = (content) => {
  const applyFiltersRegex = /const applyFilters = \(\) => \{[\s\S]*?\}/g
  
  const newApplyFilters = `const applyFilters = debounce(() => {
  pagination.page = 1
  loadData()
}, 300)`

  return content.replace(applyFiltersRegex, newApplyFilters)
}

// Helper function to fix clearFilters method
const fixClearFilters = (content) => {
  const clearFiltersRegex = /const clearFilters = \(\) => \{[\s\S]*?\}/g
  
  const newClearFilters = `const clearFilters = () => {
  Object.keys(filters).forEach(key => {
    filters[key] = ''
  })
  search.value = ''
  pagination.page = 1
  loadData()
}`

  return content.replace(clearFiltersRegex, newClearFilters)
}

// Helper function to fix loadFilterOptions method
const fixLoadFilterOptions = (content) => {
  const loadFilterOptionsRegex = /const loadFilterOptions = async \(\) => \{[\s\S]*?\}\s*(?=\n\n|\nconst)/g
  
  // This is a generic template - needs to be customized for each screen
  const newLoadFilterOptions = `const loadFilterOptions = async () => {
  try {
    // Load filter options with proper filters parameter
    // Example:
    // const result = await someService.getList({ 
    //   fields: ['name', 'title'],
    //   page_length: 1000,
    //   filters: {}
    // })
    // if (result.success) {
    //   filterOptions.items = result.data.map(item => ({
    //     title: item.title || item.name,
    //     value: item.name
    //   }))
    // }
  } catch (error) {
    console.error('Error loading filter options:', error)
  }
}`

  return content.replace(loadFilterOptionsRegex, newLoadFilterOptions)
}

// List of files to fix
const filesToFix = [
  'ActionManagement.vue',
  'InteractionManagement.vue'
]

// Process each file
filesToFix.forEach(filename => {
  const filePath = path.join(__dirname, 'src', 'pages', filename)
  
  if (fs.existsSync(filePath)) {
    console.log(`Processing ${filename}...`)
    
    let content = fs.readFileSync(filePath, 'utf8')
    
    // Apply fixes
    content = fixLoadDataMethod(content)
    content = fixApplyFilters(content)
    content = fixClearFilters(content)
    // content = fixLoadFilterOptions(content) // Uncomment if needed
    
    // Write back
    fs.writeFileSync(filePath, content)
    console.log(`Fixed ${filename}`)
  } else {
    console.log(`File ${filename} not found`)
  }
})

console.log('All files processed')
