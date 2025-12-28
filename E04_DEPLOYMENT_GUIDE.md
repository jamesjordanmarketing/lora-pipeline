# Section E04: Training Execution & Monitoring - Deployment Guide

**Generated:** December 27, 2025  
**Section:** E04 - Training Execution & Monitoring  
**Status:** ✅ Implementation Complete

---

## 📋 What Was Implemented

This section implements the complete training execution pipeline and real-time monitoring system:

### Components Created

1. **Edge Function: `process-training-jobs`**
   - File: `supabase/functions/process-training-jobs/index.ts`
   - Purpose: Background job processor that polls for queued jobs, submits to GPU cluster, and tracks progress
   - Runs on Cron schedule (every 30 seconds)

2. **API Routes**
   - `GET /api/jobs/[jobId]` - Fetch job details with metrics and cost records
   - `POST /api/jobs/[jobId]/cancel` - Cancel running training jobs

3. **React Hook**
   - `useCancelJob` - Added to `src/hooks/useTrainingConfig.ts`

4. **UI Page**
   - `/training/jobs/[jobId]` - Real-time training monitor with metrics visualization
   - File: `src/app/(dashboard)/training/jobs/[jobId]/page.tsx`

---

## 🚀 Deployment Instructions

### Step 1: Deploy Edge Function

```bash
# Navigate to project root
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline"

# Make sure Supabase CLI is installed
# npm install -g supabase

# Deploy the edge function
supabase functions deploy process-training-jobs
```

**Expected Output:**
```
✓ process-training-jobs deployed successfully
Function URL: https://<project-id>.supabase.co/functions/v1/process-training-jobs
```

### Step 2: Set Environment Variables in Supabase Dashboard

1. Go to: https://supabase.com/dashboard/project/<your-project-id>
2. Navigate to: **Edge Functions** → **Settings** → **Secrets**
3. Add the following environment variables:

```bash
SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
GPU_CLUSTER_API_URL=https://your-gpu-cluster.com
GPU_CLUSTER_API_KEY=<your-gpu-api-key>
```

**Where to find these values:**
- `SUPABASE_URL`: Project Settings → API → Project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Project Settings → API → Service Role Key (⚠️ Keep secret!)
- `GPU_CLUSTER_API_URL`: Your GPU cluster provider's API endpoint
- `GPU_CLUSTER_API_KEY`: Your GPU cluster API authentication key

### Step 3: Configure Cron Schedule

1. In Supabase Dashboard, go to: **Edge Functions** → **Cron Jobs**
2. Click **Create Cron Job**
3. Configure:
   - **Function:** `process-training-jobs`
   - **Schedule:** `*/30 * * * * *` (every 30 seconds)
   - **Enabled:** ✅ Yes

**Cron Schedule Explanation:**
- `*/30 * * * * *` = Every 30 seconds
- This provides near-real-time updates without overwhelming the GPU cluster API

### Step 4: Set Local Environment Variables

Add these to your `.env.local` file for the Next.js app:

```bash
# Already should exist from previous sections
NEXT_PUBLIC_SUPABASE_URL=https://<your-project-id>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-anon-key>
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>

# Add these for E04
GPU_CLUSTER_API_URL=https://your-gpu-cluster.com
GPU_CLUSTER_API_KEY=<your-gpu-api-key>
```

---

## 🧪 Testing Instructions

### Test 1: Verify Edge Function Deployment

```bash
# Test edge function manually (trigger a cycle)
curl -X POST https://<your-project-id>.supabase.co/functions/v1/process-training-jobs \
  -H "Authorization: Bearer <anon-key>"

# Expected response:
# {"success":true,"message":"Job processing cycle complete"}
```

### Test 2: Verify Database Tables with SAOL

