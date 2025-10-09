<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader
      :useTeleport="false"
      :sticky="true"
      sticky-classes="sticky top-0 z-50 bg-gray-50 border-b"
    >
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
      <template #right-header>
        <Button variant="solid" theme="gray" @click="openCreateDialog" :loading="loading">
          <template #prefix>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
          </template>
          {{ __("Create New") }}
        </Button>
      </template>
    </LayoutHeader>

    <div class="container mx-auto px-6 py-6">
      <div class="flex items-center justify-between mb-6">
        <div class="relative">
          <input
            v-model="searchText"
            type="text"
            :placeholder="__('Search by template name...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearchInput"
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
              />
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
          <Button
            variant="outline"
            theme="gray"
            @click="refreshList"
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

      <!-- Controls đến từ ViewControls (dùng cho tải dữ liệu, phân trang, group search có sẵn) -->
      <!-- <ViewControls
        :key="componentKey"
        ref="viewControls"
        v-model="listData"
        v-model:loadMore="loadMore"
        v-model:resizeColumn="triggerResize"
        v-model:updatedPageCount="updatedPageCount"
        :filters="{}"
        doctype="MIRA_Email_Template"
        :enableGroupSearch="true"
      /> -->

      <div class="bg-white rounded-lg border border-gray-200">
        <Loading v-if="loading" text="Loading email templates..." />
        <!-- List view -->
        <div v-if="!loading && viewMode === 'list'" class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ __("Template Name") }}
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ __("Template Type") }}
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ __("Created Date") }}
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ __("Owner") }}
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {{ __("Actions") }}
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="item in items" :key="item.name" class="hover:bg-gray-50">
                <td class="px-6 py-4">
                  <button
                    class="text-left text-gray-800 text-base hover:underline"
                    @click="view(item)"
                  >
                    {{ item.template_name }}
                  </button>
                </td>
                <td class="px-6 py-4 text-gray-700 text-base">
                  {{ formatTemplateType(item.template_type) }}
                </td>
                <td class="px-6 py-4 text-gray-700 text-base">
                  {{ formatDate(item.creation) }}
                </td>
                <td class="px-6 py-4 text-gray-700 text-base">{{ item.owner }}</td>
                <td class="px-6 py-4 space-x-2">
                  <button
                    @click="edit(item)"
                    class="text-blue-600 hover:text-blue-900"
                    title="Edit"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                      />
                    </svg>
                  </button>
                  <button
                    @click="remove(item)"
                    class="text-red-600 hover:text-red-900"
                    title="Delete"
                  >
                    <svg
                      class="w-5 h-5"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Pagination -->
          <div
            v-if="pagination.pages > 1"
            class="flex items-center justify-between px-6 py-4 border-t border-gray-200"
          >
            <div class="text-sm text-gray-500">
              {{ __("Display") }}
              {{
                pagination.total === 0
                  ? 0
                  : Math.min(
                      (pagination.page - 1) * pagination.limit + 1,
                      pagination.total
                    )
              }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }}
              {{ __("of") }} {{ pagination.total }} {{ __("records") }}
            </div>
            <div class="flex items-center space-x-2">
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="
                  pagination.page === 1
                    ? 'text-gray-400 border-gray-200 cursor-not-allowed'
                    : 'text-gray-700 border-gray-300 hover:bg-gray-50'
                "
                :disabled="pagination.page === 1"
                @click="goToPage(pagination.page - 1)"
              >
                {{ __("Prev") }}
              </button>
              <button
                v-for="p in pagination.pages"
                :key="p"
                class="px-3 py-1 rounded border text-sm"
                :class="
                  p === pagination.page
                    ? 'bg-black text-white border-black'
                    : 'text-gray-700 border-gray-300 hover:bg-gray-50'
                "
                @click="goToPage(p)"
              >
                {{ p }}
              </button>
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="
                  pagination.page === pagination.pages
                    ? 'text-gray-400 border-gray-200 cursor-not-allowed'
                    : 'text-gray-700 border-gray-300 hover:bg-gray-50'
                "
                :disabled="pagination.page === pagination.pages"
                @click="goToPage(pagination.page + 1)"
              >
                {{ __("Next") }}
              </button>
            </div>
          </div>
        </div>

        <!-- Card view -->
        <div
          v-if="!loading && viewMode === 'card'"
          class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
        >
          <!-- Template cards -->
          <div
            v-for="item in items"
            :key="item.name"
            class="border rounded-lg p-4 hover:shadow cursor-pointer"
            @click="view(item)"
          >
            <div class="flex items-start justify-between">
              <h3 class="text-base font-semibold text-gray-800 truncate">
                {{ item.template_name }}
              </h3>
            </div>
            <p class="text-sm text-gray-500 mt-1">
              {{ formatTemplateType(item.template_type) || "Email Template" }}
            </p>

            <div class="mt-4 flex items-center justify-between">
              <div class="mt-3 text-xs text-gray-500">
                <span>{{ __("Created:") }} {{ formatDate(item.creation) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <button
                  @click.stop="edit(item)"
                  class="text-blue-600 hover:text-blue-900"
                  title="Edit"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                </button>
                <button
                  @click.stop="remove(item)"
                  class="text-red-600 hover:text-red-900"
                  title="Delete"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Create New Card at end -->
          <div
            class="border-2 border-dashed rounded-lg p-6 flex items-center justify-center h-40 cursor-pointer hover:bg-gray-50"
            @click="openCreateDialog"
          >
            <div class="text-center">
              <div
                class="mx-auto w-10 h-10 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center"
              >
                <svg
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v12m6-6H6"
                  />
                </svg>
              </div>
              <div class="mt-3 font-medium">{{ __("Create New Template") }}</div>
              <div class="text-xs text-gray-500">
                {{ __("Start a new email template") }}
              </div>
            </div>
          </div>

          <!-- Pagination (card view) -->
          <div
            v-if="pagination.pages > 1"
            class="col-span-full flex items-center justify-between pt-4"
          >
            <div class="text-sm text-gray-500">
              {{ __("Display") }}
              {{
                pagination.total === 0
                  ? 0
                  : Math.min(
                      (pagination.page - 1) * pagination.limit + 1,
                      pagination.total
                    )
              }}-{{ Math.min(pagination.page * pagination.limit, pagination.total) }}
              {{ __("of") }} {{ pagination.total }} {{ __("records") }}
            </div>
            <div class="flex items-center space-x-2">
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="
                  pagination.page === 1
                    ? 'text-gray-400 border-gray-200 cursor-not-allowed'
                    : 'text-gray-700 border-gray-300 hover:bg-gray-50'
                "
                :disabled="pagination.page === 1"
                @click="goToPage(pagination.page - 1)"
              >
                {{ __("Prev") }}
              </button>
              <button
                v-for="p in pagination.pages"
                :key="p"
                class="px-3 py-1 rounded border text-sm"
                :class="
                  p === pagination.page
                    ? 'bg-black text-white border-black'
                    : 'text-gray-700 border-gray-300 hover:bg-gray-50'
                "
                @click="goToPage(p)"
              >
                {{ p }}
              </button>
              <button
                class="px-3 py-1 rounded border text-sm"
                :class="
                  pagination.page === pagination.pages
                    ? 'text-gray-400 border-gray-200 cursor-not-allowed'
                    : 'text-gray-700 border-gray-300 hover:bg-gray-50'
                "
                :disabled="pagination.page === pagination.pages"
                @click="goToPage(pagination.page + 1)"
              >
                {{ __("Next") }}
              </button>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div
          v-if="!loading && items.length === 0"
          class="flex h-60 items-center justify-center"
        >
          <div
            class="flex flex-col items-center gap-3 text-base font-medium text-gray-500"
          >
            <EmailIcon class="h-10 w-10" />
            <span>{{ __("No Data Found") }}</span>
            <p class="text-sm text-gray-400">
              Items: {{ items.length }}, Filtered: {{ filteredRows.length }}
            </p>
            <Button :label="__('Create')" @click="openCreateDialog">
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
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
              </template>
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- <QuickEntryModal v-model="showQuickEntryModal" doctype="MIRA_Email_Template" /> -->
    <!-- Trigger buttons -->
    <!-- <Button @click="showCreateModal = true">Create Template</Button>
		  <Button @click="editTemplate(template.name)">Edit Template</Button> -->
  </div>
</template>

<script setup>
import EmailIcon from "@/components/Icons/EmailIcon.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import Loading from "@/components/Loading.vue";
import { useToast } from "@/composables/useToast";

import {
  Breadcrumbs,
  Button,
  Select,
  createResource,
  call,
  createListResource,
} from "frappe-ui";
import { ref, computed, onMounted, reactive, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const toast = useToast();
const route = useRoute();
const router = useRouter();

const breadcrumbs = [
  { label: __("Email Template"), route: { name: "ListEmailTemplate" } },
];

// State management
const loading = ref(false);
const items = ref([]);
const pagination = ref({
  page: 1,
  limit: 10,
  total: 0,
  pages: 0,
  has_next: false,
  has_prev: false,
});
const searchText = ref("");
const statusFilter = ref("all");
const viewMode = ref("list");

// Computed properties
const filteredRows = computed(() => {
  let filtered = items.value;

  console.log("Computing filtered rows. Items:", items.value.length);
  console.log("Search text:", searchText.value);
  console.log("Status filter:", statusFilter.value);

  // Filter by search text
  if (searchText.value) {
    const search = searchText.value.toLowerCase();
    filtered = filtered.filter(
      (item) =>
        item.template_name?.toLowerCase().includes(search) ||
        item.template_type?.toLowerCase().includes(search)
    );
  }

  // Filter by status
  if (statusFilter.value !== "all") {
    filtered = filtered.filter((item) => item.is_active === statusFilter.value);
  }

  console.log("Filtered rows:", filtered.length);
  return filtered;
});

// Client-side pagination computed values
const totalFiltered = computed(() => filteredRows.value.length);
const totalPages = computed(() =>
  totalFiltered.value === 0 ? 0 : Math.ceil(totalFiltered.value / pagination.value.limit)
);
const pagedRows = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.limit;
  const end = start + pagination.value.limit;
  return filteredRows.value.slice(start, end);
});

// Helper functions
const badgeClass = (status) => {
  return status === "1"
    ? "bg-green-100 text-xs text-green-800"
    : "bg-gray-100 text-xs text-gray-800";
};

const formatDate = (date) => {
  return date
    ? new Date(date).toLocaleDateString("vi-VN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      })
    : "";
};

// Formatters
const formatTemplateType = (value) => {
  if (!value) return "";
  return String(value).replace(/[-_]+/g, " ");
};

// Create list resource as fallback
const templatesResource = createListResource({
  type: "list",
  doctype: "MIRA_Email_Template",
  fields: ["name", "template_name", "template_type", "is_active", "creation", "owner"],
  filters: [],
  orderBy: "creation desc",
  pageLength: 20,
  auto: false,
});

// Data loading functions
const loadData = async () => {
  loading.value = true;
  try {
    console.log("Loading email templates (server-side pagination)...");

    // Build filters based on search and status
    const filters = [];
    if (statusFilter.value !== "all") {
      filters.push(["is_active", "=", statusFilter.value]);
    }
    if (searchText.value) {
      const term = `%${searchText.value}%`;
      // Filter by template_name directly for reliable search
      filters.push(["template_name", "like", term]);
    }

    // 1) Get total count first
    let total = 0;
    try {
      total = await call("frappe.client.get_count", {
        doctype: "MIRA_Email_Template",
        filters,
      });
    } catch (e) {
      const countResponse = await call("frappe.client.get_list", {
        doctype: "MIRA_Email_Template",
        fields: ["name"],
        filters,
        limit_page_length: 0,
      });
      total = Array.isArray(countResponse) ? countResponse.length : 0;
    }

    pagination.value.total = total;
    pagination.value.pages = Math.max(1, Math.ceil(total / pagination.value.limit));

    // Ensure current page is within range
    if (pagination.value.page > pagination.value.pages) {
      pagination.value.page = pagination.value.pages;
    }

    // 2) Fetch current page rows
    const response = await call("frappe.client.get_list", {
      doctype: "MIRA_Email_Template",
      fields: [
        "name",
        "template_name",
        "template_type",
        "is_active",
        "creation",
        "owner",
      ],
      filters,
      order_by: "creation desc",
      limit_start: (pagination.value.page - 1) * pagination.value.limit,
      limit_page_length: pagination.value.limit,
    });

    items.value = Array.isArray(response) ? response : [];
  } catch (error) {
    console.error("Error loading email templates:", error);
    toast.error(__("Error loading email templates"));
    items.value = [];
    pagination.value.total = 0;
    pagination.value.pages = 0;
  } finally {
    loading.value = false;
  }
};

// Search functionality
let searchTimer = null;
const handleSearchInput = () => {
  if (searchTimer) clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    // Reset to first page and reload (server-side filtering)
    pagination.value.page = 1;
    loadData();
  }, 300);
};

