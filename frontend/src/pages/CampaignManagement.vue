<template>
  <div class="flex h-screen bg-gray-50">
    <!-- Automation Sidebar -->
    <AutomationSidebar
      @create="handleCreateFromSidebar"
    />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
     

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
          @create="openCreateDialog"
        />

        <campaign-card-view
          v-else
          :campaigns="campaigns"
          :loading="loading"
          @edit="openEditDialog"
          @view="openViewDialog"
          @delete="handleDelete"
          @create="openCreateDialog"
        />
      </div>

      <!-- Dialogs -->
      <!-- Wizard cho tạo mới -->
      <campaign-wizard
        v-model="showCreateWizard"
        @success="handleCreateSuccess"
        @draft-created="handleDraftCreated"
      />

      <!-- Wizard cho chỉnh sửa -->
      <campaign-wizard
        v-model="showEditForm"
        :editing-campaign="selectedCampaign"
        @success="handleEditSuccess"
        @draft-created="handleDraftCreated"
      />

      <!-- Toast notifications -->
      <toast-container />

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
import { useRouter } from "vue-router";
import { useCampaignList, useCampaignCRUD } from "../composables/useCampaign";
import useToast from "@/composables/useToast";
import {
  CampaignTable,
  CampaignCardView,
  CampaignWizard,
  CampaignForm,
  CampaignView,
} from "@/components/campaign";
import { ToastContainer } from "@/components/shared";
import { Button, Breadcrumbs, Select, Dialog } from "frappe-ui";
import LayoutHeader from "@/components/LayoutHeader.vue";
import Loading from "@/components/Loading.vue";
import { useCampaignStore } from "@/stores/campaign";
import AutomationSidebar from "@/components/AutomationSidebar.vue";
import { useAutomationStatsStore } from "@/stores/automationStats";

// Router
const router = useRouter();

// Campaign store
const campaignStore = useCampaignStore();

// Automation stats store
const statsStore = useAutomationStatsStore();

// Breadcrumbs
const breadcrumbs = [{ label: __("Campaigns"), route: { name: "CampaignManagement" } }];

// Page state
const viewMode = ref("list");
const showCreateWizard = ref(false); // Wizard cho tạo mới
const showEditForm = ref(false); // Form cho chỉnh sửa
const showViewDialog = ref(false);
const selectedCampaign = ref(null);
const refreshTrigger = ref(0);
const searchDebounceTimer = ref(null);
const isSearching = ref(false);

// Delete confirmation dialog
const showDeleteConfirmDialog = ref(false);
const campaignToDelete = ref(null);
const linkedDocuments = ref([]);

// Composables
const {
  campaigns,
  loading,
  pagination,
  loadCampaigns,
  searchText,
  statusFilter,
  typeFilter,
  activeFilter,
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
        status: statusFilter.value !== "all" ? statusFilter.value : undefined,
        type: typeFilter.value !== "all" ? typeFilter.value : undefined,
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
  showCreateWizard.value = true;
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
  showEditForm.value = true;
};

const openViewDialog = (campaign) => {
  // Navigate to campaign detail view instead of opening modal
  router.push(`/campaigns/${campaign.name}`);
};

const editFromView = () => {
  showViewDialog.value = false;
  showEditForm.value = true;
};

const handleCreateSuccess = async (event) => {
  const { action, data } = event;

  console.log("Create wizard success:", { action, data });
  console.log("Campaigns before reload:", campaigns.value.length);

  // Close wizard
  showCreateWizard.value = false;
  selectedCampaign.value = null;

  // Reload data
  await loadCampaigns();

  // Refresh sidebar stats
  statsStore.refreshStats();

  console.log("Campaigns after reload:", campaigns.value.length);

  // Show success message
  showToast(__(`Campaign "${data.campaign_name}" created successfully!`), "success");
};

const handleDraftCreated = async (draftCampaign) => {
  console.log("📄 Draft campaign created:", draftCampaign.name);

  // Reload campaign list to show the new draft
  await loadCampaigns();

  console.log("📋 Campaign list refreshed after draft creation");
};

const handleEditSuccess = async (event) => {
  const { action, data } = event;

  console.log("Edit form success:", { action, data });
  console.log("Campaigns before reload:", campaigns.value.length);

  // Close form
  showEditForm.value = false;
  selectedCampaign.value = null;

  // Reload data
  await loadCampaigns();

  console.log("Campaigns after reload:", campaigns.value.length);

  // Show success message
  showToast(__(`Campaign "${data.campaign_name}" updated successfully!`), "success");
};

const handleFormCancel = () => {
  showEditForm.value = false;
  selectedCampaign.value = null;
};

const handleClearSearch = () => {
  searchText.value = "";
  // Clear search sẽ trigger watcher và reload data
};

const handleRefresh = async () => {
  await loadCampaigns();

  showToast(__("Data refreshed"), "info", 2000);
};

const handleDelete = async (campaign) => {
  try {
    const successDelete = await deleteCampaign(campaign.name, campaign.campaign_name);

    if (successDelete) {
      showToast(__(`Campaign "${campaign.campaign_name}" deleted`), "success");
      loadCampaigns();
      
      // Refresh sidebar stats
      statsStore.refreshStats();
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
    loadCampaigns();
    statsStore.refreshStats();
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

// Initialize
onMounted(() => {
  loadCampaigns();
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
