<template>
  <div class="external-connections-container">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">{{ __("External Connections") }}</h1>
        <p class="text-sm text-gray-600 mt-1">
          {{ __("Manage your connections to external platforms") }}
        </p>
      </div>
      <Button @click="refreshConnections" :loading="isRefreshing" variant="outline">
        <template #prefix>
          <FeatherIcon name="refresh-cw" class="w-4 h-4" />
        </template>
        {{ __("Refresh") }}
      </Button>
    </div>

    <!-- Connection Types Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-2 gap-6">
      <div
        v-for="(typeData, typeKey) in CONNECTION_TYPES"
        :key="typeKey"
        class="bg-white rounded-lg border border-gray-200 shadow-sm"
      >
        <!-- Type Header -->
        <div class="p-4 border-b border-gray-100">
          <div class="flex items-center gap-3">
            <div
              class="w-10 h-10 rounded-lg flex items-center justify-center"
              :class="typeData.color"
            >
              <FeatherIcon :name="typeData.icon" class="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 class="font-semibold text-gray-900">{{ __(typeData.title) }}</h3>
              <p class="text-xs text-gray-500">
                {{ typeData.platforms.length }} {{ __("platforms") }}
              </p>
            </div>
          </div>
        </div>

        <!-- Platforms List -->
        <div class="p-4 space-y-3">
          <div
            v-for="platform in typeData.platforms"
            :key="platform.id"
            class="border rounded-lg p-3 transition-all duration-200 hover:shadow-md"
            :class="platform.color"
          >
            <!-- Platform Header -->
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-3">
                <span class="text-lg">{{ platform.icon }}</span>
                <div>
                  <h4 class="font-medium text-gray-900">{{ platform.name }}</h4>
                  <p class="text-xs text-gray-500">{{ __(platform.description) }}</p>
                </div>
              </div>

              <!-- Connection Status Badge -->
              <Badge :variant="getConnectionBadgeVariant(platform.id)" size="sm">
                {{ getConnectionStatusText(platform.id) }}
              </Badge>
            </div>

            <!-- Connected Accounts -->
            <div
              v-if="getConnectedAccountsForPlatform(platform.id).length > 0"
              class="mb-3"
            >
              <div class="text-xs text-gray-600 mb-1">
                {{ __("Connected Accounts:") }}
              </div>
              <div class="space-y-1">
                <div
                  v-for="account in getConnectedAccountsForPlatform(platform.id)"
                  :key="account.external_account_id"
                  class="flex items-center gap-2 text-xs"
                >
                  <div
                    class="w-4 h-4 rounded-full bg-green-100 flex items-center justify-center"
                  >
                    <FeatherIcon name="check" class="w-2 h-2 text-green-600" />
                  </div>
                  <span class="text-gray-700">{{ account.account_name }}</span>
                  <Badge v-if="account.is_primary" variant="subtle" size="xs">{{
                    __("Primary")
                  }}</Badge>
                </div>
              </div>
            </div>

            <!-- Platform Features -->
            <div class="mb-3">
              <div class="flex flex-wrap gap-1">
                <Badge
                  v-for="feature in platform.features"
                  :key="feature"
                  variant="outline"
                  size="xs"
                >
                  {{ __(feature) }}
                </Badge>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <!-- Connect Button - Chỉ khi chưa có kết nối -->
              <Button
                v-if="!hasConnection(platform.id)"
                @click="initiatePlatformConnection(platform)"
                variant="solid"
                size="sm"
                :loading="connectingPlatforms.includes(platform.id)"
              >
                <template #prefix>
                  <FeatherIcon name="link" class="w-3 h-3" />
                </template>
                {{ __("Connect") }}
              </Button>

              <!-- Disconnect Button - Cho Connected và Pending -->
              <Button
                v-if="canManageConnection(platform.id)"
                @click="confirmAndDisconnect(platform.id)"
                variant="outline"
                size="sm"
                theme="red"
                :loading="disconnectingPlatforms.includes(platform.id)"
                :disabled="disconnectingPlatforms.includes(platform.id)"
              >
                <template #prefix>
                  <FeatherIcon name="unlink" class="w-3 h-3" />
                </template>
                {{ __("Disconnect") }}
              </Button>

              <!-- Edit Button - Cho Connected và Pending -->
              <Button
                v-if="canManageConnection(platform.id)"
                @click="editConnectionForPlatform(platform.id)"
                variant="ghost"
                size="sm"
                :disabled="
                  connectingPlatforms.includes(platform.id) ||
                  disconnectingPlatforms.includes(platform.id)
                "
              >
                <template #prefix>
                  <FeatherIcon name="edit-2" class="w-3 h-3" />
                </template>
                {{ __("Edit") }}
              </Button>

              <!-- Sync Button - Chỉ cho Connected -->
              <Button
                v-if="isConnectionConnected(platform.id)"
                @click="syncAccounts(platform.id)"
                variant="outline"
                size="sm"
                :loading="syncingPlatforms.includes(platform.id)"
                :disabled="
                  syncingPlatforms.includes(platform.id) ||
                  disconnectingPlatforms.includes(platform.id)
                "
              >
                <template #prefix>
                  <FeatherIcon name="refresh-cw" class="w-3 h-3" />
                </template>
                {{ __("Sync") }}
              </Button>

              <!-- Settings Button - Chỉ cho Connected -->
              <Button
                v-if="isConnectionConnected(platform.id)"
                @click="openAccountSettingsForPlatform(platform.id)"
                variant="ghost"
                size="sm"
              >
                <template #prefix>
                  <FeatherIcon name="settings" class="w-3 h-3" />
                </template>
                {{ __("Settings") }}
              </Button>

              <!-- Retry Button - Cho Failed/Disconnected -->
              <Button
                v-if="isConnectionFailed(platform.id)"
                @click="retryConnection(platform.id)"
                variant="outline"
                size="sm"
                theme="orange"
                :loading="connectingPlatforms.includes(platform.id)"
              >
                <template #prefix>
                  <FeatherIcon name="rotate-ccw" class="w-3 h-3" />
                </template>
                {{ __("Retry") }}
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
              <p class="text-sm text-gray-600">{{ __(selectedPlatform.description) }}</p>
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
        <div v-if="editingConnection && selectedPlatform" class="space-y-4">
          <!-- Platform Info -->
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
            <span class="text-2xl">{{ selectedPlatform.icon }}</span>
            <div>
              <h3 class="font-semibold text-gray-900">{{ selectedPlatform.name }}</h3>
              <p class="text-sm text-gray-600">{{ __("Edit connection settings") }}</p>
              <Badge
                :variant="getConnectionBadgeVariant(selectedPlatform.id)"
                size="sm"
                class="mt-1"
              >
                {{ getConnectionStatusText(selectedPlatform.id) }}
              </Badge>
            </div>
          </div>

          <!-- Status-specific Messages -->
          <div
            v-if="getConnectionStatus(selectedPlatform.id) === 'Pending'"
            class="bg-yellow-50 border border-yellow-200 rounded-lg p-3"
          >
            <div class="flex items-center gap-2">
              <FeatherIcon name="clock" class="w-4 h-4 text-yellow-600" />
              <span class="text-sm text-yellow-800">
                {{
                  __(
                    "This connection is pending authentication. You can edit settings or disconnect if needed."
                  )
                }}
              </span>
            </div>
          </div>

          <div
            v-else-if="getConnectionStatus(selectedPlatform.id) === 'Failed'"
            class="bg-red-50 border border-red-200 rounded-lg p-3"
          >
            <div class="flex items-center gap-2">
              <FeatherIcon name="alert-triangle" class="w-4 h-4 text-red-600" />
              <span class="text-sm text-red-800">
                {{
                  __(
                    "This connection failed to authenticate. You can edit settings and try again."
                  )
                }}
              </span>
            </div>
          </div>

          <div
            v-else-if="getConnectionStatus(selectedPlatform.id) === 'Disconnected'"
            class="bg-gray-50 border border-gray-200 rounded-lg p-3"
          >
            <div class="flex items-center gap-2">
              <FeatherIcon name="unlink" class="w-4 h-4 text-gray-600" />
              <span class="text-sm text-gray-800">
                {{
                  __(
                    "This connection has been disconnected. You can edit settings to reconnect."
                  )
                }}
              </span>
            </div>
          </div>

          <!-- Connected Accounts Section - Enhanced -->
          <div
            v-if="editingConnection.accounts && editingConnection.accounts.length > 0"
            class="bg-blue-50 rounded-lg p-4"
          >
            <h4 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
              <FeatherIcon name="users" class="w-4 h-4" />
              {{ __("Currently Connected Accounts") }}
            </h4>
            <div class="space-y-2">
              <div
                v-for="account in editingConnection.accounts"
                :key="account.external_account_id"
                class="flex items-center justify-between p-2 bg-white rounded border"
              >
                <div class="flex items-center gap-2">
                  <div
                    class="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center"
                  >
                    <FeatherIcon name="check" class="w-3 h-3 text-green-600" />
                  </div>
                  <div>
                    <span class="text-sm font-medium text-gray-900">{{
                      account.account_name
                    }}</span>
                    <div class="text-xs text-gray-500">{{ account.account_type }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-1">
                  <Badge v-if="account.is_primary" variant="subtle" size="xs">{{
                    __("Primary")
                  }}</Badge>
                  <Badge :variant="account.is_active ? 'success' : 'gray'" size="xs">
                    {{ account.is_active ? __("Active") : __("Inactive") }}
                  </Badge>
                </div>
              </div>
            </div>
          </div>

          <!-- No Accounts Message for Pending/Failed -->
          <div
            v-else-if="getConnectionStatus(selectedPlatform.id) === 'Pending'"
            class="bg-yellow-50 rounded-lg p-4"
          >
            <div class="flex items-center gap-2">
              <FeatherIcon name="clock" class="w-4 h-4 text-yellow-600" />
              <span class="text-sm text-yellow-800">
                {{
                  __(
                    "No accounts connected yet. Complete authentication to see connected accounts."
                  )
                }}
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

    <!-- Account Settings Modal -->
    <Dialog
      v-if="showAccountModal"
      v-model="showAccountModal"
      :options="{ title: __('Account Settings'), size: '2xl' }"
    >
      <template #body-content>
        <div v-if="selectedConnection" class="space-y-6">
          <!-- Connection Info -->
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="font-semibold text-gray-900 mb-2">
              {{ __("Connection Information") }}
            </h3>
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span class="text-gray-600">{{ __("Platform:") }}</span>
                <span class="ml-2 font-medium">{{
                  selectedConnection.platform_type
                }}</span>
              </div>
              <div>
                <span class="text-gray-600">{{ __("Status:") }}</span>
                <Badge
                  :variant="
                    selectedConnection.connection_status === 'Connected'
                      ? 'success'
                      : getStatusVariant(selectedConnection.connection_status)
                  "
                  size="sm"
                  class="ml-2"
                >
                  {{ __(selectedConnection.connection_status) || __("Unknown") }}
                </Badge>
              </div>
              <div>
                <span class="text-gray-600">{{ __("Created:") }}</span>
                <span class="ml-2">{{ formatDate(selectedConnection.creation) }}</span>
              </div>
              <div>
                <span class="text-gray-600">{{ __("Last Sync:") }}</span>
                <span class="ml-2">{{
                  formatDate(selectedConnection.last_sync_time)
                }}</span>
              </div>
            </div>
          </div>

          <!-- Connected Accounts -->
          <div
            v-if="selectedConnection.accounts && selectedConnection.accounts.length > 0"
          >
            <h3 class="font-semibold text-gray-900 mb-3">
              {{ __("Connected Accounts") }}
            </h3>
            <div class="space-y-2">
              <div
                v-for="account in selectedConnection.accounts"
                :key="account.external_account_id"
                class="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <div
                    class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center"
                  >
                    <FeatherIcon name="user" class="w-4 h-4 text-gray-600" />
                  </div>
                  <div>
                    <div class="font-medium text-gray-900">
                      {{ account.account_name }}
                    </div>
                    <div class="text-xs text-gray-500">
                      {{ account.account_type }} • {{ account.external_account_id }}
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <Badge v-if="account.is_primary" variant="success" size="sm">{{
                    __("Primary")
                  }}</Badge>
                  <Badge :variant="account.is_active ? 'success' : 'gray'" size="sm">
                    {{ account.is_active ? __("Active") : __("Inactive") }}
                  </Badge>
                </div>
              </div>
            </div>
          </div>

          <!-- No Accounts Message -->
          <div v-else class="text-center py-6">
            <FeatherIcon name="users" class="w-12 h-12 text-gray-400 mx-auto mb-2" />
            <p class="text-gray-500">{{ __("No accounts connected") }}</p>
          </div>

          <!-- Statistics -->
          <div
            v-if="selectedConnection.accounts && selectedConnection.accounts.length > 0"
          >
            <h3 class="font-semibold text-gray-900 mb-3">
              {{ __("Connection Statistics") }}
            </h3>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center p-3 bg-blue-50 rounded-lg">
                <div class="text-2xl font-bold text-blue-600">
                  {{ selectedConnection.total_api_calls || 0 }}
                </div>
                <div class="text-xs text-blue-600">{{ __("Total API Calls") }}</div>
              </div>
              <div class="text-center p-3 bg-green-50 rounded-lg">
                <div class="text-2xl font-bold text-green-600">
                  {{ selectedConnection.successful_calls || 0 }}
                </div>
                <div class="text-xs text-green-600">{{ __("Successful Calls") }}</div>
              </div>
              <div class="text-center p-3 bg-red-50 rounded-lg">
                <div class="text-2xl font-bold text-red-600">
                  {{ selectedConnection.failed_calls || 0 }}
                </div>
                <div class="text-xs text-red-600">{{ __("Failed Calls") }}</div>
              </div>
            </div>

            <!-- Success Rate -->
            <div class="mt-3 p-3 bg-gray-50 rounded-lg">
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">{{ __("Success Rate:") }}</span>
                <span
                  class="font-medium"
                  :class="getSuccessRateColor(selectedConnection)"
                >
                  {{ calculateSuccessRate(selectedConnection) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex items-center gap-2">
          <!-- Refresh Connection Button -->
          <Button
            v-if="selectedConnection.connection_status === 'Connected'"
            @click="refreshSingleConnection(selectedConnection)"
            variant="outline"
            size="sm"
            :loading="isRefreshingSingle"
          >
            <template #prefix>
              <FeatherIcon name="refresh-cw" class="w-3 h-3" />
            </template>
            {{ __("Refresh") }}
          </Button>

          <Button @click="closeAccountModal" variant="ghost">
            {{ __("Close") }}
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
  <ExtenalSharing/>
</template>

<script setup>
import { ref, reactive, onMounted, computed, shallowRef, nextTick } from "vue";
// import { useToast } from '@/composables/useToast'
import { Button, Dialog, FormControl, Badge, FeatherIcon, call } from "frappe-ui";
import { showToast } from "@/utils";
import { ToastContainer } from "@/components/shared";
import FacebookConnectionForm from "@/components/Connectors/FacebookConnectionForm.vue";
import ZaloConnectionForm from "@/components/Connectors/ZaloConnectionForm.vue";
import CalcomConnectionForm from "@/components/Connectors/CalcomConnectionForm.vue";
import TopcvConnectionForm from "@/components/Connectors/TopcvConnectionForm.vue";
import useToast from "@/composables/useToast";
import ExtenalSharing from "@/components/Connectors/ExtenalSharing.vue";
// Simple notifier to standardize icon usage
const {
  success: toastSuccess,
  error: toastError,
  warning: toastWarning,
  info: toastInfo,
} = useToast();
const notify = (type, title, text) => {
  if (type === "success") return toastSuccess(`${title}: ${text}`);
  if (type === "error") return toastError(`${title}: ${text}`);
  if (type === "warning") return toastWarning(`${title}: ${text}`);
  return toastInfo(`${title}: ${text}`);
};

// Master data cho các nhóm connect type và platform
const CONNECTION_TYPES = {
  social_media: {
    title: __("Social Media"),
    icon: "users",
    color: "bg-blue-500",
    platforms: [
      {
        id: "facebook",
        name: "Facebook",
        icon: "📘",
        description: __("Connect Facebook Pages and Personal Profiles"),
        color: "border-blue-500",
        features: [
          __("Pages Management"),
          __("Posts Publishing"),
          __("Comments Monitoring"),
          __("Insights Analytics"),
        ],
      },
    ],
  },
  messaging: {
    title: __("Messaging Platforms"),
    icon: "message-circle",
    color: "bg-green-500",
    platforms: [
      {
        id: "zalo",
        name: "Zalo",
        icon: "💬",
        description: __("Connect Zalo Official Accounts"),
        color: "border-blue-400",
        features: [
          __("Message Broadcasting"),
          __("Customer Chat"),
          __("Template Messages"),
          __("User Management"),
        ],
      },
    ],
  },
  calendar: {
    title: __("Calendar Integration"),
    icon: "calendar",
    color: "bg-orange-500",
    platforms: [
      {
        id: "cal_com",
        name: "Cal.com",
        icon: "📅",
        description: __("Connect Cal.com Scheduling"),
        color: "border-orange-500",
        features: [
          __("Event Scheduling"),
          __("Calendar Sync"),
          __("Booking Management"),
          __("Availability Settings"),
        ],
      },
    ],
  },
  job_board: {
    title: __("Job Board"),
    icon: "briefcase",
    color: "bg-purple-500",
    platforms: [
      {
        id: "topcv",
        name: "TopCV",
        icon: "💼",
        description: __("Connect TopCV Job Portal"),
        color: "border-purple-500",
        features: [
          __("Job Posting"),
          __("Candidate Management"),
          __("Application Tracking"),
          __("Resume Database Access"),
        ],
      },
    ],
  },
};

// Platform form components mapping
const platformFormComponents = shallowRef({
  facebook: FacebookConnectionForm,
  zalo: ZaloConnectionForm,
  cal_com: CalcomConnectionForm,
  topcv: TopcvConnectionForm,
});

// State
const connections = ref([]);
const isRefreshing = ref(false);
const showConnectModal = ref(false);
const showAccountModal = ref(false);
const showEditModal = ref(false);

const selectedPlatform = shallowRef(null);
const selectedConnection = shallowRef(null);
const editingConnection = shallowRef(null);

const connectingPlatforms = ref([]);
const disconnectingPlatforms = ref([]);
const syncingPlatforms = ref([]);
const isConnecting = ref(false);
const isUpdating = ref(false);
const isRefreshingSingle = ref(false);

// Form data
const connectForm = reactive({
  tenant_name: "",
  hook_url: "",
  redirect_url: "",
});

const editFormData = reactive({
  tenant_name: "",
  hook_url: "",
  redirect_url: "",
});

const emit = defineEmits(["connection-updated", "job-shared"]);

// Computed values
const currentFormComponent = computed(() => {
  if (!selectedPlatform.value?.id) return null;
  return (
    platformFormComponents.value[selectedPlatform.value.id] || FacebookConnectionForm
  );
});

const currentConnectionForm = computed({
  get() {
    return { ...connectForm };
  },
  set(value) {
    Object.assign(connectForm, value);
  },
});

const currentEditForm = computed({
  get() {
    return { ...editFormData };
  },
  set(value) {
    Object.assign(editFormData, value);
  },
});

// Helper methods để kiểm tra trạng thái connection
const getConnectionByPlatformId = (platformId) => {
  if (!Array.isArray(connections.value)) return null;
  return connections.value.find(
    (conn) => conn.platform_type.toLowerCase() === platformId
  );
};

const getConnectionStatus = (platformId) => {
  const connection = getConnectionByPlatformId(platformId);
  return connection?.connection_status || null;
};

// Kiểm tra có connection hay không (bất kỳ trạng thái nào)
const hasConnection = (platformId) => {
  return getConnectionByPlatformId(platformId);
};

// Kiểm tra connection đang Connected
const isConnectionConnected = (platformId) => {
  const status = getConnectionStatus(platformId);
  return status === "Connected";
};

// Kiểm tra connection đang Pending
const isConnectionPending = (platformId) => {
  const status = getConnectionStatus(platformId);
  return status === "Pending";
};

// Kiểm tra connection Failed hoặc Disconnected
const isConnectionFailed = (platformId) => {
  const status = getConnectionStatus(platformId);
  return status === "Failed" || status === "Disconnected";
};

// Kiểm tra có thể manage connection (edit/disconnect) - Connected hoặc Pending
const canManageConnection = (platformId) => {
  const status = getConnectionStatus(platformId);
  return status !== null;
};

const getConnectedAccountsForPlatform = (platformId) => {
  const connection = getConnectionByPlatformId(platformId);

  // Chỉ hiển thị accounts khi Connected
  if (!connection || connection.connection_status !== "Connected") {
    return [];
  }

  return connection?.accounts || connection?.connected_accounts || [];
};

const getConnectionBadgeVariant = (platformId) => {
  const status = getConnectionStatus(platformId);

  switch (status) {
    case "Connected":
      return "success";
    case "Pending":
      return "warning";
    case "Failed":
    case "Disconnected":
      return "red";
    default:
      return "subtle";
  }
};

const getConnectionStatusText = (platformId) => {
  const status = getConnectionStatus(platformId);
  return status ? __(status) : __("Not Connected");
};

const getStatusVariant = (status) => {
  switch (status) {
    case "Connected":
      return "success";
    case "Pending":
      return "warning";
    case "Failed":
    case "Disconnected":
      return "red";
    default:
      return "gray";
  }
};

const getModalTitle = (type) => {
  if (!selectedPlatform.value) return __("Platform Connection");

  if (type === "connect") {
    return `${__("Connect to")} ${selectedPlatform.value.name}`;
  } else if (type === "edit") {
    const status = getConnectionStatus(selectedPlatform.value.id);
    return `${__("Edit")} ${selectedPlatform.value.name} ${__("Connection")}${
      status ? ` (${__(status)})` : ""
    }`;
  }

  return __("Platform Connection");
};

// Utility methods
const resetForm = (formObject) => {
  Object.keys(formObject).forEach((key) => {
    formObject[key] = "";
  });
};

const clearLoadingState = (platformId, loadingArray) => {
  const index = loadingArray.findIndex((id) => id === platformId);
  if (index > -1) {
    loadingArray.splice(index, 1);
  }
};

const validateConnectionData = (connectionData) => {
  const required = [];
  const missing = required.filter((field) => !connectionData[field]?.trim());

  if (missing.length > 0) {
    throw new Error(`${__("Missing required fields:")} ${missing.join(", ")}`);
  }

  return true;
};

const handleApiResponse = (
  response,
  successMessage = __("Operation completed successfully")
) => {
  if (response?.data?.login_url) {
    const win = window.open(response.data.login_url, "_blank");
    if (!win || win.closed || typeof win.closed === "undefined") {
      notify(
        "warning",
        __("Popup Blocked"),
        __("Please allow popups to complete authentication.")
      );
    } else {
      notify(
        "info",
        __("Authentication"),
        __("Please complete authentication in the new window.")
      );
    }
    return {
      success: true,
      message: __("Please complete authentication in the new window."),
      requiresAuth: true,
    };
  } else if (response?.status === "success") {
    return {
      success: true,
      message: successMessage,
      requiresAuth: false,
    };
  } else {
    throw new Error(response?.message || __("Operation failed"));
  }
};

const calculateSuccessRate = (connection) => {
  const total = connection.total_api_calls || 0;
  const successful = connection.successful_calls || 0;

  if (total === 0) return 0;
  return Math.round((successful / total) * 100);
};

const getSuccessRateColor = (connection) => {
  const rate = calculateSuccessRate(connection);
  if (rate >= 95) return "text-green-600";
  if (rate >= 80) return "text-yellow-600";
  return "text-red-600";
};

const formatDate = (dateString) => {
  if (!dateString) return __("N/A");
  try {
    return new Date(dateString).toLocaleDateString("vi-VN", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (error) {
    return __("Invalid Date");
  }
};

// Modal control methods
const closeConnectModal = () => {
  showConnectModal.value = false;
  selectedPlatform.value = null;
  resetForm(connectForm);
};

const closeEditModal = () => {
  showEditModal.value = false;
  editingConnection.value = null;
  selectedPlatform.value = null;
  resetForm(editFormData);
};

const closeAccountModal = () => {
  showAccountModal.value = false;
  selectedConnection.value = null;
};

// Platform action methods
const initiatePlatformConnection = (platform) => {
  selectedPlatform.value = { ...platform };
  resetForm(connectForm);
  showConnectModal.value = true;
};

const editConnectionForPlatform = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);

  if (!connection) {
    notify("error", __("Error"), __("Connection not found"));
    return;
  }

  try {
    let accountsData = [];

    // Chỉ load account details cho Connected connections
    if (connection.connection_status === "Connected") {
      try {
        const response = await call(
          "mbw_mira.api.external_connections.get_account_details",
          {
            connection_id: connection.connection_id || connection.name,
          }
        );

        if (response?.message?.status === "success") {
          accountsData = response.message.data || [];
        } else if (response?.status === "success") {
          accountsData = response.data || [];
        } else if (Array.isArray(response)) {
          accountsData = response;
        } else if (response?.message) {
          accountsData = Array.isArray(response.message) ? response.message : [];
        }
      } catch (accountError) {
        console.warn(
          __("Failed to load account details, proceeding without accounts:"),
          accountError
        );
      }
    }

    // Tạo enriched connection object
    const enrichedConnection = {
      ...connection,
      accounts: accountsData,
      connected_accounts: accountsData,
    };

    editingConnection.value = enrichedConnection;
    selectedPlatform.value = Object.values(CONNECTION_TYPES)
      .flatMap((type) => type.platforms)
      .find((platform) => platform.id === platformId);

    // Reset và populate edit form
    resetForm(editFormData);
    Object.assign(editFormData, {
      tenant_name: enrichedConnection.tenant_name || "",
      hook_url: enrichedConnection.hook_url || "",
      redirect_url: enrichedConnection.redirect_url || "",
    });

    showEditModal.value = true;
  } catch (error) {
    console.error("Error loading connection for edit:", error);
    notify("error", __("Error"), __("Failed to load connection details for editing"));
  }
};

const openAccountSettingsForPlatform = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);

  if (!connection) return;

  // Chỉ cho phép account settings cho Connected connections
  if (connection.connection_status !== "Connected") {
    notify(
      "warning",
      __("Cannot Access Settings"),
      __("Account settings are only available for connected platforms")
    );
    return;
  }

  try {
    const response = await call("mbw_mira.api.external_connections.get_account_details", {
      connection_id: connection.connection_id || connection.name,
    });

    let accountsData = [];

    if (response?.message?.status === "success") {
      accountsData = response.message.data || [];
    } else if (response?.status === "success") {
      accountsData = response.data || [];
    } else if (Array.isArray(response)) {
      accountsData = response;
    } else if (response?.message) {
      accountsData = Array.isArray(response.message) ? response.message : [];
    }

    selectedConnection.value = {
      ...connection,
      accounts: accountsData,
    };

    showAccountModal.value = true;
  } catch (error) {
    console.error("Error loading account details:", error);
    notify("error", __("Error"), __("Failed to load account details"));
  }
};

// Enhanced connection operations
const createConnection = async (connectionData) => {
  try {
    validateConnectionData(connectionData);

    const response = await call("mbw_mira.api.external_connections.create_connection", {
      platform_type: selectedPlatform.value.name,
      //tenant_name: connectionData.tenant_name,
      hook_url: connectionData.hook_url,
      redirect_url: connectionData.redirect_url,
      user_email: connectionData.user_email,
      full_name: connectionData.full_name,
    });

    const result = handleApiResponse(response, __("Connection created successfully"));

    notify("success", __("Success"), result.message);

    await refreshConnections();
    emit("connection-updated", {
      action: "create",
      platform: selectedPlatform.value.name,
      requiresAuth: result.requiresAuth,
    });

    return result;
  } catch (error) {
    console.error("Error creating connection:", error);
    notify("error", __("Error"), error.message || __("Failed to create connection"));
    throw error;
  }
};

const updateConnection = async (connectionData) => {
  try {
    validateConnectionData(connectionData);

    const response = await call("mbw_mira.api.external_connections.update_connection", {
      connection_id:
        editingConnection.value.connection_id || editingConnection.value.name,
      tenant_name: connectionData.tenant_name,
      hook_url: connectionData.hook_url,
      redirect_url: connectionData.redirect_url,
      user_email: connectionData.user_email,
      full_name: connectionData.full_name,
    });

    const result = handleApiResponse(response, __("Connection updated successfully"));

    notify("success", __("Success"), result.message);

    await refreshConnections();
    emit("connection-updated", {
      action: "update",
      platform: selectedPlatform.value?.name,
      requiresAuth: result.requiresAuth,
    });

    return result;
  } catch (error) {
    console.error("Error updating connection:", error);
    notify("error", __("Error"), error.message || __("Failed to update connection"));
    throw error;
  }
};

const confirmAndDisconnect = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);
  if (!connection) return;

  const platformName =
    Object.values(CONNECTION_TYPES)
      .flatMap((type) => type.platforms)
      .find((platform) => platform.id === platformId)?.name || __("Platform");

  if (
    !confirm(
      `${__("Are you sure you want to disconnect from")} ${platformName}? ${__(
        "This action cannot be undone."
      )}`
    )
  ) {
    return;
  }

  await disconnectPlatform(platformId);
};

