<script setup>
import { ref, onMounted } from "vue";
import { X, Plus } from "lucide-vue-next";
import { Dialog, Button, Autocomplete, toast, call } from "frappe-ui";
import { createToast } from "@/utils/";

const props = defineProps({
	docname: String,
	doctype: String,
	modelValue: [Array, String], // Accept cả mảng hoặc chuỗi
	isTalentView: {
		type: Boolean,
		default: false,
	},
});

const emit = defineEmits(["update:modelValue"]);

const rawValue = props.modelValue || [];

// Khởi tạo tags
const tags = ref(
	Array.isArray(rawValue)
		? [...rawValue]
		: String(rawValue)
				.split(",")
				.map((tag) => tag.trim())
				.filter(Boolean)
				.map((tag) => ({
					label: tag,
					value: tag,
					color: null,
				})),
);

const dialog = ref(false);
const selectedTags = ref([]);
const suggestions = ref([]);

// 🟢 Đồng bộ màu sắc cho tag hiện có
const syncTagColors = async () => {
	const res = await call("frappe.client.get_list", {
		doctype: "Mira Tag",
		fields: ["name", "title", "color"],
	});

	const colorMap = {};
	for (const item of res || []) {
		colorMap[item.title] = item.color;
	}

	tags.value = tags.value.map((tag) => ({
		...tag,
		color: colorMap[tag.value] || null,
	}));
};

// Gọi khi mounted component
onMounted(() => {
	syncTagColors();
});

const fetchSuggestions = async () => {
	const res = await call("frappe.client.get_list", {
		doctype: "Mira Tag",
		fields: ["name", "title", "color"],
		order_by: "title asc",
		limit_page_length: 50
	});

	suggestions.value = (res || []).map((tag) => ({
		label: tag.title,
		value: tag.title,
		color: tag.color || "#A1A1AA",
	}));
};

const openDialog = () => {
	selectedTags.value = [];
	dialog.value = true;
	fetchSuggestions();
};

const addTags = async () => {
	const newTags = selectedTags.value.filter(
		(tag) => !tags.value.find((t) => t.value === tag.value),
	);

	if (newTags.length === 0) {
		createToast({
			title: "Info",
			text: "Tất cả thẻ đã tồn tại",
			icon: "info",
			iconClasses: "bg-surface-blue-3 text-ink-white rounded-md p-px",
		});
		dialog.value = false;
		return;
	}

	for (const tag of newTags) {
		await call("frappe.desk.doctype.tag.tag.add_tag", {
			tag: tag.value,
			dt: props.doctype,
			dn: props.docname,
		});
		tags.value.push(tag);
	}

	emit("update:modelValue", [...tags.value]);

	createToast({
		title: "Success",
		text: "Đã thêm thẻ thành công",
		icon: "check",
		iconClasses: "bg-surface-green-3 text-ink-white rounded-md p-px",
	});

	dialog.value = false;
};

const removeTag = async (tag) => {
	await call("frappe.desk.doctype.tag.tag.remove_tag", {
		tag: tag.value,
		dt: props.doctype,
		dn: props.docname,
	});

	tags.value = tags.value.filter((t) => t.value !== tag.value);
	emit("update:modelValue", [...tags.value]);

	createToast({
		title: "Success",
		text: "Đã xoá thẻ",
		icon: "check",
		iconClasses: "bg-surface-green-3 text-ink-white rounded-md p-px",
	});
};
</script>

<template>
	<div :class="{'flex items-center gap-2': isTalentView}">
		<div class="mb-0.5 text-xs text-gray-500 flex items-center gap-2">
			{{ __("Tags") }}
            <!-- Dấu + mở dialog -->
			<div
				class="flex items-center justify-center w-7 h-7 rounded-md border border-dashed border-gray-300 text-gray-500 hover:bg-gray-50 cursor-pointer"
				@click="openDialog"
			>
				<Plus class="w-4 h-4" />
			</div>
		</div>

		<div class="flex items-center flex-wrap gap-2">
			<div
				v-for="tag in tags"
				:key="tag.value"
				class="flex items-center px-2 py-1 rounded-md text-white text-sm"
				:style="{ backgroundColor: tag.color || '#A1A1AA' }"
			>
				{{ tag.label }}
				<X class="stroke-1.5 w-3 h-3 ml-2 cursor-pointer" @click="removeTag(tag)" />
			</div>

			
		</div>

		<!-- Dialog chọn thẻ -->
		<Dialog v-model="dialog">
			<template #body-title>
				<h3 class="text-lg font-medium">{{ __("Chọn thẻ gắn vào ứng viên") }}</h3>
			</template>

			<template #body-content>
				<Autocomplete
					v-model="selectedTags"
					:options="suggestions"
					placeholder="Chọn thẻ"
					:multiple="true"
				>
					<template #item-prefix="{ option }">
						<div
							class="w-3 h-3 rounded-full mr-2"
							:style="{ backgroundColor: option.color || '#A1A1AA' }"
						></div>
					</template>

					<template #item-suffix="{ option }">
						<!-- Checkmark nếu đang được chọn -->
						<div v-if="selectedTags.find((t) => t.value === option.value)">
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-4 w-4 text-green-500"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M5 13l4 4L19 7"
								/>
							</svg>
						</div>
					</template>
				</Autocomplete>
			</template>

			<template #actions>
				<div class="flex justify-end">
					<Button variant="solid" @click="addTags"> OK </Button>
					<Button variant="subtle" class="ml-2" @click="dialog = false"> Huỷ </Button>
				</div>
			</template>
		</Dialog>
	</div>
</template>
