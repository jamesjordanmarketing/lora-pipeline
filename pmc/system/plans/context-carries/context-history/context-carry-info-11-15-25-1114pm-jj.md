# Context Carryover: Multi-Perspective + Purpose-Driven Training Framework

## 📌 Active Development Focus

**Primary Task**: Implement Multi-Perspective + Purpose-Driven LoRA Training Dataset Framework - Generation Prompt Creation Phase

### Current Status: Schemas Complete, Ready for Prompt Template Development

**What Was Completed** (December 11, 2025):

1. ✅ **Comprehensive Research & Analysis**
   - Researched current state of multi-agent deliberation (Dec 2025)
   - Analyzed Constitutional AI, debate-based reasoning, purpose-driven LoRA techniques
   - Validated integration viability with current technology
   - Projected 2026-2027 developments in dynamic persona systems

2. ✅ **Framework Architecture Designed**
   - Created bidirectional influence model (purpose ↔ perspectives)
   - Designed nested turn structure with stateful personas
   - Defined persona weighting strategies (static, hybrid, dynamic)
   - Established framework nesting architecture with context accumulation

3. ✅ **Initial Schema Created (v1 - Example Format)**
   - Example conversation in Multi-Perspective format: `c-alpha-build_v3.4_multi-lora-pipeline-JSON-schema_v1.json`
   - 3 full example training pairs (market validation, product definition, legal/risk)
   - 8 expert personas with state-driven weighting
   - Purpose progression through 6 business planning states
   - Internal deliberation transcripts with challenges, consensus, synthesis

4. ✅ **Comprehensive Analysis Document**
   - 1,689 lines covering integration framework, viability, implementation roadmap
   - EvertBody business plan case study demonstrating value
   - Static vs dynamic persona weighting analysis (300+ lines)
   - 2026-2027 predictions with quarterly roadmap
   - Phased implementation strategy (Q2 2026 → Q2 2027)

**What Was Completed** (December 12, 2025):

5. ✅ **Production JSON Schemas Created (v2 - Proper Schema Format)**
   - **Single Conversation Schema**: `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v2.json`
     - 1,018 lines of comprehensive JSON Schema (Draft 2020-12)
     - Complete field definitions with types, constraints, validation rules
     - Enums for controlled vocabularies (domains, complexity, generation methods)
     - Proper `$schema`, `$id`, `title`, `description` metadata
     - Designed for individual conversation generation via Claude API
   
   - **Full Dataset Schema**: `c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-schema_v2.json`
     - 990 lines of dataset-level schema
     - Aggregates multiple conversations with metadata
     - Quality summary metrics, framework configuration
     - Dataset creation metadata (generation method, cost, duration)
     - Used for training file aggregation

6. ✅ **Production Example Files Created**
   - **Single Conversation Example**: `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-example_v1.json`
     - 897 lines demonstrating complete conversation
     - 3 turns with full deliberation transcripts
     - 8 expert personas (fashion, legal, manufacturing, financial, etc.)
     - Strategic pivots: $200k capital saved, 35x TAM expansion
     - 7 blind spots identified, 2 catastrophic risks prevented
     - Quality scores: 0.88, 0.92, 0.95 (escalating quality)
   
   - **Full Dataset Example**: `c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-example_v2.json`
     - 3 complete conversations across different domains:
       1. Apparel startup (plus-size sorority) - High complexity
       2. SaaS EdTech platform (K-12 engagement) - High complexity
       3. Specialty coffee shop - Medium complexity
     - 9 total training pairs (3 turns each)
     - Aggregated quality metrics: 0.92 avg synthesis quality, 4.33 blind spots/conversation
     - Domain diversity demonstrates cross-domain generalization

**What's Next** (For This Agent):

The next agent will create **Claude API generation prompts** for the Multi-Perspective + Purpose-Driven framework:

### **PRIMARY TASK: Create Prompt Templates for Multi-Perspective Generation**

**Context Required**:
1. **Study existing prompt template system** in `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`
   - How `prompt_templates` table is structured
   - How templates are used in `conversation-generation-service.ts`
   - Current scaffolding approach (personas, emotional_arcs, training_topics)
   - Claude API structured output implementation

