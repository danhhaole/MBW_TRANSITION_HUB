<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header></template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="flex items-center justify-between mb-6">
        <div class="relative">
          <input v-model="searchText" type="text" :placeholder="__('Search by name...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearchInput" />
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <Select v-model="statusFilter" :options="statusOptions" @change="reload" class="min-w-40 text-sm" size="md" variant="outlined" placeholder="All Statuses" />
          <Select v-model="sourceFilter" :options="sourceOptions" @change="reload" class="min-w-40 text-sm" size="md" variant="outlined" placeholder="All Sources" />
          <Button variant="outline" theme="gray" @click="reload" :loading="loading" class="flex items-center py-4">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" :class="{ 'animate-spin': loading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </template>
            {{ __('Refresh') }}
          </Button>
        </div>
      </div>

      <div class="bg-white rounded-lg border border-gray-200">
        <Loading v-if="loading" text="Loading candidates..." />
        <div v-if="!loading" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Full Name') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Email') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Phone') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Source') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Status') }}</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Email Opt Out') }}</th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in items" :key="item.name" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <button class="text-left text-gray-900 hover:underline" @click="view(item)">{{ item.full_name }}</button>
                </td>
                <td class="px-6 py-4">{{ item.email || __('None') }}</td>
                <td class="px-6 py-4">{{ item.phone || __('None') }}</td>
                <td class="px-6 py-4">{{ item.source || __('None') }}</td>
                <td class="px-6 py-4">
                  <span :class="badgeClass(item.status)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ item.status || __('None') }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span :class="emailOptOutClass(item.email_opt_out)" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
                    {{ item.email_opt_out ? __('Opted Out') : __('Active') }}
                  </span>
                </td>
              </tr>
              <tr v-if="items.length === 0">
                <td colspan="6" class="px-6 py-8 text-center text-gray-500">{{ __('No records') }}</td>
              </tr>
            </tbody>
          </table>

          <div v-if="pagination.pages > 1" class="flex items-center justify-between px-6 py-4 border-t border-gray-200">
            <div class="text-sm text-gray-500">
              {{ __('Display') }} {{ Math.min(((pagination.page - 1) * pagination.limit) + 1, pagination.total) }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }} {{ __('of') }} {{ pagination.total }} {{ __('records') }}
            </div>
            <div class="flex items-center space-x-2">
              <button class="px-3 py-1 rounded border text-sm" :class="pagination.page === 1 ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'" :disabled="pagination.page === 1" @click="goToPage(pagination.page - 1)">
                {{ __('Prev') }}
              </button>
              <button v-for="p in pagination.pages" :key="p" class="px-3 py-1 rounded border text-sm" :class="p === pagination.page ? 'bg-black text-white border-black' : 'text-gray-700 border-gray-300 hover:bg-gray-50'" @click="goToPage(p)">{{ p }}</button>
              <button class="px-3 py-1 rounded border text-sm" :class="pagination.page === pagination.pages ? 'text-gray-400 border-gray-200 cursor-not-allowed' : 'text-gray-700 border-gray-300 hover:bg-gray-50'" :disabled="pagination.page === pagination.pages" @click="goToPage(pagination.page + 1)">
                {{ __('Next') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import LayoutHeader from '@/components/LayoutHeader.vue'
import Loading from '@/components/Loading.vue'
import { Breadcrumbs, Button, Select } from 'frappe-ui'
import { call } from 'frappe-ui'

const router = useRouter()
const breadcrumbs = [{ label: __('Candidates'), route: { name: 'CandidateManagementSimple' } }]

const loading = ref(false)
const items = ref([])
const pagination = ref({ page: 1, limit: 10, total: 0, pages: 0, has_next: false, has_prev: false })
const searchText = ref('')
const statusFilter = ref('all')
const sourceFilter = ref('all')

const statusOptions = [
  { label: __('All Statuses'), value: 'all' },
  { label: 'NEW', value: 'NEW' },
  { label: 'SOURCED', value: 'SOURCED' },
  { label: 'NURTURING', value: 'NURTURING' },
  { label: 'ENGAGED', value: 'ENGAGED' },
  { label: 'ARCHIVED', value: 'ARCHIVED' }
]

const sourceOptions = [
  { label: __('All Sources'), value: 'all' },
  { label: __('Manual'), value: 'Manual' },
  { label: __('LinkedIn'), value: 'LinkedIn' },
  { label: __('Email'), value: 'Email' },
  { label: __('Referral'), value: 'Referral' },
  { label: __('ATS Import'), value: 'ATS Import' },
  { label: __('Website'), value: 'Website' }
]

const fetchList = async () => {
  const filterArray = []
  if (statusFilter.value !== 'all') filterArray.push(['status', '=', statusFilter.value])
  if (sourceFilter.value !== 'all') filterArray.push(['source', '=', sourceFilter.value])
  if (searchText.value && searchText.value.trim()) filterArray.push(['full_name', 'like', `%${searchText.value.trim()}%`])

  const res = await call('frappe.client.get_list', {
    doctype: 'Candidate',
    filters: filterArray.length ? filterArray : {},
    fields: ['name','full_name','email','phone','source','status','email_opt_out','creation'],
    order_by: 'modified desc',
    limit_start: (pagination.value.page - 1) * pagination.value.limit,
    limit_page_length: pagination.value.limit
  })
  const total = await call('frappe.client.get_count', {
    doctype: 'Candidate',
    filters: filterArray.length ? filterArray : {}
  })
  items.value = res || []
  pagination.value.total = total || 0
  pagination.value.pages = Math.ceil((total || 0) / pagination.value.limit)
}

const reload = async () => {
  loading.value = true
  try { await fetchList() } finally { loading.value = false }
}

let searchTimer = null
const handleSearchInput = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    pagination.value.page = 1
    reload()
  }, 300)
}

watch(searchText, () => handleSearchInput())

const view = (item) => router.push(`/candidates-simple/${item.name}`)

const badgeClass = (status) => ({
  'NEW': 'bg-gray-100 text-gray-800',
  'SOURCED': 'bg-blue-100 text-blue-800',
  'NURTURING': 'bg-yellow-100 text-yellow-800',
  'ENGAGED': 'bg-green-100 text-green-800',
  'ARCHIVED': 'bg-red-100 text-red-800'
}[status] || 'bg-gray-100 text-gray-800')

const emailOptOutClass = (emailOptOut) => {
  return emailOptOut 
    ? 'bg-red-100 text-red-800' 
    : 'bg-green-100 text-green-800'
}

const formatDate = (date) => date ? new Date(date).toLocaleDateString('vi-VN', { year: 'numeric', month: '2-digit', day: '2-digit' }) : ''

const goToPage = async (page) => {
  if (!pagination.value.pages) return
  if (page < 1 || page > pagination.value.pages) return
  if (page === pagination.value.page) return
  pagination.value.page = page
  await reload()
}

onMounted(async () => {
  await reload()
})
</script> 