# LoRA Fine-tuning Script for Ollama Llama 3.2 Model
# Adapted for Green University Chatbot with feedback-based learning

import os
import json
import requests
import logging
from typing import Dict, List, Any, Optional
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaLoRAFinetuner:
    """LoRA fine-tuning for Ollama Llama 3.2 model using feedback data"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2:1b"  # Using the 1B parameter model
        self.finetuned_model_name = "llama3.2:1b-finetuned"

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration for Ollama LoRA fine-tuning"""
        return {
            'feedback_data_file': 'user_feedback_data.json',
            'modelfile_template': '''
FROM llama3.2:1b

# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

# System message for university chatbot
SYSTEM """
You are a helpful assistant for Green University. You provide accurate information about:
- Academic programs and admission requirements
- Tuition fees and payment information
- Course details and curriculum
- Campus facilities and student services
- Contact information and important dates

Always be polite, accurate, and helpful. If you don't know something, admit it rather than making up information.
"""

# Add training data as context
{training_context}
''',
            'max_retries': 3,
            'timeout': 300,  # 5 minutes timeout
        }

    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                logger.info(f"✅ Ollama connected. Available models: {model_names}")

                if self.model_name in model_names:
                    logger.info(f"✅ Base model {self.model_name} is available")
                    return True
                else:
                    logger.warning(f"⚠️  Base model {self.model_name} not found. Available: {model_names}")
                    return False
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Cannot connect to Ollama: {e}")
            logger.info("Make sure Ollama is running: ollama serve")
            return False

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

    def prepare_training_context(self, feedback_data: List[Dict]) -> str:
        """Prepare training context from feedback data"""
        try:
            logger.info("Preparing training context from feedback data...")

            # Filter positive feedback only
            positive_feedback = [
                f for f in feedback_data
                if f.get('feedback') == 'like' and f.get('question') and f.get('answer')
            ]

            if not positive_feedback:
                logger.warning("No positive feedback found for training")
                return ""

            # Create training examples
            training_examples = []

            for feedback in positive_feedback:
                question = feedback.get('question', '').strip()
                answer = feedback.get('answer', '').strip()

                if question and answer:
                    example = f"""
# Example: {question}
Q: {question}
A: {answer}
"""
                    training_examples.append(example)

            # Combine all examples
            training_context = "\n".join(training_examples)

            logger.info(f"✅ Prepared {len(positive_feedback)} training examples")
            return training_context

        except Exception as e:
            logger.error(f"❌ Error preparing training context: {e}")
            return ""

    def create_modelfile(self, training_context: str) -> str:
        """Create Ollama modelfile for fine-tuning"""
        try:
            modelfile_content = self.config['modelfile_template'].format(
                training_context=training_context
            )

            # Save modelfile
            modelfile_path = "Modelfile"
            with open(modelfile_path, 'w', encoding='utf-8') as f:
                f.write(modelfile_content)

            logger.info(f"✅ Modelfile created: {modelfile_path}")
            return modelfile_path

        except Exception as e:
            logger.error(f"❌ Error creating modelfile: {e}")
            return ""

    def create_finetuned_model(self, modelfile_path: str) -> bool:
        """Create the fine-tuned model using Ollama"""
        try:
            logger.info(f"Creating fine-tuned model: {self.finetuned_model_name}")

            # Build the model using ollama create command
            import subprocess

            cmd = ["ollama", "create", self.finetuned_model_name, "-f", modelfile_path]

            logger.info(f"Running command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config['timeout']
            )

            if result.returncode == 0:
                logger.info("✅ Fine-tuned model created successfully")
                logger.info(f"Model output: {result.stdout}")
                return True
            else:
                logger.error(f"❌ Failed to create model: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            logger.error("❌ Model creation timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error creating fine-tuned model: {e}")
            return False

    def test_finetuned_model(self) -> bool:
        """Test the fine-tuned model with sample queries"""
        try:
            logger.info("Testing fine-tuned model...")

            test_questions = [
                "What are the tuition fees for CSE program?",
                "How can I apply for admission?",
                "What facilities are available on campus?"
            ]

            for question in test_questions:
                logger.info(f"\n🤖 Testing: {question}")

                response = self.generate_response(question)
                if response:
                    logger.info(f"Response: {response[:200]}...")
                else:
                    logger.warning("No response generated")

                time.sleep(1)  # Brief pause between requests

            return True

        except Exception as e:
            logger.error(f"❌ Error testing model: {e}")
            return False

    def generate_response(self, prompt: str, max_tokens: int = 256) -> Optional[str]:
        """Generate response using the fine-tuned model"""
        try:
            payload = {
                "model": self.finetuned_model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                logger.error(f"❌ API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {e}")
            return None

    def finetune(self) -> bool:
        """Complete fine-tuning process"""
        try:
            logger.info("🚀 Starting Ollama LoRA Fine-tuning Process")
            logger.info("=" * 60)

            # Step 1: Check Ollama connection
            if not self.check_ollama_connection():
                logger.error("❌ Ollama connection failed")
                return False

            # Step 2: Load feedback data
            feedback_data = self.load_feedback_data()
            if not feedback_data:
                logger.error("❌ No feedback data available")
                return False

            # Step 3: Prepare training context
            training_context = self.prepare_training_context(feedback_data)
            if not training_context:
                logger.error("❌ Failed to prepare training context")
                return False

            # Step 4: Create modelfile
            modelfile_path = self.create_modelfile(training_context)
            if not modelfile_path:
                logger.error("❌ Failed to create modelfile")
                return False

            # Step 5: Create fine-tuned model
            if not self.create_finetuned_model(modelfile_path):
                logger.error("❌ Failed to create fine-tuned model")
                return False

            # Step 6: Test the model
            if not self.test_finetuned_model():
                logger.warning("⚠️  Model testing failed, but model was created")

            logger.info("✅ Fine-tuning process completed successfully!")
            logger.info(f"🎯 Fine-tuned model: {self.finetuned_model_name}")
            return True

        except Exception as e:
            logger.error(f"❌ Error during fine-tuning: {e}")
            return False

    def save_config(self):
        """Save the current configuration"""
        try:
            config_file = "lora_config.json"
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"✅ Configuration saved to {config_file}")
        except Exception as e:
            logger.error(f"❌ Error saving config: {e}")


def main():
    """Main fine-tuning function"""
    print("🚀 Starting Ollama Llama 3.2 LoRA Fine-tuning for Green University Chatbot")

    # Initialize fine-tuner
    finetuner = OllamaLoRAFinetuner()

    # Save configuration
    finetuner.save_config()

    # Run fine-tuning
    if finetuner.finetune():
        print("✅ Fine-tuning completed successfully!")
        print(f"🎯 Fine-tuned model available as: {finetuner.finetuned_model_name}")
        print("\nTo use the fine-tuned model in your chatbot:")
        print("1. Update your rag_api_server.py to use the new model name")
        print("2. Restart your chatbot server")
        print("3. Test with CSE fee queries to see improvements")
    else:
        print("❌ Fine-tuning failed. Check the logs above for details.")


if __name__ == "__main__":
    main()
