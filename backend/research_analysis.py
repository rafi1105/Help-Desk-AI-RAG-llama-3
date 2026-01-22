"""
Research Analysis Script
========================
Standalone script to analyze chatbot performance for research purposes

Usage:
    python research_analysis.py
    
This script will:
1. Load all response logs and feedback data
2. Calculate accuracy metrics
3. Analyze response times
4. Generate comprehensive research reports
5. Export data to CSV for Excel/SPSS analysis
"""

import sys
import os

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from evaluation_analytics import ChatbotEvaluator
from datetime import datetime
import json

# Import visualization module
try:
    from research_visualization import ResearchVisualizer
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("⚠️ Visualization module not available. Install: pip install matplotlib seaborn")


def print_banner():
    """Print banner"""
    print("\n" + "="*100)
    print(" " * 30 + "CHATBOT RESEARCH ANALYSIS SYSTEM")
    print("="*100)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*100 + "\n")

def print_section(title):
    """Print section header"""
    print("\n" + "-"*100)
    print(f"📊 {title}")
    print("-"*100)

def main():
    """Main research analysis function"""
    print_banner()
    
    # Initialize evaluator
    print("🔧 Initializing evaluation system...")
    evaluator = ChatbotEvaluator(
        response_log_file='response_logs.json',
        feedback_file='user_feedback_data.json',
        ground_truth_file='dataset/ground_truth.json'
    )
    print(f"✅ Loaded {len(evaluator.response_logs)} response logs")
    print(f"✅ Loaded {len(evaluator.feedback_data)} feedback entries")
    
    # ============================================================================
    # 1. RESPONSE TIME ANALYSIS
    # ============================================================================
    print_section("RESPONSE TIME ANALYSIS")
    
    rt_stats = evaluator.calculate_response_time_statistics()
    
    if 'average_response_time' in rt_stats:
        print(f"\n📈 Overall Statistics:")
        print(f"   Total Responses: {rt_stats['total_responses']}")
        print(f"   Average Response Time: {rt_stats['average_response_time']:.3f}s")
        print(f"   Median Response Time: {rt_stats['median_response_time']:.3f}s")
        print(f"   Min Response Time: {rt_stats['min_response_time']:.3f}s")
        print(f"   Max Response Time: {rt_stats['max_response_time']:.3f}s")
        print(f"   Standard Deviation: {rt_stats['std_deviation']:.3f}s")
        
        print(f"\n📊 Percentile Analysis:")
        for p, value in rt_stats['percentiles'].items():
            print(f"   {p}: {value:.3f}s")
        
        print(f"\n⏱️ Response Time Distribution:")
        dist = rt_stats['distribution']
        total = sum(dist.values())
        for range_name, count in dist.items():
            percentage = (count/total)*100 if total > 0 else 0
            print(f"   {range_name}: {count} ({percentage:.1f}%)")
        
        print(f"\n🔍 Performance by Source:")
        for source, stats in rt_stats['by_source'].items():
            print(f"   {source}:")
            print(f"      Count: {stats['count']}")
            print(f"      Average: {stats['average']:.3f}s")
            print(f"      Median: {stats['median']:.3f}s")
    else:
        print("⚠️ No response time data available")
    
    # ============================================================================
    # 2. ACCURACY EVALUATION
    # ============================================================================
    print_section("MODEL ACCURACY EVALUATION")
    
    # Note: This requires ground truth data
    print("\n⚠️ Note: Accuracy evaluation requires ground truth dataset")
    print("   Create 'dataset/ground_truth.json' with format:")
    print('   [{"question": "...", "answer": "..."}]')
    
    if evaluator.ground_truth:
        print(f"\n✅ Found {len(evaluator.ground_truth)} ground truth entries")
        
        acc_eval = evaluator.batch_evaluate_accuracy(limit=50)  # Evaluate last 50
        
        if 'overall_metrics' in acc_eval:
            metrics = acc_eval['overall_metrics']
            print(f"\n📊 Overall Accuracy Metrics:")
            print(f"   Evaluated Responses: {acc_eval['total_evaluated']}")
            print(f"   Mean Accuracy: {metrics['mean_accuracy']*100:.2f}%")
            print(f"   Median Accuracy: {metrics['median_accuracy']*100:.2f}%")
            print(f"   Min Accuracy: {metrics['min_accuracy']*100:.2f}%")
            print(f"   Max Accuracy: {metrics['max_accuracy']*100:.2f}%")
            print(f"   Std Deviation: {metrics['std_accuracy']*100:.2f}%")
            
            print(f"\n🎯 Detailed Metrics:")
            print(f"   Semantic Similarity: {acc_eval['semantic_similarity']['mean']:.3f}")
            print(f"   BLEU Score: {acc_eval['bleu_score']['mean']:.3f}")
            print(f"   F1 Score: {acc_eval['f1_score']['mean']:.3f}")
            
            print(f"\n📈 Grade Distribution:")
            for grade, count in acc_eval['grade_distribution'].items():
                percentage = (count/acc_eval['total_evaluated'])*100
                print(f"   {grade}: {count} ({percentage:.1f}%)")
    else:
        print("\n❌ No ground truth data found")
        print("   Accuracy evaluation requires a ground truth dataset")
    
    # ============================================================================
    # 3. USER FEEDBACK ANALYSIS
    # ============================================================================
    print_section("USER FEEDBACK ANALYSIS")
    
    feedback_stats = evaluator.analyze_user_feedback()
    
    if 'total_feedback' in feedback_stats:
        print(f"\n👥 Feedback Summary:")
        print(f"   Total Feedback: {feedback_stats['total_feedback']}")
        print(f"   Likes: {feedback_stats['likes']} 👍")
        print(f"   Dislikes: {feedback_stats['dislikes']} 👎")
        print(f"   Satisfaction Rate: {feedback_stats['satisfaction_rate']:.2f}%")
        
        ratio = feedback_stats['like_dislike_ratio']
        print(f"   Like/Dislike Ratio: {ratio:.2f}" if ratio != float('inf') else "   Like/Dislike Ratio: All Likes")
        
        if feedback_stats.get('most_liked_topics'):
            print(f"\n✅ Most Liked Topics:")
            for topic in feedback_stats['most_liked_topics'][:5]:
                print(f"   • {topic['topic']}: {topic['count']} occurrences")
        
        if feedback_stats.get('most_disliked_topics'):
            print(f"\n❌ Most Disliked Topics:")
            for topic in feedback_stats['most_disliked_topics'][:5]:
                print(f"   • {topic['topic']}: {topic['count']} occurrences")
    else:
        print("⚠️ No feedback data available")
    
    # ============================================================================
    # 4. GENERATE COMPREHENSIVE REPORT
    # ============================================================================
    print_section("GENERATING COMPREHENSIVE RESEARCH REPORT")
    
    # Create timestamped folder for this research session
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_folder = f"research_reports_{timestamp}"
    os.makedirs(report_folder, exist_ok=True)
    
    report_file = os.path.join(report_folder, f"research_report_{timestamp}.json")
    report = evaluator.generate_research_report(report_file)
    
    print(f"\n✅ Comprehensive report generated: {report_file}")
    
    # ============================================================================
    # 5. EXPORT TO CSV
    # ============================================================================
    print_section("EXPORTING DATA TO CSV")
    
    export_dir = os.path.join(report_folder, "csv_exports")
    evaluator.export_to_csv(export_dir)
    
    print(f"\n✅ Data exported to: {export_dir}/")
    print(f"   Files:")
    print(f"   • response_logs.csv - All chatbot interactions with timing")
    print(f"   • feedback_data.csv - User feedback data")
    print(f"\n📁 All research files saved to: {report_folder}/")
    
    # ============================================================================
    # 6. GENERATE VISUALIZATIONS
    # ============================================================================
    print_section("GENERATING VISUALIZATIONS")
    
    try:
        # Prepare evaluation data for visualization
        viz_evaluation_data = {}
        if evaluator.ground_truth:
            acc_eval = evaluator.batch_evaluate_accuracy(limit=None)  # All data
            viz_evaluation_data = acc_eval
        
        viz_dir = os.path.join(report_folder, "visualizations")
        visualizer = ResearchVisualizer(evaluation_data=viz_evaluation_data)
        visualizer.generate_all_visualizations(viz_dir)
        print(f"\n✅ Visualizations saved to: {viz_dir}/")
        print(f"🌐 Open report: {viz_dir}/index.html")
    except Exception as e:
        print(f"⚠️ Visualization generation failed: {e}")
        print("   Install matplotlib and seaborn: pip install matplotlib seaborn")
    
    # ============================================================================
    # 7. RECOMMENDATIONS FOR RESEARCH
    # ============================================================================
    print_section("RESEARCH RECOMMENDATIONS")
    
    print("""
📝 For Your Research Paper:

1. **Response Time Analysis:**
   - Use the percentile data (p50, p90, p95) to show system reliability
   - Compare response times by source (dataset vs LLM)
   - Create charts showing response time distribution
   
2. **Model Accuracy:**
   - Report mean, median, and standard deviation of accuracy scores
   - Show BLEU scores and semantic similarity metrics
   - Create confusion matrices if applicable
   
3. **User Satisfaction:**
   - Report satisfaction rate and like/dislike ratio
   - Analyze trends over time using timeline data
   - Identify problem areas from disliked topics
   
4. **Statistical Analysis:**
   - All data exported to CSV for SPSS/Excel analysis
   - Perform t-tests, ANOVA on response times
   - Correlation analysis between confidence and satisfaction
   
5. **Visualization Recommendations:**
   - Box plots for response time distribution
   - Line charts for performance trends
   - Bar charts for accuracy grade distribution
   - Pie charts for user satisfaction breakdown
    """)
    
    # ============================================================================
    # SUMMARY
    # ============================================================================
    print("\n" + "="*100)
    print(" " * 35 + "✅ ANALYSIS COMPLETE")
    print("="*100)
    
    print(f"\n📁 Generated Files:")
    print(f"   • {report_file}")
    print(f"   • {export_dir}/response_logs.csv")
    print(f"   • {export_dir}/feedback_data.csv")
    
    # Show visualization link prominently
    viz_html = os.path.join(report_folder, "visualizations", "index.html")
    if os.path.exists(viz_html):
        print(f"\n📊 VISUALIZATIONS:")
        print(f"   • Location: {os.path.join(report_folder, 'visualizations')}/")
        print(f"   • 🌐 HTML Report: {viz_html}")
        print(f"\n   👉 OPEN IN BROWSER: {viz_html}")
    
    print(f"\n📂 All files saved in: {report_folder}/")
    
    print("\n💡 Next Steps:")
    print("   1. ✅ Open the HTML visualization report in your browser")
    print("   2. 📊 Review all 10 interactive charts and graphs")
    print("   3. 📈 Open CSV files in Excel or SPSS for statistical analysis")
    print("   4. 📄 Review the JSON report for detailed metrics")
    print("   5. 📝 Include the metrics and visualizations in your research paper")
    
    # Ask user if they want to open the HTML report
    if os.path.exists(viz_html):
        print("\n" + "="*100)
        try:
            response = input("\n🌐 Would you like to open the HTML report in your browser now? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                import webbrowser
                import urllib.request
                from pathlib import Path
                file_url = Path(viz_html).as_uri()
                webbrowser.open(file_url)
                print(f"\n✅ Opening {viz_html} in your default browser...")
        except:
            pass  # If input fails, just skip
    
    print("\n" + "="*100 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Analysis interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
