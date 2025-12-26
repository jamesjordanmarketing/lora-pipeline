# Section E02: Dataset Management - Testing Guide

**Date:** December 26, 2025  
**Section:** E02 - Dataset Upload, Validation & Management

---

## 🧪 Complete Testing Workflow

### Prerequisites

1. **Environment Setup**
   ```bash
   # Ensure .env.local has required variables
   NEXT_PUBLIC_SUPABASE_URL=your-project-url
   SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   ```

2. **Database Verification**
   ```bash
   # Verify datasets table exists
   cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"
   node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentIntrospectSchema({table:'datasets',transport:'pg'});console.log('Datasets table:',r.success?'✅':'❌');})();"
   
   # Verify notifications table exists
   node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentIntrospectSchema({table:'notifications',transport:'pg'});console.log('Notifications table:',r.success?'✅':'❌');})();"
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

---

## Test 1: API - Create Dataset & Get Upload URL

### Step 1: Create Dataset
```bash
# Note: Replace YOUR_AUTH_TOKEN with actual auth token from browser cookies
curl -X POST http://localhost:3000/api/datasets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -d '{
    "name": "Test Customer Support Dataset",
    "description": "Sample conversations for testing",
    "file_name": "sample-dataset.jsonl",
    "file_size": 2048
  }'
```

### Expected Response:
```json
{
  "success": true,
  "data": {
    "dataset": {
      "id": "uuid-here",
      "user_id": "user-uuid",
      "name": "Test Customer Support Dataset",
      "status": "uploading",
      ...
    },
    "uploadUrl": "https://...supabase.co/storage/v1/object/upload/...",
    "storagePath": "user-id/dataset-id/sample-dataset.jsonl"
  }
}
```

### Step 2: Upload File to Presigned URL
```bash
# Save the uploadUrl from previous response
UPLOAD_URL="<paste-upload-url-here>"

# Upload the sample dataset
curl -X PUT "$UPLOAD_URL" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@scripts/test-data/sample-dataset.jsonl"
```

### Expected Response:
```
200 OK (empty body)
```

### Step 3: Confirm Upload
```bash
# Save dataset ID from step 1
DATASET_ID="<paste-dataset-id-here>"

curl -X POST http://localhost:3000/api/datasets/$DATASET_ID/confirm \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"
```

### Expected Response:
```json
{
  "success": true,
  "data": {
    "dataset": {
      "id": "...",
      "status": "validating",
      ...
    }
  }
}
```

---

## Test 2: Database - Verify Dataset Created

### Using SAOL:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

# Query datasets
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,status,file_name',orderBy:[{column:'created_at',asc:false}],limit:5});console.log('Recent datasets:');r.data.forEach(d=>console.log('-',d.name,'|',d.status,'|',d.file_name));})();"
```

### Expected Output:
```
Recent datasets:
- Test Customer Support Dataset | validating | sample-dataset.jsonl
```

---

## Test 3: Edge Function - Validation

### Step 1: Deploy Edge Function
```bash
cd c:/Users/james/Master/BrightHub/BRun/lora-pipeline

# Deploy function
supabase functions deploy validate-datasets
```

### Step 2: Manual Invocation (Testing)
```bash
# Invoke function manually
supabase functions invoke validate-datasets --no-verify-jwt
```

### Expected Response:
```json
{
  "success": true,
  "processed": 1,
  "message": "Processed 1 dataset(s)"
}
```

### Step 3: Check Validation Results
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

# Query dataset after validation
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,status,training_ready,total_training_pairs,total_tokens',where:[{column:'status',operator:'eq',value:'ready'}],limit:5});console.log('Ready datasets:');r.data.forEach(d=>console.log('-',d.name,'|',d.total_training_pairs,'pairs |',d.total_tokens,'tokens'));})();"
```

### Expected Output:
```
Ready datasets:
- Test Customer Support Dataset | 14 pairs | 182 tokens
```

### Step 4: Check Notification Created
```bash
# Query notifications
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'notifications',select:'type,title,message,created_at',where:[{column:'type',operator:'eq',value:'dataset_ready'}],orderBy:[{column:'created_at',asc:false}],limit:3});console.log('Recent notifications:');r.data.forEach(n=>console.log('-',n.title,'|',n.message));})();"
```

### Expected Output:
```
Recent notifications:
- Dataset Ready | Your dataset "Test Customer Support Dataset" is ready for training
```

---

## Test 4: Edge Function - Invalid Dataset

### Step 1: Upload Invalid Dataset
```bash
# Create dataset
curl -X POST http://localhost:3000/api/datasets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN" \
  -d '{
    "name": "Invalid Test Dataset",
    "description": "Dataset with validation errors",
    "file_name": "invalid-dataset.jsonl",
    "file_size": 256
  }'

