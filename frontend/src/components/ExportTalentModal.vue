<template>
    <Dialog v-model="internalShow" :options="{ size: '3xl' }">
        <template #body-title>
            <span>{{ __("Export") }}</span>
        </template>
        <template #body-content>
            <div class="space-y-6">
                <!-- Export Type -->
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">
                        {{ __('Export Type') }}
                    </label>
                    <select
                        v-model="exportType"
                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                    >
                        <option value="Excel">Excel</option>
                        <option value="CSV">CSV</option>
                    </select>
                </div>

                <!-- Export All Records Checkbox -->
                <div class="flex items-center">
                    <input
                        id="export-all"
                        v-model="exportAll"
                        type="checkbox"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="export-all" class="ml-2 text-sm text-gray-700">
                        {{ __('Export All {0} Record(s)', [totalRecords]) }}
                    </label>
                </div>

                <!-- Select Fields -->
                <div>
                    <div class="flex items-center justify-between mb-3">
                        <label class="text-sm font-medium text-gray-700">
                            {{ __('Select Fields ({0})', [selectedFields.length]) }}
                        </label>
                        <button
                            @click="toggleSelectAll"
                            class="text-sm text-blue-600 hover:text-blue-700 font-medium"
                        >
                            {{ allSelected ? __('Deselect All') : __('Select All') }}
                        </button>
                    </div>

                    <!-- Search Fields -->
                    <div class="mb-3 relative">
                        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                            <FeatherIcon name="search" class="w-4 h-4 text-gray-400" />
                        </div>
                        <input
                            v-model="searchQuery"
                            type="text"
                            :placeholder="__('Search fields...')"
                            class="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-sm"
                        />
                    </div>

                    <!-- Fields Grid -->
                    <div class="border border-gray-200 rounded-lg max-h-96 overflow-y-auto p-4">
                        <div class="grid grid-cols-2 gap-3">
                            <div
                                v-for="field in filteredFields"
                                :key="field.fieldname"
                                class="flex items-start"
                            >
                                <input
                                    :id="`field-${field.fieldname}`"
                                    v-model="selectedFields"
                                    :value="field.fieldname"
                                    type="checkbox"
                                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded mt-0.5"
                                />
                                <label
                                    :for="`field-${field.fieldname}`"
                                    class="ml-2 text-sm cursor-pointer"
                                    :class="field.reqd ? 'font-medium text-gray-900' : 'text-gray-700'"
                                >
                                    {{ field.label }}
                                    <span v-if="field.reqd" class="text-red-500">*</span>
                                </label>
                            </div>
                        </div>

                        <!-- Empty State -->
                        <div v-if="filteredFields.length === 0" class="text-center py-8">
                            <FeatherIcon name="search" class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                            <p class="text-sm text-gray-500">{{ __('No fields found') }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </template>
        <template #actions>
            <div class="flex justify-end gap-3 pt-4 border-t border-gray-200">
                <Button
                    variant="outline"
                    theme="gray"
                    @click="closeModal"
                >
                    {{ __('Cancel') }}
                </Button>
                <Button
                    variant="solid"
                    theme="gray"
                    @click="handleExport"
                    :loading="isExporting"
                    :disabled="selectedFields.length === 0"
                >
                    {{ __('Download') }}
                </Button>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { Dialog, Button, FeatherIcon, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    },
    filters: {
        type: Object,
        default: () => ({})
    },
    totalRecords: {
        type: Number,
        default: 0
    },
    currentPageSize: {
        type: Number,
        default: 10
    }
})

const emit = defineEmits(['update:modelValue', 'close'])

const { showSuccess, showError } = useToast()

// State
const internalShow = ref(props.modelValue)
const exportType = ref('Excel')
const exportAll = ref(false)
const selectedFields = ref([])
const searchQuery = ref('')
const availableFields = ref([])
const isExporting = ref(false)
const isLoadingFields = ref(false)

// Computed
const filteredFields = computed(() => {
    if (!searchQuery.value) return availableFields.value
    
    const query = searchQuery.value.toLowerCase()
    return availableFields.value.filter(field => 
        field.label.toLowerCase().includes(query) ||
        field.fieldname.toLowerCase().includes(query)
    )
})

const allSelected = computed(() => {
    return availableFields.value.length > 0 && 
           selectedFields.value.length === availableFields.value.length
})

// Watch
watch(() => props.modelValue, (newVal) => {
    internalShow.value = newVal
    if (newVal) {
        loadFields()
    }
})

watch(internalShow, (newVal) => {
    emit('update:modelValue', newVal)
    if (!newVal) {
        emit('close')
    }
})

