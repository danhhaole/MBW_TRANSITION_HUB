<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Layout Header -->
      <LayoutHeader>
        <template #left-header>
          <Breadcrumbs :items="breadcrumbs" />
        </template>
        <template #right-header>
          <Button variant="solid" theme="gray" @click="openCreateDialog" v-if="canCreate">
            <template #prefix>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </template>
            {{ __('Create Campaign') }}
          </Button>
        </template>
      </LayoutHeader>

      <div class="flex-1 overflow-auto">
        <div class="max-w-full mx-2 px-6 py-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <!-- Search box -->
        <div class="relative">
          <input
            v-model="searchText"
            type="text"
            :placeholder="__('Search...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="setSearchText($event.target.value)"
          />
          <div
            class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
          >
            <svg
              class="h-5 w-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              ></path>
            </svg>
          </div>
          <button
            v-if="searchText"
            @click="handleClearSearch"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <svg
              class="h-5 w-5 text-gray-400 hover:text-gray-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
          <div
            v-if="loading || isSearching"
            class="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <svg
              class="animate-spin h-5 w-5 text-blue-500"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <!-- Birthday Stats Button -->
          <!-- <Button
            variant="outline"
            theme="blue"
            @click="showBirthdayStats = true; loadBirthdayStats()"
            class="flex items-center py-4"
          >
            <template #prefix>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"
                />
              </svg>
            </template>
            {{ __("Birthday Stats") }}
          </Button> -->

          <!-- View mode toggle -->
          <div class="flex rounded-md">
            <button
              @click="viewMode = 'list'"
              :class="[
                viewMode === 'list'
                  ? 'bg-black text-white'
                  : 'bg-white text-gray-700 hover:text-gray-500',
                'relative inline-flex items-center px-4 py-2 rounded-l-md border border-gray-300 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-black focus:border-black',
              ]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6h16M4 10h16M4 14h16M4 18h16"
                />
              </svg>
              {{ __("List") }}
            </button>
            <button
              @click="viewMode = 'card'"
              :class="[
                viewMode === 'card'
                  ? 'bg-black text-white'
                  : 'bg-white text-gray-700 hover:text-gray-500',
                'relative inline-flex items-center px-4 py-2 rounded-r-md border border-gray-300 border-l-0 text-sm font-medium focus:z-10 focus:outline-none focus:ring-1 focus:ring-black focus:border-black',
              ]"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
                />
              </svg>
              {{ __("Card") }}
            </button>
          </div>

          <!-- Status Filter -->
          <Select
            v-model="statusFilter"
            :options="statusOptions"
            @change="setStatusFilter"
            class="min-w-40 text-sm"
            size="md"
            variant="outlined"
            placeholder="All Statuses"
          />

          <!-- Tag Filter -->
          <Select
            v-model="tagFilter"
            :options="tagOptions"
            @change="setTagFilter"
            class="min-w-40 text-sm"
            size="md"
            variant="outlined"
            placeholder="All Tags"
          />

          <!-- Test Birthday Button -->
          <!-- <Button
            variant="outline"
            theme="blue"
            @click="testBirthdayTrigger"
            :loading="testingBirthday"
            class="flex items-center py-4"
          >
            <template #prefix>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v13m0-13V6a2 2 0 112 2h-2zm0 0V5.5A2.5 2.5 0 109.5 8H12zm-7 4h14M5 12a2 2 0 110-4h14a2 2 0 110 4M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"
                />
              </svg>
            </template>
            {{ __("Test Birthday") }}
          </Button> -->

          <!-- Refresh Button -->
          <Button
            variant="outline"
            theme="gray"
            @click="handleRefresh"
            :loading="loading"
            class="flex items-center py-4"
          >
            <template #prefix>
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                :class="{ 'animate-spin': loading }"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </template>
            {{ __("Refresh") }}
          </Button>
        </div>
      </div>

      <!-- Main content -->
      <div class="bg-white rounded-lg border border-gray-200">
        <!-- <Loading v-if="loading" text="Loading campaigns..." /> -->
        <!-- Table/Card view -->
        <campaign-table
          v-if="viewMode === 'list'"
          :campaigns="campaigns"
          :loading="loading"
          :pagination="pagination"
          @page-change="goToPage"
          @edit="openEditDialog"
          @view="openViewDialog"
          @delete="handleDelete"
          @save-as-template="handleSaveAsTemplate"
          @create="openCreateDialog"
        />

        <campaign-card-view
          v-else
          :campaigns="campaigns"
          :loading="loading"
          @edit="openEditDialog"
          @view="openViewDialog"
          @delete="handleDelete"
          @save-as-template="handleSaveAsTemplate"
          @create="openCreateDialog"
        />
      </div>

      <!-- Dialogs -->
      <!-- Creation Method Selection Modal -->
      <CampaignCreationMethodModal
        v-model="showMethodSelection"
        @select="handleMethodSelection"
      />

      <!-- Template Selection Modal -->
      <TemplateSelectionModal
        v-model="showTemplateSelection"
        :campaign-type="props.campaignType"
        @select="handleTemplateSelection"
      />

      <!-- New Wizards (Atomic Design) - Support both create and edit -->
      <AttractionCampaignWizard
        v-if="props.campaignType === 'ATTRACTION'"
        :show="showCreateWizard || showEditWizard"
        :campaign-type="props.campaignType"
        :edit-campaign-id="selectedCampaign?.name"
        @close="handleWizardClose"
        @success="handleWizardSuccess"
        @campaign-created="handleCampaignCreated"
      />

      <NurturingCampaignWizard
        v-if="props.campaignType === 'NURTURING'"
        :show="showCreateWizard || showEditWizard"
        :campaign-type="props.campaignType"
        :edit-campaign-id="selectedCampaign?.name"
        @close="handleWizardClose"
        @success="handleWizardSuccess"
        @campaign-created="handleCampaignCreated"
      />

      <RecruitmentCampaignWizard
        v-if="props.campaignType === 'RECRUITMENT'"
        :show="showCreateWizard || showEditWizard"
        :campaign-type="props.campaignType"
        :edit-campaign-id="selectedCampaign?.name"
        @close="handleWizardClose"
        @success="handleWizardSuccess"
      />

      <!-- Toast notifications -->
      <toast-container />

      <!-- Save as Template Modal -->
      <SaveAsTemplateModal
        v-model="showSaveAsTemplateModal"
        :campaign="campaignToSaveAsTemplate"
        @saved="handleTemplateSaved"
      />

      <!-- Birthday Statistics Modal -->
      <!-- <Dialog
        v-model="showBirthdayStats"
        :options="{
          title: 'Birthday Statistics',
          size: '5xl',
        }"
      >
        <template #body-content>
          <div v-if="loadingBirthdayStats" class="flex justify-center items-center py-8">
            <svg class="animate-spin h-8 w-8 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="ml-2">Loading statistics...</span>
          </div>

          <div v-else class="space-y-6">
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                Today's Birthday Check
              </h3>

              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-gray-900">{{ birthdayStats.today.talents_checked }}</div>
                  <div class="text-sm text-gray-600">Talents Checked</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-orange-600">{{ birthdayStats.today.birthdays_found }}</div>
                  <div class="text-sm text-gray-600">Birthdays Found</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-green-600">{{ birthdayStats.today.emails_sent }}</div>
                  <div class="text-sm text-gray-600">Emails Sent</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-red-600">{{ birthdayStats.today.emails_failed }}</div>
                  <div class="text-sm text-gray-600">Emails Failed</div>
                </div>
              </div>

              <div class="mt-4 flex items-center justify-between">
                <div class="flex items-center">
                  <span class="text-sm text-gray-600">Status:</span>
                  <span :class="{
                    'bg-green-100 text-green-800': birthdayStats.today.status === 'Success',
                    'bg-yellow-100 text-yellow-800': birthdayStats.today.status === 'No Run Today',
                    'bg-red-100 text-red-800': birthdayStats.today.status === 'Failed'
                  }" class="ml-2 px-2 py-1 text-xs font-medium rounded-full">
                    {{ birthdayStats.today.status }}
                  </span>
                </div>

                <div class="flex space-x-2">
                  <Button
                    variant="outline"
                    theme="blue"
                    size="sm"
                    @click="triggerBirthdayCheck(false)"
                  >
                    Run Check Now
                  </Button>
                  <Button
                    variant="outline"
                    theme="orange"
                    size="sm"
                    @click="triggerBirthdayCheck(true)"
                  >
                    Migration Run
                  </Button>
                  <Button
                    variant="outline"
                    theme="green"
                    size="sm"
                    @click="runBirthdayTest()"
                  >
                    Debug Test
                  </Button>
                </div>
              </div>
            </div>

            <div class="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                Last 30 Days Summary
              </h3>

              <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-gray-900">{{ birthdayStats.monthly.total_talents }}</div>
                  <div class="text-sm text-gray-600">Total Talents</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-orange-600">{{ birthdayStats.monthly.total_birthdays }}</div>
                  <div class="text-sm text-gray-600">Total Birthdays</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-green-600">{{ birthdayStats.monthly.total_emails_sent }}</div>
                  <div class="text-sm text-gray-600">Emails Sent</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-blue-600">{{ birthdayStats.monthly.success_rate }}%</div>
                  <div class="text-sm text-gray-600">Success Rate</div>
                </div>
                <div class="bg-white rounded-lg p-4 text-center shadow-sm">
                  <div class="text-2xl font-bold text-purple-600">{{ birthdayStats.monthly.total_runs }}</div>
                  <div class="text-sm text-gray-600">Total Runs</div>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-medium text-gray-900 mb-2">🎂 Talent Pools với Sinh Nhật Hôm Nay</h4>
              <div v-if="birthdayPools && birthdayPools.length > 0" class="space-y-2">
                <div v-for="pool in birthdayPools" :key="pool.pool_name"
                     class="flex justify-between items-center bg-white rounded p-2 border">
                  <div>
                    <span class="font-medium">{{ pool.pool_name }}</span>
                    <span class="text-sm text-gray-600 ml-2">({{ pool.birthday_count }} ứng viên)</span>
                  </div>
                  <Button
                    variant="outline"
                    theme="blue"
                    size="sm"
                    @click="viewPoolDetails(pool.pool_name)"
                  >
                    Xem Chi Tiết
                  </Button>
                </div>
              </div>
              <div v-else class="text-sm text-gray-600">
                Không có ứng viên nào sinh nhật hôm nay
              </div>

              <div class="mt-3 pt-3 border-t">
                <p class="text-xs text-gray-500">
                  • Hệ thống đọc trực tiếp từ Talent Pools<br>
                  • Chỉ gửi cho ứng viên có email và chưa opt-out<br>
                  • Chạy tự động hàng ngày hoặc manual trigger
                </p>
              </div>
            </div>
          </div>
        </template>

        <template #actions>
          <div class="flex justify-end space-x-2">
            <Button
              @click="showBirthdayStats = false"
              variant="outline"
            >
              {{ __('Close') }}
            </Button>
          </div>
        </template>
      </Dialog> -->

      <!-- Delete Confirmation Dialog -->
      <Dialog
        v-model="showDeleteConfirmDialog"
        :options="{
          title: 'Confirm Delete Campaign',
          size: 'md',
        }"
      >
        <template #body-content>
          <div class="space-y-4">
            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div class="flex items-start">
                <svg class="h-6 w-6 text-yellow-600 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-yellow-800">
                    {{ __('Warning') }}
                  </h3>
                  <p class="mt-2 text-sm text-yellow-700">
                    {{ __('Deleting this campaign will also delete all related data.') }}
                  </p>
                </div>
              </div>
            </div>

            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
              <p class="text-sm text-red-800">
                <strong>{{ __('This action cannot be undone.') }}</strong> {{ __('Are you sure you want to continue?') }}
              </p>
            </div>
          </div>
        </template>

        <template #actions>
          <div class="flex justify-end space-x-2">
            <Button
              @click="cancelDelete"
              variant="outline"
            >
              {{ __('Cancel') }}
            </Button>
            <Button
              @click="confirmForceDelete"
              theme="red"
            >
              {{ __('Confirm') }}
            </Button>
          </div>
        </template>
      </Dialog>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useCampaignList, useCampaignCRUD } from "../composables/useCampaign";
