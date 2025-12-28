# New Model Deployment Guide: Adding Support for Additional Base Models

**Document Version:** 1.0  
**Date:** December 28, 2025  
**Purpose:** Guide for deploying new base models (DeepSeek, Llama, frontier models, etc.) to the LoRA training pipeline  
**Prerequisites:** Completed initial setup with Qwen3-Next-80B-A3B-Instruct

---

## Overview

This guide explains how to add support for **new base models** to your LoRA training infrastructure. You do NOT need to repeat the entire setup from scratch - most components are reusable.

### Frequency of Use

- **One-time setup** (already complete): RunPod account, Docker Hub account, Supabase project, application codebase
- **Per-model setup** (this guide): Add each new base model you want to support (e.g., DeepSeek-V3, Llama 4, Claude Haiku, Qwen2.5-VL)

---

## Architecture: One-Time vs Per-Model Components

### ✅ One-Time Setup (Already Complete)

These components are **shared across all models** and only need to be set up once:

| Component | Description | Reusable? |
|-----------|-------------|-----------|
| **Application Codebase** | Next.js app with E01-E03 (datasets, configuration, job creation) | ✅ Yes |
| **Database Schema** | `datasets`, `training_jobs`, `metrics_points`, etc. | ✅ Yes |
| **Supabase Storage** | `lora-datasets`, `lora-models` buckets | ✅ Yes |
| **Docker Worker Code** | `handler.py`, `train_lora.py` (with dynamic model loading) | ✅ Yes (with minor updates) |
| **RunPod Account** | Account, API keys, billing setup | ✅ Yes |
| **Docker Hub Account** | Registry for Docker images | ✅ Yes |

### 🔄 Per-Model Setup (Repeat for Each New Model)

These components are **model-specific** and need to be configured for each new base model:

| Component | Description | Per-Model? |
|-----------|-------------|------------|
| **Network Volume** | Storage for model weights (~50-200GB per model) | 🔄 Yes |
| **Model Download** | Download specific model weights from HuggingFace | 🔄 Yes |
| **Docker Image** | Build new image with model-specific config | 🔄 Maybe (see Strategy) |
| **RunPod Template** | Template with model-specific environment variables | 🔄 Yes |
| **RunPod Endpoint** | Serverless endpoint for this model | 🔄 Yes |
| **Application Config** | Update UI to offer this model as an option | 🔄 Yes |

---

## Deployment Strategies

### Strategy 1: Separate Endpoints per Model (Recommended)

**Use Case**: Supporting multiple distinct models (Qwen, DeepSeek, Llama, etc.)

**Advantages**:
- ✅ Clean separation of concerns
- ✅ Independent scaling per model
- ✅ Easy to deprecate old models
- ✅ Model-specific GPU selection (e.g., DeepSeek needs H100, Llama works on A100)

**Disadvantages**:
- ❌ Higher infrastructure cost (separate endpoints idle when not in use)
- ❌ More RunPod configuration to manage

**Architecture**:
```
Application
  ├─ Qwen Endpoint → qwen-model-cache volume → Qwen3-Next-80B-A3B-Instruct
  ├─ DeepSeek Endpoint → deepseek-model-cache volume → DeepSeek-V3-671B
  └─ Llama Endpoint → llama-model-cache volume → Llama-4-405B
```

### Strategy 2: Single Endpoint with Multiple Models (Advanced)

**Use Case**: Cost optimization when supporting many similar models

**Advantages**:
- ✅ Lower cost (one endpoint, auto-scales for all models)
- ✅ Simpler endpoint management

**Disadvantages**:
- ❌ Larger network volume needed (stores all models)
- ❌ More complex Docker worker logic (model selection)
- ❌ All models must fit on same GPU type

**Architecture**:
```
Application
  └─ Multi-Model Endpoint → shared-model-cache volume
       ├─ /models/qwen3-80b/
       ├─ /models/deepseek-v3/
       └─ /models/llama-4-405b/
```

**Note**: This guide focuses on **Strategy 1** as it's more maintainable and flexible.

---

## Step-by-Step: Adding a New Model

### Example: Adding DeepSeek-V3-671B Support

Let's walk through adding DeepSeek-V3 as a second supported model.

---

### Phase 1: Model Research & Planning

Before starting, research the model:

