<template>
  <v-container fluid class="pa-6">
    <div>
      <!-- Header -->
      <div class="d-flex align-center justify-space-between mb-6">
        <h1 class="text-h4 font-weight-bold">Talent Pools</h1>

        <div class="d-flex align-center">
          <!-- Search box -->
          <v-text-field 
            :model-value="filters.searchText"
            @update:model-value="handleSearch"
            placeholder="Search pools..."
            prepend-inner-icon="mdi-magnify"
            variant="outlined"
            density="compact"
            hide-details 
            class="mr-4" 
            style="width: 300px;"
            :loading="loading || isSearching"
            clearable
            @click:clear="clearSearch"
          />

          <!-- Create Button -->
          <v-btn
            color="primary"
            variant="elevated"
            @click="showCreateForm = true"
            prepend-icon="mdi-plus"
            class="text-none px-6"
            style="text-transform: none;"
          >
            Create Pool
          </v-btn>
        </div>
      </div>



      <!-- Loading State -->
      <div v-if="loading && !segments.length" class="text-center py-8">
        <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
        <div class="mt-2">Đang tải dữ liệu...</div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!loading && !segments.length" class="text-center py-12">
        <v-icon size="80" color="grey-lighten-1">mdi-account-group-outline</v-icon>
        <h3 class="text-h6 mt-4 mb-2">Chưa có phân khúc nào</h3>
        <p class="text-body-2 text-medium-emphasis mb-4">
          Tạo phân khúc đầu tiên để bắt đầu quản lý ứng viên
        </p>
        <v-btn 
          color="primary" 
          variant="elevated"
          @click="showCreateForm = true"
          prepend-icon="mdi-plus"
        >
          Tạo Phân khúc
        </v-btn>
      </div>

      <!-- Segments Grid -->
      <div v-else>
        <!-- Card View Only -->
        <TalentSegmentCardView
          :segments="segments"
          :loading="loading"
          @view-details="handleViewDetails"
          @edit="handleEdit"
          @delete="handleDelete"
          @create="showCreateForm = true"
        />
      </div>

      <!-- Success/Error Toast -->
      <ToastContainer 
        :show="!!error || success" 
        :message="error || (success ? 'Thao tác thành công!' : '')"
        :type="error ? 'error' : 'success'"
        @close="error = null; success = false"
      />
    </div>

    <!-- Create/Edit Dialog -->
    <TalentSegmentForm
      v-model="showCreateForm"
      :segment="editingSegment"
      @success="handleFormSuccess"
      @close="handleFormClose"
    />



    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="showDeleteDialog" max-width="500">
      <v-card>
        <v-card-title class="text-h6">Xác nhận xóa</v-card-title>
        <v-card-text>
          Bạn có chắc chắn muốn xóa phân khúc "<strong>{{ deletingSegment?.title }}</strong>"?
          Hành động này không thể hoàn tác.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn 
            variant="text" 
            @click="showDeleteDialog = false"
            :disabled="loading"
          >
            Hủy
          </v-btn>
          <v-btn 
            color="error" 
            variant="elevated"
            @click="confirmDelete"
            :loading="loading"
          >
            Xóa
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useTalentSegment } from '@/composables/useTalentSegment'
import { 
  TalentSegmentCardView,
  TalentSegmentTable,
  TalentSegmentForm
} from '@/components/talent-segment'
import { ToastContainer } from '@/components/shared'

// Composables
const router = useRouter()
const {
  segments,
  selectedSegment, 
  loading,
  error,
  success,
  filters,
  isSearching,
  segmentCount,
  loadSegments,
  searchSegments,
  clearSearch,
  setTypeFilter,
  getSegmentDetails,
  deleteSegment
} = useTalentSegment()

// Local state
const viewMode = ref('grid')
const showCreateForm = ref(false)
const showDeleteDialog = ref(false)
const editingSegment = ref(null)
const deletingSegment = ref(null)

// Filter options
const typeFilterOptions = [
  { title: 'Tất cả', value: 'all' },
  { title: 'Tự động (AI)', value: 'DYNAMIC' },
  { title: 'Thủ công', value: 'MANUAL' }
]

// Computed
const dynamicSegmentCount = computed(() => 
  segments.value.filter(s => s.type === 'DYNAMIC').length
)

const manualSegmentCount = computed(() => 
  segments.value.filter(s => s.type === 'MANUAL').length
)

const totalCandidates = computed(() => 
  segments.value.reduce((sum, s) => sum + (s.candidate_count || 0), 0)
)

// Search handling
const handleSearch = (searchText) => {
  if (searchText !== filters.searchText) {
    searchSegments(searchText || '')
  }
}

// Event handlers
const handleViewDetails = async (segment) => {
  // Navigate to detail page instead of modal
  router.push(`/talent-segments/${segment.name}`)
}

const handleEdit = (segment) => {
  editingSegment.value = segment
  showCreateForm.value = true
}



const handleDelete = (segment) => {
  deletingSegment.value = segment
  showDeleteDialog.value = true
}

const confirmDelete = async () => {
  if (!deletingSegment.value) return
  
  const result = await deleteSegment(deletingSegment.value.name)
  if (result) {
    showDeleteDialog.value = false
    deletingSegment.value = null
  }
}

const handleFormSuccess = async () => {
  showCreateForm.value = false
  editingSegment.value = null
  await loadSegments()
}

const handleFormClose = () => {
  showCreateForm.value = false
  editingSegment.value = null
}

// Watch for search results count
watch(() => filters.searchText, (newValue) => {
  if (newValue && segments.value.length > 0) {
    // Show search results count
    setTimeout(() => {
      success.value = true
      setTimeout(() => {
        success.value = false
      }, 2000)
    }, 500)
  }
})

// Initialize
onMounted(() => {
  loadSegments()
})
</script>

<style scoped>
.v-container {
  max-width: 100%;
}

/* Loading animation for cards */
.segment-card {
  transition: all 0.3s ease;
}

.segment-card:hover {
  transform: translateY(-2px);
}

/* Custom button styles */
.v-btn.text-none {
  text-transform: none;
}

/* Toast positioning */
.toast-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 1000;
}
</style> 