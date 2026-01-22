"""
Simple RAG Server - Dataset-First Approach
==========================================
- Searches dataset FIRST
- Returns EXACT dataset answers when confidence >= 55%
- Uses LLM fallback when confidence < 55%
- Shows reference in terminal
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import re
import requests

# Import evaluation middleware
from evaluation_middleware import log_chat_interaction, get_live_statistics, generate_report_api

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000", "http://127.0.0.1:5173"])

# ============================================================================
# CONFIG
# ============================================================================
CONFIDENCE_THRESHOLD = 0.55  # 55% - use LLM if below this
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"

# ============================================================================
# MASTER DATASET
# ============================================================================
class MasterDataset:
    def __init__(self):
        self.data = []
        self.questions = []
        self.answers = []
        self.vectorizer = None
        self.tfidf_matrix = None
        
    def load_all_datasets(self, dataset_folder="dataset"):
        """Load and combine all dataset files into master dataset"""
        print("\n" + "="*80)
        print("📚 LOADING MASTER DATASET")
        print("="*80)
        
        if not os.path.exists(dataset_folder):
            print(f"❌ Dataset folder not found: {dataset_folder}")
            return False
        
        # Priority order - improved datasets first
        priority_files = [
            'CSE_improved.json',
            'EEE_improved.json', 
            'BBA_improved.json',
            'Fee_Summary_CRITICAL.json',
            'General_University_Info.json'
        ]
        
        loaded_files = []
        
        # Load priority files first
        for filename in priority_files:
            filepath = os.path.join(dataset_folder, filename)
            if os.path.exists(filepath):
                count = self._load_file(filepath, filename, priority=True)
                if count > 0:
                    loaded_files.append(f"✅ {filename}: {count} items (PRIORITY)")
        
        # Load other files
        for filename in os.listdir(dataset_folder):
            if filename.endswith('.json') and filename not in priority_files:
                filepath = os.path.join(dataset_folder, filename)
                count = self._load_file(filepath, filename, priority=False)
                if count > 0:
                    loaded_files.append(f"📄 {filename}: {count} items")
        
        # Print summary
        print("-"*80)
        for f in loaded_files:
            print(f"   {f}")
        print("-"*80)
        print(f"📊 TOTAL: {len(self.data)} items in master dataset")
        print("="*80 + "\n")
        
        # Build search index
        self._build_search_index()
        
        return True
    
    def _load_file(self, filepath, filename, priority=False):
        """Load a single dataset file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                items = json.load(f)
            
            if not isinstance(items, list):
                return 0
            
            count = 0
            for item in items:
                if 'question' in item and 'answer' in item:
                    # Add to master dataset
                    entry = {
                        'question': item['question'].strip(),
                        'answer': item['answer'].strip(),
                        'keywords': item.get('keywords', []),
                        'question_variations': item.get('question_variations', []),
                        'department': item.get('department', ''),
                        'categories': item.get('categories', []),
                        'source_file': filename,
                        'priority': priority
                    }
                    self.data.append(entry)
                    self.questions.append(entry['question'])
                    self.answers.append(entry['answer'])
                    count += 1
            
            return count
        except Exception as e:
            print(f"⚠️ Error loading {filename}: {e}")
            return 0
    
    def _build_search_index(self):
        """Build TF-IDF search index"""
        if not self.questions:
            return
        
        # Combine questions with variations for better matching
        search_texts = []
        for item in self.data:
            text_parts = [item['question']]
            text_parts.extend(item.get('question_variations', []))
            text_parts.extend(item.get('keywords', []))
            search_texts.append(' '.join(text_parts).lower())
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=10000,
            stop_words='english'
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(search_texts)
        print(f"✅ Search index built: {self.tfidf_matrix.shape}")
    
    def search(self, query, top_k=5):
        """Search dataset and return best matches"""
        if not self.vectorizer or self.tfidf_matrix is None:
            return []
        
        query_lower = query.lower().strip()
        query_normalized = ' '.join(query_lower.split())
        
        # STRATEGY 1: Exact match check
        for i, item in enumerate(self.data):
            q = item['question'].lower().strip()
            q_normalized = ' '.join(q.split())
            
            # Exact match
            if query_normalized == q_normalized:
                return [{'item': item, 'score': 1.0, 'match_type': 'EXACT_MATCH'}]
            
            # Variation exact match
            for var in item.get('question_variations', []):
                var_normalized = ' '.join(var.lower().strip().split())
                if query_normalized == var_normalized:
                    return [{'item': item, 'score': 0.99, 'match_type': 'VARIATION_EXACT'}]
        
        # STRATEGY 2: Word overlap for short queries
        query_words = set(query_normalized.split())
        best_overlap = None
        best_overlap_score = 0
        
        for item in self.data:
            q_words = set(item['question'].lower().split())
            
            # Check overlap
            if len(query_words) >= 2:
                intersection = len(query_words & q_words)
                union = len(query_words | q_words)
                jaccard = intersection / union if union > 0 else 0
                
                # Also check keyword match
                keywords = set(' '.join(item.get('keywords', [])).lower().split())
                keyword_match = len(query_words & keywords) / len(query_words) if query_words else 0
                
                combined = (jaccard * 0.6) + (keyword_match * 0.4)
                
                if combined > best_overlap_score:
                    best_overlap_score = combined
                    best_overlap = item
        
        if best_overlap and best_overlap_score >= 0.5:
            return [{'item': best_overlap, 'score': best_overlap_score, 'match_type': 'WORD_OVERLAP'}]
        
        # STRATEGY 3: TF-IDF similarity
        query_vec = self.vectorizer.transform([query_lower])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Get top matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum threshold
                results.append({
                    'item': self.data[idx],
                    'score': float(similarities[idx]),
                    'match_type': 'TFIDF'
                })
        
        return results

