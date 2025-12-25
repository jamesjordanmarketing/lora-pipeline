# PIPELINE - Section E03: Training Configuration - Execution Prompts

**Product:** PIPELINE  
**Section:** 3 - Training Configuration  
**Generated:** 2025-12-25  
**Total Prompts:** 2  
**Estimated Total Time:** 12-16 hours  
**Source Section File:** 04f-pipeline-build-section-E03.md

---

## Section Overview

Enable users to configure training jobs with hyperparameter presets, advanced settings, and GPU selection.

**User Value**: Users can easily configure training parameters using presets or customize advanced settings with real-time cost estimates

**What This Section Adds**:
- Cost estimation API with GPU pricing and duration calculation
- Training job creation API with dataset validation
- Training job listing API with pagination and filtering
- Interactive configuration page with preset selection
- Real-time cost updates with debounced calculation
- GPU selection and hyperparameter customization

**What We're Reusing**:
- Supabase Auth (`requireAuth()`)
- Supabase Client for database operations
- shadcn/ui components (Slider, Select, Card, Button, Label)
- React Query for mutations and queries
- Existing API response patterns
- Database tables from Section E01
- Dataset validation from Section E02

---

## Prompt Sequence for This Section

This section has been divided into 2 progressive prompts:

1. **Prompt P01: API Layer - Cost Estimation & Job Management** (6-8h)
   - Features: FR-3.1 (Cost Estimation API), FR-3.2 (Job Creation & Listing APIs)
   - Key Deliverables: 
     - POST /api/jobs/estimate
     - POST /api/jobs
     - GET /api/jobs
     - React hooks: useEstimateCost, useCreateTrainingJob, useTrainingJobs, useTrainingJob

2. **Prompt P02: UI Layer - Training Configuration Page** (6-8h)
   - Features: FR-3.3 (Training Configuration Page)
   - Key Deliverables:
     - Training configuration page with preset selection
     - GPU configuration UI
     - Hyperparameter sliders
     - Real-time cost display
   - Dependencies: P01 (uses all APIs and hooks from P01)

---

## Integration Context

### Dependencies from Previous Sections

#### Section E01: Foundation & Authentication
**Database Tables:**
- `lora_training_jobs` - Store training job records
- `lora_datasets` - Validate dataset readiness
- `lora_notifications` - Send user notifications

**Types:**
- `TrainingJob` interface from `@/lib/types/lora-training.ts`
- `Dataset` interface from `@/lib/types/lora-training.ts`

**Authentication:**
- `requireAuth()` from `@/lib/supabase-server`
- `createServerSupabaseClient()` from `@/lib/supabase-server`

#### Section E02: Dataset Management
**Prerequisites:**
- At least one dataset with `status='ready'` and `training_ready=true`
- Dataset validation complete with statistics (total_training_pairs, total_tokens)

**API Integration:**
- Will validate datasets before creating training jobs
- Will display dataset statistics in cost calculation

### Provides for Next Sections

**For Section E04 (Training Job Monitoring):**
- Training jobs created with `status='queued'`
- Job records with complete configuration and cost estimates
- Hooks for fetching and polling job status
- API endpoints for job listing and details

**For Section E05 (Job Processing):**
- Job records ready for edge function processing
- GPU configuration and hyperparameters stored in JSONB
- Status progression structure (queued → initializing → running → completed)

---

## Dependency Flow (This Section)

```
E03-P01 (API Layer)
  ├─ POST /api/jobs/estimate (Cost calculation)
  ├─ POST /api/jobs (Job creation)
  ├─ GET /api/jobs (Job listing)
  └─ React hooks (useEstimateCost, useCreateTrainingJob, etc.)
       ↓
E03-P02 (UI Layer)
  └─ Training Configuration Page
       ├─ Uses: useEstimateCost hook (from P01)
       ├─ Uses: useCreateTrainingJob hook (from P01)
       └─ Calls: POST /api/jobs/estimate, POST /api/jobs (from P01)
```

---

# PROMPT 1: API Layer - Cost Estimation & Job Management

**Generated:** 2025-12-25  
**Section:** 3 - Training Configuration  
**Prompt:** 1 of 2 in this section  
**Estimated Time:** 6-8 hours  
**Prerequisites:** Section E01 (Database Schema), Section E02 (Dataset Management)

---

## 🎯 Mission Statement

Build the backend API layer for training job configuration. This includes cost estimation based on GPU configuration and dataset size, training job creation with validation, and job listing with filters. These APIs provide the foundation for the interactive training configuration UI in Prompt P02.

---

## 📦 Section Context

### This Section's Goal
Enable users to configure training jobs with hyperparameter presets, advanced settings, and GPU selection with real-time cost estimates.

### This Prompt's Scope
This is **Prompt 1 of 2** in Section E03. It implements:
- FR-3.1: Cost Estimation API
- FR-3.2: Training Job Creation API (POST and GET endpoints)
- React hooks for cost estimation and job management

---

## 🔗 Integration with Previous Work

### From Previous Sections

#### Section E01: Foundation & Authentication
**Database Tables We'll Use:**
- `lora_training_jobs` - Insert new job records with configuration
- `lora_datasets` - Validate dataset exists and is ready for training
- `lora_notifications` - Create notifications when jobs are queued

**Types We'll Import:**
- `TrainingJob` from `@/lib/types/lora-training.ts` - Job record structure
- `Dataset` from `@/lib/types/lora-training.ts` - Dataset record structure

**Authentication Pattern:**
- `requireAuth()` from `@/lib/supabase-server` - Protect API routes
- `createServerSupabaseClient()` from `@/lib/supabase-server` - Database queries

#### Section E02: Dataset Management
**Prerequisites:**
- Datasets with `status='ready'` and `training_ready=true`
- Dataset statistics: `total_training_pairs`, `total_tokens`

**Validation:**
- Check dataset belongs to user
- Verify dataset is ready before creating job
- Use dataset statistics for cost calculation

### From Previous Prompts (This Section)

This is the first prompt in Section E03. No previous prompts in this section.

---

## 🎯 Implementation Requirements

### Feature FR-3.1: Cost Estimation API

**Type:** API Endpoint  
**Strategy:** EXTENSION - building on existing Supabase patterns

#### Description
Calculate estimated training cost based on GPU configuration, hyperparameters, and dataset size. This endpoint performs real-time calculations of training duration, compute costs, and storage costs.

#### What Already Exists (Don't Rebuild)
- ✅ Supabase Auth system (`requireAuth()`)
- ✅ Supabase database client
- ✅ API route patterns and response formats
- ✅ Dataset records with statistics from Section E02

