<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Page Header -->
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <!-- <template #right-header>
        <Button variant="solid" theme="gray" @click="handleCreate" :loading="loading" class="">
          <template #prefix>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6">
              </path>
            </svg>
          </template>
          {{ __('Create New') }}
        </Button>
      </template> -->
    </LayoutHeader>

    <!-- Filters & Controls -->
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <!-- Search & Filters -->
          <div class="flex items-center space-x-4 flex-1">
            <!-- Search -->
            <TextInput
              v-model="searchText"
              type="text"
              :placeholder="__('Search platforms...')"
              @input="handleSearchChange"
              class="flex-1 max-w-md"
            >
              <template #prefix>
                <FeatherIcon name="search" class="w-4 h-4" />
              </template>
            </TextInput>

            <!-- Type Filter -->
            <FormControl
              type="select"
              v-model="typeFilter"
              @change="handleFilterChange"
              :options="[
                { label: __('All Types'), value: '' },
                { label: __('Social Media'), value: 'social_media' },
                { label: __('Messaging'), value: 'messaging' },
                { label: __('Job Board'), value: 'job_board' }
              ]"
              class="w-40"
            />

            <!-- Status Filter -->
            <FormControl
              type="select"
              v-model="statusFilter"
              @change="handleFilterChange"
              :options="[
                { label: __('All'), value: '' },
                { label: __('Connected'), value: 'connected' },
                { label: __('Not Connected'), value: 'not_connected' },
                { label: __('Pending'), value: 'pending' },
                { label: __('Failed'), value: 'failed' }
              ]"
              class="w-32"
            />
      </div>

          <!-- Action Buttons -->
          <div class="flex items-center space-x-3">
            <!-- Refresh Button -->
            <Button
              @click="handleRefresh"
              :loading="isRefreshing"
              variant="outline"
              theme="gray"
              size="sm"
            >
        <template #prefix>
          <FeatherIcon name="refresh-cw" class="w-4 h-4" />
        </template>
              {{ __('Refresh') }}
      </Button>
          </div>
        </div>
    </div>

      <!-- Data Table -->
      <div class="bg-white shadow-sm border border-gray-200 rounded-lg overflow-hidden">
        <!-- Loading State -->
        <Loading v-if="loading" text="Loading platforms..." />

        <!-- Error State -->
        <div v-else-if="error" class="p-8">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ __('Error loading data') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ error }}</p>
            <div class="mt-6">
              <Button @click="handleRefresh" variant="solid" theme="blue">
                {{ __('Try Again') }}
              </Button>
            </div>
            </div>
        </div>

        <!-- Data Table Content -->
        <div v-else>
          <!-- Table Header -->
          <div class="bg-gray-50 px-6 py-3 border-b border-gray-200">
            <div class="grid grid-cols-12 gap-4 text-xs font-medium text-gray-500 uppercase tracking-wider">
              <div class="col-span-3">{{ __('Data Source') }}</div>
              <div class="col-span-2">{{ __('Type') }}</div>
              <div class="col-span-2">{{ __('Status') }}</div>
              <div class="col-span-2">{{ __('Last Sync') }}</div>
              <div class="col-span-2">{{ __('Created') }}</div>
              <div class="col-span-1">{{ __('Actions') }}</div>
          </div>
        </div>

          <!-- Table Body -->
          <div class="divide-y divide-gray-200">
            <div v-for="platform in filteredPlatforms" :key="platform.id"
              class="px-6 py-4 hover:bg-gray-50 transition-colors duration-150">
              <div class="grid grid-cols-12 gap-4 items-center">
                <!-- Source Info -->
                <div class="col-span-3">
                  <div class="flex items-center space-x-3">
                    <div
                      class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <span class="text-lg">{{ platform.icon }}</span>
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="text-sm font-medium text-gray-900 truncate">{{ platform.name }}</p>
                      <p class="text-xs text-gray-500 truncate">{{ __(platform.description) }}</p>
                    </div>
                </div>
              </div>

                <!-- Type -->
                <div class="col-span-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getTypeColor(platform.type)">
                    {{ __(platform.type_display) }}
                  </span>
            </div>

                <!-- Status -->
                <div class="col-span-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full" :class="getStatusColor(platform.id)"></div>
                    <span class="text-sm text-gray-900">{{ getConnectionStatusText(platform.id) }}</span>
              </div>
                  <div v-if="getConnectionByPlatformId(platform.id)?.last_error" class="text-xs text-red-600 mt-1 truncate" 
                    :title="getConnectionByPlatformId(platform.id)?.last_error">
                    {{ getConnectionByPlatformId(platform.id)?.last_error }}
                  </div>
                </div>

                <!-- Last Sync -->
                <div class="col-span-2">
                  <p class="text-sm text-gray-900">{{ formatPagesCount(platform.id) }}</p>
                  <p v-if="getConnectedAccountsForPlatform(platform.id).length > 0" class="hidden">
                    {{ formatLastSync(platform.id) }}
                  </p>
            </div>

                <!-- Created -->
                <div class="col-span-2">
                  <p class="text-sm text-gray-900">{{ formatCreated(platform.id) }}</p>
                  <p class="text-xs text-gray-500">{{ getConnectionByPlatformId(platform.id)?.owner || 'Administrator' }}</p>
            </div>

                <!-- Actions -->
                <div class="col-span-1">
                  <div class="flex items-center gap-1">
              <!-- Connect Button - Chỉ khi chưa có kết nối -->
                    <button
                v-if="!hasConnection(platform.id)"
                @click="initiatePlatformConnection(platform)"
                      class="p-1 text-slate-400 hover:text-green-600 transition-colors"
                      :title="__('Connect')"
                      :disabled="connectingPlatforms.includes(platform.id)"
                    >
                      <FeatherIcon name="link" class="w-4 h-4" />
                    </button>

                    <!-- View Button - Cho tất cả platforms -->
                    <button
                      @click="handleView(platform)"
                      class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                      :title="__('View Details')"
                    >
                      <FeatherIcon name="eye" class="w-4 h-4" />
                    </button>

              <!-- Edit Button - Cho Connected và Pending -->
                    <button
                v-if="canManageConnection(platform.id)"
                @click="editConnectionForPlatform(platform.id)"
                      class="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                      :title="__('Edit')"
                      :disabled="connectingPlatforms.includes(platform.id) || disconnectingPlatforms.includes(platform.id)"
                    >
                      <FeatherIcon name="edit" class="w-4 h-4" />
                    </button>

                    <!-- Disconnect Button - Cho Connected và Pending -->
                    <button
                      v-if="canManageConnection(platform.id)"
                      @click="confirmAndDisconnect(platform.id)"
                      class="p-1 text-slate-400 hover:text-red-600 transition-colors"
                      :title="__('Disconnect')"
                      :disabled="disconnectingPlatforms.includes(platform.id)"
                    >
                      <FeatherIcon name="x" class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
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
    <Dialog v-model="showViewModal" :options="{
      title: __('Platform Details'),
      size: 'lg'
    }">
      <template #body>
        <div v-if="selectedPlatform" class="p-6">
          <div class="space-y-6">
            <!-- Basic Info -->
              <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Basic Information') }}</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Platform Name') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ selectedPlatform.name }}</p>
              </div>
              <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Type') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ __(selectedPlatform.type_display) }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Description') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ __(selectedPlatform.description) }}</p>
                </div>
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Features') }}</label>
                  <div class="mt-1 flex flex-wrap gap-1">
                <Badge
                      v-for="feature in selectedPlatform.features"
                      :key="feature"
                      variant="outline"
                      size="xs"
                    >
                      {{ __(feature) }}
                </Badge>
              </div>
                </div>
              </div>
            </div>

            <!-- Status Info -->
              <div>
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Connection Status') }}</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Current Status') }}</label>
                  <div class="mt-1 flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full" :class="getStatusColor(selectedPlatform.id)">
                    </div>
                    <span class="text-sm text-gray-900">{{ getConnectionStatusText(selectedPlatform.id) }}</span>
                  </div>
              </div>
              <div>
                  <label class="text-sm font-medium text-gray-500">{{ __('Last Sync') }}</label>
                  <p class="mt-1 text-sm text-gray-900">{{ formatLastSync(selectedPlatform.id) }}</p>
              </div>
            </div>
          </div>

            <!-- Connected Pages/Accounts Section -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-medium text-gray-900">{{ __('Connected Pages/Accounts') }}</h3>
                <!-- Sync Button - Chỉ hiển thị khi đã kết nối -->
                <Button
                  v-if="isConnectionConnected(selectedPlatform.id)"
                  @click="syncAccountsForView(selectedPlatform.id)"
                  variant="outline"
                  size="sm"
                  :loading="syncingPlatforms.includes(selectedPlatform.id)"
                  :disabled="syncingPlatforms.includes(selectedPlatform.id)"
                >
                  <template #prefix>
                    <FeatherIcon name="refresh-cw" class="w-4 h-4" />
                  </template>
                  {{ __('Sync Pages') }}
                </Button>
              </div>

              <!-- Loading State for Accounts -->
              <div v-if="loadingAccounts" class="flex items-center justify-center py-8">
                <div class="flex items-center space-x-2">
                  <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>
                  <span class="text-sm text-gray-600">{{ __('Loading pages...') }}</span>
                </div>
              </div>

              <!-- Connected Accounts List -->
              <div v-else-if="viewModalAccounts.length > 0" class="space-y-3">
                <div
                  v-for="account in viewModalAccounts"
                :key="account.external_account_id"
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border hover:bg-gray-100 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <div
                      class="w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg flex items-center justify-center"
                  >
                      <FeatherIcon name="user" class="w-4 h-4 text-white" />
                  </div>
                  <div>
                      <div class="font-medium text-gray-900">{{ account.account_name }}</div>
                    <div class="text-xs text-gray-500">
                      {{ account.account_type }} • {{ account.external_account_id }}
                    </div>
                      <div v-if="account.page_id" class="text-xs text-blue-600">
                        Page ID: {{ account.page_id }}
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
                    <Badge v-if="account.is_verified" variant="blue" size="sm">
                      {{ __("Verified") }}
                    </Badge>
              </div>
            </div>
          </div>

          <!-- No Accounts Message -->
              <div v-else-if="!isConnectionConnected(selectedPlatform.id)" class="text-center py-8">
                <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FeatherIcon name="link" class="w-8 h-8 text-gray-400" />
                </div>
                <h4 class="text-sm font-medium text-gray-900 mb-2">{{ __('Not Connected') }}</h4>
                <p class="text-sm text-gray-500 mb-4">{{ __('Connect to this platform to see available pages and accounts.') }}</p>
                <Button
                  @click="initiatePlatformConnection(selectedPlatform)"
                  variant="solid"
                  size="sm"
                  :loading="connectingPlatforms.includes(selectedPlatform.id)"
                >
                  <template #prefix>
                    <FeatherIcon name="link" class="w-4 h-4" />
                  </template>
                  {{ __('Connect Now') }}
                </Button>
          </div>

              <!-- No Pages Found -->
              <div v-else class="text-center py-8">
                <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FeatherIcon name="alert-circle" class="w-8 h-8 text-yellow-600" />
                </div>
                <h4 class="text-sm font-medium text-gray-900 mb-2">{{ __('No Pages Found') }}</h4>
                <p class="text-sm text-gray-500 mb-4">{{ __('No pages or accounts were found for this platform. Try syncing to refresh the list.') }}</p>
                <Button
                  @click="syncAccountsForView(selectedPlatform.id)"
                  variant="outline"
                  size="sm"
                  :loading="syncingPlatforms.includes(selectedPlatform.id)"
                >
                  <template #prefix>
                    <FeatherIcon name="refresh-cw" class="w-4 h-4" />
                  </template>
                  {{ __('Sync Pages') }}
                </Button>
              </div>
            </div>

            <!-- Connection Statistics -->
            <div v-if="isConnectionConnected(selectedPlatform.id) && connectionStats">
              <h3 class="text-lg font-medium text-gray-900 mb-4">{{ __('Connection Statistics') }}</h3>
            <div class="grid grid-cols-3 gap-4">
              <div class="text-center p-3 bg-blue-50 rounded-lg">
                <div class="text-2xl font-bold text-blue-600">
                    {{ connectionStats.total_api_calls || 0 }}
                </div>
                <div class="text-xs text-blue-600">{{ __("Total API Calls") }}</div>
              </div>
              <div class="text-center p-3 bg-green-50 rounded-lg">
                <div class="text-2xl font-bold text-green-600">
                    {{ connectionStats.successful_calls || 0 }}
                </div>
                <div class="text-xs text-green-600">{{ __("Successful Calls") }}</div>
              </div>
              <div class="text-center p-3 bg-red-50 rounded-lg">
                <div class="text-2xl font-bold text-red-600">
                    {{ connectionStats.failed_calls || 0 }}
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
                    :class="getSuccessRateColor(connectionStats)"
                >
                    {{ calculateSuccessRate(connectionStats) }}%
                </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex items-center gap-2">
          <!-- Edit Button -->
          <Button
            v-if="canManageConnection(selectedPlatform?.id)"
            @click="editConnectionForPlatform(selectedPlatform.id)"
            variant="outline"
            size="sm"
            :disabled="connectingPlatforms.includes(selectedPlatform?.id) || disconnectingPlatforms.includes(selectedPlatform?.id)"
          >
            <template #prefix>
              <FeatherIcon name="edit" class="w-4 h-4" />
            </template>
            {{ __('Edit') }}
          </Button>

          <!-- Disconnect Button -->
          <Button
            v-if="canManageConnection(selectedPlatform?.id)"
            @click="confirmAndDisconnect(selectedPlatform.id)"
            variant="outline"
            size="sm"
            theme="red"
            :disabled="disconnectingPlatforms.includes(selectedPlatform?.id)"
          >
            <template #prefix>
              <FeatherIcon name="x" class="w-4 h-4" />
            </template>
            {{ __('Disconnect') }}
          </Button>

          <Button @click="closeViewModal" variant="ghost">
            {{ __('Close') }}
          </Button>
        </div>
      </template>
    </Dialog>

    <!-- Loading Overlay -->
    <div v-if="processing" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-sm w-full mx-4">
        <div class="flex items-center space-x-3">
          <svg class="animate-spin h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
            </path>
          </svg>
          <span class="text-sm text-gray-700">{{ processingMessage }}</span>
        </div>
      </div>
    </div>

    <!-- Reusable Data Source Modal for MobiWork ATS -->
    <CandidateDataSourceFormDirect
      v-model="showDataSourceModal"
      :dataSource="dataSourceFormData"
      @success="handleDataSourceSuccess"
      @cancel="handleDataSourceCancel"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, shallowRef, nextTick, watch } from "vue";