# ============================================================================
# GLOBAL INSTANCES
# ============================================================================
master_dataset = MasterDataset()

# ============================================================================
# LLM FUNCTIONS
# ============================================================================
def call_llm(question, context=None):
    """Call Ollama LLM when dataset confidence is low"""
    try:
        prompt = f"""You are a helpful assistant for Green University of Bangladesh.
Answer the following question in English only. Be concise and accurate.

Question: {question}

{"Context from database: " + context if context else ""}

Answer:"""
        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3}
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '').strip()
        return None
    except Exception as e:
        print(f"⚠️ LLM Error: {e}")
        return None

def format_answer_with_llm(question, raw_answer):
    """Use LLM to format and present the dataset answer in a more user-friendly way"""
    try:
        prompt = f"""You are a helpful assistant for Green University of Bangladesh.

Your task is to REFORMAT the following answer to make it more organized, clear, and user-friendly.
IMPORTANT RULES:
- Keep ALL the factual information EXACTLY as provided - DO NOT change any numbers, fees, dates, or facts
- Only improve the presentation and formatting
- Use bullet points (•) for lists
- Use clear headings if appropriate
- Be concise but friendly
- Respond in English only
- DO NOT add any information that is not in the original answer

Question: {question}

Original Answer: {raw_answer}

Reformatted Answer:"""
        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}  # Low temperature for consistency
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            formatted = result.get('response', '').strip()
            # If LLM returns something reasonable, use it; otherwise fall back to original
            if formatted and len(formatted) > 20:
                return formatted
        return raw_answer  # Return original if LLM fails
    except Exception as e:
        print(f"⚠️ LLM Format Error: {e}")
        return raw_answer  # Return original on error

