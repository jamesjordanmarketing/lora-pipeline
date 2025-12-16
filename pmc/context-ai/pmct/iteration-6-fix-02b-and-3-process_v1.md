# Iteration 6 — Fix 02b User Journey + Step 03 Process Cleanup
**Date:** 2025-12-15  
**Status:** ✅ EXECUTED  
**Author:** AI Agent  
**Executed:** 2025-12-15  

---

## Executive Summary

This specification documents **all required changes** to:
1. Deprecate the 03.5 user journey segmentation process
2. Rename `02.5-user-journey-prompt_v8.md` → `02b-user-journey-prompt_v8.md`
3. Create a new script `02b-generate-user-journey_v1.js` (modeled after `01-generate-overview.js`)
4. Templatize `02b-user-journey-prompt_v8.md` with placeholders for dynamic customization
5. Update `03-generate-functional-requirements.js` to output to `_run-prompts/` (not `_prompt_engineering/output-prompts/`)

---

## PART 1: Deprecate 03.5 User Journey Segmentation

### 1.1 Files Being Deprecated

These files will **no longer be part of the active process**:

| File | Action |
|------|--------|
| `pmc/product/_tools/02-generate-user-journey-prompt-segments_v4.js` | Move to `_tools/archive/` |
| `pmc/product/_prompt_engineering/03.5-user-journey-stages-prompt-template_v9-version-e.md` | Move to `_prompt_engineering/archive/` |

### 1.2 Files Referencing Deprecated Functionality (Require Updates)

| File | Lines/Sections | Action |
|------|----------------|--------|
| `pmc/context-ai/pmct/iteration-6-fixing-pmc-process_v1.md` | Lines 9, 30, 39, 63, 101, 116, 131-132 | Rewrite document to reflect new simplified process |
| `pmc/docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md` | Lines 162, 170, 174, 609 | Update to reference `02b-user-journey-prompt_v8.md` |
| `pmc/product/_tools/03-generate-functional-requirements.js` | Line 268 | Change from `03.5-${projectAbbrev}-user-journey.md` to `02b-${projectAbbrev}-user-journey.md` |
| `pmc/product/_tools/extract-user-journey-data.js` | Line 5 | Change from `../03.5-bmo-user-journey.md` to `../02b-bmo-user-journey.md` (or deprecate) |
| `pmc/product/_tools/cache/03-bmo-paths-cache.json` | Lines 7, 14 | Will auto-update on next run |
| `pmc/product/_tools/cache/03-pipeline-paths-cache.json` | Line 7 | Will auto-update on next run |

### 1.3 Documentation Impact

The following docs reference the deprecated v4 segmenter or 03.5 pattern:

| Document | Impact |
|----------|--------|
| `pmc/docs/ltc-6a/wireframe-create-workflow-tutorial_v2.md` | Lines 19, 396 reference `03.5-bmo-user-journey.md` — update to `02b-bmo-user-journey.md` |
| `pmc/docs/ltc-6a/wireframe-workflow-optimization-analysis_v3.md` | Lines 162, 386, 429, 606 — update to `02b-` pattern |
| `pmc/docs/ltc-6a/00-pmc-ltc-overview-tutorial_v3.md` | Does NOT mention 03.5 segmentation — no changes needed |

---

## PART 2: Rename User Journey Prompt Template

### 2.1 File Rename

| Current Path | New Path |
|--------------|----------|
| `pmc/product/_prompt_engineering/02.5-user-journey-prompt_v8.md` | `pmc/product/_prompt_engineering/02b-user-journey-prompt_v8.md` |

### 2.2 Files Referencing Old Name (Require Updates)

| File | Line(s) | Old Reference | New Reference |
|------|---------|---------------|---------------|
| `pmc/docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md` | 162, 170, 174 | `02.5-user-journey-prompt_v8.md` | `02b-user-journey-prompt_v8.md` |
| `pmc/docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md` | 609 | Directory structure reference | Update accordingly |
| `pmc/context-ai/pmct/iteration-6-fixing-pmc-process_v1.md` | 58, 72 | `02.5-user-journey-prompt_v8.md` | `02b-user-journey-prompt_v8.md` |

### 2.3 Output File Naming Convention Change

| Current Pattern | New Pattern |
|-----------------|-------------|
| `02.5-{abbrev}-user-journey.md` | `02b-{abbrev}-user-journey.md` |
| `03.5-{abbrev}-user-journey.md` | `02b-{abbrev}-user-journey.md` |

This affects:
- `pmc/product/_tools/03-generate-functional-requirements.js` (line 268)
- Any cache files referencing the old pattern

---

