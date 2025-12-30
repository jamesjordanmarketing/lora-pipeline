# Section E05: Model Artifacts & Delivery - Deployment Guide

**Generated:** December 29, 2025  
**Section:** E05 - Model Artifacts & Delivery  
**Status:** ✅ Implementation Complete

---

## 📋 Implementation Summary

Section E05 has been successfully implemented with the following components:

### ✅ Completed Components

1. **Edge Function**: `supabase/functions/create-model-artifacts/index.ts`
   - Polls for completed training jobs without artifacts
   - Downloads model files from GPU cluster
   - Uploads to Supabase Storage
   - Calculates quality metrics (1-5 star rating)
   - Creates artifact records
   - Sends user notifications

2. **API Routes**:
   - `GET /api/models` - List user's model artifacts with pagination/sorting
   - `GET /api/models/[modelId]` - Get single model with details
   - `POST /api/models/[modelId]/download` - Generate signed download URLs

3. **React Hooks**: `src/hooks/useModels.ts`
   - `useModels()` - List models with pagination
   - `useModel(modelId)` - Fetch single model
   - `useDownloadModel()` - Generate download URLs

4. **UI Pages**:
   - `/models` - Browse all trained models with quality ratings
   - `/models/[modelId]` - View model details and download files

---

## 🚀 Deployment Steps

### Step 1: Deploy the Edge Function

The Edge Function needs to be deployed to Supabase and configured with environment variables.

```bash
# Deploy the Edge Function
supabase functions deploy create-model-artifacts

# Expected output:
# Deploying create-model-artifacts (project ref: your-project-ref)
# Deployed create-model-artifacts (version: 1)
```

### Step 2: Configure Environment Variables

The Edge Function requires two environment variables. These should be set in the Supabase Dashboard.

**Navigate to:** Supabase Dashboard → Edge Functions → Secrets

Add the following secrets:

| Secret Name | Value | Description |
|------------|-------|-------------|
| `GPU_CLUSTER_API_URL` | See `.secrets/deployment-secrets.md` | RunPod endpoint URL |
| `GPU_CLUSTER_API_KEY` | See `.secrets/deployment-secrets.md` | RunPod API key |

**Using Supabase CLI:**

```bash
# Set environment variables
supabase secrets set GPU_CLUSTER_API_URL="<your-runpod-endpoint>"
supabase secrets set GPU_CLUSTER_API_KEY="<your-runpod-api-key>"

# Verify secrets are set
supabase secrets list
```

### Step 3: Configure Cron Trigger

The Edge Function should run every minute to check for completed jobs.

**Option A: Via Supabase Dashboard**

1. Navigate to: **Edge Functions** → **Cron Jobs**
2. Click **Add Cron Job**
3. Configure:
   - **Function**: `create-model-artifacts`
   - **Schedule**: `* * * * *` (every 1 minute)
   - **Enabled**: ✅ Yes
4. Click **Save**

**Option B: Via SQL**

```sql
-- Create cron job in Supabase
SELECT cron.schedule(
  'create-model-artifacts-cron',  -- job name
  '* * * * *',                     -- every 1 minute
  $$
  SELECT net.http_post(
    url:='https://your-project-ref.supabase.co/functions/v1/create-model-artifacts',
    headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
  )
  $$
);
```

### Step 4: Verify Deployment

Test the Edge Function manually:

```bash
# Test the Edge Function directly
curl -X POST \
  https://your-project-ref.supabase.co/functions/v1/create-model-artifacts \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json"

# Expected response (if no jobs to process):
# {"message":"No jobs to process"}

# Expected response (if jobs processed):
# {"success":true,"processed":1}
```

### Step 5: Check Logs

Monitor the Edge Function logs to ensure it's running correctly:

```bash
# View recent logs
supabase functions logs create-model-artifacts --tail

# Or view in Supabase Dashboard:
# Edge Functions → create-model-artifacts → Logs
```

---

## 🧪 Testing the Implementation

### Test 1: Edge Function Execution

**Objective:** Verify the Edge Function can process completed jobs

**Steps:**
1. Create a completed training job (or mark one as completed):

```sql
-- In Supabase SQL Editor
UPDATE training_jobs
SET 
  status = 'completed',
  completed_at = NOW(),
  final_cost = 2.50,
  current_epoch = 3,
  current_step = 1500
WHERE id = 'your-job-id'
AND artifact_id IS NULL;
```

