# Context Carryover: Enhanced Truncation Detection & Stop Reason Tracking Specification

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
Dashboard View → Download (Raw or Enriched) → Combine Multiple JSON files into a full LoRA Training file.
```

---

## 📌 Active Development Focus

**Primary Task**: Fix Truncation Detection System to Properly Identify and Report End-of-Response Truncations

### Current Problem Statement (December 7, 2025)

**Issue**: The `\\"` truncation pattern still occurs in generated conversations but is NOT being flagged as failed, despite having:
- ✅ Turn-level truncation detection implemented (`detectTruncatedTurns()`)
- ✅ `stop_reason` capture in `claude-api-client.ts`
- ✅ `failed_generations` database table with proper schema
- ✅ Failed generations UI at `/conversations/failed`
- ✅ `FailedGenerationService` fully implemented

**Root Cause**: The current truncation pattern matching is **too broad** and causes false positives, OR the pattern is **not specific enough** to catch actual end-of-response truncations.

**Critical Requirement**: Must ONLY flag as failed when the pattern `\\"` appears at the END of a response followed by closing JSON syntax (e.g., `\\",` or `\\"}`), NOT when `\\"` appears in the middle of valid content like:
- ✅ VALID: `"I've been so focused on \"getting ahead\" that I didn't realize"` 
- ❌ TRUNCATED: `"The overwhelming number of choices, the fear of making the \\"` (at end of assistant turn)

**Missing Visibility**: 
- Cannot evaluate what caused stoppage (no `stop_reason` visibility in reports)
- No detailed truncation metadata (which turns, what patterns, position in response)
- No way to distinguish false positives from true truncations

---

## 🔍 Investigation Findings

### Current System State (Verified December 7, 2025)

**Database State**:
- `failed_generations` table: **0 records** (table exists, properly indexed, RLS configured)
- `conversations` table: **10 recent conversations** (all status: `pending_review`, enrichment_status: `completed`)
- **Implication**: Either no truncations occurred OR truncations are not being detected

**Code State**:
- ✅ `detectTruncatedContent()` exists in `truncation-detection.ts` with pattern: `/\\"\s*$/`
- ✅ `detectTruncatedTurns()` exists and IS CALLED in validation (lines 407-437 of `conversation-generation-service.ts`)
- ✅ `stop_reason` captured from Claude API (lines 312-318 of `claude-api-client.ts`)
- ✅ `stop_reason` stored in `failed_generations.stop_reason` column (TEXT type)
- ✅ Failed generation storage includes full diagnostic context

**Historical Evidence**:
From `single-convo-file-3-RAW.json` (archived truncated file):
- Turn 2 ends with: `"the fear of making the \\"` (593 chars, TRUNCATED)
- Turn 4 ends with: `"The money sitting in your savings account isn't \\"` (255 chars, TRUNCATED)
- File size: 4,332 bytes (~1,000 tokens) - FAR below 24,576 token limit
- `stop_reason` from logs: `end_turn` (not `max_tokens`)
- **Result**: Conversation was validated successfully and stored (not flagged as failed)

### Pattern Analysis: What We're Actually Detecting

**In Raw JSON** (what Claude returns):
```json
{
  "turns": [
    {
      "role": "assistant",
      "content": "text that ends with \\"
    }
  ]
}
```

**After JSON Parsing** (what `detectTruncatedTurns()` sees):
```javascript
content: 'text that ends with \"'
```

**Current Pattern**: `/\\"\s*$/`
- Matches: backslash + quote at end of string
- Problem: May match valid content like `"I said \"hello\""` if parsed incorrectly
- Solution: Need more specific end-of-response context detection

**Actual Truncation Signature**:
When Claude truncates mid-generation with structured outputs:
1. The JSON structure remains valid (closing braces added by system)
2. The content string ends with incomplete escape sequence: `\"`
3. In the turn array, this is the LAST assistant turn OR followed by incomplete dialogue
4. The preceding text does NOT show a closed quote pattern (no opening `\"` earlier in the same phrase)

---

## 🎯 Specification: Enhanced Truncation Detection System

### Phase 1: Enhanced Pattern Matching

**Objective**: Make truncation detection more accurate by adding contextual analysis.

#### 1.1 Enhanced `detectTruncatedContent()` Function

**Location**: `src/lib/utils/truncation-detection.ts`

**Current Implementation** (lines 32-42):
```typescript
const TRUNCATION_PATTERNS = [
  {
    pattern: /\\"\s*$/,
    name: 'truncated_escape_sequence',
    desc: 'Content ends with escaped quote indicating mid-sentence truncation',
    confidence: 'high' as const,
  },
];
```

