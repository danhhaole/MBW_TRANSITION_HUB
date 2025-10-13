<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  call,
  createResource,
  Textarea,
  TextInput,
  Breadcrumbs,
  Button,
  Select,
  TextEditor,
} from "frappe-ui";
import LayoutHeader from "@/components/LayoutHeader.vue";
import grapesjs from "grapesjs";
import "grapesjs/dist/css/grapes.min.css";

import pluginNewsletter from "grapesjs-preset-newsletter";
import pluginMIRABlocks from "./plugin-mira-blocks";
import { getRandom } from "../../utils";

const route = useRoute();
const router = useRouter();
const isEditMode = computed(() => !!route.params.name);
const saving = ref(false);
const showSendTest = ref(false);
const testEmail = ref("");
const editor = ref(null);
const contentEditorType = ref("grapesjs"); // 'rich' | 'grapesjs'
const richContent = ref("");
const editorTypeOptions = [
  { label: __("Rich Text"), value: "rich" },
  { label: __("Custom Email Template"), value: "grapesjs" },
];
const templateType = [
  { label: __("Confirm"), value: "confirm-email" },
  { label: __("Invited"), value: "invited-email" },
  { label: __("Reject"), value: "reject-email" },
  { label: __("Other"), value: "other-email" },
];

const _template = ref({
  template_id: getRandom(10),
  template_name: "",
  subject: "",
  template_type: "",
  default_template: 0,
  message: "",
  html_content: "",
  css_content: "",
  project_data: "",
  auto_send: 0,
  is_active: 1,
});

// Move breadcrumbs after _template so we can access template_name when editing
const breadcrumbs = computed(() => [
  { label: __("Email Template"), route: { name: "ListEmailTemplate" } },
  {
    label: isEditMode.value
      ? _template.value.template_name || __("Edit Email Template")
      : __("Create Email Template"),
  },
]);

const mergeFields = ref([
  {
    label: __("Candidate"),
    options: [
      { label: __("Full Name"), value: "can_full_name" },
      { label: __("Email"), value: "can_email" },
      { label: __("Phone"), value: "can_phone" },
      { label: __("Resume URL"), value: "can_cv" },
      { label: __("Address"), value: "can_address" },
    ],
  },
  {
    label: __("Job"),
    options: [
      { label: __("Job Title"), value: "jo_public_title" },
      { label: __("Department"), value: "job_department" },
      { label: __("Position"), value: "jo_position" },
      { label: __("Location"), value: "jo_location" },
      { label: __("Contact phone"), value: "jo_contact_phone" },
      { label: __("Contact email"), value: "jo_contact_email" },
      { label: __("Contact person"), value: " jo_contact_person" },
      { label: __("Min salary"), value: " jo_min_salary" },
      { label: __("Max salary"), value: " jo_max_salary" },
    ],
  },
  {
    label: __("Company"),
    options: [
      { label: __("Company Name"), value: "company_name" },
      { label: __("Company Website"), value: "website" },
      { label: __("Company Headquarters"), value: "headquarters" },
      { label: __("Company Industry"), value: "industry" },
      { label: __("Company Founded Year"), value: "founded_year" },
      { label: __("Company Overview"), value: "overview" },
      { label: __("Company Vision"), value: "vision" },
      { label: __("Company Mission"), value: "mission" },
    ],
  },
  // {
  //     "label": "Interview",
  //     "options": [
  //         { "label": "Interview Date", "value": "intv_date" },
  //         { "label": "Interview Time", "value": "intv_time" },
  //         { "label": "Interview Location", "value": "intv_location" },
  //         { "label": "Interview Link", "value": "intv_link" },
  //         { "label": "Interviewer", "value": "intv_interviewer" },
  //         { "label": "Interview Note", "value": "intv_note" }
  //     ]
  // },
  {
    label: __("Links"),
    options: [
      { label: __("Test Link"), value: "quiz_link" },
      { label: __("Interview Link"), value: "interview_link" },
      { label: __("Booking Link"), value: "booking_link" },
      { label: __("Portal Applicant Link"), value: "applicant_portal" },
    ],
  },
  {
    label: __("Links"),
    options: [
      { label: __("Test Link"), value: "quiz_link" },
      { label: __("Interview Link"), value: "interview_link" },
      { label: __("Booking Link"), value: "booking_link" },
      { label: __("Portal Applicant Link"), value: "applicant_portal" },
    ],
  },
]);

// Re-init or teardown editor when switching modes
watch(contentEditorType, async (val, oldVal) => {
  if (val === "grapesjs") {
    await nextTick();
    initEditor();
  } else if (oldVal === "grapesjs") {
    try {
      const html = editor.value?.getHtml?.();
      if (html) richContent.value = html;
      editor.value?.destroy?.();
    } catch (e) {}
    editor.value = null;
    try {
      const el = document.querySelector("#gjs");
      if (el) el.innerHTML = "";
    } catch (e) {}
  }
});

