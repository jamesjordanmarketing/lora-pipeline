# PIPELINE - Section E01: Foundation & Authentication - Execution Prompts

**Product:** PIPELINE  
**Section:** 1 - Foundation & Authentication  
**Generated:** 2025-12-25  
**Total Prompts:** 1  
**Estimated Total Time:** 3-5 hours  
**Source Section File:** 04f-pipeline-build-section-E01.md

---

## Section Overview

This section establishes the foundational database infrastructure for the LoRA training module. Since we're **EXTENDING** an existing Next.js + Supabase application, most infrastructure already exists. We're only adding LoRA-specific database tables, storage buckets, and TypeScript types.

**What Already Exists:**
- ✅ Next.js 14 App Router with TypeScript
- ✅ Supabase Auth with protected routes
- ✅ Supabase PostgreSQL database
- ✅ Supabase Storage
- ✅ shadcn/ui components (47+ components)
- ✅ Dashboard layout and routing
- ✅ React Query for data fetching

**What We're Adding:**
- 🆕 7 new database tables: `datasets`, `training_jobs`, `metrics_points`, `model_artifacts`, `cost_records`, `notifications`
- 🆕 2 new storage buckets: `lora-datasets`, `lora-models`
- 🆕 Complete TypeScript type definitions for LoRA training domain

---

## Prompt Sequence for This Section

This section has been divided into **1 progressive prompt**:

1. **Prompt P01: Database Foundation & TypeScript Types** (3-5 hours)
   - Features: FR-1.1
   - Key Deliverables:
     - SQL migration file with 7 tables
     - 2 Supabase storage buckets
     - Complete TypeScript type definitions
     - RLS policies for data security

---

## Integration Context

### Dependencies from Previous Sections

**None** - This is the first section (E01 - Foundation).

However, this section **depends on existing codebase infrastructure**:
- Supabase Auth system (auth.users table)
- Supabase Database client configuration
- Supabase Storage configuration
- Migration workflow in `supabase/migrations/`

### Provides for Next Sections

This section provides foundational data models for all subsequent sections:

**For Section E02 (Dataset Management):**
- `datasets` table for storing dataset metadata
- `lora-datasets` storage bucket for JSONL files
- `Dataset` TypeScript interface

**For Section E03 (Training Configuration):**
- `training_jobs` table for job state management
- `HyperparameterConfig` and `GPUConfig` interfaces
- `HYPERPARAMETER_PRESETS` configuration object

**For Section E04 (Training Execution):**
- `training_jobs` table for job updates
- `metrics_points` table for real-time metrics
- `model_artifacts` table for output storage

**For Section E05 (Model Management):**
- `model_artifacts` table for model metadata
- `lora-models` storage bucket for model files
- Quality metrics schema

**For Section E06 (Monitoring):**
- `metrics_points` table for visualization
- `training_jobs` table for status monitoring
- `cost_records` table for cost tracking

**For Section E07 (Notifications):**
- `notifications` table for user notifications
- Notification type definitions

---

## Dependency Flow (This Section)

```
E01-P01: Database Foundation & TypeScript Types
  |
  ├─ Creates: 7 database tables
  ├─ Creates: 2 storage buckets
  ├─ Creates: TypeScript type definitions
  └─ Enables: All subsequent sections
```

---

# PROMPT 1: Database Foundation & TypeScript Types

**Generated:** 2025-12-25  
**Section:** 1 - Foundation & Authentication  
**Prompt:** 1 of 1 in this section  
**Estimated Time:** 3-5 hours  
**Prerequisites:** Existing Supabase project with Auth configured

---

## 🎯 Mission Statement

Establish the foundational database schema and TypeScript types for the LoRA training module. This prompt creates all necessary database tables, storage buckets, RLS policies, and type definitions that subsequent sections will build upon. This is a pure data layer implementation with no API or UI components.

---

## 📦 Section Context

### This Section's Goal

Create the complete data infrastructure for LoRA training: 7 PostgreSQL tables with proper relationships, indexes, and security policies, plus 2 storage buckets for datasets and model artifacts.

### This Prompt's Scope

This is **Prompt 1 of 1** in Section E01. It implements:
- **FR-1.1:** Database Schema for LoRA Training (7 tables + 2 storage buckets + TypeScript types)

