<template>
  <div class="space-y-6">
    <!-- Activities List -->
    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Recent Activities</h3>
      </div>
      <div class="divide-y divide-gray-200">
        <!-- <div v-for="activity in activities" :key="activity.id" class="p-6">
          <div class="flex items-start space-x-4">
            <div class="flex-shrink-0">
              <div 
                class="w-8 h-8 rounded-full flex items-center justify-center"
                :class="getActivityIconClass(activity.type)"
              >
                <FeatherIcon :name="getActivityIcon(activity.type)" class="w-4 h-4" />
              </div>
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ activity.title }}</p>
                  <p class="text-sm text-gray-500">{{ activity.content }}</p>
                </div>
                <div class="text-right">
                  <p class="text-xs text-gray-400">{{ activity.timeAgo }}</p>
                  <p class="text-xs text-gray-500">by {{ activity.owner }}</p>
                </div>
              </div>
            </div>
          </div>
        </div> -->
      </div>
    </div>

    <!-- Activity Timeline -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Activity Timeline</h3>
      <!-- <div class="relative">
        <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
        <div class="space-y-6">
          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-blue-500 rounded-full">
              <FeatherIcon name="user-plus" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Profile created</p>
              <p class="text-xs text-gray-500">Talent profile was created in the system</p>
              <p class="text-xs text-gray-400">1 month ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-green-500 rounded-full">
              <FeatherIcon name="phone" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Initial contact</p>
              <p class="text-xs text-gray-500">First phone call to discuss opportunities</p>
              <p class="text-xs text-gray-400">3 weeks ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-purple-500 rounded-full">
              <FeatherIcon name="file-text" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Resume updated</p>
              <p class="text-xs text-gray-500">Latest resume and portfolio uploaded</p>
              <p class="text-xs text-gray-400">2 weeks ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-orange-500 rounded-full">
              <FeatherIcon name="briefcase" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Job application</p>
              <p class="text-xs text-gray-500">Applied for Senior Developer position</p>
              <p class="text-xs text-gray-400">1 week ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-indigo-500 rounded-full">
              <FeatherIcon name="calendar" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Interview scheduled</p>
              <p class="text-xs text-gray-500">Technical interview scheduled for next week</p>
              <p class="text-xs text-gray-400">3 days ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-teal-500 rounded-full">
              <FeatherIcon name="check-circle" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Status updated</p>
              <p class="text-xs text-gray-500">Candidate status changed to "Under Review"</p>
              <p class="text-xs text-gray-400">1 day ago</p>
            </div>
          </div>
        </div>
      </div> -->
    </div>

    <!-- Activity Stats -->
    <!-- <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Activity Statistics</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center p-4 bg-blue-50 rounded-lg">
          <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="file-text" class="w-4 h-4 text-blue-600" />
          </div>
          <p class="text-sm font-medium text-blue-900">Profile Updates</p>
          <p class="text-2xl font-bold text-blue-600">{{ getActivityCount('note') }}</p>
        </div>
        
        <div class="text-center p-4 bg-green-50 rounded-lg">
          <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="phone" class="w-4 h-4 text-green-600" />
          </div>
          <p class="text-sm font-medium text-green-900">Phone Calls</p>
          <p class="text-2xl font-bold text-green-600">{{ getActivityCount('call') }}</p>
        </div>
        
        <div class="text-center p-4 bg-purple-50 rounded-lg">
          <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="mail" class="w-4 h-4 text-purple-600" />
          </div>
          <p class="text-sm font-medium text-purple-900">Emails</p>
          <p class="text-2xl font-bold text-purple-600">{{ getActivityCount('email') }}</p>
        </div>
        
        <div class="text-center p-4 bg-orange-50 rounded-lg">
          <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-2">
            <FeatherIcon name="calendar" class="w-4 h-4 text-orange-600" />
          </div>
          <p class="text-sm font-medium text-orange-900">Meetings</p>
          <p class="text-2xl font-bold text-orange-600">{{ getActivityCount('meeting') }}</p>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})

// Mock activities data
const activities = ref([
  {
    id: 1,
    type: 'note',
    title: 'Profile updated',
    content: 'Updated skills and experience information',
    owner: 'System',
    timeAgo: '2 hours ago',
    creation: new Date()
  },
  {
    id: 2,
    type: 'call',
    title: 'Phone screening',
    content: 'Completed initial phone screening with HR team',
    owner: 'Jane Smith',
    timeAgo: '1 day ago',
    creation: new Date()
  },
  {
    id: 3,
    type: 'email',
    title: 'Email communication',
    content: 'Sent follow-up email regarding job opportunity',
    owner: 'Mike Johnson',
    timeAgo: '3 days ago',
    creation: new Date()
  },
  {
    id: 4,
    type: 'meeting',
    title: 'Interview scheduled',
    content: 'Technical interview scheduled for next week',
    owner: 'Sarah Wilson',
    timeAgo: '5 days ago',
    creation: new Date()
  }
])

const getActivityIcon = (type) => {
  const icons = {
    note: 'file-text',
    call: 'phone',
    email: 'mail',
    meeting: 'calendar'
  }
  return icons[type] || 'activity'
}

const getActivityIconClass = (type) => {
  const classes = {
    note: 'bg-blue-100 text-blue-600',
    call: 'bg-green-100 text-green-600',
    email: 'bg-purple-100 text-purple-600',
    meeting: 'bg-orange-100 text-orange-600'
  }
  return classes[type] || 'bg-gray-100 text-gray-600'
}

const getActivityCount = (type) => {
  return activities.value.filter(activity => activity.type === type).length
}
</script>
