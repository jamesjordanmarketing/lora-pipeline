# Context Carryover: Multi-Perspective + Purpose-Driven Training Framework

## 📌 Active Development Focus

**Primary Task**: Implement and Expand Multi-Perspective + Purpose-Driven LoRA Training Dataset Framework

### Current Status: Framework Simplified and Production-Ready for Implementation

**What Was Completed** (December 13, 2025 - THIS SESSION):

1. ✅ **Framework Simplification - Removed Explicit Blind-Spot Engineering**
   - **Key Insight**: Domain experts naturally provide comprehensive coverage through their expertise - no artificial labeling needed
   - **Rationale**: When a licensing attorney, CFO, and risk planner deliberate, they inherently raise concerns the user didn't explicitly ask about. This is natural expertise, not a "blind spot" to be detected and labeled.
   - **Implementation**: Removed all explicit blind-spot detection fields while maintaining the same capability through natural multi-perspective deliberation

2. ✅ **Production Schema Updated to v3 (Simplified)**
   - **Single Conversation Schema v3**: `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v3.json`
     * Removed: `identifies_blind_spots`, `user_didnt_ask_about_this`, `blind_spot_identification`, `blind_spots_identified_by_deliberation`, `blind_spots_identified_that_user_didnt_ask`, `blind_spots_identified`
     * Result: Cleaner schema where personas simply contribute from their domain expertise
   
   - **Full Dataset Schema v3**: `c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-schema_v3.json`
     * Removed: `avg_blind_spots_identified_per_conversation`, `blind_spot_detection_enabled`
     * Removed: All blind-spot tracking fields from training metadata
     * Result: Simplified framework focused on multi-perspective deliberation naturally surfacing comprehensive coverage

3. ✅ **Specification Document Updated to v2**
   - **File**: `iteration-4-multi-perspective-datasets_v2.md`
   - **Changes**: 
     * Updated all terminology from "blind spot detection" to "comprehensive coverage" or "naturally comprehensive"
     * Emphasized that expert perspectives naturally surface what user didn't explicitly ask about
     * Maintained all technical architecture while simplifying conceptual model
     * Example: "Risk planner naturally raises concerns" vs "Risk planner identifies blind spot #3"

4. ✅ **Emotional Dataset Schema Updated to v5**
   - **File**: `c-alpha-build_v3.4_emotional-dataset-full-JSON-format_v5.json`
   - **Changes**: Removed blind-spot detection functionality to align with simplified approach
   - **Note**: This is for the existing emotional/financial planning vertical, updated for consistency

5. ✅ **Market Fit Analysis Reviewed**
   - **File**: `iteration-4-multi-perspective-market-fit_v1.md`
   - **Key Finding**: 70-80% probability of demonstrable effectiveness when properly scoped to single vertical
   - **Recommended First Vertical**: Fast-growth traction building and blue ocean product/business strategy
   - **Success Metric**: Human evaluators should prefer MP+PD-trained responses 65-75% of the time vs. baseline models

---

## 🎯 Multi-Perspective + Purpose-Driven Framework Overview (UPDATED)

### What Is This Framework?

This is a **pioneering LoRA training methodology** that combines:

1. **Multi-Perspective Internal Deliberation**: AI simulates expert panel debates internally (e.g., founder + CFO + attorney + marketer debate business decisions)
2. **Purpose-Driven State Progression**: Conversations progress through defined states (idea → validated → launched)
3. **Dynamic Persona Weighting**: Expert influence adjusts based on purpose state (market researcher dominates validation phase, legal dominates risk phase)
4. **Synthesized Output**: AI outputs one coherent recommendation reflecting all perspectives, not separate viewpoints
5. **Natural Comprehensive Coverage**: Expert personas naturally surface considerations the user didn't explicitly request - this emerges from domain expertise, not artificial detection

### Why This Matters

**Current Problem (as of Dec 2025)**:
- LLMs miss critical perspectives users don't know to ask about
- Example: User asks "help me start a business" → Model provides good advice but misses licensing blockers, manufacturing constraints, contingency planning
- User must prompt 10+ times to get complete picture

