# Research Data Visualization Guide

## 📊 Overview
The research visualization system generates publication-quality graphs and charts for your academic research. All visualizations are automatically created when you run the research analysis.

## 🎨 Available Visualizations

### 1. **Response Time Timeline** ⏰
- **Type**: Line chart with trend analysis
- **Shows**: Response times over the data collection period
- **Features**:
  - Individual data points with markers
  - Polynomial trend line (red dashed)
  - Average response time line (green dashed)
- **Use For**: Identifying performance trends and patterns over time

### 2. **Response Time Distribution** 📊
- **Type**: Histogram with color gradient
- **Shows**: Frequency distribution of response times
- **Features**:
  - 30 bins with viridis color gradient
  - Mean line (red dashed)
  - Median line (green dashed)
- **Use For**: Understanding typical response time ranges and identifying outliers

### 3. **Response Time Box Plot** 📦
- **Type**: Statistical box plot
- **Shows**: Quartile analysis with percentiles
- **Features**:
  - P0, P25, P50 (median), P75, P100
  - Mean marker (red diamond)
  - Outlier detection
  - Labeled percentile values
- **Use For**: Statistical summary for academic papers (median, IQR, outliers)

### 4. **Response Time by Source** 🔄
- **Type**: Dual chart (box plot + bar chart)
- **Shows**: Performance comparison across sources (Dataset, LLM, RAG)
- **Features**:
  - Side-by-side box plots for distribution comparison
  - Bar chart showing average times
  - Color-coded by source
- **Use For**: Comparing different response generation methods

### 5. **Accuracy Metrics** 🎯
- **Type**: Bar chart with thresholds
- **Shows**: Model performance metrics
- **Features**:
  - Semantic Similarity (TF-IDF)
  - BLEU Score
  - F1 Score
  - Overall Accuracy
  - Threshold lines at 70% (good) and 50% (acceptable)
- **Use For**: Evaluating model quality and reporting metrics

### 6. **User Satisfaction** 😊
- **Type**: Pie chart + bar chart combo
- **Shows**: Like vs dislike distribution
- **Features**:
  - Percentage breakdown (pie chart)
  - Count breakdown (bar chart)
  - Satisfaction rate calculation
- **Use For**: User experience analysis and satisfaction reporting

### 7. **Feedback Timeline** ⏰
- **Type**: Scatter plot timeline
- **Shows**: Positive (green circles) vs negative (red X) feedback over time
- **Features**:
  - Temporal distribution
  - Visual separation of feedback types
  - Time-based patterns
- **Use For**: Identifying problematic time periods or improvement trends

### 8. **Confidence vs Response Time** 🎲
- **Type**: Scatter plot with correlation
- **Shows**: Relationship between confidence scores and response times
- **Features**:
  - Color-coded by source
  - Trend line showing correlation
  - Individual data points
- **Use For**: Analyzing if confidence affects response time

### 9. **Hourly Activity Distribution** 🕐
- **Type**: Bar chart with gradient
- **Shows**: User activity by hour of day
- **Features**:
  - 24-hour breakdown
  - Plasma color gradient
  - Peak hours highlighted (red border)
- **Use For**: Understanding usage patterns and peak times

### 10. **Source Distribution** 📚
- **Type**: Pie chart + bar chart
- **Shows**: Breakdown of responses by source
- **Features**:
  - Percentage distribution
  - Absolute counts
  - Color-coded categories
- **Use For**: Understanding which sources are most utilized

---

## 🚀 How to Generate Visualizations

### Method 1: Automatic (Recommended)
Visualizations are automatically generated when you run the full research analysis:

```bash
cd backend
.\run_research_analysis.bat
# Select option 2: Run FULL RESEARCH ANALYSIS
```

### Method 2: Manual
Generate visualizations separately:

```bash
cd backend
& "D:/VS Code/Help-Desk-AI-RAG-llama-3/.venv/Scripts/python.exe" research_visualization.py
```

### Method 3: From Python Code
```python
from research_visualization import ResearchVisualizer

# Initialize visualizer
visualizer = ResearchVisualizer()

# Generate all visualizations
output_dir = visualizer.generate_all_visualizations()

# Or generate specific visualization
visualizer.plot_response_time_timeline('my_timeline.png')
```

---

## 📁 Output Structure

When visualizations are generated, they are saved in a timestamped folder:

```
research_reports_20260116_150530/
├── research_report_20260116_150530.json
├── csv_exports/
│   ├── response_logs.csv
│   └── feedback_data.csv
└── visualizations/
    ├── index.html                         ← Interactive HTML report
    ├── response_time_timeline.png
    ├── response_time_distribution.png
    ├── response_time_boxplot.png
    ├── response_time_by_source.png
    ├── accuracy_metrics.png
    ├── user_satisfaction_pie.png
    ├── feedback_timeline.png
    ├── confidence_vs_time.png
    ├── hourly_activity.png
    └── source_distribution.png
```

---

## 🌐 Interactive HTML Report

The system generates an `index.html` file with:
- **Summary statistics** at the top
- **All visualizations** embedded with descriptions
- **Professional styling** with gradient themes
- **Responsive design** for mobile/desktop
- **Print-ready** for PDF export

