# PIPELINE - Section E06: Cost Tracking & Notifications - Execution Prompts

**Product:** PIPELINE  
**Section:** 6 - Cost Tracking & Notifications  
**Generated:** 2025-12-24  
**Total Prompts:** 1  
**Estimated Total Time:** 3-5 hours  
**Source Section File:** 04f-pipeline-build-section-E06.md

---

## Section Overview

Track training costs in real-time and notify users of important events throughout the training lifecycle.

**User Value**: Transparent cost tracking and timely notifications keep users informed and in control

This section implements two simple API endpoints that expose data already being collected throughout the training lifecycle. Cost records and notifications are created by earlier sections (3-5), and this section provides the read/query interfaces.

---

## Prompt Sequence for This Section

This section has been divided into **1 progressive prompt**:

1. **Prompt P01: Cost & Notification APIs** (3-5h)
   - Features: FR-6.1 (Cost Dashboard API), FR-6.2 (Notifications API)
   - Key Deliverables: 
     - `GET /api/costs` - cost analytics with aggregation
     - `GET /api/notifications` - list notifications
     - `PATCH /api/notifications/[id]/read` - mark as read

---

## Integration Context

### Dependencies from Previous Sections

This section relies on data created by earlier sections:

#### Section E01: Foundation & Authentication
- **Tables**: `lora_cost_records`, `lora_notifications`
- **Auth**: `requireAuth()` from `@/lib/supabase-server`
- **Database Client**: `createServerSupabaseClient()`

#### Section E03: Training Configuration
- **Cost Records**: Created when jobs are queued with estimated costs

#### Section E04: Training Execution & Monitoring
- **Cost Records**: Updated during job execution with actual costs
- **Notifications**: Created for job lifecycle events (started, failed, completed)

#### Section E05: Model Artifacts & Delivery
- **Notifications**: Created when artifacts are ready for download

### Provides for Next Sections

This section completes the core training pipeline. Future enhancements could add:
- UI components for cost dashboard visualization
- UI components for notification bell/dropdown
- Real-time notification updates via WebSockets
- Cost alerting and budget management

---

## Dependency Flow (This Section)

```
Section E01 (Tables) → Section E06-P01 (Read APIs)
    ↓
Section E03-E05 (Write Cost/Notification Records)
    ↓
Section E06-P01 (Query & Display)
```

**Note**: This section is purely read-only. All data is written by earlier sections.

---

# PROMPT 1: Cost & Notification APIs

**Generated:** 2025-12-24  
**Section:** 6 - Cost Tracking & Notifications  
**Prompt:** 1 of 1 in this section  
**Estimated Time:** 3-5 hours  
**Prerequisites:** 
- Section E01: Database tables (`lora_cost_records`, `lora_notifications`)
- Section E03-E05: Cost records and notifications being created

---

## 🎯 Mission Statement

Implement read-only API endpoints for querying cost analytics and user notifications. These APIs aggregate and expose data that's already being collected throughout the training lifecycle, providing users with transparent cost tracking and timely notifications about their training jobs.

---

## 📦 Section Context

### This Section's Goal

Track training costs in real-time and notify users of important events throughout the training lifecycle. This section provides the query interfaces for data already being written by earlier sections.

### This Prompt's Scope

This is **Prompt 1 of 1** in Section E06. It implements:
- FR-6.1: Cost Dashboard API (aggregate cost data for analytics)
- FR-6.2: Notifications API (fetch and manage notifications)

---

## 🔗 Integration with Previous Work

### From Previous Sections

#### Section E01: Foundation & Authentication
**Database Tables We'll Query:**
- `lora_cost_records` - Stores cost data for training jobs
  - Schema: `id`, `user_id`, `job_id`, `cost_type`, `amount`, `details`, `billing_period`, `recorded_at`
  - Used for: Aggregating costs by period, type, and job
  
- `lora_notifications` - Stores user notifications
  - Schema: `id`, `user_id`, `type`, `title`, `message`, `priority`, `read`, `action_url`, `metadata`, `created_at`
  - Used for: Fetching user notifications with unread count

**Auth We'll Use:**
- `requireAuth()` from `@/lib/supabase-server` - Authenticate all API requests
- `createServerSupabaseClient()` - Database client for queries

#### Section E03: Training Configuration
**Cost Records Created:**
- Initial estimated cost recorded when job is created (status: 'queued')

