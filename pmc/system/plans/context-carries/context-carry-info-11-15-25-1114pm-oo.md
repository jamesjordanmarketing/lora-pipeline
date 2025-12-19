# Context Carryover: LoRA Training Pipeline - Wireframe Generation Complete

## 📌 Active Development Focus

**Primary Task**: Implement Frontend UI for LoRA Training Pipeline (Stages 1-6)

### Current Status: Wireframe Specifications Complete, Frontend Implementation Next

**What Was Completed** (December 18, 2025):

1. ✅ **Comprehensive Wireframe Prompt Generation for Stage 8 (E08)**
   - Generated 5 complete Figma-ready wireframe prompts for Team Collaboration & Notifications
   - FR8.1.1: Job Creator Attribution (4 pages, team coordination and accountability)
   - FR8.1.2: Job Sharing & Collaboration (5 pages, shareable links with visibility controls)
   - FR8.2.1: Training Completion Notifications (5 pages, email/Slack notifications)
   - FR8.2.2: Job Notes and Experiment Documentation (5 pages, experiment tracking)
   - FR8.3.1: Team Knowledge Base Integration (6 pages, future enhancement)
   - Total: 1,413 lines, 25 detailed page specifications
   - All prompts ready for Figma Make AI (self-contained, no external dependencies)

2. ✅ **All Figma Wireframe Prompts Generated (Stages 1-8)**
   - E01: Training Job Configuration & Setup (919 lines)
   - E02: Training Job Execution & Monitoring (597 lines)  
   - E03: Error Handling & Recovery (not counted in this phase)
   - E04: Model Artifacts & Downloads (1,399 lines)
   - E05: Training Comparison & Optimization (1,408 lines)
   - E06: Model Quality Validation (2,294 lines)
   - E07: Cost Management & Budget Control (1,026 lines, deferred for advanced build)
   - E08: Team Collaboration & Notifications (1,413 lines, just completed)
   - **Focus for Next Agent: E01-E06 only** (E07-E08 are advanced features)

3. ✅ **Functional Requirements Specifications Created**
   - FR spec files document all acceptance criteria for each stage
   - Each FR includes: User Story Acceptance Criteria + Functional Requirements Acceptance Criteria
   - Comprehensive UI requirements: components, states, interactions, accessibility
   - Mapped to User Stories and User Journey stages
   - **Focus for Next Agent: FR-wireframes-E01 through E06 only**

**What's Next** (For This Agent):

The next agent will implement the frontend UI components based on the complete wireframe specifications and functional requirements. The agent must:

- **Internalize all FIGMA wireframe prompts** for E01-E06 to understand complete UI/UX requirements
- **Internalize all FR specification documents** for E01-E06 to understand acceptance criteria
- **Build React/Next.js components** that match wireframe specifications exactly
- **Implement all UI states** (loading, error, success, empty, disabled, in-progress, etc.)
- **Ensure accessibility compliance** (WCAG AA, keyboard navigation, screen readers)
- **Connect to backend APIs** (Supabase queries, RunPod training orchestration)
- **Test all user flows** described in wireframe interaction sections

---

## 📂 Critical Files for Frontend Implementation

### Figma Wireframe Prompts (MUST INTERNALIZE - E01-E06 ONLY)

| File | Stage | Lines | Scope |
|------|-------|-------|-------|
| **`pmc/product/_mapping/fr-maps/04-pipeline-FIGMA-wireframes-output-E01.md`** | **Stage 1: Training Job Configuration & Setup** | 919 | Job creation, dataset selection, hyperparameter presets, GPU selection, cost estimation, configuration review |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FIGMA-wireframes-output-E02.md`** | **Stage 2: Training Job Execution & Monitoring** | 597 | Real-time progress tracking, loss curves, stage indicators, webhook event logs, job control (cancel), multi-job management |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FIGMA-wireframes-output-E04.md`** | **Stage 4: Model Artifacts & Downloads** | 1,399 | LoRA adapter downloads, adapter storage/versioning, training metrics export (CSV/JSON), training report PDF generation, deployment package creation |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FIGMA-wireframes-output-E05.md`** | **Stage 5: Training Comparison & Optimization** | 1,408 | Side-by-side training run comparison, overlaid loss curves, configuration performance analytics, training history, configuration templates library |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FIGMA-wireframes-output-E06.md`** | **Stage 6: Model Quality Validation** | 2,294 | Perplexity benchmarking, perplexity by category analysis, emotional intelligence validation, regression detection, catastrophic forgetting tests, brand voice consistency scoring |

