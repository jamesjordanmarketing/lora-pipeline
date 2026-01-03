# Next Steps Summary

**Date**: January 2, 2026  
**Status**: Documentation updated for EU-RO-1 storage

---

## ✅ What's Been Updated

### 1. Storage Configuration Files
- ✅ `deployment-secrets.md` - Updated volume ID and S3 endpoint
- ✅ `docker-urls-and-edge-changes_v1.md` - Updated Step 4 with new storage
- ✅ `04f-pipeline-post-build-section-X01-runpod-connect_v1.md` - Updated problem summary

### 2. Docker Worker Code
- ✅ `handler.py` (in workfiles directory) - Added boto3, S3 upload function, modified return statement

### 3. RunPod Endpoint
- ✅ Environment variables updated (you completed this)

---

## ❌ Other Storage Changes Needed?

### Supabase
**No changes needed.**
- Supabase doesn't store or reference the RunPod storage volume ID
- Edge Functions use RunPod API endpoints only
- No S3 bucket references in Supabase

### Vercel
**No changes needed.**
- Next.js app doesn't directly access RunPod storage
- All RunPod interactions go through Supabase Edge Functions
- Frontend only receives download URLs from Edge Functions

---

## 🔴 CRITICAL: What's Still Needed

### 1. Copy Updated handler.py to Docker Worker Directory

**Action Required:**
```bash
# Copy from workfiles to actual Docker worker directory
copy C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_mapping\pipeline\workfiles\handler.py C:\Users\james\Master\BrightHub\BRun\brightrun-trainer\handler.py
```

**Or manually:**
1. Open `C:\Users\james\Master\BrightHub\BRun\lora-pipeline\pmc\product\_mapping\pipeline\workfiles\handler.py`
2. Copy all contents
3. Open `C:\Users\james\Master\BrightHub\BRun\brightrun-trainer\handler.py`
4. Replace all contents with copied code
5. Save

### 2. Verify boto3 in requirements.txt

**Check:**
```bash
# Navigate to Docker worker directory
cd C:\Users\james\Master\BrightHub\BRun\brightrun-trainer

# Check requirements.txt
type requirements.txt
```

**Add if missing:**
```
boto3
```

### 3. Rebuild Docker Image (YES, REQUIRED)

**Why?** The updated handler.py with S3 upload code must be built into the Docker image.

**Commands:**
```bash
cd C:\Users\james\Master\BrightHub\BRun\brightrun-trainer

docker build -t brighthub/brightrun-trainer:v2 .
docker login
docker push brighthub/brightrun-trainer:v2
```

### 4. Update RunPod Endpoint to Use v2 Image

**Steps:**
1. Go to https://console.runpod.io/serverless
2. Click endpoint `ei82ickpenoqlp`
3. Edit → Container Image
4. Change from `brighthub/brightrun-trainer:v1` to `brighthub/brightrun-trainer:v2`
5. Save
6. Wait 2-5 minutes for workers to restart

### 5. Deploy Edge Functions to Supabase

**Commands:**
```bash
cd C:\Users\james\Master\BrightHub\BRun\lora-pipeline

supabase link --project-ref hqhtbxlgzysfbekexwku
supabase secrets set GPU_CLUSTER_API_KEY=rpa_550JTL8271ULHL73VGU6ED4ZWBU5HB2KNAPMTW38cu8d8v
supabase secrets set GPU_CLUSTER_ENDPOINT=https://api.runpod.ai/v2/ei82ickpenoqlp

supabase functions deploy process-training-jobs
supabase functions deploy create-model-artifacts
```

---

## 📋 Did We Change Docker Image to Output URLs?

### Yes ✅

**What changed in handler.py:**

1. **Imports added:**
   ```python
   import boto3
   import os
   from pathlib import Path
   ```

2. **New function added:**
   ```python
   def upload_model_to_s3(job_id, model_dir):
       # Uploads model files to RunPod S3
       # Returns dict of {filename: presigned_url}
   ```

3. **Handler return modified:**
   ```python
   # OLD return (line 168 in original):
   return result

   # NEW return (lines 251-281 in updated):
   return {
       "status": "success",
       "model_files": {
           "adapter_model.bin": "https://presigned-url...",
           "adapter_config.json": "https://presigned-url..."
       },
       "model_metadata": {...},
       "progress": 100,
       ...
   }
   ```

**But:** The updated code is only in the workfiles directory, not yet in the actual Docker worker directory.

---

## 🚀 Quick Checklist to Complete Deployment

- [ ] Copy updated handler.py to `C:\Users\james\Master\BrightHub\BRun\brightrun-trainer\`
- [ ] Verify `boto3` in requirements.txt
- [ ] Build Docker image v2
- [ ] Push Docker image v2 to Docker Hub
- [ ] Update RunPod endpoint to use v2 image
- [ ] Wait for workers to restart (2-5 min)
- [ ] Deploy Edge Functions to Supabase
- [ ] Test with a training job
- [ ] Verify model files are returned with URLs

---

## 🎯 Next Immediate Steps

**Step 1:** Copy handler.py
**Step 2:** Check/update requirements.txt
**Step 3:** Build and push Docker image
**Step 4:** Update RunPod endpoint
**Step 5:** Deploy Edge Functions

After these 5 steps, the system will be fully operational with model file URLs.
