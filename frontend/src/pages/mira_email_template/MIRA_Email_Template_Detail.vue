<template>
  <div class="h-screen w-full flex flex-col">
    <!-- Header -->
    <div class="bg-white border-b px-4 py-3 flex items-center justify-between">
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
        <div>
          <h1 class="text-lg font-semibold">
            {{ _template?.template_name || __("Email Template Editor") }}
          </h1>
          <p class="text-sm text-gray-500">{{ getEmailTypeDisplay() }}</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <Button variant="outline" theme="gray" @click="openAIModal">
          {{ __("Generate With AI") }}
        </Button>
        <!-- <Button 
					variant="outline" 
					theme="green" 
					@click="previewEmail"
				>
					{{ __('Preview') }}
				</Button> -->
        <Button variant="outline" theme="gray" @click="showEditModal = true">
          {{ __("Edit Info") }}
        </Button>
        <Button variant="outline" theme="gray" @click="forceReload" :loading="reloading">
          {{ __("Reload") }}
        </Button>
        <Button variant="outline" theme="gray" @click="saveContent" :loading="loading">
          {{ __("Save") }}
        </Button>
        <Button variant="solid" theme="blue" @click="exportHtml" :loading="exporting">
          {{ isEditMode ? __("Update Template") : __("Create Template") }}
        </Button>
      </div>
    </div>

    <!-- Email Editor Component -->
    <EmailEditor
      ref="emailEditor"
      :initial-content="editorInitialContent"
      :initial-css="editorInitialCss"
      :merge-fields="mergeFields"
      :template-type="''"
      :show-merge-fields="true"
      :auto-load-merge-fields="true"
      @content-change="handleContentChange"
      @css-change="handleCssChange"
      @editor-ready="handleEditorReady"
      @merge-fields-loaded="handleMergeFieldsLoaded"
    />
  </div>

  <!-- Edit Info Modal -->
  <Dialog v-model="showEditModal" :options="{ size: 'lg' }">
    <template #body-title>
      <h3
        class="flex items-center gap-2 text-2xl font-semibold leading-6 text-ink-gray-9"
      >
        <div>{{ __("Edit Template Info") }}</div>
      </h3>
    </template>
    <template #body-content>
      <div class="space-y-4">
        <!-- Template Name -->
        <FormControl
          type="text"
          :label="__('Template Name')"
          v-model="_template.template_name"
          required
        />

        <!-- Subject -->
        <FormControl
          type="text"
          :label="__('Subject')"
          v-model="displaySubject"
          @input="_template.subject = convertPlaceholderToJinja($event.target.value)"
        />

        <!-- Using Unit -->
        <!-- <div class="flex flex-col gap-1.5">
                    <span class="block text-xs text-ink-gray-5">
                        {{ __("Using Unit") }}
                    </span>
                    <Link
                        class="form-control"
                        :value="_template.unit_name"
                        doctype="_Unit"
                        @change="(option) => (_template.unit_name = option)"
                        :placeholder="__('Select Unit')"
                        :hideMe="true"
                    >
                        <template #prefix> </template>
                        <template #item-prefix="{ option }"> </template>
                        <template #item-label="{ option }">
                            {{ option.label }}
                        </template>
                    </Link>
                </div> -->

        <!-- Status -->
        <FormControl
          :label="__('Status')"
          v-model="_template.is_active"
          type="select"
          :options="[
            { label: 'Active', value: '1' },
            { label: 'Inactive', value: '0' },
          ]"
        />

        <!-- Auto Send -->
        <Checkbox
          v-model="_template.auto_send"
          :label="
            __('Automatically send email to candidates upon adding them to the system')
          "
        />
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" theme="gray" @click="showEditModal = false">
          {{ __("Cancel") }}
        </Button>
        <Button
          variant="solid"
          theme="blue"
          @click="handleEditInfoSave"
          :loading="loading"
        >
          {{ __("Save") }}
        </Button>
      </div>
    </template>
  </Dialog>

  <!-- EmailAI Modal -->
  <EmailAIModal
    v-if="showAIModal"
    v-model="showAIModal"
    :emailType="getEmailTypeDisplay()"
    :templateType="route.params.templateType"
    @generated="handleAIGenerated"
  />

  <!-- Preview Modal -->
  <Dialog v-model="showPreview" :options="{ size: '4xl' }">
    <template #body-title>
      <h3 class="flex items-center gap-2 text-xl font-semibold leading-6 text-ink-gray-9">
        <div>{{ __("Email Preview") }}</div>
      </h3>
    </template>
    <template #body-content>
      <div class="space-y-4">
        <!-- Subject Preview -->
        <div class="p-3 bg-gray-50 rounded-lg border">
          <div class="text-sm font-medium text-gray-600 mb-1">{{ __("Subject:") }}</div>
          <div class="text-base font-medium">{{ displaySubject || "No subject" }}</div>
        </div>

        <!-- Email Content Preview -->
        <div class="border rounded-lg">
          <div class="bg-gray-50 px-4 py-2 border-b">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-600">{{
                __("Email Content")
              }}</span>
              <div class="flex space-x-2">
                <button
                  @click="previewMode = 'desktop'"
                  :class="
                    previewMode === 'desktop'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500'
                  "
                  class="px-2 py-1 text-xs rounded"
                >
                  🖥️ Desktop
                </button>
                <button
                  @click="previewMode = 'mobile'"
                  :class="
                    previewMode === 'mobile'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500'
                  "
                  class="px-2 py-1 text-xs rounded"
                >
                  📱 Mobile
                </button>
              </div>
            </div>
          </div>
          <div class="p-4 bg-white">
            <div
              :class="previewMode === 'mobile' ? 'max-w-sm mx-auto' : 'w-full'"
              class="transition-all duration-200"
            >
              <div
                v-html="previewHtml"
                class="border rounded p-4 bg-white"
                style="font-family: Arial, sans-serif"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" theme="gray" @click="showPreview = false">
          {{ __("Close") }}
        </Button>
        <Button variant="solid" theme="blue" @click="exportHtml">
          {{ isEditMode ? __("Update Template") : __("Create Template") }}
        </Button>
      </div>
    </template>
  </Dialog>

  <!-- Send Preview Modal -->
  <Dialog v-model="showSendModal" :options="{ size: '4xl' }">
    <template #body-title>
      <h3 class="flex items-center gap-2 text-xl font-semibold leading-6 text-ink-gray-9">
        <div>{{ __("Send Email Preview") }}</div>
      </h3>
    </template>
    <template #body-content>
      <div class="space-y-4">
        <!-- Email Recipients -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">{{
              __("Send To")
            }}</label>
            <FormControl
              type="email"
              v-model="previewEmail.to"
              :placeholder="__('Enter email address')"
              required
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">{{
              __("From Name")
            }}</label>
            <FormControl
              type="text"
              v-model="previewEmail.fromName"
              :placeholder="__('Your Name')"
            />
          </div>
        </div>

        <!-- Sample Data for Merge Fields -->
        <div class="border rounded-lg p-4 bg-gray-50">
          <h4 class="text-sm font-medium text-gray-700 mb-3">
            {{ __("Sample Data for Merge Fields") }}
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-40 overflow-y-auto">
            <div
              v-for="field in mergeFields"
              :key="field.name"
              class="flex items-center space-x-2"
            >
              <label
                :for="field.name"
                class="text-xs font-medium text-gray-600 w-24 truncate"
              >
                {{ field.name }}:
              </label>
              <FormControl
                :id="field.name"
                type="text"
                v-model="sampleData[field.name]"
                :placeholder="__('Sample value')"
                class="flex-1 text-sm"
              />
            </div>
          </div>
        </div>

        <!-- Email Preview -->
        <div class="border rounded-lg">
          <div class="bg-gray-50 px-4 py-2 border-b">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-gray-600">{{
                __("Email Preview with Sample Data")
              }}</span>
              <div class="flex space-x-2">
                <button
                  @click="sendPreviewMode = 'desktop'"
                  :class="
                    sendPreviewMode === 'desktop'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500'
                  "
                  class="px-2 py-1 text-xs rounded"
                >
                  🖥️ Desktop
                </button>
                <button
                  @click="sendPreviewMode = 'mobile'"
                  :class="
                    sendPreviewMode === 'mobile'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-500'
                  "
                  class="px-2 py-1 text-xs rounded"
                >
                  📱 Mobile
                </button>
              </div>
            </div>
          </div>

          <!-- Subject with Sample Data -->
          <div class="px-4 py-3 bg-white border-b">
            <div class="text-sm font-medium text-gray-600 mb-1">{{ __("Subject:") }}</div>
            <div class="text-base font-medium">{{ previewSubjectWithData }}</div>
          </div>

          <!-- Email Content with Sample Data -->
          <div class="p-4 bg-white">
            <div
              :class="sendPreviewMode === 'mobile' ? 'max-w-sm mx-auto' : 'w-full'"
              class="transition-all duration-200"
            >
              <div
                v-html="previewContentWithData"
                class="border rounded p-4 bg-white"
                style="font-family: Arial, sans-serif"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template #actions>
      <div class="flex justify-end space-x-2">
        <Button variant="outline" theme="gray" @click="showSendModal = false">
          {{ __("Cancel") }}
        </Button>
        <Button variant="outline" theme="blue" @click="refreshPreview">
          {{ __("Refresh Preview") }}
        </Button>
        <Button
          variant="solid"
          theme="purple"
          @click="sendTestEmail"
          :loading="sendingEmail"
        >
          {{ __("Send Test Email") }}
        </Button>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { Button, Dialog, FormControl, Checkbox, createResource, call } from "frappe-ui";
