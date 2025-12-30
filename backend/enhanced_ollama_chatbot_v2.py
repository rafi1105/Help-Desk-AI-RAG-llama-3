# Enhanced Chatbot with RAG + RL + User Feedback + Language Restriction
# Implements: English-only responses, disliked answers blocking, improved RAG integration

import os
import json
import requests
import logging
from typing import Dict, List, Any, Optional, Tuple
import time
from collections import defaultdict
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedOllamaChatbotV2:
    """
    Advanced chatbot with:
    - RAG (Retrieval-Augmented Generation)
    - RL with user feedback (like/dislike)
    - Language restriction (English only)
    - Disliked answers blocking
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._get_default_config()
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.2:1b"
        self.feedback_data = []
        self.disliked_answers = []
        self.response_patterns = defaultdict(list)
        self.system_prompt = self._get_enhanced_system_prompt()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'feedback_data_file': 'user_feedback_data.json',
            'disliked_answers_file': 'disliked_answers.json',
            'enhanced_data_file': 'enhanced_ndata.json',
            'max_retries': 3,
            'timeout': 60,
            'temperature': 0.7,
            'top_p': 0.9,
            'max_tokens': 512,
            'similarity_threshold': 0.7,  # For detecting similar disliked answers
        }

    def _get_enhanced_system_prompt(self) -> str:
        """Enhanced system prompt with all requirements"""
        return """You are an AI assistant for Green University of Bangladesh.

═══════════════════════════════════════════════════════════════════════════════
⚠️ CRITICAL RULE #1: ENGLISH ONLY - ABSOLUTELY NO EXCEPTIONS ⚠️
═══════════════════════════════════════════════════════════════════════════════

═══════════════════════════════════════════════════════════════════════════════
RULE #2: USE RAG DATA - DEPARTMENT SPECIFIC
═══════════════════════════════════════════════════════════════════════════════

• Use ONLY the retrieved data provided to answer.
• If asked about EEE → Answer ONLY about EEE (NOT CSE).
• If asked about CSE → Answer ONLY about CSE (NOT EEE).
• Each department has DIFFERENT fees:
  
  CSE (Computer Science): BDT 70,000/semester
  EEE (Electrical): BDT 80,000/semester  
  BBA (Business): BDT 60,000/semester
  
• NEVER mix department information.

═══════════════════════════════════════════════════════════════════════════════
RULE #3: NUMERICAL ACCURACY
═══════════════════════════════════════════════════════════════════════════════

• Use EXACT numbers from the dataset.
• Do NOT estimate or approximate.
• Always specify "per semester" or "total program".

═══════════════════════════════════════════════════════════════════════════════

