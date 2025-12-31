# Context Carryover: LoRA Pipeline Module - Structured Specification & Integration Workflow Complete

## 📌 Active Development Focus

**Primary Task**: Implement LoRA Pipeline Module into Existing Production Codebase

### Current Status: Documentation & Integration Planning Phase Complete (December 22, 2024)

---

## ✅ What Was Accomplished in This Session

### Phase 1: Progressive Structured Specification Created

We successfully transformed the unstructured LoRA Pipeline wireframe specification into a comprehensive, production-ready progressive structured specification.

**Input Document**:
- `pmc/product/_mapping/pipeline/iteration-8-LoRA-pipeline-figma-conversion.md` (3,307 lines)
- Unstructured wireframe-to-production specification

**Output Document**:
- `pmc/product/_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md` (3,437 lines)
- **Status**: ✅ COMPLETE

**What This Specification Provides**:

1. **7 Progressive Sections** - Each section builds incrementally on previous sections:
   - Section 1: Foundation & Authentication (Next.js 14, database schema, NextAuth.js)
   - Section 2: Dataset Management (upload, validation, CRUD)
   - Section 3: Training Configuration (hyperparameters, presets, cost estimation)
   - Section 4: Training Execution & Monitoring (job queue, real-time SSE, GPU cluster)
   - Section 5: Model Artifacts & Delivery (S3 storage, download, quality metrics)
   - Section 6: Cost Tracking & Notifications (real-time cost, budget alerts)
   - Section 7: Complete System Integration (validation, E2E flows, deployment)

2. **Explicit Progressive Integration**:
   - Every section explicitly references specific components/APIs from previous sections
   - Zero redundancy - no duplicated functionality
   - Clear data flow diagrams showing cross-section communication
   - Example: "Section 3 uses Dataset model from Section 2, TrainingJob model from Section 1"

3. **Production-Ready Technical Detail**:
   - Complete API schemas (request/response for 20+ endpoints)
   - Full TypeScript interfaces
   - Database schema with 12 models (User, Dataset, TrainingJob, MetricsPoint, Checkpoint, JobLog, ModelArtifact, CostRecord, Notification)
   - Wireframe-level UI specifications with ASCII diagrams
   - Component hierarchies and data flows
   - Testing strategies (unit, integration, E2E)
   - Development tasks with time estimates

4. **Complete Implementation Guidance**:
   - Estimated 152-188 hours total development time
   - 6-8 week timeline for 2-3 developers
   - Task breakdown: 30+ granular tasks (2-8 hours each)
   - Clear prerequisites and dependencies

**Key Achievement**: This specification treats the project as **greenfield** (new Next.js app from scratch), which is intentional for the next phase.

---

### Phase 2: Codebase Integration Analysis System Created

We identified a critical gap: The structured specification assumes a new project, but the LoRA Pipeline module must integrate into **existing production codebase** at `src/`.

**Problem Identified**:
- Existing codebase has authentication, database, components, APIs already built
- Structured spec would cause overwrites and breaking changes if followed literally
- Need to discover what exists, determine integration strategy, and document specific modifications

**Solution Implemented**: Two-Phase Workflow with Specialized Integration Analysis

```
Phase 1: Structured Spec (Greenfield) → Already Complete ✓
           ↓
Phase 2: Integration Analysis (New) → Workflow Created ✓
         - Discovers existing codebase
         - Compares spec vs reality  
         - Produces integration strategy
         - Documents exact modifications needed
```

---

### Phase 2 Deliverables Created

#### 1. Integration Analysis Meta-Prompt
**File**: `pmc/product/_prompt_engineering/04d-integrate-existing-codebase_v1.md` (1,508 lines)
**Status**: ✅ COMPLETE

**Purpose**: Comprehensive instructions for AI agent to analyze existing codebase and generate integration documentation.

**What It Does**:
- **Phase 1**: Comprehensive Codebase Discovery (10 analysis steps)
  - Project architecture analysis
  - Authentication system discovery
  - Database & ORM discovery  
  - API architecture discovery
  - Component library inventory
  - State management patterns
  - File storage & external services
  - Utility functions & helpers
  - Testing infrastructure
  - Environment & configuration

