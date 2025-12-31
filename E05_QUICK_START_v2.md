# E05 Quick Start v2 - Web Interface Guide

**Date:** December 29, 2025  
**Focus:** Step-by-step web interface instructions only

---

## Prerequisites

- Supabase account with access to project: `hqhtbxlgzysfbekexwku`
- Browser open to: https://supabase.com/dashboard
- Edge Function code file ready: `supabase/functions/create-model-artifacts/index.ts`

---

## Part 1: Deploy Edge Function via Supabase Dashboard

### Option A: Using Supabase CLI (Recommended)

1. Open **Terminal** or **Command Prompt**
2. Navigate to project:
   ```
   cd C:\Users\james\Master\BrightHub\BRun\lora-pipeline
   ```
3. Login to Supabase:
   ```
   supabase login
   ```
4. Deploy the function:
   ```
   supabase secrets set GPU_CLUSTER_API_URL=https://api.runpod.ai/v2/your-endpoint-id
   supabase functions deploy create-model-artifacts --project-ref hqhtbxlgzysfbekexwku
   ```
5. Wait for: `Deployed function create-model-artifacts`

### Option B: Via Supabase Dashboard (Manual Upload)

**Note:** As of 2024/2025, Supabase primarily requires CLI for Edge Function deployment. Dashboard provides monitoring only.

1. Navigate to: https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku
2. Click: **Edge Functions** (left sidebar)
3. Look for deployment status of `create-model-artifacts`
4. If not deployed, use CLI (Option A above)

---

## Part 2: Set Environment Secrets

### Step 1: Access Edge Function Secrets

1. Go to: https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/settings/functions
2. Click: **Edge Functions** in left sidebar
3. Click: **Secrets** tab at the top
4. You'll see a list of existing secrets

### Step 2: Add GPU_CLUSTER_API_URL

1. Click: **Add New Secret** button
2. In "Secret Name" field, type: `GPU_CLUSTER_API_URL`
3. In "Secret Value" field, paste: `https://api.runpod.ai/v2/ei82ickpenoqlp`
4. Click: **Save** or **Add Secret**

### Step 3: Add GPU_CLUSTER_API_KEY

1. Click: **Add New Secret** button
2. In "Secret Name" field, type: `GPU_CLUSTER_API_KEY`
3. In "Secret Value" field, paste: `rpa_550JTL8271ULHL73VGU6ED4ZWBU5HB2KNAPMTW38cu8d8v`
4. Click: **Save** or **Add Secret**

### Step 4: Verify Secrets

You should see two secrets listed:
- ✅ `GPU_CLUSTER_API_URL`
- ✅ `GPU_CLUSTER_API_KEY`

---

## Part 3: Configure Cron Job

### Step 1: Access Cron Jobs

1. Go to: https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/database/cron-jobs
2. Or navigate: **Database** → **Cron Jobs** (left sidebar)

### Step 2: Create New Cron Job

1. Click: **Create a new Cron Job** button
2. Fill in the form:

**Name:**
```
create-model-artifacts-cron
```

**Schedule:**
```
* * * * *
```
(This means: every 1 minute)

**SQL Command:**
```sql
SELECT
  net.http_post(
    url := 'https://hqhtbxlgzysfbekexwku.supabase.co/functions/v1/create-model-artifacts',
    headers := '{"Content-Type": "application/json", "Authorization": "Bearer ' || current_setting('app.settings.service_role_key') || '"}'::jsonb
  ) as request_id;
```

3. Click: **Create Cron Job**

### Alternative: Using pg_cron Extension

If the above interface is not available:

1. Go to: **SQL Editor** (left sidebar)
2. Click: **New Query**
3. Paste:
```sql
SELECT cron.schedule(
  'create-model-artifacts-cron',
  '* * * * *',
  $$
  SELECT net.http_post(
    url := 'https://hqhtbxlgzysfbekexwku.supabase.co/functions/v1/create-model-artifacts',
    headers := '{"Content-Type": "application/json", "Authorization": "Bearer SERVICE_ROLE_KEY_HERE"}'::jsonb
  );
  $$
);
```
4. Replace `SERVICE_ROLE_KEY_HERE` with your actual service role key from `.env.local`
5. Click: **Run** (or press F5)

---

## Part 4: Verify Deployment

### Step 1: Check Edge Function Logs

1. Go to: https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/functions/create-model-artifacts/logs
2. Or navigate: **Edge Functions** → **create-model-artifacts** → **Logs** tab
3. Look for recent log entries (refreshes every 1 minute)
4. Check for: `[ArtifactCreator] Starting artifact creation cycle`

### Step 2: Test Edge Function Manually

1. Go to: **Edge Functions** → **create-model-artifacts**
2. Click: **Invoke** or **Test** button
3. Leave request body empty: `{}`
4. Click: **Invoke Function**
5. Check response:
   - Success: `{"message":"No jobs to process"}` (if no completed jobs)
   - Success: `{"success":true,"processed":1}` (if jobs processed)

### Step 3: Verify Storage Bucket Exists

1. Go to: https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/storage/buckets
2. Or navigate: **Storage** (left sidebar)
3. Verify bucket exists: **lora-models**
4. If not, click: **New Bucket**
5. Name: `lora-models`
6. Privacy: **Private**
7. File size limit: `5GB`
8. Click: **Create Bucket**

---

## Part 5: Access UI Pages

### Step 1: Start Development Server

1. Open Terminal
2. Navigate to project:
   ```
   cd C:\Users\james\Master\BrightHub\BRun\lora-pipeline
   ```
