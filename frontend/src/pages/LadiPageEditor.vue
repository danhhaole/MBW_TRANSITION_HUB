<template>
    <div class="h-screen w-full flex flex-col">
        <!-- Header -->
        <div class="bg-white border-b px-4 py-3 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <Button variant="outline" theme="gray" @click="goBack">
                    <template #prefix>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                        </svg>
                    </template>
                    {{ __('Back') }}
                </Button>
                <div>
                    <h1 class="text-lg font-semibold">{{ pageData?.title || __('Ladi Page Editor') }}</h1>
                    <p class="text-sm text-gray-500">{{ pageData?.route }}</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <Button variant="outline" theme="gray" @click="showEditModal = true">
                    {{ __('Edit Info') }}
                </Button>
                <Button variant="outline" theme="gray" @click="forceReload" :loading="reloading">
                    {{ __('Reload') }}
                </Button>
                <Button variant="outline" theme="gray" @click="saveContent" :loading="store.loading">
                    {{ __('Save') }}
                </Button>
                <Button variant="solid" theme="blue" @click="exportHtml" :loading="exporting">
                    {{ __('Export & Submit') }}
                </Button>
            </div>
        </div>

        <!-- Editor Container -->
        <div ref="editorContainer" class="flex-1 border" />
    </div>

    <!-- Edit Info Modal -->
    <Dialog v-model="showEditModal" :options="{ size: 'lg' }">
        <template #body-title>
            <h3 class="flex items-center gap-2 text-2xl font-semibold leading-6 text-ink-gray-9">
                <div>{{ __('Edit Page Info') }}</div>
            </h3>
        </template>
        <template #body-content>
            <div class="space-y-4">
                <!-- Title -->
                <FormControl
                    type="text"
                    :label="__('Page Title')"
                    v-model="editForm.title"
                    required
                />

                <!-- Route -->
                <FormControl
                    type="text"
                    :label="__('Slug')"
                    v-model="editForm.route"
                    required
                />

                <!-- Campaign -->
                <FormControl
                    type="select"
                    :label="__('Campaign')"
                    v-model="editForm.campaign"
                    :options="campaignOptions"
                />

                <!-- Published -->
                <FormControl
                    type="checkbox"
                    :label="__('Published')"
                    v-model="editForm.published"
                />
            </div>
        </template>
        <template #actions>
            <div class="flex justify-end space-x-2">
                <Button variant="outline" theme="gray" @click="showEditModal = false">
                    {{ __('Cancel') }}
                </Button>
                <Button variant="solid" theme="blue" @click="handleEditInfoSave" :loading="store.loading">
                    {{ __('Save') }}
                </Button>
            </div>
        </template>
    </Dialog>
    <ToastContainer />
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Dialog, FormControl } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { useLadiPageStore } from '@/stores/ladiPage'
import { ToastContainer } from '@/components/shared'
import grapesjs from 'grapesjs'
import pluginWebpage from 'grapesjs-preset-webpage';
import pluginExport from 'grapesjs-plugin-export';
import pluginNavbar from 'grapesjs-navbar';
import pluginCustomCode from 'grapesjs-custom-code';
import pluginFlexbox from 'grapesjs-blocks-flexbox';
import pluginForms from 'grapesjs-plugin-forms';
import pluginCountdown from 'grapesjs-component-countdown';
import pluginTabs from 'grapesjs-tabs';
import 'grapesjs/dist/css/grapes.min.css'
import { loadLadiTailwindBlocks } from '@/utils/ladi-style-tailwind-blocks'

const route = useRoute()
const router = useRouter()
const store = useLadiPageStore()
const { showSuccess, showError } = useToast()

const editorContainer = ref(null)
const pageData = ref(null)
const exporting = ref(false)
const reloading = ref(false)
const showEditModal = ref(false)
const editForm = ref({
    title: '',
    route: '',
    campaign: null,
    published: false
})
const campaignOptions = ref([])
let editor = null

// Load page data
const loadPageData = async () => {
    try {
        const data = await store.fetchLadiPage(route.params.id)
        pageData.value = data
        updateEditForm() // Update edit form when page data changes
        return data
    } catch (error) {
        showError(__('Failed to load page data'))
        console.error('Error loading page data:', error)
    }
}

// Load campaign options
const loadCampaignOptions = async () => {
    try {
        const options = await store.fetchCampaignOptions()
        campaignOptions.value = options
    } catch (error) {
        console.error('Error loading campaign options:', error)
    }
}

// Update edit form with current page data
const updateEditForm = () => {
    if (pageData.value) {
        editForm.value = {
            title: pageData.value.title || '',
            route: pageData.value.route || '',
            campaign: pageData.value.campaign || null,
            published: pageData.value.published || false
        }
    }
}

// Handle edit info save
const handleEditInfoSave = async () => {
    try {
        await store.updateLadiPage(route.params.id, editForm.value)
        await loadPageData() // Refresh page data
        showEditModal.value = false
        showSuccess(__('Page info updated successfully'))
    } catch (error) {
        showError(__('Failed to update page info'))
        console.error('Error updating page info:', error)
    }
}

