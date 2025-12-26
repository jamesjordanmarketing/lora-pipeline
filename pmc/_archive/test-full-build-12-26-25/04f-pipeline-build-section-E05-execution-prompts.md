# PIPELINE - Section E05: Model Artifacts & Delivery - Execution Prompts

**Product:** PIPELINE  
**Section:** 5 - Model Artifacts & Delivery  
**Generated:** 2025-12-24  
**Total Prompts:** 1  
**Estimated Total Time:** 5 hours  
**Source Section File:** 04f-pipeline-build-section-E05.md

---

## Section Overview

Store trained model artifacts, calculate quality metrics, and provide secure download access.

**User Value**: Users can view training results, quality assessments, and download trained models for deployment.

**What This Section Implements:**
- Automated artifact creation when training jobs complete
- Model file download from GPU cluster to Supabase Storage
- Quality metrics calculation (convergence, perplexity, overall score)
- Model browsing interface with filtering and sorting
- Secure download URL generation for model files
- Quality rating display (5-star system)

---

## Prompt Sequence for This Section

This section has been divided into **1 prompt**:

1. **Prompt P01: Complete Model Artifacts & Delivery System** (5h)
   - Features: FR-5.1 (Artifact Creation Edge Function), FR-5.3 (Model Artifacts Pages)
   - Key Deliverables: Edge function, API routes, React hooks, list page, detail page
   - Dependencies: Section E04 completed training jobs

---

## Integration Context

### Dependencies from Previous Sections

#### Section E01: Foundation & Authentication
- `lora_model_artifacts` table in database
- `lora-models` storage bucket
- `lora_notifications` table
- Database types from `src/lib/types/lora-training.ts`

#### Section E02: Dataset Management
- Dataset information for artifact metadata

#### Section E03: Training Configuration
- Job configuration details for artifact metadata

#### Section E04: Training Execution & Monitoring
- Completed training jobs trigger artifact creation
- `lora_training_jobs` table with `completed_at` timestamp
- `lora_metrics_points` table for quality calculations
- Training job completion workflow

### Provides for Next Sections

#### Section E06: Cost Tracking & Notifications
- Artifact creation notifications
- Model storage cost records
- Completed artifact records for cost analysis

#### Section E07: Admin Dashboard
- Model artifact statistics
- Quality metrics aggregation
- Storage usage metrics

---

## Dependency Flow (This Section)

```
Section E04: Training Job Completes
  ↓
E05-P01: Artifact Creation Edge Function
  ├── Downloads model from GPU cluster
  ├── Uploads to Supabase Storage
  ├── Calculates quality metrics
  └── Creates artifact record
  ↓
E05-P01: Model Artifacts UI
  ├── API routes for listing and detail
  ├── React hooks for data fetching
  ├── Models list page with filtering
  └── Model detail page with download
```

---

# PROMPT 1: Complete Model Artifacts & Delivery System

**Generated:** 2025-12-24  
**Section:** 5 - Model Artifacts & Delivery  
**Prompt:** 1 of 1 in this section  
**Estimated Time:** 5 hours  
**Prerequisites:** Section E04 completed

---

## 🎯 Mission Statement

Implement the complete model artifacts and delivery system for the LoRA training pipeline. This prompt creates the edge function that automatically processes completed training jobs by downloading model files from the GPU cluster, uploading them to Supabase Storage, calculating quality metrics, and creating artifact records. It also implements the user-facing interface for browsing trained models, viewing quality assessments, and securely downloading model files.

This is the final step in the training pipeline - giving users access to their trained models with quality ratings and download capabilities.

---

## 📦 Section Context

### This Section's Goal

Enable users to access their trained model artifacts with quality assessments and secure downloads.

### This Prompt's Scope

This is **Prompt 1 of 1** in Section E05. It implements:
- FR-5.1: Artifact Creation Edge Function
- FR-5.3: Model Artifacts Pages (with supporting API routes)

---

## 🔗 Integration with Previous Work

### From Previous Sections

#### Section E01: Foundation & Authentication

**Database Tables We'll Use:**
- `lora_model_artifacts` - Store artifact metadata and quality metrics
- `lora_training_jobs` - Query completed jobs, update with artifact_id
- `lora_datasets` - Fetch dataset name for artifact naming
- `lora_metrics_points` - Calculate quality metrics from training history
- `lora_notifications` - Notify users when artifacts are ready

**Storage Bucket We'll Use:**
- `lora-models` - Store model files (adapters, tokenizer, config)

**Types We'll Import:**
- `ModelArtifact` interface (if defined, otherwise we'll infer from schema)
- `TrainingJob` interface
- `MetricsPoint` interface

**Authentication Patterns:**
- `requireAuth()` for API routes
- `createServerSupabaseClient()` for database queries
- `createServerSupabaseAdminClient()` for storage operations

#### Section E02: Dataset Management

**Data We'll Reference:**
- Dataset name and metadata for artifact naming
- Dataset ID for artifact linkage

#### Section E03: Training Configuration

**Data We'll Reference:**
- Training configuration (hyperparameters, GPU config)
- Preset information for artifact metadata

#### Section E04: Training Execution & Monitoring

**Integration Points:**
- Completed training jobs (status='completed') trigger artifact creation
- Training metrics history for quality calculation
- Training cost data for artifact summary
- External job ID for GPU cluster artifact retrieval

**Workflow:**
```
Training Job Completes (Section E04)
  ↓
Edge Function finds completed jobs without artifacts
  ↓
Downloads model files from GPU cluster
  ↓
Uploads to Supabase Storage
  ↓
Calculates quality metrics
  ↓
Creates artifact record
  ↓
Updates job with artifact_id
  ↓
Notifies user
```

### From Previous Prompts (This Section)

This is the first prompt in Section E05. No previous prompts in this section.

---

## 🎯 Implementation Requirements

### Feature FR-5.1: Artifact Creation Edge Function

**Type:** Edge Function (Background Processing)  
**Strategy:** EXTENSION - using existing Supabase Edge Functions infrastructure

#### Description

Automatically process completed training jobs by downloading model artifacts from the GPU cluster, uploading to Supabase Storage, calculating quality metrics, and creating artifact records.

#### What Already Exists (Don't Rebuild)

- ✅ Supabase Edge Functions infrastructure
- ✅ Supabase Storage (`lora-models` bucket)
- ✅ Database tables: `lora_model_artifacts`, `lora_training_jobs`, `lora_metrics_points`
- ✅ Training job completion workflow from Section E04
- ✅ GPU cluster API access patterns

#### What We're Building (New in This Prompt)

- 🆕 `supabase/functions/create-model-artifacts/index.ts` - Edge function
- 🆕 Quality metrics calculation algorithm
- 🆕 Artifact file organization in storage
- 🆕 Artifact-job linkage logic
- 🆕 Success/failure notifications

#### Implementation Details

**Edge Function:** `supabase/functions/create-model-artifacts/index.ts`

**Purpose:** Run on a schedule (every 2 minutes) to process completed training jobs

**Algorithm:**
1. Query for jobs with `status='completed'` and `artifact_id=null`
2. For each job:
   - Fetch artifact download URLs from GPU cluster API
   - Download each artifact file (adapter weights, tokenizer, config, etc.)
   - Upload files to Supabase Storage at `{user_id}/{artifact_id}/{filename}`
   - Calculate quality metrics from `lora_metrics_points` history
   - Create artifact record in `lora_model_artifacts` table
   - Update training job with `artifact_id`
   - Create "artifact_ready" notification
3. Handle errors gracefully (log and continue to next job)

**Code:**

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
);

