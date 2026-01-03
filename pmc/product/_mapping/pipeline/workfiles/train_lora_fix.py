# train_lora.py Dataset Loading Fix
# 
# This file contains the REPLACEMENT code for the load_dataset function
# in train_lora.py to support BrightRun format.
#
# HOW TO APPLY:
# 1. Open C:\Users\james\Master\BrightHub\BRun\brightrun-trainer\train_lora.py
# 2. Find the load_dataset function (around line 175-200)
# 3. Replace the entire function with the code below
# 4. Save the file
# 5. Rebuild Docker image

# =====================================================
# REPLACEMENT FUNCTION - Copy this entire function
# =====================================================

def load_dataset(self, dataset_path: str) -> List[Dict]:
    """
    Load dataset supporting both OpenAI Chat format and BrightRun format.
    
    OpenAI format: {"messages": [{"role": "...", "content": "..."}]}
    BrightRun format: {"system_prompt": "...", "current_user_input": "...", "target_response": "..."}
    
    Args:
        dataset_path: Path to JSONL dataset file
        
    Returns:
        List of conversation dictionaries in OpenAI format
    """
    conversations = []
    line_num = 0
    brightrun_converted = 0
    openai_loaded = 0
    skipped = 0
    
    logger.info(f"Loading dataset from: {dataset_path}")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_num += 1
            line = line.strip()
            if not line:
                continue
                
            try:
                data = json.loads(line)
                
                # Skip metadata line (BrightRun format has _meta header)
                if '_meta' in data:
                    logger.info(f"Line {line_num}: Skipping metadata header (version: {data.get('_meta', {}).get('version', 'unknown')})")
                    continue
                
                # ===== OpenAI Chat format (standard) =====
                if 'messages' in data:
                    # Validate messages array
                    if isinstance(data['messages'], list) and len(data['messages']) > 0:
                        conversations.append(data)
                        openai_loaded += 1
                        continue
                    else:
                        logger.warning(f"Line {line_num}: Empty or invalid 'messages' array")
                        skipped += 1
                        continue
                
                # ===== BrightRun LoRA format - convert to OpenAI format =====
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
                                if content:  # Only add non-empty messages
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
                    
                    # Add target response (this is what we're training to generate)
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
                        logger.warning(f"Line {line_num}: BrightRun format but insufficient messages after conversion")
                        skipped += 1
                        continue
                
                # Unknown format
                logger.warning(f"Line {line_num}: Unknown format - missing 'messages' or 'target_response'")
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
    
    return conversations

# =====================================================
# END OF REPLACEMENT FUNCTION
# =====================================================

# VERIFICATION:
# After applying this fix, the worker logs should show:
#   "BrightRun format converted: 15"
#   "Total conversations: 15"
# Instead of:
#   "Missing 'messages' field"
#   "Loaded 0 conversations"
