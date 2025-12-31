# LoRA Pipeline Deployment - Remaining Tasks

**Date:** 2025-12-30  
**Time:** 21:30 PST  
**Status:** Partial deployment complete, remaining tasks identified

---

## ✅ Completed Automated Checks

### 1. Database Tables ✅ VERIFIED
All 6 LoRA training tables exist and are accessible:
- ✅ `datasets` - 1 record exists
- ✅ `training_jobs` - Table exists
- ✅ `metrics_points` - Table exists
- ✅ `model_artifacts` - Table exists
- ✅ `cost_records` - Table exists
- ✅ `notifications` - Table exists

**Verification Method:** SAOL queries executed successfully

### 2. Storage Buckets ✅ VERIFIED
Both required storage buckets exist:
- ✅ `lora-datasets` - Exists (private bucket)
- ✅ `lora-models` - Exists (private bucket)

**Verification Method:** Supabase Storage API

### 3. Edge Functions ✅ DEPLOYED
All 3 Edge Functions are deployed and responding:
- ✅ `validate-datasets` - HTTP 202 (Accepted)
- ✅ `process-training-jobs` - HTTP 200 (OK)
- ✅ `create-model-artifacts` - HTTP 200 (OK)

**Verification Method:** HTTP POST requests to function endpoints

### 4. Supabase CLI ✅ LINKED
- ✅ Supabase CLI linked to project `hqhtbxlgzysfbekexwku`
- ✅ Migrations visible via `npx supabase migration list`

### 5. Integration Verification ✅ PASSED
- ✅ Script `verify-lora-integration.ts` runs successfully
- ✅ All system checks passing
- ✅ Environment variables loaded correctly

---

## ⚠️ Remaining Manual Tasks

### Priority 1: Critical Deployment Tasks

#### 1.1 Storage Bucket RLS Policies ⚠️ MANUAL REQUIRED
**Status:** Buckets exist but RLS policies need verification/creation

**Action Required:** Navigate to Supabase Dashboard and apply these policies:

**For `lora-datasets` bucket:**
```sql
-- Users can upload to their own folder
CREATE POLICY "Users can upload own datasets"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'lora-datasets' AND
  (storage.foldername(name))[1] = auth.uid()::text
);

-- Users can read their own files
CREATE POLICY "Users can read own datasets"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'lora-datasets' AND
  (storage.foldername(name))[1] = auth.uid()::text
);

-- Users can delete their own files
CREATE POLICY "Users can delete own datasets"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'lora-datasets' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

**For `lora-models` bucket:**
```sql
-- Users can access their own model files
CREATE POLICY "Users can read own models"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'lora-models' AND
  (storage.foldername(name))[1] = auth.uid()::text
);

-- Service role can write model files
CREATE POLICY "Service can write model files"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'lora-models' AND
  auth.role() = 'service_role'
);
```

**How to Apply:**
1. Navigate to: **Supabase Dashboard → Storage → Policies**
2. Select each bucket
3. Click **New Policy**
4. Paste SQL above for each policy
5. Save

**Verification:**
Run integration script again: `npx tsx scripts/verify-lora-integration.ts`

---

#### 1.2 Edge Function Environment Variables ⚠️ MANUAL REQUIRED
**Status:** Functions deployed but secrets need verification

**Action Required:** Verify/set secrets in Supabase Dashboard

**Navigate to:** Supabase Dashboard → Edge Functions → Settings

**Required Secrets:**
| Key | Value | Source |
|-----|-------|--------|
| `GPU_CLUSTER_API_KEY` | `rpa_550JTL8271ULHL73VGU6ED4ZWBU5HB2KNAPMTW38cu8d8v` | `.secrets/deployment-secrets.md` line 16 |
| `GPU_CLUSTER_ENDPOINT` | `https://api.runpod.ai/v2/ei82ickpenoqlp` | `.secrets/deployment-secrets.md` line 17 |
| `SUPABASE_URL` | `https://hqhtbxlgzysfbekexwku.supabase.co` | Auto-provided by Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | (from `.env.local`) | Auto-provided by Supabase |

