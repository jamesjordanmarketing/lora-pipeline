# BrightRun LoRA Training Platform - Integrated Extension Specification

**Version:** 1.0  
**Date:** December 24, 2025  
**Source:** 04c-pipeline-structured-from-wireframe_v1.md  
**Integration Basis:** Infrastructure Inventory v1, Extension Strategy v1, Implementation Guide v1

---

## INTEGRATION SUMMARY

This specification describes how to implement the BrightRun LoRA Training Platform as an EXTENSION to the existing BrightHub application.

**Approach**: EXTENSION (not separate application)

**Infrastructure Decisions**:
- ✅ Use existing Supabase Auth (not NextAuth)
- ✅ Use existing Supabase PostgreSQL (not Prisma)
- ✅ Use existing Supabase Storage (not S3)
- ✅ Use existing shadcn/ui components
- ✅ Use existing React Query (not SWR)
- ✅ Use Edge Functions + Cron (not BullMQ + Redis)

**What We're Adding**:
- 7 new database tables
- 2 new storage buckets
- ~25 new API routes
- ~8-10 new pages
- ~25-30 new components
- ~15 new hooks
- 2 Edge Functions

**What We're NOT Creating**:
- ❌ New authentication system
- ❌ New database client
- ❌ New storage client
- ❌ Job queue infrastructure
- ❌ Component library

---

## SECTION 1: Foundation & Authentication - INTEGRATED

**Extension Status**: ✅ Most infrastructure ALREADY EXISTS - only adding LoRA-specific tables

