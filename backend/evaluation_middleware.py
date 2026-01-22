"""
Evaluation Middleware Integration
==================================
Integrates the evaluation and analytics system with Flask servers
Automatically tracks response times and logs all interactions
"""

from functools import wraps
import time
from evaluation_analytics import ChatbotEvaluator

# Global evaluator instance
_evaluator_instance = None

def get_evaluator():
    """Get or create evaluator instance"""
    global _evaluator_instance
    if _evaluator_instance is None:
        _evaluator_instance = ChatbotEvaluator(
            response_log_file='response_logs.json',
            feedback_file='user_feedback_data.json'
        )
    return _evaluator_instance

def track_response_time(source='unknown'):
    """
    Decorator to automatically track response time and log responses
    
    Usage:
        @track_response_time(source='dataset')
        def my_function(question):
            return answer
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Execute the function
            result = func(*args, **kwargs)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Extract question and answer from result if possible
            question = kwargs.get('question', '') or (args[0] if args else '')
            answer = result if isinstance(result, str) else str(result)
            confidence = kwargs.get('confidence', None)
            
            # Log the response
            evaluator = get_evaluator()
            evaluator.log_response(
                question=question,
                answer=answer,
                response_time=response_time,
                source=source,
                confidence=confidence
            )
            
            return result
        return wrapper
    return decorator

def log_chat_interaction(question: str, answer: str, response_time: float, 
                         source: str = 'unknown', confidence: float = None):
    """
    Manually log a chat interaction
    Use this when you can't use the decorator
    """
    evaluator = get_evaluator()
    return evaluator.log_response(
        question=question,
        answer=answer,
        response_time=response_time,
        source=source,
        confidence=confidence
    )

def get_live_statistics():
    """
    Get current statistics for live monitoring
    Returns a quick summary suitable for API responses
    """
    evaluator = get_evaluator()
    
    # Get recent statistics (last 24 hours)
    rt_stats = evaluator.calculate_response_time_statistics(time_window_hours=24)
    feedback_stats = evaluator.analyze_user_feedback()
    
    return {
        'response_time': {
            'average': rt_stats.get('average_response_time', 0),
            'median': rt_stats.get('median_response_time', 0),
            'min': rt_stats.get('min_response_time', 0),
            'max': rt_stats.get('max_response_time', 0),
            'total_responses': rt_stats.get('total_responses', 0)
        },
        'user_feedback': {
            'total': feedback_stats.get('total_feedback', 0),
            'likes': feedback_stats.get('likes', 0),
            'dislikes': feedback_stats.get('dislikes', 0),
            'satisfaction_rate': feedback_stats.get('satisfaction_rate', 0)
        }
    }

def generate_report_api():
    """
    Generate a full research report (for API endpoint)
    """
    evaluator = get_evaluator()
    report = evaluator.generate_research_report()
    return report
