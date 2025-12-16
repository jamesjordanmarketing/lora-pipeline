# Iteration 6 — PMC Process (User Journey Simplified)
**Date:** 2025-12-15  
**Status:** COMPLETED  
**Context:** LoRA Pipeline (`pipeline`) PMC workflow  

## Summary of Changes (Executed)

This document originally described issues with the 03.5 user journey segmentation workflow. Those issues have been resolved by **simplifying the process** and **deprecating the v4 segmenter**.

### What Changed

1. **Deprecated the v4 segmentation process**
   - Moved `02-generate-user-journey-prompt-segments_v4.js` to `_tools/archive/`
   - Moved `03.5-user-journey-stages-prompt-template_v9-version-e.md` to `_prompt_engineering/archive/` (if existed)

2. **Renamed files from 02.5 to 02b pattern**
   - `02.5-user-journey-prompt_v8.md` → `02b-user-journey-prompt_v8.md`
   - Output files: `02.5-{abbrev}-user-journey.md` → `02b-{abbrev}-user-journey.md`

3. **Created new automated script**
   - New: `02b-generate-user-journey_v1.js`
   - Modeled after `01-generate-overview.js`
   - Outputs customized prompts to `_run-prompts/`

4. **Updated 03-generate-functional-requirements.js**
   - Changed output directory from `_prompt_engineering/output-prompts/` to `_run-prompts/`
   - Changed user journey input from `03.5-{abbrev}-user-journey.md` to `02b-{abbrev}-user-journey.md`

---

## New Simplified Process Sequence

```
Step 00: Seed Story Generation
  Script: 00-generate-seed-story.js
  Output: 00-{abbrev}-seed-story.md

Step 01: Overview Generation
  Script: 01-generate-overview.js
  Output prompt: _run-prompts/01-product-{abbrev}-overview-prompt-v1.md
  Output document: 01-{abbrev}-overview.md

Step 02: User Stories Generation
  Script: 01-02-generate-product-specs.js (or manual)
  Output: 02-{abbrev}-user-stories.md

Step 02b: User Journey Generation (NEW - Simplified)
  Script: 02b-generate-user-journey_v1.js
  Prompt Template: _prompt_engineering/02b-user-journey-prompt_v8.md
  Output prompt: _run-prompts/02b-product-{abbrev}-user-journey-prompt-v1.md
  Output document: 02b-{abbrev}-user-journey.md

Step 03: Functional Requirements Generation
  Script: 03-generate-functional-requirements.js
  Input: 02b-{abbrev}-user-journey.md
  Output prompts: _run-prompts/3a-*.md, 3b-*.md
  Output document: 03-{abbrev}-functional-requirements.md

Step 04: Wireframe Generation
  Script: 04-generate-FR-wireframe-segments_v4.js
  ...
```

---

## How to Create User Journey (New Process)

### Step 1: Generate Customized Prompt
```bash
cd pmc/product/_tools/
node 02b-generate-user-journey_v1.js "LoRA Pipeline" pipeline
```

The script will:
1. Prompt for input file paths (with defaults)
2. Validate files exist
3. Generate customized prompt in `_run-prompts/02b-product-pipeline-user-journey-prompt-v1.md`

### Step 2: Run Prompt in AI Assistant
1. Open the generated prompt file
2. Copy the complete content
3. Paste into AI assistant with input files attached
4. Save AI output as `pmc/product/02b-pipeline-user-journey.md`

### Step 3: Continue to Functional Requirements
```bash
node 03-generate-functional-requirements.js "LoRA Pipeline" pipeline
```

The script now expects `02b-pipeline-user-journey.md` (not `03.5-`).

---

## Files Modified

| File | Change |
|------|--------|
| `_tools/02-generate-user-journey-prompt-segments_v4.js` | Moved to `_tools/archive/` |
| `_prompt_engineering/03.5-user-journey-stages-prompt-template_v9-version-e.md` | Moved to `_prompt_engineering/archive/` (if existed) |
| `_prompt_engineering/02.5-user-journey-prompt_v8.md` | Renamed to `02b-user-journey-prompt_v8.md` + added placeholders |
| `_tools/02b-generate-user-journey_v1.js` | **Created** - new script |
| `_tools/03-generate-functional-requirements.js` | Updated output dir and user journey path |
| `_tools/extract-user-journey-data.js` | Updated path from `03.5-` to `02b-` |
| `docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md` | Updated all 02.5/03.5 references to 02b |
| `docs/ltc-6a/wireframe-create-workflow-tutorial_v2.md` | Updated user journey references |
| `docs/ltc-6a/wireframe-workflow-optimization-analysis_v3.md` | Updated user journey references |

---

## Why This Simplification?

The original v4 segmentation process was complex:
- Required a "master" user journey file with specific heading formats
- Split into per-stage specs and prompts
- Required running each stage prompt separately
- Generated many intermediate files

The new process is simpler:
- One script generates one customized prompt
- One AI interaction produces the complete user journey document
- Direct naming pattern (`02b-`) aligns with step numbering
- No intermediate segmentation required

---

**Document Status:** Completed  
**Executed By:** AI Agent  
**Execution Date:** 2025-12-15

