"""
LoRA Fine-Tuning Training Script with QLoRA (4-bit Quantization)

This script handles the actual training process:
- Loads base model with 4-bit quantization
- Downloads dataset from Supabase Storage
- Configures LoRA adapters using PEFT
- Trains with SFTTrainer
- Reports progress and metrics
- Uploads trained adapter to Supabase Storage

Author: Bright Run AI
Date: December 28, 2025
"""

import os
import json
import logging
import tempfile
import tarfile
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import torch
import requests
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    TrainerCallback
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import Dataset
from supabase import create_client, Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProgressCallback(TrainerCallback):
    """Custom callback to report training progress."""
    
    def __init__(self, status_manager, job_id: str, total_steps: int):
        self.status_manager = status_manager
        self.job_id = job_id
        self.total_steps = total_steps
        self.start_time = time.time()
        
    def on_step_end(self, args, state, control, **kwargs):
        """Called at the end of each training step."""
        current_step = state.global_step
        current_epoch = int(state.epoch) if state.epoch else 0
        
        # Calculate progress
        progress = (current_step / self.total_steps) * 100
        
        # Get latest metrics
        logs = state.log_history[-1] if state.log_history else {}
        training_loss = logs.get('loss', 0.0)
        learning_rate = logs.get('learning_rate', 0.0)
        
        # Calculate throughput
        elapsed_time = time.time() - self.start_time
        throughput = current_step / elapsed_time if elapsed_time > 0 else 0
        
        # Get GPU utilization
        gpu_util = self._get_gpu_utilization()
        
        # Update status
        self.status_manager.update_status(
            job_id=self.job_id,
            status='running',
            stage='training',
            progress=progress,
            current_epoch=current_epoch,
            current_step=current_step,
            metrics={
                'training_loss': training_loss,
                'learning_rate': learning_rate,
                'throughput': throughput,
                'gpu_utilization': gpu_util,
            }
        )
        
        # Log progress every 10 steps
        if current_step % 10 == 0:
            logger.info(
                f"Step {current_step}/{self.total_steps} "
                f"({progress:.1f}%) - Loss: {training_loss:.4f}"
            )
    
    def on_epoch_end(self, args, state, control, **kwargs):
        """Called at the end of each epoch."""
        current_epoch = int(state.epoch) if state.epoch else 0
        logger.info(f"Completed epoch {current_epoch}")
    
    def _get_gpu_utilization(self) -> float:
        """Get current GPU utilization percentage."""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader,nounits'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                return float(result.stdout.strip().split('\n')[0])
        except Exception as e:
            logger.warning(f"Failed to get GPU utilization: {e}")
        return 0.0