import { usePermissionStore } from "@/stores/permission"
import useToast from "@/composables/useToast";
import {
  CampaignTable,
  CampaignCardView,
  CampaignWizard,
  CampaignForm,
  CampaignView,
  CampaignCreationMethodModal,
  TemplateSelectionModal,
  SaveAsTemplateModal,
} from "@/components/campaign";
import { ToastContainer } from "@/components/shared";
import { Button, Breadcrumbs, Select, Dialog, call } from "frappe-ui";
import LayoutHeader from "@/components/LayoutHeader.vue";
import Loading from "@/components/Loading.vue";
import { useCampaignStore } from "@/stores/campaign";

// New Campaign Wizards (Atomic Design)
import AttractionCampaignWizard from "@/pages/AttractionCampaignWizard.vue";
import NurturingCampaignWizard from "@/pages/NurturingCampaignWizard.vue";
import RecruitmentCampaignWizard from "@/pages/RecruitmentCampaignWizard.vue";

const permission = usePermissionStore()
const canCreate = permission.can("Mira Campaign", "create")
const canEdit = permission.can("Mira Campaign", "edit")
const canDelete = permission.can("Mira Campaign", "delete")

// Props
const props = defineProps({
  campaignType: {
    type: String,
    default: null
  }
});
// import AutomationSidebar from "@/components/AutomationSidebar.vue";
// import { useAutomationStatsStore } from "@/stores/automationStats";