#### Section E04: Training Execution & Monitoring
**Cost Records Created:**
- Cost records updated during job execution
- Compute costs tracked per training step
- Notifications created for job lifecycle events:
  - `job_started` - When training begins
  - `job_failed` - When training fails
  - `job_cancelled` - When user cancels

#### Section E05: Model Artifacts & Delivery
**Notifications Created:**
- `artifact_ready` - When model is ready for download

### From Previous Prompts (This Section)

This is the first (and only) prompt in Section E06. No previous prompts in this section.

---

## 🎯 Implementation Requirements

### Feature FR-6.1: Cost Dashboard API

**Type:** API Endpoint  
**Strategy:** EXTENSION - using existing Supabase patterns

#### Description

Aggregate cost data for analytics and budget tracking. Provide filtering by time period, cost breakdown by type, and chart data for visualization.

#### What Already Exists (Don't Rebuild)

- ✅ `lora_cost_records` table (from Section E01)
- ✅ Cost records being created throughout Sections E03-E05
- ✅ Supabase Auth and database client patterns
- ✅ API response format (`{ success, data }` or `{ error, details }`)

#### What We're Building (New in This Prompt)

- 🆕 `src/app/api/costs/route.ts` - GET endpoint for cost analytics

#### Implementation Details

**File:** `src/app/api/costs/route.ts`

**Endpoint:** `GET /api/costs`

**Query Parameters:**
- `period` - Time period filter: `week`, `month`, `year` (default: `month`)
- `start_date` - Custom date range start (ISO 8601 format)
- `end_date` - Custom date range end (ISO 8601 format)

**Response Schema:**

```typescript
{
  success: true,
  data: {
    total_cost: number,              // Total cost for period
    cost_by_type: {                  // Breakdown by cost type
      [cost_type: string]: number
    },
    chart_data: Array<{              // Data for charts
      date: string,
      amount: number
    }>,
    records: Array<CostRecord>       // Individual cost records
  }
}
```

**Implementation:**

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * GET /api/costs - Get cost analytics with filtering
 */
