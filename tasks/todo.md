# Task: Update Integration Meta-Prompt v1 → v2

## Problem Analysis

The current meta-prompt (`04d-integrate-existing-codebase_v1.md`) has a fundamental defect:
- It frames "integration" as **merging two independent applications**
- When run, it produces analysis saying "INTEGRATION NOT VIABLE - build separately"
- But the user's intent is: **build a new module that sits alongside existing code with direct access to objects, artifacts, and interfaces**

### Core Issue
The v1 meta-prompt leads to:
1. Discovery that identifies "incompatibilities" (Prisma vs Supabase, NextAuth vs Supabase Auth)
2. Strategy that recommends building separately
3. Conclusion that these are "different apps"

### User's Actual Intent
When user says "integrate" they mean:
- New module **sits alongside** existing code
- New module **uses existing infrastructure** (auth, DB, storage, components)
- Module functions **holistically** with existing system
- NOT replacing infrastructure, just ADDING new features

## Solution Approach

Create v2 meta-prompt that:
1. **Reframes the goal** - Not "merge two apps" but "add a module that extends the existing app"
2. **Different discovery focus** - "What infrastructure can the new module USE?" vs "What are the mismatches?"
3. **Assumes coexistence** - New module WILL use existing auth, DB client, storage
4. **Extension-focused output** - What to ADD (new tables, APIs, components) using existing patterns

## TODO Items

- [x] Read and analyze input file (update-integration-meta-prompt_v1.md)
- [x] Read context carry file for background
- [x] Read "why incompatible" explanation to understand the problem
- [x] Read current meta-prompt v1 (04d-integrate-existing-codebase_v1.md)
- [x] Read generator script for context
- [x] Read generated output files to see what v1 produced
- [x] Analyze defects in current meta-prompt framing
- [x] Write new meta-prompt v2 with corrected framing
- [x] Save to: `pmc/product/_prompt_engineering/04d-integrate-existing-codebase_v2.md`

---

## COMPLETED

**Output File**: `pmc/product/_prompt_engineering/04d-integrate-existing-codebase_v2.md`

### Summary of Changes (v1 → v2)

| Aspect | v1 (Defective) | v2 (Fixed) |
|--------|----------------|------------|
| **Title** | "Codebase Integration Analysis" | "Module Extension Blueprint" |
| **Goal** | Compare two apps for compatibility | Add features to existing app |
| **Discovery Focus** | Find "mismatches" and "incompatibilities" | Inventory what exists TO USE |
| **Strategy** | Decide USE_EXISTING vs CREATE_NEW per area | Always USE_EXISTING infrastructure |
| **Output** | "Integration Strategy" with option to build separately | "Extension Strategy" - module WILL be added |
| **Language** | "integrate", "mismatch", "incompatible" | "add", "extend", "use existing" |
| **Spec Treatment** | Compare spec's tech stack to codebase | Extract FEATURES only, ignore spec's infrastructure |
| **Final Recommendation** | May recommend building separately | Module IS being added, no alternatives |

### Key New Sections in v2

1. **CRITICAL FRAMING** - Explicit statement that this is EXTENSION not integration comparison
2. **How to Read the Spec** - Extract WHAT to build, ignore HOW
3. **Infrastructure Inventory** - Document what exists FOR the new module to USE
4. **Infrastructure Mapping** - How new module USES each existing component
5. **Implementation Guide** - Exact, copy-pasteable code following existing patterns
6. **REMEMBER section** - Final reminder that module WILL be added

### Files Changed
- Created: `pmc/product/_prompt_engineering/04d-integrate-existing-codebase_v2.md`

---

**Status**: COMPLETE

---
---

# Task 2: Raw Spec and Integration Specs Segmentation

## Problem Analysis

The user needs to understand how the three integration documents relate to the original structured specification and how to produce execution prompts that build progressively.

### Key Questions
1. Do the three integration docs REPLACE or SUPPLEMENT the structured spec?
2. How to produce prompts that build progressively within and between sections?
3. How to handle the relationship between integration knowledge and structured spec when segmenting?

## TODO Items

- [x] Read and analyze the task file (raw-spec-and-integration-specs-segmentation_v1.md)
- [x] Read the three integration output documents
- [x] Read the original structured spec (04c) - structure
- [x] Read the deprecated segmentation script
- [x] Read example execution prompt
- [x] Analyze relationships and write solution document

---

## COMPLETED

**Output File**: `pmc/product/_mapping/pipeline/workfiles/spec-integration-segmentation-solution_v1.md`

### Key Findings

1. **Integration docs SUPPLEMENT, don't replace**: The structured spec defines WHAT to build; the integration docs define HOW to build using existing infrastructure

2. **Two-stage pipeline needed**:
   - **Stage 1 (Merge)**: Combine structured spec with integration knowledge → Integrated Extension Spec
   - **Stage 2 (Segment)**: Segment integrated spec into progressive execution prompts