**This Framework Solves**:
- AI automatically identifies 8 relevant expert personas (market researcher, attorney, CFO, risk planner, etc.)
- Personas debate internally, challenge assumptions, naturally surface comprehensive considerations
- Model outputs complete analysis including concerns user didn't state explicitly
- **64% better cross-domain generalization** vs simple multi-perspective training

### Key Innovation: Nobody Has Published This Integration Yet

**Dec 2025 Research Finding**:
- Multi-agent deliberation: ✅ Production-ready (MPDF framework)
- Purpose-driven LoRA: ✅ Established (AdaLoRA, MT-LoRA)
- Constitutional AI: ✅ Validated approach
- **Integration of all three: ❌ No published research** → **BrightRun's opportunity**

**12-18 month first-mover advantage window**

---

## 📂 Critical Files for Multi-Perspective Framework (UPDATED)

### Framework Design & Analysis

| File | Purpose | Lines | Version |
|------|---------|-------|---------|
| **`pmc/context-ai/pmct/iteration-4-multi-perspective-datasets_v2.md`** | **PRIMARY REFERENCE** - Simplified framework analysis, research findings, implementation roadmap | 1,689 | **v2.0 (NEW)** |
| `pmc/context-ai/pmct/iteration-4-multi-perspective-datasets_v1.md` | Original framework with explicit blind-spot detection (superseded) | 1,683 | v1.0 |
| `pmc/context-ai/pmct/iteration-4-multi-perspective-market-fit_v1.md` | Market fit analysis and effectiveness assessment | 1,145 | v1.0 |
| `pmc/context-ai/pmct/iteration-4-next-datasets_v2.md` | Earlier research on multi-perspective approaches | 800+ | v2.0 |

**What's in `iteration-4-multi-perspective-datasets_v2.md`** (UPDATED):
- Part 1: Current state of multi-perspective training (Dec 2025 research)
- Part 2: EvertBody business plan analysis (demonstrates value)
- Part 3: Integration framework architecture (bidirectional influence model)
- Part 4: Viability assessment (training data requirements, generalization)
- Part 5: Implementation recommendations (phased rollout Q2 2026 → Q2 2027)
- Part 6: 2026 outlook (automated persona generation, hierarchical deliberation)
- **Part 7: Static vs Dynamic Persona Weighting** (300+ lines - implementation decision analysis)
- **NEW IN v2**: Simplified approach - removed explicit blind-spot engineering, emphasizes natural expertise

### Production Schema (UPDATED TO v3)

| File | Purpose | Version |
|------|---------|---------|
| **`pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v3.json`** | **SINGLE CONVERSATION SCHEMA** - Complete training data structure for one conversation | **v3.0 (NEW)** |
| **`pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-schema_v3.json`** | **FULL DATASET SCHEMA** - Aggregated training file structure | **v3.0 (NEW)** |
| `pmc/context-ai/pmct/training-data-seeds/c-alpha-build_v3.4_emotional-dataset-full-JSON-format_v5.json` | Emotional dataset schema (updated for consistency) | **v5.0 (NEW)** |

**Schema v3 Key Changes**:
```diff
REMOVED (Artificial Engineering):
- identifies_blind_spots (persona property)
- blind_spot_identification (deliberation statement property)
- user_didnt_ask_about_this (deliberation statement flag)
- blind_spots_identified_by_deliberation (consensus building property)
- blind_spots_identified_that_user_didnt_ask (synthesized output property)
- blind_spots_identified (training metadata counter)
- avg_blind_spots_identified_per_conversation (quality summary)
- blind_spot_detection_enabled (framework configuration)

RETAINED (Natural Expertise):
+ Expert personas with domain expertise arrays
+ Deliberation statements where experts naturally raise their concerns
+ Consensus building showing comprehensive considerations
+ Synthesized output incorporating all perspectives
+ Quality scoring based on comprehensiveness and actionability
```

