# Research & Evaluation System Documentation

## Overview
This system provides comprehensive LLM model accuracy evaluation and response time analysis for academic research purposes.

## 🎯 Key Features

### 1. **LLM Model Accuracy Evaluation**
   - **Semantic Similarity Analysis**: TF-IDF and cosine similarity
   - **BLEU Score Calculation**: Standard metric for NLG evaluation
   - **Keyword F1 Score**: Precision, recall, and F1 for keyword matching
   - **Overall Accuracy Score**: Weighted combination of metrics
   - **Grade Classification**: A+ to F grading system

### 2. **Response Time Analysis**
   - **Average Response Time**: Mean, median, min, max
   - **Percentile Analysis**: P50, P75, P90, P95, P99
   - **Distribution Analysis**: Response time buckets
   - **Source Comparison**: Dataset vs LLM vs RAG performance
   - **Temporal Trends**: Performance over time

### 3. **User Feedback Analysis**
   - **Satisfaction Rate**: Like/dislike ratio
   - **Topic Analysis**: Most liked/disliked topics
   - **Timeline Trends**: Feedback patterns over time
   - **Engagement Metrics**: Total interactions and feedback count

### 4. **Research Export**
   - **JSON Reports**: Comprehensive structured data
   - **CSV Export**: For Excel, SPSS, R analysis
   - **Statistical Summaries**: Ready for publication

## 📦 Installation

### Prerequisites
Ensure you have Python 3.8+ installed.

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt

# Download NLTK data (required for BLEU scores)
python -c "import nltk; nltk.download('punkt')"
```

## 🚀 Usage

### Method 1: Automatic Tracking (Recommended)
The system automatically tracks all chatbot interactions when using the integrated server:

```bash
# Start the server with evaluation enabled
python simple_rag_server.py
```

All responses are automatically logged with:
- Response time
- Question and answer
- Confidence score
- Source (dataset/llm/rag)

### Method 2: Manual Analysis
Run comprehensive research analysis on collected data:

```bash
# Generate full research report
python research_analysis.py
```

This will:
1. Analyze all response times
2. Calculate accuracy metrics
3. Process user feedback
4. Generate JSON report
5. Export CSV files

### Method 3: API Endpoints
Access real-time analytics via REST API:

```bash
# Start server
python simple_rag_server.py

# Then access:
# http://localhost:5000/analytics/live          - Live statistics
# http://localhost:5000/analytics/report        - Full report
# http://localhost:5000/analytics/export        - Export CSV
```

### Method 4: Programmatic Access
Use the evaluation system in your code:

```python
from evaluation_analytics import ChatbotEvaluator

# Initialize
evaluator = ChatbotEvaluator()

# Log a response
evaluator.log_response(
    question="What is the CSE fee?",
    answer="The fee is Tk. 589,900",
    response_time=1.234,
    source='dataset',
    confidence=0.85
)

# Get statistics
rt_stats = evaluator.calculate_response_time_statistics()
accuracy = evaluator.batch_evaluate_accuracy()
feedback = evaluator.analyze_user_feedback()