2. **Review Multi-Perspective schemas and examples**:
   - Single conversation schema: `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v2.json`
   - Single conversation example: `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-example_v1.json`
   - Full dataset example: `c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-example_v2.json`

**Deliverables**:
1. **Master Prompt Template** for Multi-Perspective conversation generation
   - Uses Claude Structured JSON output feature (`anthropic-beta: structured-outputs-2025-11-13`)
   - Guides Claude to generate complete conversations matching single conversation schema
   - Includes instructions for:
     - Domain-specific persona identification
     - Purpose progression state management
     - Deliberation transcript generation with challenges/consensus
     - Blind spot identification requirements
     - Synthesis quality targets
   
2. **Turn-by-Turn Prompt Strategy**
   - Separate prompts for each turn type:
     - Market validation turn
     - Product definition turn
     - Legal/risk assessment turn
     - Financial modeling turn
   - Persona reweighting instructions per turn
   - Context accumulation from previous turns

3. **Domain Template Variants**
   - Business planning domain (apparel, SaaS, retail)
   - Healthcare decision support
   - Educational curriculum design
   - Expandable to other domains

4. **Quality Control Prompts**
   - Validation prompt to check generated conversations
   - Blind spot identification checklist
   - Purpose progression verification
   - Synthesis quality assessment

**Integration Notes**:
- Build **ON TOP OF** existing BrightRun functionality at `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`
- DO NOT rewrite existing generation pipeline
- Add new prompt templates to `prompt_templates` table
- New templates should work with existing Claude API integration
- Codebase changes will come later - focus on prompt design first

---

## 🎯 Multi-Perspective + Purpose-Driven Framework Overview

### What Is This Framework?

This is a **pioneering LoRA training methodology** that combines:

1. **Multi-Perspective Internal Deliberation**: AI simulates expert panel debates internally (e.g., founder + CFO + attorney + marketer debate business decisions)
2. **Purpose-Driven State Progression**: Conversations progress through defined states (idea → validated → launched)
3. **Dynamic Persona Weighting**: Expert influence adjusts based on purpose state (market researcher dominates validation phase, legal dominates risk phase)
4. **Synthesized Output**: AI outputs one coherent recommendation reflecting all perspectives, not separate viewpoints

### Why This Matters

**Current Problem (as of Dec 2025)**:
- LLMs miss critical perspectives users don't know to ask about
- Example: User asks "help me start a business" → Model provides good advice but misses licensing blockers, manufacturing constraints, contingency planning
- User must prompt 10+ times to get complete picture

**This Framework Solves**:
- AI automatically identifies 8 relevant expert personas (market researcher, attorney, CFO, risk planner, etc.)
- Personas debate internally, challenge assumptions, identify blind spots
- Model outputs complete analysis including needs user didn't state explicitly
- **64% better cross-domain generalization** vs simple multi-perspective training

### Key Innovation: Nobody Has Published This Integration Yet

**Dec 2025 Research Finding**:
- Multi-agent deliberation: ✅ Production-ready (MPDF framework)
- Purpose-driven LoRA: ✅ Established (AdaLoRA, MT-LoRA)
- Constitutional AI: ✅ Validated approach
- **Integration of all three: ❌ No published research** → **BrightRun's opportunity**

**12-18 month first-mover advantage window**

---

## 📂 Critical Files for Multi-Perspective Framework

### Framework Design & Analysis

| File | Purpose | Lines |
|------|---------|-------|
| **`pmc/context-ai/pmct/iteration-4-multi-perspective-datasets_v1.md`** | **PRIMARY REFERENCE** - Complete framework analysis, research findings, implementation roadmap | 1,689 |
| `pmc/context-ai/pmct/iteration-4-next-datasets_v2.md` | Earlier research on multi-perspective approaches, internal deliberation | 800+ |

**What's in `iteration-4-multi-perspective-datasets_v1.md`**:
- Part 1: Current state of multi-perspective training (Dec 2025 research)
- Part 2: EvertBody business plan analysis (demonstrates value)
- Part 3: Integration framework architecture (bidirectional influence model)
- Part 4: Viability assessment (training data requirements, generalization)
- Part 5: Implementation recommendations (phased rollout Q2 2026 → Q2 2027)
- Part 6: 2026 outlook (automated persona generation, hierarchical deliberation)
- **Part 7: Static vs Dynamic Persona Weighting** (300+ lines - implementation decision analysis)