import { Button, Dialog, FormControl, Badge, FeatherIcon, call, TextInput, Breadcrumbs } from "frappe-ui";
import { showToast } from "@/utils";
import { ToastContainer } from "@/components/shared";
import FacebookConnectionForm from "@/components/Connectors/FacebookConnectionForm.vue";
import ZaloConnectionForm from "@/components/Connectors/ZaloConnectionForm.vue";
import TopcvConnectionForm from "@/components/Connectors/TopcvConnectionForm.vue";
import LayoutHeader from '@/components/LayoutHeader.vue';
import Loading from '@/components/Loading.vue';
import useToast from "@/composables/useToast";
import CandidateDataSourceFormDirect from '@/components/candidateDataSource/CandidateDataSourceFormDirect.vue'

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

// Master data cho các nhóm connect type và platform (LOẠI BỎ CAL.COM)
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
        type: "social_media",
        type_display: __("Social Network"),
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
        type: "messaging",
        type_display: __("Messaging"),
        features: [
          __("Message Broadcasting"),
          __("Customer Chat"),
          __("Template Messages"),
          __("User Management"),
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
        type: "job_board",
        type_display: __("Job Board"),
        features: [
          __("Job Posting"),
          __("Candidate Management"),
          __("Application Tracking"),
          __("Resume Database Access"),
        ],
      },
      {
        id: "mobiwork_ats",
        name: "MobiWork ATS",
        icon: "🧰",
        description: __("Connect MobiWork Applicant Tracking System"),
        color: "border-purple-400",
        type: "job_board",
        type_display: __("ATS"),
        features: [
          __("Job Posting"),
          __("Candidate Management"),
          __("Pipeline Tracking"),
          __("Integration Webhooks"),
        ],
      },
    ],
  },
};