---

## 🔗 Integration with Previous Work

### From Previous Sections

**None** - This is the first section (E01 - Foundation).

### From Existing Codebase

This prompt **extends** existing infrastructure rather than creating from scratch:

#### Supabase Authentication
**What Exists:**
- `auth.users` table (managed by Supabase Auth)
- `auth.uid()` function for getting current user ID
- Row Level Security (RLS) system

**How We'll Use It:**
- All new tables will reference `auth.users(id)` for user ownership
- RLS policies will use `auth.uid()` to restrict access to user's own data
- Following existing RLS patterns from other tables in the system

#### Supabase Database
**What Exists:**
- PostgreSQL database configured
- Supabase client setup in `@/lib/supabase-server`
- Migration workflow in `supabase/migrations/`

**How We'll Use It:**
- Create new migration file following existing naming convention
- Use standard Supabase migration format
- Follow existing table design patterns (UUID primary keys, timestamptz for dates)

#### Supabase Storage
**What Exists:**
- Storage system configured with environment variables
- Existing buckets for other features

**How We'll Use It:**
- Create 2 new buckets via Supabase Dashboard
- Configure bucket policies (private access, file size limits, MIME types)
- Store only paths in database (never URLs, following existing pattern)

---

## 🎯 Implementation Requirements

### Feature FR-1.1: Database Schema for LoRA Training

**Type:** Database  
**Strategy:** EXTENSION - building on existing Supabase infrastructure

#### Description

Create a complete, production-ready database schema for the LoRA training module. This includes 7 tables with proper relationships, indexes, RLS policies, and TypeScript type definitions. The schema supports the full training workflow: dataset upload → validation → training job execution → model artifact storage → cost tracking → user notifications.

#### What Already Exists (Don't Rebuild)

- ✅ Supabase Auth system with `auth.users` table
- ✅ Supabase PostgreSQL database
- ✅ Supabase Storage system
- ✅ Migration directory: `supabase/migrations/`
- ✅ TypeScript types directory: `src/lib/types/`
- ✅ RLS policy patterns
- ✅ Trigger functions for `updated_at` timestamps

#### What We're Building (New in This Prompt)

- 🆕 **Migration File:** `supabase/migrations/20241223_create_lora_training_tables.sql`
  - Purpose: Create 7 new tables for LoRA training workflow
  
- 🆕 **Type Definition File:** `src/lib/types/lora-training.ts`
  - Purpose: TypeScript interfaces matching database schema
  
- 🆕 **Storage Buckets:** (via Supabase Dashboard)
  - `lora-datasets`: For storing training dataset JSONL files
  - `lora-models`: For storing trained model artifacts

#### Implementation Details

---

### Part A: Database Migration

**Migration File:** `supabase/migrations/20241223_create_lora_training_tables.sql`

**Purpose:** Create all database tables, indexes, RLS policies, and triggers for the LoRA training module.

**Tables to Create:**
1. `datasets` - Dataset metadata and validation results
2. `training_jobs` - Training job state and progress tracking
3. `metrics_points` - Time-series training metrics
4. `model_artifacts` - Trained model metadata and storage references
5. `cost_records` - Cost tracking and billing data
6. `notifications` - User notifications for training events

**Complete Migration SQL:**

