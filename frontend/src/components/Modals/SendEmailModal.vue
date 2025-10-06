<template>
    <Dialog v-model="show" :options="{ size: '5xl' }">
        <template #body>
            <!-- Header -->
            <div class="flex items-center justify-between p-5">
                <h2 class="text-xl font-semibold">{{ __("Send email to candidate") }}</h2>
                <Button variant="ghost" @click="closeModal">
                    <FeatherIcon name="x" class="h-4 w-4" />
                </Button>
            </div>
            <div class="p-4">

                <!-- Form -->
                <form @submit.prevent="sendEmail" class="p-4 space-y-6">
                    <!-- Email Template Selection -->
                    <div>
                        <label for="template" class="block text-sm font-medium text-gray-700 mb-2">
                            {{ __("Email Template") }} <span class="text-red-500">*</span>
                        </label>
                        <select id="template" v-model="emailData.template" @change="loadTemplate"
                            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base"
                            required>
                            <option value="">{{ __("Select template...") }}</option>
                            <option v-for="template in emailTemplates" :key="template.name" :value="template.name">
                                {{ template.title }}
                            </option>
                        </select>
                    </div>

                    <!-- Recipients Grid -->
                    <div class="space-y-4">
                        <!-- To Field -->
                        <div>
                            <label for="to" class="block text-sm font-medium text-gray-700 mb-2">
                                {{ __("To") }} <span class="text-red-500">*</span>
                            </label>
                            <div class="relative">
                                <textarea id="to" v-model="emailData.to" rows="1"
                                    class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base"
                                    :placeholder="__('email1@example.com, email2@example.com')" required></textarea>
                                <!-- CC/BCC Toggle -->
                                <div class="absolute right-2 bottom-2 flex space-x-2">
                                    <button type="button" v-if="!showCC" @click="showCC = true"
                                        class="text-xs text-blue-600 hover:text-blue-800 font-medium">
                                        {{ __("CC") }}
                                    </button>
                                    <button type="button" v-if="!showBCC" @click="showBCC = true"
                                        class="text-xs text-blue-600 hover:text-blue-800 font-medium">
                                        {{ __("BCC") }}
                                    </button>
                                </div>
                            </div>
                            <p class="mt-1 text-sm text-gray-500">{{ __("Separate multiple emails with commas") }}</p>
                        </div>

                        <!-- CC Field (conditional) -->
                        <div v-if="showCC" class="relative">
                            <label for="cc" class="block text-sm font-medium text-gray-700 mb-2">
                                {{ __("CC") }}
                                <button type="button" @click="hideCC"
                                    class="ml-2 text-xs text-gray-400 hover:text-gray-600" :title="__('Hide CC')">
                                    ✕
                                </button>
                            </label>
                            <textarea id="cc" v-model="emailData.cc" rows="1"
                                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base"
                                :placeholder="__('cc@example.com')"></textarea>
                        </div>

                        <!-- BCC Field (conditional) -->
                        <div v-if="showBCC" class="relative">
                            <label for="bcc" class="block text-sm font-medium text-gray-700 mb-2">
                                {{ __("BCC") }}
                                <button type="button" @click="hideBCC"
                                    class="ml-2 text-xs text-gray-400 hover:text-gray-600" :title="__('Hide BCC')">
                                    ✕
                                </button>
                            </label>
                            <textarea id="bcc" v-model="emailData.bcc" rows="1"
                                class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base"
                                :placeholder="__('bcc@example.com')"></textarea>
                        </div>
                    </div>

                    <!-- Subject -->
                    <div>
                        <label for="subject" class="block text-sm font-medium text-gray-700 mb-2">
                            {{ __("Subject") }} <span class="text-red-500">*</span>
                        </label>
                        <input type="text" id="subject" v-model="emailData.subject"
                            class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-base"
                            :placeholder="__('Enter email subject...')" required>
                    </div>

                    <!-- Content -->
                    <div>
                        <label for="content" class="block text-sm font-medium text-gray-700 mb-2">
                            {{ __("Content") }} <span class="text-red-500">*</span>
                        </label>
                        <div class="border border-gray-300 rounded-md overflow-hidden">
                            <TextEditor ref="contentTextarea" variant="outline" :class="'w-full'"
                                :content="emailData.content || ''" :placeholder="__('Enter email content...')"
                                :bubbleMenu="true" :fixedMenu="true" @change="
                                    (content) => {
                                        // console.log(content);
                                        if (content != '<p></p>') {
                                            emailData.content = content;
                                        }
                                    }
                                " editor-class="!prose-sm !w-full overflow-auto !max-w-full min-h-[180px] max-h-80 py-1.5 px-2 rounded border border-gray-300 bg-white hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400 text-gray-800 transition-colors" />
                        </div>
                        <p class="mt-2 text-sm text-gray-500">
                            {{ __("Use variables like {can_full_name}, {job_public_title}, {company_name} to personalize email") }}
                        </p>
                    </div>

                    <!-- Attachments -->
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            {{ __("Attachments") }}
                        </label>
                        <div
                            class="border-2 border-dashed border-gray-300 rounded-md p-6 hover:border-gray-400 transition-colors">
                            <div class="text-center">
                                <svg class="mx-auto h-12 w-12 text-gray-400 mb-4" stroke="currentColor" fill="none"
                                    viewBox="0 0 48 48">
                                    <path
                                        d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                                        stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                                </svg>
                                <div class="flex text-sm text-gray-600">
                                    <label for="file-upload"
                                        class="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500">
                                        <span>{{ __("Upload files") }}</span>
                                        <input id="file-upload" name="file-upload" type="file" class="sr-only" multiple
                                            @change="handleFileUpload">
                                    </label>
                                    <p class="pl-1">{{ __("or drag and drop here") }}</p>
                                </div>
                                <p class="text-xs text-gray-500 mt-1">{{ __("PNG, JPG, PDF, DOC, DOCX up to 10MB") }}
                                </p>
                            </div>
                        </div>

                        <!-- Selected Files -->
                        <div v-if="emailData.attachments.length > 0" class="mt-4">
                            <h4 class="text-sm font-medium text-gray-700 mb-2">{{ __("Selected files") }}:</h4>
                            <div class="space-y-2">
                                <div v-for="(file, index) in emailData.attachments" :key="index"
                                    class="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                                    <div class="flex items-center">
                                        <svg class="h-5 w-5 text-gray-400 mr-3" fill="none" viewBox="0 0 24 24"
                                            stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                        </svg>
                                        <span class="text-sm text-gray-700">{{ file.name }}</span>
                                        <span class="text-xs text-gray-500 ml-2">({{ formatFileSize(file.size)
                                        }})</span>
                                    </div>
                                    <button type="button" @click="removeFile(index)"
                                        class="text-red-500 hover:text-red-700 p-1" :title="__('Remove file')">
                                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M6 18L18 6M6 6l12 12" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
                        <button type="button" @click="closeModal"
                            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                            {{ __("Cancel") }}
                        </button>
                        <button type="button" @click="saveDraft" :disabled="loading || isSaving"
                            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50">
                            {{ isSaving ? __('Saving...') : __('Save Draft') }}
                        </button>
                        <button type="submit" :disabled="loading || isSending || !isFormValid"
                            class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ isSending ? __('Sending...') : __('Send Email') }}
                        </button>
                    </div>
                </form>
            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, onBeforeUnmount } from 'vue'
