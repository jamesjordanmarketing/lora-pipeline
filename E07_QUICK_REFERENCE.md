# Section E07: Quick Reference Guide

**Version:** 2.0  
**Last Updated:** December 30, 2025  
**Status:** ✅ Implementation Complete

---

## 🚀 Quick Start Commands

### Run Integration Verification
```bash
npx tsx scripts/verify-lora-integration.ts
```
**Purpose:** Verify all system components are properly integrated  
**Expected:** All checks pass (green), exit code 0

### Run Health Check
```bash
npx tsx scripts/check-lora-health.ts
```
**Purpose:** Quick operational health status  
**Expected:** Visual health dashboard with system metrics

---

## 📁 Files Created in Section E07

| File | Purpose | Size |
|------|---------|------|
| `scripts/verify-lora-integration.ts` | Automated integration verification | 250 lines |
| `scripts/check-lora-health.ts` | Quick health check script | 130 lines |
| `docs/LORA_DEPLOYMENT_CHECKLIST.md` | Complete deployment guide | 400+ lines |
| `docs/LORA_MONITORING_SETUP.md` | Monitoring and observability guide | 500+ lines |
| `docs/E07_IMPLEMENTATION_COMPLETE.md` | Implementation summary | This section |

---

## 🎯 What Section E07 Delivers

### 1. Integration Verification
- Automated checking of all system components
- Environment variable validation
- Database table and RLS policy verification
- Storage bucket configuration checks
- API route and type definition verification

### 2. Deployment Documentation
- Step-by-step deployment checklist
- Database setup verification
- Storage bucket configuration with RLS policies
- Edge Functions deployment and cron setup
- Frontend deployment to Vercel
- Post-deployment testing procedures
- Rollback plans

### 3. Monitoring & Observability
- Key metrics with SQL queries (15+ queries)
- Logging strategies for API routes, Edge Functions, and client
- Alert configuration (Critical, Warning, Info levels)
- Dashboard setup instructions
- Performance monitoring targets
- Health check automation
- Incident response procedures
- Regular maintenance tasks

### 4. Operational Tools
- Integration verification script
- Health check script
- Ready-to-use SQL queries for monitoring
- Troubleshooting guides

---

## 📊 Integration Checks Performed

The integration verification script checks:

1. ✅ **Environment Variables**
   - NEXT_PUBLIC_SUPABASE_URL
   - NEXT_PUBLIC_SUPABASE_ANON_KEY
   - SUPABASE_SERVICE_ROLE_KEY
   - GPU_CLUSTER_API_URL (optional)
   - GPU_CLUSTER_API_KEY (optional)

2. ✅ **Database Tables** (6 tables)
   - datasets
   - training_jobs
   - metrics_points
   - model_artifacts
   - cost_records
   - notifications

3. ✅ **RLS Policies**
   - Verifies RLS enabled on user-facing tables
   - Ensures data isolation between users

4. ✅ **Storage Buckets** (2 buckets)
   - lora-datasets (private, 500MB limit)
   - lora-models (private, 5GB limit)

5. ✅ **Database Indexes** (6+ indexes)
   - Performance optimization verification

6. ✅ **Edge Functions** (3 functions)
   - validate-datasets
   - process-training-jobs
   - create-model-artifacts

7. ✅ **API Routes** (5 main routes)
   - /api/datasets
   - /api/jobs
   - /api/models
   - /api/costs
   - /api/notifications

8. ✅ **Type Definitions**
   - src/lib/types/lora-training.ts

---

## 🔍 Key Monitoring Queries

### Check Queue Depth
```sql
SELECT COUNT(*) FROM training_jobs WHERE status = 'queued';
```
**Target:** < 10 (normal), 10-50 (warning), > 50 (critical)

### Check Failed Jobs (24h)
```sql
SELECT COUNT(*) FROM training_jobs 
WHERE status = 'failed' 
  AND created_at > NOW() - INTERVAL '24 hours';
```
**Target:** 0 (ideal), 1-5 (acceptable), > 5 (investigate)

### Check Storage Usage
```sql
SELECT 
  SUM(file_size) / 1024 / 1024 / 1024 as total_gb
FROM datasets
WHERE deleted_at IS NULL;
```
**Monitor:** Stay below Supabase plan limit

### Check Daily Cost
```sql
SELECT 
  DATE(recorded_at) as date,
  SUM(amount) as total_cost
FROM cost_records
WHERE recorded_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(recorded_at)
ORDER BY date DESC;
```
**Monitor:** For unexpected spikes