#### What We're Building (New in This Prompt)
- 🆕 `src/app/api/jobs/estimate/route.ts` - Cost estimation endpoint
- 🆕 Validation schema for estimate requests
- 🆕 GPU pricing and throughput configuration
- 🆕 Training duration calculation algorithm
- 🆕 Cost breakdown calculation

#### Implementation Details

**File:** `src/app/api/jobs/estimate/route.ts`

**Endpoint:** `POST /api/jobs/estimate`

**Request Schema:**
```typescript
{
  dataset_id: string (UUID),
  gpu_config: {
    type: 'A100-80GB' | 'A100-40GB' | 'H100' | 'V100-32GB',
    count: number (1-8)
  },
  hyperparameters: {
    batch_size: number (1-64),
    epochs: number (1-20),
    learning_rate: number (0.00001-0.001),
    rank: number (4-128)
  }
}
```

**Response Schema:**
```typescript
{
  success: true,
  data: {
    estimated_cost: number,
    cost_breakdown: {
      compute: number,
      storage: number
    },
    estimated_duration_hours: number,
    hourly_rate: number,
    training_details: {
      total_steps: number,
      steps_per_epoch: number,
      estimated_throughput_tokens_per_sec: number,
      dataset_name: string
    }
  }
}
```

**Implementation:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';
import { z } from 'zod';

// Validation schema
const EstimateRequestSchema = z.object({
  dataset_id: z.string().uuid(),
  gpu_config: z.object({
    type: z.enum(['A100-80GB', 'A100-40GB', 'H100', 'V100-32GB']),
    count: z.number().int().min(1).max(8),
  }),
  hyperparameters: z.object({
    batch_size: z.number().int().min(1).max(64),
    epochs: z.number().int().min(1).max(20),
    learning_rate: z.number().min(0.00001).max(0.001),
    rank: z.number().int().min(4).max(128),
  }),
});

/**
 * POST /api/jobs/estimate - Calculate cost estimate for training configuration
 * 
 * This endpoint calculates:
 * - Training duration based on dataset size and throughput
 * - Compute cost based on GPU pricing
 * - Storage cost for model artifacts
 * - Total estimated cost
 */
