<template>
    <header class="sticky top-0 z-10 flex items-center justify-between border-b bg-surface-white px-3 py-2.5 sm:px-5">
        <Breadcrumbs :items="breadcrumbs" />
    </header>
    <div class="p-6 overflow-auto space-y-10">
        <div class="p-4 border border-gray-300 rounded-sm">
            <h2 class="font-bold text-xl mb-4">Connection Settings</h2>

            <!-- TOPCV -->
            <div class="space-y-4">
                <div class="flex justify-between items-center">
                    <h3 class="font-bold text-lg">Connect to TopCV</h3>
                    <Switch size="sm" label="Activate" v-model="setting.active_topcv" />
                </div>

                <div v-if="setting.active_topcv" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                        <!-- Secret Key -->
                        <div class="relative">
                            <FormControl :type="showSecretKey ?  'text' : 'password' " placeholder="Secret key"
                                v-model="setting.secret_key_topcv" :label="__('Secret Key')" required 
                                :disabled="setting.status_topcv" />
                            <button type="button" v-if="!setting.status_topcv"
                                class="absolute top-[26px] right-2 text-sm text-gray-500 hover:text-black"
                                @click="showSecretKey = !showSecretKey">
                                {{ showSecretKey ? __('Hide') : __("Show") }}
                            </button>
                        </div>

                        <!-- Token Key -->
                        <div class="relative">
                            <FormControl :type="showTokenKey ? 'text' : 'password'" placeholder="Token key" required 
                                v-model="setting.access_token_topcv" :label="__('Token Key')"
                                :disabled="setting.status_topcv" />
                            <button type="button" v-if="!setting.status_topcv"
                                class="absolute top-[26px] right-2 text-sm text-gray-500 hover:text-black"
                                @click="showTokenKey = !showTokenKey">
                                {{ showTokenKey ? __('Hide') : __("Show") }}
                            </button>
                        </div>
                    </div>

                    <!-- Button ở góc phải dưới -->
                    <div class="flex justify-end items-end">
                        <Button variant="solid" :loading="connect_topcv.loading" v-if="!setting.status_topcv" @click="connectTopCV">{{ __('Connect')
                            }}</Button>
                        <Button variant="solid" theme="red" v-else @click="disconnect('topcv')">
                            {{ __('Disconnect') }}
                        </Button>

                    </div>
                </div>
            </div>

            <!-- Kết nối Facebook -->
            <div class="space-y-4 mt-10 border-t">
                <div class="flex justify-between items-center">
                    <h3 class="font-bold text-lg">Connect to Facebook</h3>
                    <Switch size="sm" label="Activate" v-model="setting.active_facebook" />
                </div>

                <div v-if="setting.active_facebook" class="grid grid-cols-1 md:grid-cols-2 gap-6">
             
                        <div class="space-y-4">
                            <!-- Secret Key -->
                            <div class="relative">
                                <FormControl :type="text" placeholder="Client ID" required 
                                    v-model="setting.facebook_client_id" :label="__('Client ID')"
                                    :disabled="setting.status_facebook" />
                                <!-- <button type="button" v-if="!setting.status_facebook"
                                    class="absolute top-[26px] right-2 text-sm text-gray-500 hover:text-black"
                                    @click="showSecretKey = !showSecretKey">
                                    {{ showSecretKey ? __('Hide') : __("Show") }}
                                </button> -->
                            </div>

                            <!-- Token Key -->
                            <div class="relative">
                                <FormControl :type="text" placeholder="Client Secret" required 
                                    v-model="setting.facebook_client_secret" :label="__('Client Secret')"
                                    :disabled="setting.status_facebook" />
                                <!-- <button type="button" v-if="!setting.status_topcv"
                                    class="absolute top-[26px] right-2 text-sm text-gray-500 hover:text-black"
                                    @click="showTokenKey = !showTokenKey">
                                    {{ showTokenKey ? __('Hide') : __("Show") }}
                                </button> -->
                            </div>
                        </div>
                    <div  class="flex justify-end items-end">
                        <Button variant="solid" v-if="!facebookConnected" @click="handleFacebook"  :loading="auth_Facebook.loading">
                            {{ __('Authenticate Facebook') }}
                        </Button>
                        <Button variant="solid" theme="red" v-else @click="disconnect('facebook')">
                            {{ __('Disconnect') }}
                        </Button>
                    </div>
                </div>
            </div>

            <!-- Kết nối LinkedIn -->
            <div class="space-y-4 mt-10 border-t">
                <div class="flex justify-between items-center">
                    <h3 class="font-bold text-lg">Connect to LinkedIn</h3>
                    <Switch size="sm" label="Activate" v-model="setting.active_linkedin" />
                </div>

                <div v-if="setting.active_linkedin"  class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="space-y-4">
                            <!-- Secret Key -->
                            <div class="relative">
                                <FormControl :type="text" placeholder="Client ID" required 
                                    v-model="setting.linkedin_client_id" :label="__('Secret Key')"
                                    :disabled="setting.status_linkedin" />
                                <!-- <button type="button" v-if="!setting.status_linkedin"
                                    class="absolute top-[26px] right-2 text-sm text-gray-500 hover:text-black"
                                    @click="showSecretKey = !showSecretKey">
                                    {{ showSecretKey ? __('Hide') : __("Show") }}
                                </button> -->
                            </div>

                            <!-- Token Key -->
                            <div class="relative">
                                <FormControl :type="text" placeholder="Client Secret" required 
                                    v-model="setting.linkedin_client_secret" :label="__('Token Key')"
                                    :disabled="setting.status_linkedin" />
                                <!-- <button type="button" v-if="!setting.status_linkedin"
                                    class="absolute top-[26px] right-2 text-sm text-gray-500 hover:text-black"
                                    @click="showTokenKey = !showTokenKey">
                                    {{ showTokenKey ? __('Hide') : __("Show") }}
                                </button> -->
                            </div>
                        </div>
                    <div  class="flex justify-end items-end">
                        <Button variant="solid" v-if="!linkedinConnected" :loading="auth_LinkedIn.loading" @click="handleLinkeIn">
                            {{ __('Authenticate LinkedIn') }}
                        </Button>
                        <Button variant="solid" theme="red" v-else @click="disconnect('linkedin')">
                            {{ __('Disconnect') }}
                        </Button>
                        <!-- <button @click="shareJobPost()">Chia sẻ lên LinkedIn</button> -->
                    </div>
                </div>
            </div>
        </div>

        <!-- Facebook Dialog -->
        <Dialog v-model="showFacebookDialog" :options="{
            size: 'xl',
            title: 'Authentication Facebook',
        }">
            <template #title>Authenticate Facebook</template>
            <template #body-content>
                <p class="text-sm text-gray-700 mb-4">Enter Facebook token to authenticate:</p>
                <FormControl label="Facebook Access Token" placeholder="Enter token" v-model="facebookTempToken" />
            </template>
            <template #footer>
                <Button variant="ghost" @click="showFacebookDialog = false">Close</Button>
                <Button @click="confirmFacebookConnect">Confirm</Button>
            </template>
        </Dialog>

        <!-- LinkedIn Dialog -->
        <Dialog v-model="showLinkedInDialog" :options="{
            size: 'xl',
            title: 'Authentication LinkedIn',
        }">
            <template #title>Authenticate LinkedIn</template>
            <template #body-content>
                <p class="text-sm text-gray-700 mb-4">Enter LinkedIn token to authenticate:</p>
                <FormControl label="LinkedIn Access Token" placeholder="Enter token" v-model="linkedinTempToken" />
            </template>
            <template #actions>
                <Button variant="ghost" @click="showLinkedInDialog = false">Close</Button>
                <Button @click="confirmLinkedInConnect">Confirm</Button>
            </template>
        </Dialog>
    </div>
    <ConfirmModal v-model="showConfirmModal" @confirm="() => actionConfirm(selectedPlatform)">
        <template #title>
            <div class="text-lg font-semibold text-center">
                {{ __("Confirm Disconnection") }}
            </div>
        </template>

        <template #content>
            <div class="text-center">
                {{ __("Are you sure you want to disconnect from") }}
                <span class="font-semibold text-red-500">{{ selectedPlatform }}</span>?
            </div>
        </template>
    </ConfirmModal>
