# Two-Stage Pipeline - Quick Start

**Status:** ✅ Ready to Run  
**Validation:** ✅ All checks passed

---

## Run Pipeline (Both Stages)

```bash
# Navigate to tools directory
cd "C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools"

# STAGE 1: Merge (~5-10 seconds)
node 04e-merge-integration-spec_v1.js \
  --spec "../_mapping/pipeline/04c-pipeline-structured-from-wireframe_v1.md" \
  --inventory "../_mapping/pipeline/_run-prompts/04d-infrastructure-inventory_v1.md" \
  --strategy "../_mapping/pipeline/_run-prompts/04d-extension-strategy_v1.md" \
  --guide "../_mapping/pipeline/_run-prompts/04d-implementation-guide_v1.md" \
  --output "../_mapping/pipeline/04e-integrated-extension-spec_v1.md"

# STAGE 2: Segment (~10-20 seconds)
node 04f-segment-integrated-spec_v1.js \
  --input "../_mapping/pipeline/04e-integrated-extension-spec_v1.md" \
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

**After Stage 1:**
- `../pmc/product/_mapping/pipeline/04e-integrated-extension-spec_v1.md`

**After Stage 2:**
- `../pmc/product/_mapping/pipeline/_execution-prompts/` (directory)
  - `EXECUTION-INDEX.md` (start here)
  - `04f-execution-E01-P01.md` through `04f-execution-E07-P04.md`

---

## Next Steps After Pipeline

1. Open `_execution-prompts/EXECUTION-INDEX.md`
2. Review execution order
3. Start with `04f-execution-E01-P01.md`
4. Execute prompts progressively

---

## Files Created

| File | Purpose | Size |
|------|---------|------|
| `04e-merge-integration-spec-meta-prompt_v1.md` | Merge instructions | 24 KB |
| `04e-merge-integration-spec_v1.js` | Stage 1 script | 19 KB |
| `04f-segment-integrated-spec_v1.js` | Stage 2 script | 20 KB |
| `validate-pipeline.js` | Validation script | 7 KB |
| `PIPELINE-USAGE-GUIDE.md` | Complete guide | 15 KB |
| `IMPLEMENTATION-COMPLETE.md` | Summary doc | 12 KB |

---

## Documentation

- **Complete Guide**: `PIPELINE-USAGE-GUIDE.md`
- **Implementation Summary**: `IMPLEMENTATION-COMPLETE.md`
- **This Quick Start**: `QUICK-START.md`

---

**Ready to run!** Execute the commands above to start the pipeline.

