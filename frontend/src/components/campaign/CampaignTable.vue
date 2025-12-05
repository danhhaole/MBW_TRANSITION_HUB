<template>
  <!-- Table Container Only -->
  <div>
      <!-- Loading State -->
      <Loading v-if="loading" text="Loading campaigns..." />

      <!-- Table -->
      <div v-else-if="campaigns?.length > 0" class="overflow-x-auto">
        <table class="min-w-full bg-white rounded-lg overflow-hidden">
          <thead class="bg-gray-100">
            <tr>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Name') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Sender') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Send Date') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Sent') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Receiver') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Open') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Click') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Status') }}</th>
              <th class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider">{{ __('Actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr 
              v-for="campaign in campaigns" 
              :key="campaign.name || campaign.id"
              class="hover:bg-gray-50"
            >
              <!-- Tên -->
              <td class="py-4 px-4">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center mr-3">
                    <FeatherIcon 
                      :name="getInteractionIcon(campaign.interaction_method)" 
                      class="h-4 w-4 text-blue-600" 
                    />
                  </div>
                  <div>
                    <div class="font-medium text-base text-gray-800">{{ campaign.campaign_name || campaign.name }}</div>
                    <div class="text-xs text-gray-500">{{ getInteractionMethodText(campaign.interaction_method) }}</div>
                  </div>
                </div>
              </td>

              <!-- Người gửi -->
              <td class="py-4 px-4 text-sm text-gray-700">
                {{ campaign.sender || campaign.owner || 'Admin' }}
              </td>

              <!-- Ngày gửi -->
              <td class="py-4 px-4 text-sm text-gray-700">
                {{ formatDate(campaign.sent_date || campaign.start_date) }}
              </td>

              <!-- Đã gửi -->
              <td class="py-4 px-4 text-sm text-gray-700">
                <div class="flex items-center">
                  <span class="font-medium">{{ campaign.sent_count || 0 }}</span>
                  <span class="text-gray-500 ml-1">/ {{ campaign.total_recipients || 0 }}</span>
                </div>
              </td>

              <!-- Người nhận -->
              <td class="py-4 px-4 text-sm text-gray-700">
                {{ campaign.delivered_count || 0 }}
              </td>

              <!-- Người mở -->
              <td class="py-4 px-4 text-sm text-gray-700">
                <div class="flex items-center">
                  <span class="font-medium">{{ campaign.opened_count || 0 }}</span>
                  <span class="text-xs text-gray-500 ml-1">
                    ({{ getOpenRate(campaign) }}%)
                  </span>
                </div>
              </td>

              <!-- Lượt click -->
              <td class="py-4 px-4 text-sm text-gray-700">
                <div class="flex items-center">
                  <span class="font-medium">{{ campaign.clicked_count || 0 }}</span>
                  <span class="text-xs text-gray-500 ml-1">
                    ({{ getClickRate(campaign) }}%)
                  </span>
                </div>
              </td>

              <!-- Trạng thái -->
              <td class="py-4 px-4">
                <select
                  :value="campaign.status"
                  @change="handleStatusChange(campaign, $event.target.value)"
                  :class="getStatusSelectClass(campaign.status)"
                  class="text-xs px-2 py-1 rounded-full border-0 font-medium cursor-pointer focus:outline-none focus:ring-2 focus:ring-offset-1"
                >
                  <option value="DRAFT">{{ __('Draft') }}</option>
                  <option value="ACTIVE">{{ __('Active') }}</option>
                  <option value="PAUSED">{{ __('Paused') }}</option>
                  <option value="ARCHIVED">{{ __('Archived') }}</option>
                </select>
              </td>

              <!-- Actions -->
              <td class="py-4 px-4">
                <div class="flex items-center space-x-2">
                  <button 
                    @click="handleView(campaign)"
                    class="text-gray-600 hover:text-blue-600 p-2 rounded-md hover:bg-blue-50 transition-colors"
                    :title="__('View Details')"
                  >
                    <FeatherIcon name="eye" class="h-4 w-4" />
                  </button>
                  <button 
                    v-if="canEdit"
                    @click="handleEdit(campaign)"
                    class="text-gray-600 hover:text-green-600 p-2 rounded-md hover:bg-green-50 transition-colors"
                    :title="__('Edit')"
                  >
                    <FeatherIcon name="edit" class="h-4 w-4" />
                  </button>
                  <button 
                    v-if="canEdit"
                    @click="handleSaveAsTemplate(campaign)"
                    class="text-gray-600 hover:text-purple-600 p-2 rounded-md hover:bg-purple-50 transition-colors"
                    :title="__('Save as Template')"
                  >
                    <FeatherIcon name="bookmark" class="h-4 w-4" />
                  </button>
                  <button
                    v-if="campaign.status === 'DRAFT' && canDelete" 
                    @click="handleDelete(campaign)"
                    class="text-gray-600 hover:text-red-600 p-2 rounded-md hover:bg-red-50 transition-colors"
                    :title="__('Delete')"
                  >
                    <FeatherIcon name="trash-2" class="h-4 w-4" />
                  </button>
                  <!-- <button v-if="campaign.status === 'ACTIVE'" @click="handleShowQr(campaign)" class="text-gray-600 hover:text-indigo-600 p-2 rounded-md hover:bg-indigo-50 transition-colors" :title="__('Show QR Code')">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h6v6H3V3zm12 0h6v6h-6V3zM3 15h6v6H3v-6zm12 0h6v6h-6v-6z" />
                    </svg>
                  </button> -->
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- No Data State -->
      <div v-else class="text-center py-12">
        <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">{{ __('No campaigns found') }}</h3>
        <p class="text-gray-500 mb-4">{{ __('Start creating your first recruitment campaign') }}</p>
        <Button
          @click="$emit('create')"
          theme="gray"
          variant="solid"
          class="text-sm font-medium"
        >
          {{ __('Create Campaign') }}
        </Button>
      </div>

      <!-- Pagination -->
      <div v-if="campaigns?.length > 0 && pagination.total > 0" class="flex items-center justify-between mt-6 p-6 border-t border-gray-200 ">
        <div class="text-sm text-gray-600">
          {{ __('Display') }} {{ pagination.showing_from || 1 }}-{{ pagination.showing_to || campaigns.length }} {{ __('of') }} {{ pagination.total || campaigns.length }} {{ __('campaigns') }}
        </div>
        <div class="flex space-x-1">
          <button 
            @click="handlePageChange(1)"
            :disabled="pagination.page === 1"
            class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          
          <template v-for="page in getPaginationRange()" :key="page">
            <button
              v-if="page === '...'"
              class="px-3 py-1 text-gray-500"
              disabled
            >
              ...
            </button>
            <button
              v-else
              @click="handlePageChange(page)"
              :class="pagination.page === page ? 'bg-black text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
              class="px-3 py-1 rounded-md"
            >
              {{ page }}
            </button>
          </template>
          
          <button 
            @click="handlePageChange(pagination.page + 1)"
            :disabled="pagination.page >= pagination.pages"
            class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
  </div>


  <!-- QR Code Dialog -->
  <Dialog v-model="showQrDialog" :options="{ title: 'QR Code', size: 'md' }">
    <template #body-content>
      <div class="flex flex-col items-center justify-center p-4">
        <img v-if="qrData.image" :src="qrData.image" alt="QR Code" class="mb-4 w-48 h-48 object-contain" />
        <div v-if="qrData.url" class="text-sm break-all text-center">
          <a :href="qrData.url" target="_blank" class="text-blue-600 underline">{{ qrData.url }}</a>
        </div>
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end">
        <Button variant="outline" theme="gray" @click="showQrDialog = false">{{ __('Close') }}</Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Dialog, FeatherIcon } from 'frappe-ui'