import { Dialog, Button, FeatherIcon, TextEditor } from 'frappe-ui'
import { EmailAPI, emailUtils } from '@/utils/email_api.js'
import { createToast, setupAssignees, setupCustomizations, copyToClipboard } from '@/utils';

// Props
const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    },
    candidate: {
        type: Object,
        default: () => ({})
    },
    jobTitle: {
        type: String,
        default: ''
    },
    jobOpeningId: {
        type: String,
        default: ''
    }
})

// Emits
const emit = defineEmits(['update:modelValue', 'email-sent', 'draft-saved'])

// Reactive data
const show = computed({
    get: () => props.modelValue,
    set: (value) => {
        if (value !== props.modelValue) {
            emit('update:modelValue', value)
        }
    }
})

const loading = ref(false)
const isSending = ref(false) // Separate loading states
const isSaving = ref(false)
const contentTextarea = ref(null)
const showCC = ref(false)
const showBCC = ref(false)

// Initialize emailData with proper reactive structure
const emailData = reactive({
    template: '',
    to: '',
    cc: '',
    bcc: '',
    subject: '',
    content: '',
    attachments: []
})

const emailTemplates = ref([])
const loadingTemplates = ref(false)
const templatesLoaded = ref(false) // Prevent multiple loads

// Computed
const isFormValid = computed(() => {
    return emailData.to.trim() && emailData.subject.trim() && emailData.content.trim()
})

