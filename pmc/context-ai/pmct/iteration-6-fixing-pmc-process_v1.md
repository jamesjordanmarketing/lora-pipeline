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

## Script Duplication Analysis: 01-generate-overview.js vs 01-02-generate-product-specs.js

### Questions Answered

**Q1: What does `01-generate-overview.js` do?**
- Generates **ONLY** the overview prompt
- Processes `config.documents[0]` (the first document in prompts-config.json)
- Outputs: `_run-prompts/01-product-{abbrev}-overview-prompt-v1.md`

**Q2: What does `01-02-generate-product-specs.js` do?**
- Generates **BOTH** overview and user stories prompts
- Processes `config.documents[0]` for overview
- Then processes `config.documents[1]` for user stories
- Outputs: 
  - `_run-prompts/01-product-{abbrev}-overview-prompt-v1.md`
  - `_run-prompts/02-product-{abbrev}-user-stories-prompt-v1.md`

**Q3: Is there duplicate functionality?**
- **YES** - Both scripts generate the exact same overview prompt file
- The output filename is identical: `01-product-{abbrev}-overview-prompt-v1.md`
- The output directory is identical: `_run-prompts/`
- The template used is identical: `01-product-overview-prompt-template_v1.md`
- The placeholders processed are identical

**Q4: Does running 01-02 overwrite the 01 prompt?**
- **YES** - Running `01-02-generate-product-specs.js` will overwrite the file created by `01-generate-overview.js`
- Since they write to the same filename, the second execution replaces the first

**Q5: Are the prompts exactly the same in content?**
- **YES** - Both scripts:
  - Load the same `prompts-config.json`
  - Process the same `config.documents[0]` entry
  - Use the same template file
  - Replace the same placeholders
  - Generate byte-for-byte identical output

### Process Impact

**Current Tutorial Says:**
1. Run `01-generate-overview.js` first
2. Then run `01-02-generate-product-specs.js`

**What Actually Happens:**
1. `01-generate-overview.js` creates `01-product-{abbrev}-overview-prompt-v1.md`
2. `01-02-generate-product-specs.js` **overwrites** that same file
3. Then creates `02-product-{abbrev}-user-stories-prompt-v1.md`

### Recommended Solution

**Option A: Use only 01-02-generate-product-specs.js**
- Skip `01-generate-overview.js` entirely
- Run `01-02-generate-product-specs.js` once to generate both prompts
- This is more efficient and avoids confusion

**Option B: Keep both scripts (current approach)**
- Useful if you only want to regenerate the overview prompt without user stories
- Accept that running both will result in overwrite (harmless since content is identical)

**Option C: Deprecate 01-generate-overview.js**
- Since `01-02-generate-product-specs.js` is a superset
- Move `01-generate-overview.js` to archive
- Update tutorials to use only `01-02-generate-product-specs.js`

### Current Decision
- **Keep both scripts** for now
- Update tutorial to clarify that running `01-02-generate-product-specs.js` alone is sufficient
- Document that `01-generate-overview.js` is useful only for regenerating overview without touching user stories

---

## Step 03 & Step 04 Process Analysis (December 16, 2025)

### User Questions & Context

**Scenario:** User ran `03-generate-functional-requirements.js` which created:
- Output: `_run-prompts/3a-preprocess-functional-requirements-prompt_v1-output.md`
- User executed that prompt in AI, created: `03-pipeline-functional-requirements.md`
- Script now asking for "FR Preprocessing Instructions" and path to `3b-functional-requirements-prompt_v1.md`

**Questions:**
1. What is expected to complete the enhancements?
2. Is there another prompt for detailed enhancements?
3. Does executing `3b-functional-requirements-prompt_v1.md` add value?
4. Are wireframe scripts (`04-generate-FR-prompt-segments.js` and `04-generate-FR-wireframe-segments_v5.js`) the next step?
5. Are those scripts/prompts templatized?

---

### Analysis: Step 03 Functional Requirements Process

#### How Step 03 Works (Two-Phase Process)

**Phase 1: Preprocess (3a)**
```
Input: Raw/initial functional requirements
Script: 03-generate-functional-requirements.js (preprocess mode)
Template: _prompt_engineering/3a-preprocess-functional-requirements-prompt_v1.md
Output Prompt: _run-prompts/3a-preprocess-functional-requirements-prompt_v1-output.md
Action: User copies prompt → AI execution → Saves as 03-{abbrev}-functional-requirements.md
Purpose: Clean, deduplicate, and reorder requirements
```

