<template>
  <div class="link-field-demo pa-6">
    <h2 class="mb-6">Demo LinkField Component - Unified</h2>
    
    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-card-title>Mode: Simple (Core API)</v-card-title>
          <v-card-text>
            <LinkField
              v-model="selectedUser1"
              doctype="User"
              mode="simple"
              label="Chọn User (Simple)"
              placeholder="Nhập tên user..."
              @change="handleChange('Simple Mode', $event)"
            />
            <div class="mt-2 text-caption">
              Giá trị đã chọn: {{ selectedUser1 }}
            </div>
            <div class="mt-1 text-caption text-grey">
              Sử dụng: frappe.desk.search.search_link
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-card-title>Mode: Auto (Meta Detection)</v-card-title>
          <v-card-text>
            <LinkField
              v-model="selectedUser2"
              doctype="User"
              mode="auto"
              label="Chọn User (Auto)"
              placeholder="Nhập tên user..."
              @change="handleChange('Auto Mode', $event)"
            />
            <div class="mt-2 text-caption">
              Giá trị đã chọn: {{ selectedUser2 }}
            </div>
            <div class="mt-1 text-caption text-grey">
              Sử dụng: frappe.client.get_list + meta
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-card-title>Mode: Custom (Display Field)</v-card-title>
          <v-card-text>
            <LinkField
              v-model="selectedUser3"
              doctype="User"
              mode="custom"
              display-field="full_name"
              search-field="email"
              label="Chọn User (Custom)"
              placeholder="Nhập tên user..."
              @change="handleChange('Custom Mode', $event)"
            />
            <div class="mt-2 text-caption">
              Giá trị đã chọn: {{ selectedUser3 }}
            </div>
            <div class="mt-1 text-caption text-grey">
              Sử dụng: search_link_custom API
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-6">
      <v-col cols="12" md="2">

      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-card-title>Custom Display Field (Campaign)</v-card-title>
          <v-card-text>
            <LinkField
              v-model="selectedCampaign"
              doctype="Campaign"
              
              label="Chọn Campaign"
              placeholder="Nhập tên campaign..."
              @change="handleChange('Campaign Custom', $event)"
            />
            <div class="mt-2 text-caption">
              Giá trị đã chọn: {{ selectedCampaign }}
            </div>
            <div class="mt-1 text-caption text-grey">
              display-field="campaign_name"
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card class="pa-4">
          <v-card-title>With Filters (Candidate)</v-card-title>
          <v-card-text>
            <LinkField
              v-model="selectedCandidate"
              doctype="Candidate"
              display-field="full_name"
              
              label="Chọn Candidate"
              placeholder="Nhập tên candidate..."
              @change="handleChange('Candidate Filtered', $event)"
            />
            <div class="mt-2 text-caption">
              Giá trị đã chọn: {{ selectedCandidate }}
            </div>
            <div class="mt-1 text-caption text-grey">
              filters: [['status', '=', 'Active']]
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-title>Tính năng & Mode Explanation</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="4">
                <div class="feature-box">
                  <h4 class="text-primary mb-2">Simple Mode</h4>
                  <p class="text-body-2 mb-2">
                    <code>mode="simple"</code>
                  </p>
                  <ul class="text-body-2">
                    <li>Sử dụng core API <code>frappe.desk.search.search_link</code></li>
                    <li>Nhanh và đơn giản</li>
                    <li>Tương thích hoàn toàn với core</li>
                    <li>Không cần display-field</li>
                  </ul>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="feature-box">
                  <h4 class="text-primary mb-2">Auto Mode (Default)</h4>
                  <p class="text-body-2 mb-2">
                    <code>mode="auto"</code> hoặc không set
                  </p>
                  <ul class="text-body-2">
                    <li>Tự động detect display field từ meta</li>
                    <li>Sử dụng <code>frappe.client.get_list</code></li>
                    <li>Thông minh, linh hoạt</li>
                    <li>Fallback logic cho description</li>
                  </ul>
                </div>
              </v-col>
              
              <v-col cols="12" md="4">
                <div class="feature-box">
                  <h4 class="text-primary mb-2">Custom Mode</h4>
                  <p class="text-body-2 mb-2">
                    <code>display-field="field_name"</code>
                  </p>
                  <ul class="text-body-2">
                    <li>Chỉ định chính xác display field</li>
                    <li>Sử dụng custom API backend</li>
                    <li>Hỗ trợ search-field tùy chỉnh</li>
                    <li>Kiểm soát hoàn toàn</li>
                  </ul>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <v-row class="mt-6">
      <v-col cols="12">
        <v-card class="pa-4">
          <v-card-title>Log Activity</v-card-title>
          <v-card-text>
            <div class="logs">
              <div v-for="(log, index) in logs" :key="index" class="log-item mb-1">
                <span class="text-primary">{{ log.timestamp }}</span> - 
                <span class="text-secondary">{{ log.component }}</span>: 
                <span class="font-weight-bold">{{ log.value }}</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LinkField from './LinkField.vue'

// Reactive data
const selectedUser1 = ref('')
const selectedUser2 = ref('')
const selectedUser3 = ref('')
const selectedCustomer = ref('')
const selectedCampaign = ref('')
const selectedCandidate = ref('')

const logs = ref([])

// Methods
const handleChange = (component, value) => {
  const timestamp = new Date().toLocaleTimeString()
  logs.value.unshift({
    timestamp,
    component,
    value
  })
  
  // Giữ chỉ 20 logs gần nhất
  if (logs.value.length > 20) {
    logs.value = logs.value.slice(0, 20)
  }
  
  console.log(`${component} changed to:`, value)
}
</script>

<style scoped>
.link-field-demo {
  max-width: 1200px;
  margin: 0 auto;
}

.logs {
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
  font-size: 0.875rem;
}

.log-item {
  padding: 4px 8px;
  border-radius: 4px;
  background-color: rgba(var(--v-theme-surface-variant), 0.1);
}

.feature-box {
  height: 100%;
  padding: 16px;
  border: 1px solid rgba(var(--v-theme-outline), 0.2);
  border-radius: 8px;
  background-color: rgba(var(--v-theme-surface), 0.5);
}

.feature-box h4 {
  margin-bottom: 8px;
}

.feature-box ul {
  margin: 0;
  padding-left: 16px;
}

.feature-box li {
  margin-bottom: 4px;
}

code {
  background-color: rgba(var(--v-theme-primary), 0.1);
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.75rem;
}
</style> 