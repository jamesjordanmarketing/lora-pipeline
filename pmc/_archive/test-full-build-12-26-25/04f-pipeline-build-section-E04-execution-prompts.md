# PIPELINE - Section E04: Training Execution & Monitoring - Execution Prompts

**Product:** PIPELINE  
**Section:** 4 - Training Execution & Monitoring  
**Generated:** 2025-12-24  
**Total Prompts:** 1  
**Estimated Total Time:** 3-5 hours  
**Source Section File:** 04f-pipeline-build-section-E04.md

---

## Section Overview

Execute training jobs on GPU cluster and provide real-time progress monitoring with metrics visualization.

**User Value**: Real-time visibility into training progress with detailed metrics, loss curves, and cost tracking

**Implementation Approach**: This section uses Supabase Edge Functions with Cron scheduling for background job processing (replacing BullMQ+Redis) and React Query polling for real-time UI updates (replacing Server-Sent Events).

---

## Prompt Sequence for This Section

This section has been divided into **1 prompt**:

1. **Prompt P01: Complete Training Execution & Monitoring** (3-5h)
   - Features: FR-4.1, FR-4.4
   - Key Deliverables:
     - Edge Function: `process-training-jobs` (background job processor)
     - API Route: `GET /api/jobs/[jobId]` (job details with metrics)
     - React Hook: `useTrainingJob` (polling for real-time updates)
     - Page: `/training/jobs/[jobId]` (real-time training monitor)
   - Dependencies: E01 (database), E02 (datasets), E03 (job creation)

---

## Integration Context

### Dependencies from Previous Sections

#### Section E01: Foundation & Authentication
**Database Tables:**
- `lora_training_jobs` - Job records with status, progress, metrics
- `lora_metrics_points` - Time-series training metrics
- `lora_cost_records` - Cost tracking records
- `lora_notifications` - User notifications
- `lora_datasets` - Dataset metadata (for joined queries)

**TypeScript Types:**
- `TrainingJob` interface from `@/lib/types/lora-training.ts`
- `JobStatus` type: 'queued' | 'initializing' | 'running' | 'completed' | 'failed' | 'cancelled'

**Infrastructure:**
- Supabase Auth via `requireAuth()` from `@/lib/supabase-server`
- Supabase Client via `createServerSupabaseClient()`
- Storage signed URLs for dataset access

#### Section E02: Dataset Management
**Tables We'll Query:**
- `lora_datasets` - Will join with jobs for dataset name and statistics

**APIs:**
- Dataset validation patterns (background edge functions with Cron)

#### Section E03: Training Configuration
**Tables We'll Update:**
- `lora_training_jobs` - Jobs created in E03, now processed in E04

**Patterns:**
- React Query polling patterns
- shadcn/ui components (Card, Badge, Button, Progress, Tabs)
- Cost tracking methodology

### Provides for Next Sections

**For Section E05 (Model Deployment):**
- Completed jobs with `status='completed'` and `artifact_id` set
- Model artifacts metadata stored in database
- Cost records for billing summaries

**For Section E06 (Notifications & History):**
- Job status change events (for notification triggers)
- Historical metrics data (for analytics)
- Cost records (for spending reports)

---

## Dependency Flow (This Section)

```
E01-P01 (Database Schema)
  ↓
E03-P01 (Job Creation) → Job record with status='queued'
  ↓
E04-P01 (This Prompt)
  ├─ Edge Function: process-training-jobs
  │   ├─ Poll for queued jobs
  │   ├─ Submit to GPU cluster
  │   ├─ Update job status: queued → initializing → running
  │   ├─ Poll GPU cluster for progress
  │   ├─ Store metrics in lora_metrics_points
  │   ├─ Update job.current_metrics, job.progress
  │   └─ Handle completion/failure
  │
  └─ UI Monitor Page
      ├─ useTrainingJob hook (polls every 5s for active jobs)
      ├─ Display live progress bar
      ├─ Display real-time metrics (loss, throughput, cost)
      ├─ Render loss curves with Recharts
      └─ Allow job cancellation
```

---

# PROMPT 1: Complete Training Execution & Monitoring

**Generated:** 2025-12-24  
**Section:** 4 - Training Execution & Monitoring  
**Prompt:** 1 of 1 in this section  
**Estimated Time:** 3-5 hours  
**Prerequisites:** 
- Section E01 completed (database tables exist)
- Section E02 completed (datasets can be uploaded)
- Section E03 completed (jobs can be created)

---

## 🎯 Mission Statement

Implement the complete training execution pipeline and real-time monitoring interface. This prompt creates the background job processor that submits training jobs to a GPU cluster and polls for progress updates, along with a dynamic monitoring page that displays live metrics, loss curves, and progress tracking. This is the critical section that brings the entire training pipeline to life, transforming queued job records into running training processes with real-time visibility.

---

## 📦 Section Context

### This Section's Goal

Execute training jobs on GPU cluster and provide real-time progress monitoring with metrics visualization, cost tracking, and interactive controls (pause/cancel).

### This Prompt's Scope

This is **Prompt 1 of 1** in Section E04. It implements:
- **FR-4.1**: Job Processing Edge Function (background processor)
- **FR-4.4**: Training Monitor Page (real-time UI)

---

## 🔗 Integration with Previous Work

### From Previous Sections

#### Section E01: Foundation & Authentication

**Database Tables We'll Query/Update:**
- `lora_training_jobs` - Created in E01, now updating status/progress/metrics
  - Will update: `status`, `current_stage`, `progress`, `current_epoch`, `current_step`, `current_metrics`, `started_at`, `completed_at`, `external_job_id`, `current_cost`, `final_cost`, `error_message`
- `lora_metrics_points` - Inserting time-series metrics during training
- `lora_datasets` - Joining to get dataset info (name, storage_path, total_training_pairs)
- `lora_cost_records` - Recording compute costs during training
- `lora_notifications` - Creating user notifications on status changes

**TypeScript Types We'll Use:**
- `TrainingJob` from `@/lib/types/lora-training.ts`
- `JobStatus` type for status progression
- `CurrentMetrics` interface for real-time metrics

**Storage Integration:**
- Generate signed URLs for dataset download in Edge Function
- Store model artifacts in `lora-models` bucket upon completion

#### Section E02: Dataset Management