// Also react if searchText changes via code or IME composition scenarios
watch(searchText, () => {
  if (searchTimer) clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    pagination.value.page = 1;
    loadData();
  }, 300);
});

// Pagination
const goToPage = async (page) => {
  if (!pagination.value.pages) return;
  if (page < 1 || page > pagination.value.pages) return;
  if (page === pagination.value.page) return;
  pagination.value.page = page;
  await loadData();
};

// CRUD operations
const view = (item) => {
  router.push({
    name: "EditEmailTemplate",
    params: { name: item.name },
  });
};

const edit = (item) => {
  router.push({
    name: "EditEmailTemplate",
    params: { name: item.name },
  });
};

const remove = async (item) => {
  if (confirm(__("Are you sure you want to delete this template?"))) {
    try {
      await call("frappe.client.delete", {
        doctype: "MIRA_Email_Template",
        name: item.name,
      });

      toast.success(__("Template deleted successfully"));
      await loadData();
    } catch (error) {
      console.error("Error deleting template:", error);
      toast.error(__("Error deleting template"));
    }
  }
};

// Dialog handlers
const openCreateDialog = () => {
  router.push({
    name: "NewEmailTemplate",
    params: { templateType: "" },
  });
};

// Filter functions
const applyActiveStatusFilter = () => {
  // Reset to first page and reload (server-side filtering)
  pagination.value.page = 1;
  loadData();
};

const refreshList = async () => {
  await loadData();
};

// Debug function
const debugData = async () => {
  console.log("=== DEBUG INFO ===");
  console.log("Items:", items.value);
  console.log("Filtered rows:", filteredRows.value);
  console.log("Loading:", loading.value);
  console.log("Pagination:", pagination.value);

  // Test direct API call
  try {
    const testResponse = await call("frappe.client.get_list", {
      doctype: "MIRA_Email_Template",
      fields: ["name", "template_name"],
      filters: [],
      limit_page_length: 5,
    });
    console.log("Direct API test:", testResponse);
  } catch (error) {
    console.error("Direct API test failed:", error);
  }
};

// Lifecycle
onMounted(async () => {
  await loadData();
});
</script>