export async function POST(request: NextRequest) {
  try {
    // Authentication (existing pattern)
    const { user, response } = await requireAuth(request);
    if (response) return response;

    // Parse and validate request
    const body = await request.json();
    const validation = EstimateRequestSchema.safeParse(body);
    
    if (!validation.success) {
      return NextResponse.json(
        {
          error: 'Validation error',
          details: validation.error.flatten().fieldErrors,
        },
        { status: 400 }
      );
    }

    const { dataset_id, gpu_config, hyperparameters } = validation.data;

    const supabase = createServerSupabaseClient();

    // Fetch dataset statistics for accurate duration estimation
    const { data: dataset, error: datasetError } = await supabase
      .from('lora_datasets')
      .select('total_training_pairs, total_tokens, name')
      .eq('id', dataset_id)
      .eq('user_id', user.id)
      .single();

    if (datasetError || !dataset) {
      return NextResponse.json(
        { error: 'Dataset not found or access denied' },
        { status: 404 }
      );
    }

    // GPU pricing configuration (per hour, per GPU)
    const GPU_PRICING: Record<string, number> = {
      'A100-80GB': 3.50,
      'A100-40GB': 2.80,
      'H100': 4.20,
      'V100-32GB': 2.10,
    };

    // GPU throughput (tokens per second per GPU)
    const GPU_THROUGHPUT: Record<string, number> = {
      'A100-80GB': 1800,
      'A100-40GB': 1500,
      'H100': 2200,
      'V100-32GB': 1200,
    };

    const pricePerGpu = GPU_PRICING[gpu_config.type];
    const throughputPerGpu = GPU_THROUGHPUT[gpu_config.type];
    const hourlyRate = pricePerGpu * gpu_config.count;
    const totalThroughput = throughputPerGpu * gpu_config.count;

    // Calculate training duration
    const trainingPairs = dataset.total_training_pairs || 1000;
    const totalTokens = dataset.total_tokens || trainingPairs * 200;
    
    // Steps calculation
    const stepsPerEpoch = Math.ceil(trainingPairs / hyperparameters.batch_size);
    const totalSteps = stepsPerEpoch * hyperparameters.epochs;
    
    // Time calculation
    const avgTokensPerStep = (totalTokens / trainingPairs) * hyperparameters.batch_size;
    const secondsPerStep = avgTokensPerStep / totalThroughput;
    const totalTrainingSeconds = totalSteps * secondsPerStep;
    
    // Add overhead: initialization (10 min), validation between epochs (5 min/epoch), final save (5 min)
    const overheadSeconds = (10 * 60) + (hyperparameters.epochs * 5 * 60) + (5 * 60);
    const totalSeconds = totalTrainingSeconds + overheadSeconds;
    const estimatedHours = totalSeconds / 3600;

    // Cost calculation
    const computeCost = hourlyRate * estimatedHours;
    const storageCost = 0.50; // Model artifacts storage (~2-5GB in Supabase Storage)
    const totalCost = computeCost + storageCost;

    return NextResponse.json({
      success: true,
      data: {
        estimated_cost: parseFloat(totalCost.toFixed(2)),
        cost_breakdown: {
          compute: parseFloat(computeCost.toFixed(2)),
          storage: storageCost,
        },
        estimated_duration_hours: parseFloat(estimatedHours.toFixed(2)),
        hourly_rate: parseFloat(hourlyRate.toFixed(2)),
        training_details: {
          total_steps: totalSteps,
          steps_per_epoch: stepsPerEpoch,
          estimated_throughput_tokens_per_sec: totalThroughput,
          dataset_name: dataset.name,
        },
      },
    });
  } catch (error: any) {
    console.error('Cost estimation error:', error);
    return NextResponse.json(
      { error: 'Failed to estimate cost', details: error.message },
      { status: 500 }
    );
  }
}
```

**Key Points:**
- Uses: `requireAuth()` from existing auth system
- Queries: `lora_datasets` table from Section E01
- Returns: Detailed cost breakdown with duration estimate
- Error handling: Validates dataset exists and belongs to user

---

### Feature FR-3.2: Training Job Creation API

**Type:** API Endpoint  
**Strategy:** EXTENSION - building on existing Supabase patterns

#### Description
Create training job records with validated configuration and queue for processing. Includes both job creation (POST) and job listing (GET) endpoints.

#### What Already Exists (Don't Rebuild)
- ✅ Supabase Auth system
- ✅ Database client and query patterns
- ✅ `lora_training_jobs` table from Section E01
- ✅ Dataset validation from Section E02

#### What We're Building (New in This Prompt)
- 🆕 `src/app/api/jobs/route.ts` - Job creation and listing endpoint
- 🆕 Job creation with dataset validation
- 🆕 Job listing with pagination and filtering
- 🆕 Notification creation on job queue
- 🆕 Total steps calculation for progress tracking

#### Implementation Details

**File:** `src/app/api/jobs/route.ts`

**Endpoint 1:** `POST /api/jobs` - Create new training job

**Request Schema:**
```typescript
{
  dataset_id: string (UUID),
  preset_id: 'fast' | 'balanced' | 'quality' | 'custom',
  gpu_config: {
    type: string,
    count: number (1-8)
  },
  hyperparameters: {
    learning_rate: number,
    batch_size: number,
    epochs: number,
    rank: number,
    alpha?: number,
    dropout?: number
  },
  estimated_cost: number
}
```

**Response Schema:**
```typescript
{
  success: true,
  data: TrainingJob // Complete job record
}
```

**Endpoint 2:** `GET /api/jobs` - List user's training jobs

**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 10)
- `status` (optional filter)

**Response Schema:**
```typescript
{
  success: true,
  data: {
    jobs: TrainingJob[],
    pagination: {
      page: number,
      limit: number,
      total: number,
      totalPages: number
    }
  }
}
```

**Implementation:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';
import { z } from 'zod';

// Create job validation schema
const CreateJobSchema = z.object({
  dataset_id: z.string().uuid(),
  preset_id: z.enum(['fast', 'balanced', 'quality', 'custom']),
  gpu_config: z.object({
    type: z.string(),
    count: z.number().int().min(1).max(8),
  }),
  hyperparameters: z.object({
    learning_rate: z.number(),
    batch_size: z.number().int(),
    epochs: z.number().int(),
    rank: z.number().int(),
    alpha: z.number().optional(),
    dropout: z.number().optional(),
  }),
  estimated_cost: z.number(),
});

/**
 * POST /api/jobs - Create new training job
 * 
 * Flow:
 * 1. Validate dataset is ready
 * 2. Calculate total steps for progress tracking
 * 3. Create job record with status='queued'
 * 4. Edge Function (Section 4) will pick up and process
 */
export async function POST(request: NextRequest) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const body = await request.json();
    const validation = CreateJobSchema.safeParse(body);
    
    if (!validation.success) {
      return NextResponse.json(
        {
          error: 'Validation error',
          details: validation.error.flatten().fieldErrors,
        },
        { status: 400 }
      );
    }

    const { dataset_id, preset_id, gpu_config, hyperparameters, estimated_cost } = validation.data;

    const supabase = createServerSupabaseClient();

    // Verify dataset exists, belongs to user, and is ready for training
    const { data: dataset, error: datasetError } = await supabase
      .from('lora_datasets')
      .select('id, name, training_ready, status, total_training_pairs')
      .eq('id', dataset_id)
      .eq('user_id', user.id)
      .single();

    if (datasetError || !dataset) {
      return NextResponse.json(
        { error: 'Dataset not found or access denied' },
        { status: 404 }
      );
    }

    if (!dataset.training_ready || dataset.status !== 'ready') {
      return NextResponse.json(
        { 
          error: 'Dataset not ready for training',
          details: `Dataset must have status='ready' and training_ready=true. Current: status='${dataset.status}', training_ready=${dataset.training_ready}`
        },
        { status: 400 }
      );
    }

    // Calculate total steps for accurate progress tracking
    const stepsPerEpoch = Math.ceil((dataset.total_training_pairs || 1000) / hyperparameters.batch_size);
    const totalSteps = stepsPerEpoch * hyperparameters.epochs;

    // Create training job record
    const { data: job, error: jobError } = await supabase
      .from('lora_training_jobs')
      .insert({
        user_id: user.id,
        dataset_id,
        preset_id,
        status: 'queued',
        current_stage: 'queued',
        progress: 0,
        current_epoch: 0,
        total_epochs: hyperparameters.epochs,
        current_step: 0,
        total_steps: totalSteps,
        gpu_config,
        hyperparameters,
        estimated_total_cost: estimated_cost,
        current_cost: 0,
        current_metrics: {},
        queued_at: new Date().toISOString(),
      })
      .select()
      .single();

    if (jobError) {
      console.error('Job creation error:', jobError);
      return NextResponse.json(
        { error: 'Failed to create training job', details: jobError.message },
        { status: 500 }
      );
    }

    // Create notification for user
    await supabase.from('lora_notifications').insert({
      user_id: user.id,
      type: 'job_queued',
      title: 'Training Job Queued',
      message: `Your training job for "${dataset.name}" has been queued and will start shortly`,
      priority: 'low',
      action_url: `/training/jobs/${job.id}`,
      metadata: { job_id: job.id, dataset_name: dataset.name },
    });

    // Note: Edge Function (Section 4) will poll for queued jobs and process them
    // Status progression: queued → initializing → running → completed/failed

    return NextResponse.json({
      success: true,
      data: job,
    }, { status: 201 });
  } catch (error: any) {
    console.error('Job creation error:', error);
    return NextResponse.json(
      { error: 'Failed to create job', details: error.message },
      { status: 500 }
    );
  }
}

/**
 * GET /api/jobs - List user's training jobs with pagination and filtering
 */
export async function GET(request: NextRequest) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = createServerSupabaseClient();
    const { searchParams } = new URL(request.url);
    
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '10');
    const status = searchParams.get('status');
    const offset = (page - 1) * limit;

    // Build query with dataset join
    let query = supabase
      .from('lora_training_jobs')
      .select(`
        *,
        dataset:lora_datasets(name, format, total_training_pairs)
      `, { count: 'exact' })
      .eq('user_id', user.id)
      .order('created_at', { ascending: false })
      .range(offset, offset + limit - 1);

    // Apply optional status filter
    if (status) {
      query = query.eq('status', status);
    }

    const { data: jobs, error, count } = await query;

    if (error) {
      return NextResponse.json(
        { error: 'Failed to fetch jobs', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      data: {
        jobs: jobs || [],
        pagination: {
          page,
          limit,
          total: count || 0,
          totalPages: Math.ceil((count || 0) / limit),
        },
      },
    });
  } catch (error: any) {
    console.error('Jobs fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch jobs', details: error.message },
      { status: 500 }
    );
  }
}
```

**Key Points:**
- Uses: Existing auth patterns from Section E01
- Validates: Dataset readiness from Section E02
- Creates: Job record with complete configuration
- Notifies: User via `lora_notifications` table
- Prepares: Job for edge function processing (Section 4)

---

### React Hooks for API Integration

**File:** `src/hooks/useTrainingConfig.ts`

