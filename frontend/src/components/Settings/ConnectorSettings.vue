<template>
  <div class="flex flex-col h-full">
    <!-- Header Section -->
    <div class="flex items-center justify-between px-6 py-5 border-b border-gray-200">
      <div>
        <h2 class="text-lg font-semibold text-gray-900">{{ __('Connectors') }}</h2>
        <p class="mt-1 text-sm text-gray-500">
          {{ __('Manage external integrations and data source connections') }}
        </p>
      </div>
    </div>

    <!-- Content Section -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Filters & Controls -->
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex flex-wrap items-center gap-3">
          <!-- Search -->
          <div class="flex-1 min-w-[200px]">
            <FormControl
              v-model="searchText"
              type="text"
              :placeholder="__('Search connectors...')"
            >
              <template #prefix>
                <FeatherIcon name="search" class="w-4" />
              </template>
            </FormControl>
          </div>

          <!-- Type Filter -->
          <FormControl
            type="select"
            v-model="typeFilter"
            :options="[
              { label: __('All Types'), value: '' },
              { label: __('Social Media'), value: 'social_media' },
              { label: __('Messaging'), value: 'messaging' },
              { label: __('Job Board'), value: 'job_board' },
            ]"
            class="w-32"
          />

          <!-- Status Filter -->
          <FormControl
            type="select"
            v-model="statusFilter"
            :options="[
              { label: __('All'), value: '' },
              { label: __('Connected'), value: 'connected' },
              { label: __('Not Connected'), value: 'not_connected' },
              { label: __('Pending'), value: 'pending' },
              { label: __('Failed'), value: 'failed' },
            ]"
            class="w-32"
          />

          <!-- Refresh Button -->
          <Button
            @click="handleRefresh"
            :loading="isRefreshing"
            variant="outline"
            size="sm"
          >
            <template #prefix>
              <FeatherIcon name="refresh-cw" class="w-4 h-4" />
            </template>
            {{ __("Refresh") }}
          </Button>
        </div>
      </div>

      <!-- Connectors List -->
      <div class="px-6 py-4 overflow-y-auto">
        <!-- Loading State -->
        <div v-if="loading" class="flex items-center justify-center py-12">
          <FeatherIcon name="loader" class="w-6 h-6 animate-spin text-gray-400" />
          <span class="ml-2 text-sm text-gray-500">{{ __('Loading...') }}</span>
        </div>

        <!-- Connectors Grid -->
        <div v-else class="grid grid-cols-1 gap-3">
          <div
            v-for="platform in filteredPlatforms"
            :key="platform.id"
            class="flex items-center justify-between p-4 bg-white border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-sm transition-all"
          >
            <div class="flex items-center flex-1 min-w-0">
              <!-- Platform Icon -->
              <div class="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-2xl">
                {{ platform.icon }}
              </div>

              <!-- Platform Info -->
              <div class="ml-4 flex-1 min-w-0">
                <div class="flex items-center space-x-2">
                  <h3 class="text-sm font-medium text-gray-900">{{ platform.name }}</h3>
                  <span
                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                    :class="getTypeColor(platform.type)"
                  >
                    {{ platform.type_display }}
                  </span>
                </div>
                <p class="text-xs text-gray-500 mt-0.5">{{ platform.description }}</p>
                
                <!-- Connection Status -->
                <div class="flex items-center space-x-2 mt-1">
                  <div
                    class="w-2 h-2 rounded-full"
                    :class="getStatusColor(platform.id)"
                  ></div>
                  <span class="text-xs text-gray-600">{{ getConnectionStatusText(platform.id) }}</span>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center space-x-1 ml-4">
              <!-- Connect Button - Chỉ khi chưa kết nối -->
               
              <Button
                v-if="!hasConnection(platform.id)"
                variant="ghost"
                size="sm"
                @click="handleConnect(platform)"
                :title="__('Connect')"
              >
                <FeatherIcon name="link" class="w-4 h-4" />
              </Button>
              
              <!-- View Button - Luôn hiển thị -->
              <Button
                variant="ghost"
                size="sm"
                @click="handleView(platform)"
                :title="__('View')"
              >
                <FeatherIcon name="eye" class="w-4 h-4" />
              </Button>

              <!-- Edit Button - Chỉ khi đã kết nối -->
              <Button
                v-if="hasConnection(platform.id)"
                variant="ghost"
                size="sm"
                @click="handleEdit(platform)"
                :title="__('Edit')"
              >
                <FeatherIcon name="edit" class="w-4 h-4" />
              </Button>
              
              <!-- Disconnect Button - Chỉ khi đã kết nối -->
              <Button
                v-if="hasConnection(platform.id)"
                variant="ghost"
                size="sm"
                @click="handleDisconnect(platform)"
                class="text-red-600 hover:text-red-700"
                :title="__('Disconnect')"
              >
                <FeatherIcon name="x" class="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Connect Platform Modal -->
    <Dialog
      v-if="showConnectModal"
      v-model="showConnectModal"
      :options="{ title: getModalTitle('connect'), size: '2xl' }"
    >
      <template #body-content>
        <div v-if="selectedPlatform" class="space-y-4 p-4">
          <!-- Platform Info -->
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
            <span class="text-2xl">{{ selectedPlatform.icon }}</span>
            <div>
              <h3 class="font-semibold text-gray-900">{{ selectedPlatform.name }}</h3>
              <p class="text-sm text-gray-600">{{ selectedPlatform.description }}</p>
            </div>
          </div>

          <!-- Dynamic Form based on Platform -->
          <component
            :is="currentFormComponent"
            v-model="currentConnectionForm"
            :platform="selectedPlatform"
            :is-edit="false"
            @submit="handleConnectionSubmit"
            @cancel="closeConnectModal"
          />
        </div>
      </template>
    </Dialog>

    <!-- Edit Connection Modal -->
    <Dialog
      v-if="showEditModal"
      v-model="showEditModal"
      :options="{ title: getModalTitle('edit'), size: '2xl' }"
    >
      <template #body-content>
        <div v-if="editingConnection && selectedPlatform" class="space-y-4 p-4">
          <!-- Platform Info -->
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
            <span class="text-2xl">{{ selectedPlatform.icon }}</span>
            <div>
              <h3 class="font-semibold text-gray-900">{{ selectedPlatform.name }}</h3>
              <p class="text-sm text-gray-600">{{ __("Edit connection settings") }}</p>
              <span
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium mt-1"
                :class="getConnectionStatusBadgeClass(selectedPlatform.id)"
              >
                {{ getConnectionStatusText(selectedPlatform.id) }}
              </span>
            </div>
          </div>

          <!-- Dynamic Form based on Platform -->
          <component
            :is="currentFormComponent"
            v-model="currentEditForm"
            :platform="selectedPlatform"
            :connectionType="selectedPlatform"
            :isEdit="true"
            :existingConnection="editingConnection"
            :connectedAccounts="editingConnection.accounts || []"
            @submit="handleConnectionUpdate"
            @cancel="closeEditModal"
          />
        </div>
      </template>
    </Dialog>

    <!-- View Modal -->
    <Dialog
      v-model="showViewModal"
      :options="{
        title: __('Platform Details'),
        size: 'lg',
      }"
    >
      <template #body>
        <div v-if="selectedPlatform" class="p-6">
          <div class="space-y-6">
            <!-- Basic Info -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">
                {{ __("Basic Information") }}
              </h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-500">{{
                    __("Platform Name")
                  }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedPlatform.name }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{
                    __("Type")
                  }}</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ selectedPlatform.type_display }}
                  </p>
                </div>
                <div class="col-span-2">
                  <label class="text-sm font-medium text-gray-500">{{
                    __("Description")
                  }}</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ selectedPlatform.description }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Status Info -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">
                {{ __("Connection Status") }}
              </h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-500">{{
                    __("Current Status")
                  }}</label>
                  <div class="mt-1 flex items-center space-x-2">
                    <div
                      class="w-2 h-2 rounded-full"
                      :class="getStatusColor(selectedPlatform.id)"
                    ></div>
                    <span class="text-sm text-gray-900">{{
                      getConnectionStatusText(selectedPlatform.id)
                    }}</span>
                  </div>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{
                    __("Connection ID")
                  }}</label>
                  <p class="mt-1 text-xs text-gray-900 font-mono">
                    {{ getConnectionByPlatformId(selectedPlatform.id)?.connection_id || 'N/A' }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Connected Accounts Section -->
            <div v-if="getConnectionStatus(selectedPlatform.id) === 'Connected'">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-medium text-gray-900">
                  {{ __("Connected Pages/Accounts") }}
                </h3>
              </div>

              <!-- Loading State for Accounts -->
              <div v-if="loadingAccounts" class="flex items-center justify-center py-8">
                <FeatherIcon name="loader" class="w-5 h-5 animate-spin text-blue-600 mr-2" />
                <span class="text-sm text-gray-600">{{ __("Loading pages...") }}</span>
              </div>

              <!-- Connected Accounts List -->
              <div v-else-if="viewModalAccounts.length > 0" class="space-y-3">
                <div
                  v-for="account in viewModalAccounts"
                  :key="account.external_account_id"
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border"
                >
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                      <FeatherIcon name="user" class="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <div class="font-medium text-gray-900 text-sm">
                        {{ account.account_name }}
                      </div>
                      <div class="text-xs text-gray-500">
                        {{ account.external_account_id }}
                      </div>
                    </div>
                  </div>
                  <div class="text-xs text-gray-500">
                    {{ account.is_active ? __('Active') : __('Inactive') }}
                  </div>
                </div>
              </div>

              <!-- No Pages Found -->
              <div v-else class="text-center py-8">
                <FeatherIcon name="alert-circle" class="w-12 h-12 text-gray-400 mx-auto mb-2" />
                <p class="text-sm text-gray-500">{{ __("No pages or accounts found") }}</p>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <Button @click="closeViewModal" variant="ghost">
          {{ __("Close") }}
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, shallowRef, reactive } from 'vue'
import { Button, FeatherIcon, FormControl, Dialog, call } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { disableSettingModalOutsideClick } from '@/composables/settings'
import FacebookConnectionForm from '@/components/Connectors/FacebookConnectionForm.vue'
import ZaloConnectionForm from '@/components/Connectors/ZaloConnectionForm.vue'
import TopcvConnectionForm from '@/components/Connectors/TopcvConnectionForm.vue'

