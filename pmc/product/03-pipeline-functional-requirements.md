# LoRA Pipeline - Functional Requirements
**Version:** 2.0.0  
**Date:** 12/16/2025  
**Category:** Design System Platform
**Product Abbreviation:** pipeline

**Source References:**
- Seed Story: `pmc\product\00-pipeline-seed-story.md`
- Overview Document: `pmc\product\01-pipeline-overview.md`
- User Stories: `pmc\product\02-pipeline-user-stories.md`

## 1. Training Job Configuration & Setup

- **FR1.1.1:** Create Training Job from Training File
  * Description: System shall provide a comprehensive training job creation interface that enables users to select training files from a searchable dropdown, view detailed metadata including quality scores and scaffolding distribution, validate dataset eligibility, and initiate job configuration with pre-populated settings based on training file characteristics. The interface shall enforce minimum data quality thresholds, provide visual feedback on dataset readiness, and seamlessly transition users to the hyperparameter configuration workflow.
  * Impact Weighting: Operational Efficiency / Time-to-Value / Ease of Use
  * Priority: High
  * User Stories: US1.1.1
  * User Journey: UJ2.1.1 (Selecting Training Dataset), UJ2.1.2 (Understanding Dataset Impact)
  * Tasks: [T-1.1.1]
  * User Story Acceptance Criteria:
    - Training files dropdown populated from `training_files` table showing file name, conversation count, total training pairs
    - Click training file displays metadata: quality scores, scaffolding distribution, human review count
    - "Create Training Job" button opens configuration modal
    - Job creation form pre-populates with training file details
    - Form validation ensures training file has minimum 50 conversations
    - Success: Job created in database with status "pending_configuration"
    - Redirect to job configuration page with job ID
  * Functional Requirements Acceptance Criteria:
    - System queries `training_files` table and displays only files with status='active' and conversation_count >= 50
    - Dropdown component renders with search/filter capability (by name, conversation count range, quality score range)
    - Each training file entry displays: name, conversation count, total training pairs, average quality score with visual indicator (✓ High Quality ≥4.0, ⚠ Review <4.0)
    - Upon training file selection, system fetches and displays comprehensive metadata within 2 seconds: quality score breakdown (empathy, clarity, appropriateness), scaffolding distribution (personas, emotional arcs, topics with percentages), human review statistics, file size, last updated timestamp
    - System validates training file eligibility: file paths exist in storage, enrichment status = 'completed', no active training jobs using same file
    - "Create Training Job" button disabled until valid training file selected and eligibility checks pass
    - Click "Create Training Job" inserts record into `training_jobs` table with fields: id (UUID), training_file_id (FK), name (auto-generated: "{training_file_name} - {current_date}"), status ('pending_configuration'), created_by (current user), created_at (timestamp)
    - Upon successful job creation, system redirects to `/training-jobs/{job_id}/configure` with job_id in URL
    - Error handling displays specific messages: "Training file not found" (if deleted), "Training file not enriched" (if still processing), "Insufficient conversations" (if <50), "Storage file missing" (if file path invalid)
    - System logs all job creation attempts with user_id, training_file_id, timestamp, success/failure status for audit trail
    - Form pre-populates configuration defaults based on training file characteristics: Conservative preset if conversation_count < 150, Balanced if 150-300, Aggressive if >300
    - Visual feedback shows dataset readiness indicators: ✓ Ready for Training, ⏳ Processing, ⚠ Review Required with explanatory tooltips
    - System provides estimated training metrics preview: estimated duration (8-20 hours based on conversation count), estimated cost range ($25-100 based on preset), expected quality improvement (30-40% based on historical data for similar datasets)

- **FR1.1.2:** Select Hyperparameter Preset
  * Description: System shall provide three scientifically-validated hyperparameter presets (Conservative, Balanced, Aggressive) presented as interactive radio cards with comprehensive metadata including technical parameters, estimated duration/cost, risk level, historical success rates, and recommended use cases. Each preset shall include contextual tooltips explaining complex concepts in plain language, real-time cost impact visualization, and links to educational documentation. The interface shall guide non-expert users toward optimal configurations while enabling informed decision-making through transparent trade-off presentation.
  * Impact Weighting: Ease of Use / Success Rate / Risk Mitigation
  * Priority: High
  * User Stories: US1.1.2
  * User Journey: UJ2.2.1 (Choosing Hyperparameter Preset), UJ2.2.2 (Understanding Preset Trade-offs)
  * Tasks: [T-1.1.2]
  * User Story Acceptance Criteria:
    - Three preset options displayed as radio cards with icons
    - **Conservative Preset**: r=8, lr=1e-4, epochs=2, batch_size=4, gradient_accumulation_steps=1
    - Description: "Best for high-quality seed datasets and first training runs"
    - Estimated duration: 8-10 hours
    - Estimated cost: $25-30 (spot) / $80-120 (on-demand)
    - Risk level: Low
    - Success rate: 98% based on historical data
    - **Balanced Preset**: r=16, lr=2e-4, epochs=3, batch_size=2, gradient_accumulation_steps=2
    - Description: "Production-ready configuration for most use cases"
    - Estimated duration: 12-15 hours
    - Estimated cost: $50-60 (spot) / $120-140 (on-demand)
    - Risk level: Medium
    - Success rate: 96% based on historical data
    - **Aggressive Preset**: r=32, lr=3e-4, epochs=4, batch_size=1, gradient_accumulation_steps=4
    - Description: "Maximum quality for complex datasets, experimentation, when quality is paramount"
    - Estimated duration: 18-20 hours
    - Estimated cost: $80-100 (spot) / $200-240 (on-demand)
    - Risk level: Higher
    - Success rate: 92% based on historical data
    - Default selection: Balanced preset
    - Tooltip explaining each hyperparameter in simple terms
    - Link to "Understanding LoRA Hyperparameters" documentation
  * Functional Requirements Acceptance Criteria:
    - System displays three preset options as visually distinct radio cards with clear selection state (selected: blue border + checkmark, unselected: gray border)
    - Each preset card renders with structured layout: preset name and icon (top), one-sentence description, technical parameters (collapsible section), estimated metrics, risk indicator, success rate badge
    - **Conservative Preset** technical parameters stored and applied: rank (r) = 8, learning_rate (lr) = 0.0001, num_train_epochs = 2, per_device_train_batch_size = 4, gradient_accumulation_steps = 1, lora_alpha = 16, target_modules = ["q_proj", "v_proj", "k_proj", "o_proj"], lora_dropout = 0.05, warmup_ratio = 0.03, lr_scheduler_type = "cosine"
    - **Balanced Preset** technical parameters: r = 16, lr = 0.0002, epochs = 3, batch_size = 2, gradient_accumulation_steps = 2, lora_alpha = 32, target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], lora_dropout = 0.1, warmup_ratio = 0.05, lr_scheduler_type = "cosine"
    - **Aggressive Preset** technical parameters: r = 32, lr = 0.0003, epochs = 4, batch_size = 1, gradient_accumulation_steps = 4, lora_alpha = 64, target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], lora_dropout = 0.1, warmup_ratio = 0.05, lr_scheduler_type = "cosine"
    - System calculates estimated duration dynamically: (conversation_count × training_pairs_per_conversation × epochs × seconds_per_training_pair) / 3600, where seconds_per_training_pair varies by preset (Conservative: 120s, Balanced: 180s, Aggressive: 300s)
    - System calculates estimated cost range: duration_hours × gpu_hourly_rate, displaying both spot ($2.49/hr) and on-demand ($7.99/hr) options with percentage savings indicator
    - Risk level indicator displays as color-coded badge with explanation tooltip: Low (green) = "Minimal OOM risk, proven for most datasets, fastest completion"; Medium (yellow) = "Moderate complexity, requires good dataset quality, production-ready"; High (orange) = "Highest quality potential, requires excellent dataset, longer training, experimentation recommended"
    - Historical success rate badge displays percentage with data source: "98% success rate (based on 127 completed jobs)" - data queried from `training_jobs` table WHERE preset = '{preset_name}' AND status = 'completed'
    - Default selection logic: If conversation_count < 150 → Conservative; If 150-300 → Balanced; If >300 OR user has completed >=3 successful jobs → Aggressive option enabled, otherwise disabled with tooltip "Unlock after 3 successful training runs"
    - Interactive tooltips trigger on hover for each hyperparameter: "Rank (r): Number of trainable parameters - higher = more learning capacity but slower training", "Learning Rate: Speed of model updates - higher = faster learning but risk of instability", "Epochs: Complete passes through dataset - more = better learning but diminishing returns", "Batch Size: Training examples processed simultaneously - larger = faster but more memory", "Gradient Accumulation: Simulates larger batch sizes - higher = more stable gradients"
    - Link to documentation opens in new tab: "/docs/hyperparameters-explained" with visual diagrams, interactive examples, preset comparison chart
    - System updates cost estimate panel in real-time (within 500ms) when preset selection changes, showing: previous estimate → new estimate with delta amount and percentage change
    - Preset selection stores in job configuration object: {preset_name, preset_config: {...parameters}, estimated_duration_hours, estimated_cost_spot, estimated_cost_ondemand}
    - System validates GPU memory requirements per preset: Conservative (requires 60GB VRAM), Balanced (70GB), Aggressive (75GB) - ensures H100 80GB GPU is sufficient, blocks job if insufficient
    - Recommended use cases displayed per preset: Conservative ("First training run, high-quality seed data, budget-conscious, quick validation"), Balanced ("Production models, proven reliability, standard datasets, client delivery"), Aggressive ("Complex emotional intelligence, maximum quality, research/experimentation, when budget allows")
    - System tracks preset selection analytics: count of jobs per preset, success rate trends, average cost actual vs estimate variance - data used to refine estimates quarterly

- **FR1.1.3:** Select GPU Type with Cost Comparison
  * Description: System shall provide an intelligent GPU selection interface comparing spot and on-demand instances with detailed cost-benefit analysis, real-time pricing, historical reliability metrics, automatic checkpoint recovery capabilities, and context-aware recommendations. The interface shall calculate and display cost savings percentages, interruption probability based on historical data, expected recovery time, and total cost impact to enable informed decision-making balancing cost optimization with reliability requirements.
  * Impact Weighting: Cost Efficiency / Operational Efficiency / Risk Management
  * Priority: High
  * User Stories: US1.1.3
  * User Journey: UJ2.3.1 (GPU Selection & Cost Trade-offs), UJ1.3.1 (Understanding Training Costs)
  * Tasks: [T-1.1.3]
  * User Story Acceptance Criteria:
    - GPU selection toggle: Spot vs On-Demand
    - **Spot Instance Option**:
    - Price: $2.49/hr (H100 PCIe 80GB)
    - Savings: 70% cheaper than on-demand
    - Risk: 10-30% chance of interruption
    - Recovery: Automatic checkpoint recovery, <10 min resume time
    - Recommendation: "Best for non-urgent training, cost optimization"
    - **On-Demand Option**:
    - Price: $7.99/hr (H100 PCIe 80GB)
    - Guarantee: No interruptions, predictable completion time
    - Recommendation: "Best for client deadlines, critical deliveries"
    - Real-time cost estimate updates when switching between spot/on-demand
    - Display historical interruption rate for spot instances (e.g., "18% interruption rate last 30 days")
    - Success metric: "95%+ jobs complete successfully with spot instances"
    - Confirmation prompt if selecting on-demand for jobs estimated >$150
  * Functional Requirements Acceptance Criteria:
    - System displays GPU selection as prominent toggle control with two options clearly labeled: "Spot Instance (Recommended)" and "On-Demand Instance"
    - **Spot Instance** configuration stored: gpu_type = "H100_PCIE_80GB", pricing_tier = "spot", hourly_rate = 2.49, checkpoint_interval_steps = 100, max_recovery_attempts = 3, recovery_timeout_minutes = 10
    - **On-Demand Instance** configuration stored: gpu_type = "H100_PCIE_80GB", pricing_tier = "on_demand", hourly_rate = 7.99, guaranteed_completion = true
    - Each option displays as comparison card with structured sections: Price ($/hr with large font), Key Benefits (bullet list), Trade-offs (honest disclosure), Cost Savings (percentage and dollar amount), Historical Performance (success rate, interruption frequency)
    - Spot instance card shows: Current rate $2.49/hr (fetched from RunPod API every 24 hours), Savings badge "Save 70% ($5.50/hr)", Risk disclosure "10-30% interruption chance based on datacenter demand", Automatic recovery guarantee "Resume within 10 minutes from last checkpoint (saved every 100 steps)", Success metric "95.4% of spot jobs complete successfully (based on last 90 days)"
    - On-demand card shows: Fixed rate $7.99/hr (no fluctuation), Guarantee badge "100% uptime guaranteed", Zero interruption risk, Predictable completion time "Finish exactly when estimated, no recovery delays", Premium indicator "Best for client deadlines, mission-critical training"
    - System calculates real-time cost estimates for both options: spot_total = estimated_duration_hours × 2.49, ondemand_total = estimated_duration_hours × 7.99, savings_amount = ondemand_total - spot_total, savings_percentage = (savings_amount / ondemand_total) × 100
    - Cost estimate panel updates dynamically within 300ms when GPU selection changes: displays previous estimate (strikethrough), new estimate (bold green if cheaper, red if more expensive), delta amount with arrow indicator (↓ $XX saved or ↑ $XX increase)
    - Historical interruption rate queried from `training_jobs` table: SELECT COUNT(*) WHERE gpu_pricing_tier='spot' AND checkpoint_recovery_count > 0 AND created_at > NOW() - INTERVAL '30 days' / COUNT(*) WHERE gpu_pricing_tier='spot' AND created_at > NOW() - INTERVAL '30 days' - display as "18% interruption rate (last 30 days)"
    - System tracks spot instance success rate: jobs with status='completed' / all spot jobs × 100 - display as "95%+ jobs complete successfully" badge with confidence indicator
    - Context-aware recommendation logic displays below toggle: IF estimated_duration > 20 hours OR estimated_cost > 150 THEN recommend on-demand ("Long training run - on-demand guarantees completion"); IF user_budget_remaining < estimated_cost_ondemand THEN recommend spot ("Budget optimization - spot instances save $XX"); IF deadline_hours < 24 THEN recommend on-demand ("Urgent deadline - guaranteed completion"); ELSE recommend spot ("Cost-effective choice for most training runs")
    - Confirmation modal triggers if user selects on-demand AND estimated_cost_ondemand > 150: "High-Cost On-Demand Instance - Estimated cost: $XXX. Spot instance would save $YYY. Are you sure? [Recommended: Use Spot] [Continue with On-Demand] [Cancel]"
    - System stores GPU selection in job configuration: {gpu_pricing_tier, hourly_rate, estimated_cost, interruption_risk_percentage, checkpoint_enabled}
    - Tooltip explanations for technical terms: "Spot Instance: Unused datacenter capacity offered at discount - may be reclaimed if needed, but we automatically save progress and resume quickly", "On-Demand: Dedicated GPU guaranteed for your job duration - no interruptions, but costs 3x more", "Checkpoint: Progress snapshot saved every 100 training steps - enables recovery from exact point if interrupted"
    - Cost comparison visualization: side-by-side bar chart showing spot vs on-demand total cost, with savings amount highlighted in green, interruption overhead estimate added to spot cost (typically +$2-5 for recovery time)
    - System tracks user GPU selection patterns: percentage of spot vs on-demand usage, correlation with job success rates, cost savings achieved - analytics displayed in budget dashboard
    - Warning indicator if spot availability is low: "⚠ High spot demand currently (87% datacenter utilization) - longer provisioning time expected (5-10 minutes)" - queried from RunPod API real-time availability endpoint