**Questions to Answer**:
1. **Model ID**: What's the HuggingFace model ID? (e.g., `deepseek-ai/DeepSeek-V3`)
2. **Model Size**: How large are the weights? (e.g., 671B params = ~1.3TB FP16, ~335GB 4-bit)
3. **Architecture**: What's the model architecture? (affects target_modules for LoRA)
4. **Context Length**: What's the max sequence length? (affects memory requirements)
5. **Quantization**: Does it support 4-bit quantization? (QLoRA requirement)
6. **License**: Is it permissible for your use case? (commercial vs research)
7. **GPU Requirement**: What GPU does it need? (671B needs H100 80GB even with 4-bit)

**DeepSeek-V3 Example**:
- **Model ID**: `deepseek-ai/DeepSeek-V3`
- **Size**: ~335GB (4-bit quantized)
- **Architecture**: MoE (Mixture of Experts) Transformer
- **Context**: 128K tokens
- **Quantization**: Supports 4-bit (bitsandbytes compatible)
- **License**: MIT (permissive for commercial use)
- **GPU**: H100 80GB minimum (MoE architecture is memory-intensive)

**Decision**: Proceed with deployment on H100 GPUs with 4-bit QLoRA.

---

### Phase 2: Create Network Volume & Download Model

#### Step 2.1: Create New Network Volume

1. Log into RunPod Console: https://runpod.io/console/storage
2. Click **+ New Network Volume**
3. Configure:
   - **Name**: `deepseek-v3-cache` (use descriptive name)
   - **Size**: `400 GB` (335GB model + 20% overhead)
   - **Datacenter**: Same as your other volumes for consistency (e.g., US-CA-2)
4. Click **Create**
5. Note the **Volume ID**

**Naming Convention**: `{model-name}-cache` (lowercase, hyphenated)

#### Step 2.2: Download Model Weights

1. Go to **Pods** → **+ Deploy**
2. Select:
   - **GPU**: CPU pod (cheapest option for downloads)
   - **Template**: RunPod PyTorch
   - **Network Volume**: Select `deepseek-v3-cache`
3. Deploy pod
4. Click **Connect** → **Web Terminal**
5. Run download script:

```bash
pip install huggingface_hub

cat << 'EOF' > /tmp/download_model.py
from huggingface_hub import snapshot_download

MODEL_ID = "deepseek-ai/DeepSeek-V3"
LOCAL_DIR = "/workspace/models/DeepSeek-V3"

print(f"Starting {MODEL_ID} download...")
print(f"Destination: {LOCAL_DIR}")
print("-" * 60)

try:
    snapshot_download(
        MODEL_ID,
        local_dir=LOCAL_DIR,
        resume_download=True,
        token='YOUR_HF_TOKEN_HERE'  # Replace with your token
    )
    print("\n" + "=" * 60)
    print("Download complete!")
    print("=" * 60)
except Exception as e:
    print(f"\nError: {e}")
    print("You can re-run this command to resume.")
EOF

python3 /tmp/download_model.py
```

6. Wait for download (335GB may take 1-3 hours)
7. Verify: `ls -lh /workspace/models/DeepSeek-V3/`
8. **Terminate pod** (download complete)

**Critical**: Always use `/workspace/models/{MODEL_NAME}/` path format for consistency.

---

### Phase 3: Update Docker Worker (If Needed)

**When to Update Docker Worker**:

- ✅ **Skip update if**: Model uses same architecture as existing (e.g., both are decoder-only transformers with similar target modules)
- 🔄 **Update required if**: Model has different architecture (different target_modules for LoRA)

#### Step 3.1: Check Target Modules

Different architectures require different LoRA target modules:

**Standard Transformer (Qwen, Llama, Mistral)**:
```python
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj"
]
```

**DeepSeek-V3 (MoE - Mixture of Experts)**:
```python
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
    # MoE-specific (if present):
    "gate",  # Expert routing gate
]
```

**Other Architectures** (consult model docs):
- **Vision-Language Models**: May include vision encoder projections
- **Encoder-Decoder Models** (T5, BART): Include encoder attention layers

#### Step 3.2: Update train_lora.py (If Needed)

If target modules differ, update `train_lora.py`:

```python
# Make target_modules dynamic based on model architecture
def get_target_modules(model_name: str) -> list[str]:
    """Get LoRA target modules based on model architecture."""
    
    if "deepseek" in model_name.lower():
        return [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
            "gate"  # MoE routing
        ]
    elif "qwen" in model_name.lower() or "llama" in model_name.lower():
        return [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ]
    else:
        # Default to standard transformer modules
        return [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ]

# In LoraConfig:
lora_config = LoraConfig(
    r=config["lora_rank"],
    lora_alpha=config["lora_alpha"],
    lora_dropout=config["lora_dropout"],
    target_modules=get_target_modules(config["base_model"]),
    bias="none",
    task_type="CAUSAL_LM"
)
```

