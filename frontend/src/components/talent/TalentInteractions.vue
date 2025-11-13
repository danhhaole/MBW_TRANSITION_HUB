<template>
  <div class="space-y-6">
    <!-- Interaction Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-blue-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100">
            <FeatherIcon name="users" class="w-6 h-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-blue-600">Total Flows</p>
            <p class="text-2xl font-bold text-blue-900">0</p>
          </div>
        </div>
      </div>
      
      <div class="bg-green-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100">
            <FeatherIcon name="send" class="w-6 h-6 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-green-600">Campaigns</p>
            <p class="text-2xl font-bold text-green-900">0</p>
          </div>
        </div>
      </div>
      
      <div class="bg-purple-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100">
            <FeatherIcon name="layers" class="w-6 h-6 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-purple-600">Sequences</p>
            <p class="text-2xl font-bold text-purple-900">0</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Flow Participation -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Flow Participation</h3>
      <div class="space-y-4">
        <!-- <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
            <div>
              <p class="font-medium text-gray-900">Recruitment Flow - Senior Developer</p>
              <p class="text-sm text-gray-500">Started 5 days ago</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <Badge theme="blue" variant="subtle">Active</Badge>
            <span class="text-sm text-gray-500">Step 3/5</span>
          </div>
        </div>

        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <div>
              <p class="font-medium text-gray-900">Onboarding Flow</p>
              <p class="text-sm text-gray-500">Completed 2 weeks ago</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <Badge theme="green" variant="subtle">Completed</Badge>
            <span class="text-sm text-gray-500">5/5</span>
          </div>
        </div>

        <div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center space-x-3">
            <div class="w-3 h-3 bg-orange-500 rounded-full"></div>
            <div>
              <p class="font-medium text-gray-900">Follow-up Sequence</p>
              <p class="text-sm text-gray-500">Paused 1 week ago</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <Badge theme="orange" variant="subtle">Paused</Badge>
            <span class="text-sm text-gray-500">2/4</span>
          </div>
        </div> -->
      </div>
    </div>

    <!-- Campaign History -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Campaign History</h3>
      <div class="space-y-4">
        <!-- <div class="border-l-4 border-blue-500 pl-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900">Email Campaign - Tech Talent Pool</p>
              <p class="text-sm text-gray-500">Sent 3 days ago</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-green-600">Opened</p>
              <p class="text-xs text-gray-500">Click rate: 45%</p>
            </div>
          </div>
        </div>

        <div class="border-l-4 border-green-500 pl-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900">SMS Campaign - Interview Reminder</p>
              <p class="text-sm text-gray-500">Sent 1 week ago</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-blue-600">Replied</p>
              <p class="text-xs text-gray-500">Response time: 2h</p>
            </div>
          </div>
        </div>

        <div class="border-l-4 border-purple-500 pl-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900">WhatsApp Campaign - Job Opportunity</p>
              <p class="text-sm text-gray-500">Sent 2 weeks ago</p>
            </div>
            <div class="text-right">
              <p class="text-sm font-medium text-purple-600">Delivered</p>
              <p class="text-xs text-gray-500">Read: Yes</p>
            </div>
          </div>
        </div> -->
      </div>
    </div>

    <!-- Interaction Timeline -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Interaction Timeline</h3>
      <div class="relative">
        <!-- <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
        <div class="space-y-6">
          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-blue-500 rounded-full">
              <FeatherIcon name="mail" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Email sent: Interview invitation</p>
              <p class="text-xs text-gray-500">3 days ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-green-500 rounded-full">
              <FeatherIcon name="phone" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Phone call: Technical screening</p>
              <p class="text-xs text-gray-500">1 week ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-purple-500 rounded-full">
              <FeatherIcon name="message-circle" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">WhatsApp: Job opportunity shared</p>
              <p class="text-xs text-gray-500">2 weeks ago</p>
            </div>
          </div>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon, Badge } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})
</script>