const refreshSingleConnection = async (connection) => {
  if (!connection) return;

  isRefreshingSingle.value = true;

  try {
    const response = await call("mbw_mira.api.external_connections.get_account_details", {
      connection_id: connection.connection_id || connection.name,
      force_refresh: true,
    });

    let accountsData = [];

    if (response?.message?.status === "success") {
      accountsData = response.message.data || [];
    } else if (response?.status === "success") {
      accountsData = response.data || [];
    } else if (Array.isArray(response)) {
      accountsData = response;
    }

    // Update selectedConnection
    selectedConnection.value = {
      ...selectedConnection.value,
      accounts: accountsData,
      last_sync_time: new Date().toISOString(),
    };

    notify("success", __("Success"), __("Connection refreshed successfully"));

    // Also refresh the main connections list
    await refreshConnections();
  } catch (error) {
    console.error("Error refreshing single connection:", error);
    notify("error", __("Error"), error.message || __("Failed to refresh connection"));
  } finally {
    isRefreshingSingle.value = false;
  }
};

// Main methods
const refreshConnections = async () => {
  isRefreshing.value = true;
  try {
    const requestParams = {
      tenant_name: connectForm.tenant_name || "",
    };

    const response = await call(
      "mbw_mira.api.external_connections.get_connection_info",
      requestParams
    );

    let connectionsData = [];

    if (response && response.status === "success" && response.data) {
      connectionsData = Array.isArray(response.data) ? response.data : [];
    } else if (response && response.message) {
      connectionsData = Array.isArray(response.message) ? response.message : [];
    } else if (Array.isArray(response)) {
      connectionsData = response;
    } else {
      console.warn(__("Unexpected response format:"), response);
      connectionsData = [];
    }

    await nextTick();
    connections.value = connectionsData;
  } catch (error) {
    console.error("Error refreshing connections:", error);
    connections.value = [];
    notify(
      "error",
      __("Error"),
      `${__("Failed to refresh connections:")} ${error.message || error}`
    );
  } finally {
    isRefreshing.value = false;
  }
};

