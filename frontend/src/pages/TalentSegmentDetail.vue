<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <!-- Back Button -->
      <div class="mb-6">
        <Button
          variant="ghost"
          theme="gray"
          @click="$router.back()"
          class="text-sm"
        >
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </template>
          {{ __('Back to Talent Pools') }}
        </Button>
      </div>

      <!-- Header -->
      <div class="flex justify-between items-start mb-8">
        <div class="flex items-center">
          <div class="h-12 w-12 rounded-full bg-blue-500 flex items-center justify-center mr-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gray-900 mb-1">{{ segmentTitle }}</h1>
            <div class="text-sm text-gray-500">
              {{ candidateCount }} candidates • Created on {{ formatCreationDate(creationDate) }}
            </div>
          </div>
        </div>
        
        <div class="flex items-center space-x-3">
          <Button
            variant="outline"
            theme="gray"
            @click="exportData"
          >
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </template>
            {{ __('Export') }}
          </Button>
          <Dropdown :options="getMoreMenuOptions()" placement="bottom-end">
            <Button variant="outline" theme="gray">
              {{ __('More') }}
              <template #suffix>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </template>
            </Button>
          </Dropdown>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
          <div class="text-sm opacity-90 mb-1">{{ __('Total Talent') }}</div>
          <div class="text-3xl font-bold mb-2">{{ candidateCount }}</div>
          <div class="text-sm flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            +{{ newCandidatesThisMonth }} {{ __('this month') }}
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
          <div class="text-sm opacity-90 mb-1">{{ __('Engagement Rate') }}</div>
          <div class="text-3xl font-bold mb-2">{{ engagementRate }}%</div>
          <div class="text-sm flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            +{{ engagementChange }}% {{ __('from last month') }}
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
          <div class="text-sm opacity-90 mb-1">{{ __('Active Campaigns') }}</div>
          <div class="text-3xl font-bold mb-2">{{ activeCampaigns }}</div>
          <div class="text-sm flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ pendingApprovals }} {{ __('pending approval') }}
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
          <div class="text-sm opacity-90 mb-1">{{ __('Avg. Response Time') }}</div>
          <div class="text-3xl font-bold mb-2">{{ avgResponseTime }} days</div>
          <div class="text-sm flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
            </svg>
            {{ responseTimeChange }} {{ __('days from last month') }}
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-3 mb-8">
        <Button
          variant="solid"
          theme="purple"
          @click="createCampaign"
        >
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </template>
          {{ __('Create Campaign') }}
        </Button>
        
        <Button
          variant="solid"
          theme="blue"
          @click="addCandidates"
        >
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </template>
          {{ __('Add Talents') }}
        </Button>
        
        <Button
          variant="solid"
          theme="green"
          @click="scheduleNurturing"
        >
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </template>
          {{ __('Schedule Nurturing') }}
        </Button>
        
        <Button
          variant="solid"
          theme="purple"
          @click="viewAnalytics"
        >
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </template>
          {{ __('Analytics') }}
        </Button>
      </div>

      <!-- Candidates Table -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200">
        <div class="flex justify-between items-center p-6 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">{{ __('Talent in this Pool') }}</h2>
          <div class="flex items-center space-x-3">
            <div class="relative">
              <input
                v-model="candidateSearch"
                type="text"
                placeholder="{{ __('Search talents...') }}"
                class="block w-80 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              />
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </div>
            </div>
            <Button
              variant="outline"
              theme="gray"
              @click="showFilters = !showFilters"
            >
              <template #prefix>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                </svg>
              </template>
              {{ __('Filter') }} 
            </Button>
          </div>
        </div>

        <!-- Filters (Collapsible) -->
        <div v-show="showFilters" class="p-6 border-b border-gray-200 bg-gray-50">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Status') }}</label>
              <select
                v-model="statusFilter"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option v-for="option in statusOptions" :key="option.value" :value="option.value">
                  {{ option.title }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Skills') }}</label>
              <select
                v-model="skillFilter"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option v-for="option in skillOptions" :key="option.value" :value="option.value">
                  {{ option.title }}
                </option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Engagement') }}</label>
              <select
                v-model="engagementFilter"
                class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              >
                <option v-for="option in engagementOptions" :key="option.value" :value="option.value">
                  {{ option.title }}
                </option>
              </select>
            </div>
            <div class="flex items-end">
              <Button
                variant="ghost"
                theme="gray"
                @click="clearFilters"
                class="w-full"
              >
                {{ __('Clear Filters') }}
              </Button>
            </div>
          </div>
        </div>

        <!-- Data Table -->
        <div class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-300">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Candidate') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Skills') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Last Contact') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Engagement') }}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Status') }}
                </th>
                <th scope="col" class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {{ __('Actions') }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-if="loadingCandidates">
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                  <div class="flex justify-center">
                    <svg class="animate-spin h-5 w-5 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span class="ml-2">{{ __('Loading talents...') }}</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="paginatedCandidates.length === 0">
                <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                  {{ __('No talent found') }}
                </td>
              </tr>
              <tr v-else v-for="candidate in paginatedCandidates" :key="candidate.id" class="hover:bg-gray-50">
                <!-- Candidate column -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div :class="getAvatarColorClass(candidate.name)" class="h-10 w-10 rounded-full flex items-center justify-center mr-3">
                      <span class="text-sm font-medium text-white">
                        {{ getAvatarText(candidate.name) }}
                      </span>
                    </div>
                    <div>
                      <div class="text-sm font-medium text-gray-900">{{ candidate.name }}</div>
                      <div class="text-sm text-gray-500">{{ candidate.email }}</div>
                    </div>
                  </div>
                </td>

                <!-- Skills column -->
                <td class="px-6 py-4">
                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="skill in candidate.skills"
                      :key="skill"
                      :class="getSkillColorClass(skill)"
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    >
                      {{ skill }}
                    </span>
                  </div>
                </td>

                <!-- Last Contact column -->
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatRelativeTime(candidate.last_contact) }}
                </td>

                <!-- Engagement column -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center" style="min-width: 120px;">
                    <div class="w-full bg-gray-200 rounded-full h-2 mr-2">
                      <div 
                        :class="getEngagementColorClass(candidate.engagement)"
                        class="h-2 rounded-full transition-all duration-300"
                        :style="{ width: `${candidate.engagement}%` }"
                      ></div>
                    </div>
                    <span class="text-sm font-medium text-gray-700">{{ candidate.engagement }}%</span>
                  </div>
                </td>

                <!-- Status column -->
                <td class="px-6 py-4 whitespace-nowrap">
                  <span 
                    :class="getStatusColorClass(candidate.status)"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  >
                    {{ candidate.status }}
                  </span>
                </td>

                <!-- Actions column -->
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
                  <div class="flex items-center justify-center space-x-2">
                    <Button
                      variant="ghost"
                      theme="blue"
                      size="sm"
                      @click="viewCandidate(candidate)"
                    >
                      {{ __('View') }} 
                    </Button>
                    <Dropdown :options="getCandidateMenuOptions(candidate)" placement="bottom-end">
                      <Button variant="ghost" theme="gray" size="sm">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                        </svg>
                      </Button>
                    </Dropdown>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex justify-between items-center px-6 py-4 border-t border-gray-200">
          <div class="text-sm text-gray-500">
            {{ __('Showing') }} {{ paginationStart }} {{ __('to') }} {{ paginationEnd }} {{ __('of') }} {{ filteredCandidates.length }} {{ __('candidates') }}
          </div>
          <div class="flex items-center space-x-2">
            <Button
              variant="outline"
              theme="gray"
              size="sm"
              @click="previousPage"
              :disabled="currentPage <= 1"
            >
              {{ __('Previous') }}
            </Button>
            <div class="flex space-x-1">
              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'px-3 py-1 text-sm rounded-md',
                  page === currentPage
                    ? 'bg-blue-500 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                ]"
              >
                {{ page }}
              </button>
            </div>
            <Button
              variant="outline"
              theme="gray"
              size="sm"
              @click="nextPage"
              :disabled="currentPage >= totalPages"
            >
              {{ __('Next') }}
            </Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Dropdown, Breadcrumbs, FeatherIcon } from 'frappe-ui'