## PART 3: Templatize 02b-user-journey-prompt_v8.md

### 3.1 Current State Analysis

Reading the current `02.5-user-journey-prompt_v8.md`, I found these **hardcoded values** that need to become placeholders:

| Current Hardcoded Value | Replacement Placeholder |
|-------------------------|-------------------------|
| `pmc\product\00-train-seed-story.md` | `{SEED_STORY_PATH}` |
| `pmc\product\01-train-overview.md` | `{OVERVIEW_PATH}` |
| `pmc\product\02-train-user-stories.md` | `{USER_STORIES_PATH}` |
| `pmc\product\02.5-train-user-journey.md` | `{OUTPUT_PATH}` |
| `pmc\product\_templates\03-functional-requirements-template.md` | `{TEMPLATE_PATH}` |
| `pmc\product\_examples\03-bmo-functional-requirements.md` | `{EXAMPLE_PATH}` |

### 3.2 Required Placeholder Changes in 02b-user-journey-prompt_v8.md

#### Section: "Required Inputs" (lines 7-10)

**Current:**
```markdown
## Required Inputs
- **Template:** `pmc\product\_templates\03-functional-requirements-template.md`
  - Defines the required format, structure, and numbering conventions for organizing the user journey document.
- **Example:** `pmc\product\_examples\03-bmo-functional-requirements.md`  
  - Provides a reference for structure, depth, quality expectations, and organizational formatting.
```

**Change to:**
```markdown
## Required Inputs
- **Template:** `{TEMPLATE_PATH}`
  - Defines the required format, structure, and numbering conventions for organizing the user journey document.
- **Example:** `{EXAMPLE_PATH}`  
  - Provides a reference for structure, depth, quality expectations, and organizational formatting.
```

#### Section: "Source Document Integration" (lines 228-232)

**Current:**
```markdown
## Source Document Integration

Read and incorporate insights from these project artifacts:
1. **pmc\product\00-train-seed-story.md** - Core vision and value proposition
2. **pmc\product\01-train-overview.md** - Technical architecture and requirements
3. **pmc\product\02-train-user-stories.md** - Detailed user stories and acceptance criteria
```

**Change to:**
```markdown
## Source Document Integration

Read and incorporate insights from these project artifacts:
1. **{SEED_STORY_PATH}** - Core vision and value proposition
2. **{OVERVIEW_PATH}** - Technical architecture and requirements
3. **{USER_STORIES_PATH}** - Detailed user stories and acceptance criteria
```

#### Section: "Output Location" (~line 267)

**Current:**
```markdown
## Output Requirements

### Output Location
Save the completed **User Journey Document** in: `pmc\product\02.5-train-user-journey.md`
```

**Change to:**
```markdown
## Output Requirements

### Output Location
Save the completed **User Journey Document** in: `{OUTPUT_PATH}`
```

#### Section: Document Header in Output Template (lines 275-286)

**Current:**
```markdown
# Bright Run LoRA Training Data Platform - User Journey Document
**Version:** [Version number]  
**Date:** [MM-DD-YYYY]  
**Category:** LoRA Fine-Tuning Training Data Platform User Journey
**Product Abbreviation:** train

**Source References:**
- Seed Story: `pmc/product/00-train-seed-story.md`
- Overview Document: `pmc/product/01-train-overview.md`
- User Stories: `pmc/product/02-train-user-stories.md`
```

**Change to:**
```markdown
# {PROJECT_NAME} - User Journey Document
**Version:** [Version number]  
**Date:** [MM-DD-YYYY]  
**Category:** {PROJECT_NAME} User Journey
**Product Abbreviation:** {PROJECT_ABBREVIATION}

**Source References:**
- Seed Story: `{SEED_STORY_PATH}`
- Overview Document: `{OVERVIEW_PATH}`
- User Stories: `{USER_STORIES_PATH}`
```

### 3.3 Complete Placeholder Summary

| Placeholder | Description | Example Value |
|-------------|-------------|---------------|
| `{PROJECT_NAME}` | Full project name | `LoRA Pipeline` |
| `{PROJECT_ABBREVIATION}` | Short abbreviation | `pipeline` |
| `{SEED_STORY_PATH}` | Path to seed story | `pmc/product/00-pipeline-seed-story.md` |
| `{OVERVIEW_PATH}` | Path to overview | `pmc/product/01-pipeline-overview.md` |
| `{USER_STORIES_PATH}` | Path to user stories | `pmc/product/02-pipeline-user-stories.md` |
| `{TEMPLATE_PATH}` | Path to FR template | `pmc/product/_templates/03-functional-requirements-template.md` |
| `{EXAMPLE_PATH}` | Path to example | `pmc/product/_examples/03-bmo-functional-requirements.md` |
| `{OUTPUT_PATH}` | Output file path | `pmc/product/02b-pipeline-user-journey.md` |