const handleConnectionSubmit = async (connectionData) => {
  if (!selectedPlatform.value) return;

  isConnecting.value = true;
  connectingPlatforms.value.push(selectedPlatform.value.id);

  try {
    await createConnection(connectionData);
    closeConnectModal();
  } catch (error) {
    // Error already handled in createConnection
  } finally {
    isConnecting.value = false;
    clearLoadingState(selectedPlatform.value?.id, connectingPlatforms.value);
  }
};

const handleConnectionUpdate = async (connectionData) => {
  if (!editingConnection.value) return;

  isUpdating.value = true;

  try {
    await updateConnection(connectionData);
    closeEditModal();
  } catch (error) {
    // Error already handled in updateConnection
  } finally {
    isUpdating.value = false;
  }
};

const disconnectPlatform = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);

  if (!connection) {
    notify("error", __("Error"), __("Connection not found"));
    return;
  }

  // Kiểm tra có thể disconnect không
  if (!canManageConnection(platformId)) {
    notify(
      "warning",
      __("Cannot Disconnect"),
      __("This connection cannot be disconnected in its current state")
    );
    return;
  }

  disconnectingPlatforms.value.push(platformId);

  try {
    const response = await call(
      "mbw_mira.api.external_connections.disconnect_connection",
      {
        connection_id: connection.connection_id,
        reason: __("User requested disconnect"),
      }
    );

    const result = handleApiResponse(response, __("Platform disconnected successfully"));

    notify("success", __("Success"), result.message);

    await refreshConnections();

    emit("connection-updated", {
      action: "disconnect",
      platform: connection.platform_type,
    });
  } catch (error) {
    console.error("Error disconnecting platform:", error);
    notify("error", __("Error"), error.message || __("Failed to disconnect platform"));
  } finally {
    clearLoadingState(platformId, disconnectingPlatforms.value);
  }
};