**Original Infrastructure** (from spec): NextAuth.js, Prisma ORM, base layouts  
**Actual Infrastructure** (what we're using): Supabase Auth, Supabase PostgreSQL, existing DashboardLayout

---

### Overview (from original spec)

This section establishes the foundational infrastructure. However, since we're EXTENDING an existing application, most of this already exists.

**What Already Exists**:
- ✅ Next.js 14 App Router with TypeScript
- ✅ Supabase Auth with protected routes
- ✅ Supabase PostgreSQL database
- ✅ Supabase Storage
- ✅ shadcn/ui components (47+ components)
- ✅ Dashboard layout and routing
- ✅ React Query for data fetching

**What We're Adding** (LoRA Training specific):
- New database tables: `datasets`, `training_jobs`, `metrics_points`, `model_artifacts`, `cost_records`, `notifications`
- New storage buckets: `lora-datasets`, `lora-models`

---

### Dependencies

**Codebase Prerequisites** (MUST exist before this section):
- ✅ Supabase Auth configured (`@/lib/supabase-server`, `@/lib/auth-service`)
- ✅ Supabase Database client (`createServerSupabaseClient()`)
- ✅ Supabase Storage configured (environment variables)
- ✅ DashboardLayout component (`(dashboard)/layout.tsx`)
- ✅ shadcn/ui components in `/components/ui/`
- ✅ React Query provider configured

**Previous Section Prerequisites**: N/A (foundation section)

---

### Features & Requirements (INTEGRATED)

#### FR-1.1: Database Schema for LoRA Training

**Type**: Data Model

**Description**: Create new PostgreSQL tables for LoRA training features using Supabase migrations.

**Implementation Strategy**: EXTENSION (using existing Supabase database)

---

**Database Changes (INTEGRATED)**:

Instead of Prisma, use **Supabase Client** with direct SQL migration:

**Migration File**: `supabase/migrations/20241223_create_lora_training_tables.sql`

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

**Pattern Source**: Infrastructure Inventory Section 2 - Database Infrastructure

**Storage Buckets to Create** (via Supabase Dashboard):

1. **Bucket**: `lora-datasets`
   - Public: No (private)
   - File size limit: 500 MB
   - Allowed MIME types: `application/json`, `application/x-jsonlines`

2. **Bucket**: `lora-models`
   - Public: No (private)
   - File size limit: 5 GB
   - Allowed MIME types: `application/octet-stream`, `application/x-tar`, `application/json`

---

**TypeScript Interfaces:**

**File**: `src/lib/types/lora-training.ts`

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

---

**Acceptance Criteria** (from spec):
1. ✅ Database tables created with proper indexes
2. ✅ RLS policies active for user data isolation
3. ✅ Storage buckets created with private access
4. ✅ TypeScript interfaces defined matching schema
5. ✅ Migration runs successfully

**Verification Steps**:
1. ✅ Database: Run migration, verify 7 tables exist
2. ✅ Storage: Create buckets via Supabase Dashboard
3. ✅ Types: TypeScript compiles without errors
4. ✅ RLS: Test that users can only access their own data

---

### Section Summary

**What Was Added**:
- 7 new database tables (datasets, training_jobs, metrics_points, model_artifacts, cost_records, notifications)
- 2 new storage buckets (lora-datasets, lora-models)
- Complete TypeScript type definitions
- RLS policies for data security

**What Was Reused**:
- Existing Supabase PostgreSQL database
- Existing authentication system (auth.users table)
- Existing migration workflow

**Integration Points**:
- All tables reference `auth.users(id)` for user ownership
- RLS policies use `auth.uid()` from existing auth system
- Storage buckets use same Supabase project

---

## SECTION 2: Dataset Management - INTEGRATED

**Extension Status**: ✅ Transformed to use existing infrastructure  
**Original Infrastructure**: S3 presigned URLs, BullMQ validation workers  
**Actual Infrastructure**: Supabase Storage on-demand signed URLs, Edge Functions for validation

---

### Overview (from original spec)

Enable users to upload, validate, and manage conversation datasets for LoRA training.

**User Value**: Users can upload conversation datasets, validate formats, view statistics, and manage their dataset library

---

### Dependencies

**Codebase Prerequisites** (MUST exist before this section):
- ✅ Supabase Auth (`requireAuth()` function from `@/lib/supabase-server`)
- ✅ Supabase Storage configured (buckets created)
- ✅ Database tables created (from Section 1)
- ✅ DashboardLayout component

**Previous Section Prerequisites**:
- Section 1: Dataset table, storage buckets, type definitions

---

### Features & Requirements (INTEGRATED)

#### FR-2.1: Dataset Upload with Presigned URLs

**Type**: Storage Integration

**Description**: Allow users to upload large dataset files directly to Supabase Storage using presigned upload URLs.

**Implementation Strategy**: EXTENSION (using existing Supabase Storage)

---

**API Routes (INTEGRATED)**:

Instead of AWS S3 SDK, use **Supabase Storage** with existing patterns:

**File**: `src/app/api/datasets/route.ts`

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth } from '@/lib/supabase-server';
import { createServerSupabaseClient, createServerSupabaseAdminClient } from '@/lib/supabase-server';
import { CreateDatasetSchema } from '@/lib/types/lora-training';

/**
 * POST /api/datasets - Create dataset and generate presigned upload URL
 */