### Production Schemas (v2 - Proper JSON Schema Format)

| File | Purpose | Lines |
|------|---------|-------|
| **`pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v2.json`** | **SINGLE CONVERSATION SCHEMA** - JSON Schema Draft 2020-12 for individual conversation generation | 1,018 |
| **`pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-schema_v2.json`** | **FULL DATASET SCHEMA** - Aggregates multiple conversations with quality metrics | 990 |

### Production Examples

| File | Purpose | Lines |
|------|---------|-------|
| **`pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-example_v1.json`** | **SINGLE CONVERSATION EXAMPLE** - Complete 3-turn business planning conversation (apparel startup) | 897 |
| **`pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-example_v2.json`** | **FULL DATASET EXAMPLE** - 3 conversations across domains (apparel, SaaS, coffee shop) | ~2,500 |

### Legacy Files (v1 - Example Format, Not Schema)

| File | Purpose | Note |
|------|---------|------|
| `pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-JSON-schema_v1.json` | Initial example conversation | This is NOT a schema - it's populated example data. Use v2 schemas instead. |

---

## 🔬 Framework Architecture Details

### Single Conversation Schema Structure

**Top-Level Fields** (from `single-dataset-JSON-schema_v2.json`):
```json
{
  "conversation_id": "string (UUID or descriptive)",
  "conversation_metadata": {
    "domain": "enum [entrepreneurship, healthcare, education, etc.]",
    "subdomain": "string",
    "complexity": "enum [low, medium, high, expert]",
    "purpose_progression_stages": "integer (2-10)",
    "total_turns": "integer (1-20)",
    "personas_involved": "integer (2-20)",
    "created_date": "ISO 8601 datetime",
    "generation_method": "enum [ai_generated_claude, ai_generated_gpt4, human_authored, hybrid]",
    "quality_tier": "enum [seed_dataset, production, experimental, review_needed]",
    "tags": ["array of strings"]
  },
  "purpose_framework": {
    "purpose_type": "string",
    "overall_starting_state": {
      "state_name": "string",
      "state_score": "number (0-1)",
      "characteristics": {
        "market_validation": "number (0-1)",
        "product_definition": "number (0-1)",
        // ... dimensional breakdown
      }
    },
    "overall_target_state": { /* same structure */ },
    "progression_stages": ["array of state transitions"]
  },
  "persona_library": {
    "personas": [
      {
        "persona_id": "string (pattern: ^[a-z_]+_[0-9]{3}$)",
        "role": "string",
        "expertise": ["array of expertise areas"],
        "perspective_focus": "string",
        "communication_style": "string",
        "weight_by_state": {
          "idea": 0.9,
          "market_validated": 0.7,
          // ... weights for each purpose state
        },
        "critical_blocker_likelihood": "number (0-1)",
        "identifies_blind_spots": "boolean"
      }
    ],
    "persona_selection_rationale": "string (min 50 chars)"
  },
  "training_pairs": [
    {
      "turn_number": "integer (min 1)",
      "turn_id": "string",
      "purpose_state_at_turn_start": {
        "current_state": "string",
        "current_score": "number (0-1)",
        "target_state_this_turn": "string",
        "target_score_this_turn": "number (0-1)",
        "gap_to_close_this_turn": "number (0-1)",
        "context_from_previous_turns": ["array of strings"]
      },
      "active_personas_this_turn": {
        "personas_weighted_for_this_state": [
          {
            "persona_id": "string",
            "weight": "number (0-1)",
            "rationale": "string (min 20 chars)"
          }
        ]
      },
      "user_input": "string (min 10 chars)",
      "internal_deliberation": {
        "deliberation_context": {
          "personas_know": {
            "current_purpose_state": "string",
            "next_target_state": "string",
            "ultimate_goal": "string",
            "user_context": "string"
          }
        },
        "deliberation_transcript": [
          {
            "speaker": "persona_id",
            "statement": "string (min 20 chars)",
            // 30+ optional fields for rich deliberation
            "challenges_to_others": ["array of persona_ids"],
            "identifies_blind_spot": "string",
            "user_didnt_ask_this": "boolean",
            "critical_blocker": "boolean",
            // ... many more optional fields
          }
        ],
        "consensus_building": {
          "areas_of_agreement": ["array of strings (min 1)"],
          "blind_spots_identified_by_deliberation": ["array"],
          "strategic_pivots_recommended": ["array"]
        }
      },
      "synthesized_output": {
        "response_to_user": "string (min 100 chars)",
        "incorporates_perspectives": ["array of strings (min 1)"],
        "blind_spots_identified_that_user_didnt_ask": ["array"],
        "quality_score": "number (0-1, target >0.85)"
      },
      "purpose_state_at_turn_end": {
        "achieved_state": "string",
        "achieved_score": "number (0-1)",
        "progression_this_turn": "number",
        "ready_for_next_state": "boolean"
      },
      "training_metadata": {
        "turn_type": "string",
        "personas_active_count": "integer (min 1)",
        "deliberation_depth": "enum",
        "blind_spots_identified": "integer (min 0)",
        "purpose_progression_target_met": "boolean"
      }
    }
  ]
}
```

