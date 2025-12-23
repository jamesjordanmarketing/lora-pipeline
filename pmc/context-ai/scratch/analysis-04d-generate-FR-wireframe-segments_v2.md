# Operational Analysis: 04d-generate-FR-wireframe-segments_v1.js

**Analysis Date:** December 22, 2025  
**Analyzer:** Antigravity AI  
**Script Analyzed:** `pmc\product\_tools\04d-generate-FR-wireframe-segments_v1.js`

---

## Executive Summary

This script is a **prompt generator** (also called a "meta-prompt generator") that automates the creation of AI prompts for generating Figma wireframes from functional requirements. It transforms structured product specifications into ready-to-use prompts that can be fed to an AI coding agent (like Claude) to create UI wireframe designs.

The system follows a **3-tier prompt architecture**:
1. **Script runs** → Creates "Generator Prompts" (meta-prompts)
2. **AI Agent runs Generator Prompts** → Creates "Figma-Ready Prompts"  
3. **Figma Make AI runs Final Prompts** → Creates actual wireframes

---

## 1. Input Templates, References & Examples Used

### Primary Input Templates

| Template | Location | Purpose |
|----------|----------|---------|
| **Task Creation Template** | `pmc/product/_prompt_engineering/04-FR-with-wireframes-create-tasks_v1.md` | Defines how to generate comprehensive task inventories from requirements + wireframes for React applications |
| **Execution Template** | `pmc/product/_prompt_engineering/04-FR-with-wireframes-execution-prompts_v1.md` | Defines how to convert task inventories into executable SQL instructions and implementation prompts |

### Reference Documents

| Reference | Location | Purpose |
|-----------|----------|---------|
| **Product Overview** | `pmc/product/01-[prod-abbr]-overview.md` | Product vision, goals, architecture, scope |
| **User Stories** | `pmc/product/02-[prod-abbr]-user-stories.md` | User requirements and acceptance criteria |
| **User Journey** | `pmc/product/02b-[prod-abbr]-user-journey.md` | User flow and emotional journey mapping |
| **Functional Requirements** | `pmc/product/03-[prod-abbr]-functional-requirements.md` | Detailed FR specifications with acceptance criteria |
| **Journey Mapping Data** | `pmc/product/_mapping/journey-to-wireframe-mapping.json` | Maps user journey stages to wireframe design elements (goals, emotions, progressive disclosure, success indicators) |

### Example Context

The journey mapping JSON provides rich context for each of 9 user journey stages, including:
- **Goals**: What users are trying to accomplish (e.g., "First-time platform discovery", "Content ingestion and upload")
- **Emotions**: How to address user emotional states (e.g., "Build confidence through simple language", "Reduce anxiety with progress indicators")
- **Progressive Disclosure Levels**: Basic → Advanced → Expert feature rollout
- **Success Indicators**: What defines successful completion of each stage

---

## 2. Input Specification Used

### Main Input: Functional Requirements Document

**File:** `pmc/product/03-[prod-abbr]-functional-requirements.md`

The script parses this document expecting a very specific structure:

```markdown
## 1. [Section Title]

- **FR1.1.0:** [FR Title]
  * Description: [text]
  * User Story Acceptance Criteria: [list]
  * Functional Requirements Acceptance Criteria: [list]

- **FR1.2.0:** [Another FR]
  ...

## 2. [Next Section Title]
...
```

**Key Parsing Rules:**
- Sections are identified by `## X. [Title]` headers (e.g., `## 1. Database Foundation`)
- Each section becomes a numbered "E[XX]" segment (E01, E02, E03, etc.)
- FRs are identified by pattern `**FRX.Y.Z:**` (e.g., FR1.1.1, FR2.3.2)
- The script extracts FR numbers for each section automatically

### Command-Line Inputs

```bash
node 04d-generate-FR-wireframe-segments_v1.js "<Project Name>" <project-abbreviation>
```

**Example:**
```bash
node 04d-generate-FR-wireframe-segments_v1.js "Bright Run LoRA Fine-Tuning Training Data Platform" bmo
```

---

## 3. What Running the Script Does

When you run the script, it performs these operations:

### Step 1: Parse Functional Requirements
- Reads the FR document at `pmc/product/03-[prod-abbr]-functional-requirements.md`
- Splits it into sections based on `## X.` headers
- Assigns section IDs (E01, E02, E03, etc.)
- Extracts all FR numbers from each section

### Step 2: Load Templates
- Loads the task creation template
- Loads the execution template
- Loads the journey mapping JSON

### Step 3: Generate "Generator Prompts" (Per-FR)
For each FR in each section, the script:
- Fills in all template placeholders with FR-specific values
- Injects journey context (goals, emotions, progressive disclosure, success indicators)
- Calculates the line number where each FR block starts
- Appends the filled template to a combined output file

**Output Location:** `pmc/product/_mapping/fr-maps/prompts/04-FR-wireframes-prompt-E[XX].md`

### Step 4: Generate "Execution Prompts" (Per-Section)
For each section, the script:
- Creates a single execution prompt covering all FRs in that section
- Includes references to previous section outputs for context continuity
- Injects journey-informed design elements

**Output Location:** `pmc/product/_mapping/fr-maps/prompts/04-FR-wireframes-execution-prompt-E[XX].md`

### Step 5: Create Output Directories
- Ensures `pmc/product/_mapping/fr-maps/` exists
- Ensures `pmc/product/_mapping/fr-maps/prompts/` exists

---

## 4. Does It Create Prompts to Run?

**Yes, absolutely.** This is the script's primary purpose.

It creates **two types of prompts**:

### Type A: Generator Prompts (Per-FR)
- **What they are:** Meta-prompts that instruct an AI agent to generate Figma-ready wireframe prompts
- **Location:** `prompts/04-FR-wireframes-prompt-E[XX].md`
- **Quantity:** One file per section, containing multiple per-FR prompt blocks
- **Who runs them:** A human or AI coding agent (like Claude 4.5 Sonnet)

### Type B: Execution Prompts (Per-Section)
- **What they are:** Meta-prompts that instruct an AI agent to convert task inventories into implementation instructions
- **Location:** `prompts/04-FR-wireframes-execution-prompt-E[XX].md`
- **Quantity:** One file per section
- **Who runs them:** A human or AI coding agent

---

## 5. What Those Prompts Do

### Generator Prompts Purpose

When an AI agent is given a Generator Prompt, it will:

1. **Read** the source documents (Overview, User Stories, User Journey, FR Spec)
2. **Locate** the specific FR in the FR mapping document
3. **Extract** all acceptance criteria (User Story + Functional Requirements)
4. **Classify** each criterion as UI-relevant vs Non-UI
5. **Compute** a Page Plan (minimum 3 pages) to satisfy all UI-relevant criteria
6. **Output** a self-contained Figma Make AI prompt that:
   - Embeds all UI-relevant acceptance criteria
   - Includes journey integration (goals, emotions, progressive disclosure)
   - Defines explicit UI requirements (components, states, interactions)
   - Specifies a page plan with screen names and purposes
   - Maps acceptance criteria to UI components
   - Includes accessibility guidance and information architecture

**Output Format for Generator Prompts:**
```markdown
=== BEGIN PROMPT FR: FR1.1.1 ===

**Title**: FR FR1.1.1 Wireframes — Stage 1 — [Stage Name]

**Context Summary**: [2-4 sentences]

**Journey Integration**: [user goals, emotions, progressive disclosure]

**Wireframe Goals**: [bulleted list]

**Explicit UI Requirements**: [from acceptance criteria]

**Interactions and Flows**: [navigation and interactions]

**Page Plan**: [list of screens with purposes]

**Acceptance Criteria → UI Component Mapping**: [table]

**Estimated Page Count**: [number + rationale]

=== END PROMPT FR: FR1.1.1 ===
```

### Execution Prompts Purpose

When an AI agent is given an Execution Prompt, it will:

1. **Analyze** the completed task inventory
2. **Examine** the current codebase state
3. **Assess** risk factors and complexity
4. **Generate** strategic implementation prompts optimized for 200k token context windows
5. **Output** executable instructions including:
   - Database SQL operations
   - Implementation prompts for developers/AI agents
   - Quality validation checklists
   - Cross-prompt consistency requirements

