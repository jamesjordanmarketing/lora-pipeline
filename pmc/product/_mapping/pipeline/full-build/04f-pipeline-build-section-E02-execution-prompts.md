# PIPELINE - Section E02: Dataset Management - Execution Prompts

**Product:** PIPELINE  
**Section:** 2 - Dataset Management  
**Generated:** 2025-12-25  
**Total Prompts:** 1  
**Estimated Total Time:** 4-5 hours  
**Source Section File:** 04f-pipeline-build-section-E02.md

---

## Section Overview

Enable users to upload, validate, and manage conversation datasets for LoRA training.

**User Value**: Users can upload conversation datasets, validate formats, view statistics, and manage their dataset library.

**What This Section Implements:**
- Dataset upload with Supabase Storage presigned URLs
- Background validation using Edge Functions
- Dataset listing with filters and search
- Complete dataset management UI

---

## Prompt Sequence for This Section

This section has been divided into **1 progressive prompt**:

1. **Prompt P01: Complete Dataset Management** (4-5h)
   - Features: FR-2.1 (Upload with Presigned URLs), FR-2.2 (Validation)
   - Key Deliverables: API routes, Edge Function, React hooks, Components, Pages

---

## Integration Context

### Dependencies from Previous Sections

#### Section E01: Foundation & Authentication
**Database Tables We'll Use:**
- `datasets` table - Store dataset metadata and validation results
- `notifications` table - Notify users when validation completes

**Storage Buckets We'll Use:**
- `lora-datasets` bucket - Store uploaded dataset files

**Types We'll Use:**
- `Dataset`, `CreateDatasetInput`, `DatasetStatus` from `@/lib/types/lora-training.ts`

**Authentication:**
- `requireAuth()` from `@/lib/supabase-server` - Protect API routes
- `createServerSupabaseClient()` - Query database
- `createServerSupabaseAdminClient()` - Generate signed URLs

### Provides for Next Sections

**For Section E03 (Training Configuration):**
- API endpoint: `GET /api/datasets` - Fetch ready datasets for training
- React hook: `useDatasets()` - Query datasets in UI
- Type: `Dataset` interface with validation status

**For Section E04 (Job Execution):**
- Dataset validation status - Ensure only validated datasets can be used
- Dataset statistics - Use for job planning (training pairs, tokens)

---

## Dependency Flow (This Section)

```
E02-P01 (Dataset Upload & Validation)
  ├─ API Routes (POST, GET)
  ├─ Edge Function (validation)
  ├─ React Hooks (data fetching)
  ├─ Components (DatasetCard)
  └─ Page (datasets list)
```

---

# PROMPT 1: Complete Dataset Management

**Generated:** 2025-12-25  
**Section:** 2 - Dataset Management  
**Prompt:** 1 of 1 in this section  
**Estimated Time:** 4-5 hours  
**Prerequisites:** Section E01 - Foundation & Authentication

---

## 🎯 Mission Statement

Implement a complete dataset management system that allows users to upload large dataset files directly to Supabase Storage, automatically validate formats using Edge Functions, and manage their dataset library through an intuitive UI. This is the foundation for all training jobs, ensuring data quality before training begins.

---

## 📦 Section Context

### This Section's Goal
Enable users to upload, validate, and manage conversation datasets for LoRA training.

### This Prompt's Scope
This is **Prompt 1 of 1** in Section E02. It implements:
- FR-2.1: Dataset Upload with Presigned URLs
- FR-2.2: Dataset Validation

---

## 🔗 Integration with Previous Work

### From Previous Sections

#### Section E01: Foundation & Authentication

**Database Tables We'll Query:**
- `datasets` table (created in E01 migration)
  - Schema: id, user_id, name, status, storage_path, file_name, validation_errors, etc.
  - We'll INSERT new records on upload
  - We'll SELECT for listing user's datasets
  - We'll UPDATE after validation completes

- `notifications` table (created in E01 migration)
  - Schema: id, user_id, type, title, message, priority, action_url
  - We'll INSERT notifications when validation completes

**Storage Buckets We'll Use:**
- `lora-datasets` bucket (created in E01)
  - Private bucket for user dataset files
  - We'll generate presigned upload URLs
  - Edge Function will download files for validation

**Types We'll Reuse:**
- `Dataset` interface from `@/lib/types/lora-training.ts`
- `DatasetStatus` type: 'uploading' | 'validating' | 'ready' | 'error'
- `ValidationError` interface for error reporting

