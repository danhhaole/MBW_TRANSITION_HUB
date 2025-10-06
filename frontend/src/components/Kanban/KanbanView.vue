<template>
  <div class="flex overflow-x-auto h-full bg-surface-gray-1">
    <Draggable
      v-if="processColumns"
      :list="processColumns"
      item-key="stage_id"
      @end="updateStageOrder"
      :delay="isTouchScreenDevice() ? 200 : 0"
      class="flex sm:mx-2.5 mx-2 pb-3.5 gap-4"
    >
      <template #item="{ element: stage }">
        <div
          v-if="!stage.hidden"
          class="flex flex-col gap-3 min-w-80 w-80 bg-surface-white rounded-xl border border-surface-gray-3 p-4 shadow-sm hover:shadow-md transition-shadow"
        >
          <!-- 🎯 Stage Header -->
          <div class="flex gap-3 items-center group justify-between">
            <div class="flex items-center gap-3 flex-1">
              <!-- Stage Color Indicator -->
              <NestedPopover>
                <template #target>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="hover:!bg-surface-gray-2 p-1"
                  >
                    <IndicatorIcon :class="parseStageColor(stage.color || stage.stage_id)" />
                  </Button>
                </template>
                <template #body="{ close }">
                  <div class="flex flex-col gap-3 px-3 py-2.5 min-w-40 rounded-lg bg-surface-modal shadow-2xl ring-1 ring-black ring-opacity-5">
                    <div class="flex gap-1 flex-wrap">
                      <Button
                        variant="ghost"
                        v-for="color in stageColors"
                        :key="color"
                        @click="() => updateStageColor(stage.stage_id, color)"
                        class="p-1"
                      >
                        <IndicatorIcon :class="parseStageColor(color)" />
                      </Button>
                    </div>
                    <Button
                      variant="solid"
                      :label="__('Apply')"
                      @click="close"
                      size="sm"
                    />
                  </div>
                </template>
              </NestedPopover>

              <!-- Stage Info -->
              <div class="flex flex-col flex-1">
                <div class="text-ink-gray-9 font-semibold text-base">
                  {{ stage.stage_name || stage.stage_id }}
                </div>
                <div class="text-ink-gray-5 text-sm flex items-center gap-2">
                  <span class="font-bold text-lg text-ink-gray-7">
                    {{ stage.candidates?.length || 0 }}
                  </span>
                  <span>{{ __('candidates') }}</span>
                  <div v-if="stage.requirements?.duration" class="text-xs bg-surface-gray-2 px-2 py-1 rounded">
                    {{ stage.requirements.duration }}d max
                  </div>
                </div>
              </div>
            </div>

            <!-- Stage Actions -->
            <div class="flex gap-1">
              <Dropdown :options="stageActions(stage)">
                <template #default>
                  <Button
                    class="hidden group-hover:flex opacity-60 hover:opacity-100"
                    icon="more-horizontal"
                    variant="ghost"
                    size="sm"
                  />
                </template>
              </Dropdown>
              <Button
                icon="plus"
                variant="ghost"
                size="sm"
                @click="options.onNewCandidate?.(stage)"
                class="opacity-60 hover:opacity-100"
                :title="__('Add Candidate')"
              />
            </div>
          </div>

          <!-- 📋 Stage Requirements/Info -->
          <div v-if="stage.requirements || stage.steps?.length" class="text-xs bg-surface-gray-1 rounded-lg p-2">
            <div v-if="stage.requirements?.auto_advance" class="flex items-center gap-1 text-green-600 mb-1">
              <FeatherIcon name="zap" class="h-3 w-3" />
              <span>{{ __('Auto advance') }}</span>
            </div>
            <div v-if="stage.steps?.length" class="text-ink-gray-6">
              {{ stage.steps.length }} {{ __('steps configured') }}
            </div>
            <div v-if="stage.requirements?.required_approvals" class="text-ink-gray-6">
              {{ __('Requires') }} {{ stage.requirements.required_approvals }} {{ __('approvals') }}
            </div>
          </div>

          <!-- 👥 Candidates List -->
          <div class="overflow-y-auto flex flex-col gap-3 flex-1 max-h-96">
            <Draggable
              :list="stage.candidates || []"
              group="candidates"
              item-key="name"
              class="flex flex-col gap-3 flex-1"
              @end="moveCandidateToStage"
              :delay="isTouchScreenDevice() ? 200 : 0"
              :data-stage="stage.stage_id"
            >
              <template #item="{ element: candidate }">
                <component
                  :is="options.getRoute ? 'router-link' : 'div'"
                  class="bg-surface-white border border-surface-gray-3 rounded-lg p-3 cursor-pointer hover:border-surface-gray-4 hover:shadow-sm transition-all group/card"
                  :data-candidate="candidate.name"
                  v-bind="{
                    to: options.getRoute ? options.getRoute(candidate) : undefined,
                    onClick: options.onClick ? () => options.onClick(candidate) : undefined,
                  }"
                >
                  <!-- Candidate Header -->
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex-1 min-w-0">
                      <div class="font-medium text-ink-gray-9 truncate">
                        {{ candidate.can_full_name || candidate.name }}
                      </div>
                      <div class="text-sm text-ink-gray-5 truncate">
                        {{ candidate.can_email }}
                      </div>
                    </div>
                    <div class="ml-2 flex-shrink-0">
                      <Badge :status="candidate.status" ></Badge>
                    </div>
                  </div>

                  <!-- Candidate Details -->
                  <div class="space-y-2 text-sm">
                    <!-- Application Date -->
                    <div v-if="candidate.can_application_date" class="flex items-center gap-2 text-ink-gray-6">
                      <FeatherIcon name="calendar" class="h-3 w-3" />
                      <span>{{ formatDate(candidate.can_application_date) }}</span>
                    </div>

                    <!-- Current Stage Duration -->
                    <div v-if="candidate.stage_duration" class="flex items-center gap-2 text-ink-gray-6">
                      <FeatherIcon name="clock" class="h-3 w-3" />
                      <span>{{ candidate.stage_duration }}d in stage</span>
                    </div>

                    <!-- Source -->
                    <div v-if="candidate.candidatesource_id" class="flex items-center gap-2 text-ink-gray-6">
                      <FeatherIcon name="users" class="h-3 w-3" />
                      <span>{{ candidate.candidatesource_id }}</span>
                    </div>

                    <!-- Score/Rating -->
                    <div v-if="candidate.overall_score" class="flex items-center gap-2">
                      <FeatherIcon name="star" class="h-3 w-3 text-yellow-500" />
                      <div class="flex-1 bg-surface-gray-2 rounded-full h-2">
                        <div 
                          class="bg-yellow-500 h-2 rounded-full" 
                          :style="`width: ${(candidate.overall_score || 0)}%`"
                        ></div>
                      </div>
                      <span class="text-xs font-medium">{{ candidate.overall_score }}%</span>
                    </div>
                  </div>

                  <!-- Quick Actions -->
                  <div class="flex items-center justify-between mt-3 pt-2 border-t border-surface-gray-2">
                    <div class="flex gap-1">
                      <Button
                        v-if="candidate.can_cv_file"
                        icon="file-text"
                        variant="ghost"
                        size="sm"
                        @click.stop="viewCV(candidate)"
                        :title="__('View CV')"
                        class="opacity-0 group-hover/card:opacity-100 transition-opacity"
                      />
                      <Button
                        icon="message-circle"
                        variant="ghost"
                        size="sm"
                        @click.stop="sendMessage(candidate)"
                        :title="__('Send Message')"
                        class="opacity-0 group-hover/card:opacity-100 transition-opacity"
                      />
                    </div>
                    <div class="flex gap-1">
                      <Button
                        icon="calendar"
                        variant="ghost"
                        size="sm"
                        @click.stop="scheduleInterview(candidate)"
                        :title="__('Schedule Interview')"
                        class="opacity-0 group-hover/card:opacity-100 transition-opacity"
                      />
                      <Button
                        icon="arrow-right"
                        variant="ghost"
                        size="sm"
                        @click.stop="advanceCandidate(candidate)"
                        :title="__('Advance')"
                        class="opacity-0 group-hover/card:opacity-100 transition-opacity"
                      />
                    </div>
                  </div>
                </component>
              </template>
            </Draggable>

            <!-- Load More Button -->
            <div
              v-if="stage.hasMore"
              class="flex items-center justify-center"
            >
              <Button
                :label="__('Load More')"
                @click="emit('loadMore', stage.stage_id)"
                variant="ghost"
                size="sm"
              />
            </div>
          </div>

          <!-- Add Candidate Button -->
          <div class="pt-2 border-t border-surface-gray-2">
            <Button
              :label="__('Add Candidate')"
              variant="ghost"
              class="w-full text-ink-gray-5 hover:text-ink-gray-7"
              @click="options.onNewCandidate?.(stage)"
            >
              <template #prefix>
                <FeatherIcon name="plus" class="h-4 w-4" />
              </template>
            </Button>
          </div>
        </div>
      </template>
    </Draggable>

    <!-- Add Stage Button -->
    <div v-if="allowAddStage" class="shrink-0 min-w-64 flex items-start pt-4">
      <Button
        :label="__('Add Stage')"
        variant="outline"
        class="w-full"
        @click="emit('addStage')"
      >
        <template #prefix>
          <FeatherIcon name="plus" class="h-4" />
        </template>
      </Button>
    </div>
  </div>