# ============================================================================
# ROUTES
# ============================================================================
@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint - searches dataset first"""
    start_time = time.time()  # Track response time
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided', 'answer': 'Please provide a message.'}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'error': 'Empty message', 'answer': 'Please enter a message.'}), 400
        
        # Search dataset
        results = master_dataset.search(user_message)
        
        # Terminal logging
        print("\n" + "="*80)
        print(f"❓ USER QUESTION: {user_message}")
        print("="*80)
        
        best_score = results[0]['score'] if results else 0
        
        # HIGH CONFIDENCE (>= 55%) - Format dataset answer with LLM for better presentation
        if results and best_score >= CONFIDENCE_THRESHOLD:
            best = results[0]
            item = best['item']
            raw_answer = item['answer']
            
            # Show dataset reference in terminal
            print(f"✅ HIGH CONFIDENCE MATCH - Formatting with LLM")
            print(f"   📊 Score: {best['score']:.2%} (threshold: {CONFIDENCE_THRESHOLD:.0%})")
            print(f"   🔍 Match Type: {best['match_type']}")
            print(f"   📁 Source: {item['source_file']}")
            print(f"   🏷️ Department: {item.get('department', 'N/A')}")
            print("-"*80)
            print(f"📚 DATASET QUESTION:")
            print(f"   {item['question']}")
            print("-"*80)
            print(f"📝 RAW DATASET ANSWER:")
            print(f"   {raw_answer[:200]}..." if len(raw_answer) > 200 else f"   {raw_answer}")
            
            # Format the answer with LLM for better presentation
            formatted_answer = format_answer_with_llm(user_message, raw_answer)
            
            print("-"*80)
            print(f"✨ FORMATTED ANSWER:")
            print(f"   {formatted_answer[:200]}..." if len(formatted_answer) > 200 else f"   {formatted_answer}")
            print("="*80 + "\n")
            
            # Log interaction for research
            response_time = time.time() - start_time
            log_chat_interaction(
                question=user_message,
                answer=formatted_answer,
                response_time=response_time,
                source='dataset_formatted',
                confidence=best['score']
            )
            
            return jsonify({
                'answer': formatted_answer,
                'confidence': best['score'],
                'method': f"DATASET_{best['match_type']}",
                'source': item['source_file'],
                'department': item.get('department', ''),
                'is_from_dataset': True,
                'llm_formatted': True,
                'response_time': response_time
            })
        
        # LOW CONFIDENCE (< 55%) - Use LLM with context
        elif results and best_score >= 0.2:
            best = results[0]
            item = best['item']
            
            print(f"⚠️ LOW CONFIDENCE ({best_score:.2%}) - Using LLM with Dataset Context")
            print(f"   📁 Context from: {item['source_file']}")
            
            # Call LLM with dataset context
            llm_answer = call_llm(user_message, item['answer'])
            
            if llm_answer:
                print(f"🤖 LLM RESPONSE:")
                print(f"   {llm_answer[:200]}...")
                print("="*80 + "\n")
                
                # Log interaction for research
                response_time = time.time() - start_time
                log_chat_interaction(
                    question=user_message,
                    answer=llm_answer,
                    response_time=response_time,
                    source='llm_with_context',
                    confidence=best_score
                )
                
                return jsonify({
                    'answer': llm_answer,
                    'confidence': best_score,
                    'method': 'LLM_WITH_CONTEXT',
                    'source': item['source_file'],
                    'is_from_dataset': False,
                    'llm_used': True,
                    'response_time': response_time
                })
        
        # NO MATCH - Use LLM without context
        print(f"❌ NO MATCH - Using LLM Only")
        llm_answer = call_llm(user_message)
        
        if llm_answer:
            print(f"🤖 LLM RESPONSE (no context):")
            print(f"   {llm_answer[:200]}...")
            print("="*80 + "\n")
            
            # Log interaction for research
            response_time = time.time() - start_time
            log_chat_interaction(
                question=user_message,
                answer=llm_answer,
                response_time=response_time,
                source='llm_only',
                confidence=0
            )
            
            return jsonify({
                'answer': llm_answer,
                'confidence': 0,
                'method': 'LLM_ONLY',
                'is_from_dataset': False,
                'llm_used': True,
                'response_time': response_time
            })
        
        # Fallback
        return jsonify({
            'answer': "I couldn't find specific information about that. Please try asking about:\n\n• **Tuition fees** for specific programs (CSE, EEE, BBA)\n• **Admission requirements** and process\n• **Program duration** and curriculum\n• **Scholarships** and financial aid\n\nOr contact the admission office at Green University: 01775234234",
            'confidence': 0,
            'method': 'no_match',
            'is_from_dataset': False
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")

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
            'timestamp': datetime.now().isoformat()
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
        return jsonify({'error': str(e), 'answer': 'An error occurred. Please try again.'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'dataset_size': len(master_dataset.data),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/stats', methods=['GET'])
def stats():
    """Dataset statistics"""
    # Count by department
    dept_counts = {}
    for item in master_dataset.data:
        dept = item.get('department', 'Unknown')
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    return jsonify({
        'total_items': len(master_dataset.data),
        'by_department': dept_counts,
        'sources': list(set(item['source_file'] for item in master_dataset.data))
    })

@app.route('/feedback', methods=['POST'])
def feedback():
    """Handle feedback"""
    data = request.get_json()
    feedback_type = data.get('feedback', 'unknown')
    print(f"📝 Feedback received: {feedback_type}")
    return jsonify({'status': 'success', 'message': f'Feedback ({feedback_type}) recorded'})

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Green University Simple RAG Server',
        'status': 'running',
        'dataset_size': len(master_dataset.data),
        'endpoints': {
            'POST /chat': 'Send message',
            'GET /health': 'Health check',
            'GET /stats': 'Dataset statistics',
            'POST /feedback': 'Submit feedback'
        }
    })

# ============================================================================
# MAIN
# ============================================================================
if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 GREEN UNIVERSITY SIMPLE RAG SERVER")
    print("="*80)
    print("📋 Features:")
    print("   ✅ Dataset-first approach")
    print("   ✅ Exact answer matching")
    print("   ✅ Terminal reference logging")
    print("   ✅ No unnecessary LLM generation")
    print("="*80 + "\n")
    
    # Load master dataset
    master_dataset.load_all_datasets('dataset')
    
    # Start server
    print("\n🌐 Starting server on http://localhost:5000")
    print("📡 Ready to receive requests...\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)
