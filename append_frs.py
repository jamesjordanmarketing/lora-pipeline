#!/usr/bin/env python3
import os

output_file = r"c:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_mapping\fr-maps\04-pipeline-FIGMA-wireframes-output-E02.md"

# Due to token limits, I'll create abbreviated but comprehensive versions of the remaining FRs
# focusing on the most critical UI elements while maintaining the required format

fr2_1_3_content = """
=== BEGIN PROMPT FR: FR2.1.3 ===

Title
- FR FR2.1.3 Wireframes — Stage 2 — Training Job Execution & Monitoring

Context Summary
- This feature provides a comprehensive chronological event log displaying all webhook events received from the GPU training container, including status changes, metrics updates, warnings, and errors. The event log serves as the authoritative troubleshooting tool for engineers to diagnose failures, understand training progression, and access detailed webhook payloads. Users access the Event Log tab on the job details page to review complete training history with color-coded events, expandable JSON payloads, powerful filtering, and export capabilities.

Journey Integration
- Stage goals: Troubleshoot training issues by accessing detailed event history, understand what happened during failures, export data for analysis
- Key emotions: Empowerment through detailed information, confidence through transparency, reduced frustration via self-service debugging
- Progressive disclosure levels:
  * Basic: Event list with timestamps and messages (chronological view of what happened)
  * Advanced: Expandable JSON payloads with syntax highlighting for deep dive
  * Expert: Filtering by event type, keyword search, export for offline analysis
- Persona adaptations: Primary for technical users debugging issues; Support teams reviewing tickets; QA analysts investigating quality concerns

### Journey-Informed Design Elements
- User Goals: Find error events quickly, understand failure root causes, review checkpoint save confirmations, export complete history for analysis
- Emotional Requirements: Complete transparency into training operations, self-service debugging capability, confidence through data access
- Progressive Disclosure:
  * Basic: Table view with timestamp, event type badge, message summary
  * Advanced: Click row to expand full JSON webhook payload
  * Expert: Filter to specific event types, search keywords, export JSON/CSV
- Success Indicators: User identifies root cause of failure, User finds performance warning, User successfully exports data for team analysis

Wireframe Goals
- Display complete chronological audit trail of training events
- Enable rapid problem identification through color-coded event types
- Support deep technical investigation via expandable JSON payloads
- Provide filtering to focus on errors, warnings, or specific event types
- Enable keyword search across all event data
- Support export for external tools and team collaboration
- Update in real-time during active training (polling every 10s)

Explicit UI Requirements (from acceptance criteria)
- **Event Log Tab**: Accessible from job details page navigation ("Overview | Metrics | Event Log | Artifacts"), URL: `/training-jobs/{job_id}?tab=event-log`
- **Event Table Layout**: Responsive table with fixed header, Four columns: Timestamp (150px), Event Type (120px badge), Message (flexible width), Actions (80px expand button), Alternate row backgrounds (white/light gray)
- **Timestamp Column**: Format "YYYY-MM-DD HH:mm:ss" with user timezone, Relative time on hover ("3 hours ago"), Sortable (default DESC - newest first)
- **Event Type Column**: Badge-style with colors: Status (blue), Metrics (green), Warning (yellow), Error (red), Info (gray), Checkpoint (purple), Icon prefix: ℹ️ Status, 📊 Metrics, ⚠️ Warning, ❌ Error, 💾 Checkpoint
- **Message Column**: Extracted summary: Status: "{old_status} → {new_status}", Metrics: "Step {step}: loss={loss}, lr={lr}, gpu_util={util}%", Checkpoint: "Checkpoint saved at step {step} ({size}MB)", Warning: "{warning_message}", Error: "{error_type}: {error_message}", Truncated to 100 chars with "..." if longer
- **Expandable Row Details**: Click anywhere on row to expand, Expanded section slides down below row, Displays formatted JSON with syntax highlighting (keys blue, strings green, numbers orange, booleans purple, null gray), "Copy JSON" button copies full payload to clipboard with toast "JSON copied", Collapse button or click row again to hide
- **Event Type Filtering**: Dropdown filter above table: "Show: [All Events ▼]", Options: All Events, Status Changes Only, Metrics Updates Only, Warnings Only, Errors Only, Checkpoints Only, Multiple selection allowed (e.g., "Warnings + Errors"), Filter applies immediately, URL updated: `?filter=warnings,errors`
- **Keyword Search**: Search input box: "Search events by message or payload...", Debounced 500ms after user stops typing, Searches message text and full JSON payload (case-insensitive), Highlights matching keywords (yellow background), Displays match count: "Found 23 events matching 'checkpoint'"
- **Real-Time Updates**: Polling every 10 seconds: Fetch new events with received_at > last_loaded_timestamp, Prepend new events to top of table, Blue pulse animation on newly added rows (2 second duration), Badge in tab label if user viewing different tab: "Event Log (5 new)", Auto-scroll to top when critical events (errors/warnings) arrive
- **Pagination**: 50 events per page (configurable: 25/50/100 options), Controls: "< Previous | Page X of Y | Next >", Numbered page links: "< 1 2 [3] 4 5 ... 42 >", Total count: "Showing 101-150 of 2,847 events", Keyboard shortcuts: Arrow keys to navigate pages
- **Export Functionality**: "Export Log" button above table, Export modal with options: JSON format (complete event array), CSV format (columns: timestamp, event_type, message, full_payload), "Export current filtered view only" checkbox, Date range pickers: From/To dates, Download triggers immediate file download, Filename: `{job_name}-event-log-{timestamp}.{json|csv}`
- **Example Events**: "2025-12-15 14:23:42 | Status | Training started (GPU: H100 PCIe 80GB spot)", "2025-12-15 14:28:15 | Metrics | Step 100: loss=0.521, lr=0.0002, gpu_util=89%", "2025-12-15 14:33:08 | Warning | GPU utilization dropped to 45% (possible throttling)", "2025-12-15 15:12:33 | Error | Spot instance interrupted, initiating checkpoint recovery"
- States: Empty (no events yet), Loading (skeleton rows), Populated with events, Filtered results, Search results with highlights, Expanded row showing JSON, Error fetching data (retry button)

Interactions and Flows
- **Access Flow**: User on job details page → Clicks "Event Log" tab → Tab becomes active → Event table loads → Database query fetches events → Table displays sorted newest first → Real-time polling begins (if job active)
- **Event Exploration**: User scans event list → Spots yellow warning badge → Clicks warning row → Row expands with JSON payload → User reviews detailed warning data → Clicks "Copy JSON" → Payload copied, toast confirms → User clicks row again to collapse
- **Troubleshooting Flow**: User reviewing failed job → Clicks Event Log tab → Applies filter: "Errors Only" → Table shows only red error events → User clicks error row → Reviews full error payload with stack trace → Identifies OOM error → User exports filtered log → Downloads CSV with all errors → Shares with team for analysis
- **Real-Time Monitoring**: User watching active training → Event Log tab open → New metric event arrives → After 10s poll, new event prepends to table → Row pulses blue → User scrolls to top to see latest event → Process repeats every 10s
- **Search Flow**: User needs to verify checkpoints → Types "checkpoint" in search → After 500ms, results filter → Table shows only matching events → Keywords highlighted yellow → Count shows "Found 23 events" → User confirms checkpoints saved every 100 steps

Visual Feedback
- **Color-Coded Event Types**: Status (blue badge white text), Metrics (green badge white text), Warning (yellow badge dark text), Error (red badge white text), Info (gray badge white text), Checkpoint (purple badge white text)
- **Row Interactions**: Hover: Light blue background tint, Click: Smooth expand animation (300ms), Expand icon rotates from down (▼) to up (▲) arrow
- **New Event Animations**: New row prepended: Blue pulse animation (2 seconds), Subtle slide-in from top animation
- **Search Highlights**: Matching text: Yellow background highlight, Multiple matches: All independently highlighted
- **Loading States**: Initial load: Skeleton rows (gray animated shimmer), Pagination change: Dimmed table with spinner overlay, Real-time fetch: Small spinner in tab badge

Accessibility Guidance
- **Keyboard Navigation**: Tab moves through table rows, Enter expands/collapses selected row, Arrow keys navigate between rows, Escape closes expanded rows
- **Screen Reader**: Table announced: "Event log table with 2,847 events. Use arrow keys to navigate.", Each row: "Event at [timestamp], Type: [type], Message: [message]", Expanded: "Event details: [JSON content]", Filter changes: "Showing 15 events matching filter"
- **Focus Indicators**: 2px blue outline on focused elements, High contrast on interactive elements
- **Color Independence**: Event types identified by icons + text (not color alone), High contrast mode support

Information Architecture
- **Page Layout**: Event Log tab (within job details tabs) → Filter/Search bar (full width above table) → Event table (main content) → Pagination controls (below table)
- **Table Structure**: Fixed header (stays visible on scroll) → Data rows (timestamp left, type center-left, message center-right, expand right) → Expanded row content (full width below parent row)
- **Content Density**: Compact: 50 events per page, ~20 visible without scroll, Expandable detail on demand (doesn't clutter default view)

Page Plan
1. **Event Log - Active Job with Mixed Events**
   - Purpose: Display typical event log during active training showing variety of event types
   - Components: Event Log tab (active), Filter bar (All Events selected), Search box (empty), Event table with ~20 visible events showing mix of Status (blue), Metrics (green), Warning (yellow), Checkpoint (purple) events, Pagination showing "1-50 of 127 events", Real-time polling active indicator
   - States: Auto-refreshing every 10s, No filters applied, Events sorted newest first
   - Sample events: Training started, Step metrics, Checkpoint saves, GPU warnings

2. **Event Log - Expanded JSON Payload**
   - Purpose: Show detailed webhook payload when user expands event for deep dive
   - Components: Event table with one row expanded, Expanded section displaying formatted JSON with syntax highlighting, Example payload: `{event_type: "metrics_update", step: 100, training_loss: 0.521, validation_loss: 0.538, learning_rate: 0.0002, gpu_utilization: 89, gpu_memory_used_gb: 68, tokens_per_second: 1247}`, "Copy JSON" button active, Collapse arrow indicator
   - States: Single row expanded, Others collapsed, Smooth animation
   - Actions: User can copy JSON, collapse row, expand different row

3. **Event Log - Filtered to Errors and Warnings**
   - Purpose: Focus on problems by filtering to only errors and warnings for troubleshooting
   - Components: Filter dropdown showing "Warnings, Errors" selected (checkboxes), Event table displaying only yellow warning and red error events, Count updated: "Showing 1-15 of 15 events", "Clear Filters" button visible, Error messages prominent
   - States: Filter active, URL: `?filter=warnings,errors`, Subset of events displayed
   - Use case: Engineer troubleshooting failed job, wants to see only problems

4. **Event Log - Keyword Search with Highlights**
   - Purpose: Find specific events using keyword search across all event data
   - Components: Search box with "checkpoint" entered, Event table showing only matching events (23 results), Keywords highlighted in yellow in message column and expanded JSON (if visible), Match count: "Found 23 events matching 'checkpoint'", Clear search "X" button
   - States: Search filter applied, Results highlighted, Count displayed
   - Use case: Verifying checkpoint saves occurred every 100 steps as expected

5. **Event Log - Export Modal**
   - Purpose: Export event data for offline analysis, sharing with team, or compliance
   - Components: Modal overlay with dark backdrop, Export options: Format selection (Radio buttons: JSON / CSV), "Export current filtered view only" checkbox, Date range pickers: From [date] To [date], Preview text: "Exporting 127 events", Buttons: "Download" (primary blue), "Cancel" (secondary gray)
   - States: Modal open, User selecting format and options
   - Actions: Click Download → File downloads (instant) → Modal closes → Toast: "Event log exported"

Annotations (Mandatory)
- Attach notes to table columns citing US2.1.3 and FR2.1.3 acceptance criteria
- Create "Event Type Reference Table" frame mapping: Event Type → Color Code → Icon → Sample Messages → Payload Structure
- Document expand/collapse interaction flow with animation specs
- Link filtering and search features to specific acceptance criteria

Acceptance Criteria → UI Component Mapping

| Criterion | Source | Screen(s) | Component(s) | State(s) | Notes |
|-----------|--------|-----------|--------------|----------|-------|
| "Event Log" tab on job details page | US2.1.3 | All | Tab navigation | Active | Third tab in job details navigation |
| Table columns: Timestamp, Event Type, Message, Payload (expandable) | US2.1.3 | 1-5 | Table structure | All | Four-column responsive layout |
| Event types color-coded | US2.1.3 | 1-5 | Event Type badges | All types | Blue/Green/Yellow/Red/Gray/Purple with icons |
| Status changes (blue), Metrics (green), Warnings (yellow), Errors (red) | US2.1.3 | 1,3,4 | Event badges | Respective types | Consistent color coding throughout |
| Expandable rows show full webhook payload as formatted JSON | US2.1.3 | 2 | Expanded row | Expanded | Syntax highlighting, copy button |
| Filter events by type: All / Status / Metrics / Warnings / Errors | US2.1.3 | 3 | Filter dropdown | Filtered | Multi-select, immediate application |
| Search by keyword in messages | US2.1.3 | 4 | Search input | Search active | Debounced 500ms, highlights matches |
| Export log as JSON or CSV | US2.1.3 | 5 | Export modal | Export flow | Complete or filtered subset |
| Real-time updates: new events appear automatically | US2.1.3 | 1 | Auto-refresh | Active job | Every 10s, prepend with animation |
| Pagination: 50 events per page | US2.1.3 | All | Pagination controls | All | Configurable 25/50/100 |
| Example events with proper formatting | US2.1.3 | 1,3,4 | Event rows | Various | Training started, metrics, warnings, errors |
| Timestamp format "YYYY-MM-DD HH:mm:ss" with timezone | FR2.1.3 | All | Timestamp column | All | User's local timezone, UTC offset shown |
| Relative time on hover | FR2.1.3 | All | Timestamp hover tooltip | Hover | "3 hours ago" |
| Sortable timestamp (ASC/DESC toggle) | FR2.1.3 | All | Timestamp header | Interactive | Click to sort, default DESC |
| Event Type badges with icons and colors | FR2.1.3 | All | Event Type column | All | Consistent badge styling |
| Message extraction from payload | FR2.1.3 | All | Message column | All | Generated summary, 100 char limit |
| Click row to expand JSON payload | FR2.1.3 | 2 | Row click area | Interactive | Smooth slide animation |
| Syntax-highlighted JSON | FR2.1.3 | 2 | Expanded JSON display | Expanded | Color-coded by data type |
| "Copy JSON" button | FR2.1.3 | 2 | Copy button | Interactive | Clipboard API, toast confirmation |
| Event type filter with multi-select | FR2.1.3 | 3 | Filter checkboxes | Filtered | Multiple event types selectable |
| Filter applies immediately | FR2.1.3 | 3 | Filter logic | Active filter | No Apply button needed |
| URL updated with filter state | FR2.1.3 | 3 | URL parameters | Filtered | `?filter=warnings,errors` |
| Keyword search with debounce | FR2.1.3 | 4 | Search mechanism | Search active | 500ms delay after typing |
| Case-insensitive search | FR2.1.3 | 4 | Search logic | Search active | Matches regardless of case |
| Yellow highlight on matching keywords | FR2.1.3 | 4 | Search result styling | Matches found | Background color highlight |
| Match count display | FR2.1.3 | 4 | Search results info | Matches found | "Found X events matching 'keyword'" |
| Real-time polling every 10 seconds | FR2.1.3 | 1 | Polling logic | Active job | Fetches new events after last timestamp |
| New events prepended with animation | FR2.1.3 | 1 | New row animation | New events | Blue pulse for 2 seconds |
| Badge in tab if viewing different tab | FR2.1.3 | N/A | Tab notification badge | New events available | "Event Log (5 new)" |
| Configurable page size (25/50/100) | FR2.1.3 | All | Page size selector | All | Dropdown in pagination controls |
| Numbered page links | FR2.1.3 | All | Pagination navigation | Multiple pages | "< 1 2 [3] 4 5 ... 42 >" |
| Total event count | FR2.1.3 | All | Pagination info | All | "Showing X-Y of Z events" |
| Export button opens modal | FR2.1.3 | 5 | Export button | Click | Modal overlay with options |
| JSON export format option | FR2.1.3 | 5 | Format selector | Export modal | Radio button selection |
| CSV export format option | FR2.1.3 | 5 | Format selector | Export modal | Radio button selection |
| "Export filtered view only" option | FR2.1.3 | 5 | Export checkbox | Export modal | Exports current filter/search results |
| Date range selection | FR2.1.3 | 5 | Date pickers | Export modal | From/To date constraints |
| Immediate download | FR2.1.3 | 5 | Download action | Export complete | No server processing delay |

Non-UI Acceptance Criteria

| Criterion | Impact | UI Hint |
|-----------|--------|---------|
| Events loaded from training_webhook_events table | Backend data | SQL query provides event data |
| Indexed database query (job_id, received_at DESC) | Performance | Fast event retrieval |
| JSONB storage for event payloads | Database efficiency | Efficient JSON operations |
| Lazy loading of expanded payloads | Performance | Payload not loaded until expanded |
| Virtualized scrolling for >500 events | Performance | Renders only visible rows |
| Client-side export generation | Performance | No server processing, instant download |

Estimated Page Count
- **5 screens** providing complete event log functionality coverage:
  1. Active Job with Mixed Events (typical viewing during training)
  2. Expanded JSON Payload (detailed event investigation)
  3. Filtered to Errors and Warnings (troubleshooting focus)
  4. Keyword Search with Highlights (finding specific events)
  5. Export Modal (data export for analysis)
- Rationale: Complete workflow from viewing (1), investigating details (2), troubleshooting (3), searching (4), to exporting (5), satisfying all UI-relevant acceptance criteria

=== END PROMPT FR: FR2.1.3 ===

"""

# Append to file
with open(output_file, 'a', encoding='utf-8') as f:
    f.write(fr2_1_3_content)

print("FR2.1.3 appended successfully!")
print(f"File now at: {os.path.getsize(output_file)} bytes")
