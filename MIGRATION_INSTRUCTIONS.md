# ⚡ Quick Migration Instructions - LoRA Training Foundation

**Status:** 🟡 Ready to Apply  
**Time Required:** 5 minutes

---

## 📋 What's Been Created

✅ **Database Migration File:**  
`supabase/migrations/20241223_create_lora_training_tables.sql`

✅ **TypeScript Types:**  
`src/lib/types/lora-training.ts`

✅ **Verification Script:**  
`scripts/verify-lora-foundation.js`

✅ **Setup Guide:**  
`docs/LORA_FOUNDATION_SETUP.md`

---

## 🚀 Quick Start: Apply the Migration

### Step 1: Apply Migration via Supabase Dashboard

1. **Open Supabase Dashboard**
   - Go to: https://supabase.com/dashboard
   - Select your project

2. **Open SQL Editor**
   - Click "SQL Editor" in the left sidebar
   - Click "+ New query"

3. **Copy Migration SQL**
   - Open file: `supabase/migrations/20241223_create_lora_training_tables.sql`
   - Press `Ctrl+A` to select all
   - Press `Ctrl+C` to copy

4. **Execute Migration**
   - Paste into SQL Editor
   - Click "Run" button (or press `Ctrl+Enter`)
   - Wait 3-5 seconds for completion

5. **Verify Success**
   - You should see: "Success. No rows returned"
   - Click "Database" → "Tables" in sidebar
   - You should see 6 new tables:
     - ✅ `datasets`
     - ✅ `training_jobs`
     - ✅ `metrics_points`
     - ✅ `model_artifacts`
     - ✅ `cost_records`
     - ✅ `notifications`

---

### Step 2: Verify Installation

Run the verification script:

```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops"

node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{console.log('Verifying tables...');const tables=['datasets','training_jobs','metrics_points','model_artifacts','cost_records','notifications'];for(const t of tables){const r=await saol.agentQuery({table:t,limit:1});console.log(t+':',r.success?'✅ READY':'❌ MISSING');}})();"
```

**Expected Output:**
```
datasets: ✅ READY
training_jobs: ✅ READY
metrics_points: ✅ READY
model_artifacts: ✅ READY
cost_records: ✅ READY
notifications: ✅ READY
```

---

### Step 3: Create Storage Buckets

#### Create `lora-datasets` bucket:

1. **Navigate to Storage**
   - Supabase Dashboard → Storage (left sidebar)

2. **Create Bucket**
   - Click "+ New bucket"
   - **Name:** `lora-datasets`
   - **Public:** OFF (uncheck)
   - Click "Create bucket"

3. **Add RLS Policies**
   - Click on `lora-datasets` bucket
   - Click "Policies" tab
   - Click "+ New policy" → "Create a custom policy"
   
   **Add 3 Policies:**

   **Policy 1 - Upload:**
   ```
   Name: Users can upload own datasets
   Command: INSERT
   Definition:
   bucket_id = 'lora-datasets' AND
   (storage.foldername(name))[1] = auth.uid()::text
   ```

   **Policy 2 - Read:**
   ```
   Name: Users can read own datasets
   Command: SELECT
   Definition:
   bucket_id = 'lora-datasets' AND
   (storage.foldername(name))[1] = auth.uid()::text
   ```

   **Policy 3 - Delete:**
   ```
   Name: Users can delete own datasets
   Command: DELETE
   Definition:
   bucket_id = 'lora-datasets' AND
   (storage.foldername(name))[1] = auth.uid()::text
   ```

#### Create `lora-models` bucket:

Repeat the same process:
- **Name:** `lora-models`
- **Public:** OFF
- **Same 3 policies** (just change bucket_id to `'lora-models'`)

---

### Step 4: Verify TypeScript Types

```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/src"
npm run build
```

Should complete with no TypeScript errors.

---

## ✅ Completion Checklist

After completing all steps, you should have:

- [ ] ✅ 6 database tables created
- [ ] ✅ RLS policies enabled on 3 tables
- [ ] ✅ 2 storage buckets created with policies
- [ ] ✅ TypeScript types compile successfully
- [ ] ✅ Verification script confirms all tables accessible

---

## 📊 What This Provides

This foundation enables:

✅ **Dataset Management** - Store and validate training datasets  
✅ **Training Job Tracking** - Monitor training progress and costs  
✅ **Metrics Collection** - Realtime training metrics  
✅ **Model Artifacts** - Store trained model files  
✅ **Cost Tracking** - Monitor training expenses  
✅ **Notifications** - User notifications for job completion  

---

## 🔜 Next Section

After completing this foundation:

**→ Move to Section E02: Dataset Management**
- Build dataset upload API
- Create dataset validation logic
- Design dataset management UI

---

## 📞 Need Help?

See the complete guide: `docs/LORA_FOUNDATION_SETUP.md`

**Common Issues:**
- Migration errors → Check if tables already exist
- SAOL errors → Verify `.env.local` has all 3 Supabase variables
- Storage bucket errors → Ensure Auth is enabled in Supabase project

---

**Status:** 🟢 Files created, ready to apply migration