- **Phase 2**: Integration Strategy Development (7 strategy steps)
  - Architecture comparison (spec vs reality)
  - Integration strategies per area (USE_EXISTING | EXTEND | ADAPT | CREATE_NEW)
  - Component reuse strategy
  - Database integration strategy
  - API integration strategy
  - Routing integration strategy
  - State management integration strategy

- **Phase 3**: Implementation Deltas Specification
  - Delta for EVERY section of structured spec
  - Specific file-level modifications (SKIP | USE | EXTEND | ADAPT | CREATE)
  - Code examples showing exact changes
  - Quick reference guides
  - Developer checklists

**Output**: AI agent executing this prompt will generate 3 integration documents (~5,500-9,500 lines total).

---

#### 2. Integration Analysis Generator Script
**File**: `pmc/product/_tools/04d-generate-wireframe-integration-plan_v1.js` (486 lines)
**Status**: ✅ COMPLETE

**Purpose**: Generate executable prompt for AI agent that analyzes codebase integration.

**Usage**:
```bash
cd pmc/product/_tools
node 04d-generate-wireframe-integration-plan_v1.js "LoRA Pipeline" pipeline
```

**What It Does**:
1. Loads meta-prompt template: `04d-integrate-existing-codebase_v1.md`
2. Interactively validates paths:
   - Structured spec: `_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md`
   - Codebase directory: `../../../src`
3. Replaces placeholders with actual paths
4. Saves executable prompt to: `_mapping/pipeline/_run-prompts/04d-pipeline-integration-analysis_v1-build.md`

**Pattern**: Follows same structure as existing PMC generator scripts (00, 01, 02a, 02b).

---

#### 3. Integration Analysis Documentation
**File**: `pmc/context-ai/scratch/04d-integrate-codebase-analysis.md` (724 lines)
**Status**: ✅ COMPLETE

**Purpose**: Comprehensive analysis of integration approaches, architecture decision, and implementation plan.

**Contents**:
- Analysis of 5 different integration approaches (Option 1-5)
- Comparison matrix with scoring (complexity, maintainability, reliability, etc.)
- Recommended solution: Option 5 (Two-Phase Workflow)
- Context window analysis (shows it fits within 1M token limit)
- Risk assessment and mitigations
- Success criteria
- Implementation timeline (~15 hours)

**Key Recommendation**: Two-phase workflow where structured spec stays greenfield, and integration analysis is a separate focused step.

---

#### 4. Quick Start Guide
**File**: `pmc/product/_tools/QUICKSTART-integration-analysis.md` (480 lines)
**Status**: ✅ COMPLETE

**Purpose**: Step-by-step guide for using the codebase integration workflow.

**Contents**:
- Complete workflow diagram
- Step-by-step execution guide
- Command reference
- Troubleshooting
- Best practices
- File locations reference

---

### Phase 2 Generated Documents (Already Created by AI Agent)

These were generated during testing of the integration workflow:

#### 1. Codebase Discovery Document
**File**: `pmc/product/_mapping/pipeline/_run-prompts/04d-codebase-discovery_v1.md` (1,715 lines)
**Status**: ✅ COMPLETE

**What It Contains**:
- Complete analysis of existing `src/` codebase
- Authentication: Supabase Auth (not NextAuth.js as spec assumes)
- Database: Drizzle ORM with PostgreSQL (not Prisma as spec assumes)
- API patterns: Next.js API routes with existing conventions
- Component library: shadcn/ui components already available
- State management: SWR for data fetching
- File storage: Supabase Storage already configured
- Complete inventory of reusable components, hooks, utilities

**Key Findings**:
- 4 database models already exist (users, conversations, training_files, etc.)
- Authentication system fully implemented with Supabase
- S3-compatible storage (Supabase Storage) already working
- Many UI components from spec already exist

---

#### 2. Integration Strategy Document
**File**: `pmc/product/_mapping/pipeline/_run-prompts/04d-integration-strategy_v1.md` (1,170 lines)
**Status**: ✅ COMPLETE

**What It Contains**:
- Strategic decisions for each integration area:
  - **Authentication**: USE_EXISTING (Supabase Auth, not NextAuth.js)
  - **Database**: EXTEND (add 8 new models to existing Drizzle schema)
  - **API**: CREATE_NEW + EXTEND (new endpoints, match existing patterns)
  - **Components**: REUSE + CREATE (reuse UI library, create new feature components)
  - **Storage**: USE_EXISTING (Supabase Storage already configured)
  - **State**: USE_EXISTING (SWR pattern already established)

