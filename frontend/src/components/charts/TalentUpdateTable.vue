<template>
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
		<div class="flex items-center justify-between mb-4">
			<div>
				<h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
				<p class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
			</div>
			<div class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-semibold">
				{{ data.length }} {{ __('talents') }}
			</div>
		</div>
		
		<div class="overflow-x-auto" :style="{ maxHeight: tableHeight }">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50 sticky top-0">
					<tr>
						<th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							{{ __('Name') }}
						</th>
						<th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							{{ __('Last Interaction') }}
						</th>
						<th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							{{ __('Days Since') }}
						</th>
						<th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							{{ __('Status') }}
						</th>
						<th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							{{ __('Source') }}
						</th>
						<th scope="col" class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
							{{ __('Action') }}
						</th>
					</tr>
				</thead>
				<tbody class="bg-white divide-y divide-gray-200">
					<tr v-for="(talent, index) in data" :key="index" class="hover:bg-gray-50 transition-colors">
						<td class="px-4 py-3 whitespace-nowrap">
							<div class="flex items-center">
								<div class="flex-shrink-0 h-8 w-8 bg-blue-500 rounded-full flex items-center justify-center">
									<span class="text-white text-sm font-medium">{{ getInitials(talent.name) }}</span>
								</div>
								<div class="ml-3">
									<div class="text-sm font-medium text-gray-900">{{ talent.name }}</div>
									<div class="text-xs text-gray-500">{{ talent.title }}</div>
								</div>
							</div>
						</td>
						<td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
							{{ talent.lastInteraction }}
						</td>
						<td class="px-4 py-3 whitespace-nowrap">
							<span :class="getDaysSinceClass(talent.daysSince)" class="px-2 py-1 text-xs font-semibold rounded-full">
								{{ talent.daysSince }} {{ __('days') }}
							</span>
						</td>
						<td class="px-4 py-3 whitespace-nowrap">
							<span :class="getStatusClass(talent.status)" class="px-2 py-1 text-xs font-semibold rounded-full">
								{{ talent.status }}
							</span>
						</td>
						<td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">
							{{ talent.source }}
						</td>
						<td class="px-4 py-3 whitespace-nowrap text-sm">
							<button 
								class="text-blue-600 hover:text-blue-800 font-medium"
								@click="$emit('contact-talent', talent)"
							>
								{{ __('Contact') }}
							</button>
						</td>
					</tr>
				</tbody>
			</table>
			
			<div v-if="data.length === 0" class="text-center py-8 text-gray-500">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
				<p class="text-sm">{{ __('All talents are up to date!') }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	title: {
		type: String,
		default: 'Talent Requiring Update'
	},
	subtitle: {
		type: String,
		default: 'Talents needing re-engagement (6+ months inactive)'
	},
	data: {
		type: Array,
		default: () => []
	},
	tableHeight: {
		type: String,
		default: '450px'
	}
})

defineEmits(['contact-talent'])

const getInitials = (name) => {
	if (!name) return '?'
	const parts = name.split(' ')
	if (parts.length >= 2) {
		return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
	}
	return name.substring(0, 2).toUpperCase()
}

const getDaysSinceClass = (days) => {
	if (days >= 365) return 'bg-red-100 text-red-800'
	if (days >= 270) return 'bg-orange-100 text-orange-800'
	return 'bg-yellow-100 text-yellow-800'
}

const getStatusClass = (status) => {
	const statusClasses = {
		'Passive': 'bg-blue-100 text-blue-800',
		'Interested': 'bg-green-100 text-green-800',
		'Considering': 'bg-purple-100 text-purple-800',
		'Inactive': 'bg-gray-100 text-gray-800'
	}
	return statusClasses[status] || 'bg-gray-100 text-gray-800'
}
</script>
