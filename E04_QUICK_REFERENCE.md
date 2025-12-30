# Section E04: Quick Reference Card

**Training Execution & Monitoring**  
**Implementation Status:** ✅ Complete  
**Generated:** December 29, 2025

---

## 🚀 Quick Deploy (5 minutes)

### 1. Deploy Edge Function
```bash
npx supabase functions deploy process-training-jobs
```

### 2. Set Environment Variables
**Supabase Dashboard → Edge Functions → Settings**
```
GPU_CLUSTER_API_URL=<your-gpu-cluster-endpoint>
GPU_CLUSTER_API_KEY=<your-gpu-cluster-key>
```

### 3. Configure Cron
**Supabase Dashboard → Edge Functions → Cron Jobs**
- Function: `process-training-jobs`
- Schedule: `*/30 * * * * *` (every 30 seconds)
- Status: ✅ Enabled

### 4. Verify
```bash
node scripts/test-e04-database.js
npx supabase functions logs process-training-jobs --follow
```

---

## 📁 Files Created

```
supabase/functions/process-training-jobs/index.ts   - Job processor
src/app/api/jobs/[jobId]/route.ts                   - Job details API
src/app/api/jobs/[jobId]/cancel/route.ts            - Cancel API
src/app/(dashboard)/training/jobs/[jobId]/page.tsx  - Monitor UI
src/hooks/useTrainingConfig.ts                      - Added useCancelJob
E04_DEPLOYMENT_AND_TESTING_GUIDE.md                 - Full guide
E04_IMPLEMENTATION_COMPLETE.md                      - Summary
scripts/test-e04-database.js                        - Database tests
```

---

## 🔗 Key URLs

| Route | Description |
|-------|-------------|
| `/training/jobs` | Jobs list (from E03) |
| `/training/jobs/[jobId]` | Job monitor (NEW in E04) |
| `GET /api/jobs/[jobId]` | Job details + metrics |
| `POST /api/jobs/[jobId]/cancel` | Cancel job |

---

## 🗄️ Database Tables Used

✅ All use correct names (no `lora_` prefix):
- `training_jobs` - Job records and status
- `datasets` - Dataset info and storage bucket
- `metrics_points` - Time-series metrics
- `cost_records` - Cost tracking
- `notifications` - Job lifecycle events

---

## 🔄 Job Status Flow

```
queued → initializing → running → completed
                              ↘ failed
                              ↘ cancelled
```

**Edge Function Actions:**
- `queued` → Submit to GPU, update to `initializing`
- `running` → Poll for metrics, update progress
- `completed` → Record final cost, create notification
- `failed` → Log error, create notification

---

## 📊 Real-Time Updates

| Component | Update Frequency | Trigger |
|-----------|-----------------|---------|
| Edge Function | 30 seconds | Cron schedule |
| UI Polling | 5 seconds | React Query (active jobs only) |
| Metrics Insert | Per GPU update | Edge function polling |
| Cost Calculation | Per polling cycle | Edge function |

**UI Polling Stops When:**
- Job status is `completed`
- Job status is `failed`
- Job status is `cancelled`

---

## 🪣 Storage Buckets (CRITICAL)

**Dual bucket support:**
```typescript
// Edge function reads from dataset
const storageBucket = job.dataset.storage_bucket || 'lora-datasets';

// Supports both:
'lora-datasets'    // Manual uploads (E02)
'training-files'   // Imported files (DATA-BRIDGE)
```

**Verify bucket configuration:**
```bash
cd supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',select:'name,storage_bucket',limit:10});r.data.forEach(d=>console.log(d.name,'-',d.storage_bucket||'lora-datasets'))})();"
```

---

## 🧪 Quick Tests

### Test 1: Job Processing
```bash
# Monitor edge function logs
npx supabase functions logs process-training-jobs --follow

# Expected output:
# [JobProcessor] Processing 1 queued jobs
# [JobProcessor] Job abc123... submitted to GPU cluster
```

### Test 2: Database Updates
```bash
node scripts/test-e04-database.js
```

### Test 3: UI Monitor
1. Go to `http://localhost:3000/training/jobs/<job-id>`
2. Verify status badge, progress bar, metrics cards
3. Check DevTools Network tab for 5-second polling

### Test 4: Job Cancellation
1. Click "Cancel Job" on monitor page
2. Confirm cancellation
3. Verify status changes to "cancelled"

---

## 🛠️ Troubleshooting (30 seconds)

### Jobs stuck in "queued"?
```bash
# Check if edge function is deployed
npx supabase functions list

# Check if cron is enabled
# Go to Supabase Dashboard → Edge Functions → Cron Jobs
```

### UI not updating?
```bash
# Check job is active
cd supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'training_jobs',select:'id,status',limit:1});console.log(r.data)})();"

# Status must be: queued, initializing, or running for polling
```

### Charts not rendering?
```bash
# Verify recharts installed
npm list recharts

# Should show: recharts@2.x.x
```

---

## 📦 Dependencies

**Installed:**
- `recharts` - Chart visualization

**Environment Variables Required:**
- `GPU_CLUSTER_API_URL` - Your GPU cluster endpoint
- `GPU_CLUSTER_API_KEY` - Your GPU cluster API key

---

## ✅ Checklist

**Deployment:**
- [ ] Edge function deployed
- [ ] Environment variables set
- [ ] Cron job configured and enabled
- [ ] Database migrations run (from E01)

**Testing:**
- [ ] Job processing works (queued → running)
- [ ] Metrics being inserted
- [ ] Monitor UI displays correctly
- [ ] Job cancellation works
- [ ] Both storage buckets supported

**Ready for E05:**
- [ ] Completed jobs available
- [ ] Metrics history populated
- [ ] Final costs recorded

---

## 🔜 Next: Section E05

**E05 will use:**
- Completed jobs (`status='completed'`)
- Job metadata (hyperparameters, config)
- Metrics from `metrics_points` table
- Final costs from `training_jobs.final_cost`

---

## 📞 Quick Commands Reference

```bash
# Deploy edge function
npx supabase functions deploy process-training-jobs

# View logs
npx supabase functions logs process-training-jobs --follow

# Test database
node scripts/test-e04-database.js

# Install dependencies
npm install recharts

# Type check
npm run type-check

# Lint
npm run lint
```

---

**E04 Status:** ✅ **COMPLETE - Ready for deployment!**

**Time to deploy:** ~5 minutes  
**Time to test:** ~10 minutes  
**Total setup time:** ~15 minutes

🚀 **Let's deploy!**