#### Step 3.3: Rebuild Docker Image (If Updated)

If you modified `train_lora.py`:

```bash
cd C:\Users\james\Master\BrightHub\BRun\brightrun-trainer

# Increment version number
docker build --platform linux/amd64 -t yourdockerhub/brightrun-trainer:v2 .
docker push yourdockerhub/brightrun-trainer:v2
```

**Note**: If no changes to Docker worker, skip this step and reuse existing image.

---

### Phase 4: Create RunPod Template for New Model

1. Go to RunPod Console → **Serverless** → **Templates**
2. Click **+ New Template**
3. Configure:

| Field | Value |
|-------|-------|
| **Template Name** | `BrightRun LoRA Trainer - DeepSeek-V3` |
| **Container Image** | `yourdockerhub/brightrun-trainer:v1` (or v2 if updated) |
| **Container Disk** | `20 GB` |
| **Volume Mount Path** | `/runpod-volume` |

4. Add **Environment Variables**:

| Key | Value (DeepSeek-V3 Specific) |
|-----|------------------------------|
| `HF_HOME` | `/runpod-volume/.cache/huggingface` |
| `TRANSFORMERS_CACHE` | `/runpod-volume/models` |
| `MODEL_PATH` | `/runpod-volume/models/DeepSeek-V3` ← **Change this** |
| `SUPABASE_URL` | `https://hqhtbxlgzysfbekexwku.supabase.co` |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJ...` (your service role key) |

5. Click **Save Template**

**Key Change**: Only `MODEL_PATH` changes per model. All other environment variables stay the same.

---

### Phase 5: Deploy RunPod Endpoint for New Model

1. Go to **Serverless** → **Endpoints**
2. Click **+ New Endpoint**
3. Configure:

| Field | Value (DeepSeek-V3) |
|-------|---------------------|
| **Endpoint Name** | `brightrun-lora-trainer-deepseek-v3` |
| **Template** | Select `BrightRun LoRA Trainer - DeepSeek-V3` |
| **GPU** | `NVIDIA H100 80GB` ← **DeepSeek requires H100** |
| **Active Workers** | `0` (auto-scale) |
| **Max Workers** | `1` (expensive model, limit concurrency) |
| **Idle Timeout** | `60` seconds |
| **Execution Timeout** | `43200` seconds (12 hours) |
| **Network Volume** | Select `deepseek-v3-cache` ← **Important** |

4. Click **Deploy**
5. Wait for status: **Ready**

#### Step 5.1: Get Endpoint Credentials

1. Click endpoint name
2. Copy **Endpoint URL**: `https://api.runpod.ai/v2/{deepseek-endpoint-id}`
3. Note this as `GPU_CLUSTER_API_URL_DEEPSEEK`

**API Key**: Use the same RunPod API key as Qwen (keys are account-level, not endpoint-specific)

---

### Phase 6: Update Application Configuration

Now make the new model available in your application.

#### Step 6.1: Update .env.local

Add new endpoint configuration:

```bash
# GPU Cluster Configuration - Qwen (existing)
GPU_CLUSTER_API_URL_QWEN=https://api.runpod.ai/v2/qwen-endpoint-id
GPU_CLUSTER_API_KEY=rp_your-api-key-here

# GPU Cluster Configuration - DeepSeek V3 (new)
GPU_CLUSTER_API_URL_DEEPSEEK=https://api.runpod.ai/v2/deepseek-endpoint-id
# Same API key for all endpoints
```

#### Step 6.2: Update Backend Logic

**File**: `src/app/api/jobs/route.ts` (or similar)

Add model selection logic:

```typescript
// Map model to endpoint
function getEndpointForModel(modelName: string): string {
  if (modelName.includes('qwen')) {
    return process.env.GPU_CLUSTER_API_URL_QWEN!;
  } else if (modelName.includes('deepseek')) {
    return process.env.GPU_CLUSTER_API_URL_DEEPSEEK!;
  } else {
    throw new Error(`Unsupported model: ${modelName}`);
  }
}

// In job creation endpoint:
const endpointUrl = getEndpointForModel(hyperparameters.base_model);
```