const toast = useToast()

// Platform form components mapping
const platformFormComponents = shallowRef({
  facebook: FacebookConnectionForm,
  zalo: ZaloConnectionForm,
  topcv: TopcvConnectionForm,
})

// State
const searchText = ref('')
const typeFilter = ref('')
const statusFilter = ref('')
const loading = ref(false)
const isRefreshing = ref(false)
const connections = ref([])
const showViewModal = ref(false)
const showConnectModal = ref(false)
const showEditModal = ref(false)
const selectedPlatform = shallowRef(null)
const editingConnection = shallowRef(null)
const loadingAccounts = ref(false)
const viewModalAccounts = ref([])

// Form data
const connectForm = reactive({
  tenant_name: '',
  hook_url: '',
  redirect_url: '',
  user_email: '',
  full_name: '',
})

const editFormData = reactive({
  tenant_name: '',
  hook_url: '',
  redirect_url: '',
  user_email: '',
  full_name: '',
})

// Platform definitions
const platforms = [
  {
    id: 'facebook',
    name: 'Facebook',
    icon: '📘',
    description: 'Connect Facebook Pages and Personal Profiles',
    type: 'social_media',
    type_display: 'Social Network',
  },
  {
    id: 'zalo',
    name: 'Zalo',
    icon: '💬',
    description: 'Connect Zalo Official Accounts',
    type: 'messaging',
    type_display: 'Messaging',
  },
  {
    id: 'topcv',
    name: 'TopCV',
    icon: '💼',
    description: 'Connect TopCV Job Portal',
    type: 'job_board',
    type_display: 'Job Board',
  },
  {
    id: 'mobiwork_ats',
    name: 'MobiWork ATS',
    icon: '🧰',
    description: 'Connect MobiWork Applicant Tracking System',
    type: 'job_board',
    type_display: 'ATS',
  },
]

