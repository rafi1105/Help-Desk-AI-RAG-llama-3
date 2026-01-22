"""
Research Data Visualization Module
===================================
Generates comprehensive graphs and charts for academic research analysis
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path
import seaborn as sns

# Set style for professional academic charts
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class ResearchVisualizer:
    """Generate publication-quality visualizations for research data"""
    
    def __init__(self, response_logs_file: str = 'response_logs.json',
                 feedback_file: str = 'user_feedback_data.json',
                 evaluation_data: Dict = None):
        self.response_logs_file = response_logs_file
        self.feedback_file = feedback_file
        self.response_logs = []
        self.feedback_data = []
        self.evaluation_data = evaluation_data or {}  # Store evaluation metrics
        
        # Load data
        self._load_data()
    
    def _load_data(self):
        """Load response logs and feedback data"""
        try:
            if os.path.exists(self.response_logs_file):
                with open(self.response_logs_file, 'r', encoding='utf-8') as f:
                    self.response_logs = json.load(f)
                print(f"✅ Loaded {len(self.response_logs)} response logs")
            else:
                print(f"⚠️ Response logs file not found: {self.response_logs_file}")
        except Exception as e:
            print(f"❌ Error loading response logs: {e}")
        
        try:
            if os.path.exists(self.feedback_file):
                with open(self.feedback_file, 'r', encoding='utf-8') as f:
                    self.feedback_data = json.load(f)
                print(f"✅ Loaded {len(self.feedback_data)} feedback entries")
            else:
                print(f"⚠️ Feedback file not found: {self.feedback_file}")
        except Exception as e:
            print(f"❌ Error loading feedback: {e}")
    
    def generate_all_visualizations(self, output_dir: str = None) -> str:
        """
        Generate all research visualizations
        Returns the output directory path
        """
        if not self.response_logs:
            print("⚠️ No data available for visualization")
            return None
        
        # Create output directory
        if output_dir is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = f"research_visualizations_{timestamp}"
        
        os.makedirs(output_dir, exist_ok=True)
        print(f"\n📊 Generating visualizations in: {output_dir}/")
        
        # Generate all charts
        charts = [
            ("response_time_timeline", self.plot_response_time_timeline),
            ("response_time_distribution", self.plot_response_time_distribution),
            ("response_time_boxplot", self.plot_response_time_boxplot),
            ("response_time_by_source", self.plot_response_time_by_source),
            ("accuracy_metrics", self.plot_accuracy_metrics),
            ("user_satisfaction_pie", self.plot_user_satisfaction),
            ("feedback_timeline", self.plot_feedback_timeline),
            ("confidence_vs_time", self.plot_confidence_vs_time),
            ("hourly_activity", self.plot_hourly_activity),
            ("source_distribution", self.plot_source_distribution),
        ]
        
        generated = []
        for filename, func in charts:
            try:
                filepath = os.path.join(output_dir, f"{filename}.png")
                func(filepath)
                generated.append(filename)
                print(f"  ✅ {filename}.png")
            except Exception as e:
                print(f"  ❌ {filename}.png - Error: {e}")
        
        # Generate summary HTML
        self._generate_html_report(output_dir, generated)
        
        print(f"\n✅ Generated {len(generated)} visualizations")
        print(f"📄 View report: {output_dir}/index.html")
        
        return output_dir
    
    def plot_response_time_timeline(self, filepath: str):
        """Time series plot of response times"""
        if not self.response_logs:
            return
        
        # Parse timestamps and response times
        timestamps = []
        response_times = []
        
        for log in self.response_logs:
            try:
                ts = datetime.fromisoformat(log['timestamp'])
                timestamps.append(ts)
                response_times.append(log.get('response_time', 0))
            except:
                continue
        
        if not timestamps:
            return
        
        # Create figure
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plot line with markers
        ax.plot(timestamps, response_times, marker='o', markersize=4, 
                linewidth=1.5, color='#2E86DE', alpha=0.8, label='Response Time')
        
        # Add trend line
        x_numeric = mdates.date2num(timestamps)
        z = np.polyfit(x_numeric, response_times, 1)
        p = np.poly1d(z)
        ax.plot(timestamps, p(x_numeric), "--", color='#EE5A6F', 
                linewidth=2, alpha=0.7, label=f'Trend Line')
        
        # Add average line
        avg_time = np.mean(response_times)
        ax.axhline(y=avg_time, color='#10AC84', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f'Average: {avg_time:.2f}s')
        
        # Formatting
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Response Time Over Time', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(loc='upper right', fontsize=10)
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_response_time_distribution(self, filepath: str):
        """Histogram of response time distribution"""
        if not self.response_logs:
            return
        
        response_times = [log.get('response_time', 0) for log in self.response_logs]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create histogram
        n, bins, patches = ax.hist(response_times, bins=30, color='#5F27CD', 
                                    alpha=0.7, edgecolor='black')
        
        # Color gradient
        cm = plt.cm.viridis
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        col = bin_centers - min(bin_centers)
        col /= max(col)
        
        for c, p in zip(col, patches):
            plt.setp(p, 'facecolor', cm(c))
        
        # Add statistics
        mean_time = np.mean(response_times)
        median_time = np.median(response_times)
        
        ax.axvline(mean_time, color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {mean_time:.2f}s')
        ax.axvline(median_time, color='green', linestyle='--', linewidth=2, 
                   label=f'Median: {median_time:.2f}s')
        
        # Formatting
        ax.set_xlabel('Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frequency', fontsize=12, fontweight='bold')
        ax.set_title('Response Time Distribution', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_response_time_boxplot(self, filepath: str):
        """Box plot showing percentiles and outliers"""
        if not self.response_logs:
            return
        
        response_times = [log.get('response_time', 0) for log in self.response_logs]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create box plot
        bp = ax.boxplot([response_times], vert=True, patch_artist=True,
                        labels=['Response Times'],
                        widths=0.6,
                        showmeans=True,
                        meanprops=dict(marker='D', markerfacecolor='red', markersize=10))
        
        # Color the box
        for patch in bp['boxes']:
            patch.set_facecolor('#00D2D3')
            patch.set_alpha(0.7)
        
        # Add percentile labels
        percentiles = [0, 25, 50, 75, 100]
        values = np.percentile(response_times, percentiles)
        
        for i, (p, v) in enumerate(zip(percentiles, values)):
            if p == 50:
                label = f'Median (P{p}): {v:.2f}s'
            else:
                label = f'P{p}: {v:.2f}s'
            ax.text(1.15, v, label, fontsize=10, va='center')
        
        # Formatting
        ax.set_ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Response Time Box Plot (Percentile Analysis)', 
                     fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_response_time_by_source(self, filepath: str):
        """Compare response times by source (dataset/llm/rag)"""
        if not self.response_logs:
            return
        
        # Group by source
        sources = {}
        for log in self.response_logs:
            source = log.get('source', 'unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append(log.get('response_time', 0))
        
        if not sources:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Box plot comparison
        source_names = list(sources.keys())
        source_data = [sources[s] for s in source_names]
        
        bp = ax1.boxplot(source_data, labels=source_names, patch_artist=True,
                         showmeans=True, meanprops=dict(marker='D', markerfacecolor='red'))
        
        # Color boxes
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax1.set_ylabel('Response Time (seconds)', fontsize=11, fontweight='bold')
        ax1.set_xlabel('Source', fontsize=11, fontweight='bold')
        ax1.set_title('Response Time by Source (Box Plot)', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # Bar chart with averages
        avg_times = [np.mean(sources[s]) for s in source_names]
        bars = ax2.bar(source_names, avg_times, color=colors[:len(source_names)], alpha=0.7)
        
        # Add value labels on bars
        for bar, avg in zip(bars, avg_times):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{avg:.2f}s', ha='center', va='bottom', fontweight='bold')
        
        ax2.set_ylabel('Average Response Time (seconds)', fontsize=11, fontweight='bold')
        ax2.set_xlabel('Source', fontsize=11, fontweight='bold')
        ax2.set_title('Average Response Time by Source', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_accuracy_metrics(self, filepath: str):
        """Bar chart of accuracy metrics"""
        # Get real metrics from evaluation data or use placeholders
        has_real_data = False
        if self.evaluation_data and 'overall_metrics' in self.evaluation_data:
            eval_metrics = self.evaluation_data
            metrics = {
                'Semantic\nSimilarity': eval_metrics.get('semantic_similarity', {}).get('mean', 0.0),
                'BLEU\nScore': eval_metrics.get('bleu_score', {}).get('mean', 0.0),
                'F1\nScore': eval_metrics.get('f1_score', {}).get('mean', 0.0),
                'Overall\nAccuracy': eval_metrics.get('overall_metrics', {}).get('mean_accuracy', 0.0)
            }
            has_real_data = True
        else:
            # Fallback to placeholder data if no evaluation results
            metrics = {
                'Semantic\nSimilarity': 0.0,
                'BLEU\nScore': 0.0,
                'F1\nScore': 0.0,
                'Overall\nAccuracy': 0.0
            }
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        colors = ['#3498DB', '#E74C3C', '#2ECC71', '#F39C12']
        bars = ax.bar(metrics.keys(), metrics.values(), color=colors, alpha=0.8, 
                      edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for bar, (name, value) in zip(bars, metrics.items()):
            height = bar.get_height()
            percentage = value * 100
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{percentage:.1f}%', ha='center', va='bottom', 
                   fontweight='bold', fontsize=11)
        
        # Add threshold line
        ax.axhline(y=0.7, color='green', linestyle='--', linewidth=2, 
                   alpha=0.7, label='Good Threshold (70%)')
        ax.axhline(y=0.5, color='orange', linestyle='--', linewidth=2, 
                   alpha=0.7, label='Acceptable Threshold (50%)')
        
        # Add warning if no real data
        if not has_real_data:
            ax.text(0.5, 0.85, '⚠ No Ground Truth Data - Showing Zero Values\nAdd dataset/ground_truth.json for real metrics',
                   transform=ax.transAxes, ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                   fontsize=10, fontweight='bold')
        
        ax.set_ylabel('Score (0-1)', fontsize=12, fontweight='bold')
        ax.set_title('Model Accuracy Metrics', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 1.0)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_user_satisfaction(self, filepath: str):
        """Pie chart of user satisfaction (likes/dislikes)"""
        # Calculate from feedback data
        likes = sum(1 for f in self.feedback_data if f.get('feedback') == 'like')
        dislikes = sum(1 for f in self.feedback_data if f.get('feedback') == 'dislike')
        
        # If no data, show message chart
        if likes == 0 and dislikes == 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, 'No User Feedback Data Available\n\nUsers need to provide likes/dislikes',
                   ha='center', va='center', fontsize=14, fontweight='bold')
            ax.axis('off')
            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        sizes = [likes, dislikes]
        labels = [f'Positive\n({likes})', f'Negative\n({dislikes})']
        colors = ['#2ECC71', '#E74C3C']
        explode = (0.05, 0.05)
        
        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                                            autopct='%1.1f%%', shadow=True, startangle=90,
                                            textprops={'fontsize': 12, 'fontweight': 'bold'})
        
        ax1.set_title('User Satisfaction Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart
        total = likes + dislikes
        satisfaction_rate = (likes / total * 100) if total > 0 else 0
        
        categories = ['Positive', 'Negative', 'Total']
        values = [likes, dislikes, total]
        bar_colors = ['#2ECC71', '#E74C3C', '#3498DB']
        
        bars = ax2.bar(categories, values, color=bar_colors, alpha=0.8, edgecolor='black')
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(value)}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=12)
        
        ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax2.set_title(f'Satisfaction Rate: {satisfaction_rate:.1f}%', 
                     fontsize=14, fontweight='bold', pad=20)
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_feedback_timeline(self, filepath: str):
        """Timeline of positive vs negative feedback"""
        if not self.feedback_data:
            return
        
        # Parse timestamps
        likes = []
        dislikes = []
        
        for feedback in self.feedback_data:
            try:
                ts = datetime.fromisoformat(feedback['timestamp'])
                if feedback.get('feedback') == 'like':
                    likes.append(ts)
                else:
                    dislikes.append(ts)
            except:
                continue
        
        if not likes and not dislikes:
            return
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plot likes and dislikes
        if likes:
            ax.scatter(likes, [1]*len(likes), c='green', s=100, alpha=0.6, 
                      marker='o', label='Positive', edgecolors='black')
        if dislikes:
            ax.scatter(dislikes, [0]*len(dislikes), c='red', s=100, alpha=0.6, 
                      marker='x', label='Negative', edgecolors='black', linewidths=2)
        
        ax.set_ylim(-0.5, 1.5)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Negative', 'Positive'])
        ax.set_xlabel('Time', fontsize=12, fontweight='bold')
        ax.set_title('Feedback Timeline', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=10)
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_confidence_vs_time(self, filepath: str):
        """Scatter plot of confidence vs response time"""
        if not self.response_logs:
            return
        
        confidences = []
        times = []
        sources = []
        
        for log in self.response_logs:
            conf = log.get('confidence')
            time = log.get('response_time')
            source = log.get('source', 'unknown')
            
            if conf is not None and time is not None:
                confidences.append(conf)
                times.append(time)
                sources.append(source)
        
        if not confidences:
            return
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Create scatter plot with different colors for sources
        unique_sources = list(set(sources))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_sources)))
        
        for source, color in zip(unique_sources, colors):
            mask = [s == source for s in sources]
            conf_subset = [c for c, m in zip(confidences, mask) if m]
            time_subset = [t for t, m in zip(times, mask) if m]
            ax.scatter(conf_subset, time_subset, c=[color], s=50, alpha=0.6, 
                      label=source, edgecolors='black')
        
        # Add correlation line
        if len(confidences) > 1:
            z = np.polyfit(confidences, times, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(confidences), max(confidences), 100)
            ax.plot(x_line, p(x_line), "--", color='red', linewidth=2, 
                   alpha=0.7, label='Trend')
        
        ax.set_xlabel('Confidence Score', fontsize=12, fontweight='bold')
        ax.set_ylabel('Response Time (seconds)', fontsize=12, fontweight='bold')
        ax.set_title('Confidence Score vs Response Time', fontsize=14, fontweight='bold', pad=20)
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_hourly_activity(self, filepath: str):
        """Bar chart of activity by hour"""
        if not self.response_logs:
            return
        
        hours = []
        for log in self.response_logs:
            try:
                ts = datetime.fromisoformat(log['timestamp'])
                hours.append(ts.hour)
            except:
                continue
        
        if not hours:
            return
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Count by hour
        hour_counts = {}
        for h in range(24):
            hour_counts[h] = hours.count(h)
        
        hours_list = list(hour_counts.keys())
        counts_list = list(hour_counts.values())
        
        # Create gradient colors
        colors = plt.cm.plasma(np.linspace(0.2, 0.8, 24))
        
        bars = ax.bar(hours_list, counts_list, color=colors, alpha=0.8, edgecolor='black')
        
        # Highlight peak hours
        max_count = max(counts_list)
        for bar, count in zip(bars, counts_list):
            if count == max_count:
                bar.set_edgecolor('red')
                bar.set_linewidth(3)
        
        ax.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Interactions', fontsize=12, fontweight='bold')
        ax.set_title('Activity Distribution by Hour', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(hours_list)
        ax.set_xticklabels([f'{h:02d}:00' for h in hours_list], rotation=45, ha='right')
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def plot_source_distribution(self, filepath: str):
        """Pie chart of response sources"""
        if not self.response_logs:
            return
        
        sources = {}
        for log in self.response_logs:
            source = log.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        if not sources:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Pie chart
        labels = list(sources.keys())
        sizes = list(sources.values())
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))
        explode = [0.05] * len(labels)
        
        wedges, texts, autotexts = ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
                                            autopct='%1.1f%%', shadow=True, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
        
        ax1.set_title('Response Source Distribution', fontsize=14, fontweight='bold', pad=20)
        
        # Bar chart
        bars = ax2.bar(labels, sizes, color=colors, alpha=0.8, edgecolor='black')
        
        for bar, size in zip(bars, sizes):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(size)}', ha='center', va='bottom', 
                    fontweight='bold', fontsize=11)
        
        ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Source', fontsize=12, fontweight='bold')
        ax2.set_title('Response Count by Source', fontsize=14, fontweight='bold', pad=20)
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
    
    def _generate_html_report(self, output_dir: str, generated: List[str]):
        """Generate HTML report with all visualizations"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Analysis Visualizations</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        .stat-card h3 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        .stat-card p {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .chart {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .chart h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .chart img {{
            width: 100%;
            border-radius: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #999;
        }}
        .timestamp {{
            background: #ffeaa7;
            padding: 10px 20px;
            border-radius: 10px;
            display: inline-block;
            margin-bottom: 30px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Research Analysis Report</h1>
        <p class="subtitle">Comprehensive Data Visualization for Academic Research</p>
        
        <div style="text-align: center;">
            <span class="timestamp">🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(self.response_logs)}</h3>
                <p>Total Responses</p>
            </div>
            <div class="stat-card">
                <h3>{len(self.feedback_data)}</h3>
                <p>Feedback Entries</p>
            </div>
            <div class="stat-card">
                <h3>{len(generated)}</h3>
                <p>Visualizations</p>
            </div>
        </div>
        
        <div class="chart">
            <h2>📈 Response Time Timeline</h2>
            <img src="response_time_timeline.png" alt="Response Time Timeline">
            <p style="margin-top: 15px; color: #666;">Shows response times over the collection period with trend analysis.</p>
        </div>
        
        <div class="chart">
            <h2>📊 Response Time Distribution</h2>
            <img src="response_time_distribution.png" alt="Response Time Distribution">
            <p style="margin-top: 15px; color: #666;">Histogram showing the frequency distribution of response times.</p>
        </div>
        
        <div class="chart">
            <h2>📦 Response Time Box Plot</h2>
            <img src="response_time_boxplot.png" alt="Response Time Box Plot">
            <p style="margin-top: 15px; color: #666;">Statistical summary with quartiles and outliers.</p>
        </div>
        
        <div class="chart">
            <h2>🔄 Response Time by Source</h2>
            <img src="response_time_by_source.png" alt="Response Time by Source">
            <p style="margin-top: 15px; color: #666;">Comparison of response times across different sources (Dataset, LLM, RAG).</p>
        </div>
        
        <div class="chart">
            <h2>🎯 Accuracy Metrics</h2>
            <img src="accuracy_metrics.png" alt="Accuracy Metrics">
            <p style="margin-top: 15px; color: #666;">Model performance metrics including BLEU, semantic similarity, and F1 scores.</p>
        </div>
        
        <div class="chart">
            <h2>😊 User Satisfaction</h2>
            <img src="user_satisfaction_pie.png" alt="User Satisfaction">
            <p style="margin-top: 15px; color: #666;">Distribution of positive vs negative user feedback.</p>
        </div>
        
        <div class="chart">
            <h2>⏰ Feedback Timeline</h2>
            <img src="feedback_timeline.png" alt="Feedback Timeline">
            <p style="margin-top: 15px; color: #666;">Temporal distribution of user feedback over time.</p>
        </div>
        
        <div class="chart">
            <h2>🎲 Confidence vs Response Time</h2>
            <img src="confidence_vs_time.png" alt="Confidence vs Time">
            <p style="margin-top: 15px; color: #666;">Correlation analysis between confidence scores and response times.</p>
        </div>
        
        <div class="chart">
            <h2>🕐 Hourly Activity Distribution</h2>
            <img src="hourly_activity.png" alt="Hourly Activity">
            <p style="margin-top: 15px; color: #666;">User activity patterns throughout the day.</p>
        </div>
        
        <div class="chart">
            <h2>📚 Source Distribution</h2>
            <img src="source_distribution.png" alt="Source Distribution">
            <p style="margin-top: 15px; color: #666;">Breakdown of responses by source type.</p>
        </div>
        
        <div class="footer">
            <p>Generated by Research Visualization System</p>
            <p>Green University Help Desk AI - RAG System</p>
            <p style="margin-top: 10px; font-size: 0.9em;">📄 For statistical analysis, use the CSV files in the research_reports folder</p>
        </div>
    </div>
</body>
</html>
"""
        
        html_path = os.path.join(output_dir, 'index.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)


def main():
    """Generate all visualizations"""
    print("="*80)
    print("📊 RESEARCH DATA VISUALIZATION SYSTEM")
    print("="*80)
    print()
    
    visualizer = ResearchVisualizer()
    
    if not visualizer.response_logs:
        print("⚠️ No data available. Please collect data first by:")
        print("   1. Running the chatbot server")
        print("   2. Having conversations with users")
        print("   3. Running research_analysis.py")
        return
    
    output_dir = visualizer.generate_all_visualizations()
    
    if output_dir:
        print()
        print("="*80)
        print("✅ VISUALIZATION COMPLETE")
        print("="*80)
        print(f"\n📁 All visualizations saved to: {output_dir}/")
        print(f"🌐 Open in browser: {output_dir}/index.html")
        print()


if __name__ == '__main__':
    main()
