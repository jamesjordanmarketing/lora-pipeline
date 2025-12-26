# Section E02: Deployment Checklist

**Quick Reference Guide for Deploying to Vercel**

---

## ☑️ Before You Start

- [ ] Section E01 is deployed (database tables exist)
- [ ] Vercel project connected to Github
- [ ] Supabase CLI installed and logged in
- [ ] Environment variables set in Vercel

---

## 📝 Deployment Steps

### 1. Push Code to Github (Auto-deploys to Vercel)

```bash
cd c:/Users/james/Master/BrightHub/BRun/lora-pipeline
git add .
git commit -m "feat: Implement Section E02 - Dataset Management"
git push origin main
```

- [ ] Code committed
- [ ] Code pushed to Github
- [ ] Vercel build started (check Vercel dashboard)
- [ ] Vercel build completed successfully

---

### 2. Deploy Edge Function to Supabase

```bash
supabase functions deploy validate-datasets
```

- [ ] Function deployed successfully
- [ ] Function appears in `supabase functions list`
- [ ] Can invoke manually: `supabase functions invoke validate-datasets --no-verify-jwt`

---

### 3. Configure Cron Job

**In Supabase Dashboard → Database → Cron Jobs:**
- Name: `validate-datasets-cron`
- Schedule: `* * * * *` (every 1 minute)
- Function: `validate-datasets`
- Enable: ✅

- [ ] Cron job created
- [ ] Schedule set to every 1 minute
- [ ] Job is enabled

**Verify:**
```sql
SELECT * FROM cron.job WHERE jobname = 'validate-datasets-cron';
```

---

### 4. Verify Storage Bucket

**In Supabase Dashboard → Storage:**
- [ ] Bucket `lora-datasets` exists
- [ ] Bucket is private (not public)
- [ ] RLS policies configured

---

### 5. Test in Production

**Go to: `https://your-app.vercel.app/datasets`**

- [ ] Page loads without errors
- [ ] Can click "Upload Dataset" button
- [ ] Upload a test file
- [ ] Dataset status changes: uploading → validating → ready (wait ~1 min)
- [ ] Statistics displayed correctly
- [ ] Can search/filter datasets
- [ ] Notification created (check notifications table)

---

## ✅ All Done!

When all boxes are checked, Section E02 is fully deployed and ready for production use.

**Next:** Proceed to Section E03 - Training Job Configuration

---

**Full Guide:** See `04f-pipeline-build-section-E02-execution-addendum-help.md` for detailed instructions and troubleshooting.