def download_dataset(dataset_url: str, output_path: str) -> bool:
    """
    Download dataset from Supabase Storage.
    
    Args:
        dataset_url: Signed URL to dataset file
        output_path: Local path to save dataset
        
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Downloading dataset from: {dataset_url[:60]}...")
    
    try:
        response = requests.get(dataset_url, stream=True, timeout=300)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Log progress every 10MB
                    if downloaded % (10 * 1024 * 1024) == 0:
                        progress = (downloaded / total_size * 100) if total_size > 0 else 0
                        logger.info(f"Downloaded: {downloaded / 1024 / 1024:.1f}MB ({progress:.1f}%)")
        
        logger.info(f"Dataset downloaded successfully: {downloaded / 1024 / 1024:.1f}MB")
        return True
        
    except requests.RequestException as e:
        logger.error(f"Failed to download dataset: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error downloading dataset: {e}")
        return False


def load_and_prepare_dataset(dataset_path: str) -> Optional[Dataset]:
    """
    Load JSONL dataset and prepare for training.
    
    Supports two formats:
    1. OpenAI Chat format: {"messages": [{"role": "user", "content": "..."}, ...]}
    2. BrightRun format: {"system_prompt": "...", "current_user_input": "...", "target_response": "..."}
    
    Args:
        dataset_path: Path to JSONL file
        
    Returns:
        Hugging Face Dataset object or None if failed
    """
    logger.info(f"Loading dataset from: {dataset_path}")
    
    try:
        conversations = []
        openai_loaded = 0
        brightrun_converted = 0
        skipped = 0
        
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    data = json.loads(line)
                    
                    # Skip metadata line (BrightRun format has _meta header)
                    if '_meta' in data:
                        logger.info(f"Line {line_num}: Skipping metadata header")
                        continue
                    
                    # OpenAI Chat format (standard)
                    if 'messages' in data:
                        if isinstance(data['messages'], list) and len(data['messages']) > 0:
                            conversations.append(data)
                            openai_loaded += 1
                            continue
                        else:
                            logger.warning(f"Line {line_num}: Empty 'messages' array")
                            skipped += 1
                            continue
                    
                    # BrightRun format - convert to OpenAI format
                    if 'target_response' in data and 'current_user_input' in data:
                        messages = []
                        
                        # Add system prompt if present
                        system_prompt = data.get('system_prompt')
                        if system_prompt and isinstance(system_prompt, str) and system_prompt.strip():
                            messages.append({
                                "role": "system", 
                                "content": system_prompt.strip()
                            })
                        
                        # Add conversation history (previous turns)
                        conversation_history = data.get('conversation_history', [])
                        if isinstance(conversation_history, list):
                            for msg in conversation_history:
                                if isinstance(msg, dict) and 'content' in msg:
                                    role = msg.get('role', 'user')
                                    content = msg.get('content', '')
                                    if content:
                                        messages.append({
                                            "role": role,
                                            "content": content
                                        })
                        
                        # Add current user input
                        user_input = data.get('current_user_input', '')
                        if user_input:
                            messages.append({
                                "role": "user",
                                "content": user_input
                            })
                        
                        # Add target response (training target)
                        target = data.get('target_response', '')
                        if target:
                            messages.append({
                                "role": "assistant", 
                                "content": target
                            })
                        
                        # Only add if we have at least user+assistant pair
                        if len([m for m in messages if m['role'] in ['user', 'assistant']]) >= 2:
                            conversations.append({"messages": messages})
                            brightrun_converted += 1
                            continue
                        else:
                            logger.warning(f"Line {line_num}: Insufficient messages after conversion")
                            skipped += 1
                            continue
                    
                    # Unknown format
                    logger.warning(f"Line {line_num}: Unknown format")
                    skipped += 1
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"Line {line_num}: Invalid JSON - {e}")
                    skipped += 1
        
        # Log summary
        logger.info(f"=" * 60)
        logger.info(f"Dataset loading complete:")
        logger.info(f"  - OpenAI format loaded: {openai_loaded}")
        logger.info(f"  - BrightRun format converted: {brightrun_converted}")
        logger.info(f"  - Skipped/invalid: {skipped}")
        logger.info(f"  - Total conversations: {len(conversations)}")
        logger.info(f"=" * 60)
        
        if len(conversations) == 0:
            logger.error("No valid conversations found in dataset")
            return None
        
        # Create Hugging Face Dataset
        dataset = Dataset.from_dict({"messages": [c["messages"] for c in conversations]})
        
        return dataset
        
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return None


def format_chat_template(example, tokenizer):
    """Format messages for training."""
    messages = example["messages"]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
    return {"text": text}


def train_lora_model(
    job_id: str,
    dataset_url: str,
    hyperparameters: Dict[str, Any],
    gpu_config: Dict[str, Any],
    callback_url: Optional[str],
    status_manager
) -> Dict[str, Any]:
    """
    Main training function.
    
    Args:
        job_id: Unique job identifier
        dataset_url: Signed URL to dataset
        hyperparameters: Training hyperparameters
        gpu_config: GPU configuration
        callback_url: URL for status callbacks
        status_manager: StatusManager instance
        
    Returns:
        Dictionary with training results
    """
    temp_dir = None
    
    try:
        # Create temporary directory for this job
        temp_dir = tempfile.mkdtemp(prefix=f"job_{job_id}_")
        logger.info(f"Working directory: {temp_dir}")
        
        # Step 1: Download dataset
        logger.info("=" * 80)
        logger.info("STEP 1: Downloading dataset")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='downloading',
            progress=5.0
        )
        
        dataset_path = os.path.join(temp_dir, "dataset.jsonl")
        if not download_dataset(dataset_url, dataset_path):
            raise Exception("Dataset download failed - please check URL and retry")
        
        # Step 2: Load and prepare dataset
        logger.info("=" * 80)
        logger.info("STEP 2: Loading and preparing dataset")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='preparing',
            progress=10.0
        )
        
        dataset = load_and_prepare_dataset(dataset_path)
        if dataset is None:
            raise Exception("Dataset loading failed - invalid format or empty file")
        
        # Step 3: Load model with 4-bit quantization
        logger.info("=" * 80)
        logger.info("STEP 3: Loading base model with 4-bit quantization")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='loading_model',
            progress=15.0
        )
        
        # Determine model source: environment variable, local path, or HuggingFace
        env_model_path = os.environ.get('MODEL_PATH')
        base_model = hyperparameters.get('base_model', 'mistralai/Mistral-7B-v0.1')
        
        # Priority: 1) ENV var if exists locally, 2) hyperparameters base_model
        if env_model_path and os.path.exists(env_model_path):
            model_path = env_model_path
            logger.info(f"Using cached model from: {model_path}")
        else:
            # Use HuggingFace model ID from hyperparameters (will download)
            model_path = base_model
            logger.info(f"Downloading model from HuggingFace: {model_path}")
        
        # Configure 4-bit quantization (QLoRA)
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )
        
        logger.info("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        
        # Set pad token if not present
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        logger.info("Loading model with 4-bit quantization...")
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16
        )
        
        logger.info(f"Model loaded successfully on device: {model.device}")
        
        # Step 4: Configure LoRA
        logger.info("=" * 80)
        logger.info("STEP 4: Configuring LoRA adapters")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='configuring',
            progress=20.0
        )
        
        lora_config = LoraConfig(
            r=hyperparameters.get('rank', hyperparameters.get('lora_rank', 16)),
            lora_alpha=hyperparameters.get('alpha', hyperparameters.get('lora_alpha', 32)),
            lora_dropout=hyperparameters.get('dropout', hyperparameters.get('lora_dropout', 0.05)),
            target_modules=[
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        logger.info(f"LoRA Config: r={lora_config.r}, alpha={lora_config.lora_alpha}, dropout={lora_config.lora_dropout}")
        logger.info(f"Target modules: {lora_config.target_modules}")
        
        # Prepare model for k-bit training
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, lora_config)
        
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        total_params = sum(p.numel() for p in model.parameters())
        logger.info(f"Trainable parameters: {trainable_params:,} ({trainable_params/total_params*100:.2f}%)")
        
        # Step 5: Prepare training data
        logger.info("=" * 80)
        logger.info("STEP 5: Formatting training data")
        logger.info("=" * 80)
        
        dataset = dataset.map(lambda x: format_chat_template(x, tokenizer), num_proc=1)
        
        # Step 6: Configure training
        logger.info("=" * 80)
        logger.info("STEP 6: Configuring training parameters")
        logger.info("=" * 80)
        
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Calculate total steps for progress tracking
        steps_per_epoch = len(dataset) // hyperparameters['batch_size']
        total_steps = steps_per_epoch * hyperparameters.get('epochs', hyperparameters.get('num_epochs', 3))
        
        logger.info(f"Dataset size: {len(dataset)}")
        logger.info(f"Batch size: {hyperparameters['batch_size']}")
        logger.info(f"Epochs: {hyperparameters.get('epochs', hyperparameters.get('num_epochs', 3))}")
        logger.info(f"Steps per epoch: {steps_per_epoch}")
        logger.info(f"Total training steps: {total_steps}")
        
        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=hyperparameters.get('epochs', hyperparameters.get('num_epochs', 3)),
            per_device_train_batch_size=hyperparameters['batch_size'],
            gradient_accumulation_steps=1,
            learning_rate=hyperparameters['learning_rate'],
            logging_steps=10,
            save_strategy="epoch",
            fp16=True,
            optim="adamw_torch",
            warmup_ratio=0.1,
            lr_scheduler_type="cosine",
            report_to="none",
            remove_unused_columns=False,
        )
        
        # Create progress callback
        progress_callback = ProgressCallback(status_manager, job_id, total_steps)
        
        # Step 7: Train model
        logger.info("=" * 80)
        logger.info("STEP 7: Training LoRA adapters")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='training',
            progress=25.0,
            current_epoch=0,
            current_step=0
        )
        
        trainer = SFTTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            dataset_text_field="text",
            max_seq_length=2048,
            callbacks=[progress_callback],
        )
        
        logger.info("Starting training...")
        train_start = time.time()
        
        try:
            trainer.train()
            train_duration = time.time() - train_start
            logger.info(f"Training completed in {train_duration/60:.2f} minutes")
        except RuntimeError as e:
            if "out of memory" in str(e).lower():
                raise Exception(
                    "CUDA Out of Memory: Try reducing batch_size (current: "
                    f"{hyperparameters['batch_size']}) or lora_rank (current: "
                    f"{hyperparameters['lora_rank']})"
                )
            raise
        
        # Step 8: Save adapter
        logger.info("=" * 80)
        logger.info("STEP 8: Saving LoRA adapter")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='saving',
            progress=95.0
        )
        
        adapter_dir = os.path.join(temp_dir, "adapter")
        os.makedirs(adapter_dir, exist_ok=True)
        
        model.save_pretrained(adapter_dir)
        tokenizer.save_pretrained(adapter_dir)
        
        logger.info(f"Adapter saved to: {adapter_dir}")
        
        # Step 9: Create archive
        logger.info("Creating tar.gz archive...")
        archive_path = os.path.join(temp_dir, f"{job_id}.tar.gz")
        
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(adapter_dir, arcname=os.path.basename(adapter_dir))
        
        archive_size = os.path.getsize(archive_path)
        logger.info(f"Archive created: {archive_size / 1024 / 1024:.2f}MB")
        
        # Step 10: Upload to Supabase
        logger.info("=" * 80)
        logger.info("STEP 10: Uploading adapter to Supabase Storage")
        logger.info("=" * 80)
        
        status_manager.update_status(
            job_id=job_id,
            status='running',
            stage='uploading',
            progress=97.0
        )
        
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        
        if not supabase_url or not supabase_key:
            logger.warning("Supabase credentials not found - skipping upload")
            adapter_path = f"local://{archive_path}"
        else:
            supabase: Client = create_client(supabase_url, supabase_key)
            
            storage_path = f"adapters/{job_id}.tar.gz"
            
            with open(archive_path, 'rb') as f:
                response = supabase.storage.from_('lora-models').upload(
                    storage_path,
                    f.read(),
                    file_options={"content-type": "application/gzip"}
                )
            
            adapter_path = f"lora-models/{storage_path}"
            logger.info(f"Adapter uploaded to: {adapter_path}")
        
        # Step 11: Complete
        logger.info("=" * 80)
        logger.info("TRAINING COMPLETE")
        logger.info("=" * 80)
        
        final_metrics = {
            'training_loss': progress_callback.status_manager.get_status(job_id).get('metrics', {}).get('training_loss', 0.0),
            'total_steps': total_steps,
            'train_duration_minutes': train_duration / 60,
        }
        
        status_manager.update_status(
            job_id=job_id,
            status='completed',
            stage='completed',
            progress=100.0,
            metrics=final_metrics
        )
        
        return {
            "status": "completed",
            "job_id": job_id,
            "adapter_path": adapter_path,
            "metrics": final_metrics,
            "progress": 100.0
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Training failed: {error_msg}")
        
        # Special error handling for common issues
        if "out of memory" in error_msg.lower():
            error_msg = f"GPU Out of Memory: {error_msg}. Try reducing batch_size or lora_rank."
        elif "download" in error_msg.lower():
            error_msg = f"Download failed: {error_msg}. Please check dataset URL and retry."
        elif "nan" in error_msg.lower():
            error_msg = f"Training instability (NaN): {error_msg}. Try reducing learning_rate."
        
        status_manager.update_status(
            job_id=job_id,
            status='failed',
            error_message=error_msg
        )
        
        return {
            "status": "failed",
            "job_id": job_id,
            "error_message": error_msg
        }
        
    finally:
        # Cleanup temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp directory: {e}")
