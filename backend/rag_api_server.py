from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import os
from dotenv import load_dotenv
import json
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import datetime
from typing import Dict, List, Any, Optional
import threading
import pickle

# Import enhanced chatbots
# DISABLED: V1 chatbot - using only V2 now
# from enhanced_ollama_chatbot import EnhancedOllamaChatbot
from enhanced_ollama_chatbot_v2 import EnhancedOllamaChatbotV2, get_chatbot_instance

# Import evaluation middleware for research
from evaluation_middleware import log_chat_interaction, get_live_statistics, generate_report_api

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
    "http://[::]:3000",
    "http://localhost:5173",  # Vite default dev server
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # Vite alternative port
    "http://127.0.0.1:5174"
])

# Store system components in Flask app config for persistence
app.config['SYSTEM_COMPONENTS'] = {
    'llm': None,
    'search_system': None,
    'enhanced_chatbot': None,
    'initialized': False
}

# Global variables for backward compatibility (will be updated from app.config)
llm = None
search_system = None
enhanced_chatbot = None
enhanced_chatbot_v2 = None  # New V2 chatbot with RAG+RL+Feedback
_system_initialized = False
feedback_memory = {}
use_v2_chatbot = True  # Toggle to use V2 chatbot with enhanced features
learning_stats = {
    'total_feedback': 0,
    'likes': 0,
    'dislikes': 0,
    'blocked_answers': 0,
    'improved_responses': 0
}

def ensure_system_initialized():
    """Ensure system components are initialized"""
    global llm, search_system, enhanced_chatbot, enhanced_chatbot_v2, _system_initialized

    print(f"🔍 ensure_system_initialized called - _system_initialized: {_system_initialized}")
    print(f"🔍 Current global variables: llm={llm is not None}, search_system={search_system is not None}, enhanced_chatbot={enhanced_chatbot is not None}, v2={enhanced_chatbot_v2 is not None}")

    if not _system_initialized:
        print("🔄 Lazy initialization of system components...")
        _system_initialized = initialize_system()
        print(f"✅ Lazy initialization result: {_system_initialized}")
        print(f"📊 After initialization: llm={llm is not None}, search={search_system is not None}, v1={enhanced_chatbot is not None}, v2={enhanced_chatbot_v2 is not None}")

        # Update Flask app config with initialized components
        app.config['SYSTEM_COMPONENTS'] = {
            'llm': llm,
            'search_system': search_system,
            'enhanced_chatbot': enhanced_chatbot,
            'enhanced_chatbot_v2': enhanced_chatbot_v2,
            'initialized': _system_initialized
        }
        print("✅ Updated Flask app config with system components")

    # Sync from Flask app config to ensure consistency
    components = app.config.get('SYSTEM_COMPONENTS', {})
    if components.get('initialized', False):
        llm = components.get('llm')
        search_system = components.get('search_system')
        enhanced_chatbot = components.get('enhanced_chatbot')
        enhanced_chatbot_v2 = components.get('enhanced_chatbot_v2')
        _system_initialized = components.get('initialized')
        print("✅ Synced components from Flask app config")

    return _system_initialized

# Load configuration
try:
    import config
    OFFLINE_MODE = getattr(config, 'OFFLINE_MODE', False)
except ImportError:
    # Fallback if config.py doesn't exist
    OFFLINE_MODE = os.getenv('OFFLINE_MODE', 'True').lower() == 'true'

print(f"🔧 Server mode: {'OFFLINE' if OFFLINE_MODE else 'ONLINE'}")