// Router
const router = useRouter();
const route = useRoute();

// Campaign store
const campaignStore = useCampaignStore();

// Automation stats store
// const statsStore = useAutomationStatsStore();

// Breadcrumbs - dynamic based on campaign type
const campaignTypeLabels = {
  'ATTRACTION': 'Attraction Campaigns',
  'NURTURING': 'Attract-Nurture Campaigns',
  'RECRUITMENT': 'Recruitment Campaigns'
};

const breadcrumbs = computed(() => {
  const label = props.campaignType ? campaignTypeLabels[props.campaignType] : 'All Campaigns';
  return [{ label: __(label), route: { name: route.name } }];
});

// Create button label - dynamic based on campaign type
const createButtonLabel = computed(() => {
  if (!props.campaignType) return __('Create Campaign');
  const typeLabel = campaignTypeLabels[props.campaignType]?.replace(' Campaigns', '');
  return __(`Create ${typeLabel} Campaign`);
});

// Page state
const viewMode = ref("list");
const showMethodSelection = ref(false); // Modal chọn phương thức tạo
const showTemplateSelection = ref(false); // Modal chọn template
const showCreateWizard = ref(false); // Wizard cho tạo mới
const showEditWizard = ref(false); // Wizard cho edit
const showViewDialog = ref(false);
const selectedCampaign = ref(null);
const refreshTrigger = ref(0);
const searchDebounceTimer = ref(null);
const isSearching = ref(false);

