# Context Carryover: LoRA Training Infrastructure Implementation

## 📌 Active Development Focus

**Primary Task**: Implement Production LoRA Training Infrastructure for Existing 242-Conversation Dataset

### ⚠️ IMMEDIATE NEXT TASK: PMC Script Consolidation (THIS SESSION - December 16, 2025)

**What Was Just Completed**:

1. ✅ **PMC Process Simplification** (Iteration 6)
   - Deprecated v4 segmentation process (moved to archive/)
   - Renamed 02.5 → 02b pattern for user journey files
   - Created new `02b-generate-user-journey_v1.js` script
   - Updated `03-generate-functional-requirements.js` to use 02b pattern
   - Updated all PMC documentation and tutorials

2. ✅ **Script Duplication Analysis**
   - **Discovery**: Both `01-generate-overview.js` and `01-02-generate-product-specs.js` generate IDENTICAL overview prompts
   - **File**: Both write to `_run-prompts/01-product-{abbrev}-overview-prompt-v1.md`
   - **Content**: Byte-for-byte identical (same template, same placeholders, same config)
   - **Impact**: Running both scripts causes harmless overwrite (second replaces first with identical content)
   - **Root Cause**: `01-02-generate-product-specs.js` is a superset that generates BOTH overview + user stories prompts

3. ✅ **Documentation Updated**
   - Created comprehensive analysis in `pmc/context-ai/pmct/iteration-6-fixing-pmc-process_v1.md`
   - Created operational tutorial: `pmc/docs/ltc-6a/00-pmc-ltc-operational-tutorial_v1.md`
   - Updated overview tutorial: `pmc/docs/ltc-6a/00-pmc-ltc-overview-tutorial_v4.md`

### 🎯 NEXT AGENT IMMEDIATE TASK: Split 01-02 Script for Operational Consistency

**Current Problem**:
- `01-02-generate-product-specs.js` generates BOTH step 01 (overview) and step 02 (user stories)
- This violates operational consistency: one script should do one thing
- Causes confusion: why run `01-generate-overview.js` if `01-02` overwrites it?

**Solution to Implement**:

**Step 1: Modify `01-02-generate-product-specs.js`**
- **Location**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\01-02-generate-product-specs.js`
- **Action**: Remove all 01 (overview) generation functionality
- **Keep**: Only the 02 (user stories) generation code
- **Details**:
  - Remove lines 535-551 (overview generation section)
  - Remove `overviewDoc` variable
  - Keep only `userStoriesDoc` processing (lines 563-581)
  - Keep all utility functions (they're reused)
  - Update script header comment to reflect new single purpose

**Step 2: Create `02a-generate-user-story-spec.js`**
- **Location**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\02a-generate-user-story-spec.js`
- **Action**: Create new script from modified `01-02-generate-product-specs.js`
- **Functionality**: 
  - Takes same inputs as current 02 process
  - Outputs same 02 prompt: `_run-prompts/02-product-{abbrev}-user-stories-prompt-v1.md`
  - Uses `config.documents[1]` (user stories config)
  - Requires `01-{abbrev}-overview.md` as input (from config placeholders)
- **Implementation**: Copy modified version of `01-02-generate-product-specs.js` with user stories code only

**Step 3: Update Tutorial Documentation**
- **File**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\docs\ltc-6a\00-pmc-ltc-overview-tutorial_v4.md`
- **Changes Required**:
  - Update Section 2.2 (Step 01): Keep `01-generate-overview.js` instructions (no change)
  - Update Section 2.3 (Step 02): Change from `01-02-generate-product-specs.js` to `02a-generate-user-story-spec.js`
  - Add note: "`02a-generate-user-story-spec.js` requires `01-{abbrev}-overview.md` to exist first"
  - Update process flow diagram if present
  - Update any examples showing file execution order

**Step 4: Update Operational Tutorial**
- **File**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\docs\ltc-6a\00-pmc-ltc-operational-tutorial_v1.md`
- **Changes Required**:
  - Update FAQ section about `01-02-generate-product-specs.js`
  - Add note that script is now deprecated (functionality split)
  - Update execution order: `01-generate-overview.js` → `02a-generate-user-story-spec.js`
  - Update all examples and command sequences

**Step 5: Archive Old Script**
- **File**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\01-02-generate-product-specs.js`
- **Action**: Move to `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_tools\archive/01-02-generate-product-specs.js`
- **Reason**: Keep for reference but deprecate in favor of split scripts

**Expected Result After Implementation**:

```
Step 00: Seed Story Generation
  Script: 00-generate-seed-story.js
  Output: 00-{abbrev}-seed-story.md

