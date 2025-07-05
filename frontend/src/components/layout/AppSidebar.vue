<script setup>
import SidebarBrand from './SidebarBrand.vue'

defineProps({ mini: Boolean })

const menuItems = [
  {
    id: 'product-introduction',
    title: 'Product Introduction',
    icon: 'mdi-information',
    to: '/product-introduction'
  },
  {
    id: 'dashboard',
    title: 'Dashboard',
    icon: 'mdi-view-dashboard',
    to: '/dashboard'
  },
  {
    id: 'campaign',
    title: 'Campaign',
    icon: 'mdi-target',
    to: '/campaigns'
  },
  {
    id: 'talentsegments',
    title: 'Talent Segments',
    icon: 'mdi-account-group',
    to: '/talent-segments'
  },
  {
    id: 'candidates',
    title: 'Candidates',
    icon: 'mdi-account',
    to: '/candidates'
  },
  {
    id: 'user',
    title: 'User',
    icon: 'mdi-account',
    children: [
      { id: 'profile', title: 'Profile', to: '/profile' },
      { id: 'settings', title: 'Settings', to: '/user-settings' }
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
          prepend-icon="mdi-chevron-right"
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
