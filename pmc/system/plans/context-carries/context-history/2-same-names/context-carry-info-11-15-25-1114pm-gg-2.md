# Context Carryover: Truncation Detection & Stop Reason Fix Specification

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

---

## 📌 Active Development Focus

**Primary Task**: Fix Truncation Detection Logic & Ensure Stop Reason Storage

### 1. The Problem
The current truncation detection logic is inconsistent.
1.  **False Negatives**: Truncated responses ending in `\\",` (escaped quote followed by comma in Raw JSON) are NOT being flagged as failures.
2.  **Stop Reason Visibility**: The `stop_reason` is not always clearly associated with the failure in a way that allows easy debugging of "why" it stopped.
3.  **False Positives (Risk)**: The user noted that `\\"` inside a string (e.g., `"I said \"hello\""`) must NOT trigger a failure, but `\\",` at the end of a response MUST trigger a failure.

### 2. Root Cause Analysis
- **Current Detection**: `detectTruncatedContent` uses `/\\"\s*$/`. This matches a string ending in `\"`.
- **The Missing Pattern**: The user identified `\\",` as a critical truncation indicator in the **Raw JSON**. This pattern (`\` `"` `,`) typically occurs when a JSON field is cut off immediately after an escaped quote, or when the JSON structure itself is truncated.
- **Parse Errors vs. Truncation**: If the Raw JSON is truncated (e.g., ends in `\\",`), `JSON.parse` fails. Currently, this is caught as a generic "Parse Error", not a "Truncation Error", and thus might not be reporting the `stop_reason` as clearly as a dedicated truncation failure.

### 3. Specification for the Fix

#### A. Update Truncation Detection Logic
Modify `src/lib/utils/truncation-detection.ts` to include the specific pattern identified by the user.

**New Pattern to Add**:
- **Pattern**: `/\\",\s*$/` (Matches `\",` at the end of the string)
- **Context**: This check must be applied to the **Raw JSON Content** (`apiResponse.content`), NOT the parsed turn content.
- **Reasoning**: This indicates the JSON response was cut off exactly at a field boundary involving an escaped quote.

#### B. Enhance `validateAPIResponse` in `conversation-generation-service.ts`
1.  **Stop Reason Check**: Ensure `stop_reason` is checked **first**. If `stop_reason` is `max_tokens` or `length`, fail immediately with `TruncatedResponseError`.
2.  **Raw JSON Truncation Check**:
    - Apply `detectTruncatedContent` to `apiResponse.content`.
    - Ensure the new `\\",` pattern is active.
3.  **Parsed Turn Truncation Check**:
    - Continue to call `detectTruncatedTurns` on parsed content to catch truncations *inside* valid JSON strings (where `stop_reason` might be `end_turn` but the model hallucinated a stop).

#### C. Handle Parse Errors as Potential Truncations
In `conversation-generation-service.ts`, inside the `catch` block for `JSON.parse`:
- If parsing fails, check the **Raw Content** for truncation patterns again.
- If a truncation pattern (like `\\",`) is found at the end of the raw content, throw a `TruncatedResponseError` instead of a generic `Error`.
- This ensures the failure is categorized as "Truncation" and the `stop_reason` is preserved in the failure report.

#### D. Store `stop_reason` for All Conversations
To enable debugging of "successful" but suspicious runs:
- **Action**: Update `ConversationStorageService.storeRawResponse` and `parseAndStoreFinal`.
- **Change**: Ensure `stop_reason` is saved in the `metadata` JSONB column of the `conversations` table.
- **Verification**: Check if `metadata` currently includes it. If not, add it.

### 4. Implementation Steps (For Next Agent)

1.  **Modify `src/lib/utils/truncation-detection.ts`**:
    - Add the `truncated_json_field` pattern: `/\\",\s*$/`.
    - Update `detectTruncatedContent` to use this pattern.

2.  **Modify `src/lib/services/conversation-generation-service.ts`**:
    - In `validateAPIResponse`:
        - Ensure `detectTruncatedContent` is called on `apiResponse.content`.
    - In `parseClaudeResponse` (or where `JSON.parse` happens):
        - Catch `SyntaxError`.
        - Check `content` against truncation patterns.
        - If matched, throw `TruncatedResponseError` with the `stop_reason` (passed down from caller).

3.  **Modify `src/lib/services/conversation-storage-service.ts`**:
    - Ensure `stop_reason` is added to the `metadata` object when creating the conversation record.

4.  **Verify**:
    - Run a generation that produces `\\",` (might be hard to force, so mock it or find a historical example).
    - Verify `failed_generations` table contains the record with `failure_type: 'truncation'` and the correct `stop_reason`.

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