### Full Dataset Schema Structure

**Top-Level Fields** (from `full-dataset-JSON-schema_v2.json`):
```json
{
  "dataset_metadata": {
    "schema_version": "brightrun-multi-lora-pipeline-v2.0",
    "dataset_type": "multi_perspective_deliberation_with_purpose_progression",
    "conversation_count": "integer",
    "total_training_pairs": "integer",
    "quality_summary": {
      "avg_synthesis_quality_score": "number (0-1)",
      "avg_purpose_progression_achieved": "number (0-1, target >0.75)",
      "avg_blind_spots_identified_per_conversation": "number (target 2-3)",
      "persona_identification_accuracy": "number (0-1, target >0.90)",
      "catastrophic_risks_prevented_count": "integer"
    },
    "framework_configuration": {
      "persona_weighting_approach": "enum [static_predefined, static_with_keyword_boosting, dynamic_learned_meta_policy]",
      "purpose_progression_methodology": "enum",
      "deliberation_depth_requirement": "enum",
      "blind_spot_detection_enabled": "boolean"
    }
  },
  "conversations": [
    /* Array of single conversation objects matching single schema */
  ]
}
```

### How Nesting Works

**Each purpose progression step triggers full multi-perspective deliberation where ALL personas are aware of**:
1. **Current state** (where you are now)
2. **Next target state** (immediate goal for this turn)
3. **Ultimate goal** (final destination - when helpful)
4. **Progress so far** (context from previous turns)

**Example Flow** (from single conversation example):
```
CONVERSATION: Business Planning (idea → investor_pitch_ready)
├─ TURN 1: Market Validation (0.1 → 0.4)
│  ├─ Active: market_researcher(0.9), fashion_expert(0.7), community_marketer(0.8)
│  ├─ Suppressed: legal(0.1), manufacturing(0.2) - premature
│  ├─ Deliberation: TAM sizing → challenged by community_marketer
│  │  • Blind spots identified: Price validation needed, Beta testing required
│  └─ Output: Market validated, realistic Year 1 expectations (0.42 achieved)
│
├─ TURN 2: Product Definition (0.42 → 0.65)
│  ├─ REWEIGHTING: fashion_expert NOW 0.95, manufacturing NOW 0.8
│  ├─                market_researcher REDUCED to 0.3 (validation done)
│  ├─ Deliberation: 8-style proposal → manufacturing challenges MOQ
│  │  • Critical blocker: $192k-320k inventory for 8 styles
│  │  • Strategic pivot: fashion expert proposes 1-hero-product
│  │  • Capital saved: $200k (85% reduction)
│  └─ Output: Product strategy refined, 1-hero-product focus (0.68 achieved)
│
└─ TURN 3: Legal & Risk (0.68 → 0.80)
   ├─ REWEIGHTING: legal NOW 0.95, risk_planner NOW 0.9
   ├─                fashion REDUCED to 0.2, manufacturing to 0.25
   ├─ Deliberation: attorney identifies 6-12 month licensing blocker
   │  • Critical blocker: AKA licensing can be denied, business model collapses
   │  • Blind spot: No contingency plan
   │  • Strategic pivot: Dual-track strategy (non-branded + AKA branded)
   │  • TAM expansion: 35x (144k → 5M)
   └─ Output: Legal structure + contingency (0.82 achieved, catastrophic failure prevented)
```

