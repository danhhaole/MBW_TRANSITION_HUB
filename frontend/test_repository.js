// Test script để kiểm tra universalRepository sau khi sửa

import { emailLogRepository } from './src/repositories/universalRepository.js'

// Test data
const testData = {
  candidate_id: 'TEST001',
  recipients: 'test@example.com',
  subject: 'Test Email',
  body: 'This is a test email',
  status: 'Sent',
  sent_at: new Date().toISOString()
}

// Test create
console.log('Testing create...')
try {
  const result = await emailLogRepository.save(testData)
  console.log('Create result:', result)
  
  if (result.success) {
    console.log('✅ Create successful')
    
    // Test update
    console.log('Testing update...')
    const updatedData = {
      ...testData,
      subject: 'Updated Test Email',
      status: 'Delivered'
    }
    
    const updateResult = await emailLogRepository.save(updatedData, result.data.name)
    console.log('Update result:', updateResult)
    
    if (updateResult.success) {
      console.log('✅ Update successful')
    } else {
      console.log('❌ Update failed:', updateResult.error)
    }
  } else {
    console.log('❌ Create failed:', result.error)
  }
} catch (error) {
  console.log('❌ Error:', error.message)
}

// Test list
console.log('Testing list...')
try {
  const listResult = await emailLogRepository.getList({
    filters: {
      status: 'Sent'
    },
    page_length: 10,
    start: 0
  })
  console.log('List result:', listResult)
  
  if (listResult.success) {
    console.log('✅ List successful, found', listResult.data.length, 'records')
  } else {
    console.log('❌ List failed:', listResult.error)
  }
} catch (error) {
  console.log('❌ Error:', error.message)
}

console.log('Test completed')