```typescript
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';

/**
 * Hook for cost estimation with debouncing
 */
export function useEstimateCost() {
  return useMutation({
    mutationFn: async (config: {
      dataset_id: string;
      gpu_config: { type: string; count: number };
      hyperparameters: any;
    }) => {
      const response = await fetch('/api/jobs/estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.details || error.error || 'Cost estimation failed');
      }
      
      return response.json();
    },
  });
}

/**
 * Hook for creating training jobs
 */
export function useCreateTrainingJob() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  return useMutation({
    mutationFn: async (config: any) => {
      const response = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.details || error.error || 'Job creation failed');
      }
      
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['training-jobs'] });
      toast({
        title: 'Success',
        description: 'Training job created and queued for processing',
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Error',
        description: error.message,
        variant: 'destructive',
      });
    },
  });
}

/**
 * Hook for fetching training jobs with filters
 */
export function useTrainingJobs(params?: { 
  status?: string; 
  page?: number; 
  limit?: number;
}) {
  return useQuery({
    queryKey: ['training-jobs', params],
    queryFn: async () => {
      const searchParams = new URLSearchParams();
      if (params?.status) searchParams.set('status', params.status);
      if (params?.page) searchParams.set('page', params.page.toString());
      if (params?.limit) searchParams.set('limit', params.limit.toString());

      const response = await fetch(`/api/jobs?${searchParams}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch training jobs');
      }
      
      return response.json();
    },
  });
}

/**
 * Hook for fetching single job details
 */