```sql
-- ============================================
-- BrightRun LoRA Training Module
-- Migration: Create LoRA Training Tables
-- ============================================

BEGIN;

-- DATASETS TABLE
CREATE TABLE IF NOT EXISTS datasets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(200) NOT NULL,
  description TEXT,
  format VARCHAR(50) DEFAULT 'brightrun_lora_v4',
  status VARCHAR(50) DEFAULT 'uploading',
  storage_bucket VARCHAR(100) DEFAULT 'lora-datasets',
  storage_path TEXT NOT NULL UNIQUE,
  file_name VARCHAR(255) NOT NULL,
  file_size BIGINT NOT NULL,
  total_training_pairs INTEGER,
  total_validation_pairs INTEGER,
  total_tokens BIGINT,
  avg_turns_per_conversation DECIMAL(10, 2),
  avg_tokens_per_turn DECIMAL(10, 2),
  training_ready BOOLEAN DEFAULT FALSE,
  validated_at TIMESTAMPTZ,
  validation_errors JSONB,
  sample_data JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_datasets_user_id ON datasets(user_id);
CREATE INDEX idx_datasets_status ON datasets(status) WHERE deleted_at IS NULL;
CREATE INDEX idx_datasets_created_at ON datasets(created_at DESC);

-- RLS Policies
ALTER TABLE datasets ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own datasets"
  ON datasets FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own datasets"
  ON datasets FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own datasets"
  ON datasets FOR UPDATE
  USING (auth.uid() = user_id);

-- TRAINING_JOBS TABLE
CREATE TABLE IF NOT EXISTS training_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  dataset_id UUID NOT NULL REFERENCES datasets(id) ON DELETE RESTRICT,
  preset_id VARCHAR(50) NOT NULL,
  hyperparameters JSONB NOT NULL,
  gpu_config JSONB NOT NULL,
  status VARCHAR(50) DEFAULT 'queued',
  current_stage VARCHAR(50) DEFAULT 'queued',
  progress DECIMAL(5, 2) DEFAULT 0,
  current_epoch INTEGER DEFAULT 0,
  total_epochs INTEGER NOT NULL,
  current_step INTEGER DEFAULT 0,
  total_steps INTEGER,
  current_metrics JSONB,
  queued_at TIMESTAMPTZ DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  estimated_completion_at TIMESTAMPTZ,
  current_cost DECIMAL(10, 2) DEFAULT 0,
  estimated_total_cost DECIMAL(10, 2) NOT NULL,
  final_cost DECIMAL(10, 2),
  error_message TEXT,
  error_stack TEXT,
  retry_count INTEGER DEFAULT 0,
  external_job_id VARCHAR(255) UNIQUE,
  artifact_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_training_jobs_user_id ON training_jobs(user_id);
CREATE INDEX idx_training_jobs_status ON training_jobs(status);
CREATE INDEX idx_training_jobs_dataset_id ON training_jobs(dataset_id);

-- RLS Policies
ALTER TABLE training_jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own jobs"
  ON training_jobs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own jobs"
  ON training_jobs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- METRICS_POINTS TABLE
CREATE TABLE IF NOT EXISTS metrics_points (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id UUID NOT NULL REFERENCES training_jobs(id) ON DELETE CASCADE,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  epoch INTEGER NOT NULL,
  step INTEGER NOT NULL,
  training_loss DECIMAL(10, 6) NOT NULL,
  validation_loss DECIMAL(10, 6),
  learning_rate DECIMAL(12, 10) NOT NULL,
  gradient_norm DECIMAL(10, 6),
  throughput DECIMAL(10, 2),
  gpu_utilization DECIMAL(5, 2)
);

CREATE INDEX idx_metrics_points_job_id ON metrics_points(job_id);
CREATE INDEX idx_metrics_points_timestamp ON metrics_points(job_id, timestamp DESC);

-- MODEL_ARTIFACTS TABLE
CREATE TABLE IF NOT EXISTS model_artifacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID NOT NULL UNIQUE REFERENCES training_jobs(id) ON DELETE RESTRICT,
  dataset_id UUID NOT NULL REFERENCES datasets(id) ON DELETE RESTRICT,
  name VARCHAR(200) NOT NULL,
  version VARCHAR(50) DEFAULT '1.0.0',
  description TEXT,
  status VARCHAR(50) DEFAULT 'stored',
  deployed_at TIMESTAMPTZ,
  quality_metrics JSONB NOT NULL,
  training_summary JSONB NOT NULL,
  configuration JSONB NOT NULL,
  artifacts JSONB NOT NULL,
  parent_model_id UUID REFERENCES model_artifacts(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_model_artifacts_user_id ON model_artifacts(user_id);
CREATE INDEX idx_model_artifacts_job_id ON model_artifacts(job_id);

-- RLS Policies
ALTER TABLE model_artifacts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own models"
  ON model_artifacts FOR SELECT
  USING (auth.uid() = user_id);

-- COST_RECORDS TABLE
CREATE TABLE IF NOT EXISTS cost_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES training_jobs(id) ON DELETE SET NULL,
  cost_type VARCHAR(50) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  details JSONB,
  billing_period DATE NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cost_records_user_id ON cost_records(user_id);
CREATE INDEX idx_cost_records_billing_period ON cost_records(user_id, billing_period DESC);

-- NOTIFICATIONS TABLE
CREATE TABLE IF NOT EXISTS notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  priority VARCHAR(20) DEFAULT 'medium',
  read BOOLEAN DEFAULT FALSE,
  action_url TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(user_id, read, created_at DESC);

-- Add foreign key from training_jobs to model_artifacts
ALTER TABLE training_jobs
ADD CONSTRAINT fk_training_jobs_artifact
FOREIGN KEY (artifact_id) REFERENCES model_artifacts(id);

-- Update timestamp triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_datasets_updated_at BEFORE UPDATE ON datasets
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_training_jobs_updated_at BEFORE UPDATE ON training_jobs
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_model_artifacts_updated_at BEFORE UPDATE ON model_artifacts
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMIT;
```