Step 01: Overview Generation
  Script: 01-generate-overview.js
  Output prompt: _run-prompts/01-product-{abbrev}-overview-prompt-v1.md
  Output document: 01-{abbrev}-overview.md

Step 02: User Stories Generation (UPDATED)
  Script: 02a-generate-user-story-spec.js (NEW - renamed from 01-02)
  Input required: 01-{abbrev}-overview.md
  Output prompt: _run-prompts/02-product-{abbrev}-user-stories-prompt-v1.md
  Output document: 02-{abbrev}-user-stories.md

Step 02b: User Journey Generation
  Script: 02b-generate-user-journey_v1.js
  Output prompt: _run-prompts/02b-product-{abbrev}-user-journey-prompt-v1.md
  Output document: 02b-{abbrev}-user-journey.md

Step 03: Functional Requirements Generation
  Script: 03-generate-functional-requirements.js
  Input: 02b-{abbrev}-user-journey.md
  Output prompts: _run-prompts/3a-*.md, 3b-*.md
  Output document: 03-{abbrev}-functional-requirements.md
```

**Rationale**:
- **Operational Consistency**: Each script does ONE thing (matches rest of PMC process)
- **Clear Dependencies**: Step 02a explicitly requires Step 01 output
- **No Duplication**: Removes overlapping functionality between `01-generate-overview.js` and `01-02-generate-product-specs.js`
- **Naming Convention**: 02a follows established pattern (like 02b for user journey)

### 🚫 CRITICAL: DO NOT START LORA INFRASTRUCTURE WORK YET

**After completing the PMC script consolidation task above**:
1. ✅ Report completion summary
2. ✅ Confirm all files modified/created correctly
3. ✅ Wait for human confirmation
4. ⚠️ **DO NOT** proceed to LoRA training infrastructure implementation
5. ⚠️ **DO NOT** start building database tables, APIs, or Docker containers
6. ✅ Internalize the LoRA context (read specs below) but DO NOT implement
7. ✅ Wait for explicit human instruction to begin LoRA work

---

## 📋 PMC Process Current State (For Context)

### PMC Script Execution Order (After Consolidation Above)

```
pmc/product/_tools/
├── 00-generate-seed-story.js          → 00-{abbrev}-seed-story.md
├── 01-generate-overview.js            → 01-product-{abbrev}-overview-prompt-v1.md
├── 02a-generate-user-story-spec.js    → 02-product-{abbrev}-user-stories-prompt-v1.md (NEW)
├── 02b-generate-user-journey_v1.js    → 02b-product-{abbrev}-user-journey-prompt-v1.md
├── 03-generate-functional-requirements.js → 3a/3b prompts
└── 04-generate-FR-wireframe-segments_v4.js → wireframe prompts
```

### Key PMC Files Modified This Session

| File | Change | Status |
|------|--------|--------|
| `_tools/02-generate-user-journey-prompt-segments_v4.js` | Moved to archive/ | ✅ Deprecated |
| `_prompt_engineering/02.5-user-journey-prompt_v8.md` | Renamed to 02b-user-journey-prompt_v8.md | ✅ Completed |
| `_tools/02b-generate-user-journey_v1.js` | Created (409 lines) | ✅ Completed |
| `_tools/03-generate-functional-requirements.js` | Updated for 02b pattern | ✅ Completed |
| `docs/ltc-6a/00-pmc-ltc-overview-tutorial_v4.md` | Updated with 02b process | ✅ Completed |
| `docs/ltc-6a/00-pmc-ltc-operational-tutorial_v1.md` | Created operational guide | ✅ Completed |
| `context-ai/pmct/iteration-6-fixing-pmc-process_v1.md` | Added duplication analysis | ✅ Completed |
| `_tools/01-02-generate-product-specs.js` | TO BE MODIFIED (remove 01 functionality) | ⏳ Next Task |
| `_tools/02a-generate-user-story-spec.js` | TO BE CREATED (from modified 01-02) | ⏳ Next Task |

### PMC Script Duplication Issue (Resolved by Next Task)

**Current State**:
- `01-generate-overview.js`: Generates overview prompt only
- `01-02-generate-product-specs.js`: Generates BOTH overview + user stories prompts (duplicate!)
- Both write to same file: `01-product-{abbrev}-overview-prompt-v1.md`
- Content is byte-for-byte identical

**After Next Task**:
- `01-generate-overview.js`: Generates overview prompt only (no change)
- `02a-generate-user-story-spec.js`: Generates user stories prompt only (new)
- No duplication, operational consistency achieved

---

## 🏗️ LoRA Training Infrastructure (DO NOT IMPLEMENT YET - Context Only)

### Current Status: LoRA Training Infrastructure Specification Complete, Implementation Phase Next

**What Was Completed** (December 13, 2025 - PREVIOUS SESSION):

1. ✅ **Comprehensive LoRA Training Infrastructure Roadmap**
   - **File**: `pmc/context-ai/pmct/iteration-5-LoRA-training-initial.md` (2,139 lines)
   - Complete technical specification for training Llama 3 70B on RunPod H100
   - Database schema extensions (training_jobs, model_artifacts, training_metrics_history tables)
   - Vercel API endpoints specification (training-service.ts, API routes)
   - RunPod Docker container design (CUDA 12.1, PyTorch, Hugging Face stack)
   - Training orchestrator architecture (QLoRA, SFTTrainer, dataset preprocessing)
   - Webhook integration for progress reporting
   - Cost analysis: $260-410 for 3-month proof of concept
   - 4-week implementation timeline (122 hours total effort)

2. ✅ **Executive-Friendly TLDR Document**
   - **File**: `pmc/context-ai/pmct/iteration-5-LoRA-training-initial-tldr.md` (616 lines)
   - Non-technical explanation of what we're building
   - Business case and ROI analysis
   - Plain language architecture descriptions
   - Decision framework with weekly checkpoints
   - Glossary of technical terms

3. ✅ **Testing & Validation Framework**
   - **File**: `pmc/context-ai/pmct/iteration-5-LoRA-emotional-training-measuring.md` (1,687 lines)
   - Comprehensive testing methodology for proving dataset effectiveness
   - Three-model comparison design (baseline, generic control, emotional training)
   - Two-tier metrics system: human evaluation (8 dimensions) + automated metrics (13 measurements)
   - 50 test scenario structure with proper hold-out dataset
   - Statistical validity requirements and sample size calculations
   - Success criteria: Model C ≥15% better than baseline, ≥10% better than generic control
   - Complete execution process (3 weeks, $980-1,700 investment)
   - Client-facing deliverables specification

4. ✅ **Experimental Design Analysis & Revision**
   - **File**: `pmc/context-ai/pmct/iteration-5-LoRA-emotional-training-measurement-viability_v1.md` (1,083 lines)
   - **Critical Insight**: Original testing framework had flawed control group design
   - Analysis confirmed generic financial Q&A control is "apples vs oranges" comparison
   - **Revised Recommendation**: Two options:
     * Option 1 (Simple): Baseline vs. Emotional only ($525-875, 2 weeks)
     * Option 2 (Gold Standard): Baseline vs. Neutral Control vs. Emotional ($1,000-1,700, 3 weeks)
   - Neutral Control = same 242 scenarios with emotionally neutral responses (isolates emotional intelligence as variable)
   - Confirmed existing 242-conversation dataset is production-ready, NO refactoring needed
   - Dataset teaches HOW to respond (emotional style), not WHAT to say (financial knowledge)

5. ✅ **Infrastructure Assessment Complete**
   - **Existing Dataset**: 242 conversations, 1,567 training pairs in `pmc/_archive/full-file-training-json-242-conversations.json`
   - **Dataset Quality**: Superior to most open-source datasets (structured conversation history, emotional scaffolding, brand voice)
   - **Existing Application**: Next.js 14 + Supabase at `src/` - conversation generation, enrichment, storage ALL working
   - **RunPod H100 PCIe**: 80GB VRAM sufficient for Llama 3 70B + QLoRA (4-bit quantization)
   - **Cost Validated**: $50-150 per training run, $260-410 total first 3 months
   - **Timeline Validated**: 4 weeks to first trained model (achievable)

**What's Next** (For Future Agent - AFTER PMC Task):

⚠️ **CRITICAL: DO NOT START BUILDING YET** ⚠️

**First, complete the PMC script consolidation task above.**

**Then, you must internalize the LoRA context:**

1. **Read the Existing Codebase** (`C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`)
   - Understand current conversation generation pipeline
   - Study `training-file-service.ts` (aggregates conversations into training files)
   - Review API structure in `src/app/api/`
   - Understand database schema (conversations, training_files, personas, emotional_arcs, training_topics)
   - Note what's working: Claude API generation, 5-stage enrichment, Supabase storage

2. **Study the LoRA Training Specifications**
   - **Technical Roadmap**: `pmc/context-ai/pmct/iteration-5-LoRA-training-initial.md`
   - **Business Context**: `pmc/context-ai/pmct/iteration-5-LoRA-training-initial-tldr.md`
   - **Testing Framework**: `pmc/context-ai/pmct/iteration-5-LoRA-emotional-training-measuring.md`
   - **Experimental Design**: `pmc/context-ai/pmct/iteration-5-LoRA-emotional-training-measurement-viability_v1.md`

3. **Understand the Dataset**
   - Location: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\_archive\full-file-training-json-242-conversations.json`
   - Format: brightrun-lora-v4 (excellent structure for LoRA training)
   - Contents: 242 conversations, 1,567 training pairs
   - Scaffolding: 3 personas × 7 emotional arcs × 20 financial topics
   - Consultant profile: Elena Morales, CFP (warm, emotionally intelligent tone)
   - **Key insight**: Dataset teaches emotional intelligence and brand voice, NOT primarily financial knowledge

