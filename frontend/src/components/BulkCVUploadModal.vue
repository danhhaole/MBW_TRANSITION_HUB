<template>
    <Dialog v-model="show" :options="{ size: '5xl' }">
        <template #body>
            <div class="flex items-center justify-between p-5">
                <h2 class="text-xl font-semibold">{{ __("Upload Multiple Resumes") }}</h2>
                <Button variant="ghost" @click="closeModal">
                    <FeatherIcon name="x" class="h-4 w-4" />
                </Button>
            </div>
            <div class="p-4">
                <!-- Dropzone and File Input -->
                <div :class="[
                    'border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors duration-300',
                    isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                ]" @dragover.prevent="onDragOver" @dragleave.prevent="onDragLeave" @drop.prevent="onDrop"
                    @click="triggerFileInput">
                    <input ref="fileInput" type="file" multiple accept=".pdf" class="hidden" @change="onFileSelect" />
                    <div class="flex flex-col items-center">
                        <svg class="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12">
                            </path>
                        </svg>
                        <p class="text-gray-600">{{ __("Drag and drop PDF files here or") }} <span
                                class="font-semibold text-blue-600">{{ __("click to select files") }}</span></p>
                        <p class="text-sm text-gray-500 mt-1">{{ __("Only PDF files are accepted") }}</p>
                    </div>
                </div>

                <!-- Selected Files List -->
                <div v-if="selectedFiles.length" class="mt-6">
                    <h2 class="text-lg font-semibold mb-3">{{ __("Selected Files") }} ({{ selectedFiles.length }})</h2>
                    <ul class="space-y-2 max-h-48 overflow-y-auto border rounded-lg p-3 bg-white">
                        <li v-for="(file, index) in selectedFiles" :key="index"
                            class="flex items-center justify-between p-2 rounded-md hover:bg-gray-100">
                            <div class="flex items-center space-x-3">
                                <svg class="w-6 h-6 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd"
                                        d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
                                        clip-rule="evenodd"></path>
                                </svg>
                                <span class="text-gray-800 text-sm">{{ file.name }}</span>
                                <span class="text-gray-500 text-xs">({{ (file.size / 1024).toFixed(2) }} KB)</span>
                            </div>
                            <button @click="removeFile(index)" class="p-1 rounded-full hover:bg-red-100 text-red-500">
                                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd"
                                        d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                                        clip-rule="evenodd"></path>
                                </svg>
                            </button>
                        </li>
                    </ul>
                </div>
                <div class="flex justify-end mt-6">
                    <Button variant="solid" :loading="isUploading" @click="uploadFiles"
                        :disabled="selectedFiles.length === 0">
                        {{ isUploading ? __("Uploading...") : __("Upload") }}
                    </Button>
                </div>
                <!-- Upload History -->
                <div class="mt-8">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold">{{ __("Upload History") }}</h2>
                        <button @click="fetchHistory" :disabled="isLoadingHistory"
                            class="p-2 rounded-md hover:bg-gray-200">
                            <svg class="w-5 h-5 text-gray-600" :class="{ 'animate-spin': isLoadingHistory }" fill="none"
                                stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M4 4v5h5M20 20v-5h-5M4 4L9 9M20 20l-5-5"></path>
                            </svg>
                        </button>
                    </div>
                    <div v-if="isLoadingHistory" class="text-center p-8">
                        <p>{{ __("Loading history...") }}</p>
                    </div>
                    <div v-else-if="uploadSessions.length === 0" class="text-center p-8 border rounded-lg bg-white">
                        <p class="text-gray-500">{{ __("No upload sessions found.") }}</p>
                    </div>
                    <div v-else class="space-y-4 max-h-96 overflow-y-auto">
                        <div v-for="session in uploadSessions" :key="session.name"
                            class="bg-white border rounded-lg shadow-sm p-4">
                            <div class="grid grid-cols-2 md:grid-cols-5 gap-4 items-center">
                                <div>
                                    <p class="text-xs text-gray-500">{{ __("Session") }}</p>
                                    <p class="font-mono text-sm text-blue-700">{{ session.name }}</p>
                                </div>
                                <div>
                                    <p class="text-xs text-gray-500">{{ __("Upload Date") }}</p>
                                    <p class="text-sm">{{ moment(session.upload_at).format("DD/MM/YYYY HH:mm") }}</p>
                                </div>
                                <div>
                                    <p class="text-xs text-gray-500">{{ __("Status") }}</p>
                                    <span :class="getStatusClass(session.status)"
                                        class="px-2 py-1 text-xs font-medium rounded-full">
                                        {{ session.status }}
                                    </span>
                                </div>
                                <div>
                                    <p class="text-xs text-gray-500">{{ __("Progress") }}</p>
                                    <p class="text-sm font-semibold">{{ session.success_count + session.failed_count +
                                        session.duplicated_count }} / {{ session.total_files }}</p>
                                </div>
                                <div class="flex justify-end">
                                    <button @click="toggleSessionDetails(session.name)"
                                        class="p-2 rounded-full hover:bg-gray-100">
                                        <svg class="w-5 h-5 transition-transform"
                                            :class="{ 'rotate-180': expandedSessions.includes(session.name) }"
                                            fill="currentColor" viewBox="0 0 20 20">
                                            <path fill-rule="evenodd"
                                                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                                                clip-rule="evenodd"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <div v-if="expandedSessions.includes(session.name)" class="mt-4 pt-4 border-t">
                                <h4 class="font-semibold mb-2">{{ __("File Details") }}</h4>
                                <Button v-if="session.failed_count > 0" variant="outline"
                                    @click="retryFailedFiles(session.name)">
                                    {{ __("Retry Failed Files") }}
                                </Button>
                                <table class="w-full text-sm text-left">
                                    <thead class="bg-gray-50">
                                        <tr>
                                            <th class="p-2">{{ __("File Name") }}</th>
                                            <th class="p-2">{{ __("Status") }}</th>
                                            <th class="p-2">{{ __("Candidate") }}</th>
                                            <th class="p-2">{{ __("Error Message") }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="file in session.files" :key="file.name" class="border-b">
                                            <td class="p-2">{{ file.file_name }}</td>
                                            <td class="p-2"><span :class="getStatusClass(file.status)"
                                                    class="px-2 py-1 text-xs font-medium rounded-full">{{ file.status
                                                    }}</span></td>
                                            <td class="p-2">
                                                <a v-if="file.candidate_id"
                                                    :href="`/app/ats_candidate/${file.candidate_id}`"
                                                    class="text-blue-600 hover:underline" target="_blank">{{
                                                        file.candidate_id }}</a>
                                            </td>
                                            <td class="p-2 text-red-600">{{ file.error_message }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </template>
    </Dialog>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { Dialog, Button, FeatherIcon, call } from 'frappe-ui';
import moment from 'moment';
import { globalStore } from '@/stores/global';
import { useToast } from '@/composables/useToast'
const { showToast, showSuccess, showError } = useToast()

const { $socket } = globalStore();

// Props for v-model to control dialog visibility from parent
const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['update:modelValue']);

// Computed property to sync with the parent's v-model
const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
});