**Phase 2: Enhance (3b) - TWO SEPARATE PROMPTS**

After preprocessing, the script asks: "Ready to continue to enhancement step? (y/n)"

When you say "yes", it generates **TWO enhancement prompts** (not one):

**Enhancement Prompt #1:**
```
Template: _prompt_engineering/3b-#1-functional-requirements-legacy-prompt_v1.md
Output Prompt: _run-prompts/3b-#1-functional-requirements-legacy-prompt_v1-output.md
Purpose: Enhance requirements with detailed acceptance criteria and identify gaps
Action: User copies prompt → AI execution → Updates 03-{abbrev}-functional-requirements.md
```

**Enhancement Prompt #2:**
```
Template: _prompt_engineering/3b-#2-functional-requirements-legacy-code-prompt_v1.md
Output Prompt: _run-prompts/3b-#2-functional-requirements-legacy-code-prompt_v1-output.md
Purpose: Add legacy code references underneath each acceptance criterion
Action: User copies prompt → AI execution → Updates 03-{abbrev}-functional-requirements.md again
```

**Note:** The original `3b-functional-requirements-prompt_v1.md` template is **NOT used** by the script. It's kept for reference only.

---

### Answers to User Questions

#### Q1: What is expected to complete the enhancements?

**Answer:**
When the script asks for "FR Preprocessing Instructions" at the enhance step, it's asking you to confirm the path to the enhancement template. You should:

1. **Press Enter** to accept default: `_prompt_engineering/3b-functional-requirements-prompt_v1.md`
2. Script will then ask for paths to:
   - `03-{abbrev}-functional-requirements.md` (your preprocessed FR file)
   - `01-{abbrev}-overview.md`
   - `02-{abbrev}-user-stories.md`
   - `02b-{abbrev}-user-journey.md`
   - Reference example (if exists)
   - Codebase review (optional - say "n" unless you have legacy code to reference)

3. Script generates **TWO** enhancement prompts in `_run-prompts/`:
   - `3b-#1-functional-requirements-legacy-prompt_v1-output.md`
   - `3b-#2-functional-requirements-legacy-code-prompt_v1-output.md`

4. Execute **Prompt #1** first:
   - Copy content → Paste in AI
   - AI enhances your FR with detailed acceptance criteria
   - Save output, replacing your `03-{abbrev}-functional-requirements.md`

5. Execute **Prompt #2** second (optional):
   - Copy content → Paste in AI
   - AI adds legacy code references under each criterion
   - Save output, replacing your `03-{abbrev}-functional-requirements.md` again

---

#### Q2: Is there another prompt for detailed enhancements?

**Answer:** YES - There are **TWO** enhancement prompts, not one.

**Files Overview:**
```
_prompt_engineering/
├── 3b-functional-requirements-prompt_v1.md              (REFERENCE ONLY - not used by script)
├── 3b-#1-functional-requirements-legacy-prompt_v1.md    (ACTIVE - enhancement step 1)
└── 3b-#2-functional-requirements-legacy-code-prompt_v1.md (ACTIVE - enhancement step 2)
```

**Status of Each File:**

1. **`3b-functional-requirements-prompt_v1.md`**
   - **Status:** Original/reference template
   - **Used by script:** NO (script code has it commented out)
   - **Purpose:** Historical reference, shows original single-step enhancement approach
   - **Recommended:** Keep for reference, but don't execute

2. **`3b-#1-functional-requirements-legacy-prompt_v1.md`**
   - **Status:** ACTIVE - Part 1 of enhancement
   - **Used by script:** YES
   - **Purpose:** Enhance requirements with:
     - Detailed acceptance criteria
     - New requirements to fill gaps
     - Consistent depth across all sections
   - **Execution:** REQUIRED for quality FRs

3. **`3b-#2-functional-requirements-legacy-code-prompt_v1.md`**
   - **Status:** ACTIVE - Part 2 of enhancement
   - **Used by script:** YES
   - **Purpose:** Add legacy code references under each acceptance criterion
   - **Execution:** OPTIONAL (only if you have legacy codebase to reference)

