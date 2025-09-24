<template>
    <div class="min-h-screen bg-gray-50">
      <LayoutHeader>
        <template #left-header>
          <Breadcrumbs :items="breadcrumbs" />
        </template>
      </LayoutHeader>
  
      <div class="container mx-auto px-6 py-6">
        <!-- Tabs -->
        <div class="flex items-center gap-2 mb-4">
          <button
            class="px-3 py-1.5 rounded-md text-sm"
            :class="activeTab==='pending' ? 'bg-black text-white' : 'bg-white text-gray-700 border hover:text-gray-900'"
            @click="setTab('pending')"
          >{{ __('All tasks') }}</button>
          <button
            class="px-3 py-1.5 rounded-md text-sm"
            :class="activeTab==='completed' ? 'bg-black text-white' : 'bg-white text-gray-700 border hover:text-gray-900'"
            @click="setTab('completed')"
          >{{ __('Done') }}</button>
        </div>
  
        <div class="bg-white rounded-lg border border-gray-200">
          <Loading v-if="loading" text="Loading actions..." />
  
          <div v-if="!loading" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Tên công việc') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Trạng thái') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Ngày tạo') }}</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ __('Thao tác') }}</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in currentItems" :key="item.name" class="hover:bg-gray-50">
                  <td class="px-6 py-4">
                    <div class="flex items-start gap-3">
                      <div class="mt-2">
                          <svg viewBox="0 0 24 24" width="16" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1 text-blue-500"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>
                      </div>
                      <div>
                        <div class="text-gray-900 font-medium">{{ item.campaign_step_name || item.campaign_step }}</div>
                        <div class="text-xs text-gray-500">{{ item.campaign_name }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span :class="badgeClass(labelStatus(item.status))" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">{{ labelStatus(item.status) }}</span>
                  </td>
                  <td class="px-6 py-4">{{ formatDate(item.creation) }}</td>
                  <td class="px-6 py-4">
                    <div class="flex items-center gap-2">
                      <button
                        class="inline-flex items-center px-3 py-1.5 rounded-md text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                        @click="activeTab === 'completed' ? openView(item) : openEdit(item)"
                      >
                        {{ activeTab === 'completed' ? __('Xem chi tiết') : __('Cập nhật') }}
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="currentItems.length === 0">
                  <td colspan="4" class="px-6 py-8 text-center text-gray-500">{{ __('Không có dữ liệu') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
  
          <div v-if="pagination && pagination.total > pagination.limit" class="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1 flex justify-between sm:hidden">
                <button
                  @click="handlePreviousPage"
                  :disabled="!pagination.has_prev"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ __('Previous') }}
                </button>
                <button
                  @click="handleNextPage"
                  :disabled="!pagination.has_next"
                  class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ __('Next') }}
                </button>
              </div>
              <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
                <div>
                  <p class="text-sm text-gray-700">
                    {{ __('Showing') }}
                    <span class="font-medium">{{ showingFrom }}</span>
                    {{ __('to') }}
                    <span class="font-medium">{{ showingTo }}</span>
                    {{ __('of') }}
                    <span class="font-medium">{{ pagination.total }}</span>
                    {{ __('results') }}
                  </p>
                </div>
                <div>
                  <nav class="relative z-0 inline-flex rounded-md -space-x-px" aria-label="Pagination">
                    <button
                      @click="handlePreviousPage"
                      :disabled="!pagination.has_prev"
                      class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <FeatherIcon name="chevron-left" class="w-5 h-5" />
                    </button>
                    <button
                      v-for="p in visiblePages"
                      :key="p"
                      @click="goToPage(p)"
                      class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                      :class="p === pagination.page ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600' : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'"
                    >
                      {{ p }}
                    </button>
                    <button
                      @click="handleNextPage"
                      :disabled="!pagination.has_next"
                      class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <FeatherIcon name="chevron-right" class="w-5 h-5" />
                    </button>
                  </nav>
                </div>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Edit Modal -->
        <Dialog v-model="showEdit" :options="{ title: __('Chỉnh sửa hành động'), size: 'xl' }">
          <template #body-content>
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormControl type="select" :label="__('Chiến dịch ứng cử viên')" v-model="editForm.talent_campaign_id" :options="editOptions.candidateCampaigns" />
                <FormControl type="select" :label="__('Bước chiến dịch')" v-model="editForm.campaign_step" :options="editOptions.campaignSteps" />
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormControl type="select" :label="__('Trạng thái')" v-model="editForm.status" :options="statusOptions" />
                <FormControl type="select" :label="__('Người được giao')" v-model="editForm.assignee_id" :options="editOptions.assignees" />
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormControl type="datetime-local" :label="__('Dự kiến tại')" v-model="editForm.scheduled_at" />
                <FormControl type="datetime-local" :label="__('Thực hiện tại')" v-model="editForm.executed_at" />
              </div>
              <FormControl type="textarea" :label="__('Kết quả (JSON)')" v-model="editForm.result" :rows="4" :placeholder="__('Nhập dữ liệu JSON hoặc để trống ...')" />
            </div>
          </template>
          <template #actions>
            <Button variant="ghost" @click="showEdit = false">{{ __('Cancel') }}</Button>
            <Button variant="solid" :loading="savingEdit" @click="submitEdit">{{ __('Update') }}</Button>
          </template>
        </Dialog>
  
        <!-- View Modal -->
        <Dialog v-model="showView" :options="{ title: __('Chi tiết hành động'), size: 'xl' }">
          <template #body-content>
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Task name') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ viewData.campaign_step_name || viewData.campaign_step || '-' }}</div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Chiến dịch') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ viewData.campaign_name || '-' }}</div>
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Trạng thái') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">
                    <span :class="badgeClass(labelStatus(viewData.status))" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">{{ labelStatus(viewData.status) }}</span>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Người được giao') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ viewData.assignee_name || '-' }}</div>
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Ngày tạo') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ formatDate(viewData.creation) }}</div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Dự kiến tại') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ viewData.scheduled_at ? formatDate(viewData.scheduled_at) : '-' }}</div>
                </div>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Thực hiện tại') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ viewData.executed_at ? formatDate(viewData.executed_at) : '-' }}</div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Loại hành động') }}</label>
                  <div class="p-3 bg-gray-50 rounded-md text-sm">{{ viewData.action_type || '-' }}</div>
                </div>
              </div>
              <div v-if="viewData.result">
                <label class="block text-sm font-medium text-gray-700 mb-1">{{ __('Kết quả') }}</label>
                <div class="p-3 bg-gray-50 rounded-md text-sm">
                  <pre class="whitespace-pre-wrap text-xs">{{ typeof viewData.result === 'string' ? viewData.result : JSON.stringify(viewData.result, null, 2) }}</pre>
                </div>
              </div>
            </div>
          </template>
          <!-- <template #actions>
            <Button variant="ghost" @click="showView = false">{{ __('Đóng') }}</Button>
          </template> -->
        </Dialog>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, computed, onMounted } from 'vue'
  import { createResource, Breadcrumbs, FeatherIcon, Dialog, FormControl, Button } from 'frappe-ui'
  import { candidateCampaignService, campaignStepService, userService } from '../services/universalService'
  import { ToastContainer } from '@/components/shared'
  import { useToast } from '@/composables/useToast'
  import LayoutHeader from '@/components/LayoutHeader.vue'
  const breadcrumbs = [
    { label: __('My Tasks'), route: { name: 'MyActions' } }
  ]
  
  const activeTab = ref('pending')
  const loading = ref(false)
  const pending = ref([])
  const completed = ref([])
  const paginationState = ref({ pending: {}, completed: {} })
  const toast = useToast()

  const resource = createResource({
    url: 'mbw_mira.mbw_mira.doctype.action.action.get_my_actions',
    method: 'POST',
  })
  
  const page = ref(1)
  const limit = ref(10)
  
  const loadData = async () => {
    loading.value = true
    try {
      const res = await resource.submit({ page: page.value, limit: limit.value, include_scheduled_as_pending: 1, include_unassigned: 1 })
      if (res?.success) {
        pending.value = res.pending || []
        completed.value = res.completed || []
        paginationState.value = res.pagination || { pending: {}, completed: {} }
      }
    } finally {
      loading.value = false
    }
  }
  
  const currentItems = computed(() => activeTab.value === 'pending' ? pending.value : completed.value)
  const pagination = computed(() => paginationState.value[activeTab.value] || { page: 1, limit: limit.value, total: 0 })
  const showingFrom = computed(() => pagination.value.total === 0 ? 0 : ((pagination.value.page - 1) * pagination.value.limit) + 1)
  const showingTo = computed(() => Math.min(pagination.value.page * pagination.value.limit, pagination.value.total || 0))
  const totalPages = computed(() => pagination.value.pages || (pagination.value.total && pagination.value.limit ? Math.ceil(pagination.value.total / pagination.value.limit) : 1))
  
  const visiblePages = computed(() => {
    const total = totalPages.value
    const current = pagination.value.page || 1
    const delta = 2
    const range = []
    for (let i = Math.max(1, current - delta); i <= Math.min(total, current + delta); i++) {
      range.push(i)
    }
    if (!range.includes(1)) range.unshift(1)
    if (!range.includes(total)) range.push(total)
    return Array.from(new Set(range)).filter(p => p >= 1 && p <= total)
  })
  
  const setTab = (tab) => {
    activeTab.value = tab
    // dùng chung page cho đơn giản
  }
  
  const handleNextPage = () => {
    if (pagination.value.has_next) {
      page.value++
      loadData()
    }
  }
  const handlePreviousPage = () => {
    if (pagination.value.has_prev && page.value > 1) {
      page.value--
      loadData()
    }
  }
  
  const goToPage = (p) => {
    if (p && p !== pagination.value.page) {
      page.value = p
      loadData()
    }
  }
  
  const labelStatus = (s) => {
    if (s === 'PENDING_MANUAL' || s === 'SCHEDULED') return 'Đang chờ'
    if (s === 'EXECUTED') return 'Hoàn thành'
    return s
  }
  
  const badgeClass = (label) => ({
    'Đang chờ': 'bg-yellow-100 text-yellow-800',
    'Hoàn thành': 'bg-green-100 text-green-800'
  }[label] || 'bg-gray-100 text-gray-800')
  
  const formatDate = (v) => v ? new Date(v).toLocaleString() : ''
  
  onMounted(loadData)
  
  // Update action to EXECUTED
  const updateAction = async (item) => {
    try {
      const updater = createResource({ url: 'mbw_mira.mbw_mira.doctype.action.action.update_action', method: 'POST' })
      const payload = {
        name: item.name,
        status: 'EXECUTED',
        executed_at: new Date().toISOString()
      }
      const res = await updater.submit(payload)
      if (res?.success) {
        toast.success(__('Đã cập nhật hành động thành công'))
        // Reload data and switch to Completed tab
        await loadData()
        activeTab.value = 'completed'
      } else {
        toast.error(res?.error || __('Cập nhật hành động thất bại'))
      }
    } catch (e) {
      toast.error(e.message || __('Cập nhật hành động thất bại'))
    }
  }
  
  // Edit modal logic
  const showEdit = ref(false)
  const savingEdit = ref(false)
  const editForm = reactive({
    name: '',
    talent_campaign_id: '',
    campaign_step: '',
    status: 'PENDING_MANUAL',
    assignee_id: '',
    scheduled_at: '',
    executed_at: '',
    result: ''
  })
  
  // View modal logic
  const showView = ref(false)
  const viewData = reactive({})
  
  const statusOptions = [
    { label: 'Pending Manual', value: 'PENDING_MANUAL' },
    { label: 'Scheduled', value: 'SCHEDULED' },
    { label: 'Executed', value: 'EXECUTED' },
    { label: 'Skipped', value: 'SKIPPED' },
    { label: 'Failed', value: 'FAILED' }
  ]
  
  // Options for modal selects
  const editOptions = reactive({
    candidateCampaigns: [],
    campaignSteps: [],
    assignees: []
  })
  
  const loadEditOptions = async () => {
    try {
      const candidateCampaignResult = await candidateCampaignService.getList({
        fields: ['name', 'talent_id', 'campaign_id'],
        page_length: 1000
      })
      if (candidateCampaignResult.success) {
        editOptions.candidateCampaigns = candidateCampaignResult.data.map(i => ({
          label: `${i.name} (${i.talent_id} - ${i.campaign_id})`,
          value: i.name
        }))
      }
  
      const campaignStepResult = await campaignStepService.getList({
        fields: ['name', 'campaign_step_name', 'campaign'],
        page_length: 1000
      })
      if (campaignStepResult.success) {
        editOptions.campaignSteps = campaignStepResult.data.map(i => ({
          label: `${i.campaign_step_name} (${i.campaign})`,
          value: i.name,
          campaign: i.campaign
        }))
      }
  
      const userResult = await userService.getList({ fields: ['name', 'full_name', 'email'], page_length: 1000 })
      if (userResult.success) {
        editOptions.assignees = userResult.data.map(u => ({ label: `${u.full_name} (${u.email})`, value: u.name }))
      }
    } catch (e) {
      // ignore
    }
  }
  
  const openView = async (item) => {
    // Lấy dữ liệu đầy đủ từ server để hiển thị chi tiết
    try {
      const getDoc = createResource({ url: 'mbw_mira.api.common.get_form_data', method: 'POST' })
      const res = await getDoc.submit({ doctype: 'Action', name: item.name })
      const data = res?.data || {}
      Object.assign(viewData, {
        ...item,
        ...data,
        campaign_step_name: data.campaign_step_name || item.campaign_step_name || item.campaign_step,
        campaign_name: data.campaign_name || item.campaign_name,
        assignee_name: data.assignee_name || item.assignee_name
      })
    } catch (e) {
      // fallback dùng dữ liệu trong list
      Object.assign(viewData, {
        ...item,
        campaign_step_name: item.campaign_step_name || item.campaign_step,
        campaign_name: item.campaign_name,
        assignee_name: item.assignee_name
      })
    }
    showView.value = true
  }
  
  const openEdit = async (item) => {
    if (!editOptions.candidateCampaigns.length) {
      await loadEditOptions()
    }
    // Lấy dữ liệu đầy đủ từ server để đảm bảo có field result
    try {
      const getDoc = createResource({ url: 'mbw_mira.api.common.get_form_data', method: 'POST' })
      const res = await getDoc.submit({ doctype: 'Action', name: item.name })
      const data = res?.data || {}
      Object.assign(editForm, {
        name: data.name || item.name,
        talent_campaign_id: data.talent_campaign_id || item.talent_campaign_id,
        campaign_step: data.campaign_step || item.campaign_step,
        status: data.status || item.status,
        assignee_id: data.assignee_id || item.assignee_id || '',
        scheduled_at: data.scheduled_at ? String(data.scheduled_at).substring(0, 16) : (item.scheduled_at ? item.scheduled_at.substring(0, 16) : ''),
        executed_at: data.executed_at ? String(data.executed_at).substring(0, 16) : (item.executed_at ? item.executed_at.substring(0, 16) : ''),
        result: data.result ? (typeof data.result === 'string' ? data.result : JSON.stringify(data.result)) : (item.result ? (typeof item.result === 'string' ? item.result : JSON.stringify(item.result)) : '')
      })
    } catch (e) {
      // fallback dùng dữ liệu trong list
      Object.assign(editForm, {
        name: item.name,
        talent_campaign_id: item.talent_campaign_id,
        campaign_step: item.campaign_step,
        status: item.status,
        assignee_id: item.assignee_id || '',
        scheduled_at: item.scheduled_at ? item.scheduled_at.substring(0, 16) : '',
        executed_at: item.executed_at ? item.executed_at.substring(0, 16) : '',
        result: item.result ? (typeof item.result === 'string' ? item.result : JSON.stringify(item.result)) : ''
      })
    }
    showEdit.value = true
  }
  
  const submitEdit = async () => {
    savingEdit.value = true
    try {
      const updater = createResource({ url: 'mbw_mira.mbw_mira.doctype.action.action.update_action', method: 'POST' })
      const res = await updater.submit({
        name: editForm.name,
        talent_campaign_id: editForm.talent_campaign_id,
        campaign_step: editForm.campaign_step,
        status: editForm.status,
        assignee_id: editForm.assignee_id || null,
        scheduled_at: editForm.scheduled_at || null,
        executed_at: editForm.executed_at || null,
        result: editForm.result || ''
      })
      if (res?.success) {
        toast.success(__('Cập nhật hành động thành công'))
        showEdit.value = false
        await loadData()
      } else {
        toast.error(res?.error || __('Cập nhật thất bại'))
      }
    } catch (e) {
      toast.error(e.message || __('Cập nhật thất bại'))
    } finally {
      savingEdit.value = false
    }
  }
  </script>
  
  <style scoped>
  </style>
  
  