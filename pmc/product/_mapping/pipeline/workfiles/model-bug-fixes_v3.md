# Model Loading Path Error Analysis v3

**Date**: January 2, 2026  
**Status**: Dataset loading FIXED ✅, Model path issue identified

---

## Progress ✅

**Dataset loading now works!**
```
BrightRun format converted: 14
Total conversations: 14
```

**Base model now uses Qwen:**
```
Base Model: Qwen/Qwen3-Next-80B-A3B-Instruct
```

---

## New Error

```
Repo id must be in the form 'repo_name' or 'namespace/repo_name': 
'/workspace/models/Qwen3-Next-80B-A3B-Instruct'. 
Use `repo_type` argument if needed.
```

---

## Root Cause Analysis

**Two conflicting model path sources:**

| Source | Value | Used For |
|--------|-------|----------|
| hyperparameters['base_model'] | `Qwen/Qwen3-Next-80B-A3B-Instruct` | Logged in handler |
| `MODEL_PATH` env var | `/workspace/models/Qwen3-Next-80B-A3B-Instruct` | Actually used in train_lora.py |

**The conflict:**
1. Edge Function sends: `base_model: 'Qwen/Qwen3-Next-80B-A3B-Instruct'` (HuggingFace hub format)
2. train_lora.py uses `MODEL_PATH` env var: `/workspace/models/Qwen3-Next-80B-A3B-Instruct` (local path)
3. But the env var path starts with `/workspace` which doesn't exist on this worker

**Key evidence from logs:**
- Line 71: `Model path: /workspace/models/Qwen3-Next-80B-A3B-Instruct`
- This path starts with `/workspace` but should be `/runpod-volume` based on the network volume mount

---

## Solution Options

### Option A: Fix MODEL_PATH Environment Variable (Recommended)

**In RunPod Console:**
1. Go to https://console.runpod.io/serverless
2. Click endpoint `ei82ickpenoqlp`
3. Edit → Environment Variables
4. Add or update: `MODEL_PATH=/runpod-volume/models/Qwen3-Next-80B-A3B-Instruct`

**No code changes needed.**

### Option B: Modify train_lora.py to Use base_model from Hyperparameters

**Change line ~374 in train_lora.py:**

**Current:**
```python
model_path = os.environ.get('MODEL_PATH', '/runpod-volume/models/Qwen3-Next-80B-A3B-Instruct')
```

**Updated:**
```python
# First check if local cached model exists
default_local_path = '/runpod-volume/models/Qwen3-Next-80B-A3B-Instruct'
model_path = os.environ.get('MODEL_PATH', default_local_path)

# If local path doesn't exist, use HuggingFace hub ID from hyperparameters
if not os.path.exists(model_path):
    model_path = hyperparameters.get('base_model', 'Qwen/Qwen3-Next-80B-A3B-Instruct')
    logger.info(f"Local model not found, downloading from HuggingFace: {model_path}")
```

### Option C: Update the local_files_only Flag

**If model exists on network volume, add `local_files_only=True`:**

```python
tokenizer = AutoTokenizer.from_pretrained(
    model_path, 
    trust_remote_code=True,
    local_files_only=True  # Don't try to validate as HF repo ID
)
```

---

## Recommended Fix: Option A + Verification

### Step 1: Verify Model Location on Network Volume

The model should be at one of these paths on the worker:
- `/runpod-volume/models/Qwen3-Next-80B-A3B-Instruct`
- `/workspace/models/Qwen3-Next-80B-A3B-Instruct`

**Check which path the volume mounts to:**
- If your endpoint config shows mount path as `/runpod-volume`, use that
- If it shows `/workspace`, the path is correct but model may not exist

### Step 2: Update MODEL_PATH Environment Variable

**Add this to RunPod endpoint environment variables:**
```
MODEL_PATH=/runpod-volume/models/Qwen3-Next-80B-A3B-Instruct
```

**OR if volume mounts to /workspace:**
```
MODEL_PATH=/workspace/models/Qwen3-Next-80B-A3B-Instruct
```

### Step 3: Verify Model Exists on Volume

**Option 1**: SSH into a worker and check:
```bash
ls -la /runpod-volume/models/
ls -la /workspace/models/
```

**Option 2**: Check RunPod Volume Browser in console

---

## Quick Fix (If Model Not on Volume)

If the Qwen model doesn't exist on the network volume, you need to either:

1. **Download it to the volume** (takes time, 84GB)
2. **Use a smaller model** temporarily for testing:
   - `mistralai/Mistral-7B-v0.1` (14GB, downloads quickly)
   - `Qwen/Qwen2.5-7B-Instruct` (7GB)

To use smaller model, update Edge Function:
```typescript
base_model: job.hyperparameters.base_model || 'mistralai/Mistral-7B-v0.1',
```

---

## Files to Update

| File | Change |
|------|--------|
| RunPod Environment Variables | Add `MODEL_PATH=/runpod-volume/models/Qwen3-Next-80B-A3B-Instruct` |
| (Optional) train_lora.py | Add fallback to download from HuggingFace if local not found |

---

## Priority

1. **Check if model exists on volume** - most likely issue
2. **Fix MODEL_PATH env var** to point to correct location
3. **Test with smaller model** if large model not cached