const syncAccounts = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);

  if (!connection) {
    notify("error", __("Error"), __("Connection not found"));
    return;
  }

  // Chỉ cho phép sync cho Connected connections
  if (connection.connection_status !== "Connected") {
    notify(
      "warning",
      __("Cannot Sync"),
      __("Account sync is only available for connected platforms")
    );
    return;
  }

  syncingPlatforms.value.push(platformId);

  try {
    const response = await call("mbw_mira.api.external_connections.sync_accounts", {
      connection_id: connection.connection_id,
      force_sync: true,
    });

    const result = handleApiResponse(response, __("Accounts synced successfully"));

    notify("success", __("Success"), result.message);

    await refreshConnections();
  } catch (error) {
    console.error("Error syncing accounts:", error);
    notify("error", __("Error"), error.message || __("Failed to sync accounts"));
  } finally {
    clearLoadingState(platformId, syncingPlatforms.value);
  }
};

const retryConnection = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);

  if (!connection) {
    notify("error", __("Error"), __("Connection not found"));
    return;
  }

  if (!isConnectionFailed(platformId)) {
    notify(
      "warning",
      __("Cannot Retry"),
      __("Connection retry is only available for failed connections")
    );
    return;
  }

  connectingPlatforms.value.push(platformId);

  try {
    const response = await call("mbw_mira.api.external_connections.retry_connection", {
      connection_id: connection.connection_id || connection.name,
    });

    const result = handleApiResponse(
      response,
      __("Connection retry initiated successfully")
    );

    notify(
      "success",
      result.requiresAuth ? __("Retry Initiated") : __("Success"),
      result.message
    );

    await refreshConnections();

    emit("connection-updated", {
      action: "retry",
      platform: connection.platform_type,
    });
  } catch (error) {
    console.error("Error retrying connection:", error);
    notify("error", __("Error"), error.message || __("Failed to retry connection"));
  } finally {
    clearLoadingState(platformId, connectingPlatforms.value);
  }
};

