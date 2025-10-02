<template>
    <Dialog :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)" :options="{ size: '2xl' }">
        <template #body-title>
            <div class="flex items-center justify-between">
                <h3 class="text-xl font-semibold text-gray-900">Copy link với UTM tracking</h3>

            </div>
        </template>

        <template #body-content>
            <div class="space-y-6">
                <!-- Job Preview Card -->
                <div class="bg-gray-50 rounded-lg p-4 border">
                    <div class="flex items-start gap-3">
                        <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                            <FeatherIcon name="briefcase" class="h-6 w-6 text-green-600" />
                        </div>
                        <div class="flex-1 min-w-0">
                            <h4 class="font-semibold text-gray-900 text-sm line-clamp-2">
                                {{ jobData?.job_title || 'Job Opening' }}
                            </h4>
                            <p class="text-gray-600 text-xs mt-1">
                                {{ jobData?.jo_using_unit || 'Company' }} • {{ jobData?.location_name || 'Location' }}
                            </p>
                            <p class="text-gray-500 text-xs mt-1">
                                {{ formatSalary(jobData?.jo_min_salary, jobData?.jo_max_salary, jobData?.jo_currency) }}
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Share URL Section -->
                <div class="space-y-3">
                    <h4 class="text-sm font-medium text-gray-900">Copy link</h4>
                    <div class="flex gap-2">
                        <input :value="shareUrl" type="text" readonly
                            class="flex-1 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                            placeholder="Đang tạo liên kết..." />
                        <Button @click="copyShareUrl" variant="outline" size="sm" :loading="isCopying"
                            class="flex-shrink-0">
                            <template #prefix>
                                <FeatherIcon name="copy" class="h-4 w-4" />
                            </template>
                            {{ isCopying ? 'Đã copy' : 'Copy' }}
                        </Button>
                    </div>

                    <!-- UTM Preview -->
                    <div v-if="selectedUTMSource && (utmParams.utm_campaign || utmParams.utm_content)"
                        class="p-3 bg-green-50 border border-green-200 rounded-lg">
                        <div class="flex items-center gap-2 mb-2">
                            <FeatherIcon name="check-circle" class="h-4 w-4 text-green-600" />
                            <span class="text-sm font-medium text-green-800">UTM Parameters đã được thêm</span>
                        </div>
                        <div class="text-xs text-green-700 space-y-1">
                            <div v-if="utmParams.utm_source">
                                <span class="font-medium">Source:</span> {{ utmParams.utm_source }}
                            </div>
                            <div v-if="utmParams.utm_medium">
                                <span class="font-medium">Medium:</span> {{ utmParams.utm_medium }}
                            </div>
                            <div v-if="utmParams.utm_campaign">
                                <span class="font-medium">Campaign:</span> {{ utmParams.utm_campaign }}
                            </div>
                            <div v-if="utmParams.utm_content">
                                <span class="font-medium">Content:</span> {{ utmParams.utm_content }}
                            </div>
                        </div>
                    </div>
                </div>



                <!-- UTM Source Selection -->
                <div class="space-y-3">
                    <h4 class="text-sm font-medium text-gray-900">Thêm UTM tracking</h4>
                    <div class="p-3 bg-gray-50 rounded-lg">
                        <Autocomplete :options="utmSourceOptions" v-model="selectedUTMSource"
                            placeholder="Chọn nguồn để tự động thêm UTM parameters" @update:modelValue="onUTMSourceChange">
                            <template #prefix>
                                <FeatherIcon name="link" class="h-4 w-4 text-gray-500" />
                            </template>
                            <template #item-prefix="{ option }">
                                <div class="w-6 h-6 rounded-full flex items-center justify-center" :class="option.bgColor">
                                    <FeatherIcon :name="option.icon" class="h-3 w-3 text-white" />
                                </div>
                            </template>
                            <template #item-suffix="{ option }">
                                <span class="text-xs text-gray-500">{{ option.description }}</span>
                            </template>
                        </Autocomplete>

                        <!-- Campaign Input -->
                        <div class="mt-3" v-if="selectedUTMSource">
                            <label class="block text-xs font-medium text-gray-700 mb-1">Tên chiến dịch (Campaign)</label>
                            <input v-model="campaignName" type="text"
                                placeholder="Ví dụ: q3_2025, summer_hire, tech_talent..."
                                class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                @input="updateUTMParams" />
                        </div>

                        <!-- Content Input -->
                        <div class="mt-3" v-if="selectedUTMSource">
                            <label class="block text-xs font-medium text-gray-700 mb-1">Nội dung (Content) - Tùy
                                chọn</label>
                            <input v-model="contentName" type="text" placeholder="Ví dụ: creative_a, banner_1, job_title..."
                                class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
                                @input="updateUTMParams" />
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <template #actions>
            <div class="flex justify-end gap-3">
                <Button variant="subtle" @click="$emit('update:modelValue', false)">
                    Đóng
                </Button>
            </div>
        </template>
    </Dialog>