**Proposed Enhancement**:
```typescript
const TRUNCATION_PATTERNS = [
  {
    // Pattern 1: Content ends with \\" at the end (NO preceding closing quote)
    // This catches: "...the fear of making the \"
    // But NOT: "I said \"hello\" and then"
    pattern: /[^"]\\"\s*$/,
    name: 'truncated_escape_sequence',
    desc: 'Content ends with unmatched escaped quote indicating mid-sentence truncation',
    confidence: 'high' as const,
  },
  {
    // Pattern 2: Content ends with incomplete word after \\
    // This catches: "...the account isn\\"
    pattern: /\w+\\"\s*$/,
    name: 'truncated_word_with_escape',
    desc: 'Content ends with incomplete word followed by escaped quote',
    confidence: 'high' as const,
  },
  {
    // Pattern 3: Content ends with \\ followed by any non-quote character
    // This catches: "...text ends with \t" or "...text ends with \n"
    pattern: /\\[^"\s]\s*$/,
    name: 'truncated_escape_character',
    desc: 'Content ends with incomplete escape sequence',
    confidence: 'medium' as const,
  },
];
```

**Rationale**:
- Pattern 1 `[^"]\\"\s*$`: Ensures the `\"` is NOT preceded by another quote (which would indicate a closed quote pair)
- Pattern 2 `\w+\\"\s*$`: Catches cases where the truncation happens mid-word
- Pattern 3 `\\[^"\s]\s*$`: Catches other incomplete escape sequences (e.g., `\t`, `\n`, `\r`)

**Additional Context Check**:
```typescript
// Add contextual validation
export function detectTruncatedContent(content: string): TruncationDetectionResult {
  if (!content || content.trim().length === 0) {
    return {
      isTruncated: false,
      pattern: null,
      details: 'Empty content',
      confidence: 'low',
    };
  }

  const trimmed = content.trim();

  // Check against known truncation patterns
  for (const { pattern, name, desc, confidence } of TRUNCATION_PATTERNS) {
    if (pattern.test(trimmed)) {
      // Additional validation: Check if this is likely a true truncation
      // by analyzing content length and structure
      const isLikelyTruncation = validateTruncationContext(trimmed, name);
      
      if (isLikelyTruncation) {
        return {
          isTruncated: true,
          pattern: name,
          details: desc,
          confidence,
        };
      }
    }
  }

  return {
    isTruncated: false,
    pattern: null,
    details: 'Content appears complete (no truncation patterns detected)',
    confidence: 'high',
  };
}

/**
 * Validate truncation context to reduce false positives
 * @private
 */
function validateTruncationContext(content: string, patternName: string): boolean {
  // Rule 1: Content must be at least 50 chars (avoid flagging single words)
  if (content.length < 50) {
    return false;
  }

  // Rule 2: For escaped quote patterns, check if there's an opening quote
  if (patternName === 'truncated_escape_sequence') {
    // Count quotes in the content
    const quoteCount = (content.match(/[^\\]"/g) || []).length;
    // If even number of quotes, last quote might be closing a pair
    // If odd number, likely truncation
    return quoteCount % 2 === 1;
  }

  // Rule 3: Content should not end with a complete sentence pattern
  // (this would indicate intentional ending, not truncation)
  const completeEndingPattern = /[.!?]\s*["']?\s*$/;
  if (completeEndingPattern.test(content)) {
    return false;
  }

  // Default: Trust the pattern match
  return true;
}
```

#### 1.2 Enhanced Turn-Level Detection with Position Tracking

**Enhancement**: Add position tracking to identify WHICH turns are truncated and WHERE in the conversation.

**New Interface** (add to `truncation-detection.ts`):
```typescript
export interface TruncatedTurnDetail {
  turnIndex: number;
  turnNumber: number; // User-friendly numbering (1-based)
  role: 'assistant';
  result: TruncationDetectionResult;
  contentLength: number;
  contentPreview: string; // Last 100 chars for reporting
  isLastAssistantTurn: boolean; // Critical indicator
}

export interface ConversationTruncationAnalysis {
  isTruncated: boolean;
  truncatedTurns: TruncatedTurnDetail[];
  totalTurns: number;
  totalAssistantTurns: number;
  truncationSummary: string;
  confidence: 'high' | 'medium' | 'low';
}
```

**Enhanced Function**:
```typescript
/**
 * Analyze entire conversation for truncation with detailed reporting
 */
export function analyzeConversationTruncation(
  turns: Array<{ role: 'user' | 'assistant'; content: string }>
): ConversationTruncationAnalysis {
  const truncatedTurns: TruncatedTurnDetail[] = [];
  let lastAssistantTurnIndex = -1;

  // Find last assistant turn
  for (let i = turns.length - 1; i >= 0; i--) {
    if (turns[i].role === 'assistant') {
      lastAssistantTurnIndex = i;
      break;
    }
  }

  // Analyze each assistant turn
  turns.forEach((turn, index) => {
    if (turn.role === 'assistant') {
      const result = detectTruncatedContent(turn.content);
      if (result.isTruncated) {
        const isLastAssistantTurn = index === lastAssistantTurnIndex;
        
        truncatedTurns.push({
          turnIndex: index,
          turnNumber: index + 1,
          role: 'assistant',
          result,
          contentLength: turn.content.length,
          contentPreview: turn.content.slice(-100),
          isLastAssistantTurn,
        });
      }
    }
  });

  // Determine overall confidence
  let confidence: 'high' | 'medium' | 'low' = 'low';
  if (truncatedTurns.length > 0) {
    // High confidence if last assistant turn is truncated
    const hasLastTurnTruncated = truncatedTurns.some(t => t.isLastAssistantTurn);
    if (hasLastTurnTruncated) {
      confidence = 'high';
    } else if (truncatedTurns.length > 1) {
      confidence = 'medium';
    } else {
      confidence = 'medium';
    }
  }

  // Generate summary
  const totalAssistantTurns = turns.filter(t => t.role === 'assistant').length;
  const truncationSummary = truncatedTurns.length > 0
    ? `${truncatedTurns.length} of ${totalAssistantTurns} assistant turns truncated (turns: ${truncatedTurns.map(t => t.turnNumber).join(', ')})`
    : 'No truncations detected';

  return {
    isTruncated: truncatedTurns.length > 0,
    truncatedTurns,
    totalTurns: turns.length,
    totalAssistantTurns,
    truncationSummary,
    confidence,
  };
}
```