export async function GET(request: NextRequest) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = createServerSupabaseClient();
    const { searchParams } = new URL(request.url);
    
    const period = searchParams.get('period') || 'month'; // month, week, year
    const startDate = searchParams.get('start_date');
    const endDate = searchParams.get('end_date');

    // Calculate date range
    let dateFilter;
    if (startDate && endDate) {
      dateFilter = { gte: startDate, lte: endDate };
    } else {
      const now = new Date();
      if (period === 'week') {
        const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        dateFilter = { gte: weekAgo.toISOString() };
      } else if (period === 'year') {
        const yearAgo = new Date(now.getTime() - 365 * 24 * 60 * 60 * 1000);
        dateFilter = { gte: yearAgo.toISOString() };
      } else {
        // month (default)
        const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        dateFilter = { gte: monthAgo.toISOString() };
      }
    }

    // Fetch cost records
    const { data: costs, error } = await supabase
      .from('lora_cost_records')
      .select('*')
      .eq('user_id', user.id)
      .gte('recorded_at', dateFilter.gte)
      .order('recorded_at', { ascending: true });

    if (error) {
      return NextResponse.json(
        { error: 'Failed to fetch costs', details: error.message },
        { status: 500 }
      );
    }

    // Calculate aggregates
    const totalCost = costs?.reduce((sum, record) => sum + parseFloat(record.amount), 0) || 0;
    const byType = costs?.reduce((acc: any, record) => {
      acc[record.cost_type] = (acc[record.cost_type] || 0) + parseFloat(record.amount);
      return acc;
    }, {});

    // Group by day for chart data
    const byDay = costs?.reduce((acc: any, record) => {
      const date = record.recorded_at.split('T')[0];
      acc[date] = (acc[date] || 0) + parseFloat(record.amount);
      return acc;
    }, {});

    const chartData = Object.entries(byDay || {}).map(([date, amount]) => ({
      date,
      amount,
    }));

    return NextResponse.json({
      success: true,
      data: {
        total_cost: parseFloat(totalCost.toFixed(2)),
        cost_by_type: byType,
        chart_data: chartData,
        records: costs || [],
      },
    });
  } catch (error: any) {
    console.error('Costs fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch costs', details: error.message },
      { status: 500 }
    );
  }
}
```

**Key Points:**
- Uses: `requireAuth()` from Section E01
- Queries: `lora_cost_records` table (created in Section E01)
- Returns: Aggregated cost data with breakdown by type and date
- Date filtering: Flexible period filters or custom date ranges
- Performance: Efficient aggregation in application layer (could be moved to DB for large datasets)

**Pattern Source**: Infrastructure Inventory Section 4 (API Architecture)

---

### Feature FR-6.2: Notifications API

**Type:** API Endpoints  
**Strategy:** EXTENSION - using existing Supabase patterns

#### Description

Fetch and manage user notifications. Provide listing with unread filtering and mark-as-read functionality.

#### What Already Exists (Don't Rebuild)

- ✅ `lora_notifications` table (from Section E01)
- ✅ Notifications being created throughout Sections E03-E05
- ✅ Supabase Auth and database client patterns
- ✅ API response format

#### What We're Building (New in This Prompt)

- 🆕 `src/app/api/notifications/route.ts` - GET endpoint for listing notifications
- 🆕 `src/app/api/notifications/[id]/read/route.ts` - PATCH endpoint for marking as read

#### Implementation Details

**File 1:** `src/app/api/notifications/route.ts`

**Endpoint:** `GET /api/notifications`

**Query Parameters:**
- `unread` - Filter to unread only: `true` or `false` (default: false = all)
- `limit` - Number of notifications to return (default: 20, max: 50)

**Response Schema:**

```typescript
{
  success: true,
  data: {
    notifications: Array<Notification>,
    unread_count: number
  }
}
```

**Implementation:**

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * GET /api/notifications - Get user notifications
 */
export async function GET(request: NextRequest) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = createServerSupabaseClient();
    const { searchParams } = new URL(request.url);
    
    const unreadOnly = searchParams.get('unread') === 'true';
    const limit = parseInt(searchParams.get('limit') || '20');

    let query = supabase
      .from('lora_notifications')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false })
      .limit(limit);

    if (unreadOnly) {
      query = query.eq('read', false);
    }

    const { data: notifications, error } = await query;

    if (error) {
      return NextResponse.json(
        { error: 'Failed to fetch notifications', details: error.message },
        { status: 500 }
      );
    }

    // Count unread
    const { count: unreadCount } = await supabase
      .from('lora_notifications')
      .select('*', { count: 'exact', head: true })
      .eq('user_id', user.id)
      .eq('read', false);

    return NextResponse.json({
      success: true,
      data: {
        notifications: notifications || [],
        unread_count: unreadCount || 0,
      },
    });
  } catch (error: any) {
    console.error('Notifications fetch error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch notifications', details: error.message },
      { status: 500 }
    );
  }
}
```

**File 2:** `src/app/api/notifications/[id]/read/route.ts`

**Endpoint:** `PATCH /api/notifications/[id]/read`

**Response Schema:**

```typescript
{ success: true }
```

**Implementation:**

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { requireAuth, createServerSupabaseClient } from '@/lib/supabase-server';

/**
 * PATCH /api/notifications/[id]/read - Mark notification as read
 */