// Watch for candidate changes and update email field
watch(() => props.candidate, (newCandidate) => {
    if (newCandidate?.can_email && newCandidate.can_email !== emailData.to) {
        emailData.to = newCandidate.can_email
    }
}, { immediate: true, deep: true })

// Watch modal visibility to reset form when closed
watch(() => props.modelValue, (newValue, oldValue) => {
    if (newValue && !oldValue) {
        // Modal is opening
        initializeModal()
    } else if (!newValue && oldValue) {
        // Modal is closing - reset form after animation
        setTimeout(resetForm, 300)
    }
})

// Methods
const closeModal = () => {
    if (loading.value || isSending.value || isSaving.value) {
        return // Prevent closing during operations
    }
    show.value = false
}

const hideCC = () => {
    showCC.value = false
    emailData.cc = ''
}

const hideBCC = () => {
    showBCC.value = false
    emailData.bcc = ''
}

const loadTemplate = async () => {
    if (!emailData.template || loading.value) return

    try {
        loading.value = true
        const response = await EmailAPI.getEmailTemplate(emailData.template)

        if (response.success && response.data) {
            const template = response.data
            emailData.subject = template.subject || ''
            emailData.content = template.message || template.html_content || ''

            // Replace variables if candidate data is available
            const variables = {
                can_full_name: props.candidate.can_full_name || '',
                job_title: props.jobTitle || '',
                company_name: 'ABC Company' // You can get this from settings
            }

            emailData.subject = EmailAPI.replaceVariables(emailData.subject, variables)
            emailData.content = EmailAPI.replaceVariables(emailData.content, variables)
        }
    } catch (error) {
        console.error('Error loading template:', error)
        createToast({
            title: __('Error loading template'),
            text: __('Error loading template.'),
            icon: 'x',
            iconClasses: 'text-red-600',
        });
    } finally {
        loading.value = false
    }
}

const loadEmailTemplates = async () => {
    if (templatesLoaded.value || loadingTemplates.value) {
        return // Prevent multiple loads
    }
    
    loadingTemplates.value = true
    try {
        const response = await EmailAPI.getEmailTemplates({
            is_active: 1
        })

        if (response.success) {
            emailTemplates.value = response.data.map(template => ({
                name: template.template_id,
                title: template.template_name,
                template_type: template.template_type,
                subject: template.subject,
                content: template.message || template.html_content
            }))
            templatesLoaded.value = true
        }
    } catch (error) {
        console.error('Error loading templates:', error)
        createToast({
            title: __('Error loading email template'),
            text: __('Error loading email template.'),
            icon: 'x',
            iconClasses: 'text-red-600',
        });
    } finally {
        loadingTemplates.value = false
    }
}

const handleFileUpload = (event) => {
    const files = Array.from(event.target.files)
    const allowedTypes = [
        'image/png', 'image/jpeg', 'image/jpg',
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]
    const maxSize = 10 * 1024 * 1024 // 10MB

    files.forEach(file => {
        if (!allowedTypes.includes(file.type)) {
            createToast({
                title: __('File type is not supported'),
                text: __('File type {0} is not supported', [file.name]),
                icon: 'x',
                iconClasses: 'text-red-600',
            });
            return
        }

        if (file.size > maxSize) {
            createToast({
                title: __('File type is too large '),
                text: __('File {0} is too large (max 10MB)', [file.name]),
                icon: 'x',
                iconClasses: 'text-red-600',
            });
            return
        }

        emailData.attachments.push(file)
    })

    // Reset input
    event.target.value = ''
}

const removeFile = (index) => {
    emailData.attachments.splice(index, 1)
}

const formatFileSize = (bytes) => {
    return emailUtils.formatFileSize(bytes)
}