# Upload invalid file
curl -X PUT "<upload-url-from-response>" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@scripts/test-data/invalid-dataset.jsonl"

# Confirm upload
curl -X POST http://localhost:3000/api/datasets/<dataset-id>/confirm \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"
```

### Step 2: Run Validation
```bash
# Invoke Edge Function
supabase functions invoke validate-datasets --no-verify-jwt
```

### Step 3: Check Error Status
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

# Query error datasets
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,status,error_message,validation_errors',where:[{column:'status',operator:'eq',value:'error'}],limit:5});console.log('Error datasets:');r.data.forEach(d=>{console.log('-',d.name,'|',d.error_message);if(d.validation_errors){console.log('  Errors:',JSON.stringify(d.validation_errors,null,2));}});})();"
```

### Expected Output:
```
Error datasets:
- Invalid Test Dataset | Found 5 validation error(s)
  Errors: [
    { "line": 2, "error": "Empty turns array", "suggestion": "..." },
    { "line": 3, "error": "Invalid structure", "suggestion": "..." },
    ...
  ]
```

---

## Test 5: UI - Datasets Page

### Step 1: Navigate to Datasets Page
1. Open browser: `http://localhost:3000/datasets`
2. Login if required

### Expected Behavior:
- ✅ Page loads without errors
- ✅ Datasets grid displays
- ✅ Search input visible
- ✅ Status filter dropdown visible
- ✅ Upload button visible
- ✅ Stats summary shows (Total, Ready, Validating, Errors)

### Step 2: Test Search
1. Type "Customer" in search box
2. Verify datasets filtered by name

### Step 3: Test Status Filter
1. Select "Ready" from status dropdown
2. Verify only ready datasets shown

### Step 4: Test Empty State
1. Clear filters
2. If no datasets, verify empty state displays with helpful message

### Step 5: Test Dataset Card
1. Verify each card shows:
   - ✅ Dataset name
   - ✅ File name
   - ✅ Status badge (colored)
   - ✅ Statistics (if ready)
   - ✅ Action buttons (View Details, Start Training, or Delete)

### Step 6: Test Delete
1. Find a dataset with status "error"
2. Click Delete button
3. Confirm deletion
4. Verify dataset removed from list

---

## Test 6: API - List Datasets

### Test Pagination
```bash
# List first page
curl http://localhost:3000/api/datasets?page=1&limit=10 \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"
```

### Test Filtering
```bash
# Filter by status
curl "http://localhost:3000/api/datasets?status=ready" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"

# Search by name
curl "http://localhost:3000/api/datasets?search=customer" \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"
```

### Expected Response Structure:
```json
{
  "success": true,
  "data": {
    "datasets": [...],
    "total": 5,
    "page": 1,
    "limit": 25,
    "totalPages": 1
  }
}
```

---

## Test 7: API - Get Single Dataset

```bash
curl http://localhost:3000/api/datasets/<dataset-id> \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"
```

### Expected Response:
```json
{
  "success": true,
  "data": {
    "dataset": {
      "id": "...",
      "name": "...",
      "status": "ready",
      "training_ready": true,
      "total_training_pairs": 14,
      "total_tokens": 182,
      "sample_data": [...],
      ...
    }
  }
}
```

---

## Test 8: API - Delete Dataset

```bash
curl -X DELETE http://localhost:3000/api/datasets/<dataset-id> \
  -H "Authorization: Bearer YOUR_AUTH_TOKEN"
```

### Expected Response:
```json
{
  "success": true,
  "data": {
    "dataset": {
      "id": "...",
      "deleted_at": "2025-12-26T23:15:00.000Z",
      ...
    }
  }
}
```

### Verify Soft Delete:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

