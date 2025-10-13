<template>
  <div class="min-h-screen bg-gray-50">
    <LayoutHeader>
      <template #left-header>
        <Breadcrumbs :items="breadcrumbs" />
      </template>
    </LayoutHeader>
    <div class="container mx-auto px-6 py-6">
      <div class="flex items-center justify-between mb-6">
        <div class="relative flex gap-4 items-center">
          <input
            v-model="searchText"
            type="text"
            :placeholder="__('Search...')"
            class="block w-60 pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            @input="handleSearch"
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
            @click="clearSearch"
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
        </div>
        <div class="flex gap-3 items-center">
          <Select
            v-model="campaignFilter"
            :options="[
              { label: 'All Campaigns', value: '' },
              ...campaignOptions.map((c) => ({ label: c.label, value: c.value })),
            ]"
            class="w-48"
            @update:model-value="handleSearch"
          />
          <Select
            v-model="segmentFilter"
            :options="[
              { label: 'All Segments', value: '' },
              ...segmentOptions.map((s) => ({ label: s.label, value: s.value })),
            ]"
            class="w-48"
            @update:model-value="handleSearch"
          />
          <Button variant="outline" theme="gray" @click="refreshData" :disabled="loading">
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
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
            </template>
            {{ __("Refresh") }}
          </Button>
        </div>
      </div>
      <div class="bg-white rounded-lg border border-gray-200">
        <Loading v-if="loading" text="Loading applicant pool..." />
        <template v-else-if="items.length === 0">
          <div class="text-center py-16">
            <div
              class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-4"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8 text-gray-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                ></path>
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              {{ __("No applications found") }}
            </h3>
            <p class="text-gray-500 mb-4">{{ __("No applicant data available.") }}</p>
          </div>
        </template>
        <template v-else>
          <div class="overflow-x-auto">
            <table class="min-w-full bg-white rounded-lg overflow-hidden">
              <thead class="bg-gray-100">
                <tr>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Talent
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Campaign
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Segment
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Status
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Result
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Score
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Application Date
                  </th>
                  <th
                    class="py-3 px-4 text-left text-xs font-medium text-gray-600 uppercase tracking-wider"
                  >
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 text-sm">
                <tr v-for="item in items" :key="item.name">
                  <td class="py-4 px-4">{{ item.talent_id }}</td>
                  <td class="py-4 px-4">{{ item.campaign_id }}</td>
                  <td class="py-4 px-4">{{ item.segment_id }}</td>
                  <td class="py-4 px-4">{{ item.application_status }}</td>
                  <td class="py-4 px-4">{{ item.result }}</td>
                  <td class="py-4 px-4">{{ item.score }}</td>
                  <td class="py-4 px-4">{{ formatDate(item.application_date) }}</td>
                  <td class="py-4 px-4">
                    <div class="flex items-center space-x-2">
                      <button
                        @click="handleView(item)"
                        class="text-gray-600 hover:text-blue-600 p-2 rounded-md hover:bg-blue-50 transition-colors"
                        :title="__('View Details')"
                      >
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
                            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                          />
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                          />
                        </svg>
                      </button>
                      <button
                        @click="handleEdit(item)"
                        class="text-gray-600 hover:text-green-600 p-2 rounded-md hover:bg-green-50 transition-colors"
                        :title="__('Edit')"
                      >
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
                            d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
                          />
                        </svg>
                      </button>
                      <button
                        @click="handleDelete(item)"
                        class="text-gray-600 hover:text-red-600 p-2 rounded-md hover:bg-red-50 transition-colors"
                        :title="__('Delete')"
                      >
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
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                          />
                        </svg>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div
            v-if="pagination.pages > 1"
            class="flex items-center justify-between mt-6 p-6 border-t border-gray-200"
          >
            <div class="text-sm text-gray-600">
              {{ __("Display") }} {{ pagination.showing_from || 1 }}-{{
                pagination.showing_to || items.length
              }}
              {{ __("of") }} {{ pagination.total || items.length }}
              {{ __("applications") }}
            </div>
            <div class="flex space-x-1">
              <button
                @click="goToPage(1)"
                :disabled="pagination.page === 1"
                class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
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
                    d="M15 19l-7-7 7-7"
                  ></path>
                </svg>
              </button>
              <template v-for="page in getPaginationRange()" :key="page">
                <button v-if="page === '...'" class="px-3 py-1 text-gray-500" disabled>
                  ...
                </button>
                <button
                  v-else
                  @click="goToPage(page)"
                  :class="
                    pagination.page === page
                      ? 'bg-black text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  "
                  class="px-3 py-1 rounded-md"
                >
                  {{ page }}
                </button>
              </template>
              <button
                @click="goToPage(pagination.page + 1)"
                :disabled="pagination.page >= pagination.pages"
                class="px-3 py-1 rounded-md bg-gray-100 text-gray-600 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
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
                    d="M9 5l7 7-7 7"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
        </template>
      </div>
      <!-- Dialogs -->
      <Dialog
        v-model="showEditDialog"
        :options="{ title: __('Edit Application'), size: '2xl' }"
      >
        <template #body-content>
          <div class="space-y-4 w-full">
            <FormControl
              type="text"
              label="Name"
              v-model="editItem.name"
              :disabled="true"
            />
            <Link
              v-model="editItem.talent_id"
              :doctype="'Mira Contact'"
              label="Talent Profile"
              :disabled="true"
            />
            <Link
              v-model="editItem.campaign_id"
              :doctype=""Mira Campaign""
              label="Mira Campaign"
              :disabled="true"
            />
            <Link
              v-model="editItem.segment_id"
              :doctype="'Mira Segment'"
              label="Segment"
              :disabled="true"
            />
            <Link
              v-model="editItem.interaction_id"
              :doctype="'Mira Interaction'"
              label="Mira Interaction"
              :disabled="true"
            />
            <DateTimePicker
              v-model="editItem.application_date"
              label="Application Date"
              :disabled="true"
            />
            <FormControl
              type="text"
              label="Application Position"
              v-model="editItem.position"
            />
            <FormControl
              type="text"
              label="Resume"
              v-model="editItem.resume"
              :description="'File URL hoặc đường dẫn file'"
            />
            <FormControl
              type="select"
              label="Status"
              v-model="editItem.application_status"
              :options="[
                { label: 'New', value: 'New' },
                { label: 'Under Review', value: 'Under Review' },
                { label: 'Rejected', value: 'Rejected' },
                { label: 'Shortlisted', value: 'Shortlisted' },
              ]"
            />
            <FormControl type="textarea" label="Notes" v-model="editItem.notes" />
            <FormControl type="number" label="Score" v-model="editItem.score" />
            <FormControl
              type="select"
              label="Result"
              v-model="editItem.result"
              :options="[
                { label: 'Pass', value: 'Pass' },
                { label: 'Fail', value: 'Fail' },
              ]"
            />
          </div>
        </template>
        <template #actions>
          <div class="flex gap-2 justify-end">
            <Button variant="ghost" @click="showEditDialog = false">{{
              __("Cancel")
            }}</Button>
            <Button variant="solid" @click="saveEdit">{{ __("Save") }}</Button>
          </div>
        </template>
      </Dialog>
      <Dialog
        v-model="showViewDialog"
        :options="{ title: __('Application Details'), size: '2xl' }"
      >
        <template #body-content>
          <div class="space-y-4">
            <FormControl type="text" label="Name" :model-value="viewItem.name" disabled />
            <FormControl
              type="text"
              label="Talent Profile"
              :model-value="viewItem.talent_id"
              disabled
            />
            <FormControl
              type="text"
              label="Mira Campaign"
              :model-value="viewItem.campaign_id"
              disabled
            />
            <FormControl
              type="text"
              label="Segment"
              :model-value="viewItem.segment_id"
              disabled
            />
            <FormControl
              type="text"
              label="Mira Interaction"
              :model-value="viewItem.interaction_id"
              disabled
            />
            <FormControl
              type="text"
              label="Application Date"
              :model-value="formatDate(viewItem.application_date)"
              disabled
            />
            <FormControl
              type="text"
              label="Application Position"
              :model-value="viewItem.position"
              disabled
            />
            <FormControl
              type="text"
              label="Resume"
              :model-value="viewItem.resume"
              disabled
            />
            <FormControl
              type="text"
              label="Status"
              :model-value="viewItem.application_status"
              disabled
            />
            <FormControl
              type="textarea"
              label="Notes"
              :model-value="viewItem.notes"
              disabled
            />
            <FormControl
              type="number"
              label="Score"
              :model-value="viewItem.score"
              disabled
            />
            <FormControl
              type="text"
              label="Result"
              :model-value="viewItem.result"
              disabled
            />
          </div>
        </template>
      </Dialog>
      <Dialog
        v-model="showDeleteDialog"
        :options="{ title: __('Confirm Delete'), size: 'sm' }"
      >
        <template #body-content>
          <div class="text-center">
            <div
              class="w-12 h-12 mx-auto mb-4 bg-red-100 rounded-full flex items-center justify-center"
            >
              <svg
                class="w-6 h-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.996-.833-2.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
            </div>
            <p class="text-slate-600 mb-2">
              {{ __("Are you sure you want to delete this application?") }}
            </p>
            <p class="font-medium text-gray-900">"{{ deleteItem?.name }}"</p>
            <p class="text-sm text-red-600 mt-2">
              {{ __("This action cannot be undone!") }}
            </p>
          </div>
        </template>
        <template #actions>
          <Button variant="ghost" @click="showDeleteDialog = false">{{
            __("Cancel")
          }}</Button>
          <Button variant="solid" theme="red" @click="confirmDelete">{{
            __("Delete")
          }}</Button>
        </template>
      </Dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from "vue";