- Risk assessment per area (LOW/MEDIUM/HIGH)
- Implementation phases with time estimates
- Validation checklist
- Breaking change analysis

**Critical Decisions Documented**:
- Skip NextAuth.js implementation - use existing Supabase Auth
- Skip Prisma setup - extend existing Drizzle schema
- Skip S3 client setup - use existing Supabase Storage
- Reuse existing UI components where possible
- Match existing API response formats

---

#### 3. Implementation Deltas Document
**File**: `pmc/product/_mapping/pipeline/_run-prompts/04d-implementation-deltas_v1.md` (NOT YET CREATED)
**Status**: ⚠️ PENDING (to be generated when full analysis runs)

**What It Will Contain**:
- Delta for EVERY section of structured spec (Sections 1-7)
- Specific modifications required:
  - **SKIP**: Files NOT to create (already exist)
  - **USE**: Existing files/functions to use instead
  - **EXTEND**: Files to modify with exact changes
  - **CREATE**: New files to create per spec
- Code examples showing exact changes
- Quick reference sections for developers
- Implementation checklist

**Usage During Development**:
Developer reads structured spec section → checks corresponding delta section → applies modifications → implements with integration awareness.

---

## 🎯 What Happens Next: Implementation Phase

### The Complete Workflow (All Steps)

