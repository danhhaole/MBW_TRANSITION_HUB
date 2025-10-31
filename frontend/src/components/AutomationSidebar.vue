<template>
  <div class="w-64 bg-white border-r border-gray-200 flex flex-col">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200">
      <h1 class="text-xl font-bold text-gray-900">Automation</h1>
      <p class="text-sm text-gray-500 mt-1">Marketing automation</p>
    </div>

    <!-- Menu Items -->
    <nav class="flex-1 p-4">
      <router-link
        v-for="item in menuItems"
        :key="item.id"
        :to="item.route"
        custom
        v-slot="{ navigate, isActive }"
      >
        <button
          @click="navigate"
          :class="[
            'w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-all',
            isActive
              ? 'bg-blue-50 text-blue-700'
              : 'text-gray-700 hover:bg-gray-50'
          ]"
        >
          <FeatherIcon
            :name="item.icon"
            :class="[
              'w-5 h-5',
              isActive ? 'text-blue-600' : 'text-gray-500'
            ]"
          />
          <span
            :class="[
              'flex-1 text-left font-medium',
              isActive ? 'text-blue-700' : 'text-gray-700'
            ]"
          >
            {{ item.label }}
          </span>
          <Badge
            :variant="isActive ? 'subtle' : 'outline'"
            :theme="isActive ? 'blue' : 'gray'"
          >
            {{ item.count }}
          </Badge>
        </button>
      </router-link>
    </nav>

    <!-- Footer -->
    <div class="p-4 border-t border-gray-200">
      <Button variant="solid" theme="blue" class="w-full" @click="handleCreate">
        <template #prefix>
          <FeatherIcon name="plus" class="w-4 h-4" />
        </template>
        Create New
      </Button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Button, Badge, FeatherIcon } from 'frappe-ui'
import { useAutomationStatsStore } from '@/stores/automationStats'

// Props
const props = defineProps({
  campaignCount: {
    type: Number,
    default: null
  },
  flowCount: {
    type: Number,
    default: null
  },
  sequenceCount: {
    type: Number,
    default: null
  }
})

// Emits
const emit = defineEmits(['create'])

// Router
const route = useRoute()

// Automation stats store (global cache)
const statsStore = useAutomationStatsStore()

// Use props if provided, otherwise use store values
const finalCampaignCount = computed(() => 
  props.campaignCount !== null ? props.campaignCount : statsStore.campaignCount
)
const finalFlowCount = computed(() => 
  props.flowCount !== null ? props.flowCount : statsStore.flowCount
)
const finalSequenceCount = computed(() => 
  props.sequenceCount !== null ? props.sequenceCount : statsStore.sequenceCount
)

// Menu items configuration
const menuItems = computed(() => [
  { 
    id: 'campaigns', 
    label: 'Campaigns', 
    icon: 'mail', 
    count: finalCampaignCount.value,
    route: '/campaigns'
  },
  { 
    id: 'flows', 
    label: 'Flows', 
    icon: 'git-branch', 
    count: finalFlowCount.value,
    route: '/flows'
  },
  { 
    id: 'sequences', 
    label: 'Sequences', 
    icon: 'list', 
    count: finalSequenceCount.value,
    route: '/sequences'
  }
])

// Get active section from current route
const activeSection = computed(() => {
  const path = route.path
  if (path.includes('/campaigns')) return 'campaigns'
  if (path.includes('/flows')) return 'flows'
  if (path.includes('/sequences')) return 'sequences'
  return null
})

// Handle create button click
const handleCreate = () => {
  emit('create', activeSection.value)
}

// Fetch stats on mount - store sẽ tự động check cache
onMounted(() => {
  statsStore.fetchStats()
})
</script>

<style scoped>
/* Custom styles if needed */
</style>