---

### Phase 2: Enhanced Validation in Generation Service

**Objective**: Update validation logic to use enhanced truncation analysis and provide detailed error reporting.

#### 2.1 Update `validateAPIResponse()` Method

**Location**: `src/lib/services/conversation-generation-service.ts` (lines 378-440)

**Current Implementation**:
- ✅ Validates `stop_reason`
- ✅ Checks raw JSON for truncation
- ✅ Checks individual turns for truncation
- ❌ Does NOT provide detailed truncation context in errors

**Required Changes**:

**Step 1**: Add import for enhanced analysis:
```typescript
import { 
  detectTruncatedContent, 
  detectTruncatedTurns,
  analyzeConversationTruncation,
  type ConversationTruncationAnalysis,
  type TruncatedTurnDetail
} from '../utils/truncation-detection';
```

**Step 2**: Replace VALIDATION 3 (lines 407-437) with enhanced version:
```typescript
// VALIDATION 3: Comprehensive turn-level truncation analysis
try {
  const parsed = JSON.parse(apiResponse.content);
  
  if (parsed.turns && Array.isArray(parsed.turns)) {
    const analysis = analyzeConversationTruncation(parsed.turns);
    
    if (analysis.isTruncated) {
      // Log detailed truncation information
      console.warn(`[${generationId}] ⚠️ TRUNCATION DETECTED`);
      console.warn(`[${generationId}] Summary: ${analysis.truncationSummary}`);
      console.warn(`[${generationId}] Confidence: ${analysis.confidence}`);
      console.warn(`[${generationId}] stop_reason: ${apiResponse.stop_reason}`);
      
      // Log each truncated turn
      analysis.truncatedTurns.forEach(turn => {
        console.warn(`[${generationId}] Turn ${turn.turnNumber} (${turn.contentLength} chars):`);
        console.warn(`[${generationId}]   Pattern: ${turn.result.pattern}`);
        console.warn(`[${generationId}]   Preview: ...${turn.contentPreview}`);
        console.warn(`[${generationId}]   Is last assistant turn: ${turn.isLastAssistantTurn}`);
      });
      
      // Build detailed error message
      const truncationDetails = analysis.truncatedTurns
        .map(t => {
          const location = t.isLastAssistantTurn ? ' [LAST TURN]' : '';
          return `Turn ${t.turnNumber}${location}: ${t.result.pattern} (${t.contentLength} chars, confidence: ${t.result.confidence})`;
        })
        .join('; ');
      
      // Store analysis for failed generation report
      const analysisContext = {
        analysis,
        stop_reason: apiResponse.stop_reason,
        usage: apiResponse.usage,
      };
      
      throw new TruncatedResponseError(
        `Content truncated in ${analysis.truncatedTurns.length} turn(s): ${truncationDetails}`,
        apiResponse.stop_reason,
        analysis.truncatedTurns[0].result.pattern,
        analysisContext // Pass detailed context for storage
      );
    }
  }
} catch (parseError) {
  if (parseError instanceof TruncatedResponseError) {
    throw parseError;  // Re-throw TruncatedResponseError
  }
  // Log but don't throw for other parse errors - they'll be handled downstream
  console.warn(`[${generationId}] Could not parse content for turn-level validation: ${parseError instanceof Error ? parseError.message : 'Unknown error'}`);
}
```

**Step 3**: Update `TruncatedResponseError` class to accept analysis context:
```typescript
/**
 * Custom error for truncated responses with enhanced context
 */
export class TruncatedResponseError extends Error {
  constructor(
    message: string,
    public stopReason: string | null,
    public pattern: string | null,
    public analysisContext?: {
      analysis: ConversationTruncationAnalysis;
      stop_reason: string | null;
      usage: { input_tokens: number; output_tokens: number };
    }
  ) {
    super(message);
    this.name = 'TruncatedResponseError';
  }
}
```

---

### Phase 3: Enhanced Failed Generation Storage

**Objective**: Store comprehensive truncation metadata for analysis and reporting.

#### 3.1 Add Truncation Metadata Fields to Database

**Database Migration Required**: NO (existing schema is sufficient with JSONB usage)