</template>

<script setup>
import Autocomplete from '@/components/frappe-ui/Autocomplete.vue'
import NestedPopover from '@/components/NestedPopover.vue'
import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
import { isTouchScreenDevice, parseColor } from '@/utils'
import Draggable from 'vuedraggable'
import { Dropdown, FeatherIcon,Badge } from 'frappe-ui'
import { computed, ref } from 'vue'

const props = defineProps({
  recruitmentProcess: {
    type: Array,
    default: () => []
  },
  candidates: {
    type: Array,
    default: () => []
  },
  options: {
    type: Object,
    default: () => ({
      getRoute: null,
      onClick: null,
      onNewCandidate: null,
    }),
  },
  allowAddStage: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update', 'loadMore', 'addStage', 'moveCandidate', 'updateStageOrder'])

// 🎨 Stage Colors
const stageColors = ['blue', 'green', 'yellow', 'red', 'purple', 'pink', 'indigo', 'gray']

const parseStageColor = (color) => {
  const colorMap = {
    'blue': 'text-blue-500',
    'green': 'text-green-500',
    'yellow': 'text-yellow-500',
    'red': 'text-red-500',
    'purple': 'text-purple-500',
    'pink': 'text-pink-500',
    'indigo': 'text-indigo-500',
    'gray': 'text-gray-500',
    // Default mapping by stage name
    'screening': 'text-blue-500',
    'interview': 'text-yellow-500',
    'technical': 'text-purple-500',
    'final': 'text-green-500',
    'offer': 'text-green-600',
    'hired': 'text-green-700',
    'rejected': 'text-red-500'
  }
  return colorMap[color] || colorMap[color?.toLowerCase()] || 'text-gray-500'
}

// 📊 Process Columns từ recruitment_process
const processColumns = computed(() => {
  if (!props.recruitmentProcess?.length) return []

  return props.recruitmentProcess
    .filter(stage => !stage.hidden)
    .sort((a, b) => (a.stage_order || 0) - (b.stage_order || 0))
    .map(stage => {
      // Lọc candidates theo stage
      const stageCandidates = props.candidates.filter(candidate => 
        candidate.current_stage === stage.stage_id || 
        candidate.status === stage.stage_id
      )

      return {
        ...stage,
        candidates: stageCandidates,
        hasMore: false, // Implement pagination logic if needed
        color: stage.color || getDefaultStageColor(stage.stage_id)
      }
    })
})

// 🎯 Default colors based on stage type
const getDefaultStageColor = (stageId) => {
  const defaults = {
    'screening': 'blue',
    'phone_screen': 'blue',
    'technical': 'purple',
    'interview': 'yellow',
    'final_interview': 'yellow',
    'reference': 'indigo',
    'offer': 'green',
    'hired': 'green',
    'rejected': 'red',
    'withdrawn': 'gray'
  }
  return defaults[stageId?.toLowerCase()] || 'gray'
}

// 🔧 Stage Actions
const stageActions = (stage) => [
  {
    group: __('Stage Options'),
    hideLabel: true,
    items: [
      {
        label: __('Edit Stage'),
        icon: 'edit',
        onClick: () => emit('editStage', stage),
      },
      {
        label: __('Configure Steps'),
        icon: 'settings',
        onClick: () => emit('configureSteps', stage),
      },
      {
        label: __('View Analytics'),
        icon: 'bar-chart-2',
        onClick: () => emit('viewAnalytics', stage),
      },
      {
        label: __('Hide Stage'),
        icon: 'eye-off',
        onClick: () => hideStage(stage.stage_id),
      }
    ],
  },
]

// 📅 Date formatting
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric'
  })
}