# Generate report
report = evaluator.generate_research_report('my_report.json')
```

## 📊 Metrics Explanation

### Accuracy Metrics

#### 1. **Semantic Similarity (0-1)**
Measures how similar the generated answer is to the reference answer using TF-IDF vectorization and cosine similarity.
- **1.0**: Perfect semantic match
- **0.7-0.9**: Very similar meaning
- **0.5-0.7**: Somewhat similar
- **<0.5**: Different meaning

#### 2. **BLEU Score (0-1)**
Standard metric for evaluating machine-generated text against reference text.
- **>0.8**: Excellent quality
- **0.6-0.8**: Good quality
- **0.4-0.6**: Acceptable
- **<0.4**: Poor quality

#### 3. **F1 Score (0-1)**
Harmonic mean of precision and recall for keyword matching.
- **Precision**: % of generated keywords that are correct
- **Recall**: % of reference keywords that were generated
- **F1**: Balanced score

#### 4. **Overall Accuracy (0-1)**
Weighted combination:
```
Overall = (Semantic * 0.4) + (BLEU * 0.3) + (F1 * 0.3)
```

### Grading System
- **A+ (90-100%)**: Excellent
- **A (80-89%)**: Very Good
- **B (70-79%)**: Good
- **C (60-69%)**: Acceptable
- **D (50-59%)**: Poor
- **F (<50%)**: Very Poor

## 📈 Research Report Structure

The generated JSON report includes:

```json
{
  "report_generated": "timestamp",
  "data_period": {
    "start": "first_interaction",
    "end": "last_interaction"
  },
  "accuracy_evaluation": {
    "total_evaluated": 100,
    "overall_metrics": {
      "mean_accuracy": 0.85,
      "median_accuracy": 0.87,
      "std_accuracy": 0.12,
      "min_accuracy": 0.45,
      "max_accuracy": 0.98
    },
    "semantic_similarity": {...},
    "bleu_score": {...},
    "f1_score": {...},
    "grade_distribution": {...}
  },
  "response_time_analysis": {
    "total_responses": 500,
    "average_response_time": 2.34,
    "median_response_time": 1.89,
    "percentiles": {...},
    "distribution": {...},
    "by_source": {...}
  },
  "user_feedback_analysis": {
    "total_feedback": 150,
    "likes": 120,
    "dislikes": 30,
    "satisfaction_rate": 80.0,
    "like_dislike_ratio": 4.0
  },
  "summary": {
    "accuracy": {...},
    "response_time": {...},
    "user_satisfaction": {...}
  }
}
```

## 📁 Output Files

### Generated Files
1. **response_logs.json** - All chatbot interactions with timing
2. **research_report_YYYYMMDD_HHMMSS.json** - Comprehensive analysis
3. **research_exports_YYYYMMDD_HHMMSS/**
   - response_logs.csv
   - feedback_data.csv

### CSV Format for Excel/SPSS

**response_logs.csv:**
```csv
timestamp,question,answer,response_time,source,confidence
2026-01-16T10:30:00,What is CSE fee?,The fee is...,1.234,dataset,0.85
```

**feedback_data.csv:**
```csv
timestamp,question,answer,feedback
2026-01-16T10:35:00,What is CSE fee?,The fee is...,like
```

## 🔬 Research Applications

### 1. Response Time Analysis
- **Hypothesis Testing**: Compare response times between methods
- **Performance Optimization**: Identify bottlenecks
- **Reliability Studies**: Use percentile data

### 2. Accuracy Evaluation
- **Model Comparison**: Compare different LLM models
- **RAG Effectiveness**: Measure impact of retrieval
- **Quality Assurance**: Monitor answer quality

### 3. User Satisfaction Studies
- **UX Research**: Understand user preferences
- **A/B Testing**: Compare different approaches
- **Feedback Analysis**: Identify improvement areas

### 4. Statistical Analysis
Use exported CSV data for:
- **T-tests**: Compare means between groups
- **ANOVA**: Multiple group comparison
- **Correlation**: Relationship between metrics
- **Regression**: Predict satisfaction from metrics

## 📚 Example Research Workflow

### Step 1: Data Collection
```bash
# Run your chatbot with evaluation enabled
python simple_rag_server.py
```

### Step 2: Generate Analysis
```bash
# After collecting data (e.g., 100+ interactions)
python research_analysis.py
```

### Step 3: Statistical Analysis
```bash
# Open in Excel or import to SPSS/R
# Files in: research_exports_YYYYMMDD_HHMMSS/
```

### Step 4: Create Visualizations
- Box plots for response times
- Bar charts for accuracy distribution
- Line charts for trends
- Scatter plots for correlations

### Step 5: Report Findings
Use the metrics in your research paper:
```
"The system achieved a mean response time of 2.34s (SD=1.12) 
with a 95th percentile of 4.56s. Model accuracy averaged 85.3% 
(BLEU=0.78, Semantic Similarity=0.82) with user satisfaction 
rate of 80%."
```

## 🎓 Academic Citation Format

### APA Style
```
[Your Name]. (2026). LLM Model Evaluation and Response Time Analysis 
for RAG-Based Chatbot Systems. Green University Research Report.
```

### Metrics to Report
1. **Response Time**: Mean, SD, Median, P95
2. **Accuracy**: Mean, SD, by metric type
3. **Satisfaction**: Rate, ratio, trends
4. **Sample Size**: Total interactions, evaluation set size
5. **Time Period**: Data collection dates

## 🐛 Troubleshooting

### Issue: No data in reports
**Solution**: Ensure the server is logging interactions:
```python
from evaluation_middleware import log_chat_interaction
log_chat_interaction(question, answer, response_time, source)
```

### Issue: NLTK punkt not found
**Solution**: Download NLTK data:
```python
import nltk
nltk.download('punkt')
```

### Issue: Ground truth not loading
**Solution**: Create `dataset/ground_truth.json`:
```json
[
  {"question": "...", "answer": "..."}
]
```

### Issue: CSV encoding errors
**Solution**: Use UTF-8 encoding when opening CSVs:
```python
pd.read_csv('file.csv', encoding='utf-8')
```

## 🔧 Configuration

### Customize Accuracy Weights
Edit `evaluation_analytics.py`:
```python
overall_accuracy = (
    semantic_sim * 0.4 +      # Adjust weight
    bleu * 0.3 +              # Adjust weight
    keyword_metrics['f1_score'] * 0.3  # Adjust weight
)
```

### Customize Grading Thresholds
```python
def _grade_accuracy(self, score: float) -> str:
    if score >= 0.9:    # Change threshold
        return 'A+ (Excellent)'
    # ... etc
```

## 📞 Support

For research support or questions:
1. Check the code documentation
2. Review example outputs
3. Consult academic papers on chatbot evaluation
4. Refer to BLEU score and cosine similarity literature

## 📄 License

This evaluation system is part of the Green University Help Desk AI project.

## 🙏 Acknowledgments

Built using:
- NLTK for natural language processing
- scikit-learn for ML metrics
- Flask for API integration
- pandas for data export

---

**Good luck with your research! 🎓📊**