---

## 🚨 Alert Thresholds

### Critical (Immediate Action)
- Queue depth > 50 for > 30 minutes
- Edge Function failures (3+ consecutive)
- Database connection errors (10+ in 5 minutes)

### Warning (Action Within 24h)
- Job failure rate > 20% over 24h
- Storage usage > 80% of plan limit
- Average validation time > 5 minutes

### Info (Awareness)
- Daily summary reports
- Usage trends
- System metrics

---

## 📋 Pre-Deployment Checklist

Before deploying to production:

- [ ] Run integration verification script (all checks pass)
- [ ] No TypeScript errors (`npm run build`)
- [ ] No linter warnings (`npm run lint`)
- [ ] All environment variables documented
- [ ] Database migration applied
- [ ] Storage buckets created with RLS policies
- [ ] Edge Functions deployed
- [ ] Cron schedules configured
- [ ] Monitoring queries tested
- [ ] Rollback plan reviewed

---

## 🎯 Post-Deployment Verification

After deploying:

1. **Run Scripts**
   ```bash
   npx tsx scripts/verify-lora-integration.ts
   npx tsx scripts/check-lora-health.ts
   ```

2. **Test User Flows**
   - Dataset upload → validation → ready
   - Training job creation → execution → completion
   - Model artifact download

3. **Check Monitoring**
   - Supabase Dashboard: Edge Functions running
   - Database: Queries executing normally
   - Logs: No recurring errors

4. **Verify Security**
   - RLS policies enforcing correctly
   - No cross-user data leakage
   - Authentication working on all routes

---

## 💡 Common Commands

### Check Environment Variables
```bash
# Show configured variables (be careful not to expose secrets!)
grep -E "^(NEXT_PUBLIC_|SUPABASE_|GPU_)" .env.local
```

### Deploy Edge Functions
```bash
cd supabase
npx supabase functions deploy validate-datasets
npx supabase functions deploy process-training-jobs
npx supabase functions deploy create-model-artifacts
```

### Check Edge Function Logs
```bash
npx supabase functions logs validate-datasets --follow
```

### Build Frontend
```bash
cd src
npm run build
```

### Deploy to Vercel
```bash
cd src
vercel --prod
```

---

## 🔧 Troubleshooting Quick Reference

| Issue | Check | Solution |
|-------|-------|----------|
| Jobs stuck in queue | Edge Function running? | Verify cron schedule, redeploy function |
| Upload fails | Storage bucket exists? | Check RLS policies, verify bucket config |
| Auth errors | Environment variables set? | Verify SUPABASE keys in production |
| High costs | Unexpected job volume? | Review cost records, check job configs |
| Slow validation | Large dataset? | Check Edge Function logs, optimize validation |

---

## 📚 Documentation Index

1. **Integration & Testing**
   - `scripts/verify-lora-integration.ts` - Automated verification
   - `scripts/check-lora-health.ts` - Health monitoring
   - `docs/E07_IMPLEMENTATION_COMPLETE.md` - Implementation summary

2. **Deployment**
   - `docs/LORA_DEPLOYMENT_CHECKLIST.md` - Complete deployment guide
   - Sections: Database, Storage, Edge Functions, Frontend

3. **Monitoring**
   - `docs/LORA_MONITORING_SETUP.md` - Monitoring guide
   - Sections: Metrics, Logging, Alerts, Dashboards, Incidents

4. **Previous Sections**
   - E01: Foundation & Authentication
   - E02: Dataset Management
   - E03: Training Configuration
   - E04: Training Execution & Monitoring
   - E05: Model Artifacts & Delivery
   - E06: Cost Tracking & Notifications

---

## 🎉 Success Criteria

Deployment is successful when:

✅ Integration verification script passes  
✅ All database tables accessible  
✅ All storage buckets configured  
✅ All Edge Functions running  
✅ All API routes responding  
✅ RLS policies enforcing  
✅ Complete user workflows working  
✅ No critical errors in logs  
✅ Health check shows all green  

---

## 🚀 You're Ready to Deploy!

All tools, documentation, and verification scripts are in place. Follow the deployment checklist step-by-step, and you'll have a production-ready LoRA Training Platform!

**Next Step:** Open `docs/LORA_DEPLOYMENT_CHECKLIST.md` and start deploying!

---

**Quick Reference Complete!**  
**Date:** December 30, 2025  
**Status:** ✅ READY FOR PRODUCTION