#### Step 6.3: Update Frontend UI

**File**: `src/app/(dashboard)/training/configure/page.tsx`

Add model selection to configuration form:

```typescript
// Add model selector before GPU configuration
<div className="space-y-2">
  <Label>Base Model</Label>
  <Select value={selectedModel} onValueChange={setSelectedModel}>
    <SelectTrigger>
      <SelectValue placeholder="Select base model" />
    </SelectTrigger>
    <SelectContent>
      <SelectItem value="Qwen/Qwen3-Next-80B-A3B-Instruct">
        Qwen3-Next-80B (80B params, A100 compatible)
      </SelectItem>
      <SelectItem value="deepseek-ai/DeepSeek-V3">
        DeepSeek-V3 (671B params, H100 required)
      </SelectItem>
    </SelectContent>
  </Select>
</div>
```

#### Step 6.4: Update Cost Estimation

**File**: `src/app/api/jobs/estimate/route.ts`

Update GPU pricing to reflect H100 requirement for DeepSeek:

```typescript
// GPU pricing map
const GPU_PRICING = {
  'A100-80GB': { hourly: 3.50, throughput: 1800 },
  'A100-40GB': { hourly: 2.80, throughput: 1500 },
  'H100-80GB': { hourly: 4.20, throughput: 2200 },  // For DeepSeek
  'V100-32GB': { hourly: 2.10, throughput: 1200 },
};

// Restrict GPU selection based on model
function getCompatibleGPUs(modelName: string): string[] {
  if (modelName.includes('deepseek-v3')) {
    return ['H100-80GB'];  // DeepSeek V3 requires H100
  } else if (modelName.includes('qwen')) {
    return ['A100-80GB', 'A100-40GB', 'H100-80GB'];  // Qwen works on A100 or H100
  }
  return ['A100-80GB', 'H100-80GB'];  // Default
}
```

#### Step 6.5: Update Database Schema (Optional)

If you want to track which model was used:

```sql
-- Add model_name column to training_jobs table
ALTER TABLE training_jobs 
ADD COLUMN IF NOT EXISTS model_name TEXT DEFAULT 'Qwen/Qwen3-Next-80B-A3B-Instruct';

-- Add index for filtering by model
CREATE INDEX IF NOT EXISTS idx_training_jobs_model_name 
ON training_jobs(model_name);
```

---

### Phase 7: Testing & Verification

#### Step 7.1: Test Endpoint Directly

```bash
curl -X POST "https://api.runpod.ai/v2/deepseek-endpoint-id/run" \
  -H "Authorization: Bearer rp_your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "job_id": "test-deepseek-001",
      "dataset_url": "https://signed-url/test.jsonl",
      "hyperparameters": {
        "base_model": "deepseek-ai/DeepSeek-V3",
        "learning_rate": 0.0001,
        "batch_size": 2,
        "num_epochs": 1,
        "lora_rank": 16
      }
    }
  }'
```

Expected response:
```json
{
  "id": "runpod-job-xxxxx",
  "status": "IN_QUEUE"
}
```

#### Step 7.2: Test End-to-End in Application

1. Create test dataset (small, ~10 training pairs)
2. Go to `/training/configure`
3. Select **DeepSeek-V3** as base model
4. Configure with minimal settings (batch_size=2, epochs=1)
5. Create training job
6. Monitor job execution
7. Verify adapter uploaded to Supabase Storage

#### Step 7.3: Monitor Costs

- Watch RunPod billing dashboard
- Verify H100 hourly rate matches expectations (~$4.20/hr)
- Check job duration vs estimated duration

---

## Model-Specific Considerations

### GPU Memory Requirements

| Model Size | Quantization | Minimum GPU | Recommended GPU |
|------------|--------------|-------------|-----------------|
| 7-13B | 4-bit | A100 40GB | A100 80GB |
| 30-80B | 4-bit | A100 80GB | A100 80GB or H100 |
| 180-400B | 4-bit | H100 80GB | H100 80GB (2x for faster training) |
| 400B+ (MoE) | 4-bit | H100 80GB | H100 80GB (may need multi-GPU) |

### Network Volume Sizing

**Formula**: `volume_size = model_size_4bit × 1.2 + 50GB`

- **50GB**: Base overhead (HuggingFace cache, temp files)
- **1.2x**: 20% buffer for checkpoints during download

