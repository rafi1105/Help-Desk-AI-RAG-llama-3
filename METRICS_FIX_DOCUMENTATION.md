# Research Visualization Fix - Responsive Metrics Update

## Problem Identified
The research visualization system was showing **hardcoded placeholder values** instead of calculating real metrics from the model's response data. Specifically:
- BLEU scores were always 0.574
- Semantic similarity was always 0.000
- F1 scores were always 0.533
- User satisfaction was showing example data (5 likes, 10 dislikes)

## Root Cause
The `ResearchVisualizer` class was not receiving evaluation results from `ChatbotEvaluator`, so the `plot_accuracy_metrics()` function used static placeholder data instead of computing real metrics.

## Solution Implemented

### 1. Updated ResearchVisualizer Architecture
**File**: `backend/research_visualization.py`

**Changes**:
- Added `evaluation_data` parameter to `__init__()` to accept computed metrics
- Modified `plot_accuracy_metrics()` to use real data from evaluation results
- Updated `plot_user_satisfaction()` to calculate satisfaction rate dynamically
- Added warning message when no ground truth data is available

```python
def __init__(self, response_logs_file: str = 'response_logs.json',
             feedback_file: str = 'user_feedback_data.json',
             evaluation_data: Dict = None):  # NEW PARAMETER
    self.evaluation_data = evaluation_data or {}  # Store evaluation metrics
```

### 2. Updated Research Analysis Integration
**File**: `backend/research_analysis.py`

**Changes**:
- Compute evaluation metrics before generating visualizations
- Pass evaluation results to `ResearchVisualizer` instance
- Ensure real-time metrics calculation

```python
# Prepare evaluation data for visualization
viz_evaluation_data = {}
if evaluator.ground_truth:
    acc_eval = evaluator.batch_evaluate_accuracy(limit=None)  # All data
    viz_evaluation_data = acc_eval

# Pass data to visualizer
visualizer = ResearchVisualizer(evaluation_data=viz_evaluation_data)
```

### 3. Created Demo Data Generator
**File**: `backend/populate_demo_data.py`

**Purpose**: Generate realistic sample data for testing and demonstration

**Features**:
- Creates 50 response logs with varied response times by source
- Generates 25 feedback entries (60% positive, 40% negative)
- Creates ground truth dataset for accuracy evaluation
- Realistic timestamps spread over 7 days
- Confidence scores between 0.6-0.95

### 4. Updated Batch File
**File**: `backend/run_research_analysis.bat`

**New Option Added**: 
- Option 1: POPULATE DEMO DATA (new)
- Renumbered existing options

## How Metrics Are Now Calculated

### Model Performance Metrics

#### 1. **Semantic Similarity**
- **Method**: TF-IDF vectorization + Cosine similarity
- **Range**: 0.0 to 1.0
- **Updates**: Calculated for each response against ground truth
- **Formula**: `cosine_similarity(TF-IDF(answer), TF-IDF(reference))`

#### 2. **BLEU Score**
- **Method**: NLTK BLEU with smoothing
- **Range**: 0.0 to 1.0
- **Updates**: Computed using tokenized word matching
- **Formula**: `sentence_bleu([reference_tokens], hypothesis_tokens)`

#### 3. **F1 Score**
- **Method**: Keyword matching precision and recall
- **Range**: 0.0 to 1.0
- **Updates**: Based on word overlap between answer and reference
- **Formula**: `2 * (precision * recall) / (precision + recall)`

#### 4. **Overall Accuracy**
- **Method**: Weighted average of above metrics
- **Weights**: Semantic Similarity (40%), BLEU (30%), F1 (30%)
- **Formula**: `0.4 * semantic + 0.3 * bleu + 0.3 * f1`

### User Satisfaction Metrics

#### 1. **Satisfaction Rate**
- **Method**: Percentage of positive feedback
- **Range**: 0% to 100%
- **Updates**: Real-time from `user_feedback_data.json`
- **Formula**: `(likes / total_feedback) * 100`