const sendEmail = async () => {
    if (!isFormValid.value || isSending.value) return

    // Validate email addresses
    const toValidation = EmailAPI.validateEmailList(emailData.to)
    if (!toValidation.valid) {
        createToast({
            title: __('Invalid email addresses'),
            text: __('Invalid email addresses in To field: {0}', [toValidation.invalidEmails.join(', ')]),
            icon: 'x',
            iconClasses: 'text-red-600',
        });
        return
    }

    if (emailData.cc) {
        const ccValidation = EmailAPI.validateEmailList(emailData.cc)
        if (!ccValidation.valid) {
            createToast({
                title: __('Invalid email addresses'),
                text: __('Invalid email addresses in CC field: {0}', [ccValidation.invalidEmails.join(', ')]),
                icon: 'x',
                iconClasses: 'text-red-600'
            });
            return
        }
    }

    if (emailData.bcc) {
        const bccValidation = EmailAPI.validateEmailList(emailData.bcc)
        if (!bccValidation.valid) {
            createToast({
                title: __('Invalid email addresses'),
                text: __('Invalid email addresses in BCC field: {0}', [bccValidation.invalidEmails.join(', ')]),
                icon: 'x',
                iconClasses: 'text-red-600',
            });
            return
        }
    }

    isSending.value = true
    loading.value = true

    try {
        const emailPayload = {
            template_id: emailData.template,
            candidate_id: props.candidate.name,
            to_emails: emailData.to,
            cc_emails: emailData.cc,
            bcc_emails: emailData.bcc,
            subject: emailData.subject,
            content: emailData.content,
            attachments: emailData.attachments,
            job_opening_id: props.jobOpeningId || ''
        }

        const response = await EmailAPI.sendCandidateEmail(emailPayload)

        if (response.success) {
            createToast({
                title: __('Email sent successfully'),
                text: __('Email sent successfully'),
                icon: 'check',
                iconClasses: 'text-green-600',
            });
            emit('email-sent', emailPayload)
            closeModal()
        } else {
            createToast({
                title: __('Failed to send email'),
                text: response.message || __('Failed to send email'),
                icon: 'x',
                iconClasses: 'text-red-600',
            });
        }
    } catch (error) {
        console.error('Error sending email:', error)
        createToast({
            title: __('An error occurred while sending email'),
            text: error.message || __('An error occurred while sending email'),
            icon: 'x',
            iconClasses: 'text-red-600',
        });
    } finally {
        isSending.value = false
        loading.value = false
    }
}

const saveDraft = async () => {
    if (isSaving.value) return

    isSaving.value = true
    loading.value = true

    try {
        const draftData = {
            template_id: emailData.template,
            candidate_id: props.candidate.name,
            to_emails: emailData.to,
            cc_emails: emailData.cc,
            bcc_emails: emailData.bcc,
            subject: emailData.subject,
            content: emailData.content,
            attachments: emailData.attachments,
            job_opening_id: props.jobOpeningId || ''
        }

        const response = await EmailAPI.saveEmailDraft(draftData)

        if (response.success) {
            createToast({
                title: __('Draft saved successfully'),
                text: __('Draft saved successfully'),
                icon: 'check',
                iconClasses: 'text-green-600',
            });
            emit('draft-saved', draftData)
        } else {
            createToast({
                title: __('Failed to save draft'),
                text: response.message || __('Failed to save draft'),
                icon: 'x',
                iconClasses: 'text-red-600',
            });
        }

    } catch (error) {
        console.error('Error saving draft:', error)
        createToast({
            title: __('An error occurred while saving draft'),
            text: __('An error occurred while saving draft'),
            icon: 'x',
            iconClasses: 'text-red-600',
        });
    } finally {
        isSaving.value = false
        loading.value = false
    }
}

const resetForm = () => {
    // Reset form data
    Object.assign(emailData, {
        template: '',
        to: props.candidate?.can_email || '',
        cc: '',
        bcc: '',
        subject: '',
        content: '',
        attachments: []
    })

    // Reset states
    showCC.value = false
    showBCC.value = false
    loading.value = false
    isSending.value = false
    isSaving.value = false
}

const initializeModal = async () => {
    // Set candidate email if available
    if (props.candidate?.can_email) {
        emailData.to = props.candidate.can_email
    }
    
    // Load templates if not already loaded
    if (!templatesLoaded.value) {
        await loadEmailTemplates()
    }
}

// Initialize on mount
onMounted(async () => {
    await loadEmailTemplates()
})

// Cleanup on unmount
onBeforeUnmount(() => {
    resetForm()
})
</script>