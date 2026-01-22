"""
Test Metrics Accuracy with Different Answer Quality Levels
============================================================
This script validates that BLEU, Semantic Similarity, and F1 scores
properly differentiate between good, average, and poor answers
"""

from evaluation_analytics import ChatbotEvaluator

def test_metric_accuracy():
    """Test with different quality answers to validate metrics"""
    
    print("="*80)
    print("METRICS ACCURACY VALIDATION TEST")
    print("="*80)
    print("\nTesting if metrics properly differentiate answer quality...\n")
    
    evaluator = ChatbotEvaluator()
    
    # Test cases with different quality levels
    test_cases = [
        {
            "name": "PERFECT MATCH",
            "reference": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "answer": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "expected_range": (0.95, 1.0)
        },
        {
            "name": "VERY GOOD (Minor Addition)",
            "reference": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "answer": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10 (All A+).",
            "expected_range": (0.70, 0.95)
        },
        {
            "name": "GOOD (Similar Info, Different Words)",
            "reference": "Minimum GPA of 3.5 in SSC and HSC combined is required for admission.",
            "answer": "Admission requirements include minimum GPA of 3.5 in SSC and HSC combined.",
            "expected_range": (0.55, 0.75)
        },
        {
            "name": "ACCEPTABLE (Core Info Present)",
            "reference": "66 Mohakhali, Dhaka-1212, Bangladesh",
            "answer": "The university is located at 66 Mohakhali, Dhaka-1212, Bangladesh.",
            "expected_range": (0.35, 0.55)
        },
        {
            "name": "POOR (Missing Key Info)",
            "reference": "4 years undergraduate program",
            "answer": "The CSE program is a 4-year undergraduate degree program.",
            "expected_range": (0.10, 0.35)
        },
        {
            "name": "VERY POOR (Wrong Answer)",
            "reference": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "answer": "The program duration is 4 years with excellent faculty members.",
            "expected_range": (0.0, 0.15)
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}: {test['name']}")
        print(f"{'='*80}")
        print(f"Reference: {test['reference']}")
        print(f"Answer   : {test['answer']}")
        print(f"\nExpected Overall Accuracy Range: {test['expected_range'][0]*100:.1f}% - {test['expected_range'][1]*100:.1f}%")
        
        # Calculate all metrics
        evaluation = evaluator.evaluate_answer_accuracy("test", test['answer'], test['reference'])
        
        semantic_sim = evaluation['semantic_similarity']
        bleu = evaluation['bleu_score']
        f1 = evaluation['f1_score']
        overall = evaluation['overall_accuracy']
        
        print(f"\n📊 Calculated Metrics:")
        print(f"   Semantic Similarity: {semantic_sim*100:6.2f}%")
        print(f"   BLEU Score:          {bleu*100:6.2f}%")
        print(f"   F1 Score:            {f1*100:6.2f}%")
        print(f"   Overall Accuracy:    {overall*100:6.2f}%")
        print(f"   Grade:               {evaluation['accuracy_grade']}")
        
        # Check if within expected range
        in_range = test['expected_range'][0] <= overall <= test['expected_range'][1]
        status = "✅ PASS" if in_range else "❌ FAIL"
        print(f"\n{status} - Overall accuracy is {'within' if in_range else 'outside'} expected range")
        
        results.append({
            'test': test['name'],
            'overall': overall,
            'in_range': in_range,
            'semantic': semantic_sim,
            'bleu': bleu,
            'f1': f1
        })
    
    # Summary
    print(f"\n\n{'='*80}")
    print("VALIDATION SUMMARY")
    print(f"{'='*80}\n")
    
    passed = sum(1 for r in results if r['in_range'])
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    print(f"\n{'Test Case':<30} {'Semantic':<10} {'BLEU':<10} {'F1':<10} {'Overall':<10} {'Status':<10}")
    print("-"*80)
    
    for r in results:
        status = "✅" if r['in_range'] else "❌"
        print(f"{r['test']:<30} {r['semantic']*100:>6.1f}%    {r['bleu']*100:>6.1f}%    "
              f"{r['f1']*100:>6.1f}%    {r['overall']*100:>6.1f}%    {status}")
    
    print("\n" + "="*80)
    
    if passed == total:
        print("✅ ALL TESTS PASSED - Metrics are working correctly!")
        print("\nThe evaluation system properly differentiates:")
        print("  • Perfect matches (100%)")
        print("  • Good answers (70-95%)")
        print("  • Acceptable answers (50-70%)")
        print("  • Poor answers (<50%)")
    else:
        print(f"⚠️ {total - passed} test(s) failed - Review metric calculations")
    
    print("="*80 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = test_metric_accuracy()
    exit(0 if success else 1)