```
┌─────────────────────────────────────────────────────────────┐
│ COMPLETED: Structured Specification (Greenfield)            │
│ File: 04c-pipeline-structured-from-wireframe_v1.md          │
│ Purpose: Complete feature specification (what to build)     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ COMPLETED: Integration Analysis System                      │
│ - Meta-prompt: 04d-integrate-existing-codebase_v1.md        │
│ - Generator: 04d-generate-wireframe-integration-plan_v1.js  │
│ - Documentation: Analysis + Quick Start guides              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ COMPLETED (PARTIAL): Integration Documents Generated        │
│ ✅ 04d-codebase-discovery_v1.md (1,715 lines)               │
│ ✅ 04d-integration-strategy_v1.md (1,170 lines)             │
│ ⚠️  04d-implementation-deltas_v1.md (PENDING)               │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ NEXT: Development & Implementation                          │
│ Developer uses ALL documents:                               │
│ 1. Structured spec (what to build)                          │
│ 2. Codebase discovery (what exists)                         │
│ 3. Integration strategy (how to integrate)                  │
│ 4. Implementation deltas (modifications required)           │
│                                                              │
│ Implements section-by-section with integration awareness    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Critical Files for Next Agent to Internalize

### PHASE A: Context Internalization (DO THIS FIRST - DO NOT SKIP)

**CRITICAL**: The next agent MUST internalize all context before receiving any implementation instructions. This is mandatory.

#### 1. Primary Specification Document
**File**: `pmc/product/_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md` (3,437 lines)
**Purpose**: Complete structured specification of LoRA Pipeline module
**Time to Read**: 3-4 hours
**Focus Areas**:
- Section structure and progressive building approach
- Database schema (12 models)
- API endpoints (20+ endpoints with schemas)
- UI pages (P01-P05) with component hierarchies
- Integration points between sections

#### 2. Integration Strategy Document
**File**: `pmc/product/_mapping/pipeline/_run-prompts/04d-integration-strategy_v1.md` (1,170 lines)
**Purpose**: How new module integrates with existing codebase
**Time to Read**: 2-3 hours
**Focus Areas**:
- Architecture comparison (spec assumptions vs codebase reality)
- Strategic decisions per area (USE_EXISTING | EXTEND | ADAPT | CREATE_NEW)
- Risk assessment
- Implementation phases

#### 3. Codebase Discovery Document
**File**: `pmc/product/_mapping/pipeline/_run-prompts/04d-codebase-discovery_v1.md` (1,715 lines)
**Purpose**: Complete analysis of what exists in current codebase
**Time to Read**: 2-3 hours
**Focus Areas**:
- Authentication: Supabase Auth implementation
- Database: Drizzle ORM with existing tables
- Components: Available shadcn/ui components
- APIs: Existing endpoint patterns
- Storage: Supabase Storage setup

#### 4. Integration Workflow Documentation
**File**: `pmc/product/_tools/QUICKSTART-integration-analysis.md` (480 lines)
**Purpose**: Understanding the two-phase workflow
**Time to Read**: 30 minutes
**Focus Areas**:
- How structured spec + integration docs work together
- Implementation workflow (read spec → check deltas → code)
- Best practices

#### 5. Generator Script (Pattern Reference)
**File**: `pmc/product/_tools/04d-generate-wireframe-integration-plan_v1.js` (486 lines)
**Purpose**: Understanding how integration prompts are generated
**Time to Read**: 30 minutes
**Focus Areas**:
- Path validation patterns
- Placeholder replacement logic
- Interactive prompt workflow

#### 6. Meta-Prompt (Architecture Reference)
**File**: `pmc/product/_prompt_engineering/04d-integrate-existing-codebase_v1.md` (1,508 lines)
**Purpose**: Understanding the comprehensive integration analysis process
**Time to Read**: 2 hours
**Focus Areas**:
- 10-step codebase discovery process
- 7-step integration strategy development
- Implementation deltas specification structure

#### 7. Production Codebase (Critical)
**Directory**: `src/` (entire directory)
**Purpose**: Understanding existing implementation to avoid overwrites
**Time to Analyze**: 4-6 hours
**Focus Areas**:
- `/app/api/` - Existing API routes and patterns
- `/app/components/` - Existing UI components
- `/lib/` - Utilities, database client, storage client
- `/lib/supabase/` - Supabase integration (auth, database)
- `/hooks/` - Custom React hooks
- `/types/` - TypeScript definitions
- Service files:
  - `conversation-generation-service.ts`
  - `enrichment-pipeline-orchestrator.ts`
  - `training-file-service.ts`

**IMPORTANT**: The codebase analysis is NOT optional. The next agent MUST understand:
- What authentication system exists (Supabase Auth)
- What database ORM is used (Drizzle, not Prisma)
- What components are already available
- What API patterns are established
- What storage system is configured

**Total Internalization Time: 15-20 hours** (This is intentional and necessary to avoid breaking changes)

---

### PHASE B: Wait for Explicit Human Instructions

**CRITICAL**: After completing Phase A (context internalization), the next agent MUST **STOP and WAIT** for explicit human instructions.

**DO NOT**:
- ❌ Start implementing any features
- ❌ Create any new files
- ❌ Modify any existing files
- ❌ Run any migrations
- ❌ Install any packages
- ❌ Make any code changes
- ❌ "Fix" or "improve" anything
- ❌ Generate the missing implementation deltas document
- ❌ Make suggestions or recommendations

**ONLY DO**:
- ✅ Read and internalize all documents listed in Phase A
- ✅ Understand the two-phase workflow (structured spec + integration)
- ✅ Understand existing codebase architecture
- ✅ Understand integration strategies decided upon
- ✅ Confirm context internalization is complete
- ✅ Wait for human to provide specific implementation instructions

**Why This Matters**:
- The structured spec + integration strategy represent ~10,000 lines of documentation
- Rushing into implementation without full context leads to:
  - Breaking changes (overwriting shared code)
  - Duplicate functionality (recreating what exists)
  - Pattern inconsistency (not matching existing conventions)
  - Integration failures (missing dependencies)
  - Technical debt (divergent implementations)

---

## 🔍 Integration Strategy Summary (Key Decisions)

For quick reference, these are the major integration decisions already made in the strategy document:

### Authentication & Authorization
- **Decision**: USE_EXISTING (Supabase Auth)
- **Rationale**: Supabase Auth fully functional, used by existing modules
- **Impact**: Skip NextAuth.js implementation in structured spec Section 1
- **Modification**: Adapt API auth middleware to use Supabase session checking

### Database & ORM
- **Decision**: EXTEND (Drizzle ORM)
- **Rationale**: Drizzle already configured, 4 models already exist
- **Impact**: Skip Prisma setup, extend existing schema
- **Modification**: 
  - Add 8 new tables (datasets, training_jobs, metrics_points, checkpoints, job_logs, model_artifacts, cost_records, notifications)
  - Extend users table with subscription fields
  - Create Drizzle migration files (not Prisma)

### API Architecture
- **Decision**: CREATE_NEW + MATCH_PATTERNS
- **Rationale**: New endpoints needed, must match existing conventions
- **Impact**: Create new API routes per spec, use existing response formats
- **Modification**: Adapt spec's error responses to match existing format

### Component Library
- **Decision**: REUSE + CREATE
- **Rationale**: shadcn/ui already available, many components exist
- **Impact**: Reuse existing UI components, create only feature-specific components
- **Modification**: 
  - Reuse: Button, Card, Dialog, Input, Select, Slider, Tabs (from existing)
  - Create: DatasetCard, PresetSelector, LossCurveGraph, QualityMetricsCard (new)

### File Storage
- **Decision**: USE_EXISTING (Supabase Storage)
- **Rationale**: Supabase Storage already configured and working
- **Impact**: Skip S3 client setup in spec Section 2
- **Modification**: Use existing `/lib/storage.ts`, extend with dataset-specific functions

### State Management
- **Decision**: USE_EXISTING (SWR)
- **Rationale**: SWR already used for data fetching
- **Impact**: Use SWR for all new API data fetching
- **Modification**: Follow existing SWR patterns in codebase

### Job Queue & Background Processing
- **Decision**: CREATE_NEW (BullMQ + Redis)
- **Rationale**: No existing job queue system
- **Impact**: Implement as specified in Section 4
- **Modification**: None - implement as greenfield

---

## 📋 Document Hierarchy & Usage

When the human provides implementation instructions, the next agent should reference documents in this order:

### During Feature Implementation:

```
1. READ: Structured Spec Section [N]
   └─ Understand: What features to build, APIs to create, UI to design
   