// Delete confirmation dialog
const showDeleteConfirmDialog = ref(false);
const campaignToDelete = ref(null);
const linkedDocuments = ref([]);

// Save as template modal
const showSaveAsTemplateModal = ref(false);
const campaignToSaveAsTemplate = ref(null);

// Composables
const {
  campaigns,
  loading,
  pagination,
  searchText,
  statusFilter,
  typeFilter,
  activeFilter,
  loadCampaigns,
  smartLoadCampaigns,
  goToPage,
  changeItemsPerPage,
  setSearchText,
  setStatusFilter,
  setTypeFilter,
  setActiveFilter,
} = useCampaignList();

const { deleteCampaign, forceDeleteCampaign } = useCampaignCRUD();
const { success, error, info } = useToast();

// Wrapper để thống nhất cách hiển thị toast như kỳ vọng showToast
const showToast = (message, type = "info", duration = 3000) => {
  const opts = { duration };
  if (type === "success") return success(message, opts);
  if (type === "error") return error(message, opts);
  return info(message, opts);
};

// Status filter options
const statusOptions = [
  { label: __("All Statuses"), value: "all" },
  { label: __("Draft"), value: "DRAFT" },
  { label: __("Active"), value: "ACTIVE" },
  { label: __("Paused"), value: "PAUSED" },
  { label: __("Failed"), value: "FAILED" },
  { label: __("Cancelled"), value: "CANCELLED" },
  { label: __("Archived"), value: "ARCHIVED" },
];

