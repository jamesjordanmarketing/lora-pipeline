# Extension Pipeline - Quick Start (v2)

**Status:** ✅ Ready to Run  
**Version:** 2.0 (Meta-Prompt Workflow)

---

## Three-Stage Pipeline Workflow

### Stage 0: Generate Custom Integration Prompt

```bash
# Navigate to tools directory
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools"

# Generate custom prompt from template (~1-2 seconds)
node 04e-merge-integration-spec_v2.js \
  --template "../_prompt_engineering/04d-integrate-existing-codebase_v2.md" \
  --spec "../_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md" \
  --codebase "../../../src" \
  --output-dir "../_mapping/pipeline/_run-prompts" \
  --prompt-output "../_mapping/pipeline/04e-custom-integration-prompt_v1.md"
```

**Output:** `04e-custom-integration-prompt_v1.md` (ready-to-execute prompt)

---

### Stage 1: Execute Integration Analysis (Manual AI Execution)

**Process:**
1. Open the generated prompt: `04e-custom-integration-prompt_v1.md`
2. Provide the prompt to an AI assistant (Claude, ChatGPT, etc.)
3. Save the three generated documents to `_run-prompts/` directory:
   - `04d-infrastructure-inventory_v1.md`
   - `04d-extension-strategy_v1.md`
   - `04d-implementation-guide_v1.md`

**Note:** This is a manual step requiring AI analysis of the codebase.

---

### Stage 2: Segment into Execution Prompts

```bash
# After Stage 1 is complete, run segmentation
node 04f-segment-integrated-spec_v1.js \
  --inventory "../_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md" \
  --strategy "../_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md" \
  --guide "../_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md" \
  --output-dir "../_mapping/pipeline/_execution-prompts/"
```

**Output:** Progressive execution prompts in `_execution-prompts/` directory

---

## Complete Workflow (All Commands)

```bash
# Navigate to tools directory
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools"

# ===== STAGE 0: Generate Custom Prompt =====
node 04e-merge-integration-spec_v2.js \
  --template "../_prompt_engineering/04d-integrate-existing-codebase_v2.md" \
  --spec "../_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md" \
  --codebase "../../../src" \
  --output-dir "../_mapping/pipeline/_run-prompts" \
  --prompt-output "../_mapping/pipeline/04e-custom-integration-prompt_v1.md"

# ===== STAGE 1: Execute with AI (Manual) =====
# 1. Open: ../pmc/product/_mapping/pipeline/04e-custom-integration-prompt_v1.md
# 2. Execute with AI assistant
# 3. Save three documents to _run-prompts/ directory

# ===== STAGE 2: Segment (After Stage 1 complete) =====
node 04f-segment-integrated-spec_v1.js \
  --inventory "../_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md" \
  --strategy "../_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md" \
  --guide "../_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md" \
  --output-dir "../_mapping/pipeline/_execution-prompts/"
```

---

## Validate Before Running

```bash
node validate-pipeline.js
```

Expected: `✅ VALIDATION PASSED - Ready to run pipeline!`

---

## Output Files

**After Stage 0:**
- `04e-custom-integration-prompt_v1.md` (~46 KB)

**After Stage 1 (AI execution):**
- `04d-infrastructure-inventory_v1.md` (~50-100 KB)
- `04d-extension-strategy_v1.md` (~40-80 KB)
- `04d-implementation-guide_v1.md` (~60-120 KB)

**After Stage 2:**
- `_execution-prompts/` directory
  - `EXECUTION-INDEX.md` (start here)
  - `04f-execution-E01-P01.md` through `04f-execution-E07-P04.md`

---

## Next Steps After Pipeline

1. Open `_execution-prompts/EXECUTION-INDEX.md`
2. Review execution order
3. Start with `04f-execution-E01-P01.md`
4. Execute prompts progressively

---

## Key Files Reference

| File | Purpose | Type | Size |
|------|---------|------|------|
| `04d-integrate-existing-codebase_v2.md` | Generic meta-prompt template | Template | 44 KB |
| `04e-merge-integration-spec_v2.js` | Prompt generator (Stage 0) | Script | 9 KB |
| `04f-segment-integrated-spec_v1.js` | Segmentation (Stage 2) | Script | 20 KB |
| `validate-pipeline.js` | Validation script | Script | 7 KB |
| `PIPELINE-USAGE-GUIDE.md` | Complete guide | Docs | 18 KB |
| `QUICK-START.md` | This file | Docs | 4 KB |

---

## v2 vs v1 Changes

**v2 Workflow:**
- Stage 0: Generate custom prompt from template
- Stage 1: AI analyzes codebase (manual execution)
- Stage 2: Segment into execution prompts

**v1 Workflow (deprecated):**
- Stage 1: Hardcoded merge transformation
- Stage 2: Segment into execution prompts

**Why v2?**
- Product/project agnostic meta-prompt
- Flexible for different codebases
- Better framing (EXTENSION, not integration)
- More accurate codebase analysis

---

## Documentation

- **Complete Guide**: `../product/_mapping/pipeline/PIPELINE-USAGE-GUIDE.md`
- **Generic Template**: `../product/_prompt_engineering/04d-integrate-existing-codebase_v2.md`
- **This Quick Start**: `QUICK-START.md`

---

**Ready to run!** Execute Stage 0 command above to start the pipeline.