**Files We'll Import:**
- Dataset validation patterns (Edge Function structure with Cron)
- React Query patterns from `@/hooks/use-datasets.ts`

**Database Joins:**
- `lora_datasets` joined with `lora_training_jobs` for display

#### Section E03: Training Configuration

**Jobs We'll Process:**
- Training jobs created via `POST /api/jobs` with `status='queued'`

**Files We'll Import:**
- `@/hooks/useTrainingConfig.ts` - `useTrainingJob` hook pattern
- GPU pricing configuration (for cost accumulation)

**Components We'll Reuse:**
- shadcn/ui: Card, CardContent, CardHeader, CardTitle, CardDescription
- shadcn/ui: Badge, Button, Progress, Alert, Tabs
- shadcn/ui: Skeleton (for loading states)
- Recharts: LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer

### From Previous Prompts (This Section)

This is the first and only prompt in Section E04. No previous prompts in this section.

---

## 🎯 Implementation Requirements

### Feature FR-4.1: Job Processing Edge Function

**Type:** Background Processing (Edge Function)  
**Strategy:** EXTENSION - using Supabase Edge Functions + Cron instead of BullMQ + Redis

#### Description

Background worker that:
1. Polls database for jobs with `status='queued'`
2. Submits jobs to external GPU cluster API
3. Updates job status to `initializing` → `running`
4. Polls GPU cluster for progress updates every 30 seconds
5. Stores metrics in `lora_metrics_points` table
6. Updates job progress and current_metrics
7. Handles completion, failure, and cancellation
8. Records costs and creates notifications

#### What Already Exists (Don't Rebuild)

- ✅ Supabase Edge Functions runtime (Deno environment)
- ✅ Supabase Client with service role access
- ✅ Database tables: `lora_training_jobs`, `lora_metrics_points`, `lora_cost_records`, `lora_notifications`
- ✅ Storage bucket: `lora-datasets` (for accessing dataset files)
- ✅ Cron trigger capability in Supabase

#### What We're Building (New in This Prompt)

- 🆕 `supabase/functions/process-training-jobs/index.ts` - Main edge function
- 🆕 Cron configuration for 30-second polling cycle
- 🆕 GPU cluster API integration (submit, poll, cancel endpoints)
- 🆕 Progress calculation and metrics storage logic
- 🆕 Cost accumulation logic

#### Implementation Details

**Edge Function File:** `supabase/functions/process-training-jobs/index.ts`

**Purpose:** Background worker that processes queued training jobs and updates running jobs

**Key Features:**
- Runs on Cron schedule (every 30 seconds)
- Two main functions: `processQueuedJobs()` and `updateRunningJobs()`
- Submits up to 5 queued jobs per cycle
- Polls all running jobs for progress updates
- Handles GPU cluster API responses
- Creates user notifications on status changes

**Implementation:**