// Tag filter
const tagFilter = ref("all");
const tagOptions = ref([
  { label: __("All Tags"), value: "all" },
]);

// Set tag filter
const setTagFilter = (value) => {
  tagFilter.value = value;
  loadCampaignsWithFilters();
};

// Load campaigns with all filters
const loadCampaignsWithFilters = async () => {
  const filters = {
    type: props.campaignType, // Filter by campaign type from props
    status: statusFilter.value !== "all" ? statusFilter.value : undefined,
    tag: tagFilter.value !== "all" ? tagFilter.value : undefined,
    searchText: searchText.value && searchText.value.trim() ? searchText.value.trim() : undefined,
  };

  await loadCampaigns(filters);
};

// Debounced search function
const debouncedSearch = (searchValue) => {
  // Clear existing timer
  if (searchDebounceTimer.value) {
    clearTimeout(searchDebounceTimer.value);
  }

  // Set new timer
  searchDebounceTimer.value = setTimeout(async () => {
    isSearching.value = true;
    console.log("Performing search for:", searchValue);

    try {
      // Prepare filters
      const filters = {
        type: props.campaignType, // Filter by campaign type from props
        status: statusFilter.value !== "all" ? statusFilter.value : undefined,
        isActive:
          activeFilter.value !== "all" ? activeFilter.value === "active" : undefined,
      };

      // Only add searchText if it's not empty
      if (searchValue && searchValue.trim()) {
        filters.searchText = searchValue.trim();
      }

      await loadCampaigns(filters);

      // Show search feedback
      if (searchValue && searchValue.trim()) {
        const resultCount = campaigns.value.length;
        showToast(__(`Found ${resultCount} results for "${searchValue}"`), "info", 3000);
      }
    } finally {
      isSearching.value = false;
    }
  }, 500); // 500ms delay
};

// Watch search text changes
watch(
  searchText,
  (newValue) => {
    debouncedSearch(newValue);
  },
  { immediate: false }
);

// Event handlers
const openCreateDialog = () => {
  selectedCampaign.value = null;
  showMethodSelection.value = true; // Show method selection first
};

const handleMethodSelection = (method) => {
  if (method === 'manual') {
    // Close method selection modal
    showMethodSelection.value = false;
    // Open new wizard for manual creation
    showCreateWizard.value = true;
  } else if (method === 'template') {
    // Open template selection
    showTemplateSelection.value = true;
  }
};

const handleTemplateSelection = async (template) => {
  console.log('Template selected, campaign created:', template);
  showTemplateSelection.value = false;

  // Campaign was already created in the modal
  if (template?.createdCampaign) {
    success(__('Campaign created from template successfully!'));

    // Reload campaign list
    await loadCampaignsWithFilters();

    // Open the created campaign for editing
    const createdCampaign = template.createdCampaign;
    if (createdCampaign?.campaign_id) {
      const campaign = campaigns.value.find(c => c.name === createdCampaign.campaign_id);
      if (campaign) {
        openEditDialog(campaign);
      }
    }
  }
};

const handleCreateFromSidebar = (section) => {
  console.log('Create new from sidebar:', section);
  if (section === 'campaigns') {
    openCreateDialog();
  }
  // Flow và Sequence sẽ được xử lý sau
};

const openEditDialog = (campaign) => {
  selectedCampaign.value = campaign;
  showEditWizard.value = true;
};

const openViewDialog = (campaign) => {
  // Navigate to campaign detail view instead of opening modal
  router.push(`/campaigns/${campaign.name}`);
};

