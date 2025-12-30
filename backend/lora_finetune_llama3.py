# LoRA Fine-tuning Script for Llama 3.2 Model
# Adapted for Green University Chatbot with feedback-based learning

import os
import json
import torch
from datasets import load_dataset, Dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import bitsandbytes as bnb
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Llama3LoRAFinetuner:
    """LoRA fine-tuning for Llama 3.2 model using feedback data"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.model = None
        self.tokenizer = None
        self.peft_model = None

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for Llama 3.2 LoRA fine-tuning"""
        return {
            'model_name': 'meta-llama/Meta-Llama-3.1-8B-Instruct',  # Llama 3.1 8B as base
            'max_seq_length': 512,
            'lora_r': 16,
            'lora_alpha': 32,
            'lora_dropout': 0.05,
            'target_modules': [
                "q_proj", "k_proj", "v_proj", "o_proj",
                "gate_proj", "up_proj", "down_proj"
            ],  # Llama 3.2 specific modules
            'per_device_train_batch_size': 2,
            'gradient_accumulation_steps': 4,
            'learning_rate': 2e-4,
            'num_train_epochs': 3,
            'warmup_steps': 100,
            'logging_steps': 10,
            'save_steps': 500,
            'output_dir': './lora_llama3_finetuned',
            'feedback_data_file': 'user_feedback_data.json',
            'use_4bit': True,
            'use_nested_quant': False,
        }

    def load_base_model(self):
        """Load the base Llama 3.2 model with quantization"""
        try:
            logger.info(f"Loading base model: {self.config['model_name']}")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config['model_name'],
                trust_remote_code=True
            )

            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            # Load model with 4-bit quantization
            if self.config['use_4bit']:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config['model_name'],
                    load_in_4bit=True,
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True,
                    quantization_config=bnb.BitsAndBytesConfig(
                        load_in_4bit=True,
                        bnb_4bit_compute_dtype=torch.float16,
                        bnb_4bit_use_double_quant=self.config['use_nested_quant'],
                        bnb_4bit_quant_type="nf4"
                    )
                )
            else:
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.config['model_name'],
                    torch_dtype=torch.float16,
                    device_map="auto",
                    trust_remote_code=True
                )

            logger.info("✅ Base model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error loading base model: {e}")
            return False

    def setup_lora(self):
        """Setup LoRA configuration for Llama 3.2"""
        try:
            logger.info("Setting up LoRA configuration...")

            # Prepare model for k-bit training
            self.model = prepare_model_for_kbit_training(self.model)

            # LoRA configuration optimized for Llama 3.2
            lora_config = LoraConfig(
                r=self.config['lora_r'],
                lora_alpha=self.config['lora_alpha'],
                target_modules=self.config['target_modules'],
                lora_dropout=self.config['lora_dropout'],
                bias="none",
                task_type="CAUSAL_LM",
                modules_to_save=["embed_tokens", "lm_head"]  # Save embeddings and output layer
            )

            # Apply LoRA
            self.peft_model = get_peft_model(self.model, lora_config)

            # Print trainable parameters
            self.peft_model.print_trainable_parameters()

            logger.info("✅ LoRA setup completed")
            return True

        except Exception as e:
            logger.error(f"❌ Error setting up LoRA: {e}")
            return False

    def prepare_training_data(self, feedback_data: List[Dict]) -> Dataset:
        """Prepare feedback data for training"""
        try:
            logger.info(f"Preparing training data from {len(feedback_data)} feedback entries")

            # Convert feedback to training examples
            training_examples = []

            for feedback in feedback_data:
                if feedback.get('feedback') == 'like':  # Only use positive feedback
                    question = feedback.get('question', '')
                    answer = feedback.get('answer', '')

                    if question and answer:
                        # Create a conversational format
                        conversation = f"Human: {question}\n\nAssistant: {answer}"

                        training_examples.append({
                            'text': conversation,
                            'question': question,
                            'answer': answer
                        })

            if not training_examples:
                logger.warning("No positive feedback found for training")
                return None

            # Create dataset
            dataset = Dataset.from_list(training_examples)

            # Tokenize dataset
            def tokenize_function(examples):
                return self.tokenizer(
                    examples['text'],
                    truncation=True,
                    padding='max_length',
                    max_length=self.config['max_seq_length']
                )

            tokenized_dataset = dataset.map(
                tokenize_function,
                batched=True,
                remove_columns=['text', 'question', 'answer']
            )

            logger.info(f"✅ Training dataset prepared with {len(tokenized_dataset)} examples")
            return tokenized_dataset

        except Exception as e:
            logger.error(f"❌ Error preparing training data: {e}")
            return None

    def load_feedback_data(self) -> List[Dict]:
        """Load feedback data for training"""
        try:
            feedback_file = self.config['feedback_data_file']

            if not os.path.exists(feedback_file):
                logger.warning(f"Feedback file not found: {feedback_file}")
                return []

            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)

            logger.info(f"Loaded {len(feedback_data)} feedback entries")
            return feedback_data

        except Exception as e:
            logger.error(f"Error loading feedback data: {e}")
            return []

    def train(self):
        """Train the LoRA model"""
        try:
            logger.info("Starting LoRA training...")

            # Load and prepare data
            feedback_data = self.load_feedback_data()
            if not feedback_data:
                logger.error("No feedback data available for training")
                return False

            train_dataset = self.prepare_training_data(feedback_data)
            if train_dataset is None:
                logger.error("Failed to prepare training data")
                return False

            # Training arguments
            training_args = TrainingArguments(
                output_dir=self.config['output_dir'],
                per_device_train_batch_size=self.config['per_device_train_batch_size'],
                gradient_accumulation_steps=self.config['gradient_accumulation_steps'],
                learning_rate=self.config['learning_rate'],
                num_train_epochs=self.config['num_train_epochs'],
                warmup_steps=self.config['warmup_steps'],
                logging_steps=self.config['logging_steps'],
                save_steps=self.config['save_steps'],
                save_total_limit=2,
                evaluation_strategy="no",
                load_best_model_at_end=False,
                fp16=True,
                gradient_checkpointing=True,
                optim="paged_adamw_8bit"
            )

            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False
            )

            # Trainer
            trainer = Trainer(
                model=self.peft_model,
                args=training_args,
                train_dataset=train_dataset,
                data_collator=data_collator
            )

            # Train
            logger.info("🚀 Starting training...")
            trainer.train()

            # Save model
            self.save_model()

            logger.info("✅ Training completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error during training: {e}")
            return False

    def save_model(self):
        """Save the fine-tuned model"""
        try:
            output_dir = self.config['output_dir']
            os.makedirs(output_dir, exist_ok=True)

            # Save LoRA adapters
            self.peft_model.save_pretrained(output_dir)

            # Save tokenizer
            self.tokenizer.save_pretrained(output_dir)

            # Save configuration
            with open(os.path.join(output_dir, 'training_config.json'), 'w') as f:
                json.dump(self.config, f, indent=2)

            logger.info(f"✅ Model saved to {output_dir}")
            return True

        except Exception as e:
            logger.error(f"❌ Error saving model: {e}")
            return False

    def load_finetuned_model(self, model_path: str):
        """Load a previously fine-tuned model"""
        try:
            logger.info(f"Loading fine-tuned model from {model_path}")

            # Load base model
            if not self.load_base_model():
                return False

            # Load LoRA adapters
            from peft import PeftModel
            self.peft_model = PeftModel.from_pretrained(
                self.model,
                model_path,
                torch_dtype=torch.float16
            )

            logger.info("✅ Fine-tuned model loaded successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error loading fine-tuned model: {e}")
            return False

    def generate_response(self, prompt: str, max_length: int = 256) -> str:
        """Generate response using the fine-tuned model"""
        try:
            if self.peft_model is None:
                logger.error("Model not loaded")
                return ""

            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.peft_model.device)

            # Generate
            with torch.no_grad():
                outputs = self.peft_model.generate(
                    **inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Remove the input prompt from response
            if response.startswith(prompt):
                response = response[len(prompt):].strip()

            return response

        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return ""


def main():
    """Main training function"""
    print("🚀 Starting Llama 3.2 LoRA Fine-tuning for Green University Chatbot")

    # Initialize fine-tuner
    finetuner = Llama3LoRAFinetuner()

    # Load base model
    if not finetuner.load_base_model():
        print("❌ Failed to load base model")
        return

    # Setup LoRA
    if not finetuner.setup_lora():
        print("❌ Failed to setup LoRA")
        return

    # Train
    if finetuner.train():
        print("✅ Fine-tuning completed successfully!")
        print(f"Model saved to: {finetuner.config['output_dir']}")

        # Test the model
        test_prompt = "What are the admission requirements for Green University?"
        response = finetuner.generate_response(test_prompt)
        print(f"\nTest Response: {response}")
    else:
        print("❌ Fine-tuning failed")


if __name__ == "__main__":
    main()