The current `failed_generations` table has:
- ✅ `stop_reason` (TEXT) - stores Claude's stop reason
- ✅ `truncation_pattern` (TEXT) - stores detected pattern name
- ✅ `truncation_details` (TEXT) - stores description
- ✅ `raw_response` (JSONB) - can store additional metadata

**Enhancement**: Use `raw_response` JSONB field to store comprehensive truncation analysis.

#### 3.2 Update `storeFailedGeneration()` Method

**Location**: `src/lib/services/conversation-generation-service.ts` (lines 451-527)

**Required Changes**:

**Step 1**: Extract truncation analysis from error context:
```typescript
private async storeFailedGeneration(
  error: Error,
  context: {
    prompt: string;
    apiResponse: ClaudeAPIResponse;
    params: GenerationParams;
  },
  generationId: string
): Promise<void> {
  try {
    console.log(`[${generationId}] Storing as failed generation...`);

    const failedGenService = getFailedGenerationService();

    // Determine failure type and details
    let failureType: 'truncation' | 'parse_error' | 'api_error' | 'validation_error' = 'api_error';
    let truncationPattern: string | null = null;
    let truncationDetails: string | null = null;
    let truncationAnalysis: any = null; // Will store in raw_response

    if (error instanceof TruncatedResponseError) {
      failureType = 'truncation';
      truncationPattern = error.pattern;
      truncationDetails = error.message;
      
      // Extract comprehensive analysis if available
      if (error.analysisContext) {
        truncationAnalysis = {
          truncation_analysis: {
            total_turns: error.analysisContext.analysis.totalTurns,
            total_assistant_turns: error.analysisContext.analysis.totalAssistantTurns,
            truncated_turns_count: error.analysisContext.analysis.truncatedTurns.length,
            truncated_turns: error.analysisContext.analysis.truncatedTurns.map(turn => ({
              turn_number: turn.turnNumber,
              turn_index: turn.turnIndex,
              pattern: turn.result.pattern,
              confidence: turn.result.confidence,
              content_length: turn.contentLength,
              content_preview: turn.contentPreview,
              is_last_assistant_turn: turn.isLastAssistantTurn,
            })),
            summary: error.analysisContext.analysis.truncationSummary,
            confidence: error.analysisContext.analysis.confidence,
          },
          stop_reason_analysis: analyzeStopReason(
            error.stopReason,
            error.analysisContext.usage,
            context.params.maxTokens || AI_CONFIG.maxTokens
          ),
        };
      }
    } else if (error instanceof UnexpectedStopReasonError) {
      failureType = 'truncation';
      truncationPattern = 'unexpected_stop_reason';
      truncationDetails = `stop_reason was '${error.stopReason}' instead of 'end_turn'`;
    }

    // Build failed generation input with enhanced metadata
    const input: CreateFailedGenerationInput = {
      conversation_id: generationId,
      run_id: context.params.runId,
      
      prompt: context.prompt,
      model: context.apiResponse.model,
      max_tokens: context.params.maxTokens || AI_CONFIG.maxTokens,
      temperature: context.params.temperature || AI_CONFIG.temperature,
      structured_outputs_enabled: true,
      
      raw_response: {
        id: context.apiResponse.id,
        model: context.apiResponse.model,
        stop_reason: context.apiResponse.stop_reason,
        usage: context.apiResponse.usage,
        cost: context.apiResponse.cost,
        durationMs: context.apiResponse.durationMs,
        // Add truncation analysis if available
        ...(truncationAnalysis || {}),
      },
      response_content: context.apiResponse.content,
      
      stop_reason: context.apiResponse.stop_reason,
      input_tokens: context.apiResponse.usage.input_tokens,
      output_tokens: context.apiResponse.usage.output_tokens,
      
      failure_type: failureType,
      truncation_pattern: truncationPattern,
      truncation_details: truncationDetails,
      
      error_message: error.message,
      error_stack: error.stack,
      
      created_by: context.params.userId,
      
      persona_id: context.params.scaffoldingIds?.personaId,
      emotional_arc_id: context.params.scaffoldingIds?.emotionalArcId,
      training_topic_id: context.params.scaffoldingIds?.trainingTopicId,
      template_id: context.params.templateId,
    };

    await failedGenService.storeFailedGeneration(input);

    console.log(`[${generationId}] ✅ Failed generation stored with enhanced truncation analysis`);
  } catch (storeError) {
    console.error(`[${generationId}] ❌ Error storing failed generation:`, storeError);
  }
}

/**
 * Analyze stop_reason in context of token usage
 * @private
 */
function analyzeStopReason(
  stopReason: string | null,
  usage: { input_tokens: number; output_tokens: number },
  maxTokens: number
): string {
  if (!stopReason) {
    return 'stop_reason not available - may indicate API error';
  }

  const tokensRemaining = maxTokens - usage.output_tokens;
  const usagePercent = Math.round((usage.output_tokens / maxTokens) * 100);

  switch (stopReason) {
    case 'end_turn':
      if (tokensRemaining < maxTokens * 0.1) {
        return `Claude finished with 'end_turn' but used ${usagePercent}% of tokens (${usage.output_tokens}/${maxTokens}) - may have been constrained`;
      }
      return `Claude finished naturally with 'end_turn' - ${tokensRemaining} tokens remaining - truncation likely during structured output generation`;
    
    case 'max_tokens':
      return `Hit max_tokens limit (${maxTokens}) - response was cut off by token constraint`;
    
    case 'stop_sequence':
      return `Stopped due to stop_sequence - may indicate early termination`;
    
    default:
      return `Unexpected stop_reason: '${stopReason}' - requires investigation`;
  }
}
```