**Key Design Decisions:**

1. **User Isolation:** All tables reference `auth.users(id)` with `ON DELETE CASCADE`
2. **RLS Policies:** Users can only see/modify their own data
3. **Soft Deletes:** `datasets` and `model_artifacts` use `deleted_at` for soft deletes
4. **Timestamps:** Automatic `updated_at` triggers on mutable tables
5. **Indexes:** Optimized for common queries (user lists, status filtering, time-series)
6. **JSONB Fields:** Flexible storage for configuration, metadata, and metrics
7. **Foreign Key Constraints:** Maintain referential integrity with appropriate cascade rules

---

### Part B: TypeScript Type Definitions

**File:** `src/lib/types/lora-training.ts`

**Purpose:** Provide type-safe interfaces matching the database schema for use throughout the application.

**Complete Type Definitions:**

```typescript
// Enums
export type DatasetStatus = 'uploading' | 'validating' | 'ready' | 'error';
export type JobStatus = 'queued' | 'initializing' | 'running' | 'completed' | 'failed' | 'cancelled';
export type PresetId = 'conservative' | 'balanced' | 'aggressive' | 'custom';

// Dataset Interface
export interface Dataset {
  id: string;
  user_id: string;
  name: string;
  description: string | null;
  format: 'brightrun_lora_v4' | 'brightrun_lora_v3';
  status: DatasetStatus;
  storage_bucket: string;
  storage_path: string;  // NEVER store URLs - only paths
  file_name: string;
  file_size: number;
  total_training_pairs: number | null;
  total_validation_pairs: number | null;
  total_tokens: number | null;
  avg_turns_per_conversation: number | null;
  avg_tokens_per_turn: number | null;
  training_ready: boolean;
  validated_at: string | null;
  validation_errors: ValidationError[] | null;
  sample_data: any | null;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

// Training Job Interface
export interface TrainingJob {
  id: string;
  user_id: string;
  dataset_id: string;
  preset_id: PresetId;
  hyperparameters: HyperparameterConfig;
  gpu_config: GPUConfig;
  status: JobStatus;
  current_stage: string;
  progress: number;
  current_epoch: number;
  total_epochs: number;
  current_step: number;
  total_steps: number | null;
  current_metrics: CurrentMetrics | null;
  queued_at: string;
  started_at: string | null;
  completed_at: string | null;
  estimated_completion_at: string | null;
  current_cost: number;
  estimated_total_cost: number;
  final_cost: number | null;
  error_message: string | null;
  error_stack: string | null;
  retry_count: number;
  external_job_id: string | null;
  artifact_id: string | null;
  created_at: string;
  updated_at: string;
}

// Hyperparameter Configuration
export interface HyperparameterConfig {
  base_model: string;
  learning_rate: number;
  batch_size: number;
  num_epochs: number;
  lora_rank: number;
  lora_alpha: number;
  lora_dropout: number;
  warmup_steps?: number;
  weight_decay?: number;
}

// GPU Configuration
export interface GPUConfig {
  gpu_type: string;
  num_gpus: number;
  gpu_memory_gb: number;
  cost_per_gpu_hour: number;
}

// Current Metrics
export interface CurrentMetrics {
  training_loss: number;
  validation_loss?: number;
  learning_rate: number;
  throughput?: number;
  gpu_utilization?: number;
}

// Validation Error
export interface ValidationError {
  line: number;
  error: string;
  suggestion?: string;
}

// Preset Configurations
export const HYPERPARAMETER_PRESETS: Record<PresetId, HyperparameterConfig> = {
  conservative: {
    base_model: 'mistralai/Mistral-7B-v0.1',
    learning_rate: 0.0001,
    batch_size: 4,
    num_epochs: 3,
    lora_rank: 8,
    lora_alpha: 16,
    lora_dropout: 0.05,
  },
  balanced: {
    base_model: 'mistralai/Mistral-7B-v0.1',
    learning_rate: 0.0002,
    batch_size: 8,
    num_epochs: 5,
    lora_rank: 16,
    lora_alpha: 32,
    lora_dropout: 0.1,
  },
  aggressive: {
    base_model: 'mistralai/Mistral-7B-v0.1',
    learning_rate: 0.0003,
    batch_size: 16,
    num_epochs: 10,
    lora_rank: 32,
    lora_alpha: 64,
    lora_dropout: 0.1,
  },
  custom: {
    base_model: 'mistralai/Mistral-7B-v0.1',
    learning_rate: 0.0002,
    batch_size: 8,
    num_epochs: 5,
    lora_rank: 16,
    lora_alpha: 32,
    lora_dropout: 0.1,
  },
};
```