**Why Two Prompts?**
- AI context limits prevent doing everything in one pass
- Splitting into two phases ensures:
  - Phase 1: Deep enhancement of requirements quality
  - Phase 2: Traceability to legacy code (if applicable)

---

#### Q3: Does executing `3b-functional-requirements-prompt_v1.md` add value?

**Answer:** NO - Do NOT execute `3b-functional-requirements-prompt_v1.md` manually.

**Reasoning:**
1. **Script doesn't use it** - The code explicitly skips generating this prompt (it's commented out in lines 438-444)
2. **Superseded by split prompts** - The `3b-#1` and `3b-#2` prompts replaced it
3. **Will cause confusion** - Running it would duplicate enhancement work already done by `3b-#1`

**What You Should Do:**
- **Execute:** `3b-#1-functional-requirements-legacy-prompt_v1-output.md` (generated by script)
- **Optionally Execute:** `3b-#2-functional-requirements-legacy-code-prompt_v1-output.md` (if you have legacy code)
- **Ignore:** `3b-functional-requirements-prompt_v1.md` (reference only)

**Recommendation:** Move `3b-functional-requirements-prompt_v1.md` to archive with note that it's superseded by split prompts.

---

#### Q4: Are wireframe scripts the next step?

**Answer:** YES - After completing Step 03 enhancements, Step 04 generates wireframe prompts.

**Correct Next Steps:**

```
Step 03 Complete ✅
  ├─ 3a preprocessing executed
  ├─ 3b-#1 enhancement executed
  └─ 3b-#2 legacy code references executed (optional)
        ↓
Step 04: Wireframe Generation
  ├─ Script: 04-generate-FR-wireframe-segments_v5.js (RECOMMENDED)
  └─ Alternative: 04-generate-FR-prompt-segments.js (older version)
```

**Which Script to Use:**

1. **`04-generate-FR-wireframe-segments_v5.js`** (RECOMMENDED - Latest)
   - More sophisticated
   - Uses journey mapping data
   - Generates both generator prompts AND execution prompts
   - Outputs to `_mapping/fr-maps/prompts/`

2. **`04-generate-FR-prompt-segments.js`** (Older)
   - Simpler segmentation
   - Outputs to `_mapping/ui-functional-maps/`
   - May be deprecated or for different use case

**Recommendation:** Use `04-generate-FR-wireframe-segments_v5.js` (v5 is the latest version in your codebase).

---

#### Q5: Are wireframe scripts/prompts templatized?

**Answer:** YES - Both scripts are fully templatized and automated.

**How Step 04 Works:**

**Script:** `04-generate-FR-wireframe-segments_v5.js`

**Process:**
1. **Reads** your `03-{abbrev}-functional-requirements.md`
2. **Segments** it into sections (E01, E02, E03, etc.)
3. **For each section:**
   - Extracts all FR IDs (e.g., FR1.1.0, FR1.2.0, FR1.3.0)
   - Generates a customized prompt PER FR using template
   - Calculates line numbers for traceability
4. **Outputs:**
   - Generator prompts: `_mapping/fr-maps/prompts/04-FR-wireframes-prompt-E[XX].md`
   - Execution prompts: `_mapping/fr-maps/prompts/04-FR-with-wireframes-execution-prompts_v1.md`
   - Final wireframe output path: `_mapping/fr-maps/04-bmo-FR-wireframes-output-E[XX].md`

**Templates Used:**
- `_prompt_engineering/04-FR-with-wireframes-create-tasks_v1.md` (generator template)
- `_prompt_engineering/04-FR-with-wireframes-execution-prompts_v1.md` (execution template)

**Placeholders Replaced:**
- `[FR_NUMBER_PLACEHOLDER]` → Actual FR ID (e.g., FR1.1.0)
- `[STAGE_NAME_PLACEHOLDER]` → Section name
- `[MINIMUM_PAGE_COUNT_PLACEHOLDER]` → Page count requirement
- `[SECTION_ID_PLACEHOLDER]` → Section ID (e.g., E01)
- `[FR_LOCATE_FILE_PATH_PLACEHOLDER]` → Path to FR file
- `[FR_LOCATE_LINE_PLACEHOLDER]` → Line number in FR file
- `[OUTPUT_FILE_PATH_PLACEHOLDER]` → Output path for wireframe