</template>

<script setup>
import {
    Breadcrumbs,
    createResource,
    FormControl,
    Button,
    Switch,
    Dialog,
    toast,
    call
} from 'frappe-ui'

import { ref, reactive, computed, onMounted } from 'vue'
import { showToast, updateDocumentTitle } from '@/utils'
import ConfirmModal from "@/components/Modals/ConfirmModal.vue";

const setting = reactive({
    active_topcv: false,
    access_token_topcv: null,
    secret_key_topcv: null,
    api_access_token: null,
    status_topcv: 0,

    active_facebook: false,
    status_facebook: 0,
    facebook_client_id:null,
    facebook_client_secret:null,
    status_facebook: 0,

    active_linkedin: false,
    status_linkedin: 0,
    linkedin_client_id:null,
    linkedin_client_secret:null
})

const integrate_data = ref({})

// trạng thái toggle password
const showSecretKey = ref(false)
const showTokenKey = ref(false)

// trạng thái kết nối
const facebookConnected = ref(false)
const linkedinConnected = ref(false)

// dialog điều khiển
const showFacebookDialog = ref(false)
const showLinkedInDialog = ref(false)

// temp token trong modal
const facebookTempToken = ref('')
const linkedinTempToken = ref('')

const showConfirmModal = ref(false);
const selectedPlatform = ref(null); // "topcv", "facebook", "linkedin"