export async function POST(request: NextRequest) {
  try {
    // Authentication (existing pattern)
    const { user, response } = await requireAuth(request);
    if (response) return response;

    // Parse and validate request
    const body = await request.json();
    const validation = CreateDatasetSchema.safeParse(body);
    
    if (!validation.success) {
      return NextResponse.json(
        {
          error: 'Validation error',
          details: validation.error.flatten().fieldErrors,
        },
        { status: 400 }
      );
    }

    const { name, description, format = 'brightrun_lora_v4', file_name, file_size } = validation.data;

    // Check file size limit (500MB)
    const MAX_FILE_SIZE = 500 * 1024 * 1024;
    if (file_size > MAX_FILE_SIZE) {
      return NextResponse.json(
        { error: 'File size exceeds limit', details: 'Maximum file size is 500MB' },
        { status: 400 }
      );
    }

    // Generate unique dataset ID and storage path
    const datasetId = crypto.randomUUID();
    const storagePath = `${user.id}/${datasetId}/${file_name}`;

    // Create dataset record in database
    const supabase = await createServerSupabaseClient();
    const { data: dataset, error: dbError } = await supabase
      .from('datasets')
      .insert({
        id: datasetId,
        user_id: user.id,
        name,
        description,
        format,
        storage_bucket: 'lora-datasets',
        storage_path: storagePath,  // Store path only, NOT URL
        file_name,
        file_size,
        status: 'uploading',
      })
      .select()
      .single();

    if (dbError) {
      console.error('Database error:', dbError);
      return NextResponse.json(
        { error: 'Failed to create dataset', details: dbError.message },
        { status: 500 }
      );
    }

    // Generate presigned upload URL (valid for 1 hour)
    const supabaseAdmin = createServerSupabaseAdminClient();
    const { data: uploadData, error: uploadError } = await supabaseAdmin.storage
      .from('lora-datasets')
      .createSignedUploadUrl(storagePath);

    if (uploadError) {
      console.error('Storage error:', uploadError);
      // Rollback dataset creation
      await supabase.from('datasets').delete().eq('id', datasetId);
      return NextResponse.json(
        { error: 'Failed to generate upload URL', details: uploadError.message },
        { status: 500 }
      );
    }

    // Return dataset info and upload URL
    return NextResponse.json(
      {
        success: true,
        data: {
          dataset,
          uploadUrl: uploadData.signedUrl,  // Client uploads directly to this URL
          storagePath,
        },
      },
      { status: 201 }
    );
  } catch (error) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      {
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/datasets - List user's datasets with pagination
 */
export async function GET(request: NextRequest) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    // Parse query parameters
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '25');
    const status = searchParams.get('status');
    const search = searchParams.get('search');

    // Database query (existing pattern)
    const supabase = await createServerSupabaseClient();
    let query = supabase
      .from('datasets')
      .select('*', { count: 'exact' })
      .eq('user_id', user.id)
      .is('deleted_at', null)
      .order('created_at', { ascending: false });

    // Apply filters
    if (status) query = query.eq('status', status);
    if (search) query = query.ilike('name', `%${search}%`);

    // Apply pagination
    const from = (page - 1) * limit;
    const to = from + limit - 1;
    query = query.range(from, to);

    const { data: datasets, error, count } = await query;

    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to fetch datasets', details: error.message },
        { status: 500 }
      );
    }

    // Response format (existing pattern)
    return NextResponse.json({
      success: true,
      data: {
        datasets: datasets || [],
        total: count || 0,
        page,
        limit,
        totalPages: Math.ceil((count || 0) / limit),
      },
    });
  } catch (error) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      {
        error: 'Internal server error',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}
```

**Pattern Source**: Infrastructure Inventory Section 3 - Storage Infrastructure, Section 4 - API Architecture

**Storage Best Practices** (from inventory):
- Never store URLs in database - store only `storage_path`
- Generate signed URLs on-demand via API routes
- Use admin client for signing operations
- Set appropriate expiry (3600 seconds = 1 hour)

---

**Client-Side Upload Flow**:

```typescript
// In React component
const { mutate: createDataset } = useCreateDataset();

