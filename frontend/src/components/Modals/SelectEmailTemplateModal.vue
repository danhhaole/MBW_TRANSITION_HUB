<template>
	<Dialog
		v-model="show"
		:options="{
			title: 'Email Notification',
			size: 'xl',
		}"
	>
		<template #body-content>
			<div class="flex flex-col gap-4">
				<!-- Chọn Mẫu Email -->
				<div>
					<FormControl
						type="select"
						:options="emailTemplates"
						v-model="selectedTemplate"
						@change="updateTemplateContent"
						:placeholder="__('Select Email Template')"
						label="Select Email Template"
					/>
				</div>

				<!-- Subject -->
				<div class="flex flex-col gap-1">
					<label class="block text-xs font-medium text-ink-gray-6">
						{{ __("Subject") }}
					</label>
					<FormControl
						ref="subject"
						v-model="displaySubject"
						:placeholder="__('Enter email subject')"
						class="w-full"
					/>
				</div>

				<!-- Content -->
				<div class="flex flex-col gap-1">
					<label class="block text-xs font-medium text-ink-gray-6">
						{{ __("Content") }}
					</label>
					<div class="border border-outline-gray-3 bg-white rounded-md overflow-hidden">
						<TextEditor
							id="email-editor"
							variant="outline"
							ref="message"
							editor-class="!prose-sm !w-full !max-w-full overflow-auto min-h-[250px] max-h-96 p-3 rounded-md bg-white border-none"
							:bubbleMenu="true"
							:fixed-menu="true"
							:extensions="[MergeFieldNode]"
							:content="displayMessage"
							@change="(val) => updateContent(val)"
							:placeholder="__('Enter email content')"
						/>
					</div>
				</div>
			</div>
		</template>

		<template #actions>
			<div class="flex justify-between w-full">
				<!-- Nút Back -->
				<Button variant="ghost" @click="show = false">
					<template #prefix>
						<FeatherIcon name="arrow-left" class="h-4 w-4" />
					</template>
					Back
				</Button>
				<!-- Send Email Button -->
				<Button @click="sendEmail" variant="solid">
					{{
						editMode
							? __("Update Schedule and send Email")
							: __("Create Schedule and Send Email")
					}}
				</Button>
			</div>
		</template>
	</Dialog>
</template>

<script setup>
import { ref, watch, onMounted, computed } from "vue";
import { call, Dialog, FormControl, TextEditor, Button, createResource } from "frappe-ui";
import { Node } from "@tiptap/core";

const props = defineProps({
	editMode: {
		type: Boolean,
		default: false,
	},
});

const show = defineModel();
const emailTemplates = ref([]);
const selectedTemplate = ref(null);
const selectedTemplateData = ref({ subject: "", message: "" });
const mergeFields = ref([]);
const emit = defineEmits(["update"]);

const activeField = ref("message");

// Fetch danh sách mẫu email và Merge Fields
onMounted(async () => {
	const response = await call("frappe.client.get_list", {
		doctype: "Mira Email Template",
		fields: ["name", "subject", "message", "template_name"],
	});
	emailTemplates.value = response.map((item) => ({
		label: item.template_name,
		value: item.name,
		subject: item.subject,
		message: item.message,
	}));

	// Fetch Merge Fields
	const mergerResponse = await createResource({
			url: "mbw_mira.mbw_mira.doctype.mira_merge_field_list.mira_merge_field_list.get_merge_fields",
			auto: true,
			onSuccess: (data) => {
				mergeFields.value = data?.map((item) => ({
					name: item.name,
					jinja_variable: item.jinja_variable,
				}));
			},
		});

	// Chọn mẫu đầu tiên mặc định
	if (emailTemplates.value.length > 0) {
		selectedTemplate.value = emailTemplates.value[0].value;
		updateTemplateContent();
	}
});

// Cập nhật nội dung khi chọn mẫu email
const updateTemplateContent = () => {
	const template = emailTemplates.value.find((t) => t.value === selectedTemplate.value);
	if (template) {
		selectedTemplateData.value.subject = template.subject;
		selectedTemplateData.value.message = template.message;
	}
};

// Hiển thị Subject & Message với Merge Field
const displaySubject = computed({
	get() {
		return convertJinjaToPlaceholder(selectedTemplateData.value.subject);
	},
	set(val) {
		selectedTemplateData.value.subject = convertPlaceholderToJinja(val);
	},
});
const displayMessage = computed({
	get() {
		return convertJinjaToHTML(selectedTemplateData.value.message);
	},
	set(val) {
		selectedTemplateData.value.message = convertHTMLToJinja(val);
	},
});

// Cập nhật nội dung khi thay đổi Message
const updateContent = (val) => {
	selectedTemplateData.value.message = convertHTMLToJinja(val);
};

// Chuyển đổi Jinja → Placeholder
function convertJinjaToPlaceholder(text) {
	if (!text) return "";
	mergeFields.value.forEach((field) => {
		text = text.replaceAll(field.jinja_variable, `[${field.name}]`);
	});
	return text;
}

// Chuyển đổi Placeholder → Jinja
function convertPlaceholderToJinja(text) {
	if (!text) return "";
	mergeFields.value.forEach((field) => {
		text = text.replaceAll(`[${field.name}]`, field.jinja_variable);
	});
	return text;
}

// Chuyển đổi Jinja → HTML
function convertJinjaToHTML(text) {
	if (!text) return "";
	mergeFields.value.forEach((field) => {
		const tag = `<span data-merge-field="${field.name}" class="bg-blue-100 text-blue-700 px-2 py-1 rounded-md font-medium">${field.name}</span>`;
		text = text.replaceAll(field.jinja_variable, tag);
	});
	return text;
}

// Chuyển đổi HTML → Jinja
function convertHTMLToJinja(text) {
	if (!text) return "";
	mergeFields.value.forEach((field) => {
		const regex = new RegExp(
			`<span[^>]*data-merge-field="${field.name}"[^>]*>.*?</span>`,
			"g",
		);
		text = text.replace(regex, field.jinja_variable);
	});
	return text;
}

// Tạo Custom Node cho Merge Field
const MergeFieldNode = Node.create({
	name: "mergeField",
	group: "inline",
	inline: true,
	atom: true,

	addAttributes() {
		return {
			field: { default: "" },
		};
	},

	parseHTML() {
		return [
			{
				tag: "span[data-merge-field]",
				getAttrs: (dom) => {
					return { field: dom.getAttribute("data-merge-field") };
				},
			},
		];
	},

	renderHTML({ node }) {
		return [
			"span",
			{
				"data-merge-field": node.attrs.field,
				class: "bg-blue-100 text-blue-700 px-2 py-1 rounded-md font-medium",
			},
			node.attrs.field,
		];
	},
});

// Gửi Email
const sendEmail = async () => {
	emit("update", {
		subject: selectedTemplateData.value.subject,
		template: selectedTemplate.value,
		message: convertHTMLToJinja(selectedTemplateData.value.message),
	});
	show.value = false;
};
</script>