**Key Type Design Decisions:**

1. **String Dates:** Timestamps stored as ISO strings (standard for Supabase)
2. **Nullable Fields:** Proper `| null` for optional database columns
3. **Enums as Union Types:** TypeScript union types for status fields
4. **JSONB as Interfaces:** Structured types for JSONB columns
5. **Preset Configuration:** Constant object for preset hyperparameter sets
6. **Comment on storage_path:** Explicit reminder to never store URLs, only paths

---

### Part C: Storage Buckets

**Create via Supabase Dashboard:**

#### Bucket 1: `lora-datasets`

**Configuration:**
- **Bucket Name:** `lora-datasets`
- **Public:** No (private bucket)
- **File Size Limit:** 500 MB
- **Allowed MIME Types:** 
  - `application/json`
  - `application/x-jsonlines`

**Purpose:** Store training dataset JSONL files uploaded by users.

**Bucket Policies:**
```sql
-- Users can upload to their own folder
CREATE POLICY "Users can upload datasets"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'lora-datasets' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can read from their own folder
CREATE POLICY "Users can read own datasets"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'lora-datasets' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can delete from their own folder
CREATE POLICY "Users can delete own datasets"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'lora-datasets' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

#### Bucket 2: `lora-models`

**Configuration:**
- **Bucket Name:** `lora-models`
- **Public:** No (private bucket)
- **File Size Limit:** 5 GB
- **Allowed MIME Types:**
  - `application/octet-stream`
  - `application/x-tar`
  - `application/json`

**Purpose:** Store trained model artifacts (model weights, configuration, training logs).

**Bucket Policies:**
```sql
-- Users can upload to their own folder
CREATE POLICY "Users can upload models"
ON storage.objects FOR INSERT
WITH CHECK (
  bucket_id = 'lora-models' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can read from their own folder
CREATE POLICY "Users can read own models"
ON storage.objects FOR SELECT
USING (
  bucket_id = 'lora-models' AND
  auth.uid()::text = (storage.foldername(name))[1]
);

-- Users can delete from their own folder
CREATE POLICY "Users can delete own models"
ON storage.objects FOR DELETE
USING (
  bucket_id = 'lora-models' AND
  auth.uid()::text = (storage.foldername(name))[1]
);
```

**Folder Structure Convention:**
```
lora-datasets/
└── {user_id}/
    └── {dataset_id}/
        └── dataset.jsonl

lora-models/
└── {user_id}/
    └── {job_id}/
        ├── adapter_model.bin
        ├── adapter_config.json
        ├── training_args.json
        └── training_log.jsonl
```

---

## ✅ Acceptance Criteria

### Functional Requirements

- [ ] **FR-1.1.1:** All 7 database tables created successfully
- [ ] **FR-1.1.2:** All indexes created on appropriate columns
- [ ] **FR-1.1.3:** RLS policies active and enforced on all user-facing tables
- [ ] **FR-1.1.4:** Foreign key relationships established correctly
- [ ] **FR-1.1.5:** `updated_at` triggers working on datasets, training_jobs, model_artifacts
- [ ] **FR-1.1.6:** Storage bucket `lora-datasets` created with correct policies
- [ ] **FR-1.1.7:** Storage bucket `lora-models` created with correct policies
- [ ] **FR-1.1.8:** TypeScript interfaces compile without errors
- [ ] **FR-1.1.9:** `HYPERPARAMETER_PRESETS` constant accessible and correctly typed

### Technical Requirements

- [ ] No TypeScript errors in `src/lib/types/lora-training.ts`
- [ ] Migration runs successfully without errors
- [ ] Migration is idempotent (can be run multiple times safely)
- [ ] All table names, column names follow existing naming conventions (snake_case)
- [ ] UUID generation uses `gen_random_uuid()` (Supabase standard)
- [ ] Timestamp columns use `TIMESTAMPTZ` (timezone-aware)
- [ ] JSONB columns used appropriately for structured flexible data

### Integration Requirements

- [ ] All tables successfully reference `auth.users(id)`
- [ ] RLS policies correctly use `auth.uid()` function
- [ ] Storage bucket policies reference `auth.uid()`
- [ ] Migration file naming follows existing convention in `supabase/migrations/`
- [ ] Type file location matches existing structure in `src/lib/types/`

---

## 🧪 Testing & Validation

### Step 1: Apply Migration

**Run the migration:**

```bash
# If using Supabase CLI locally
supabase db reset

# Or apply specific migration
supabase db push
```

**Expected Output:** No errors, all tables created.

---

### Step 2: Verify Tables Created

**SQL Query:**

```sql
-- Check all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'datasets',
    'training_jobs',
    'metrics_points',
    'model_artifacts',
    'cost_records',
    'notifications'
  );