**Alternative Method (CLI):**
```bash
cd C:\Users\james\Master\BrightHub\BRun\lora-pipeline
npx supabase secrets set GPU_CLUSTER_API_KEY=rpa_550JTL8271ULHL73VGU6ED4ZWBU5HB2KNAPMTW38cu8d8v
npx supabase secrets set GPU_CLUSTER_ENDPOINT=https://api.runpod.ai/v2/ei82ickpenoqlp
```

**Verification:**
```bash
npx supabase secrets list
```

---

#### 1.3 Vercel Environment Variables ⚠️ MANUAL REQUIRED
**Status:** Not yet configured

**Action Required:** Add environment variables to Vercel project

**Navigate to:** Vercel Dashboard → [Your Project] → Settings → Environment Variables

**Required Variables:**
| Key | Value | Environments |
|-----|-------|--------------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://hqhtbxlgzysfbekexwku.supabase.co` | Production, Preview, Development |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | (from `.env.local`) | Production, Preview, Development |
| `SUPABASE_SERVICE_ROLE_KEY` | (from `.env.local`) | Production, Preview, Development |
| `GPU_CLUSTER_API_URL` | `https://api.runpod.ai/v2/ei82ickpenoqlp` | Production |
| `GPU_CLUSTER_API_KEY` | `rpa_550JTL8271ULHL73VGU6ED4ZWBU5HB2KNAPMTW38cu8d8v` | Production |
| `MAX_DATASET_SIZE_MB` | `500` | Production (optional) |
| `MAX_TRAINING_DURATION_HOURS` | `48` | Production (optional) |

**Note:** Get actual keys from `.env.local` file (not shown here for security)

**After Adding:** Redeploy the application for variables to take effect

---

#### 1.4 Cron Job Configuration ⚠️ MANUAL REQUIRED
**Status:** Edge Functions deployed but cron not configured

**Action Required:** Choose ONE of the following options:

**Option A: Using cron-job.org (Recommended for simplicity)**
1. Create free account at https://cron-job.org
2. Create 3 cron jobs:

**validate-datasets:**
- URL: `https://hqhtbxlgzysfbekexwku.supabase.co/functions/v1/validate-datasets`
- Schedule: Every 1 minute
- Method: POST
- Headers: `Authorization: Bearer [SUPABASE_SERVICE_ROLE_KEY]`

**process-training-jobs:**
- URL: `https://hqhtbxlgzysfbekexwku.supabase.co/functions/v1/process-training-jobs`
- Schedule: Every 30 seconds
- Method: POST
- Headers: `Authorization: Bearer [SUPABASE_SERVICE_ROLE_KEY]`

**create-model-artifacts:**
- URL: `https://hqhtbxlgzysfbekexwku.supabase.co/functions/v1/create-model-artifacts`
- Schedule: Every 1 minute
- Method: POST
- Headers: `Authorization: Bearer [SUPABASE_SERVICE_ROLE_KEY]`

**Option B: Using Vercel Cron Jobs**
1. Create API routes in your Next.js app that trigger Edge Functions
2. Configure `vercel.json` with cron schedules
3. Redeploy to Vercel

**Option C: Using Supabase pg_cron**
- Navigate to: Database → Cron Jobs
- If pg_cron extension is available, create scheduled jobs
- If not available, use Option A or B

---

### Priority 2: Deployment Verification Tasks

#### 2.1 Database Verification ⚠️ MANUAL RECOMMENDED
**Action Required:** Run these SQL queries in Supabase SQL Editor

**Check RLS Policies:**
```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN ('datasets', 'training_jobs', 'model_artifacts');
```
**Expected:** All tables should have `rowsecurity = true`

**Check Indexes:**
```sql
SELECT indexname, tablename 
FROM pg_indexes 
WHERE schemaname = 'public'
  AND tablename IN ('datasets', 'training_jobs', 'model_artifacts')
ORDER BY tablename, indexname;
```
**Expected indexes:**
- `idx_datasets_user_id`
- `idx_datasets_status`
- `idx_datasets_created_at`
- `idx_training_jobs_user_id`
- `idx_training_jobs_status`
- `idx_model_artifacts_user_id`

---

#### 2.2 Frontend Deployment ⚠️ MANUAL REQUIRED
**Status:** Not yet deployed to production

