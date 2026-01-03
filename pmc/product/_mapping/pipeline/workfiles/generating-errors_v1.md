## Requests Log
{
  "delayTime": 8635,
  "executionTime": 1510,
  "id": "ccd85999-a159-4518-ab44-cf0558a8467a-u2",
  "output": {
    "error_message": "Repo id must be in the form 'repo_name' or 'namespace/repo_name': '/workspace/models/Qwen3-Next-80B-A3B-Instruct'. Use `repo_type` argument if needed.",
    "job_id": "3ce3c69d-f189-42e6-a125-69df5fe54da1",
    "status": "failed"
  },
  "status": "COMPLETED",
  "workerId": "jpoppionpkx94d"
}

## Worker Log
2026-01-03T07:17:05.352092367Z ==========
2026-01-03T07:17:05.352102015Z == CUDA ==
2026-01-03T07:17:05.352120690Z ==========
2026-01-03T07:17:05.353781084Z CUDA Version 11.8.0
2026-01-03T07:17:05.354445436Z Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.
2026-01-03T07:17:05.354851485Z This container image and its contents are governed by the NVIDIA Deep Learning Container License.
2026-01-03T07:17:05.354852698Z By pulling and using the container, you accept the terms and conditions of this license:
2026-01-03T07:17:05.354853720Z https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license
2026-01-03T07:17:05.354855713Z A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.
2026-01-03T07:17:07.462551698Z /usr/local/lib/python3.10/dist-packages/transformers/utils/hub.py:110: FutureWarning: Using `TRANSFORMERS_CACHE` is deprecated and will be removed in v5 of Transformers. Use `HF_HOME` instead.
2026-01-03T07:17:07.462578829Z   warnings.warn(
2026-01-03T07:17:08.302730984Z /usr/local/lib/python3.10/dist-packages/torchvision/io/image.py:13: UserWarning: Failed to load image Python extension: 'Could not load this library: /usr/local/lib/python3.10/dist-packages/torchvision/image.so'If you don't plan on using image functionality from `torchvision.io`, you can ignore this warning. Otherwise, there might be something wrong with your environment. Did you have `libjpeg` or `libpng` installed before building `torchvision` from source?
2026-01-03T07:17:08.302755941Z   warn(
2026-01-03T07:17:08.612056682Z config.py           :59   2026-01-03 07:17:08,611 PyTorch version 2.9.1 available.
2026-01-03T07:17:08.841892394Z status_manager.py   :32   2026-01-03 07:17:08,841 StatusManager initialized
2026-01-03T07:17:08.841911961Z handler.py          :316  2026-01-03 07:17:08,841 Starting RunPod serverless worker...
2026-01-03T07:17:08.841913183Z handler.py          :317  2026-01-03 07:17:08,841 Waiting for jobs...
2026-01-03T07:17:08.841894338Z --- Starting Serverless Worker |  Version 1.8.1 ---
2026-01-03T07:17:09.281396515Z {"requestId": null, "message": "Jobs in queue: 1", "level": "INFO"}
2026-01-03T07:17:09.281412535Z {"requestId": null, "message": "Jobs in progress: 1", "level": "INFO"}
2026-01-03T07:17:09.281445226Z {"requestId": "ccd85999-a159-4518-ab44-cf0558a8467a-u2", "message": "Started.", "level": "INFO"}
2026-01-03T07:17:09.281582182Z handler.py          :192  2026-01-03 07:17:09,281 ================================================================================
2026-01-03T07:17:09.281586991Z handler.py          :193  2026-01-03 07:17:09,281 RunPod Handler: New job received
2026-01-03T07:17:09.281588804Z handler.py          :194  2026-01-03 07:17:09,281 ================================================================================
2026-01-03T07:17:09.281593012Z handler.py          :201  2026-01-03 07:17:09,281 Job ID: 3ce3c69d-f189-42e6-a125-69df5fe54da1
2026-01-03T07:17:09.281594074Z handler.py          :202  2026-01-03 07:17:09,281 Input keys: ['callback_url', 'dataset_url', 'gpu_config', 'hyperparameters', 'job_id']
2026-01-03T07:17:09.281613581Z handler.py          :219  2026-01-03 07:17:09,281 Validation passed
2026-01-03T07:17:09.281658024Z handler.py          :231  2026-01-03 07:17:09,281 Base Model: Qwen/Qwen3-Next-80B-A3B-Instruct
2026-01-03T07:17:09.281661180Z handler.py          :232  2026-01-03 07:17:09,281 Learning Rate: 5e-05
2026-01-03T07:17:09.281676949Z handler.py          :233  2026-01-03 07:17:09,281 Batch Size: 4
2026-01-03T07:17:09.281678372Z handler.py          :234  2026-01-03 07:17:09,281 Epochs: 3
2026-01-03T07:17:09.281681788Z handler.py          :235  2026-01-03 07:17:09,281 LoRA Rank: 16
2026-01-03T07:17:09.281692228Z handler.py          :236  2026-01-03 07:17:09,281 GPU Type: A100-80GB
2026-01-03T07:17:09.281694191Z handler.py          :239  2026-01-03 07:17:09,281 Starting training execution...
2026-01-03T07:17:09.281790531Z train_lora.py       :327  2026-01-03 07:17:09,281 Working directory: /tmp/job_3ce3c69d-f189-42e6-a125-69df5fe54da1_1037j8zt
2026-01-03T07:17:09.281809196Z train_lora.py       :330  2026-01-03 07:17:09,281 ================================================================================
2026-01-03T07:17:09.281811461Z train_lora.py       :331  2026-01-03 07:17:09,281 STEP 1: Downloading dataset
2026-01-03T07:17:09.281814306Z train_lora.py       :332  2026-01-03 07:17:09,281 ================================================================================
2026-01-03T07:17:09.281816801Z train_lora.py       :133  2026-01-03 07:17:09,281 Downloading dataset from: https://hqhtbxlgzysfbekexwku.supabase.co/storage/v1/object/s...
2026-01-03T07:17:10.734714189Z train_lora.py       :153  2026-01-03 07:17:10,734 Dataset downloaded successfully: 0.2MB
2026-01-03T07:17:10.735568566Z train_lora.py       :346  2026-01-03 07:17:10,735 ================================================================================
2026-01-03T07:17:10.735600145Z train_lora.py       :347  2026-01-03 07:17:10,735 STEP 2: Loading and preparing dataset
2026-01-03T07:17:10.735608190Z train_lora.py       :348  2026-01-03 07:17:10,735 ================================================================================
2026-01-03T07:17:10.735613981Z train_lora.py       :178  2026-01-03 07:17:10,735 Loading dataset from: /tmp/job_3ce3c69d-f189-42e6-a125-69df5fe54da1_1037j8zt/dataset.jsonl
2026-01-03T07:17:10.735705833Z train_lora.py       :197  2026-01-03 07:17:10,735 Line 1: Skipping metadata header
2026-01-03T07:17:10.736287009Z train_lora.py       :271  2026-01-03 07:17:10,736 ============================================================
2026-01-03T07:17:10.736295425Z train_lora.py       :272  2026-01-03 07:17:10,736 Dataset loading complete:
2026-01-03T07:17:10.736297118Z train_lora.py       :273  2026-01-03 07:17:10,736   - OpenAI format loaded: 0
2026-01-03T07:17:10.736304993Z train_lora.py       :274  2026-01-03 07:17:10,736   - BrightRun format converted: 14
2026-01-03T07:17:10.736307287Z train_lora.py       :275  2026-01-03 07:17:10,736   - Skipped/invalid: 0
2026-01-03T07:17:10.736308640Z train_lora.py       :276  2026-01-03 07:17:10,736   - Total conversations: 14
2026-01-03T07:17:10.736320973Z train_lora.py       :277  2026-01-03 07:17:10,736 ============================================================
2026-01-03T07:17:10.741553095Z train_lora.py       :362  2026-01-03 07:17:10,741 ================================================================================
2026-01-03T07:17:10.741557674Z train_lora.py       :363  2026-01-03 07:17:10,741 STEP 3: Loading base model with 4-bit quantization
2026-01-03T07:17:10.741559667Z train_lora.py       :364  2026-01-03 07:17:10,741 ================================================================================
2026-01-03T07:17:10.741585816Z train_lora.py       :374  2026-01-03 07:17:10,741 Model path: /workspace/models/Qwen3-Next-80B-A3B-Instruct
2026-01-03T07:17:10.742429684Z train_lora.py       :384  2026-01-03 07:17:10,742 Loading tokenizer...
2026-01-03T07:17:10.742587479Z train_lora.py       :612  2026-01-03 07:17:10,742 Training failed: Repo id must be in the form 'repo_name' or 'namespace/repo_name': '/workspace/models/Qwen3-Next-80B-A3B-Instruct'. Use `repo_type` argument if needed.
2026-01-03T07:17:10.742721229Z train_lora.py       :640  2026-01-03 07:17:10,742 Cleaned up temporary directory: /tmp/job_3ce3c69d-f189-42e6-a125-69df5fe54da1_1037j8zt
2026-01-03T07:17:10.742749602Z handler.py          :286  2026-01-03 07:17:10,742 ================================================================================
2026-01-03T07:17:10.742757206Z handler.py          :287  2026-01-03 07:17:10,742 Training failed!
2026-01-03T07:17:10.742764560Z handler.py          :288  2026-01-03 07:17:10,742 Error: Repo id must be in the form 'repo_name' or 'namespace/repo_name': '/workspace/models/Qwen3-Next-80B-A3B-Instruct'. Use `repo_type` argument if needed.
2026-01-03T07:17:10.742770681Z handler.py          :289  2026-01-03 07:17:10,742 ================================================================================
2026-01-03T07:17:10.992347252Z {"requestId": "ccd85999-a159-4518-ab44-cf0558a8467a-u2", "message": "Finished.", "level": "INFO"}