---

### Phase 4: Enhanced Error Report Generation

**Objective**: Generate comprehensive error reports with truncation analysis for easy diagnosis.

#### 4.1 Update `createErrorReport()` Method

**Location**: `src/lib/services/failed-generation-service.ts` (lines 382-440)

**Enhancement**: Add truncation-specific analysis section to error report.

**Required Changes**:
```typescript
private createErrorReport(input: CreateFailedGenerationInput, failureId: string): ErrorFileReport {
  const inputTokens = input.input_tokens || 0;
  const outputTokens = input.output_tokens || 0;
  const maxTokens = input.max_tokens;
  const tokensRemaining = maxTokens - outputTokens;

  // Analyze stop_reason
  let stopReasonAnalysis = 'Unknown';
  if (input.stop_reason === 'end_turn') {
    if (tokensRemaining < maxTokens * 0.1) {
      stopReasonAnalysis = `Claude finished with 'end_turn' but used ${Math.round((outputTokens/maxTokens)*100)}% of tokens - may have been constrained`;
    } else {
      stopReasonAnalysis = 'Claude finished naturally with end_turn, but content appears truncated - likely truncation during structured output JSON generation';
    }
  } else if (input.stop_reason === 'max_tokens') {
    stopReasonAnalysis = 'Claude hit max_tokens limit - response was cut off';
  } else if (!input.stop_reason) {
    stopReasonAnalysis = 'stop_reason not available - may indicate API error or missing field';
  } else {
    stopReasonAnalysis = `Unexpected stop_reason: '${input.stop_reason}' - requires investigation`;
  }

  // Determine conclusion
  let conclusion = '';
  if (input.stop_reason === 'max_tokens') {
    conclusion = `Truncation caused by max_tokens limit (${maxTokens})`;
  } else if (tokensRemaining > maxTokens * 0.8) {
    conclusion = `Truncation occurred FAR below max_tokens limit (used ${outputTokens}/${maxTokens} tokens) - root cause is structured output generation, not token limits`;
  } else {
    conclusion = 'Truncation cause unclear - review raw response and stop_reason';
  }

  // Extract truncation analysis from raw_response if available
  let truncationAnalysisSection = null;
  if (input.raw_response?.truncation_analysis) {
    truncationAnalysisSection = input.raw_response.truncation_analysis;
  }

  return {
    error_report: {
      failure_type: input.failure_type,
      stop_reason: input.stop_reason || null,
      stop_reason_analysis: stopReasonAnalysis,
      truncation_pattern: input.truncation_pattern || null,
      truncation_details: input.truncation_details || null,
      timestamp: new Date().toISOString(),
      analysis: {
        input_tokens: inputTokens,
        output_tokens: outputTokens,
        max_tokens_configured: maxTokens,
        tokens_remaining: tokensRemaining,
        conclusion,
      },
      // Add detailed truncation analysis if available
      ...(truncationAnalysisSection ? { truncation_analysis: truncationAnalysisSection } : {}),
    },
    request_context: {
      model: input.model,
      temperature: input.temperature || 0.7,
      max_tokens: maxTokens,
      structured_outputs_enabled: input.structured_outputs_enabled !== false,
      prompt_length: input.prompt.length,
    },
    raw_response: input.raw_response,
    extracted_content: input.response_content,
    scaffolding_context: {
      persona_id: input.persona_id,
      emotional_arc_id: input.emotional_arc_id,
      training_topic_id: input.training_topic_id,
      template_id: input.template_id,
    },
  };
}
```

**Enhanced ErrorFileReport Interface**:
```typescript
export interface ErrorFileReport {
  error_report: {
    failure_type: string;
    stop_reason: string | null;
    stop_reason_analysis: string;
    truncation_pattern: string | null;
    truncation_details: string | null;
    timestamp: string;
    analysis: {
      input_tokens: number;
      output_tokens: number;
      max_tokens_configured: number;
      tokens_remaining: number;
      conclusion: string;
    };
    // NEW: Detailed truncation analysis
    truncation_analysis?: {
      total_turns: number;
      total_assistant_turns: number;
      truncated_turns_count: number;
      truncated_turns: Array<{
        turn_number: number;
        turn_index: number;
        pattern: string;
        confidence: string;
        content_length: number;
        content_preview: string;
        is_last_assistant_turn: boolean;
      }>;
      summary: string;
      confidence: string;
    };
  };
  request_context: {
    model: string;
    temperature: number;
    max_tokens: number;
    structured_outputs_enabled: boolean;
    prompt_length: number;
  };
  raw_response: any;
  extracted_content: string;
  scaffolding_context?: {
    persona_id?: string;
    emotional_arc_id?: string;
    training_topic_id?: string;
    template_id?: string;
  };
}
```