```bash
# Navigate to SAOL directory
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

# Check training_jobs table
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'training_jobs',select:'id,status,current_stage,progress,created_at',orderBy:[{column:'created_at',asc:false}],limit:5});console.log('Training jobs:',r.data.length);r.data.forEach(j=>console.log('-',j.id.slice(0,8),'/',j.status,'/',j.progress+'%'));})();"

# Check metrics_points table (if any jobs have run)
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'metrics_points',select:'job_id,epoch,step,training_loss,timestamp',orderBy:[{column:'timestamp',asc:false}],limit:10});console.log('Recent metrics:',r.data.length);if(r.data.length>0){r.data.forEach(m=>console.log('-',m.job_id.slice(0,8),'| epoch',m.epoch,'| step',m.step,'| loss',m.training_loss.toFixed(4)));}else{console.log('No metrics yet (expected if no jobs have started)');}})();"

# Check notifications table
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'notifications',select:'type,title,message,created_at',orderBy:[{column:'created_at',asc:false}],limit:5});console.log('Recent notifications:',r.data.length);r.data.forEach(n=>console.log('-',n.type,'/',n.title));})();"
```

### Test 3: Monitor Edge Function Logs

```bash
# View real-time logs from edge function
supabase functions logs process-training-jobs --follow

# Expected output (every 30 seconds):
# [JobProcessor] Starting job processing cycle
# [JobProcessor] No queued jobs to process
# [JobProcessor] No running jobs to update
# Job processing cycle complete
```

### Test 4: Test Job Creation and Monitoring (E2E)

1. **Create a Test Job:**
   - Navigate to: `http://localhost:3000/training/configure`
   - Select a dataset
   - Configure training parameters
   - Click "Start Training"

2. **Verify Job is Queued:**
   ```bash
   cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"
   node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'training_jobs',where:[{column:'status',operator:'eq',value:'queued'}]});console.log('Queued jobs:',r.data.length);})();"
   ```

3. **Watch Edge Function Process It:**
   - Check logs: `supabase functions logs process-training-jobs --follow`
   - Should see: "Processing 1 queued jobs"
   - Then: "Generated signed URL for job <id> from bucket: <bucket-name>"
   - Then: "Job <id> submitted to GPU cluster: <external-id>"

4. **Monitor Real-Time Updates:**
   - Navigate to: `http://localhost:3000/training/jobs/<job-id>`
   - Verify page displays:
     - ✅ Job status badge
     - ✅ Progress bar (if running)
     - ✅ Metrics cards
     - ✅ Loss curves (if metrics available)
     - ✅ Auto-refresh every 5 seconds (check Network tab)

5. **Test Job Cancellation:**
   - Click "Cancel Job" button
   - Confirm cancellation
   - Verify status changes to "Cancelled"
   - Verify notification appears

### Test 5: Verify Dual Storage Bucket Support

The edge function MUST handle both storage buckets correctly:

```bash
# Check datasets with different buckets
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,storage_bucket,storage_path',limit:10});console.log('Datasets by bucket:');r.data.forEach(d=>console.log('-',d.name,'→',d.storage_bucket));})();"
```

**Expected:**
- Some datasets in `training-files` (imported via DATA-BRIDGE)
- Some datasets in `lora-datasets` (uploaded via E02)
- Edge function generates correct signed URLs for both

---

## 🔍 Troubleshooting

### Issue: Edge Function Not Processing Jobs

**Symptoms:**
- Jobs stay in `queued` status
- No logs in edge function

**Checks:**
1. Verify Cron is enabled in Supabase Dashboard
2. Check environment variables are set correctly
3. Check edge function logs for errors: `supabase functions logs process-training-jobs`

**Solution:**
```bash
# Manually trigger to test
curl -X POST https://<project-id>.supabase.co/functions/v1/process-training-jobs \
  -H "Authorization: Bearer <anon-key>"
```

### Issue: "Failed to generate dataset signed URL"

**Symptoms:**
- Jobs fail immediately after being picked up
- Error: "Failed to generate dataset signed URL from bucket: <bucket-name>"

**Checks:**
1. Verify storage bucket exists in Supabase Storage
2. Verify dataset record has correct `storage_bucket` and `storage_path`

**Solution:**
```bash
# Check dataset storage configuration
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'id,name,storage_bucket,storage_path',where:[{column:'id',operator:'eq',value:'<job-dataset-id>'}]});console.log(JSON.stringify(r.data[0],null,2));})();"
```