2. READ: Integration Strategy for Section [N] area
   └─ Understand: Strategic decision (USE_EXISTING | EXTEND | CREATE_NEW)
   
3. READ: Implementation Deltas for Section [N] (when available)
   └─ Understand: Specific file modifications (SKIP | USE | EXTEND | CREATE)
   
4. READ: Codebase Discovery for relevant area
   └─ Understand: What already exists, where it is, how it works
   
5. IMPLEMENT: Code with integration awareness
   └─ Action: Write code following deltas, reusing existing infrastructure
   
6. TEST: Both new features AND existing features
   └─ Validate: No breaking changes, integration working correctly
```

### Quick Reference Chain:

```
Structured Spec → "Build feature X with API Y and UI Z"
        ↓
Integration Strategy → "Use existing Auth, extend DB, create new API"
        ↓
Implementation Deltas → "Skip auth.ts, extend schema, create api/datasets/"
        ↓
Codebase Discovery → "Auth at /lib/supabase/auth.ts, DB at /lib/db.ts"
        ↓
Implementation → Code that integrates correctly
```

---

## 🔍 Supabase Agent Ops Library (SAOL) Quick Reference

**Version:** 2.1 (Bug Fixes Applied - December 6, 2025)

### Setup & Usage

**Installation**: Already available in project
```bash
# SAOL is installed and configured
# Located in supa-agent-ops/ directory
```

**CRITICAL: You MUST use the Supabase Agent Ops Library (SAOL) for ALL database operations.**  
Do not use raw `supabase-js` or PostgreSQL scripts. SAOL is safe, robust, and handles edge cases for you.

**Library Path:** `C:\Users\james\Master\BrightHub\brun\lora-pipeline\supa-agent-ops\`  
**Quick Start:** `C:\Users\james\Master\BrightHub\brun\lora-pipeline\supa-agent-ops\QUICK_START.md` (READ THIS FIRST)  
**Troubleshooting:** `C:\Users\james\Master\BrightHub\brun\lora-pipeline\supa-agent-ops\TROUBLESHOOTING.md`

### Key Rules
1. **Use Service Role Key:** Operations require admin privileges. Ensure `SUPABASE_SERVICE_ROLE_KEY` is loaded.  
2. **Run Preflight:** Always run `agentPreflight({ table })` before modifying data.  
3. **No Manual Escaping:** SAOL handles special characters automatically.
4. **Parameter Flexibility:** SAOL accepts both `where`/`column` (recommended) and `filters`/`field` (backward compatible).

### Quick Reference: One-Liner Commands

**Note:** All examples updated for SAOL v2.1 with bug fixes applied.

```bash
# Query conversations (all columns)
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'conversations',limit:5});console.log('Success:',r.success);console.log('Count:',r.data.length);console.log(JSON.stringify(r.data,null,2));})();"