import { Button } from 'frappe-ui'
import Loading from '@/components/Loading.vue'
import { call } from 'frappe-ui'
import { usePermissionStore } from "@/stores/permission"

const permission = usePermissionStore()
const canEdit = permission.can("Mira Campaign", "edit")
const canDelete = permission.can("Mira Campaign", "delete")

// Translation helper function  


// Props
const props = defineProps({
  campaigns: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  pagination: {
    type: Object,
    default: () => ({
      page: 1,
      limit: 10,
      total: 0,
      pages: 1,
      has_next: false,
      has_prev: false,
      showing_from: 0,
      showing_to: 0
    })
  }
})

// Emits
const emit = defineEmits([
  'edit', 'view', 'delete', 'save-as-template', 'page-change', 'status-change'
])

// Refs
const showQrDialog = ref(false)
const qrData = ref({ url: '', image: '' })

// Handle status change
const handleStatusChange = async (campaign, newStatus) => {
  try {
    await call('frappe.client.set_value', {
      doctype: 'Mira Campaign',
      name: campaign.name,
      fieldname: 'status',
      value: newStatus
    })
    
    // Update local data
    campaign.status = newStatus
    
    // Emit event to parent
    emit('status-change', { campaign, newStatus })
    
    console.log(`✅ Status updated to ${newStatus}`)
  } catch (error) {
    console.error('❌ Error updating status:', error)
    // Revert on error
    location.reload()
  }
}

