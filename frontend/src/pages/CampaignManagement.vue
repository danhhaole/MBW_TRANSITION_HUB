<template>
    <v-container fluid>
        <!-- Header -->
        <div class="d-flex align-center justify-space-between mb-4">
            <h1 class="text-h5 font-weight-bold text-no-wrap">Danh sách yêu cầu tuyển dụng</h1>

            <div class="d-flex align-center flex-1-1 w-100 justify-end">
                <!-- Search box -->
                <v-text-field 
                    v-model="searchText" 
                    prepend-inner-icon="mdi-magnify" 
                    placeholder="Tìm kiếm tên chiến dịch, mô tả..."
                    variant="outlined" 
                    density="compact" 
                    hide-details 
                    class="mr-2" 
                    style="max-width: 500px; width: 100% ; --v-field-focused-outline-width: 1px;"
                    :loading="loading || isSearching"
                    clearable
                    @update:model-value="setSearchText" 
                    @click:clear="handleClearSearch"
                />

                <!-- View mode toggle -->
                <v-btn-toggle v-model="viewMode" mandatory color="deep-purple-accent-3" density="comfortable"
                    class="mr-2">
                    <v-btn value="list" prepend-icon="mdi-format-list-bulleted">
                        List
                    </v-btn>
                    <v-btn value="card" prepend-icon="mdi-view-grid">
                        Card
                    </v-btn>
                </v-btn-toggle>

                <!-- Create button -->
                <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
                    Tạo mới
                </v-btn>
            </div>
        </div>

        <!-- Main content -->
        <v-card>
            <!-- Table/Card view -->
            <campaign-table v-if="viewMode === 'list'" 
                :campaigns="campaigns" 
                :loading="loading"
                :pagination="pagination"
                :search-text="searchText" 
                :status-filter="statusFilter" 
                :type-filter="typeFilter"
                :active-filter="activeFilter" 
                @update:search-text="setSearchText"
                @update:status-filter="setStatusFilter" 
                @update:type-filter="setTypeFilter"
                @update:active-filter="setActiveFilter" 
                @page-change="goToPage"
                @items-per-page-change="changeItemsPerPage"
                @refresh="handleRefresh" 
                @edit="openEditDialog"
                @view="openViewDialog" 
                @delete="handleDelete" />


            <campaign-card-view v-else :campaigns="campaigns" :loading="loading" @edit="openEditDialog"
                @view="openViewDialog" @delete="handleDelete" @create="openCreateDialog"/>


        </v-card>

        <!-- Dialogs -->
        <!-- Wizard cho tạo mới -->
        <campaign-wizard v-model="showCreateWizard" @success="handleCreateSuccess" />
        
        <!-- Form cho chỉnh sửa -->
        <campaign-form v-model="showEditForm" :campaign="selectedCampaign" 
            @success="handleEditSuccess" @cancel="handleFormCancel" />

        <!-- Dialog xem chi tiết -->
        <campaign-view v-model="showViewDialog" :campaign="selectedCampaign" @edit="editFromView" />

        <!-- Toast notifications -->
        <toast-container />
    </v-container>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useCampaignList, useCampaignCRUD } from '../composables/useCampaign'
import { useToast } from '@/composables/useToast'
import { 
  CampaignTable,
  CampaignCardView,
  CampaignWizard,
  CampaignForm,
  CampaignView
} from '@/components/campaign'
import { ToastContainer } from '@/components/shared'

// Router
const router = useRouter()

// Page state
const viewMode = ref('list')
const showCreateWizard = ref(false)  // Wizard cho tạo mới
const showEditForm = ref(false)      // Form cho chỉnh sửa
const showViewDialog = ref(false)
const selectedCampaign = ref(null)
const refreshTrigger = ref(0)
const searchDebounceTimer = ref(null)
const isSearching = ref(false)

// Composables
const {
    campaigns,
    loading,
    pagination,
    loadCampaigns,
    searchText,
    statusFilter,
    typeFilter,
    activeFilter,
    goToPage,
    changeItemsPerPage,
    setSearchText,
    setStatusFilter,
    setTypeFilter,
    setActiveFilter
} = useCampaignList()

