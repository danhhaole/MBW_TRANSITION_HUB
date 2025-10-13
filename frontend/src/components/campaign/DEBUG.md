# Campaign Wizard - Debug Guide

## 🐛 Lỗi hiện tại

**Error**: `Cannot read properties of undefined (reading 'exc_type')`

**Nguyên nhân**: Lỗi này xảy ra khi gọi API `frappe.client.insert` nhưng response không đúng format hoặc có lỗi network/authentication.

## 🔧 Các giải pháp đã implement

### 1. Enhanced Error Handling
- ✅ Added detailed error logging trong `campaign.js`
- ✅ Added try-catch blocks với specific error messages
- ✅ Added response validation

### 2. Debug Utilities
- ✅ Created `debugApi.js` với detailed logging
- ✅ Added `debugApiCall` function để track API calls
- ✅ Added `testFrappeConnection` để test connection

### 3. API Debugger Component
- ✅ Created `ApiDebugger.vue` để test API calls
- ✅ Test connection, create campaign, raw API calls
- ✅ Real-time debug log với timestamps

### 4. Alternative API Methods
- ✅ Added `testApiConnection()` method
- ✅ Added `createCampaignViaCustomAPI()` fallback method
- ✅ Updated CampaignWizard để try multiple approaches

### 5. Improved CampaignWizard
- ✅ Test connection trước khi create campaign
- ✅ Try custom API first, fallback to standard method
- ✅ Better error messages và user feedback

## 🧪 Cách debug

### Bước 1: Sử dụng ApiDebugger
```vue
<CampaignWizardDemo />
```

1. Click "Test API Connection" - kiểm tra connection
2. Click "Test Create Campaign" - test tạo campaign
3. Click "Test Raw API Call" - test raw API calls
4. Xem debug log để identify root cause

### Bước 2: Check Console Logs
Mở browser console và xem:
- 🚀 API call data
- ✅ Response details  
- ❌ Error details với full stack trace
- 🔍 Response type và keys

### Bước 3: Check Network Tab
1. Mở DevTools > Network
2. Filter by XHR/Fetch
3. Xem request/response details
4. Check status codes và response body

## 🔍 Common Issues & Solutions

### Issue 1: Authentication Error
**Symptoms**: 401/403 errors, "Not logged in"
**Solution**: Check login status, refresh session

### Issue 2: CORS Error  
**Symptoms**: CORS policy errors
**Solution**: Check server CORS settings

### Issue 3: Invalid Doctype
**Symptoms**: "DocType not found"
**Solution**: Check if `Mira Campaign` doctype exists

### Issue 4: Missing Fields
**Symptoms**: "Mandatory field missing"
**Solution**: Check required fields trong doctype definition

### Issue 5: Network Error
**Symptoms**: "Network request failed"
**Solution**: Check server status, network connection

## 📋 Debug Checklist

- [ ] API connection test passes
- [ ] User is logged in
- [ ] `Mira Campaign` doctype exists
- [ ] Required fields are provided
- [ ] Server is running
- [ ] Network connection is stable
- [ ] CORS is configured correctly
- [ ] No JavaScript errors trong console

## 🚀 Next Steps

1. **Run ApiDebugger** để identify exact issue
2. **Check server logs** for backend errors
3. **Verify doctype** definition và permissions
4. **Test with minimal data** để isolate issue
5. **Use alternative API methods** nếu standard method fails

## 📞 Support

Nếu vẫn gặp lỗi sau khi debug:
1. Share full console logs
2. Share network request/response details
3. Share server error logs (nếu có)
4. Describe exact steps to reproduce