const editFromView = () => {
  showViewDialog.value = false;
  showEditWizard.value = true;
};

const handleCreateSuccess = async (campaign) => {
  console.log("Create wizard success:", campaign);
  console.log("Campaigns before reload:", campaigns.value.length);

  // Close wizard
  showCreateWizard.value = false;
  selectedCampaign.value = null;

  // Reload data
  await loadCampaignsWithFilters();

  // Refresh sidebar stats
  // statsStore.refreshStats();

  console.log("Campaigns after reload:", campaigns.value.length);

  // Show success message
  const campaignName = campaign?.campaign_name || campaign?.name || 'Campaign';
  showToast(__(`Campaign "${campaignName}" created successfully!`), "success");
};

const handleDraftCreated = async (draftCampaign) => {
  console.log("📄 Draft campaign created:", draftCampaign.name);

  // Reload campaign list to show the new draft
  await loadCampaignsWithFilters();

  console.log("📋 Campaign list refreshed after draft creation");
};

const handleWizardClose = () => {
  showCreateWizard.value = false;
  showEditWizard.value = false;
  selectedCampaign.value = null;
};

const handleWizardSuccess = async (campaign) => {
  console.log("Wizard success:", campaign);

  const isEdit = showEditWizard.value;

  // Close wizard
  handleWizardClose();

  // Reload data
  await loadCampaignsWithFilters();

  // Show success message
  const campaignName = campaign?.campaign_name || campaign?.name || 'Campaign';
  const action = isEdit ? 'updated' : 'created';
  // showToast(__(`Campaign "${campaignName}" ${action} successfully!`), "success");
};

const handleCampaignCreated = async (campaign) => {
  console.log("Campaign created in Step 1:", campaign);

  // Reload campaign list to show new campaign
  await loadCampaignsWithFilters();
};

const handleClearSearch = () => {
  searchText.value = "";
  // Clear search sẽ trigger watcher và reload data
};

const handleRefresh = async () => {
  await loadCampaignsWithFilters();

  showToast(__("Data refreshed"), "info", 2000);
};

const handleDelete = async (campaign) => {
  try {
    const successDelete = await deleteCampaign(campaign.name, campaign.campaign_name);

    if (successDelete) {
      showToast(__("Campaign deleted"), "success");
      loadCampaignsWithFilters();

      // Refresh sidebar stats
      // statsStore.refreshStats();
    }
  } catch (errorDelete) {
    console.error('Delete error:', errorDelete);

    // Check if it's a LinkExistsError
    if (errorDelete.errorType === 'LinkExistsError' && errorDelete.linkedDocuments) {
      // Show Frappe UI dialog with linked documents
      campaignToDelete.value = campaign;
      linkedDocuments.value = errorDelete.linkedDocuments;
      showDeleteConfirmDialog.value = true;
    } else {
      showToast(__("Error deleting campaign"), "error");
    }
  }
};

const confirmForceDelete = async () => {
  if (!campaignToDelete.value) return;

  try {
    await forceDeleteCampaign(campaignToDelete.value.name, campaignToDelete.value.campaign_name);
    showToast(
      __("Campaign deleted successfully!"),
      "success"
    );
    loadCampaignsWithFilters();
    // statsStore.refreshStats();
    showDeleteConfirmDialog.value = false;
    campaignToDelete.value = null;
    linkedDocuments.value = [];
  } catch (forceError) {
    console.error('Force delete error:', forceError);
    showToast(__("Error deleting campaign"), "error");
  }
};

const cancelDelete = () => {
  showDeleteConfirmDialog.value = false;
  campaignToDelete.value = null;
  linkedDocuments.value = [];
};

const handleSaveAsTemplate = (campaign) => {
  campaignToSaveAsTemplate.value = campaign;
  showSaveAsTemplateModal.value = true;
};

const handleTemplateSaved = (templateData) => {
  showToast(__('Campaign saved as template successfully!'), 'success');
  console.log('✅ Template created:', templateData);
  showSaveAsTemplateModal.value = false;
  campaignToSaveAsTemplate.value = null;
};