// Enhanced error recovery
const handleConnectionError = async (error, platformId, operation) => {
  console.error(`Error in ${operation} for platform ${platformId}:`, error);

  // Check if it's an authentication error
  if (error.message && error.message.includes("authentication")) {
    notify(
      "warning",
      __("Authentication Required"),
      __("Your authentication has expired. Please reconnect to continue.")
    );

    // Optionally trigger reconnect flow
    const platform = Object.values(CONNECTION_TYPES)
      .flatMap((type) => type.platforms)
      .find((p) => p.id === platformId);

    if (platform && confirm(__("Would you like to reconnect now?"))) {
      initiatePlatformConnection(platform);
    }
  } else if (error.message && error.message.includes("network")) {
    notify(
      "error",
      __("Network Error"),
      __("Please check your internet connection and try again.")
    );
  } else {
    notify("error", __("Error"), error.message || `${__("Failed to")} ${operation}`);
  }
};

// Lifecycle
onMounted(async () => {
  await refreshConnections();

  // Auto-refresh every 30 seconds for pending connections
  setInterval(async () => {
    const hasPendingConnections = connections.value.some(
      (conn) => conn.connection_status === "Pending"
    );

    if (hasPendingConnections && !isRefreshing.value) {
      console.log(__("Auto-refreshing due to pending connections"));
      await refreshConnections();
    }
  }, 30000);
});
</script>

<style scoped>
.external-connections-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Custom scrollbar for modal content */
::deep(.dialog-body) {
  max-height: 70vh;
  overflow-y: auto;
}

/* Hover effects */
.transition-all {
  transition: all 0.2s ease-in-out;
}

/* Grid responsive adjustments */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: 1fr;
  }
}

/* Loading states */
.loading-overlay {
  position: relative;
}

.loading-overlay::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.7);
  border-radius: inherit;
  pointer-events: none;
}

/* Status-specific styling */
.status-pending {
  border-left: 4px solid #f59e0b;
}

.status-connected {
  border-left: 4px solid #10b981;
}

.status-failed {
  border-left: 4px solid #ef4444;
}

.status-disconnected {
  border-left: 4px solid #6b7280;
}
</style>
