<template>
  <div class="p-6 bg-gray-50 rounded-lg">
    <h3 class="text-lg font-semibold mb-4">API Debugger</h3>
    
    <div class="space-y-4">
      <!-- Connection Test -->
      <div>
        <Button 
          @click="testConnection" 
          :loading="testing"
          variant="outline"
          theme="blue"
        >
          Test API Connection
        </Button>
        <div v-if="connectionResult" class="mt-2 text-sm">
          <span :class="connectionResult.success ? 'text-green-600' : 'text-red-600'">
            {{ connectionResult.message }}
          </span>
        </div>
      </div>

      <!-- Create Test Campaign -->
      <div>
        <Button 
          @click="testCreateCampaign" 
          :loading="creating"
          variant="solid"
          theme="green"
        >
          Test Create Campaign
        </Button>
        <div v-if="createResult" class="mt-2 text-sm">
          <span :class="createResult.success ? 'text-green-600' : 'text-red-600'">
            {{ createResult.message }}
          </span>
        </div>
      </div>

      <!-- Raw API Test -->
      <div>
        <Button 
          @click="testRawApi" 
          :loading="rawTesting"
          variant="outline"
          theme="gray"
        >
          Test Raw API Call
        </Button>
        <div v-if="rawResult" class="mt-2 text-sm">
          <span :class="rawResult.success ? 'text-green-600' : 'text-red-600'">
            {{ rawResult.message }}
          </span>
        </div>
      </div>
    </div>

    <!-- Debug Log -->
    <div v-if="debugLog.length > 0" class="mt-6">
      <h4 class="font-medium mb-2">Debug Log:</h4>
      <div class="bg-black text-green-400 p-4 rounded text-xs font-mono max-h-60 overflow-y-auto">
        <div v-for="(log, index) in debugLog" :key="index" class="mb-1">
          <span class="text-gray-400">[{{ log.timestamp }}]</span>
          <span :class="log.type === 'error' ? 'text-red-400' : 'text-green-400'">
            {{ log.message }}
          </span>
        </div>
      </div>
      <Button @click="clearLog" size="sm" variant="ghost" theme="gray" class="mt-2">
        Clear Log
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Button } from 'frappe-ui'
import { call } from 'frappe-ui'
import { testFrappeConnection, debugApiCall } from '@/utils/debugApi'
import { useCampaignStore } from '@/stores/campaign'

const campaignStore = useCampaignStore()

// State
const testing = ref(false)
const creating = ref(false)
const rawTesting = ref(false)
const connectionResult = ref(null)
const createResult = ref(null)
const rawResult = ref(null)
const debugLog = ref([])

// Helper to add log
const addLog = (message, type = 'info') => {
  debugLog.value.push({
    timestamp: new Date().toLocaleTimeString(),
    message,
    type
  })
}

// Test connection
const testConnection = async () => {
  testing.value = true
  connectionResult.value = null
  
  try {
    addLog('🧪 Starting connection test...')
    const result = await testFrappeConnection()
    
    if (result) {
      connectionResult.value = { success: true, message: '✅ Connection successful' }
      addLog('✅ Connection test passed')
    } else {
      connectionResult.value = { success: false, message: '❌ Connection failed' }
      addLog('❌ Connection test failed', 'error')
    }
  } catch (error) {
    connectionResult.value = { success: false, message: `❌ Error: ${error.message}` }
    addLog(`❌ Connection error: ${error.message}`, 'error')
  } finally {
    testing.value = false
  }
}

// Test create campaign
const testCreateCampaign = async () => {
  creating.value = true
  createResult.value = null
  
  try {
    addLog('🚀 Testing campaign creation...')
    
    const testData = {
      campaign_name: `Test Campaign ${Date.now()}`,
      description: 'Test campaign created from debugger',
      type: 'NURTURING',
      status: 'DRAFT'
    }
    
    addLog(`📝 Test data: ${JSON.stringify(testData)}`)
    
    const result = await campaignStore.submitNewCampaign(testData)
    
    if (result && (result.success || result.name)) {
      createResult.value = { success: true, message: '✅ Campaign created successfully' }
      addLog(`✅ Campaign created: ${result.data?.name || result.name}`)
    } else {
      createResult.value = { success: false, message: '❌ Campaign creation failed' }
      addLog('❌ Campaign creation failed', 'error')
    }
  } catch (error) {
    createResult.value = { success: false, message: `❌ Error: ${error.message}` }
    addLog(`❌ Campaign creation error: ${error.message}`, 'error')
  } finally {
    creating.value = false
  }
}

// Test raw API call
const testRawApi = async () => {
  rawTesting.value = true
  rawResult.value = null
  
  try {
    addLog('🔧 Testing raw API call...')
    
    // Test simple get_list first
    const listResult = await debugApiCall('frappe.client.get_list', {
      doctype: 'User',
      limit_page_length: 1
    })
    
    addLog(`📋 Get list result: ${JSON.stringify(listResult)}`)
    
    // Test insert
    const insertResult = await debugApiCall('frappe.client.insert', {
      doc: {
        doctype: 'Mira Campaign',
        campaign_name: `Raw Test ${Date.now()}`,
        description: 'Raw API test',
        type: 'NURTURING',
        status: 'DRAFT'
      }
    })
    
    addLog(`📝 Insert result: ${JSON.stringify(insertResult)}`)
    
    rawResult.value = { success: true, message: '✅ Raw API calls successful' }
  } catch (error) {
    rawResult.value = { success: false, message: `❌ Error: ${error.message}` }
    addLog(`❌ Raw API error: ${error.message}`, 'error')
  } finally {
    rawTesting.value = false
  }
}

// Clear log
const clearLog = () => {
  debugLog.value = []
}
</script>
