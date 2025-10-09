<template>
  <ListView
    :class="[$attrs.class, 'overflow-x-hidden']"
    :columns="columns"
    :rows="rows"
    :options="{
      // ...(props.valueType === '1'
      // 	? { onRowClick: (row) => emit('showyyy', row.name) }
      // 	: {
      // 			getRowRoute: (row) => ({
      // 				name: 'ats_institution',
      // 				params: { yyyId: row.name },
      // 			}),
      // 		}),
      selectable: options.selectable,
      showTooltip: options.showTooltip,
      resizeColumn: options.resizeColumn,
    }"
    row-key="name"
  >
    <ListHeader class="sm:mx-5 mx-3 whitespace-nowrap overflow-x-hidden" @columnWidthUpdated="emit('columnWidthUpdated')">
      <ListHeaderItem
        v-for="column in columns"
        :key="column.key"
        :item="column"
        @columnWidthUpdated="emit('columnWidthUpdated', column)"
      >
        <Button
          v-if="column.key == '_liked_by'"
          variant="ghosted"
          class="!h-4"
          @click="() => emit('applyLikeFilter')"
        >
          <HeartIcon class="h-4 w-4" />
        </Button>
      </ListHeaderItem>
    </ListHeader>

    <ListRows :rows="rows" v-slot="{ idx, column, item, row }" class="relative whitespace-nowrap overflow-x-hidden">
      <div v-if="column.key === 'template_name'">
        <Tooltip :text="item">
          <div
            class="flex items-center gap-2 truncate text-base cursor-pointer"
            @click="
              (event) => {
                fieldStore.childTableField = row.name;
                fieldStore.actionType = 'edit';
                navigateToEdit(row.name);
              }
            "
          >
            <div v-if="item" class="truncate">
              {{ item }}
            </div>
          </div>
        </Tooltip>
      </div>
      <div v-else-if="column.key === 'is_active'">
        <Tooltip :text="item">
          <div v-if="item == '1'" class="cursor-pointer">
            <Badge
              :variant="'subtle'"
              :theme="catStatusColor[item]"
              size="md"
              :label="__('Active')"
              @click="
                (event) =>
                  emit('applyFilter', {
                    event,
                    idx,
                    column,
                    item,
                    firstColumn: columns[0],
                  })
              "
            />
          </div>
          <div v-if="item == '0'" class="cursor-pointer">
            <Badge
              :variant="'subtle'"
              :theme="catStatusColor[item]"
              size="md"
              :label="__('Inactive')"
              @click="
                (event) =>
                  emit('applyFilter', {
                    event,
                    idx,
                    column,
                    item,
                    firstColumn: columns[0],
                  })
              "
            />
          </div>
        </Tooltip>
      </div>
      <div v-else-if="column.key === 'created_by'">
        <Tooltip :text="item">
          <div class="flex items-center gap-2 truncate text-base">
            <Avatar :image="item" :label="item" size="sm" />
            <div class="truncate">
              {{ item }}
            </div>
          </div>
        </Tooltip>
      </div>
      <div v-else-if="column.key === 'creation'">
        <Tooltip :text="item">
          <div class="flex items-center gap-2 truncate text-base">
            <CalendarIcon class="h-4 w-4 text-gray-500" />
            <div class="truncate">
              {{ dateFormat(item) }}
            </div>
          </div>
        </Tooltip>
      </div>
      <div v-else-if="column.key === '_actions'" class="flex items-center justify-end gap-2 pr-3">
        <Tooltip :text="__('View')">
          <button class="text-gray-600 hover:text-black" @click.stop="navigateToEdit(row.name)" title="View">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          </button>
        </Tooltip>
        <Tooltip :text="__('Edit')">
          <button class="text-blue-600 hover:text-blue-900" @click.stop="navigateToEdit(row.name)" title="Edit">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          </button>
        </Tooltip>
        <Tooltip :text="__('Delete')">
          <button class="text-red-600 hover:text-red-900" @click.stop="() => { fieldStore.childTableField = row.name; fieldStore.actionType = 'delete'; showConfirmModal = true }" title="Delete">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
          </button>
        </Tooltip>
      </div>
      <ListRowItem v-else :item="item" class="">
        <template #prefix> </template>
        <template #default="{ label }">
          <Tooltip :text="label">
            <div class="truncate text-base">
              {{ label }}
            </div>
          </Tooltip>
        </template>
      </ListRowItem>
    </ListRows>
    <ListSelectBanner>
      <template #actions="{ selections, unselectAll }">
        <Dropdown :options="listBulkActionsRef.bulkActions(selections, unselectAll)">
          <Button icon="more-horizontal" variant="ghost" />
        </Dropdown>
      </template>
    </ListSelectBanner>
  </ListView>

  <ListFooter
    v-if="pageLengthCount"
    class="border-t sm:px-5 px-3 py-2"
    v-model="pageLengthCount"
    :options="{
      rowCount: options.rowCount,
      totalCount: options.totalCount,
    }"
    @loadMore="emit('loadMore')"
  />
  <ListBulkActions
    ref="listBulkActionsRef"
    v-model="list"
    :doctype="props.doctype"
    :options="{
      hideAssign: true,
    }"
  />
  <ConfirmModal
    v-model="showConfirmModal"
    @confirm="() => deleteRecord(fieldStore.childTableField)"
  >
    <template #title>
      <div class="text-lg font-semibold flex justify-center">
        {{ __("Confirm Deletion") }}
      </div>
    </template>
    <template #content>
      <span class="flex justify-center">
        {{ __("Are you sure you want to delete this record?") }}
      </span>
    </template>
  </ConfirmModal>