---

## 6. Complete Operational Flow

Here is the **full nested flow** from running the script to final wireframes:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LEVEL 0: SCRIPT EXECUTION                       │
│  node 04d-generate-FR-wireframe-segments_v1.js "Project Name" proj-abbr      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUTS TO SCRIPT                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Functional Requirements Doc: pmc/product/03-proj-abbr-functional-req.md   │
│ • Task Creation Template: pmc/product/_prompt_engineering/04-FR-*.md        │
│ • Execution Template: pmc/product/_prompt_engineering/04-FR-*-execution.md  │
│ • Journey Mapping: pmc/product/_mapping/journey-to-wireframe-mapping.json   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LEVEL 1: SCRIPT OUTPUTS                               │
│                        (Meta-Prompts / Generator Prompts)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ OUTPUT A - Generator Prompts (one file per section, multiple FR blocks):    │
│   • prompts/04-FR-wireframes-prompt-E01.md                                   │
│   • prompts/04-FR-wireframes-prompt-E02.md                                   │
│   • prompts/04-FR-wireframes-prompt-E03.md                                   │
│   • ... (one per section in the FR doc)                                      │
│                                                                              │
│ OUTPUT B - Execution Prompts (one file per section):                         │
│   • prompts/04-FR-wireframes-execution-prompt-E01.md                         │
│   • prompts/04-FR-wireframes-execution-prompt-E02.md                         │
│   • ... (one per section in the FR doc)                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
          ┌────────────────────────────┴────────────────────────────┐
          ▼                                                         ▼
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│ PATH A: WIREFRAME GENERATION    │       │ PATH B: IMPLEMENTATION          │
│ (Using Generator Prompts)       │       │ (Using Execution Prompts)       │
└─────────────────────────────────┘       └─────────────────────────────────┘
          │                                         │
          ▼                                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEVEL 2: AI AGENT RUNS GENERATOR PROMPTS                  │