const GPU_CLUSTER_API_URL = Deno.env.get('GPU_CLUSTER_API_URL')!;
const GPU_CLUSTER_API_KEY = Deno.env.get('GPU_CLUSTER_API_KEY')!;

/**
 * Create Model Artifacts Edge Function
 * 
 * Triggered on a schedule to process completed training jobs.
 * Downloads model files from GPU cluster and uploads to Supabase Storage.
 * Calculates quality metrics and creates artifact records.
 */
Deno.serve(async (req) => {
  try {
    console.log('[ArtifactCreator] Starting artifact creation cycle');

    // Find completed jobs without artifacts
    const { data: completedJobs, error } = await supabase
      .from('lora_training_jobs')
      .select('*')
      .eq('status', 'completed')
      .is('artifact_id', null)
      .not('external_job_id', 'is', null);

    if (error) {
      console.error('[ArtifactCreator] Error fetching completed jobs:', error);
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }

    if (!completedJobs || completedJobs.length === 0) {
      console.log('[ArtifactCreator] No completed jobs waiting for artifacts');
      return new Response(JSON.stringify({ message: 'No jobs to process' }));
    }

    console.log(`[ArtifactCreator] Processing ${completedJobs.length} completed jobs`);

    const results = [];
    for (const job of completedJobs) {
      try {
        const artifactId = await createArtifactForJob(job);
        results.push({ job_id: job.id, artifact_id: artifactId, success: true });
      } catch (error) {
        console.error(`[ArtifactCreator] Error creating artifact for job ${job.id}:`, error);
        results.push({ job_id: job.id, success: false, error: error.message });
      }
    }

    return new Response(
      JSON.stringify({ success: true, processed: completedJobs.length, results }),
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('[ArtifactCreator] Error:', error);
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json' } }
    );
  }
});

/**
 * Create artifact for a single training job
 */
async function createArtifactForJob(job: any): Promise<string> {
  console.log(`[ArtifactCreator] Creating artifact for job ${job.id}`);

  // Step 1: Get artifact download URLs from GPU cluster
  const response = await fetch(
    `${GPU_CLUSTER_API_URL}/training/artifacts/${job.external_job_id}`,
    {
      headers: { 'Authorization': `Bearer ${GPU_CLUSTER_API_KEY}` },
    }
  );

  if (!response.ok) {
    throw new Error(`Failed to get artifact URLs from GPU cluster: ${response.statusText}`);
  }

  const artifactData = await response.json();
  const { download_urls, model_metadata } = artifactData;

  if (!download_urls || Object.keys(download_urls).length === 0) {
    throw new Error('No artifact files available from GPU cluster');
  }

  // Step 2: Download and upload each artifact file
  const artifactId = crypto.randomUUID();
  const storagePath = `${job.user_id}/${artifactId}`;
  const uploadedFiles: Record<string, string> = {};

  for (const [fileName, downloadUrl] of Object.entries(download_urls)) {
    try {
      console.log(`[ArtifactCreator] Downloading ${fileName}...`);
      
      // Download file from GPU cluster
      const fileResponse = await fetch(downloadUrl as string);
      if (!fileResponse.ok) {
        console.error(`Failed to download ${fileName}: ${fileResponse.statusText}`);
        continue;
      }

      const fileBlob = await fileResponse.blob();
      const fileBuffer = await fileBlob.arrayBuffer();

      // Upload to Supabase Storage
      const uploadPath = `${storagePath}/${fileName}`;
      const { error: uploadError } = await supabase.storage
        .from('lora-models')
        .upload(uploadPath, fileBuffer, {
          contentType: 'application/octet-stream',
          upsert: false,
        });

      if (uploadError) {
        console.error(`Upload error for ${fileName}:`, uploadError);
        continue;
      }

      uploadedFiles[fileName] = uploadPath;
      console.log(`[ArtifactCreator] Uploaded ${fileName} to ${uploadPath}`);
    } catch (error) {
      console.error(`Error processing ${fileName}:`, error);
    }
  }

  if (Object.keys(uploadedFiles).length === 0) {
    throw new Error('Failed to upload any artifact files');
  }

  // Step 3: Calculate quality metrics from training history
  const { data: metrics } = await supabase
    .from('lora_metrics_points')
    .select('*')
    .eq('job_id', job.id)
    .order('timestamp', { ascending: true });

  const qualityMetrics = calculateQualityMetrics(metrics || [], job);

  // Step 4: Fetch dataset info for artifact name
  const { data: dataset } = await supabase
    .from('lora_datasets')
    .select('name')
    .eq('id', job.dataset_id)
    .single();

  // Step 5: Create artifact record
  const { data: artifact, error: artifactError } = await supabase
    .from('lora_model_artifacts')
    .insert({
      id: artifactId,
      user_id: job.user_id,
      job_id: job.id,
      dataset_id: job.dataset_id,
      name: `${dataset?.name || 'Model'} - ${new Date().toLocaleDateString()}`,
      version: '1.0.0',
      status: 'stored',
      quality_metrics: qualityMetrics,
      training_summary: {
        epochs_completed: job.current_epoch,
        total_steps: job.current_step,
        final_loss: job.current_metrics?.training_loss,
        training_duration_hours: job.completed_at && job.started_at
          ? (new Date(job.completed_at).getTime() - new Date(job.started_at).getTime()) / (1000 * 60 * 60)
          : null,
        total_cost: job.final_cost,
      },
      configuration: {
        preset_id: job.preset_id,
        hyperparameters: job.hyperparameters,
        gpu_config: job.gpu_config,
      },
      artifacts: uploadedFiles,
    })
    .select()
    .single();

  if (artifactError) {
    throw new Error(`Failed to create artifact record: ${artifactError.message}`);
  }

  // Step 6: Link artifact to job
  await supabase
    .from('lora_training_jobs')
    .update({ artifact_id: artifactId })
    .eq('id', job.id);

  // Step 7: Create notification
  await supabase.from('lora_notifications').insert({
    user_id: job.user_id,
    type: 'artifact_ready',
    title: 'Model Ready for Download',
    message: `Your trained model is ready. Quality score: ${qualityMetrics.overall_score}/5 stars`,
    priority: 'high',
    action_url: `/models/${artifactId}`,
    metadata: { artifact_id: artifactId, job_id: job.id },
  });

  console.log(`[ArtifactCreator] Artifact ${artifactId} created for job ${job.id}`);
  return artifactId;
}