async function handleUpload(file: File) {
  // Step 1: Create dataset record and get upload URL
  const response = await createDataset({
    name: datasetName,
    file_name: file.name,
    file_size: file.size,
  });

  const { uploadUrl, dataset } = response.data;

  // Step 2: Upload file directly to Supabase Storage
  const uploadResponse = await fetch(uploadUrl, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/octet-stream',
    },
    body: file,
  });

  if (!uploadResponse.ok) {
    throw new Error('Failed to upload file');
  }

  // Step 3: Confirm upload to trigger validation
  await fetch(`/api/datasets/${dataset.id}/confirm`, {
    method: 'POST',
  });
}
```

---

#### FR-2.2: Dataset Validation

**Type**: Background Processing

**Description**: Validate uploaded datasets for format correctness and calculate statistics.

**Implementation Strategy**: EXTENSION (using Edge Functions instead of BullMQ)

---

**Background Processing (INTEGRATED)**:

Instead of BullMQ + Redis, use **Supabase Edge Functions** with Cron:

**File**: `supabase/functions/validate-datasets/index.ts`

```typescript
import { createClient } from '@supabase/supabase-js';

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  // Fetch datasets pending validation
  const { data: datasets } = await supabase
    .from('datasets')
    .select('*')
    .eq('status', 'validating');

  for (const dataset of datasets || []) {
    try {
      // Download dataset file
      const { data: fileData } = await supabase.storage
        .from('lora-datasets')
        .download(dataset.storage_path);

      if (!fileData) {
        throw new Error('Failed to download file');
      }

      // Parse and validate JSONL format
      const text = await fileData.text();
      const lines = text.split('\n').filter(l => l.trim());
      
      let totalPairs = 0;
      let totalTokens = 0;
      const errors: any[] = [];
      const sampleData: any[] = [];

      for (let i = 0; i < lines.length; i++) {
        try {
          const conversation = JSON.parse(lines[i]);
          
          // Validate structure
          if (!conversation.conversation_id || !Array.isArray(conversation.turns)) {
            errors.push({
              line: i + 1,
              error: 'Invalid structure',
              suggestion: 'Each line must have conversation_id and turns array',
            });
            continue;
          }

          // Count training pairs
          totalPairs += conversation.turns.length;
          
          // Estimate tokens (rough estimation)
          totalTokens += conversation.turns.reduce((sum: number, turn: any) => {
            return sum + (turn.content?.split(' ').length || 0) * 1.3;
          }, 0);

          // Sample first 3 conversations
          if (sampleData.length < 3) {
            sampleData.push(conversation);
          }
        } catch (parseError) {
          errors.push({
            line: i + 1,
            error: 'JSON parse error',
            suggestion: 'Ensure each line is valid JSON',
          });
        }
      }

      // Update dataset with validation results
      const updateData: any = {
        validated_at: new Date().toISOString(),
      };

      if (errors.length > 0) {
        updateData.status = 'error';
        updateData.validation_errors = errors.slice(0, 10);  // First 10 errors
        updateData.training_ready = false;
      } else {
        updateData.status = 'ready';
        updateData.training_ready = true;
        updateData.total_training_pairs = totalPairs;
        updateData.total_tokens = Math.round(totalTokens);
        updateData.sample_data = sampleData;
        updateData.avg_turns_per_conversation = totalPairs / lines.length;
      }

      await supabase
        .from('datasets')
        .update(updateData)
        .eq('id', dataset.id);

      // Create notification
      if (updateData.status === 'ready') {
        await supabase.from('notifications').insert({
          user_id: dataset.user_id,
          type: 'dataset_ready',
          title: 'Dataset Ready',
          message: `Your dataset "${dataset.name}" is ready for training`,
          priority: 'medium',
          action_url: `/datasets/${dataset.id}`,
        });
      }
    } catch (error) {
      console.error(`Validation error for dataset ${dataset.id}:`, error);
      
      await supabase
        .from('datasets')
        .update({
          status: 'error',
          error_message: error instanceof Error ? error.message : 'Validation failed',
        })
        .eq('id', dataset.id);
    }
  }

  return new Response('OK');
});
```

**Deployment**: Via Supabase CLI (`supabase functions deploy validate-datasets`)

**Cron Trigger**: Configure in Supabase Dashboard  
- Function: `validate-datasets`
- Schedule: `* * * * *` (every 1 minute)

**Reason for Change**: BullMQ + Redis adds infrastructure complexity. Supabase Edge Functions + Cron provides equivalent functionality with less overhead.

**Pattern Source**: Extension Strategy Section - Background Processing

---

**Data Fetching (INTEGRATED)**:

Instead of SWR, use **React Query** with existing patterns:

**File**: `src/hooks/use-datasets.ts`

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import type { Dataset, CreateDatasetInput } from '@/lib/types/lora-training';

export function useDatasets(filters?: { status?: string; search?: string }) {
  return useQuery({
    queryKey: ['datasets', filters],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (filters?.status) params.set('status', filters.status);
      if (filters?.search) params.set('search', filters.search);
      
      const response = await fetch(`/api/datasets?${params.toString()}`);
      if (!response.ok) throw new Error('Failed to fetch datasets');
      return response.json();
    },
    staleTime: 30 * 1000, // 30 seconds (from existing config)
  });
}

export function useDataset(id: string | null) {
  return useQuery({
    queryKey: ['datasets', id],
    queryFn: async () => {
      const response = await fetch(`/api/datasets/${id}`);
      if (!response.ok) throw new Error('Failed to fetch dataset');
      return response.json();
    },
    enabled: !!id,
  });
}

export function useCreateDataset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateDatasetInput) => {
      const response = await fetch('/api/datasets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Failed to create dataset');
      }
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['datasets'] });
      toast.success('Dataset created successfully');
    },
    onError: (error: Error) => {
      toast.error(`Error: ${error.message}`);
    },
  });
}

export function useConfirmDatasetUpload() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (datasetId: string) => {
      const response = await fetch(`/api/datasets/${datasetId}/confirm`, {
        method: 'POST',
      });
      if (!response.ok) throw new Error('Failed to confirm upload');
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['datasets'] });
      toast.success('Validation started');
    },
    onError: (error: Error) => {
      toast.error(`Error: ${error.message}`);
    },
  });
}

export function useDeleteDataset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const response = await fetch(`/api/datasets/${id}`, {
        method: 'DELETE',
      });
      if (!response.ok) throw new Error('Failed to delete dataset');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['datasets'] });
      toast.success('Dataset deleted');
    },
    onError: (error: Error) => {
      toast.error(`Error: ${error.message}`);
    },
  });
}
```

