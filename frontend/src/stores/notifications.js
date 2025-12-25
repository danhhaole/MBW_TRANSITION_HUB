import { defineStore } from 'pinia'
import { createResource, createListResource } from 'frappe-ui'
import { computed, ref } from 'vue'

export const visible = ref(false)

// Use createListResource for unread notifications (similar to mbw_ats)
export const unReadNotifications = createListResource({
  doctype: 'Notification Log',
  url: 'mbw_mira.api.notifications.get_notifications',
  filters: {
    read: 0,
  },
  auto: true,
  cache: 'Unread Notifications',
})

// Use createListResource for read notifications
export const readNotifications = createListResource({
  doctype: 'Notification Log',
  url: 'mbw_mira.api.notifications.get_notifications',
  filters: {
    read: 1,
  },
  auto: true,
  cache: 'Read Notifications',
})

// Computed for unread count
export const unreadNotificationsCount = computed(
  () => unReadNotifications.data?.length || 0,
)

// Legacy notifications resource for backward compatibility
export const notifications = computed(() => unReadNotifications)

export const notificationsStore = defineStore('mira-notifications', () => {
  const mark_as_read = createResource({
    url: 'mbw_mira.api.notifications.mark_as_read',
    makeParams(values) {
      return {
        name: values.name,
      }
    },
    onSuccess(data) {
      unReadNotifications.reload()
      readNotifications.reload()
    },
  })

  const mark_all_as_read = createResource({
    url: 'mbw_mira.api.notifications.mark_all_as_read',
    onSuccess(data) {
      unReadNotifications.reload()
      readNotifications.reload()
    },
  })

  function toggle() {
    visible.value = !visible.value
  }

  function mark_doc_as_read(doc) {
    if (typeof doc === 'string') {
      // If doc is a name, use mark_as_read
      mark_as_read.submit({ name: doc })
    } else {
      // Legacy support
      mark_as_read.params = { doc: doc }
      mark_as_read.reload()
    }
  }

  return {
    unreadNotificationsCount,
    mark_as_read,
    mark_all_as_read,
    mark_doc_as_read,
    toggle,
  }
})