```typescript
import { createClient } from '@supabase/supabase-js';

// Initialize Supabase client with service role key
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
);

// GPU Cluster API configuration
const GPU_CLUSTER_API_URL = Deno.env.get('GPU_CLUSTER_API_URL')!;
const GPU_CLUSTER_API_KEY = Deno.env.get('GPU_CLUSTER_API_KEY')!;

/**
 * Process training jobs edge function
 * 
 * This function runs on a cron schedule (every 30 seconds) and:
 * 1. Finds jobs with status='queued'
 * 2. Submits them to the GPU cluster
 * 3. Updates status to 'initializing'
 * 4. Polls running jobs for progress updates
 * 5. Updates metrics and progress in database
 * 6. Handles job completion and errors
 */
Deno.serve(async (req) => {
  try {
    console.log('[JobProcessor] Starting job processing cycle');

    // Process queued jobs (submit to GPU cluster)
    await processQueuedJobs();

    // Update running jobs (poll GPU cluster for progress)
    await updateRunningJobs();

    return new Response(
      JSON.stringify({ success: true, message: 'Job processing cycle complete' }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('[JobProcessor] Error:', error);
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});

/**
 * Process queued jobs - submit to GPU cluster
 */
async function processQueuedJobs() {
  // Fetch jobs waiting to be submitted
  const { data: queuedJobs, error } = await supabase
    .from('lora_training_jobs')
    .select(`
      *,
      dataset:lora_datasets(storage_path, storage_bucket, total_training_pairs)
    `)
    .eq('status', 'queued')
    .order('created_at', { ascending: true })
    .limit(5); // Process up to 5 jobs per cycle

  if (error) {
    console.error('[JobProcessor] Error fetching queued jobs:', error);
    return;
  }

  if (!queuedJobs || queuedJobs.length === 0) {
    console.log('[JobProcessor] No queued jobs to process');
    return;
  }

  console.log(`[JobProcessor] Processing ${queuedJobs.length} queued jobs`);

  for (const job of queuedJobs) {
    try {
      // Update status to initializing
      await supabase
        .from('lora_training_jobs')
        .update({
          status: 'initializing',
          current_stage: 'initializing',
        })
        .eq('id', job.id);

      // Get signed URL for dataset
      const { data: signedUrlData } = await supabase.storage
        .from(job.dataset.storage_bucket)
        .createSignedUrl(job.dataset.storage_path, 3600 * 24); // 24 hour expiry

      if (!signedUrlData) {
        throw new Error('Failed to generate dataset signed URL');
      }

      // Submit job to GPU cluster
      const gpuJobPayload = {
        job_id: job.id,
        dataset_url: signedUrlData.signedUrl,
        hyperparameters: {
          ...job.hyperparameters,
          base_model: 'mistralai/Mistral-7B-v0.1',
        },
        gpu_config: job.gpu_config,
        callback_url: `${Deno.env.get('SUPABASE_URL')}/functions/v1/training-callback`,
      };

      const response = await fetch(`${GPU_CLUSTER_API_URL}/training/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${GPU_CLUSTER_API_KEY}`,
        },
        body: JSON.stringify(gpuJobPayload),
      });

      if (!response.ok) {
        const errorData = await response.text();
        throw new Error(`GPU cluster submission failed: ${errorData}`);
      }

      const gpuJob = await response.json();

      // Update job with external ID and status
      await supabase
        .from('lora_training_jobs')
        .update({
          external_job_id: gpuJob.external_job_id,
          status: 'running',
          current_stage: 'training',
          started_at: new Date().toISOString(),
        })
        .eq('id', job.id);

      console.log(`[JobProcessor] Job ${job.id} submitted to GPU cluster: ${gpuJob.external_job_id}`);

      // Create notification
      await supabase.from('lora_notifications').insert({
        user_id: job.user_id,
        type: 'job_started',
        title: 'Training Started',
        message: `Your training job has started on ${job.gpu_config.count}x ${job.gpu_config.type}`,
        priority: 'medium',
        action_url: `/training/jobs/${job.id}`,
        metadata: { job_id: job.id },
      });

    } catch (error) {
      console.error(`[JobProcessor] Error processing job ${job.id}:`, error);
      
      // Mark job as failed
      await supabase
        .from('lora_training_jobs')
        .update({
          status: 'failed',
          error_message: error.message,
          error_stack: error.stack,
        })
        .eq('id', job.id);

      // Create error notification
      await supabase.from('lora_notifications').insert({
        user_id: job.user_id,
        type: 'job_failed',
        title: 'Training Failed',
        message: `Your training job failed to start: ${error.message}`,
        priority: 'high',
        action_url: `/training/jobs/${job.id}`,
        metadata: { job_id: job.id },
      });
    }
  }
}

/**
 * Update running jobs - poll GPU cluster for progress
 */
async function updateRunningJobs() {
  // Fetch jobs currently running
  const { data: runningJobs, error } = await supabase
    .from('lora_training_jobs')
    .select('*')
    .in('status', ['running', 'initializing'])
    .not('external_job_id', 'is', null);

  if (error) {
    console.error('[JobProcessor] Error fetching running jobs:', error);
    return;
  }

  if (!runningJobs || runningJobs.length === 0) {
    console.log('[JobProcessor] No running jobs to update');
    return;
  }

  console.log(`[JobProcessor] Updating ${runningJobs.length} running jobs`);

  for (const job of runningJobs) {
    try {
      // Poll GPU cluster for job status
      const response = await fetch(
        `${GPU_CLUSTER_API_URL}/training/status/${job.external_job_id}`,
        {
          headers: {
            'Authorization': `Bearer ${GPU_CLUSTER_API_KEY}`,
          },
        }
      );

      if (!response.ok) {
        console.error(`[JobProcessor] Failed to get status for job ${job.id}`);
        continue;
      }

      const gpuJobStatus = await response.json();

      // Update job progress and metrics
      const updates: any = {
        progress: gpuJobStatus.progress || job.progress,
        current_epoch: gpuJobStatus.current_epoch || job.current_epoch,
        current_step: gpuJobStatus.current_step || job.current_step,
        current_stage: gpuJobStatus.stage || job.current_stage,
      };

      // Update current metrics if available
      if (gpuJobStatus.metrics) {
        updates.current_metrics = {
          training_loss: gpuJobStatus.metrics.training_loss,
          validation_loss: gpuJobStatus.metrics.validation_loss,
          learning_rate: gpuJobStatus.metrics.learning_rate,
          throughput: gpuJobStatus.metrics.throughput,
          gpu_utilization: gpuJobStatus.metrics.gpu_utilization,
        };

        // Store metrics point
        await supabase.from('lora_metrics_points').insert({
          job_id: job.id,
          epoch: gpuJobStatus.current_epoch,
          step: gpuJobStatus.current_step,
          training_loss: gpuJobStatus.metrics.training_loss,
          validation_loss: gpuJobStatus.metrics.validation_loss,
          learning_rate: gpuJobStatus.metrics.learning_rate,
          gradient_norm: gpuJobStatus.metrics.gradient_norm,
          throughput: gpuJobStatus.metrics.throughput,
          gpu_utilization: gpuJobStatus.metrics.gpu_utilization,
        });
      }

      // Calculate and update cost
      if (job.started_at) {
        const startTime = new Date(job.started_at).getTime();
        const now = Date.now();
        const hoursElapsed = (now - startTime) / (1000 * 60 * 60);
        const gpuPricing: Record<string, number> = {
          'A100-80GB': 3.50,
          'A100-40GB': 2.80,
          'H100': 4.20,
          'V100-32GB': 2.10,
        };
        const hourlyRate = gpuPricing[job.gpu_config.type] * job.gpu_config.count;
        updates.current_cost = parseFloat((hourlyRate * hoursElapsed).toFixed(2));
      }

      // Handle job completion
      if (gpuJobStatus.status === 'completed') {
        updates.status = 'completed';
        updates.completed_at = new Date().toISOString();
        updates.final_cost = updates.current_cost;
        updates.progress = 100;

        // Download and store model artifacts (implementation depends on GPU cluster API)
        // This is a placeholder - actual implementation would download artifacts
        console.log(`[JobProcessor] Job ${job.id} completed - artifacts ready`);

        // Create completion notification
        await supabase.from('lora_notifications').insert({
          user_id: job.user_id,
          type: 'job_completed',
          title: 'Training Completed',
          message: `Your training job completed successfully. Final cost: $${updates.final_cost}`,
          priority: 'high',
          action_url: `/training/jobs/${job.id}`,
          metadata: { job_id: job.id },
        });

        // Record final cost
        await supabase.from('lora_cost_records').insert({
          user_id: job.user_id,
          job_id: job.id,
          cost_type: 'training_compute',
          amount: updates.final_cost,
          details: {
            gpu_type: job.gpu_config.type,
            gpu_count: job.gpu_config.count,
            duration_hours: (updates.final_cost / (gpuPricing[job.gpu_config.type] * job.gpu_config.count)).toFixed(2),
          },
          billing_period: new Date().toISOString().split('T')[0],
        });
      }

      // Handle job failure
      if (gpuJobStatus.status === 'failed') {
        updates.status = 'failed';
        updates.error_message = gpuJobStatus.error || 'Training failed on GPU cluster';
        updates.final_cost = updates.current_cost;

        // Create failure notification
        await supabase.from('lora_notifications').insert({
          user_id: job.user_id,
          type: 'job_failed',
          title: 'Training Failed',
          message: `Your training job failed: ${updates.error_message}`,
          priority: 'high',
          action_url: `/training/jobs/${job.id}`,
          metadata: { job_id: job.id },
        });
      }

      // Apply updates to database
      await supabase
        .from('lora_training_jobs')
        .update(updates)
        .eq('id', job.id);

    } catch (error) {
      console.error(`[JobProcessor] Error updating job ${job.id}:`, error);
    }
  }
}
```

