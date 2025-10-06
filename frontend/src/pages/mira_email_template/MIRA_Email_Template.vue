<template>
	<LayoutHeader>
		<template #left-header>
			<Breadcrumbs :items="breadcrumbs" />
		</template>
		<template #right-header>
			<Button variant="solid" :label="__('Create')" @click="handleCreateClick">
				<template #prefix>
					<FeatherIcon name="plus" class="h-4" />
				</template>
			</Button>
		</template>
	</LayoutHeader>
	<ViewControls :key="componentKey" ref="viewControls" v-model="listData" v-model:loadMore="loadMore"
		v-model:resizeColumn="triggerResize" v-model:updatedPageCount="updatedPageCount"
		:filters="{}" doctype="MIRA_Email_Template" :enableGroupSearch="true" />
	<DataListView ref="dataListView" v-if="listData.data && rows.length" v-model="listData.data.page_length_count"
		v-model:list="listData" :doctype="'MIRA_Email_Template'" :rows="rows" :columns="listData.data?.columns || []"
		:options="{
			showTooltip: false,
			resizeColumn: true,
			rowCount: listData.data?.row_count || 0,
			totalCount: listData.data?.total_count || 0,
		}" @loadMore="() => loadMore++" @columnWidthUpdated="() => triggerResize++"
		@updatePageCount="(count) => (updatedPageCount = count)" @applyFilter="(data) => viewControls.applyFilter(data)"
		@deleteRecord="listData.reload()"
		@selectionsChanged="(selections) => viewControls.updateSelections(selections)" />

	<div v-else-if="listData.data" class="flex h-full items-center justify-center">
		<div class="flex flex-col items-center gap-3 text-xl font-medium text-gray-500">
			<EmailIcon class="h-10 w-10" />
			<span>{{ __("No Data Found") }}</span>
			<Button :label="__('Create')"  @click="handleCreateClick">
				<template #prefix>
					<FeatherIcon name="plus" class="h-4" />
				</template>
			</Button>
		</div>
	</div>

	<!-- <QuickEntryModal v-model="showQuickEntryModal" doctype="MIRA_Email_Template" /> -->
	<!-- Trigger buttons -->
	<!-- <Button @click="showCreateModal = true">Create Template</Button>
  <Button @click="editTemplate(template.name)">Edit Template</Button> -->
</template>

<script setup>
import EmailIcon from "@/components/Icons/EmailIcon.vue";
import LayoutHeader from "@/components/LayoutHeader.vue";
import ViewControls from "@/components/ViewControls.vue";
import DataListView from "@/components/ListViews/MIRA_Email_Template_ListView.vue";


import { Breadcrumbs, Button, createResource } from "frappe-ui";
import { ref, computed, onMounted, reactive, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
// import { usePermissionStore } from "@/stores/permission";

const showModal = ref(false)
const modalMode = ref('create')
const selectedTemplateId = ref('')
const selectedType = ref('')

const editTemplate = (templateId) => {
	selectedTemplateId.value = templateId
	modalMode.value = 'edit'
	showModal.value = true
}

const handleTemplateSaved = (templateData) => {
	// Refresh list, navigate, etc.
	if (templateData.mode === 'edit') {
		// Switch to edit mode after save & continue
		modalMode.value = 'edit'
		selectedTemplateId.value = templateData.name
	}
}

const handleTemplateDeleted = ()=>{

}

const handleModalCancelled = ()=>{

}

// const { can } = usePermissionStore();

// const canCreate = can("MIRA_Email_Template", "create");

const route = useRoute();
const router = useRouter();

const filter = ref({ template_type: '' });
const componentKey = ref(0);

function forceRerender() {
	componentKey.value++;
}

const breadcrumbs = [{ label: __("Email Template"), route: { name: "ListEmailTemplate" } }];

const dataListView = ref(null);
const listData = ref({});
const loadMore = ref(1);
const triggerResize = ref(1);
const updatedPageCount = ref(20);
const viewControls = ref(null);

watch(
	() => route.params,
	(newParams) => {
		console.log(newParams);

		filter.value.template_type = newParams.templateType || "";
		forceRerender(); // Gọi hàm để ép component render lại
	},
	{ immediate: true },
);



const pageLengthCount = computed(() => listData.value?.data?.page_length_count || 20);

const rows = computed(() => {
	if (!listData.value?.data?.data) return [];
	return listData.value?.data.data;
});

const showQuickEntryModal = ref(false);

const handleCreateClick = () => {
	router.push({
		name: "NewEmailTemplate",
		params: { templateType: filter.value.template_type },
	})
};

</script>