// Platform form components mapping (LOẠI BỎ CALCOM CONNECTION FORM)
const platformFormComponents = shallowRef({
  facebook: FacebookConnectionForm,
  zalo: ZaloConnectionForm,
  topcv: TopcvConnectionForm,
});

// State
const connections = ref([]);
const loading = ref(false);
const processing = ref(false);
const processingMessage = ref('');
const error = ref(null);
const isRefreshing = ref(false);
const showConnectModal = ref(false);
const showEditModal = ref(false);
const showViewModal = ref(false);

// New states for view modal
const loadingAccounts = ref(false);
const viewModalAccounts = ref([]);
const connectionStats = ref(null);

const selectedPlatform = shallowRef(null);
const editingConnection = shallowRef(null);

const connectingPlatforms = ref([]);
const disconnectingPlatforms = ref([]);
const syncingPlatforms = ref([]);
const isConnecting = ref(false);
const isUpdating = ref(false);
const isRefreshingSingle = ref(false);

const showDataSourceModal = ref(false)
const editingDataSource = ref(null)
const dataSourceFormData = ref(null)

// Filters and search
const searchText = ref('');
const typeFilter = ref('');
const statusFilter = ref('');

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

// Breadcrumbs
const breadcrumbs = [
  { label: __('External Connections'), route: { name: 'Connectors' } }
];

