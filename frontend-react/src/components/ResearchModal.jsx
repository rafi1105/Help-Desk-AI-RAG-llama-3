import React, { useState } from 'react';
import { exportAnalytics, generateResearchReport } from '../services/api';

const ResearchModal = ({ isOpen, onClose }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [message, setMessage] = useState('');
  const [messageType, setMessageType] = useState('');

  if (!isOpen) return null;

  const showMessage = (text, type = 'success') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => setMessage(''), 4000);
  };

  const handleExportCSV = async () => {
    setIsExporting(true);
    try {
      await exportAnalytics();
      showMessage('✅ CSV files exported successfully! Check backend/research_exports_* folder', 'success');
    } catch (error) {
      showMessage('❌ Export failed: ' + error.message, 'error');
    } finally {
      setIsExporting(false);
    }
  };

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    try {
      const data = await generateResearchReport();
      showMessage('✅ Research report generated! Check backend/research_reports_* folder', 'success');
    } catch (error) {
      showMessage('❌ Generation failed: ' + error.message, 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="modal fixed inset-0 z-50 flex items-center justify-center" onClick={onClose}>
      <div className="modal-overlay absolute inset-0 bg-black/50 backdrop-blur-sm" />
      <div
        className="modal-content bg-white/95 dark:bg-slate-800/95 backdrop-blur-lg rounded-2xl shadow-2xl max-w-3xl w-full mx-4 max-h-[90vh] overflow-auto relative border border-purple-200 dark:border-purple-500/30"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="modal-header p-6 border-b border-purple-200 dark:border-purple-500/30">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-500 bg-clip-text text-transparent flex items-center gap-2">
              <span className="text-3xl">🔬</span> Research Analysis Tools
            </h2>
            <button
              className="modal-close bg-transparent border-0 text-xl cursor-pointer text-gray-500 dark:text-gray-400 p-2 rounded-lg hover:bg-purple-50 dark:hover:bg-slate-700 transition-all duration-200"
              onClick={onClose}
            >
              ✕
            </button>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Generate comprehensive reports and export data for academic research
          </p>
        </div>

        {/* Body */}
        <div className="modal-body p-6 space-y-6">
          {/* Message Banner */}
          {message && (
            <div className={`p-4 rounded-lg border ${
              messageType === 'success' 
                ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-500/30 text-green-700 dark:text-green-300'
                : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-500/30 text-red-700 dark:text-red-300'
            }`}>
              {message}
            </div>
          )}

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Generate Report */}
            <div className="research-card bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-xl p-6 border border-purple-200 dark:border-purple-500/30">
              <div className="flex items-start gap-3 mb-4">
                <span className="text-3xl">📊</span>
                <div>
                  <h3 className="font-bold text-purple-700 dark:text-purple-300 text-lg">Research Report</h3>
                  <p className="text-sm text-purple-600 dark:text-purple-400 mt-1">
                    Generate comprehensive analysis with metrics
                  </p>
                </div>
              </div>
              <ul className="text-sm space-y-1 text-purple-600 dark:text-purple-400 mb-4">
                <li>• Response time analysis</li>
                <li>• Model accuracy evaluation (BLEU, F1)</li>
                <li>• User satisfaction metrics</li>
                <li>• Statistical summaries</li>
              </ul>
              <button
                onClick={handleGenerateReport}
                disabled={isGenerating}
                className={`w-full py-3 rounded-lg font-medium transition-all ${
                  isGenerating
                    ? 'bg-purple-300 cursor-not-allowed'
                    : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white shadow-lg hover:shadow-xl'
                }`}
              >
                {isGenerating ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="animate-spin">⚙️</span> Generating...
                  </span>
                ) : (
                  '📊 Generate Full Report'
                )}
              </button>
            </div>

            {/* Export CSV */}
            <div className="research-card bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-900/20 dark:to-blue-900/20 rounded-xl p-6 border border-cyan-200 dark:border-cyan-500/30">
              <div className="flex items-start gap-3 mb-4">
                <span className="text-3xl">📁</span>
                <div>
                  <h3 className="font-bold text-cyan-700 dark:text-cyan-300 text-lg">Export CSV Data</h3>
                  <p className="text-sm text-cyan-600 dark:text-cyan-400 mt-1">
                    Export data for Excel, SPSS, R analysis
                  </p>
                </div>
              </div>
              <ul className="text-sm space-y-1 text-cyan-600 dark:text-cyan-400 mb-4">
                <li>• response_logs.csv</li>
                <li>• feedback_data.csv</li>
                <li>• Ready for statistical analysis</li>
                <li>• Compatible with SPSS, Excel, R</li>
              </ul>
              <button
                onClick={handleExportCSV}
                disabled={isExporting}
                className={`w-full py-3 rounded-lg font-medium transition-all ${
                  isExporting
                    ? 'bg-cyan-300 cursor-not-allowed'
                    : 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-700 hover:to-blue-700 text-white shadow-lg hover:shadow-xl'
                }`}
              >
                {isExporting ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="animate-spin">⚙️</span> Exporting...
                  </span>
                ) : (
                  '📁 Export to CSV'
                )}
              </button>
            </div>
          </div>

          {/* Features Info */}
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-xl p-6 border border-indigo-200 dark:border-indigo-500/30">
            <h3 className="font-bold text-indigo-700 dark:text-indigo-300 text-lg mb-3 flex items-center gap-2">
              <span>📚</span> Research Capabilities
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <h4 className="font-semibold text-indigo-600 dark:text-indigo-400 mb-2">🎯 Accuracy Metrics</h4>
                <ul className="text-indigo-600 dark:text-indigo-400 space-y-1">
                  <li>• Semantic Similarity (TF-IDF)</li>
                  <li>• BLEU Score (0-1)</li>
                  <li>• Keyword F1 Score</li>
                  <li>• Overall Accuracy Grade</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-indigo-600 dark:text-indigo-400 mb-2">⚡ Response Time</h4>
                <ul className="text-indigo-600 dark:text-indigo-400 space-y-1">
                  <li>• Mean, Median, Std Dev</li>
                  <li>• Percentiles (P50-P99)</li>
                  <li>• Distribution analysis</li>
                  <li>• By source comparison</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-indigo-600 dark:text-indigo-400 mb-2">😊 User Satisfaction</h4>
                <ul className="text-indigo-600 dark:text-indigo-400 space-y-1">
                  <li>• Like/Dislike ratio</li>
                  <li>• Satisfaction rate %</li>
                  <li>• Topic analysis</li>
                  <li>• Temporal trends</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-indigo-600 dark:text-indigo-400 mb-2">📈 Export Formats</h4>
                <ul className="text-indigo-600 dark:text-indigo-400 space-y-1">
                  <li>• JSON reports</li>
                  <li>• CSV for Excel/SPSS</li>
                  <li>• Statistical summaries</li>
                  <li>• Publication-ready data</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Usage Instructions */}
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20 rounded-xl p-6 border border-amber-200 dark:border-amber-500/30">
            <h3 className="font-bold text-amber-700 dark:text-amber-300 text-lg mb-3 flex items-center gap-2">
              <span>💡</span> How to Use
            </h3>
            <ol className="text-sm text-amber-600 dark:text-amber-400 space-y-2">
              <li>1. <strong>Collect Data:</strong> Chat with the bot to generate interaction data</li>
              <li>2. <strong>Generate Report:</strong> Click "Generate Full Report" for comprehensive analysis</li>
              <li>3. <strong>Export Data:</strong> Click "Export to CSV" for statistical software analysis</li>
              <li>4. <strong>Analyze:</strong> Use Excel, SPSS, or R to perform statistical tests</li>
              <li>5. <strong>Publish:</strong> Include metrics in your research paper with proper citations</li>
            </ol>
          </div>

          {/* API Documentation Link */}
          <div className="text-center pt-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              📖 For more details, see <span className="font-semibold text-purple-600 dark:text-purple-400">RESEARCH_EVALUATION_GUIDE.md</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResearchModal;
