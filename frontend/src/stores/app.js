// stores/app.js
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', {
  state: () => ({
    sidebarMini: false,
    drawer: true,
    isMobile: false
  }),

  actions: {
    toggleSidebar() {
      this.drawer = !this.drawer
    },
    setMobile(status) {
      this.isMobile = status
    }
  }
})