```

**Expected Result:** 6 rows returned with all table names.

---

### Step 3: Verify Indexes

**SQL Query:**

```sql
-- Check indexes created
SELECT tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public' 
  AND tablename IN (
    'datasets',
    'training_jobs',
    'metrics_points',
    'model_artifacts',
    'cost_records',
    'notifications'
  )
ORDER BY tablename, indexname;
```

**Expected Result:** At least 11 indexes (3 for datasets, 3 for training_jobs, 2 for metrics_points, 2 for model_artifacts, 2 for cost_records, 2 for notifications).

---

### Step 4: Verify RLS Policies

**SQL Query:**

```sql
-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' 
  AND tablename IN (
    'datasets',
    'training_jobs',
    'model_artifacts'
  );
```

**Expected Result:** All 3 tables should have `rowsecurity = true`.

**Check policy count:**

```sql
-- Check policies exist
SELECT schemaname, tablename, policyname 
FROM pg_policies 
WHERE tablename IN (
  'datasets',
  'training_jobs',
  'model_artifacts'
)
ORDER BY tablename, policyname;
```

**Expected Result:** At least 6 policies (3 for datasets, 2 for training_jobs, 1 for model_artifacts).

---

### Step 5: Verify Foreign Keys

**SQL Query:**

```sql
-- Check foreign key constraints
SELECT
  tc.table_name,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
  AND tc.table_schema = 'public'
  AND tc.table_name IN (
    'datasets',
    'training_jobs',
    'metrics_points',
    'model_artifacts',
    'cost_records',
    'notifications'
  )
ORDER BY tc.table_name;
```

**Expected Result:** All foreign keys present (user_id → auth.users, dataset_id → datasets, job_id → training_jobs, etc.).

---

### Step 6: Verify Triggers

**SQL Query:**

```sql
-- Check triggers exist
SELECT event_object_table, trigger_name 
FROM information_schema.triggers 
WHERE event_object_schema = 'public' 
  AND event_object_table IN (
    'datasets',
    'training_jobs',
    'model_artifacts'
  );