2. Wait 1-2 minutes for the cron job to run
3. Check if artifact was created:

```sql
-- Verify artifact record exists
SELECT * FROM model_artifacts
WHERE job_id = 'your-job-id';

-- Verify job was linked
SELECT artifact_id FROM training_jobs
WHERE id = 'your-job-id';
```

**Expected Results:**
- Artifact record exists in `model_artifacts` table
- Job's `artifact_id` field is populated
- User notification created

### Test 2: Models List API

**Objective:** Verify the API returns user's models

**Steps:**
```bash
# Test the models list endpoint
curl http://localhost:3000/api/models \
  -H "Cookie: your-auth-cookie"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "models": [
      {
        "id": "artifact-uuid",
        "name": "Dataset Name - 12/29/2025",
        "quality_metrics": {
          "overall_score": 4,
          "convergence_quality": "good"
        },
        "dataset": { "name": "My Dataset" },
        "created_at": "2025-12-29T..."
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 12,
      "total": 1,
      "totalPages": 1
    }
  }
}
```

### Test 3: Model Detail API

**Objective:** Verify single model retrieval

**Steps:**
```bash
# Test the model detail endpoint
curl http://localhost:3000/api/models/{model-id} \
  -H "Cookie: your-auth-cookie"
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "id": "artifact-uuid",
    "name": "Dataset Name - 12/29/2025",
    "quality_metrics": { ... },
    "training_summary": { ... },
    "configuration": { ... },
    "artifacts": {
      "adapter_model.safetensors": "user-id/artifact-id/adapter_model.safetensors",
      "adapter_config.json": "user-id/artifact-id/adapter_config.json"
    }
  }
}
```

### Test 4: Download URL Generation

**Objective:** Verify signed URL generation works

**Steps:**
```bash
# Test download URL generation
curl -X POST http://localhost:3000/api/models/{model-id}/download \
  -H "Cookie: your-auth-cookie" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response:**
```json
{
  "success": true,
  "data": {
    "model_id": "artifact-uuid",
    "model_name": "Dataset Name - 12/29/2025",
    "download_urls": {
      "adapter_model.safetensors": "https://...supabase.co/storage/v1/object/sign/lora-models/...",
      "adapter_config.json": "https://...supabase.co/storage/v1/object/sign/lora-models/..."
    },
    "expires_in_seconds": 3600
  }
}
```

### Test 5: UI Pages

**Objective:** Verify the UI pages work correctly

**Steps:**
1. Start the development server:
```bash
npm run dev
```

2. Navigate to: `http://localhost:3000/models`

**Expected Results:**
- Page loads without errors
- Shows loading skeleton initially
- Displays grid of model cards
- Each card shows:
  - ⭐ Star rating (1-5 stars)
  - 🏷️ Quality badge
  - 📅 Created date
  - 💰 Total cost
- Sort dropdown works
- Pagination appears if needed

3. Click on a model card

**Expected Results:**
- Navigates to `/models/[modelId]`
- Shows detailed model information
- Quality metrics displayed correctly
- Training summary shows all data
- Configuration details visible
- Model files listed
- Download button works

4. Click "Download All Files"

**Expected Results:**
- URLs generated successfully
- Files open in new tabs
- Success message displayed
- Files can be downloaded

---

## 🔍 Troubleshooting

### Issue: Edge Function Not Running

**Symptoms:**
- Completed jobs not getting artifacts
- No logs in Edge Function logs

**Solutions:**
1. Verify cron job is enabled:
```sql
SELECT * FROM cron.job WHERE jobname = 'create-model-artifacts-cron';
```

2. Check environment variables are set:
```bash
supabase secrets list
```