---

## PART 4: Create 02b-generate-user-journey_v1.js Script

### 4.1 Script Location

`pmc/product/_tools/02b-generate-user-journey_v1.js`

### 4.2 Script Behavior (Modeled After 01-generate-overview.js)

The script should:

1. **Accept CLI arguments**: `node 02b-generate-user-journey_v1.js "Project Name" project-abbrev`
2. **Load prompt template**: `_prompt_engineering/02b-user-journey-prompt_v8.md`
3. **Prompt user for file paths** (with defaults):
   - Seed Story: `00-{abbrev}-seed-story.md`
   - Overview: `01-{abbrev}-overview.md`
   - User Stories: `02-{abbrev}-user-stories.md`
   - Template: `_templates/03-functional-requirements-template.md`
   - Example: `_examples/03-bmo-functional-requirements.md`
4. **Replace placeholders** in template with actual paths
5. **Output customized prompt** to: `_run-prompts/02b-product-{abbrev}-user-journey-prompt-v1.md`

### 4.3 Key Functions to Implement (Based on 01-generate-overview.js)

```javascript
// Core functions needed:
- loadPromptsConfig() or hardcoded config
- getValidFilePath() - prompt user for paths with defaults
- normalizePath() - handle Windows/Unix paths
- toLLMPath() - convert to LLM-friendly format
- savePromptToFile() - write to _run-prompts/
- generatePrompt() - replace placeholders
- main() - orchestrate the flow
```

### 4.4 Configuration Structure

Either create a config file or hardcode this in the script:

```javascript
const USER_JOURNEY_CONFIG = {
  type: "user-journey",
  prompt_template_path: "_prompt_engineering/02b-user-journey-prompt_v8.md",
  required_placeholders: {
    "PROJECT_NAME": "{project_name}",
    "PROJECT_ABBREVIATION": "{{project_abbreviation}}",
    "SEED_STORY_PATH": "00-{{project_abbreviation}}-seed-story.md",
    "OVERVIEW_PATH": "01-{{project_abbreviation}}-overview.md",
    "USER_STORIES_PATH": "02-{{project_abbreviation}}-user-stories.md",
    "TEMPLATE_PATH": "_templates/03-functional-requirements-template.md",
    "EXAMPLE_PATH": "_examples/03-bmo-functional-requirements.md",
    "OUTPUT_PATH": "02b-{{project_abbreviation}}-user-journey.md"
  }
};
```

### 4.5 Output Location

All output prompts go to: `pmc/product/_run-prompts/`

Output filename pattern: `02b-product-{abbrev}-user-journey-prompt-v1.md`

---

## PART 5: Update 03-generate-functional-requirements.js Output Location

### 5.1 Current Behavior

The script currently writes output prompts to:
- `pmc/product/_prompt_engineering/output-prompts/`

### 5.2 Required Change

Change output directory to:
- `pmc/product/_run-prompts/`

### 5.3 Code Changes Required

#### Line 309 (writePromptToFile function)

**Current:**
```javascript
function writePromptToFile(prompt, templatePath, projectAbbrev) {
  try {
    // Create output directory if it doesn't exist
    const outputDir = path.resolve(__dirname, '..', '_prompt_engineering', 'output-prompts');
```

**Change to:**
```javascript
function writePromptToFile(prompt, templatePath, projectAbbrev) {
  try {
    // Create output directory if it doesn't exist
    const outputDir = path.resolve(__dirname, '..', '_run-prompts');
```

#### Line 481 (main function - console log)

**Current:**
```javascript
const outputDir = path.resolve(__dirname, '..', '_prompt_engineering', 'output-prompts');
ensureDirectoryExists(outputDir);
console.log(`Prompt outputs will be saved to: ${outputDir}`);
```

**Change to:**
```javascript
const outputDir = path.resolve(__dirname, '..', '_run-prompts');
ensureDirectoryExists(outputDir);
console.log(`Prompt outputs will be saved to: ${outputDir}`);
```

### 5.4 User Journey Path Reference Change

#### Line 268

**Current:**
```javascript
paths.userJourney = await getValidFilePath(
  'User Journey',
  `03.5-${projectAbbrev}-user-journey.md`,
  projectAbbrev
);
```

**Change to:**
```javascript
paths.userJourney = await getValidFilePath(
  'User Journey',
  `02b-${projectAbbrev}-user-journey.md`,
  projectAbbrev
);
```

---

## PART 6: Documentation Updates Required