const disconnect = (platform) => {
    selectedPlatform.value = platform;
    showConfirmModal.value = true;
};

const actionConfirm = (platform) => {
    console.log("Disconnecting from", platform);
    // Gọi API tương ứng để ngắt kết nối
    // eg: await apiDisconnect(platform)
    if (platform == "topcv") {
        disconnectTopCV()
    } else if (platform == "facebook") {
        disconnectFacebook("Facebook")
    } else if (platform == "linkedin") {
        disconnectLinkedIn("Linkedin")
    }
    showConfirmModal.value = false;
};


// Kết nối giả lập
const connectTopCV = () => {
    connect_topcv.submit(
        {},
        {
            onSuccess(data) {
                showToast(__('Success'), __('Connect successfully'), 'check')
                checkStatus_TopCV.reload();
            },
            onError(err) {
                
                showToast(__('Error'), __(err?.message|| "Connect fail"), 'x')
                return;
            }
        }
    )
}

const disconnectTopCV = () => {
    disconnect_topcv.submit(
        {},
        {
            onSuccess(data) {
                showToast(__('Success'), __('Disconnect successfully'), 'check')
                checkStatus_TopCV.reload();
            },
            onError(err) {
                showToast(__('Error'), __(err.message || "Disconnect fail"), 'x')
                return;
            }
        }
    )
}

const confirmFacebookConnect = () => {
    if (facebookTempToken.value) {
        facebookConnected.value = true
        showFacebookDialog.value = false
        toast.success('Kết nối Facebook thành công!')
    } else {
        toast.error('Vui lòng nhập token Facebook!')
    }
}

const disconnectFacebook = () => {
    facebookConnected.value = false
    facebookTempToken.value = ''
    toast.info('Đã hủy kết nối Facebook.')
}

const handleLinkeIn = async () => {
    auth_LinkedIn.submit({
        client_id:setting.linkedin_client_id,
        client_secret:setting.linkedin_client_secret
    }, {
        onSuccess(data) {
            window.open(data, "linkedinPopup", "width=600,height=700");
        },
        onError(err) {
            showToast(__('Error'), __("Authentication LinkedIn fail"), 'x')
        }
    })

};
const auth_LinkedIn = createResource({
    url: 'mbw_mira.integration.social.get_linkedin_auth_url',
    auto: false,
    validate(params) {
        if (!params.client_id) {
            // return a string message to throw an error
            return __('client_id is required')
        }
        if (!params.client_secret) {
            // return a string message to throw an error
            return __('client_secret is required')
        }
    },
})

const handleFacebook = async () => {
    auth_Facebook.submit({
        client_id:setting.facebook_client_id,
        client_secret:setting.facebook_client_secret
    }, {
        onSuccess(data) {
            window.open(data, "facebookPopup", "width=600,height=700");
        },
        onError(err) {
            showToast(__('Error'), __(err.messages?.[0] || err), 'x')
        }
    })
};
const auth_Facebook = createResource({
    url: 'mbw_mira.integration.social.get_facebook_auth_url',
    auto: false,
    validate(params) {
        if (!params.client_id) {
            // return a string message to throw an error
            return __('client_id is required')
        }
        if (!params.client_secret) {
            // return a string message to throw an error
            return __('client_secret is required')
        }
    },
})