### Issue: GPU Cluster API Errors

**Symptoms:**
- Jobs fail with "GPU cluster submission failed"
- External job ID not set

**Checks:**
1. Verify `GPU_CLUSTER_API_URL` is correct
2. Verify `GPU_CLUSTER_API_KEY` is valid
3. Check GPU cluster is reachable

**Solution:**
```bash
# Test GPU cluster API manually
curl -X POST <GPU_CLUSTER_API_URL>/training/submit \
  -H "Authorization: Bearer <GPU_CLUSTER_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### Issue: UI Not Auto-Refreshing

**Symptoms:**
- Metrics don't update automatically
- Need to manually refresh page

**Checks:**
1. Open browser DevTools → Network tab
2. Look for API calls to `/api/jobs/[jobId]` every 5 seconds
3. Verify job status is `running`, `queued`, or `initializing`

**Solution:**
- If job is in terminal state (`completed`, `failed`, `cancelled`), polling stops (expected)
- If job is active but not polling, check console for React Query errors

### Issue: Charts Not Rendering

**Symptoms:**
- Loss curves don't display
- Error: "recharts is not defined"

**Checks:**
1. Verify recharts is installed: `npm list recharts`
2. Check browser console for errors

**Solution:**
```bash
cd src
npm install recharts@^2.12.7
```

---

## 📊 Expected Behavior

### Job Lifecycle

1. **Queued** (status: `queued`)
   - User creates job via `/training/configure`
   - Job sits in database waiting for edge function

2. **Initializing** (status: `initializing`)
   - Edge function picks up job (within 30 seconds)
   - Generates signed URL for dataset
   - Prepares to submit to GPU cluster

3. **Running** (status: `running`)
   - Job submitted to GPU cluster
   - External job ID recorded
   - Notification sent to user
   - Edge function polls for updates every 30 seconds
   - Metrics inserted into `metrics_points` table
   - Cost calculated and updated in real-time

4. **Completed** (status: `completed`)
   - GPU cluster reports completion
   - Final cost recorded in `cost_records`
   - Progress set to 100%
   - Notification sent to user

5. **Failed** (status: `failed`)
   - Error occurs during submission or training
   - Error message recorded
   - Notification sent to user

6. **Cancelled** (status: `cancelled`)
   - User clicks "Cancel Job"
   - GPU cluster notified (if external job exists)
   - Local status updated
   - Notification sent to user

### Real-Time Updates

- **Polling Frequency:** Every 5 seconds (client-side via React Query)
- **Edge Function Frequency:** Every 30 seconds (server-side via Cron)
- **Metrics Refresh:** Automatic via polling (no page refresh needed)
- **Charts Update:** Automatic when new metrics arrive

---

## ✅ Verification Checklist

Use this checklist to confirm everything is working:

- [ ] Edge function deployed successfully
- [ ] Cron job configured and enabled (every 30 seconds)
- [ ] Environment variables set in Supabase Dashboard
- [ ] Local environment variables set in `.env.local`
- [ ] Edge function processes queued jobs (check logs)
- [ ] Jobs transition: queued → initializing → running
- [ ] Signed URLs generated for both storage buckets
- [ ] Metrics inserted into `metrics_points` table
- [ ] Costs calculated and recorded
- [ ] Notifications created for job events
- [ ] Training monitor page accessible at `/training/jobs/[jobId]`
- [ ] Page auto-refreshes every 5 seconds for active jobs
- [ ] Polling stops for completed/failed/cancelled jobs
- [ ] Loss curves render with Recharts
- [ ] Job cancellation works end-to-end
- [ ] No TypeScript errors
- [ ] No linter warnings

---

## 🎉 Success Indicators

You've successfully deployed E04 when:

1. ✅ Queued jobs automatically start within 30 seconds
2. ✅ Running jobs show real-time progress on monitor page
3. ✅ Metrics appear and update automatically
4. ✅ Loss curves visualize training progress
5. ✅ Job cancellation works immediately
6. ✅ Costs calculate correctly
7. ✅ Notifications appear for all job events
8. ✅ Dual storage bucket support works (training-files AND lora-datasets)

---

## 📝 Important Notes

### Table Names (CRITICAL)

All table references use the correct names WITHOUT `lora_` prefix:
- ✅ `training_jobs`
- ✅ `datasets`
- ✅ `metrics_points`
- ✅ `cost_records`
- ✅ `notifications`

### Storage Buckets (CRITICAL)

The edge function correctly handles BOTH buckets:
- `training-files` - Imported files from DATA-BRIDGE section
- `lora-datasets` - Newly uploaded files from E02

The code reads `dataset.storage_bucket` and uses the correct bucket for signed URLs.

### Hook Integration

The `useTrainingJob` hook from Section E03 already includes polling logic:
- Polls every 5 seconds for active jobs
- Stops polling for terminal states
- We only added `useCancelJob` as a new hook

---

## 🔜 Next Steps

After E04 is deployed and tested:

1. **Proceed to Section E05: Model Artifacts & Deployment**
   - Completed jobs will be ready for artifact creation
   - Job metadata available for artifact records
   - Cost data ready for billing analysis

2. **Monitor Edge Function Performance**
   - Watch logs for any errors
   - Monitor job processing latency
   - Adjust Cron frequency if needed (30s is recommended)

3. **GPU Cluster Integration**
   - Replace mock GPU_CLUSTER_API_URL with real endpoint
   - Test with actual GPU cluster
   - Verify callback URL works

---

**End of Deployment Guide**

## Deployment FAQs

The issue is that you installed Supabase as a local dev dependency (`-D` flag), so it's not available as a global command. You need to use `npx` to run it.

## Quick Fix

Replace `supabase` with `npx supabase` in all commands:

```bash
# Instead of:
supabase functions deploy process-training-jobs