**Schema Structure (v3 Simplified)**:
```json
{
  "conversation_id": "conv_business_plan_001",
  "conversation_metadata": { domain, complexity, purpose_progression_stages },
  "purpose_framework": {
    "overall_starting_state": { state_name: "idea_stage", state_score: 0.1 },
    "overall_target_state": { state_name: "investor_pitch_ready", state_score: 0.9 },
    "progression_stages": [ "idea → market_validated → product_defined → ..." ]
  },
  "persona_library": {
    "personas": [
      {
        "persona_id": "market_researcher_001",
        "role": "Market Research Analyst",
        "expertise": ["market_sizing", "competitive_analysis", "TAM_SAM_SOM"],
        "perspective_focus": "data_driven_market_validation",
        "weight_by_state": { "idea": 0.9, "product_defined": 0.3 },
        "unique_value": "Identifies fit as competitive moat, not just sizing"
      }
      // 8 total personas for business planning use case
    ]
  },
  "training_pairs": [
    {
      "turn_number": 1,
      "purpose_state_at_turn_start": { current: 0.1, target: 0.4 },
      "active_personas_this_turn": {
        "personas_weighted_for_this_state": [
          { "persona_id": "market_researcher", "weight": 0.9, "rationale": "..." }
        ]
      },
      "internal_deliberation": {
        "deliberation_transcript": [
          {
            "speaker": "market_researcher",
            "statement": "Let's size the market. AKA has 360,000 members...",
            "reasoning": "Market validation requires TAM analysis",
            "supports": ["establishes addressable market"]
          },
          {
            "speaker": "community_marketer",
            "statement": "Year 1 TAM realistically 200-500 early adopters, not 144k",
            "challenges_to_others": ["market_researcher"],
            "refines_to": "More realistic Year 1 expectations"
          }
        ],
        "consensus_building": {
          "areas_of_agreement": ["Premium positioning validated"],
          "risks_identified": ["Licensing timeline", "MOQ constraints"],
          "strategic_pivots_recommended": ["1-product launch vs 8-style"]
        }
      },
      "synthesized_output": {
        "response_to_user": "Based on our analysis...",
        "incorporates_perspectives": ["Market researcher: TAM", "Fashion expert: differentiation"],
        "quality_score": 0.85
      },
      "purpose_state_at_turn_end": { achieved_score: 0.42 }
    }
  ]
}
```

**Key Schema Features (v3)**:
- **Nested structure**: Conversation → Turns → Deliberations → Synthesis
- **State-driven weighting**: Each turn specifies persona weights based on current purpose state
- **Context accumulation**: Later turns reference earlier decisions
- **Ultimate goal awareness**: Personas know final destination (when helpful for strategic decisions)
- **Natural comprehensive coverage**: Expert statements naturally address concerns user didn't explicitly raise
- **Simpler generation**: No need to artificially categorize or label "blind spots"

---

## 🔬 Framework Architecture Details

### How Nesting Works

**Each purpose progression step triggers full multi-perspective deliberation where ALL personas are aware of**:
1. **Current state** (where you are now)
2. **Next target state** (immediate goal for this turn)
3. **Ultimate goal** (final destination - when helpful)
4. **Progress so far** (context from previous turns)

**Example Flow** (Simplified v3):
```
CONVERSATION: Business Planning (idea → investor_pitch_ready)
├─ TURN 1: Market Validation (0.1 → 0.4)
│  ├─ Active: market_researcher(0.9), fashion_expert(0.7), community_marketer(0.8)
│  ├─ Suppressed: legal(0.1), manufacturing(0.2) - premature
│  ├─ Deliberation: 
│  │   - Market researcher: Sizes TAM at 144k
│  │   - Community marketer: Challenges ("Realistically 200-500 Year 1")
│  │   - Market researcher: Revises based on feedback
│  │   → Natural comprehensive coverage through expert debate
│  └─ Output: Market validated, realistic Year 1 expectations (0.42 achieved)
│
├─ TURN 2: Product Definition (0.42 → 0.65)
│  ├─ REWEIGHTING: fashion_expert NOW 0.95, manufacturing NOW 0.8
│  ├─                market_researcher REDUCED to 0.3 (validation done)
│  ├─ Deliberation:
│  │   - Fashion expert: Proposes 8 styles
│  │   - Manufacturing: Raises MOQ concerns ($200k inventory)
│  │   - Financial: Validates cost impact
│  │   - Fashion: Pivots to 1-hero-product strategy
│  │   → Comprehensive coverage through cross-functional expertise
│  └─ Output: Product strategy refined, capital saved $185k (0.68 achieved)
│
└─ TURN 3: Legal & Risk (0.68 → 0.80)
   ├─ REWEIGHTING: legal NOW 0.95, risk_planner NOW 0.9
   ├─ Deliberation:
   │   - Attorney: Identifies 6-12 month licensing timeline
   │   - Risk planner: Raises contingency question ("What if rejected?")
   │   - Attorney: Proposes dual-track strategy (Plan B)
   │   → Natural risk identification through expert domain knowledge
   └─ Output: Legal structure + contingency (0.82 achieved)
```