### Opening the Report:
```bash
# Windows
start backend/research_reports_TIMESTAMP/visualizations/index.html

# Or double-click the index.html file
```

---

## 📈 Using Visualizations in Research Papers

### For LaTeX Papers:
```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{response_time_timeline.png}
    \caption{Response time analysis showing performance trends over the data collection period (N=50 responses).}
    \label{fig:response_time}
\end{figure}
```

### For Word Documents:
1. Copy PNG files from the visualizations folder
2. Insert → Picture → Select visualization
3. Add captions with Figure numbers
4. Reference in text: "As shown in Figure 1..."

### Statistical Reporting:
Use the box plot visualization to report:
```
"Response times showed a median of 2.71s (IQR: 1.89-3.77s) 
with 95th percentile at 4.66s (see Figure 3)."
```

---

## 🎨 Customization Options

### Change Figure Size:
Edit `research_visualization.py`:
```python
fig, ax = plt.subplots(figsize=(14, 6))  # Width x Height in inches
```

### Change Colors:
```python
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Custom color palette
```

### Change DPI (Resolution):
```python
plt.savefig(filepath, dpi=300, bbox_inches='tight')  # 300 DPI for publications
```

### Add Watermark:
```python
ax.text(0.5, 0.5, 'DRAFT', transform=ax.transAxes,
        fontsize=40, color='gray', alpha=0.3,
        ha='center', va='center', rotation=30)
```

---

## 📊 Chart Specifications

### Publication Standards:
- **Resolution**: 300 DPI (print quality)
- **Format**: PNG with transparency support
- **Size**: Optimized for A4/Letter paper
- **Fonts**: System fonts (Segoe UI, Tahoma, Verdana)
- **Colors**: Colorblind-friendly palettes (viridis, Set3)

### Academic Requirements Met:
✅ High resolution for journals  
✅ Clear axis labels with units  
✅ Legends for all data series  
✅ Statistical annotations  
✅ Error bars and confidence intervals (where applicable)  
✅ Professional styling  

---

## 🔧 Troubleshooting

### Issue: "Module not found: matplotlib"
**Solution:**
```bash
& "D:/VS Code/Help-Desk-AI-RAG-llama-3/.venv/Scripts/python.exe" -m pip install matplotlib seaborn
```

### Issue: Visualizations are blurry
**Solution:** Increase DPI in code:
```python
plt.savefig(filepath, dpi=600, bbox_inches='tight')  # Higher resolution
```

### Issue: Fonts look different on another computer
**Solution:** Use standard system fonts or embed fonts:
```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
```

### Issue: Charts not showing in HTML report
**Solution:** Ensure PNG files are in the same directory as index.html

### Issue: Out of memory for large datasets
**Solution:** Sample the data:
```python
import random
sampled_logs = random.sample(self.response_logs, 1000)  # Use 1000 samples
```

---

## 📚 Data Requirements

### Minimum Data Needed:
- **Response Logs**: At least 10 entries for meaningful visualizations
- **Timestamps**: Required for timeline charts
- **Response Times**: Required for performance analysis
- **Feedback**: Optional, but needed for satisfaction charts

### Optimal Data Size:
- **50-500 responses**: Good statistical power
- **500-5000 responses**: Excellent for publications
- **5000+ responses**: May need sampling for performance

---

## 🎓 Academic Citation

### Citing Visualizations in Your Paper:

**APA Format:**
```
Figure 1: Response time timeline showing performance trends over the data 
collection period. Generated using custom Python visualization system 
(matplotlib 3.10.8, seaborn 0.13.2).
```

**IEEE Format:**
```
[1] Response time analysis visualization. Data collected from N=50 chatbot 
interactions over 24-hour period. Statistical analysis performed using 
Python 3.13 with matplotlib and seaborn libraries.
```

---

## 💡 Tips for Better Visualizations

1. **Collect More Data**: 50+ responses give better statistical significance
2. **Diverse Time Periods**: Collect data across different hours/days
3. **Label Everything**: Clear axis labels and legends
4. **Use Color Wisely**: Ensure colorblind accessibility
5. **Add Context**: Include sample sizes in figure captions
6. **Export High-Res**: Use 300-600 DPI for print publications
7. **Test Print**: Preview on paper before submitting

---

## 🔗 Related Documentation

- [RESEARCH_EVALUATION_GUIDE.md](RESEARCH_EVALUATION_GUIDE.md) - Complete research system guide
- [RESEARCH_QUICK_START.md](RESEARCH_QUICK_START.md) - Quick start guide
- [RESEARCH_SYSTEM_UPDATE.md](RESEARCH_SYSTEM_UPDATE.md) - Latest updates

---

## 📞 Support

For visualization issues:
1. Check matplotlib documentation: https://matplotlib.org/
2. Seaborn gallery: https://seaborn.pydata.org/examples/
3. Review generated HTML report for embedded visualizations
4. Check console output for specific errors

---

**Generated by Research Visualization System**  
**Version:** 1.0  
**Last Updated:** January 16, 2026  
**Status:** ✅ Production Ready