- **FR1.2.1:** Real-Time Cost Estimation
  * Description: System shall provide a continuously-updated cost estimation panel displaying comprehensive cost forecasts including duration range, cost range (min-max), GPU compute costs, spot interruption overhead, and total estimates based on dynamic configuration inputs. The estimation engine shall utilize historical job data, machine learning prediction models, and real-time GPU pricing to calculate accurate forecasts within ±15% variance, updating estimates within 500ms of configuration changes while displaying confidence intervals, accuracy disclaimers, and cost breakdown visualizations.
  * Impact Weighting: Cost Transparency / Budget Control / User Confidence
  * Priority: High
  * User Stories: US1.2.1
  * User Journey: UJ2.4.1 (Reviewing Cost Estimates), UJ1.3.1 (Understanding Training Costs)
  * Tasks: [T-1.2.1]
  * User Story Acceptance Criteria:
    - Cost estimation panel always visible on configuration screen
    - Displays: Estimated duration (hours), Estimated cost range (min-max)
    - Updates dynamically when changing: preset, GPU type, epochs, batch size
    - Calculation formula: (dataset_size × epochs × avg_time_per_epoch) × gpu_hourly_rate
    - Display accuracy disclaimer: "±15% based on historical data"
    - Show cost breakdown: GPU cost ($X), estimated spot interruptions (+$Y), total estimate ($Z)
    - Warning indicator if estimated cost exceeds $100
    - Warning if estimated duration exceeds 24 hours
    - Historical accuracy metric: "Past estimates within ±12% for balanced preset"
  * Functional Requirements Acceptance Criteria:
    - Cost estimation panel positioned as fixed sidebar or prominent card (always visible, no scrolling required) on job configuration screen
    - Estimation engine calculates duration using formula: estimated_duration_hours = (conversation_count × training_pairs_per_conversation × epochs × seconds_per_pair[preset]) / 3600, where seconds_per_pair = {Conservative: 120, Balanced: 180, Aggressive: 300}
    - Duration range calculation: min_duration = estimated_duration × 0.85, max_duration = estimated_duration × 1.15 (accounts for dataset complexity variance)
    - Cost calculation: base_gpu_cost = estimated_duration_hours × gpu_hourly_rate[spot: 2.49, on_demand: 7.99]
    - Spot interruption overhead calculation (if spot selected): interruption_probability = historical_interruption_rate (query from jobs table), expected_interruptions = CEIL(estimated_duration_hours / 8) × interruption_probability, recovery_overhead_cost = expected_interruptions × 0.25 × gpu_hourly_rate (assumes 15 min recovery time)
    - Total cost estimate: total_cost = base_gpu_cost + recovery_overhead_cost (if spot)
    - Cost range display: min_cost = total_cost × 0.85, max_cost = total_cost × 1.15 (±15% variance based on historical accuracy)
    - Real-time update mechanism: onChange event handlers for preset selector, GPU toggle, training file selection → debounced update (500ms delay) → recalculate estimates → animate transition to new values
    - Cost breakdown visualization: stacked bar chart or itemized list showing: "GPU Compute: $XX.XX (YY hours × $Z.ZZ/hr)", "Spot Interruption Buffer: +$X.XX (estimated recovery time)", "Total Estimate: $XX.XX - $YY.YY"
    - Accuracy disclaimer displayed prominently: "±15% variance based on 347 historical jobs. Actual cost depends on dataset complexity, spot interruptions, and training convergence."
    - Historical accuracy metric calculated: SELECT AVG(ABS((actual_cost - estimated_cost) / estimated_cost)) FROM training_jobs WHERE preset = '{selected_preset}' AND status = 'completed' AND created_at > NOW() - INTERVAL '90 days' - display as "Past estimates within ±12% for Balanced preset"
    - Warning triggers: IF estimated_cost > 100 THEN display warning badge "⚠ High Cost Job: $XXX estimated. Review configuration or consider Conservative preset."; IF estimated_duration_hours > 24 THEN display warning "⚠ Long Training Run: >24 hours. Consider reducing epochs or dataset size."
    - Budget validation check: IF estimated_cost > user_monthly_budget_remaining THEN display error "❌ Insufficient Budget: Estimated $XXX exceeds remaining budget $YYY. Increase budget limit or adjust configuration."
    - Cost comparison indicator: IF configuration changed THEN display delta: "↑ $XX.XX higher than previous estimate" or "↓ $XX.XX savings vs previous"
    - Confidence interval display: estimation_confidence = historical_accuracy_percentage (e.g., 88% of jobs within ±15%) - show as "88% confidence this estimate is accurate within range"
    - Tooltip explanations for each cost component: "GPU Compute: Primary cost based on training duration. Spot instances offer 70% savings.", "Spot Buffer: Estimated overhead for automatic checkpoint recovery if interrupted. Average 1-2 recoveries per 12-hour job.", "Total Estimate: Conservative range accounting for variance. 85% of jobs finish within this range."
    - Time-to-completion estimate: IF job started now THEN "Estimated completion: {current_date + estimated_duration_hours} (assuming spot provisioning <5 min)"
    - System stores estimation data in job record: estimated_duration_hours, estimated_cost_min, estimated_cost_max, estimation_confidence_percentage, estimation_algorithm_version, estimated_at_timestamp
    - Estimation refinement over time: System tracks actual vs estimated for each completed job, updates prediction model coefficients monthly using linear regression on: conversation_count, training_pairs, epochs, preset, GPU type → improved accuracy over time
    - Cost estimate export: "Download Cost Estimate" button generates PDF with: configuration summary, detailed cost breakdown, comparison to alternative configurations, historical accuracy data - useful for client quotes or budget approvals

- **FR1.2.2:** Pre-Job Budget Validation
  * Description: System shall implement comprehensive pre-job budget validation that queries current monthly spending, calculates remaining budget, compares against estimated job cost, and enforces budget limits with intelligent override mechanisms. The validation system shall provide clear error messaging, budget increase workflows with approval routing, forecast calculations including active jobs, and complete audit logging of all budget-related decisions while enabling manager overrides with justification requirements for financial accountability.
  * Impact Weighting: Budget Control / Financial Planning / Risk Mitigation
  * Priority: High
  * User Stories: US1.2.2
  * User Journey: UJ1.3.2 (Setting Monthly Budget Limits), UJ2.4.2 (Budget Validation Before Start)
  * Tasks: [T-1.2.2]
  * User Story Acceptance Criteria:
    - Calculate remaining monthly budget: (monthly_limit - month_to_date_spend)
    - Block job creation if estimated cost exceeds remaining budget
    - Error message: "Estimated cost ($75) exceeds remaining monthly budget ($50). Adjust configuration or increase budget limit."
    - Option to increase monthly budget limit directly from error dialog (requires manager approval)
    - Warning at 80% budget utilization: "You're at 80% of monthly budget ($400 of $500)"
    - Show forecast: "With X active jobs + this new job, projected monthly spend: $Y"
    - Allow budget override for managers with confirmation: "Proceed anyway (requires justification)"
    - Log all budget override actions for audit trail
  * Functional Requirements Acceptance Criteria:
    - System queries monthly budget data on job configuration page load: SELECT monthly_budget_limit, SUM(actual_cost) FROM budget_config JOIN training_jobs WHERE DATE_TRUNC('month', created_at) = CURRENT_MONTH GROUP BY user_id
    - Remaining budget calculation: remaining_budget = monthly_budget_limit - month_to_date_actual_cost - SUM(estimated_cost_max WHERE status IN ('active', 'queued', 'provisioning'))
    - Real-time budget validation executes before "Start Training" button enables: IF estimated_cost_max > remaining_budget THEN block_job_creation = true
    - Budget exceeded error modal displays with structured information: "❌ Budget Exceeded - Estimated Cost: $75, Remaining Budget: $50, Shortfall: $25", action options: "Reduce Job Cost (adjust preset/configuration)", "Increase Budget Limit", "Cancel Job Creation"
    - Budget utilization warning displays at 80% threshold: "⚠ Budget Alert: You've used 80% of your monthly budget ($400 of $500). Remaining: $100 for this billing period (resets {next_month_date})."
    - Forecast calculation includes active jobs: active_jobs_estimated_remaining = SUM(estimated_cost_max - (actual_cost || 0)) WHERE status IN ('active', 'provisioning', 'queued'), projected_monthly_total = month_to_date_actual_cost + active_jobs_estimated_remaining + current_job_estimated_cost_max
    - Forecast display: "Projected Monthly Spend: $XXX (includes X active jobs + this job). Budget Limit: $YYY. Projected Overage: $ZZZ" - color coded: green if under budget, red if over
    - Budget increase workflow: Click "Increase Budget Limit" → Modal with form fields: "New Monthly Limit: $_____ (current: $500)", "Justification (required): _____ (min 50 characters)", "Effective Date: [This Month / Next Month]", "Approval Required: Yes (manager must approve via email)"
    - Manager approval notification: System sends email to user's manager with: budget increase request details, justification, current spend vs limit, projected spend, "Approve" and "Deny" action buttons (unique signed URLs)
    - Manager approval processing: Click approve → Update budget_config SET monthly_budget_limit = new_limit, approved_by = manager_id, approved_at = NOW() → Email requester: "Budget increase approved, new limit: $XXX effective immediately"
    - Budget override for managers: IF user_role IN ('manager', 'admin', 'owner') THEN display "Manager Override" button → Confirmation modal: "Proceed despite budget limit? This will exceed your monthly budget. Justification Required: _____" → Log override: INSERT INTO budget_overrides (user_id, job_id, override_amount, justification, approved_at)
    - Audit logging: All budget-related actions logged in `budget_audit_log` table with fields: action_type (validation_blocked, override_approved, limit_increased, warning_triggered), user_id, job_id, amount, justification, timestamp, ip_address
    - Budget dashboard link displayed in error message: "View detailed budget breakdown and history: [Budget Dashboard]"
    - Configuration adjustment suggestions: "💡 Cost Reduction Tips: Switch to Conservative preset (save $XX), Use Spot instead of On-Demand (save $YY), Reduce epochs from X to Y (save $ZZ)"
    - Soft warning at 90% budget utilization: "⚠ Critical Budget Alert: 90% of monthly budget used ($450 of $500). Only $50 remaining. Consider prioritizing essential training runs."
    - Budget reset notification: On first day of new billing period, display: "✓ Budget Reset: Your monthly training budget has been reset to $XXX. Last month's spend: $YYY."
    - Grace period handling: System allows up to 10% budget overage (configurable) without blocking: "⚠ Slight Overage: This job will exceed budget by 5% ($525 total vs $500 limit). Proceeding allowed as within 10% grace period."
    - Budget forecast accuracy tracking: System compares projected vs actual monthly spend, displays historical accuracy: "Budget forecasts have been within ±8% for past 6 months" - builds user confidence in estimates