// Computed
const filteredPlatforms = computed(() => {
  let filtered = platforms

  // Search filter
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    filtered = filtered.filter(p => 
      p.name.toLowerCase().includes(search) ||
      p.description.toLowerCase().includes(search)
    )
  }

  // Type filter
  if (typeFilter.value) {
    filtered = filtered.filter(p => p.type === typeFilter.value)
  }

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(p => {
      const status = getConnectionStatus(p.id)
      switch (statusFilter.value) {
        case 'connected':
          return status === 'Connected'
        case 'not_connected':
          return !status
        case 'pending':
          return status === 'Pending'
        case 'failed':
          return status === 'Failed' || status === 'Disconnected'
        default:
          return true
      }
    })
  }

  return filtered
})

const currentFormComponent = computed(() => {
  if (!selectedPlatform.value?.id) return null
  return platformFormComponents.value[selectedPlatform.value.id] || FacebookConnectionForm
})

const currentConnectionForm = computed({
  get() {
    return { ...connectForm }
  },
  set(value) {
    Object.assign(connectForm, value)
  },
})

const currentEditForm = computed({
  get() {
    return { ...editFormData }
  },
  set(value) {
    Object.assign(editFormData, value)
  },
})

const getModalTitle = (type) => {
  if (!selectedPlatform.value) return __('Platform Connection')
  if (type === 'connect') {
    return `${__('Connect to')} ${selectedPlatform.value.name}`
  } else if (type === 'edit') {
    const status = getConnectionStatus(selectedPlatform.value.id)
    return `${__('Edit')} ${selectedPlatform.value.name} ${__('Connection')}${
      status ? ` (${status})` : ''
    }`
  }
  return __('Platform Connection')
}