4. **Understand What We're Building**
   - **NOT** building multi-perspective framework (that's future work)
   - **YES** building actual LoRA training infrastructure to train models on EXISTING 242-conversation dataset
   - **Goal**: Prove our emotional intelligence training data creates measurably better AI responses
   - **Infrastructure**: Vercel APIs → RunPod GPU training → Webhook updates → Supabase storage
   - **Output**: Trained LoRA adapters we can load onto Llama 3 70B

5. **Wait for Human Instructions**
   - After internalizing context, report your understanding
   - Ask clarifying questions if needed
   - Wait for explicit instruction to begin implementation
   - Human will decide: start with Phase 1 (Database), Phase 2 (RunPod), or Phase 3 (Testing)

---

## 🎯 Project Pivot: From Multi-Perspective Framework to Production Training

### Context Shift (Important)

**Previous Focus** (through December 11, 2025):
- Designing multi-perspective + purpose-driven training framework (theoretical)
- Creating schemas for expert panel deliberations
- Research on persona weighting strategies
- Future-facing innovation work

**Current Focus** (December 13, 2025 onwards):
- **Building actual training infrastructure** to train models NOW
- Using EXISTING 242-conversation emotional intelligence dataset
- Proving our training data works with measurable results
- Production system for training, testing, and deploying LoRA models

**Why the Pivot:**
> "The analysis of the new dataset concepts made me realize that 'proof' is the most critical. Proof means creating the LoRA training functionality using our current dataset."
> - User (December 13, 2025)

**Key Insight:**
- We already have a production-quality dataset (242 conversations)
- Multi-perspective framework is innovative but theoretical
- Business needs PROOF that our training methodology works
- Can't sell trained models without training infrastructure
- Can't prove ROI without measurable results

**The multi-perspective framework work is NOT abandoned** - it's deferred until after we prove the foundational approach works with our simpler emotional intelligence dataset.

---

## 🏗️ What We're Building: LoRA Training Infrastructure (Context - DO NOT IMPLEMENT)

### System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    VERCEL (Next.js Application)                         │
│                    Location: src/                                       │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  NEW: Training Job Management APIs                                │ │
│  │  - POST /api/training/start-job                                   │ │
│  │  - GET /api/training/jobs/:id                                     │ │
│  │  - DELETE /api/training/jobs/:id (cancel)                         │ │
│  │  - POST /api/training/webhook (receives RunPod updates)           │ │
│  └─────────────────────────┬─────────────────────────────────────────┘ │
└────────────────────────────┼────────────────────────────────────────────┘
                             │ HTTP POST
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    RUNPOD (GPU Training Environment)                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Docker Container (H100 PCIe 80GB)                                │ │
│  │  - FastAPI Server                                                 │ │
│  │  - Training Orchestrator (Python)                                 │ │
│  │  - Dataset Preprocessor (brightrun-v4 → Llama 3 format)          │ │
│  │  - LoRA Training (QLoRA, SFTTrainer)                              │ │
│  │  - vLLM Inference (for testing)                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Network Volume (200GB persistent storage)                             │
│  - /models/llama-3-70b-base (70GB)                                     │
│  - /lora_adapters/run_001/ (500MB per run)                             │
│  - /datasets/processed/ (2GB)                                          │
└─────────────────────────────────────────────────────────────────────────┘
                             │ Upload artifacts
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    SUPABASE (Storage & Database)                        │
│  NEW Storage Bucket:                                                    │
│  - model-artifacts/                                                     │
│    ├─ lora_adapters/run_001/adapter_model.bin                           │
│    └─ training_logs/run_001.json                                        │
│                                                                         │
│  NEW Database Tables:                                                   │
│  - training_jobs (tracks training runs)                                 │
│  - model_artifacts (stores trained models)                              │
│  - training_metrics_history (loss, learning_rate over time)             │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Components to Build (FUTURE WORK)

**Phase 1: Database & Vercel APIs (Week 1)**
- Create new tables: training_jobs, model_artifacts, training_metrics_history
- Build TrainingService class (`src/lib/services/training-service.ts`)
- Implement API routes (`src/app/api/training/*`)
- Add webhook endpoint for RunPod progress updates

**Phase 2: RunPod Docker Container (Week 2)**
- Dockerfile with CUDA 12.1 + PyTorch + Hugging Face
- Training orchestrator (loads model, runs QLoRA training, saves adapters)
- Dataset preprocessor (brightrun-v4 JSON → Llama 3 chat format)
- FastAPI server for job management

**Phase 3: Integration & Testing (Week 3)**
- End-to-end workflow testing
- Webhook flow validation
- Error handling & recovery
- Cost tracking

**Phase 4: Dashboard UI (Week 4)**
- Training job management interface
- Progress visualization
- Model download/testing

---

## 📊 Training Approach: QLoRA on Llama 3 70B (Context - DO NOT IMPLEMENT)

### Technical Details

**Base Model**: Meta Llama 3 70B Instruct
- 70 billion parameters
- Already trained on financial concepts (Reddit, Investopedia, etc.)
- What it LACKS: emotional intelligence, brand voice, consultant personality

**Training Method**: QLoRA (Quantized LoRA)
- Loads base model in 4-bit quantization (INT4) → saves memory
- Trains small adapter matrices (200-500MB) → parameter efficient
- Preserves base model knowledge → no catastrophic forgetting
- Fits on single H100 80GB GPU → cost effective

**Training Hyperparameters** (Initial):
```python
lora_config = {
    "r": 16,                    # Rank
    "lora_alpha": 32,           # Scaling factor
    "lora_dropout": 0.05,       # Dropout rate
    "target_modules": [         # Which layers to adapt
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ]
}

training_args = {
    "num_epochs": 3,
    "batch_size": 4,
    "learning_rate": 2e-4,
    "gradient_accumulation_steps": 4,
    "max_seq_length": 2048
}
```

**Dataset Preprocessing**:
- Input: `full-file-training-json-242-conversations.json` (brightrun-lora-v4 format)
- Output: Llama 3 chat format with special tokens
- Conversion: Extract system_prompt, conversation_history, current_user_input, target_response
- Format: `<|begin_of_text|><|start_header_id|>system<|end_header_id|>...`

**Expected Results**:
- Training time: 10-15 hours on H100
- Cost per run: $25-75 (spot instance)
- Output: LoRA adapters (200-500MB file)
- Improvement: 15-50% on emotional intelligence metrics vs baseline

---

## 🧪 Testing Framework: Proving Dataset Effectiveness (Context - DO NOT IMPLEMENT)

### Two-Phase Testing Approach

**Phase 1: Simple Validation (Recommended First)**
- **Models**: Baseline (Llama 3 70B) vs. Emotional Training (your 242 conversations)
- **Process**: 50 test scenarios → 100 responses → 3-5 evaluators score on 8 dimensions
- **Investment**: $525-875, 2 weeks
- **Proof**: "Our training improves responses by X% over baseline"

**Phase 2: Gold Standard (If Needed for Clients)**
- **Models**: Baseline vs. Neutral Control vs. Emotional Training
- **Neutral Control**: Same 242 scenarios with emotionally neutral responses (new dataset to create)
- **Purpose**: Isolates emotional intelligence as THE variable (not just "any training helps")
- **Investment**: $1,000-1,700, 3 weeks
- **Proof**: "Our emotional training improves by X% over baseline and Y% over neutral, proving it's the emotional scaffolding specifically"

### Why We Revised the Testing Framework

**Original Proposal (Flawed)**:
- Model A: Baseline
- Model B: Generic financial Q&A (Reddit, forums)
- Model C: Your emotional dataset

**Problem**: Comparing knowledge-focused training (Model B) vs. emotional-focused training (Model C) is "apples vs. oranges"

**User's Insight** (Correct):
> "Is generic financial Q&A useful? Aren't LLMs already trained on this? Why would we train on random financial dataset that doesn't test emotional intelligence?"

**Revised Approach**:
- **Option 1**: Skip Model B entirely (simplest, still valid)
- **Option 2**: Use emotionally neutral responses to SAME scenarios as control (gold standard)

### Eight Evaluation Dimensions (Human Scoring)

1. **Emotional Recognition** - Does AI notice client's feelings?
2. **Emotional Validation** - Does AI validate feelings as legitimate?
3. **Empathy Before Advice** - Does AI build connection before problem-solving?
4. **Reframing** - Does AI shift either/or thinking to both/and?
5. **Specific Guidance** - Are next steps concrete and actionable?
6. **Brand Voice Alignment** - Does it sound like Elena Morales?
7. **Avoids Pitfalls** - No jargon, judgment, or overwhelming?
8. **Overall Effectiveness** - Would this help the client?

### Success Criteria

**Primary**: Model C (emotional) scores ≥15% better than Model A (baseline) on aggregate
**Secondary**: Evaluators prefer Model C ≥65-75% of the time
**Statistical**: p < 0.05 (statistically significant improvement)

---

## 📦 Existing Dataset: Production-Ready (Context Only)

### Dataset Location & Structure

**File**: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\_archive\full-file-training-json-242-conversations.json`

**Format**: brightrun-lora-v4 (custom structured format)

**Contents**:
- 242 complete conversations
- 1,567 training pairs (individual turns)
- 3 client personas (anxious_planner, overwhelmed_avoider, pragmatic_optimist)
- 7 emotional arcs (couple_conflict_to_alignment, confusion_to_clarity, overwhelm_to_empowerment, etc.)
- 20 financial topics (negotiating_compensation, estate_planning, mortgage_payoff, etc.)

**Consultant Profile**:
- Name: Elena Morales, CFP
- Business: Pathways Financial Planning
- Core Philosophy: 5 principles (money is emotional, judgment-free space, education-first, etc.)
- Communication Style: Warm, professional, never condescending
- Techniques: Acknowledge emotions explicitly, use metaphors, provide specific numbers, celebrate wins

**Training Pair Structure**:
```json
{
  "turn_number": 2,
  "system_prompt": "You are an emotionally intelligent financial planning chatbot...",
  "conversation_history": [
    { "turn": 1, "role": "user", "content": "...", "emotional_state": {...} }
  ],
  "current_user_input": "I'm really stressed about this...",
  "emotional_context": {
    "detected_emotions": {
      "primary": "frustration",
      "secondary": "anxiety",
      "intensity": 0.72
    }
  },
  "target_response": "Jennifer, first—take a breath. What you're experiencing...",
  "training_metadata": {
    "quality_score": 3,
    "quality_criteria": { "empathy_score": 3.1, "clarity_score": 2.9 }
  }
}
```

### Why This Dataset Is Excellent

**Compared to typical open-source LoRA datasets**:

| Feature | Typical Dataset | Your Dataset |
|---------|----------------|--------------|
| **Structure** | Single-turn Q&A | Multi-turn conversations with full history |
| **Emotional Context** | Absent | Explicit emotion tracking every turn |
| **Brand Voice** | Generic | Consistent consultant personality (Elena) |
| **Scaffolding** | Unstructured | 3 personas × 7 arcs × 20 topics = rich distribution |
| **Quality Metadata** | Minimal | Empathy scores, clarity scores, emotional progression |

**Key Strengths**:
1. ✅ **Structured conversation flow** - Teaches contextual responses
2. ✅ **Emotional intelligence metadata** - Every turn has emotional state
3. ✅ **Consistent voice** - Elena Morales personality throughout
4. ✅ **Proper training format** - System + user + assistant ready for LoRA
5. ✅ **Sufficient volume** - 1,567 pairs meets minimum threshold (research shows 500-1,000 minimum)

**Critical Insight**: Dataset teaches HOW to respond (emotional style, brand voice) NOT primarily WHAT to say (financial knowledge). Llama 3 70B already knows financial concepts - we're teaching it emotional intelligence and consultant personality.

**No Refactoring Needed**: Dataset is production-ready as-is.

---

## 💰 Cost & Timeline Summary (Context Only)

### Infrastructure Investment

| Phase | Duration | Cost | Deliverables |
|-------|----------|------|--------------|
| **Phase 1: Database & APIs** | Week 1 | $0 (dev time only) | New tables, TrainingService, API routes |
| **Phase 2: RunPod Container** | Week 2 | $0 (dev time only) | Docker image, training orchestrator |
| **Phase 3: Integration** | Week 3 | $25-75 (first training run) | End-to-end working system |
| **Phase 4: Dashboard UI** | Week 4 | $0 (dev time only) | Training job management interface |
| **TOTAL INFRASTRUCTURE** | **4 weeks** | **$25-75** | **Production training pipeline** |

### Testing Investment (After Infrastructure)

| Test Type | Duration | Cost | Deliverables |
|-----------|----------|------|--------------|
| **Simple Validation** | 2 weeks | $525-875 | Baseline vs. emotional comparison |
| **Gold Standard** | 3 weeks | $1,000-1,700 | Baseline vs. neutral vs. emotional |

### Operating Costs (Ongoing)

| Activity | Frequency | Cost per Run |
|----------|-----------|--------------|
| **Training Run** | As needed | $25-75 (H100 spot, 10-15 hrs) |
| **Hyperparameter Testing** | 3-5 iterations | $75-375 total |
| **Storage** | Monthly | $20-30 (200GB network volume) |

### ROI Calculation

**Without Training Infrastructure**:
- Can only sell datasets: $5k-10k
- Client question: "How do I know it works?" → No proof

**With Training Infrastructure**:
- Can sell trained models: $15k-30k
- Client pitch: "We've tested rigorously - 21% improvement, 73% preference rate"
- **Premium pricing justified by measurable proof**

**Break-even**: After first trained model sale (infrastructure $75 + testing $1,700 = $1,775 total investment, first sale +$15k revenue = 8.5x ROI)

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

### ⚠️ IMMEDIATE TASK: PMC Script Consolidation (Complete This First)

**Before doing anything else, complete the PMC script consolidation task described at the top of this document:**

1. Modify `01-02-generate-product-specs.js` to remove 01 (overview) functionality
2. Create `02a-generate-user-story-spec.js` with only 02 (user stories) functionality
3. Update `00-pmc-ltc-overview-tutorial_v4.md` with new process
4. Update `00-pmc-ltc-operational-tutorial_v1.md` with new execution order
5. Archive old `01-02-generate-product-specs.js`

**After completing PMC task, report**:
- ✅ Summary of files modified/created
- ✅ Confirmation all scripts work correctly
- ✅ Any issues encountered

### ⚠️ THEN: DO NOT START BUILDING LORA INFRASTRUCTURE YET ⚠️

**After PMC task completion, your next task is context internalization:**

### Step 1: Internalize the Existing Codebase

**Read and understand the current application** (`C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`):

**Key Files to Study**:
1. **`src/lib/services/training-file-service.ts`** (336 lines)
   - Currently aggregates conversations into training files
   - Will be extended with training job orchestration
   - Study the patterns: how it handles Supabase, how it structures data

2. **`src/lib/services/conversation-generation-service.ts`**
   - Understand Claude API integration
   - Study structured output handling
   - Note error handling patterns

3. **`src/app/api/` structure**
   - Review existing API patterns
   - Note authentication, error handling, response formats
   - Understand Next.js 14 App Router conventions

4. **Database schema** (via SAOL queries)
   - Run SAOL introspection on key tables
   - Understand relationships between conversations, training_files, personas
   - Note what columns exist and their types

**Questions to Answer**:
- How does the current system store files in Supabase Storage?
- How are training files currently created and managed?
- What's the authentication pattern for API routes?
- How does error handling work in services?
- What TypeScript patterns are used?

### Step 2: Study the LoRA Training Specifications

**Read these documents in order**:

1. **`pmc/context-ai/pmct/iteration-5-LoRA-training-initial-tldr.md`** (616 lines)
   - Start here for high-level understanding
   - Understand the business case and ROI
   - Get familiar with the architecture concepts

2. **`pmc/context-ai/pmct/iteration-5-LoRA-training-initial.md`** (2,139 lines)
   - Deep technical specification
   - Database schema additions (SQL provided)
   - API specifications (TypeScript interfaces)
   - Docker container design
   - Training orchestrator architecture
   - Complete implementation roadmap

3. **`pmc/context-ai/pmct/iteration-5-LoRA-emotional-training-measurement-viability_v1.md`** (1,083 lines)
   - Understanding testing approach
   - Why we're NOT using generic financial control
   - Dataset quality assessment
   - Experimental design decisions

4. **`pmc/context-ai/pmct/iteration-5-LoRA-emotional-training-measuring.md`** (1,687 lines)
   - Complete testing framework (for later)
   - Human evaluation rubrics
   - Automated metrics
   - Statistical validity requirements

### Step 3: Understand the Dataset

**Examine** (but don't try to read all 133k lines):
- Location: `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\_archive\full-file-training-json-242-conversations.json`
- Read lines 1-100 to understand structure
- Read a few complete conversations (search for conversation_metadata)
- Understand the training_pairs structure

**Key Insights**:
- 242 conversations, 1,567 training pairs
- Each pair has: system_prompt, conversation_history, current_user_input, emotional_context, target_response
- Rich metadata: quality scores, emotional progression, scaffolding info
- Production-ready for LoRA training (no refactoring needed)

### Step 4: Report Your Understanding

**After completing Steps 1-3, report back with**:

1. **Codebase Understanding Summary**
   - What's the current architecture?
   - What are the key patterns (authentication, storage, APIs)?
   - Where will new training infrastructure integrate?
   - What existing code can be reused?

2. **LoRA Training Clarity**
   - What are we building? (in your own words)
   - What's the data flow? (Vercel → RunPod → Supabase)
   - What are the key technical challenges?
   - What's the 4-week implementation plan?

3. **Dataset Assessment**
   - What makes this dataset good for LoRA training?
   - What is it teaching? (emotional intelligence, brand voice)
   - What is it NOT teaching? (financial knowledge)
   - Why is it production-ready as-is?

4. **Questions & Clarifications**
   - What's unclear from the specifications?
   - What additional information do you need?
   - What technical decisions need human input?
   - What are the biggest risks you see?

### Step 5: Wait for Human Direction

**DO NOT start implementing LoRA infrastructure until**:
- PMC script consolidation is complete
- Human reviews your understanding summary
- Human confirms you've internalized the context correctly
- Human explicitly says "proceed with Phase X implementation"

**Possible next directions** (human will decide):
- Phase 1: Database schema + Vercel APIs
- Phase 2: RunPod container + training orchestrator
- Phase 3: End-to-end integration
- Alternative: Start with testing framework first
- Alternative: Dataset preprocessing exploration

---

## 📚 Reference Documents Index

### Core Specifications (Read These After PMC Task)

| Document | Lines | Purpose |
|----------|-------|---------|
| **iteration-5-LoRA-training-initial.md** | 2,139 | Technical roadmap - database, APIs, Docker, orchestrator |
| **iteration-5-LoRA-training-initial-tldr.md** | 616 | Executive summary - business case, plain language |
| **iteration-5-LoRA-emotional-training-measuring.md** | 1,687 | Testing framework - metrics, evaluation, statistics |
| **iteration-5-LoRA-emotional-training-measurement-viability_v1.md** | 1,083 | Experimental design analysis - control groups, validity |
| **iteration-6-fixing-pmc-process_v1.md** | ~180 | PMC process fixes + script duplication analysis |

### Dataset

| File | Size | Contents |
|------|------|----------|
| **full-file-training-json-242-conversations.json** | 133,539 lines | 242 conversations, 1,567 training pairs, emotional intelligence |

### Background (Multi-Perspective Framework - Deferred)

| Document | Lines | Status |
|----------|-------|--------|
| **iteration-4-multi-perspective-datasets_v1.md** | 1,689 | Future work - multi-expert deliberation framework |
| **c-alpha-build_v3.4_multi-lora-pipeline-JSON-schema_v1.json** | ~500 | Future work - schema for expert panel training |

---

## 🎯 Success Criteria

### For PMC Script Consolidation (IMMEDIATE)

**You successfully completed PMC task when**:
- ✅ `01-02-generate-product-specs.js` has been modified to remove 01 functionality
- ✅ `02a-generate-user-story-spec.js` exists and generates only 02 prompts
- ✅ Both scripts tested and working correctly
- ✅ `00-pmc-ltc-overview-tutorial_v4.md` updated with new process
- ✅ `00-pmc-ltc-operational-tutorial_v1.md` updated with new execution order
- ✅ Old `01-02-generate-product-specs.js` moved to archive/

### For Context Internalization Phase (AFTER PMC TASK)

**You successfully internalized context when you can**:
- ✅ Explain the existing codebase architecture in your own words
- ✅ Describe what we're building without reading the specs
- ✅ Identify where new code will integrate with existing code
- ✅ Explain why the dataset is production-ready
- ✅ Describe the LoRA training workflow (Vercel → RunPod → Supabase)
- ✅ List the 4 phases of implementation
- ✅ Explain why we're NOT using generic financial control for testing
- ✅ Identify key risks and technical challenges

### For Implementation Phase (MUCH LATER - AFTER HUMAN APPROVAL)

**Phase 1 Success**: Database tables created, API routes responding, TrainingService working  
**Phase 2 Success**: Docker image builds, training orchestrator runs, can train a model  
**Phase 3 Success**: End-to-end workflow from "click button" to "download LoRA adapters"  
**Phase 4 Success**: Dashboard UI for training management, progress tracking

### For Testing Phase (MUCH LATER)

**Simple Test Success**: Model C beats Model A by ≥15%, evaluators prefer C ≥65% of time  
**Gold Standard Success**: Model C beats both A and B, improvement attributed to emotional scaffolding  

---

**Last Updated**: December 16, 2025  
**Session Focus**: PMC Script Consolidation + LoRA Infrastructure Context Ready  
**Current State**: PMC task ready to execute, then context internalization, then wait for human approval  
**Document Version**: mm (PMC consolidation + LoRA context handoff)

**Next Agent: Start with PMC script consolidation task. Then internalize LoRA context. Do NOT begin building LoRA infrastructure until human confirms your understanding is correct. Report back with summary of your understanding and any questions.**
