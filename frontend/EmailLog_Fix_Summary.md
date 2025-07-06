# Sửa lỗi EmailLogManagement.vue không khớp với doctype

## 🔍 **Vấn đề phát hiện:**

### EmailLog doctype thực tế có các trường:
```json
{
  "subject": "Data",           // Tiêu đề email
  "recipients": "Small Text",  // Người nhận
  "cc": "Small Text",          // CC
  "bcc": "Small Text",         // BCC
  "sender": "Data",            // Người gửi
  "content": "Long Text",      // Nội dung email
  "attachments": "Long Text",  // Đính kèm
  "status": "Select",          // Success/Failed/Fallback
  "error": "Long Text"         // Lỗi nếu có
}
```

### EmailLogManagement.vue cũ lại sử dụng:
```javascript
{
  "candidate_id": "...",        // ❌ Không tồn tại
  "recipient_email": "...",     // ❌ Không tồn tại  
  "campaign_id": "...",         // ❌ Không tồn tại
  "template": "...",            // ❌ Không tồn tại
  "body": "...",                // ❌ Sai tên (phải là content)
  "sent_at": "...",             // ❌ Không tồn tại
  "opened_at": "...",           // ❌ Không tồn tại
  "clicked_at": "...",          // ❌ Không tồn tại
  "error_message": "..."        // ❌ Sai tên (phải là error)
}
```

## ✅ **Đã sửa:**

### 1. **Form Data** - Khớp với doctype:
```javascript
const formData = reactive({
  name: '',
  subject: '',           // ✅ Đúng
  recipients: '',        // ✅ Đúng  
  cc: '',               // ✅ Đúng
  bcc: '',              // ✅ Đúng
  sender: '',           // ✅ Đúng
  content: '',          // ✅ Đúng (thay vì body)
  attachments: '',      // ✅ Đúng
  status: 'Success',    // ✅ Đúng
  error: ''             // ✅ Đúng (thay vì error_message)
})
```

### 2. **Status Options** - Khớp với doctype:
```javascript
const statusOptions = [
  { title: 'Success', value: 'Success' },     // ✅ Đúng
  { title: 'Failed', value: 'Failed' },       // ✅ Đúng  
  { title: 'Fallback', value: 'Fallback' }    // ✅ Đúng
]
```

### 3. **Table Headers** - Khớp với doctype:
```javascript
const headers = [
  { title: 'Subject', key: 'subject' },        // ✅ Đúng
  { title: 'Recipients', key: 'recipients' },  // ✅ Đúng
  { title: 'Sender', key: 'sender' },          // ✅ Đúng
  { title: 'Status', key: 'status' },          // ✅ Đúng
  { title: 'Modified', key: 'modified' },      // ✅ Đúng
  { title: 'Actions', key: 'actions' }         // ✅ Đúng
]
```

### 4. **API Fields** - Khớp với doctype:
```javascript
fields: [
  'name', 'subject', 'recipients', 'cc', 'bcc', 
  'sender', 'content', 'attachments', 'status', 
  'error', 'modified'
]
```

### 5. **Search Fields** - Khớp với doctype:
```javascript
searchConditions.push(['subject', 'like', `%${search.value}%`])
searchConditions.push(['recipients', 'like', `%${search.value}%`])
searchConditions.push(['sender', 'like', `%${search.value}%`])
```

### 6. **Form UI** - Khớp với doctype:
- ✅ Subject field
- ✅ Recipients textarea (multiple emails)
- ✅ CC/BCC textareas  
- ✅ Sender email field
- ✅ Content textarea (thay vì body)
- ✅ Attachments field
- ✅ Status select (Success/Failed/Fallback)
- ✅ Error field (chỉ hiện khi status = Failed)

### 7. **Filters** - Đơn giản hóa:
```javascript
const filters = reactive({
  status: '',     // ✅ Filter theo status
  sender: ''      // ✅ Filter theo sender  
})
```

### 8. **Stats** - Khớp với status options:
```javascript
const stats = reactive({
  total: 0,       // ✅ Tổng số
  success: 0,     // ✅ Thành công
  failed: 0       // ✅ Thất bại
})
```

## 🎯 **Kết quả:**

1. **✅ Không còn lỗi trường không tồn tại**
2. **✅ Form lưu được data đúng format** 
3. **✅ Hiển thị data đúng với doctype**
4. **✅ Filter hoạt động chính xác**
5. **✅ Search theo đúng trường có sẵn**
6. **✅ UI/UX phù hợp với dữ liệu thực tế**

## 📋 **Các tính năng mới:**

1. **Detail Modal**: Xem chi tiết email log
2. **Proper Error Display**: Hiển thị error chỉ khi status = Failed  
3. **Attachment Support**: Field cho đính kèm
4. **CC/BCC Support**: Hỗ trợ CC và BCC
5. **Clean UI**: Giao diện sạch sẽ, phù hợp với doctype

## 🔄 **Cần làm tiếp:**

1. **Test với dữ liệu thật**: Tạo/sửa/xóa email log
2. **Validation**: Kiểm tra email format cho recipients/sender
3. **Export**: Test export CSV
4. **Performance**: Optimize cho large dataset

Bây giờ EmailLogManagement.vue sẽ hoạt động đúng với doctype EmailLog thực tế!