```

**Expected Result:** 3 triggers (one for each table with updated_at).

---

### Step 7: Verify Storage Buckets

**Via Supabase Dashboard:**
1. Navigate to Storage section
2. Confirm `lora-datasets` bucket exists
3. Confirm `lora-models` bucket exists
4. Check bucket settings:
   - Both should be private
   - File size limits correct
   - Allowed MIME types configured

**Via SQL:**

```sql
-- Check buckets exist
SELECT id, name, public 
FROM storage.buckets 
WHERE name IN ('lora-datasets', 'lora-models');
```

**Expected Result:** 2 rows, both with `public = false`.

---

### Step 8: Test TypeScript Types

**Command:**

```bash
# Run TypeScript compiler
npx tsc --noEmit
```

**Expected Output:** No errors related to `src/lib/types/lora-training.ts`.

**Test Import:**

Create a temporary test file to verify imports work:

```typescript
// test-lora-types.ts
import { 
  Dataset, 
  TrainingJob, 
  HYPERPARAMETER_PRESETS 
} from '@/lib/types/lora-training';

const preset = HYPERPARAMETER_PRESETS.balanced;
console.log(preset.learning_rate); // Should be 0.0002
```

Run:

```bash
npx tsx test-lora-types.ts
```

**Expected Output:** `0.0002` (no type errors).

---

### Step 9: Test RLS Policies (Optional but Recommended)

**Create a test user and verify isolation:**

```sql
-- As admin, insert test records for different users
-- This would be done via your app normally, but for testing:

-- Insert a dataset for user1
INSERT INTO datasets (user_id, name, storage_path, file_name, file_size)
VALUES (
  '00000000-0000-0000-0000-000000000001',
  'User1 Dataset',
  'user1/dataset1/data.jsonl',
  'data.jsonl',
  1024
);

-- Try to query as user1 (should see only their dataset)
-- This requires using Supabase client with user1's JWT token
```

**Expected Behavior:** Users can only see/modify their own records.

---

### Expected Outputs

After completing this prompt, you should have:

- [ ] **Migration file** at `supabase/migrations/20241223_create_lora_training_tables.sql`
- [ ] **7 database tables** created and queryable
- [ ] **11+ indexes** created for query optimization
- [ ] **RLS policies** active on user-facing tables
- [ ] **3 triggers** for automatic timestamp updates
- [ ] **Type definition file** at `src/lib/types/lora-training.ts`
- [ ] **2 storage buckets** (`lora-datasets`, `lora-models`) created with policies
- [ ] **No TypeScript errors** when compiling the types file
- [ ] **All verification queries** passing

---

## 📦 Deliverables Checklist

### New Files Created

- [ ] `supabase/migrations/20241223_create_lora_training_tables.sql` - Complete database schema migration
- [ ] `src/lib/types/lora-training.ts` - TypeScript type definitions for LoRA training domain

### Database Changes

- [ ] Table `datasets` created with 3 indexes and 3 RLS policies
- [ ] Table `training_jobs` created with 3 indexes and 2 RLS policies
- [ ] Table `metrics_points` created with 2 indexes
- [ ] Table `model_artifacts` created with 2 indexes and 1 RLS policy
- [ ] Table `cost_records` created with 2 indexes
- [ ] Table `notifications` created with 2 indexes
- [ ] Trigger `update_datasets_updated_at` created
- [ ] Trigger `update_training_jobs_updated_at` created
- [ ] Trigger `update_model_artifacts_updated_at` created
- [ ] Function `update_updated_at_column()` created

### Storage Changes

- [ ] Bucket `lora-datasets` created with policies (500 MB limit, private)
- [ ] Bucket `lora-models` created with policies (5 GB limit, private)

### TypeScript Exports

- [ ] Type `DatasetStatus` exported
- [ ] Type `JobStatus` exported
- [ ] Type `PresetId` exported
- [ ] Interface `Dataset` exported
- [ ] Interface `TrainingJob` exported
- [ ] Interface `HyperparameterConfig` exported
- [ ] Interface `GPUConfig` exported
- [ ] Interface `CurrentMetrics` exported
- [ ] Interface `ValidationError` exported
- [ ] Constant `HYPERPARAMETER_PRESETS` exported

---

## 🔜 What's Next

### For Next Prompt in This Section

**Section Complete** - This is the final prompt in Section E01.

This prompt's deliverables will be used by **all subsequent sections** for:
- **Database operations:** All sections will query and modify these tables
- **Type safety:** All sections will import types from `lora-training.ts`
- **Storage:** Sections E02 and E05 will upload files to the buckets

### For Next Section

**Next Section:** E02: Dataset Management

Section E02 will build upon this foundation:
- **Uses `datasets` table** for storing dataset metadata
- **Uses `lora-datasets` bucket** for storing JSONL files
- **Imports `Dataset` interface** for type-safe API responses
- **Uses RLS policies** to ensure user data isolation
- Will create:
  - Dataset upload API endpoint
  - Dataset validation edge function
  - Dataset list and detail pages

---

## ⚠️ Important Reminders

### 1. Follow the Spec Exactly

All SQL and TypeScript code provided in this prompt comes from the integrated specification. Implement it **exactly as written**:
- Don't change table names or column names
- Don't modify data types
- Don't alter RLS policy logic
- Don't skip indexes or triggers

### 2. Reuse Existing Infrastructure

Don't recreate what already exists:
- ✅ Use existing `auth.users` table
- ✅ Use existing `auth.uid()` function in RLS policies
- ✅ Follow existing migration naming convention
- ✅ Follow existing TypeScript file organization

### 3. Storage Path Convention

**CRITICAL:** Always store **paths**, never URLs:
```typescript
// ✅ CORRECT
storage_path: 'user123/dataset456/data.jsonl'