- **FR1.3.1:** Add Job Metadata & Documentation
  * Description: System shall provide comprehensive metadata and documentation capabilities enabling users to assign descriptive names, add purpose descriptions, document experimental hypotheses and notes, apply searchable tags, associate jobs with client projects for cost attribution, and maintain complete documentation trails. The metadata system shall support auto-generation of intelligent default names, validation of input constraints, tag management with custom tag creation, and full-text search across all metadata fields to enable efficient job organization, knowledge sharing, and historical tracking.
  * Impact Weighting: Organization / Knowledge Sharing / Searchability
  * Priority: Medium
  * User Stories: US1.3.1
  * User Journey: UJ2.5.1 (Adding Job Documentation), UJ8.3.1 (Job Notes and Experiment Documentation)
  * Tasks: [T-1.3.1]
  * User Story Acceptance Criteria:
    - Job name field (required, 3-100 characters): Auto-populated as "[Training File Name] - [Preset] - [Date]"
    - Description field (optional, 500 character limit): "Document the purpose of this training run"
    - Notes field (optional, 2000 character limit): "Experimental notes, hypothesis, configuration rationale"
    - Tags field: Multi-select dropdown with common tags (experiment, production, client-delivery, test, poc)
    - Custom tag creation allowed
    - Client/Project assignment dropdown (optional): Link job to specific client project for cost tracking
    - All metadata searchable in job history
    - Metadata visible in job details page and comparison views
  * Functional Requirements Acceptance Criteria:
    - Job name field displayed as required text input with character counter (0/100), validation enforces 3-100 character length, displays error "Job name must be between 3 and 100 characters" if invalid
    - Auto-population logic executes on configuration page load: job_name = "{training_file_name} - {preset_name} - {YYYY-MM-DD}" (e.g., "Elena Morales Financial - Balanced - 2025-12-16"), user can edit/override default name
    - Name uniqueness check: System queries existing job names for current user, displays warning (not error) if duplicate found: "⚠ Similar job name already exists. Consider adding version number or distinguishing details."
    - Description field rendered as textarea (max 500 characters) with counter display, placeholder text: "What is the purpose of this training run? (e.g., 'First production model for Acme client', 'Testing aggressive parameters on high-emotion dataset')", optional field allows empty submission
    - Notes field rendered as larger textarea (2000 character limit) with markdown formatting support (bold, italic, lists, code blocks), placeholder: "Document your hypothesis, experimental variables, expected outcomes, or configuration rationale. Use markdown for formatting.", auto-save draft notes to localStorage every 30 seconds to prevent data loss
    - Tags system: Multi-select dropdown populated with predefined tags from `job_tags` table: {experiment, production, client-delivery, test, poc, research, optimization, validation, baseline, iteration-1, iteration-2, high-priority, low-priority, approved, needs-review}
    - Tag selection: Click dropdown → Display checkbox list → Select multiple tags → Selected tags display as colored pills below dropdown with X icon to remove
    - Custom tag creation: Type new tag name in dropdown → If not found in existing tags → Display "Create new tag: '{tag_name}'" option → Click to add → New tag inserted into `job_tags` table and available for future jobs
    - Tag validation: Max 10 tags per job, tag names limited to 3-30 characters, lowercase alphanumeric + hyphen only (no spaces), displays error "Maximum 10 tags allowed" if limit exceeded
    - Client/Project assignment: Dropdown populated from `clients` and `projects` tables, displays hierarchical structure "Client: Acme Financial → Project: Q4 2025 Model Enhancement", optional selection enables cost attribution reporting
    - Client/Project autocomplete: Type to search client/project names, displays matching results with highlighting, "Create New Client/Project" option at bottom of dropdown if no match found
    - Metadata storage in `training_jobs` table: name (VARCHAR 100), description (TEXT 500), notes (TEXT 2000), tags (JSONB array), client_id (UUID FK nullable), project_id (UUID FK nullable), metadata_updated_at (TIMESTAMP)
    - Search functionality: Job history page includes search bar with placeholder "Search by name, description, notes, or tags", search executes as user types (debounced 500ms), performs full-text search across name, description, notes fields using PostgreSQL tsvector, tag search uses JSONB array containment operator
    - Search results highlighting: Matching text highlighted in yellow in search results, displays match context (50 characters before/after match), shows match count per job: "3 matches in notes"
    - Metadata display in job details page: Dedicated "Job Information" card showing: Name (editable inline), Description (editable), Notes (expandable/collapsible with markdown rendering), Tags (clickable pills linking to filtered job list), Client/Project (linked to project cost dashboard), Created By (user avatar + name), Created At, Last Updated
    - Metadata editing after job creation: "Edit Metadata" button opens modal with all fields pre-populated, allows updates to description, notes, tags, client/project (name cannot be changed if job started), saves changes with metadata_updated_at timestamp
    - Job comparison views include metadata: Side-by-side comparison shows each job's name, tags, description in header section, enables comparison filtering by shared tags
    - Export functionality: "Export Job Data" includes metadata in CSV/JSON export: all fields, tag array, client/project names
    - Analytics integration: System tracks most-used tags, common job naming patterns, documentation completeness percentage (jobs with description + notes / total jobs) - insights displayed in team dashboard
    - Template integration: When saving job as configuration template, metadata fields are optionally included: "Include job description as template description? [Yes/No]"
    - Notification mentions: When sharing job link, description is included in email/Slack notification: "Check out this training job: {name} - {description}"

- **FR1.3.2:** Review Configuration Before Start
  * Description: System shall implement a comprehensive pre-flight configuration review process presenting users with a full-screen confirmation modal displaying complete training configuration summary, cost breakdown, budget impact analysis, risk warnings, and interactive confirmation checklist before initiating GPU provisioning. The review interface shall consolidate all configuration decisions, validate prerequisites, enable last-minute adjustments, require explicit user acknowledgment of costs and risks, and provide clear cancellation options to prevent accidental or uninformed job initiation while building user confidence through transparent information disclosure.
  * Impact Weighting: Risk Mitigation / Cost Control / User Confidence
  * Priority: High
  * User Stories: US1.3.2
  * User Journey: UJ2.6.1 (Configuration Review), UJ2.6.2 (Pre-Start Confirmation)
  * Tasks: [T-1.3.2]
  * User Story Acceptance Criteria:
    - "Review & Start Training" button opens full-screen confirmation modal
    - Display complete configuration summary:
    - Training file: name, conversation count, quality scores
    - Hyperparameters: preset name + all values (r, lr, epochs, batch_size, gradient_accumulation_steps)
    - GPU selection: spot/on-demand, GPU type, hourly rate
    - Cost estimate: duration range, cost range, spot interruption risk
    - Budget impact: current monthly spend, this job cost, projected total
    - Warnings section: Display any configuration warnings (high cost, aggressive parameters, low budget)
    - Confirmation checklist:
    - [ ] I have reviewed the configuration
    - [ ] I understand the estimated cost ($X-Y)
    - [ ] I have budget approval if required
    - "Start Training" button disabled until checklist completed
    - "Edit Configuration" button to go back and adjust
    - "Cancel" button to abort job creation
    - After confirmation: Job status changes to "queued", GPU provisioning begins
  * Functional Requirements Acceptance Criteria:
    - "Review & Start Training" button displayed prominently at bottom of configuration form, styled as primary action button (large, blue, with icon), enabled only when all required configuration fields are valid (training file selected, preset chosen, GPU type selected, name entered)
    - Click button triggers full-screen modal overlay (dims background, prevents interaction with configuration form), modal cannot be closed by clicking outside (must use explicit Cancel or Start Training buttons)
    - Modal header displays: "Review Training Configuration - Final Check Before Starting" with warning icon, estimated total cost prominently shown in header: "Total Estimated Cost: $45-60"
    - **Configuration Summary Section** rendered as structured cards:
    - **Training Dataset Card**: Training file name (bold), Conversation count ("242 conversations, 1,567 training pairs"), Average quality scores with visual indicators ("Empathy: 4.5/5 ✓, Clarity: 4.3/5 ✓, Appropriateness: 4.6/5 ✓"), Scaffolding distribution preview ("10 personas, 8 emotional arcs, 6 topics"), Human review percentage ("15% human-reviewed"), File size and storage location
    - **Hyperparameters Card**: Preset name with badge (Conservative/Balanced/Aggressive with color coding), All technical parameters in readable format: "LoRA Rank (r): 16", "Learning Rate: 0.0002", "Training Epochs: 3", "Batch Size: 2", "Gradient Accumulation: 2 steps", "Target Modules: Query, Key, Value, Output projections", "LoRA Alpha: 32", "Dropout Rate: 0.1", Tooltip: "Hover over any parameter for explanation"
    - **GPU Configuration Card**: GPU type ("H100 PCIe 80GB"), Pricing tier with badge ("Spot Instance - Save 70%"), Hourly rate ("$2.49/hr"), Estimated interruption risk ("18% chance based on 30-day history"), Recovery guarantee ("Automatic checkpoint recovery <10 minutes"), Provisioning time estimate ("2-5 minutes to start")
    - **Cost Analysis Section**: Visual cost breakdown as horizontal bar chart showing: "GPU Compute: $XX.XX (YY hrs × $Z.ZZ/hr) [80% of total]", "Spot Interruption Buffer: $X.XX [5% of total]", "Storage & Transfer: $X.XX [2% of total]", Total estimate range: "$45.00 - $60.00 (±15% variance)", Confidence level: "88% of jobs finish within this range", Comparison to on-demand alternative: "Save $90 vs on-demand ($150)"
    - **Budget Impact Section**: Current monthly spend with progress bar ("$387 of $500 used - 77%"), This job cost (highlighted): "+$52 (estimated max)", Projected monthly total: "$439 total (88% of budget)", Remaining budget after this job: "$61 available", Visual indicator: green if <90% budget, yellow if 90-95%, red if >95%, Forecast: "Sufficient budget for 1-2 more jobs this month"
    - **Warnings Section** (conditionally displayed): High cost warning (if estimated_cost > 100): "⚠ High-Cost Training Run: This job will cost $XXX. Consider Conservative preset to reduce cost by 60%.", Aggressive parameters warning (if preset = aggressive): "⚠ Advanced Configuration: Aggressive parameters may take longer and cost more. Recommended only for complex datasets.", Low budget warning (if remaining_budget < estimated_cost_max × 1.5): "⚠ Limited Budget Remaining: This job will use most of your remaining monthly budget. Consider budgeting for potential overages.", Long duration warning (if estimated_duration > 20): "⚠ Extended Training Time: This job may take over 20 hours. Spot interruptions are more likely for long runs.", First-time user warning: "ℹ First Training Run: This is your first training job. Start with Conservative preset to gain familiarity with the platform."
    - **Confirmation Checklist**: Three mandatory checkboxes (must all be checked before "Start Training" button enables): "☐ I have reviewed the complete training configuration above and confirm all settings are correct", "☐ I understand the estimated cost ($45-60) and agree to proceed with charges within this range", "☐ I have obtained necessary budget approval (if required by my organization) and authorization to incur these costs", Checkbox validation: "Start Training" button remains disabled (grayed out) until all three checkboxes are checked
    - **Action Buttons**: "Start Training" button (prominent, green, initially disabled): Click triggers job start workflow (described below), "Edit Configuration" button (secondary styling): Closes modal and returns to configuration form with all settings preserved for editing, "Cancel" button (tertiary styling): Closes modal and returns to job list (does not create job in database)
    - **Job Start Workflow** (triggered by "Start Training" click): Insert training_job record with status='queued', Redirect to job details page (/training-jobs/{job_id}), Initiate async GPU provisioning: Call RunPod API to create pod with configuration, Update job status to 'provisioning', Display loading screen: "Provisioning GPU... Estimated time: 2-5 minutes", Stream provisioning status updates via webhook, On GPU ready: Update status to 'starting', launch training container, Send notification: "Training started for {job_name}"
    - **Job Record Creation**: training_jobs INSERT with fields: id (UUID), training_file_id (FK), name, description, notes, tags (JSONB), preset (VARCHAR), configuration (JSONB with all hyperparameters), gpu_pricing_tier, gpu_hourly_rate, estimated_duration_hours, estimated_cost_min, estimated_cost_max, status ('queued'), created_by (user_id), created_at (NOW()), Budget check: IF estimated_cost_max > remaining_monthly_budget AND NOT manager_override THEN ROLLBACK INSERT AND display error
    - Review modal accessibility: Keyboard navigation support (Tab through sections, Enter to check checkboxes, Escape to cancel), Screen reader announcements for all sections and warnings, High contrast mode support, Focus trap (Tab key cycles within modal, cannot Tab to background elements)
    - Analytics tracking: Log review modal views, time spent on review page (median should be 30-60 seconds), checkbox completion rates, edit button clicks (indicates configuration uncertainty), cancel vs start rates - insights used to improve configuration UX
    - Template support: If starting from saved template, display "Based on Template: {template_name}" with link to template details
    - Comparison to previous job: If user has completed similar jobs (same training file or preset), display: "Similar to your previous job: {job_name} - Final cost was $XX vs estimated $YY (difference: Z%)" - builds confidence in estimates

## 2. Training Job Execution & Monitoring