class IntegratedSearchSystem:
    """Integrated system combining JSON analysis with LLaMA model"""

    def __init__(self, data_file_path: str = "enhanced_ndata.json", json_file_path: str = "green_university_30k_instruction_response.json", dataset_folder: str = "dataset"):
        """Initialize the integrated search system"""

        # NLP setup
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)  # Open Multilingual Wordnet
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english')) | {"university", "please", "can"}

        # File paths
        self.data_file_path = data_file_path
        self.json_file_path = json_file_path
        self.dataset_folder = dataset_folder
        self.feedback_file_path = "user_feedback_data.json"
        self.disliked_answers_file = "disliked_answers.json"
        self.blocked_keywords_file = "blocked_keywords.json"
        self.learning_model_file = "learning_model.pkl"

        # Load and process data
        self.load_data()
        self.load_dataset_files()  # Load additional dataset files
        self.load_feedback_data()
        self.preprocess_all_data()
        self.train_models()

        print(f"✅ Integrated Search System initialized with {len(self.data)} data points")

    def load_data(self):
        """Load JSON and json data with enhanced processing for learning"""
        self.data = []
        self.instruction_responses = []  # Separate store for instruction-response pairs
        
        # Load enhanced_ndata.json
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            if isinstance(json_data, list):
                for item in json_data:
                    if 'question' in item and 'answer' in item:
                        # Normalize to expected format
                        normalized_item = {
                            'question': item['question'],
                            'answer': item['answer'],
                            'keywords': item.get('keywords', []),
                            'categories': item.get('categories', []),
                            'source': 'enhanced_json',
                            'confidence_score': item.get('confidence_score', 1.0),
                            'question_variations': item.get('question_variations', [])
                        }
                        self.data.append(normalized_item)
        except Exception as e:
            print(f"Error loading JSON data: {e}")
        
        # Load green_university_30k_instruction_response.json with enhanced learning
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    line = line.strip()
                    if line:
                        item = json.loads(line)
                        if 'instruction' in item and 'output' in item:
                            # Store in instruction_responses for specialized learning
                            instruction_item = {
                                'instruction': item['instruction'],
                                'output': item['output'],
                                'source': 'instruction_dataset',
                                'line_number': line_num
                            }
                            self.instruction_responses.append(instruction_item)
                            
                            # Also convert to general format for unified search
                            normalized_item = {
                                'question': item['instruction'],
                                'answer': item['output'],
                                'keywords': self._extract_keywords_from_text(item['instruction']),
                                'categories': [self._auto_categorize_instruction(item['instruction'])],
                                'source': 'instruction_dataset',
                                'confidence_score': 0.8  # Slightly lower confidence for auto-generated
                            }
                            self.data.append(normalized_item)
        except Exception as e:
            print(f"Error loading json data: {e}")
        
        print(f"Loaded {len(self.data)} total data points from JSON and json files")
        print(f"Loaded {len(self.instruction_responses)} instruction-response pairs for specialized learning")

    def load_dataset_files(self):
        """Load all JSON dataset files from the dataset folder with priority handling"""
        if not os.path.exists(self.dataset_folder):
            print(f"⚠️ Dataset folder '{self.dataset_folder}' not found, skipping dataset files")
            return
        
        dataset_count = 0
        critical_count = 0
        try:
            # First pass: load critical/improved files (higher priority)
            priority_files = ['Fee_Summary_CRITICAL.json', 'CSE_improved.json', 'EEE_improved.json', 
                            'BBA_improved.json', 'General_University_Info.json']
            
            for filename in os.listdir(self.dataset_folder):
                if filename.endswith('.json'):
                    # Skip old files if improved versions exist
                    if filename == 'cse.json' and 'CSE_improved.json' in os.listdir(self.dataset_folder):
                        print(f"⏭️ Skipping old {filename}, using improved version")
                        continue
                    if filename == 'EEE2.json' and 'EEE_improved.json' in os.listdir(self.dataset_folder):
                        print(f"⏭️ Skipping old {filename}, using improved version")
                        continue
                    if filename == 'BBA.json' and 'BBA_improved.json' in os.listdir(self.dataset_folder):
                        print(f"⏭️ Skipping old {filename}, using improved version")
                        continue
                        
                    file_path = os.path.join(self.dataset_folder, filename)
                    is_priority = filename in priority_files
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            dataset_items = json.load(f)
                        
                        if isinstance(dataset_items, list):
                            for item in dataset_items:
                                if 'question' in item and 'answer' in item:
                                    # Determine priority boost
                                    priority = item.get('priority', 'normal')
                                    priority_boost = 0.0
                                    if priority == 'critical' or is_priority:
                                        priority_boost = 0.2
                                        critical_count += 1
                                    elif priority == 'high':
                                        priority_boost = 0.1
                                    
                                    # Normalize dataset format with priority
                                    normalized_item = {
                                        'question': item['question'],
                                        'answer': item['answer'],
                                        'keywords': item.get('keywords', []),
                                        'categories': item.get('categories', []),
                                        'source': f'dataset_{filename}',
                                        'confidence_score': min(item.get('confidence_score', 1.0) + priority_boost, 1.0),
                                        'question_variations': item.get('question_variations', []),
                                        'department': item.get('department', ''),
                                        'priority': priority
                                    }
                                    self.data.append(normalized_item)
                                    dataset_count += 1
                        
                        print(f"✅ Loaded {len(dataset_items)} items from dataset/{filename}" + 
                              (f" (PRIORITY)" if is_priority else ""))
                    except Exception as file_error:
                        print(f"⚠️ Error loading dataset/{filename}: {file_error}")
            
            print(f"📚 Total dataset files loaded: {dataset_count} items ({critical_count} critical/priority)")
        except Exception as e:
            print(f"⚠️ Error reading dataset folder: {e}")


    def load_feedback_data(self):
        """Load feedback and learning data"""
        # Load disliked answers
        try:
            with open(self.disliked_answers_file, 'r', encoding='utf-8') as f:
                self.disliked_answers = json.load(f)
        except:
            self.disliked_answers = []

        # Load general feedback
        try:
            with open(self.feedback_file_path, 'r', encoding='utf-8') as f:
                self.feedback_data = json.load(f)
        except:
            self.feedback_data = []

        # Load learning model if exists
        try:
            with open(self.learning_model_file, 'rb') as f:
                self.learning_model = pickle.load(f)
        except:
            self.learning_model = None

    def save_feedback_data(self):
        """Save all feedback data"""
        with open(self.disliked_answers_file, "w", encoding='utf-8') as f:
            json.dump(self.disliked_answers, f, indent=2, ensure_ascii=False)

        with open(self.feedback_file_path, "w", encoding='utf-8') as f:
            json.dump(self.feedback_data, f, indent=2, ensure_ascii=False)

        # Save learning model
        if hasattr(self, 'learning_model') and self.learning_model:
            with open(self.learning_model_file, 'wb') as f:
                pickle.dump(self.learning_model, f)

    def preprocess(self, text: str) -> str:
        """Text preprocessing"""
        if not text:
            return ""
        text = text.lower().strip()
        text = ''.join([c for c in text if c.isalnum() or c.isspace()])
        words = [self.lemmatizer.lemmatize(word) for word in text.split()
                if word not in self.stop_words]
        return ' '.join(words)

    def preprocess_all_data(self):
        """Preprocess all data"""
        self.questions = []
        self.answers = []
        self.keywords_list = []
        self.categories = []

        for item in self.data:
            # Skip if answer is blocked
            if any(disliked['answer'] == item['answer'] for disliked in self.disliked_answers):
                continue

            processed_question = self.preprocess(item["question"])
            processed_keywords = [self.preprocess(kw) for kw in item.get("keywords", [])]

            self.questions.append(processed_question)
            self.answers.append(item["answer"])
            self.keywords_list.append(processed_keywords)

            # Determine category
            if "categories" in item and item["categories"]:
                self.categories.append(item["categories"][0])
            else:
                self.categories.append(self._auto_categorize(item.get("keywords", [])))

    def _extract_keywords_from_text(self, text: str) -> List[str]:
        """Extract keywords from instruction text for better categorization"""
        if not text:
            return []
        
        # Common university-related keywords
        keywords = []
        text_lower = text.lower()
        
        # Academic keywords
        academic_terms = ['admission', 'fee', 'tuition', 'course', 'program', 'semester', 'gpa', 'grade', 'exam', 'credit']
        for term in academic_terms:
            if term in text_lower:
                keywords.append(term)
        
        # Department keywords
        dept_terms = ['cse', 'computer science', 'engineering', 'bba', 'business', 'english', 'law', 'textile']
        for term in dept_terms:
            if term in text_lower:
                keywords.append(term)
        
        # Facility keywords
        facility_terms = ['library', 'lab', 'hostel', 'cafeteria', 'wifi', 'sports', 'club']
        for term in facility_terms:
            if term in text_lower:
                keywords.append(term)
        
        return list(set(keywords))  # Remove duplicates

    def _auto_categorize_instruction(self, instruction: str) -> str:
        """Auto-categorize instructions for better learning"""
        instruction_lower = instruction.lower()
        
        if any(word in instruction_lower for word in ["fee", "tuition", "cost", "price", "payment"]):
            return "fees_financial"
        elif any(word in instruction_lower for word in ["admission", "requirement", "apply", "enrollment", "deadline"]):
            return "admission_requirements"
        elif any(word in instruction_lower for word in ["program", "course", "department", "cse", "bba", "engineering"]):
            return "academic_programs"
        elif any(word in instruction_lower for word in ["contact", "phone", "email", "address", "location"]):
            return "contact_information"
        elif any(word in instruction_lower for word in ["facility", "library", "lab", "hostel", "cafeteria", "wifi"]):
            return "campus_facilities"
        elif any(word in instruction_lower for word in ["scholarship", "merit", "financial aid"]):
            return "scholarships_aid"
        elif any(word in instruction_lower for word in ["club", "society", "extracurricular", "sports"]):
            return "student_activities"
        else:
            return "general_inquiry"

    def search_instruction_responses(self, user_input: str) -> Dict[str, Any]:
        """Optimized search through instruction-response pairs with multiple strategies"""
        if not hasattr(self, 'instruction_responses') or not self.instruction_responses:
            return {"answer": "", "confidence": 0, "method": "no_instruction_data"}
        
        processed_input = self.preprocess(user_input)
        input_words = set(processed_input.split())
        user_input_lower = user_input.lower()
        
        # Track top matches
        matches = []
        
        for item in self.instruction_responses:
            processed_instruction = self.preprocess(item['instruction'])
            
            if not processed_instruction or not processed_input:
                continue
            
            instruction_words = set(processed_instruction.split())
            
            # STRATEGY 1: Jaccard similarity (word overlap)
            intersection = len(input_words & instruction_words)
            union = len(input_words | instruction_words)
            jaccard_score = intersection / union if union > 0 else 0
            
            # STRATEGY 2: Word order similarity (considers sequence)
            input_list = processed_input.split()
            instruction_list = processed_instruction.split()
            order_matches = 0
            for i, word in enumerate(input_list):
                if word in instruction_list:
                    # Bonus if word appears in similar position
                    inst_pos = instruction_list.index(word)
                    position_diff = abs(i / len(input_list) - inst_pos / len(instruction_list))
                    order_matches += (1 - position_diff) * 0.1
            order_score = order_matches / len(input_list) if input_list else 0
            
            # STRATEGY 3: Key term matching (important words get more weight)
            key_terms = ['fee', 'admission', 'program', 'course', 'scholarship', 'requirement', 
                        'faculty', 'department', 'contact', 'facility', 'hostel', 'library']
            key_term_matches = sum(1 for term in key_terms if term in processed_input and term in processed_instruction)
            key_term_score = (key_term_matches / len([t for t in key_terms if t in processed_input])) if any(t in processed_input for t in key_terms) else 0
            
            # STRATEGY 4: Exact phrase matching
            phrases = self._extract_phrases(user_input_lower)
            instruction_lower = item['instruction'].lower()
            phrase_matches = sum(1 for phrase in phrases if phrase in instruction_lower and len(phrase) > 5)
            phrase_score = (phrase_matches / max(len(phrases), 1)) * 0.3
            
            # Combined weighted score
            combined_score = (
                jaccard_score * 0.4 +      # Jaccard weight: 40%
                order_score * 0.2 +        # Order weight: 20%
                key_term_score * 0.25 +    # Key terms weight: 25%
                phrase_score * 0.15        # Phrase weight: 15%
            )
            
            if combined_score > 0.15:  # Minimum threshold
                matches.append({
                    "answer": item['output'],
                    "confidence": combined_score,
                    "instruction": item['instruction'],
                    "source": item.get('source', 'instruction_dataset'),
                    "method": "optimized_instruction_match",
                    "score_breakdown": {
                        "jaccard": jaccard_score,
                        "order": order_score,
                        "key_terms": key_term_score,
                        "phrase": phrase_score
                    }
                })
        
        # Sort by confidence and return best match
        if matches:
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            best_match = matches[0]
            
            # Add source references from top matches
            source_refs = []
            for i, match in enumerate(matches[:3]):
                source_refs.append({
                    "instruction": match['instruction'],
                    "confidence": float(match['confidence']),
                    "rank": i + 1
                })
            
            best_match['source_references'] = source_refs
            print(f"📖 Instruction match found with confidence: {best_match['confidence']:.3f}")
            return best_match
        
        return {"answer": "", "confidence": 0, "method": "no_match"}

    def _auto_categorize(self, keywords: List[str]) -> str:
        """Auto-categorize based on keywords"""
        keywords_lower = [kw.lower() for kw in keywords]

        if any(word in keywords_lower for word in ["fee", "tuition", "cost", "price"]):
            return "fees"
        elif any(word in keywords_lower for word in ["admission", "requirement", "apply", "enrollment"]):
            return "admission"
        elif any(word in keywords_lower for word in ["program", "course", "department", "cse", "bba"]):
            return "programs"
        elif any(word in keywords_lower for word in ["contact", "phone", "email", "address"]):
            return "contact"
        else:
            return "general"

    def train_models(self):
        """Train ML models"""
        if not self.questions:
            return

        try:
            # TF-IDF Vectorization
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=5000, min_df=1, max_df=0.95)
            self.X = self.vectorizer.fit_transform(self.questions)
            print(f"✅ TF-IDF vectorizer trained with {self.X.shape[0]} samples and {self.X.shape[1]} features")

            # Category Classification - simplified for faster training
            if len(set(self.categories)) > 1:
                encoded_categories = LabelEncoder().fit_transform(self.categories)
                # Use smaller dataset for faster training
                sample_size = min(1000, len(self.questions))
                if sample_size < len(self.questions):
                    indices = np.random.choice(len(self.questions), sample_size, replace=False)
                    X_sample = self.X[indices]
                    y_sample = encoded_categories[indices]
                else:
                    X_sample = self.X
                    y_sample = encoded_categories
                
                X_train, X_test, y_train, y_test = train_test_split(
                    X_sample, y_sample, test_size=0.2, random_state=42
                )
                # Use fewer estimators for faster training
                self.category_classifier = RandomForestClassifier(n_estimators=20, random_state=42, n_jobs=1)
                self.category_classifier.fit(X_train, y_train)
                print(f"✅ Category classifier trained with {len(X_train)} samples")
        except Exception as e:
            print(f"⚠️ Model training error: {e}")
            # Continue without ML models
            self.vectorizer = None
            self.category_classifier = None

    def search_json_data(self, user_input: str) -> Dict[str, Any]:
        """Optimized search with multiple matching strategies and source references"""
        if not self.questions:
            print("❌ No questions loaded in dataset!")
            return {"answer": "", "confidence": 0, "method": "no_data"}

        # Check if vectorizer is available
        if not hasattr(self, 'vectorizer') or self.vectorizer is None:
            return {"answer": "", "confidence": 0, "method": "vectorizer_not_trained"}

        user_input_lower = user_input.lower().strip()
        user_input_normalized = ' '.join(user_input_lower.split())  # Normalize whitespace
        
        # CRITICAL: Detect which department user is asking about
        detected_department = self._detect_department(user_input_lower)
        print(f"🎯 Detected department: {detected_department}")
        print(f"🔍 Searching through {len(self.data)} dataset items...")
        
        # STRATEGY 0: EXACT/NEAR-EXACT QUESTION MATCH (HIGHEST PRIORITY)
        best_match = None
        best_match_score = 0
        best_match_type = None
        
        for idx, item in enumerate(self.data):
            dataset_question = item.get('question', '').lower().strip()
            dataset_question_normalized = ' '.join(dataset_question.split())
            
            # Check exact match (normalized)
            if user_input_normalized == dataset_question_normalized:
                print(f"✅ EXACT MATCH FOUND: {dataset_question[:80]}")
                return {
                    "answer": item['answer'],
                    "confidence": 1.0,
                    "method": "exact_question_match",
                    "analyzed_items": len(self.questions),
                    "is_exact_match": True
                }
            
            # Check question variations for exact match
            for variation in item.get('question_variations', []):
                variation_normalized = ' '.join(variation.lower().strip().split())
                if user_input_normalized == variation_normalized:
                    print(f"✅ VARIATION EXACT MATCH: {variation}")
                    return {
                        "answer": item['answer'],
                        "confidence": 0.98,
                        "method": "variation_exact_match",
                        "analyzed_items": len(self.questions),
                        "is_exact_match": True
                    }
            
            # Calculate word overlap similarity
            dataset_words = set(dataset_question_normalized.split())
            user_words = set(user_input_normalized.split())
            
            if len(user_words) >= 2 and len(dataset_words) >= 2:
                # Calculate Jaccard similarity
                intersection = len(dataset_words & user_words)
                union = len(dataset_words | user_words)
                jaccard_sim = intersection / union if union > 0 else 0
                
                # Also check if all user words appear in dataset question
                user_word_coverage = len(dataset_words & user_words) / len(user_words) if len(user_words) > 0 else 0
                
                # Combined score
                combined_sim = (jaccard_sim * 0.5) + (user_word_coverage * 0.5)
                
                if combined_sim > best_match_score:
                    best_match_score = combined_sim
                    best_match = item
                    best_match_type = "word_similarity"
                    
            # Also check variations for similarity
            for variation in item.get('question_variations', []):
                variation_words = set(variation.lower().split())
                if len(variation_words) >= 2:
                    intersection = len(variation_words & user_words)
                    union = len(variation_words | user_words)
                    var_sim = intersection / union if union > 0 else 0
                    
                    if var_sim > best_match_score:
                        best_match_score = var_sim
                        best_match = item
                        best_match_type = "variation_similarity"
        
        # If we found a good word-level match
        if best_match and best_match_score >= 0.5:
            print(f"✅ HIGH SIMILARITY MATCH ({best_match_score:.0%} via {best_match_type})")
            print(f"   Question: {best_match.get('question', '')[:80]}")
            return {
                "answer": best_match['answer'],
                "confidence": min(0.85 + (best_match_score * 0.15), 0.98),
                "method": f"high_{best_match_type}",
                "analyzed_items": len(self.questions),
                "is_exact_match": True
            }
        
        # STRATEGY 1: TF-IDF Cosine Similarity (semantic matching)
        processed_input = self.preprocess(user_input)
        try:
            user_vec = self.vectorizer.transform([processed_input])
            similarities = cosine_similarity(user_vec, self.X).flatten()
        except Exception as e:
            print(f"❌ Vectorizer transform error: {e}")
            return {"answer": "", "confidence": 0, "method": "processing_error"}

        # STRATEGY 2: Keyword exact matching boost
        keyword_scores = np.zeros(len(self.questions))
        user_keywords = set(processed_input.split())
        
        for idx, keywords in enumerate(self.keywords_list):
            if keywords:
                keyword_set = set(' '.join(keywords).split())
                keyword_match = len(user_keywords & keyword_set) / max(len(user_keywords), 1)
                keyword_scores[idx] = keyword_match * 0.3  # Boost factor
        
        # STRATEGY 3: Question variation matching
        variation_scores = np.zeros(len(self.questions))
        for idx, item in enumerate(self.data):
            if 'question_variations' in item:
                for variation in item['question_variations']:
                    processed_variation = self.preprocess(variation)
                    variation_words = set(processed_variation.split())
                    variation_match = len(user_keywords & variation_words) / max(len(user_keywords), 1)
                    if variation_match > variation_scores[idx]:
                        variation_scores[idx] = variation_match * 0.25
        
        # STRATEGY 4: Exact phrase matching
        phrase_scores = np.zeros(len(self.questions))
        for idx, question in enumerate(self.questions):
            original_question = self.data[idx]['question'].lower()
            # Check for common phrases
            common_phrases = self._extract_phrases(user_input_lower)
            for phrase in common_phrases:
                if phrase in original_question and len(phrase) > 3:
                    phrase_scores[idx] += 0.15
        
        # STRATEGY 5: DEPARTMENT-SPECIFIC BOOST (CRITICAL for correct answers)
        department_scores = np.zeros(len(self.questions))
        if detected_department:
            for idx, item in enumerate(self.data):
                item_dept = item.get('department', '').lower()
                item_question = item.get('question', '').lower()
                item_answer = item.get('answer', '').lower()
                
                # Strong boost if department matches
                if detected_department in item_dept or detected_department in item_question:
                    department_scores[idx] = 0.4  # Strong boost for matching department
                # Penalty if different department mentioned
                elif self._mentions_different_department(item_question, item_answer, detected_department):
                    department_scores[idx] = -0.5  # Strong penalty for wrong department
        
        # Combine all strategies with weighted scoring
        combined_scores = (
            similarities * 0.4 +          # TF-IDF weight: 40%
            keyword_scores * 0.2 +        # Keyword weight: 20%
            variation_scores * 0.1 +      # Variation weight: 10%
            phrase_scores * 0.1 +         # Phrase weight: 10%
            department_scores * 0.2       # Department weight: 20% (CRITICAL)
        )
        
        # Get top 3 matches for better context
        top_indices = np.argsort(combined_scores)[-3:][::-1]
        top_scores = combined_scores[top_indices]
        
        print(f"🔍 Top 3 matches: {top_scores}")
        print(f"🔍 Top match question: {self.data[top_indices[0]]['question'][:100]}")
        
        if top_scores[0] >= 0.25:  # Confidence threshold
            best_idx = top_indices[0]
            best_score = top_scores[0]
            answer = self.answers[best_idx]
            
            # Collect source references
            source_refs = []
            for idx in top_indices:
                if combined_scores[idx] >= 0.2:  # Include relevant matches
                    ref_data = self.data[idx]
                    source_refs.append({
                        'question': ref_data['question'],
                        'source': ref_data.get('source', 'unknown'),
                        'confidence': float(combined_scores[idx]),
                        'categories': ref_data.get('categories', [])
                    })
            
            # Enhance answer with multiple sources if available
            if len(source_refs) > 1 and top_scores[1] >= 0.3:
                # Combine insights from top matches
                additional_context = []
                for i in range(1, min(len(top_indices), 3)):
                    if top_scores[i] >= 0.3:
                        additional_context.append(self.answers[top_indices[i]])
                
                if additional_context:
                    print(f"📚 Combining {len(additional_context) + 1} sources for comprehensive answer")
            
            # Validate fee information
            if self._is_fee_question(user_input):
                if not self._validate_fee_answer(answer, user_input):
                    print(f"⚠️ Detected potentially incorrect fee information, lowering confidence")
                    best_score = 0.3
            
            return {
                "answer": answer,
                "confidence": float(best_score),
                "method": "optimized_multi_strategy_search",
                "analyzed_items": len(self.questions),
                "source_references": source_refs[:3],  # Top 3 sources
                "matching_strategies_used": ["tfidf", "keyword", "variation", "phrase", "department"],
                "detected_department": detected_department,
                "combined_score_breakdown": {
                    "tfidf": float(similarities[best_idx]),
                    "keyword": float(keyword_scores[best_idx]),
                    "variation": float(variation_scores[best_idx]),
                    "phrase": float(phrase_scores[best_idx]),
                    "department": float(department_scores[best_idx])
                }
            }


        return {"answer": "", "confidence": 0, "method": "no_match"}
    
    def _extract_phrases(self, text: str) -> List[str]:
        """Extract meaningful phrases from text"""
        words = text.split()
        phrases = []
        
        # Extract 2-word phrases
        for i in range(len(words) - 1):
            phrases.append(f"{words[i]} {words[i+1]}")
        
        # Extract 3-word phrases
        for i in range(len(words) - 2):
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
        
        return phrases
    
    def _detect_department(self, text: str) -> str:
        """Detect which department user is asking about - CRITICAL for correct answers"""
        text_lower = text.lower()
        
        # Department detection patterns (order matters - more specific first)
        department_patterns = {
            'eee': ['eee', 'electrical', 'electronic', 'electrical and electronic', 'electrical engineering'],
            'cse': ['cse', 'computer science', 'computer engineering', 'software', 'programming'],
            'bba': ['bba', 'business', 'business administration', 'management'],
            'textile': ['textile', 'textile engineering', 'garment'],
            'law': ['law', 'llb', 'legal', 'advocate'],
            'english': ['english', 'ba english', 'literature', 'linguistics'],
            'journalism': ['journalism', 'media', 'communication'],
            'sociology': ['sociology', 'social science'],
        }
        
        for dept, patterns in department_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return dept
        
        return ""  # No specific department detected
    
    def _mentions_different_department(self, question: str, answer: str, target_dept: str) -> bool:
        """Check if answer mentions a different department than what user asked"""
        if not target_dept:
            return False
            
        text = (question + " " + answer).lower()
        
        # Map of departments and their exclusive keywords
        dept_keywords = {
            'eee': ['eee', 'electrical', 'electronic'],
            'cse': ['cse', 'computer science', 'computer engineering'],
            'bba': ['bba', 'business administration'],
            'textile': ['textile engineering'],
            'law': ['llb', 'law'],
            'english': ['ba english', 'english department'],
        }
        
        # Check if answer mentions a DIFFERENT department
        for dept, keywords in dept_keywords.items():
            if dept != target_dept:
                for keyword in keywords:
                    if keyword in text:
                        # Answer mentions different department
                        return True
        
        return False
    
    def _is_fee_question(self, question: str) -> bool:
        """Check if question is about fees"""
        fee_keywords = ['fee', 'tuition', 'cost', 'price', 'payment', 'semester fee', 'how much', 'total cost', 'program cost']
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in fee_keywords)
    
    def _validate_fee_answer(self, answer: str, question: str) -> bool:
        """Validate fee information in answer - ensures correct department-specific fees"""
        answer_lower = answer.lower()
        question_lower = question.lower()
        
        # Known correct fees per semester for validation (BDT)
        correct_fees = {
            # CSE
            'cse': 70000,
            'computer science': 70000,
            'computer engineering': 70000,
            # EEE
            'eee': 80000,
            'electrical': 80000,
            'electronic': 80000,
            'electrical and electronic': 80000,
            # BBA
            'bba': 60000,
            'business administration': 60000,
            'business': 60000,
            # Textile
            'textile': 65000,
            'textile engineering': 65000,
            # Law
            'law': 55000,
            'llb': 55000,
            # English
            'english': 50000,
            'ba english': 50000,
        }
        
        # Check if question mentions any program
        import re
        for program, correct_fee in correct_fees.items():
            if program in question_lower:
                # Extract fee amount from answer (looking for BDT amounts)
                fee_matches = re.findall(r'bdt\s*(\d{1,3}(?:,\d{3})*)', answer_lower)
                if fee_matches:
                    # Convert found fee to integer
                    found_fee = int(fee_matches[0].replace(',', ''))
                    # Allow some tolerance (within 10% or for total program costs)
                    if found_fee != correct_fee and found_fee != correct_fee * 8:  # semester or total
                        # Check if it's a per-semester fee (should match exact) or could be total
                        if 'semester' in answer_lower and found_fee != correct_fee:
                            print(f"⚠️ Found incorrect semester fee {found_fee} for {program}, expected {correct_fee}")
                            return False
        
        return True

    def generate_llama_response(self, user_input: str, context: str = "") -> str:
        """Generate response using enhanced chatbot V2 or fallback to V1/LLaMA"""
        print(f"🤖 Generating response for: '{user_input}'")
        print(f"🤖 V2 Chatbot available: {enhanced_chatbot_v2 is not None}")
        print(f"🤖 V1 Chatbot available: {enhanced_chatbot is not None}")
        print(f"🤖 LLaMA model available: {llm is not None}")

        # Priority 1: Use enhanced chatbot V2 (with RAG+RL+Feedback)
        if use_v2_chatbot and enhanced_chatbot_v2:
            try:
                print("🎯 Using enhanced chatbot V2 with RAG+RL+Feedback+Language restriction")
                response = enhanced_chatbot_v2.generate_response(user_input, rag_context=context)
                if response:
                    print(f"✅ Enhanced chatbot V2 response generated, length: {len(response)}")
                    print(f"📄 Response preview: {response[:200]}...")
                    return response
                else:
                    print("⚠️ Enhanced chatbot V2 returned empty response, falling back")
            except Exception as e:
                print(f"⚠️ Enhanced chatbot V2 error: {e}, falling back")

        # Priority 2: Use enhanced chatbot V1 if available
        if enhanced_chatbot:
            try:
                print("🎯 Using enhanced chatbot V1 with feedback learning")
                response = enhanced_chatbot.generate_response(user_input)
                if response:
                    print(f"✅ Enhanced chatbot V1 response generated, length: {len(response)}")
                    print(f"📄 Response preview: {response[:200]}...")
                    return response
                else:
                    print("⚠️ Enhanced chatbot V1 returned empty response, falling back to LLaMA")
            except Exception as e:
                print(f"⚠️ Enhanced chatbot V1 error: {e}, falling back to LLaMA")

        # Priority 3: Fallback to original LLaMA model
        if not llm:
            print("❌ No LLaMA model available")
            return "AI model is currently unavailable."

        try:
            # Enhanced prompt for better responses
            if "python" in user_input.lower() or "code" in user_input.lower():
                prompt = f"""You are a helpful programming assistant for Green University students.

Question: {user_input}

Please provide a clear, well-commented Python code solution. Include explanations and best practices.

Answer:"""
                print("🐍 Using Python code prompt")
            elif "calculate" in user_input.lower() or "math" in user_input.lower():
                prompt = f"""You are a helpful assistant specializing in calculations and mathematics.

Question: {user_input}

Please provide a step-by-step solution with clear explanations.

Answer:"""
                print("🔢 Using math calculation prompt")
            else:
                prompt = f"""You are a helpful assistant for Green University of Bangladesh.

Context from knowledge base:
{context}

User Question: {user_input}

Please provide a helpful, accurate answer in English only. If this is about programming or technical topics, include relevant code examples when appropriate.

Answer:"""
                print("🎓 Using general university prompt")

            print(f"📝 Prompt length: {len(prompt)} characters")
            print(f"📝 Prompt preview: {prompt[:200]}...")

            response = llm.invoke(prompt)
            print(f"✅ LLaMA response generated, length: {len(response)}")
            print(f"📄 Response preview: {response[:200]}...")

            return response

        except Exception as e:
            print(f"❌ LLaMA generation error: {e}")
            import traceback
            traceback.print_exc()
            return "I apologize, but I'm having trouble generating a response right now."

    def integrated_search(self, user_input: str) -> Dict[str, Any]:
        """Optimized integrated search with comprehensive source references"""
        start_time = time.time()
        print(f"\n{'='*80}")
        print(f"🔍 SEARCH REQUEST: '{user_input}'")
        print(f"{'='*80}")

        try:
            # PARALLEL SEARCH: Execute both searches
            instruction_result = self.search_instruction_responses(user_input)
            print(f"📚 Instruction search: confidence={instruction_result.get('confidence', 0):.3f}, method={instruction_result.get('method', 'MISSING')}")

            json_result = self.search_json_data(user_input)
            print(f"📊 JSON search: confidence={json_result.get('confidence', 0):.3f}, method={json_result.get('method', 'MISSING')}")
            
            # CRITICAL: If we have an exact match from JSON, use it IMMEDIATELY
            if json_result.get('is_exact_match'):
                print(f"\n{'='*80}")
                print(f"✅ USING EXACT DATASET MATCH")
                print(f"{'='*80}")
                print(f"❓ Question: {user_input}")
                print(f"📊 Confidence: {json_result.get('confidence', 0):.0%}")
                print(f"✅ Answer from Dataset:")
                print(json_result.get('answer', ''))
                print(f"{'='*80}\n")
                
                return {
                    "answer": json_result.get('answer', ''),
                    "confidence": json_result.get('confidence', 0),
                    "method": json_result.get('method', 'exact_match'),
                    "processing_time": round(time.time() - start_time, 2),
                    "source": "exact_dataset_match",
                    "analyzed_items": json_result.get('analyzed_items', 0),
                    "is_exact_match": True
                }

            # Collect all source references
            all_sources = []
            if instruction_result.get('source_references'):
                all_sources.extend([{**ref, 'search_type': 'instruction'} for ref in instruction_result['source_references']])
            if json_result.get('source_references'):
                all_sources.extend([{**ref, 'search_type': 'json'} for ref in json_result['source_references']])
            
            # Choose best result based on confidence
            if instruction_result.get("confidence", 0) > json_result.get("confidence", 0):
                best_result = instruction_result
                alternate_result = json_result
                primary_source = "instruction_dataset"
            else:
                best_result = json_result
                alternate_result = instruction_result
                primary_source = "json_dataset"
            
            print(f"🏆 Primary source: {primary_source}, confidence={best_result.get('confidence', 0):.3f}")
            
            # Check if this is a fee question and validate the answer
            is_fee_question = self._is_fee_question(user_input)
            if is_fee_question and best_result.get("answer"):
                if not self._validate_fee_answer(best_result.get("answer", ""), user_input):
                    print("⚠️ Fee validation failed, forcing LLaMA enhancement")
                    best_result["confidence"] = 0.3
            
            if best_result.get("confidence", 0) >= 0.7:  # High confidence from either search
                print("✅ Using EXACT dataset answer (high confidence)")
                
                # Use EXACT answer from dataset - NO LLM modification
                exact_answer = best_result.get("answer", "")
                confidence = best_result.get("confidence", 0)
                
                # TERMINAL LOGGING FOR CROSS-CHECK
                print("\n" + "="*80)
                print("📝 DATASET MATCH FOUND - USING EXACT ANSWER")
                print("="*80)
                print(f"❓ USER QUESTION: {user_input}")
                print("-"*80)
                print(f"✅ EXACT ANSWER FROM DATASET:")
                print(exact_answer)
                print("-"*80)
                print(f"📊 CONFIDENCE: {confidence:.2%}")
                print(f"📚 SOURCE: {primary_source}")
                print("="*80 + "\n")
                
                # Add confidence notification to response
                confidence_notice = ""
                if confidence < 0.85:
                    confidence_notice = f"\n\n⚠️ *Confidence: {confidence:.0%} - Please verify with admission office if needed.*"
                
                result = {
                    "answer": exact_answer + confidence_notice,
                    "confidence": confidence,
                    "method": "exact_dataset_match",
                    "processing_time": round(time.time() - start_time, 2),
                    "source": f"exact_match_{primary_source}",
                    "analyzed_items": best_result.get("analyzed_items", 0),
                    "source_references": all_sources[:5],
                    "matching_details": best_result.get("combined_score_breakdown") or best_result.get("score_breakdown"),
                    "is_exact_match": True
                }
                return result
            elif best_result.get("confidence", 0) >= 0.4:  # Medium-high confidence - USE DATASET ANSWER
                confidence = best_result.get("confidence", 0)
                dataset_answer = best_result.get("answer", "")
                
                # TERMINAL LOGGING FOR CROSS-CHECK
                print("\n" + "="*80)
                print("📝 MEDIUM CONFIDENCE - USING DATASET ANSWER")
                print("="*80)
                print(f"❓ USER QUESTION: {user_input}")
                print("-"*80)
                print(f"✅ DATASET ANSWER:")
                print(dataset_answer)
                print("-"*80)
                print(f"📊 CONFIDENCE: {confidence:.2%}")
                print("="*80 + "\n")
                
                # Add confidence notification
                confidence_notice = f"\n\n⚠️ *Confidence: {confidence:.0%} - Please verify with admission office for latest information.*"
                
                return {
                    "answer": dataset_answer + confidence_notice,
                    "confidence": confidence,
                    "method": "dataset_match_medium",
                    "analyzed_items": best_result.get("analyzed_items", 0),
                    "processing_time": round(time.time() - start_time, 2),
                    "source": f"dataset_{primary_source}",
                    "source_references": all_sources[:5],
                    "is_exact_match": True
                }
            elif best_result.get("confidence", 0) >= 0.25:  # Low-medium confidence - enhance with LLM
                if not OFFLINE_MODE and llm:
                    print("🔄 Low confidence, using LLM with dataset context")
                    
                    # Use dataset answer as strong context
                    context = f"IMPORTANT - Use this EXACT information from our database:\n{best_result.get('answer', '')}"
                    enhanced_answer = self.generate_llama_response(user_input, context)
                    
                    # Add confidence warning
                    enhanced_answer += f"\n\n⚠️ *Confidence: {best_result.get('confidence', 0):.0%} - This information may need verification.*"

                    return {
                        "answer": enhanced_answer,
                        "confidence": best_result.get("confidence", 0),
                        "method": "llm_enhanced_low_confidence",
                        "analyzed_items": len(self.questions) + len(getattr(self, 'instruction_responses', [])),
                        "processing_time": round(time.time() - start_time, 2),
                        "source": "llm_with_dataset_context",
                        "source_references": all_sources[:5]
                    }
                else:
                    print("📄 Using dataset answer (offline mode)")
                    return {
                        **best_result,
                        "answer": best_result.get("answer", "") + f"\n\n⚠️ *Confidence: {best_result.get('confidence', 0):.0%}*",
                        "processing_time": round(time.time() - start_time, 2),
                        "source": "medium_confidence_offline"
                    }
            else:
                if not OFFLINE_MODE and llm:  # Only use LLaMA if online mode and available
                    print("🤖 Using LLaMA primary response (low confidence from all sources)")
                    # Low confidence from all sources, use LLaMA primarily
                    llama_answer = self.generate_llama_response(user_input)

                    return {
                        "answer": llama_answer,
                        "confidence": 0.8,  # LLaMA responses get high confidence
                        "method": "llama_primary_multi_search",
                        "analyzed_items": len(self.questions) + len(getattr(self, 'instruction_responses', [])),
                        "processing_time": round(time.time() - start_time, 2),
                        "source": "llama_fallback_enhanced"
                    }
                else:
                    print("📝 Using enhanced fallback response (offline mode, low confidence)")
                    # Enhanced offline fallback response
                    return {
                        "answer": "I found some information but I'm not fully confident about the answer. Please rephrase your question or ask about specific topics like admissions, fees, programs, or facilities at Green University.",
                        "confidence": best_result.get("confidence", 0),
                        "method": "enhanced_offline_fallback",
                        "analyzed_items": len(self.questions) + len(getattr(self, 'instruction_responses', [])),
                        "processing_time": round(time.time() - start_time, 2),
                        "source": "fallback_response"
                    }
        except Exception as search_error:
            print(f"❌ Integrated search error: {search_error}")
            import traceback
            traceback.print_exc()
            return {
                "answer": "An error occurred during search. Please try again.",
                "confidence": 0,
                "method": "search_error",
                "analyzed_items": 0,
                "processing_time": round(time.time() - start_time, 2),
                "source": "error_fallback"
            }

    def record_feedback(self, user_question: str, bot_answer: str, feedback_type: str) -> Dict[str, Any]:
        """Record feedback with learning"""
        timestamp = datetime.datetime.now().isoformat()

        # Record feedback
        feedback_entry = {
            'timestamp': timestamp,
            'question': user_question,
            'answer': bot_answer,
            'feedback': feedback_type
        }
        self.feedback_data.append(feedback_entry)

        # Update learning stats
        global learning_stats
        learning_stats['total_feedback'] += 1
        if feedback_type == 'like':
            learning_stats['likes'] += 1
        elif feedback_type == 'dislike':
            learning_stats['dislikes'] += 1
            learning_stats['blocked_answers'] += 1

            # Block the disliked answer
            dislike_entry = {
                'answer': bot_answer,
                'question': user_question,
                'timestamp': timestamp,
                'blocked_permanently': True
            }
            self.disliked_answers.append(dislike_entry)

            # Retrain models without this answer
            self.preprocess_all_data()
            self.train_models()

        # Save feedback data
        self.save_feedback_data()

        return {
            "status": "success",
            "message": f"Feedback recorded: {feedback_type}",
            "learning_stats": learning_stats
        }