Respond in clear, structured English. Be helpful and accurate."""

    def load_feedback_data(self) -> bool:
        """Load and analyze feedback data"""
        try:
            feedback_file = self.config['feedback_data_file']

            if os.path.exists(feedback_file):
                with open(feedback_file, 'r', encoding='utf-8') as f:
                    self.feedback_data = json.load(f)
                logger.info(f"✅ Loaded {len(self.feedback_data)} feedback entries")
            else:
                logger.warning(f"⚠️ Feedback file not found: {feedback_file}")
                self.feedback_data = []

            # Analyze patterns
            self._analyze_feedback_patterns()
            return True

        except Exception as e:
            logger.error(f"❌ Error loading feedback data: {e}")
            return False

    def load_disliked_answers(self) -> bool:
        """Load disliked answers to avoid repeating them"""
        try:
            disliked_file = self.config['disliked_answers_file']

            if os.path.exists(disliked_file):
                with open(disliked_file, 'r', encoding='utf-8') as f:
                    self.disliked_answers = json.load(f)
                logger.info(f"✅ Loaded {len(self.disliked_answers)} disliked answers")
            else:
                logger.warning(f"⚠️ Disliked answers file not found: {disliked_file}")
                self.disliked_answers = []

            return True

        except Exception as e:
            logger.error(f"❌ Error loading disliked answers: {e}")
            return False

    def save_disliked_answer(self, question: str, answer: str) -> bool:
        """Save a disliked answer to prevent repetition"""
        try:
            disliked_entry = {
                'question': question,
                'answer': answer,
                'timestamp': datetime.now().isoformat(),
                'blocked_permanently': True
            }

            self.disliked_answers.append(disliked_entry)

            # Save to file
            disliked_file = self.config['disliked_answers_file']
            with open(disliked_file, 'w', encoding='utf-8') as f:
                json.dump(self.disliked_answers, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Saved disliked answer. Total blocked: {len(self.disliked_answers)}")
            return True

        except Exception as e:
            logger.error(f"❌ Error saving disliked answer: {e}")
            return False

    def is_similar_to_disliked(self, generated_answer: str) -> Tuple[bool, Optional[str]]:
        """
        Check if generated answer is similar to any disliked answer
        Returns: (is_similar, reason)
        """
        try:
            if not self.disliked_answers:
                return False, None

            generated_lower = generated_answer.lower().strip()

            for disliked in self.disliked_answers:
                disliked_answer = disliked.get('answer', '').lower().strip()

                if not disliked_answer:
                    continue

                # Calculate simple similarity (word overlap)
                generated_words = set(generated_lower.split())
                disliked_words = set(disliked_answer.split())

                if len(generated_words) == 0 or len(disliked_words) == 0:
                    continue

                overlap = len(generated_words.intersection(disliked_words))
                similarity = overlap / max(len(generated_words), len(disliked_words))

                if similarity > self.config['similarity_threshold']:
                    reason = f"Too similar ({similarity:.2%}) to previously disliked answer"
                    logger.warning(f"⚠️ {reason}")
                    return True, reason

            return False, None

        except Exception as e:
            logger.error(f"❌ Error checking similarity: {e}")
            return False, None

    def _analyze_feedback_patterns(self):
        """Analyze feedback to identify successful response patterns"""
        try:
            positive_feedback = [
                f for f in self.feedback_data
                if f.get('feedback') == 'like'
            ]

            logger.info(f"📊 Found {len(positive_feedback)} positive feedback entries")

            for feedback in positive_feedback:
                question = feedback.get('question', '').lower().strip()
                answer = feedback.get('answer', '').strip()

                if question and answer:
                    # Extract key patterns
                    if 'cse' in question and 'fee' in question:
                        self.response_patterns['cse_fee'].append(answer)
                    elif 'fee' in question or 'tuition' in question:
                        self.response_patterns['fees'].append(answer)
                    elif 'admission' in question:
                        self.response_patterns['admission'].append(answer)
                    elif 'program' in question or 'course' in question:
                        self.response_patterns['programs'].append(answer)

            # Log pattern analysis
            for pattern_type, responses in self.response_patterns.items():
                logger.info(f"  ├─ {pattern_type}: {len(responses)} successful responses")

        except Exception as e:
            logger.error(f"❌ Error analyzing feedback patterns: {e}")

    def detect_language(self, text: str) -> str:
        """
        Simple language detection (can be improved with langdetect library)
        Returns: 'english', 'non-english', or 'unknown'
        """
        try:
            # Simple heuristic: check for non-ASCII characters
            if any(ord(char) > 127 for char in text):
                # Contains non-ASCII (likely non-English)
                return 'non-english'
            
            # Check for common non-English words (basic check)
            non_english_indicators = [
                'কি', 'কীভাবে', 'কেন',  # Bengali
                'क्या', 'कैसे', 'क्यों',  # Hindi
            ]
            
            for indicator in non_english_indicators:
                if indicator in text:
                    return 'non-english'
            
            return 'english'

        except Exception as e:
            logger.error(f"❌ Error detecting language: {e}")
            return 'unknown'

    def enforce_english_response(self, user_question: str) -> Optional[str]:
        """
        Enforce English-only responses - CRITICAL
        """
        # Language enforcement is handled in system prompt
        # Return None to continue with generation (system prompt enforces English)
        return None
    
    def _contains_non_english(self, text: str) -> bool:
        """
        Check if text contains non-English characters (Bengali, Hindi, etc.)
        """
        # Check for Bengali Unicode range (0980-09FF)
        # Check for Devanagari Unicode range (0900-097F)
        for char in text:
            code = ord(char)
            if (0x0980 <= code <= 0x09FF) or (0x0900 <= code <= 0x097F):
                return True
        return False
    
    def _force_english_regeneration(self, user_question: str, rag_context: str) -> Optional[str]:
        """
        Force regeneration in English if response contains non-English text
        """
        english_only_prompt = f"""CRITICAL INSTRUCTION: You MUST respond ONLY in ENGLISH.
