# Two-Stage Spec Integration & Segmentation Pipeline - Usage Guide

**Version:** 1.0  
**Date:** December 23, 2025  
**Purpose:** Complete guide for running the two-stage pipeline to transform structured specs into execution-ready prompts

---

## OVERVIEW

This pipeline transforms a generic structured specification into progressive execution prompts by merging integration knowledge with feature requirements.

**Two Stages:**
1. **Stage 1 (MERGE)**: Combine structured spec + integration docs → integrated extension spec
2. **Stage 2 (SEGMENT)**: Break integrated spec → progressive execution prompts

---

## PREREQUISITES

### Required Files

Before running the pipeline, ensure you have:

1. **Structured Specification** (04c)
   - Path: `pmc/product/_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md`
   - Contains: 7 sections of features with generic infrastructure

2. **Infrastructure Inventory** (04d)
   - Path: `pmc/product/_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md`
   - Contains: What exists in codebase to USE

3. **Extension Strategy** (04d)
   - Path: `pmc/product/_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md`
   - Contains: How features map to existing infrastructure

4. **Implementation Guide** (04d)
   - Path: `pmc/product/_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md`
   - Contains: Exact code patterns to follow

### Required Tools

- Node.js (v14 or higher)
- Access to the repository files

---

## STAGE 1: MERGE

### Purpose
Transform the structured spec from generic infrastructure (Prisma, NextAuth, S3) to extension-aware spec (Supabase patterns).

### Input Files
- Structured spec (04c)
- Infrastructure Inventory (04d)
- Extension Strategy (04d)
- Implementation Guide (04d)

### Output File
- `04e-integrated-extension-spec_v1.md` - Merged spec with all infrastructure replaced

### Command

```bash
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools"

node 04e-merge-integration-spec_v1.js \
  --spec "../_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md" \
  --inventory "../_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md" \
  --strategy "../_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md" \
  --guide "../_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md" \
  --output "../_mapping/pipeline/04e-integrated-extension-spec_v1.md"
```

### Expected Output

```
🚀 Integration Spec Merger v1

📂 Reading input files...

✅ Structured Spec: ../path/04c-pipeline-structured-from-wireframe_v1.md
✅ Infrastructure Inventory: ../path/04d-infrastructure-inventory_v1.md
✅ Extension Strategy: ../path/04d-extension-strategy_v1.md
✅ Implementation Guide: ../path/04d-implementation-guide_v1.md

🔍 Extracting sections from structured spec...

✅ Found 7 sections

🔄 Transforming sections...

   Processing Section 1: Foundation & Authentication
   Processing Section 2: Dataset Management
   Processing Section 3: Training Configuration
   Processing Section 4: Training Execution & Monitoring
   Processing Section 5: Model Artifacts & Delivery
   Processing Section 6: Cost Tracking & Notifications
   Processing Section 7: Complete System Integration

✅ All sections transformed

📝 Generating integrated specification...

💾 Writing output file...

✅ Written: ../path/04e-integrated-extension-spec_v1.md

✅ MERGE COMPLETE!

📊 Summary:
   - Sections processed: 7
   - Output file: ../path/04e-integrated-extension-spec_v1.md
   - File size: XXX KB

🎯 Next step: Run segmentation script
```

### Validation

After running Stage 1, verify:

1. **Output file exists**: `04e-integrated-extension-spec_v1.md`
2. **File size is reasonable**: Should be similar to input spec size
3. **All sections present**: Should have 7 sections marked "INTEGRATED"
4. **No Prisma references**: Search for "Prisma" - should only appear in comparison contexts
5. **No NextAuth references**: Search for "NextAuth" - should be replaced with "Supabase Auth"
6. **Infrastructure substitutions**: Check that generic infrastructure is replaced

**Quick validation command:**
```bash
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_mapping\pipeline"

# Check file exists and size
ls -lh 04e-integrated-extension-spec_v1.md

# Count sections
grep -c "## SECTION.*INTEGRATED" 04e-integrated-extension-spec_v1.md
# Expected: 7

# Check for problematic references
grep -i "prisma" 04e-integrated-extension-spec_v1.md | head -5
grep -i "nextauth" 04e-integrated-extension-spec_v1.md | head -5
```

---

## STAGE 2: SEGMENT

### Purpose
Break the integrated extension spec into progressive execution prompts with proper dependencies.

### Input File
- `04e-integrated-extension-spec_v1.md` (output from Stage 1)

### Output Files
- Multiple execution prompts: `04f-execution-E[XX]-P[YY].md`
- Execution index: `EXECUTION-INDEX.md`

### Command

```bash
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools"

node 04f-segment-integrated-spec_v1.js \
  --input "../_mapping/pipeline/04e-integrated-extension-spec_v1.md" \
  --output-dir "../_mapping/pipeline/_execution-prompts/"
```