// State management
const fileInput = ref(null);
const selectedFiles = ref([]);
const isDragging = ref(false);
const isUploading = ref(false);
const isLoadingHistory = ref(false);
const uploadSessions = ref([]);
const expandedSessions = ref([]);
const selected_jobs = ref(null);
// --- File Handling ---
const triggerFileInput = () => {
    fileInput.value.click();
};

const onFileSelect = (event) => {
    addFiles([...event.target.files]);
    console.log('Selected files:', selectedFiles.value);
};

const onDrop = (event) => {
    isDragging.value = false;
    addFiles([...event.dataTransfer.files]);
};

const addFiles = (files) => {
    const maxSize = 10 * 1024 * 1024; // 10MB
    const pdfFiles = files.filter(file => file.type === 'application/pdf' && file.size <= maxSize);
    if (pdfFiles.length !== files.length) {
        showError(__('Some files were skipped due to invalid format or size exceeding 10MB.'))
    }
    selectedFiles.value = [...selectedFiles.value, ...pdfFiles];
};

const removeFile = (index) => {
    selectedFiles.value.splice(index, 1);
};

const onDragOver = () => {
    isDragging.value = true;
};

const onDragLeave = () => {
    isDragging.value = false;
};

const closeModal = () => {
    show.value = false;
};

