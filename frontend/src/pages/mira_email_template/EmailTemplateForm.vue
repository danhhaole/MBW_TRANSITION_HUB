<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import { call, createResource, Textarea, TextInput } from "frappe-ui";
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

onMounted(async () => {
  if (isEditMode.value) {
    const data = await call("frappe.client.get", {
      doctype: "MIRA_Email_Template",
      name: route.params.name,
    });
    _template.value = data;
  }

  // await loadMergeFields()
  await nextTick();
  initEditor();
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
    components: _template.value.html_content || "",
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
  const html = editor.value.getHtml();
  const css = editor.value.getCss();
  const projectData = editor.value.getProjectData();

  _template.value.html_content = html;
  _template.value.css_content = css;
  _template.value.project_data = JSON.stringify(projectData);

  saving.value = true;
  try {
    if (isEditMode.value) {
      await call("frappe.client.set_value", {
        doctype: "MIRA_Email_Template",
        name: route.params.name,
        fieldname: _template.value,
      });
    } else {
      await call("frappe.client.insert", {
        doc: {
          doctype: "MIRA_Email_Template",
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
      content: editor.value.getHtml(),
    });
    alert("Đã gửi email test");
  } catch (e) {
    console.error(e);
    alert("Gửi test thất bại");
  }
}
</script>

<template>
  <div class="h-screen flex flex-col overflow-hidden">
    <!-- Header -->
    <div
      class="sticky top-0 bg-white z-50 border-b px-4 py-3 flex items-center justify-between"
    >
      <div class="flex items-center space-x-4">
        <Button variant="outline" theme="gray" @click="goBack">
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
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </template>
          {{ __("Back") }}
        </Button>
        <h2 class="text-2xl font-bold">
          {{ isEditMode ? __("Edit Email Template") : __("Create Email Template") }}
        </h2>
      </div>
      <div class="flex space-x-2">
        <Button variant="outline" :disabled="saving" @click="saveTemplate">
          {{ saving ? __("Saving...") : __("💾 Save Template") }}
        </Button>
        <!-- <Button variant="outline" @click="showSendTest = !showSendTest">📨 Test Email</Button> -->
      </div>
    </div>
    <div class="container mx-auto flex-1 overflow-y-auto px-5 space-y-4">
      <!-- THÔNG TIN -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-medium mb-1">{{ __("Template Name") }}</label>
          <TextInput v-model="_template.template_name" />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1">{{ __("Type") }}</label>
          <select v-model="_template.template_type" class="form-select w-full">
            <option value="confirm-email">Confirm</option>
            <option value="invited-email">Invited</option>
            <option value="reject-email">Reject</option>
            <option value="other-email">Other</option>
          </select>
        </div>
        <!-- <div>
                    <label class="block text-sm font-medium mb-1">Đơn vị</label>
                    <TextInput v-model="_template.unit_name"  />
                </div> -->
      </div>
      <div>
        <label class="block text-sm font-medium mb-1">{{ __("Subject") }}</label>
        <Textarea v-model="_template.subject" row="3" />
      </div>
      <!-- EDITOR -->
      <div>
        <label class="block text-sm font-medium mb-2">{{ __("Content") }}</label>
        <div class="flex-1 overflow-hidden">
          <div id="gjs" class="h-full"></div>
        </div>
      </div>

      <!-- GHI CHÚ -->
      <div>
        <label class="block text-sm font-medium mb-1">{{ __("Note") }}</label>
        <Textarea v-model="_template.message" rows="3" />
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
