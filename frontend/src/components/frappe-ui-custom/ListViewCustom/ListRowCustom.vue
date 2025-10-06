<template>
	<component
		:is="list.options.getRowRoute ? 'router-link' : 'div'"
		:class="{ 'cursor-pointer': isHoverable }"
		class="flex flex-col transition-all duration-300 ease-in-out relative group"
		v-bind="{
			to: list.options.getRowRoute ? list.options.getRowRoute(row) : undefined,
			onClick: list.options.onRowClick ? () => list.options.onRowClick(row) : undefined,
		}"
	>
		<!-- Nút ở cuối hàng, hiển thị khi hover và cố định ở bên phải -->
		<div class="absolute right-1 top-1/2 -translate-y-1/2 duration-300">
			<!-- Nút của bạn -->
			<div class="flex gap-2">
				<Dropdown :options="quickOptions(quickOptions, row)">
					<Button icon="more-vertical" class="text-gray-600" variant="ghost" />
				</Dropdown>
			</div>
		</div>
		<component
			:is="list.options.getRowRoute ? 'template' : 'button'"
			class="[all:unset] hover:[all:unset]"
		>
			<div
				class="grid items-center space-x-4 rounded px-2 py-2"
				:class="[
					isSelected ? 'bg-gray-100' : '',
					isHoverable ? (isSelected ? 'hover:bg-gray-200' : 'hover:bg-gray-50') : '',
				]"
				:style="{
					minHeight: rowHeight,
					gridTemplateColumns: getGridTemplateColumns(
						list.columns,
						list.options.selectable,
					),
				}"
			>
				<Checkbox
					v-if="list.options.selectable"
					:modelValue="list.selections.has(row[list.rowKey])"
					@click.stop="list.toggleRow(row[list.rowKey])"
					class="cursor-pointer duration-300"
				/>
				<div
					v-for="(column, i) in list.columns"
					:key="column.key"
					:class="[
						alignmentMap[column.align],
						i == 0 ? 'text-gray-900' : 'text-gray-700',
					]"
				>
					<slot v-bind="{ idx: i, column, item: row[column.key] }">
						<component
							v-if="list.slots.cell"
							:is="list.slots.cell"
							v-bind="{
								column,
								row,
								item: row[column.key],
								align: column.align,
							}"
						/>
						<ListRowItem
							v-else
							:column="column"
							:row="row"
							:item="row[column.key]"
							:align="column.align"
						/>
					</slot>
				</div>
			</div>

			<div v-if="!isLastRow" class="mx-2 h-px border-t border-gray-200" />
		</component>
		
		<!-- Dialog hiển thị thông tin chi tiết -->
		<Dialog
			v-model="testDialog"
			:options="{
				size: '3xl',
				title: 'Cap nhat ho so nhan su',
			}"
		>
			<template #body-content>
				<Tabs v-model="tabIndex" :tabs="tabs">
					<template #default="{ tab }">
						<div class="p-5">
							<div class="grid gap-4 grid-cols-2">
								<div v-for="field in tab.fields" :key="field.name">
									<FormControlCustom
										v-if="field.type == 'Data'"
										:type="'text'"
										size="sm"
										variant="subtle"
										:label="field.label"
										:value="getFieldValue(field.label)"
										@input="(e) => setFieldValue(field.label, e.target.value)"
									/>
									<FormControlCustom
										v-else-if="field.type == 'Select'"
										type="select"
										:options="field.options"
										size="sm"
										variant="subtle"
										:label="field.label"
										:value="getFieldValue(field.label)"
										@input="(e) => setFieldValue(field.label, e.target.value)"
									/>
									<FormControl
										v-else-if="field.type == 'Date'"
										:type="'date'"
										size="sm"
										variant="subtle"
										:label="field.label"
										:value="getFieldValue(field.label)"
										@input="(e) => setFieldValue(field.label, e.target.value)"
									/>
								</div>
							</div>
						</div>
					</template>
				</Tabs>
			</template>
			<template #actions>
				<div class="flex flex-row-reverse gap-2">
					<Button
						variant="solid"
						label="Cập nhật"
						:loading="isInfoEmployeeCreating"
						@click="onCreateInfoEmployee"
					/>
				</div>
			</template>
		</Dialog>
	</component>

	<!-- Email Modal - Chỉ render khi cần thiết và với key unique -->
	<SendEmailModal 
		v-if="showEmailModal"
		:key="`email-modal-${selectedCandidateId}`"
		v-model="showEmailModal" 
		:candidate="selectedCandidate" 
		:job-title="jobTitle"
		:job-opening-id="jobOpeningId"
		@email-sent="handleEmailSent" 
		@draft-saved="handleDraftSaved" 
	/>