// 🎬 Actions
const updateStageColor = (stageId, color) => {
  emit('update', {
    type: 'stage_color',
    stage_id: stageId,
    color: color
  })
}

const hideStage = (stageId) => {
  emit('update', {
    type: 'hide_stage',
    stage_id: stageId
  })
}

const updateStageOrder = (event) => {
  const newOrder = processColumns.value.map((stage, index) => ({
    stage_id: stage.stage_id,
    stage_order: index
  }))
  
  emit('updateStageOrder', newOrder)
}

const moveCandidateToStage = (event) => {
  const candidateName = event.item.dataset.candidate
  const toStage = event.to.dataset.stage
  const fromStage = event.from.dataset.stage
  
  if (toStage !== fromStage && candidateName) {
    emit('moveCandidate', {
      candidate: candidateName,
      fromStage,
      toStage
    })
  }
}

// 🎯 Quick Actions
const viewCV = (candidate) => {
  // Implement CV viewer
  emit('viewCV', candidate)
}

const sendMessage = (candidate) => {
  // Implement messaging
  emit('sendMessage', candidate)
}

const scheduleInterview = (candidate) => {
  // Implement interview scheduling
  emit('scheduleInterview', candidate)
}

const advanceCandidate = (candidate) => {
  // Implement candidate advancement
  emit('advanceCandidate', candidate)
}
</script>

<style scoped>
/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Drag and drop visual feedback */
.sortable-chosen {
  transform: rotate(2deg);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.sortable-ghost {
  opacity: 0.5;
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
}
</style>