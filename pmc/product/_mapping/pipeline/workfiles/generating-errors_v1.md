## Requests Log
{
  "delayTime": 870,
  "executionTime": 1608,
  "id": "fb1f97b5-34d4-4db1-8a66-d40d47dfe196-u1",
  "output": {
    "error_message": "Dataset loading failed - invalid format or empty file",
    "job_id": "4e284001-d976-48f4-9b10-c45709b6e125",
    "status": "failed"
  },
  "status": "COMPLETED",
  "workerId": "qi77oc4zpdniy9"
}

## Worker Log
2026-01-03T06:23:01.661733839Z {"requestId": null, "message": "Jobs in queue: 1", "level": "INFO"}
2026-01-03T06:23:01.661752895Z {"requestId": null, "message": "Jobs in progress: 1", "level": "INFO"}
2026-01-03T06:23:01.661756241Z {"requestId": "fb1f97b5-34d4-4db1-8a66-d40d47dfe196-u1", "message": "Started.", "level": "INFO"}
2026-01-03T06:23:01.661827515Z handler.py          :192  2026-01-03 06:23:01,661 ================================================================================
2026-01-03T06:23:01.661836893Z handler.py          :193  2026-01-03 06:23:01,661 RunPod Handler: New job received
2026-01-03T06:23:01.661880264Z handler.py          :194  2026-01-03 06:23:01,661 ================================================================================
2026-01-03T06:23:01.661906844Z handler.py          :201  2026-01-03 06:23:01,661 Job ID: 4e284001-d976-48f4-9b10-c45709b6e125
2026-01-03T06:23:01.661908296Z handler.py          :202  2026-01-03 06:23:01,661 Input keys: ['callback_url', 'dataset_url', 'gpu_config', 'hyperparameters', 'job_id']
2026-01-03T06:23:01.661909158Z handler.py          :219  2026-01-03 06:23:01,661 Validation passed
2026-01-03T06:23:01.661911883Z handler.py          :231  2026-01-03 06:23:01,661 Base Model: mistralai/Mistral-7B-v0.1
2026-01-03T06:23:01.661913987Z handler.py          :232  2026-01-03 06:23:01,661 Learning Rate: 5e-05
2026-01-03T06:23:01.661914809Z handler.py          :233  2026-01-03 06:23:01,661 Batch Size: 4
2026-01-03T06:23:01.661916281Z handler.py          :234  2026-01-03 06:23:01,661 Epochs: 3
2026-01-03T06:23:01.661920740Z handler.py          :235  2026-01-03 06:23:01,661 LoRA Rank: 16
2026-01-03T06:23:01.661928364Z handler.py          :236  2026-01-03 06:23:01,661 GPU Type: A100-80GB
2026-01-03T06:23:01.661932492Z handler.py          :239  2026-01-03 06:23:01,661 Starting training execution...
2026-01-03T06:23:01.662009837Z train_lora.py       :246  2026-01-03 06:23:01,661 Working directory: /tmp/job_4e284001-d976-48f4-9b10-c45709b6e125_d7pgj8qo
2026-01-03T06:23:01.662014295Z train_lora.py       :249  2026-01-03 06:23:01,661 ================================================================================
2026-01-03T06:23:01.662020938Z train_lora.py       :250  2026-01-03 06:23:01,662 STEP 1: Downloading dataset
2026-01-03T06:23:01.662024544Z train_lora.py       :251  2026-01-03 06:23:01,662 ================================================================================
2026-01-03T06:23:01.662047367Z train_lora.py       :133  2026-01-03 06:23:01,662 Downloading dataset from: https://hqhtbxlgzysfbekexwku.supabase.co/storage/v1/object/s...
2026-01-03T06:23:03.240774981Z train_lora.py       :153  2026-01-03 06:23:03,240 Dataset downloaded successfully: 0.2MB
2026-01-03T06:23:03.241564170Z train_lora.py       :265  2026-01-03 06:23:03,241 ================================================================================
2026-01-03T06:23:03.241583205Z train_lora.py       :266  2026-01-03 06:23:03,241 STEP 2: Loading and preparing dataset
2026-01-03T06:23:03.241585099Z train_lora.py       :267  2026-01-03 06:23:03,241 ================================================================================
2026-01-03T06:23:03.241587994Z train_lora.py       :177  2026-01-03 06:23:03,241 Loading dataset from: /tmp/job_4e284001-d976-48f4-9b10-c45709b6e125_d7pgj8qo/dataset.jsonl
2026-01-03T06:23:03.241655511Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 1: Missing 'messages' field
2026-01-03T06:23:03.241693342Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 2: Missing 'messages' field
2026-01-03T06:23:03.241729299Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 3: Missing 'messages' field
2026-01-03T06:23:03.241788320Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 4: Missing 'messages' field
2026-01-03T06:23:03.241847611Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 5: Missing 'messages' field
2026-01-03T06:23:03.241878248Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 6: Missing 'messages' field
2026-01-03T06:23:03.241916009Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 7: Missing 'messages' field
2026-01-03T06:23:03.241968568Z train_lora.py       :192  2026-01-03 06:23:03,241 Line 8: Missing 'messages' field
2026-01-03T06:23:03.242051834Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 9: Missing 'messages' field
2026-01-03T06:23:03.242077822Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 10: Missing 'messages' field
2026-01-03T06:23:03.242103691Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 11: Missing 'messages' field
2026-01-03T06:23:03.242137154Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 12: Missing 'messages' field
2026-01-03T06:23:03.242159876Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 13: Missing 'messages' field
2026-01-03T06:23:03.242188009Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 14: Missing 'messages' field
2026-01-03T06:23:03.242224668Z train_lora.py       :192  2026-01-03 06:23:03,242 Line 15: Missing 'messages' field
2026-01-03T06:23:03.242235828Z train_lora.py       :196  2026-01-03 06:23:03,242 Loaded 0 conversations
2026-01-03T06:23:03.242242281Z train_lora.py       :199  2026-01-03 06:23:03,242 No valid conversations found in dataset
2026-01-03T06:23:03.242254503Z train_lora.py       :531  2026-01-03 06:23:03,242 Training failed: Dataset loading failed - invalid format or empty file
2026-01-03T06:23:03.242378696Z train_lora.py       :559  2026-01-03 06:23:03,242 Cleaned up temporary directory: /tmp/job_4e284001-d976-48f4-9b10-c45709b6e125_d7pgj8qo
2026-01-03T06:23:03.242389016Z handler.py          :286  2026-01-03 06:23:03,242 ================================================================================
2026-01-03T06:23:03.242395768Z handler.py          :287  2026-01-03 06:23:03,242 Training failed!
2026-01-03T06:23:03.242402411Z handler.py          :288  2026-01-03 06:23:03,242 Error: Dataset loading failed - invalid format or empty file
2026-01-03T06:23:03.242407380Z handler.py          :289  2026-01-03 06:23:03,242 ================================================================================
2026-01-03T06:23:03.482183604Z {"requestId": "fb1f97b5-34d4-4db1-8a66-d40d47dfe196-u1", "message": "Finished.", "level": "INFO"}