**Key Principles**:
- **Stateful personas**: Each persona "remembers" previous turns
- **Natural rotation**: Early-stage personas decrease weight as goals met
- **Accumulative synthesis**: Each turn builds on previous work (not replacement)
- **Natural comprehensiveness**: Experts raise domain concerns without artificial labeling
- **Ultimate goal conditional**: Shown when helpful (strategic planning), hidden when harmful (creative brainstorming)

---

## 📊 Static vs Dynamic Persona Weighting (Critical Decision)

### Current Recommendation (Dec 2025): Static Pre-Defined Weighting

**Schema A: Fully Static**
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

**Disadvantages**:
- ❌ Inflexible to exceptions (user asks legal question during design phase → legal still weighted 0.15)
- ❌ Requires manual weight design (8 personas × 6 states = 48 values)
- ❌ Cannot learn from feedback

### Future Option: Dynamic Learned Weighting

**Schema C: Fully Dynamic (2026-2027 Research Goal)**
- Model learns meta-policy to adjust weights based on query content
- Example: User says "I'm worried about trademark issues" during product_defined phase
  → Dynamic system boosts legal weight from 0.15 → 0.9 for that specific turn
- **Requires**: 1,000-2,000 examples, RL training, meta-policy architecture
- **Cost**: $12k-20k dataset creation
- **Viability**: Research prototype Q4 2026, production maybe Q2 2027

### Phased Roadmap

**Q2 2026: Launch Schema A (Static)**
- 300-500 training examples
- Price: $5k-10k per dataset
- **Rationale**: Proven, reliable, establishes market position

**Q4 2026: Upgrade to Schema B (Hybrid)**
- Static base + keyword boosting rules
- Example: if query contains "legal" → boost legal persona weight
- 400-600 training examples
- Price: $7k-12k
- **Rationale**: Better contextual relevance, still deterministic

**Q2 2027: Pilot Schema C (Dynamic)**
- Fully learned meta-policy (cautiously with 2-3 beta clients)
- 1,000+ examples
- Custom pricing: $15k-25k
- **Rationale**: Stay at forefront, validate before production

**Industry Prediction**: Will converge on Schema B (hybrid) as production standard by late 2027, with Schema C (dynamic) remaining premium feature for high-value use cases only.

---

## 🎯 Training Data Requirements

### Initial Implementation (Schema A - Static, v3 Simplified)

**Volume**: 300-500 complete conversations
- Each conversation: 4-6 turns (purpose progression stages)
- Each turn: Full deliberation transcript + synthesis
- Total training pairs: ~1,500-3,000

**Domains to Cover** (for generalization):
1. **Business planning** (current example) - Fast-growth traction building, blue ocean strategy
2. Healthcare decision support
3. Educational curriculum design
4. Strategic consulting
5. Financial planning

**Cost Estimate**: $4,000-7,000
- Synthetic generation using GPT-4/Claude
- 20% human quality validation
- 20 days generation + review

**Quality Criteria** (Updated for v3):
- Persona identification accuracy: >90%
- Purpose progression achieved: >75% of target state per turn
- Natural comprehensive coverage: Experts raise 2-3+ concerns user didn't explicitly request per conversation
- Synthesis incorporates all valid perspectives: 100%
- Avoided critical failures: 2+ per conversation
- Deliberation quality: Multi-round with challenges and consensus

### Generation Approach (Simplified for v3)