export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { user, response } = await requireAuth(request);
    if (response) return response;

    const supabase = createServerSupabaseClient();

    const { error } = await supabase
      .from('lora_notifications')
      .update({ read: true })
      .eq('id', params.id)
      .eq('user_id', user.id);

    if (error) {
      return NextResponse.json(
        { error: 'Failed to update notification', details: error.message },
        { status: 500 }
      );
    }

    return NextResponse.json({ success: true });
  } catch (error: any) {
    console.error('Notification update error:', error);
    return NextResponse.json(
      { error: 'Failed to update notification', details: error.message },
      { status: 500 }
    );
  }
}
```

**Key Points:**
- Uses: `requireAuth()` from Section E01
- Queries: `lora_notifications` table (created in Section E01)
- Returns: Notifications list with unread count
- Update: Marks individual notifications as read
- Security: User can only access their own notifications (enforced by RLS and query filter)

**Pattern Source**: Infrastructure Inventory Section 4 (API Architecture)

---

## ✅ Acceptance Criteria

### Functional Requirements

- [ ] **FR-6.1**: Cost Dashboard API returns aggregated cost data
  - [ ] Supports period filters: `week`, `month`, `year`
  - [ ] Supports custom date range with `start_date` and `end_date`
  - [ ] Returns total cost for period
  - [ ] Returns cost breakdown by type
  - [ ] Returns chart data grouped by day
  - [ ] Returns individual cost records

- [ ] **FR-6.2**: Notifications API provides notification management
  - [ ] Returns user's notifications with pagination (limit)
  - [ ] Supports filtering to unread only
  - [ ] Returns unread count
  - [ ] Mark as read endpoint updates notification status
  - [ ] Users can only access their own notifications

### Technical Requirements

- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Follows existing API patterns from Sections E02-E05
- [ ] All imports resolve correctly
- [ ] Code matches specification exactly
- [ ] Proper error handling for database errors
- [ ] Consistent response format (`{ success, data }` or `{ error, details }`)

### Integration Requirements

- [ ] Successfully authenticates using `requireAuth()` from Section E01
- [ ] Successfully queries `lora_cost_records` table
- [ ] Successfully queries `lora_notifications` table
- [ ] RLS policies enforce user data isolation
- [ ] Date filtering works correctly for all period options
- [ ] Aggregation calculations are accurate

---

## 🧪 Testing & Validation

### Manual Testing Steps

1. **Cost API Testing**
   
   Test default period (month):
   ```bash
   curl http://localhost:3000/api/costs \
     -H "Cookie: [auth-cookie]"
   ```
   
   Test custom date range:
   ```bash
   curl "http://localhost:3000/api/costs?start_date=2024-01-01&end_date=2024-12-31" \
     -H "Cookie: [auth-cookie]"
   ```
   
   Test week period:
   ```bash
   curl "http://localhost:3000/api/costs?period=week" \
     -H "Cookie: [auth-cookie]"
   ```
   
   Expected response:
   ```json
   {
     "success": true,
     "data": {
       "total_cost": 45.32,
       "cost_by_type": {
         "compute": 42.50,
         "storage": 2.82
       },
       "chart_data": [
         { "date": "2024-12-01", "amount": 15.20 },
         { "date": "2024-12-02", "amount": 30.12 }
       ],
       "records": [...]
     }
   }
   ```

2. **Notifications API Testing**
   
   Get all notifications:
   ```bash
   curl http://localhost:3000/api/notifications \
     -H "Cookie: [auth-cookie]"
   ```
   
   Get unread only:
   ```bash
   curl "http://localhost:3000/api/notifications?unread=true" \
     -H "Cookie: [auth-cookie]"
   ```
   
   Mark notification as read:
   ```bash
   curl -X PATCH http://localhost:3000/api/notifications/[notification-id]/read \
     -H "Cookie: [auth-cookie]"
   ```
   
   Expected response:
   ```json
   {
     "success": true,
     "data": {
       "notifications": [...],
       "unread_count": 3
     }
   }
   ```

3. **Database Verification**
   
   Verify cost records exist:
   ```sql
   SELECT * FROM lora_cost_records 
   WHERE user_id = '[your-user-id]'
   ORDER BY recorded_at DESC
   LIMIT 10;
   ```
   
   Verify notifications exist:
   ```sql
   SELECT * FROM lora_notifications 
   WHERE user_id = '[your-user-id]'
   ORDER BY created_at DESC
   LIMIT 10;
   ```

4. **Integration Testing**
   
   - Complete a training job (from Section E03-E04)
   - Verify cost records are created
   - Call `/api/costs` to see aggregated costs
   - Verify notifications are created for job events
   - Call `/api/notifications` to see notifications
   - Mark a notification as read
   - Verify unread count decreases

### Expected Outputs

After completing this prompt, you should have:
- [ ] All files created at specified paths
- [ ] Application runs without errors
- [ ] All API endpoints testable and working
- [ ] Cost aggregation accurate
- [ ] Notifications queried successfully
- [ ] Mark as read functionality works

---

## 📦 Deliverables Checklist

### New Files Created

- [ ] `src/app/api/costs/route.ts` - Cost analytics API
- [ ] `src/app/api/notifications/route.ts` - Notifications list API
- [ ] `src/app/api/notifications/[id]/read/route.ts` - Mark as read API

### Existing Files Modified

None - this prompt only creates new API routes.

### Database Changes

None - this prompt only reads from existing tables.

### API Endpoints

- [ ] `GET /api/costs` - Get cost analytics with aggregation
  - Query params: `period` (week/month/year), `start_date`, `end_date`
  - Returns: Total cost, breakdown by type, chart data, records

- [ ] `GET /api/notifications` - Get user notifications
  - Query params: `unread` (true/false), `limit` (number)
  - Returns: Notifications array, unread count

- [ ] `PATCH /api/notifications/[id]/read` - Mark notification as read
  - Returns: Success status

---

## 🔜 What's Next

### For Next Prompt in This Section

**Section Complete:** This is the final prompt in Section E06.

### For Next Section

**Next Section:** E07 (if applicable) or Section Complete

This section completes the core training pipeline APIs. The cost and notification data is now queryable and ready for UI integration. Future enhancements could include:

- UI components for cost dashboard with charts
- UI components for notification bell/dropdown
- Real-time notification updates
- Cost alerting and budget management
- Export functionality for cost reports

**Integration Points for Future UI:**
- Cost dashboard page will call `GET /api/costs`
- Notification bell will call `GET /api/notifications?unread=true`
- Notification dropdown will call `PATCH /api/notifications/[id]/read`

---

## ⚠️ Important Reminders

1. **Follow the Spec Exactly:** All code provided in this prompt comes from the integrated specification. Implement it as written.

2. **Reuse Existing Infrastructure:** Don't recreate what already exists. Import and use:
   - `requireAuth()` from `@/lib/supabase-server` (Section E01)
   - `createServerSupabaseClient()` from `@/lib/supabase-server` (Section E01)
   - Existing API response format pattern
   - Existing error handling pattern

3. **Data Already Exists:** This section only reads data. Cost records and notifications are created by Sections E03-E05. If no data appears:
   - Verify earlier sections are working correctly
   - Check that training jobs are creating cost records
   - Check that notifications are being inserted

4. **Pattern Consistency:** Match existing patterns:
   - API responses: `{ success: true, data }` or `{ error, details }`
   - File organization: Follow existing structure
   - Error handling: Log errors, return meaningful messages
   - Query patterns: Use Supabase client consistently

5. **Don't Skip Steps:** Implement all endpoints listed in this prompt before moving to the next section.

6. **Security:** RLS policies on both tables ensure users can only access their own data. The API routes also filter by `user_id` for defense in depth.

---

## 📚 Reference Materials

### Files from Previous Work

#### Section E01: Foundation & Authentication
- `supabase/migrations/20241223_create_lora_training_tables.sql` - Database schema
- `src/lib/types/lora-training.ts` - TypeScript interfaces
- `src/lib/supabase-server.ts` - Auth and database utilities

#### Section E03: Training Configuration
- `src/app/api/jobs/route.ts` - Example of API pattern with cost records

#### Section E04: Training Execution & Monitoring
- `supabase/functions/process-training-jobs/index.ts` - Creates cost records and notifications

#### Section E05: Model Artifacts & Delivery
- `supabase/functions/create-model-artifacts/index.ts` - Creates artifact_ready notifications

### Infrastructure Patterns

- **Authentication:** `requireAuth()` pattern for all API routes
- **Database:** Supabase client pattern with RLS policies
- **API:** Route handler pattern with error handling
- **Response Format:** `{ success: true, data }` or `{ error, details }`

### Database Schema Reference

**lora_cost_records:**
```sql
CREATE TABLE lora_cost_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES lora_training_jobs(id) ON DELETE SET NULL,
  cost_type VARCHAR(50) NOT NULL,
  amount DECIMAL(10, 2) NOT NULL,
  details JSONB,
  billing_period DATE NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT NOW()
);
```

**lora_notifications:**
```sql
CREATE TABLE lora_notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  title VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  priority VARCHAR(20) DEFAULT 'medium',
  read BOOLEAN DEFAULT FALSE,
  action_url TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Section Completion Checklist

After completing all prompts in this section:

- [ ] All API endpoints implemented and tested
- [ ] Cost aggregation returns accurate data
- [ ] Notifications can be queried and marked as read
- [ ] Authentication working on all endpoints
- [ ] RLS policies enforcing data isolation
- [ ] Date filtering working for all period options
- [ ] No TypeScript errors
- [ ] No linter warnings
- [ ] Integration with previous sections verified
- [ ] Ready to build UI components (future work)

---

**End of Section E06 Execution Prompts**