# Use:
npx supabase functions deploy process-training-jobs
```

## All E04 Commands Updated

Here are the corrected commands for your workflow:

### Deploy Edge Function
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline"
npx supabase functions deploy process-training-jobs
```

### Watch Logs
```bash
npx supabase functions logs process-training-jobs --follow
```

### Manual Trigger Test
```bash
# After deployment, test with curl
curl -X POST https://<your-project-id>.supabase.co/functions/v1/process-training-jobs \
  -H "Authorization: Bearer <your-anon-key>"
```

## Why This Happens

- **Global install** (`npm install -g supabase`): Command available everywhere as `supabase`
- **Local dev install** (`npm install -D supabase`): Command only available via `npx supabase` or npm scripts

## Alternative: Add npm Script

You can add shortcuts to your `package.json`:

[1 tool called]

Perfect! I can see Supabase is installed as a dev dependency. Let me add helpful npm scripts:

[1 tool called]

Perfect! Now you have three options:

## Option 1: Use npx (Recommended for one-off commands)
```bash
npx supabase functions deploy process-training-jobs
npx supabase functions logs process-training-jobs --follow
```

## Option 2: Use npm scripts (Easiest for common tasks)
```bash
# Deploy the edge function
npm run sb:deploy:jobs

# Watch logs
npm run sb:logs

# Deploy any function
npm run sb:deploy process-training-jobs

# Use any supabase command
npm run supabase -- functions list
```

## Option 3: Install globally (If you prefer)
```bash
npm install -g supabase
# Then use: supabase functions deploy process-training-jobs
```

## Updated Deployment Commands

For **E04 deployment**, use either:

### Using npx:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline"
npx supabase functions deploy process-training-jobs
npx supabase functions logs process-training-jobs --follow
```

### Using npm scripts (shorter):
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline"
npm run sb:deploy:jobs
npm run sb:logs
```

## Summary

✅ **Your issue:** Local install requires `npx` prefix  
✅ **Quick fix:** Use `npx supabase` instead of `supabase`  
✅ **Better fix:** Use the npm scripts I just added (`npm run sb:deploy:jobs`)  

Try deploying now with:
```bash
npm run sb:deploy:jobs
```

This should work! Let me know if you hit any other issues.