/**
 * Calculate quality metrics from training metrics history
 */
function calculateQualityMetrics(metrics: any[], job: any) {
  if (metrics.length === 0) {
    return {
      overall_score: 3,
      convergence_quality: 'unknown',
      final_training_loss: null,
      final_validation_loss: null,
      perplexity: null,
      loss_improvement: null,
    };
  }

  const finalMetrics = metrics[metrics.length - 1];
  const firstMetrics = metrics[0];
  
  const finalTrainingLoss = finalMetrics.training_loss;
  const finalValidationLoss = finalMetrics.validation_loss;
  const initialTrainingLoss = firstMetrics.training_loss;

  // Calculate perplexity (exp of loss)
  const perplexity = finalValidationLoss ? Math.exp(finalValidationLoss) : null;

  // Calculate loss improvement
  const lossImprovement = initialTrainingLoss 
    ? ((initialTrainingLoss - finalTrainingLoss) / initialTrainingLoss) * 100
    : null;

  // Assess convergence quality based on loss trajectory
  let convergence_quality = 'good';
  let overall_score = 4;

  if (finalTrainingLoss < 0.5 && lossImprovement && lossImprovement > 50) {
    convergence_quality = 'excellent';
    overall_score = 5;
  } else if (finalTrainingLoss < 1.0 && lossImprovement && lossImprovement > 30) {
    convergence_quality = 'good';
    overall_score = 4;
  } else if (finalTrainingLoss < 2.0 && lossImprovement && lossImprovement > 10) {
    convergence_quality = 'fair';
    overall_score = 3;
  } else {
    convergence_quality = 'poor';
    overall_score = 2;
  }

  // Check for validation-training gap (overfitting indicator)
  if (finalValidationLoss && finalTrainingLoss) {
    const gap = finalValidationLoss - finalTrainingLoss;
    if (gap > 0.5) {
      convergence_quality = 'overfitting detected';
      overall_score = Math.max(1, overall_score - 1);
    }
  }

  return {
    overall_score,
    convergence_quality,
    final_training_loss: finalTrainingLoss,
    final_validation_loss: finalValidationLoss,
    perplexity,
    loss_improvement: lossImprovement,
  };
}
```

**Deployment:**

```bash
# Deploy the edge function
supabase functions deploy create-model-artifacts

# Set up cron trigger (every 2 minutes)
# Configure in Supabase Dashboard:
# - Function: create-model-artifacts
# - Schedule: */2 * * * * (every 2 minutes)
# - Enabled: Yes
```

**Key Points:**
- Runs on a schedule (every 2 minutes) to process completed jobs
- Downloads model files from GPU cluster API
- Uploads to Supabase Storage with organized paths
- Calculates quality metrics based on training history
- Creates artifact records with comprehensive metadata
- Links artifacts to jobs via `artifact_id` field
- Notifies users when artifacts are ready
- Handles errors gracefully (logs and continues)

---

### Feature FR-5.3: Model Artifacts Pages

**Type:** API + UI  
**Strategy:** EXTENSION - using existing patterns and shadcn/ui components

#### Description

User-facing interface for browsing trained models, viewing quality assessments, and downloading model files securely.

#### What Already Exists (Don't Rebuild)

- ✅ shadcn/ui components (Card, Badge, Button, Select, Skeleton)
- ✅ React Query infrastructure
- ✅ Dashboard layout
- ✅ Supabase Storage signed URL generation pattern
- ✅ API route patterns with requireAuth()

#### What We're Building (New in This Prompt)

- 🆕 `src/app/api/models/route.ts` - List models API
- 🆕 `src/app/api/models/[id]/route.ts` - Get model detail API
- 🆕 `src/app/api/models/[id]/download/route.ts` - Generate download URLs API
- 🆕 `src/hooks/useModels.ts` - React Query hooks
- 🆕 `src/app/(dashboard)/models/page.tsx` - Models list page
- 🆕 `src/app/(dashboard)/models/[id]/page.tsx` - Model detail page

#### Implementation Details

##### Part 1: API Routes

**File:** `src/app/api/models/route.ts`

**Purpose:** List user's model artifacts with pagination and sorting

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * GET /api/models - List user's model artifacts
 * 
 * Query params:
 * - page: Page number (default: 1)
 * - limit: Results per page (default: 12)
 * - sort: Sort field (default: 'created_at', options: 'created_at', 'quality')
 */
export async function GET(request: NextRequest) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '12');
    const sort = searchParams.get('sort') || 'created_at';

    const supabase = createServerSupabaseClient();

    // Build query
    let query = supabase
      .from('lora_model_artifacts')
      .select(`
        *,
        dataset:lora_datasets(name),
        job:lora_training_jobs(id, preset_id, created_at)
      `, { count: 'exact' })
      .eq('user_id', user.id)
      .is('deleted_at', null);

    // Apply sorting
    if (sort === 'quality') {
      query = query.order('quality_metrics->overall_score', { ascending: false });
    } else {
      query = query.order('created_at', { ascending: false });
    }

    // Apply pagination
    const from = (page - 1) * limit;
    const to = from + limit - 1;
    query = query.range(from, to);

    const { data: models, error, count } = await query;

    if (error) {
      console.error('Database error:', error);
      return NextResponse.json(
        { error: 'Failed to fetch models', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      data: {
        models: models || [],
        pagination: {
          page,
          limit,
          total: count || 0,
          totalPages: Math.ceil((count || 0) / limit),
        },
      },
    });
  } catch (error: any) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}
```