</template>

<script setup>
import HeartIcon from "@/components/Icons/HeartIcon.vue";
import MoneyIcon from "@/components/Icons/MoneyIcon.vue";
import IndicatorIcon from "@/components/Icons/IndicatorIcon.vue";
import PhoneIcon from "@/components/Icons/PhoneIcon.vue";
import MultipleAvatar from "@/components/MultipleAvatar.vue";
import CalendarIcon from "@/components/Icons/CalendarIcon.vue";
import EmailIcon from "@/components/Icons/EmailIcon.vue";
import EmailAtIcon from "@/components/Icons/EmailAtIcon.vue";
import Email2Icon from "@/components/Icons/Email2Icon.vue";
import ListBulkActions from "@/components/ListBulkActions.vue";
import ListRows from "@/components/ListViews/ListRows.vue";
import { dateFormat } from "@/utils";
import {
  Avatar,
  ListView,
  ListHeader,
  ListHeaderItem,
  ListRowItem,
  ListFooter,
  Dropdown,
  Tooltip,
  Badge,
  createResource,
} from "frappe-ui";
import { catStatusColor } from "../../utils";
import { ref, computed, watch, onMounted, reactive, provide } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useFieldStore } from "../../stores/activeRecord";
import { call } from "frappe-ui";
import ConfirmModal from "../Modals/ConfirmModal.vue";
import ListSelectBanner from "../frappe-ui-custom/ListViewCustom/ListSelectBanner.vue";
import useToast from "@/composables/useToast";

const fieldStore = useFieldStore();
const showConfirmModal = ref(false);
provide("hideDelete", false);
provide("hideEdit", false);
const router = useRouter();
const route = useRoute();

watch(
  () => fieldStore.timestamp,
  () => {
    console.log("Fields updated");
    if (fieldStore.actionType === "edit") {
      navigateToEdit(fieldStore.childTableField);
    } else if (fieldStore.actionType === "delete") {
      showConfirmModal.value = true;
    }
  }
);

const props = defineProps({
  rows: {
    type: Array,
    required: true,
  },
  columns: {
    type: Array,
    required: true,
  },
  doctype: {
    type: String,
    required: true,
  },
  options: {
    type: Object,
    default: () => ({
      selectable: true,
      showTooltip: true,
      resizeColumn: false,
      totalCount: 0,
      rowCount: 0,
    }),
  },
});

const emit = defineEmits([
  "loadMore",
  "updatePageCount",
  "columnWidthUpdated",
  "showModal",
  "applyFilter",
  "applyLikeFilter",
  "likeDoc",
  "deleteRecord",
  "refresh",
]);

const pageLengthCount = defineModel();
const list = defineModel("list");

watch(pageLengthCount, (val, old_value) => {
  if (val === old_value) return;
  emit("updatePageCount", val);
});

const listBulkActionsRef = ref(null);

defineExpose({
  customListActions: computed(() => listBulkActionsRef.value?.customListActions),
  // Expose create toast helpers so parents can call after creating records
  handleCreateSuccess,
  handleCreateError,
});
let errorShown = ref(false);

// Toasts (align with APIIntegrationList.vue)
const {
  success: toastSuccess,
  error: toastError,
  warning: toastWarning,
  info: toastInfo,
} = useToast();

function deleteRecord(name) {
  call("frappe.client.delete", { doctype: props.doctype, name })
    .then(() => {
      emit("refresh");
      emit("deleteRecord");
      // Success toast consistent with APIIntegrationList's style
      toastSuccess(`${__("Deleted Successfully")}`);
    })
    .catch((err) => {
      console.log("Error occurred in deleteRecord:", err);
      const errText = __(err?.messages?.[0]) || __("An unexpected error occurred.");
      toastError(`${__("Error occurred")}: ${errText}`);
    });
}

// Reusable toast helpers for create flows
function handleCreateSuccess() {
  toastSuccess(`${__("Created Successfully")}`);
}

function handleCreateError(err) {
  const errText = __(err?.messages?.[0]) || __("An unexpected error occurred.");
  toastError(`${__("Error occurred")}: ${errText}`);
}

const navigateToEdit = (row) => {
  router.push({
    name: "EditEmailTemplate",
    params: {
      name: row,
    },
  });
};

// Expose navigation functions for parent components
defineExpose({
  navigateToEdit,
  deleteRecord,
  handleCreateSuccess,
  handleCreateError,
});
</script>