**Deferred for Advanced Build** (DO NOT IMPLEMENT YET):
- ~~E07: Cost Management & Budget Control~~ (1,026 lines) - Advanced feature
- ~~E08: Team Collaboration & Notifications~~ (1,413 lines) - Advanced feature

### Functional Requirements Specifications (MUST INTERNALIZE - E01-E06 ONLY)

| File | Stage | Purpose |
|------|-------|---------|
| **`pmc/product/_mapping/fr-maps/04-pipeline-FR-wireframes-E01.md`** | **Stage 1: Training Job Configuration & Setup** | Complete acceptance criteria for job creation, dataset selection, hyperparameter configuration, GPU selection, cost estimation workflows |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FR-wireframes-E02.md`** | **Stage 2: Training Job Execution & Monitoring** | Acceptance criteria for real-time progress tracking, loss curves, stage indicators, event logs, job cancellation, queue management |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FR-wireframes-E03.md`** | **Stage 3: Error Handling & Recovery** | Acceptance criteria for OOM errors, dataset format errors, GPU provisioning errors, checkpoint recovery, retry mechanisms |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FR-wireframes-E04.md`** | **Stage 4: Model Artifacts & Downloads** | Acceptance criteria for adapter downloads, storage/versioning, metrics export, PDF reports, deployment packages |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FR-wireframes-E05.md`** | **Stage 5: Training Comparison & Optimization** | Acceptance criteria for job comparison, configuration analytics, training history, template library |
| **`pmc/product/_mapping/fr-maps/04-pipeline-FR-wireframes-E06.md`** | **Stage 6: Model Quality Validation** | Acceptance criteria for perplexity benchmarks, EI validation, regression detection, catastrophic forgetting tests, brand voice scoring |

**Deferred for Advanced Build** (DO NOT IMPLEMENT YET):
- ~~FR-wireframes-E07: Cost Management & Budget Control~~ - Advanced feature
- ~~FR-wireframes-E08: Team Collaboration & Notifications~~ - Advanced feature

### Source Reference Documents

| File | Purpose |
|------|---------|
| `pmc/product/01-pipeline-overview.md` | Product vision, business context, user pain points, success metrics |
| `pmc/product/02-pipeline-user-stories.md` | 84 user stories across 8 categories with detailed acceptance criteria |
| `pmc/product/03-pipeline-functional-requirements.md` | Functional requirements mapped to user stories with technical acceptance criteria |
| `pmc/product/02b-pipeline-user-journey.md` | User journey stages, emotional requirements, progressive disclosure, success indicators |

---

## 🎯 Wireframe Structure & Organization

### How Figma Prompt Documents Are Structured

Each FIGMA wireframe output file (E01-E06) contains multiple FR prompts, each delineated by explicit markers:

```markdown
=== BEGIN PROMPT FR: FR1.1.1 ===
[Complete Figma-ready prompt for this FR]
=== END PROMPT FR: FR1.1.1 ===

=== BEGIN PROMPT FR: FR1.1.2 ===
[Complete Figma-ready prompt for this FR]
=== END PROMPT FR: FR1.1.2 ===
```

### Each FR Prompt Includes (Comprehensive Specification):

1. **Title** - FR number, stage name, feature name
2. **Context Summary** - 2-4 sentences: scope, user value, constraints
3. **Journey Integration** - User goals, key emotions, progressive disclosure levels, persona adaptations
4. **Journey-Informed Design Elements** - User goals, emotional requirements, progressive disclosure specifics, success indicators
5. **Wireframe Goals** - Bulleted goals mapped to this FR
6. **Explicit UI Requirements** - Each acceptance criterion translated to concrete UI elements, components, states, interactions
7. **Interactions and Flows** - Step-by-step user workflows (Primary, Secondary, Tertiary flows)
8. **Visual Feedback** - Progress indicators, status chips, ETAs, logs, toasts, badges
9. **Accessibility Guidance** - Focus management, ARIA labels, keyboard navigation, screen reader support, color contrast
10. **Information Architecture** - Layout hierarchy, component grouping, page structure
11. **Page Plan** - List of screens with names, purposes, components, states (≥3 pages per FR)
12. **Annotations (Mandatory)** - Notes linking UI elements to acceptance criteria, mapping table format
13. **Acceptance Criteria → UI Component Mapping** - Detailed table: Criterion → Source → Screen(s) → Component(s) → State(s) → Notes
14. **Non-UI Acceptance Criteria** - Backend/system requirements with UI hints
15. **Estimated Page Count** - Number and rationale tied to criteria coverage