---

### Phase 5: UI Enhancements for Failed Generations

**Objective**: Display truncation details in the Failed Generations UI for easy diagnosis.

#### 5.1 Update Failed Generations Table

**Location**: `src/app/(dashboard)/conversations/failed/page.tsx`

**Required Enhancement**: Add columns for truncation details.

**New Columns to Add**:
1. **Truncated Turns** - Show count and turn numbers
2. **Confidence** - Show truncation detection confidence
3. **Last Turn?** - Indicator if last assistant turn was truncated (high priority)

**Implementation** (conceptual - actual UI code will need adjustment):
```typescript
// Add to table columns
{
  header: 'Truncation Details',
  accessor: (row: FailedGeneration) => {
    if (row.failure_type !== 'truncation') return '-';
    
    const analysis = row.raw_response?.truncation_analysis;
    if (!analysis) {
      return row.truncation_pattern || 'Details unavailable';
    }
    
    return (
      <div className="text-sm">
        <div className="font-medium">
          {analysis.truncated_turns_count} turn(s) affected
        </div>
        <div className="text-muted-foreground">
          Turns: {analysis.truncated_turns.map(t => t.turn_number).join(', ')}
        </div>
        {analysis.truncated_turns.some(t => t.is_last_assistant_turn) && (
          <Badge variant="destructive" className="mt-1">
            Last turn truncated
          </Badge>
        )}
      </div>
    );
  },
},
{
  header: 'Confidence',
  accessor: (row: FailedGeneration) => {
    const analysis = row.raw_response?.truncation_analysis;
    if (!analysis) return '-';
    
    const variant = analysis.confidence === 'high' ? 'destructive' : 
                    analysis.confidence === 'medium' ? 'warning' : 'default';
    
    return <Badge variant={variant}>{analysis.confidence}</Badge>;
  },
}
```

---

## 📋 Implementation Checklist

### Phase 1: Pattern Enhancement (Priority: CRITICAL)
- [ ] Update `TRUNCATION_PATTERNS` in `truncation-detection.ts` with 3 enhanced patterns
- [ ] Implement `validateTruncationContext()` helper function
- [ ] Update `detectTruncatedContent()` to use context validation
- [ ] Add `TruncatedTurnDetail` and `ConversationTruncationAnalysis` interfaces
- [ ] Implement `analyzeConversationTruncation()` function
- [ ] Write unit tests for pattern matching (test valid vs truncated content)

### Phase 2: Validation Enhancement (Priority: CRITICAL)
- [ ] Update imports in `conversation-generation-service.ts`
- [ ] Update `TruncatedResponseError` class to accept analysis context
- [ ] Replace VALIDATION 3 with enhanced version using `analyzeConversationTruncation()`
- [ ] Add detailed logging for truncation events
- [ ] Implement `analyzeStopReason()` helper function

### Phase 3: Storage Enhancement (Priority: HIGH)
- [ ] Update `storeFailedGeneration()` to extract and store truncation analysis
- [ ] Add `analyzeStopReason()` function to generation service
- [ ] Test failed generation storage with mock truncated data
- [ ] Verify `raw_response` JSONB field stores truncation_analysis correctly

### Phase 4: Reporting Enhancement (Priority: HIGH)
- [ ] Update `createErrorReport()` in `failed-generation-service.ts`
- [ ] Update `ErrorFileReport` interface with `truncation_analysis` field
- [ ] Test error report generation with truncation data
- [ ] Verify error report JSON structure in storage bucket

### Phase 5: UI Enhancement (Priority: MEDIUM)
- [ ] Update Failed Generations table columns
- [ ] Add truncation details display component
- [ ] Add confidence badge component
- [ ] Test UI with mock failed generations

### Phase 6: Testing & Validation (Priority: CRITICAL)
- [ ] Create test script to generate intentionally truncated content
- [ ] Test pattern matching with historical truncated files
- [ ] Verify failed generations are stored correctly
- [ ] Verify `/conversations/failed` page shows truncation details
- [ ] Test false positive scenarios (valid escaped quotes)
- [ ] Verify `stop_reason` is captured and displayed correctly

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

# Check failed generations (NEW)
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'failed_generations',select:'id,failure_type,stop_reason,truncation_pattern,created_at',orderBy:[{column:'created_at',asc:false}],limit:10});console.log('Failed generations:',r.data.length);console.log(JSON.stringify(r.data,null,2));})();"
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

**Check failed generations with truncation details** (NEW):
```bash
cd "c:/Users/james/Master/BrightHub/BRun/lora-pipeline/supa-agent-ops" && node -e "require('dotenv').config({path:'../.env.local'});const saol=require('.');(async()=>{const r=await saol.agentQuery({table:'failed_generations',select:'*',where:[{column:'failure_type',operator:'eq',value:'truncation'}],orderBy:[{column:'created_at',asc:false}],limit:5});console.log('Truncated generations:',r.data.length);r.data.forEach(f=>{console.log('-',f.id.slice(0,8),'/',f.stop_reason,'/',f.truncation_pattern);if(f.raw_response?.truncation_analysis){console.log('  Turns affected:',f.raw_response.truncation_analysis.truncated_turns_count);}});})();"
```