const { deleteCampaign } = useCampaignCRUD()
const { showToast } = useToast()

// Debounced search function
const debouncedSearch = (searchValue) => {
    // Clear existing timer
    if (searchDebounceTimer.value) {
        clearTimeout(searchDebounceTimer.value)
    }
    
    // Set new timer
    searchDebounceTimer.value = setTimeout(async () => {
        isSearching.value = true
        console.log('Performing search for:', searchValue)
        
        try {
            // Prepare filters
            const filters = {
                status: statusFilter.value !== 'all' ? statusFilter.value : undefined,
                type: typeFilter.value !== 'all' ? typeFilter.value : undefined,
                isActive: activeFilter.value !== 'all' ? (activeFilter.value === 'active') : undefined
            }
            
            // Only add searchText if it's not empty
            if (searchValue && searchValue.trim()) {
                filters.searchText = searchValue.trim()
            }
            
            await loadCampaigns(filters)
            
            // Show search feedback
            if (searchValue && searchValue.trim()) {
                const resultCount = campaigns.value.length
                showToast(`Tìm thấy ${resultCount} kết quả cho "${searchValue}"`, 'info', 3000)
            }
        } finally {
            isSearching.value = false
        }
    }, 500) // 500ms delay
}

// Watch search text changes
watch(searchText, (newValue) => {
    debouncedSearch(newValue)
}, { immediate: false })

// Event handlers
const openCreateDialog = () => {
    selectedCampaign.value = null
    showCreateWizard.value = true
}

const openEditDialog = (campaign) => {
    selectedCampaign.value = campaign
    showEditForm.value = true
}

const openViewDialog = (campaign) => {
    // Navigate to campaign detail view instead of opening modal
    router.push(`/campaigns/${campaign.name}`)
}

const editFromView = () => {
    showViewDialog.value = false
    showEditForm.value = true
}

const handleCreateSuccess = async (event) => {
    const { action, data } = event
    
    console.log('Create wizard success:', { action, data })
    console.log('Campaigns before reload:', campaigns.value.length)
    
    // Close wizard
    showCreateWizard.value = false
    selectedCampaign.value = null
    
    // Reload data
    await loadCampaigns()
    
    console.log('Campaigns after reload:', campaigns.value.length)
    
    // Show success message
    showToast(`Đã tạo chiến dịch "${data.campaign_name}" thành công!`, 'success')
}

const handleEditSuccess = async (event) => {
    const { action, data } = event
    
    console.log('Edit form success:', { action, data })
    console.log('Campaigns before reload:', campaigns.value.length)
    
    // Close form
    showEditForm.value = false
    selectedCampaign.value = null
    
    // Reload data
    await loadCampaigns()
    
    console.log('Campaigns after reload:', campaigns.value.length)
    
    // Show success message
    showToast(`Đã cập nhật chiến dịch "${data.campaign_name}" thành công!`, 'success')
}

const handleFormCancel = () => {
    showEditForm.value = false
    selectedCampaign.value = null
}

const handleClearSearch = () => {
    searchText.value = ''
    // Clear search sẽ trigger watcher và reload data
}



const handleRefresh = async () => {
    await loadCampaigns()

    showToast('Đã làm mới dữ liệu', 'info', 2000)
}

const handleDelete = async (campaign) => {
    try {
        const success = await deleteCampaign(campaign.name, campaign.campaign_name)

        if (success) {
            showToast(`Đã xóa chiến dịch "${campaign.campaign_name}"`, 'success')
            loadCampaigns()
        } else {
            showToast('Có lỗi xảy ra khi xóa chiến dịch', 'error')
        }
    } catch (error) {
        showToast('Có lỗi xảy ra khi xóa chiến dịch', 'error')
    }
}

// Initialize
onMounted(() => {
    loadCampaigns()
})

// Cleanup
onUnmounted(() => {
    if (searchDebounceTimer.value) {
        clearTimeout(searchDebounceTimer.value)
    }
})
</script>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    pointer-events: none;
}

.toast-container .v-snackbar {
    pointer-events: all;
}
</style>