### Key FR Sections Breakdown by Stage

**Stage 1 (E01): Training Job Configuration & Setup**
- FR1.1.1: Create Training Job from Training File
- FR1.1.2: Select Hyperparameter Preset (Conservative/Balanced/Aggressive)
- FR1.1.3: Select GPU Type with Cost Comparison (Spot vs On-Demand)
- FR1.2.1: Real-Time Cost Estimation (dynamic updates)
- FR1.2.2: Pre-Job Budget Validation (prevent overages)
- FR1.3.1: Add Job Metadata & Documentation
- FR1.3.2: Review Configuration Before Start (final confirmation)

**Stage 2 (E02): Training Job Execution & Monitoring**
- FR2.1.1: Live Training Progress Dashboard (loss curves, metrics, ETA)
- FR2.1.2: Training Stage Indicators (Preprocessing → Model Loading → Training → Finalization)
- FR2.1.3: Webhook Event Log (chronological event tracking)
- FR2.2.1: Cancel Active Training Job (cost control)
- FR2.2.2: Pause and Resume Training (future enhancement)
- FR2.3.1: View All Training Jobs (list with filters)
- FR2.3.2: Training Queue Management

**Stage 3 (E03): Error Handling & Recovery**
- FR3.1.1: Out of Memory Error Handling (actionable guidance)
- FR3.1.2: Dataset Format Error Handling (specific error details)
- FR3.1.3: GPU Provisioning Error Handling (auto-retry options)
- FR3.2.1: Spot Instance Interruption Recovery (automatic checkpoint recovery)
- FR3.2.2: Manual Checkpoint Resume
- FR3.3.1: One-Click Retry with Same Configuration
- FR3.3.2: Retry with Suggested Adjustments

**Stage 4 (E04): Model Artifacts & Downloads**
- FR4.1.1: Download Trained LoRA Adapters (ZIP with adapter files)
- FR4.1.2: Adapter Storage and Versioning (Supabase Storage)
- FR4.2.1: Export Training Metrics as CSV/JSON
- FR4.2.2: Generate Training Report PDF (executive summary)
- FR4.3.1: Create Complete Deployment Package (adapters + scripts + README)
- FR4.3.2: API Inference Endpoint Template (future enhancement)

**Stage 5 (E05): Training Comparison & Optimization**
- FR5.1.1: Compare Multiple Training Runs (side-by-side, overlaid loss curves)
- FR5.1.2: Configuration Performance Analytics (aggregate success rates)
- FR5.2.1: Comprehensive Training History (filters, search, export)
- FR5.2.2: Configuration Templates Library (save successful configs)

**Stage 6 (E06): Model Quality Validation**
- FR6.1.1: Calculate Perplexity Improvement (baseline vs trained)
- FR6.1.2: Perplexity by Category Analysis (persona, emotional arc, topic)
- FR6.2.1: Run Emotional Intelligence Benchmarks (50 test scenarios)
- FR6.2.2: Emotional Intelligence Regression Detection
- FR6.3.1: Financial Knowledge Retention Test (catastrophic forgetting)
- FR6.3.2: Domain-Specific Knowledge Probes (custom test suites)
- FR6.4.1: Elena Morales Voice Consistency Scoring (brand alignment)
- FR6.4.2: Client Brand Customization (future enhancement)

---

## 🔬 Understanding FR Specifications (Critical for Implementation)

### FR Specification File Structure

Each `04-pipeline-FR-wireframes-E##.md` file contains:

```markdown
## [Stage Number]. [Stage Name]

- **FR#.#.#:** [Feature Name]
  * Description: [Detailed feature description]
  * Impact Weighting: [Business impact categories]
  * Priority: High/Medium/Low
  * User Stories: US#.#.#
  * User Journey: UJ#.#.# (references to journey stages)
  * Tasks: [T-#.#.#]
  * User Story Acceptance Criteria:
    - [Original user story criteria - high-level]
  * Functional Requirements Acceptance Criteria:
    - [Detailed technical implementation criteria]
    - [Database requirements, API specifications, validation rules]
    - [Performance requirements, error handling, edge cases]
```

### Key Differences: User Story vs Functional Requirements Criteria

**User Story Acceptance Criteria** (High-Level, User-Focused):
- Describes WHAT the user can do
- Focuses on user experience and outcomes
- Example: "Training files dropdown populated from `training_files` table showing file name, conversation count, total training pairs"