3. Run:
   ```
   npm run dev
   ```
4. Wait for: `Local: http://localhost:3000`

### Step 2: View Models List Page

1. Open browser
2. Go to: http://localhost:3000/models
3. You should see:
   - Header: "Model Artifacts"
   - Grid of model cards (if any exist)
   - Or: "No models yet" message

### Step 3: View Model Detail Page

1. If models exist, click on any model card
2. Or manually go to: http://localhost:3000/models/{model-id}
3. You should see:
   - Model name and star rating
   - Quality metrics
   - Training summary
   - Download button

---

## Part 6: Test Download Functionality

### Step 1: Create Test Artifact (SQL)

1. Go to: **SQL Editor** in Supabase Dashboard
2. Click: **New Query**
3. Paste:
```sql
-- Insert a test artifact
INSERT INTO model_artifacts (
  id,
  user_id,
  job_id,
  dataset_id,
  name,
  version,
  status,
  quality_metrics,
  training_summary,
  configuration,
  artifacts
) VALUES (
  gen_random_uuid(),
  (SELECT id FROM auth.users LIMIT 1),
  (SELECT id FROM training_jobs WHERE status = 'completed' LIMIT 1),
  (SELECT id FROM datasets LIMIT 1),
  'Test Model - ' || NOW()::date,
  '1.0.0',
  'stored',
  '{"overall_score": 4, "convergence_quality": "good"}'::jsonb,
  '{"total_cost": 2.50, "epochs_completed": 3}'::jsonb,
  '{"hyperparameters": {}, "gpu_config": {}}'::jsonb,
  '{"adapter_model.safetensors": "test/path/model.safetensors"}'::jsonb
);
```
4. Click: **Run**

### Step 2: View Test Model

1. Go to: http://localhost:3000/models
2. You should see the test model card
3. Click on it to view details

### Step 3: Test Download (Will Fail Until Files Uploaded)

1. On model detail page, click: **Download All Files**
2. Expected behavior:
   - If files exist: URLs generated, files download
   - If files don't exist: Error message shown

---

## Part 7: Monitor Artifact Creation

### Watch for Completed Jobs

1. Go to: **Database** → **Table Editor** → **training_jobs**
2. Look for jobs with:
   - `status` = `completed`
   - `artifact_id` = `null`
3. Wait 1-2 minutes
4. Refresh the page
5. Check if `artifact_id` is now populated

### Check Artifact Records

1. Go to: **Table Editor** → **model_artifacts**
2. Look for new records
3. Check fields:
   - `name` - Should have dataset name + date
   - `quality_metrics` - Should have `overall_score`
   - `status` - Should be `stored`
   - `artifacts` - Should have file paths

### Check Notifications

1. Go to: **Table Editor** → **notifications**
2. Look for notifications with:
   - `type` = `artifact_ready`
   - `title` = "Model Ready for Download"

---

## Part 8: Troubleshooting

### Edge Function Not Running

**Check Logs:**
1. **Edge Functions** → **create-model-artifacts** → **Logs**
2. Look for errors or recent executions

**Check Secrets:**
1. **Settings** → **Edge Functions** → **Secrets**
2. Verify both secrets are set

**Re-deploy:**
1. Terminal: `supabase functions deploy create-model-artifacts --project-ref hqhtbxlgzysfbekexwku`

### Cron Job Not Triggering

**Check Cron Jobs:**
1. **Database** → **Cron Jobs**
2. Look for `create-model-artifacts-cron`
3. Check "Last Run" timestamp

**View Cron Job Runs:**
1. **SQL Editor** → **New Query**
2. Run:
```sql
SELECT * FROM cron.job_run_details
WHERE jobname = 'create-model-artifacts-cron'
ORDER BY start_time DESC
LIMIT 10;
```

### No Models Showing in UI

**Check Database:**
1. **Table Editor** → **model_artifacts**
2. Verify records exist
3. Check `deleted_at` is NULL
4. Check `user_id` matches your logged-in user

**Check Browser Console:**
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for API errors

### Download URLs Not Working

**Check Storage Files:**
1. **Storage** → **lora-models** bucket
2. Browse folders: `{user_id}/{artifact_id}/`
3. Verify files exist

**Check Bucket Privacy:**
1. **Storage** → **lora-models**
2. Click bucket settings icon
3. Ensure it's set to **Private**

---

## Quick Reference: URLs

| Service | URL |
|---------|-----|
| Supabase Dashboard | https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku |
| Edge Functions | https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/functions |
| SQL Editor | https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/sql |
| Table Editor | https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/editor |
| Storage | https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/storage/buckets |
| Cron Jobs | https://supabase.com/dashboard/project/hqhtbxlgzysfbekexwku/database/cron-jobs |
| Local App | http://localhost:3000 |
| Models Page | http://localhost:3000/models |

---

## Completion Checklist

After following all steps, verify:

- [ ] Edge Function `create-model-artifacts` is deployed
- [ ] Secrets `GPU_CLUSTER_API_URL` and `GPU_CLUSTER_API_KEY` are set
- [ ] Cron job `create-model-artifacts-cron` is scheduled
- [ ] Cron job shows recent runs in logs
- [ ] Storage bucket `lora-models` exists and is private
- [ ] Local dev server runs on http://localhost:3000
- [ ] Models page loads at http://localhost:3000/models
- [ ] Completed jobs get artifacts created automatically
- [ ] Model cards display with star ratings
- [ ] Download button generates signed URLs

---

**Status:** Ready for use  
**Estimated Setup Time:** 15-20 minutes