**Pattern Source**: Infrastructure Inventory Section 6 - State & Data Fetching

---

**Components (INTEGRATED)**:

Use exact patterns from Infrastructure Inventory Section 5:

**File**: `src/components/datasets/DatasetCard.tsx`

```typescript
'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Database } from 'lucide-react';
import type { Dataset } from '@/lib/types/lora-training';

interface DatasetCardProps {
  dataset: Dataset;
  onSelect?: (dataset: Dataset) => void;
  onDelete?: (id: string) => void;
}

export function DatasetCard({ dataset, onSelect, onDelete }: DatasetCardProps) {
  const statusColor = {
    uploading: 'bg-blue-500',
    validating: 'bg-yellow-500',
    ready: 'bg-green-500',
    error: 'bg-red-500',
  }[dataset.status];

  return (
    <Card className="hover:shadow-md transition-shadow cursor-pointer">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-2">
            <Database className="h-5 w-5 text-gray-500" />
            <div>
              <CardTitle className="text-lg">{dataset.name}</CardTitle>
              <CardDescription className="text-sm">
                {dataset.file_name}
              </CardDescription>
            </div>
          </div>
          <Badge className={statusColor}>{dataset.status}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        {dataset.training_ready && (
          <div className="mb-3 text-sm text-gray-600">
            <p>{dataset.total_training_pairs} training pairs</p>
            {dataset.total_tokens && (
              <p>{(dataset.total_tokens / 1000).toFixed(1)}K tokens</p>
            )}
          </div>
        )}
        <div className="flex gap-2">
          <Button 
            onClick={() => onSelect?.(dataset)}
            variant="outline"
            className="flex-1"
          >
            View Details
          </Button>
          {dataset.status === 'ready' && (
            <Button 
              onClick={() => onSelect?.(dataset)}
              className="flex-1"
            >
              Start Training
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
```