// Methods for UI
const getStatusBadgeClass = (status) => {
  const classes = {
    'DRAFT': 'bg-gray-100 text-gray-800',
    'ACTIVE': 'bg-blue-100 text-blue-800',
    'PAUSED': 'bg-yellow-100 text-yellow-800',
    'ARCHIVED': 'bg-green-100 text-green-800',
    'FAILED': 'bg-red-100 text-red-800',
    'CANCELLED': 'bg-orange-100 text-orange-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

// Status select styling
const getStatusSelectClass = (status) => {
  const classes = {
    'DRAFT': 'bg-gray-100 text-gray-800 focus:ring-gray-500',
    'ACTIVE': 'bg-blue-100 text-blue-800 focus:ring-blue-500',
    'PAUSED': 'bg-yellow-100 text-yellow-800 focus:ring-yellow-500',
    'ARCHIVED': 'bg-green-100 text-green-800 focus:ring-green-500'
  }
  return classes[status] || 'bg-gray-100 text-gray-800 focus:ring-gray-500'
}

const getStatusText = (status) => {
  const texts = {
    'DRAFT': 'Draft',
    'ACTIVE': 'Active', 
    'PAUSED': 'Paused',
    'ARCHIVED': 'Archived',
    'FAILED': 'Failed',
    'CANCELLED': 'Cancelled'
  }
  return texts[status] || status
}

// New helper methods for interaction methods
const getInteractionIcon = (method) => {
  const icons = {
    'EMAIL': 'mail',
    'ZALO_ZNS': 'message-circle',
    'ZALO_CARE': 'heart'
  }
  return icons[method] || 'mail'
}

const getInteractionMethodText = (method) => {
  const texts = {
    'EMAIL': 'Email',
    'ZALO_ZNS': 'Zalo ZNS',
    'ZALO_CARE': 'Zalo Quan tâm'
  }
  return texts[method] || method
}

// Calculate rates
const getOpenRate = (campaign) => {
  if (!campaign.delivered_count || campaign.delivered_count === 0) return 0
  return Math.round((campaign.opened_count || 0) / campaign.delivered_count * 100)
}

const getClickRate = (campaign) => {
  if (!campaign.opened_count || campaign.opened_count === 0) return 0
  return Math.round((campaign.clicked_count || 0) / campaign.opened_count * 100)
}

const getProgressBarClass = (status) => {
  const classes = {
    'DRAFT': 'bg-gray-500',
    'ACTIVE': 'bg-blue-500',
    'PAUSED': 'bg-yellow-500',
    'ARCHIVED': 'bg-green-500'
  }
  return classes[status] || 'bg-gray-500'
}

const getProgress = (campaign) => {
  if (!campaign.start_date || !campaign.end_date) {
    // Default progress based on status
    const progressMap = {
      'DRAFT': 10,
      'ACTIVE': 60,
      'PAUSED': 40,
      'ARCHIVED': 100
    }
    return progressMap[campaign.status] || 0
  }
  
  const now = new Date()
  const start = new Date(campaign.start_date)
  const end = new Date(campaign.end_date)
  
  if (now < start) return 0
  if (now > end) return 100
  
  const total = end - start
  const current = now - start
  return Math.round((current / total) * 100)
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  try {
    return new Date(dateString).toLocaleDateString('vi-VN')
  } catch {
    return dateString
  }
}

// const getInitials = (name) => {
//   if (!name) return '?'
//   return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
// }

const getPaginationRange = () => {
  const totalPages = props.pagination?.pages || 1
  const currentPage = props.pagination?.page || 1
  const range = []
  
  if (totalPages <= 5) {
    for (let i = 1; i <= totalPages; i++) {
      range.push(i)
    }
  } else {
    if (currentPage <= 3) {
      range.push(1, 2, 3, 4, '...', totalPages)
    } else if (currentPage >= totalPages - 2) {
      range.push(1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages)
    } else {
      range.push(1, '...', currentPage - 1, currentPage, currentPage + 1, '...', totalPages)
    }
  }
  
  return range
}

// Event handlers
const handleEdit = (item) => {
  emit('edit', item)
}

const handleView = (item) => {
  emit('view', item)
}

const handleDelete = (item) => {
  // Emit delete event directly to parent
  emit('delete', item)
}

const handleSaveAsTemplate = (item) => {
  emit('save-as-template', item)
}

const handlePageChange = (page) => {
  emit('page-change', page)
}

async function handleShowQr(campaign) {
  try {
    const res = await call('mbw_mira.api.get_campaign_qrcode', {
      campaign_id: campaign.name
    })
    qrData.value = res
    showQrDialog.value = true
  } catch (e) {
    qrData.value = { url: '', image: '' }
    showQrDialog.value = false
  }
}
</script>

<style scoped>
/* Basic Tailwind CSS styles are handled by classes in template */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