```
1. Select domain + use case (e.g., "start apparel business for plus-size sorority members")
2. Define purpose progression (idea → launch_ready, 6 stages)
3. Prompt GPT-4/Claude to generate:
   a) Relevant expert personas for this domain/stage
   b) Persona weights by stage
   c) Stage-by-stage deliberation where experts naturally contribute from their domain
   d) Synthesis for each stage incorporating all perspectives
4. Quality review (20% human validation):
   - Do personas speak from genuine domain expertise?
   - Do experts naturally raise important concerns?
   - Is synthesis comprehensive and actionable?
5. Format as training JSON per v3 schema
```

**Key Difference in v3 Generation**:
- **OLD (v1/v2)**: "Have the risk planner identify blind spot #3: contingency planning"
- **NEW (v3)**: "The risk planner, from their domain expertise in startup risk mitigation, naturally asks 'What if AKA rejects the licensing application?'"

---

## 📈 Expected Outcomes & Metrics

### Business Impact

**Compared to baseline (no multi-perspective training)**:
- **Output quality**: 8.7/10 vs 6.5/10
- **Completeness**: 85% vs 60%
- **Natural comprehensive coverage**: 80% vs 10%
- **User prompting required**: Minimal (auto-adapts) vs Extensive (10+ follow-ups)

