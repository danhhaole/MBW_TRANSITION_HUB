<template>
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
		<h3 v-if="title" class="text-lg font-semibold text-gray-900 mb-4">{{ title }}</h3>
		
		<div class="overflow-x-auto">
			<table class="w-full text-sm">
				<thead>
					<tr :class="headerClass">
						<th 
							v-for="column in columns" 
							:key="column.key"
							:class="[
								'py-2.5 font-medium text-gray-700',
								column.align === 'right' ? 'text-right' : 
								column.align === 'center' ? 'text-center' : 'text-left'
							]"
						>
							{{ column.label }}
						</th>
					</tr>
				</thead>
				<tbody>
					<tr 
						v-for="(row, index) in data" 
						:key="row[rowKey] || index"
						:class="[rowClass, 'border-b border-gray-100 last:border-0']"
					>
						<td 
							v-for="column in columns" 
							:key="column.key"
							:class="[
								'py-2.5',
								column.align === 'right' ? 'text-right' : 
								column.align === 'center' ? 'text-center' : 'text-left',
								getCellClass(row, column)
							]"
						>
							<!-- Slot for custom cell rendering -->
							<slot 
								:name="`cell-${column.key}`" 
								:row="row" 
								:value="row[column.key]"
								:column="column"
							>
								<!-- Default cell rendering -->
								<span :class="column.class">
									{{ formatCellValue(row[column.key], column) }}
								</span>
							</slot>
						</td>
					</tr>
				</tbody>
			</table>

			<!-- Empty state -->
			<div v-if="!data || data.length === 0" class="text-center py-8">
				<slot name="empty">
					<p class="text-gray-500">{{ emptyText }}</p>
				</slot>
			</div>
		</div>

		<!-- Pagination (optional) -->
		<div v-if="showPagination && totalPages > 1" class="mt-4 flex items-center justify-between">
			<div class="text-sm text-gray-600">
				{{ __('Showing') }} {{ startItem }} - {{ endItem }} {{ __('of') }} {{ totalItems }}
			</div>
			<div class="flex gap-2">
				<button
					:disabled="currentPage === 1"
					@click="$emit('page-change', currentPage - 1)"
					class="px-3 py-1 border rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
				>
					{{ __('Previous') }}
				</button>
				<button
					:disabled="currentPage === totalPages"
					@click="$emit('page-change', currentPage + 1)"
					class="px-3 py-1 border rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
				>
					{{ __('Next') }}
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
	// Table configuration
	title: {
		type: String,
		default: ''
	},
	columns: {
		type: Array,
		required: true,
		// Format: [{ key: 'name', label: 'Name', align: 'left', format: 'text', class: '' }]
	},
	data: {
		type: Array,
		default: () => []
	},
	rowKey: {
		type: String,
		default: 'id'
	},
	
	// Styling
	headerClass: {
		type: String,
		default: 'border-b border-gray-200'
	},
	rowClass: {
		type: String,
		default: ''
	},
	
	// Features
	showPagination: {
		type: Boolean,
		default: false
	},
	currentPage: {
		type: Number,
		default: 1
	},
	pageSize: {
		type: Number,
		default: 10
	},
	totalItems: {
		type: Number,
		default: 0
	},
	
	// Empty state
	emptyText: {
		type: String,
		default: 'No data available'
	}
})

defineEmits(['page-change', 'row-click'])

// Computed
const totalPages = computed(() => {
	return Math.ceil(props.totalItems / props.pageSize)
})

const startItem = computed(() => {
	return (props.currentPage - 1) * props.pageSize + 1
})

const endItem = computed(() => {
	return Math.min(props.currentPage * props.pageSize, props.totalItems)
})

// Methods
const formatCellValue = (value, column) => {
	if (value === null || value === undefined) return '-'
	
	switch (column.format) {
		case 'number':
			return typeof value === 'number' ? value.toLocaleString() : value
		case 'currency':
			return `$${parseFloat(value).toFixed(2)}`
		case 'percentage':
			return `${parseFloat(value).toFixed(1)}%`
		case 'date':
			return new Date(value).toLocaleDateString()
		case 'datetime':
			return new Date(value).toLocaleString()
		default:
			return value
	}
}

const getCellClass = (row, column) => {
	// Dynamic class based on column configuration
	if (typeof column.cellClass === 'function') {
		return column.cellClass(row)
	}
	return column.cellClass || ''
}
</script>

<style scoped>
table {
	border-collapse: collapse;
}
</style>