**Authentication Patterns:**
- `requireAuth()` - Pattern for protecting API routes
- `createServerSupabaseClient()` - Pattern for database queries
- `createServerSupabaseAdminClient()` - Pattern for admin operations (signing URLs)

**UI Components Available:**
- All 47+ shadcn/ui components from `/components/ui/`
- `DashboardLayout` for page structure

**Data Fetching Patterns:**
- React Query with `useQuery` and `useMutation`
- Standard response format: `{ success: true, data }` or `{ error, details }`

### From Previous Prompts (This Section)

This is the first prompt in Section E02. No previous prompts in this section.

---

## 🎯 Implementation Requirements

### Feature FR-2.1: Dataset Upload with Presigned URLs

**Type:** Storage Integration + API  
**Strategy:** EXTENSION - building on existing Supabase Storage infrastructure

#### Description
Allow users to upload large dataset files (up to 500MB) directly to Supabase Storage using presigned upload URLs. This avoids routing files through the Next.js server and provides better performance for large uploads.

#### What Already Exists (Don't Rebuild)
- ✅ Supabase Storage configured (from E01)
- ✅ `lora-datasets` storage bucket created
- ✅ `datasets` table in database
- ✅ `requireAuth()` authentication helper
- ✅ React Query provider configured

#### What We're Building (New in This Prompt)
- 🆕 `src/app/api/datasets/route.ts` - API routes for dataset CRUD
- 🆕 `src/app/api/datasets/[id]/confirm/route.ts` - Trigger validation
- 🆕 `src/app/api/datasets/[id]/route.ts` - Get single dataset
- 🆕 `src/hooks/use-datasets.ts` - React Query hooks
- 🆕 `src/components/datasets/DatasetCard.tsx` - Display dataset
- 🆕 `src/app/(dashboard)/datasets/page.tsx` - List datasets page

#### Implementation Details

##### API Route: Create Dataset & Generate Upload URL

**File:** `src/app/api/datasets/route.ts`

**Endpoint:** `POST /api/datasets`

**Request Schema:**
```typescript
{
  name: string;          // Dataset name
  description?: string;  // Optional description
  format?: string;       // Default: 'brightrun_lora_v4'
  file_name: string;     // Original filename
  file_size: number;     // File size in bytes
}
```

**Response Schema:**
```typescript
{
  success: true;
  data: {
    dataset: Dataset;       // Created dataset record
    uploadUrl: string;      // Presigned upload URL (1 hour expiry)
    storagePath: string;    // Path where file will be stored
  }
}
```

**Implementation:**
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

**Key Points:**
- Uses `requireAuth()` from Section E01 for authentication
- Uses `createServerSupabaseAdminClient()` for signing operations
- Stores only `storage_path` in database, NOT URLs (on-demand URL generation)
- Validates file size before creating record
- Rolls back dataset creation if URL generation fails
- Returns presigned URL valid for 1 hour

---

##### API Route: Get Single Dataset

**File:** `src/app/api/datasets/[id]/route.ts`

**Endpoint:** `GET /api/datasets/[id]`