**Functional Requirements Acceptance Criteria** (Technical, Implementation-Focused):
- Describes HOW the system implements the feature
- Includes database queries, API calls, validation logic, error handling
- Example: "System queries `training_files` table and displays only files with status='active' and conversation_count >= 50. Dropdown component renders with search/filter capability (by name, conversation count range, quality score range). Each training file entry displays: name, conversation count, total training pairs, average quality score with visual indicator (✓ High Quality ≥4.0, ⚠ Review <4.0)."

### Critical Implementation Notes

1. **BOTH Sets of Criteria Must Be Satisfied**
   - User Story Criteria = "What success looks like to the user"
   - Functional Requirements Criteria = "How to technically achieve that success"

2. **UI States Are Comprehensive**
   - Every FR specifies multiple UI states: loading, error, success, empty, disabled, in-progress, hover, focus, active, invalid, warning
   - Implementation MUST handle all specified states

3. **Accessibility Is Mandatory**
   - WCAG AA compliance required
   - Keyboard navigation for all interactive elements (Tab, Enter, Esc, Arrow keys)
   - ARIA labels, roles, and live regions
   - Screen reader support with descriptive announcements
   - Color contrast minimum 4.5:1
   - Focus indicators visible

4. **Performance Requirements**
   - API responses: <2 seconds for data fetch
   - UI updates: <500ms for interactions
   - Real-time updates: 60-second polling interval (or WebSocket)
   - Large file downloads: progress indicators required

5. **Error Handling Is Specific**
   - Each FR includes detailed error scenarios
   - Error messages must be actionable (tell user what to do next)
   - Examples: "Training file not found (if deleted)", "Insufficient conversations (if <50)", "Storage file missing (if file path invalid)"

---

## 🎨 Frontend Implementation Guidance

### Technology Stack (Existing Application)

**Current Tech Stack** (Already Implemented):
- **Framework**: Next.js 14 (App Router, TypeScript)
- **UI Components**: Shadcn/UI + Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage (conversation-files, training-files buckets)
- **AI**: Claude API (Anthropic) - `claude-sonnet-4-5-20250929`
- **Deployment**: Vercel

**New Components Needed for LoRA Training**:
- Training job management pages (`/training-jobs/*`)
- Real-time monitoring dashboards (with WebSocket or polling)
- Cost estimation calculators (client-side)
- Loss curve visualizations (Chart.js or Recharts)
- File download handlers (ZIP, CSV, JSON, PDF generation)
- Notification system (email via SendGrid, Slack via API)

### Database Schema Requirements

**New Tables Needed** (Backend Implementation):
```sql
-- Training Jobs
training_jobs (
  id UUID PRIMARY KEY,
  name VARCHAR(200),
  training_file_id UUID REFERENCES training_files(id),
  status VARCHAR(50), -- 'pending_configuration', 'queued', 'training', 'completed', 'failed', 'cancelled'
  preset VARCHAR(50), -- 'conservative', 'balanced', 'aggressive'
  gpu_type VARCHAR(50), -- 'spot', 'on-demand'
  estimated_cost_min DECIMAL(10,2),
  estimated_cost_max DECIMAL(10,2),
  actual_cost DECIMAL(10,2),
  estimated_duration_hours INT,
  actual_duration_seconds INT,
  final_training_loss DECIMAL(10,6),
  final_validation_loss DECIMAL(10,6),
  perplexity_improvement_percent DECIMAL(5,2),
  created_by UUID,
  created_at TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  notes TEXT
);

-- Training Job Events (webhook logs)
training_job_events (
  id UUID PRIMARY KEY,
  job_id UUID REFERENCES training_jobs(id),
  event_type VARCHAR(50), -- 'status_change', 'metrics_update', 'warning', 'error'
  event_message TEXT,
  payload JSONB,
  created_at TIMESTAMP
);

-- Training Job Metrics (loss curves, learning rates)
training_job_metrics (
  id UUID PRIMARY KEY,
  job_id UUID REFERENCES training_jobs(id),
  step_number INT,
  epoch INT,
  training_loss DECIMAL(10,6),
  validation_loss DECIMAL(10,6),
  learning_rate DECIMAL(12,10),
  gpu_utilization_percent DECIMAL(5,2),
  perplexity DECIMAL(10,4),
  timestamp TIMESTAMP
);

-- Training Job Artifacts (model files)
training_job_artifacts (
  id UUID PRIMARY KEY,
  job_id UUID REFERENCES training_jobs(id),
  artifact_type VARCHAR(50), -- 'adapter_model', 'adapter_config', 'training_report_pdf', 'metrics_csv'
  file_path VARCHAR(500), -- Supabase Storage path
  file_size_bytes BIGINT,
  download_count INT DEFAULT 0,
  created_at TIMESTAMP
);

-- Configuration Templates
configuration_templates (
  id UUID PRIMARY KEY,
  name VARCHAR(200),
  description TEXT,
  preset VARCHAR(50),
  hyperparameters JSONB,
  gpu_type VARCHAR(50),
  tags TEXT[],
  created_by UUID,
  usage_count INT DEFAULT 0,
  success_rate DECIMAL(5,2),
  created_at TIMESTAMP
);
```

