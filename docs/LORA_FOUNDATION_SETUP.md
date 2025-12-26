# LoRA Training Module - Foundation Setup Guide

**Section:** E01 - Foundation & Authentication  
**Date:** 2025-12-26  
**Status:** 🟢 Ready to Apply

---

## 📋 Overview

This guide walks you through setting up the foundational database infrastructure for the LoRA Training Module. You'll be creating:

- ✅ 7 new database tables
- ✅ Complete TypeScript type definitions
- ✅ 2 Supabase Storage buckets
- ✅ Row-Level Security (RLS) policies

**Estimated Time:** 30-45 minutes

---

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Supabase project created and accessible
- [ ] Environment variables configured in `.env.local`:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
- [ ] Access to Supabase Dashboard
- [ ] Node.js and npm installed

---

## 🗂️ Files Created

The following files have been created and are ready to use:

### 1. Database Migration
**Location:** `supabase/migrations/20241223_create_lora_training_tables.sql`

Contains:
- 7 table definitions
- Indexes for query performance
- RLS policies for data security
- Triggers for automatic timestamp updates

### 2. TypeScript Types
**Location:** `src/lib/types/lora-training.ts`

Contains:
- All interface definitions matching database schema
- Type enums for status fields
- Preset configurations for hyperparameters
- GPU configuration constants

### 3. Verification Script
**Location:** `scripts/verify-lora-foundation.js`

A comprehensive verification script that uses SAOL to check:
- All tables were created
- All indexes exist
- RLS policies are enabled
- Foreign keys are correct

---

## 🚀 Step-by-Step Setup

### Step 1: Apply the Database Migration

You have two options for applying the migration:

#### Option A: Via Supabase Dashboard (Recommended)

