<template>
  <div class="space-y-6">
    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-blue-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100">
            <FeatherIcon name="briefcase" class="w-6 h-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-blue-600">Applications</p>
            <p class="text-2xl font-bold text-blue-900">0</p>
          </div>
        </div>
      </div>
      
      <div class="bg-green-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-green-100">
            <FeatherIcon name="check-circle" class="w-6 h-6 text-green-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-green-600">Interviews</p>
            <p class="text-2xl font-bold text-green-900">0</p>
          </div>
        </div>
      </div>
      
      <div class="bg-purple-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-purple-100">
            <FeatherIcon name="star" class="w-6 h-6 text-purple-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-purple-600">Rating</p>
            <p class="text-2xl font-bold text-purple-900">0</p>
          </div>
        </div>
      </div>

      <div class="bg-orange-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100">
            <FeatherIcon name="clock" class="w-6 h-6 text-orange-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-orange-600">Response Time</p>
            <p class="text-2xl font-bold text-orange-900">0</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Chart -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Performance Overview</h3>
      <div class="h-64 flex items-center justify-center bg-gray-50 rounded-lg">
        <div class="text-center">
          <FeatherIcon name="bar-chart-2" class="w-12 h-12 text-gray-400 mx-auto mb-2" />
          <p class="text-gray-500">Performance chart will be implemented here</p>
        </div>
      </div>
    </div>

    <!-- Recent Activity Summary -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
      <!-- <div class="space-y-4">
        <div class="flex items-center space-x-4">
          <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">Applied to Senior Developer position</p>
            <p class="text-xs text-gray-500">2 hours ago</p>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="w-2 h-2 bg-green-500 rounded-full"></div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">Completed technical interview</p>
            <p class="text-xs text-gray-500">1 day ago</p>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
          <div class="flex-1">
            <p class="text-sm text-gray-900">Profile updated</p>
            <p class="text-xs text-gray-500">3 days ago</p>
          </div>
        </div>
      </div> -->
    </div>

    <!-- Skills Assessment -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Skills Assessment</h3>
      <div class="space-y-4">
        <!-- <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="text-gray-700">JavaScript</span>
            <span class="text-gray-500">90%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-blue-600 h-2 rounded-full" style="width: 90%"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="text-gray-700">Vue.js</span>
            <span class="text-gray-500">85%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-green-600 h-2 rounded-full" style="width: 85%"></div>
          </div>
        </div>
        <div>
          <div class="flex justify-between text-sm mb-1">
            <span class="text-gray-700">Python</span>
            <span class="text-gray-500">75%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div class="bg-purple-600 h-2 rounded-full" style="width: 75%"></div>
          </div>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})
</script>