import {
  Dialog,
  Button,
  Breadcrumbs,
  Select,
  FormControl,
  DateTimePicker,
} from "frappe-ui";
import LayoutHeader from "@/components/LayoutHeader.vue";
import Loading from "@/components/Loading.vue";
import Link from "@/components/Controls/Link.vue";
import { useMiraTalentPool } from "@/composables/useMiraTalentPool";

const breadcrumbs = [
  { label: __("Applicant Pool"), route: { name: "ApplicantPoolManagement" } },
];

// Use Mira Talent Pool composable
const {
  talentPools,
  loading,
  error,
  pagination,
  filters,
  filterOptions,
  fetchTalentPools,
  updateTalentPoolAPI,
  deleteTalentPoolAPI,
  fetchFilterOptions,
  updateSearch,
  updateCampaign,
  updateSegment,
  clearSearch,
  goToPage,
  getPaginationRange,
  initialize
} = useMiraTalentPool()

// Local reactive data
const items = computed(() => talentPools.value)
const searchText = ref(filters.search)

const showEditDialog = ref(false);
const showViewDialog = ref(false);
const showDeleteDialog = ref(false);
const editItem = ref({});
const viewItem = ref({});
const deleteItem = ref(null);

const editFields = [
  { fieldname: "talent_id", label: "Talent", readonly: true },
  { fieldname: "campaign_id", label: "Mira Campaign", readonly: true },
  { fieldname: "segment_id", label: "Segment", readonly: true },
  { fieldname: "application_status", label: "Status", readonly: false },
  { fieldname: "result", label: "Result", readonly: false },
  { fieldname: "score", label: "Score", readonly: false },
  { fieldname: "application_date", label: "Application Date", readonly: true },
  { fieldname: "notes", label: "Notes", readonly: false },
];