3. **Progressive dependencies**:
   - **Intra-section**: Database → API → UI → Integration
   - **Inter-section**: E01 → E02 → E03 → ... with clear dependency chains

### Solution Architecture

```
Structured Spec + Integration Docs
        ↓ (Merge)
Integrated Extension Spec (04e)
        ↓ (Segment)
Execution Prompts (04f-E[XX]-P[YY])
```

### Next Steps

1. Create `04e-merge-integration-spec-meta-prompt_v1.md`
2. Create `04e-merge-integration-spec_v1.js` script
3. Run merge to produce integrated spec
4. Create `04f-segment-integrated-spec_v1.js` script
5. Run segmentation to produce execution prompts

---

**Status**: COMPLETE

---
---

# Task 3: E04 RunPod Architecture Analysis & Implementation

## Problem Analysis

The user needs to implement a complete LoRA training pipeline that connects their Vercel-hosted Next.js application to RunPod for GPU-accelerated training of Qwen3-Next-80B-A3B models. Key questions include:

1. Serverless vs Private Pod for training
2. How LoRA training actually works (frozen base + adapters)
3. Best architecture for Qwen 80B training
4. How to obtain GPU_CLUSTER_API_URL and GPU_CLUSTER_API_KEY
5. Cost optimization strategies
6. Technical requirements for training large MoE models

### Key Findings from Research

1. **Serverless vs Pods**: Use **Pods** for multi-hour training jobs (cheaper), **Serverless** for inference/deployment (autoscaling)
2. **LoRA Works on Qwen3-80B**: Confirmed via PEFT library, ms-swift framework, and community success reports
3. **Architecture**: Vercel → RunPod Serverless Custom Worker → Network Volume (cached model) → Supabase Storage
4. **API Credentials**: Created by deploying custom Docker image as RunPod Serverless Endpoint
5. **Cost**: Pods ~$1.99-2.39/hr (H100), Serverless ~$3.35-4.18/hr but only charges during processing

### Conflicting Guidance Resolution

- **Gemini**: Recommended Serverless for training (auto-shutdown benefit)
- **Perplexity**: Recommended Pods for training (cheaper for long jobs)
- **Resolution**: Both are VALID approaches. For **automated pipelines**, Serverless is better (zero idle cost risk, programmatic triggering). For **interactive/experimental** work, Pods are cheaper.

## TODO Items

- [x] Read and analyze input file (04f-pipeline-build-section-E04-runpod-scope-input_v1.md)
- [x] Read Gemini architecture guide
- [x] Read Perplexity architecture guide
- [x] Explore current codebase for training infrastructure
- [x] Search web for current RunPod pricing, Qwen LoRA support, serverless vs pods
- [x] Analyze existing training job infrastructure in codebase
- [x] Resolve conflicting guidance from multiple sources
- [x] Write Deliverable 1: Detailed Analysis (non-ML-engineer readable)
- [x] Write Deliverable 2: Implementation Instructions (RunPod ops + agent prompt)

---

## DELIVERABLES

### Deliverable 1
**File**: `pmc/product/_mapping/pipeline/full-build/04f-pipeline-build-section-E04.5-runpod-analysis.md`
- Full analysis answering all 10 questions
- Written for non-ML engineers
- Reconciles conflicting guidance
- Provides clear recommendations

### Deliverable 2
**File**: `pmc/product/_mapping/pipeline/full-build/04f-pipeline-build-section-E04.5-runpod-instructions.md`
- Section 1: Manual RunPod setup steps for human engineer
- Section 2: Autonomous coding agent prompt for implementation

---

**Status**: COMPLETE

### Summary of Deliverables

| Deliverable | Location | Content |
|-------------|----------|---------|
| **Analysis Document** | `04f-pipeline-build-section-E04.5-runpod-analysis.md` | Complete answers to all 10 questions, conflicting guidance resolution, codebase analysis |
| **Implementation Guide** | `04f-pipeline-build-section-E04.5-runpod-instructions.md` | Section 1: Manual RunPod setup steps; Section 2: Autonomous agent prompt |

### Key Findings Summary

1. **Architecture Decision:** Use RunPod Serverless Custom Workers for automated training pipeline
2. **LoRA on Qwen3-80B:** Confirmed working with QLoRA (4-bit quantization) via PEFT library
3. **Cost Optimization:** Serverless eliminates idle cost risk; ~$13-14 per 4-hour training run
4. **Missing Components:** Docker image, RunPod endpoint deployment, API credentials in .env.local

### Next Steps for Human Engineer

1. Create Network Volume and pre-download Qwen model
2. Build Docker image from agent-generated code
3. Deploy Serverless Endpoint
4. Copy credentials to .env.local and Supabase secrets
5. Test end-to-end with small dataset