- **FR2.1.1:** Live Training Progress Dashboard
  * Description: System shall provide a comprehensive real-time training progress dashboard featuring live-updating progress indicators, interactive loss curve visualization with dual-axis charting, detailed metrics table with trend indicators, cost accumulation tracking, and automated refresh mechanisms. The dashboard shall fetch metrics via webhook-driven database updates or polling, render loading states gracefully, support data export, provide zoom/pan controls for detailed analysis, and maintain responsive performance with 60-second refresh intervals while displaying comprehensive training status information to eliminate user anxiety and enable informed monitoring decisions.
  * Impact Weighting: User Confidence / Transparency / Productivity
  * Priority: High
  * User Stories: US2.1.1
  * User Journey: UJ3.1.1 (Monitoring Live Training Progress), UJ3.1.2 (Understanding Training Metrics)
  * Tasks: [T-2.1.1]
  * User Story Acceptance Criteria:
    - Training jobs list page shows all jobs (active, completed, failed, queued)
    - Click active job opens detailed progress dashboard
    - **Progress Header Card**:
    - Overall progress: 42% complete (Step 850 of 2000)
    - Current stage: Training (with visual stage indicator)
    - Elapsed time: 6h 23m
    - Estimated remaining: 8h 15m (updates based on actual speed)
    - Current epoch: 2 of 3
    - **Live Loss Curve Graph**:
    - Line chart with dual y-axes: training loss (left), validation loss (right)
    - X-axis: training step number
    - Updates every 60 seconds via polling or websocket
    - Zoom controls to focus on recent steps
    - Export graph as PNG for reports
    - **Current Metrics Table**:
    - Training loss: 0.342 (↓ from 0.389)
    - Validation loss: 0.358 (↓ from 0.412)
    - Learning rate: 0.000182 (current schedule value)
    - GPU utilization: 87%
    - Perplexity (if available): 1.43
    - **Cost Tracker Card**:
    - Estimated cost: $45-55
    - Current spend: $22.18 (49% of estimate)
    - Hourly rate: $2.49/hr (spot)
    - Projected final cost: $47.32
    - Auto-refresh every 60 seconds (with manual refresh button)
    - Loading skeletons during data fetch
  * Functional Requirements Acceptance Criteria:
    - Dashboard page accessible at `/training-jobs/{job_id}`, loads within 2 seconds for jobs with <10K metric data points
    - **Progress Header Card** renders with structured layout: Overall progress bar (animated, color-coded: blue for active, green for completed, red for failed), Progress percentage (large font: "42% Complete"), Current step indicator ("Step 850 of 2,000"), Current stage badge ("Training" with animated pulse icon), Elapsed time ("6h 23m"), Estimated remaining ("8h 15m remaining, updates every 60s based on actual training speed"), Current epoch ("Epoch 2 of 3")
    - Progress percentage calculation: (current_step / total_steps) × 100, where total_steps = conversation_count × training_pairs_per_conversation × epochs
    - Elapsed time calculated: NOW() - job.started_at, formatted as "Xh Ym" or "Xd Yh" if >24 hours
    - Estimated remaining calculation: ((total_steps - current_step) × average_seconds_per_step) / 3600, where average_seconds_per_step = (NOW() - started_at).total_seconds() / current_step, updated every 60 seconds as actual speed observed
    - **Live Loss Curve Graph** implemented with Chart.js or Recharts: Dual y-axis line chart (training loss on left axis, validation loss on right axis), X-axis displays training step numbers with smart tick intervals (every 100 steps if <1000 total, every 500 if >5000), Training loss line: solid blue with data points, Validation loss line: dashed orange with data points, Grid lines: light gray, Tooltip on hover: "Step 850: Training Loss 0.342, Validation Loss 0.358", Legend with toggle buttons to show/hide series
    - Loss data fetched from `training_metrics_history` table: SELECT step, training_loss, validation_loss FROM training_metrics_history WHERE training_job_id = {job_id} ORDER BY step ASC, data cached in component state, new data appended on refresh
    - Zoom controls: Interactive zoom buttons (+/-) or pinch-to-zoom on mobile, Zoom in: focus on most recent 500 steps, Zoom out: show full training history, Reset zoom: display complete dataset, Pan controls: drag chart horizontally to view different time ranges
    - Export functionality: "Export Graph" button generates PNG image (2000×1200px) using canvas rendering, includes job name, timestamp, axis labels, embedded in download with filename: "{job_name}-loss-curve-{timestamp}.png"
    - **Current Metrics Table** renders as responsive data table: Two-column layout (metric name | current value with trend indicator), Metrics displayed: "Training Loss: 0.342 ↓ from 0.389 (-12.1%)", "Validation Loss: 0.358 ↓ from 0.412 (-13.1%)", "Learning Rate: 0.000182 (cosine schedule)", "GPU Utilization: 87%", "GPU Memory: 68GB / 80GB (85%)", "Perplexity: 1.43 (if calculated)", "Tokens/Second: 1,247", "Steps/Hour: 156"
    - Trend indicators: Calculate delta from previous metric value (stored in job record: latest_loss vs previous_loss), Display arrow: ↓ green if improving (loss decreasing), ↑ red if worsening (loss increasing), — gray if unchanged, Percentage change: "(±X.X%)"
    - Learning rate display: Current LR value from scheduler, Schedule type indicator: "(cosine schedule, warmup: 5%)"
    - GPU metrics: Utilization percentage from RunPod webhook, Memory usage: "{used_gb}GB / {total_gb}GB ({percentage}%)", Warning if utilization <50%: "⚠ Low GPU utilization, possible bottleneck"
    - **Cost Tracker Card**: Prominent card with large cost display, Layout: "Estimated Cost: $45-55" (top, gray), "Current Spend: $22.18" (large, bold, color-coded), "49% of estimate" (progress bar), Hourly rate: "$2.49/hr (spot)", Projected final cost: "$47.32" (based on current rate and estimated remaining time)
    - Cost calculation: current_spend = ((NOW() - started_at).total_hours + spot_interruption_recovery_time_hours) × gpu_hourly_rate, projected_final_cost = current_spend + (estimated_remaining_hours × gpu_hourly_rate)
    - Cost progress visualization: Horizontal progress bar showing current_spend vs estimated_cost_max, Color coding: green if <80% of estimate, yellow if 80-100%, red if >100%
    - Cost warning alerts: If current_spend > estimated_cost_max: "⚠ Cost Exceeding Estimate: Current $XX vs estimated $YY. Monitor closely or consider cancelling."
    - **Auto-Refresh Mechanism**: Polling approach: setInterval(() => fetchJobMetrics(), 60000), Fetches latest data from `/api/training/jobs/{job_id}/metrics?latest=true`, Updates all dashboard components with new data, Loading indicator: small spinner icon in header during fetch
    - Manual refresh button: Circular arrow icon in dashboard header, Click triggers immediate fetchJobMetrics(), Disabled during fetch (prevents duplicate requests), Toast notification: "Metrics updated" on successful refresh
    - Loading skeletons: During initial page load, display skeleton placeholders (gray animated rectangles) matching final layout: header card skeleton, graph skeleton (empty chart with axes), metrics table skeleton (4-5 rows), cost card skeleton - replaced with actual data once loaded
    - Websocket alternative (future enhancement): Real-time updates pushed from server via WebSocket connection, Eliminates polling delay, More efficient for multiple concurrent users, Falls back to polling if WebSocket unavailable
    - Error handling: If metrics fetch fails: Display last known data with timestamp "Last updated: 2 minutes ago", Retry button: "Retry Refresh", Error message: "Unable to fetch latest metrics. Check connection."
    - Responsiveness: Dashboard adapts to screen sizes: Desktop (>1024px): Side-by-side layout for graph + metrics, Tablet (768-1023px): Stacked layout, Mobile (<768px): Single column, collapsible sections
    - Performance optimization: Virtualization for metric history if >5000 data points, Graph re-renders only when new data available (memoization), Debounced resize handlers for responsive charts

- **FR2.1.2:** Training Stage Indicators
  * Description: [To be filled]
  * Impact Weighting: User Experience / Transparency / Reduced Anxiety
  * Priority: Medium
  * User Stories: US2.1.2
  * Tasks: [T-2.1.2]
  * User Story Acceptance Criteria:
    - Visual stage progress bar with 4 stages:
    1. **Preprocessing** (2-5 minutes):
       - Dataset loading from Supabase Storage
       - Tokenization and formatting
       - Train/validation split (80/20)
       - Status: "Tokenizing 242 conversations..."
    2. **Model Loading** (10-15 minutes):
       - Download Llama 3 70B from Hugging Face Hub (or load from cache)
       - Apply 4-bit quantization (QLoRA)
       - Initialize LoRA adapters with target modules
       - Status: "Loading Llama 3 70B model (4-bit quantization)..."
    3. **Training** (10-20 hours):
       - Gradient updates across epochs
       - Checkpoint saves every 100 steps
       - Validation runs after each epoch
       - Status: "Training epoch 2/3 - Step 850/2000..."
    4. **Finalization** (5-10 minutes):
       - Save final LoRA adapters (adapter_model.bin, adapter_config.json)
       - Upload artifacts to Supabase Storage
       - Calculate final metrics
       - Status: "Saving adapters and finalizing..."
    - Each stage shows: name, status (pending/active/complete), estimated duration, actual duration
    - Progress bar fills proportionally (preprocessing 2%, model loading 8%, training 85%, finalization 5%)
    - Current stage highlighted with animated indicator
    - Completed stages show checkmark and actual duration
    - Failed stage shows error icon and error message
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR2.1.3:** Webhook Event Log
  * Description: [To be filled]
  * Impact Weighting: Debugging / Troubleshooting / Support Reduction
  * Priority: Medium
  * User Stories: US2.1.3
  * Tasks: [T-2.1.3]
  * User Story Acceptance Criteria:
    - "Event Log" tab on job details page
    - Table view with columns: Timestamp, Event Type, Message, Payload (expandable)
    - Event types color-coded:
    - Status changes (blue): queued → preprocessing → training → completed
    - Metrics updates (green): loss updated, epoch completed, checkpoint saved
    - Warnings (yellow): GPU utilization low, loss plateau detected
    - Errors (red): OOM error, API timeout, validation failure
    - Expandable rows show full webhook payload as formatted JSON
    - Filter events by type: All / Status / Metrics / Warnings / Errors
    - Search by keyword in messages
    - Export log as JSON or CSV for detailed analysis
    - Real-time updates: new events appear automatically
    - Pagination: 50 events per page
    - Example events:
    - "2025-12-15 14:23:42 | Status | Training started (GPU: H100 PCIe 80GB spot)"
    - "2025-12-15 14:28:15 | Metrics | Step 100: loss=0.521, lr=0.0002, gpu_util=89%"
    - "2025-12-15 14:33:08 | Warning | GPU utilization dropped to 45% (possible throttling)"
    - "2025-12-15 15:12:33 | Error | Spot instance interrupted, initiating checkpoint recovery"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR2.2.1:** Cancel Active Training Job
  * Description: [To be filled]
  * Impact Weighting: Cost Control / Risk Mitigation / User Control
  * Priority: High
  * User Stories: US2.2.1
  * Tasks: [T-2.2.1]
  * User Story Acceptance Criteria:
    - "Cancel Job" button prominent on job dashboard (red, destructive styling)
    - Click opens confirmation modal:
    - Warning: "This will permanently stop training and terminate the GPU instance"
    - Display: Current progress (42% complete), elapsed time (6h 23m), cost spent ($22.18)
    - Question: "Reason for cancellation?" (dropdown: Loss not decreasing, Too expensive, Wrong configuration, Testing, Other)
    - Optional notes field for explanation
    - Confirmation checkbox: "I understand this action cannot be undone"
    - After confirmation:
    - Job status updates to "cancelled"
    - Send cancellation request to RunPod API
    - Terminate GPU instance within 60 seconds
    - Final cost calculation based on elapsed time
    - Notification: "Job cancelled. Final cost: $22.18. GPU instance terminated."
    - Cancelled jobs appear in job history with "cancelled" status badge
    - Can view partial progress (loss curves, metrics) even after cancellation
    - Cannot resume cancelled jobs (must create new job)
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR2.2.2:** Pause and Resume Training (Future Enhancement)
  * Description: [To be filled]
  * Impact Weighting: Cost Optimization / Flexibility
  * Priority: Low (Future Enhancement)
  * User Stories: US2.2.2
  * Tasks: [T-2.2.2]
  * User Story Acceptance Criteria:
    - "Pause Job" button next to "Cancel Job"
    - Pause action:
    - Save checkpoint immediately
    - Upload checkpoint to Supabase Storage
    - Terminate GPU instance
    - Update job status to "paused"
    - Record pause timestamp
    - "Resume Job" button on paused jobs:
    - Provision new GPU instance (spot or on-demand)
    - Download latest checkpoint
    - Continue training from last saved step
    - Update status to "training"
    - Track total paused duration separately from training duration
    - Cost calculation includes only active training time
    - Use case: Pause during expensive peak hours, resume during cheaper off-peak hours
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR2.3.1:** View All Training Jobs
  * Description: [To be filled]
  * Impact Weighting: Team Coordination / Oversight / Organization
  * Priority: High
  * User Stories: US2.3.1
  * Tasks: [T-2.3.1]
  * User Story Acceptance Criteria:
    - Training jobs list page at `/dashboard/training-jobs`
    - Table columns: Job Name, Status, Configuration, Created By, Started At, Duration, Cost, Actions
    - Status badges color-coded: Queued (gray), Training (blue), Completed (green), Failed (red), Cancelled (orange)
    - Filters:
    - Status: All / Active / Completed / Failed / Cancelled / Queued
    - Created by: All / [User dropdown]
    - Date range: Last 7 days / Last 30 days / Last 90 days / Custom range
    - Configuration preset: All / Conservative / Balanced / Aggressive
    - Cost range: All / <$50 / $50-100 / >$100
    - GPU type: All / Spot / On-Demand
    - Sort by: Created date (newest first), Duration, Cost, Status, Creator
    - Search by: Job name, notes, tags
    - Pagination: 25 / 50 / 100 jobs per page
    - Click row opens job details page
    - Bulk actions: Select multiple jobs, Cancel selected (if active), Delete selected (if completed/failed)
    - Export table as CSV for reporting
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR2.3.2:** Training Queue Management
  * Description: [To be filled]
  * Impact Weighting: Resource Planning / Client Communication / Operational Efficiency
  * Priority: Medium
  * User Stories: US2.3.2
  * Tasks: [T-2.3.2]
  * User Story Acceptance Criteria:
    - "Queue" tab on training jobs page
    - Shows jobs with status "queued" or "pending_gpu_provisioning"
    - Displays: Queue position, Job name, Configuration, Estimated start time, Creator
    - Estimated start time calculation: SUM(remaining_time_of_active_jobs) + GPU_provisioning_time
    - Real-time updates as active jobs complete
    - Queue priority logic: FIFO (first in, first out) by default
    - Option to promote urgent jobs to front of queue (requires manager approval)
    - Max concurrent training jobs limit: 3 (configurable based on budget)
    - If queue limit reached, block new job creation with message: "Queue full (3/3 active jobs). Wait for completion or cancel an active job."
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