const getConnectionStatusBadgeClass = (platformId) => {
  const status = getConnectionStatus(platformId)
  switch (status) {
    case 'Connected':
      return 'bg-green-100 text-green-800'
    case 'Pending':
      return 'bg-yellow-100 text-yellow-800'
    case 'Failed':
    case 'Disconnected':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

// Methods
const loadConnections = async () => {
  loading.value = true
  try {
    const response = await call('mbw_mira.api.external_connections.get_connection_info', {})
    
    let connectionsData = []
    if (response && response.status === 'success' && response.data) {
      connectionsData = Array.isArray(response.data) ? response.data : []
    } else if (response && response.message) {
      connectionsData = Array.isArray(response.message) ? response.message : []
    } else if (Array.isArray(response)) {
      connectionsData = response
    }
    
    connections.value = connectionsData
  } catch (error) {
    console.error('Error loading connections:', error)
    toast.error(__('Failed to load connections'))
  } finally {
    loading.value = false
  }
}

const getConnectionByPlatformId = (platformId) => {
  if (!Array.isArray(connections.value)) return null

  return connections.value.find(
    (conn) => conn.platform_type.toLowerCase() === platformId
  )
}

const getConnectionStatus = (platformId) => {
  const connection = getConnectionByPlatformId(platformId)

  return connection?.connection_status || null
}

const hasConnection = (platformId) => {

  return getConnectionByPlatformId(platformId) !== undefined
}

const getConnectionStatusText = (platformId) => {
  const status = getConnectionStatus(platformId)
  return status ? __(status) : __('Not Connected')
}

const getStatusColor = (platformId) => {
  const status = getConnectionStatus(platformId)
  const colors = {
    Connected: 'bg-green-500',
    Pending: 'bg-yellow-500',
    Failed: 'bg-red-500',
    Disconnected: 'bg-gray-500',
  }
  return colors[status] || 'bg-gray-300'
}

const getTypeColor = (type) => {
  if (type === 'social_media') return 'bg-blue-100 text-blue-800'
  if (type === 'messaging') return 'bg-green-100 text-green-800'
  if (type === 'job_board') return 'bg-purple-100 text-purple-800'
  return 'bg-gray-100 text-gray-800'
}

const handleConnect = (platform) => {
  selectedPlatform.value = { ...platform }
  resetForm(connectForm)
  showConnectModal.value = true
  disableSettingModalOutsideClick.value = true
}

const closeConnectModal = () => {
  showConnectModal.value = false
  selectedPlatform.value = null
  resetForm(connectForm)
  disableSettingModalOutsideClick.value = false
}

const resetForm = (formObject) => {
  Object.keys(formObject).forEach((key) => {
    formObject[key] = ''
  })
}

const handleConnectionSubmit = async (connectionData) => {
  try {
    const response = await call('mbw_mira.api.external_connections.create_connection', {
      platform_type: selectedPlatform.value.name,
      ...connectionData,
    })

    // Handle response with login URL
    if (response?.data?.login_url) {
      const win = window.open(response.data.login_url, '_blank')
      if (!win || win.closed || typeof win.closed === 'undefined') {
        toast.warning(__('Please allow popups to complete authentication.'))
      } else {
        toast.info(__('Please complete authentication in the new window.'))
      }
    } else {
      toast.success(__('Connection created successfully'))
    }

    closeConnectModal()
    await loadConnections()
  } catch (error) {
    console.error('Error creating connection:', error)
    toast.error(error.message || __('Failed to create connection'))
  }
}

const handleView = async (platform) => {
  selectedPlatform.value = platform
  showViewModal.value = true
  disableSettingModalOutsideClick.value = true

  // Load accounts if platform is connected
  if (getConnectionStatus(platform.id) === 'Connected') {
    await loadAccountsForView(platform.id)
  }
}

const handleEdit = async (platform) => {
  const connection = getConnectionByPlatformId(platform.id)

  if (!connection) {
    toast.error(__('Connection not found'))
    return
  }

  try {
    let accountsData = []

    // Chỉ load account details cho Connected connections
    if (connection.connection_status === 'Connected') {
      try {
        const response = await call(
          'mbw_mira.api.external_connections.get_account_details',
          {
            connection_id: connection.connection_id || connection.name,
          }
        )

        if (response?.message?.status === 'success') {
          accountsData = response.message.data || []
        } else if (response?.status === 'success') {
          accountsData = response.data || []
        } else if (Array.isArray(response)) {
          accountsData = response
        } else if (response?.message) {
          accountsData = Array.isArray(response.message) ? response.message : []
        }
      } catch (accountError) {
        console.warn('Failed to load account details:', accountError)
      }
    }

    // Tạo enriched connection object
    const enrichedConnection = {
      ...connection,
      accounts: accountsData,
      connected_accounts: accountsData,
    }

    editingConnection.value = enrichedConnection
    selectedPlatform.value = platform

    // Reset và populate edit form
    resetForm(editFormData)
    Object.assign(editFormData, {
      tenant_name: enrichedConnection.tenant_name || '',
      hook_url: enrichedConnection.hook_url || '',
      redirect_url: enrichedConnection.redirect_url || '',
      user_email: enrichedConnection.user_email || '',
      full_name: enrichedConnection.full_name || '',
    })

    showEditModal.value = true
    disableSettingModalOutsideClick.value = true
  } catch (error) {
    console.error('Error loading connection for edit:', error)
    toast.error(__('Failed to load connection details for editing'))
  }
}

const closeEditModal = () => {
  showEditModal.value = false
  editingConnection.value = null
  selectedPlatform.value = null
  resetForm(editFormData)
  disableSettingModalOutsideClick.value = false
}

const handleConnectionUpdate = async (connectionData) => {
  try {
    const response = await call('mbw_mira.api.external_connections.update_connection', {
      connection_id: editingConnection.value.connection_id || editingConnection.value.name,
      ...connectionData,
    })

    // Handle response with login URL
    if (response?.data?.login_url) {
      const win = window.open(response.data.login_url, '_blank')
      if (!win || win.closed || typeof win.closed === 'undefined') {
        toast.warning(__('Please allow popups to complete authentication.'))
      } else {
        toast.info(__('Please complete authentication in the new window.'))
      }
    } else {
      toast.success(__('Connection updated successfully'))
    }

    closeEditModal()
    await loadConnections()
  } catch (error) {
    console.error('Error updating connection:', error)
    toast.error(error.message || __('Failed to update connection'))
  }
}

const closeViewModal = () => {
  showViewModal.value = false
  selectedPlatform.value = null
  viewModalAccounts.value = []
  loadingAccounts.value = false
  disableSettingModalOutsideClick.value = false
}

const loadAccountsForView = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId)
  if (!connection) return

  loadingAccounts.value = true
  viewModalAccounts.value = []

  try {
    const response = await call('mbw_mira.api.external_connections.get_account_details', {
      connection_id: connection.connection_id || connection.name,
    })

    let accountsData = []
    if (response?.message?.status === 'success') {
      accountsData = response.message.data || []
    } else if (response?.status === 'success') {
      accountsData = response.data || []
    } else if (Array.isArray(response)) {
      accountsData = response
    } else if (response?.message) {
      accountsData = Array.isArray(response.message) ? response.message : []
    }

    viewModalAccounts.value = accountsData
  } catch (error) {
    console.error('Error loading accounts for view:', error)
    toast.error(__('Failed to load account details'))
  } finally {
    loadingAccounts.value = false
  }
}

