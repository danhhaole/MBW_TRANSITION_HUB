<template>
	<div
		v-if="title !== 'Data'"
		class="mx-4 my-3 flex items-center justify-between text-lg font-medium sm:mx-10 sm:mb-4 sm:mt-8"
	>
		<div class="flex h-8 items-center text-xl font-semibold text-gray-800">
			{{ __(title) }}
		</div>
		<Button v-if="title == 'Comments'" variant="solid" @click="emailBox.showComment = true">
			<template #prefix>
				<FeatherIcon name="plus" class="h-4 w-4" />
			</template>
			<span>{{ __("New Comment") }}</span>
		</Button>
		<Button
			v-else-if="title == 'Attachments'"
			variant="solid"
			@click="showFilesUploader = true"
		>
			<template #prefix>
				<FeatherIcon name="plus" class="h-4 w-4" />
			</template>
			<span>{{ __("Upload Attachment") }}</span>
		</Button>
		<Dropdown v-else :options="defaultActions" @click.stop>
			<template v-slot="{ open }">
				<Button variant="solid" class="flex items-center gap-1">
					<template #prefix>
						<FeatherIcon name="plus" class="h-4 w-4" />
					</template>
					<span>{{ __("New") }}</span>
					<template #suffix>
						<FeatherIcon
							:name="open ? 'chevron-up' : 'chevron-down'"
							class="h-4 w-4"
						/>
					</template>
				</Button>
			</template>
		</Dropdown>
	</div>
</template>
<script setup>
import CommentIcon from "@/components/Icons/CommentIcon.vue";
import AttachmentIcon from "@/components/Icons/AttachmentIcon.vue";
import { Dropdown } from "frappe-ui";
import { computed, h } from "vue";
import { FeatherIcon, Button } from "frappe-ui";

const props = defineProps({
	tabs: Array,
	title: String,
	doc: Object,
	modalRef: Object,
	emailBox: Object,
});

const tabIndex = defineModel();
const showFilesUploader = defineModel("showFilesUploader");

const defaultActions = computed(() => {
	let actions = [
		{
			icon: h(CommentIcon, { class: "h-4 w-4" }),
			label: __("New Comment"),
			onClick: () => (props.emailBox.showComment = true),
		},
		{
			icon: h(AttachmentIcon, { class: "h-4 w-4" }),
			label: __("Upload Attachment"),
			onClick: () => (showFilesUploader.value = true),
		},
	];
	return actions.filter((action) => (action.condition ? action.condition() : true));
});
</script>