## 3. Error Handling & Recovery

- **FR3.1.1:** Out of Memory Error Handling
  * Description: [To be filled]
  * Impact Weighting: Success Rate / User Experience / Learning
  * Priority: High
  * User Stories: US3.1.1
  * Tasks: [T-3.1.1]
  * User Story Acceptance Criteria:
    - Detect "OutOfMemoryError" or "CUDA out of memory" in training logs
    - Job status updates to "failed" with error type "OOM"
    - Error modal displays:
    - **Problem**: "Your configuration exceeded the 80GB VRAM capacity of the H100 GPU"
    - **Likely cause**: "batch_size=4 with 242 conversations and r=32 requires ~92GB VRAM"
    - **Suggested fixes**:
      1. Reduce batch_size to 2 (recommended)
      2. Switch to Conservative preset (r=8 instead of r=32)
      3. Reduce sequence length (if conversations are very long)
    - **Quick retry**: Button "Retry with batch_size=2" pre-fills configuration with suggested fix
    - Link to documentation: "Understanding VRAM Usage in LoRA Training"
    - Track OOM error frequency per configuration to improve preset recommendations
    - Example error message: "OutOfMemoryError: Your dataset + batch_size=4 + r=32 exceeds 80GB VRAM. Try batch_size=2 (Conservative preset) or contact support if issue persists."
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR3.1.2:** Dataset Format Error Handling
  * Description: [To be filled]
  * Impact Weighting: Debugging / Data Quality / Time Savings
  * Priority: High
  * User Stories: US3.1.2
  * Tasks: [T-3.1.2]
  * User Story Acceptance Criteria:
    - Detect dataset validation errors during preprocessing stage
    - Job status updates to "failed" with error type "Dataset Format Error"
    - Error modal displays:
    - **Problem**: "Training data validation failed during preprocessing"
    - **Specific error**: "Conversation #47 (ID: conv_abc123) is missing required field 'target_response'"
    - **Conversation details**: Show conversation metadata (persona, emotional_arc, topic)
    - **Data sample**: Display the malformed conversation JSON with error highlighted
    - **How to fix**:
      1. Go to conversation editor
      2. Fix missing field
      3. Regenerate training file
      4. Retry training job
    - **Quick action**: "Open Conversation Editor" button (deep link to conversation ID)
    - Validate training file schema before job creation to catch errors early
    - Prevent job creation if validation fails with clear error message
    - Example error: "DatasetFormatError: Training pair #47 missing 'target_response' field. Fix in conversation editor and regenerate training file."
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR3.1.3:** GPU Provisioning Error Handling
  * Description: [To be filled]
  * Impact Weighting: User Experience / Flexibility / Reliability
  * Priority: High
  * User Stories: US3.1.3
  * Tasks: [T-3.1.3]
  * User Story Acceptance Criteria:
    - Detect GPU provisioning failures from RunPod API
    - Common scenarios:
    - **No spot GPUs available**: "All H100 spot instances are currently in use. High demand."
    - **Spot provisioning timeout**: "Waited 10 minutes, no spot GPU allocated."
    - **Region unavailable**: "RunPod datacenter temporarily unavailable."
    - Error modal displays:
    - **Problem**: "No H100 spot GPUs currently available"
    - **Reason**: "High demand in RunPod datacenter (92% utilization)"
    - **Options**:
      1. **Auto-retry** (spot): "Automatically retry every 5 minutes until GPU available (max 1 hour)"
      2. **Switch to on-demand**: "Start immediately on-demand GPU (+$5/hr, guaranteed availability)"
      3. **Cancel and retry later**: "Cancel job, try again in 30-60 minutes during off-peak hours"
    - **Estimated wait time**: "Historical data shows spot GPUs typically available within 15-30 minutes"
    - If auto-retry selected:
    - Job status: "queued_waiting_for_gpu"
    - Retry every 5 minutes for 1 hour
    - Notification when GPU provisioned and training starts
    - Notification if 1 hour timeout reached: "Still no spot GPU available. Switch to on-demand or cancel?"
    - Track provisioning failure rate to identify patterns (time of day, datacenter congestion)
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR3.2.1:** Spot Instance Interruption Recovery
  * Description: [To be filled]
  * Impact Weighting: Cost Efficiency / Reliability / User Confidence
  * Priority: High
  * User Stories: US3.2.1
  * Tasks: [T-3.2.1]
  * User Story Acceptance Criteria:
    - **During training**: Checkpoint saved every 100 steps to Supabase Storage bucket `training-checkpoints`
    - Checkpoint includes: model weights (LoRA adapters), optimizer state, training step, epoch, random seed
    - Checkpoint naming: `{job_id}/checkpoint-step-{step_number}.pt`
    - **On spot interruption**:
    - RunPod sends webhook: "Spot instance interrupted"
    - Job status updates to "interrupted"
    - System initiates recovery immediately
    - **Automatic recovery process**:
      1. Provision new spot instance (same configuration)
      2. Download latest checkpoint from storage
      3. Resume training from last saved step
      4. Update status to "training" (resumed)
      5. Track interruption count
    - **Dashboard display**:
    - Interruption badge: "Interrupted 2× (auto-recovered)"
    - Interruption log: "Interrupted at step 850 (6h 23m), resumed at step 850 (6h 32m) - 9 min downtime"
    - Total interruption downtime tracked separately
    - **Success criteria**:
    - Resume within 10 minutes of interruption
    - 95%+ successful recovery rate
    - Cost tracking includes interruption overhead
    - Notification: "Training interrupted at 42% complete. Auto-recovery in progress... [Track Status]"
    - Notification: "Training resumed from checkpoint (Step 850). Estimated completion: 8h 15m remaining."
    - If recovery fails 3 times: Offer option to switch to on-demand instance
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR3.2.2:** Manual Checkpoint Resume
  * Description: [To be filled]
  * Impact Weighting: Cost Efficiency / Flexibility / User Control
  * Priority: Medium
  * User Stories: US3.2.2
  * Tasks: [T-3.2.2]
  * User Story Acceptance Criteria:
    - Failed jobs with available checkpoints show "Resume from Checkpoint" button
    - Click opens configuration modal pre-filled with previous settings
    - Allow adjustments:
    - Switch GPU type (spot → on-demand)
    - Adjust remaining epochs
    - Change learning rate schedule
    - Modify batch size (if OOM was the issue)
    - Display: "Resume from Step 850 (42% complete). Remaining: 1.5 epochs (~8 hours)"
    - Cost estimate updates based on remaining work
    - Confirmation: "Resume training from last checkpoint with adjusted configuration?"
    - After confirmation:
    - Create new job linked to original job
    - Download checkpoint from storage
    - Continue training from saved step
    - Track as "resumed from job_abc123"
    - Useful scenarios: OOM error → reduce batch_size → resume; Spot interruption loop → switch to on-demand → resume
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR3.3.1:** One-Click Retry with Same Configuration
  * Description: [To be filled]
  * Impact Weighting: Productivity / User Experience / Time Savings
  * Priority: Medium
  * User Stories: US3.3.1
  * Tasks: [T-3.3.1]
  * User Story Acceptance Criteria:
    - Failed jobs show "Retry Job" button
    - Click creates new job with identical configuration:
    - Same training file
    - Same hyperparameter preset
    - Same GPU selection (spot/on-demand)
    - Same job name with suffix " (Retry #2)"
    - Confirmation modal displays:
    - **Original job**: Name, failure reason, elapsed time before failure
    - **Retry configuration**: Complete configuration summary
    - **Cost estimate**: Fresh estimate for new attempt
    - Option to edit configuration before retrying
    - After confirmation:
    - Create new job in "queued" status
    - Link to original job for reference
    - Start training automatically
    - Useful for transient errors: Network timeouts, GPU provisioning delays, spot interruptions without checkpoints
    - Track retry count per job: "This is retry #2 of job_abc123"
    - Success rate metric: "85% of retried jobs complete successfully"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR3.3.2:** Retry with Suggested Adjustments
  * Description: [To be filled]
  * Impact Weighting: Success Rate / Learning / User Guidance
  * Priority: Medium
  * User Stories: US3.3.2
  * Tasks: [T-3.3.2]
  * User Story Acceptance Criteria:
    - For specific error types, offer "Retry with Suggested Fix" button
    - **OOM Error Suggestions**:
    - Reduce batch_size: 4 → 2
    - Switch to Conservative preset
    - Highlight changes: "batch_size: 4 ~~→~~ **2**"
    - **Timeout Error Suggestions**:
    - Reduce epochs: 4 → 3
    - Switch to Balanced preset
    - Increase checkpoint frequency
    - **Spot Interruption Loop Suggestions** (if interrupted >3 times):
    - Switch to on-demand instance
    - Accept higher cost for reliability
    - Confirmation modal shows diff of configuration changes
    - User can accept suggested fixes or manually edit
    - After retry with suggestions:
    - Track success rate of suggested fixes
    - Learn from patterns to improve future suggestions
    - Example: "Your previous job failed with OOM error. Retry with batch_size=2 (suggested) for 95% success rate?"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

## 4. Model Artifacts & Downloads