const emit = defineEmits(["connection-updated", "job-shared"]);

// Computed property to get all platforms (connected and unconnected)
const allPlatforms = computed(() => {
  return Object.values(CONNECTION_TYPES)
    .flatMap(type => type.platforms)
    .map(platform => ({
      ...platform,
      // Add connection info if exists
      connection: getConnectionByPlatformId(platform.id)
    }));
});

// Filtered platforms based on search and filters
const filteredPlatforms = computed(() => {
  let platforms = allPlatforms.value;

  // Search filter
  if (searchText.value) {
    const search = searchText.value.toLowerCase();
    platforms = platforms.filter(platform => 
      platform.name.toLowerCase().includes(search) ||
      platform.description.toLowerCase().includes(search)
    );
  }

  // Type filter
  if (typeFilter.value) {
    platforms = platforms.filter(platform => platform.type === typeFilter.value);
  }

  // Status filter
  if (statusFilter.value) {
    platforms = platforms.filter(platform => {
      const status = getConnectionStatus(platform.id);
      switch (statusFilter.value) {
        case 'connected':
          return status === 'Connected';
        case 'not_connected':
          return !status;
        case 'pending':
          return status === 'Pending';
        case 'failed':
          return status === 'Failed' || status === 'Disconnected';
        default:
          return true;
      }
    });
  }

  return platforms;
});

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
  } else if (type === "datasource") {
    return `${__("Edit")} ${editingDataSource.value?.name || 'MobiWork ATS'} ${__("Data Source")}`;
  }

  return __("Platform Connection");
};