### SAOL Parameter Formats (Both Work)

**Recommended Format** (clear intent):
```javascript
const result = await saol.agentQuery({
  table: 'failed_generations',
  select: ['id', 'failure_type', 'stop_reason', 'truncation_pattern'],
  where: [{ column: 'failure_type', operator: 'eq', value: 'truncation' }],
  orderBy: [{ column: 'created_at', asc: false }]
});
```

**Backward Compatible Format**:
```javascript
const result = await saol.agentQuery({
  table: 'failed_generations',
  select: 'id,failure_type,stop_reason,truncation_pattern',
  filters: [{ field: 'failure_type', operator: 'eq', value: 'truncation' }],
  orderBy: [{ column: 'created_at', asc: false }]
});
```

---

## 📋 Project Context

### What This Application Does

**BrightHub BRun LoRA Training Data Platform** - A Next.js 14 application that generates emotionally-intelligent financial planning training conversations for LoRA fine-tuning.

### Production Pipeline

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
│    ⚠️  NEEDS FIX: Truncation detection                      │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. VALIDATION & QUALITY CHECK (Enhanced Truncation)         │
│    → validateAPIResponse() with turn-level analysis         │
│    → Comprehensive truncation detection                     │
│    → Failed generations storage                             │
│    🔄 TO BE ENHANCED per this specification                 │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. ENRICHMENT (Metadata Addition)                           │
│    → enrichment-pipeline-orchestrator.ts                    │
│    → conversation-enrichment-service.ts                     │
│    → Output: Enriched JSON with training_pairs[]            │
│    → Stored in: conversation-files/{userId}/{id}/enriched.json│
│    ✅ Working                                                │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. TRAINING FILE AGGREGATION                                │
│    → training-file-service.ts                               │
│    → Combines multiple enriched files into one              │
│    → Output: Full JSON + JSONL in brightrun-lora-v4 format  │
│    → Stored in: training-files/{fileId}/training.json       │
│    ✅ Working                                                │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Database**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage (buckets: conversation-files, training-files, failed-generation-files)
- **AI**: Claude API (Anthropic) - `claude-sonnet-4-5-20250929`
- **Structured Outputs**: `anthropic-beta: structured-outputs-2025-11-13`
- **UI**: Shadcn/UI + Tailwind CSS
- **Deployment**: Vercel

---

## 📁 Key Files Reference

### Files to Modify (Implementation Order)

| Priority | File | Changes Required |
|----------|------|------------------|
| 1 | `src/lib/utils/truncation-detection.ts` | Enhanced pattern matching + context validation |
| 2 | `src/lib/services/conversation-generation-service.ts` | Update validation logic + error context |
| 3 | `src/lib/services/failed-generation-service.ts` | Enhanced error report generation |
| 4 | `src/app/(dashboard)/conversations/failed/page.tsx` | UI enhancements for truncation details |

### Database Tables

| Table | Purpose | Key Columns for This Spec |
|-------|---------|---------------------------|
| `failed_generations` | Failed generation storage | `stop_reason`, `truncation_pattern`, `truncation_details`, `raw_response` (JSONB) |
| `conversations` | Generated conversations | `id`, `conversation_id`, `status`, `enrichment_status` |

### Storage Buckets

| Bucket | Purpose |
|--------|---------|
| `failed-generation-files` | Error report JSON files with truncation analysis |
| `conversation-files` | Raw and enriched conversation files |

---

## 🎯 Success Criteria

### After Implementation

- [ ] Enhanced pattern matching reduces false positives
- [ ] True truncations at end-of-response are caught reliably
- [ ] `stop_reason` is captured and stored for every failed generation
- [ ] Truncation analysis includes:
  - [ ] Which turns are truncated (turn numbers)
  - [ ] Which patterns were detected
  - [ ] Whether last assistant turn was truncated
  - [ ] Confidence level of detection
  - [ ] Content previews for diagnosis
- [ ] Failed generations table populated with comprehensive metadata
- [ ] Error reports include `truncation_analysis` section
- [ ] UI displays truncation details clearly
- [ ] No truncated conversations reach enrichment or training files

### Validation Queries

**Check failed generations count**:
```sql
SELECT COUNT(*) FROM failed_generations WHERE failure_type = 'truncation';
```

**Check truncation analysis storage**:
```sql
SELECT 
  id,
  stop_reason,
  truncation_pattern,
  raw_response->'truncation_analysis' as analysis
FROM failed_generations 
WHERE failure_type = 'truncation'
ORDER BY created_at DESC
LIMIT 5;
```

**Check stop_reason distribution**:
```sql
SELECT 
  stop_reason, 
  COUNT(*) as count 
FROM failed_generations 
WHERE failure_type = 'truncation'
GROUP BY stop_reason
ORDER BY count DESC;
```

---

## 🚨 Critical Notes for Implementation