// Birthday Statistics
const birthdayStats = ref({
  today: {
    talents_checked: 0,
    birthdays_found: 0,
    emails_sent: 0,
    emails_failed: 0,
    status: 'No Run Today'
  },
  monthly: {
    total_talents: 0,
    total_birthdays: 0,
    total_emails_sent: 0,
    success_rate: 0,
    total_runs: 0
  }
});

const showBirthdayStats = ref(false);
const loadingBirthdayStats = ref(false);
const birthdayPools = ref([]);
const testingBirthday = ref(false);

// Load birthday statistics
const loadBirthdayStats = async () => {
  try {
    loadingBirthdayStats.value = true;

    // Load stats
    const statsResult = await call('mbw_mira.api.birthday_api.get_birthday_stats_for_campaign');
    if (statsResult && statsResult.status === 'success') {
      birthdayStats.value = statsResult.data;
    }

    // Load pools with birthdays
    const poolsResult = await call('mbw_mira.api.birthday_api.get_talent_pools_with_birthdays');
    if (poolsResult && poolsResult.status === 'success') {
      birthdayPools.value = poolsResult.data;
    }

  } catch (error) {
    console.error('Error loading birthday stats:', error);
  } finally {
    loadingBirthdayStats.value = false;
  }
};

// View pool details
const viewPoolDetails = async (poolName) => {
  try {
    const result = await call('mbw_mira.api.birthday_api.get_pool_birthday_details', {
      pool_name: poolName
    });

    if (result && result.status === 'success') {
      const details = result.data;
      const talentNames = details.birthday_talents.map(t => t.full_name).join(', ');
      showToast(`Pool "${poolName}": ${details.count} ứng viên sinh nhật hôm nay\n${talentNames}`, 'info', 5000);
    }
  } catch (error) {
    console.error('Error loading pool details:', error);
    showToast('Lỗi khi tải chi tiết pool', 'error');
  }
};

// Trigger birthday check manually
const triggerBirthdayCheck = async (migrationRun = false) => {
  try {
    showToast('Đang chạy kiểm tra sinh nhật...', 'info');

    const result = await call('mbw_mira.api.birthday_api.trigger_birthday_check', {
      migration_run: migrationRun
    });

    if (result && result.status === 'success') {
      showToast(result.message, 'success');
      // Reload stats after successful run
      await loadBirthdayStats();
    } else {
      showToast(result.message || 'Lỗi khi chạy kiểm tra sinh nhật', 'error');
    }
  } catch (error) {
    console.error('Error triggering birthday check:', error);
    showToast('Lỗi khi chạy kiểm tra sinh nhật', 'error');
  }
};

// Run birthday test for debugging
const runBirthdayTest = async () => {
  try {
    showToast('Đang chạy debug test...', 'info');

    const result = await call('mbw_mira.api.birthday_api.run_birthday_test');

    if (result && result.status === 'success') {
      const data = result.data;
      const summary = `
Debug Test Complete:
• Data: ${data.data_result.birthday_today} birthdays today
• Email: ${data.email_result.success ? 'Success' : 'Failed'}
• Birthday Check: ${data.birthday_result.success ? 'Success' : 'Failed'}
• Emails Sent: ${data.birthday_result.emails_sent || 0}
• Emails Failed: ${data.birthday_result.emails_failed || 0}
      `;
      showToast(summary, data.birthday_result.success ? 'success' : 'error', 8000);

      // Reload stats
      await loadBirthdayStats();
    } else {
      showToast(result.message || 'Debug test failed', 'error');
    }
  } catch (error) {
    console.error('Error running birthday test:', error);
    showToast('Lỗi khi chạy debug test', 'error');
  }
};

// Test Birthday Trigger - Manually trigger birthday check
// const testBirthdayTrigger = async () => {
//   try {
//     testingBirthday.value = true;
//     showToast('🎂 Đang kiểm tra chiến dịch sinh nhật...', 'info');

//     const result = await call('mbw_mira.schedulers.trigger_birthday.run_daily_birthday_check', {
//       migration_run: false
//     });

//     console.log('🎂 Birthday check result:', result);