**EvertBody Case Study Results** (analysis in iteration-4 doc):
- Auto-identified 8 relevant expert personas (vs user had to manually prompt for sales/personas)
- Naturally surfaced critical concerns:
  * AKA licensing: 6-12 month timeline + $10k-25k annual minimum (user assumed formality)
  * MOQ reality: $50k-120k initial inventory (user hadn't considered)
  * Contingency plan if licensing rejected (risk planner's domain expertise)
- Strategic pivots:
  * From 8-style launch ($200k capital) to 1-hero-product ($15k capital) - saved $185k
  * From AKA-only to diversified brand strategy - prevented business model collapse
- **Realistic timeline**: 18-24 months vs user's implied 6-12 months
- **Realistic costs**: $75k-150k vs implied $20k-40k

### Technical Validation

**Generalization Test**:
> Research evidence: "Trained on business strategy debates. Tested on personal finance decisions (different domain). Still applied deliberation framework 64% of the time (vs 34% for explicit perspective-showing)."

**Why purpose-driven helps generalization**:
- Purpose states are UNIVERSAL (idea→validated→launched applies to ANY domain)
- Persona types are TRANSFERABLE (financial, legal, operational perspectives needed everywhere)
- The PATTERN transfers, not just content
- Natural expertise coverage generalizes better than artificial labeling

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

**New Capabilities Added** (v3 Simplified):
1. **Multi-Perspective Deliberation**: Instead of single-voice generations, simulate expert panel debates where experts naturally contribute from domain knowledge
2. **Purpose Progression**: Track user's journey through states (idea → validated → launched)
3. **Dynamic Persona Weighting**: Adjust expert influence based on current state
4. **Natural Comprehensive Coverage**: Experts inherently raise concerns beyond user's explicit questions
5. **Synthesized Output**: Coherent recommendations reflecting all expert viewpoints

**Integration Points**:
- **Personas table**: Expand to include expert personas (market_researcher, legal, CFO, etc.) not just client personalities
- **New table needed**: `purpose_states` - Define progression paths for different use cases
- **Generation service**: Enhance to support multi-turn deliberation generation
- **Schema**: Extend brightrun-lora-v4 to include deliberation transcripts, persona weighting
- **Quality metrics**: Track comprehensive coverage quality, purpose progression tracking

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

### Context for Next Agent

**You are continuing work on the Multi-Perspective + Purpose-Driven LoRA training framework.**

**Critical Context**:
1. **Framework has been simplified (v3)** - Removed explicit "blind-spot" detection. Expert personas now naturally provide comprehensive coverage through their domain expertise.
2. **Schemas are production-ready (v3)** - Use these for generation:
   - Single conversation: `c-alpha-build_v3.4_multi-lora-pipeline-single-dataset-JSON-schema_v3.json`
   - Full dataset: `c-alpha-build_v3.4_multi-lora-pipeline-full-dataset-JSON-schema_v3.json`
3. **Building on existing codebase** - Located at `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src`
4. **First vertical identified** - Fast-growth traction building and blue ocean product/business strategy

### Required Reading (IN ORDER)

1. **THIS DOCUMENT** - Context carryover with framework overview
2. **`iteration-4-multi-perspective-datasets_v2.md`** - Complete framework specification (simplified)
3. **`iteration-4-multi-perspective-market-fit_v1.md`** - Market fit analysis and effectiveness assessment
4. **Schema v3 files** (listed above) - Production data structures
5. **Existing codebase** - `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\src` - Understand current generation pipeline

### Primary Task Options

#### **Option 1: Build Expert Generation Prompts (RECOMMENDED NEXT)**
1. **Study v3 Schemas**: Internalize simplified structure where experts contribute naturally
2. **Create Claude Prompts**: Build prompts that generate multi-perspective deliberations for first vertical (fast-growth traction building)
3. **Prompt Components Needed**:
   - Persona identification prompt (given domain → identify 8 relevant experts)
   - Deliberation generation prompt (given personas + purpose state → generate debate transcript)
   - Synthesis prompt (given deliberation → create unified recommendation)
   - Full conversation prompt (orchestrate all above for 4-6 turn conversation)
4. **Test Prompts**: Generate 5-10 example conversations manually to validate quality
5. **Document Patterns**: What works, what doesn't, refinements needed

#### **Option 2: Extend Generation Pipeline**
1. **Review Existing Code**: `src/lib/services/conversation-generation-service.ts`
2. **Design Multi-Perspective Extension**:
   - How to integrate persona weighting?
   - How to manage multi-turn with state progression?
   - How to generate deliberation transcripts?
3. **Implement Prototype**: Add multi-perspective capability to existing pipeline
4. **Test with v3 Schema**: Generate conversations following new structure
5. **Validate Quality**: Do deliberations feel authentic? Do personas contribute from domain expertise?

#### **Option 3: Generate First Training Dataset**
1. **Select Domain**: Fast-growth traction building (recommended first vertical)
2. **Define Use Cases**: 10-20 specific scenarios (e.g., "SaaS product launch", "marketplace business model")
3. **Generate Examples**: Create 50-100 conversations using v3 schema
4. **Quality Review**: 20% human validation
5. **Format for LoRA**: Prepare dataset for fine-tuning
6. **Document Results**: Quality metrics, patterns observed

### Key Considerations

**When Working on This Framework**:
- ✅ **Use v3 schemas** - Simplified approach without explicit blind-spot engineering
- ✅ **Reference v2 spec** - `iteration-4-multi-perspective-datasets_v2.md` is source of truth
- ✅ **Build on existing codebase** - Extend, don't replace the working pipeline at `lora-pipeline/src`
- ✅ **Focus on natural expertise** - Personas contribute from domain knowledge, not artificial labels
- ✅ **Start with first vertical** - Fast-growth traction building, blue ocean strategy
- ❌ **Don't engineer blind-spots** - Let comprehensive coverage emerge naturally from expert deliberation

**Generation Philosophy (v3)**:
```
OLD (v1/v2): "Generate blind spot #3 where risk planner identifies missing contingency"
NEW (v3):    "The risk planner, from their expertise in startup risk mitigation, asks: 
              'What's your contingency if this doesn't work?' This naturally surfaces 
              a concern the user hadn't considered."
```

**Success Criteria**:
- Training data where experts authentically contribute from domain knowledge
- Purpose progression that guides conversation toward goals
- Persona deliberation that challenges assumptions and improves recommendations
- Natural comprehensive coverage (2-3+ concerns surfaced that user didn't explicitly request)
- Cross-domain generalization (patterns transfer, not just content)

---

**Last Updated**: December 13, 2025  
**Session Focus**: Framework Simplified (v3) - Removed Explicit Blind-Spot Engineering  
**Current State**: Production v3 schemas ready, specification updated, ready for prompt engineering and generation  
**Document Version**: kk (Multi-perspective v3 simplified handoff)