### 1. Pattern Matching Balance

**Challenge**: Must balance sensitivity vs. specificity
- Too sensitive → False positives (flagging valid content)
- Too specific → False negatives (missing truncations)

**Strategy**: Use multi-pattern approach + context validation
- Primary pattern: `[^"]\\"\s*$` (unmatched escaped quote)
- Secondary patterns: word-level, escape-level
- Context validation: quote counting, length checks, sentence structure

### 2. Structured Outputs Behavior

**Key Insight**: Claude with structured outputs ALWAYS returns valid JSON
- The JSON structure will close properly (brackets, braces)
- Truncation occurs INSIDE string content fields
- `stop_reason` is often `end_turn` even with truncated content
- Token usage is typically LOW (not hitting `max_tokens`)

**Implication**: Cannot rely on `stop_reason` alone to detect truncation

### 3. False Positive Prevention

**Common False Positive Scenarios**:
1. Valid escaped quotes in dialogue: `"She said \"hello\" and I replied"`
2. Intentional quote at end: `"The term is called \"front-loading\""`
3. Short test content: `"test \"quote\""`

**Mitigation**:
- Check quote pairing (odd vs. even count)
- Require minimum content length (50+ chars)
- Exclude content ending with complete sentence patterns
- Prioritize last assistant turn (most likely to be truncated)

### 4. Backward Compatibility

**Existing System**:
- `detectTruncatedTurns()` already exists and is called
- Current pattern: `/\\"\s*$/` (simple escaped quote match)
- No context validation

**Migration Path**:
- Keep `detectTruncatedTurns()` function signature
- Enhance `detectTruncatedContent()` internally
- Add new `analyzeConversationTruncation()` as optional upgrade
- Ensure existing error handling still works

---

## 📊 Testing Strategy

### Unit Tests

**Test File**: `src/lib/utils/__tests__/truncation-detection.test.ts`

**Test Cases**:
1. **True Positives** (should detect truncation):
   - Content ending with `\\"` and no preceding quote
   - Content ending with `\\` followed by word
   - Last assistant turn truncated
   - Multiple turns truncated

2. **True Negatives** (should NOT detect truncation):
   - Valid escaped quotes in middle: `"I said \"hello\" and left"`
   - Complete sentences: `"This is a complete thought."`
   - Short test strings: `"test"`
   - Proper quote pairing: `"She said \"I'm ready\" to me"`

3. **Edge Cases**:
   - Empty content
   - Single character content
   - Content with only whitespace
   - Content with multiple escape sequences

### Integration Tests

**Test Scenarios**:
1. Generate conversation with mock truncated response
2. Verify `validateAPIResponse()` throws `TruncatedResponseError`
3. Verify failed generation is stored with analysis
4. Verify error report contains `truncation_analysis` section
5. Verify UI displays truncation details

### Manual Testing

**Using Historical Truncated File**:
```bash
# Copy single-convo-file-3-RAW.json to test directory
# Run generation service with this as mock response
# Verify detection and storage
```

---

## 🔄 Rollback Plan

**If Enhanced Detection Causes Issues**:

1. **Phase 1 Rollback** (Pattern Matching):
   - Revert `TRUNCATION_PATTERNS` to single pattern: `/\\"\s*$/`
   - Remove context validation function
   - Keep existing `detectTruncatedContent()` implementation

2. **Phase 2 Rollback** (Validation):
   - Revert to simple turn detection without analysis
   - Keep `TruncatedResponseError` as-is
   - Remove `analyzeConversationTruncation()` call

3. **Phase 3 Rollback** (Storage):
   - Remove `truncation_analysis` from `raw_response`
   - Keep basic `truncation_pattern` and `truncation_details`
   - Existing schema supports both approaches

**No Database Migration Required** - All enhancements use existing JSONB fields

---

## 📝 Next Agent Instructions

**Read This Specification Completely** before starting implementation.

**Implementation Order**:
1. Start with Phase 1 (pattern enhancement) - most critical
2. Write unit tests for new patterns
3. Move to Phase 2 (validation enhancement)
4. Test with historical truncated file
5. Implement Phase 3 (storage enhancement)
6. Verify failed generation records
7. Implement Phase 4 (reporting enhancement)
8. Implement Phase 5 (UI enhancement) last

**Validation at Each Phase**:
- Run unit tests after pattern changes
- Test with mock data after validation changes
- Check database after storage changes
- Review error reports after reporting changes
- Manually test UI after UI changes

**Success Indicators**:
- Historical truncated file (`single-convo-file-3-RAW.json`) IS detected as truncated
- Valid content with escaped quotes is NOT flagged
- Failed generations table has comprehensive metadata
- Error reports show detailed truncation analysis
- UI displays truncation details clearly

**Critical**: This specification is based on actual codebase and database state verified on December 7, 2025. All file paths, function names, line numbers, and schema details are accurate as of this date.

---

**Last Updated**: December 7, 2025  
**Document Version**: gg (enhanced truncation detection specification)  
**Status**: Ready for Implementation  
**Estimated Implementation Time**: 4-6 hours (all phases)
