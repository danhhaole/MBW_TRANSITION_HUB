<template>
  <div class="space-y-6">
    <!-- Application Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-blue-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-blue-100">
            <FeatherIcon name="file-text" class="w-6 h-6 text-blue-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-blue-600">Total Applications</p>
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
            <p class="text-sm font-medium text-green-600">Accepted</p>
            <p class="text-2xl font-bold text-green-900">0</p>
          </div>
        </div>
      </div>
      
      <div class="bg-orange-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-orange-100">
            <FeatherIcon name="clock" class="w-6 h-6 text-orange-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-orange-600">Pending</p>
            <p class="text-2xl font-bold text-orange-900">0</p>
          </div>
        </div>
      </div>

      <div class="bg-red-50 rounded-lg p-6">
        <div class="flex items-center">
          <div class="p-3 rounded-full bg-red-100">
            <FeatherIcon name="x-circle" class="w-6 h-6 text-red-600" />
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-red-600">Rejected</p>
            <p class="text-2xl font-bold text-red-900">4</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Applications List -->
    <div class="bg-white rounded-lg border border-gray-200">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">Recent Applications</h3>
      </div>
      <div class="divide-y divide-gray-200">
        <!-- <div class="p-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <FeatherIcon name="briefcase" class="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h4 class="text-lg font-medium text-gray-900">Senior Frontend Developer</h4>
                <p class="text-sm text-gray-500">TechCorp Inc. • Remote</p>
                <p class="text-xs text-gray-400">Applied 2 days ago</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <Badge theme="green" variant="subtle">Interview Scheduled</Badge>
              <Button variant="outline" size="sm">
                <div class="flex items-center space-x-2">
                  <FeatherIcon name="eye" class="w-4 h-4 mr-2" />
                  View
                </div>
              </Button>
            </div>
          </div>
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <FeatherIcon name="code" class="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h4 class="text-lg font-medium text-gray-900">Full Stack Developer</h4>
                <p class="text-sm text-gray-500">StartupXYZ • Ho Chi Minh City</p>
                <p class="text-xs text-gray-400">Applied 1 week ago</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <Badge theme="orange" variant="subtle">Under Review</Badge>
              <Button variant="outline" size="sm">
                  <div class="flex items-center space-x-2">
                  <FeatherIcon name="eye" class="w-4 h-4 mr-2" />
                  View
                </div>
              </Button>
            </div>
          </div>
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                <FeatherIcon name="smartphone" class="w-6 h-6 text-green-600" />
              </div>
              <div>
                <h4 class="text-lg font-medium text-gray-900">Mobile App Developer</h4>
                <p class="text-sm text-gray-500">MobileFirst Ltd. • Hanoi</p>
                <p class="text-xs text-gray-400">Applied 2 weeks ago</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <Badge theme="blue" variant="subtle">Offer Extended</Badge>
              <Button variant="outline" size="sm">
                <div class="flex items-center space-x-2">
                  <FeatherIcon name="eye" class="w-4 h-4 mr-2" />
                  View
                </div>
              </Button>
            </div>
          </div>
        </div>

        <div class="p-6">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
                <FeatherIcon name="server" class="w-6 h-6 text-red-600" />
              </div>
              <div>
                <h4 class="text-lg font-medium text-gray-900">Backend Engineer</h4>
                <p class="text-sm text-gray-500">CloudTech Solutions • Da Nang</p>
                <p class="text-xs text-gray-400">Applied 3 weeks ago</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <Badge theme="red" variant="subtle">Not Selected</Badge>
              <Button variant="outline" size="sm">
                <div class="flex items-center space-x-2">
                  <FeatherIcon name="eye" class="w-4 h-4 mr-2" />
                  View
                </div>
              </Button>
            </div>
          </div>
        </div> -->
      </div>
    </div>

    <!-- Application Timeline -->
    <div class="bg-white rounded-lg border border-gray-200 p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Application Timeline</h3>
      <div class="relative">
        <div class="absolute left-4 top-0 bottom-0 w-0.5 bg-gray-200"></div>
        <!-- <div class="space-y-6">
          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-green-500 rounded-full">
              <FeatherIcon name="check" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Application submitted</p>
              <p class="text-xs text-gray-500">Senior Frontend Developer at TechCorp Inc.</p>
              <p class="text-xs text-gray-400">2 days ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-blue-500 rounded-full">
              <FeatherIcon name="eye" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Application reviewed</p>
              <p class="text-xs text-gray-500">HR team reviewed your profile</p>
              <p class="text-xs text-gray-400">1 week ago</p>
            </div>
          </div>

          <div class="relative flex items-start space-x-4">
            <div class="relative z-10 flex items-center justify-center w-8 h-8 bg-purple-500 rounded-full">
              <FeatherIcon name="phone" class="w-4 h-4 text-white" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Phone screening completed</p>
              <p class="text-xs text-gray-500">30-minute call with hiring manager</p>
              <p class="text-xs text-gray-400">2 weeks ago</p>
            </div>
          </div>
        </div> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { FeatherIcon, Badge, Button } from 'frappe-ui'

const props = defineProps({
  talent: {
    type: Object,
    required: true
  }
})
</script>
