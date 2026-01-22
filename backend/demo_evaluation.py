"""
Quick Start - Research Evaluation Demo
=======================================
This script demonstrates the evaluation system with sample data
"""

import json
import random
from datetime import datetime, timedelta
from evaluation_analytics import ChatbotEvaluator
import time

def generate_sample_data():
    """Generate sample response logs for demonstration"""
    print("📝 Generating sample data...")
    
    questions = [
        "What is the tuition fee for CSE?",
        "How long is the CSE program?",
        "What are the admission requirements?",
        "What programs does Green University offer?",
        "How can I get a scholarship?",
        "What is the BBA program fee?",
        "What facilities does the university have?",
        "When does admission start?",
        "What is the fee for EEE department?",
        "What is the textile engineering fee?"
    ]
    
    answers = [
        "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10 (All A+).",
        "The BSc in CSE is a 4-year undergraduate program consisting of 8 semesters.",
        "Admission requires minimum GPA in SSC and HSC, performance in admission test, and English proficiency.",
        "Green University offers CSE, EEE, BBA, Textile Engineering, English, Law, and more.",
        "Merit-based scholarships are available for top 5% students each semester based on GPA.",
        "The BBA program fee varies. Merit-based scholarships are available to reduce costs.",
        "The university has modern labs, computer facilities, library, sports facilities, and cafeteria.",
        "Please check the website or contact admission office at 01775234234 for admission dates.",
        "The EEE program fee varies. Merit-based scholarships are available for top performers.",
        "The Textile Engineering fee is BDT 70,000 per semester."
    ]
    
    sources = ['dataset', 'llm', 'rag', 'dataset_formatted']
    
    logs = []
    for i in range(50):
        idx = i % len(questions)
        
        # Generate timestamp
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        log = {
            'timestamp': timestamp.isoformat(),
            'question': questions[idx],
            'answer': answers[idx],
            'response_time': random.uniform(0.5, 5.0),
            'source': random.choice(sources),
            'confidence': random.uniform(0.5, 0.95) if random.random() > 0.2 else random.uniform(0.2, 0.5)
        }
        logs.append(log)
    
    # Save logs
    with open('response_logs.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated {len(logs)} sample response logs")
    return logs

def demo_live_stats():
    """Demonstrate live statistics"""
    print("\n" + "="*80)
    print("📊 LIVE STATISTICS DEMO")
    print("="*80)
    
    evaluator = ChatbotEvaluator()
    
    # Response time stats
    rt_stats = evaluator.calculate_response_time_statistics()
    
    print(f"\n⚡ Response Time Performance:")
    print(f"   Total Responses: {rt_stats.get('total_responses', 0)}")
    print(f"   Average Time: {rt_stats.get('average_response_time', 0):.3f}s")
    print(f"   Median Time: {rt_stats.get('median_response_time', 0):.3f}s")
    print(f"   95th Percentile: {rt_stats.get('percentiles', {}).get('p95', 0):.3f}s")
    
    if 'distribution' in rt_stats:
        print(f"\n⏱️ Response Time Distribution:")
        for range_name, count in rt_stats['distribution'].items():
            print(f"   {range_name}: {count}")
    
    if 'by_source' in rt_stats:
        print(f"\n🔍 Performance by Source:")
        for source, stats in rt_stats['by_source'].items():
            print(f"   {source}: {stats['average']:.3f}s avg ({stats['count']} requests)")

def demo_accuracy_evaluation():
    """Demonstrate accuracy evaluation"""
    print("\n" + "="*80)
    print("🎯 ACCURACY EVALUATION DEMO")
    print("="*80)
    
    evaluator = ChatbotEvaluator()
    
    # Example evaluation
    question = "What is the tuition fee for CSE?"
    generated = "The tuition fee for Computer Science and Engineering (CSE) is Tk. 589,900."
    reference = "The tuition fee for the Computer Science and Engineering (CSE) program at Green University of Bangladesh varies based on academic performance. For students with a combined GPA of 10 (All A+), the fee is Tk. 589,900."
    
    result = evaluator.evaluate_answer_accuracy(question, generated, reference)
    
    print(f"\n📝 Question: {question}")
    print(f"\n✅ Evaluation Results:")
    print(f"   Overall Accuracy: {result['overall_accuracy']*100:.2f}%")
    print(f"   Grade: {result['accuracy_grade']}")
    print(f"   Semantic Similarity: {result['semantic_similarity']:.3f}")
    print(f"   BLEU Score: {result['bleu_score']:.3f}")
    print(f"   Precision: {result['precision']:.3f}")
    print(f"   Recall: {result['recall']:.3f}")
    print(f"   F1 Score: {result['f1_score']:.3f}")
    
    if result['matched_keywords']:
        print(f"   Matched Keywords: {', '.join(result['matched_keywords'][:5])}")

def demo_feedback_analysis():
    """Demonstrate feedback analysis"""
    print("\n" + "="*80)
    print("😊 USER FEEDBACK ANALYSIS DEMO")
    print("="*80)
    
    evaluator = ChatbotEvaluator()
    feedback_stats = evaluator.analyze_user_feedback()
    
    if 'total_feedback' in feedback_stats:
        print(f"\n👥 Feedback Summary:")
        print(f"   Total Feedback: {feedback_stats['total_feedback']}")
        print(f"   Likes: {feedback_stats['likes']} 👍")
        print(f"   Dislikes: {feedback_stats['dislikes']} 👎")
        print(f"   Satisfaction Rate: {feedback_stats['satisfaction_rate']:.2f}%")
        
        ratio = feedback_stats['like_dislike_ratio']
        if ratio != float('inf'):
            print(f"   Like/Dislike Ratio: {ratio:.2f}")
    else:
        print("\n⚠️ No feedback data available")
        print("   Feedback will be collected as users interact with the chatbot")

def demo_full_report():
    """Generate and display full report"""
    print("\n" + "="*80)
    print("📊 GENERATING COMPREHENSIVE RESEARCH REPORT")
    print("="*80)
    
    evaluator = ChatbotEvaluator()
    report = evaluator.generate_research_report('demo_research_report.json')
    
    print("\n✅ Report generated successfully!")
    print(f"   File: demo_research_report.json")
    
    # Display summary
    if 'summary' in report:
        summary = report['summary']
        
        if 'response_time' in summary:
            print(f"\n⚡ Response Time Summary:")
            print(f"   Average: {summary['response_time']['average']}")
            print(f"   Performance: {summary['response_time']['performance_grade']}")
            print(f"   Consistency: {summary['response_time']['consistency']}")
        
        if 'user_satisfaction' in summary:
            print(f"\n😊 User Satisfaction Summary:")
            print(f"   Satisfaction Rate: {summary['user_satisfaction']['satisfaction_rate']}")
            print(f"   Grade: {summary['user_satisfaction']['grade']}")

def main():
    """Main demo function"""
    print("\n" + "="*100)
    print(" " * 30 + "RESEARCH EVALUATION SYSTEM - DEMO")
    print("="*100)
    print("\n🚀 This demo will showcase the evaluation system capabilities\n")
    
    # Step 1: Generate sample data
    print("Step 1: Generating Sample Data")
    print("-"*80)
    generate_sample_data()
    
    time.sleep(1)
    
    # Step 2: Live statistics
    print("\nStep 2: Live Statistics")
    print("-"*80)
    demo_live_stats()
    
    time.sleep(1)
    
    # Step 3: Accuracy evaluation
    print("\nStep 3: Accuracy Evaluation")
    print("-"*80)
    demo_accuracy_evaluation()
    
    time.sleep(1)
    
    # Step 4: Feedback analysis
    print("\nStep 4: Feedback Analysis")
    print("-"*80)
    demo_feedback_analysis()
    
    time.sleep(1)
    
    # Step 5: Full report
    print("\nStep 5: Full Research Report")
    print("-"*80)
    demo_full_report()
    
    # Final summary
    print("\n" + "="*100)
    print(" " * 35 + "DEMO COMPLETE")
    print("="*100)
    print("\n📁 Generated Files:")
    print("   • response_logs.json - Sample response data")
    print("   • demo_research_report.json - Comprehensive analysis")
    print("\n💡 Next Steps:")
    print("   1. Run 'python research_analysis.py' for full analysis")
    print("   2. Start the server with 'python simple_rag_server.py'")
    print("   3. Access analytics at http://localhost:5000/analytics/live")
    print("   4. Review RESEARCH_EVALUATION_GUIDE.md for details")
    print("\n" + "="*100 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