│                    (Human gives Generator Prompt to Claude/GPT)              │
├─────────────────────────────────────────────────────────────────────────────┤
│ INPUTS THE AI AGENT READS:                                                   │
│   • pmc/product/01-proj-abbr-overview.md (Product Overview)                  │
│   • pmc/product/02-proj-abbr-user-stories.md (User Stories)                  │
│   • pmc/product/02b-proj-abbr-user-journey.md (User Journey)                 │
│   • pmc/product/03-proj-abbr-functional-requirements.md (Full FR Doc)        │
│   • pmc/product/_mapping/fr-maps/04-proj-abbr-FR-wireframes-E[XX].md         │
│       (Section-specific FR subset)                                           │
│   • train-wireframe/src/* (Current implementation codebase)                  │
│                                                                              │
│ WHAT THE AI AGENT DOES:                                                      │
│   1. Extracts all acceptance criteria for each FR                            │
│   2. Classifies criteria as UI-relevant vs Non-UI                            │
│   3. Computes a page plan (≥3 pages) satisfying UI criteria                  │
│   4. Generates a self-contained Figma-ready prompt                           │
│                                                                              │
│ OUTPUT:                                                                       │
│   • pmc/product/_mapping/fr-maps/04-proj-abbr-FIGMA-wireframes-output-E[XX].md│
│     (Appends Figma-ready prompts between === BEGIN/END PROMPT === markers)   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   LEVEL 3: FIGMA MAKE AI RUNS FINAL PROMPTS                  │
│                   (Human pastes Figma-ready prompt into Figma)               │
├─────────────────────────────────────────────────────────────────────────────┤
│ INPUT:                                                                        │
│   • The Figma-ready prompt block from Level 2 output                          │
│     (Text between === BEGIN PROMPT FR: FRX.X.X === and === END PROMPT ===)   │
│                                                                              │
│ WHAT FIGMA MAKE AI DOES:                                                     │
│   1. Interprets the UI requirements as screen designs                        │
│   2. Creates wireframe pages matching the page plan                          │
│   3. Adds annotations mapping acceptance criteria to components              │
│   4. Generates states (loading, error, empty, success, etc.)                 │
│                                                                              │
│ OUTPUT:                                                                       │
│   • Figma wireframe file with:                                               │
│     - 3-6 pages per FR                                                       │
│     - Components for each UI requirement                                      │
│     - Annotations linking criteria to components                             │
│     - Mapping table frame                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary Table: Complete Flow

| Step | Actor | Input | Action | Output |
|------|-------|-------|--------|--------|
| **0** | Human | Project name, abbreviation | Runs Node.js script | Generator prompts + Execution prompts |
| **1.A** | AI Agent (Claude) | Generator prompts + source docs | Extracts criteria, classifies, computes page plan | Figma-ready prompts |
| **1.B** | AI Agent (Claude) | Execution prompts + task inventory | Analyzes complexity, generates implementation instructions | SQL + dev prompts |
| **2** | Figma Make AI | Figma-ready prompts | Interprets and designs | Wireframe screens |
| **3** | Developers | Implementation prompts | Builds React components | Working UI application |

---

## Key Files Summary

### Inputs
| File | Type | Description |
|------|------|-------------|
| `03-[abbr]-functional-requirements.md` | Spec | Master functional requirements document |
| `04-FR-with-wireframes-create-tasks_v1.md` | Template | Task generation template |
| `04-FR-with-wireframes-execution-prompts_v1.md` | Template | Execution prompt template |
| `journey-to-wireframe-mapping.json` | Data | User journey emotional/UX mapping |

### Outputs
| File | Type | Description |
|------|------|-------------|
| `prompts/04-FR-wireframes-prompt-E[XX].md` | Generator Prompts | Per-section FR generator prompts |
| `prompts/04-FR-wireframes-execution-prompt-E[XX].md` | Execution Prompts | Per-section implementation prompts |
| `04-[abbr]-FIGMA-wireframes-output-E[XX].md` | Final Prompts | AI-generated Figma-ready prompts |

---

## Conclusion

The `04d-generate-FR-wireframe-segments_v1.js` script is a **prompt engineering automation tool** that:

1. **Reads** structured product specifications (functional requirements)
2. **Generates** meta-prompts (generator prompts) that instruct AI to create wireframe prompts
3. **Injects** user journey context (goals, emotions, progressive disclosure) for UX-informed designs
4. **Produces** prompts that can be chain-executed: Script → AI Agent → Figma Make AI → Wireframes

This creates a **reproducible, automated pipeline** for transforming product requirements into UI designs with minimal manual intervention, while maintaining traceability from acceptance criteria to wireframe components.

---
---

# Operational Analysis: 04a-generate-FIGMA-wireframe-prompts_v1.js

**Analysis Date:** December 22, 2025  
**Analyzer:** Antigravity AI  
**Script Analyzed:** `pmc\product\_tools\04a-generate-FIGMA-wireframe-prompts_v1.js`

---

## Executive Summary

This script is a **Figma-focused prompt generator** that creates meta-prompts specifically designed for the Figma Make AI wireframe generation workflow. Unlike the 04d script which has a dual-purpose architecture (both wireframe prompts AND execution/implementation prompts), this script focuses solely on generating prompts that will become Figma wireframes.

The system follows a **3-tier prompt architecture** (same as 04d):
1. **Script runs** → Creates "Generator Prompts" (meta-prompts)
2. **AI Agent runs Generator Prompts** → Creates "Figma-Ready Prompts"  
3. **Figma Make AI runs Final Prompts** → Creates actual wireframes

---

## 1. Input Templates, References & Examples Used

### Primary Input Template

| Template | Location | Purpose |
|----------|----------|---------|
| **FIGMA Prompt Template** | `pmc/product/_prompt_engineering/04-FR-wireframes-FIGMA-prompt_v4.md` | Defines how to generate Figma-ready wireframe prompts from acceptance criteria |

> **Key Difference from 04d:** This script uses only ONE template, while 04d uses TWO (task creation + execution).

### Reference Documents

| Reference | Location | Purpose |
|-----------|----------|---------|
| **Product Overview** | `pmc/product/01-[prod-abbr]-overview.md` | Product vision, goals, architecture, scope |
| **User Stories** | `pmc/product/02-[prod-abbr]-user-stories.md` | User requirements and acceptance criteria |
| **User Journey** | `pmc/product/02b-[prod-abbr]-user-journey.md` | User flow and emotional journey mapping |
| **Functional Requirements** | `pmc/product/_mapping/{proj-abbr}/03-{proj-abbr}-functional-requirements.md` | Detailed FR specifications |
| **Journey Mapping Data** | `pmc/product/_mapping/journey-to-wireframe-mapping.json` | Maps user journey stages to wireframe design elements |

### Key Directory Structure Difference

| Script | FR Input Location | Output Location |
|--------|-------------------|-----------------|
| **04d** | `pmc/product/03-*.md` (root product folder) | `pmc/product/_mapping/fr-maps/` (hardcoded) |
| **04a** | `pmc/product/_mapping/{proj-abbr}/03-*.md` (project subfolder) | `pmc/product/_mapping/{proj-abbr}/` (dynamic per project) |

---

## 2. Input Specification Used

### Main Input: Functional Requirements Document

**File:** `pmc/product/_mapping/{project-abbr}/03-{project-abbr}-functional-requirements.md`

> **Note:** This is a PROJECT-SPECIFIC location, not the root product folder like 04d uses.

The script parses this document with the same structure expectations as 04d:

```markdown
## 1. [Section Title]

- **FR1.1.0:** [FR Title]
  * Description: [text]
  * User Story Acceptance Criteria: [list]
  * Functional Requirements Acceptance Criteria: [list]

## 2. [Next Section Title]
...
```

### Command-Line Inputs

```bash
node 04a-generate-FIGMA-wireframe-prompts_v1.js "<Project Name>" <project-abbreviation>
```

**Example:**
```bash
node 04a-generate-FIGMA-wireframe-prompts_v1.js "LoRA Pipeline" pipeline
```

---

## 3. What Running the Script Does

When you run the script, it performs these operations:

### Step 1: Parse Functional Requirements
- Reads the FR document at `pmc/product/_mapping/{proj-abbr}/03-{proj-abbr}-functional-requirements.md`
- Splits it into sections based on `## X.` headers
- Assigns section IDs (E01, E02, E03, etc.)
- Extracts all FR numbers from each section

### Step 2: Load Template
- Loads the FIGMA prompt template
- Loads the journey mapping JSON (same as 04d)

### Step 3: Generate Per-Section FR Segment Files
For each section, the script:
- Creates a section-specific FR requirements file
- Writes it to `pmc/product/_mapping/{proj-abbr}/04-{proj-abbr}-FR-wireframes-E[XX].md`

### Step 4: Generate "Generator Prompts" (Per-FR)
For each FR in each section, the script:
- Fills in all template placeholders with FR-specific values
- Injects journey context (goals, emotions, progressive disclosure, success indicators)
- Calculates the line number where each FR block starts
- Appends the filled template to a combined output file

**Output Location:** `pmc/product/_mapping/{proj-abbr}/_run-prompts/04a-FIGMA-wireframes-prompt-E[XX].md`

### Step 5: Generate Index File
- Creates an index file linking all sections and their prompt files
- Output: `pmc/product/_mapping/{proj-abbr}/04-FR-wireframes-index.md`

---

## 4. Does It Create Prompts to Run?

**Yes.** It creates ONE type of prompt:

### Generator Prompts (Per-FR)
- **What they are:** Meta-prompts that instruct an AI agent to generate Figma-ready wireframe prompts
- **Location:** `_run-prompts/04a-FIGMA-wireframes-prompt-E[XX].md`
- **Quantity:** One file per section, containing multiple per-FR prompt blocks
- **Who runs them:** A human or AI coding agent (like Claude)

> **Key Difference from 04d:** No execution prompts are generated. This script is purely for wireframe generation, not implementation.

---

## 5. What Those Prompts Do

### Generator Prompts Purpose

When an AI agent is given a Generator Prompt from 04a, it will:

1. **Read** the source documents (Overview, User Stories, User Journey, FR Spec)
2. **Locate** the specific FR in the FR mapping document
3. **Extract** all acceptance criteria (User Story + Functional Requirements)
4. **Classify** each criterion as UI-relevant vs Non-UI
5. **Compute** a Page Plan (minimum 3 pages) to satisfy all UI-relevant criteria
6. **Output** a self-contained Figma Make AI prompt that:
   - Embeds all UI-relevant acceptance criteria
   - Includes journey integration (goals, emotions, progressive disclosure)
   - Defines explicit UI requirements (components, states, interactions)
   - Specifies a page plan with screen names and purposes
   - Maps acceptance criteria to UI components
   - Includes accessibility guidance and information architecture

**Output Format:**
```markdown
=== BEGIN PROMPT FR: FR1.1.1 ===

Title
- FR FR1.1.1 Wireframes — Stage 1 — [Stage Name]

Context Summary
- [2–4 sentences]

Journey Integration
- Stage X user goals: [extracted from journey]
- Key emotions: [list]
- Progressive disclosure levels: [basic, advanced, expert]

Wireframe Goals
- [Bulleted goals]

Explicit UI Requirements
- [From acceptance criteria]

Interactions and Flows
- [Navigation and interactions]

Visual Feedback
- [Progress indicators, status chips, toasts]

Accessibility Guidance
- [Focus, labels, aria hints]

Information Architecture
- [Layout groups and hierarchy]

Page Plan
- [List of screens with purposes]

Acceptance Criteria → UI Component Mapping
- [Table mapping criteria to components]

Non-UI Acceptance Criteria
- [List with impact notes]

Estimated Page Count
- [Number and rationale]

=== END PROMPT FR: FR1.1.1 ===
```

---

## 6. Complete Operational Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              LEVEL 0: SCRIPT EXECUTION                       │
│  node 04a-generate-FIGMA-wireframe-prompts_v1.js "Project Name" proj-abbr    │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INPUTS TO SCRIPT                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ • Functional Requirements: pmc/product/_mapping/{proj}/03-*.md              │
│ • FIGMA Template: pmc/product/_prompt_engineering/04-FR-wireframes-FIGMA.md │
│ • Journey Mapping: pmc/product/_mapping/journey-to-wireframe-mapping.json   │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LEVEL 1: SCRIPT OUTPUTS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ OUTPUT A - Section FR Files (one per section):                               │
│   • {proj}/04-{proj}-FR-wireframes-E01.md                                    │
│   • {proj}/04-{proj}-FR-wireframes-E02.md                                    │
│                                                                              │
│ OUTPUT B - Generator Prompts (one file per section, multiple FR blocks):     │
│   • {proj}/_run-prompts/04a-FIGMA-wireframes-prompt-E01.md                   │
│   • {proj}/_run-prompts/04a-FIGMA-wireframes-prompt-E02.md                   │
│                                                                              │
│ OUTPUT C - Index File:                                                        │
│   • {proj}/04-FR-wireframes-index.md                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LEVEL 2: AI AGENT RUNS GENERATOR PROMPTS                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ INPUTS THE AI AGENT READS:                                                   │
│   • Product documentation (overview, stories, journey)                       │
│   • Section-specific FR requirements                                         │
│                                                                              │
│ WHAT THE AI AGENT DOES:                                                      │
│   1. Extracts all acceptance criteria for each FR                            │
│   2. Classifies criteria as UI-relevant vs Non-UI                            │
│   3. Computes a page plan (≥3 pages) satisfying UI criteria                  │
│   4. Generates a self-contained Figma-ready prompt                           │
│                                                                              │
│ OUTPUT:                                                                       │
│   • {proj}/04-{proj}-FIGMA-wireframes-output-E[XX].md                        │
│     (Appends Figma-ready prompts between === BEGIN/END === markers)          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   LEVEL 3: FIGMA MAKE AI RUNS FINAL PROMPTS                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ INPUT: The Figma-ready prompt block from Level 2 output                      │
│                                                                              │
│ OUTPUT: Figma wireframe file with 3-6 pages per FR                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Files Summary for 04a

### Inputs
| File | Type | Description |
|------|------|-------------|
| `_mapping/{proj}/03-{proj}-functional-requirements.md` | Spec | Project-specific FR document |
| `04-FR-wireframes-FIGMA-prompt_v4.md` | Template | FIGMA prompt template (single template) |
| `journey-to-wireframe-mapping.json` | Data | User journey emotional/UX mapping |

### Outputs
| File | Type | Description |
|------|------|-------------|
| `{proj}/04-{proj}-FR-wireframes-E[XX].md` | Section Files | Per-section FR requirements for traceability |
| `{proj}/_run-prompts/04a-FIGMA-wireframes-prompt-E[XX].md` | Generator Prompts | Per-section FR generator prompts |
| `{proj}/04-FR-wireframes-index.md` | Index | Links to all sections and prompts |
| `{proj}/04-{proj}-FIGMA-wireframes-output-E[XX].md` | Final Prompts | AI-generated Figma-ready prompts |

---
---

# Comparison: 04a vs 04d Scripts

## Is 04a a "More Advanced" Version?

**No, 04a is NOT a more advanced version.** They serve different purposes in the workflow:

| Aspect | 04d Script | 04a Script |
|--------|------------|------------|
| **Primary Purpose** | Full-stack development pipeline (wireframes + implementation) | Pure Figma wireframe generation |
| **Templates Used** | 2 templates (task creation + execution) | 1 template (FIGMA prompt only) |
| **Output Types** | Generator prompts + Execution prompts | Generator prompts only |
| **Target Workflow** | Requirements → Wireframes → Implementation → Code | Requirements → Wireframes |
| **Naming Convention** | `04-FR-wireframes-prompt-E[XX].md` | `04a-FIGMA-wireframes-prompt-E[XX].md` |
| **Output Directory** | Hardcoded `fr-maps/` | Dynamic `{project-abbr}/` |
| **Index File** | Creates index file | Creates index file |
| **Section Files** | Does NOT create section FR files | Creates section FR files for traceability |

## Relationship Between the Scripts

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SCRIPT FAMILY TREE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   04a-generate-FIGMA-wireframe-prompts_v1.js                                 │
│   └── SPECIALIZED: Only for Figma wireframe generation                       │
│   └── OUTPUT: _run-prompts/04a-FIGMA-wireframes-prompt-*.md                   │
│   └── TEMPLATE: 04-FR-wireframes-FIGMA-prompt_v4.md (1 template)             │
│   └── PROJECT-BASED output directories                                       │
│                                                                              │
│   04d-generate-FR-wireframe-segments_v1.js                                   │
│   └── GENERAL: Wireframes + Implementation Instructions                      │
│   └── OUTPUT: prompts/04-FR-wireframes-prompt-*.md                            │
│   └──         prompts/04-FR-wireframes-execution-prompt-*.md                  │
│   └── TEMPLATES: 04-FR-with-wireframes-create-tasks_v1.md (tasks)            │
│   └──            04-FR-with-wireframes-execution-prompts_v1.md (execution)   │
│   └── HARDCODED fr-maps/ output directory                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## When to Use Which Script

| Scenario | Use Script |
|----------|-----------|
| You only need Figma wireframes from FR specs | **04a** |
| You need wireframes AND implementation prompts | **04d** |
| You have multiple projects with separate directories | **04a** (supports project-based paths) |
| You're working in the shared `fr-maps/` folder | **04d** |
| You want traceability section files written out | **04a** (writes 04-{proj}-FR-wireframes-E[XX].md) |
| You need execution prompts for SQL/implementation | **04d** (only one that creates execution prompts) |

## Summary

- **04d is MORE COMPREHENSIVE** - it has the dual-template architecture for both wireframe generation and implementation execution
- **04a is MORE FOCUSED** - it's optimized specifically for the Figma Make AI workflow with project-based organization
- **Neither is "more advanced"** - they serve different use cases in the overall product development pipeline
- **04a creates section files** for traceability, which 04d does not
- **04d creates execution prompts** for implementation, which 04a does not

The "d" vs "a" in the naming likely refers to different workflow paths (path D vs path A) rather than version progression.
