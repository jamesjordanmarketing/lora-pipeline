# Bug Fix: React Query refetchInterval Type Error

**Date:** December 26, 2025  
**Issue:** Vercel build failure due to TypeScript error in `useTrainingConfig.ts`  
**Status:** ✅ FIXED

---

## Error Details

**Build Error:**
```
Type error: Property 'data' does not exist on type 'Query<any, Error, any, string[]>'.

./hooks/useTrainingConfig.ts:106:28
const status = data?.data?.status;
               ^^^^
```

**Root Cause:** 
The `refetchInterval` callback in React Query v5 receives a query object, not the data directly. The parameter was incorrectly typed, causing TypeScript to fail during build.

---

## Fix Applied

**File:** `src/hooks/useTrainingConfig.ts`

**Before (Incorrect):**
```typescript
refetchInterval: (data) => {
  const status = data?.data?.status;
  return status === 'running' || status === 'queued' || status === 'initializing' 
    ? 5000 
    : false;
},
```

**After (Correct):**
```typescript
refetchInterval: (query: any) => {
  // Poll every 5 seconds if job is active
  // In React Query v5, refetchInterval callback receives the query object
  const responseData = query.state?.data;
  const status = responseData?.data?.status;
  return status === 'running' || status === 'queued' || status === 'initializing' 
    ? 5000 
    : false;
},
```

**Key Changes:**
1. Changed parameter name from `data` to `query` (more descriptive)
2. Added explicit type annotation: `query: any`
3. Access data through `query.state?.data` (React Query v5 API)
4. Added safe navigation operator `?.` for `query.state`

---

## React Query v5 API Notes

In React Query v5, the `refetchInterval` callback receives a `Query` object with this structure:

```typescript
{
  state: {
    data: any,           // The actual query data
    error: Error,
    status: string,
    // ... other state properties
  },
  // ... other query properties
}
```

To access the API response data, use: `query.state?.data`

---

## Verification

**Local Build:** ✅ Passed
```bash
cd src && npm run build
# ✓ Compiled successfully
```

**TypeScript Check:** ✅ No errors
```bash
# No linter errors found in:
# - src/hooks/useTrainingConfig.ts
# - src/app/(dashboard)/training/configure/page.tsx
# - src/app/api/jobs/estimate/route.ts
# - src/app/api/jobs/route.ts
```

---

## Files Modified

- `src/hooks/useTrainingConfig.ts` - Fixed `useTrainingJob` hook `refetchInterval` callback

---

## Next Steps

1. Commit the fix: `git add src/hooks/useTrainingConfig.ts`
2. Commit message: `fix: correct refetchInterval callback type in useTrainingJob hook`
3. Push to GitHub: `git push origin main`
4. Vercel will auto-deploy with the fix

---

**End of Bug Fix Summary**