import LayoutHeader from '@/components/LayoutHeader.vue'
import { getTalentSegmentDetails, getSegmentCandidates } from '@/services/talentSegmentService'

// Route params
const route = useRoute()
const router = useRouter()
const segmentId = route.params.id

// Breadcrumbs
const breadcrumbs = [
  { label: 'Talent Pools', route: { name: 'TalentSegments' } },
  { label: 'Detail', route: { name: 'TalentSegmentDetail' } }
]

// State
const loading = ref(true)
const loadingCandidates = ref(false)
const candidateSearch = ref('')
const showFilters = ref(false)
const statusFilter = ref('all')
const skillFilter = ref('all')
const engagementFilter = ref('all')

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Segment data (from backend)
const segmentData = ref({})
const segmentTitle = computed(() => segmentData.value.title || 'Loading...')
const candidateCount = computed(() => segmentData.value.candidate_count || 0)
const creationDate = computed(() => segmentData.value.creation || '')
const segmentType = computed(() => segmentData.value.type || 'MANUAL')
const segmentDescription = computed(() => segmentData.value.description || '')
const ownerId = computed(() => segmentData.value.owner_id || '')

// Mock stats data (these would come from analytics APIs)
const newCandidatesThisMonth = ref(12)
const engagementRate = ref(78)
const engagementChange = ref(5)
const activeCampaigns = ref(3)
const pendingApprovals = ref(1)
const avgResponseTime = ref(2.4)
const responseTimeChange = ref(-0.5)