**Key Points:**
- Uses Supabase service role client (admin access to bypass RLS)
- Polls every 30 seconds via Cron trigger
- Processes up to 5 queued jobs per cycle (to avoid overload)
- Updates all running jobs with latest metrics
- Stores time-series metrics in `lora_metrics_points` table
- Calculates cost based on elapsed time and GPU pricing
- Creates user notifications on status changes
- Handles errors gracefully and marks jobs as failed

**Deployment Command:**

```bash
# Deploy edge function
supabase functions deploy process-training-jobs

# Set environment variables
supabase secrets set GPU_CLUSTER_API_URL=https://your-gpu-cluster.com
supabase secrets set GPU_CLUSTER_API_KEY=your_api_key_here
```

**Cron Configuration:**

Configure in Supabase Dashboard → Edge Functions → Cron Jobs:
- Function: `process-training-jobs`
- Schedule: `*/30 * * * * *` (every 30 seconds)
- HTTP Method: POST
- Description: "Process queued training jobs and update running jobs"

**Verification:**

```sql
-- Verify jobs are being processed
SELECT id, status, current_stage, progress, current_epoch, external_job_id
FROM lora_training_jobs
WHERE status IN ('queued', 'initializing', 'running')
ORDER BY created_at DESC;

-- Verify metrics are being stored
SELECT job_id, epoch, step, training_loss, validation_loss, timestamp
FROM lora_metrics_points
WHERE job_id = '[your-job-id]'
ORDER BY timestamp DESC
LIMIT 10;

-- Check edge function logs
-- Use Supabase Dashboard → Edge Functions → Logs
```

---

### Feature FR-4.4: Training Monitor Page

**Type:** UI Page  
**Strategy:** EXTENSION - using React Query polling instead of Server-Sent Events

#### Description

Real-time training monitor page that displays:
- Live progress bar (epoch/step tracking)
- Key metrics cards (loss, throughput, cost)
- Loss curve charts (training and validation loss over time)
- GPU utilization and performance metrics
- Job control buttons (cancel job)
- Status badges and notifications

#### What Already Exists (Don't Rebuild)

- ✅ Next.js App Router page structure
- ✅ shadcn/ui components (Card, Badge, Button, Progress, Tabs, Alert)
- ✅ Recharts library for charts
- ✅ React Query for data fetching
- ✅ `useTrainingJob` hook pattern from Section E03

#### What We're Building (New in This Prompt)

- 🆕 `src/app/api/jobs/[jobId]/route.ts` - API endpoint for job details with metrics
- 🆕 `src/app/api/jobs/[jobId]/cancel/route.ts` - API endpoint for job cancellation
- 🆕 `src/app/(dashboard)/training/jobs/[jobId]/page.tsx` - Training monitor page component
- 🆕 Enhanced `useTrainingJob` hook in `@/hooks/useTrainingConfig.ts` (with polling)

#### Implementation Details

**API Route:** `src/app/api/jobs/[jobId]/route.ts`

**Purpose:** Fetch job details with metrics and cost records

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * GET /api/jobs/[jobId] - Get job details with metrics and cost records
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { jobId: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const { jobId } = params;
    const supabase = createServerSupabaseClient();

    // Fetch job with dataset join
    const { data: job, error: jobError } = await supabase
      .from('lora_training_jobs')
      .select(`
        *,
        dataset:lora_datasets(id, name, format, total_training_pairs, total_tokens)
      `)
      .eq('id', jobId)
      .eq('user_id', user.id)
      .single();

    if (jobError || !job) {
      return NextResponse.json(
        { error: 'Job not found or access denied' },
        { status: 404 }
      );
    }

    // Fetch metrics points (last 100 for chart)
    const { data: metrics } = await supabase
      .from('lora_metrics_points')
      .select('*')
      .eq('job_id', jobId)
      .order('timestamp', { ascending: true })
      .limit(100);

    // Fetch cost records
    const { data: costRecords } = await supabase
      .from('lora_cost_records')
      .select('*')
      .eq('job_id', jobId)
      .order('recorded_at', { ascending: false });

    return NextResponse.json({
      success: true,
      data: {
        job,
        metrics: metrics || [],
        cost_records: costRecords || [],
      },
    });
  } catch (error: any) {
    console.error('Job fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch job', details: error.message },
      { status: 500 }
    );
  }
}
```

**API Route:** `src/app/api/jobs/[jobId]/cancel/route.ts`

**Purpose:** Cancel a running training job

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * POST /api/jobs/[jobId]/cancel - Cancel running job
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { jobId: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const { jobId } = params;
    const supabase = createServerSupabaseClient();

    // Fetch job to verify ownership and status
    const { data: job, error: jobError } = await supabase
      .from('lora_training_jobs')
      .select('id, status, external_job_id, user_id, current_cost')
      .eq('id', jobId)
      .eq('user_id', user.id)
      .single();

    if (jobError || !job) {
      return NextResponse.json(
        { error: 'Job not found or access denied' },
        { status: 404 }
      );
    }

    // Check if job can be cancelled
    if (!['queued', 'initializing', 'running'].includes(job.status)) {
      return NextResponse.json(
        { error: 'Job cannot be cancelled', details: `Job is already ${job.status}` },
        { status: 400 }
      );
    }

    // If job has external_job_id, send cancel request to GPU cluster
    if (job.external_job_id) {
      const GPU_CLUSTER_API_URL = process.env.GPU_CLUSTER_API_URL!;
      const GPU_CLUSTER_API_KEY = process.env.GPU_CLUSTER_API_KEY!;

      try {
        await fetch(`${GPU_CLUSTER_API_URL}/training/cancel/${job.external_job_id}`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${GPU_CLUSTER_API_KEY}`,
          },
        });
      } catch (error) {
        console.error('Failed to cancel job on GPU cluster:', error);
        // Continue with database update even if cluster cancel fails
      }
    }

    // Update job status to cancelled
    await supabase
      .from('lora_training_jobs')
      .update({
        status: 'cancelled',
        final_cost: job.current_cost,
        completed_at: new Date().toISOString(),
      })
      .eq('id', jobId);

    // Create cancellation notification
    await supabase.from('lora_notifications').insert({
      user_id: job.user_id,
      type: 'job_cancelled',
      title: 'Training Cancelled',
      message: 'Your training job was cancelled successfully',
      priority: 'medium',
      action_url: `/training/jobs/${jobId}`,
      metadata: { job_id: jobId },
    });

    return NextResponse.json({
      success: true,
      message: 'Job cancelled successfully',
    });
  } catch (error: any) {
    console.error('Job cancellation error:', error);
    return NextResponse.json(
      { error: 'Failed to cancel job', details: error.message },
      { status: 500 }
    );
  }
}
```

**Page Component:** `src/app/(dashboard)/training/jobs/[jobId]/page.tsx`

**Purpose:** Real-time training monitor with live metrics and interactive controls

```typescript
'use client';

