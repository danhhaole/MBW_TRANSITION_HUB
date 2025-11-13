<template>
	<div :class="[
		'stat-card group',
		cardClass
	]">
		<div class="flex items-start justify-between mb-3">
			<!-- Icon -->
			<div 
				v-if="icon || $slots.icon"
				:class="[
					'p-2 rounded-lg transition-colors',
					iconBgClass,
					`group-hover:${iconBgHoverClass}`
				]"
			>
				<slot name="icon">
					<component 
						v-if="icon" 
						:is="icon" 
						:class="['w-5 h-5', iconColorClass]"
					/>
					<svg v-else class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
					</svg>
				</slot>
			</div>

			<!-- Badge (optional) -->
			<div v-if="badge || $slots.badge" :class="badgeClass">
				<slot name="badge">
					{{ badge }}
				</slot>
			</div>
		</div>

		<!-- Value -->
		<div class="mb-1">
			<slot name="value">
				<p :class="['font-bold', valueClass]">
					{{ formattedValue }}
				</p>
			</slot>
		</div>

		<!-- Label -->
		<div>
			<slot name="label">
				<p :class="['text-xs', labelClass]">
					{{ label }}
				</p>
			</slot>
		</div>

		<!-- Trend/Meta info (optional) -->
		<div v-if="trend || meta || $slots.meta" class="mt-2">
			<slot name="meta">
				<p v-if="trend" :class="['text-xs font-medium', getTrendClass()]">
					<svg v-if="trendDirection === 'up'" class="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
					</svg>
					<svg v-else-if="trendDirection === 'down'" class="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
					</svg>
					{{ trend }}
				</p>
				<p v-if="meta" class="text-xs text-gray-500">
					{{ meta }}
				</p>
			</slot>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
	// Content
	label: {
		type: String,
		default: ''
	},
	value: {
		type: [String, Number],
		default: ''
	},
	valueFormat: {
		type: String,
		default: 'text', // text, number, currency, percentage
		validator: (value) => ['text', 'number', 'currency', 'percentage'].includes(value)
	},
	
	// Icon
	icon: {
		type: [Object, String],
		default: null
	},
	iconBgClass: {
		type: String,
		default: 'bg-blue-50'
	},
	iconBgHoverClass: {
		type: String,
		default: 'bg-blue-100'
	},
	iconColorClass: {
		type: String,
		default: 'text-blue-600'
	},
	
	// Trend
	trend: {
		type: String,
		default: ''
	},
	trendDirection: {
		type: String,
		default: 'neutral', // up, down, neutral
		validator: (value) => ['up', 'down', 'neutral'].includes(value)
	},
	trendType: {
		type: String,
		default: 'positive', // positive, negative, neutral
		validator: (value) => ['positive', 'negative', 'neutral'].includes(value)
	},
	
	// Additional info
	meta: {
		type: String,
		default: ''
	},
	badge: {
		type: String,
		default: ''
	},
	badgeClass: {
		type: String,
		default: 'px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full'
	},
	
	// Styling
	cardClass: {
		type: String,
		default: ''
	},
	valueClass: {
		type: String,
		default: 'text-2xl text-gray-900'
	},
	labelClass: {
		type: String,
		default: 'text-gray-600'
	}
})

// Computed
const formattedValue = computed(() => {
	if (props.value === null || props.value === undefined) return '-'
	
	switch (props.valueFormat) {
		case 'number':
			return typeof props.value === 'number' 
				? props.value.toLocaleString() 
				: props.value
		case 'currency':
			return `$${parseFloat(props.value).toFixed(2)}`
		case 'percentage':
			return `${parseFloat(props.value).toFixed(1)}%`
		default:
			return props.value
	}
})

const getTrendClass = () => {
	if (props.trendType === 'positive') {
		return props.trendDirection === 'up' ? 'text-green-600' : 'text-red-600'
	} else if (props.trendType === 'negative') {
		return props.trendDirection === 'up' ? 'text-red-600' : 'text-green-600'
	}
	return 'text-gray-600'
}
</script>

<style scoped>
.stat-card {
	background: white;
	border-radius: 0.75rem;
	padding: 1rem;
	border: 1px solid #e2e8f0;
	transition: all 0.2s ease;
}

.stat-card:hover {
	box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
	border-color: #cbd5e1;
	transform: translateY(-1px);
}
</style>