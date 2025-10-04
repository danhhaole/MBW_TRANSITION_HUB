<template>
  <div class="relative flex h-full flex-col justify-between transition-all duration-300 ease-in-out"
    :class="isSidebarCollapsed ? 'w-12' : 'w-[230px]'">
    <div>
      <UserDropdown class="p-2" :isCollapsed="isSidebarCollapsed" />
    </div>
    <div class="flex-1 overflow-y-auto">
      <div class="mb-3 flex flex-col">
        <SidebarLink id="notifications-btn" :label="__('Notifications')" :icon="NotificationsIcon"
          :isCollapsed="isSidebarCollapsed" @click="() => toggleNotificationPanel()" class="relative mx-2 my-0.5">
          <template #right>
            <Badge v-if="!isSidebarCollapsed && unreadNotificationsCount" :label="unreadNotificationsCount"
              variant="subtle" />
            <div v-else-if="unreadNotificationsCount"
              class="absolute -left-1.5 top-1 z-20 h-[5px] w-[5px] translate-x-6 translate-y-1 rounded-full bg-surface-gray-6 ring-1 ring-white" />
          </template>
        </SidebarLink>
      </div>
      <div v-for="view in allViews" :key="view.label">
        <div v-if="!view.hideLabel && isSidebarCollapsed && view.views?.length" class="mx-2 my-2 h-1 border-b" />
        <Section :label="view.name" :hideLabel="view.hideLabel" :opened="view.opened">
          <template #header="{ opened, hide, toggle }">
            <div v-if="!hide"
              class="flex cursor-pointer gap-1.5 px-1 text-base font-medium text-ink-gray-5 transition-all duration-300 ease-in-out"
              :class="isSidebarCollapsed
                ? 'ml-0 h-0 overflow-hidden opacity-0'
                : 'ml-2 mt-4 h-7 w-auto opacity-100'
                " @click="toggle()">
              <FeatherIcon name="chevron-right" class="h-4 text-ink-gray-9 transition-all duration-300 ease-in-out"
                :class="{ 'rotate-90': opened }" />
              <span>{{ __(view.name) }}</span>
            </div>
          </template>
          <nav class="flex flex-col">
            <!-- Main menu items -->
            <template v-for="link in view.views" :key="link.label">
              <!-- Menu item không có submenu -->
              <SidebarLink v-if="!link.submenu || link.submenu.length === 0" :icon="link.icon" :label="__(link.label)"
                :to="link.to" :isCollapsed="isSidebarCollapsed" class="mx-2 my-0.5" />

              <!-- Menu item có submenu -->
              <div v-else class="mx-2 my-0.5 relative group overflow-visible">
                <!-- Parent menu item với icon expand/collapse -->
                <div @click="!isSidebarCollapsed && toggleSubmenu(link.label)"
                  @mouseenter="isSidebarCollapsed && onEnterParent(link.label, $event)"
                  @mouseleave="isSidebarCollapsed && onLeaveParent()"
                  class="flex items-center cursor-pointer rounded-lg hover:bg-gray-50 transition-colors duration-200"
                  :class="[
                    isSidebarCollapsed ? 'p-2 justify-center' : 'px-2 py-2',
                    hasActiveSubmenuItem(link.submenu)
                      ? 'bg-gray-200 text-gray-900 font-semibold border-l-3 border-gray-400'
                      : ''
                  ]">
                  <!-- Icon của menu chính -->
                  <div class="flex-shrink-0">
                    <component :is="link.icon" class="h-4 w-4" :class="[
                      isSidebarCollapsed ? '' : 'mr-3',
                      hasActiveSubmenuItem(link.submenu) ? 'text-gray-900' : 'text-ink-gray-7'
                    ]" />
                  </div>

                  <!-- Label và chevron (chỉ hiện khi sidebar mở) -->
                  <div v-if="!isSidebarCollapsed" class="flex items-center justify-between flex-1 min-w-0">
                    <span class="text-sm font-medium truncate"
                      :class="hasActiveSubmenuItem(link.submenu) ? 'text-gray-900' : 'text-ink-gray-7'">
                      {{ __(link.label) }}
                    </span>
                    <FeatherIcon name="chevron-right"
                      class="h-3 w-3 text-ink-gray-5 transition-transform duration-200 flex-shrink-0 ml-2"
                      :class="{ 'rotate-90': expandedMenus[link.label] }" />
                  </div>
                </div>

                <!-- Submenu items - EXPANDED MODE -->
                <div v-if="!isSidebarCollapsed" class="overflow-hidden transition-all duration-300 ease-in-out"
                  :class="expandedMenus[link.label] ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'">
                  <div class="pl-10 pr-2 py-1 space-y-1">
                    <SidebarLink v-for="sublink in link.submenu" :key="sublink.label" :label="__(sublink.label)"
                      :to="sublink.to" :isCollapsed="false" class="text-sm submenu-item" :icon="sublink.icon" />
                  </div>
                </div>

                <!-- Flyout submenu - COLLAPSED MODE -->
                <Teleport to="body">
                  <transition name="fade">
                    <div v-if="isSidebarCollapsed && hoveredParent === link.label && link.submenu?.length"
                      :style="flyoutStyle(link.label)"
                      class="fixed z-[99999] bg-white shadow-lg rounded-lg border border-gray-200 py-2 min-w-[12rem]"
                      @mouseenter="onEnterParent(link.label)" @mouseleave="onLeaveParent()">
                      <div class="px-3 py-2 border-b text-sm font-medium text-ink-gray-8">
                        {{ __(link.label) }}
                      </div>
                      <router-link v-for="sublink in link.submenu" :key="sublink.label" :to="sublink.to"
                        class="block px-3 py-2 text-sm text-gray-600 hover:bg-gray-200 hover:text-gray-900 hover:font-semibold transition-colors duration-150"
                        :class="{ 'bg-gray-100 text-gray-900 font-semibold': $route.name === (sublink.to.name || sublink.to) }">
                        {{ __(sublink.label) }}
                      </router-link>
                    </div>
                  </transition>
                </Teleport>
              </div>
            </template>
          </nav>
        </Section>
      </div>
    </div>
    <div class="m-2 flex flex-col gap-1">
      <div class="flex flex-col gap-2 mb-1">
        <SignupBanner v-if="isDemoSite" :isSidebarCollapsed="isSidebarCollapsed"
          :afterSignup="() => capture('signup_from_demo_site')" />
        <TrialBanner v-if="isFCSite" :isSidebarCollapsed="isSidebarCollapsed"
          :afterUpgrade="() => capture('upgrade_plan_from_trial_banner')" />
      </div>
      <SidebarLink :label="isSidebarCollapsed ? __('Expand') : __('Collapse')" :isCollapsed="isSidebarCollapsed"
        @click="isSidebarCollapsed = !isSidebarCollapsed" class="">
        <template #icon>
          <span class="grid h-4 w-4 flex-shrink-0 place-items-center">
            <CollapseSidebar class="h-4 w-4 text-ink-gray-7 duration-300 ease-in-out"
              :class="{ '[transform:rotateY(180deg)]': isSidebarCollapsed }" />
          </span>
        </template>
      </SidebarLink>
    </div>
    <Notifications />
    <IntermediateStepModal v-model="showIntermediateModal" :currentStep="currentStep" />
  </div>
