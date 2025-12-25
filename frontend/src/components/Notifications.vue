<template>
  <div
    v-if="visible"
    ref="target"
    class="absolute z-20 h-screen bg-surface-white transition-all duration-300 ease-in-out"
    :style="{
      'box-shadow': '8px 0px 8px rgba(0, 0, 0, 0.1)',
      'max-width': '350px',
      'min-width': '350px',
      left: 'calc(100% + 1px)',
    }"
  >
    <div class="flex h-screen flex-col text-ink-gray-9">
      <div
        class="z-20 flex items-center justify-between border-b bg-surface-white px-5 py-2.5"
      >
        <div class="text-base font-medium">{{ __('Notifications') }}</div>
        <div class="flex gap-1">
          <Tooltip :text="__('Mark all as read')">
            <div>
              <Button variant="ghost" @click="() => markAllAsRead()">
                <template #icon>
                  <MarkAsDoneIcon class="h-4 w-4" />
                </template>
              </Button>
            </div>
          </Tooltip>
          <Tooltip :text="__('Close')">
            <div>
              <Button variant="ghost" @click="() => toggle()">
                <template #icon>
                  <FeatherIcon name="x" class="h-4 w-4" />
                </template>
              </Button>
            </div>
          </Tooltip>
        </div>
      </div>
      <div
        v-if="notifications?.length"
        class="divide-y divide-outline-gray-modals overflow-auto text-base"
      >
        <RouterLink
          v-for="log in notifications"
          :key="log.name"
          :to="getRoute(log)"
          class="flex cursor-pointer items-start gap-2.5 px-4 py-2.5 hover:bg-surface-gray-2"
          @click="markAsRead(log.name)"
        >
          <div class="mt-1 flex items-center gap-2.5 flex-shrink-0">
            <div
              class="size-[5px] rounded-full"
              :class="[log.read ? 'bg-transparent' : 'bg-surface-gray-7']"
            />
            <WhatsAppIcon v-if="log.type == 'WhatsApp'" class="size-7" />
            <Avatar 
              v-else 
              :image="log.user_image" 
              :label="log.full_name" 
              class="mr-2" 
            />
          </div>
          <div class="flex-1">
            <div v-if="log.subject" class="notification text-ink-gray-7 mb-1" v-html="log.subject" />
            <div v-else class="mb-2 space-x-1 leading-5 text-ink-gray-5">
              <span class="font-medium text-ink-gray-9">
                {{ log.full_name }}
              </span>
              <span v-if="log.document_type">
                {{ __('mentioned you in {0}', [log.document_type]) }}
              </span>
              <span class="font-medium text-ink-gray-9" v-if="log.document_name">
                {{ log.document_name }}
              </span>
            </div>
            <div class="text-sm text-ink-gray-5">
              {{ __(timeAgo(log.creation)) }}
            </div>
          </div>
        </RouterLink>
      </div>
      <div
        v-else
        class="flex flex-1 flex-col items-center justify-center gap-2"
      >
        <NotificationsIcon class="h-20 w-20 text-ink-gray-2" />
        <div class="text-lg font-medium text-ink-gray-4">
          {{ __('No new notifications') }}
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import WhatsAppIcon from '@/components/Icons/WhatsAppIcon.vue'
import MarkAsDoneIcon from '@/components/Icons/MarkAsDoneIcon.vue'
import NotificationsIcon from '@/components/Icons/NotificationsIcon.vue'
import {
  visible,
  unReadNotifications,
  notificationsStore,
} from '@/stores/notifications'
import { globalStore } from '@/stores/global'
import { timeAgo } from '@/utils'
import { onClickOutside } from '@vueuse/core'
import { capture } from '@/telemetry'
import { Tooltip, Avatar } from 'frappe-ui'
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'

const { $socket } = globalStore()
const { mark_as_read, mark_all_as_read, toggle, mark_doc_as_read } = notificationsStore()

// Use unReadNotifications data
const notifications = computed(() => unReadNotifications.data || [])

const target = ref(null)
onClickOutside(
  target,
  () => {
    if (visible.value) toggle()
  },
  {
    ignore: ['#notifications-btn'],
  },
)

function markAsRead(name) {
  capture('notification_mark_as_read')
  mark_as_read.submit({ name: name })
}

function markAllAsRead() {
  capture('notification_mark_all_as_read')
  mark_all_as_read.submit()
}

onBeforeUnmount(() => {
  // $socket.off('mira_notification')
})

onMounted(() => {
  // $socket.on('mira_notification', () => {
  //   notifications.reload()
  // })
})

function getRoute(notification) {
  // Nếu có link từ notification, sử dụng trực tiếp (giống mbw_ats)
  if (notification.link) {
    // Link từ Notification Log có thể là string path hoặc đã được format
    // Nếu là string, parse nó để convert sang route object
    if (typeof notification.link === 'string') {
      try {
        // Parse link: /campaigns/{id}#comments
        const linkMatch = notification.link.match(/\/campaigns?\/([^#]+)(#.*)?/)
        if (linkMatch) {
          const campaignId = linkMatch[1]
          const hash = linkMatch[2] || ''
          return {
            name: 'CampaignDetailView',
            params: { id: campaignId },
            hash: hash,
          }
        }
        
        // Parse các link khác nếu có format tương tự
        const contactsMatch = notification.link.match(/\/contacts\/([^#]+)(#.*)?/)
        if (contactsMatch) {
          const contactId = contactsMatch[1]
          const hash = contactsMatch[2] || ''
          return {
            name: 'CandidateDetailView',
            params: { id: contactId },
            hash: hash,
          }
        }
        
        // Nếu không match pattern nào, có thể là absolute path
        // Return link string để router xử lý
        return notification.link
      } catch (e) {
        console.error('Error parsing notification link:', e)
        return notification.link
      }
    } else {
      // Nếu link đã là route object, return trực tiếp
      return notification.link
    }
  }
  
  // Fallback: sử dụng document_type và document_name để tạo route
  if (notification.document_type && notification.document_name) {
    const doctype = notification.document_type
    const docname = notification.document_name
    
    if (doctype === 'Mira Campaign') {
      return {
        name: 'CampaignDetailView',
        params: { id: docname },
        hash: '#comments',
      }
    }
    
    // Có thể thêm các doctype khác ở đây
  }

  // Default fallback
  return { name: 'Dashboard' }
}
</script>
<style scoped>
.notification strong {
  font-weight: 400;
}
.notification b {
  font-weight: 400;
}
</style>