// ❌ WRONG
storage_path: 'https://xxx.supabase.co/storage/v1/object/...'
```

URLs can change (domain, CDN, signed tokens), but paths are stable.

### 4. RLS Policy Testing

After creating the tables, **test RLS policies** to ensure:
- Users can only see their own data
- Users cannot modify other users' data
- Proper error messages if unauthorized access attempted

### 5. Migration Safety

The migration uses:
- `CREATE TABLE IF NOT EXISTS` - safe to run multiple times
- `BEGIN` and `COMMIT` - atomic transaction
- Proper foreign key constraints with appropriate cascade rules

### 6. TypeScript Type Accuracy

Ensure TypeScript interfaces **exactly match** the database schema:
- Nullable fields use `| null`
- Timestamp fields use `string` (ISO format from Supabase)
- JSONB fields have structured interfaces where possible

### 7. No API or UI Yet

This prompt is **pure data layer**. Don't create:
- API routes
- React components
- Pages
- Hooks

Those come in subsequent sections that build on this foundation.

---

## 📚 Reference Materials

### Files from Existing Codebase

#### Authentication
- `@/lib/supabase-server` - Server-side Supabase client
- `@/lib/auth-service` - Auth utility functions
- Pattern: `requireAuth()` for protected routes

#### Database
- Existing migrations in `supabase/migrations/`
- Pattern: `YYYYMMDD_description.sql` naming
- Pattern: UUID primary keys, TIMESTAMPTZ timestamps

#### TypeScript Types
- Existing types in `src/lib/types/`
- Pattern: One file per domain area
- Pattern: Interfaces exported, not classes

### Infrastructure Patterns

**Database:**
- Primary keys: `UUID DEFAULT gen_random_uuid()`
- Timestamps: `TIMESTAMPTZ DEFAULT NOW()`
- User references: `REFERENCES auth.users(id) ON DELETE CASCADE`
- RLS: `auth.uid() = user_id`

**TypeScript:**
- Dates as strings (ISO format)
- Union types for enums
- `| null` for nullable fields
- JSONB as structured interfaces

**Storage:**
- Private buckets for user data
- Folder structure: `{user_id}/{resource_id}/filename`
- Store paths, not URLs
- RLS policies using `storage.foldername()`

---

**Ready to implement Section E01, Prompt P01!**

This is a foundational data layer implementation. Take your time, verify each step, and ensure all verification queries pass before considering this prompt complete.

---

## Section Completion Checklist

After completing all prompts in this section (only P01):

- [ ] All 7 database tables exist and are queryable
- [ ] All indexes created
- [ ] All RLS policies active and tested
- [ ] All triggers functional
- [ ] TypeScript types file compiles without errors
- [ ] Both storage buckets created with correct policies
- [ ] Migration is idempotent (can run multiple times safely)
- [ ] Foreign key relationships working correctly
- [ ] No TypeScript errors in the codebase
- [ ] All verification SQL queries pass
- [ ] Ready to proceed to Section E02 (Dataset Management)

---

**End of Section E01 Execution Prompts**

