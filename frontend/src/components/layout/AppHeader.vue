<script setup>
import { ref } from 'vue'
import { sessionStore as session } from '@/stores/session'
const loading = ref(false)
defineEmits(['toggle-drawer'])


async function handleLogout() {
  loading.value = true
  try {
    await session().logout.submit()
  } catch (e) {
    error.value = e.message || 'Logout failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-app-bar flat app color="primary" dark>
    <!-- Nút toggle sidebar -->
    <v-app-bar-nav-icon @click="$emit('toggle-drawer')" />

    <!-- Tiêu đề app -->
    <!-- <v-toolbar-title class="text-h6 font-weight-medium">MBW Mira</v-toolbar-title> -->

    <v-spacer />

    <!-- Nút chuông thông báo -->
    <v-btn icon>
      <v-icon>mdi-bell</v-icon>
    </v-btn>

    <!-- Menu user/avatar -->
    <v-menu offset-y>
      <template #activator="{ props }">
        <v-btn icon v-bind="props">
          <v-avatar size="32">
            <img src="https://i.pravatar.cc/150?img=3" alt="User" />
          </v-avatar>
        </v-btn>
      </template>

      <v-list>
        <v-list-item @click="handleLogout" :loading="loading">
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>