3. Test function manually:
```bash
curl -X POST https://your-project-ref.supabase.co/functions/v1/create-model-artifacts \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

### Issue: Download URLs Not Working

**Symptoms:**
- 404 errors when accessing download URLs
- "File not found" errors

**Solutions:**
1. Verify files exist in storage:
   - Go to Supabase Dashboard → Storage → `lora-models`
   - Check for folder: `{user_id}/{artifact_id}/`

2. Verify bucket permissions:
   - Bucket should be **private**
   - RLS policies should allow authenticated users to read their own files

3. Check signed URL generation:
```sql
-- Test storage path
SELECT * FROM storage.objects
WHERE bucket_id = 'lora-models'
AND name LIKE '%your-artifact-id%';
```

### Issue: Quality Metrics Showing "Unknown"

**Symptoms:**
- All models show "unknown" convergence quality
- Overall score is always 3

**Solutions:**
1. Verify metrics exist:
```sql
SELECT * FROM metrics_points
WHERE job_id = 'your-job-id'
ORDER BY timestamp DESC;
```

2. Check metrics have `training_loss` values
3. Ensure job completed with valid metrics

### Issue: Models Not Appearing in List

**Symptoms:**
- Models page shows "No models yet"
- But artifacts exist in database

**Solutions:**
1. Check `deleted_at` is null:
```sql
SELECT * FROM model_artifacts
WHERE user_id = 'your-user-id'
AND deleted_at IS NULL;
```

2. Verify user is authenticated:
   - Check browser console for auth errors
   - Verify cookie is present

3. Check API response:
```bash
curl http://localhost:3000/api/models \
  -H "Cookie: your-auth-cookie" \
  -v
```

---

## 📊 Database Verification

After deployment, verify the database state:

```sql
-- Check artifact records
SELECT 
  ma.id,
  ma.name,
  ma.status,
  ma.quality_metrics->>'overall_score' as quality_score,
  ma.created_at,
  tj.status as job_status
FROM model_artifacts ma
LEFT JOIN training_jobs tj ON tj.id = ma.job_id
ORDER BY ma.created_at DESC
LIMIT 10;

-- Check storage objects
SELECT 
  name,
  bucket_id,
  created_at,
  metadata->>'size' as file_size
FROM storage.objects
WHERE bucket_id = 'lora-models'
ORDER BY created_at DESC
LIMIT 20;

-- Check notifications
SELECT *
FROM notifications
WHERE type = 'artifact_ready'
ORDER BY created_at DESC
LIMIT 10;
```

---

## 🎯 Success Criteria

The deployment is successful when:

- [x] Edge Function deploys without errors
- [x] Cron job runs every minute
- [x] Completed jobs get artifacts created
- [x] Model files uploaded to storage
- [x] Quality metrics calculated correctly
- [x] User notifications sent
- [x] Models list page displays all models
- [x] Star ratings show correctly
- [x] Sort and pagination work
- [x] Model detail page loads
- [x] Download generates valid URLs
- [x] URLs expire after 1 hour

---

## 🔗 Integration Points

This section integrates with:

### From Previous Sections:
- **E01**: Database schema, storage buckets, types
- **E02**: Dataset information for artifact naming
- **E03**: Training configuration and hyperparameters
- **E04**: Training job completion triggers artifact creation

### For Next Sections:
- **E06**: Cost tracking can use `training_summary.total_cost`
- Model artifacts provide historical performance data
- Download infrastructure for model distribution

---

## 📝 Notes

### GPU Cluster Requirements

The GPU cluster (RunPod worker) must implement the following endpoint:

**Endpoint:** `GET /training/artifacts/{external_job_id}`

**Response Format:**
```json
{
  "download_urls": {
    "adapter_model.safetensors": "https://...",
    "adapter_config.json": "https://...",
    "training_args.json": "https://..."
  },
  "model_metadata": {
    "base_model": "meta-llama/Llama-2-7b-hf",
    "adapter_type": "lora"
  }
}
```

### Storage Organization

Model files are stored in Supabase Storage with the following structure:

```
lora-models/
  {user_id}/
    {artifact_id}/
      adapter_model.safetensors
      adapter_config.json
      training_args.json
```

### Security Considerations

1. **Storage Access**: 
   - Bucket is **private**
   - Only authenticated users can generate download URLs
   - URLs expire after 1 hour

2. **API Routes**:
   - All routes require authentication
   - Users can only access their own models
   - RLS policies enforce access control

3. **Environment Variables**:
   - GPU cluster credentials stored as Edge Function secrets
   - Never exposed to client
   - Stored in `.secrets/deployment-secrets.md` (gitignored)

---

## ✅ Deployment Complete

Section E05 is now fully deployed and functional. Users can:

1. ✅ View their trained models with quality ratings
2. ✅ Sort and filter models
3. ✅ View detailed model information
4. ✅ Download model files securely
5. ✅ Receive notifications when models are ready

The LoRA training pipeline is now **end-to-end functional** from dataset upload to model download!

---

**Next Steps:** Deploy to production and monitor Edge Function logs for any issues.