// Initialize editor
const initEditor = async () => {
    const data = await loadPageData()
    
    // Destroy existing editor if any
    if (editor) {
        editor.destroy()
        editor = null
    }
    
    editor = grapesjs.init({
        container: editorContainer.value,
        plugins: [
            pluginWebpage,
            pluginExport,
            pluginNavbar,
            pluginCustomCode,
            pluginFlexbox,
            pluginForms,
            pluginCountdown,
            pluginTabs
        ],
        pluginsOpts: {
            [pluginWebpage]: {},
            [pluginExport]: {},
            [pluginNavbar]: {},
            [pluginCustomCode]: {},
            [pluginFlexbox]: {},
            [pluginForms]: {},
            [pluginCountdown]: {},
            [pluginTabs]: {}
        },
        // Clear any cached content and load fresh data
        components: data?.content || '',
        style: data?.css || '',
        // Disable storage to prevent caching
        storageManager: false,
        // Device manager options
        deviceManager: {
            devices: [
                {
                    name: 'Desktop',
                    width: '',
                },
                {
                    name: 'Tablet',
                    width: '768px',
                    widthMedia: '992px',
                },
                {
                    name: 'Mobile',
                    width: '320px',
                    widthMedia: '480px',
                },
            ],
        },
        // Canvas options
        canvas: {
            styles: [
                'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
            ],
            scripts: [
                'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
            ],
        },
        // Asset manager
        assetManager: {
            embedAsBase64: true,
        },
        // Undo manager
        undoManager: {
            trackSelection: false,
        },
    });

    // Load custom blocks
    editor.on('load', () => {
        loadLadiTailwindBlocks(editor);
    });
}

// Force reload editor completely
const forceReload = async () => {
    try {
        reloading.value = true
        await initEditor()
        showSuccess(__('Content reloaded successfully'))
    } catch (error) {
        console.error('Error force reloading:', error)
        showError(__('Failed to reload content'))
    } finally {
        reloading.value = false
    }
}

// Reload editor with fresh data
const reloadEditor = async () => {
    try {
        reloading.value = true
        const data = await loadPageData()
        
        if (editor && data) {
            // Clear current content
            editor.DomComponents.clear()
            editor.CssComposer.clear()
            
            // Load fresh content
            if (data.content) {
                editor.setComponents(data.content)
            }
            if (data.css) {
                editor.setStyle(data.css)
            }
        }
    } catch (error) {
        console.error('Error reloading editor:', error)
        showError(__('Failed to reload content'))
    } finally {
        reloading.value = false
    }
}

// Save content to database
const saveContent = async () => {
    try {
        const html = editor.getHtml()
        const css = editor.getCss()
        
        await store.savePageContent(route.params.id, html, css)
        showSuccess(__('Content saved successfully'))
        
        // Refresh page data after save
        await loadPageData()
    } catch (error) {
        showError(__('Failed to save content'))
        console.error('Error saving content:', error)
    }
}

// Export HTML
const exportHtml = async () => {
    try {
        exporting.value = true
        const html = editor.getHtml()
        const css = editor.getCss()
        const fullHtml = `
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>${pageData.value?.title || 'Ladi Page'}</title>
                    <style>${css}</style>
                </head>
                <body>${html}</body>
            </html>
        `

        // Save to database first
        await store.savePageContent(route.params.id, html, css)
        
        // Create download link
        const blob = new Blob([fullHtml], { type: 'text/html' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `${pageData.value?.title || 'ladi-page'}.html`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        
        showSuccess(__('HTML exported successfully'))
    } catch (error) {
        showError(__('Failed to export HTML'))
        console.error('Error exporting HTML:', error)
    } finally {
        exporting.value = false
    }
}

// Navigation
const goBack = () => {
    router.push({ name: 'ladi-pages' })
}

// Lifecycle
onMounted(() => {
    initEditor()
    loadCampaignOptions()
    updateEditForm()
})

onUnmounted(() => {
    if (editor) {
        editor.destroy()
    }
})

// Watch for route changes to reload editor
watch(() => route.params.id, (newId, oldId) => {
    if (newId && newId !== oldId) {
        initEditor()
        loadCampaignOptions()
        updateEditForm()
    }
})
</script>

<style>
/* GrapesJS Device Controls */
.gjs-devices-c {
    padding: 0px;
}

.gjs-pn-devices select,
.gjs-field select,
.gjs-btn,
.gjs-input {
    all: unset;
    font-family: sans-serif;
    font-size: 14px;
    padding: 1px 1px;
    background: #2c2c2c;
    color: #fff;
    border: 1px solid #555;
    border-radius: 4px;
    text-align: justify;
}

/* Device Manager */
.gjs-devices-c {
    padding: 0px;
}

.gjs-devices-c select {
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #555;
    background: #2c2c2c;
    color: #fff;
    font-size: 12px;
}

/* Canvas Container */
.gjs-cv-canvas {
    width: 100%;
    height: 100%;
}

/* Asset Manager */
.gjs-am-assets {
    background: #2c2c2c;
    color: #fff;
}

.gjs-am-assets-header {
    background: #1a1a1a;
    border-bottom: 1px solid #555;
}

/* GrapesJS General Styling */
.gjs-one-bg {
    background-color: #2c2c2c;
}

.gjs-two-color {
    color: #fff;
}

.gjs-three-bg {
    background-color: #007bff;
}

.gjs-four-color {
    color: #007bff;
}

.gjs-pn-btn {
    border-radius: 4px;
    margin: 2px;
}

.gjs-pn-btn:hover {
    background-color: #007bff;
}

/* Device Preview */
.gjs-frame {
    border: 2px solid #007bff;
    border-radius: 4px;
    margin: 0 auto;
    display: block;
}

/* Toolbar */
.gjs-toolbar {
    background: #2c2c2c;
    border: 1px solid #555;
    border-radius: 4px;
}

.gjs-toolbar-item {
    color: #fff;
    padding: 4px 8px;
    border-radius: 2px;
    margin: 1px;
}

.gjs-toolbar-item:hover {
    background: #007bff;
}

/* Responsive Design */
@media (max-width: 768px) {
    .gjs-devices-c select {
        font-size: 10px;
        padding: 2px 4px;
    }
}
</style>