def initialize_system():
    """Initialize the integrated system with optional LLaMA and search"""
    global llm, search_system, enhanced_chatbot, enhanced_chatbot_v2, use_v2_chatbot

    if not OFFLINE_MODE:
        # Initialize LLaMA model (online mode)
        try:
            llm = Ollama(model="llama3.2:1b")
            test_response = llm.invoke("Hello")
            print("✅ LLaMA 3.2 model initialized successfully")
            print(f"Test response: {test_response}")
        except Exception as e:
            print(f"❌ Error initializing LLaMA model: {e}")
            print("Make sure Ollama is running and the model is pulled")
            return False
    else:
        print("🔌 OFFLINE MODE: Skipping LLaMA model initialization")
        llm = None

    # Initialize enhanced chatbot V2 (with RAG+RL+Feedback+Language restriction)
    if use_v2_chatbot:
        try:
            enhanced_chatbot_v2 = EnhancedOllamaChatbotV2()
            if enhanced_chatbot_v2.initialize():
                print("✅ Enhanced chatbot V2 initialized successfully")
                print("   🎯 Features: RAG + RL + Feedback + English-only + Disliked blocking")
            else:
                print("⚠️ Enhanced chatbot V2 initialization failed, falling back to V1")
                enhanced_chatbot_v2 = None
                use_v2_chatbot = False
        except Exception as e:
            print(f"⚠️ Error initializing enhanced chatbot V2: {e}")
            enhanced_chatbot_v2 = None
            use_v2_chatbot = False

    # Initialize enhanced chatbot V1 (fallback) - DISABLED
    # if not use_v2_chatbot or enhanced_chatbot_v2 is None:
    #     try:
    #         enhanced_chatbot = EnhancedOllamaChatbot()
    #         if enhanced_chatbot.initialize():
    #             print("✅ Enhanced chatbot V1 initialized successfully")
    #         else:
    #             print("⚠️ Enhanced chatbot V1 initialization failed, using basic mode")
    #             enhanced_chatbot = None
    #     except Exception as e:
    #         print(f"⚠️ Error initializing enhanced chatbot V1: {e}")
    #         enhanced_chatbot = None
    
    # V1 chatbot is disabled - using V2 only
    enhanced_chatbot = None
    print("ℹ️ Enhanced chatbot V1 is disabled - using V2 only")

    # Initialize integrated search system (always available)
    try:
        search_system = IntegratedSearchSystem()
        print(f"✅ Search system created: {search_system is not None}")
        print("✅ Integrated search system initialized")
    except Exception as e:
        print(f"❌ Error initializing search system: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True

@app.before_request
def initialize_on_first_request():
    """Initialize system on first request if not already initialized"""
    ensure_system_initialized()

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests with integrated JSON processing (offline/online)"""
    start_time = time.time()  # Track response time for research
    try:
        # Ensure system is initialized - try multiple approaches
        global llm, search_system, enhanced_chatbot
        
        # First, try to get from Flask app config
        components = app.config.get('SYSTEM_COMPONENTS', {})
        if components.get('initialized', False):
            llm = components.get('llm')
            search_system = components.get('search_system') 
            enhanced_chatbot = components.get('enhanced_chatbot')
            print("✅ Loaded components from Flask app config")
        else:
            # Fallback: initialize directly if not available
            print("🔄 Components not available in config, initializing directly...")
            if not initialize_system():
                return jsonify({
                    'error': 'System initialization failed',
                    'answer': 'The AI system failed to initialize. Please try again later.',
                    'method': 'initialization_error',
                    'confidence': 0,
                    'analyzed_items': 0
                }), 500

        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Missing message field',
                'answer': 'Please provide a message to process.',
                'method': 'error',
                'confidence': 0,
                'analyzed_items': 0
            }), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'answer': 'Please enter a valid message.',
                'method': 'error',
                'confidence': 0,
                'analyzed_items': 0
            }), 400

        print(f"📝 Processing message: '{user_message}'")
        print(f"🔍 Search system available: {search_system is not None}")
        print(f"🤖 LLaMA model available: {llm is not None}")
        print(f"🎯 Enhanced chatbot available: {enhanced_chatbot is not None}")

        # Use integrated search system
        if search_system:
            try:
                result = search_system.integrated_search(user_message)
                print(f"✅ Search result: method={result.get('method', 'MISSING')}, confidence={result.get('confidence', 0)}")

                # Calculate response time and log for research
                response_time = time.time() - start_time
                
                # Log interaction for research analysis
                log_chat_interaction(
                    question=user_message,
                    answer=result.get('answer', ''),
                    response_time=response_time,
                    source=result.get('method', 'unknown'),
                    confidence=result.get('confidence', 0)
                )

                return jsonify({
                    'answer': result.get('answer', 'No answer generated'),
                    'method': result.get('method', 'unknown_method'),
                    'confidence': result.get('confidence', 0),
                    'analyzed_items': result.get('analyzed_items', 0),
                    'processing_time': result.get('processing_time', 0),
                    'model': 'offline_json' if OFFLINE_MODE else 'integrated_llama3.2_json',
                    'source': result.get('source', 'unknown_source'),
                    'offline_mode': OFFLINE_MODE,
                    'response_time': response_time
                })
            except Exception as search_error:
                print(f"❌ Search system error: {search_error}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'error': f'Search error: {str(search_error)}',
                    'answer': 'An error occurred during search. Please try again.',
                    'method': 'search_error',
                    'confidence': 0,
                    'analyzed_items': 0
                }), 500

        # Fallback if system not initialized
        print("❌ Search system not available")
        return jsonify({
            'answer': 'The AI system is currently initializing. Please try again in a moment.',
            'method': 'system_initializing',
            'confidence': 0,
            'analyzed_items': 0
        })

    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'answer': 'An unexpected error occurred. Please try again.',
            'method': 'error',
            'confidence': 0,
            'analyzed_items': 0
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """Handle feedback with learning and memory (enhanced with V2)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        print(f"📝 Feedback received: {data}")

        question = data.get('question', '')
        answer = data.get('answer', '')
        feedback_type = data.get('feedback', 'unknown')

        # Priority 1: Use V2 chatbot feedback handler (with disliked answer blocking)
        if use_v2_chatbot and enhanced_chatbot_v2:
            try:
                print("🎯 Using V2 chatbot feedback handler")
                result = enhanced_chatbot_v2.handle_feedback(question, answer, feedback_type)
                
                return jsonify({
                    'status': 'success',
                    'message': result.get('message', 'Feedback recorded'),
                    'action': result.get('action', 'recorded'),
                    'learning_stats': learning_stats,
                    'blocked_answers': len(enhanced_chatbot_v2.disliked_answers),
                    'total_feedback': len(enhanced_chatbot_v2.feedback_data),
                    'version': 'v2'
                })
            except Exception as e:
                print(f"⚠️ V2 feedback handler error: {e}, falling back to V1")

        # Priority 2: Use search system feedback recording
        if search_system:
            result = search_system.record_feedback(question, answer, feedback_type)

            return jsonify({
                'status': 'success',
                'message': 'Feedback recorded and learning updated',
                'learning_stats': result['learning_stats'],
                'blocked_answers': len(search_system.disliked_answers),
                'total_feedback': len(search_system.feedback_data),
                'version': 'v1'
            })

        return jsonify({
            'status': 'success',
            'message': 'Feedback recorded (system learning temporarily disabled)',
            'blocked_answers': 0,
            'total_feedback': 0,
            'version': 'basic'
        })

    except Exception as e:
        print(f"❌ Feedback endpoint error: {e}")
        return jsonify({'error': str(e)}), 500

# ============================================================================
# RESEARCH & EVALUATION ENDPOINTS
# ============================================================================

@app.route('/analytics/live', methods=['GET'])
def analytics_live():
    """Get live analytics and statistics for research"""
    try:
        stats = get_live_statistics()
        return jsonify({
            'status': 'success',
            'data': stats,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/report', methods=['GET'])
def analytics_report():
    """Generate comprehensive research report"""
    try:
        report = generate_report_api()
        return jsonify({
            'status': 'success',
            'report': report
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics/export', methods=['GET'])
def analytics_export():
    """Export research data to CSV files"""
    try:
        from evaluation_analytics import ChatbotEvaluator
        evaluator = ChatbotEvaluator()
        evaluator.export_to_csv('research_exports')
        
        return jsonify({
            'status': 'success',
            'message': 'Data exported to research_exports/ folder',
            'files': ['response_logs.csv', 'feedback_data.csv']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    mode_status = "OFFLINE MODE" if OFFLINE_MODE else "ONLINE MODE"
    chatbot_version = "V2" if (use_v2_chatbot and enhanced_chatbot_v2) else "V1" if enhanced_chatbot else "Basic"
    
    return jsonify({
        'message': f'Green University Enhanced RAG API Server ({mode_status})',
        'status': 'running',
        'mode': 'offline' if OFFLINE_MODE else 'online',
        'chatbot_version': chatbot_version,
        'endpoints': {
            'GET /health': 'Health check',
            'GET /stats': 'System statistics',
            'POST /chat': 'Chat with AI',
            'POST /feedback': 'Submit feedback with learning',
            'GET /analytics/live': 'Live analytics and statistics',
            'GET /analytics/report': 'Generate research report',
            'GET /analytics/export': 'Export data to CSV'
        },
        'features': [
            'JSON data analysis' + (' (Offline Only)' if OFFLINE_MODE else ' with Enhanced Chatbot'),
            'Feedback-based learning and pattern recognition',
            'Memory and continuous learning',
            'CSE fee accuracy guarantee (BDT 70,000 per semester)',
            'No internet connection required' if OFFLINE_MODE else 'Requires Ollama for Enhanced Chatbot'
        ],
        'enhanced_features_v2': [
            '✅ RAG (Retrieval-Augmented Generation)',
            '✅ RL with User Feedback (Like/Dislike)',
            '✅ Language Restriction (English Only)',
            '✅ Disliked Answer Blocking',
            '✅ Response Pattern Learning',
            '✅ Accurate CSE tuition fee responses',
            '✅ Improved response quality through pattern analysis'
        ] if chatbot_version == "V2" else [
            'Learns from user feedback patterns',
            'Accurate CSE tuition fee responses',
            'Improved response quality through pattern analysis',
            'Seamless integration with existing search system'
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    print("🏥 Health endpoint called")
    
    # Ensure system is initialized before checking status
    system_ready = ensure_system_initialized()
    
    # Get components from Flask app config
    components = app.config.get('SYSTEM_COMPONENTS', {})
    llm_loaded = components.get('llm') is not None
    search_system_loaded = components.get('search_system') is not None
    enhanced_chatbot_loaded = components.get('enhanced_chatbot') is not None
    enhanced_chatbot_v2_loaded = components.get('enhanced_chatbot_v2') is not None
    
    chatbot_version = "V2" if enhanced_chatbot_v2_loaded else "V1" if enhanced_chatbot_loaded else "Basic"
    
    print(f"🔍 Health check - System ready: {system_ready}")
    print(f"🔍 Health check - Components: llm={llm_loaded}, search={search_system_loaded}, v1={enhanced_chatbot_loaded}, v2={enhanced_chatbot_v2_loaded}")
    
    return jsonify({
        'status': 'healthy' if system_ready else 'initializing',
        'mode': 'offline' if OFFLINE_MODE else 'online',
        'chatbot_version': chatbot_version,
        'llm_loaded': llm_loaded,
        'enhanced_chatbot_v1_loaded': enhanced_chatbot_loaded,
        'enhanced_chatbot_v2_loaded': enhanced_chatbot_v2_loaded,
        'search_system_loaded': search_system_loaded,
        'model': 'offline_json_search' if OFFLINE_MODE else 'enhanced_llama3.2_json_v2',
        'timestamp': time.time(),
        'learning_active': system_ready,
        'offline_capable': True,
        'feedback_learning': enhanced_chatbot_v2_loaded or enhanced_chatbot_loaded,
        'system_ready': system_ready,
        'features': {
            'rag': enhanced_chatbot_v2_loaded,
            'reinforcement_learning': enhanced_chatbot_v2_loaded,
            'english_only': enhanced_chatbot_v2_loaded,
            'disliked_blocking': enhanced_chatbot_v2_loaded
        }
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Get system statistics"""
    global learning_stats

    if search_system:
        return jsonify({
            'total_feedback': learning_stats['total_feedback'],
            'likes': learning_stats['likes'],
            'dislikes': learning_stats['dislikes'],
            'blocked_answers': learning_stats['blocked_answers'],
            'improved_responses': learning_stats['improved_responses'],
            'available_data': len(search_system.questions) if hasattr(search_system, 'questions') else 0,
            'total_original_data': len(search_system.data) if hasattr(search_system, 'data') else 0,
            'llm_active': llm is not None,
            'learning_enabled': True
        })

    return jsonify({
        'total_feedback': learning_stats['total_feedback'],
        'likes': learning_stats['likes'],
        'dislikes': learning_stats['dislikes'],
        'blocked_answers': learning_stats['blocked_answers'],
        'available_data': 0,
        'total_original_data': 0,
        'llm_active': llm is not None,
        'learning_enabled': False
    })

if __name__ == '__main__':
    mode_text = "OFFLINE" if OFFLINE_MODE else "Enhanced LLaMA 3.2 + JSON"
    print(f"🚀 Initializing {mode_text} RAG API Server...")

    # Initialize system before starting Flask
    print("🔄 Pre-initializing system components...")
    try:
        init_success = initialize_system()
    except Exception as init_error:
        print(f"❌ System initialization error: {init_error}")
        import traceback
        traceback.print_exc()
        init_success = False

    if init_success:
        print("✅ System pre-initialized successfully")
        print("🌐 Starting Flask server on port 5000...")
        features_text = "JSON analysis + Offline processing" if OFFLINE_MODE else "JSON analysis + Enhanced Chatbot + RL learning + Feedback Learning"
        print(f"🎯 Features: {features_text}")
        if OFFLINE_MODE:
            print("🔌 OFFLINE MODE: No internet connection required")
        else:
            print("🌐 ONLINE MODE: Enhanced chatbot with feedback learning")
            print("💡 Enhanced features:")
            print("   - Learns from user feedback patterns")
            print("   - Accurate CSE fee responses (BDT 70,000 per semester)")
            print("   - Improved response quality through pattern analysis")

        try:
            print("🔗 Server will be accessible at:")
            print("   - http://localhost:5000")
            print("   - http://127.0.0.1:5000")
            print("📡 Ready to receive requests...")
            app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as flask_error:
            print(f"❌ Flask server error: {flask_error}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ Failed to initialize system")
        if not OFFLINE_MODE:
            print("💡 Make sure Ollama is running with: ollama serve")
            print("💡 And the model is pulled with: ollama pull llama3.2:1b")
        else:
            print("💡 Check that enhanced_ndata.json file exists and is valid")