---

**File:** `src/app/api/models/[id]/route.ts`

**Purpose:** Get detailed information about a specific model artifact

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * GET /api/models/[id] - Get model artifact details
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = createServerSupabaseClient();

    // Fetch model with related data
    const { data: model, error } = await supabase
      .from('lora_model_artifacts')
      .select(`
        *,
        dataset:lora_datasets(id, name, total_training_pairs, total_tokens),
        job:lora_training_jobs(
          id,
          preset_id,
          hyperparameters,
          gpu_config,
          queued_at,
          started_at,
          completed_at,
          estimated_total_cost,
          final_cost
        )
      `)
      .eq('id', params.id)
      .eq('user_id', user.id)
      .is('deleted_at', null)
      .single();

    if (error || !model) {
      return NextResponse.json(
        { error: 'Model not found or access denied' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: model,
    });
  } catch (error: any) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}
```

---

**File:** `src/app/api/models/[id]/download/route.ts`

**Purpose:** Generate signed download URLs for model artifact files

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient, createServerSupabaseAdminClient } from '@/lib/supabase-server';

/**
 * POST /api/models/[id]/download - Generate signed download URLs
 * 
 * Request body (optional):
 * {
 *   "files": ["adapter_model.bin", "adapter_config.json"] // Specific files or all if omitted
 * }
 * 
 * Response:
 * {
 *   "success": true,
 *   "data": {
 *     "download_urls": {
 *       "adapter_model.bin": "https://...",
 *       "adapter_config.json": "https://...",
 *       ...
 *     },
 *     "expires_at": "2024-12-25T12:00:00Z"
 *   }
 * }
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = createServerSupabaseClient();

    // Verify user owns this model
    const { data: model, error } = await supabase
      .from('lora_model_artifacts')
      .select('artifacts')
      .eq('id', params.id)
      .eq('user_id', user.id)
      .is('deleted_at', null)
      .single();

    if (error || !model) {
      return NextResponse.json(
        { error: 'Model not found or access denied' },
        { status: 404 }
      );
    }

    // Parse optional files filter
    const body = await request.json().catch(() => ({}));
    const requestedFiles = body.files || null;

    // Get artifact file paths
    const artifactFiles = model.artifacts as Record<string, string>;
    
    if (!artifactFiles || Object.keys(artifactFiles).length === 0) {
      return NextResponse.json(
        { error: 'No artifact files available' },
        { status: 404 }
      );
    }

    // Filter files if specific ones requested
    const filesToDownload = requestedFiles
      ? Object.entries(artifactFiles).filter(([fileName]) => 
          requestedFiles.includes(fileName)
        )
      : Object.entries(artifactFiles);

    // Generate signed URLs (valid for 1 hour)
    const supabaseAdmin = createServerSupabaseAdminClient();
    const downloadUrls: Record<string, string> = {};
    const expiresInSeconds = 3600; // 1 hour

    for (const [fileName, storagePath] of filesToDownload) {
      const { data: urlData, error: urlError } = await supabaseAdmin.storage
        .from('lora-models')
        .createSignedUrl(storagePath, expiresInSeconds);

      if (urlError) {
        console.error(`Error generating URL for ${fileName}:`, urlError);
        continue;
      }

      if (urlData?.signedUrl) {
        downloadUrls[fileName] = urlData.signedUrl;
      }
    }

    if (Object.keys(downloadUrls).length === 0) {
      return NextResponse.json(
        { error: 'Failed to generate download URLs' },
        { status: 500 }
      );
    }

    const expiresAt = new Date(Date.now() + expiresInSeconds * 1000).toISOString();

    return NextResponse.json({
      success: true,
      data: {
        download_urls: downloadUrls,
        expires_at: expiresAt,
      },
    });
  } catch (error: any) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { error: 'Internal server error', details: error.message },
      { status: 500 }
    );
  }
}
```

---

##### Part 2: React Hooks

**File:** `src/hooks/useModels.ts`

**Purpose:** React Query hooks for models data fetching

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useToast } from '@/components/ui/use-toast';

/**
 * Fetch list of models with pagination and sorting
 */
export function useModels(params?: { page?: number; limit?: number; sort?: string }) {
  return useQuery({
    queryKey: ['models', params],
    queryFn: async () => {
      const searchParams = new URLSearchParams();
      if (params?.page) searchParams.set('page', params.page.toString());
      if (params?.limit) searchParams.set('limit', params.limit.toString());
      if (params?.sort) searchParams.set('sort', params.sort);

      const response = await fetch(`/api/models?${searchParams}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch models');
      }
      
      return response.json();
    },
    staleTime: 30 * 1000, // 30 seconds
  });
}

/**
 * Fetch single model details
 */
export function useModel(modelId: string | null) {
  return useQuery({
    queryKey: ['model', modelId],
    queryFn: async () => {
      const response = await fetch(`/api/models/${modelId}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch model');
      }
      
      return response.json();
    },
    enabled: !!modelId,
  });
}