const handleDisconnect = async (platform) => {
  const connection = getConnectionByPlatformId(platform.id)
  if (!connection) {
    toast.error(__('Connection not found'))
    return
  }

  if (!confirm(`${__('Are you sure you want to disconnect from')} ${platform.name}?`)) {
    return
  }

  try {
    await call('mbw_mira.api.external_connections.disconnect_connection', {
      connection_id: connection.connection_id,
      reason: __('User requested disconnect'),
    })

    toast.success(__('Platform disconnected successfully'))
    await loadConnections()
  } catch (error) {
    console.error('Error disconnecting platform:', error)
    toast.error(error.message || __('Failed to disconnect platform'))
  }
}

const handleRefresh = async () => {
  isRefreshing.value = true
  try {
    await loadConnections()
    toast.success(__('Connections refreshed'))
  } catch (error) {
    toast.error(__('Failed to refresh connections'))
  } finally {
    isRefreshing.value = false
  }
}

// Watch individual modals to reset state when they close
watch(showConnectModal, (isOpen, wasOpen) => {
  // Chỉ reset khi modal đóng (từ true -> false)
  if (wasOpen && !isOpen) {
    disableSettingModalOutsideClick.value = false
  }
})

watch(showEditModal, (isOpen, wasOpen) => {
  if (wasOpen && !isOpen) {
    disableSettingModalOutsideClick.value = false
  }
})

watch(showViewModal, (isOpen, wasOpen) => {
  if (wasOpen && !isOpen) {
    disableSettingModalOutsideClick.value = false
  }
})

// Lifecycle
onMounted(async () => {
  await loadConnections()
})
</script>