### API Endpoints Needed (Backend Implementation)

**Training Jobs API** (`/api/training-jobs/*`):
- `GET /api/training-jobs` - List all jobs with filters
- `POST /api/training-jobs` - Create new job
- `GET /api/training-jobs/:id` - Get job details
- `PATCH /api/training-jobs/:id` - Update job (cancel, retry)
- `DELETE /api/training-jobs/:id` - Delete job
- `GET /api/training-jobs/:id/metrics` - Get loss curves and metrics
- `GET /api/training-jobs/:id/events` - Get webhook event log
- `POST /api/training-jobs/:id/artifacts/download` - Generate download link

**Configuration API** (`/api/configuration/*`):
- `GET /api/configuration/presets` - Get hyperparameter presets
- `POST /api/configuration/estimate-cost` - Calculate cost estimate
- `GET /api/configuration/templates` - Get saved templates
- `POST /api/configuration/templates` - Save new template

**Validation API** (`/api/validation/*`):
- `POST /api/validation/perplexity` - Run perplexity benchmarks
- `POST /api/validation/emotional-intelligence` - Run EI tests
- `POST /api/validation/catastrophic-forgetting` - Run knowledge retention tests
- `GET /api/validation/:job_id/results` - Get validation results

**Comparison API** (`/api/comparison/*`):
- `POST /api/comparison/jobs` - Compare multiple jobs (accepts job IDs array)
- `GET /api/comparison/analytics` - Get configuration performance analytics

### Component Implementation Strategy

**Phase 1: Core Job Management** (Start Here)
1. Training jobs list page (`/training-jobs`)
   - Table with filters, search, sorting
   - Status badges, progress indicators
   - Action buttons (view, cancel, retry)
2. Job creation form (`/training-jobs/new`)
   - Training file selector (dropdown with search)
   - Hyperparameter preset selector (radio cards)
   - GPU type selector (toggle with cost comparison)
   - Cost estimation display (real-time updates)
   - Configuration review modal
3. Job details page (`/training-jobs/:id`)
   - Overview section (status, progress, creator)
   - Configuration section (hyperparameters, GPU)
   - Real-time progress tracking (if active)
   - Results section (if completed)
   - Actions toolbar (download, export, cancel, retry)

**Phase 2: Real-Time Monitoring**
4. Live progress dashboard (on job details page)
   - Progress header card (%, ETA, elapsed time)
   - Loss curve graph (Chart.js or Recharts)
   - Current metrics table (loss, learning rate, GPU util)
   - Cost tracker card (current spend, projected final)
   - Training stage indicators (Preprocessing → Training → Finalization)
   - Auto-refresh (polling every 60 seconds or WebSocket)
5. Webhook event log (expandable section)
   - Chronological event table
   - Event type filtering
   - Expandable JSON payload
   - Search functionality

**Phase 3: Artifacts & Downloads**
6. Adapter download functionality
   - "Download Adapters" button
   - ZIP generation (adapter_model.bin + adapter_config.json + README)
   - Signed URL generation (24-hour expiration)
   - Download progress indicator
7. Metrics export
   - CSV export (all metrics)
   - JSON export (structured data)
   - PDF report generation (executive summary)
8. Deployment package
   - Complete package ZIP (adapters + scripts + README + requirements.txt)
   - Pre-configured inference scripts

**Phase 4: Comparison & Optimization**
9. Job comparison view (`/training-jobs/compare`)
   - Multi-select job list
   - Overlaid loss curves
   - Metrics comparison table
   - Configuration diff view
   - Winner recommendation
10. Training history (`/training-jobs/history`)
    - Comprehensive filters (date, creator, status, preset, cost)
    - Search by name, notes, tags
    - Export as CSV
11. Configuration templates library (`/training-jobs/templates`)
    - Grid view of saved templates
    - Template detail modal
    - "Start from Template" functionality

