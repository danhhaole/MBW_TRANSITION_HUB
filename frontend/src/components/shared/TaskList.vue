<template>
	<div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
		<h3 v-if="title" class="text-lg font-semibold text-gray-900 mb-4 pb-3 border-b border-gray-100">
			{{ title }}
		</h3>
		
		<ul :class="listClass">
			<li 
				v-for="(task, index) in tasks" 
				:key="task[taskKey] || index"
				:class="[
					'flex items-start gap-2.5 py-2',
					clickable ? 'cursor-pointer hover:bg-gray-50 rounded px-2 -mx-2' : ''
				]"
				@click="handleTaskClick(task)"
			>
				<!-- Status indicator -->
				<div 
					:class="[
						'mt-1.5 rounded-full flex-shrink-0',
						task.statusSize || 'w-1.5 h-1.5',
						getStatusColor(task.status)
					]"
				></div>

				<!-- Task content -->
				<div class="flex-1">
					<slot name="task-content" :task="task" :index="index">
						<p class="text-sm text-gray-700 leading-relaxed">
							{{ task.text || task.title || task.description }}
						</p>
						<div v-if="showMeta && (task.assignee || task.dueDate)" class="mt-1 flex items-center gap-3 text-xs text-gray-500">
							<span v-if="task.assignee">
								<svg class="w-3 h-3 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
								</svg>
								{{ task.assignee }}
							</span>
							<span v-if="task.dueDate">
								<svg class="w-3 h-3 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
								</svg>
								{{ formatDate(task.dueDate) }}
							</span>
						</div>
					</slot>
				</div>

				<!-- Actions slot -->
				<div v-if="$slots.actions" class="flex-shrink-0">
					<slot name="actions" :task="task" :index="index"></slot>
				</div>
			</li>
		</ul>

		<!-- Empty state -->
		<div v-if="!tasks || tasks.length === 0" class="text-center py-8">
			<slot name="empty">
				<div class="flex flex-col items-center">
					<svg class="w-12 h-12 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
					</svg>
					<p class="text-gray-500 text-sm">{{ emptyText }}</p>
				</div>
			</slot>
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	title: {
		type: String,
		default: ''
	},
	tasks: {
		type: Array,
		default: () => []
	},
	taskKey: {
		type: String,
		default: 'id'
	},
	statusColorMap: {
		type: Object,
		default: () => ({
			red: 'bg-red-500',
			orange: 'bg-orange-500',
			yellow: 'bg-yellow-500',
			green: 'bg-green-500',
			blue: 'bg-blue-500',
			purple: 'bg-purple-500',
			gray: 'bg-gray-500',
			// Direct color classes
			'bg-red-500': 'bg-red-500',
			'bg-orange-500': 'bg-orange-500',
			'bg-yellow-500': 'bg-yellow-500',
			'bg-green-500': 'bg-green-500',
			'bg-blue-500': 'bg-blue-500',
			'bg-purple-500': 'bg-purple-500',
			'bg-gray-500': 'bg-gray-500'
		})
	},
	listClass: {
		type: String,
		default: 'space-y-2.5'
	},
	clickable: {
		type: Boolean,
		default: false
	},
	showMeta: {
		type: Boolean,
		default: false
	},
	emptyText: {
		type: String,
		default: 'No tasks available'
	}
})

const emit = defineEmits(['task-click'])

// Methods
const getStatusColor = (status) => {
	// If status is already a color class
	if (status && status.startsWith('bg-')) {
		return status
	}
	// Map from status name
	return props.statusColorMap[status] || 'bg-gray-500'
}

const handleTaskClick = (task) => {
	if (props.clickable) {
		emit('task-click', task)
	}
}

const formatDate = (dateString) => {
	if (!dateString) return ''
	try {
		return new Date(dateString).toLocaleDateString()
	} catch {
		return dateString
	}
}
</script>