</template>
  
<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, Button, FeatherIcon, Autocomplete } from 'frappe-ui'
import { generateJobShareUrl, copyUrlToClipboard } from '@/utils/shareUtils'

const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    },
    jobData: {
        type: Object,
        default: () => ({})
    },
    jobId: {
        type: String,
        required: true
    }
})

const emit = defineEmits(['update:modelValue'])

// State
const shareUrl = ref('')
const isCopying = ref(false)
const selectedUTMSource = ref(null)
const campaignName = ref('')
const contentName = ref('')
const utmParams = ref({
    utm_source: '',
    utm_medium: '',
    utm_campaign: '',
    utm_content: ''
})

// UTM Source Options
const utmSourceOptions = ref([
    {
        label: 'Facebook',
        value: 'facebook',
        icon: 'facebook',
        bgColor: 'bg-blue-600',
        description: 'Chia sẻ với bạn bè',
        utm_source: 'facebook',
        utm_medium: 'social'
    },
    {
        label: 'LinkedIn',
        value: 'linkedin',
        icon: 'linkedin',
        bgColor: 'bg-blue-700',
        description: 'Chia sẻ với network',
        utm_source: 'linkedin',
        utm_medium: 'social'
    },
    {
        label: 'Twitter/X',
        value: 'twitter',
        icon: 'twitter',
        bgColor: 'bg-black',
        description: 'Chia sẻ tweet',
        utm_source: 'twitter',
        utm_medium: 'social'
    },
    {
        label: 'WhatsApp',
        value: 'whatsapp',
        icon: 'message-circle',
        bgColor: 'bg-green-500',
        description: 'Gửi tin nhắn',
        utm_source: 'whatsapp',
        utm_medium: 'social'
    },
    {
        label: 'Telegram',
        value: 'telegram',
        icon: 'send',
        bgColor: 'bg-blue-500',
        description: 'Gửi tin nhắn',
        utm_source: 'telegram',
        utm_medium: 'social'
    },
    {
        label: 'Email',
        value: 'email',
        icon: 'mail',
        bgColor: 'bg-gray-600',
        description: 'Gửi qua email',
        utm_source: 'email',
        utm_medium: 'email'
    },
    {
        label: 'Google Ads',
        value: 'google_ads',
        icon: 'search',
        bgColor: 'bg-red-500',
        description: 'Quảng cáo Google',
        utm_source: 'google',
        utm_medium: 'cpc'
    },
    {
        label: 'Facebook Ads',
        value: 'facebook_ads',
        icon: 'facebook',
        bgColor: 'bg-blue-600',
        description: 'Quảng cáo Facebook',
        utm_source: 'facebook',
        utm_medium: 'cpc'
    },
    {
        label: 'LinkedIn Ads',
        value: 'linkedin_ads',
        icon: 'linkedin',
        bgColor: 'bg-blue-700',
        description: 'Quảng cáo LinkedIn',
        utm_source: 'linkedin',
        utm_medium: 'cpc'
    },
    {
        label: 'Internal Referral',
        value: 'internal',
        icon: 'users',
        bgColor: 'bg-purple-600',
        description: 'Giới thiệu nội bộ',
        utm_source: 'internal',
        utm_medium: 'referral'
    },
    {
        label: 'Direct Traffic',
        value: 'direct',
        icon: 'link',
        bgColor: 'bg-gray-500',
        description: 'Truy cập trực tiếp',
        utm_source: 'direct',
        utm_medium: 'none'
    }
])

