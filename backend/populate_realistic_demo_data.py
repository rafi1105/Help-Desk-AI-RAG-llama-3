"""
Generate Realistic Demo Data with Varied Answer Quality
========================================================
Creates demo data with different quality levels to show
metrics working properly (not all 100%)
"""

import json
import random
from datetime import datetime, timedelta
from evaluation_analytics import ChatbotEvaluator

def generate_realistic_demo_data():
    """Generate realistic demo data with varied answer quality"""
    
    print("🔧 Generating realistic demo data with varied answer quality...")
    
    # QA pairs with different quality answers
    qa_pairs = [
        # Perfect matches (will score ~100%)
        {
            "question": "What is the tuition fee for CSE?",
            "answer": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "source": "dataset",
            "quality": "perfect"
        },
        {
            "question": "What is the address of the university?",
            "answer": "66 Mohakhali, Dhaka-1212, Bangladesh",
            "source": "dataset",
            "quality": "perfect"
        },
        
        # Very good answers (will score 70-95%)
        {
            "question": "What are the admission requirements?",
            "answer": "For admission, minimum GPA of 3.5 in SSC and HSC combined is required.",
            "source": "llm",
            "quality": "very_good"
        },
        {
            "question": "What is the duration of the CSE program?",
            "answer": "It's a 4 years undergraduate program.",
            "source": "llm",
            "quality": "very_good"
        },
        
        # Good answers (will score 50-70%)
        {
            "question": "How can I contact the admissions office?",
            "answer": "You can reach admissions at admissions@university.edu or phone +880-2-123456",
            "source": "rag",
            "quality": "good"
        },
        {
            "question": "What is the tuition fee for CSE?",
            "answer": "For CSE program, the tuition is Tk. 589,900 for top GPA students.",
            "source": "rag",
            "quality": "good"
        },
        
        # Acceptable answers (will score 30-50%)
        {
            "question": "What are the admission requirements?",
            "answer": "Students need good grades in SSC and HSC to get admission.",
            "source": "llm",
            "quality": "acceptable"
        },
        {
            "question": "What is the address of the university?",
            "answer": "The campus is in Mohakhali area of Dhaka city.",
            "source": "rag",
            "quality": "acceptable"
        },
        
        # Additional varied responses
        {
            "question": "When is the next semester starting?",
            "answer": "The next semester starts in January 2026.",
            "source": "rag",
            "quality": "good"
        },
        {
            "question": "What programs does the university offer?",
            "answer": "The university offers programs in CSE, EEE, BBA, Law, and Journalism.",
            "source": "llm",
            "quality": "very_good"
        }
    ]
    
    # Initialize evaluator
    evaluator = ChatbotEvaluator()
    evaluator.response_logs = []
    evaluator.feedback_data = []
    
    # Generate 50 response logs with varied quality
    start_time = datetime.now() - timedelta(days=7)
    
    for i in range(50):
        qa = random.choice(qa_pairs)
        
        # Vary response times based on source
        if qa['source'] == 'dataset':
            response_time = random.uniform(0.1, 0.5)
        elif qa['source'] == 'llm':
            response_time = random.uniform(2.0, 5.0)
        else:  # rag
            response_time = random.uniform(1.0, 3.0)
        
        # Confidence correlates with quality
        if qa['quality'] == 'perfect':
            confidence = random.uniform(0.90, 0.98)
        elif qa['quality'] == 'very_good':
            confidence = random.uniform(0.75, 0.90)
        elif qa['quality'] == 'good':
            confidence = random.uniform(0.60, 0.75)
        else:  # acceptable
            confidence = random.uniform(0.45, 0.60)
        
        # Random timestamp within the past 7 days
        timestamp = start_time + timedelta(
            days=random.randint(0, 6),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        # Log response
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'question': qa['question'],
            'answer': qa['answer'],
            'response_time': response_time,
            'source': qa['source'],
            'confidence': confidence
        }
        evaluator.response_logs.append(log_entry)
    
    # Generate 30 feedback entries with realistic distribution
    # Higher quality answers get more likes
    for i in range(30):
        qa = random.choice(qa_pairs)
        
        # Better quality = more likely to be liked
        if qa['quality'] in ['perfect', 'very_good']:
            feedback_type = 'like' if random.random() < 0.75 else 'dislike'
        elif qa['quality'] == 'good':
            feedback_type = 'like' if random.random() < 0.55 else 'dislike'
        else:  # acceptable
            feedback_type = 'like' if random.random() < 0.35 else 'dislike'
        
        # Random timestamp
        timestamp = start_time + timedelta(
            days=random.randint(0, 6),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        feedback_entry = {
            'timestamp': timestamp.isoformat(),
            'question': qa['question'],
            'answer': qa['answer'],
            'feedback': feedback_type
        }
        evaluator.feedback_data.append(feedback_entry)
    
    # Save data
    evaluator._save_response_logs()
    with open('user_feedback_data.json', 'w', encoding='utf-8') as f:
        json.dump(evaluator.feedback_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(evaluator.response_logs)} response logs with varied quality")
    print(f"✅ Generated {len(evaluator.feedback_data)} feedback entries")
    
    # Calculate expected metrics distribution
    likes = sum(1 for f in evaluator.feedback_data if f.get('feedback') == 'like')
    dislikes = len(evaluator.feedback_data) - likes
    satisfaction = (likes / len(evaluator.feedback_data) * 100)
    
    print(f"\n📊 Expected Results:")
    print(f"   Satisfaction Rate: ~{satisfaction:.1f}%")
    print(f"   Model Accuracy: 60-80% (mixed quality answers)")
    print(f"   BLEU Score: 40-70% (varied matches)")
    print(f"   Semantic Similarity: 55-75% (similar meanings)")
    
    # Ground truth remains the same
    ground_truth = [
        {
            "question": "What is the tuition fee for CSE?",
            "answer": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10."
        },
        {
            "question": "What are the admission requirements?",
            "answer": "Minimum GPA of 3.5 in SSC and HSC combined is required for admission."
        },
        {
            "question": "What is the address of the university?",
            "answer": "66 Mohakhali, Dhaka-1212, Bangladesh"
        },
        {
            "question": "What is the duration of the CSE program?",
            "answer": "4 years undergraduate program"
        },
        {
            "question": "How can I contact the admissions office?",
            "answer": "Contact: admissions@university.edu or +880-2-123456"
        }
    ]
    
    import os
    os.makedirs('dataset', exist_ok=True)
    with open('dataset/ground_truth.json', 'w', encoding='utf-8') as f:
        json.dump(ground_truth, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Ground truth dataset maintained with {len(ground_truth)} entries")
    print("\n🎉 Realistic demo data generation complete!")
    print("\n📊 Now run: python research_analysis.py")
    print("   Metrics will show realistic scores (NOT all 100%)!\n")

if __name__ == '__main__':
    generate_realistic_demo_data()
