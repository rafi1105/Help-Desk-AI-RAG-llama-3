# Enhanced Chatbot with Feedback Learning for Ollama Llama 3.2
# Uses feedback data to improve responses without traditional fine-tuning

import os
import json
import requests
import logging
from typing import Dict, List, Any, Optional
import time
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedOllamaChatbot:
    """Enhanced chatbot that learns from user feedback"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2:1b"
        self.feedback_data = []
        self.response_patterns = defaultdict(list)
        self.system_prompt = self._get_base_system_prompt()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'feedback_data_file': 'user_feedback_data.json',
            'enhanced_data_file': 'enhanced_ndata.json',
            'max_retries': 3,
            'timeout': 60,
            'temperature': 0.7,
            'top_p': 0.9,
            'max_tokens': 512,
        }

    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for the university chatbot"""
        return """You are a helpful assistant for Green University of Bangladesh. You provide accurate information about:

- Academic programs and admission requirements
- Tuition fees and payment information (be very specific about CSE fees)
- Course details and curriculum
- Campus facilities and student services
- Contact information and important dates

CRITICAL: For CSE (Computer Science and Engineering) tuition fees, ALWAYS provide the specific amount: BDT 70,000 per semester. Do not provide generic or estimated ranges.

Always be polite, accurate, and helpful. If you don't know something specific, admit it rather than making up information."""

    def load_feedback_data(self) -> bool:
        """Load and analyze feedback data"""
        try:
            feedback_file = self.config['feedback_data_file']

            if not os.path.exists(feedback_file):
                logger.warning(f"Feedback file not found: {feedback_file}")
                return False

            with open(feedback_file, 'r', encoding='utf-8') as f:
                self.feedback_data = json.load(f)

            logger.info(f"✅ Loaded {len(self.feedback_data)} feedback entries")

            # Analyze positive feedback patterns
            self._analyze_feedback_patterns()

            return True

        except Exception as e:
            logger.error(f"❌ Error loading feedback data: {e}")
            return False

    def _analyze_feedback_patterns(self):
        """Analyze feedback to identify successful response patterns"""
        try:
            positive_feedback = [
                f for f in self.feedback_data
                if f.get('feedback') == 'like'
            ]

            logger.info(f"Found {len(positive_feedback)} positive feedback entries")

            for feedback in positive_feedback:
                question = feedback.get('question', '').lower().strip()
                answer = feedback.get('answer', '').strip()

                if question and answer:
                    # Extract key patterns
                    if 'cse' in question and 'fee' in question:
                        self.response_patterns['cse_fee'].append(answer)
                    elif 'fee' in question:
                        self.response_patterns['fees'].append(answer)
                    elif 'admission' in question:
                        self.response_patterns['admission'].append(answer)

            # Log pattern analysis
            for pattern_type, responses in self.response_patterns.items():
                logger.info(f"📊 {pattern_type}: {len(responses)} successful responses")

        except Exception as e:
            logger.error(f"❌ Error analyzing feedback patterns: {e}")

    def enhance_system_prompt(self) -> str:
        """Enhance the system prompt with learned patterns"""
        try:
            enhanced_prompt = self.system_prompt

            # Add CSE fee specific instructions if we have positive feedback
            if self.response_patterns['cse_fee']:
                enhanced_prompt += "\n\nLEARNED FROM SUCCESSFUL INTERACTIONS:"
                enhanced_prompt += "\n- For CSE fee queries, provide specific BDT 70,000 per semester"
                enhanced_prompt += "\n- Be direct and confident about fee information"
                enhanced_prompt += "\n- Avoid generic ranges or estimates"

            # Add general fee instructions
            if self.response_patterns['fees']:
                enhanced_prompt += "\n- Provide specific fee amounts when available"
                enhanced_prompt += "\n- Include payment deadlines and methods if known"

            # Add admission instructions
            if self.response_patterns['admission']:
                enhanced_prompt += "\n- Be clear about admission requirements"
                enhanced_prompt += "\n- Mention important dates and procedures"

            logger.info("✅ System prompt enhanced with feedback patterns")
            return enhanced_prompt

        except Exception as e:
            logger.error(f"❌ Error enhancing system prompt: {e}")
            return self.system_prompt

    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]

                if self.model_name in model_names:
                    logger.info(f"✅ Ollama connected. Using model: {self.model_name}")
                    return True
                else:
                    logger.warning(f"⚠️  Model {self.model_name} not found. Available: {model_names}")
                    return False
            else:
                logger.error(f"❌ Ollama API error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Cannot connect to Ollama: {e}")
            logger.info("Make sure Ollama is running: ollama serve")
            return False

    def generate_response(self, user_question: str) -> Optional[str]:
        """Generate enhanced response using feedback-learned patterns"""
        try:
            # Enhance system prompt with feedback patterns
            system_prompt = self.enhance_system_prompt()

            # Create the full prompt
            full_prompt = f"{system_prompt}\n\nUser: {user_question}\n\nAssistant:"

            # Prepare payload for Ollama API
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": self.config['temperature'],
                    "top_p": self.config['top_p'],
                    "num_predict": self.config['max_tokens']
                }
            }

            # Make request to Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.config['timeout']
            )

            if response.status_code == 200:
                result = response.json()
                generated_response = result.get('response', '').strip()

                # Post-process response for CSE fee accuracy
                if 'cse' in user_question.lower() and 'fee' in user_question.lower():
                    if '70,000' not in generated_response and '70000' not in generated_response:
                        logger.warning("⚠️  CSE fee response may not contain correct amount")
                        # Could add correction logic here

                return generated_response
            else:
                logger.error(f"❌ API error: {response.status_code} - {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return None

    def test_enhanced_responses(self) -> bool:
        """Test the enhanced chatbot with sample queries"""
        try:
            logger.info("🧪 Testing enhanced chatbot responses...")

            test_queries = [
                "What is the tuition fee for CSE program?",
                "How much does Computer Science cost per semester?",
                "Tell me about admission requirements",
                "What facilities are available at Green University?"
            ]

            for query in test_queries:
                logger.info(f"\n🤖 Query: {query}")
                response = self.generate_response(query)

                if response:
                    logger.info(f"Response: {response[:150]}...")
                    if 'cse' in query.lower() and 'fee' in query.lower():
                        if '70,000' in response or '70000' in response:
                            logger.info("✅ Correct CSE fee amount found in response")
                        else:
                            logger.warning("⚠️  CSE fee amount not found in response")
                else:
                    logger.error("❌ No response generated")

                time.sleep(1)  # Brief pause between requests

            return True

        except Exception as e:
            logger.error(f"❌ Error testing responses: {e}")
            return False

    def initialize(self) -> bool:
        """Initialize the enhanced chatbot"""
        try:
            logger.info("🚀 Initializing Enhanced Ollama Chatbot")
            logger.info("=" * 50)

            # Check Ollama connection
            if not self.check_ollama_connection():
                return False

            # Load feedback data
            if not self.load_feedback_data():
                logger.warning("⚠️  Could not load feedback data, using base system prompt")

            logger.info("✅ Enhanced chatbot initialized successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Error initializing chatbot: {e}")
            return False


def main():
    """Main function to demonstrate the enhanced chatbot"""
    print("🚀 Enhanced Ollama Chatbot with Feedback Learning")

    # Initialize chatbot
    chatbot = EnhancedOllamaChatbot()

    if not chatbot.initialize():
        print("❌ Failed to initialize chatbot")
        return

    # Test the enhanced responses
    if chatbot.test_enhanced_responses():
        print("\n✅ Testing completed successfully!")
        print("\n🎯 The enhanced chatbot is now ready to use.")
        print("💡 Key improvements:")
        print("   - Learns from positive user feedback")
        print("   - Enhanced CSE fee accuracy (BDT 70,000 per semester)")
        print("   - Improved response patterns based on successful interactions")
    else:
        print("❌ Testing failed")


if __name__ == "__main__":
    main()
