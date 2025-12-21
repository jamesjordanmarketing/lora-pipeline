# Context Carryover: PMC Script Path Standardization - Phase 1 Complete

## 📌 Active Development Focus

**Primary Task**: Complete PMC (Project Memory Core) Script Path Standardization

### Current Status: Phase 1 Complete (Scripts 00-02b), Phase 2 Next (Scripts 03-04b)

**What Was Completed** (December 21, 2025):

## ✅ Phase 1: PMC Script Path Refactoring Complete

Successfully refactored four core PMC generation scripts to use the new project-specific directory structure (`_mapping/[abbrev]/`). This establishes operational consistency across the entire PMC document generation pipeline.

### Scripts Updated (Phase 1):

1. **00-generate-seed-story.js**
   - ✅ Added command-line arguments: `"Project Name" project-abbreviation`
   - ✅ Removed automatic reading from `seed-narrative-v1.md`
   - ✅ Updated to output prompts to: `pmc/product/_mapping/[abbrev]/_run-prompts/`
   - ✅ Updated to write final outputs to: `pmc/product/_mapping/[abbrev]/`
   - ✅ Changed input paths to use `_mapping/[abbrev]/` structure
   - ✅ Updated codebase review default to: `src/`
   - ✅ Display full absolute paths (not relative)
   - ✅ Removed cache system entirely
   - ✅ Removed verbose logging (Original/Processed/Exists)
   - ✅ Simplified to show only: `Default: [full absolute path]`

2. **01-generate-overview.js**
   - ✅ Already had command-line arguments (no change needed)
   - ✅ Updated to output prompts to: `pmc/product/_mapping/[abbrev]/_run-prompts/`
   - ✅ Updated input paths to reference `_mapping/[abbrev]/` for seed-story
   - ✅ Changed codebase review default to: `src/`
   - ✅ Display full absolute paths
   - ✅ Removed cache system
   - ✅ Removed verbose logging
   - ✅ Simplified path display

3. **02a-generate-user-story-spec.js**
   - ✅ Already had command-line arguments (no change needed)
   - ✅ Updated to output prompts to: `pmc/product/_mapping/[abbrev]/_run-prompts/`
   - ✅ Updated input paths to reference `_mapping/[abbrev]/` for seed-story and overview
   - ✅ Display full absolute paths
   - ✅ Removed cache system
   - ✅ Removed verbose logging
   - ✅ Simplified path display

4. **02b-generate-user-journey_v1.js**
   - ✅ Already had command-line arguments (no change needed)
   - ✅ Updated to output prompts to: `pmc/product/_mapping/[abbrev]/_run-prompts/`
   - ✅ Updated USER_JOURNEY_CONFIG with all `_mapping/[abbrev]/` paths
   - ✅ Display full absolute paths
   - ✅ Removed cache system
   - ✅ Removed verbose logging
   - ✅ Simplified path display

### Configuration Files Updated:

5. **seed-story-config.json**
   - ✅ Updated `RAW_DATA_PATH` to: `product/_mapping/{{project_abbreviation}}/seed-narrative-v1.md`
   - ✅ Updated `SEED_NARRATIVE_PATH` to: `product/_mapping/{{project_abbreviation}}/00-{{project_abbreviation}}-seed-narrative.md`
   - ✅ Updated `OUTPUT_PATH` entries to use `_mapping/{{project_abbreviation}}/`

6. **prompts-config.json**
   - ✅ Updated `SEED_STORY_PATH` to: `_mapping/{{project_abbreviation}}/00-{{project_abbreviation}}-seed-story.md`
   - ✅ Updated `OVERVIEW_PATH` to: `_mapping/{{project_abbreviation}}/01-{{project_abbreviation}}-overview.md`
   - ✅ Updated `OUTPUT_PATH` entries to use `_mapping/{{project_abbreviation}}/`

### Standardization Patterns Applied:

All scripts now follow these consistent patterns:

**1. Directory Structure:**
```
pmc/product/_mapping/[project-abbrev]/
├── _run-prompts/                          # Generated prompts (all steps)
│   ├── 00-product-[abbrev]-seed-narrative-prompt-v1.md
│   ├── 00-product-[abbrev]-seed-story-prompt-v1.md
│   ├── 01-product-[abbrev]-overview-prompt-v1.md
│   ├── 02-product-[abbrev]-user-stories-prompt-v1.md
│   └── 02b-product-[abbrev]-user-journey-prompt-v1.md
├── seed-narrative-v1.md                   # Raw input (Step 00)
├── 00-[abbrev]-seed-narrative.md          # Step 00 output
├── 00-[abbrev]-seed-story.md              # Step 00 output
├── 01-[abbrev]-overview.md                # Step 01 output (from AI)
├── 02-[abbrev]-user-stories.md            # Step 02a output (from AI)
└── 02b-[abbrev]-user-journey.md           # Step 02b output (from AI)
```

**2. Path Display Format:**
- Before: `pmc/product/01-abbrev-overview.md` (relative)
- After: `C:/Users/james/Master/BrightHub/BRun/lora-pipeline/pmc/product/_mapping/abbrev/01-abbrev-overview.md` (absolute)

**3. User Prompt Simplification:**
- Before:
  ```
  Requesting path for: SEED_STORY_PATH
  Default path: pmc/product/00-abbrev-seed-story.md
  Default path exists: TRUE
  
  Cached path: pmc/product/00-abbrev-seed-story.md
  Cached path exists: TRUE
  
  Enter path for SEED_STORY_PATH
  (Press Enter to use default, or type a new path)
  Path > 
  ```
- After:
  ```
  Enter path for SEED_STORY_PATH
  Default: C:/Users/james/Master/BrightHub/BRun/lora-pipeline/pmc/product/_mapping/abbrev/00-abbrev-seed-story.md
  > 
  ```

**4. Cache System Removal:**
- Removed `loadPathCache()` functions
- Removed `savePathCache()` functions
- Removed all cache checking logic
- Scripts always use hard-coded defaults from configuration files

**5. Codebase Review Default:**
- Changed from `../../product/_templates` or `../../` to `../../../src`
- Now points to: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`

---

## 🎯 What's Next: Phase 2 Script Updates

The next agent will apply identical refactoring patterns to the remaining PMC generation scripts:

### Scripts to Update (Phase 2):

1. **03-generate-FR-initial.js**
   - Located at: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\03-generate-FR-initial.js`
   - Purpose: Generates initial functional requirements from user stories and journey
   - Changes needed:
     - Update output directory to: `_mapping/[abbrev]/_run-prompts/`
     - Update input paths to reference `_mapping/[abbrev]/` for overview, user-stories, user-journey
     - Display full absolute paths
     - Remove cache system
     - Remove verbose logging
     - Simplify path display to show only default

2. **03-generate-functional-requirements.js**
   - Located at: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\03-generate-functional-requirements.js`
   - Purpose: Orchestrates the two-phase FR generation process (preprocessing + enhancement)
   - Changes needed:
     - Update output directory to: `_mapping/[abbrev]/_run-prompts/`
     - Update input paths to reference `_mapping/[abbrev]/` for overview, user-stories, user-journey
     - Update OUTPUT_PATH in prompts to write to: `_mapping/[abbrev]/03-[abbrev]-functional-requirements.md`
     - Display full absolute paths
     - Remove cache system
     - Remove verbose logging
     - Simplify path display

3. **04a-generate-FIGMA-wireframe-prompts_v1.js**
   - Located at: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\04a-generate-FIGMA-wireframe-prompts_v1.js`
   - Purpose: Generates Figma-ready wireframe prompts from functional requirements
   - Changes needed:
     - Update output directory to: `_mapping/[abbrev]/fr-maps/prompts/`
     - Update input path to reference: `_mapping/[abbrev]/03-[abbrev]-functional-requirements.md`
     - Update wireframe output location to: `_mapping/[abbrev]/fr-maps/`
     - Display full absolute paths
     - Remove cache system (if present)
     - Remove verbose logging
     - Simplify path display