### Expected Output

```
🚀 Integrated Spec Segmenter v1

📂 Reading integrated specification...

✅ Input: ../path/04e-integrated-extension-spec_v1.md

📁 Created output directory: ../path/_execution-prompts/

🔍 Extracting sections...

✅ Found 7 sections

📝 Generating execution prompts...

📦 Section 1: Foundation & Authentication
   ⚠️  Section 1 (Foundation): Most infrastructure exists, creating minimal prompts for new tables only
   📋 Found X features
      - database: X features
      - api: X features
   ✅ Generated 2 prompts

📦 Section 2: Dataset Management
   📋 Found X features
      - database: X features
      - api: X features
      - ui: X features
      - integration: X features
   ✅ Generated 4 prompts

[... continues for all 7 sections ...]

📋 Generating execution index...

✅ Created execution index: ../path/_execution-prompts/EXECUTION-INDEX.md

✅ SEGMENTATION COMPLETE!

📊 Summary:
   - Sections processed: 7
   - Prompts generated: 24
   - Output directory: ../path/_execution-prompts/
   - Total features: XX

🎯 Next step: Execute prompts in order
   Start with: 04f-execution-E01-P01.md
```

### Validation

After running Stage 2, verify:

1. **Output directory exists**: `_execution-prompts/`
2. **Multiple prompt files created**: Should have ~20-30 prompts
3. **Execution index exists**: `EXECUTION-INDEX.md`
4. **Prompt naming correct**: Format `04f-execution-E[XX]-P[YY].md`
5. **Progressive dependencies**: Each prompt references previous ones

**Quick validation command:**
```bash
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_mapping\pipeline\_execution-prompts"

# Count prompts
ls -1 04f-execution-*.md | wc -l

# Check naming pattern
ls -1 04f-execution-*.md | head -10

# Verify index exists
ls -lh EXECUTION-INDEX.md

# Check first prompt
head -30 04f-execution-E01-P01.md
```

---

## COMPLETE WORKFLOW

### Full Pipeline Execution

```bash
# Navigate to tools directory
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools"

# STAGE 1: Merge (5-10 seconds)
echo "=== STAGE 1: MERGE ==="
node 04e-merge-integration-spec_v1.js \
  --spec "../_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md" \
  --inventory "../_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md" \
  --strategy "../_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md" \
  --guide "../_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md" \
  --output "../_mapping/pipeline/04e-integrated-extension-spec_v1.md"

echo ""
echo "=== STAGE 1 COMPLETE ==="
echo ""

# STAGE 2: Segment (10-20 seconds)
echo "=== STAGE 2: SEGMENT ==="
node 04f-segment-integrated-spec_v1.js \
  --input "../_mapping/pipeline/04e-integrated-extension-spec_v1.md" \
  --output-dir "../_mapping/pipeline/_execution-prompts/"

echo ""
echo "=== STAGE 2 COMPLETE ==="
echo ""

# Show results
echo "=== RESULTS ==="
echo "Integrated spec:"
ls -lh "../_mapping/pipeline/04e-integrated-extension-spec_v1.md"
echo ""
echo "Execution prompts:"
ls -1 "../_mapping/pipeline/_execution-prompts/" | wc -l
echo "prompts generated"
```

### Total Execution Time
- Stage 1 (Merge): ~5-10 seconds
- Stage 2 (Segment): ~10-20 seconds
- **Total**: ~15-30 seconds

---

## OUTPUT STRUCTURE

### After Stage 1

```
pmc/product/_mapping/pipeline/
├── 04c-pipeline-structured-from-wireframe_v1.md  (input - original spec)
└── 04e-integrated-extension-spec_v1.md           (output - transformed spec)
```

### After Stage 2

```
pmc/product/_mapping/pipeline/
├── 04e-integrated-extension-spec_v1.md  (input from Stage 1)
└── _execution-prompts/                   (output directory)
    ├── EXECUTION-INDEX.md                (execution guide)
    ├── 04f-execution-E01-P01.md          (Section 1, Prompt 1)
    ├── 04f-execution-E01-P02.md          (Section 1, Prompt 2)
    ├── 04f-execution-E02-P01.md          (Section 2, Prompt 1)
    ├── 04f-execution-E02-P02.md          (Section 2, Prompt 2)
    ├── 04f-execution-E02-P03.md          (Section 2, Prompt 3)
    ├── 04f-execution-E02-P04.md          (Section 2, Prompt 4)
    └── ...                               (more prompts for sections 3-7)
```

---

## PROGRESSIVE EXECUTION

### After Pipeline Completion

Once both stages are complete, you have a set of execution-ready prompts:

