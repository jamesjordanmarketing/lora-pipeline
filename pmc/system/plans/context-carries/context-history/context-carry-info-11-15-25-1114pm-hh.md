# Context Carryover: Lead Magnet Strategy for Training Dataset

## 📌 Active Development Focus

**Primary Task**: Design and Implement Hugging Face Lead Magnet Strategy

### Current Status: Strategy Planning Phase

**What Was Completed** (December 6-8, 2025):
1. ✅ Fixed edge case prompt template generation (3 templates created and inserted)
2. ✅ All 10 prompt templates now exist in database (7 template tier + 3 edge_case tier)
3. ✅ Full production dataset generated: **242 conversations, 1,567 training pairs**
4. ✅ Dataset exported to JSON format and ready for distribution

**What's Next** (For This Agent):
- Design a Hugging Face lead magnet strategy for the training dataset
- Determine optimal sample size for HF preview vs. landing page download
- Create dataset packaging for distribution tiers
- Evaluate owner's preference for full giveaway vs. tiered access

---

## 🗂️ Current Dataset Specifications

### Production Dataset Location
**File Path**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\_archive\full-file-training-json-242-conversations.json`

### Dataset Statistics
| Metric | Value |
|--------|-------|
| **Total Lines** | 134,000 |
| **Total Conversations** | 242 |
| **Total Training Pairs** | 1,567 |
| **Format Version** | brightrun-lora-v4 |
| **Target Model** | claude-sonnet-4-5 |
| **Vertical** | financial_planning_consultant |

### Scaffolding Distribution

**Personas** (3 types):
- `anxious_planner`: 80 conversations
- `overwhelmed_avoider`: 79 conversations
- `pragmatic_optimist`: 83 conversations

**Emotional Arcs** (7 types used):
- `couple_conflict_to_alignment`: 59 conversations
- `confusion_to_clarity`: 60 conversations
- `overwhelm_to_empowerment`: 42 conversations
- `shame_to_acceptance`: 42 conversations
- `hostility_to_boundary`: 13 conversations (edge case)
- `overwhelm_to_triage`: 13 conversations (edge case)
- `crisis_to_referral`: 13 conversations (edge case)

**Training Topics**: 17+ unique financial planning topics including:
- Mortgage payoff strategy, estate planning, career changes
- Roth IRA conversion, student loans, eldercare costs
- ESG investing, tax loss harvesting, and more

### Data Quality
- Average quality score: 3/5 (AI-generated, not human-reviewed)
- Human reviewed: 0%
- Ready for: LoRA fine-tuning experiments

---

## 🎯 Lead Magnet Strategy Context

### Previous Analyst Recommendation: "The Billboard" Strategy

A previous analyst recommended a 3-tier funnel:

1. **Hugging Face Preview** ("The Menu")
   - Upload a sample dataset to HF
   - Use Dataset Card (README) to drive traffic to landing page
   - Enough data to look legitimate, not enough for training

2. **Landing Page Reward** ("The Appetizer")
   - Gated download of "EQ-100" file
   - Useful for testing, gets users hooked
   - Requires email capture

3. **Paid Product** ("The Meal")
   - Full dataset or custom generation service
   - The actual revenue generator

**Analyst's Sample Size Guidance** (for 1,567 total pairs):
- Give enough data so HF viewer doesn't look empty/broken
- Don't give enough for a valid training run
- Give enough to prove real data exists, force click to landing page

### Owner's Current Preference

The owner prefers a **different strategy for this iteration**:

> "For this iteration of the marketing campaign we should give away the full 242 conversations. This is because this is the first iteration of our data set and feedback from users is just as valuable as a 'sale'. Also our true product is the ability to create lots of conversations quickly, including more advanced types and uses. So I would rather we become very popular as quickly as possible for this iteration. In future higher quality iterations we can implement more gates."

**Owner's Concerns**:
- Doesn't want prospects to think the company is desperate
- Doesn't want to appear as a commodity
- Values feedback over sales for this iteration
- Sees the platform capability (not the dataset) as the true product

### Strategic Decision Needed

The next agent should consider:

1. **Full Giveaway Pros**:
   - Maximum adoption and visibility
   - User feedback is valuable for iteration
   - Demonstrates platform capability
   - Builds community and trust quickly

2. **Full Giveaway Cons**:
   - No email capture mechanism
   - No conversion funnel established
   - Harder to monetize later if precedent is "free"
   - May devalue perceived worth

3. **Hybrid Option** (Potential Recommendation):
   - Full dataset on Hugging Face (owner's preference)
   - BUT require GitHub star, follow, or minor social action
   - OR include prominent CTAs in README for feedback/survey
   - Capture value through community building, not gating

---

## 📚 Required Reading for Next Agent

### 1. Product Overview Document
**REQUIRED**: Read the full product overview to understand the platform's value proposition:
`C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\01-bmo-overview-full-brun-product.md`

This document explains:
- The BrightRun platform vision
- How conversation generation works
- The true product (platform capability, not just datasets)
- Target market and use cases

### 2. Codebase Familiarization
**REQUIRED**: Review the application codebase to understand current functionality:
`C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`

Key directories:
- `src/app/` - Next.js App Router pages and API routes
- `src/lib/services/` - Core services (generation, enrichment, training files)
- `src/components/` - UI components
- `src/lib/types/` - TypeScript type definitions

### 3. Dataset File
**Reference**: The actual training dataset (do not read fully, it's 134K lines):
`C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\_archive\full-file-training-json-242-conversations.json`

---

## 🎯 Session Accomplishments (December 6-8, 2025)

### Edge Case Template Implementation ✅

**Problem Solved**: All 36 edge case conversations were failing with "No suitable template found for the emotional arc"

**Root Cause**: Zero prompt templates existed for edge case emotional arcs

**Solution Implemented**:
1. Researched existing template structure and Elena Morales methodology
2. Created 3 edge case prompt templates:
   - `crisis_to_referral` → "Template - Crisis → Referral - Safety & Professional Boundaries"
   - `hostility_to_boundary` → "Template - Hostility → Boundary - Professional Boundary Setting"
   - `overwhelm_to_triage` → "Template - Overwhelm → Triage - Emergency Prioritization"
3. Inserted templates into database using SAOL `agentExecuteSQL`
4. Verified template-arc linkage: 3/3 edge case arcs now have templates

**Script Created**: `scripts/insert-edge-case-templates.js` - Reusable template insertion script

### Current Prompt Template Inventory

| Template Name | Tier | Arc Type |
|---------------|------|----------|
| Template - Crisis → Referral - Safety & Professional Boundaries | edge_case | crisis_to_referral |
| Template - Hostility → Boundary - Professional Boundary Setting | edge_case | hostility_to_boundary |
| Template - Overwhelm → Triage - Emergency Prioritization | edge_case | overwhelm_to_triage |
| Template - Anxiety → Confidence - Investment Anxiety | template | fear_to_confidence |
| Template - Confusion → Clarity - Education Focus | template | confusion_to_clarity |
| Template - Couple Conflict → Alignment - Money Values | template | couple_conflict_to_alignment |
| Template - Emergency → Calm - Crisis Management | template | emergency_to_calm |
| Template - Grief/Loss → Healing - Values-Based Recovery | template | grief_to_healing |
| Template - Overwhelm → Empowerment - Complex Situation | template | overwhelm_to_empowerment |
| Template - Shame → Acceptance - Financial Trauma | template | shame_to_acceptance |

**Total**: 10 templates (7 template tier + 3 edge_case tier)

---

## 📁 Important Files

### Dataset Files
| File | Purpose |
|------|---------|
| `pmc/_archive/full-file-training-json-242-conversations.json` | Production dataset (242 conversations, 1,567 pairs) |

### Product Documentation
| File | Purpose |
|------|---------|
| `pmc/product/01-bmo-overview-full-brun-product.md` | Full product overview and vision |

### Implementation Scripts
| File | Purpose |
|------|---------|
| `scripts/insert-edge-case-templates.js` | Edge case template insertion script |

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

## 🚀 Next Agent Instructions

### Primary Task: Design Hugging Face Lead Magnet Strategy

1. **Read Required Documents**:
   - Product overview: `pmc/product/01-bmo-overview-full-brun-product.md`
   - Review codebase structure: `src/` directory

2. **Understand the Dataset**:
   - 242 conversations, 1,567 training pairs
   - Financial planning consultant vertical
   - 3 personas × 7 emotional arcs × 17+ topics

3. **Evaluate Strategy Options**:
   - Full giveaway (owner's preference for this iteration)
   - Tiered access (analyst's recommendation)
   - Hybrid approach (full access with social/feedback requirements)

4. **Consider**:
   - How to maximize visibility and adoption
   - How to capture value (feedback, community, email) even if free
   - How to avoid appearing desperate or commodity
   - How to position for future paid iterations

5. **Deliverables**:
   - Recommended strategy with rationale
   - Hugging Face Dataset Card (README.md) content
   - Sample extraction strategy (if applicable)
   - Landing page requirements (if applicable)

---

**Last Updated**: December 8, 2025
**Session Focus**: Edge Case Template Implementation + Lead Magnet Strategy Planning
**Current State**: Dataset ready, strategy decision needed
**Document Version**: hh (Hugging Face handoff)