// Candidates data (from backend)
const candidates = ref([])

// Table headers
const candidateHeaders = [
  { title: 'CANDIDATE', key: 'candidate', sortable: true, width: '25%' },
  { title: 'SKILLS', key: 'skills', sortable: false, width: '20%' },
  { title: 'LAST CONTACT', key: 'last_contact', sortable: true, width: '15%' },
  { title: 'ENGAGEMENT', key: 'engagement', sortable: true, width: '15%' },
  { title: 'STATUS', key: 'status', sortable: true, width: '12%' },
  { title: 'ACTIONS', key: 'actions', sortable: false, width: '13%', align: 'center' }
]

// Filter options
const statusOptions = [
  { title: 'All Statuses', value: 'all' },
  { title: 'Active', value: 'Active' },
  { title: 'Nurturing', value: 'Nurturing' },
  { title: 'Inactive', value: 'Inactive' }
]

const skillOptions = [
  { title: 'All Skills', value: 'all' },
  { title: 'React', value: 'React' },
  { title: 'Node.js', value: 'Node.js' },
  { title: 'TypeScript', value: 'TypeScript' },
  { title: 'Vue.js', value: 'Vue.js' }
]

const engagementOptions = [
  { title: 'All Levels', value: 'all' },
  { title: 'High (80%+)', value: 'high' },
  { title: 'Medium (50-79%)', value: 'medium' },
  { title: 'Low (<50%)', value: 'low' }
]

// Computed
const filteredCandidates = computed(() => {
  let filtered = candidates.value

  // Apply search filter
  if (candidateSearch.value) {
    const search = candidateSearch.value.toLowerCase()
    filtered = filtered.filter(c => 
      c.name.toLowerCase().includes(search) ||
      c.email.toLowerCase().includes(search)
    )
  }

  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(c => c.status === statusFilter.value)
  }

  if (skillFilter.value !== 'all') {
    filtered = filtered.filter(c => c.skills.includes(skillFilter.value))
  }

  if (engagementFilter.value !== 'all') {
    if (engagementFilter.value === 'high') {
      filtered = filtered.filter(c => c.engagement >= 80)
    } else if (engagementFilter.value === 'medium') {
      filtered = filtered.filter(c => c.engagement >= 50 && c.engagement < 80)
    } else if (engagementFilter.value === 'low') {
      filtered = filtered.filter(c => c.engagement < 50)
    }
  }

  return filtered
})

// Pagination computed
const totalPages = computed(() => Math.ceil(filteredCandidates.value.length / itemsPerPage.value))
const paginatedCandidates = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredCandidates.value.slice(start, end)
})

const paginationStart = computed(() => {
  return filteredCandidates.value.length === 0 ? 0 : (currentPage.value - 1) * itemsPerPage.value + 1
})

const paginationEnd = computed(() => {
  const end = currentPage.value * itemsPerPage.value
  return Math.min(end, filteredCandidates.value.length)
})

const visiblePages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const delta = 2

  const range = []
  for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
    range.push(i)
  }
  return range
})

// Helper functions
const formatCreationDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatRelativeTime = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInDays = Math.floor((now - date) / (1000 * 60 * 60 * 24))
  
  if (diffInDays === 0) return 'today'
  if (diffInDays === 1) return '1 day ago'
  if (diffInDays < 7) return `${diffInDays} days ago`
  if (diffInDays < 14) return '1 week ago'
  return `${Math.floor(diffInDays / 7)} weeks ago`
}

const getAvatarColorClass = (name) => {
  const colors = [
    'bg-blue-500',
    'bg-green-500', 
    'bg-purple-500',
    'bg-pink-500',
    'bg-indigo-500',
    'bg-yellow-500',
    'bg-red-500'
  ]
  const hash = name.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0)
    return a & a
  }, 0)
  return colors[Math.abs(hash) % colors.length]
}