const campaignFilter = ref(filters.campaign);
const segmentFilter = ref(filters.segment);
const campaignOptions = computed(() => filterOptions.value.campaigns || []);
const segmentOptions = computed(() => filterOptions.value.segments || []);

function formatDate(dateString) {
  if (!dateString) return "-";
  try {
    return new Date(dateString).toLocaleDateString("vi-VN");
  } catch {
    return dateString;
  }
}

// Use getPaginationRange from composable

async function refreshData() {
  await initialize()
}

async function loadData() {
  await fetchTalentPools()
}

// Use methods from composable
function handleSearch() {
  updateSearch(searchText.value)
}

// Watch for filter changes
watch(campaignFilter, (newValue) => {
  updateCampaign(newValue)
})

watch(segmentFilter, (newValue) => {
  updateSegment(newValue)
})

function handleEdit(item) {
  editItem.value = { ...item };
  showEditDialog.value = true;
}

async function saveEdit() {
  try {
    const { name, ...data } = editItem.value;
    await updateTalentPoolAPI(name, data);
    showEditDialog.value = false;
  } catch (error) {
    console.error('Error updating talent pool:', error);
  }
}

function handleView(item) {
  viewItem.value = { ...item };
  showViewDialog.value = true;
}

function handleDelete(item) {
  deleteItem.value = item;
  showDeleteDialog.value = true;
}

async function confirmDelete() {
  try {
    await deleteTalentPoolAPI(deleteItem.value.name);
    showDeleteDialog.value = false;
  } catch (error) {
    console.error('Error deleting talent pool:', error);
  }
}

function getInputType(field) {
  if (field.fieldname === "score") return "number";
  if (field.fieldname === "application_date") return "date";
  return "text";
}

onMounted(async () => {
  await initialize();
});
</script>