</template>

<script setup>
import {
	Checkbox,
	ListRowItem,
	Button,
	createResource,
	Dropdown,
	createListResource,
	Dialog,
	FormControl,
	Tabs,
} from "frappe-ui";
import { alignmentMap, getGridTemplateColumns } from "./utils";
import { computed, inject, onMounted, ref, nextTick } from "vue";
import FormControlCustom from "../FormControlCustom/FormControlCustom.vue";
import { useRoute, useRouter } from "vue-router";
import { useFieldStore } from "../../../stores/activeRecord";
import SendEmailModal from "@/components/Modals/SendEmailModal.vue";

const fieldStore = useFieldStore();
const router = useRouter();
const route = useRoute();

const props = defineProps({
	row: {
		type: Object,
		required: true,
	},
});

const testDialog = ref(false);
const list_data_staff = ref([]);
const tabs = computed(() => {
	return list_data_staff.value;
});

const tabIndex = ref(0);

const list = inject("list");
const hideEdit = inject("hideEdit");
const hideDelete = inject("hideDelete");
const showEmail = inject("showEmail");

// Email Modal State - Improved management
const showEmailModal = ref(false);
const selectedCandidate = ref({});
const jobTitle = ref('Frontend Developer');
const jobOpeningId = ref('');

// Computed để tạo unique key cho modal
const selectedCandidateId = computed(() => {
	return selectedCandidate.value?.name || selectedCandidate.value?.can_email || 'default';
});

const detailViewRoute = computed(() => {
	return "EmployeeDetailView";
});

const isLastRow = computed(() => {
	if (!list.value.rows?.length) return false;
	return (
		list.value.rows[list.value.rows.length - 1][list.value.rowKey] ===
		props.row[list.value.rowKey]
	);
});

const isSelected = computed(() => {
	return list.value.selections.has(props.row[list.value.rowKey]);
});

const isHoverable = computed(() => {
	return list.value.options.getRowRoute || list.value.options.onRowClick;
});

const rowHeight = computed(() => {
	if (typeof list.value.options.rowHeight === "number") {
		return `${list.value.options.rowHeight}px`;
	}
	return list.value.options.rowHeight;
});

function quickOptions(action, row) {
    let options = [];
    
    // Add 'Edit' option if not hidden
    if (!hideEdit) {
        options.push({
            label: __('Edit'),
            icon: "edit",
            onClick: () => actionQuickEditRow(row?.name),
        });
    }

    // Add 'Delete' option if not hidden
    if (!hideDelete) {
        options.push({
            label: __('Delete'),
            icon: "trash",
            onClick: () => actionQuickDeleteRow(row?.name),
        });
    }
	
	if (showEmail) {
		options.push({
			label: __('Send Email'),
			icon: "mail",
			onClick: () => actionShowEmail(row),
		});
	}

    return options;
}

const actionQuickDeleteRow = (name) => {
	console.log('Delete:', name);
	fieldStore.setChildTableField(name, 'delete');
};

const actionQuickEditRow = (name) => {
	console.log('Edit:', name);
	fieldStore.setChildTableField(name, 'edit');
};

const actionShowEmail = async (row) => {
	try {
		// Đảm bảo modal được đóng trước khi mở lại
		if (showEmailModal.value) {
			showEmailModal.value = false;
			await nextTick(); // Đợi DOM update
		}
		
		// Set candidate data
		selectedCandidate.value = { ...row }; // Clone object để tránh reference issues
		
		// Set job data nếu có
		if (route.params.jobId) {
			jobOpeningId.value = route.params.jobId;
		}
		
		// Mở modal sau khi set data
		await nextTick();
		showEmailModal.value = true;
		
		console.log('Opening email modal for candidate:', selectedCandidate.value);
	} catch (error) {
		console.error('Error opening email modal:', error);
	}
};

const handleEmailSent = (emailData) => {
	console.log('Email sent successfully:', emailData);
	
	// Reset modal state
	showEmailModal.value = false;
	selectedCandidate.value = {};
	
	// Có thể emit event lên parent component để refresh data
	// emit('email-sent', emailData);
};

const handleDraftSaved = (draftData) => {
	console.log('Draft saved successfully:', draftData);
	
	// Có thể emit event lên parent component
	// emit('draft-saved', draftData);
};

// Cleanup khi component unmount
import { onBeforeUnmount } from "vue";

onBeforeUnmount(() => {
	showEmailModal.value = false;
	selectedCandidate.value = {};
});
</script>