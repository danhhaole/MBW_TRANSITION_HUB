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
                    <h1 class="text-lg font-semibold">{{ pageData?.title || __('Ladi Page View') }}</h1>
                    <p class="text-sm text-gray-500">{{ pageData?.route }}</p>
                </div>
            </div>
            <div class="flex items-center space-x-2">
                <Button variant="outline" theme="blue" @click="editPage">
                    {{ __('Edit') }}
                </Button>
                <Button variant="outline" theme="gray" @click="exportHtml" :loading="exporting">
                    {{ __('Export') }}
                </Button>
            </div>
        </div>

        <!-- Content Preview -->
        <div class="flex-1 bg-gray-50 p-4">
            <div class="bg-white rounded-lg shadow-sm h-full overflow-auto">
                <div v-if="loading" class="flex items-center justify-center h-full">
                    <div class="text-center">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                        <p class="mt-2 text-gray-500">{{ __('Loading content...') }}</p>
                    </div>
                </div>
                <div v-else-if="!pageData?.content" class="flex items-center justify-center h-full">
                    <div class="text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-gray-400 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <p class="mt-2 text-gray-500">{{ __('No content available') }}</p>
                        <Button variant="outline" theme="blue" @click="editPage" class="mt-2">
                            {{ __('Create Content') }}
                        </Button>
                    </div>
                </div>
                <div v-else class="h-full">
                    <iframe 
                        ref="previewFrame"
                        class="w-full h-full border-0"
                        :srcdoc="fullHtml"
                        title="Page Preview"
                    ></iframe>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button } from 'frappe-ui'
import { useToast } from '@/composables/useToast'
import { useLadiPageStore } from '@/stores/ladiPage'

const route = useRoute()
const router = useRouter()
const store = useLadiPageStore()
const { showSuccess, showError } = useToast()

const pageData = ref(null)
const loading = ref(true)
const exporting = ref(false)
const previewFrame = ref(null)

// Computed full HTML
const fullHtml = computed(() => {
    if (!pageData.value?.content) return ''
    
    return `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>${pageData.value.title || 'Ladi Page'}</title>
            <style>
                ${pageData.value.css || ''}
            </style>
        </head>
        <body>
            ${pageData.value.content || ''}
        </body>
        </html>
    `
})

// Load page data
const loadPageData = async () => {
    try {
        loading.value = true
        const data = await store.fetchLadiPage(route.params.id)
        pageData.value = data
    } catch (error) {
        showError(__('Failed to load page data'))
        console.error('Error loading page data:', error)
    } finally {
        loading.value = false
    }
}

// Export HTML
const exportHtml = async () => {
    try {
        exporting.value = true
        
        if (!pageData.value?.content) {
            showError(__('No content to export'))
            return
        }

        const blob = new Blob([fullHtml.value], { type: 'text/html' })
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

const editPage = () => {
    router.push({ name: 'ladi-page-editor', params: { id: route.params.id } })
}

// Lifecycle
onMounted(() => {
    loadPageData()
})
</script> 