**Key Principles**:
- **Stateful personas**: Each persona "remembers" previous turns
- **Natural rotation**: Early-stage personas decrease weight as goals met
- **Accumulative synthesis**: Each turn builds on previous work (not replacement)
- **Ultimate goal conditional**: Shown when helpful (strategic planning), hidden when harmful (creative brainstorming)

---

## 📊 Static vs Dynamic Persona Weighting (Critical Decision)

### Current Recommendation (Dec 2025): Static Pre-Defined Weighting

**Schema A: Fully Static** (Implemented in our schemas)
```json
{
  "persona_id": "market_researcher",
  "weight_by_state": {
    "idea": 0.9,
    "market_validated": 0.7,
    "product_defined": 0.3,
    "legally_structured": 0.15
  }
}
```

**Why Static for Initial Implementation**:
- ✅ **Viable today** with Dec 2025 technology
- ✅ **Requires 300-500 examples** (vs 1,000-2,000 for dynamic)
- ✅ **Cost-effective**: $4k-7k dataset creation
- ✅ **Predictable & debuggable**: Weights consistent
- ✅ **Can ship Q2 2026** with confidence

---

## 🎯 Training Data Requirements

### Initial Implementation (Schema A - Static)

**Volume**: 300-500 complete conversations
- Each conversation: 3-6 turns (purpose progression stages)
- Each turn: Full deliberation transcript + synthesis
- Total training pairs: ~1,000-3,000

**Domains to Cover** (for generalization):
1. ✅ Business planning (3 examples created: apparel, SaaS, coffee shop)
2. Healthcare decision support
3. Educational curriculum design
4. Strategic consulting
5. Financial planning

**Cost Estimate**: $4,000-7,000
- Synthetic generation using Claude API
- 20% human quality validation
- 20 days generation + review

**Quality Criteria** (from our examples):
- Persona identification accuracy: >90% ✅ (achieved 95%)
- Purpose progression achieved: >75% of target state per turn ✅ (achieved 78% avg)
- Blind spots identified: 2-3 per conversation ✅ (achieved 4.33 avg)
- Synthesis incorporates all valid perspectives: 100%
- Avoided critical failures: 2+ per conversation ✅ (achieved 5 total across 3 conversations)

### Generation Approach (NEXT AGENT TASK)

```
1. Create Claude API prompts that generate conversations matching single schema
2. Use Claude Structured JSON output feature (anthropic-beta: structured-outputs-2025-11-13)
3. Prompt should guide:
   a) Domain-specific persona identification
   b) Persona weight assignment by purpose state
   c) Turn-by-turn deliberation with challenges/consensus
   d) Blind spot identification requirements
   e) Synthesis quality (target >0.85)
4. Quality validation (automated + human review)
5. Format validation against JSON schema
```

---

## 🏗️ Current BrightRun Application Context

### Existing Platform (at `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`)

The Multi-Perspective + Purpose framework builds **ON TOP OF** existing BrightRun capabilities:

**Current Application** (as of Dec 2025):
- ✅ Conversation generation pipeline (Claude API with structured outputs)
- ✅ 5-stage enrichment process
- ✅ Persona + emotional arc + training topic scaffolding
- ✅ Batch generation (242 conversations working example)
- ✅ Training file aggregation (brightrun-lora-v4 format)
- ✅ Supabase storage + PostgreSQL metadata
- ✅ Dashboard UI for management

**Recent Accomplishment** (Dec 6-8, 2025):
- Fixed edge case template generation (3 templates created)
- Generated production dataset: 242 conversations, 1,567 training pairs
- File: `pmc/_archive/full-file-training-json-242-conversations.json`