**Pattern Source**: Infrastructure Inventory Section 5 - Component Library

**Available Components**: All 47+ shadcn/ui components from `/components/ui/`

---

**Pages (INTEGRATED)**:

**File**: `src/app/(dashboard)/datasets/page.tsx`

```typescript
'use client';

import { useState } from 'react';
import { useDatasets, useDeleteDataset } from '@/hooks/use-datasets';
import { DatasetCard } from '@/components/datasets/DatasetCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus, Search } from 'lucide-react';
import Link from 'next/link';

export default function DatasetsPage() {
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  const { data, isLoading } = useDatasets({ 
    search: search || undefined,
    status: statusFilter || undefined,
  });
  const { mutate: deleteDataset } = useDeleteDataset();

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-full" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Skeleton key={i} className="h-48" />
          ))}
        </div>
      </div>
    );
  }

  const datasets = data?.data?.datasets || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Datasets</h1>
          <p className="text-gray-500">
            Manage your training datasets
          </p>
        </div>
        <Link href="/datasets/new">
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Upload Dataset
          </Button>
        </Link>
      </div>

      {/* Filters */}
      <div className="flex gap-4">
        <div className="flex-1">
          <Input
            placeholder="Search datasets..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            icon={<Search className="h-4 w-4" />}
          />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="All statuses" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="">All statuses</SelectItem>
            <SelectItem value="uploading">Uploading</SelectItem>
            <SelectItem value="validating">Validating</SelectItem>
            <SelectItem value="ready">Ready</SelectItem>
            <SelectItem value="error">Error</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Dataset Grid */}
      {datasets.length === 0 ? (
        <div className="text-center py-12">
          <Database className="h-12 w-12 mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold mb-2">No datasets yet</h3>
          <p className="text-gray-500 mb-4">
            Upload your first dataset to start training
          </p>
          <Link href="/datasets/new">
            <Button>Upload Dataset</Button>
          </Link>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {datasets.map((dataset: any) => (
            <DatasetCard
              key={dataset.id}
              dataset={dataset}
              onSelect={(d) => window.location.href = `/datasets/${d.id}`}
              onDelete={deleteDataset}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

**Pattern Source**: Infrastructure Inventory Section 5 - Component Library, Section 6 - Data Fetching

---

**Acceptance Criteria** (adjusted for infrastructure):

1. ✅ User can upload dataset files up to 500MB
2. ✅ Presigned upload URL generated via Supabase Storage
3. ✅ Dataset record created in database with status tracking
4. ✅ Edge Function validates dataset format automatically
5. ✅ Statistics calculated and stored (training pairs, tokens)
6. ✅ User notified when validation completes
7. ✅ Datasets page displays all user's datasets with filters

**Verification Steps**:

1. ✅ Storage: Upload file via presigned URL works
2. ✅ Database: Dataset record created correctly
3. ✅ Edge Function: Validation runs and updates status
4. ✅ API: List endpoint returns paginated results
5. ✅ Components: UI renders correctly with shadcn/ui
6. ✅ Integration: Complete upload flow works end-to-end

---

### Section Summary

**What Was Added**:
- API route: POST /api/datasets (create with upload URL)
- API route: GET /api/datasets (list with pagination)
- API route: POST /api/datasets/[id]/confirm (trigger validation)
- Edge Function: validate-datasets (background validation)
- React hooks: useDatasets, useCreateDataset, useConfirmDatasetUpload, useDeleteDataset
- Components: DatasetCard
- Page: /datasets (list view)

**What Was Reused**:
- Supabase Storage for file uploads
- Supabase Auth for user identification
- shadcn/ui components (Card, Badge, Button, etc.)
- React Query for data fetching
- Existing API response format

**Integration Points**:
- Uses requireAuth() from existing auth system
- Stores files in Supabase Storage (same as existing features)
- Uses same database client and query patterns
- Follows existing API and component conventions

---