1. **Open**: `_execution-prompts/EXECUTION-INDEX.md`
2. **Review**: The execution order and dependencies
3. **Execute**: Each prompt in sequence:
   - Start with `04f-execution-E01-P01.md`
   - Complete all acceptance criteria
   - Run validation steps
   - Move to next prompt

### Execution Order

**Within Section** (Intra-section):
```
Database → API → UI → Integration
```

**Between Sections** (Inter-section):
```
E01 → E02 → E03 → E04 → E05 → E06 → E07
```

### Example Execution Flow

```
E01-P01 (Database)  →  E01-P02 (API)  →  E01-P03 (UI)  →  E01-P04 (Integration)
    ↓
E02-P01 (Database)  →  E02-P02 (API)  →  E02-P03 (UI)  →  E02-P04 (Integration)
    ↓
E03-P01 (Database)  →  E03-P02 (API)  →  E03-P03 (UI)  →  E03-P04 (Integration)
    ↓
[... and so on ...]
```

---

## TROUBLESHOOTING

### Stage 1 Issues

**Problem**: "Error reading file"
- **Cause**: File path incorrect or file doesn't exist
- **Solution**: Verify all input file paths are correct
```bash
ls -lh "../_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md"
ls -lh "../_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md"
ls -lh "../_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md"
ls -lh "../_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md"
```

**Problem**: "Found 0 sections"
- **Cause**: Structured spec format doesn't match expected pattern
- **Solution**: Check that spec has sections formatted as `## SECTION N: Title`

**Problem**: Output file is very small
- **Cause**: Transformation failed silently
- **Solution**: Check console output for errors, verify input files are correct format

### Stage 2 Issues

**Problem**: "Error reading file" for integrated spec
- **Cause**: Stage 1 didn't complete successfully
- **Solution**: Re-run Stage 1 and verify output file exists

**Problem**: "Found 0 sections"
- **Cause**: Integrated spec format doesn't match expected pattern
- **Solution**: Verify Stage 1 output, check for `## SECTION N: Title - INTEGRATED`

**Problem**: No prompts generated
- **Cause**: No features extracted from sections
- **Solution**: Check integrated spec has features formatted as `#### FR-X.Y: Title`

**Problem**: Too few prompts
- **Cause**: Features not categorized correctly
- **Solution**: Review feature categorization logic in script

### General Issues

**Problem**: Permission denied
- **Solution**: Check directory permissions, run with appropriate privileges

**Problem**: Node.js not found
- **Solution**: Install Node.js v14+ or add to PATH

**Problem**: Unexpected output
- **Solution**: Check all input files are the correct version (v1)

---

## FILE REFERENCE

### Input Files (Required)

| File | Purpose | Size | Version |
|------|---------|------|---------|
| `04c-pipeline-structured-from-wireframe_v1.md` | Structured spec with generic infrastructure | ~150 KB | v1 |
| `04d-infrastructure-inventory_v1.md` | What exists in codebase | ~60 KB | v1 |
| `04d-extension-strategy_v1.md` | How features map to infrastructure | ~35 KB | v1 |
| `04d-implementation-guide_v1.md` | Exact code patterns | ~100 KB | v1 |

### Tool Files (Pipeline)

| File | Purpose | Size |
|------|---------|------|
| `04e-merge-integration-spec-meta-prompt_v1.md` | Instructions for merge operation | ~40 KB |
| `04e-merge-integration-spec_v1.js` | Stage 1 merge script | ~15 KB |
| `04f-segment-integrated-spec_v1.js` | Stage 2 segmentation script | ~20 KB |

### Output Files (Generated)

| File | Purpose | Size |
|------|---------|------|
| `04e-integrated-extension-spec_v1.md` | Merged spec (Stage 1 output) | ~150 KB |
| `04f-execution-E[XX]-P[YY].md` | Execution prompts (Stage 2 output) | ~5-10 KB each |
| `EXECUTION-INDEX.md` | Execution guide (Stage 2 output) | ~5 KB |

---

## NEXT STEPS

After completing the pipeline:

1. ✅ **Review Output**: Check integrated spec and execution prompts
2. ✅ **Read Execution Index**: Understand execution order and dependencies
3. ✅ **Begin Execution**: Start with first prompt (E01-P01)
4. ✅ **Track Progress**: Mark prompts complete as you implement features
5. ✅ **Validate**: Run validation steps after each prompt

---

## SUPPORT

For issues or questions:

1. **Check**: This usage guide
2. **Validate**: Input files are correct version
3. **Review**: Console output for error messages
4. **Verify**: File paths are correct
5. **Test**: Run with sample/test files first

---

**Document Version**: 1.0  
**Last Updated**: December 23, 2025  
**Status**: Production Ready