**Current Dataset**: Financial planning consultant vertical
- 3 personas × 7 emotional arcs × 17+ topics
- Average quality: 3/5 (AI-generated, not human-reviewed)
- Use case: LoRA fine-tuning experiments

### How Multi-Perspective Framework Extends This

**New Capabilities Added**:
1. **Multi-Perspective Deliberation**: Instead of single-voice generations, simulate expert panel debates
2. **Purpose Progression**: Track user's journey through states (idea → validated → launched)
3. **Dynamic Persona Weighting**: Adjust expert influence based on current state
4. **Blind Spot Detection**: AI identifies missing perspectives user didn't request
5. **Synthesized Output**: Coherent recommendations reflecting all expert viewpoints

**Integration Points** (Future work):
- **Personas table**: Expand to include expert personas (market_researcher, legal, CFO, etc.) not just client personalities
- **New table needed**: `purpose_states` - Define progression paths for different use cases
- **Generation service**: Enhance to support multi-turn deliberation generation
- **Schema**: Extend brightrun-lora-v4 to include deliberation transcripts, persona weighting
- **Quality metrics**: Add blind-spot detection, purpose progression tracking

### Current Prompt Template System

**Key Files to Study**:
- `src/lib/services/conversation-generation-service.ts` - Main generation logic
- `src/lib/templates/` - Template system
- Database table: `prompt_templates` - Template storage

**Current Template Structure** (from existing system):
```typescript
interface PromptTemplate {
  id: string;
  template_name: string;
  tier: 'template' | 'edge_case';
  emotional_arc_type: string;
  system_prompt: string;
  user_prompt_template: string;
  // ... more fields
}
```

**How Templates Are Used**:
1. User selects scaffolding (persona, emotional_arc, training_topic)
2. System loads matching prompt_template
3. Template is populated with scaffolding data
4. Claude API called with structured output schema
5. Response validated and stored

**Next Agent Must**:
- Study this existing system thoroughly
- Create new prompt templates for Multi-Perspective generation
- Use same infrastructure but with new prompts
- Ensure prompts guide Claude to generate conversations matching our v2 single schema

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

## 🚀 Next Agent Instructions: Create Claude API Generation Prompts

### PRIMARY TASK: Design Prompt Templates for Multi-Perspective Generation

The next agent is a **cutting-edge synthetic LoRA dataset expert** who specializes in creating prompts that leverage Claude's Structured JSON output feature.

### Required Reading (In Order)

1. **Current Codebase** (`C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`):
   - `src/lib/services/conversation-generation-service.ts` - How generation works
   - `src/lib/templates/` - Current template system
   - Database: `prompt_templates` table structure (use SAOL to inspect)
   - How scaffolding (personas, emotional_arcs, training_topics) feeds into templates

2. **Multi-Perspective Schemas**:
   - `pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v2.json` (1,018 lines) - **TARGET SCHEMA**
   - `pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-schema_v2.json` (990 lines) - Dataset aggregation

3. **Example Conversations**:
   - `pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-example_v1.json` (897 lines) - **REFERENCE EXAMPLE**
   - `pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-example_v2.json` - 3 domain examples

4. **Framework Analysis**:
   - `pmc/context-ai/pmct/iteration-4-multi-perspective-datasets_v1.md` (1,689 lines) - Complete framework design

### Deliverables

**1. Master System Prompt for Multi-Perspective Generation**
   - Instructs Claude on the Multi-Perspective + Purpose-Driven framework
   - Explains persona weighting concept
   - Defines deliberation quality requirements
   - Sets blind spot identification expectations
   - Quality targets: synthesis >0.85, purpose progression >0.75, blind spots 2-3/conversation

**2. User Prompt Template (Dynamic)**
   - Takes input: domain, subdomain, user_context_archetype
   - Generates: Complete conversation matching single conversation schema v2
   - Variables to populate:
     - `{DOMAIN}` - e.g., "entrepreneurship", "healthcare"
     - `{SUBDOMAIN}` - e.g., "apparel_startup_niche_market"
     - `{COMPLEXITY}` - e.g., "high"
     - `{USER_SCENARIO}` - e.g., "First-time founder wants to start plus-size apparel for sororities"
     - `{PURPOSE_TYPE}` - e.g., "business_launch_planning"
     - `{STARTING_STATE}` - e.g., "idea_stage"
     - `{TARGET_STATE}` - e.g., "investor_pitch_ready"
     - `{NUM_TURNS}` - e.g., 3