**Execution Flow:**
```
1. Run: node 04-generate-FR-wireframe-segments_v5.js "Project Name" abbrev
2. Script auto-generates all prompts for all sections
3. For each section (E01, E02, etc.):
   - Copy the generated prompt
   - Paste in AI (Claude/ChatGPT)
   - AI creates detailed wireframes with tasks
   - Save to specified output path
4. Repeat for all sections
```

**Yes, fully templatized** - No manual editing of prompts required.

---

### Complete Step 03 & 04 Workflow Summary

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 03: Functional Requirements (Two-Phase Enhancement)       │
├─────────────────────────────────────────────────────────────────┤
│ Phase 1: Preprocess (3a)                                        │
│   Script: 03-generate-functional-requirements.js               │
│   Template: 3a-preprocess-functional-requirements-prompt_v1.md │
│   Output: 03-{abbrev}-functional-requirements.md               │
│   Purpose: Clean, deduplicate, reorder                         │
├─────────────────────────────────────────────────────────────────┤
│ Phase 2: Enhance (3b) - TWO PROMPTS                            │
│   Prompt #1: 3b-#1-functional-requirements-legacy-prompt_v1.md │
│     → Adds detailed acceptance criteria                        │
│     → Identifies gaps and adds new requirements                │
│     → REQUIRED for quality                                     │
│                                                                 │
│   Prompt #2: 3b-#2-functional-requirements-legacy-code-...     │
│     → Adds legacy code references under each criterion         │
│     → OPTIONAL (only if you have legacy codebase)              │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 04: Wireframe Generation                                  │
├─────────────────────────────────────────────────────────────────┤
│ Script: 04-generate-FR-wireframe-segments_v5.js                │
│ Templates:                                                      │
│   - 04-FR-with-wireframes-create-tasks_v1.md                   │
│   - 04-FR-with-wireframes-execution-prompts_v1.md              │
│                                                                 │
│ Process:                                                        │
│   1. Reads 03-{abbrev}-functional-requirements.md              │
│   2. Segments into sections (E01, E02, E03...)                 │
│   3. Extracts FR IDs per section                               │
│   4. Generates prompts per FR with placeholders filled         │
│   5. Outputs to _mapping/fr-maps/prompts/                      │
│                                                                 │
│ Execution:                                                      │
│   - For each section, copy generated prompt                    │
│   - Paste in AI                                                │
│   - AI creates detailed wireframes                             │
│   - Save to specified output path                              │
└─────────────────────────────────────────────────────────────────┘
```

---

### Recommended Actions

#### Immediate (For Current Session)

1. **Complete Step 03 Enhancement:**
   - Press Enter to accept `3b-functional-requirements-prompt_v1.md` path
   - Provide paths to all required files when prompted
   - Say "n" to codebase review (unless you have legacy code)
   - Execute the TWO generated prompts:
     - `3b-#1-functional-requirements-legacy-prompt_v1-output.md` (REQUIRED)
     - `3b-#2-functional-requirements-legacy-code-prompt_v1-output.md` (OPTIONAL - skip if no legacy code)

2. **Proceed to Step 04:**
   - Run: `node 04-generate-FR-wireframe-segments_v5.js "LoRA Pipeline" pipeline`
   - Execute each generated wireframe prompt section by section

#### Cleanup (For Next Session)

1. **Archive obsolete template:**
   ```bash
   mv _prompt_engineering/3b-functional-requirements-prompt_v1.md \
      _prompt_engineering/archive/3b-functional-requirements-prompt_v1.md
   ```
   - Add note: "Superseded by 3b-#1 and 3b-#2 split prompts"

2. **Update tutorials** to clarify:
   - Step 03 has TWO enhancement prompts (not one)
   - `3b-functional-requirements-prompt_v1.md` is reference only
   - Legacy code prompt (#2) is optional

3. **Verify script versions:**
   - Confirm `04-generate-FR-wireframe-segments_v5.js` is the canonical version
   - Archive or deprecate `04-generate-FR-prompt-segments.js` if superseded

---

**Document Status:** Completed  
**Executed By:** AI Agent  
**Execution Date:** 2025-12-15  
**Updated:** 2025-12-16 (Script duplication analysis + Step 03/04 process analysis added)