**Phase 5: Quality Validation**
12. Validation results page (`/training-jobs/:id/validation`)
    - Perplexity improvement display
    - Perplexity by category breakdown
    - Emotional intelligence scores
    - Regression detection alerts
    - Catastrophic forgetting test results
    - Brand voice consistency scores
13. Before/after comparison
    - Side-by-side response examples
    - Quality improvement metrics
    - Export as PDF report

---

## 🚀 Next Agent Implementation Plan

### Step 1: Internalize Documentation (CRITICAL FIRST STEP)

**MUST READ IN THIS ORDER:**

1. **Read All FIGMA Wireframe Output Files (E01-E06)**
   - Start with E01 (Training Job Configuration)
   - Read EVERY FR prompt within each file
   - Understand: UI requirements, interactions, states, accessibility, page plans
   - Time estimate: 3-4 hours to thoroughly internalize

2. **Read All FR Specification Files (E01-E06)**
   - Cross-reference with FIGMA prompts
   - Focus on: User Story Acceptance Criteria + Functional Requirements Acceptance Criteria
   - Understand: Database requirements, API specifications, validation rules
   - Time estimate: 2-3 hours

3. **Read Source Reference Documents**
   - `01-pipeline-overview.md` - Product vision, business context
   - `02-pipeline-user-stories.md` - 84 user stories (focus on Stages 1-6)
   - `02b-pipeline-user-journey.md` - User journey stages, emotional requirements
   - Time estimate: 2 hours

**Total Reading Time: ~7-9 hours** (This is intentional and necessary)

### Step 2: Database Schema Setup

1. Create database migration file for new tables:
   - `training_jobs`
   - `training_job_events`
   - `training_job_metrics`
   - `training_job_artifacts`
   - `configuration_templates`
2. Run migration using SAOL (Supabase Agent Ops Library)
3. Verify schema using `agentIntrospectSchema`
4. Seed initial data:
   - Hyperparameter presets (Conservative, Balanced, Aggressive)
   - GPU pricing (spot: $2.49/hr, on-demand: $7.99/hr)

### Step 3: API Endpoint Implementation

1. Implement training jobs CRUD endpoints
2. Implement cost estimation endpoint (client-side calculations + server validation)
3. Implement metrics polling endpoint (for real-time updates)
4. Implement artifact generation endpoints (ZIP, CSV, JSON, PDF)
5. Test all endpoints using SAOL for database operations

### Step 4: Frontend Component Development (Phase 1)

1. Create page: `/training-jobs` (list view)
2. Create page: `/training-jobs/new` (job creation form)
3. Create page: `/training-jobs/:id` (job details)
4. Implement all UI states: loading, error, success, empty
5. Implement accessibility: keyboard navigation, ARIA labels, screen reader support
6. Test all user flows from FIGMA wireframes

### Step 5: Real-Time Monitoring (Phase 2)

1. Implement live progress dashboard (polling every 60 seconds)
2. Implement loss curve visualization (Chart.js or Recharts)
3. Implement real-time cost tracking
4. Implement training stage indicators
5. Implement webhook event log
6. Test auto-refresh and connection handling

### Step 6: Validation & Iteration

1. Cross-check implementation against ALL acceptance criteria
2. Test all UI states (loading, error, success, empty, etc.)
3. Test accessibility with keyboard navigation and screen reader
4. Test responsive design (desktop, tablet, mobile)
5. Document any deviations from specifications

### Success Criteria

**Implementation is complete when:**
- ✅ All FIGMA wireframe pages (E01-E06) are implemented as functional UI
- ✅ All User Story Acceptance Criteria (E01-E06) are satisfied
- ✅ All Functional Requirements Acceptance Criteria (E01-E06) are satisfied
- ✅ All UI states are handled (loading, error, success, empty, disabled, etc.)
- ✅ Accessibility requirements met (WCAG AA, keyboard navigation, screen readers)
- ✅ Real-time updates working (loss curves, progress, cost tracking)
- ✅ File downloads working (adapters, metrics, reports, deployment packages)
- ✅ All user flows testable end-to-end

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

**Last Updated**: December 18, 2025  
**Session Focus**: Wireframe Generation Complete (Stages 1-8), Frontend Implementation Next (Stages 1-6)  
**Current State**: All FIGMA prompts generated and ready, FR specifications complete, database schema designed, API endpoints specified  
**Document Version**: oo (Wireframe completion handoff to frontend implementation)
