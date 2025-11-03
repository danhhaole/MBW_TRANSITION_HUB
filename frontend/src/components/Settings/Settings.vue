<template>
  <Dialog
    v-model="showSettings"
    :options="{ size: '5xl' }"
    @close="activeSettingsPage = ''"
    :disableOutsideClickToClose="true"
  >
    <template #body>
      <div class="relative">
        <div class="relative flex h-[calc(100vh_-_8rem)]">
        <div class="flex flex-col p-1 w-52 shrink-0 bg-surface-gray-2">
          <!-- Header với Close Button -->
          <div class="flex items-center justify-between px-3 pt-3 pb-2">
            <h1 class="text-lg font-semibold text-ink-gray-8">
              {{ __('Settings') }}
            </h1>
            <button
              @click="showSettings = false"
              class="flex items-center justify-center w-7 h-7 rounded-full hover:bg-gray-200 transition-colors"
              :title="__('Close Settings')"
            >
              <FeatherIcon name="x" class="w-4 h-4 text-red-500 hover:text-red-600" />
            </button>
          </div>
          <div class="flex flex-col overflow-y-auto">
            <template v-for="tab in tabs" :key="tab.label">
              <div
                v-if="!tab.hideLabel"
                class="py-[7px] px-2 my-1 flex cursor-pointer gap-1.5 text-base text-ink-gray-5 transition-all duration-300 ease-in-out"
              >
                <span>{{ __(tab.label) }}</span>
              </div>
              <nav class="space-y-1 px-1">
                <SidebarLink
                  v-for="i in tab.items"
                  :key="i.label"
                  :icon="i.icon"
                  :label="__(i.label)"
                  class="w-full"
                  :class="
                    activeTab?.label == i.label
                      ? 'bg-surface-selected shadow-sm hover:bg-surface-selected'
                      : 'hover:bg-surface-gray-3'
                  "
                  @click="handleItemClick(i)"
                />
              </nav>
            </template>
          </div>
        </div>
        <div class="flex flex-col flex-1 bg-surface-modal">
          <component :is="activeTab.component" v-if="activeTab" />
        </div>
        </div>
      </div>
    </template>
  </Dialog>
</template>
<script setup>
import Email2Icon from '@/components/Icons/Email2Icon.vue'
import TagIcon from '@/components/Icons/TagIcon.vue'
import ExternalLinkIcon from '@/components/Icons/ExternalLinkIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import CampaignTemplateSettings from '@/components/Settings/CampaignTemplateSettings.vue'
import TagSettings from '@/components/Settings/TagSettings.vue'
import ConnectorSettings from '@/components/Settings/ConnectorSettings.vue'
import MiraEmailTemplateSettings from '@/components/Settings/MiraEmailTemplateSettings.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import { usersStore } from '@/stores/users'
import {
  showSettings,
  activeSettingsPage,
} from '@/composables/settings'
import  { Dialog, Button, FeatherIcon }  from 'frappe-ui'
import { ref, markRaw, computed, watch, h } from 'vue'
import { useRouter } from 'vue-router'

const { getUser } = usersStore()
const router = useRouter()

const user = computed(() => getUser() || {})

const tabs = computed(() => {
  let _tabs = [

    // {
    //   label: __('Automation'),
    //   hideLabel: false,
    //   items: [
    //     {
    //       label: __('Campaign Templates'),
    //       icon: NoteIcon,
    //       component: markRaw(CampaignTemplateSettings),
    //     },
    //   ],
    // },
    {
      label: __('Organization'),
      hideLabel: false,
      items: [
        {
          label: __('Tags'),
          icon: TagIcon,
          component: markRaw(TagSettings),
        },
      ],
    },
    {
      label: __('Integrations'),
      hideLabel: false,
      items: [
        {
          label: __('Connectors'),
          icon: ExternalLinkIcon,
          component: markRaw(ConnectorSettings),
        },
      ],
    },
        {
      label: __('Communication'),
      hideLabel: false,
      items: [
        {
          label: __('Email Templates'),
          icon: Email2Icon,
          component: markRaw(MiraEmailTemplateSettings),
        },
      ],
    },
  ]

  return _tabs.filter((tab) => {
    if (tab.condition && !tab.condition()) return false
    if (tab.items) {
      tab.items = tab.items.filter((item) => {
        if (item.condition && !item.condition()) return false
        return true
      })
    }
    return true
  })
})

const activeTab = ref(tabs.value[0].items[0])

function setActiveTab(tabName) {
  activeTab.value =
    (tabName &&
      tabs.value
        .map((tab) => tab.items)
        .flat()
        .find((tab) => tab.label === tabName)) ||
    tabs.value[0].items[0]
}

function handleItemClick(item) {
  // Show component in modal
  activeSettingsPage.value = item.label
}

watch(activeSettingsPage, (activePage) => setActiveTab(activePage))
</script>