# Check schema (Deep Introspection)
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentIntrospectSchema({table:'conversations',transport:'pg'});console.log(JSON.stringify(r,null,2));})();"
```

### Common Queries

**Check conversations (specific columns, with filtering)**:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'conversations',select:'id,conversation_id,enrichment_status,title',where:[{column:'enrichment_status',operator:'eq',value:'completed'}],orderBy:[{column:'created_at',asc:false}],limit:10});console.log('Success:',r.success,'Count:',r.data.length);r.data.forEach(c=>console.log('-',c.conversation_id.slice(0,8),'/',c.enrichment_status));})();"
```

**Check training files**:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'training_files',select:'id,name,conversation_count,total_training_pairs,created_at',orderBy:[{column:'created_at',asc:false}],limit:5});console.log('Files:',r.data.length);r.data.forEach(f=>console.log('-',f.name,'(',f.conversation_count,'convs)'));})();"
```

**Check prompt templates (edge case tier)**:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'prompt_templates',select:'template_name,tier,emotional_arc_type',where:[{column:'tier',operator:'eq',value:'edge_case'}]});console.log('Edge case templates:',r.data.length);r.data.forEach(t=>console.log('-',t.template_name));})();"
```

**Check emotional arcs (edge case tier)**:
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'emotional_arcs',select:'arc_key,name,tier',where:[{column:'tier',operator:'eq',value:'edge_case'}]});console.log('Edge case arcs:',r.data.length);r.data.forEach(a=>console.log('-',a.arc_key,'→',a.name));})();"
```

### SAOL Parameter Formats (Both Work)

**Recommended Format** (clear intent):
```javascript
const result = await saol.agentQuery({
  table: 'prompt_templates',
  select: ['template_name', 'tier', 'emotional_arc_type'],  // Array
  where: [{ column: 'tier', operator: 'eq', value: 'edge_case' }],  // where + column
  orderBy: [{ column: 'created_at', asc: false }]
});
```

**Backward Compatible Format**:
```javascript
const result = await saol.agentQuery({
  table: 'prompt_templates',
  select: 'template_name,tier,emotional_arc_type',  // String
  filters: [{ field: 'tier', operator: 'eq', value: 'edge_case' }],  // filters + field
  orderBy: [{ column: 'created_at', asc: false }]
});
```

---

## 📋 Project Functional Context

### What This Application Does

**Bright Run LoRA Training Data Platform** - A Next.js 14 application that generates high-quality AI training conversations for fine-tuning large language models. The platform enables non-technical domain experts to transform proprietary knowledge into LoRA-ready training datasets.

**Core Capabilities**:
1. **Conversation Generation**: AI-powered generation using Claude API with predetermined field structure
2. **Enrichment Pipeline**: 5-stage validation and enrichment process for quality assurance
3. **Storage System**: File storage (Supabase Storage) + metadata (PostgreSQL)
4. **Management Dashboard**: UI for reviewing, downloading, and managing conversations
5. **Download System**: Export both raw (minimal) and enriched (complete) JSON formats

### Core Workflow

```
User → Generate Conversation → Claude API → Raw JSON Stored →
Enrichment Pipeline (5 stages) → Enriched JSON Stored →
Dashboard View → Download (Raw or Enriched) → Combine Multiple JSON files into a full training file.
```

### Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage (buckets: conversation-files, training-files)
- **AI**: Claude API (Anthropic) - `claude-sonnet-4-5-20250929`
- **Structured Outputs**: `anthropic-beta: structured-outputs-2025-11-13`
- **UI**: Shadcn/UI + Tailwind CSS
- **Deployment**: Vercel

### Production Pipeline (FULLY WORKING)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. SCAFFOLDING SELECTION                                    │
│    - Personas, Emotional Arcs, Training Topics              │
│    → Stored in database tables                              │
│    ✅ Working for all tiers                                 │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. CONVERSATION GENERATION (Claude API)                     │
│    → conversation-generation-service.ts                     │
│    → Output: Raw JSON with turns[]                          │
│    → Stored in: conversation-files/{userId}/{id}/raw.json   │
│    ✅ Working for ALL tiers (template + edge_case)          │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. ENRICHMENT (Metadata Addition)                           │
│    → enrichment-pipeline-orchestrator.ts                    │
│    → conversation-enrichment-service.ts                     │
│    → Output: Enriched JSON with training_pairs[]            │
│    → Stored in: conversation-files/{userId}/{id}/enriched.json│
│    ✅ Working                                                │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. TRAINING FILE AGGREGATION                                │
│    → training-file-service.ts                               │
│    → Combines multiple enriched files into one              │
│    → Output: Full JSON + JSONL in brightrun-lora-v4 format  │
│    → Stored in: training-files/{fileId}/training.json       │
│    ✅ Working (create + add conversations)                  │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema Overview

**Core Tables**:
- `conversations` - Conversation metadata and status (has `id` PK and `conversation_id` business key)
- `training_files` - Aggregated training file metadata
- `training_file_conversations` - Junction table linking conversations to training files
- `personas` - Client personality profiles (3 active)
- `emotional_arcs` - Emotional progression patterns (10 total: 7 template, 3 edge_case)
- `training_topics` - Subject matter configuration (many active)
- `prompt_templates` - Generation templates (10 total: 7 template tier, 3 edge_case tier)
- `batch_jobs` - Batch generation job tracking
- `batch_items` - Individual items in batch jobs
- `failed_generations` - Failed generation error records

---

## 📊 What the Next Agent Should Expect

When the human provides implementation instructions, expect one of these scenarios:

### Scenario 1: Complete Implementation Deltas Generation
**Task**: Generate the missing implementation deltas document
**Input**: Structured spec + codebase discovery + integration strategy
**Output**: `04d-implementation-deltas_v1.md` with section-by-section deltas
**Time**: 6-8 hours of AI processing

### Scenario 2: Section-by-Section Implementation
**Task**: Implement specific section(s) of the LoRA Pipeline module
**Example**: "Implement Section 2: Dataset Management"
**Process**:
1. Read Section 2 in structured spec
2. Check integration strategy for Section 2 decisions
3. Reference codebase discovery for what exists
4. Implement with integration awareness
5. Test new features + existing features
6. Document deviations

### Scenario 3: Specific Feature Implementation
**Task**: Implement specific feature crossing multiple sections
**Example**: "Implement dataset upload and validation flow"
**Process**:
1. Identify relevant sections (Section 2 in this case)
2. Follow same process as Scenario 2
3. Ensure cross-section integration works

### Scenario 4: Integration Issue Resolution
**Task**: Fix integration issues or breaking changes
**Example**: "Existing auth not working with new APIs"
**Process**:
1. Reference integration strategy decisions
2. Check codebase discovery for actual implementation
3. Identify misalignment
4. Propose fix respecting existing patterns

---

## ⚠️ Critical Reminders for Next Agent

1. **DO NOT assume the structured spec applies exactly as written** - Always check integration strategy and deltas first

2. **DO NOT overwrite shared code** - Many files exist and are used by other modules. Check codebase discovery.

3. **DO NOT create duplicate functionality** - If something exists (auth, storage, components), reuse it.

4. **DO NOT deviate from existing patterns** - Match API response formats, component patterns, naming conventions.

5. **DO test existing features after changes** - Breaking changes are the #1 risk in integration.

6. **DO ask questions if unclear** - Better to clarify integration strategy than make wrong assumptions.

7. **DO reference specific document sections** - When discussing implementation, cite: "Section 2, FR-2.3.1 says X, but Integration Strategy says Y, so we do Z"

8. **DO maintain traceability** - Document why you deviated from spec (because integration strategy said to)

---

**Last Updated**: December 22, 2024  
**Session Focus**: LoRA Pipeline - Structured Specification & Integration Workflow Complete  
**Current State**: Documentation phase complete, ready for implementation phase with full integration awareness  
**Document Version**: qq (LoRA Pipeline - Spec + Integration System Complete)  
**Next Phase**: Implementation (awaiting human instructions)