# Query deleted datasets (should not appear in normal queries)
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,deleted_at',where:[{column:'deleted_at',operator:'not.is',value:null}]});console.log('Deleted datasets:',r.data.length);})();"
```

---

## Test 9: Cron Job Setup

### Option 1: Via Supabase Dashboard
1. Navigate to **Database** → **Cron Jobs**
2. Click **Create a new Cron Job**
3. Configure:
   - **Name:** validate-datasets-cron
   - **Schedule:** `* * * * *` (every 1 minute)
   - **Command:** Call Edge Function URL
4. Enable the job

### Option 2: Via SQL
```sql
-- Run in Supabase SQL Editor
SELECT cron.schedule(
  'validate-datasets-cron',
  '* * * * *',
  $$
  SELECT net.http_post(
    url := 'https://YOUR_PROJECT_REF.supabase.co/functions/v1/validate-datasets',
    headers := jsonb_build_object(
      'Authorization', 
      'Bearer ' || current_setting('app.settings.service_role_key')
    )
  ) AS request_id;
  $$
);
```

### Verify Cron Job Running:
```bash
# Wait 1-2 minutes, then check Edge Function logs
supabase functions logs validate-datasets --tail
```

---

## Test 10: Integration Test - Full Flow

### Complete End-to-End Test:

1. **Create Dataset** → Status: `uploading`
2. **Upload File** → File in storage
3. **Confirm Upload** → Status: `validating`
4. **Wait 1 minute** → Cron triggers validation
5. **Check Status** → Status: `ready` (if valid) or `error` (if invalid)
6. **Check Notification** → Notification created
7. **View in UI** → Dataset appears with statistics
8. **Delete Dataset** → Soft deleted

### Automated Test Script:
```bash
#!/bin/bash
# Full integration test

echo "1. Creating dataset..."
RESPONSE=$(curl -s -X POST http://localhost:3000/api/datasets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -d '{"name":"Integration Test","file_name":"test.jsonl","file_size":1024}')

DATASET_ID=$(echo $RESPONSE | jq -r '.data.dataset.id')
UPLOAD_URL=$(echo $RESPONSE | jq -r '.data.uploadUrl')
echo "Dataset ID: $DATASET_ID"

echo "2. Uploading file..."
curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: application/octet-stream" \
  --data-binary "@scripts/test-data/sample-dataset.jsonl"

echo "3. Confirming upload..."
curl -s -X POST http://localhost:3000/api/datasets/$DATASET_ID/confirm \
  -H "Authorization: Bearer $AUTH_TOKEN"

echo "4. Waiting for validation (60 seconds)..."
sleep 60

echo "5. Checking final status..."
curl -s http://localhost:3000/api/datasets/$DATASET_ID \
  -H "Authorization: Bearer $AUTH_TOKEN" | jq '.data.dataset | {status, training_ready, total_training_pairs}'

echo "Test complete!"
```

---

## Troubleshooting

### Dataset Stuck in "validating" Status

**Possible Causes:**
1. Edge Function not deployed
2. Cron job not configured
3. File not uploaded correctly
4. Storage permissions issue

**Solutions:**
```bash
# Check if Edge Function exists
supabase functions list

# Deploy if missing
supabase functions deploy validate-datasets

# Manually trigger validation
supabase functions invoke validate-datasets --no-verify-jwt

# Check logs
supabase functions logs validate-datasets
```

### Upload URL Expired

**Error:** 401 Unauthorized on file upload

**Solution:** 
- Upload URLs expire after 1 hour
- Create a new dataset and upload immediately

### RLS Policy Blocking Access

**Error:** 404 Dataset not found

**Solution:**
```bash
# Verify RLS policies in SAOL
cd supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentIntrospectSchema({table:'datasets',transport:'pg'});console.log('RLS Enabled:',r.tables[0].rlsEnabled);console.log('Policies:',r.tables[0].policies.map(p=>p.name));})();"
```

### Validation Errors Not Showing

**Issue:** validation_errors column is null

**Check:**
```bash
# Query dataset details
cd supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,status,validation_errors',limit:1});console.log(JSON.stringify(r.data[0],null,2));})();"
```

---

## Success Criteria

All tests should pass with:
- ✅ API endpoints return correct responses
- ✅ Database records created/updated correctly
- ✅ Edge Function validates datasets successfully
- ✅ UI displays datasets and handles interactions
- ✅ Cron job runs automatically every minute
- ✅ Notifications created for ready datasets
- ✅ RLS policies enforce user isolation
- ✅ Error handling works for invalid datasets

---

**Testing Complete!** 🎉

All features in Section E02 are now implemented and tested.