/**
 * Generate download URLs for model files
 */
export function useDownloadModel() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: async ({ modelId, files }: { modelId: string; files?: string[] }) => {
      const response = await fetch(`/api/models/${modelId}/download`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ files }),
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.details || 'Failed to generate download URLs');
      }
      
      return response.json();
    },
    onSuccess: (data) => {
      // Automatically trigger downloads
      const urls = data.data.download_urls;
      Object.entries(urls).forEach(([fileName, url]) => {
        const link = document.createElement('a');
        link.href = url as string;
        link.download = fileName;
        link.click();
      });

      toast({
        title: 'Download Started',
        description: `Downloading ${Object.keys(urls).length} file(s)`,
      });
    },
    onError: (error: Error) => {
      toast({
        title: 'Download Error',
        description: error.message,
        variant: 'destructive',
      });
    },
  });
}
```

---

##### Part 3: Models List Page

**File:** `src/app/(dashboard)/models/page.tsx`

**Purpose:** Browse all model artifacts with filtering and sorting

```typescript
'use client';

import { useState } from 'react';
import { useModels } from '@/hooks/useModels';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { Package, Star, Calendar, Download, DollarSign, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-react';
import Link from 'next/link';

export default function ModelsPage() {
  const [sortBy, setSortBy] = useState('created_at');
  const [page, setPage] = useState(1);

  const { data, isLoading } = useModels({ page, sort: sortBy, limit: 12 });

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-12 w-full" />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(6)].map((_, i) => (
            <Skeleton key={i} className="h-64" />
          ))}
        </div>
      </div>
    );
  }

  const models = data?.data?.models || [];
  const pagination = data?.data?.pagination;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Model Artifacts</h1>
          <p className="text-gray-500 mt-1">Browse and download your trained models</p>
        </div>
      </div>

      {/* Controls */}
      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600">
          {pagination?.total || 0} models total
        </div>
        <Select value={sortBy} onValueChange={setSortBy}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="created_at">Most Recent</SelectItem>
            <SelectItem value="quality">Highest Quality</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Models Grid */}
      {models.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Package className="h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-lg font-semibold mb-2">No models yet</h3>
            <p className="text-gray-500 mb-4 text-center">
              Complete a training job to create your first model
            </p>
            <Link href="/training/configure">
              <Button>Start Training</Button>
            </Link>
          </CardContent>
        </Card>
      ) : (
        <>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {models.map((model: any) => (
              <Link key={model.id} href={`/models/${model.id}`}>
                <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div className="flex items-center gap-2">
                        <Package className="h-5 w-5 text-primary" />
                        <CardTitle className="text-lg line-clamp-1">{model.name}</CardTitle>
                      </div>
                      <div className="flex items-center gap-1">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            className={`h-4 w-4 ${
                              i < model.quality_metrics.overall_score
                                ? 'fill-yellow-400 text-yellow-400'
                                : 'text-gray-300'
                            }`}
                          />
                        ))}
                      </div>
                    </div>
                    <CardDescription className="text-sm">
                      {model.dataset?.name || 'Unknown dataset'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Quality:</span>
                      <Badge variant="outline">
                        {model.quality_metrics.convergence_quality}
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        Created:
                      </span>
                      <span>{new Date(model.created_at).toLocaleDateString()}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600 flex items-center gap-1">
                        <DollarSign className="h-3 w-3" />
                        Cost:
                      </span>
                      <span>${(model.training_summary?.total_cost || 0).toFixed(2)}</span>
                    </div>
                    <Button className="w-full mt-4" variant="outline">
                      View Details
                      <ArrowRight className="h-4 w-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {pagination && pagination.totalPages > 1 && (
            <div className="flex justify-center items-center gap-2 mt-6">
              <Button
                variant="outline"
                disabled={page === 1}
                onClick={() => setPage(p => p - 1)}
              >
                <ChevronLeft className="h-4 w-4" />
                Previous
              </Button>
              <span className="text-sm text-gray-600">
                Page {page} of {pagination.totalPages}
              </span>
              <Button
                variant="outline"
                disabled={page >= pagination.totalPages}
                onClick={() => setPage(p => p + 1)}
              >
                Next
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
```

---

##### Part 4: Model Detail Page

**File:** `src/app/(dashboard)/models/[id]/page.tsx`

**Purpose:** Display detailed model information and provide download functionality

```typescript
'use client';

import { useState } from 'react';
import { useModel, useDownloadModel } from '@/hooks/useModels';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  Package, 
  Star, 
  Calendar, 
  Download, 
  DollarSign, 
  Zap,
  Clock,
  ArrowLeft,
  TrendingDown,
  Cpu,
  CheckCircle2,
  Loader2
} from 'lucide-react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function ModelDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const { data, isLoading, error } = useModel(params.id);
  const downloadModel = useDownloadModel();
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);

  if (isLoading) {
    return (
      <div className="container mx-auto py-8 space-y-6">
        <Skeleton className="h-12 w-full" />
        <Skeleton className="h-64 w-full" />
        <Skeleton className="h-48 w-full" />
      </div>
    );
  }

  if (error || !data?.success) {
    return (
      <div className="container mx-auto py-8">
        <Alert variant="destructive">
          <AlertDescription>
            Failed to load model details. {error?.message || 'Unknown error'}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  const model = data.data;
  const qualityMetrics = model.quality_metrics || {};
  const trainingSummary = model.training_summary || {};
  const artifactFiles = Object.keys(model.artifacts || {});

  const handleDownload = () => {
    const filesToDownload = selectedFiles.length > 0 ? selectedFiles : undefined;
    downloadModel.mutate({ modelId: model.id, files: filesToDownload });
  };

  const toggleFileSelection = (fileName: string) => {
    setSelectedFiles(prev =>
      prev.includes(fileName)
        ? prev.filter(f => f !== fileName)
        : [...prev, fileName]
    );
  };

  return (
    <div className="container mx-auto py-8 space-y-6 max-w-5xl">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold">{model.name}</h1>
          <p className="text-gray-600 mt-1">
            Dataset: {model.dataset?.name || 'Unknown'}
          </p>
        </div>
        <div className="flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={`h-6 w-6 ${
                i < qualityMetrics.overall_score
                  ? 'fill-yellow-400 text-yellow-400'
                  : 'text-gray-300'
              }`}
            />
          ))}
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-500" />
              Quality
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{qualityMetrics.overall_score}/5</div>
            <p className="text-xs text-gray-600 mt-1">
              {qualityMetrics.convergence_quality}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <TrendingDown className="h-4 w-4 text-orange-500" />
              Final Loss
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {qualityMetrics.final_training_loss?.toFixed(4) || 'N/A'}
            </div>
            {qualityMetrics.loss_improvement && (
              <p className="text-xs text-green-600 mt-1">
                {qualityMetrics.loss_improvement.toFixed(1)}% improved
              </p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <Clock className="h-4 w-4 text-blue-500" />
              Duration
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {trainingSummary.training_duration_hours?.toFixed(1) || '0'}h
            </div>
            <p className="text-xs text-gray-600 mt-1">
              {trainingSummary.epochs_completed} epochs
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <DollarSign className="h-4 w-4 text-green-500" />
              Cost
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${trainingSummary.total_cost?.toFixed(2) || '0.00'}
            </div>
            <p className="text-xs text-gray-600 mt-1">training cost</p>
          </CardContent>
        </Card>
      </div>

      {/* Training Configuration */}
      <Card>
        <CardHeader>
          <CardTitle>Training Configuration</CardTitle>
          <CardDescription>Hyperparameters and GPU setup used for training</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-sm text-gray-600">Preset</div>
              <div className="font-medium">{model.configuration.preset_id}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Learning Rate</div>
              <div className="font-medium">
                {model.configuration.hyperparameters.learning_rate}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Batch Size</div>
              <div className="font-medium">
                {model.configuration.hyperparameters.batch_size}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Epochs</div>
              <div className="font-medium">
                {model.configuration.hyperparameters.epochs}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">LoRA Rank</div>
              <div className="font-medium">
                {model.configuration.hyperparameters.rank}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">GPU Type</div>
              <div className="font-medium">
                {model.configuration.gpu_config.type}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">GPU Count</div>
              <div className="font-medium">
                {model.configuration.gpu_config.count}x
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Download Section */}
      <Card>
        <CardHeader>
          <CardTitle>Download Model Files</CardTitle>
          <CardDescription>
            Select specific files or download all artifact files
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {artifactFiles.length === 0 ? (
            <Alert>
              <AlertDescription>No artifact files available for download</AlertDescription>
            </Alert>
          ) : (
            <>
              <div className="space-y-2">
                {artifactFiles.map((fileName) => (
                  <div
                    key={fileName}
                    className="flex items-center justify-between p-3 border rounded-lg hover:bg-gray-50 cursor-pointer"
                    onClick={() => toggleFileSelection(fileName)}
                  >
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        checked={selectedFiles.includes(fileName)}
                        onChange={() => {}}
                        className="h-4 w-4"
                      />
                      <span className="font-mono text-sm">{fileName}</span>
                    </div>
                    <Package className="h-4 w-4 text-gray-400" />
                  </div>
                ))}
              </div>

              <div className="flex gap-3 pt-4 border-t">
                <Button
                  onClick={handleDownload}
                  disabled={downloadModel.isPending}
                  className="flex-1"
                >
                  {downloadModel.isPending && (
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  )}
                  <Download className="h-4 w-4 mr-2" />
                  {selectedFiles.length > 0
                    ? `Download Selected (${selectedFiles.length})`
                    : 'Download All Files'}
                </Button>
                {selectedFiles.length > 0 && (
                  <Button
                    variant="outline"
                    onClick={() => setSelectedFiles([])}
                  >
                    Clear Selection
                  </Button>
                )}
              </div>
            </>
          )}
        </CardContent>
      </Card>

      {/* Dataset Information */}
      {model.dataset && (
        <Card>
          <CardHeader>
            <CardTitle>Dataset Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <div className="text-sm text-gray-600">Dataset Name</div>
                <div className="font-medium">{model.dataset.name}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Training Pairs</div>
                <div className="font-medium">
                  {model.dataset.total_training_pairs?.toLocaleString() || 'N/A'}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Total Tokens</div>
                <div className="font-medium">
                  {model.dataset.total_tokens 
                    ? `${(model.dataset.total_tokens / 1000).toFixed(1)}K`
                    : 'N/A'}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Related Job Link */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-medium">View Training Job Details</div>
              <p className="text-sm text-gray-600 mt-1">
                See metrics, cost breakdown, and training history
              </p>
            </div>
            <Link href={`/training/jobs/${model.job_id}`}>
              <Button variant="outline">
                View Job
                <ArrowLeft className="h-4 w-4 ml-2 rotate-180" />
              </Button>
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
```

**Key Points:**
- Lists all user's model artifacts with quality ratings
- Sortable by date or quality score
- Paginated results (12 per page)
- Detailed model view with configuration and metrics
- File-by-file download selection
- Secure signed URLs (1 hour expiry)
- Links back to training job for full history

---

## ✅ Acceptance Criteria

### Functional Requirements

**Artifact Creation:**
- [ ] Edge function runs on schedule (every 2 minutes)
- [ ] Finds completed jobs without artifacts
- [ ] Downloads model files from GPU cluster
- [ ] Uploads files to Supabase Storage with organized paths
- [ ] Calculates quality metrics from training history
- [ ] Creates artifact record in database
- [ ] Links artifact to job via `artifact_id`
- [ ] Sends notification when artifact is ready
- [ ] Handles errors gracefully (logs and continues)

**Model Browsing:**
- [ ] Models list page displays all user's artifacts
- [ ] Grid layout with quality stars (5-star system)
- [ ] Sortable by date (most recent) or quality (highest rated)
- [ ] Pagination works correctly (12 per page)
- [ ] Empty state shows when no models exist
- [ ] Loading states shown while fetching

**Model Details:**
- [ ] Detail page shows comprehensive model information
- [ ] Quality metrics displayed (score, convergence, loss)
- [ ] Training configuration shown (hyperparameters, GPU)
- [ ] Training summary displayed (duration, cost, epochs)
- [ ] Dataset information shown

**Download Functionality:**
- [ ] All artifact files listed with checkboxes
- [ ] Can select specific files or download all
- [ ] Download button generates signed URLs
- [ ] Multiple files download automatically
- [ ] URLs valid for 1 hour
- [ ] Success toast shown on download start
- [ ] Error toast shown if download fails

### Technical Requirements

- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Edge function deploys successfully
- [ ] Cron trigger configured and working
- [ ] API routes follow existing patterns
- [ ] React Query hooks implemented correctly
- [ ] Storage paths follow convention: `{user_id}/{artifact_id}/{filename}`
- [ ] Signed URLs generated via admin client
- [ ] RLS policies respected (users see only their models)

### Integration Requirements

**Section E01:**
- [ ] Uses `lora_model_artifacts` table correctly
- [ ] Stores files in `lora-models` bucket
- [ ] Respects RLS policies for data security

**Section E04:**
- [ ] Processes jobs marked as `status='completed'`
- [ ] Updates job with `artifact_id` after creation
- [ ] Uses `external_job_id` to fetch from GPU cluster
- [ ] Queries `lora_metrics_points` for quality calculation

**User Experience:**
- [ ] Notification appears when artifact is ready
- [ ] Can navigate from job monitor to model detail
- [ ] Can navigate from model detail back to job
- [ ] Quality rating is intuitive (stars + text)

---

## 🧪 Testing & Validation

### Manual Testing Steps

#### 1. Edge Function Testing

```bash
# Deploy edge function
supabase functions deploy create-model-artifacts

# Test manually (invoke via Supabase Dashboard or CLI)
supabase functions invoke create-model-artifacts

# Check logs
supabase functions logs create-model-artifacts
```

**Expected behavior:**
- Function finds completed jobs without artifacts
- Downloads files from GPU cluster
- Uploads to Supabase Storage
- Creates artifact records
- Updates jobs with artifact_id
- Sends notifications

#### 2. API Testing

**Test models list:**

```bash
curl -X GET http://localhost:3000/api/models?sort=created_at \
  -H "Cookie: ..."
```

**Expected:** JSON with models array and pagination

**Test model detail:**

```bash
curl -X GET http://localhost:3000/api/models/{model_id} \
  -H "Cookie: ..."
```

**Expected:** JSON with complete model data

**Test download URLs:**

```bash
curl -X POST http://localhost:3000/api/models/{model_id}/download \
  -H "Content-Type: application/json" \
  -H "Cookie: ..." \
  -d '{}'
```

**Expected:** JSON with signed URLs for all files

#### 3. Database Verification

```sql
-- Check artifacts created
SELECT id, name, status, quality_metrics->>'overall_score' as score
FROM lora_model_artifacts
WHERE user_id = '{your_user_id}'
ORDER BY created_at DESC;

-- Check job linkage
SELECT j.id, j.status, j.artifact_id, a.name as artifact_name
FROM lora_training_jobs j
LEFT JOIN lora_model_artifacts a ON j.artifact_id = a.id
WHERE j.user_id = '{your_user_id}' AND j.status = 'completed';

-- Check notifications sent
SELECT type, title, message, created_at
FROM lora_notifications
WHERE user_id = '{your_user_id}' AND type = 'artifact_ready'
ORDER BY created_at DESC;
```

#### 4. Storage Verification

```sql
-- Check storage paths in artifacts
SELECT id, name, artifacts
FROM lora_model_artifacts
WHERE user_id = '{your_user_id}'
LIMIT 1;
```

**Expected:** `artifacts` JSON contains paths like `{user_id}/{artifact_id}/{filename}`

**Verify in Supabase Dashboard:**
- Navigate to Storage > lora-models bucket
- Check that folders exist for user_id and artifact_id
- Verify files are present

#### 5. UI Testing

**Models List Page:**
- Navigate to `/models`
- Verify models display in grid
- Test sorting (Most Recent, Highest Quality)
- Test pagination (if > 12 models)
- Click on a model card

**Model Detail Page:**
- Verify all sections render correctly
- Check quality stars display
- Check metrics cards show values
- Test file selection checkboxes
- Click "Download All Files"
- Check toast notification appears
- Verify files download to browser

#### 6. End-to-End Flow

1. Complete a training job (Section E04)
2. Wait 2 minutes for edge function to run
3. Check notification bell for "Model Ready for Download"
4. Navigate to `/models`
5. Verify new model appears in list
6. Click on model to view details
7. Download model files
8. Verify files are downloaded successfully

### Expected Outputs

After completing this prompt, you should have:

- [ ] Edge function deployed and running on schedule
- [ ] Cron trigger configured (every 2 minutes)
- [ ] 3 API routes functional (list, detail, download)
- [ ] 3 React Query hooks working (useModels, useModel, useDownloadModel)
- [ ] 2 pages rendered correctly (list, detail)
- [ ] Artifacts created for completed jobs
- [ ] Storage files organized correctly
- [ ] Download URLs generated successfully
- [ ] Quality ratings calculated accurately
- [ ] Notifications sent when artifacts ready

---

## 📦 Deliverables Checklist

### New Files Created

- [ ] `supabase/functions/create-model-artifacts/index.ts` - Artifact creation edge function
- [ ] `src/app/api/models/route.ts` - List models API
- [ ] `src/app/api/models/[id]/route.ts` - Get model detail API
- [ ] `src/app/api/models/[id]/download/route.ts` - Generate download URLs API
- [ ] `src/hooks/useModels.ts` - React Query hooks for models
- [ ] `src/app/(dashboard)/models/page.tsx` - Models list page
- [ ] `src/app/(dashboard)/models/[id]/page.tsx` - Model detail page

### Existing Files Modified

None (this section only creates new files)

### Database Changes

- [ ] `lora_model_artifacts` table populated with new records
- [ ] `lora_training_jobs.artifact_id` updated for completed jobs
- [ ] `lora_notifications` table receives artifact_ready notifications

### Storage Changes

- [ ] Files uploaded to `lora-models` bucket
- [ ] Storage paths follow pattern: `{user_id}/{artifact_id}/{filename}`

### Edge Functions

- [ ] `create-model-artifacts` deployed
- [ ] Cron trigger: `*/2 * * * *` (every 2 minutes)
- [ ] Environment variables set: `GPU_CLUSTER_API_URL`, `GPU_CLUSTER_API_KEY`

### API Endpoints

- [ ] `GET /api/models` - List user's models (paginated, sorted)
- [ ] `GET /api/models/[id]` - Get model details
- [ ] `POST /api/models/[id]/download` - Generate signed download URLs

### Components & Pages

- [ ] `/models` - Models list page with grid, sorting, pagination
- [ ] `/models/[id]` - Model detail page with download functionality

---

## 🔜 What's Next

### For Next Prompt in This Section

**Section Complete:** This is the final prompt in Section E05.

### For Next Section

**Next Section:** E06 - Cost Tracking & Notifications

The next section will build upon:
- Artifact creation events for cost calculation
- Model storage costs
- Notification system integration
- Cost records for completed training pipeline

**Integration Points:**
- Cost calculation uses artifact creation timestamps
- Notifications system extended with new types
- Dashboard displays aggregate costs including storage

---

## ⚠️ Important Reminders

### 1. Follow the Spec Exactly

All code provided in this prompt comes from the integrated specification. Implement it as written. The edge function algorithm, quality metrics calculation, and API patterns are all specified.

### 2. Reuse Existing Infrastructure

Don't recreate what already exists. Import and use:
- Supabase Auth via `requireAuth()` from `@/lib/supabase-server`
- Supabase Client via `createServerSupabaseClient()`
- Supabase Admin Client via `createServerSupabaseAdminClient()`
- shadcn/ui components from `@/components/ui/*`
- React Query for data fetching
- Existing toast notifications

### 3. Storage Patterns

**Critical storage conventions:**

```typescript
// CORRECT: Store only the path in database
storage_path: `${user_id}/${artifact_id}/adapter_model.bin`

// WRONG: Never store URLs
storage_url: "https://xyz.supabase.co/storage/v1/..."

// Generate signed URLs on-demand in API routes
const { data } = await supabaseAdmin.storage
  .from('lora-models')
  .createSignedUrl(storagePath, 3600);
```

### 4. Quality Metrics Algorithm

The quality metrics calculation is specified in the edge function:
- Use training metrics history from `lora_metrics_points`
- Calculate loss improvement: `(initial - final) / initial * 100`
- Calculate perplexity: `exp(validation_loss)`
- Rate convergence based on final loss and improvement
- Check for overfitting (validation > training gap)
- Assign overall score 1-5 based on quality assessment

### 5. Edge Function Scheduling

**Setup cron trigger in Supabase Dashboard:**
- Function: `create-model-artifacts`
- Schedule: `*/2 * * * *` (every 2 minutes)
- Enabled: Yes
- Timezone: UTC

### 6. Download Flow

**Client-side download flow:**
1. User clicks "Download" button
2. React calls `useDownloadModel` mutation
3. API route verifies ownership
4. API generates signed URLs (1 hour expiry)
5. Client automatically triggers browser downloads
6. Toast notification shows success

### 7. Don't Skip Steps

Implement all features listed in this prompt before moving to the next section:
- Edge function with quality metrics calculation
- All 3 API routes (list, detail, download)
- All React hooks
- Both pages (list and detail)
- Test end-to-end flow

---

## 📚 Reference Materials

### Files from Previous Work

#### Section E01: Foundation & Authentication
- Database tables: `lora_model_artifacts`, `lora_training_jobs`, `lora_metrics_points`, `lora_notifications`
- Storage bucket: `lora-models`
- Auth patterns: `requireAuth()`, `createServerSupabaseClient()`
- Types: `src/lib/types/lora-training.ts`

#### Section E02: Dataset Management
- Dataset query patterns
- Storage signed URL generation patterns

#### Section E03: Training Configuration
- Job configuration structures
- Hyperparameter and GPU config types

#### Section E04: Training Execution & Monitoring
- Training job completion workflow
- Metrics collection patterns
- GPU cluster API integration

### Infrastructure Patterns

**Edge Functions:**
- Deno runtime with Supabase SDK
- Service role key for admin operations
- Cron scheduling via Supabase Dashboard
- Error handling and logging patterns

**Storage Operations:**
- Admin client for signing: `createServerSupabaseAdminClient()`
- Signed URLs: `storage.from(bucket).createSignedUrl(path, expirySeconds)`
- Upload: `storage.from(bucket).upload(path, buffer, options)`
- Download: `storage.from(bucket).download(path)`

**API Routes:**
- Authentication: `requireAuth(request)`
- Response format: `{ success: true, data }` or `{ error, details }`
- Pagination: `range(from, to)` with `count: 'exact'`
- Joins: Use `select()` with relation syntax

**React Patterns:**
- React Query: `useQuery()` for fetches, `useMutation()` for actions
- Toast notifications: `useToast()` from shadcn/ui
- Loading states: `isLoading`, `isPending`
- Error handling: `onError` in mutations

---

**Ready to implement Section E05: Model Artifacts & Delivery!**

This is the culmination of the training pipeline - users can now access their trained models with quality assessments and secure downloads. 🎉

---

## Section Completion Checklist

After completing this prompt:

- [ ] Edge function deployed and running on schedule (every 2 minutes)
- [ ] Cron trigger configured in Supabase Dashboard
- [ ] GPU cluster API integration working (artifact download)
- [ ] Quality metrics calculated correctly from training history
- [ ] Artifact records created in database
- [ ] Jobs updated with artifact_id linkage
- [ ] Storage files uploaded to correct paths
- [ ] API routes functional (list, detail, download)
- [ ] React hooks working (useModels, useModel, useDownloadModel)
- [ ] Models list page renders correctly
- [ ] Model detail page shows all information
- [ ] Download functionality generates signed URLs
- [ ] Browser downloads files successfully
- [ ] Notifications sent when artifacts ready
- [ ] End-to-end flow tested (job complete → artifact → download)
- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Ready to proceed to Section E06

---

**End of Section E05 Execution Prompts**