// Computed
const formattedJobTitle = computed(() => {
    return props.jobData?.job_title || 'Job Opening'
})

// Methods
const generateShareUrl = () => {
    try {
        const url = generateJobShareUrl(
            props.jobData?.job_url_cms,
            utmParams.value
        )
        shareUrl.value = url
    } catch (error) {
        console.error('Error generating share URL:', error)
        // Fallback to simple URL
        shareUrl.value = `${window.location.origin}/mbw_mira/jobs/${props.jobData?.job_url_cms || ''}`
    }
}

// Methods for UTM handling
const onUTMSourceChange = (value) => {
    if (value) {
        // Handle both object and string values
        const selectedValue = typeof value === 'object' ? value.value : value
        const selectedOption = utmSourceOptions.value.find(option => option.value === selectedValue)
        if (selectedOption) {
            utmParams.value.utm_source = selectedOption.utm_source
            utmParams.value.utm_medium = selectedOption.utm_medium
            updateUTMParams()
        }
    } else {
        // Reset UTM params when no source is selected
        utmParams.value.utm_source = ''
        utmParams.value.utm_medium = ''
        utmParams.value.utm_campaign = ''
        utmParams.value.utm_content = ''
        generateShareUrl()
    }
}

const updateUTMParams = () => {
    if (selectedUTMSource.value) {
        // Handle both object and string values
        const selectedValue = typeof selectedUTMSource.value === 'object' ? selectedUTMSource.value.value : selectedUTMSource.value
        const selectedOption = utmSourceOptions.value.find(option => option.value === selectedValue)

        if (selectedOption) {
            utmParams.value.utm_source = selectedOption.utm_source
            utmParams.value.utm_medium = selectedOption.utm_medium
            utmParams.value.utm_campaign = campaignName.value
            utmParams.value.utm_content = contentName.value
            generateShareUrl()
        }
    }
}

const copyShareUrl = async () => {
    if (!shareUrl.value) return

    isCopying.value = true
    const success = await copyUrlToClipboard(shareUrl.value)

    if (success) {
        // Show success feedback
        setTimeout(() => {
            isCopying.value = false
        }, 2000)
    } else {
        isCopying.value = false
    }
}

// Reset data when modal closes
const resetData = () => {
    selectedUTMSource.value = null
    campaignName.value = ''
    contentName.value = ''
    utmParams.value = {
        utm_source: '',
        utm_medium: '',
        utm_campaign: '',
        utm_content: ''
    }
    shareUrl.value = ''
}

const formatSalary = (minSalary, maxSalary, currency = 'VND') => {
    if (!minSalary && !maxSalary) return 'Thỏa thuận'

    const formatNumber = (num) => {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(0) + ' triệu'
        }
        return num.toLocaleString('vi-VN')
    }

    if (minSalary && maxSalary) {
        return `${formatNumber(minSalary)} - ${formatNumber(maxSalary)} ${currency}`
    } else if (minSalary) {
        return `Từ ${formatNumber(minSalary)} ${currency}`
    } else if (maxSalary) {
        return `Lên đến ${formatNumber(maxSalary)} ${currency}`
    }

    return 'Thỏa thuận'
}

// Watch for modal opening/closing
watch(() => props.modelValue, (newVal) => {
    if (newVal && props.jobId) {
        // Modal opened - generate initial URL
        generateShareUrl()
    } else if (!newVal) {
        // Modal closed - reset data
        resetData()
    }
})

// Watch for UTM params changes to regenerate URL
watch(utmParams, () => {
    if (props.modelValue && props.jobId) {
        generateShareUrl()
    }
}, { deep: true })

// Watch for campaign and content changes
watch([campaignName, contentName, selectedUTMSource], () => {
    updateUTMParams()
}, { deep: true })
</script>
  
<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>
  