import { createToast } from "@/utils";
import Link from "@/components/Controls/Link.vue";
import { getRandom } from "../../utils";
import EmailAIModal from "@/components/Modals/EmailAIModal.vue";
import EmailEditor from "@/components/EmailEditor/EmailEditor.vue";

const route = useRoute();
const router = useRouter();

const emailEditor = ref(null);
const exporting = ref(false);
const reloading = ref(false);
const loading = ref(false);
const showEditModal = ref(false);
const showAIModal = ref(false);
const showPreview = ref(false);
const previewHtml = ref("");
const previewMode = ref("desktop");
const mergeFields = ref([]);
const showSendModal = ref(false);
const editorInitialContent = ref("");
const editorInitialCss = ref("");
const sendPreviewMode = ref("desktop");
const sampleData = ref({});
const sendingEmail = ref(false);
const hasAutoPreviewed = ref(false);
// const previewEmail = ref({
//     to: '',
//     fromName: 'HR Team'
// })

const templateId = computed(() => route.params.id || null);
const isEditMode = computed(() => templateId.value !== null);

const _template = ref({
  template_id: getRandom(10) || "",
  template_name: "",
  subject: "",
  template_type: "",
  unit_name: "",
  is_active: 1,
  auto_send: 0,
  message: "",
  mjml_content: "",
  default_template: 0,
});