import { useState } from 'react';
import { use } from 'react';
import { useTrainingJob } from '@/hooks/useTrainingConfig';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Activity, 
  TrendingDown, 
  Zap, 
  DollarSign,
  Clock,
  Cpu,
  AlertCircle,
  CheckCircle2,
  XCircle,
  Loader2,
  ArrowLeft
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useRouter } from 'next/navigation';

export default function TrainingMonitorPage({ params }: { params: { jobId: string } }) {
  const router = useRouter();
  const { data, isLoading, error } = useTrainingJob(params.jobId);
  const [showCancelConfirm, setShowCancelConfirm] = useState(false);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (error || !data?.success) {
    return (
      <div className="container mx-auto py-8">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>
            Failed to load training job. {error?.message || 'Unknown error'}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  const job = data.data.job;
  const metrics = data.data.metrics || [];
  const costRecords = data.data.cost_records || [];

  // Status badge configuration
  const statusConfig = {
    queued: { color: 'bg-blue-500', icon: Clock, label: 'Queued' },
    initializing: { color: 'bg-yellow-500', icon: Loader2, label: 'Initializing' },
    running: { color: 'bg-green-500', icon: Activity, label: 'Running' },
    completed: { color: 'bg-emerald-600', icon: CheckCircle2, label: 'Completed' },
    failed: { color: 'bg-red-500', icon: XCircle, label: 'Failed' },
    cancelled: { color: 'bg-gray-500', icon: XCircle, label: 'Cancelled' },
  };

  const statusInfo = statusConfig[job.status as keyof typeof statusConfig];
  const StatusIcon = statusInfo.icon;

  // Prepare metrics data for chart
  const chartData = metrics.map((m: any) => ({
    step: m.step,
    epoch: m.epoch,
    training_loss: m.training_loss,
    validation_loss: m.validation_loss,
    learning_rate: m.learning_rate * 10000, // Scale for visibility
  }));

  const handleCancel = async () => {
    try {
      const response = await fetch(`/api/jobs/${job.id}/cancel`, {
        method: 'POST',
      });

      if (response.ok) {
        setShowCancelConfirm(false);
        // Job will be updated via polling
      }
    } catch (error) {
      console.error('Cancel error:', error);
    }
  };

  return (
    <div className="container mx-auto py-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.push('/training/jobs')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold">Training Monitor</h1>
            <p className="text-gray-600 mt-1">{job.dataset?.name || 'Training Job'}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge className={`${statusInfo.color} flex items-center gap-2 text-white px-3 py-1`}>
            <StatusIcon className="h-4 w-4" />
            {statusInfo.label}
          </Badge>
          {['queued', 'initializing', 'running'].includes(job.status) && (
            <Button 
              variant="destructive" 
              onClick={() => setShowCancelConfirm(true)}
            >
              Cancel Job
            </Button>
          )}
        </div>
      </div>

      {/* Cancel Confirmation Dialog */}
      {showCancelConfirm && (
        <Alert>
          <AlertCircle className="h-4 w-4" />
          <AlertDescription className="flex items-center justify-between">
            <span>Are you sure you want to cancel this training job?</span>
            <div className="flex gap-2">
              <Button size="sm" variant="outline" onClick={() => setShowCancelConfirm(false)}>
                No
              </Button>
              <Button size="sm" variant="destructive" onClick={handleCancel}>
                Yes, Cancel
              </Button>
            </div>
          </AlertDescription>
        </Alert>
      )}

      {/* Progress Bar */}
      {job.status === 'running' && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Progress</span>
                <span className="font-semibold">{job.progress.toFixed(1)}%</span>
              </div>
              <Progress value={job.progress} className="h-3" />
              <div className="flex justify-between text-xs text-gray-600">
                <span>Epoch {job.current_epoch} / {job.total_epochs}</span>
                <span>Step {job.current_step?.toLocaleString()} / {job.total_steps?.toLocaleString()}</span>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Training Loss */}
        {job.current_metrics?.training_loss && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <TrendingDown className="h-4 w-4 text-orange-500" />
                Training Loss
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {job.current_metrics.training_loss.toFixed(4)}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Validation Loss */}
        {job.current_metrics?.validation_loss && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <TrendingDown className="h-4 w-4 text-blue-500" />
                Validation Loss
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {job.current_metrics.validation_loss.toFixed(4)}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Throughput */}
        {job.current_metrics?.throughput && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center gap-2">
                <Zap className="h-4 w-4 text-yellow-500" />
                Throughput
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {job.current_metrics.throughput.toLocaleString()}
              </div>
              <div className="text-xs text-gray-600">tokens/sec</div>
            </CardContent>
          </Card>
        )}

        {/* Current Cost */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-green-500" />
              Current Cost
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${(job.final_cost || job.current_cost || 0).toFixed(2)}
            </div>
            <div className="text-xs text-gray-600">
              Est. ${job.estimated_total_cost.toFixed(2)} total
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Charts and Details Tabs */}
      <Tabs defaultValue="metrics" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="metrics">Loss Curves</TabsTrigger>
          <TabsTrigger value="config">Configuration</TabsTrigger>
          <TabsTrigger value="logs">Activity Log</TabsTrigger>
        </TabsList>

        {/* Loss Curves Tab */}
        <TabsContent value="metrics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Training & Validation Loss</CardTitle>
              <CardDescription>
                Loss progression over training steps
              </CardDescription>
            </CardHeader>
            <CardContent>
              {chartData.length > 0 ? (
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="step" 
                      label={{ value: 'Training Step', position: 'insideBottom', offset: -5 }}
                    />
                    <YAxis 
                      label={{ value: 'Loss', angle: -90, position: 'insideLeft' }}
                    />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="training_loss" 
                      stroke="#f97316" 
                      name="Training Loss"
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line 
                      type="monotone" 
                      dataKey="validation_loss" 
                      stroke="#3b82f6" 
                      name="Validation Loss"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="flex items-center justify-center h-[400px] text-gray-500">
                  <div className="text-center">
                    <Activity className="h-12 w-12 mx-auto mb-3 opacity-50" />
                    <p>No metrics data available yet</p>
                    <p className="text-sm">Metrics will appear as training progresses</p>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Configuration Tab */}
        <TabsContent value="config" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Training Configuration</CardTitle>
              <CardDescription>Hyperparameters and GPU settings</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-6">
                {/* Hyperparameters */}
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <Cpu className="h-4 w-4" />
                    Hyperparameters
                  </h3>
                  <dl className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Learning Rate:</dt>
                      <dd className="font-medium">{job.hyperparameters.learning_rate}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Batch Size:</dt>
                      <dd className="font-medium">{job.hyperparameters.batch_size}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Epochs:</dt>
                      <dd className="font-medium">{job.total_epochs}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">LoRA Rank:</dt>
                      <dd className="font-medium">{job.hyperparameters.rank}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">LoRA Alpha:</dt>
                      <dd className="font-medium">{job.hyperparameters.alpha || 'N/A'}</dd>
                    </div>
                  </dl>
                </div>

                {/* GPU Configuration */}
                <div>
                  <h3 className="font-semibold mb-3 flex items-center gap-2">
                    <Zap className="h-4 w-4" />
                    GPU Configuration
                  </h3>
                  <dl className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <dt className="text-gray-600">GPU Type:</dt>
                      <dd className="font-medium">{job.gpu_config.type}</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">GPU Count:</dt>
                      <dd className="font-medium">{job.gpu_config.count}x</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-gray-600">Preset:</dt>
                      <dd className="font-medium capitalize">{job.preset_id}</dd>
                    </div>
                  </dl>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Dataset Info */}
          <Card>
            <CardHeader>
              <CardTitle>Dataset Information</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <dt className="text-gray-600">Dataset Name:</dt>
                  <dd className="font-medium">{job.dataset?.name}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Training Pairs:</dt>
                  <dd className="font-medium">{job.dataset?.total_training_pairs?.toLocaleString()}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Total Tokens:</dt>
                  <dd className="font-medium">{job.dataset?.total_tokens?.toLocaleString()}</dd>
                </div>
              </dl>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Activity Log Tab */}
        <TabsContent value="logs" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Activity Timeline</CardTitle>
              <CardDescription>Job status and timing information</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Queued */}
                <div className="flex items-start gap-3">
                  <div className="mt-1">
                    <Clock className="h-5 w-5 text-blue-500" />
                  </div>
                  <div className="flex-1">
                    <div className="font-medium">Job Queued</div>
                    <div className="text-sm text-gray-600">
                      {new Date(job.queued_at).toLocaleString()}
                    </div>
                  </div>
                </div>

                {/* Started */}
                {job.started_at && (
                  <div className="flex items-start gap-3">
                    <div className="mt-1">
                      <Activity className="h-5 w-5 text-green-500" />
                    </div>
                    <div className="flex-1">
                      <div className="font-medium">Training Started</div>
                      <div className="text-sm text-gray-600">
                        {new Date(job.started_at).toLocaleString()}
                      </div>
                    </div>
                  </div>
                )}

                {/* Completed/Failed */}
                {job.completed_at && (
                  <div className="flex items-start gap-3">
                    <div className="mt-1">
                      {job.status === 'completed' ? (
                        <CheckCircle2 className="h-5 w-5 text-emerald-600" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-500" />
                      )}
                    </div>
                    <div className="flex-1">
                      <div className="font-medium">
                        {job.status === 'completed' ? 'Training Completed' : 'Training Failed'}
                      </div>
                      <div className="text-sm text-gray-600">
                        {new Date(job.completed_at).toLocaleString()}
                      </div>
                      {job.error_message && (
                        <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-sm text-red-700">
                          {job.error_message}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* External Job ID */}
                {job.external_job_id && (
                  <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                    <div className="text-xs text-gray-600">External Job ID</div>
                    <div className="font-mono text-sm mt-1">{job.external_job_id}</div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
```

**Key Points:**
- Uses `useTrainingJob` hook with polling every 5 seconds for active jobs
- Displays real-time progress bar with epoch/step tracking
- Shows key metrics cards (loss, throughput, cost)
- Renders loss curves using Recharts (training and validation loss)
- Provides job cancellation functionality
- Organized in tabs: Metrics, Configuration, Activity Log
- Responsive design with grid layouts
- Status badges with icons and colors
- Loading and error states handled

---

## ✅ Acceptance Criteria

### Functional Requirements

**FR-4.1: Job Processing Edge Function**
- [ ] Edge function deployed and accessible via Supabase
- [ ] Cron trigger configured to run every 30 seconds
- [ ] Queued jobs (status='queued') detected and processed
- [ ] Jobs submitted to GPU cluster API successfully
- [ ] Job status updated: queued → initializing → running
- [ ] Running jobs polled for progress updates
- [ ] Metrics stored in `lora_metrics_points` table
- [ ] Job progress and current_metrics updated in real-time
- [ ] Cost calculated and accumulated correctly
- [ ] Job completion detected and status updated to 'completed'
- [ ] Job failures detected and status updated to 'failed'
- [ ] Notifications created on status changes
- [ ] Cost records stored on completion

**FR-4.4: Training Monitor Page**
- [ ] Page loads without errors at `/training/jobs/[jobId]`
- [ ] Job details fetched and displayed correctly
- [ ] Live progress bar updates automatically (for running jobs)
- [ ] Metrics cards show current loss, throughput, and cost
- [ ] Loss curve chart renders with training and validation loss
- [ ] Chart updates automatically as new metrics arrive
- [ ] Job cancellation button visible for active jobs
- [ ] Cancel confirmation dialog works correctly
- [ ] Job cancelled successfully via API
- [ ] Configuration tab shows all hyperparameters and GPU settings
- [ ] Activity log tab shows timeline of job events
- [ ] Status badge displays correct color and icon
- [ ] Back button navigates to jobs list page

### Technical Requirements

- [ ] No TypeScript errors in all files
- [ ] No linter warnings
- [ ] Edge function uses Supabase service role key (not user context)
- [ ] API routes use `requireAuth()` for authentication
- [ ] Database queries respect RLS policies (user-owned data only)
- [ ] React Query polling configured correctly (5s interval for active jobs)
- [ ] Recharts library integrated and rendering correctly
- [ ] All shadcn/ui components imported and styled correctly
- [ ] Loading states shown during data fetching
- [ ] Error states handled gracefully

### Integration Requirements

- [ ] Edge function queries database tables from Section E01
- [ ] Edge function joins `lora_datasets` table for dataset info
- [ ] API route fetches job created in Section E03
- [ ] UI page uses components from existing shadcn/ui library
- [ ] React Query patterns match existing hooks from Section E02/E03
- [ ] Navigation flows work (back to jobs list)
- [ ] Status progression works end-to-end: queued → running → completed

---

## 🧪 Testing & Validation

### Manual Testing Steps

1. **Deploy Edge Function**
   ```bash
   # Deploy function
   supabase functions deploy process-training-jobs
   
   # Verify deployment
   supabase functions list
   
   # Check logs
   supabase functions logs process-training-jobs
   ```

2. **Test Job Processing Flow**
   - Create a training job via Section E03 configuration page
   - Wait 30 seconds for edge function to pick up job
   - Verify job status changes from 'queued' to 'initializing'
   - Check edge function logs for submission confirmation
   - Verify job status changes to 'running' after GPU cluster accepts it
   - Confirm `external_job_id` is set in database

3. **Test Metrics Storage**
   ```sql
   -- Check that metrics are being stored
   SELECT COUNT(*), MIN(timestamp), MAX(timestamp)
   FROM lora_metrics_points
   WHERE job_id = '[your-job-id]';
   
   -- View latest metrics
   SELECT epoch, step, training_loss, validation_loss, throughput
   FROM lora_metrics_points
   WHERE job_id = '[your-job-id]'
   ORDER BY timestamp DESC
   LIMIT 5;
   ```

4. **Test Monitor Page**
   - Navigate to `/training/jobs/[jobId]`
   - Expected: Page loads with job details
   - Verify progress bar shows correct percentage
   - Verify metrics cards display current values
   - Wait 5 seconds and confirm page updates automatically (polling)
   - Switch between tabs (Metrics, Configuration, Activity Log)
   - Verify loss curve chart renders and updates

5. **Test Job Cancellation**
   - Click "Cancel Job" button on monitor page
   - Expected: Confirmation dialog appears
   - Click "Yes, Cancel"
   - Expected: Job status updates to 'cancelled'
   - Verify status badge changes to "Cancelled"
   - Verify edge function stops processing this job

6. **Test Cost Tracking**
   ```sql
   -- Verify cost is being calculated
   SELECT id, current_cost, estimated_total_cost, final_cost
   FROM lora_training_jobs
   WHERE id = '[your-job-id]';
   
   -- Check cost records created on completion
   SELECT *
   FROM lora_cost_records
   WHERE job_id = '[your-job-id]';
   ```

7. **Test Notifications**
   ```sql
   -- Verify notifications created
   SELECT type, title, message, created_at
   FROM lora_notifications
   WHERE metadata->>'job_id' = '[your-job-id]'
   ORDER BY created_at DESC;
   ```

### Expected Outputs

After completing this prompt, you should have:

- [ ] Edge function deployed and running on Cron schedule
- [ ] Queued jobs automatically picked up and submitted to GPU cluster
- [ ] Job status progression working: queued → initializing → running → completed
- [ ] Metrics stored in database and visible in monitor page
- [ ] Loss curves rendering and updating in real-time
- [ ] Cost calculated and displayed accurately
- [ ] Job cancellation functional
- [ ] Notifications created on status changes
- [ ] Complete monitor page accessible at `/training/jobs/[jobId]`

---

## 📦 Deliverables Checklist

### New Files Created

- [ ] `supabase/functions/process-training-jobs/index.ts` - Background job processor edge function
- [ ] `src/app/api/jobs/[jobId]/route.ts` - Job details API endpoint (GET)
- [ ] `src/app/api/jobs/[jobId]/cancel/route.ts` - Job cancellation API endpoint (POST)
- [ ] `src/app/(dashboard)/training/jobs/[jobId]/page.tsx` - Training monitor page component

### Existing Files Modified

- [ ] `src/hooks/useTrainingConfig.ts` - Enhanced `useTrainingJob` hook with polling (already in place from E03, may need verification)

### Database Changes

- [ ] No new tables (using existing tables from Section E01)
- [ ] Metrics inserted into `lora_metrics_points` table
- [ ] Job records updated in `lora_training_jobs` table
- [ ] Cost records inserted into `lora_cost_records` table
- [ ] Notifications inserted into `lora_notifications` table

### Edge Functions

- [ ] `process-training-jobs` deployed and configured with Cron
- [ ] Cron schedule: `*/30 * * * * *` (every 30 seconds)
- [ ] Environment variables set: `GPU_CLUSTER_API_URL`, `GPU_CLUSTER_API_KEY`

### API Endpoints

- [ ] `GET /api/jobs/[jobId]` - Fetch job with metrics and cost records
- [ ] `POST /api/jobs/[jobId]/cancel` - Cancel running job

### Components & Pages

- [ ] Page: `/training/jobs/[jobId]` - Complete training monitor interface

---

## 🔜 What's Next

### For Next Prompt in This Section

**Section Complete:** This is the final and only prompt in Section E04.

### For Next Section

**Next Section:** E05: Model Artifacts & Deployment

The next section will build upon:
- **Completed jobs**: Jobs with `status='completed'` and model artifacts ready
- **Artifacts table**: `lora_model_artifacts` table populated by edge function
- **Storage**: Model files stored in `lora-models` bucket
- **Cost records**: Total training cost calculated and stored

Section E05 will add:
- Model artifact management (list, view, download)
- Model deployment to inference endpoints
- Version control and model lineage tracking
- Quality metrics and evaluation results

---

## ⚠️ Important Reminders

1. **Follow the Spec Exactly:** All code provided in this prompt comes from the integrated specification. Implement it as written.

2. **Reuse Existing Infrastructure:** Don't recreate what already exists. Import and use:
   - Supabase Auth via `requireAuth()` from `@/lib/supabase-server`
   - Supabase Client via `createServerSupabaseClient()`
   - shadcn/ui components from `@/components/ui/*`
   - React Query for data fetching
   - Recharts for data visualization
   - Existing hooks from `@/hooks/useTrainingConfig.ts`

3. **Integration Points:** When importing from previous work, add comments:
   ```typescript
   // From Section E01, Prompt P01 - database schema
   import { TrainingJob } from '@/lib/types/lora-training';
   
   // From Section E03, Prompt P01 - job creation
   const job = await supabase.from('lora_training_jobs')...
   ```

4. **Pattern Consistency:** Match existing patterns:
   - API responses: `{ success: true, data }` or `{ error, details }`
   - File organization: Follow existing structure
   - Component structure: Use existing patterns from E02/E03
   - Edge functions: Service role client, error handling, logging

5. **Don't Skip Steps:** Implement all features listed in this prompt:
   - FR-4.1: Complete edge function with both `processQueuedJobs()` and `updateRunningJobs()`
   - FR-4.4: Complete monitor page with all tabs and functionality

6. **GPU Cluster API Mock:** If you don't have access to an actual GPU cluster API:
   - Mock the API responses for testing
   - Use placeholder endpoints that return sample progress data
   - Document the expected API contract for future integration

7. **Polling Configuration:** React Query polling should:
   - Poll every 5 seconds for active jobs (`status='running'`, `'queued'`, `'initializing'`)
   - Stop polling for completed jobs (`status='completed'`, `'failed'`, `'cancelled'`)
   - Use `refetchInterval` callback to determine polling behavior

8. **Cost Calculation:** Use GPU pricing from Section E03:
   - A100-80GB: $3.50/hr
   - A100-40GB: $2.80/hr
   - H100: $4.20/hr
   - V100-32GB: $2.10/hr
   - Multiply by `gpu_config.count` for multi-GPU cost
   - Calculate based on elapsed time from `started_at`

---

## 📚 Reference Materials

### Files from Previous Work

#### Section E01: Foundation & Authentication
- `supabase/migrations/20241223_create_lora_training_tables.sql` - Database schema
- `src/lib/types/lora-training.ts` - TypeScript types and interfaces
- Database tables: `lora_training_jobs`, `lora_metrics_points`, `lora_cost_records`, `lora_notifications`, `lora_datasets`

#### Section E02: Dataset Management
- `src/hooks/use-datasets.ts` - React Query hooks patterns
- `supabase/functions/validate-datasets/index.ts` - Edge function pattern example
- API pattern: `requireAuth()`, database queries, error handling

#### Section E03: Training Configuration
- `src/app/api/jobs/route.ts` - Job creation API (POST)
- `src/app/api/jobs/estimate/route.ts` - Cost estimation logic
- `src/hooks/useTrainingConfig.ts` - `useTrainingJob` hook (base implementation)
- `src/app/(dashboard)/training/configure/page.tsx` - Form patterns and UI layout

### Infrastructure Patterns

**Authentication:** `requireAuth()` pattern from `@/lib/supabase-server`
```typescript
const { user, response } = await requireAuth(request);
if (response) return response;
```

**Database:** Supabase client pattern
```typescript
const supabase = createServerSupabaseClient();
const { data, error } = await supabase.from('table').select('*');
```

**Edge Functions:** Deno runtime with Supabase service role
```typescript
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
);
```

**API Routes:** Standard response format
```typescript
return NextResponse.json({ success: true, data });
return NextResponse.json({ error: 'Message', details: 'Details' }, { status: 400 });
```

**React Query:** Polling with conditional interval
```typescript
refetchInterval: (data) => {
  const status = data?.data?.status;
  return status === 'running' ? 5000 : false;
}
```

**Components:** shadcn/ui imports
```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
```

---

**Ready to implement Section E04: Training Execution & Monitoring!**

This prompt brings the entire training pipeline to life with background job processing and real-time monitoring. Take your time to implement each feature carefully, test thoroughly, and verify all integration points work correctly.

---

**End of Prompt P01**

---

## Section Completion Checklist

After completing all prompts in this section:

### Core Functionality
- [ ] Edge function `process-training-jobs` deployed and running on Cron
- [ ] Queued jobs automatically submitted to GPU cluster
- [ ] Job status progression working: queued → initializing → running → completed/failed/cancelled
- [ ] Metrics stored in `lora_metrics_points` table
- [ ] Progress and current_metrics updated in real-time
- [ ] Cost calculated and accumulated correctly
- [ ] Notifications created on status changes

### API Endpoints
- [ ] `GET /api/jobs/[jobId]` returns job with metrics and cost records
- [ ] `POST /api/jobs/[jobId]/cancel` successfully cancels running jobs

### UI Components
- [ ] Training monitor page renders without errors
- [ ] Live progress bar updates automatically
- [ ] Metrics cards display current values
- [ ] Loss curve chart renders and updates
- [ ] Tabs work correctly (Metrics, Configuration, Activity Log)
- [ ] Job cancellation flow works
- [ ] Status badges display correctly
- [ ] Loading and error states handled

### Integration Testing
- [ ] End-to-end flow: Create job (E03) → Process job (E04) → Monitor job (E04)
- [ ] Database tables populated correctly
- [ ] React Query polling updates UI automatically
- [ ] Cost tracking accurate
- [ ] Notifications appear in database
- [ ] Navigation flows work correctly

### Technical Verification
- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Edge function logs show successful processing
- [ ] API endpoints authenticated and secured
- [ ] Database queries performant (indexed columns)
- [ ] UI responsive on different screen sizes

### Documentation
- [ ] Edge function environment variables documented
- [ ] GPU cluster API contract documented (for future integration)
- [ ] Database schema usage verified
- [ ] Component integration points documented

---

**Ready to proceed to Section E05: Model Artifacts & Deployment** ✅

---

**End of Section E04 Execution Prompts**