**Action Required:**

**Step 1: Build locally to verify no errors**
```bash
cd C:\Users\james\Master\BrightHub\BRun\lora-pipeline
npm run build
```

**Step 2: Deploy to Vercel**

**If using Vercel CLI:**
```bash
vercel --prod
```

**If using GitHub integration:**
1. Commit and push to main branch
2. Vercel will auto-deploy

**Step 3: Verify deployment**
- [ ] Site loads at your domain
- [ ] Login/authentication works
- [ ] Navigate to `/datasets`, `/training`, `/models` pages
- [ ] No console errors in browser DevTools

---

### Priority 3: Post-Deployment Testing

#### 3.1 Test Critical User Flows
**Action Required:** Manually test these workflows

**Dataset Upload Flow:**
1. Login as test user
2. Navigate to `/datasets/new`
3. Upload a sample JSONL file
4. Wait 1-2 minutes
5. Verify status changes to 'ready'
6. Check notification received

**Training Job Flow:**
1. Navigate to `/training/configure?datasetId=[id]`
2. Select preset (e.g., "balanced")
3. Verify cost estimate displays
4. Submit training job
5. Navigate to `/training/jobs/[jobId]`
6. Verify job status updates

**Model Download Flow:**
1. Navigate to `/models`
2. Select a model
3. Click download
4. Verify download starts

---

## 📊 Deployment Progress Summary

| Category | Status | Progress |
|----------|--------|----------|
| Database Tables | ✅ Complete | 6/6 tables |
| Storage Buckets | ⚠️ Partial | 2/2 buckets exist, RLS policies need verification |
| Edge Functions | ✅ Deployed | 3/3 functions deployed |
| Edge Function Secrets | ⚠️ Unknown | Need verification |
| Cron Scheduling | ❌ Not Done | Needs configuration |
| Vercel Env Variables | ❌ Not Done | Needs configuration |
| Frontend Deployment | ❌ Not Done | Needs deployment |
| Post-Deploy Testing | ❌ Not Done | Needs testing |

**Overall Progress:** ~40% Complete

---

## 🚀 Recommended Next Steps (In Order)

1. **Set Edge Function secrets** (Priority 1.2) - 5 minutes
2. **Configure Storage bucket RLS policies** (Priority 1.1) - 10 minutes
3. **Add Vercel environment variables** (Priority 1.3) - 5 minutes
4. **Set up cron jobs** (Priority 1.4) - 15 minutes using cron-job.org
5. **Build and deploy frontend** (Priority 2.2) - 10 minutes
6. **Verify database indexes** (Priority 2.1) - 5 minutes
7. **Test critical user flows** (Priority 3.1) - 30 minutes

**Total Estimated Time:** ~1.5 hours

---

## 🛠️ Automation Status

**What Was Automated:**
- ✅ Supabase CLI linking
- ✅ Database table verification (6 tables)
- ✅ Storage bucket existence check (2 buckets)
- ✅ Edge Function deployment check (3 functions)
- ✅ Integration verification script

**What Requires Manual Action:**
- ⚠️ Storage bucket RLS policies (Supabase Dashboard or SQL)
- ⚠️ Edge Function environment variable configuration (Supabase Dashboard or CLI)
- ⚠️ Vercel environment variable configuration (Vercel Dashboard)
- ⚠️ Cron job scheduling (External service or Vercel)
- ⚠️ Frontend build and deployment (Vercel CLI or GitHub push)
- ⚠️ Post-deployment testing (Manual browser testing)

---

## 📁 Reference Files

**Deployment Secrets:**
- `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\.secrets\deployment-secrets.md`

**Deployment Checklist:**
- `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\docs\LORA_DEPLOYMENT_CHECKLIST.md`

**Monitoring Setup:**
- `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\docs\LORA_MONITORING_SETUP.md`

**Scripts:**
- Integration verification: `scripts/verify-lora-integration.ts`
- Health check: `scripts/check-lora-health.ts`
- Edge function test: `scripts/test-edge-functions.js`

---

**Last Updated:** 2025-12-30 21:30 PST  
**Next Review:** After completing Priority 1 tasks