// Load template data
const loadTemplateData = async () => {
  try {
    if (isEditMode.value) {
      const data = await call("frappe.client.get", {
        doctype: "Mira Email Template",
        name: templateId.value,
      });
      _template.value = data;

      // Set initial content for editor
      editorInitialContent.value = data?.mjml_content || data?.message || "";
      editorInitialCss.value = data?.css || "";

      return data;
    }
    return null;
  } catch (error) {
    console.error("Error loading template data:", error);
    createToast({
      title: "Error",
      text: "Failed to load template data",
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
};

// Load merge fields
const loadMergeFields = async () => {
  try {
    const response = await createResource({
      url:
        "mbw_mira.mbw_mira.doctype.mira_email_template.mira_email_template.get_merge_fields",
      auto: true,
      onSuccess: (data) => {
        console.log("Merge fields loaded:", data);
        mergeFields.value = data?.map((item) => ({
          name: item.name,
          jinja_variable: item.jinja_variable,
        }));
      },
    });
  } catch (error) {
    console.error("Error loading merge fields:", error);
  }
};

// Initialize editor
const initEditor = async () => {
  await loadTemplateData();

  // Auto show preview when entering edit mode for the first time
  if (isEditMode.value && _template.value.message) {
    // Wait a bit for the editor to be fully initialized
    setTimeout(() => {
      autoShowPreview();
    }, 1000);
  } else if (!isEditMode.value) {
    // For new templates, also auto show preview after editor is ready
    setTimeout(() => {
      autoShowPreview();
    }, 1500);
  }
};

// Email Editor Event Handlers
const handleContentChange = (html) => {
  _template.value.message = html;
  _template.value.mjml_content = html;
};

const handleCssChange = (css) => {
  // Handle CSS changes if needed
  console.log("CSS changed:", css);
};

const handleEditorReady = (editorInstance) => {
  console.log("Email editor is ready");

  // Auto show preview when editor is ready (for first time load)
  setTimeout(() => {
    autoShowPreview();
  }, 500);
};

const handleMergeFieldsLoaded = (loadedMergeFields) => {
  console.log("Merge fields loaded:", loadedMergeFields);
  mergeFields.value = loadedMergeFields;
};

// Get default email template
const getDefaultEmailTemplate = () => {
  return `
        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="font-family: Arial, sans-serif;">
            <tr>
                <td style="background-color: #f4f4f4; padding: 20px;">
                    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="margin: 0 auto; background: #ffffff;">
                        <!-- Header -->
                        <tr>
                            <td style="background-color: #ffffff; padding: 30px 20px; text-align: center;">
                                <h1 style="margin: 0; color: #333333; font-size: 28px; font-weight: bold;">Welcome to Our Company</h1>
                            </td>
                        </tr>
                        
                        <!-- Main Content -->
                        <tr>
                            <td style="padding: 30px 20px;">
                                <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.5; color: #333333;">Dear {{candidate_name}},</p>
                                <p style="margin: 0 0 15px 0; font-size: 16px; line-height: 1.5; color: #333333;">Thank you for your application for the position of {{job_title}}. We have received your application and will review it carefully.</p>
                                <p style="margin: 0 0 25px 0; font-size: 16px; line-height: 1.5; color: #333333;">We will contact you within 5-7 business days regarding the next steps in our hiring process.</p>
                                
                                <!-- Button -->
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                                    <tr>
                                        <td style="background-color: #007bff; border-radius: 4px;">
                                            <a href="#" style="background-color: #007bff; border: none; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-size: 16px;">
                                                View Application Status
                                            </a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Signature -->
                        <tr>
                            <td style="padding: 20px; font-size: 16px; line-height: 1.5; color: #333333;">
                                <p style="margin: 0 0 10px 0;">Best regards,</p>
                                <p style="margin: 0; font-weight: bold;">HR Team</p>
                                <p style="margin: 5px 0 0 0; color: #666666; font-size: 14px;">{{company_name}}</p>
                            </td>
                        </tr>
                        
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #343a40; color: white; padding: 30px 20px; text-align: center;">
                                <p style="margin: 0 0 10px 0; font-size: 14px;">© 2024 {{company_name}}. All rights reserved.</p>
                                <p style="margin: 0; font-size: 12px;">
                                    <a href="#" style="color: #adb5bd; text-decoration: none;">Unsubscribe</a> | 
                                    <a href="#" style="color: #adb5bd; text-decoration: none;">Privacy Policy</a>
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    `;
};

// Add merge field blocks (now handled by EmailEditor component)
const addMergeFieldBlocks = () => {
  // This function is now handled by the EmailEditor component
  console.log("Merge fields will be handled by EmailEditor component");
};

// Force reload editor completely
const forceReload = async () => {
  try {
    reloading.value = true;
    if (emailEditor.value) {
      await emailEditor.value.reload();
    }
  } catch (error) {
    console.error("Error force reloading:", error);
    createToast({
      title: "Error",
      text: "Failed to reload editor",
      icon: "x",
      iconClasses: "text-red-600",
    });
  } finally {
    reloading.value = false;
  }
};

// Save content to database
const saveContent = async () => {
  try {
    loading.value = true;

    if (!emailEditor.value) {
      createToast({
        title: "Error",
        text: "Editor not initialized",
        icon: "x",
        iconClasses: "text-red-600",
      });
      return;
    }

    const html = emailEditor.value.getHtml();
    const css = emailEditor.value.getCss();

    // Update template data
    _template.value.message = html;
    _template.value.mjml_content = html;

    if (isEditMode.value) {
      await call("frappe.client.set_value", {
        doctype: "Mira Email Template",
        name: templateId.value,
        fieldname: {
          ..._template.value,
          subject: convertPlaceholderToJinja(_template.value.subject),
        },
      });
    }

    createToast({
      title: "Success",
      text: "Content saved successfully",
      icon: "check",
      iconClasses: "text-green-600",
    });
  } catch (error) {
    console.error("Error saving content:", error);
    createToast({
      title: "Error",
      text: "Cannot save content",
      icon: "x",
      iconClasses: "text-red-600",
    });
  } finally {
    loading.value = false;
  }
};

// Export and create/update template
const exportHtml = async () => {
  try {
    exporting.value = true;

    if (!_template.value.template_name) {
      createToast({
        title: "Error",
        text: "Please fill in template name",
        icon: "x",
        iconClasses: "text-red-600",
      });
      return;
    }

    const html = emailEditor.value.getHtml();
    const css = emailEditor.value.getCss();

    _template.value.message = html;
    _template.value.mjml_content = html;

    if (isEditMode.value) {
      // Update existing template
      await call("frappe.client.set_value", {
        doctype: "Mira Email Template",
        name: templateId.value,
        fieldname: {
          ..._template.value,
          subject: convertPlaceholderToJinja(_template.value.subject),
        },
      });

      createToast({
        title: "Success",
        text: "Template updated successfully",
        icon: "check",
        iconClasses: "text-green-600",
      });
    } else {
      // Create new template
      const doc = await call("frappe.client.insert", {
        doc: {
          doctype: "Mira Email Template",
          ..._template.value,
          subject: convertPlaceholderToJinja(_template.value.subject),
        },
      });

      if (doc.name) {
        createToast({
          title: "Success",
          text: "Template created successfully",
          icon: "check",
          iconClasses: "text-green-600",
        });
      }
    }

    // Navigate back
    goBack();
  } catch (error) {
    console.error("Error exporting:", error);
    createToast({
      title: "Error",
      text: "Cannot save template",
      icon: "x",
      iconClasses: "text-red-600",
    });
  } finally {
    exporting.value = false;
  }
};

// Handle edit info save
const handleEditInfoSave = async () => {
  try {
    showEditModal.value = false;
    createToast({
      title: "Success",
      text: "Template info updated",
      icon: "check",
      iconClasses: "text-green-600",
    });
  } catch (error) {
    console.error("Error updating template info:", error);
    createToast({
      title: "Error",
      text: "Cannot update template info",
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
};

// Navigation
const goBack = () => {
  router.push({
    name: "ListEmailTemplate",
  });
};

// Subject display with placeholder conversion
const displaySubject = computed(() => convertJinjaToPlaceholder(_template.value.subject));

// Conversion functions
function convertJinjaToPlaceholder(text) {
  if (!text) return "";
  let result = text;
  mergeFields.value.forEach((field) => {
    const fieldName = field.jinja_variable.replace(/[{}]/g, "");
    const jinjaSyntax = `{{${fieldName}}}`;
    const placeholder = `[${field.name}]`;
    result = result.replaceAll(jinjaSyntax, placeholder);
  });
  return result;
}

function convertPlaceholderToJinja(text) {
  if (!text) return "";
  let result = text;
  mergeFields.value.forEach((field) => {
    const placeholder = `[${field.name}]`;
    const fieldName = field.jinja_variable.replace(/[{}]/g, "");
    const jinjaSyntax = `{{${fieldName}}}`;
    result = result.replaceAll(placeholder, jinjaSyntax);
  });
  return result;
}

// Email type display
function getEmailTypeDisplay() {
  const templateType = "";
  const emailTypeMap = {
    "confirm-email": "Confirm Application",
    "invited-email": "Job Invitation",
    "reject-email": "Rejection Email",
    "other-email": "Other Email",
  };
  return emailTypeMap[templateType] || "General Email";
}

// AI Modal functions
function handleAIGenerated(generatedContent) {
  try {
    if (generatedContent.subject) {
      _template.value.subject = generatedContent.subject;
    }

    if (generatedContent.content && emailEditor.value) {
      // Load AI content into editor
      emailEditor.value.setComponents(generatedContent.content);
      _template.value.message = generatedContent.content;
    }

    createToast({
      title: __("Success"),
      text: __("AI content has been applied to the template"),
      icon: "check",
      iconClasses: "text-green-500",
    });
  } catch (error) {
    console.error("Error applying AI content:", error);
    createToast({
      title: __("Error"),
      text: __("Failed to apply AI generated content"),
      icon: "x",
      iconClasses: "text-red-500",
    });
  }
}

function openAIModal() {
  showAIModal.value = true;
}

// Lifecycle
onMounted(async () => {
  await initEditor();
});

onUnmounted(() => {
  // EmailEditor component handles its own cleanup
});

// Watch for route changes to reload editor
watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId && newId !== oldId) {
      initEditor();
    }
  }
);

const previewEmail = () => {
  if (!emailEditor.value) {
    createToast({
      title: "Error",
      text: "Editor not initialized",
      icon: "x",
      iconClasses: "text-red-600",
    });
    return;
  }

  try {
    const html = emailEditor.value.getHtml();
    const css = emailEditor.value.getCss();

    // Combine HTML and CSS
    let previewContent = css ? `<style>${css}</style>${html}` : html;

    previewHtml.value = previewContent;
    showPreview.value = true;
  } catch (error) {
    console.error("Error previewing email:", error);
    createToast({
      title: "Error",
      text: "Failed to preview email",
      icon: "x",
      iconClasses: "text-red-600",
    });
  }
};

// Auto show preview when entering edit mode
const autoShowPreview = () => {
  if (!emailEditor.value) {
    console.log("Editor not ready for auto preview");
    return;
  }

  try {
    const html = emailEditor.value.getHtml();
    const css = emailEditor.value.getCss();

    // Combine HTML and CSS
    let previewContent = css ? `<style>${css}</style>${html}` : html;

    // Only show preview if there's actual content
    if (previewContent && previewContent.trim() !== "") {
      previewHtml.value = previewContent;
      showPreview.value = true;

      createToast({
        title: "Auto Preview",
        text: "Email template preview is now displayed",
        icon: "eye",
        iconClasses: "text-blue-600",
      });
    }
  } catch (error) {
    console.error("Error in auto preview:", error);
    // Don't show error toast for auto preview, just log it
  }
};

// Computed properties for preview with sample data
const previewSubjectWithData = computed(() => {
  let subject = _template.value.subject || "";

  // Replace merge fields with sample data
  mergeFields.value.forEach((field) => {
    const fieldName = field.jinja_variable.replace(/[{}]/g, "");
    const regex = new RegExp(`{{\\s*${fieldName}\\s*}}`, "g");
    const sampleValue = sampleData.value[field.name] || `[${field.name}]`;
    subject = subject.replace(regex, sampleValue);
  });

  return subject || "No subject";
});

const previewContentWithData = computed(() => {
  if (!emailEditor.value) return "";

  try {
    const html = emailEditor.value.getHtml();
    const css = emailEditor.value.getCss();

    // Combine HTML and CSS
    let content = css ? `<style>${css}</style>${html}` : html;

    // Replace merge fields with sample data
    mergeFields.value.forEach((field) => {
      const fieldName = field.jinja_variable.replace(/[{}]/g, "");
      const regex = new RegExp(`{{\\s*${fieldName}\\s*}}`, "g");
      const sampleValue = sampleData.value[field.name] || `[${field.name}]`;
      content = content.replace(regex, sampleValue);
    });

    return content;
  } catch (error) {
    console.error("Error generating preview content:", error);
    return "Error generating preview";
  }
});

// Show send preview modal
const showSendPreview = () => {
  if (!emailEditor.value) {
    createToast({
      title: "Error",
      text: "Editor not initialized",
      icon: "x",
      iconClasses: "text-red-600",
    });
    return;
  }

  // Initialize sample data if not already done
  if (Object.keys(sampleData.value).length === 0) {
    initializeSampleData();
  }

  showSendModal.value = true;
};

// Initialize sample data
const initializeSampleData = () => {
  mergeFields.value.forEach((field) => {
    if (!sampleData.value[field.name]) {
      sampleData.value[field.name] = `Sample ${field.name}`;
    }
  });
};

// Refresh preview content
const refreshPreview = () => {
  // Force reactivity update
  sendPreviewMode.value = sendPreviewMode.value;
  createToast({
    title: "Success",
    text: "Preview refreshed",
    icon: "check",
    iconClasses: "text-green-600",
  });
};

// Send test email
const sendTestEmail = async () => {
  try {
    sendingEmail.value = true;
    // Implement test email sending logic here
    createToast({
      title: "Success",
      text: "Test email sent successfully",
      icon: "check",
      iconClasses: "text-green-600",
    });
  } catch (error) {
    console.error("Error sending test email:", error);
    createToast({
      title: "Error",
      text: "Failed to send test email",
      icon: "x",
      iconClasses: "text-red-600",
    });
  } finally {
    sendingEmail.value = false;
  }
};
</script>

<style>
/* Component specific styles */
</style>