// Methods
const loadFields = async () => {
    isLoadingFields.value = true
    try {
        const response = await call('frappe.desk.form.load.getdoctype', {
            doctype: 'Mira Talent',
            with_parent: 1
        })

        if (response?.docs?.[0]) {
            const meta = response.docs[0]
            
            // Standard fields
            const stdFields = [
                { fieldname: 'name', label: 'ID', fieldtype: 'Data', reqd: 1 },
                { fieldname: 'owner', label: 'Created By', fieldtype: 'Link', reqd: 0 },
                { fieldname: 'creation', label: 'Created On', fieldtype: 'Datetime', reqd: 0 },
                { fieldname: 'modified', label: 'Last Modified', fieldtype: 'Datetime', reqd: 0 },
                { fieldname: 'modified_by', label: 'Modified By', fieldtype: 'Link', reqd: 0 }
            ]
            
            const stdFieldNames = stdFields.map(f => f.fieldname)
            
            // Filter relevant fields from DocType
            const relevantFieldtypes = [
                'Data', 'Text', 'Small Text', 'Long Text', 
                'Int', 'Float', 'Currency', 'Date', 'Datetime',
                'Check', 'Select', 'Link', 'Attach', 'Attach Image',
                'Phone', 'Email', 'Read Only'
            ]
            
            const docFields = meta.fields
                .filter(f => 
                    f.fieldtype && 
                    relevantFieldtypes.includes(f.fieldtype) &&
                    !['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Table', 'Button'].includes(f.fieldtype) &&
                    !f.hidden &&
                    !stdFieldNames.includes(f.fieldname) &&
                    f.fieldname !== 'amended_from'
                )
                .map(f => ({
                    fieldname: f.fieldname,
                    label: f.label || f.fieldname,
                    fieldtype: f.fieldtype,
                    reqd: f.reqd || 0
                }))
            
            // Combine standard fields and doc fields
            availableFields.value = [...stdFields, ...docFields]

            // Auto-select required fields and common fields
            const autoSelectFields = ['name', 'full_name', 'email', 'phone', 'skills', 'source']
            selectedFields.value = availableFields.value
                .filter(field => field.reqd || autoSelectFields.includes(field.fieldname))
                .map(field => field.fieldname)
        }
    } catch (error) {
        console.error('Error loading fields:', error)
        showError(__('Failed to load fields'))
    } finally {
        isLoadingFields.value = false
    }
}

const toggleSelectAll = () => {
    if (allSelected.value) {
        selectedFields.value = []
    } else {
        selectedFields.value = availableFields.value.map(field => field.fieldname)
    }
}

const handleExport = async () => {
    if (selectedFields.value.length === 0) {
        showError(__('Please select at least one field'))
        return
    }

    isExporting.value = true
    try {
        // Format fields: `tabDoctype`.`fieldname`
        const formattedFields = selectedFields.value.map(f => `\`tabMira Talent\`.\`${f}\``)
        const fields = JSON.stringify(formattedFields)
        
        // Build filters
        const exportFilters = { ...props.filters }
        const filters = JSON.stringify(exportFilters)
        
        // Determine page length
        let pageLength = props.currentPageSize // Export current page records only
        if (exportAll.value) {
            pageLength = 0 // Export all records (0 means no limit)
        }
        
        // Build URL with proper parameters
        const params = new URLSearchParams({
            file_format_type: exportType.value,
            title: 'Mira Talent',
            doctype: 'Mira Talent',
            fields: fields,
            filters: filters,
            order_by: '`tabMira Talent`.`modified` desc',
            page_length: pageLength,
            start: 0,
            view: 'Report',
            with_comment_count: 1
        })
        
        const url = `/api/method/frappe.desk.reportview.export_query?${params.toString()}`
        
        // Trigger download using window.location
        window.location.href = url

        showSuccess(__('Export started. Download will begin shortly.'))
        
        // Close modal after a short delay
        setTimeout(() => {
            closeModal()
        }, 500)
    } catch (error) {
        console.error('Export error:', error)
        showError(__('Failed to export data'))
    } finally {
        isExporting.value = false
    }
}

const closeModal = () => {
    internalShow.value = false
    // Reset state
    exportType.value = 'Excel'
    exportAll.value = false
    searchQuery.value = ''
}

// Lifecycle
onMounted(() => {
    if (props.modelValue) {
        loadFields()
    }
})
</script>

<style scoped>
/* Custom scrollbar for fields list */
.overflow-y-auto::-webkit-scrollbar {
    width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
    background: #555;
}
</style>