//     if (result && result.success) {
//       const message = `
// ✅ Kiểm tra sinh nhật hoàn tất!
// 📊 Chiến dịch đã quét: ${result.campaigns_processed || 0}
// 👥 Ứng viên đã kiểm tra: ${result.total_checked || 0}
// 🎉 Sinh nhật tìm thấy: ${result.birthday_found || 0}
// 📧 Email đã gửi: ${result.emails_sent || 0}
// ❌ Email thất bại: ${result.emails_failed || 0}
// ⏱️ Thời gian: ${result.execution_time || 0}s
//       `.trim();
//       showToast(message, 'success', 8000);
//     } else {
//       const errorMsg = result?.message || result?.error || 'Không có chiến dịch ACTIVE với trigger ON_BIRTHDAY';
//       showToast(`⚠️ ${errorMsg}`, 'info', 5000);
//     }
//   } catch (error) {
//     console.error('❌ Error testing birthday trigger:', error);
//     showToast('❌ Lỗi khi kiểm tra sinh nhật: ' + error.message, 'error');
//   } finally {
//     testingBirthday.value = false;
//   }
// };

// Kịch bản Thu hút - Chúc mừng sinh nhật
const runAttractionBirthdayScenario = async (poolName) => {
  console.log('🎯 Thu hút Kịch bản - Bắt đầu gửi tin nhắn chúc mừng sinh nhật tự động');

  if (!poolName) {
    showToast('Vui lòng chọn Talent Pool', 'error');
    return;
  }

  try {
    // Gọi API gửi email (sử dụng hàm gửi send_email ở backend)
    const result = await call('mbw_mira.api.campaign.run_birthday_test_for_pool', {
      pool_name: poolName,
      subject: 'Chúc mừng sinh nhật!', // Tiêu đề mặc định
      content: '<p>Chúc mừng sinh nhật bạn! Chúng tôi chúc bạn một ngày tuyệt vời.</p>' // Nội dung mặc định
    });

    if (result && result.status === 'success') {
      console.log('✅ Kịch bản Thu hút - Đã gửi email chúc mừng sinh nhật:', result);
      showToast(`Đã gửi ${result.sent_count} email chúc mừng sinh nhật`, 'success');
    } else {
      console.warn('⚠️ Kịch bản Thu hút - Không gửi được email:', result);
    }
  } catch (error) {
    console.error('❌ Lỗi chạy kịch bản Thu hút:', error);
    showToast('Lỗi khi gửi email chúc mừng sinh nhật', 'error');
  }
};

// Watch route changes to reload data when switching between campaign types
watch(
  () => route.name,
  (newRoute, oldRoute) => {
    // Only reload if route actually changed (not initial load)
    if (oldRoute !== undefined && newRoute !== oldRoute) {
      console.log('🔄 Route changed from', oldRoute, 'to', newRoute);
      console.log('📍 Current campaignType prop:', props.campaignType);
      // Reset filters when switching routes
      statusFilter.value = "all";
      tagFilter.value = "all";
      searchText.value = "";
      loadCampaignsWithFilters();
    }
  },
  { immediate: false }
);

// Also watch campaignType prop changes (in case it changes without route change)
watch(
  () => props.campaignType,
  (newType, oldType) => {
    console.log('🎯 Campaign type prop changed:', { oldType, newType });
    // Reload data whenever type changes (including initial load if oldType is undefined)
    loadCampaignsWithFilters();
  },
  { immediate: false } // Don't run on mount since onMounted already loads data
);

// Initialize
onMounted(() => {
  loadCampaignsWithFilters();
  // Load birthday stats on mount
  loadBirthdayStats();
  // Expose for testing
  window.runAttractionBirthdayScenario = runAttractionBirthdayScenario;
  window.triggerBirthdayCheck = triggerBirthdayCheck;
});

// Cleanup
onUnmounted(() => {
  if (searchDebounceTimer.value) {
    clearTimeout(searchDebounceTimer.value);
  }
});
</script>

<style scoped>
/* Custom styles for toast positioning */
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: none;
}

.toast-container > * {
  pointer-events: all;
}
</style>