onBeforeUnmount(() => {
  try {
    editor.value?.destroy?.();
  } catch (e) {}
  editor.value = null;
});

onMounted(async () => {
  if (isEditMode.value) {
    const data = await call("frappe.client.get", {
      doctype: "Mira Email Template",
      name: route.params.name,
    });
    _template.value = data;
    // initialize rich content from stored html if any
    richContent.value = _template.value.html_content || "";
  }

  // await loadMergeFields()
  await nextTick();
  if (contentEditorType.value === "grapesjs") {
    initEditor();
  }
});
const goBack = () => {
  router.push({
    name: "ListEmailTemplate",
  });
};

async function loadMergeFields() {
  try {
    await createResource({
      url:
        "mbw_mira.mbw_mira.doctype.mira_email_template.mira_email_template.get_merge_fields",
      auto: true,
      onSuccess: (data) => {
        mergeFields.value = data.map((item) => ({
          label: item.name,
          value: item.jinja_variable,
        }));
      },
    });
  } catch (e) {
    console.error("Lỗi load merge tags", e);
  }
}

function initEditor() {
  // Destroy previous instance if exists
  try {
    editor.value?.destroy?.();
  } catch (e) {}

  // Clear container to avoid stale DOM
  try {
    const el = document.querySelector("#gjs");
    if (el) el.innerHTML = "";
  } catch (e) {}
  editor.value = grapesjs.init({
    container: "#gjs",
    height: "600px",
    width: "auto",
    fromElement: false,
    storageManager: false,
    plugins: [pluginNewsletter, pluginMIRABlocks],
    pluginsOpts: {
      [pluginNewsletter]: {
        modalTitleImport: "Import template",
        modalTitleExport: "Export template",
        codeViewerTheme: "material",
        useCustomTheme: true,
      },
    },
    // Prefer latest richContent if present, otherwise fallback to stored html_content
    components:
      (richContent.value && richContent.value.trim()) ||
      _template.value.html_content ||
      "",
    style: _template.value.css_content || "",
  });

  // Load project_data nếu có
  // if (_template.value.project_data) {
  //     try {
  //         const project = JSON.parse(_template.value.project_data)
  //         editor.value.loadProjectData(project)
  //     } catch (e) {
  //         console.warn('Lỗi project_data:', e)
  //     }
  // }

  // Thêm nút chèn merge tag
  editor.value.Panels.addButton("options", {
    id: "insert-merge-tag",
    className: "fa fa-tag",
    command: "open-merge-tag-popup",
    attributes: { title: "Chèn Merge Tag" },
  });

  // Kích hoạt nút Preview khi vào edit mode lần đầu
  if (isEditMode.value) {
    setTimeout(() => {
      const previewButton = editor.value.Panels.getButton("options", "preview");
      if (previewButton) {
        previewButton.set("active", true);
        editor.value.runCommand("preview");
      }
    });
  }

  editor.value.Commands.add("open-merge-tag-popup", {
    run(editor) {
      const modal = editor.Modal;
      const content = document.createElement("div");

      content.innerHTML = `
                <style>
  .merge-tag-group {
    margin-bottom: 20px;
    padding-bottom: 8px;
    border-bottom: 1px dashed #e0e0e0;
  }
  .merge-tag-group-title {
    font-weight: 600;
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
  }
  .merge-tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .merge-tag-chip {
    background-color: #f3f4f6;
    color: #111827;
    padding: 5px 10px;
    border-radius: 9999px;
    font-size: 13px;
    border: 1px solid #d1d5db;
    cursor: pointer;
    white-space: nowrap;
    transition: background-color 0.2s;
  }
  .merge-tag-chip:hover {
    background-color: #e5e7eb;
  }
</style>

                <div id="merge-tag-groups"></div>
                `;

      const container = content.querySelector("#merge-tag-groups");

      mergeFields.value.forEach((group) => {
        const groupEl = document.createElement("div");
        groupEl.className = "merge-tag-group";

        const titleEl = document.createElement("div");
        titleEl.className = "merge-tag-group-title";
        titleEl.innerText = group.label;
        groupEl.appendChild(titleEl);

        const listEl = document.createElement("div");
        listEl.className = "merge-tag-list";

        group.options.forEach((tag) => {
          const btn = document.createElement("button");
          btn.className = "merge-tag-chip";
          btn.innerText = tag.label;
          btn.onclick = () => {
            const selected = editor.getSelected();
            const insertText = `{{ ${tag.value} }}`;
            if (selected?.is("text") || selected?.is("paragraph")) {
              const current = selected
                .components()
                .map((comp) => comp.toHTML())
                .join("");
              selected.components(current + insertText);
            } else {
              editor.RichTextEditor?.insertHTML?.(insertText);
            }
            modal.close();
          };
          listEl.appendChild(btn);
        });

        groupEl.appendChild(listEl);
        container.appendChild(groupEl);
      });

      modal.setTitle("🔗 Chèn Merge Tag");
      modal.setContent(content);
      modal.open();
    },
  });
}