**Implementation:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = await createServerSupabaseClient();
    const { data: dataset, error } = await supabase
      .from('datasets')
      .select('*')
      .eq('id', params.id)
      .eq('user_id', user.id)
      .single();

    if (error || !dataset) {
      return NextResponse.json(
        { error: 'Dataset not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: { dataset },
    });
  } catch (error) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = await createServerSupabaseClient();
    
    // Soft delete
    const { error } = await supabase
      .from('datasets')
      .update({ deleted_at: new Date().toISOString() })
      .eq('id', params.id)
      .eq('user_id', user.id);

    if (error) {
      return NextResponse.json(
        { error: 'Failed to delete dataset', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

---

##### API Route: Confirm Upload (Trigger Validation)

**File:** `src/app/api/datasets/[id]/confirm/route.ts`

**Endpoint:** `POST /api/datasets/[id]/confirm`

**Purpose:** Client calls this after successfully uploading file to trigger validation

**Implementation:**
```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = await createServerSupabaseClient();
    
    // Update status to 'validating'
    const { data: dataset, error } = await supabase
      .from('datasets')
      .update({ status: 'validating' })
      .eq('id', params.id)
      .eq('user_id', user.id)
      .select()
      .single();

    if (error || !dataset) {
      return NextResponse.json(
        { error: 'Dataset not found or failed to update' },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: { dataset },
    });
  } catch (error) {
    console.error('Unexpected error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

---

##### Add Missing Type Definition

**File:** `src/lib/types/lora-training.ts` (ADD to existing file)

**Add this export:**
```typescript
// Add to existing file
export interface CreateDatasetInput {
  name: string;
  description?: string;
  format?: 'brightrun_lora_v4' | 'brightrun_lora_v3';
  file_name: string;
  file_size: number;
}

// Zod schema for validation
import { z } from 'zod';

export const CreateDatasetSchema = z.object({
  name: z.string().min(1).max(200),
  description: z.string().optional(),
  format: z.enum(['brightrun_lora_v4', 'brightrun_lora_v3']).optional(),
  file_name: z.string().min(1).max(255),
  file_size: z.number().positive(),
});
```

---

### Feature FR-2.2: Dataset Validation

**Type:** Background Processing (Edge Function)  
**Strategy:** EXTENSION - using Supabase Edge Functions instead of BullMQ

#### Description
Automatically validate uploaded datasets for format correctness, calculate statistics (training pairs, tokens), and update the database with results. Uses Edge Functions with Cron scheduling to process datasets in the background.

#### What Already Exists (Don't Rebuild)
- ✅ Edge Functions infrastructure (Supabase)
- ✅ `datasets` table with validation fields
- ✅ `notifications` table for user alerts

#### What We're Building (New in This Prompt)
- 🆕 `supabase/functions/validate-datasets/index.ts` - Validation Edge Function

#### Implementation Details

##### Edge Function: Dataset Validation

**File:** `supabase/functions/validate-datasets/index.ts`

**Trigger:** Cron schedule (every 1 minute) or manual invocation

**Purpose:** 
- Fetch datasets with status 'validating'
- Download and parse JSONL files
- Validate BrightRun LoRA v4 format
- Calculate statistics (pairs, tokens, samples)
- Update database with results
- Create notifications for users

**Implementation:**
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

**Deployment:**
```bash
# Deploy Edge Function
supabase functions deploy validate-datasets
```

**Cron Configuration:**
Configure in Supabase Dashboard → Edge Functions → Cron Jobs:
- Function: `validate-datasets`
- Schedule: `* * * * *` (every 1 minute)
- This will automatically process datasets marked as 'validating'

---

##### React Hooks for Data Fetching

**File:** `src/hooks/use-datasets.ts`

**Purpose:** React Query hooks for dataset operations

**Implementation:**
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

**Pattern Source:** Infrastructure Inventory Section 6 - State & Data Fetching

---

##### Component: Dataset Card

**File:** `src/components/datasets/DatasetCard.tsx`

**Purpose:** Display individual dataset with status badge and actions

**Implementation:**
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

**Pattern Source:** Infrastructure Inventory Section 5 - Component Library

**Uses shadcn/ui components:**
- `Card`, `CardContent`, `CardHeader`, `CardTitle`, `CardDescription`
- `Badge`
- `Button`
- Icons from `lucide-react`

---

##### Page: Datasets List

**File:** `src/app/(dashboard)/datasets/page.tsx`

**Purpose:** Main datasets listing page with search and filters

**Implementation:**
```typescript
'use client';

import { useState } from 'react';
import { useDatasets, useDeleteDataset } from '@/hooks/use-datasets';
import { DatasetCard } from '@/components/datasets/DatasetCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Skeleton } from '@/components/ui/skeleton';
import { Plus, Search, Database } from 'lucide-react';
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

**Pattern Source:** Infrastructure Inventory Section 5 - Component Library, Section 6 - Data Fetching

**Uses:**
- React Query hooks from `use-datasets.ts`
- shadcn/ui components (Button, Input, Select, Skeleton, etc.)
- Existing DashboardLayout (from route group)

---

## ✅ Acceptance Criteria

### Functional Requirements

**FR-2.1: Dataset Upload**
- [ ] User can create dataset record via API
- [ ] Presigned upload URL is generated (1 hour expiry)
- [ ] File size validation (max 500MB) works
- [ ] Dataset record created with status 'uploading'
- [ ] Storage path (not URL) is stored in database
- [ ] User can upload file directly to Supabase Storage
- [ ] Upload confirmation triggers validation

**FR-2.2: Dataset Validation**
- [ ] Edge Function fetches datasets with status 'validating'
- [ ] Downloads and parses JSONL files correctly
- [ ] Validates BrightRun LoRA v4 format structure
- [ ] Calculates statistics (training pairs, tokens, avg)
- [ ] Updates database with validation results
- [ ] Creates notification on successful validation
- [ ] Handles validation errors gracefully

**UI Requirements**
- [ ] Datasets list page shows all user's datasets
- [ ] Search filter works
- [ ] Status filter works
- [ ] Dataset cards display correct information
- [ ] Status badges show correct colors
- [ ] Empty state displays correctly

### Technical Requirements

- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Follows existing auth patterns from E01
- [ ] Follows existing API response format
- [ ] Uses React Query correctly
- [ ] Uses shadcn/ui components correctly
- [ ] All imports resolve correctly

### Integration Requirements

- [ ] Successfully uses `requireAuth()` from E01
- [ ] Successfully queries `datasets` table from E01
- [ ] Successfully inserts into `notifications` table from E01
- [ ] Successfully uses Supabase Storage from E01
- [ ] Successfully uses type definitions from E01

---

## 🧪 Testing & Validation

### Manual Testing Steps

#### 1. API Testing - Create Dataset

```bash
# Test dataset creation
curl -X POST http://localhost:3000/api/datasets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Dataset",
    "description": "Test description",
    "file_name": "test.jsonl",
    "file_size": 1024
  }'

# Expected response:
# {
#   "success": true,
#   "data": {
#     "dataset": { ... },
#     "uploadUrl": "https://...",
#     "storagePath": "..."
#   }
# }
```

#### 2. API Testing - List Datasets

```bash
# Test listing datasets
curl http://localhost:3000/api/datasets

# Test with filters
curl "http://localhost:3000/api/datasets?status=ready&search=test"
```

#### 3. Database Verification

```sql
-- Verify dataset created
SELECT id, name, status, storage_path, created_at 
FROM datasets 
WHERE deleted_at IS NULL;

-- Verify RLS works (run as authenticated user)
SELECT * FROM datasets WHERE user_id = auth.uid();
```

#### 4. Storage Verification

- Navigate to Supabase Dashboard → Storage → `lora-datasets`
- Verify file appears after upload
- Verify file path matches `storage_path` in database

#### 5. Edge Function Testing

```bash
# Deploy Edge Function
supabase functions deploy validate-datasets

# Test manually
supabase functions invoke validate-datasets

# Check logs
supabase functions logs validate-datasets
```

#### 6. UI Testing

- Navigate to: `http://localhost:3000/datasets`
- Expected: Datasets list page displays
- Verify: Search and filter controls present
- Verify: Empty state shows if no datasets
- Test: Search functionality
- Test: Status filter dropdown
- Test: Dataset cards render correctly with status badges

#### 7. End-to-End Upload Flow

1. Create dataset record via API
2. Get presigned upload URL
3. Upload file to URL using `curl` or Postman
4. Confirm upload: `POST /api/datasets/{id}/confirm`
5. Wait 1 minute for validation Edge Function
6. Verify status changed to 'ready' or 'error'
7. Check notification created in `notifications` table

### Expected Outputs

After completing this prompt, you should have:
- [ ] All API endpoints responding correctly
- [ ] Edge Function deployed and running on Cron
- [ ] UI pages rendering without errors
- [ ] Complete upload-to-validation flow working
- [ ] Datasets visible in listing page
- [ ] Search and filters functional

---

## 📦 Deliverables Checklist

### New Files Created

**API Routes:**
- [ ] `src/app/api/datasets/route.ts` - POST (create), GET (list)
- [ ] `src/app/api/datasets/[id]/route.ts` - GET (single), DELETE
- [ ] `src/app/api/datasets/[id]/confirm/route.ts` - POST (trigger validation)

**Edge Functions:**
- [ ] `supabase/functions/validate-datasets/index.ts` - Background validation

**React Hooks:**
- [ ] `src/hooks/use-datasets.ts` - Data fetching hooks

**Components:**
- [ ] `src/components/datasets/DatasetCard.tsx` - Dataset display card

**Pages:**
- [ ] `src/app/(dashboard)/datasets/page.tsx` - Datasets list page

### Existing Files Modified

- [ ] `src/lib/types/lora-training.ts` - Add `CreateDatasetInput` interface and `CreateDatasetSchema`

### Database Changes

- [ ] No new tables (using tables from E01)
- [ ] Verify `datasets` table has correct indexes
- [ ] Verify RLS policies work correctly

### API Endpoints

- [ ] `POST /api/datasets` - Create dataset + get upload URL
- [ ] `GET /api/datasets` - List datasets with pagination
- [ ] `GET /api/datasets/[id]` - Get single dataset
- [ ] `DELETE /api/datasets/[id]` - Soft delete dataset
- [ ] `POST /api/datasets/[id]/confirm` - Trigger validation

### Edge Functions

- [ ] `validate-datasets` - Deployed and configured with Cron

### Components

- [ ] `DatasetCard` - Displays dataset with status

### Pages

- [ ] `/datasets` - List all datasets with search/filter

---

## 🔜 What's Next

### For Next Prompt in This Section

**Section Complete:** This is the final prompt in Section E02.

### For Next Section

**Next Section:** E03: Training Configuration

The next section will build upon:
- `GET /api/datasets` endpoint to fetch ready datasets
- `useDatasets()` hook to display datasets in UI
- `Dataset` type with validation status
- Dataset statistics (training_pairs, total_tokens) for job planning

Section E03 will allow users to select a validated dataset and configure training hyperparameters.

---

## ⚠️ Important Reminders

1. **Follow the Spec Exactly:** All code provided in this prompt comes from the integrated specification. Implement it as written.

2. **Reuse Existing Infrastructure:** Don't recreate what already exists. Import and use:
   - `requireAuth()` from `@/lib/supabase-server`
   - `createServerSupabaseClient()` for database queries
   - `createServerSupabaseAdminClient()` for signing operations
   - shadcn/ui components from `@/components/ui/*`
   - React Query for data fetching
   - Existing type definitions from `@/lib/types/lora-training`

3. **Storage Best Practices:**
   - **NEVER** store URLs in database - store only `storage_path`
   - Generate signed URLs on-demand via API routes
   - Use admin client for signing operations
   - Set appropriate expiry (3600 seconds = 1 hour)

4. **Integration Points:** When importing from previous work, add comments:
   ```typescript
   // From Section E01 - database schema
   import { Dataset } from '@/lib/types/lora-training';
   
   // From Section E01 - authentication
   import { requireAuth } from '@/lib/supabase-server';
   ```

5. **Pattern Consistency:** Match existing patterns:
   - API responses: `{ success: true, data }` or `{ error, details }`
   - File organization: API routes in `src/app/api/`
   - Component structure: Client components with `'use client'`
   - Hooks in `src/hooks/`

6. **Edge Function Deployment:**
   - Deploy via Supabase CLI: `supabase functions deploy validate-datasets`
   - Configure Cron in Supabase Dashboard
   - Test with: `supabase functions invoke validate-datasets`

7. **Don't Skip Steps:** Implement all features listed in this prompt before moving to the next section.

---

## 📚 Reference Materials

### Files from Previous Work

#### Section E01: Foundation & Authentication

**Database Schema:**
- `supabase/migrations/20241223_create_lora_training_tables.sql` - All tables including `datasets`

**Type Definitions:**
- `src/lib/types/lora-training.ts` - Dataset, ValidationError, and related types

**Authentication Helpers:**
- `@/lib/supabase-server` - requireAuth(), createServerSupabaseClient(), createServerSupabaseAdminClient()

**Storage Buckets:**
- `lora-datasets` bucket (private, 500MB limit)

### Infrastructure Patterns

**From Existing Codebase:**

**Authentication:**
```typescript
const { user, response } = await requireAuth(request);
if (response) return response;
```

**Database Query:**
```typescript
const supabase = await createServerSupabaseClient();
const { data, error } = await supabase.from('table').select();
```

**Storage Signing:**
```typescript
const admin = createServerSupabaseAdminClient();
const { data } = await admin.storage
  .from('bucket')
  .createSignedUploadUrl(path);
```

**API Response Format:**
```typescript
return NextResponse.json({
  success: true,
  data: { ... }
});

// Error format
return NextResponse.json({
  error: 'Error message',
  details: 'Additional details'
}, { status: 400 });
```

**React Query Pattern:**
```typescript
export function useResource() {
  return useQuery({
    queryKey: ['resource'],
    queryFn: async () => {
      const response = await fetch('/api/resource');
      if (!response.ok) throw new Error('Failed');
      return response.json();
    },
    staleTime: 30 * 1000,
  });
}
```

---

**Ready to implement Section E02, Prompt P01!**

---

## Section Completion Checklist

After completing all prompts in this section:

- [ ] All 2 features implemented (FR-2.1, FR-2.2)
- [ ] All API routes created and tested
- [ ] Edge Function deployed and running
- [ ] All React hooks working
- [ ] All components rendering correctly
- [ ] Datasets page accessible at `/datasets`
- [ ] Complete upload flow tested end-to-end
- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Integration with Section E01 verified
- [ ] Ready to proceed to Section E03

---

**End of Section E02 Execution Prompts**