- **FR4.1.1:** Download Trained LoRA Adapters
  * Description: [To be filled]
  * Impact Weighting: Productivity / Time-to-Value / Ease of Use
  * Priority: High
  * User Stories: US4.1.1
  * Tasks: [T-4.1.1]
  * User Story Acceptance Criteria:
    - Completed jobs show "Download Adapters" button (prominent, green)
    - Click initiates ZIP file download: `{job_name}-adapters-{job_id}.zip`
    - ZIP contains:
    - `adapter_model.bin` (200-500MB): Trained LoRA weight matrices
    - `adapter_config.json`: Configuration file (rank, alpha, target_modules, etc.)
    - `README.txt`: Quick integration instructions
    - `training_summary.json`: Final metrics (loss, perplexity, duration, cost)
    - Download progress indicator for large files
    - Generate signed URL valid for 24 hours (security)
    - After 24 hours: Regenerate download link
    - Track download count and timestamp for audit trail
    - Notification after download: "Adapters downloaded. See README.txt for integration instructions."
    - Example README content:
      ```
      Bright Run LoRA Adapters - Training Job: {job_name}
      
      Files:
      - adapter_model.bin: Trained weight matrices
      - adapter_config.json: LoRA configuration
      
      Integration:
      1. Install dependencies: pip install transformers peft torch
      2. Load base model: Llama 3 70B
      3. Load adapters: model = PeftModel.from_pretrained(base_model, adapter_path)
      4. Run inference: See example_inference.py
      
      Support: docs.brightrun.ai/lora-adapters
      ```
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR4.1.2:** Adapter Storage and Versioning
  * Description: [To be filled]
  * Impact Weighting: Data Management / Version Control / Recovery
  * Priority: Medium
  * User Stories: US4.1.2
  * Tasks: [T-4.1.2]
  * User Story Acceptance Criteria:
    - All adapter files stored in Supabase Storage bucket: `model-artifacts`
    - Folder structure: `{job_id}/adapters/`
    - Files: `adapter_model.bin`, `adapter_config.json`, `training_summary.json`
    - Storage retention: Permanent by default (configurable)
    - Versioning: Each training job creates unique version
    - Job details page shows:
    - Storage path
    - File sizes
    - Upload timestamp
    - Download count
    - Option to delete adapters (free up storage): Requires confirmation, creates audit log entry
    - Storage usage dashboard:
    - Total storage used: 15.3 GB
    - Number of stored models: 23
    - Average model size: 665 MB
    - Storage cost estimate (if applicable)
    - Bulk operations: Delete multiple old adapters to free storage
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR4.2.1:** Export Training Metrics as CSV/JSON
  * Description: [To be filled]
  * Impact Weighting: Reporting / Analysis / Quality Assurance
  * Priority: Medium
  * User Stories: US4.2.1
  * Tasks: [T-4.2.1]
  * User Story Acceptance Criteria:
    - "Export Metrics" button on job details page
    - Format options: CSV (spreadsheet analysis) / JSON (programmatic access)
    - **CSV Export** includes columns:
    - step_number, epoch, training_loss, validation_loss, learning_rate, perplexity, gpu_utilization, timestamp, elapsed_time_seconds
    - **JSON Export** includes nested structure:
      ```json
      {
        "job_metadata": { "job_id": "...", "name": "...", "configuration": {...} },
        "training_metrics": [
          { "step": 100, "epoch": 1, "training_loss": 0.521, "validation_loss": 0.538, ... },
          { "step": 200, "epoch": 1, "training_loss": 0.489, "validation_loss": 0.502, ... }
        ],
        "final_metrics": { "final_training_loss": 0.287, "final_validation_loss": 0.312, "perplexity_improvement": "31%" }
      }
      ```
    - Export includes all historical data from training start to completion
    - File naming: `{job_name}-metrics-{timestamp}.{csv|json}`
    - One-click download, no generation delay
    - Option to include charts (loss curves) as embedded PNG in export package
    - Track export count for audit trail
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR4.2.2:** Generate Training Report PDF
  * Description: [To be filled]
  * Impact Weighting: Client Communication / Professionalism / Sales Enablement
  * Priority: Low
  * User Stories: US4.2.2
  * Tasks: [T-4.2.2]
  * User Story Acceptance Criteria:
    - "Generate Report" button on completed job details page
    - PDF report includes:
    - **Cover Page**: Job name, training date, Bright Run branding
    - **Executive Summary** (1 page):
    - Training file: 242 conversations, quality scores
    - Configuration: Balanced preset, H100 spot instance
    - Duration: 13.2 hours
    - Final training loss: 0.287 (baseline: 1.423) - **80% improvement**
    - Cost: $48.32
    - Status: Completed successfully
    - **Training Metrics** (2 pages):
    - Loss curves graph (training + validation)
    - Learning rate schedule graph
    - Metrics table: Final loss, perplexity, GPU utilization
    - Convergence analysis: "Loss plateaued at epoch 2.5, indicating optimal training completion"
    - **Cost Breakdown** (1 page):
    - GPU cost: $33.12 (spot H100, 13.2 hours @ $2.49/hr)
    - Spot interruptions: 2 (recovery overhead: $1.20)
    - Storage costs: $0.15
    - Total cost: $48.32
    - Cost efficiency: "68% cheaper than on-demand ($146 estimate)"
    - **Appendix**:
    - Full configuration details
    - Checkpoint history
    - Event log summary
    - Report generation takes 5-10 seconds
    - Preview report before download
    - File naming: `{job_name}-training-report-{timestamp}.pdf`
    - Shareable via secure link (30-day expiration)
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR4.3.1:** Create Complete Deployment Package
  * Description: [To be filled]
  * Impact Weighting: Client Success / Integration Speed / Support Reduction
  * Priority: Medium
  * User Stories: US4.3.1
  * Tasks: [T-4.3.1]
  * User Story Acceptance Criteria:
    - "Download Deployment Package" button on completed jobs
    - ZIP file: `{job_name}-deployment-package-{job_id}.zip`
    - **Package contents**:
      1. `adapters/` folder:
         - adapter_model.bin
         - adapter_config.json
      2. `inference.py`:
         - Runnable Python script loading base model + adapters
         - Accepts prompt as CLI argument
         - Outputs model response
         - Configurable temperature, max_tokens
      3. `requirements.txt`:
         - Exact Python dependencies with versions
         - transformers==4.36.0, peft==0.7.1, torch==2.1.2, accelerate==0.25.0
      4. `README.md`:
         - Setup instructions (create venv, install deps)
         - Usage examples (run inference.py)
         - Deployment options (local, cloud, API endpoint)
         - Troubleshooting common issues
         - Support contact info
      5. `example_prompts.json`:
         - 10 sample prompts matching training domain (financial advisory)
         - Expected response quality examples
      6. `training_summary.json`:
         - Job metadata, configuration, final metrics
    - Inference script works with: `pip install -r requirements.txt && python inference.py "What are the benefits of a Roth IRA?"`
    - README includes GPU requirements, VRAM usage, inference speed estimates
    - Package size: ~500-700MB
    - Generate signed URL, valid 48 hours
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR4.3.2:** API Inference Endpoint Template
  * Description: [To be filled]
  * Impact Weighting: Client Success / Integration Speed / Developer Experience
  * Priority: Low (Future Enhancement)
  * User Stories: US4.3.2
  * Tasks: [T-4.3.2]
  * User Story Acceptance Criteria:
    - Deployment package includes `api_server/` folder:
    - `app.py`: FastAPI application serving inference endpoint
    - `Dockerfile`: Container image for deployment
    - `docker-compose.yml`: Local testing setup
    - `deploy_guide.md`: Deployment instructions (Docker, Kubernetes, cloud platforms)
    - API endpoints:
    - `POST /api/v1/chat`: Send prompt, receive model response
    - `GET /api/v1/health`: Health check endpoint
    - `GET /api/v1/model-info`: Model metadata (training job, version, metrics)
    - API features:
    - Request validation (max prompt length, rate limiting)
    - Response streaming (SSE)
    - Authentication (API key)
    - Logging (request/response tracking)
    - Docker image size: <5GB
    - Startup time: <60 seconds (model loading)
    - Inference latency: <2 seconds per response
    - Deployment guide covers:
    - Local testing: `docker-compose up`
    - Cloud deployment: AWS ECS, GCP Cloud Run, Azure Container Instances
    - GPU support: Specify GPU requirements, optimize for A10G/A100/H100
    - Example API request:
      ```bash
      curl -X POST http://localhost:8000/api/v1/chat \
        -H "Authorization: Bearer <api_key>" \
        -H "Content-Type: application/json" \
        -d '{"prompt": "Explain asset allocation", "max_tokens": 500}'
      ```
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

## 5. Training Comparison & Optimization

- **FR5.1.1:** Compare Multiple Training Runs
  * Description: [To be filled]
  * Impact Weighting: Optimization / Data-Driven Decisions / Quality Improvement
  * Priority: Medium
  * User Stories: US5.1.1
  * Tasks: [T-5.1.1]
  * User Story Acceptance Criteria:
    - "Compare Jobs" button on training jobs list page
    - Multi-select mode: Checkboxes appear on each job row
    - Select 2-4 jobs → "Compare Selected" button enabled
    - Comparison view opens in new page or modal
    - **Overlaid Loss Curves Graph**:
    - All selected jobs' loss curves on same chart
    - Color-coded by job (blue, green, red, orange)
    - Legend showing job names
    - Toggle training/validation loss visibility
    - Zoom and pan controls
    - Highlight final loss values
    - **Metrics Comparison Table**:
    - Rows: Job 1, Job 2, Job 3, Job 4
    - Columns: Final Training Loss, Final Validation Loss, Perplexity, Duration, Cost, GPU Type, Preset
    - Highlight best value in each column (green background)
    - Percentage differences: "Job 2: 15% lower loss than Job 1"
    - **Configuration Comparison**:
    - Side-by-side hyperparameters
    - Highlight differences: "Job 1: r=16, Job 2: r=32"
    - Training file, GPU type, spot/on-demand
    - **Winner Recommendation**:
    - Algorithm identifies best job based on: lowest validation loss, cost efficiency, duration
    - Display: "Recommended: Job 2 (Balanced preset) - Best quality/cost ratio"
    - Export comparison as PDF report
    - Save comparison as preset template
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR5.1.2:** Configuration Performance Analytics
  * Description: [To be filled]
  * Impact Weighting: Continuous Improvement / Cost Optimization / Knowledge Building
  * Priority: Low
  * User Stories: US5.1.2
  * Tasks: [T-5.1.2]
  * User Story Acceptance Criteria:
    - "Training Analytics" dashboard accessible from main navigation
    - **Performance by Preset**:
    - Table: Conservative, Balanced, Aggressive
    - Metrics: Average final loss, Average cost, Average duration, Success rate, Total jobs
    - Best performer highlighted
    - Example: "Balanced preset: 96% success rate, $52 avg cost, 0.312 avg final loss"
    - **Cost vs Quality Scatter Plot**:
    - X-axis: Final validation loss (lower = better quality)
    - Y-axis: Total cost (lower = cheaper)
    - Each dot = training job (color by preset)
    - Ideal zone: Lower-left (low cost, high quality)
    - Outliers highlighted for investigation
    - **Success Rate Trends**:
    - Line chart: Success rate over time (monthly)
    - Track improvements as presets optimized
    - Goal: Increase success rate from 92% → 98%
    - **Common Failure Patterns**:
    - Most frequent error types
    - Configurations with highest failure rate
    - Recommendations: "Avoid r=64 with batch_size=4 (85% OOM rate)"
    - **GPU Utilization Analysis**:
    - Spot vs on-demand usage percentage
    - Spot interruption rates by time of day
    - Cost savings from spot usage
    - Export analytics as CSV for further analysis
    - Update default presets quarterly based on data
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR5.2.1:** Comprehensive Training History
  * Description: [To be filled]
  * Impact Weighting: Team Coordination / Audit Compliance / Knowledge Sharing
  * Priority: Medium
  * User Stories: US5.2.1
  * Tasks: [T-5.2.1]
  * User Story Acceptance Criteria:
    - "Training History" page with comprehensive filters:
    - Date range: Last 7 days / 30 days / 90 days / All time / Custom
    - Creator: All / [User dropdown] / Me only
    - Status: All / Completed / Failed / Cancelled
    - Configuration: All presets / Conservative / Balanced / Aggressive
    - Cost range: <$50 / $50-100 / $100-200 / >$200
    - GPU type: All / Spot / On-Demand
    - Training file: All / [Training file dropdown]
    - Tags: Filter by job tags (experiment, production, etc.)
    - Sort options: Date (newest/oldest), Cost (high/low), Duration (long/short), Quality (best/worst)
    - Search: By job name, notes, tags, training file name
    - Results display: Paginated table (25/50/100 per page)
    - Export filtered results as CSV
    - Statistics panel:
    - Total jobs: 47
    - Success rate: 94%
    - Total cost: $2,348
    - Total training time: 623 hours
    - Average cost per job: $49.96
    - Historical trends:
    - Jobs per month (bar chart)
    - Cost per month (line chart)
    - Success rate trend (line chart)
    - Team activity:
    - Jobs per team member
    - Average cost per team member
    - Success rate per team member
    - Click any row opens job details page
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR5.2.2:** Configuration Templates Library
  * Description: [To be filled]
  * Impact Weighting: Team Efficiency / Knowledge Preservation / Best Practices Sharing
  * Priority: Low
  * User Stories: US5.2.2
  * Tasks: [T-5.2.2]
  * User Story Acceptance Criteria:
    - "Save as Template" button on completed jobs (success rate >90%)
    - Template creation modal:
    - Template name (required): "Production Financial Advisory - High Quality"
    - Description (optional): "Best configuration for 200+ conversation datasets with emotional intelligence focus"
    - Include: Hyperparameters, GPU selection, checkpoint frequency
    - Visibility: Private (my templates) / Team (shared across workspace)
    - Tags: production, financial, high-quality, balanced
    - Template library page:
    - Grid or list view of saved templates
    - Filter by: Creator, Tags, Visibility
    - Sort by: Name, Created date, Usage count
    - Template cards show: Name, Description, Configuration summary, Usage count, Success rate, Average cost
    - "Start from Template" button:
    - Opens job creation form pre-filled with template configuration
    - All fields editable before starting
    - Job notes automatically include: "Started from template: {template_name}"
    - Template analytics:
    - Usage count: How many jobs created from this template
    - Success rate: Percentage of jobs that completed successfully
    - Average metrics: Cost, duration, final loss
    - Edit template: Update description, tags, visibility
    - Delete template: Requires confirmation, doesn't affect jobs created from template
    - Default templates provided:
    - "Quick Test" (Conservative, 1 epoch, minimal cost)
    - "Standard Production" (Balanced, 3 epochs, proven quality)
    - "Maximum Quality" (Aggressive, 4 epochs, highest quality)
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

## 6. Model Quality Validation