</template>

<script setup>
import Section from '@/components/Section.vue'
import Email2Icon from '@/components/Icons/Email2Icon.vue'
import PinIcon from '@/components/Icons/PinIcon.vue'
import UserDropdown from '@/components/UserDropdown.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import DealsIcon from '@/components/Icons/DealsIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import PhoneIcon from '@/components/Icons/PhoneIcon.vue'
import CollapseSidebar from '@/components/Icons/CollapseSidebar.vue'
import NotificationsIcon from '@/components/Icons/NotificationsIcon.vue'
import ExternalLinkIcon from '@/components/Icons/ExternalLinkIcon.vue'
import ReplyIcon from '@/components/Icons/ReplyIcon.vue'
import SidebarLink from '@/components/SidebarLink.vue'
import Notifications from '@/components/Notifications.vue'
import { viewsStore } from '@/stores/views'
import {
  unreadNotificationsCount,
  notificationsStore,
} from '@/stores/notifications'
import { usersStore } from '@/stores/users'
import { sessionStore } from '@/stores/session'
import { FeatherIcon } from 'frappe-ui'
import {
  SignupBanner,
  TrialBanner,
  IntermediateStepModal,
} from 'frappe-ui/frappe'
import { capture } from '@/telemetry'
import { useStorage } from '@vueuse/core'
import { ref, computed, h, onMounted, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'

const { getPinnedViews, getPublicViews } = viewsStore()
const { toggle: toggleNotificationPanel } = notificationsStore()
const route = useRoute()

const isSidebarCollapsed = useStorage('isSidebarCollapsed', false)
// State để track menu nào đang expanded
const expandedMenus = reactive({})

const isFCSite = ref(window.is_fc_site)
const isDemoSite = ref(window.is_demo_site)

// Function để toggle submenu
const toggleSubmenu = (menuLabel) => {
  expandedMenus[menuLabel] = !expandedMenus[menuLabel]
}

// Function để check nếu submenu có item active
const hasActiveSubmenuItem = (submenu) => {
  if (!submenu || !submenu.length) return false
  return submenu.some(sublink => route.name === (sublink.to.name || sublink.to))
}

// Auto-expand menu có submenu item active
const autoExpandActiveMenus = () => {
  links.forEach(link => {
    if (link.submenu && hasActiveSubmenuItem(link.submenu)) {
      expandedMenus[link.label] = true
    }
  })
}

// script setup
const hoveredParent = ref(null)
const flyoutTop = ref(0)
const onEnterParent = (label, event) => {
  hoveredParent.value = label
  // Nếu có event (từ menu cha), lấy vị trí top của menu cha
  if (event && event.currentTarget) {
    const rect = event.currentTarget.getBoundingClientRect()
    flyoutTop.value = rect.top
  }
}
const onLeaveParent = () => (hoveredParent.value = null)

// Hàm style cho flyout submenu khi sidebar thu gọn
const flyoutStyle = (label) => {
  return {
    left: '48px',
    top: flyoutTop.value + 'px',
  }
}

const links = [
  {
    label: "Dashboard",
    icon: LeadsIcon,
    to: 'Dashboard',
  },
  {
    label: "Talent Pools",
    icon: DealsIcon,
    to: 'TalentSegments',
  },
  {
    label: "Campaigns",
    icon: OrganizationsIcon,
    to: 'CampaignManagement',
  },
  {
    label: "Job Opening",
    icon: OrganizationsIcon,
    to: 'JobOpeningManagement',
  },
  // {
  //   label: "Candidate",
  //   icon: OrganizationsIcon,
  //   to: 'CandidateManagementSimple',
  // },
  {
      label: "My Tasks",
      icon: TaskIcon,
      to: { name: 'MyActions' },
  },
  // {
  //   label: "Candidate Pools",
  //   icon: TaskIcon,
  //   to: 'CandidatePoolManagement',
  // },
  // {
  //   label: "Candidate",
  //   icon: ContactsIcon,
  //   to: 'CandidateManagement',
  // },
  // {
  //   label: "Report",
  //   icon: NoteIcon,
  //   to: 'Report',
  // },




  // {
  //   label: "Data Sources",
  //   icon: PinIcon,
  //   to: 'CandidateDataSourceManagement',
  //   submenu: [
  //     {
  //       label: "Universal Pattern",
  //       to: 'CandidateDataSourceManagement'
  //     },
  //     {
  //       label: "Direct Pattern",
  //       to: 'CandidateDataSourceManagementDirect'
  //     },
  //   ]
  // },


  {
    label: "Report",
    icon: NoteIcon,
    to: 'Report',
    submenu: [
      {
        label: "Prospect",
        icon: ContactsIcon,
        to: { name: 'CandidateManagement' },
      },
      {
        label: "Talents",
        icon: NoteIcon,
        to: { name: 'Talent' },
      },
      {
        label: "Interactions",
        icon: ReplyIcon,
        to: { name: 'InteractionManagement' },

      },
      {
        label: "Actions",
        icon: PinIcon,
        to: { name: 'ActionManagement' },
      },
      {
        label: "Email Logs",
        icon: Email2Icon,
        to: { name: 'EmailLogManagement' },
      },
    ]
  },
  {
    label: "Settings",
    icon: TaskIcon,
    to: 'Settings',
    submenu: [
      // {
      //   label: "integrations",
      //   icon: ExternalLinkIcon,
      //   to: { name: 'CandidateDataSourceManagementDirect' }
      // },
      {
        label: "Campaign Templates",
        icon: NoteIcon,
        to: { name: 'CampaignTemplateManagement' }
      },
      {
        label: "Connectors",
        icon: ExternalLinkIcon,
        to: { name: 'Connectors' }
        // to: 'Connectors'
      },
      // {
      //   label: "Email Templates",
      //   icon: Email2Icon,
      //   to: { name: 'EmailEditor' }
      // },
      {
        label: "Ladi Pages",
        icon: NoteIcon,
        to: 'ladi-pages',
      },

    ]
  },

]

const allViews = computed(() => {
  let _views = [
    {
      name: 'All Views',
      hideLabel: true,
      opened: true,
      views: links,
    },
  ]
  if (getPublicViews().length) {
    _views.push({
      name: 'Public views',
      opened: true,
      views: parseView(getPublicViews()),
    })
  }

  if (getPinnedViews().length) {
    _views.push({
      name: 'Pinned views',
      opened: true,
      views: parseView(getPinnedViews()),
    })
  }
  return _views
})

function parseView(views) {
  return views.map((view) => {
    return {
      label: view.label,
      icon: getIcon(view.route_name, view.icon),
      to: {
        name: view.route_name,
        params: { viewType: view.type || 'list' },
        query: { view: view.name },
      },
    }
  })
}

function getIcon(routeName, icon) {
  if (icon) return h('div', { class: 'size-auto' }, icon)

  switch (routeName) {
    case 'Leads':
      return LeadsIcon
    case 'Deals':
      return DealsIcon
    case 'Contacts':
      return ContactsIcon
    case 'Organizations':
      return OrganizationsIcon
    case 'Notes':
      return NoteIcon
    case 'Call Logs':
      return PhoneIcon
    default:
      return PinIcon
  }
}

// onboarding
const { user } = sessionStore()
const { users, isManager } = usersStore()

const showIntermediateModal = ref(false)
const currentStep = ref({})

onMounted(async () => {
  await users.promise
  // Auto-expand menus có submenu item active
  autoExpandActiveMenus()
})

watch(isSidebarCollapsed, (v) => {
  if (v) {
    Object.keys(expandedMenus).forEach(k => expandedMenus[k] = false)
  } else {
    hoveredParent.value = null
  }
})

// Watch route changes để auto-expand menus
watch(() => route.name, () => {
  autoExpandActiveMenus()
}, { immediate: true })
</script>

<style scoped>
/* CSS cho smooth animation */
.group:hover .group-hover\:block {
  display: block;
}

/* Custom transition cho submenu */
.submenu-enter-active,
.submenu-leave-active {
  transition: all 0.3s ease;
}

.submenu-enter-from,
.submenu-leave-to {
  max-height: 0;
  opacity: 0;
}

.submenu-enter-to,
.submenu-leave-from {
  max-height: 200px;
  opacity: 1;
}

/* Submenu item styling - không override active state */
.submenu-item {
  font-size: 0.875rem;
  /* text-sm */
}

/* Override default colors cho submenu khi KHÔNG active */
.submenu-item:not(.bg-gray-100) {
  color: #4b5563;
  /* text-gray-600 */
}

.submenu-item:not(.bg-gray-100):hover {
  background-color: #f9fafb;
  /* bg-gray-50 */
  color: #1f2937;
  /* text-gray-800 */
}

/* Đảm bảo active submenu item có styling đúng */
.submenu-item.bg-gray-100 {
  background-color: #f3f4f6;
  /* bg-gray-100 */
  color: #111827;
  /* text-gray-900 */
  font-weight: 600;
  /* font-semibold */
}

/* Border indicator cho parent menu có submenu active */
.border-l-3 {
  border-left-width: 3px;
}

/* Hover state cho parent menu */
.parent-menu-item:hover {
  background-color: #f9fafb;
  /* bg-gray-50 */
}

.parent-menu-item.has-active-submenu {
  background-color: #f3f4f6;
  /* bg-gray-100 */
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity .15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity .15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
