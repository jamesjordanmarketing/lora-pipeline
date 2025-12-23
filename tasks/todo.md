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