// --- API Calls ---
const uploadFiles = async () => {
    if (selectedFiles.value.length === 0) {
        showError(__('No Files Selected'))
        return;
    }
    isUploading.value = true;

    try {
        let csrf_token = '';
        if (window.csrf_token && window.csrf_token !== '{{ csrf_token }}') {
            csrf_token = window.csrf_token;
        }
        
        const formData = new FormData();
        
        // Add files
        selectedFiles.value.forEach((file) => {
            formData.append('file', file, file.name);
        });

        // Add field mapping
        const fieldMapping = {
            'file_name': 'name',
            'file_type': 'type',
            'file_size': 'size'
        };
        formData.append('mapping', JSON.stringify(fieldMapping));
        
        // Add other data
        formData.append('note', '');
        formData.append('job_opening', selected_jobs.value || '');

        const response = await fetch('/api/method/mbw_mira.mbw_mira.doctype.mira_resumeuploadsession.mira_resumeuploadsession.upload_resumes', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Frappe-CSRF-Token': csrf_token
            }
        });
        
        const result = await response.json();

        if (result.message && result.message.status === 'success') {
            showSuccess(__('Upload session {0} started. Processing will run in the background.', [result.message.session_name]))
            selectedFiles.value = [];
            fetchHistory();
        } else {
            throw new Error(result.message?.message || 'Unknown error');
        }
    } catch (error) {
        showError(__('Failed to upload files: {0}', [error.message || error]))
        console.error('Upload error:', error);
    } finally {
        isUploading.value = false;
    }
};

const fetchHistory = async () => {
    isLoadingHistory.value = true;
    try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_resumeuploadsession.mira_resumeuploadsession.get_upload_history');
        uploadSessions.value = response || [];
    } catch (error) {
        showError(__('Failed to load history: {0}', [error.message || error]))
        console.error('History fetch error:', error);
    } finally {
        isLoadingHistory.value = false;
    }
};

// --- UI Helpers ---
const toggleSessionDetails = (sessionName) => {
    const index = expandedSessions.value.indexOf(sessionName);
    if (index > -1) {
        expandedSessions.value.splice(index, 1);
    } else {
        expandedSessions.value.push(sessionName);
    }
};

const getStatusClass = (status) => {
    const classes = {
        'Pending': 'bg-gray-100 text-gray-800',
        'Processing': 'bg-blue-100 text-blue-800 animate-pulse',
        'Completed': 'bg-green-100 text-green-800',
        'Success': 'bg-green-100 text-green-800',
        'Error': 'bg-red-100 text-red-800',
        'Duplicate': 'bg-yellow-100 text-yellow-800',
        'Invalid Format': 'bg-orange-100 text-orange-800',
    };
    return classes[status] || 'bg-gray-100 text-gray-800';
};

const retryFailedFiles = async (sessionName) => {
    try {
        const response = await call('mbw_mira.mbw_mira.doctype.mira_resumeuploadsession.mira_resumeuploadsession.retry_failed_files', { session_name: sessionName });
        showSuccess(__('{0} file(s) retried successfully.').format(response.retried))
        fetchHistory();
    } catch (error) {
        showError(__('Failed to retry files: {0}').format(error.message || error))
    }
};

// --- Lifecycle Hook ---
let refreshInterval = null;

watch(show, (newValue) => {
    if (newValue) {
        fetchHistory();

    }
});

onMounted(() => {
    if (show.value) {
        fetchHistory();

    }
    // $socket.on('resume_upload_update', (data) => {
    //     if (data.session_name) {
    //         fetchHistory();
    //     }
    // });
});
</script>

<style scoped>
:deep(.field) {
    margin-bottom: 1rem;
}

:deep(.form-control) {
    width: 100%;
}
</style>