**3. Structured Output Schema Reference**
   - Simplified version of single conversation schema for Claude
   - Must match `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v2.json`
   - Use Claude's structured output feature: `anthropic-beta: structured-outputs-2025-11-13`

**4. Turn-Specific Guidance**
   - Instructions for different turn types:
     - **Market Validation Turn**: High weights on market_researcher, product_expert, risk_planner
     - **Product Definition Turn**: High weight on domain expert, manufacturing/ops, financial
     - **Legal/Risk Turn**: High weight on legal, risk_planner, contingency planning
     - **Financial Modeling Turn**: High weight on financial_analyst, risk_planner
   - Persona reweighting logic per turn
   - Context accumulation instructions

**5. Quality Checklist Prompt**
   - Validation prompt to verify generated conversation meets quality criteria:
     - [ ] 2-3 blind spots identified per conversation
     - [ ] Purpose progression >0.75 per turn
     - [ ] Synthesis quality >0.85
     - [ ] Persona weights change appropriately across turns
     - [ ] Deliberation includes challenges and consensus
     - [ ] Strategic pivots when appropriate
     - [ ] User assumptions challenged by personas

### Key Requirements

**Claude Structured JSON Output**:
- Use `anthropic-beta: structured-outputs-2025-11-13` header
- Provide schema to Claude for validation
- Ensure generated JSON matches schema exactly

**Integration with Existing System**:
- Build on existing prompt_templates table structure
- Don't break existing financial planning generation
- New templates should coexist with old templates
- May need new tier: `multi_perspective` (alongside `template` and `edge_case`)

**Domain Adaptability**:
- Prompts should work across domains (business, healthcare, education)
- Persona selection should be domain-aware
- Purpose states adapt to domain context
- Example domains from our examples:
  - Entrepreneurship: apparel, SaaS, specialty coffee
  - Healthcare: treatment decisions (to be created)
  - Education: curriculum design (to be created)

**Quality Targets** (from our examples):
- Synthesis quality: >0.85 (achieved 0.88-0.96 in examples)
- Purpose progression: >0.75 (achieved 0.78 avg)
- Blind spots: 2-3 per conversation (achieved 4.33 avg)
- Persona accuracy: >0.90 (achieved 0.95)

### Success Criteria

The prompts you create should enable Claude to generate conversations that:
1. ✅ Validate against `single-dataset-JSON-schema_v2.json` without errors
2. ✅ Include rich deliberation with challenges and consensus (not just agreement)
3. ✅ Identify blind spots user didn't explicitly ask about
4. ✅ Show persona weight changes across turns (natural rotation)
5. ✅ Achieve purpose progression targets (>0.75 per turn)
6. ✅ Produce strategic pivots when appropriate (preventing expensive mistakes)
7. ✅ Synthesize perspectives into coherent recommendations (not bullet points from each persona)

### Notes for Next Agent

**DO NOT**:
- Rewrite existing generation pipeline
- Modify database schema (yet)
- Change existing prompt templates
- Create code implementations (prompts only this session)

**DO**:
- Study existing system thoroughly
- Use SAOL to inspect `prompt_templates` table
- Reference example conversations extensively
- Design prompts that match schema exactly
- Think about turn-by-turn generation strategy
- Consider domain variations (business, healthcare, education)

**Future Work** (After prompts are created):
- Implement new generation service for multi-perspective
- Add database tables for purpose states
- Create UI for multi-perspective conversation generation
- Build batch generation for 300-500 training examples
- Validate quality metrics automatically

---

**Last Updated**: December 12, 2025  
**Session Focus**: Production schemas and examples created, ready for prompt template design  
**Current State**: Schemas validated, examples demonstrate quality targets, next step is Claude API prompt engineering  
**Document Version**: iii (Schema completion, prompt template design handoff)