export function useTrainingJob(jobId: string | null) {
  return useQuery({
    queryKey: ['training-job', jobId],
    queryFn: async () => {
      const response = await fetch(`/api/jobs/${jobId}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch job details');
      }
      
      return response.json();
    },
    enabled: !!jobId,
    refetchInterval: (data) => {
      // Poll every 5 seconds if job is active
      const status = data?.data?.status;
      return status === 'running' || status === 'queued' || status === 'initializing' 
        ? 5000 
        : false;
    },
  });
}
```

**Key Points:**
- Uses: React Query from existing infrastructure
- Pattern: Mutations for POST, queries for GET
- Integration: Toast notifications for user feedback
- Polling: Auto-refresh for active jobs (used in Section E04)

---

## ✅ Acceptance Criteria

### Functional Requirements

- [ ] Cost estimation API calculates duration based on dataset size
- [ ] Cost estimation API calculates compute cost based on GPU pricing
- [ ] Cost estimation API returns detailed breakdown with training details
- [ ] Job creation validates dataset exists and belongs to user
- [ ] Job creation validates dataset has status='ready' and training_ready=true
- [ ] Job creation calculates total steps for progress tracking
- [ ] Job creation inserts record with status='queued'
- [ ] Job creation creates notification for user
- [ ] Job listing returns paginated results with dataset join
- [ ] Job listing supports status filtering
- [ ] All endpoints use existing auth patterns

### Technical Requirements

- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Follows existing API patterns (response format: `{ success, data }` or `{ error, details }`)
- [ ] Uses existing Supabase client patterns
- [ ] Validation uses Zod schemas
- [ ] All imports resolve correctly

### Integration Requirements

- [ ] Successfully imports `requireAuth()` from `@/lib/supabase-server`
- [ ] Successfully queries `lora_datasets` table from Section E01
- [ ] Successfully inserts into `lora_training_jobs` table from Section E01
- [ ] Successfully inserts into `lora_notifications` table from Section E01
- [ ] React hooks use existing React Query patterns
- [ ] Toast notifications work with existing UI components

---

## 🧪 Testing & Validation

### Manual Testing Steps

1. **Cost Estimation API Testing**
   ```bash
   # Test with valid dataset
   curl -X POST http://localhost:3000/api/jobs/estimate \
     -H "Content-Type: application/json" \
     -d '{
       "dataset_id": "[valid-dataset-uuid]",
       "gpu_config": { "type": "A100-80GB", "count": 2 },
       "hyperparameters": {
         "batch_size": 4,
         "epochs": 3,
         "learning_rate": 0.0001,
         "rank": 16
       }
     }'
   
   # Expected: 200 OK with cost breakdown
   # Verify: estimated_cost > 0, duration calculated
   ```

2. **Job Creation Testing**
   ```bash
   # Test with ready dataset
   curl -X POST http://localhost:3000/api/jobs \
     -H "Content-Type: application/json" \
     -d '{
       "dataset_id": "[ready-dataset-uuid]",
       "preset_id": "balanced",
       "gpu_config": { "type": "A100-80GB", "count": 2 },
       "hyperparameters": {
         "learning_rate": 0.0001,
         "batch_size": 4,
         "epochs": 3,
         "rank": 16
       },
       "estimated_cost": 25.50
     }'
   
   # Expected: 201 Created with job record
   # Verify: status='queued', total_steps calculated
   ```

3. **Job Listing Testing**
   ```bash
   # Test pagination
   curl http://localhost:3000/api/jobs?page=1&limit=10
   
   # Test filtering
   curl http://localhost:3000/api/jobs?status=queued
   
   # Expected: 200 OK with paginated results
   ```

4. **Database Verification**
   ```sql
   -- Verify job created
   SELECT * FROM lora_training_jobs 
   WHERE status = 'queued' 
   ORDER BY created_at DESC 
   LIMIT 1;
   
   -- Verify notification created
   SELECT * FROM lora_notifications 
   WHERE type = 'job_queued' 
   ORDER BY created_at DESC 
   LIMIT 1;
   ```

5. **React Hooks Testing**
   - Test `useEstimateCost()` in browser console
   - Test `useCreateTrainingJob()` mutation
   - Verify `useTrainingJobs()` returns data
   - Check toast notifications appear

### Expected Outputs

After completing this prompt, you should have:
- [ ] Cost estimation endpoint returning accurate calculations
- [ ] Job creation endpoint creating records with proper validation
- [ ] Job listing endpoint with pagination working
- [ ] All React hooks functional
- [ ] No TypeScript or linter errors
- [ ] All manual tests passing

---

## 📦 Deliverables Checklist

### New Files Created

- [ ] `src/app/api/jobs/estimate/route.ts` - Cost estimation endpoint
- [ ] `src/app/api/jobs/route.ts` - Job creation and listing endpoints
- [ ] `src/hooks/useTrainingConfig.ts` - React hooks for API integration

### Database Changes

- [ ] No schema changes (using existing tables from Section E01)
- [ ] Inserts into `lora_training_jobs` table working
- [ ] Inserts into `lora_notifications` table working
- [ ] Queries to `lora_datasets` table working

### API Endpoints

- [ ] `POST /api/jobs/estimate` - Cost estimation
- [ ] `POST /api/jobs` - Job creation
- [ ] `GET /api/jobs` - Job listing with pagination

### React Hooks

- [ ] `useEstimateCost()` - Cost estimation mutation
- [ ] `useCreateTrainingJob()` - Job creation mutation
- [ ] `useTrainingJobs()` - Job listing query
- [ ] `useTrainingJob()` - Single job query with polling

---

## 🔜 What's Next

### For Next Prompt in This Section

**Next:** Section E03 - Prompt P02: UI Layer - Training Configuration Page

This prompt's deliverables will be used by the next prompt for:
- `useEstimateCost()` hook - Called on debounced config changes
- `useCreateTrainingJob()` hook - Called on form submission
- `POST /api/jobs/estimate` - Real-time cost calculation
- `POST /api/jobs` - Job creation and navigation

### For Next Section

**Next Section:** E04: Training Job Monitoring

The next section will build upon:
- Job records with `status='queued'` created by this section
- `useTrainingJob()` hook with polling for real-time updates
- `GET /api/jobs` endpoint for job listing

---

## ⚠️ Important Reminders

1. **Follow the Spec Exactly:** All code provided in this prompt comes from the integrated specification. Implement it as written.

2. **Reuse Existing Infrastructure:** Don't recreate what already exists. Import and use:
   - Supabase Auth via `requireAuth()` from `@/lib/supabase-server`
   - Supabase Client via `createServerSupabaseClient()`
   - React Query for mutations and queries
   - Toast notifications from existing UI

3. **Integration Points:** When importing from previous work, add comments:
   ```typescript
   // From Section E01 - database schema
   import { TrainingJob } from '@/lib/types/lora-training';
   ```

4. **Pattern Consistency:** Match existing patterns:
   - API responses: `{ success: true, data }` or `{ error, details }`
   - Error handling: Try-catch with detailed error messages
   - Validation: Zod schemas with proper error formatting

5. **Don't Skip Steps:** Implement all features listed in this prompt before moving to the next prompt.

---

## 📚 Reference Materials

### Files from Previous Work

#### Section E01: Foundation & Authentication
- `supabase/migrations/20241223_create_lora_training_tables.sql` - Database schema
- `src/lib/types/lora-training.ts` - TypeScript types
- `src/lib/supabase-server.ts` - Auth and database client utilities

#### Section E02: Dataset Management
- `src/app/api/datasets/route.ts` - Dataset API patterns
- `src/hooks/use-datasets.ts` - React Query hook patterns

### Infrastructure Patterns

- **Authentication:** `requireAuth()` pattern from existing codebase
- **Database:** Supabase client pattern with RLS policies
- **API:** Next.js App Router API route pattern
- **Data Fetching:** React Query mutation and query patterns
- **Validation:** Zod schema validation pattern

---

**Ready to implement Section E03, Prompt P01!**

---

# PROMPT 2: UI Layer - Training Configuration Page

**Generated:** 2025-12-25  
**Section:** 3 - Training Configuration  
**Prompt:** 2 of 2 in this section  
**Estimated Time:** 6-8 hours  
**Prerequisites:** Section E03 Prompt P01 (API Layer)

---

## 🎯 Mission Statement

Build the interactive training configuration page with preset selection, GPU configuration, hyperparameter customization, and real-time cost estimation. This page provides users with an intuitive interface to configure training jobs with instant feedback on costs and training duration.

---

## 📦 Section Context

### This Section's Goal
Enable users to configure training jobs with hyperparameter presets, advanced settings, and GPU selection with real-time cost estimates.

### This Prompt's Scope
This is **Prompt 2 of 2** in Section E03. It implements:
- FR-3.3: Training Configuration Page
  - Preset selection (Fast, Balanced, Quality)
  - GPU type and count configuration
  - Hyperparameter sliders
  - Real-time cost estimation
  - Form submission and navigation

---

## 🔗 Integration with Previous Work

### From Previous Sections

#### Section E01: Foundation & Authentication
**Types We'll Use:**
- `TrainingJob` from `@/lib/types/lora-training.ts`
- `Dataset` from `@/lib/types/lora-training.ts`

**Components Available:**
- All 47+ shadcn/ui components from `@/components/ui/*`
- Specifically: Card, Button, Label, Slider, Select, Alert

#### Section E02: Dataset Management
**Prerequisites:**
- User must select a dataset from `/datasets` page
- Dataset ID passed via query parameter: `?datasetId=[uuid]`

### From Previous Prompts (This Section)

#### Section E03 - Prompt P01: API Layer
**Hooks We'll Import:**
- `useEstimateCost()` from `@/hooks/useTrainingConfig.ts` - For debounced cost calculation
- `useCreateTrainingJob()` from `@/hooks/useTrainingConfig.ts` - For job creation
- `useDebounce()` from `@/hooks/useDebounce` (existing hook) - For performance optimization

**APIs We'll Call:**
- `POST /api/jobs/estimate` - Via `useEstimateCost()` hook
- `POST /api/jobs` - Via `useCreateTrainingJob()` hook

**Data Flow:**
1. User changes configuration → debounced
2. Debounced config triggers `useEstimateCost()`
3. Cost estimate updates in real-time
4. User clicks "Start Training" → `useCreateTrainingJob()`
5. Navigate to `/training/jobs/[id]` on success

---

## 🎯 Implementation Requirements

### Feature FR-3.3: Training Configuration Page

**Type:** UI Page  
**Strategy:** EXTENSION - using existing shadcn/ui components and React Query

#### Description
Interactive form for configuring training jobs with preset selection, custom hyperparameters, GPU configuration, and real-time cost estimation with debouncing.

#### What Already Exists (Don't Rebuild)
- ✅ shadcn/ui components (Card, Button, Slider, Select, etc.)
- ✅ React Query hooks from Prompt P01
- ✅ `useDebounce` hook from existing codebase
- ✅ Toast notification system
- ✅ Dashboard layout from existing app

#### What We're Building (New in This Prompt)
- 🆕 `src/app/(dashboard)/training/configure/page.tsx` - Main configuration page
- 🆕 Preset selection UI (Fast, Balanced, Quality)
- 🆕 GPU configuration UI (type selector and count slider)
- 🆕 Hyperparameter sliders (learning rate, batch size, epochs, rank)
- 🆕 Real-time cost display with breakdown
- 🆕 Form submission and error handling

#### Implementation Details

**File:** `src/app/(dashboard)/training/configure/page.tsx`

**Route:** `/training/configure?datasetId=[uuid]`

**Component Structure:**
- Header with back navigation
- Preset selection cards (3 presets)
- GPU configuration section
- Hyperparameters section (4 sliders)
- Cost estimate display (with loading state)
- Action buttons (Cancel, Start Training)

**Implementation:**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { useEstimateCost, useCreateTrainingJob } from '@/hooks/useTrainingConfig';
import { useDebounce } from '@/hooks/useDebounce';
import { Loader2, Info, Zap, Target, Crown, ArrowLeft } from 'lucide-react';

// Preset configurations
const PRESETS = {
  fast: {
    name: 'Fast',
    icon: Zap,
    description: 'Quick training for testing and iteration',
    details: 'Optimized for speed, suitable for testing',
    learning_rate: 0.0001,
    batch_size: 8,
    epochs: 1,
    rank: 8,
    alpha: 16,
    dropout: 0.05,
  },
  balanced: {
    name: 'Balanced',
    icon: Target,
    description: 'Recommended balance of quality and cost',
    details: 'Best for most use cases',
    learning_rate: 0.00005,
    batch_size: 4,
    epochs: 3,
    rank: 16,
    alpha: 32,
    dropout: 0.1,
  },
  quality: {
    name: 'Quality',
    icon: Crown,
    description: 'Maximum quality for production models',
    details: 'Slower and more expensive, but best results',
    learning_rate: 0.00003,
    batch_size: 2,
    epochs: 5,
    rank: 32,
    alpha: 64,
    dropout: 0.1,
  },
};

export default function TrainingConfigurePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const datasetId = searchParams.get('datasetId');

  const [selectedPreset, setSelectedPreset] = useState<keyof typeof PRESETS>('balanced');
  const [hyperparameters, setHyperparameters] = useState(PRESETS.balanced);
  const [gpuType, setGpuType] = useState('A100-80GB');
  const [gpuCount, setGpuCount] = useState(2);

  const estimateCost = useEstimateCost();
  const createJob = useCreateTrainingJob();

  // Debounce configuration changes to avoid excessive API calls
  const debouncedConfig = useDebounce(
    { 
      dataset_id: datasetId, 
      gpu_config: { type: gpuType, count: gpuCount }, 
      hyperparameters 
    },
    500
  );

  // Auto-estimate cost when configuration changes
  useEffect(() => {
    if (datasetId) {
      estimateCost.mutate(debouncedConfig);
    }
  }, [debouncedConfig, datasetId]);

  const handlePresetChange = (preset: keyof typeof PRESETS) => {
    setSelectedPreset(preset);
    setHyperparameters(PRESETS[preset]);
  };

  const handleSubmit = async () => {
    if (!datasetId) return;

    const result = await createJob.mutateAsync({
      dataset_id: datasetId,
      preset_id: selectedPreset,
      gpu_config: { type: gpuType, count: gpuCount },
      hyperparameters,
      estimated_cost: estimateCost.data?.data.estimated_cost || 0,
    });

    if (result.success) {
      router.push(`/training/jobs/${result.data.id}`);
    }
  };

  const costData = estimateCost.data;
  const isLoading = createJob.isPending;

  // Handle missing dataset ID
  if (!datasetId) {
    return (
      <div className="container mx-auto py-8 max-w-4xl">
        <Card>
          <CardContent className="pt-6">
            <Alert>
              <Info className="h-4 w-4" />
              <AlertDescription>
                No dataset selected. Please select a dataset from the datasets page.
              </AlertDescription>
            </Alert>
            <div className="flex justify-center mt-4">
              <Button onClick={() => router.push('/datasets')}>
                Go to Datasets
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-8 space-y-6 max-w-4xl">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button 
          variant="ghost" 
          size="icon"
          onClick={() => router.back()}
        >
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div>
          <h1 className="text-3xl font-bold">Configure Training Job</h1>
          <p className="text-gray-600 mt-1">
            Select a preset or customize hyperparameters for your training
          </p>
        </div>
      </div>

      {/* Preset Selection */}
      <Card>
        <CardHeader>
          <CardTitle>Training Preset</CardTitle>
          <CardDescription>
            Choose a pre-configured profile optimized for different use cases
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(PRESETS).map(([key, preset]) => {
              const Icon = preset.icon;
              return (
                <button
                  key={key}
                  onClick={() => handlePresetChange(key as keyof typeof PRESETS)}
                  className={`p-4 border-2 rounded-lg text-left transition-all ${
                    selectedPreset === key
                      ? 'border-primary bg-primary/5 shadow-md'
                      : 'border-gray-200 hover:border-gray-300 hover:shadow'
                  }`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Icon className={`h-5 w-5 ${
                      selectedPreset === key ? 'text-primary' : 'text-gray-500'
                    }`} />
                    <h3 className="font-semibold">{preset.name}</h3>
                  </div>
                  <p className="text-sm text-gray-600 mb-3">{preset.description}</p>
                  <div className="text-xs text-gray-500 space-y-1">
                    <div>Learning Rate: {preset.learning_rate}</div>
                    <div>Batch: {preset.batch_size} | Epochs: {preset.epochs}</div>
                    <div>LoRA Rank: {preset.rank}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* GPU Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>GPU Configuration</CardTitle>
          <CardDescription>
            Select GPU type and number of GPUs for training
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label>GPU Type</Label>
            <Select value={gpuType} onValueChange={setGpuType}>
              <SelectTrigger className="mt-2">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="A100-80GB">
                  <div className="flex flex-col">
                    <span className="font-medium">NVIDIA A100 80GB</span>
                    <span className="text-xs text-gray-500">$3.50/hr • Best overall performance</span>
                  </div>
                </SelectItem>
                <SelectItem value="A100-40GB">
                  <div className="flex flex-col">
                    <span className="font-medium">NVIDIA A100 40GB</span>
                    <span className="text-xs text-gray-500">$2.80/hr • Good for smaller models</span>
                  </div>
                </SelectItem>
                <SelectItem value="H100">
                  <div className="flex flex-col">
                    <span className="font-medium">NVIDIA H100</span>
                    <span className="text-xs text-gray-500">$4.20/hr • Fastest available</span>
                  </div>
                </SelectItem>
                <SelectItem value="V100-32GB">
                  <div className="flex flex-col">
                    <span className="font-medium">NVIDIA V100 32GB</span>
                    <span className="text-xs text-gray-500">$2.10/hr • Budget option</span>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <Label>Number of GPUs</Label>
              <span className="text-sm font-medium">{gpuCount}</span>
            </div>
            <Slider
              value={[gpuCount]}
              onValueChange={(value) => setGpuCount(value[0])}
              min={1}
              max={8}
              step={1}
              className="mt-2"
            />
            <p className="text-sm text-gray-600 mt-2">
              More GPUs = faster training via data parallelism. 
              {gpuCount > 1 && ` Training will be ${gpuCount}x faster (approximately).`}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Hyperparameters */}
      <Card>
        <CardHeader>
          <CardTitle>Hyperparameters</CardTitle>
          <CardDescription>
            Fine-tune training parameters (based on {PRESETS[selectedPreset].name} preset)
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Learning Rate */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label>Learning Rate</Label>
              <span className="text-sm font-medium">{hyperparameters.learning_rate.toFixed(5)}</span>
            </div>
            <Slider
              value={[hyperparameters.learning_rate * 100000]}
              onValueChange={(value) =>
                setHyperparameters({ ...hyperparameters, learning_rate: value[0] / 100000 })
              }
              min={1}
              max={20}
              step={0.1}
              className="mt-2"
            />
            <p className="text-sm text-gray-600 mt-1">
              Lower = more stable training, Higher = faster convergence (but risky)
            </p>
          </div>

          {/* Batch Size */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label>Batch Size</Label>
              <span className="text-sm font-medium">{hyperparameters.batch_size}</span>
            </div>
            <Slider
              value={[hyperparameters.batch_size]}
              onValueChange={(value) =>
                setHyperparameters({ ...hyperparameters, batch_size: value[0] })
              }
              min={1}
              max={16}
              step={1}
              className="mt-2"
            />
            <p className="text-sm text-gray-600 mt-1">
              Larger batch = faster training but requires more memory
            </p>
          </div>

          {/* Epochs */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label>Training Epochs</Label>
              <span className="text-sm font-medium">{hyperparameters.epochs}</span>
            </div>
            <Slider
              value={[hyperparameters.epochs]}
              onValueChange={(value) =>
                setHyperparameters({ ...hyperparameters, epochs: value[0] })
              }
              min={1}
              max={10}
              step={1}
              className="mt-2"
            />
            <p className="text-sm text-gray-600 mt-1">
              More epochs = better learning, but with diminishing returns
            </p>
          </div>

          {/* LoRA Rank */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <Label>LoRA Rank</Label>
              <span className="text-sm font-medium">{hyperparameters.rank}</span>
            </div>
            <Slider
              value={[hyperparameters.rank]}
              onValueChange={(value) =>
                setHyperparameters({ ...hyperparameters, rank: value[0] })
              }
              min={4}
              max={64}
              step={4}
              className="mt-2"
            />
            <p className="text-sm text-gray-600 mt-1">
              Higher rank = more expressive adapter, but larger model size
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Cost Estimate */}
      {estimateCost.isPending && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-center py-4">
              <Loader2 className="h-6 w-6 animate-spin mr-2 text-primary" />
              <span className="text-gray-600">Calculating cost estimate...</span>
            </div>
          </CardContent>
        </Card>
      )}

      {costData && !estimateCost.isPending && (
        <Card className="border-primary/20">
          <CardHeader>
            <CardTitle>Cost Estimate</CardTitle>
            <CardDescription>
              Estimated cost for this training configuration
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex justify-between text-gray-700">
                <span>Compute Cost:</span>
                <span className="font-semibold">
                  ${costData.data.cost_breakdown.compute.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between text-gray-700">
                <span>Storage Cost:</span>
                <span className="font-semibold">
                  ${costData.data.cost_breakdown.storage.toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between text-xl font-bold border-t pt-3 mt-3">
                <span>Total Estimated Cost:</span>
                <span className="text-primary">
                  ${costData.data.estimated_cost.toFixed(2)}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-2 text-sm text-gray-600">
                <div>
                  <div className="font-medium">Duration</div>
                  <div>{costData.data.estimated_duration_hours.toFixed(1)} hours</div>
                </div>
                <div>
                  <div className="font-medium">Hourly Rate</div>
                  <div>${costData.data.hourly_rate.toFixed(2)}/hr</div>
                </div>
                <div>
                  <div className="font-medium">Total Steps</div>
                  <div>{costData.data.training_details.total_steps.toLocaleString()}</div>
                </div>
                <div>
                  <div className="font-medium">Throughput</div>
                  <div>{costData.data.training_details.estimated_throughput_tokens_per_sec.toLocaleString()} tok/s</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4 sticky bottom-0 bg-white py-4 border-t">
        <Button 
          variant="outline" 
          onClick={() => router.back()}
          disabled={isLoading}
          className="flex-1"
        >
          Cancel
        </Button>
        <Button 
          onClick={handleSubmit} 
          disabled={isLoading || !datasetId || estimateCost.isPending}
          className="flex-1"
        >
          {isLoading && <Loader2 className="h-4 w-4 animate-spin mr-2" />}
          {isLoading ? 'Creating Job...' : 'Start Training'}
        </Button>
      </div>
    </div>
  );
}
```

**Key Points:**
- Imports: React Query hooks from Prompt P01
- Uses: `useDebounce` hook for performance (500ms debounce)
- Pattern: Auto-triggers cost estimation on config changes
- Navigation: Redirects to job monitor page on success
- Error handling: Shows alerts and toast notifications
- Loading states: Disabled buttons and spinners during operations

---

## ✅ Acceptance Criteria

### Functional Requirements

- [ ] User can select from 3 preset configurations (Fast, Balanced, Quality)
- [ ] Preset selection updates all hyperparameters immediately
- [ ] User can select GPU type from dropdown (4 options)
- [ ] User can adjust GPU count with slider (1-8)
- [ ] User can adjust learning rate with slider
- [ ] User can adjust batch size with slider
- [ ] User can adjust epochs with slider
- [ ] User can adjust LoRA rank with slider
- [ ] Cost estimate updates automatically when configuration changes (debounced 500ms)
- [ ] Cost estimate shows compute cost, storage cost, and total
- [ ] Cost estimate shows duration, hourly rate, steps, and throughput
- [ ] Loading spinner shown during cost estimation
- [ ] Submit button creates job and navigates to job monitor
- [ ] Cancel button navigates back
- [ ] Missing dataset ID shows alert with link to datasets page

### Technical Requirements

- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Uses existing shadcn/ui components correctly
- [ ] Uses React Query hooks from Prompt P01
- [ ] Follows existing page layout patterns
- [ ] All imports resolve correctly
- [ ] Component renders without errors

### Integration Requirements

- [ ] Successfully imports hooks from `@/hooks/useTrainingConfig.ts`
- [ ] Successfully uses `useDebounce` from `@/hooks/useDebounce`
- [ ] Cost estimation updates on configuration changes
- [ ] Job creation navigates to correct route
- [ ] Toast notifications work correctly
- [ ] Back navigation works correctly

---

## 🧪 Testing & Validation

### Manual Testing Steps

1. **Navigation to Page**
   - Navigate to: `/training/configure?datasetId=[valid-uuid]`
   - Expected: Page loads with default "Balanced" preset selected
   - Verify: Cost estimate loads automatically

2. **Preset Selection**
   - Click "Fast" preset
   - Expected: All hyperparameters update instantly
   - Verify: Cost recalculates after 500ms debounce

3. **GPU Configuration**
   - Change GPU type to "H100"
   - Expected: Cost updates (higher hourly rate)
   - Move GPU count slider to 4
   - Expected: Cost increases, duration decreases

4. **Hyperparameter Adjustments**
   - Adjust learning rate slider
   - Adjust batch size slider
   - Adjust epochs slider
   - Adjust LoRA rank slider
   - Expected: Cost updates after each change (debounced)

5. **Cost Estimate Display**
   - Verify compute cost displayed
   - Verify storage cost displayed
   - Verify total cost displayed
   - Verify duration, hourly rate, steps, throughput displayed

6. **Form Submission**
   - Click "Start Training"
   - Expected: Loading spinner shown, button disabled
   - Expected: Job created in database
   - Expected: Navigation to `/training/jobs/[id]`
   - Expected: Toast notification shown

7. **Error Handling**
   - Navigate to `/training/configure` (no datasetId)
   - Expected: Alert shown with link to datasets page
   - Try creating job with invalid dataset
   - Expected: Error toast shown

8. **Cancel Functionality**
   - Click "Cancel" button
   - Expected: Navigate back to previous page

### Expected Outputs

After completing this prompt, you should have:
- [ ] Training configuration page fully functional
- [ ] All presets working correctly
- [ ] All sliders updating state correctly
- [ ] Cost estimation updating in real-time (debounced)
- [ ] Job creation and navigation working
- [ ] No TypeScript or linter errors
- [ ] All manual tests passing

---

## 📦 Deliverables Checklist

### New Files Created

- [ ] `src/app/(dashboard)/training/configure/page.tsx` - Training configuration page

### Components Used (Existing)

- [ ] `Card`, `CardContent`, `CardHeader`, `CardTitle`, `CardDescription` from `@/components/ui/card`
- [ ] `Button` from `@/components/ui/button`
- [ ] `Label` from `@/components/ui/label`
- [ ] `Slider` from `@/components/ui/slider`
- [ ] `Select`, `SelectContent`, `SelectItem`, `SelectTrigger`, `SelectValue` from `@/components/ui/select`
- [ ] `Alert`, `AlertDescription` from `@/components/ui/alert`

### Hooks Used (From Prompt P01)

- [ ] `useEstimateCost()` from `@/hooks/useTrainingConfig.ts`
- [ ] `useCreateTrainingJob()` from `@/hooks/useTrainingConfig.ts`
- [ ] `useDebounce()` from `@/hooks/useDebounce` (existing)

### Pages

- [ ] `/training/configure` - Training configuration page

---

## 🔜 What's Next

### For Next Prompt in This Section

**Section Complete:** This is the final prompt in Section E03.

### For Next Section

**Next Section:** E04: Training Job Monitoring

The next section will build upon:
- Training jobs created by this section (status='queued')
- Job ID from navigation after creation
- Real-time job monitoring with progress tracking
- Cost tracking and metrics display

---

## ⚠️ Important Reminders

1. **Follow the Spec Exactly:** All code provided in this prompt comes from the integrated specification. Implement it as written.

2. **Reuse Existing Infrastructure:** Don't recreate what already exists. Import and use:
   - shadcn/ui components from `@/components/ui/*`
   - React Query hooks from Prompt P01
   - `useDebounce` hook from existing codebase
   - Toast notifications from existing UI

3. **Integration Points:** When importing from previous work, add comments:
   ```typescript
   // From Section E03, Prompt P01 - API hooks
   import { useEstimateCost, useCreateTrainingJob } from '@/hooks/useTrainingConfig';
   ```

4. **Pattern Consistency:** Match existing patterns:
   - Page structure: Container with max-width
   - Component spacing: space-y-6 for sections
   - Loading states: Loader2 spinner with disabled states
   - Navigation: useRouter for client-side navigation

5. **Don't Skip Steps:** Implement all UI sections listed in this prompt.

---

## 📚 Reference Materials

### Files from Previous Work

#### Section E01: Foundation & Authentication
- `src/lib/types/lora-training.ts` - TypeScript types
- `src/components/ui/*` - All shadcn/ui components

#### Section E02: Dataset Management
- `src/app/(dashboard)/datasets/page.tsx` - Page layout pattern
- `src/hooks/use-datasets.ts` - React Query hook pattern

#### Section E03 - Prompt P01: API Layer
- `src/hooks/useTrainingConfig.ts` - Hooks for cost estimation and job creation
- `src/app/api/jobs/estimate/route.ts` - Cost estimation API
- `src/app/api/jobs/route.ts` - Job creation API

### Infrastructure Patterns

- **Components:** shadcn/ui component patterns from existing codebase
- **State Management:** useState for local form state
- **Data Fetching:** React Query hooks for API calls
- **Debouncing:** useDebounce hook for performance optimization
- **Navigation:** useRouter for programmatic navigation
- **Toast:** Toast notifications for user feedback

---

**Ready to implement Section E03, Prompt P02!**

---

## Section Completion Checklist

After completing all prompts in this section:

### API Layer (Prompt P01)
- [ ] Cost estimation endpoint working with accurate calculations
- [ ] Job creation endpoint validating datasets correctly
- [ ] Job listing endpoint returning paginated results
- [ ] All React hooks functional
- [ ] All manual API tests passing

### UI Layer (Prompt P02)
- [ ] Training configuration page rendering correctly
- [ ] Preset selection updating hyperparameters
- [ ] GPU configuration working
- [ ] Hyperparameter sliders functional
- [ ] Real-time cost estimation updating (debounced)
- [ ] Job creation and navigation working
- [ ] All UI tests passing

### Integration
- [ ] Cost estimation triggered automatically on config changes
- [ ] Job creation succeeds and navigates to monitor page
- [ ] Toast notifications showing success/error states
- [ ] No TypeScript errors across all files
- [ ] No linter warnings across all files

### Database Verification
- [ ] Jobs created with status='queued'
- [ ] Jobs have complete configuration (gpu_config, hyperparameters)
- [ ] Jobs have accurate total_steps calculated
- [ ] Notifications created for queued jobs

### Ready for Next Section
- [ ] Section E03 fully implemented and tested
- [ ] Jobs available for monitoring in Section E04
- [ ] Jobs available for processing in Section E05

---

**End of Section E03 Execution Prompts**

