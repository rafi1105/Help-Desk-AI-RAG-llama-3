"""
Populate Demo Data for Research Visualization
==============================================
Creates sample response logs and feedback data to demonstrate
the research visualization system with realistic metrics
"""

import json
import random
from datetime import datetime, timedelta
from evaluation_analytics import ChatbotEvaluator

def generate_demo_data():
    """Generate comprehensive demo data for testing visualizations"""
    
    print("🔧 Generating demo data for research visualization...")
    
    # Sample questions and answers (matching ground truth for better BLEU scores)
    qa_pairs = [
        {
            "question": "What is the tuition fee for CSE?",
            "answer": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "source": "dataset"
        },
        {
            "question": "What are the admission requirements?",
            "answer": "Minimum GPA of 3.5 in SSC and HSC combined is required for admission.",
            "source": "llm"
        },
        {
            "question": "What is the address of the university?",
            "answer": "66 Mohakhali, Dhaka-1212, Bangladesh",
            "source": "dataset"
        },
        {
            "question": "What is the duration of the CSE program?",
            "answer": "4 years undergraduate program",
            "source": "dataset"
        },
        {
            "question": "How can I contact the admissions office?",
            "answer": "Contact: admissions@university.edu or +880-2-123456",
            "source": "dataset"
        },
        {
            "question": "When is the next semester starting?",
            "answer": "The next semester starts in January 2026.",
            "source": "rag"
        },
        {
            "question": "What programs does the university offer?",
            "answer": "The university offers programs in CSE, EEE, BBA, Law, and Journalism.",
            "source": "llm"
        },
        {
            "question": "How do I apply for scholarships?",
            "answer": "Scholarship applications can be submitted through the student portal with required documents.",
            "source": "rag"
        },
        {
            "question": "Are there any hostel facilities?",
            "answer": "Yes, the university provides separate hostel facilities for male and female students.",
            "source": "llm"
        },
        {
            "question": "What is the student-faculty ratio?",
            "answer": "The student-faculty ratio is approximately 25:1.",
            "source": "rag"
        }
    ]
    
    # Initialize evaluator
    evaluator = ChatbotEvaluator()
    
    # Clear existing data
    evaluator.response_logs = []
    evaluator.feedback_data = []
    
    # Generate 50 response logs over the past 7 days
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
        
        # Random confidence score
        confidence = random.uniform(0.6, 0.95)
        
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
    
    # Generate 25 feedback entries (mixed likes/dislikes)
    for i in range(25):
        qa = random.choice(qa_pairs)
        
        # 60% likes, 40% dislikes for realistic satisfaction rate
        feedback_type = 'like' if random.random() < 0.6 else 'dislike'
        
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
    
    print(f"✅ Generated {len(evaluator.response_logs)} response logs")
    print(f"✅ Generated {len(evaluator.feedback_data)} feedback entries")
    
    # Create sample ground truth for accuracy evaluation
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
    
    print(f"✅ Created ground truth dataset with {len(ground_truth)} entries")
    print("\n🎉 Demo data generation complete!")
    print("\n📊 Now run: python research_analysis.py")
    print("   This will generate visualizations with real metrics!\n")

if __name__ == '__main__':
    generate_demo_data()