**Examples**:
- **Qwen3-80B**: 84GB × 1.2 + 50 = ~150GB → Use 200GB volume
- **DeepSeek-V3-671B**: 335GB × 1.2 + 50 = ~450GB → Use 500GB volume
- **Llama-4-405B**: 200GB × 1.2 + 50 = ~290GB → Use 350GB volume

### Model Architecture Target Modules

**Standard Decoder-Only (GPT-style)**:
```python
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
```

**MoE (Mixture of Experts) - DeepSeek, Mixtral**:
```python
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj", "gate"]
```

**Vision-Language (Qwen-VL, LLaVA)**:
```python
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj", "vision_proj"]
```

**Encoder-Decoder (T5, BART)**:
```python
target_modules = [
    # Encoder
    "encoder.q", "encoder.k", "encoder.v", "encoder.o",
    # Decoder
    "decoder.q", "decoder.k", "decoder.v", "decoder.o",
    "decoder.cross_attn_q", "decoder.cross_attn_k", "decoder.cross_attn_v"
]
```

**Finding Target Modules**:
1. Check model's HuggingFace page → Model card → Architecture section
2. Load model locally and print: `print(model.named_modules())`
3. Check PEFT examples: https://github.com/huggingface/peft/tree/main/examples

---

## Checklist: Adding a New Model

Use this checklist each time you add a new model:

### Pre-Deployment
- [ ] Research model: size, architecture, license, GPU requirements
- [ ] Verify HuggingFace access (if gated model)
- [ ] Calculate network volume size needed
- [ ] Identify target modules for LoRA
- [ ] Verify quantization compatibility (4-bit)

### RunPod Setup
- [ ] Create network volume with appropriate size
- [ ] Download model weights to volume (`/workspace/models/{MODEL_NAME}/`)
- [ ] Verify download completion
- [ ] Terminate download pod

### Docker Worker (If Needed)
- [ ] Update `train_lora.py` with new target modules (if different architecture)
- [ ] Test updated code locally (if possible)
- [ ] Rebuild Docker image with new version tag
- [ ] Push to Docker Hub

### RunPod Endpoint
- [ ] Create new template with model-specific `MODEL_PATH`
- [ ] Deploy new endpoint with correct GPU type
- [ ] Attach correct network volume
- [ ] Verify endpoint status shows "Ready"
- [ ] Copy endpoint URL

### Application Integration
- [ ] Add endpoint URL to `.env.local`
- [ ] Update backend model routing logic
- [ ] Add model to frontend UI selector
- [ ] Update cost estimation for model-specific GPU requirements
- [ ] Update database schema (if tracking model names)
- [ ] Deploy updated application

### Testing
- [ ] Test endpoint directly with curl
- [ ] Create test dataset
- [ ] Run end-to-end training job
- [ ] Verify adapter upload
- [ ] Monitor costs and duration
- [ ] Document any model-specific quirks

---

## Cost Optimization Strategies

### Strategy 1: Shared Network Volumes

If models are similar sizes and architectures:

```
single-model-cache (500GB)
  ├─ /models/qwen3-80b/       (84GB)
  ├─ /models/llama-4-70b/     (70GB)
  └─ /models/mistral-8x7b/    (47GB)
```

**Savings**: One 500GB volume ($5/month) vs three 200GB volumes ($15/month)

**Trade-off**: All endpoints must use same datacenter and volume

### Strategy 2: On-Demand Volume Mounting

For rarely-used models:
- Keep model weights in RunPod storage (archived)
- Only mount volume when job is active
- Unmount after job completes

**Use Case**: Supporting 10+ models but only 2-3 actively trained

### Strategy 3: Auto-Scaling Configuration

```yaml
# For expensive models (H100)
Active Workers: 0
Max Workers: 1
Idle Timeout: 30 seconds  # Faster spin-down

# For cheap models (A100)
Active Workers: 0
Max Workers: 3
Idle Timeout: 60 seconds
```

**Savings**: Minimize idle time on expensive GPUs

---

## Troubleshooting New Model Deployments

### Issue: Model Fails to Load

**Symptoms**: Error during model initialization, OOM even with quantization

**Possible Causes**:
1. Model too large for GPU (even with 4-bit)
2. Incorrect quantization config
3. Model architecture not supported by bitsandbytes

**Solutions**:
- Use larger GPU (H100 instead of A100)
- Check model's recommended quantization settings
- Enable gradient checkpointing: `model.gradient_checkpointing_enable()`

### Issue: Training Runs But No Improvement

**Symptoms**: Loss stays flat or increases, no learning