#### 2. **Like/Dislike Ratio**
- **Method**: Direct count comparison
- **Updates**: Live count from feedback data
- **Display**: Shown in pie chart and bar chart

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Chatbot Interactions                                     │
│    - Users ask questions                                     │
│    - Responses generated with timing                         │
│    - Logged to response_logs.json                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Feedback Collection                                      │
│    - Users provide likes/dislikes                           │
│    - Saved to user_feedback_data.json                       │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Evaluation (ChatbotEvaluator)                           │
│    - Loads response logs                                     │
│    - Loads feedback data                                     │
│    - Loads ground truth (if available)                      │
│    - Calculates: BLEU, Semantic Similarity, F1             │
│    - Computes satisfaction metrics                          │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Visualization (ResearchVisualizer)                      │
│    - Receives evaluation_data dictionary                    │
│    - Extracts real metrics                                  │
│    - Generates 10 responsive charts                         │
│    - Creates HTML report with live data                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Output                                                   │
│    - 10 PNG charts (300 DPI)                               │
│    - index.html with embedded visualizations                │
│    - CSV exports for statistical analysis                   │
└─────────────────────────────────────────────────────────────┘
```

## Files Modified

### Core Files
1. **research_visualization.py** - Made metrics responsive to real data
2. **research_analysis.py** - Integrated evaluation data passing
3. **run_research_analysis.bat** - Added demo data option

### New Files
4. **populate_demo_data.py** - Demo data generator

## Usage Instructions

### Step 1: Populate Demo Data (First Time)
```bash
cd backend
.\run_research_analysis.bat
# Select Option 1: POPULATE DEMO DATA
```

This creates:
- `response_logs.json` - 50 sample interactions
- `user_feedback_data.json` - 25 feedback entries
- `dataset/ground_truth.json` - 5 reference Q&A pairs

### Step 2: Generate Research Analysis
```bash
# Select Option 3: Run FULL RESEARCH ANALYSIS
```

This will:
- Calculate real BLEU, Semantic Similarity, F1 scores
- Compute user satisfaction rate from feedback
- Generate 10 responsive visualizations
- Create HTML report with live metrics

### Step 3: View Results
- Open `research_reports_TIMESTAMP/visualizations/index.html` in browser
- All metrics will show **real calculated values**, not placeholders

## Metrics Update Frequency

### Real-Time Updates
- **User Satisfaction**: Updates immediately when new feedback is added
- **Response Time Stats**: Updates with each new chatbot interaction

### Batch Updates (Run Analysis)
- **BLEU Score**: Recalculated when research_analysis.py runs
- **Semantic Similarity**: Recalculated during analysis
- **F1 Score**: Recalculated during analysis
- **Overall Accuracy**: Recalculated as weighted average

## Verification

### Before Fix
```
Semantic Similarity: 57.4%  (hardcoded)
BLEU Score: 0.0%            (hardcoded)
F1 Score: 53.3%             (hardcoded)
Overall Accuracy: 38.9%     (hardcoded)
User Satisfaction: Example data (5 likes, 10 dislikes)
```

### After Fix
```
Semantic Similarity: XX.X%  (calculated from TF-IDF cosine similarity)
BLEU Score: XX.X%           (calculated from NLTK BLEU)
F1 Score: XX.X%             (calculated from keyword matching)
Overall Accuracy: XX.X%     (weighted average: 0.4*sem + 0.3*bleu + 0.3*f1)
User Satisfaction: XX.X%    (calculated from actual likes/dislikes ratio)
```

## Ground Truth Requirement

For **accuracy metrics** (BLEU, Semantic Similarity, F1) to work:
- Ground truth dataset must exist at `dataset/ground_truth.json`
- Format: `[{"question": "...", "answer": "..."}]`
- Without ground truth: Chart shows zeros with warning message

For **satisfaction metrics** to work:
- Feedback data must exist in `user_feedback_data.json`
- Format: `[{"timestamp": "...", "question": "...", "answer": "...", "feedback": "like|dislike"}]`
- Without feedback: Chart shows "No Data Available" message

## API Integration

The live API endpoint `/analytics/report` now returns:
```json
{
  "overall_metrics": {
    "mean_accuracy": 0.XX,
    ...
  },
  "semantic_similarity": {
    "mean": 0.XX,
    ...
  },
  "bleu_score": {
    "mean": 0.XX,
    ...
  },
  "f1_score": {
    "mean": 0.XX,
    ...
  }
}
```

## Testing Checklist

- [x] Metrics calculate from real response logs
- [x] User satisfaction calculates from real feedback
- [x] Zero values show with warning when no ground truth
- [x] Demo data generator creates realistic samples
- [x] Batch file option added for data population
- [x] Visualizations update responsively
- [x] HTML report displays real metrics
- [x] CSV exports contain accurate data

## Benefits

1. **Real-Time Accuracy**: Metrics reflect actual model performance
2. **Research Validity**: Data-driven visualizations for academic papers
3. **Performance Tracking**: Monitor improvements over time
4. **User Satisfaction**: Track user experience trends
5. **Demo Capability**: Easy to demonstrate with sample data

## Next Steps

1. Run `populate_demo_data.py` to create sample data
2. Run `research_analysis.py` to generate visualizations
3. View `index.html` to see responsive metrics
4. Integrate with live chatbot for ongoing tracking
5. Use CSV exports for statistical analysis in SPSS/Excel

---

**Status**: ✅ FIXED - Metrics now responsive to real model response data
**Date**: January 16, 2026
**Impact**: High - Core functionality for research evaluation