- **FR6.1.1:** Calculate Perplexity Improvement
  * Description: [To be filled]
  * Impact Weighting: Quality Assurance / Objective Measurement / Client Proof
  * Priority: High
  * User Stories: US6.1.1
  * Tasks: [T-6.1.1]
  * User Story Acceptance Criteria:
    - **Automatic Perplexity Calculation** (runs during training finalization):
    - Test baseline Llama 3 70B on validation set (20% held-out data, ~48 conversations)
    - Test trained model (base + LoRA adapters) on same validation set
    - Calculate perplexity for both models
    - Compute improvement percentage: ((baseline - trained) / baseline) × 100%
    - **Results Display** on job details page:
    - Baseline perplexity: 24.5 (Llama 3 70B without fine-tuning)
    - Trained perplexity: 16.8 (Llama 3 70B + LoRA adapters)
    - Improvement: **31.4%** (green badge if ≥30%, yellow if 20-29%, red if <20%)
    - Interpretation: "31% lower perplexity indicates significantly better prediction quality"
    - **Target Threshold**:
    - Production-ready: ≥30% improvement
    - Acceptable: 20-29% improvement
    - Needs retry: <20% improvement
    - **Quality Badge**:
    - "✓ Production Ready" (≥30% improvement)
    - "⚠ Acceptable Quality" (20-29% improvement)
    - "✗ Below Threshold" (<20% improvement)
    - Include perplexity chart: Bar chart comparing baseline vs trained
    - Export perplexity data with validation report
    - Perplexity trend: Track across multiple training runs to identify improvements
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.1.2:** Perplexity by Category Analysis
  * Description: [To be filled]
  * Impact Weighting: Quality Insights / Data-Driven Iteration / Targeted Improvement
  * Priority: Medium
  * User Stories: US6.1.2
  * Tasks: [T-6.1.2]
  * User Story Acceptance Criteria:
    - **Perplexity by Persona**:
    - Table: Persona, Baseline Perplexity, Trained Perplexity, Improvement %
    - Example: "Anxious Investor: 26.3 → 15.2 (42% improvement)"
    - Highlight personas with best/worst improvement
    - **Perplexity by Emotional Arc**:
    - Triumph arc: 23.1 → 15.8 (32% improvement)
    - Struggle-to-Success: 25.7 → 17.2 (33% improvement)
    - Identify arcs needing more training coverage
    - **Perplexity by Training Topic**:
    - Retirement Planning: 22.5 → 14.9 (34% improvement)
    - Tax Strategies: 28.3 → 19.1 (32% improvement)
    - Identify topics with lower improvement (need more training data)
    - **Visual Heatmap**:
    - Persona (rows) × Emotional Arc (columns)
    - Cell color: Green (high improvement), Yellow (medium), Red (low)
    - Quick identification of weak areas
    - **Recommendations**:
    - "Add 10+ more 'Pragmatic Skeptic + Anxiety' conversations for better coverage"
    - "Tax Strategies topic shows lower improvement - consider adding specialized training data"
    - Export detailed category analysis as CSV
    - Use insights to improve future training datasets
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.2.1:** Run Emotional Intelligence Benchmarks
  * Description: [To be filled]
  * Impact Weighting: Client Proof / Quality Assurance / Sales Enablement
  * Priority: High
  * User Stories: US6.2.1
  * Tasks: [T-6.2.1]
  * User Story Acceptance Criteria:
    - **Test Suite**: Curated set of 50 emotional intelligence scenarios
    - Categories: Empathy detection (15 scenarios), Emotional awareness (15), Supportive responses (10), Conflict handling (10)
    - Difficulty levels: Easy (20), Medium (20), Hard (10)
    - Cover personas: Anxious Investor, Pragmatic Skeptic, Hopeful Planner, etc.
    - **Validation Process**:
    - Run baseline Llama 3 70B on all 50 scenarios
    - Run trained model on same 50 scenarios
    - Capture responses for side-by-side comparison
    - **Human Evaluation** (or automated LLM-as-judge):
    - Score each response 1-5 on:
    - Empathy: Recognizes and validates emotions
    - Clarity: Clear, understandable explanations
    - Appropriateness: Tone matches situation
    - Calculate aggregate scores: Baseline avg vs Trained avg
    - **Results Display**:
    - Overall Emotional Intelligence Score: 3.2/5 (baseline) → 4.5/5 (trained) = **41% improvement**
    - Empathy subscore: 3.1 → 4.6 (48% improvement)
    - Clarity subscore: 3.4 → 4.5 (32% improvement)
    - Appropriateness subscore: 3.1 → 4.4 (42% improvement)
    - **Before/After Examples**:
    - Display 10 best improvements
    - Scenario prompt, baseline response, trained response, improvement notes
    - Example: "Scenario: Client anxious about market volatility. Baseline response: Generic advice. Trained response: Empathetic acknowledgment + specific reassurance + action plan."
    - **Quality Badge**:
    - "✓ Exceptional EI" (≥40% improvement)
    - "✓ Strong EI" (30-39% improvement)
    - "⚠ Moderate EI" (20-29% improvement)
    - "✗ Needs Improvement" (<20% improvement)
    - Include EI validation in training completion report
    - Export full evaluation results (all 50 scenarios) as CSV
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.2.2:** Emotional Intelligence Regression Detection
  * Description: [To be filled]
  * Impact Weighting: Quality Assurance / Risk Mitigation / Client Protection
  * Priority: Medium
  * User Stories: US6.2.2
  * Tasks: [T-6.2.2]
  * User Story Acceptance Criteria:
    - Regression detection: Identify scenarios where trained_score < baseline_score
    - **Regression Report**:
    - Number of regressions: 3 of 50 scenarios (6%)
    - List affected scenarios with details
    - Example: "Scenario #23: Baseline 4.2/5, Trained 3.8/5 (-10% regression)"
    - **Root Cause Analysis**:
    - Identify patterns: Which personas? Which emotional arcs? Which topics?
    - Example: "2 of 3 regressions involve 'Pragmatic Skeptic' persona - may need more training data"
    - **Severity Classification**:
    - Minor regression: <10% decrease, overall score still ≥4/5
    - Moderate regression: 10-20% decrease, score drops below 4/5
    - Major regression: >20% decrease, score drops below 3/5
    - **Quality Gate**:
    - Allow delivery if: <10% scenarios show regression, no major regressions
    - Block delivery if: ≥10% scenarios show regression or any major regression
    - Warning: "3 minor regressions detected. Review before client delivery."
    - **Corrective Actions**:
    - Add more training data for affected scenarios
    - Adjust hyperparameters (reduce learning rate, increase regularization)
    - Retry training with different configuration
    - Include regression analysis in validation report
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.3.1:** Financial Knowledge Retention Test
  * Description: [To be filled]
  * Impact Weighting: Quality Assurance / Risk Mitigation / Client Trust
  * Priority: Medium
  * User Stories: US6.3.1
  * Tasks: [T-6.3.1]
  * User Story Acceptance Criteria:
    - **Test Suite**: 100 financial knowledge questions
    - Categories: Taxes (25), Retirement planning (25), Investing (25), Insurance (25)
    - Difficulty: Basic (40), Intermediate (40), Advanced (20)
    - Multiple choice format (A/B/C/D) for objective grading
    - **Validation Process**:
    - Run baseline Llama 3 70B on all 100 questions
    - Run trained model on same 100 questions
    - Compare accuracy: Correct answers / Total questions
    - **Results Display**:
    - Baseline accuracy: 87% (87/100 correct)
    - Trained accuracy: 85% (85/100 correct)
    - Retention rate: **98%** (85/87 = 97.7%, rounds to 98%)
    - Verdict: "✓ Passed" (≥95% retention threshold)
    - **Acceptable Thresholds**:
    - ✓ Passed: ≥95% retention (trained accuracy ≥ 95% of baseline)
    - ⚠ Warning: 90-94% retention (minor knowledge loss)
    - ✗ Failed: <90% retention (catastrophic forgetting detected)
    - **Failed Questions Analysis**:
    - If retention <95%, list questions where trained model failed but baseline passed
    - Identify knowledge gaps: "5 retirement planning questions regressed"
    - Recommendations: "Retrain with lower learning rate to prevent overfitting"
    - **Quality Gate**:
    - Block delivery if retention <90%
    - Require review if retention 90-94%
    - Auto-approve if retention ≥95%
    - Include retention test results in validation report
    - Export detailed question-by-question results as CSV
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.3.2:** Domain-Specific Knowledge Probes
  * Description: [To be filled]
  * Impact Weighting: Quality Assurance / Compliance / Business-Specific Validation
  * Priority: Low (Future Enhancement - Client-Specific)
  * User Stories: US6.3.2
  * Tasks: [T-6.3.2]
  * User Story Acceptance Criteria:
    - **Custom Test Suite**: Client-provided domain knowledge questions (50-100)
    - Financial regulations (SEC, FINRA rules)
    - Product-specific knowledge (401k vs Roth IRA differences)
    - Compliance requirements (disclosure language)
    - Allow clients to upload custom test suite (CSV or JSON format)
    - Run baseline vs trained model comparison
    - Report retention rate for domain-specific knowledge
    - Flag any regressions in critical knowledge areas
    - Example: "Compliance knowledge: 92% retention (acceptable threshold: 100% for regulatory content)"
    - If compliance knowledge drops <100%: Block delivery, require retraining
    - Use case: Ensure AI doesn't give incorrect tax advice or violate regulations after training
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.4.1:** Elena Morales Voice Consistency Scoring
  * Description: [To be filled]
  * Impact Weighting: Brand Alignment / Client Satisfaction / Quality Differentiation
  * Priority: Medium
  * User Stories: US6.4.1
  * Tasks: [T-6.4.1]
  * User Story Acceptance Criteria:
    - **Elena Morales Voice Rubric** (10 characteristics, each scored 1-5):
      1. Warmth & Empathy: Genuine emotional connection
      2. Directness & Clarity: Avoids jargon, gets to the point
      3. Education-First Approach: Explains "why" behind advice
      4. Pragmatic Optimism: Realistic yet hopeful tone
      5. Question-Driven: Asks clarifying questions
      6. Storytelling: Uses relatable examples
      7. Action-Oriented: Provides concrete next steps
      8. Patience: Never rushes or dismisses concerns
      9. Humor (appropriate): Light touches when suitable
      10. Confidence: Authoritative yet humble
    - **Evaluation Process**:
    - Generate 30 responses from trained model (diverse scenarios)
    - Human evaluators score each response on 10 characteristics
    - Calculate average score per characteristic
    - Calculate overall voice consistency: Average of 10 characteristic scores
    - **Results Display**:
    - Overall voice consistency: 4.3/5 (**86% alignment**, target ≥85%)
    - Per-characteristic breakdown:
    - Warmth & Empathy: 4.5/5 (excellent)
    - Directness: 4.2/5 (strong)
    - Education-First: 4.1/5 (good)
    - Pragmatic Optimism: 4.6/5 (excellent)
    - ... (remaining characteristics)
    - Flag characteristics scoring <3/5: "Humor: 2.8/5 (needs improvement)"
    - **Quality Badge**:
    - "✓ Excellent Brand Alignment" (≥4.5/5, 90%+)
    - "✓ Strong Brand Alignment" (≥4.25/5, 85-89%)
    - "⚠ Acceptable Alignment" (≥4.0/5, 80-84%)
    - "✗ Needs Improvement" (<4.0/5, <80%)
    - **Before/After Examples**:
    - Show 5 responses demonstrating brand voice improvement
    - Baseline: Generic financial advice
    - Trained: Elena Morales style (warm, educational, action-oriented)
    - Include voice consistency report in validation PDF
    - Export detailed scoring (30 responses × 10 characteristics) as CSV
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR6.4.2:** Client Brand Customization (Future)
  * Description: [To be filled]
  * Impact Weighting: Client Customization / Brand Protection / Competitive Differentiation
  * Priority: Low (Future Enhancement - Premium Feature)
  * User Stories: US6.4.2
  * Tasks: [T-6.4.2]
  * User Story Acceptance Criteria:
    - Allow clients to define custom brand voice rubric (5-15 characteristics)
    - Client provides characteristic descriptions and scoring criteria
    - Example custom characteristics: "Conservative tone", "Risk-aware language", "Formal communication style"
    - Run evaluation using client's rubric
    - Generate brand alignment report customized to client's brand
    - Use case: Financial firm with formal, conservative brand (different from Elena Morales' warm, approachable style)
    - Enables: Bright Run to serve diverse clients with different brand personalities
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

## 7. Cost Management & Budget Control

- **FR7.1.1:** Live Cost Accumulation Display
  * Description: [To be filled]
  * Impact Weighting: Cost Control / Budget Awareness / User Empowerment
  * Priority: High
  * User Stories: US7.1.1
  * Tasks: [T-7.1.1]
  * User Story Acceptance Criteria:
    - **Cost Tracker Card** on job dashboard (prominent, top-right):
    - Estimated cost: $45-55
    - Current spend: $22.18 (49% of estimate)
    - Hourly rate: $2.49/hr (spot)
    - Elapsed time: 6h 23m
    - Projected final cost: $47.32 (within estimate)
    - **Update frequency**: Every 60 seconds (real-time polling or websocket)
    - **Cost calculation**: (elapsed_time_hours × gpu_hourly_rate) + spot_interruption_overhead
    - **Visual indicators**:
    - Green: Current spend <80% of estimate
    - Yellow: Current spend 80-100% of estimate
    - Red: Current spend >100% of estimate (over budget)
    - **Warning alerts**:
    - At 80% of estimate: "Job approaching cost estimate ($36 of $45). Monitor closely."
    - At 100% of estimate: "Job exceeded cost estimate ($46 of $45). Consider cancelling."
    - At 120% of estimate: "Job significantly over budget ($54 of $45). Review immediately."
    - **Cancel option**: "Cancel Job" button readily accessible if cost is concerning
    - **Cost breakdown**:
    - GPU compute: $21.00 (8.4 hrs @ $2.49/hr)
    - Spot interruption overhead: $1.18 (2 interruptions)
    - Storage (checkpoints): $0.00 (included)
    - Total: $22.18
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR7.1.2:** Cost vs Time Remaining Projection
  * Description: [To be filled]
  * Impact Weighting: Budget Planning / Informed Decision-Making / Cost Control
  * Priority: Medium
  * User Stories: US7.1.2
  * Tasks: [T-7.1.2]
  * User Story Acceptance Criteria:
    - **Projection Algorithm**:
    - Calculate average time per step based on completed steps
    - Estimate remaining time: (remaining_steps × avg_time_per_step)
    - Project final cost: current_cost + (remaining_time × hourly_rate)
    - **Projection Display**:
    - "At current rate, job will complete in 8.2 hours"
    - "Projected final cost: $47.32 (±15% variance)"
    - "Expected completion: Today at 11:45 PM"
    - **Scenario Analysis**:
    - Best case: Training accelerates in later epochs (GPU optimization)
    - Expected case: Current rate continues
    - Worst case: Training slows down (loss plateau, more validation runs)
    - **Decision Support**:
    - If projected cost >120% of estimate: "Consider cancelling and retrying with more efficient configuration"
    - If projected cost within estimate: "On track, continue monitoring"
    - **Historical Accuracy**:
    - Track actual vs projected cost for completed jobs
    - Display accuracy metric: "Projections typically ±12% accurate"
    - Improve projection algorithm over time based on historical data
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR7.2.1:** Monthly Budget Dashboard
  * Description: [To be filled]
  * Impact Weighting: Financial Planning / Budget Compliance / Operational Oversight
  * Priority: High
  * User Stories: US7.2.1
  * Tasks: [T-7.2.1]
  * User Story Acceptance Criteria:
    - **Budget Dashboard** page at `/dashboard/training-budget`
    - **Summary Cards** (top of page):
    - **Monthly Spending**: $487.32 / $500.00 (97% used)
    - **Remaining Budget**: $12.68
    - **Jobs This Month**: 12 (10 completed, 2 active)
    - **Average Cost per Job**: $40.61
    - **Spending Trend Graph**:
    - Line chart: Daily spending accumulation over current month
    - Budget limit line: Horizontal line at $500
    - Projected spending: Dotted line showing forecast
    - Alert zone: Red shading when approaching/exceeding limit
    - **Per-Job Breakdown Table**:
    - Job Name, Status, Cost, Percentage of Budget, Date
    - Sort by cost (highest first)
    - Identify expensive jobs: "Job XYZ: $87 (17% of monthly budget)"
    - **Budget vs Forecast**:
    - Current spend: $487.32
    - Active jobs (in progress): $42-58 (2 jobs)
    - Forecasted month-end spend: $529-545
    - Warning: "Projected to exceed budget by $29-45"
    - **Budget Controls**:
    - Set monthly budget limit: $500 (default), customizable
    - Budget period: Calendar month or rolling 30 days
    - Budget alerts: Email/Slack at 80%, 95%, 100%
    - Block new jobs: Toggle to prevent jobs when budget exceeded
    - **Historical Comparison**:
    - Last 6 months spending: Bar chart
    - Average monthly spend: $423
    - Trend: Increasing (as team scales training usage)
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR7.2.2:** Budget Alerts & Notifications
  * Description: [To be filled]
  * Impact Weighting: Proactive Management / Risk Mitigation / Communication
  * Priority: High
  * User Stories: US7.2.2, US8.2.2
  * Tasks: [T-7.2.2], [T-8.2.2]
  * User Story Acceptance Criteria:
    - **Alert Triggers**:
    - 80% threshold: "You've used 80% of monthly training budget ($400 of $500)"
    - 95% threshold: "You've used 95% of monthly training budget ($475 of $500)"
    - 100% threshold: "Monthly training budget exceeded ($505 of $500)"
    - Budget exceeded during active job: "Active job may exceed budget. Cancel or increase limit."
    - **Alert Channels**:
    - Email: Sent to budget manager and finance stakeholders
    - Slack (optional): Posted to designated channel (#training-budget)
    - In-app notification: Banner on dashboard
    - **Alert Content**:
    - Current spending: $487.32 / $500.00 (97%)
    - Remaining budget: $12.68
    - Active jobs: 2 (estimated remaining cost: $42-58)
    - Forecast: Likely to exceed budget by $29-45
    - Actions: [Increase Budget Limit] [Cancel Active Jobs] [View Budget Dashboard]
    - **Increase Budget Limit**:
    - Click "Increase Budget Limit" button in alert email
    - Opens form: New limit, Justification (required), Approval (if required)
    - Submit request: Pending approval or immediately applied (based on permissions)
    - Notification: "Budget limit increased from $500 to $750"
    - **Budget Override Log**:
    - Audit trail of all budget limit changes
    - Who changed it, when, why (justification), old limit, new limit
    - Export log for financial reporting
    - **Notification Recipients** (from US8.2.2):
    - Configurable recipients: budget manager, finance team, operations
    - **Escalation Levels** (from US8.2.2):
    - 80% alert → email only
    - 95% alert → email + Slack
    - 100% alert → email + Slack + in-app banner
    - **Daily Digest Option** (from US8.2.2):
    - "Your daily training budget summary" (total spent today, remaining budget, active jobs)
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR7.3.1:** Spot vs On-Demand Cost Analysis
  * Description: [To be filled]
  * Impact Weighting: Cost Efficiency / ROI Demonstration / Strategic Planning
  * Priority: Medium
  * User Stories: US7.3.1
  * Tasks: [T-7.3.1]
  * User Story Acceptance Criteria:
    - **Cost Optimization Report** on budget dashboard
    - **Spot Instance Savings**:
    - Total spot cost: $387.32
    - Equivalent on-demand cost: $1,243.18
    - Total savings: $855.86 (69% cheaper)
    - **Per-Job Comparison**:
    - Table: Job Name, Spot Cost, Equivalent On-Demand Cost, Savings, Interruptions
    - Example: "Job ABC: $48 (spot) vs $146 (on-demand) = $98 saved, 2 interruptions"
    - **Interruption Impact**:
    - Total spot interruptions: 23 (across 12 jobs)
    - Average interruptions per job: 1.9
    - Interruption cost overhead: $28.42 (checkpoint recovery time)
    - Net savings after overhead: $827.44
    - **ROI Calculation**:
    - Monthly spot savings: $855.86
    - Annualized savings: $10,270 (if usage remains constant)
    - Justifies investment in training infrastructure
    - **Recommendation**:
    - "Continue using spot instances for 90%+ of jobs"
    - "Reserve on-demand for urgent client deliveries"
    - "Current strategy saves $10k+ annually"
    - Export cost optimization report as PDF for stakeholders
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR7.3.2:** Cost Attribution by Client/Project
  * Description: [To be filled]
  * Impact Weighting: Financial Planning / Profitability Analysis / Pricing Strategy
  * Priority: Medium
  * User Stories: US7.3.2
  * Tasks: [T-7.3.2]
  * User Story Acceptance Criteria:
    - **Client/Project Tagging**:
    - When creating training job, optionally assign to client or project
    - Dropdown: Existing clients/projects or create new
    - Example: "Client: Acme Financial Advisors", "Project: Q1 2025 AI Enhancement"
    - **Cost Attribution Report**:
    - Table: Client/Project, Total Jobs, Total Cost, Average Cost per Job, Date Range
    - Example: "Acme Financial: 5 jobs, $287.32, $57.46 avg, Jan-Mar 2025"
    - **Project Profitability**:
    - For each project, show: Revenue, Training Cost, Other Costs, Profit, Margin %
    - Example: "Acme Financial Q1 Project: $25k revenue, $287 training, $2k other, $22.7k profit (91% margin)"
    - **Pricing Insights**:
    - Average training cost per client: $52
    - Recommended pricing: $15k-30k (287-577x training cost)
    - Current margin: 91-97% depending on pricing tier
    - **Budget Allocation**:
    - Allocate monthly budget by client priority: "$200 for Priority A clients, $150 for Priority B, $150 for experiments"
    - Export cost attribution as CSV for accounting/finance teams
    - Use case: Finance team calculates true project costs for profitability analysis
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

## 8. Team Collaboration & Notifications

- **FR8.1.1:** Job Creator Attribution
  * Description: [To be filled]
  * Impact Weighting: Team Coordination / Accountability / Knowledge Sharing
  * Priority: Medium
  * User Stories: US8.1.1
  * Tasks: [T-8.1.1]
  * User Story Acceptance Criteria:
    - All training jobs automatically tagged with creator (current user)
    - Job list displays "Created By" column with user name and avatar
    - Filter jobs by creator: "Show only my jobs" / "Show all team jobs" / "Show [specific user] jobs"
    - Job details page prominently displays creator info:
    - Created by: John Smith (john@brightrun.ai)
    - Created on: 2025-12-15 14:23 PST
    - Notes: "Testing aggressive LR for high-emotion dataset"
    - Team activity dashboard:
    - Jobs created per team member (current month)
    - Average success rate per team member
    - Average cost per team member
    - Leaderboard: Most productive team member, most cost-efficient, highest quality
    - Use cases:
    - Coordination: "John is already training this dataset, I'll work on another"
    - Learning: "Sarah's jobs have 98% success rate, let me see her configurations"
    - Accountability: "Who started this expensive job?"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR8.1.2:** Job Sharing & Collaboration
  * Description: [To be filled]
  * Impact Weighting: Knowledge Sharing / Team Learning / Collaboration
  * Priority: Low
  * User Stories: US8.1.2
  * Tasks: [T-8.1.2]
  * User Story Acceptance Criteria:
    - "Share Job" button on job details page
    - Generate shareable link: `https://app.brightrun.ai/training-jobs/{job_id}`
    - Link options:
    - Public (anyone with link can view, no authentication)
    - Team (only team members can view)
    - Private (default, only creator can view)
    - Share via:
    - Copy link to clipboard
    - Email (send link directly)
    - Slack (post to channel)
    - Shared job view shows:
    - Full configuration details
    - Progress (if active)
    - Results (if completed)
    - Creator attribution
    - Option to "Clone Configuration" (start new job with same settings)
    - Use cases:
    - "Hey Sarah, check out this configuration: [link]"
    - "Team, I got great results with this setup: [link]"
    - "Client wants to see training progress: [public link]"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR8.2.1:** Training Completion Notifications
  * Description: [To be filled]
  * Impact Weighting: Productivity / User Experience / Work-Life Balance
  * Priority: High
  * User Stories: US8.2.1
  * Tasks: [T-8.2.1]
  * User Story Acceptance Criteria:
    - **Notification Triggers**:
    - Training completed successfully
    - Training failed (with error details)
    - Training cancelled (by user or system)
    - Spot instance interrupted (if manual intervention needed)
    - **Email Notification** (training completed):
    - Subject: "✓ Training Job Completed: {job_name}"
    - Body:
    - Job name, configuration summary
    - Duration: 13.2 hours
    - Final cost: $48.32
    - Final metrics: Training loss 0.287, Perplexity improvement 31%
    - Quality: ✓ Production Ready
    - Actions: [View Job Details] [Download Adapters] [Generate Report]
    - **Slack Notification** (training completed):
    - Posted to designated channel or DM
    - Message: "✓ Training completed: **{job_name}** (13.2hrs, $48.32, 31% perplexity improvement) [View Job]"
    - **Email Notification** (training failed):
    - Subject: "✗ Training Job Failed: {job_name}"
    - Body:
    - Job name, error type, error message
    - Suggested fixes (if applicable)
    - Elapsed time before failure: 2.3 hours
    - Cost spent: $8.42
    - Actions: [View Error Details] [Retry with Suggested Fix] [Contact Support]
    - **Notification Preferences** (per user):
    - Email: On/Off, Digest mode (daily summary)
    - Slack: On/Off, Channel selection
    - In-app: Always on (banner notifications)
    - Which events: Completions only, Failures only, All events
    - **Weekend Freedom**: Engineers can start jobs Friday evening, receive notification Saturday/Sunday when complete, no need to check dashboard
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR8.2.2:** Job Notes and Experiment Documentation
  * Description: [To be filled]
  * Impact Weighting: Knowledge Preservation / Learning / Continuous Improvement
  * Priority: Medium
  * User Stories: US8.3.1
  * Tasks: [T-8.3.1]
  * User Story Acceptance Criteria:
    - **Notes Field** on job creation form:
    - Optional, multiline text area (2000 character limit)
    - Placeholder: "Document your experiment: hypothesis, expected outcomes, variables being tested"
    - Markdown support for formatting
    - **Edit Notes** after job creation:
    - "Edit Notes" button on job details page
    - Add observations during training or after completion
    - Example: "Update: Loss plateaued at epoch 2.5, suggests optimal stopping point"
    - **Notes Display**:
    - Prominent section on job details page
    - Shows creation notes + any updates with timestamps
    - Example: "Initial notes (2025-12-15 14:23): Testing aggressive LR..."
    - Example: "Update (2025-12-16 08:45): Completed successfully, 31% perplexity improvement..."
    - **Search by Notes**:
    - Job list page: Search box includes notes in query
    - Find jobs: "aggressive learning rate", "high emotion dataset", "client delivery"
    - **Notes in Reports**:
    - Include notes in exported CSV/PDF reports
    - Useful for documenting successful configurations
    - Use cases:
    - Experiment tracking: "Testing whether r=32 improves quality on emotional datasets"
    - Learning documentation: "Discovered that Balanced preset works best for 200+ conversation datasets"
    - Client context: "Training for Acme Financial Q1 project, focus on retirement planning scenarios"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]

- **FR8.3.1:** Team Knowledge Base Integration (Future)
  * Description: [To be filled]
  * Impact Weighting: Knowledge Sharing / Team Learning / Onboarding
  * Priority: Low (Future Enhancement)
  * User Stories: US8.3.2
  * Tasks: [T-8.3.2]
  * User Story Acceptance Criteria:
    - "Add to Knowledge Base" button on successful jobs
    - Create knowledge base entry:
    - Title: Job name
    - Category: Best practices, Experiments, Client deliveries, Troubleshooting
    - Tags: Aggressive LR, High emotion, Financial domain, etc.
    - Content: Configuration summary, results, key learnings, notes
    - Related jobs: Link to similar successful jobs
    - Knowledge base searchable: "How to train models on emotional datasets"
    - Use case: New engineer searches "retirement planning training" → finds 5 past successful jobs with notes and configurations
    - Auto-suggest: When creating new job, suggest related knowledge base articles: "Similar setup succeeded in Job XYZ"
  * Functional Requirements Acceptance Criteria:
    - [To be filled]


## Document Purpose
1. Break down User Stories into manageable functional requirements
2. Define clear acceptance criteria for each requirement
3. Maintain traceability between requirements, user stories, and tasks
4. Provide clear "WHAT" specifications for task generation
5. Enable validation of feature completeness against user needs

## Requirement Guidelines
1. Each requirement should map to one or more user stories
2. Requirements should focus on WHAT, not HOW
3. Both User Story and Functional Requirements acceptance criteria should be measurable
4. Technical details belong in the task specifications
5. Requirements should be understandable by non-technical stakeholders

## Document Generation Workflow
1. User Stories document is referenced
2. Functional Requirements are created based on stories
3. Implementation tasks are derived from requirements
4. Traceability is maintained across all artifacts
5. Requirements are validated against both sets of acceptance criteria

## Requirement Mapping Guide
1. Each requirement has a unique identifier (FR[X.Y.Z])
2. Requirements map to one or more user stories (US[X.Y.Z])
3. Requirements map to one or more tasks (T[X.Y.Z])
4. Requirements break down into specific tasks
5. Quality metrics are defined for validation

## Requirement Structure Guide
1. Description: Clear statement of what the feature should do
2. Impact Weighting: Business impact category
3. Priority: Implementation priority level
4. User Stories: Mapping to source user stories
5. Tasks: Mapping to implementation tasks
6. User Story Acceptance Criteria: Original criteria from user story
7. Functional Requirements Acceptance Criteria: Additional specific criteria for implementation
