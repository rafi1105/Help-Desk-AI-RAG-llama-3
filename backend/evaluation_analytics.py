"""
LLM Model Accuracy Evaluation and Response Time Analysis
=========================================================
Research Module for Chatbot Performance Evaluation

Features:
1. LLM Model Accuracy Evaluation
   - Answer relevance scoring
   - Semantic similarity metrics
   - BLEU score calculation
   - F1 score for keyword matching
   
2. Response Time Analysis
   - Average response time
   - Min/Max response time
   - Response time distribution
   - Performance over time

3. User Feedback Analysis
   - Like/Dislike ratio
   - Feedback trends
   - Answer quality metrics

4. Comprehensive Research Reports
   - JSON export for analysis
   - CSV export for spreadsheet tools
   - Statistical summaries
   - Visualization data
"""

import json
import numpy as np
import time
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import statistics
from collections import defaultdict
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class ChatbotEvaluator:
    """
    Comprehensive evaluation system for chatbot performance
    """
    
    def __init__(self, response_log_file='response_logs.json', 
                 feedback_file='user_feedback_data.json',
                 ground_truth_file='dataset/ground_truth.json'):
        self.response_log_file = response_log_file
        self.feedback_file = feedback_file
        self.ground_truth_file = ground_truth_file
        self.response_logs = []
        self.feedback_data = []
        self.ground_truth = {}
        self.load_data()
    
    def load_data(self):
        """Load all data files"""
        # Load response logs
        if os.path.exists(self.response_log_file):
            try:
                with open(self.response_log_file, 'r', encoding='utf-8') as f:
                    self.response_logs = json.load(f)
            except:
                self.response_logs = []
        
        # Load feedback data
        if os.path.exists(self.feedback_file):
            try:
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    self.feedback_data = json.load(f)
            except:
                self.feedback_data = []
        
        # Load ground truth (if exists)
        if os.path.exists(self.ground_truth_file):
            try:
                with open(self.ground_truth_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ground_truth = {item['question']: item['answer'] for item in data}
            except:
                self.ground_truth = {}
    
    def log_response(self, question: str, answer: str, response_time: float, 
                     source: str = 'unknown', confidence: float = None):
        """Log a chatbot response with timing information"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'answer': answer,
            'response_time': response_time,
            'source': source,  # 'dataset', 'llm', 'rag', etc.
            'confidence': confidence
        }
        self.response_logs.append(log_entry)
        self._save_response_logs()
        return log_entry
    
    def _save_response_logs(self):
        """Save response logs to file"""
        try:
            with open(self.response_log_file, 'w', encoding='utf-8') as f:
                json.dump(self.response_logs, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving response logs: {e}")
    
    # ============================================================================
    # ACCURACY EVALUATION METRICS
    # ============================================================================
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity using TF-IDF and cosine similarity
        Returns: similarity score between 0 and 1
        """
        try:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def calculate_bleu_score(self, reference: str, hypothesis: str) -> float:
        """
        Calculate BLEU score (0-1) for answer quality
        Higher score = better match with reference answer
        Uses safer implementation to avoid NLTK version issues
        """
        try:
            reference_tokens = word_tokenize(reference.lower())
            hypothesis_tokens = word_tokenize(hypothesis.lower())
            
            # Handle empty inputs
            if not reference_tokens or not hypothesis_tokens:
                return 0.0
            
            # Calculate n-gram precision manually (safer than NLTK's sentence_bleu)
            from collections import Counter
            
            # Calculate 1-gram to 4-gram precisions
            precisions = []
            for n in range(1, 5):
                ref_ngrams = Counter([tuple(reference_tokens[i:i+n]) 
                                     for i in range(len(reference_tokens)-n+1)])
                hyp_ngrams = Counter([tuple(hypothesis_tokens[i:i+n]) 
                                     for i in range(len(hypothesis_tokens)-n+1)])
                
                if not hyp_ngrams:
                    precisions.append(0.0)
                    continue
                
                # Count matches
                matches = sum((ref_ngrams & hyp_ngrams).values())
                total = sum(hyp_ngrams.values())
                
                # Add smoothing for zero counts
                precision = (matches + 1e-10) / (total + 1e-10)
                precisions.append(precision)
            
            # Geometric mean of precisions
            if all(p > 0 for p in precisions):
                import math
                geo_mean = math.exp(sum(math.log(p) for p in precisions) / len(precisions))
            else:
                geo_mean = 0.0
            
            # Brevity penalty
            ref_len = len(reference_tokens)
            hyp_len = len(hypothesis_tokens)
            if hyp_len >= ref_len:
                bp = 1.0
            else:
                bp = math.exp(1 - ref_len / hyp_len) if hyp_len > 0 else 0.0
            
            # Final BLEU score
            bleu = bp * geo_mean
            
            return float(min(bleu, 1.0))  # Cap at 1.0
            
        except Exception as e:
            print(f"Warning: BLEU calculation failed: {e}")
            return 0.0
    
    def calculate_keyword_f1(self, reference: str, hypothesis: str, 
                            important_keywords: List[str] = None) -> Dict:
        """
        Calculate precision, recall, and F1 score based on keyword matching
        """
        reference_words = set(reference.lower().split())
        hypothesis_words = set(hypothesis.lower().split())
        
        # If important keywords provided, focus on those
        if important_keywords:
            important_keywords = set(k.lower() for k in important_keywords)
            reference_words = reference_words.intersection(important_keywords)
        
        # Calculate metrics
        true_positives = len(reference_words.intersection(hypothesis_words))
        false_positives = len(hypothesis_words - reference_words)
        false_negatives = len(reference_words - hypothesis_words)
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'matched_keywords': list(reference_words.intersection(hypothesis_words))
        }
    
    def evaluate_answer_accuracy(self, question: str, answer: str, 
                                 reference_answer: str = None) -> Dict:
        """
        Comprehensive accuracy evaluation of a single answer
        """
        if reference_answer is None:
            reference_answer = self.ground_truth.get(question, "")
        
        if not reference_answer:
            return {
                'evaluated': False,
                'message': 'No reference answer available'
            }
        
        # Calculate multiple metrics
        semantic_sim = self.calculate_semantic_similarity(reference_answer, answer)
        bleu = self.calculate_bleu_score(reference_answer, answer)
        keyword_metrics = self.calculate_keyword_f1(reference_answer, answer)
        
        # Overall accuracy score (weighted average)
        overall_accuracy = (
            semantic_sim * 0.4 +
            bleu * 0.3 +
            keyword_metrics['f1_score'] * 0.3
        )
        
        return {
            'evaluated': True,
            'semantic_similarity': semantic_sim,
            'bleu_score': bleu,
            'precision': keyword_metrics['precision'],
            'recall': keyword_metrics['recall'],
            'f1_score': keyword_metrics['f1_score'],
            'overall_accuracy': overall_accuracy,
            'matched_keywords': keyword_metrics['matched_keywords'],
            'accuracy_grade': self._grade_accuracy(overall_accuracy)
        }
    
    def _grade_accuracy(self, score: float) -> str:
        """Convert accuracy score to letter grade"""
        if score >= 0.9:
            return 'A+ (Excellent)'
        elif score >= 0.8:
            return 'A (Very Good)'
        elif score >= 0.7:
            return 'B (Good)'
        elif score >= 0.6:
            return 'C (Acceptable)'
        elif score >= 0.5:
            return 'D (Poor)'
        else:
            return 'F (Very Poor)'
    
    def batch_evaluate_accuracy(self, limit: int = None) -> Dict:
        """
        Evaluate accuracy for all logged responses
        Returns comprehensive statistics
        """
        evaluated_responses = []
        
        logs_to_evaluate = self.response_logs[-limit:] if limit else self.response_logs
        
        for log in logs_to_evaluate:
            question = log['question']
            answer = log['answer']
            
            evaluation = self.evaluate_answer_accuracy(question, answer)
            if evaluation['evaluated']:
                evaluated_responses.append({
                    'timestamp': log['timestamp'],
                    'question': question,
                    'source': log.get('source', 'unknown'),
                    **evaluation
                })
        
        if not evaluated_responses:
            return {'message': 'No responses could be evaluated'}
        
        # Calculate statistics
        accuracies = [r['overall_accuracy'] for r in evaluated_responses]
        semantic_sims = [r['semantic_similarity'] for r in evaluated_responses]
        bleu_scores = [r['bleu_score'] for r in evaluated_responses]
        f1_scores = [r['f1_score'] for r in evaluated_responses]
        
        return {
            'total_evaluated': len(evaluated_responses),
            'overall_metrics': {
                'mean_accuracy': statistics.mean(accuracies),
                'median_accuracy': statistics.median(accuracies),
                'std_accuracy': statistics.stdev(accuracies) if len(accuracies) > 1 else 0,
                'min_accuracy': min(accuracies),
                'max_accuracy': max(accuracies)
            },
            'semantic_similarity': {
                'mean': statistics.mean(semantic_sims),
                'median': statistics.median(semantic_sims)
            },
            'bleu_score': {
                'mean': statistics.mean(bleu_scores),
                'median': statistics.median(bleu_scores)
            },
            'f1_score': {
                'mean': statistics.mean(f1_scores),
                'median': statistics.median(f1_scores)
            },
            'grade_distribution': self._calculate_grade_distribution(accuracies),
            'detailed_results': evaluated_responses
        }
    
    def _calculate_grade_distribution(self, accuracies: List[float]) -> Dict:
        """Calculate distribution of accuracy grades"""
        grades = [self._grade_accuracy(acc) for acc in accuracies]
        grade_counts = defaultdict(int)
        for grade in grades:
            grade_counts[grade] += 1
        return dict(grade_counts)
    
    # ============================================================================
    # RESPONSE TIME ANALYSIS
    # ============================================================================
    
    def calculate_response_time_statistics(self, time_window_hours: int = None) -> Dict:
        """
        Calculate comprehensive response time statistics
        
        Args:
            time_window_hours: Only consider responses within this time window
        """
        # Filter logs by time window if specified
        if time_window_hours:
            cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
            filtered_logs = [
                log for log in self.response_logs
                if datetime.fromisoformat(log['timestamp']) >= cutoff_time
            ]
        else:
            filtered_logs = self.response_logs
        
        if not filtered_logs:
            return {'message': 'No response data available'}
        
        response_times = [log['response_time'] for log in filtered_logs]
        
        # Basic statistics
        stats = {
            'total_responses': len(response_times),
            'average_response_time': statistics.mean(response_times),
            'median_response_time': statistics.median(response_times),
            'min_response_time': min(response_times),
            'max_response_time': max(response_times),
            'std_deviation': statistics.stdev(response_times) if len(response_times) > 1 else 0,
            'total_time': sum(response_times)
        }
        
        # Percentile analysis
        sorted_times = sorted(response_times)
        stats['percentiles'] = {
            'p50': self._percentile(sorted_times, 50),
            'p75': self._percentile(sorted_times, 75),
            'p90': self._percentile(sorted_times, 90),
            'p95': self._percentile(sorted_times, 95),
            'p99': self._percentile(sorted_times, 99)
        }
        
        # Response time distribution
        stats['distribution'] = {
            'under_1s': sum(1 for t in response_times if t < 1.0),
            '1s_to_2s': sum(1 for t in response_times if 1.0 <= t < 2.0),
            '2s_to_5s': sum(1 for t in response_times if 2.0 <= t < 5.0),
            '5s_to_10s': sum(1 for t in response_times if 5.0 <= t < 10.0),
            'over_10s': sum(1 for t in response_times if t >= 10.0)
        }
        
        # Performance by source
        sources = defaultdict(list)
        for log in filtered_logs:
            sources[log.get('source', 'unknown')].append(log['response_time'])
        
        stats['by_source'] = {
            source: {
                'count': len(times),
                'average': statistics.mean(times),
                'median': statistics.median(times)
            }
            for source, times in sources.items()
        }
        
        # Time-based trends
        stats['trends'] = self._calculate_time_trends(filtered_logs)
        
        return stats
    
    def _percentile(self, sorted_list: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        index = (len(sorted_list) - 1) * percentile / 100
        floor_index = int(index)
        ceil_index = floor_index + 1
        
        if ceil_index >= len(sorted_list):
            return sorted_list[floor_index]
        
        fraction = index - floor_index
        return sorted_list[floor_index] + fraction * (sorted_list[ceil_index] - sorted_list[floor_index])
    
    def _calculate_time_trends(self, logs: List[Dict]) -> Dict:
        """Calculate response time trends over time"""
        if not logs:
            return {}
        
        # Group by hour
        hourly_times = defaultdict(list)
        for log in logs:
            try:
                timestamp = datetime.fromisoformat(log['timestamp'])
                hour_key = timestamp.strftime('%Y-%m-%d %H:00')
                hourly_times[hour_key].append(log['response_time'])
            except:
                continue
        
        trends = {}
        for hour, times in sorted(hourly_times.items()):
            trends[hour] = {
                'count': len(times),
                'average': statistics.mean(times),
                'median': statistics.median(times)
            }
        
        return trends
    
    # ============================================================================
    # USER FEEDBACK ANALYSIS
    # ============================================================================
    
    def analyze_user_feedback(self) -> Dict:
        """
        Comprehensive analysis of user feedback
        """
        if not self.feedback_data:
            return {'message': 'No feedback data available'}
        
        total_feedback = len(self.feedback_data)
        likes = sum(1 for f in self.feedback_data if f.get('feedback') == 'like')
        dislikes = sum(1 for f in self.feedback_data if f.get('feedback') == 'dislike')
        
        # Calculate satisfaction rate
        satisfaction_rate = (likes / total_feedback) * 100 if total_feedback > 0 else 0
        
        # Analyze feedback over time
        feedback_timeline = defaultdict(lambda: {'likes': 0, 'dislikes': 0})
        for feedback in self.feedback_data:
            try:
                timestamp = datetime.fromisoformat(feedback['timestamp'])
                date_key = timestamp.strftime('%Y-%m-%d')
                if feedback.get('feedback') == 'like':
                    feedback_timeline[date_key]['likes'] += 1
                else:
                    feedback_timeline[date_key]['dislikes'] += 1
            except:
                continue
        
        # Most liked/disliked topics
        liked_questions = [f['question'] for f in self.feedback_data if f.get('feedback') == 'like']
        disliked_questions = [f['question'] for f in self.feedback_data if f.get('feedback') == 'dislike']
        
        return {
            'total_feedback': total_feedback,
            'likes': likes,
            'dislikes': dislikes,
            'satisfaction_rate': satisfaction_rate,
            'like_dislike_ratio': likes / dislikes if dislikes > 0 else float('inf'),
            'feedback_timeline': dict(feedback_timeline),
            'most_liked_topics': self._extract_topics(liked_questions),
            'most_disliked_topics': self._extract_topics(disliked_questions)
        }
    
    def _extract_topics(self, questions: List[str], top_n: int = 5) -> List[Dict]:
        """Extract most common topics from questions"""
        topic_counts = defaultdict(int)
        
        for question in questions:
            words = question.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    topic_counts[word] += 1
        
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'topic': topic, 'count': count} for topic, count in sorted_topics[:top_n]]
    
    # ============================================================================
    # COMPREHENSIVE RESEARCH REPORT
    # ============================================================================
    
    def generate_research_report(self, output_file: str = None) -> Dict:
        """
        Generate comprehensive research report with all metrics
        """
        print("\n" + "="*80)
        print("📊 GENERATING RESEARCH REPORT")
        print("="*80)
        
        report = {
            'report_generated': datetime.now().isoformat(),
            'data_period': {
                'start': self.response_logs[0]['timestamp'] if self.response_logs else 'N/A',
                'end': self.response_logs[-1]['timestamp'] if self.response_logs else 'N/A'
            },
            'accuracy_evaluation': self.batch_evaluate_accuracy(),
            'response_time_analysis': self.calculate_response_time_statistics(),
            'user_feedback_analysis': self.analyze_user_feedback(),
            'summary': {}
        }
        
        # Generate executive summary
        report['summary'] = self._generate_executive_summary(report)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"✅ Report saved to: {output_file}")
        
        # Print summary
        self._print_report_summary(report)
        
        return report
    
    def _generate_executive_summary(self, report: Dict) -> Dict:
        """Generate executive summary of the research"""
        summary = {}
        
        # Accuracy summary
        if 'overall_metrics' in report.get('accuracy_evaluation', {}):
            acc = report['accuracy_evaluation']['overall_metrics']
            summary['accuracy'] = {
                'average_accuracy': f"{acc['mean_accuracy']*100:.2f}%",
                'grade': self._grade_accuracy(acc['mean_accuracy']),
                'consistency': 'High' if acc.get('std_accuracy', 0) < 0.15 else 'Medium' if acc.get('std_accuracy', 0) < 0.25 else 'Low'
            }
        
        # Response time summary
        if 'average_response_time' in report.get('response_time_analysis', {}):
            rt = report['response_time_analysis']
            summary['response_time'] = {
                'average': f"{rt['average_response_time']:.3f}s",
                'performance_grade': 'Excellent' if rt['average_response_time'] < 2 else 'Good' if rt['average_response_time'] < 5 else 'Needs Improvement',
                'consistency': 'High' if rt.get('std_deviation', 0) < 1 else 'Medium' if rt.get('std_deviation', 0) < 2 else 'Low'
            }
        
        # User satisfaction summary
        if 'satisfaction_rate' in report.get('user_feedback_analysis', {}):
            uf = report['user_feedback_analysis']
            summary['user_satisfaction'] = {
                'satisfaction_rate': f"{uf['satisfaction_rate']:.2f}%",
                'grade': 'Excellent' if uf['satisfaction_rate'] >= 80 else 'Good' if uf['satisfaction_rate'] >= 60 else 'Needs Improvement',
                'total_interactions': uf['total_feedback']
            }
        
        return summary
    
    def _print_report_summary(self, report: Dict):
        """Print formatted summary to console"""
        summary = report.get('summary', {})
        
        print("\n📋 EXECUTIVE SUMMARY")
        print("-"*80)
        
        if 'accuracy' in summary:
            acc = summary['accuracy']
            print(f"\n🎯 Model Accuracy:")
            print(f"   Average Accuracy: {acc['average_accuracy']}")
            print(f"   Grade: {acc['grade']}")
            print(f"   Consistency: {acc['consistency']}")
        
        if 'response_time' in summary:
            rt = summary['response_time']
            print(f"\n⚡ Response Time Performance:")
            print(f"   Average Time: {rt['average']}")
            print(f"   Performance: {rt['performance_grade']}")
            print(f"   Consistency: {rt['consistency']}")
        
        if 'user_satisfaction' in summary:
            us = summary['user_satisfaction']
            print(f"\n😊 User Satisfaction:")
            print(f"   Satisfaction Rate: {us['satisfaction_rate']}")
            print(f"   Grade: {us['grade']}")
            print(f"   Total Interactions: {us['total_interactions']}")
        
        print("\n" + "="*80)
    
    def export_to_csv(self, output_dir: str = 'research_exports'):
        """
        Export research data to CSV files for analysis in Excel/spreadsheet tools
        """
        import csv
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Export response logs
        if self.response_logs:
            with open(f'{output_dir}/response_logs.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'question', 'answer', 'response_time', 'source', 'confidence'])
                writer.writeheader()
                writer.writerows(self.response_logs)
        
        # Export feedback data
        if self.feedback_data:
            with open(f'{output_dir}/feedback_data.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'question', 'answer', 'feedback'])
                writer.writeheader()
                writer.writerows(self.feedback_data)
        
        print(f"✅ CSV files exported to: {output_dir}/")


# ============================================================================
# STANDALONE TESTING
# ============================================================================

if __name__ == '__main__':
    print("🔬 Chatbot Evaluation and Analytics System")
    print("="*80)
    
    evaluator = ChatbotEvaluator()
    
    # Generate comprehensive report
    report = evaluator.generate_research_report('research_report.json')
    
    # Export to CSV
    evaluator.export_to_csv()
    
    print("\n✅ Evaluation complete!")