### 6.1 Files to Update

| File | Required Changes |
|------|------------------|
| `pmc/docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md` | Update all references from `02.5-` to `02b-`; remove any 03.5 segmentation references |
| `pmc/docs/ltc-6a/wireframe-create-workflow-tutorial_v2.md` | Update `03.5-bmo-user-journey.md` → `02b-bmo-user-journey.md` |
| `pmc/docs/ltc-6a/wireframe-workflow-optimization-analysis_v3.md` | Update all `03.5-` references to `02b-` |
| `pmc/context-ai/pmct/iteration-6-fixing-pmc-process_v1.md` | Rewrite to reflect new simplified process (no more v4 segmenter) |

### 6.2 New Process Sequence (Post-Update)

```
Step 00: Seed Story Generation
  Script: 00-generate-seed-story.js
  Output: 00-{abbrev}-seed-story.md

Step 01: Overview Generation
  Script: 01-generate-overview.js
  Output: 01-{abbrev}-overview.md

Step 02: User Stories Generation
  Script: 01-02-generate-product-specs.js (or manual)
  Output: 02-{abbrev}-user-stories.md

Step 02b: User Journey Generation (NEW)
  Script: 02b-generate-user-journey_v1.js
  Prompt: 02b-user-journey-prompt_v8.md
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

## PART 7: Execution Checklist

When executing this spec, complete these steps **in order**:

### Phase 1: Deprecate Old Files
- [ ] Move `pmc/product/_tools/02-generate-user-journey-prompt-segments_v4.js` → `pmc/product/_tools/archive/`
- [ ] Move `pmc/product/_prompt_engineering/03.5-user-journey-stages-prompt-template_v9-version-e.md` → `pmc/product/_prompt_engineering/archive/`

### Phase 2: Rename Files
- [ ] Rename `pmc/product/_prompt_engineering/02.5-user-journey-prompt_v8.md` → `pmc/product/_prompt_engineering/02b-user-journey-prompt_v8.md`

### Phase 3: Update Prompt Template
- [ ] Add placeholders to `02b-user-journey-prompt_v8.md` as specified in Part 3

### Phase 4: Create New Script
- [ ] Create `pmc/product/_tools/02b-generate-user-journey_v1.js` as specified in Part 4

### Phase 5: Update 03-generate-functional-requirements.js
- [ ] Change output directory from `_prompt_engineering/output-prompts/` to `_run-prompts/`
- [ ] Change user journey default path from `03.5-` to `02b-`

### Phase 6: Update Documentation
- [ ] Update `pmc/docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md`
- [ ] Update `pmc/docs/ltc-6a/wireframe-create-workflow-tutorial_v2.md`
- [ ] Update `pmc/docs/ltc-6a/wireframe-workflow-optimization-analysis_v3.md`
- [ ] Rewrite `pmc/context-ai/pmct/iteration-6-fixing-pmc-process_v1.md`

### Phase 7: Clean Up Cache Files
- [ ] Delete or let scripts auto-regenerate cache files in `pmc/product/_tools/cache/`

---

## PART 8: Risk Analysis

| Risk | Mitigation |
|------|------------|
| Existing `03.5-bmo-user-journey.md` breaks | This file can remain as-is for the `bmo` project; new projects use `02b-` pattern |
| Cache files contain old paths | Scripts will prompt for new paths on next run; caches can be deleted |
| Other scripts depend on `03.5-` pattern | `extract-user-journey-data.js` needs update or deprecation |

---

## PART 9: Files Created/Modified Summary

### New Files
- `pmc/product/_tools/02b-generate-user-journey_v1.js`
- `pmc/product/_prompt_engineering/archive/02-generate-user-journey-prompt-segments_v4.js` (moved)
- `pmc/product/_prompt_engineering/archive/03.5-user-journey-stages-prompt-template_v9-version-e.md` (moved)

### Renamed Files
- `02.5-user-journey-prompt_v8.md` → `02b-user-journey-prompt_v8.md`

### Modified Files
- `pmc/product/_prompt_engineering/02b-user-journey-prompt_v8.md` (add placeholders)
- `pmc/product/_tools/03-generate-functional-requirements.js` (output path + user journey path)
- `pmc/docs/ltc-6a/1-to-7-pmc-full-tutorial_v2.md`
- `pmc/docs/ltc-6a/wireframe-create-workflow-tutorial_v2.md`
- `pmc/docs/ltc-6a/wireframe-workflow-optimization-analysis_v3.md`
- `pmc/context-ai/pmct/iteration-6-fixing-pmc-process_v1.md`

---

**END OF SPECIFICATION**

*This document is ready for execution by a coding agent.*