**Possible Causes**:
1. Incorrect target modules (LoRA not applied to right layers)
2. Learning rate too high/low for model size
3. Dataset format incompatible with model's tokenizer

**Solutions**:
- Verify target modules with `print(model.named_modules())`
- Reduce learning rate for larger models (1e-5 for 400B+ models)
- Check tokenizer output: `tokenizer.decode(tokenized_input["input_ids"])`

### Issue: Endpoint Shows "Unhealthy"

**Symptoms**: RunPod endpoint status = "Unhealthy", jobs fail immediately

**Possible Causes**:
1. MODEL_PATH incorrect (model not found in volume)
2. Volume not attached to endpoint
3. Docker image has dependency issues

**Solutions**:
- Check Docker logs in RunPod console
- Verify volume attachment: SSH into active worker and `ls /runpod-volume/models/`
- Test Docker image locally: `docker run -it yourdockerhub/brightrun-trainer:v1 /bin/bash`

---

## Future: Frontier Models

### Preparing for Next-Gen Models (2025-2026)

**Claude 4, GPT-5, Gemini 2 Ultra, Qwen 3.5**:

These models will likely:
- Be **larger** (1T+ parameters)
- Require **multiple H100s** or next-gen GPUs (B100, H200)
- Have **multimodal** capabilities (text, image, audio)
- Use **new architectures** (may need custom LoRA implementations)

**Preparation Steps**:
1. **Monitor releases**: Subscribe to model provider updates
2. **Test early**: Use preview/beta access to test compatibility
3. **Budget for compute**: Frontier models may cost $10-20/hr
4. **Update Docker worker**: New architectures may need PEFT updates
5. **Consider alternatives**: Distilled models (e.g., Claude 4 Haiku) may suffice

### Multi-GPU Training

For models >1TB parameters:

**Docker Worker Update** (`train_lora.py`):
```python
# Enable multi-GPU training
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model)
    
# Or use DeepSpeed for better efficiency
from transformers import TrainingArguments
training_args = TrainingArguments(
    ...,
    deepspeed="./ds_config.json",  # DeepSpeed config
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16
)
```

**RunPod Endpoint**:
- Select multi-GPU option (2x H100, 4x H100, 8x H100)
- Adjust batch size and gradient accumulation accordingly
- Update cost estimation (multi-GPU is linear: 2x H100 = 2x cost)

---

## Summary: Repeatable vs One-Time

### You'll Follow the Full E04.5 Guide:
**Once** - Initial setup with Qwen3-Next-80B-A3B-Instruct (already complete)

### You'll Follow This New Model Guide:
**For each new base model** you want to support:
- DeepSeek-V3
- Llama 4
- Claude 4 (if/when available for self-hosting)
- Qwen 3.5
- Mistral Large
- Any other models

### Repeatable Steps (Per Model):
1. ✅ Download model weights (30-60 min)
2. ✅ Create RunPod template (5 min)
3. ✅ Deploy endpoint (5 min)
4. ✅ Update application config (15 min)
5. ✅ Test end-to-end (30 min)

**Total time per new model**: ~2 hours (mostly waiting for download)

### Non-Repeatable (One-Time):
- ❌ Application codebase development (E01-E03)
- ❌ Docker worker creation (E04.5 Section 2)
- ❌ Database schema setup
- ❌ Supabase project setup
- ❌ RunPod/Docker Hub accounts

---

## Appendix: Model Support Matrix

| Model | Size | 4-bit Size | Min GPU | Cost/Hr | Network Volume | Status |
|-------|------|------------|---------|---------|----------------|--------|
| Qwen3-Next-80B-A3B-Instruct | 80B | 84GB | A100 80GB | $3.50 | 200GB | ✅ Deployed |
| DeepSeek-V3 | 671B | 335GB | H100 80GB | $4.20 | 500GB | 📋 Example |
| Llama-4-405B | 405B | 200GB | H100 80GB | $4.20 | 300GB | ⏳ Pending |
| Mistral-Large-2 | 123B | 62GB | A100 80GB | $3.50 | 150GB | ⏳ Pending |
| Qwen2.5-VL-72B | 72B | 75GB | A100 80GB | $3.50 | 200GB | ⏳ Pending |

---

**Document Version**: 1.0  
**Last Updated**: December 28, 2025  
**Maintainer**: BrightRun Infrastructure Team  
**Next Review**: When adding 3rd model (validate this guide's accuracy)
