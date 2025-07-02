<template>
    <v-app>
        <v-navigation-drawer v-model="app.drawer" :mini-variant="app.sidebarMini" :permanent="!app.isMobile"
            :temporary="app.isMobile" expand-on-hover app color="white"
            @update:mini-variant="val => app.sidebarMini = val">
            <AppSidebar :mini="app.sidebarMini" />
        </v-navigation-drawer>

        <AppHeader @toggle-drawer="toggleMini" />

        <v-main>
            <v-container fluid>
                <slot />
            </v-container>
        </v-main>
    </v-app>
</template>


<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import { useAppStore } from '@/stores/app'
// import AppFooter from '@/components/layout/AppFooter.vue'

const app = useAppStore()
// Tự động cập nhật trạng thái mobile
const checkMobile = () => {
    app.setMobile(window.innerWidth < 768)
}

onMounted(() => {
    checkMobile()
    window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
    window.removeEventListener('resize', checkMobile)
})

const toggleMini = () => {
    app.toggleSidebar()
}
</script>