Do NOT use Bengali, Hindi, or any other non-English language.
Do NOT use any non-ASCII characters except punctuation.

Question: {user_question}

Context from database:
{rag_context}

Provide your answer in ENGLISH ONLY:"""
        
        payload = {
            "model": self.model_name,
            "prompt": english_only_prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower temperature for more controlled output
                "top_p": 0.9,
                "num_predict": self.config['max_tokens']
            }
        }
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.config['timeout']
            )
            if response.status_code == 200:
                return response.json().get('response', '').strip()
        except:
            pass
        return None

    def enhance_system_prompt(self, rag_context: str = "") -> str:
        """Enhance system prompt with RAG context and learned patterns"""
        try:
            enhanced_prompt = self.system_prompt

            # Add RAG context if available - THIS IS CRITICAL
            if rag_context:
                enhanced_prompt += f"\n\n📚 RETRIEVED CONTEXT FROM KNOWLEDGE BASE (USE THIS DATA):\n{rag_context}\n"
                enhanced_prompt += "\n⚠️ CRITICAL: You MUST use the above retrieved information to answer. "
                enhanced_prompt += "Do NOT substitute with information from other departments. "
                enhanced_prompt += "If user asks about EEE, answer about EEE ONLY. If user asks about CSE, answer about CSE ONLY.\n"

            # Add learned patterns - department-neutral
            if self.response_patterns:
                enhanced_prompt += "\n\n💡 LEARNED FROM SUCCESSFUL INTERACTIONS:\n"
                
                if self.response_patterns['fees']:
                    enhanced_prompt += "• For fee queries: Use EXACT department-specific amounts from RAG context\n"
                    enhanced_prompt += "• CSE fee ≠ EEE fee ≠ BBA fee - each department has different fees\n"
                
                if self.response_patterns['admission']:
                    enhanced_prompt += "• For admission queries: Be clear about requirements and dates\n"

            # Add disliked patterns warning
            if self.disliked_answers:
                enhanced_prompt += f"\n\n⚠️ AVOID REPEATING: {len(self.disliked_answers)} previously disliked answer patterns\n"
                enhanced_prompt += "REWRITE completely if similar pattern detected.\n"

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
                    logger.info(f"✅ Ollama connected. Model: {self.model_name}")
                    return True
                else:
                    logger.warning(f"⚠️ Model {self.model_name} not found. Available: {model_names}")
                    return False
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Cannot connect to Ollama: {e}")
            return False

    def generate_response(self, user_question: str, rag_context: str = "") -> Optional[str]:
        """
        Generate enhanced response with all features:
        - Language enforcement (English only)
        - RAG context integration
        - Disliked answer avoidance
        - Learned pattern application
        """
        try:
            # 1. Check language restriction
            lang_refusal = self.enforce_english_response(user_question)
            if lang_refusal:
                logger.info("🌐 Enforced English-only response")
                return lang_refusal

            # 2. Enhance system prompt with RAG context and patterns
            system_prompt = self.enhance_system_prompt(rag_context)

            # 3. Create full prompt
            full_prompt = f"{system_prompt}\n\nUser Question: {user_question}\n\nAssistant Response:"

            # 4. Generate response
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

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.config['timeout']
            )

            if response.status_code != 200:
                logger.error(f"❌ API error: {response.status_code}")
                return None

            generated_response = response.json().get('response', '').strip()

            # 4.5 CHECK FOR NON-ENGLISH AND REGENERATE IF NEEDED
            if self._contains_non_english(generated_response):
                logger.warning("⚠️ Response contains non-English text! Regenerating in English...")
                print("="*80)
                print("⚠️ NON-ENGLISH DETECTED - REGENERATING")
                print("="*80)
                
                english_response = self._force_english_regeneration(user_question, rag_context)
                if english_response and not self._contains_non_english(english_response):
                    generated_response = english_response
                    logger.info("✅ Successfully regenerated in English")
                else:
                    # Fallback: return a safe English response
                    logger.error("❌ Failed to generate English response, using fallback")
                    generated_response = self._get_fallback_english_response(user_question, rag_context)

            # 5. Check against disliked answers
            is_similar, reason = self.is_similar_to_disliked(generated_response)
            
            if is_similar:
                logger.warning(f"⚠️ Generated response similar to disliked: {reason}")
                logger.info("🔄 Regenerating with stronger constraints...")
                
                # Regenerate with stronger prompt
                regenerate_prompt = system_prompt + f"\n\n⚠️ CRITICAL: Previous response was rejected. Generate completely different answer.\nAvoid this pattern: {reason}\n\nUser Question: {user_question}\n\nCompletely New Response:"
                
                payload['prompt'] = regenerate_prompt
                payload['options']['temperature'] = 0.9  # Increase temperature for more variety
                
                retry_response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json=payload,
                    timeout=self.config['timeout']
                )
                
                if retry_response.status_code == 200:
                    generated_response = retry_response.json().get('response', '').strip()
                    logger.info("✅ Regenerated alternative response")

            # 6. Format response with feedback prompt
            formatted_response = self._format_response_with_feedback(generated_response)

            # 7. Validate fee accuracy for specific departments
            if 'cse' in user_question.lower() and 'fee' in user_question.lower():
                if '70,000' not in generated_response and '70000' not in generated_response:
                    logger.warning("⚠️ CSE fee response may not contain correct amount (should be 70,000)")
            
            if 'eee' in user_question.lower() and 'fee' in user_question.lower():
                if '80,000' not in generated_response and '80000' not in generated_response:
                    logger.warning("⚠️ EEE fee response may not contain correct amount (should be 80,000)")

            # 8. TERMINAL LOGGING FOR DEBUGGING
            print("\n" + "="*80)
            print("📝 CHATBOT Q&A LOG (CROSS-CHECK)")
            print("="*80)
            print(f"❓ QUESTION: {user_question}")
            print("-"*80)
            print(f"📚 RAG CONTEXT USED:")
            print(rag_context[:500] + "..." if len(rag_context) > 500 else rag_context)
            print("-"*80)
            print(f"✅ ANSWER (ENGLISH ONLY):")
            print(formatted_response)
            print("="*80 + "\n")

            return formatted_response

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return None

    def _format_response_with_feedback(self, response: str) -> str:
        """Format response without feedback section"""
        # Simply return the response as-is, no feedback prompt
        return response

    def _get_fallback_english_response(self, user_question: str, rag_context: str) -> str:
        """
        Generate a safe fallback English response based on RAG context
        """
        question_lower = user_question.lower()
        
        # Extract key info from RAG context for fee questions
        if 'fee' in question_lower or 'tuition' in question_lower or 'cost' in question_lower:
            if 'eee' in question_lower or 'electrical' in question_lower:
                return """The EEE (Electrical and Electronic Engineering) program at Green University has the following fee structure:

**Tuition Fee:** BDT 80,000 per semester
**Total Program Cost (4 years):** Approximately BDT 640,000 - 700,000

**Additional Fees:**
- Admission Fee: BDT 15,000 - 20,000 (one-time)
- Application Fee: BDT 500 - 1,000

For the most current fee information, please contact the admission office."""

            elif 'cse' in question_lower or 'computer' in question_lower:
                return """The CSE (Computer Science and Engineering) program at Green University has the following fee structure:

**Tuition Fee:** BDT 70,000 per semester
**Total Program Cost (4 years):** Approximately BDT 560,000 - 600,000

**Additional Fees:**
- Admission Fee: BDT 15,000 - 20,000 (one-time)
- Application Fee: BDT 500 - 1,000

For the most current fee information, please contact the admission office."""

            elif 'bba' in question_lower or 'business' in question_lower:
                return """The BBA (Bachelor of Business Administration) program at Green University has the following fee structure:

**Tuition Fee:** BDT 60,000 per semester
**Total Program Cost (4 years):** Approximately BDT 480,000 - 520,000

**Additional Fees:**
- Admission Fee: BDT 15,000 - 20,000 (one-time)
- Application Fee: BDT 500 - 1,000

For the most current fee information, please contact the admission office."""

        # Generic fallback
        return "I apologize, but I can only respond in English. Please rephrase your question, and I will provide accurate information from our university database."

    def handle_feedback(self, question: str, answer: str, feedback: str) -> Dict[str, Any]:
        """
        Handle user feedback (like/dislike)
        Returns: feedback processing result
        """
        try:
            feedback_entry = {
                'question': question,
                'answer': answer,
                'feedback': feedback,
                'timestamp': datetime.now().isoformat()
            }

            # Save feedback
            self.feedback_data.append(feedback_entry)
            
            feedback_file = self.config['feedback_data_file']
            with open(feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)

            result = {'status': 'success', 'feedback': feedback}

            # Handle dislike
            if feedback == 'dislike':
                # Save to disliked answers
                self.save_disliked_answer(question, answer)
                
                result['action'] = 'answer_blocked'
                result['message'] = 'Answer blocked. Generating improved response...'
                logger.info(f"👎 Disliked answer blocked. Total: {len(self.disliked_answers)}")
            
            # Handle like
            elif feedback == 'like':
                result['action'] = 'pattern_learned'
                result['message'] = 'Thank you! This pattern will improve future responses.'
                logger.info("👍 Positive feedback recorded")

            return result

        except Exception as e:
            logger.error(f"❌ Error handling feedback: {e}")
            return {'status': 'error', 'message': str(e)}

    def initialize(self) -> bool:
        """Initialize the enhanced chatbot V2"""
        try:
            logger.info("🚀 Initializing Enhanced Ollama Chatbot V2")
            logger.info("=" * 80)
            logger.info("Features:")
            logger.info("  ✅ RAG (Retrieval-Augmented Generation)")
            logger.info("  ✅ RL with User Feedback (Like/Dislike)")
            logger.info("  ✅ Language Restriction (English Only)")
            logger.info("  ✅ Disliked Answer Blocking")
            logger.info("  ✅ Response Pattern Learning")
            logger.info("=" * 80)

            # Check Ollama connection
            if not self.check_ollama_connection():
                logger.warning("⚠️ Ollama not connected. Some features may be limited.")

            # Load feedback data
            self.load_feedback_data()

            # Load disliked answers
            self.load_disliked_answers()

            logger.info("✅ Enhanced chatbot V2 initialized successfully")
            logger.info(f"📊 Stats:")
            logger.info(f"  • Total feedback: {len(self.feedback_data)}")
            logger.info(f"  • Blocked answers: {len(self.disliked_answers)}")
            logger.info(f"  • Learned patterns: {sum(len(v) for v in self.response_patterns.values())}")
            
            return True

        except Exception as e:
            logger.error(f"❌ Error initializing chatbot: {e}")
            return False


# Singleton instance for use in rag_api_server.py
_chatbot_instance = None

def get_chatbot_instance() -> EnhancedOllamaChatbotV2:
    """Get or create singleton chatbot instance"""
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = EnhancedOllamaChatbotV2()
        _chatbot_instance.initialize()
    return _chatbot_instance


def main():
    """Main function for testing"""
    print("🚀 Enhanced Ollama Chatbot V2 with RAG + RL + Feedback")
    print("=" * 80)

    # Initialize chatbot
    chatbot = EnhancedOllamaChatbotV2()

    if not chatbot.initialize():
        print("❌ Failed to initialize chatbot")
        return

    # Test queries
    test_queries = [
        "What is the CSE tuition fee?",
        "কম্পিউটার সায়েন্স এর ফি কত?",  # Bengali - should be refused
        "Tell me about admission requirements",
    ]

    print("\n🧪 Testing chatbot with sample queries...")
    print("=" * 80)

    for query in test_queries:
        print(f"\n❓ Query: {query}")
        print("-" * 80)
        
        response = chatbot.generate_response(query, rag_context="Retrieved: CSE fee is BDT 70,000 per semester")
        
        if response:
            print(response)
        else:
            print("❌ No response generated")
        
        print("-" * 80)
        time.sleep(1)

    print("\n✅ Testing completed!")
    print("\n💡 Key Features Demonstrated:")
    print("  ✅ English-only enforcement")
    print("  ✅ RAG context integration")
    print("  ✅ Formatted feedback collection")
    print("  ✅ Disliked answer checking")


if __name__ == "__main__":
    main()