// Helper functions
const getTypeColor = (type) => {
  const colors = {
    'social_media': 'bg-blue-100 text-blue-800',
    'messaging': 'bg-green-100 text-green-800',
    'job_board': 'bg-purple-100 text-purple-800',
  }
  return colors[type] || 'bg-gray-100 text-gray-800'
};

const getStatusColor = (platformId) => {
  const status = getConnectionStatus(platformId);
  const colors = {
    'Connected': 'bg-green-500',
    'Pending': 'bg-yellow-500',
    'Failed': 'bg-red-500',
    'Disconnected': 'bg-gray-500'
  }
  return colors[status] || 'bg-gray-500'
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

const formatPagesCount = (platformId) => {
  const accounts = getConnectedAccountsForPlatform(platformId);
  if (accounts.length > 0) {
    return `${accounts.length} ${__('pages')}`;
  }
  return __("N/A"); // Hiển thị N/A khi số pages <= 0
};

const formatLastSync = (platformId) => {
  const connection = getConnectionByPlatformId(platformId);
  if (!connection) return __("N/A");
  return formatDate(connection.last_sync_time);
};

const formatCreated = (platformId) => {
  const connection = getConnectionByPlatformId(platformId);
  if (!connection) return __("N/A");
  return formatDate(connection.creation);
};

// Event handlers
const handleRefresh = () => {
  refreshConnections();
};

const handleSearchChange = () => {
  // Search is reactive via computed property
};

const handleFilterChange = () => {
  // Filters are reactive via computed property
};

const handleCreate = () => {
  // For now, we'll just show a message
  notify('info', __('Info'), __('Please select a platform from the list to create a connection'));
};

const handleView = async (platform) => {
  selectedPlatform.value = platform;
  showViewModal.value = true;
  
  // Load accounts if platform is connected
  if (isConnectionConnected(platform.id)) {
    await loadAccountsForView(platform.id);
  }
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

// New methods for view modal
const closeViewModal = () => {
  showViewModal.value = false;
  selectedPlatform.value = null;
  viewModalAccounts.value = [];
  connectionStats.value = null;
  loadingAccounts.value = false;
};

const loadAccountsForView = async (platformId) => {
  const connection = getConnectionByPlatformId(platformId);
  if (!connection) return;

  loadingAccounts.value = true;
  viewModalAccounts.value = [];

  try {
    const response = await call(
      "mbw_mira.api.external_connections.get_account_details",
      {
        connection_id: connection.connection_id || connection.name,
      }
    );

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

    viewModalAccounts.value = accountsData;
    connectionStats.value = connection;
  } catch (error) {
    console.error("Error loading accounts for view:", error);
    notify("error", __("Error"), __("Failed to load account details"));
  } finally {
    loadingAccounts.value = false;
  }
};

const syncAccountsForView = async (platformId) => {
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

    const result = handleApiResponse(response, __("Pages synced successfully"));

    notify("success", __("Success"), result.message);

    // Reload accounts for view modal
    await loadAccountsForView(platformId);
    
    // Also refresh the main connections list
    await refreshConnections();
  } catch (error) {
    console.error("Error syncing accounts:", error);
    notify("error", __("Error"), error.message || __("Failed to sync pages"));
  } finally {
    clearLoadingState(platformId, syncingPlatforms.value);
  }
};

// Platform action methods
const initiatePlatformConnection = (platform) => {
  // Nếu là mobiwork_ats => mở modal datasource
  if (platform.id === 'mobiwork_ats') {
    editingDataSource.value = null
    // Tạo mới: không truyền dataSource để form ở chế độ create (tránh update thiếu name)
    dataSourceFormData.value = null
    showDataSourceModal.value = true
    return
  }
  selectedPlatform.value = { ...platform };
  resetForm(connectForm);
  showConnectModal.value = true;
};

const editConnectionForPlatform = async (platformId) => {
  // Nếu là mobiwork_ats => mở modal datasource edit
  if (platformId === 'mobiwork_ats') {
    const ds = await findDataSourceByPlatform('mobiwork_ats')
    editingDataSource.value = ds || null
    // Chỉ set dataSource khi có name để form vào chế độ edit; nếu không có, mở create
    dataSourceFormData.value = (ds && ds.name) ? ds : null
    showDataSourceModal.value = true
    return
  }
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

// Enhanced connection operations
const createConnection = async (connectionData) => {
  try {
    validateConnectionData(connectionData);

    const response = await call("mbw_mira.api.external_connections.create_connection", {
      platform_type: selectedPlatform.value.name,
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

// Main methods
const refreshConnections = async () => {
  isRefreshing.value = true;
  loading.value = true;
  error.value = null;

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
  } catch (err) {
    console.error("Error refreshing connections:", err);
    connections.value = [];
    error.value = err.message || __("Failed to load connections");
    notify(
      "error",
      __("Error"),
      `${__("Failed to refresh connections:")} ${err.message || err}`
    );
  } finally {
    isRefreshing.value = false;
    loading.value = false;
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
  processing.value = true;
  processingMessage.value = __('Disconnecting platform...');

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
    processing.value = false;
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

// Watch for search text changes with debounce
let searchTimeout;
watch(searchText, () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    // Search is reactive via computed property, no action needed
  }, 500);
});

// Helper functions for statistics
const calculateSuccessRate = (connection) => {
  const total = connection?.total_api_calls || 0;
  const successful = connection?.successful_calls || 0;

  if (total === 0) return 0;
  return Math.round((successful / total) * 100);
};

const getSuccessRateColor = (connection) => {
  const rate = calculateSuccessRate(connection);
  if (rate >= 95) return "text-green-600";
  if (rate >= 80) return "text-yellow-600";
  return "text-red-600";
};

// Helper: tìm data source cho mobiwork_ats (stub)
const findDataSourceByPlatform = async (platformId) => {
  try {
    // TODO: gọi API lấy datasource theo platform nếu có mapping; tạm thời trả null
    return null
  } catch (e) {
    return null
  }
}

const handleDataSourceSuccess = async () => {
  showDataSourceModal.value = false
  await refreshConnections()
  notify('success', __('Success'), __('Data source saved successfully'))
}

const handleDataSourceCancel = () => {
  showDataSourceModal.value = false
}

</script>

<style scoped>
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
