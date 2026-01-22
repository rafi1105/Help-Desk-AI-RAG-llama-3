"""
Test BLEU Score Calculation
"""
from evaluation_analytics import ChatbotEvaluator

def test_bleu_examples():
    """Test BLEU with different examples"""
    
    print("="*80)
    print("BLEU SCORE TESTING (Using Fixed Implementation)")
    print("="*80)
    
    evaluator = ChatbotEvaluator()
    
    test_cases = [
        {
            "name": "Exact Match",
            "reference": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "hypothesis": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10."
        },
        {
            "name": "Extra Words (Ground Truth vs Demo)",
            "reference": "66 Mohakhali, Dhaka-1212, Bangladesh",
            "hypothesis": "The university is located at 66 Mohakhali, Dhaka-1212, Bangladesh."
        },
        {
            "name": "Similar Meaning",
            "reference": "Minimum GPA of 3.5 in SSC and HSC combined is required for admission.",
            "hypothesis": "Admission requirements include minimum GPA of 3.5 in SSC and HSC combined."
        },
        {
            "name": "Short Answer",
            "reference": "4 years undergraduate program",
            "hypothesis": "The CSE program is a 4-year undergraduate degree program."
        },
        {
            "name": "Contact Info",
            "reference": "Contact: admissions@university.edu or +880-2-123456",
            "hypothesis": "You can contact admissions at admissions@university.edu or call +880-2-123456."
        },
        {
            "name": "Tuition Fee (Actual Demo Data)",
            "reference": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10.",
            "hypothesis": "The tuition fee for CSE is Tk. 589,900 for students with combined GPA 10 (All A+)."
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{i}. {test['name']}")
        print("-" * 80)
        print(f"Reference : {test['reference']}")
        print(f"Hypothesis: {test['hypothesis']}")
        
        # Calculate BLEU using the fixed method
        score = evaluator.calculate_bleu_score(test['reference'], test['hypothesis'])
        
        print(f"\n✓ BLEU Score: {score:.4f} ({score*100:.2f}%)")
        
        if score > 0.7:
            print("  Grade: Excellent")
        elif score > 0.5:
            print("  Grade: Good")
        elif score > 0.3:
            print("  Grade: Fair")
        else:
            print("  Grade: Poor")

if __name__ == '__main__':
    test_bleu_examples()
