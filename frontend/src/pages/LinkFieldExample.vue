<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Ví dụ sử dụng LinkField Component</v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-row>




                <!-- Test với LinkFieldCustom - Customer với customer_name -->


                <!-- Test với LinkFieldCustom - Campaign với description -->
                <v-col cols="12" md="6">
                  <LinkFieldCustom
                    v-model="formData.customCampaign"
                    doctype="Campaign"
                    display-field="campaign_name"
                    label="Custom Campaign (với description)"
                    placeholder="Tìm kiếm campaign..."
                    @change="handleCustomCampaignChange"
                  />
                </v-col>

                <!-- Customer Link Field với onCreate -->
               
              </v-row>

              <v-divider class="my-6"></v-divider>

              <v-row>
                <v-col cols="12">
                  <v-btn 
                    type="submit" 
                    color="primary" 
                    :loading="saving"
                    class="mr-4"
                  >
                    Lưu
                  </v-btn>
                  
                  <v-btn 
                    color="secondary" 
                    variant="outlined"
                    @click="resetForm"
                  >
                    Reset
                  </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Hiển thị dữ liệu form -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>Dữ liệu Form</v-card-title>
          <v-card-text>
            <pre>{{ JSON.stringify(formData, null, 2) }}</pre>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Snackbar thông báo -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="3000"
      top
    >
      {{ snackbar.message }}
      <template #actions>
        <v-btn
          variant="text"
          @click="snackbar.show = false"
        >
          Đóng
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import LinkField from '@/components/LinkField.vue'
import SimpleLinkField from '@/components/SimpleLinkField.vue'
import LinkFieldCustom from '@/components/LinkFieldCustom.vue'

const formData = reactive({
  user: '',
  company: '',
  customer: '',
  item: '',
  territory: '',
  project: '',
  testDoc: '',
  simpleTest: '',
  customUser: '',
  customCustomer: '',
  customCampaign: '',
})

const saving = ref(false)
const snackbar = reactive({
  show: false,
  message: '',
  color: 'success'
})

// Filters cho Company
const companyFilters = computed(() => [
  [] // Chỉ lấy company không phải group
])

// Filters cho Item (dynamic filter dựa vào company được chọn)
const itemFilters = computed(() => {
  const filters = [
    ['disabled', '=', 0], // Chỉ lấy item không bị disabled
    ['is_stock_item', '=', 1] // Chỉ lấy stock item
  ]
  
  // Nếu đã chọn company, filter theo company
  if (formData.company) {
    filters.push(['company', '=', formData.company])
  }
  
  return filters
})

// Event handlers
const handleUserChange = (value) => {
  console.log('User changed:', value)
  showSnackbar(`Đã chọn user: ${value}`, 'info')
}

const handleCompanyChange = (value) => {
  console.log('Company changed:', value)
  // Reset item khi company thay đổi
  formData.item = ''
  showSnackbar(`Đã chọn company: ${value}`, 'info')
}

const handleCustomerChange = (value) => {
  console.log('Customer changed:', value)
  showSnackbar(`Đã chọn customer: ${value}`, 'info')
}

const handleItemChange = (value) => {
  console.log('Item changed:', value)
  showSnackbar(`Đã chọn item: ${value}`, 'info')
}

const handleTerritoryChange = (value) => {
  console.log('Territory changed:', value)
  showSnackbar(`Đã chọn territory: ${value}`, 'info')
}

const handleProjectChange = (value) => {
  console.log('Project changed:', value)
  showSnackbar(`Đã chọn project: ${value}`, 'info')
}

const handleTestDocChange = (value) => {
  console.log('Test DocType changed:', value)
  showSnackbar(`Đã chọn doctype: ${value}`, 'info')
}

const handleSimpleTestChange = (value) => {
  console.log('Simple User Field changed:', value)
  showSnackbar(`Đã chọn simple user field: ${value}`, 'info')
}

const handleCustomUserChange = (value) => {
  console.log('Custom User Field changed:', value)
  showSnackbar(`Đã chọn custom user field: ${value}`, 'info')
}

const handleCustomCustomerChange = (value) => {
  console.log('Custom Customer Field changed:', value)
  showSnackbar(`Đã chọn custom customer field: ${value}`, 'info')
}

const handleCustomCampaignChange = (value) => {
  console.log('Custom Campaign Field changed:', value)
  showSnackbar(`Đã chọn custom campaign field: ${value}`, 'info')
}

// Xử lý tạo customer mới
const handleCreateCustomer = async (customerName, closeCallback) => {
  try {
    console.log('Creating new customer:', customerName)
    
    // Giả lập việc tạo customer mới
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Trong thực tế, bạn sẽ gọi API để tạo customer
    // const newCustomer = await call('frappe.client.insert', {
    //   doc: {
    //     doctype: 'Customer',
    //     customer_name: customerName,
    //     customer_type: 'Individual'
    //   }
    // })
    
    showSnackbar(`Đã tạo customer mới: ${customerName}`, 'success')
    formData.customer = customerName
    closeCallback()
  } catch (error) {
    console.error('Error creating customer:', error)
    showSnackbar('Lỗi khi tạo customer mới', 'error')
  }
}

// Xử lý submit form
const handleSubmit = async () => {
  saving.value = true
  
  try {
    // Giả lập việc lưu dữ liệu
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    console.log('Form submitted:', formData)
    showSnackbar('Đã lưu thành công!', 'success')
  } catch (error) {
    console.error('Error saving form:', error)
    showSnackbar('Lỗi khi lưu dữ liệu', 'error')
  } finally {
    saving.value = false
  }
}

// Reset form
const resetForm = () => {
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
  showSnackbar('Đã reset form', 'info')
}

// Hiển thị snackbar
const showSnackbar = (message, color = 'success') => {
  snackbar.message = message
  snackbar.color = color
  snackbar.show = true
}
</script>

<style scoped>
pre {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
}
</style> 