# Section E04 - Quick Reference Guide

**Quick commands and checks for Section E04: Training Execution & Monitoring**

---

## 🚀 Quick Deploy

```bash
# Navigate to project
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline"

# Deploy edge function
supabase functions deploy process-training-jobs

# Watch logs
supabase functions logs process-training-jobs --follow
```

---

## ⚙️ Environment Variables Needed

### Supabase Dashboard (Edge Functions → Settings → Secrets)
```bash
SUPABASE_URL=https://<project-id>.supabase.co
SUPABASE_SERVICE_ROLE_KEY=<service-role-key>
GPU_CLUSTER_API_URL=https://your-gpu-cluster.com
GPU_CLUSTER_API_KEY=<gpu-api-key>
```

### Local .env.local
```bash
# Add these
GPU_CLUSTER_API_URL=https://your-gpu-cluster.com
GPU_CLUSTER_API_KEY=<gpu-api-key>
```

---

## 🔍 Quick Checks (SAOL)

```bash
# Navigate to SAOL
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

# Check training jobs
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'training_jobs',select:'id,status,progress',orderBy:[{column:'created_at',asc:false}],limit:5});console.log('Jobs:');r.data.forEach(j=>console.log(j.id.slice(0,8),j.status,j.progress+'%'));})();"

# Check metrics
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'metrics_points',select:'job_id,step,training_loss',orderBy:[{column:'timestamp',asc:false}],limit:5});console.log('Metrics:',r.data.length,'points');})();"

# Check notifications
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'notifications',select:'type,title',orderBy:[{column:'created_at',asc:false}],limit:3});r.data.forEach(n=>console.log(n.type,'-',n.title));})();"

# Check storage buckets
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'name,storage_bucket'});console.log('Buckets:');r.data.forEach(d=>console.log('-',d.storage_bucket));})();"
```

---

## 🧪 Quick Test Flow

1. **Create test job:**
   - Go to: http://localhost:3000/training/configure
   - Select dataset → Configure → Start Training

2. **Verify queued:**
   ```bash
   cd supa-agent-ops
   node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'training_jobs',where:[{column:'status',operator:'eq',value:'queued'}]});console.log('Queued:',r.data.length);})();"
   ```

3. **Watch processing:**
   ```bash
   supabase functions logs process-training-jobs --follow
   ```

4. **Monitor UI:**
   - Go to: http://localhost:3000/training/jobs/[job-id]
   - Verify auto-refresh (Network tab: calls every 5s)

5. **Test cancel:**
   - Click "Cancel Job"
   - Confirm
   - Verify status → cancelled

---

## 📁 Files Created

```
supabase/functions/process-training-jobs/index.ts
src/app/api/jobs/[jobId]/route.ts
src/app/api/jobs/[jobId]/cancel/route.ts
src/app/(dashboard)/training/jobs/[jobId]/page.tsx
src/hooks/useTrainingConfig.ts (modified - added useCancelJob)
```

---

## 🎯 Key Features

- ✅ Dual storage bucket support (training-files + lora-datasets)
- ✅ Auto-polling every 30 seconds (edge function)
- ✅ Auto-refresh every 5 seconds (UI)
- ✅ Real-time metrics tracking
- ✅ Loss curve visualization (Recharts)
- ✅ Job cancellation
- ✅ Cost calculation
- ✅ Notifications

---

## 🔧 Cron Schedule

**In Supabase Dashboard:**
- Go to: Edge Functions → Cron Jobs
- Function: `process-training-jobs`
- Schedule: `*/30 * * * * *` (every 30 seconds)
- Enable: ✅

---

## 🐛 Common Issues

### Jobs not processing?
```bash
# Check cron is enabled in Supabase Dashboard
# Manually trigger test:
curl -X POST https://<project-id>.supabase.co/functions/v1/process-training-jobs \
  -H "Authorization: Bearer <anon-key>"
```

### Signed URL errors?
```bash
# Check storage bucket and path
cd supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'storage_bucket,storage_path',limit:3});console.log(JSON.stringify(r.data,null,2));})();"
```

### UI not refreshing?
- Check browser Network tab for API calls
- Verify job status is active (running/queued/initializing)
- Check browser console for errors

---

## 📊 Expected Logs

```
[JobProcessor] Starting job processing cycle
[JobProcessor] Processing 1 queued jobs
[JobProcessor] Generated signed URL for job abc123 from bucket: lora-datasets
[JobProcessor] Job abc123 submitted to GPU cluster: ext_xyz789
[JobProcessor] Updating 1 running jobs
[JobProcessor] Updated job abc123: running - 25.5%
Job processing cycle complete
```

---

## ✅ Verification Checklist

- [ ] Edge function deployed
- [ ] Cron job enabled (30s)
- [ ] Environment variables set
- [ ] Jobs auto-start within 30s
- [ ] Metrics update
- [ ] Costs calculate
- [ ] Notifications appear
- [ ] UI auto-refreshes
- [ ] Charts render
- [ ] Cancel works
- [ ] Both buckets work

---

## 📚 Full Docs

- **Deployment:** `E04_DEPLOYMENT_GUIDE.md`
- **Summary:** `E04_IMPLEMENTATION_SUMMARY.md`
- **Source:** `pmc/product/_mapping/pipeline/full-build/04f-pipeline-build-section-E04-execution-prompts_v2.md`

---

**Quick Start:** Deploy → Set env vars → Enable cron → Test!