const getAvatarText = (name) => {
  return name.split(' ').map(word => word[0]).join('').toUpperCase().substring(0, 2)
}

const getSkillColorClass = (skill) => {
  const skillColors = {
    'React': 'bg-blue-100 text-blue-800',
    'Node.js': 'bg-green-100 text-green-800',
    'TypeScript': 'bg-blue-100 text-blue-800',
    'Vue.js': 'bg-green-100 text-green-800',
    'AWS': 'bg-orange-100 text-orange-800',
    'GraphQL': 'bg-pink-100 text-pink-800',
    'React Native': 'bg-purple-100 text-purple-800'
  }
  return skillColors[skill] || 'bg-gray-100 text-gray-800'
}

const getEngagementColorClass = (engagement) => {
  if (engagement >= 80) return 'bg-green-500'
  if (engagement >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getStatusColorClass = (status) => {
  const statusColors = {
    'Active': 'bg-green-100 text-green-800',
    'Nurturing': 'bg-yellow-100 text-yellow-800',
    'Inactive': 'bg-gray-100 text-gray-800'
  }
  return statusColors[status] || 'bg-gray-100 text-gray-800'
}

const getMoreMenuOptions = () => [
  {
    label: 'Edit Pool',
    icon: 'edit',
    onClick: editSegment
  },
  {
    label: 'Duplicate',
    icon: 'copy',
    onClick: duplicateSegment
  },
  {
    label: 'Delete Pool',
    icon: 'trash-2',
    onClick: deleteSegment,
    class: 'text-red-600'
  }
]

const getCandidateMenuOptions = (candidate) => [
  {
    label: 'Contact',
    icon: 'mail',
    onClick: () => contactCandidate(candidate)
  },
  {
    label: 'Add to Campaign',
    icon: 'plus-circle',
    onClick: () => addToCampaign(candidate)
  },
  {
    label: 'Remove from Pool',
    icon: 'x-circle',
    onClick: () => removeFromPool(candidate),
    class: 'text-red-600'
  }
]

// Pagination methods
const goToPage = (page) => {
  currentPage.value = page
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}
const exportData = () => {
  console.log('Export data')
}

const editSegment = () => {
  console.log('Edit segment')
}

const duplicateSegment = () => {
  console.log('Duplicate segment')
}

const deleteSegment = () => {
  console.log('Delete segment')
}

const createCampaign = () => {
  console.log('Create campaign')
}

const addCandidates = () => {
  console.log('Add candidates')
}

const scheduleNurturing = () => {
  console.log('Schedule nurturing')
}

const viewAnalytics = () => {
  console.log('View analytics')
}

const viewCandidate = (candidate) => {
  // Navigate to candidate detail view
  router.push(`/candidate/${candidate.name}`)
}

const contactCandidate = (candidate) => {
  console.log('Contact candidate:', candidate)
}

const addToCampaign = (candidate) => {
  console.log('Add to campaign:', candidate)
}

const removeFromPool = (candidate) => {
  console.log('Remove from pool:', candidate)
}

const clearFilters = () => {
  statusFilter.value = 'all'
  skillFilter.value = 'all'
  engagementFilter.value = 'all'
}

// Data loading functions
const loadSegmentData = async () => {
  try {
    loading.value = true
    const data = await getTalentSegmentDetails(segmentId)
    segmentData.value = data
  } catch (error) {
    console.error('Failed to load segment data:', error)
    // You might want to show an error message or redirect
  } finally {
    loading.value = false
  }
}

const loadCandidatesData = async () => {
  try {
    loadingCandidates.value = true
    const data = await getSegmentCandidates(segmentId)
    candidates.value = data || []
  } catch (error) {
    console.error('Failed to load candidates:', error)
    candidates.value = []
  } finally {
    loadingCandidates.value = false
  }
}

// Initialize
onMounted(async () => {
  console.log('Loading segment:', segmentId)
  await loadSegmentData()
  await loadCandidatesData()
})
</script>

<style scoped>
/* Custom responsive table styles */
@media (max-width: 768px) {
  .table-responsive {
    overflow-x: auto;
  }
}

/* Loading animation */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Hover effects */
.hover-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

/* Progress bar transition */
.progress-bar {
  transition: width 0.5s ease-in-out;
}

/* Button hover effects */
.btn-hover:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}
</style> 