const disconnectLinkedIn = (platform) => {
    disconnect_linkedin.submit({
        platform: platform
    }, {
        onSuccess(data) {
            checkConnect.reload();
        },
        onError(err) {
            showToast(__('Error'), __("Disconnect LinkedIn fail"), 'x')
        }
    })
}

const disconnect_linkedin = createResource({
    url: 'mbw_mira.integration.social.disconnect_platform',
    auto: false
})

// Dữ liệu từ backend (mock)
const setting_Source = createResource({
    url: 'frappe.client.get',
    makeParams: () => ({ doctype: 'MIRA_Integrations' }),
    auto: false,
    onSuccess(data) {
        Object.keys(data).forEach((key) => {
            if (Object.hasOwn(setting, key)) {
                if (data[key] == 1) {
                    data[key] = true
                } else if (data[key] == 0) {
                    data[key] = false
                }
                setting[key] = data[key]
            }
        })
    }
})

const checkConnect = createResource({
    url: "mbw_mira.integration.social.check_social_media_connection",
    auto: false,
    onSuccess(data) {
        if (data.connected) {
            if (data.platform == 'Facebook') {
                setting.active_facebook = true;
                facebookConnected.value = true;
                setting.facebook_client_id = data.client_id
                setting.facebook_client_secret = data.client_secret
            } else if (data.platform == 'LinkedIn') {
                setting.active_linkedin = true;
                linkedinConnected.value = true;
                setting.linkedin_client_id = data.client_id;
                setting.linkedin_client_secret = data.client_secret;
            }
        }
    },
    onError(err) {

    }

})

//connect topcv
const connect_topcv = createResource({
    url: 'mbw_mira.integration.topcv.connect_topcv',
    validate(params) {
        if (!params.access_token_topcv) {
            // return a string message to throw an error
            return __('access_token_topcv is required')
        }
        if (!params.secret_key_topcv) {
            // return a string message to throw an error
            return __('secret_key_topcv is required')
        }
    },
    makeParams: () => ({
        access_token_topcv: setting['access_token_topcv'],
        secret_key_topcv: setting['secret_key_topcv']
    }),
    auto: false
})

const shareJobPost = () => {
    post_job.submit({}, {
        onSuccess(data) {

        },
        onError(err) {

        }
    })
}
//Post Job
const post_job = createResource({
    url: 'mbw_mira.integration.social.share_job_post_on_social_media',
    makeParams: () => ({
        job_post_id: "Tuyển dụng Lập trình Python",
        platform: 'linkedin'
    }),
    auto: false
})

//disconnect topcv
const disconnect_topcv = createResource({
    url: 'mbw_mira.integration.topcv.disconnect_topcv',
    method: "PUT",
    auto: false
})

const checkStatus_TopCV = createResource({
    url: 'frappe.client.get',
    makeParams(values) {
        return { doctype: 'MIRA_Integrations' }
    },
    auto: false,
    onSuccess(data) {
        setting.active_topcv = data.active_topcv == 1 ? true : false
        setting.status_topcv = data.status_topcv == 1 ? true : false
        setting.secret_key_topcv = data.secret_key_topcv
        setting.access_token_topcv = data.access_token_topcv
    },
    onError(err) {

    }
})



onMounted(() => {
    window.addEventListener("message", (event) => {
        if ((event.data?.platform === "linkedin" && event.data?.status === "connected") || (event.data.platform === "facebook" && event.data.status === "connected")) {
            // Đã kết nối thành công
            checkConnect.reload()
        }
    });
    setting_Source.reload();
    checkStatus_TopCV.reload();

})

const breadcrumbs = computed(() => [
    { label: __('Connect'), route: { name: 'integration' } },
])
const pageMeta = computed(() => {
    return {
        title: __('Integration'),
        description: __('Integration'),
    }
})

updateDocumentTitle(pageMeta)
</script>