async function saveTemplate() {
  if (contentEditorType.value === "grapesjs") {
    const html = editor.value?.getHtml?.() || "";
    const css = editor.value?.getCss?.() || "";
    const projectData = editor.value?.getProjectData?.() || {};
    _template.value.html_content = html;
    _template.value.css_content = css;
    _template.value.project_data = JSON.stringify(projectData);
  } else {
    // Rich text mode: save only HTML content produced by TextEditor
    _template.value.html_content = richContent.value || "";
    _template.value.css_content = "";
    _template.value.project_data = "";
  }

  saving.value = true;
  try {
    if (isEditMode.value) {
      await call("frappe.client.set_value", {
        doctype: "Mira Email Template",
        name: route.params.name,
        fieldname: _template.value,
      });
    } else {
      await call("frappe.client.insert", {
        doc: {
          doctype: "Mira Email Template",
          ..._template.value,
        },
      });
    }
    router.back();
  } catch (e) {
    console.error(e);
  } finally {
    saving.value = false;
  }
}

async function sendTestEmail() {
  try {
    await call("frappe.core.doctype.communication.email.send_email", {
      recipients: testEmail.value,
      subject: _template.value.subject,
      content:
        contentEditorType.value === "grapesjs"
          ? editor.value?.getHtml?.()
          : richContent.value,
    });
    alert("Đã gửi email test");
  } catch (e) {
    console.error(e);
    alert("Gửi test thất bại");
  }
}
</script>

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
        <div class="flex space-x-2">
          <Button variant="solid" theme="gray" :disabled="saving" @click="saveTemplate">
            {{ saving ? __("Saving...") : __("Save") }}
          </Button>
        </div>
      </template>
    </LayoutHeader>

    <div class="container mx-auto py-6 space-y-6">
      <!-- Basic Information Card -->
      <div class="rounded-lg">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-lg font-medium mb-1">{{
              __("Template Name")
            }}</label>
            <TextInput
              v-model="_template.template_name"
              :placeholder="__('Enter template name')"
            />
          </div>
          <div>
            <label class="block text-lg font-medium mb-1">{{ __("Type") }}</label>
            <Select
              v-model="_template.template_type"
              :options="templateType"
              size="sm"
              variant="outlined"
              class="bg-gray-100"
              :placeholder="__('Select type')"
            />
          </div>
          <div class="md:col-span-2">
            <label class="block text-sm font-medium mb-1">{{ __("Subject") }}</label>
            <Textarea
              v-model="_template.subject"
              row="3"
              :placeholder="__('Enter email subject')"
            />
          </div>
        </div>
      </div>

      <div class="bg-gray-100">
        <Select
          v-model="contentEditorType"
          :options="editorTypeOptions"
          size="sm"
          variant="outlined"
          class="min-w-40"
          :placeholder="__('Choose editor')"
        />
      </div>

      <!-- Editor Card -->
      <div class="rounded-lg">
        <div class="flex items-center justify-between mb-4"></div>

        <!-- Rich Text Mode -->
        <div v-if="contentEditorType === 'rich'">
          <TextEditor
            variant="outline"
            editor-class="!prose-sm !max-w-full overflow-auto !w-full min-h-[220px] max-h-[500px] py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors"
            :bubbleMenu="true"
            :fixedMenu="true"
            :content="richContent"
            @change="richContent = $event"
          />
        </div>

        <!-- GrapesJS Mode -->
        <div v-else class="flex-1 overflow-hidden">
          <div id="gjs" class="h-full bg-gray-100"></div>
        </div>
      </div>

      <!-- Note Card -->
      <div class="rounded-lg">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">{{ __("Note") }}</h2>
        <Textarea v-model="_template.message" rows="3" :placeholder="__('Enter note')" />
      </div>

      <!-- TEST EMAIL -->
      <!-- <div v-if="showSendTest" class="mt-4 p-4 border rounded bg-gray-50">
        <h3 class="text-lg font-semibold mb-2">📤 Gửi thử Email</h3>
        <TextInput v-model="testEmail" placeholder="Email nhận thử"  />
        <Button @click="sendTestEmail">Gửi thử</Button>
      </div> -->
    </div>
  </div>
</template>

<style>
#gjs {
  border: 1px solid #e5e7eb;
}

#gjs .gjs-pn-panel,
#gjs .gjs-sm-properties,
#gjs .gjs-sm-property {
  background-color: #2c2c2c;
  color: white;
}

#gjs .gjs-field input,
#gjs .gjs-field select {
  color: white;
  background-color: #1e1e1e;
}

#gjs .gjs-field select option {
  color: black;
}
</style>
