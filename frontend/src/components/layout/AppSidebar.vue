<script setup>
import SidebarBrand from './SidebarBrand.vue'

defineProps({ mini: Boolean })

const menuItems = [
  // {
  //   id: 'product-introduction',
  //   title: 'Product Introduction',
  //   icon: 'mdi-information',
  //   to: '/product-introduction'
  // },
  {
    id: 'dashboard',
    title: 'Dashboard',
    icon: 'mdi-view-dashboard',
    to: '/dashboard'
  },
  {
    id: 'campaign',
    title: 'Campaign Management',
    icon: 'mdi-bullhorn',
    children: [
      { 
        id: 'campaigns', 
        title: 'Campaigns', 
        to: '/campaigns',
        icon: 'mdi-target'
      },
      { 
        id: 'campaign-steps', 
        title: 'Campaign Steps', 
        to: '/campaign-steps',
        icon: 'mdi-chart-timeline-variant'
      }
    ]
  },
  {
    id: 'talent-management',
    title: 'Talent Management',
    icon: 'mdi-account-group',
    children: [
      { 
        id: 'talent-segments', 
        title: 'Talent Segments', 
        to: '/talent-segments',
        icon: 'mdi-account-group'
      },
      { 
        id: 'candidates', 
        title: 'Candidates', 
        to: '/candidates',
        icon: 'mdi-account'
      },
      // { 
      //   id: 'candidate-segments', 
      //   title: 'Candidate Segments', 
      //   to: '/candidate-segments',
      //   icon: 'mdi-account-network'
      // }
    ]
  },
  {
    id: 'campaign-execution',
    title: 'Campaign Execution',
    icon: 'mdi-play-circle',
    children: [
      // { 
      //   id: 'candidate-campaigns', 
      //   title: 'Candidate Campaigns', 
      //   to: '/candidate-campaigns',
      //   icon: 'mdi-account-arrow-right'
      // },
      { 
        id: 'actions', 
        title: 'Actions', 
        to: '/actions',
        icon: 'mdi-lightning-bolt'
      },
      { 
        id: 'interactions', 
        title: 'Interactions', 
        to: '/interactions',
        icon: 'mdi-chat'
      }
    ]
  },
  {
    id: 'communications',
    title: 'Communications',
    icon: 'mdi-email',
    children: [
      { 
        id: 'email-logs', 
        title: 'Email Logs', 
        to: '/email-logs',
        icon: 'mdi-email-outline'
      }
    ]
  },
  {
    id: 'user',
    title: 'User',
    icon: 'mdi-account',
    children: [
      { id: 'profile', title: 'Profile', to: '/profile', icon: 'mdi-account-circle' },
      { id: 'settings', title: 'Settings', to: '/user-settings', icon: 'mdi-cog' }
    ]
  }
]
</script>

<template>
  <div class="sidebar-wrapper">
    <!-- Logo / Avatar -->
    <SidebarBrand :mini="mini" title="MBW Mira" />

    <!-- Menu -->
    <v-list nav dense class="pa-0">
      <!-- Mục không có submenu -->
      <v-list-item
        v-for="item in menuItems.filter(i => !i.children)"
        :key="item.id"
        :to="item.to"
        link
        :prepend-icon="item.icon"
        class="sidebar-item"
      >
        <v-list-item-title v-if="!mini">{{ item.title }}</v-list-item-title>
      </v-list-item>

      <!-- Mục có submenu -->
      <v-list-group
        v-for="item in menuItems.filter(i => i.children)"
        :key="item.id"
        :prepend-icon="item.icon"
        class="sidebar-item"
      >
        <template #activator="{ props }">
          <v-list-item v-bind="props">
            <v-list-item-title v-if="!mini">{{ item.title }}</v-list-item-title>
          </v-list-item>
        </template>

        <!-- Submenu -->
        <v-list-item
          v-for="child in item.children"
          :key="child.id"
          :to="child.to"
          link
          :prepend-icon="child.icon || 'mdi-chevron-right'"
          class="pl-8"
        >
          <v-list-item-title v-if="!mini">{{ child.title }}</v-list-item-title>
        </v-list-item>
      </v-list-group>
    </v-list>
  </div>
</template>

<style scoped>
.sidebar-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #ffffff;
  overflow-y: auto;
}

.sidebar-item {
  min-height: 44px;
  transition: all 0.2s ease;
}

.v-list-item-title {
  white-space: nowrap;
}
</style>
