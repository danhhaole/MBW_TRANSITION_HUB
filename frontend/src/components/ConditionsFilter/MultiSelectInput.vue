<template>
	<div class="w-full space-y-2">
		<!-- Display selected values as chips -->
		<div v-if="selectedItems.length > 0" class="flex flex-wrap gap-2">
			<span
				v-for="(item, index) in selectedItems"
				:key="index"
				class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
				:class="chipColorClass"
			>
				{{ item }}
				<button
					type="button"
					@click="removeItem(index)"
					class="ml-1.5 h-4 w-4 rounded-full inline-flex items-center justify-center hover:bg-opacity-20 focus:outline-none"
				>
					<svg class="h-2 w-2" stroke="currentColor" fill="none" viewBox="0 0 8 8">
						<path stroke-linecap="round" stroke-width="1.5" d="m1 1 6 6m0-6-6 6" />
					</svg>
				</button>
			</span>
		</div>

		<!-- Input field with dropdown -->
		<div class="relative">
			<input
				ref="inputRef"
				v-model="searchQuery"
				type="text"
				:placeholder="placeholder"
				class="block w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
				@focus="showDropdown = true"
				@blur="handleBlur"
				@keydown.enter.prevent="selectFromSearch"
				@keydown.escape="showDropdown = false"
			/>

			<!-- Dropdown menu -->
			<div
				v-if="showDropdown && filteredOptions.length > 0"
				class="absolute z-50 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto"
			>
				<div
					v-for="option in filteredOptions"
					:key="option"
					class="px-3 py-2 hover:bg-gray-100 cursor-pointer text-sm flex items-center gap-2"
					:class="{ 'bg-blue-50': selectedItems.includes(option) }"
					@mousedown.prevent="selectOption(option)"
				>
					<input
						type="checkbox"
						:checked="selectedItems.includes(option)"
						class="rounded h-4 w-4"
						@click.stop
					/>
					<span>{{ option }}</span>
				</div>
			</div>
		</div>

		<!-- Helper text -->
		<p v-if="helperText" class="text-xs text-gray-500">
			{{ helperText }}
		</p>
	</div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
	modelValue: {
		type: String,
		default: '',
	},
	options: {
		type: Array,
		required: true,
	},
	placeholder: {
		type: String,
		default: 'Select values...',
	},
	chipColor: {
		type: String,
		default: 'blue',
	},
	helperText: {
		type: String,
		default: '',
	},
})

const emit = defineEmits(['update:modelValue'])

const inputRef = ref(null)
const searchQuery = ref('')
const showDropdown = ref(false)

// Parse comma-separated string to array
const selectedItems = computed(() => {
	if (!props.modelValue) return []
	return props.modelValue
		.split(',')
		.map((s) => s.trim())
		.filter((s) => s)
})

// Filter options based on search and exclude already selected
const filteredOptions = computed(() => {
	const query = searchQuery.value.toLowerCase()
	return props.options.filter((opt) => {
		return opt.toLowerCase().includes(query)
	})
})

// Chip color classes (match SkillsTagsInput style)
const chipColorClass = computed(() => {
	const colors = {
		blue: 'bg-blue-100 text-blue-800',
		green: 'bg-green-100 text-green-800',
		purple: 'bg-purple-100 text-purple-800',
		orange: 'bg-orange-100 text-orange-800',
		red: 'bg-red-100 text-red-800',
	}
	return colors[props.chipColor] || colors.blue
})

const focusInput = () => {
	inputRef.value?.focus()
}

const selectOption = (option) => {
	if (selectedItems.value.includes(option)) {
		// Remove if already selected
		removeItemByValue(option)
	} else {
		// Add to selection
		const newItems = [...selectedItems.value, option]
		emit('update:modelValue', newItems.join(', '))
	}
	searchQuery.value = ''
}

const selectFromSearch = () => {
	const query = searchQuery.value.trim()
	if (!query) return

	// Find exact match or first filtered option
	const match = filteredOptions.value.find((opt) => opt.toLowerCase() === query.toLowerCase())
	if (match && !selectedItems.value.includes(match)) {
		selectOption(match)
	} else if (filteredOptions.value.length > 0) {
		selectOption(filteredOptions.value[0])
	}
}

const removeItem = (index) => {
	const newItems = selectedItems.value.filter((_, i) => i !== index)
	emit('update:modelValue', newItems.join(', '))
}

const removeItemByValue = (value) => {
	const newItems = selectedItems.value.filter((item) => item !== value)
	emit('update:modelValue', newItems.join(', '))
}

const handleBlur = () => {
	// Delay to allow click on dropdown items
	setTimeout(() => {
		showDropdown.value = false
	}, 200)
}

// Watch for external changes
watch(
	() => props.modelValue,
	() => {
		searchQuery.value = ''
	},
)
</script>