4. **04b-generate-FIGMA-wireframe-combined-prompt_v1.js**
   - Located at: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\04b-generate-FIGMA-wireframe-combined-prompt_v1.js`
   - Purpose: Generates combined wireframe prompt for task-oriented planning
   - Changes needed:
     - Update output directory to: `_mapping/[abbrev]/fr-maps/prompts/`
     - Update input path to reference: `_mapping/[abbrev]/03-[abbrev]-functional-requirements.md`
     - Update wireframe output location to: `_mapping/[abbrev]/fr-maps/`
     - Display full absolute paths
     - Remove cache system (if present)
     - Remove verbose logging
     - Simplify path display

### Reference Implementation Examples:

The next agent should study the Phase 1 scripts (00, 01, 02a, 02b) to understand the exact patterns to apply. Key files to examine:

**Script Examples:**
- `pmc/product/_tools/00-generate-seed-story.js` - Shows command-line args, simplified path display
- `pmc/product/_tools/01-generate-overview.js` - Shows cache removal, simplified getValidFilePath
- `pmc/product/_tools/02a-generate-user-story-spec.js` - Shows path processing updates
- `pmc/product/_tools/02b-generate-user-journey_v1.js` - Shows USER_JOURNEY_CONFIG updates

**Config Examples:**
- `pmc/product/_tools/seed-story-config.json` - Shows _mapping path structure
- `pmc/product/_tools/config/prompts-config.json` - Shows _mapping path structure

---

## 📂 Critical Files for Next Agent

### Scripts to Internalize (Phase 1 - Reference Examples):

| Script | Purpose | Key Patterns |
|--------|---------|--------------|
| `pmc/product/_tools/00-generate-seed-story.js` | Seed story generation | Command-line args, simplified prompts, absolute paths |
| `pmc/product/_tools/01-generate-overview.js` | Overview generation | Cache removal, simplified getValidFilePath |
| `pmc/product/_tools/02a-generate-user-story-spec.js` | User stories generation | Path processing, _mapping structure |
| `pmc/product/_tools/02b-generate-user-journey_v1.js` | User journey generation | Config updates, path display |

### Scripts to Update (Phase 2 - Work Items):

| Script | Lines | Complexity | Priority |
|--------|-------|------------|----------|
| `pmc/product/_tools/03-generate-FR-initial.js` | ~400 | Medium | High |
| `pmc/product/_tools/03-generate-functional-requirements.js` | ~600 | High | High |
| `pmc/product/_tools/04a-generate-FIGMA-wireframe-prompts_v1.js` | ~500 | Medium | High |
| `pmc/product/_tools/04b-generate-FIGMA-wireframe-combined-prompt_v1.js` | ~400 | Medium | Medium |

### Configuration Files to Check:

| File | Purpose | Update Needed? |
|------|---------|----------------|
| `pmc/product/_tools/seed-story-config.json` | Step 00 config | ✅ Already updated |
| `pmc/product/_tools/config/prompts-config.json` | Steps 01-02 config | ✅ Already updated |
| FR generation configs (if exist) | Step 03 config | ⚠️ Check and update |
| Wireframe generation configs (if exist) | Step 04 config | ⚠️ Check and update |

### Source Code to Internalize:

**Application Codebase:**
- **Directory**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`
- **Purpose**: Understand the application structure for accurate codebase review path defaults
- **Focus Areas**:
  - Service files (conversation-generation-service.ts, enrichment-pipeline-orchestrator.ts, training-file-service.ts)
  - API routes (app/api/*)
  - Database operations (lib/supabase/*)
  - UI components (app/components/*)

---

## 🔍 Implementation Guidance for Next Agent

### Step-by-Step Approach:

**IMPORTANT: Do NOT start updating scripts yet. First, internalize all context.**

#### Phase A: Context Internalization (DO THIS FIRST)

1. **Read Phase 1 Scripts (Reference Examples)**
   - Read `00-generate-seed-story.js` completely
   - Read `01-generate-overview.js` completely
   - Read `02a-generate-user-story-spec.js` completely
   - Read `02b-generate-user-journey_v1.js` completely
   - **Focus on**: savePromptToFile, getValidFilePath, path processing, config loading
   - **Time estimate**: 2-3 hours

2. **Read Phase 2 Scripts (Work Items)**
   - Read `03-generate-FR-initial.js` completely
   - Read `03-generate-functional-requirements.js` completely
   - Read `04a-generate-FIGMA-wireframe-prompts_v1.js` completely
   - Read `04b-generate-FIGMA-wireframe-combined-prompt_v1.js` completely
   - **Focus on**: Current path handling, cache usage, output directories
   - **Time estimate**: 3-4 hours

3. **Read Configuration Files**
   - Read `seed-story-config.json` (see _mapping pattern)
   - Read `prompts-config.json` (see _mapping pattern)
   - Look for FR/wireframe configs
   - **Time estimate**: 30 minutes

4. **Internalize Application Codebase**
   - Browse `src/` directory structure
   - Understand service layer architecture
   - Understand API route organization
   - Understand database schema usage
   - **Time estimate**: 2-3 hours

**Total Internalization Time: ~8-11 hours** (This is intentional and necessary)

#### Phase B: Wait for Human Instructions

**CRITICAL**: After completing Phase A (context internalization), **STOP and wait for explicit human instructions** before proceeding with any script modifications.

Do NOT:
- ❌ Start updating scripts
- ❌ Make any file changes
- ❌ Create new files
- ❌ Modify configurations

The human will provide specific instructions on:
- Which script to start with
- Any deviations from the Phase 1 pattern
- Testing approach
- Validation criteria

---

## 🎯 Refactoring Patterns to Apply (For Reference)

When the human gives approval to proceed, apply these patterns:

### Pattern 1: Update savePromptToFile Function

**Before:**
```javascript
function savePromptToFile(prompt, filename, projectAbbrev) {
  const outputDir = path.resolve(__dirname, '../_run-prompts');
  // ...
}
```

**After:**
```javascript
function savePromptToFile(prompt, filename, projectAbbrev) {
  const outputDir = path.resolve(__dirname, `../_mapping/${projectAbbrev}/_run-prompts`);
  // ...
}
```

### Pattern 2: Update Input Path Defaults

**Before:**
```javascript
"SEED_STORY_PATH": "00-{{project_abbreviation}}-seed-story.md"
```

**After:**
```javascript
"SEED_STORY_PATH": "_mapping/{{project_abbreviation}}/00-{{project_abbreviation}}-seed-story.md"
```

### Pattern 3: Simplify getValidFilePath Display

**Before:**
```javascript
console.log(`Requesting path for: ${description}`);
console.log(`Default path: ${fullDefaultPath}`);
console.log(`Default path exists: ${fs.existsSync(fullDefaultPath) ? 'TRUE' : 'FALSE'}`);
// ... cache checking logic ...
```

**After:**
```javascript
console.log(`\nEnter path for ${description}`);
console.log(`Default: ${fullDefaultPath}`);
// No cache, no verbose logging
```

### Pattern 4: Remove Cache System

**Remove these functions:**
- `loadPathCache()`
- `savePathCache()`
- All cache checking logic in `getValidFilePath()`

### Pattern 5: Update Codebase Review Default

**Before:**
```javascript
const defaultPath = path.resolve(__dirname, '../../product', '_templates');
```

**After:**
```javascript
const defaultPath = path.resolve(__dirname, '../../../src');
```

### Pattern 6: Display Full Absolute Paths

**Before:**
```javascript
function toProjectPath(absolutePath) {
  const normalized = absolutePath.replace(/\\/g, '/');
  const projectRoot = 'pmc/';
  if (normalized.includes(projectRoot)) {
    return normalized.substring(normalized.indexOf(projectRoot));
  }
  return normalized;
}
```

**After:**
```javascript
function toProjectPath(absolutePath) {
  const normalized = absolutePath.replace(/\\/g, '/');
  return normalized; // Return full absolute path
}
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

**Last Updated**: December 21, 2025  
**Session Focus**: PMC Script Path Standardization - Phase 1 Complete  
**Current State**: Scripts 00-02b refactored and tested, Scripts 03-04b ready for Phase 2  
**Document Version**: pp (PMC Path Standardization - Phase 1 Complete)