1. **Navigate to Supabase Dashboard**
   - Go to [https://supabase.com/dashboard](https://supabase.com/dashboard)
   - Select your project

2. **Open SQL Editor**
   - Click "SQL Editor" in the left sidebar
   - Click "New query"

3. **Copy Migration SQL**
   - Open `supabase/migrations/20241223_create_lora_training_tables.sql`
   - Copy the entire contents
   - Paste into the SQL Editor

4. **Execute Migration**
   - Click "Run" button (or press Ctrl+Enter / Cmd+Enter)
   - Wait for completion (should take 3-5 seconds)
   - Look for "Success. No rows returned" message

5. **Verify Execution**
   - Click "Database" in left sidebar
   - Click "Tables"
   - You should see 6 new tables:
     - `datasets`
     - `training_jobs`
     - `metrics_points`
     - `model_artifacts`
     - `cost_records`
     - `notifications`

#### Option B: Via Supabase CLI (Alternative)

```bash
# Make sure you're in the project root
cd /c/Users/james/Master/BrightHub/BRun/lora-pipeline

# Link to your Supabase project (if not already linked)
npx supabase link --project-ref YOUR_PROJECT_REF

# Apply the migration
npx supabase db push
```

---

### Step 2: Verify Database Tables (Using SAOL)

Run the verification script to ensure all tables, indexes, and policies were created:

```bash
cd /c/Users/james/Master/BrightHub/BRun/lora-pipeline
node scripts/verify-lora-foundation.js
```

**Expected Output:**

```
╔════════════════════════════════════════════════════════════╗
║   LoRA Training Module - Foundation Verification           ║
╚════════════════════════════════════════════════════════════╝

🔍 Verifying LoRA Training Tables...

✅ datasets - EXISTS
   └─ Columns: 21
   └─ Primary Key: id
✅ training_jobs - EXISTS
   └─ Columns: 25
   └─ Primary Key: id
✅ metrics_points - EXISTS
   └─ Columns: 10
   └─ Primary Key: id
✅ model_artifacts - EXISTS
   └─ Columns: 14
   └─ Primary Key: id
✅ cost_records - EXISTS
   └─ Columns: 8
   └─ Primary Key: id
✅ notifications - EXISTS
   └─ Columns: 10
   └─ Primary Key: id

... (indexes and RLS checks) ...

📊 VERIFICATION SUMMARY:

Tables:        ✅ PASS
Indexes:       ✅ PASS
RLS Policies:  ✅ PASS

✅ All verification checks passed!
   The LoRA Training foundation is ready.
```

**If Verification Fails:**
- Check that the migration ran without errors
- Verify environment variables are set correctly
- Try running the migration again (it's idempotent with `IF NOT EXISTS`)

---

### Step 3: Create Storage Buckets

You need to create 2 storage buckets for dataset uploads and model artifacts.

#### Bucket 1: `lora-datasets`

1. **Navigate to Storage**
   - Open Supabase Dashboard
   - Click "Storage" in left sidebar

2. **Create Bucket**
   - Click "New bucket"
   - Enter bucket name: `lora-datasets`
   - Set "Public bucket": **OFF** (keep private)
   - Click "Create bucket"

3. **Configure Bucket Settings**
   - Click on the `lora-datasets` bucket
   - Click "Settings" tab
   - Set **File size limit:** `500 MB`
   - Set **Allowed MIME types:** 
     ```
     application/json
     application/x-jsonlines
     text/plain
     ```
   - Click "Save"

4. **Add RLS Policies**
   - Click "Policies" tab
   - Click "New policy"
   - Select "Create a custom policy"
   
   **Policy 1: Upload**
   - Name: `Users can upload own datasets`
   - Policy command: `INSERT`
   - Policy definition:
     ```sql
     bucket_id = 'lora-datasets' AND
     (storage.foldername(name))[1] = auth.uid()::text
     ```
   - Click "Review" → "Save policy"
   
   **Policy 2: Read**
   - Name: `Users can read own datasets`
   - Policy command: `SELECT`
   - Policy definition:
     ```sql
     bucket_id = 'lora-datasets' AND
     (storage.foldername(name))[1] = auth.uid()::text
     ```
   - Click "Review" → "Save policy"
   
   **Policy 3: Delete**
   - Name: `Users can delete own datasets`
   - Policy command: `DELETE`
   - Policy definition:
     ```sql
     bucket_id = 'lora-datasets' AND
     (storage.foldername(name))[1] = auth.uid()::text
     ```
   - Click "Review" → "Save policy"

#### Bucket 2: `lora-models`

Repeat the same process as above with these settings:

- **Bucket name:** `lora-models`
- **Public:** OFF
- **File size limit:** `5 GB` (5000 MB)
- **Allowed MIME types:**
  ```
  application/octet-stream
  application/x-tar
  application/gzip
  application/json
  ```

**RLS Policies** (same structure, just change bucket name to `lora-models`):
1. `Users can upload own models` (INSERT)
2. `Users can read own models` (SELECT)
3. `Users can delete own models` (DELETE)

---

### Step 4: Verify TypeScript Types

Ensure the TypeScript types compile correctly:

```bash
cd /c/Users/james/Master/BrightHub/BRun/lora-pipeline/src
npm run build
```

**Expected:** No TypeScript compilation errors related to `lora-training.ts`

You can also test importing the types:

```typescript
// Test in any TypeScript file
import { 
  Dataset, 
  TrainingJob, 
  HYPERPARAMETER_PRESETS,
  GPU_CONFIGURATIONS
} from '@/lib/types/lora-training';

// Should compile without errors
const preset = HYPERPARAMETER_PRESETS.balanced;
console.log('Learning rate:', preset.learning_rate);
```

---

### Step 5: Manual Database Query Tests (Optional)

You can use SAOL one-liners to manually test database access:

#### Test 1: Query datasets table

```bash
cd /c/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'datasets',limit:5});console.log('Datasets count:',r.data.length);console.log('Success:',r.success);})();"
```

**Expected:** `Success: true` and `Datasets count: 0` (table is empty initially)

#### Test 2: Check RLS policies on datasets

```bash
cd /c/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentIntrospectSchema({table:'datasets',transport:'pg'});if(r.success){console.log('RLS Enabled:',r.data.rlsEnabled);console.log('Policy count:',r.data.policies.length);r.data.policies.forEach(p=>console.log('-',p.name));}})();"
```

**Expected:** 
```
RLS Enabled: true
Policy count: 3
- Users can view own datasets
- Users can create own datasets
- Users can update own datasets
```

#### Test 3: Verify foreign keys

```bash
cd /c/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops
node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentIntrospectSchema({table:'training_jobs',transport:'pg'});if(r.success){console.log('Foreign keys:');r.data.foreignKeys.forEach(fk=>console.log('-',fk.column,'→',fk.referencedTable+'.'+fk.referencedColumn));}})();"
```

**Expected:**
```
Foreign keys:
- user_id → users.id
- dataset_id → datasets.id
- artifact_id → model_artifacts.id
```

---

## ✅ Acceptance Criteria

After completing all steps, verify:

- [ ] ✅ 6 tables visible in Supabase Dashboard → Database → Tables
- [ ] ✅ All tables have correct column counts (see verification script output)
- [ ] ✅ RLS enabled on `datasets`, `training_jobs`, `model_artifacts`
- [ ] ✅ Storage bucket `lora-datasets` exists with RLS policies
- [ ] ✅ Storage bucket `lora-models` exists with RLS policies
- [ ] ✅ TypeScript types compile without errors
- [ ] ✅ Verification script passes all checks

---

## 🐛 Troubleshooting

### Issue: Migration fails with "relation already exists"

**Solution:** The migration is idempotent. If tables already exist, this is not an error. You can safely ignore this message or drop the tables and re-run:

```sql
-- CAREFUL: This deletes all data!
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS cost_records CASCADE;
DROP TABLE IF EXISTS model_artifacts CASCADE;
DROP TABLE IF EXISTS metrics_points CASCADE;
DROP TABLE IF EXISTS training_jobs CASCADE;
DROP TABLE IF EXISTS datasets CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;
```

Then re-run the migration.

### Issue: SAOL verification fails with "table not found"

**Possible causes:**
1. Migration didn't complete successfully
2. Wrong Supabase project (check `NEXT_PUBLIC_SUPABASE_URL`)
3. Using wrong database schema (tables should be in `public` schema)

**Solution:**
- Check Supabase Dashboard → Database → Tables to confirm tables exist
- Verify environment variables in `.env.local`
- Check for error messages in migration execution

### Issue: Storage bucket policies fail to apply

**Solution:**
- Ensure you're using the exact policy definitions from this guide
- Verify auth is enabled on your Supabase project
- Try removing and re-adding the policy
- Check Dashboard → Authentication → Policies for errors

### Issue: TypeScript compilation errors

**Solution:**
- Ensure `typescript` is installed: `npm install --save-dev typescript`
- Check `tsconfig.json` includes `src/lib/types/` in paths
- Try running: `cd src && npx tsc --noEmit`

---

## 📚 Next Steps

After completing this foundation setup, you're ready to move on to:

**Section E02: Dataset Management**
- Upload API endpoints
- Dataset validation logic
- Dataset management UI components

The foundation you've built provides:
- Database tables for storing datasets, jobs, metrics, models
- TypeScript types for type-safe development
- Storage buckets for file uploads
- Security through RLS policies

---

## 📞 Support

If you encounter issues:

1. **Check the verification script output** - It shows detailed error messages
2. **Review SAOL documentation** - `supa-agent-ops/QUICK_START.md`
3. **Check Supabase logs** - Dashboard → Database → Logs
4. **Verify environment variables** - Ensure all 3 Supabase keys are set

---

**Foundation Setup Complete! 🎉**

You've successfully established the database infrastructure for the LoRA Training Module.

