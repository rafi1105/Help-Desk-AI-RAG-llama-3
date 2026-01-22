import React, { useState } from 'react';
import { exportAnalytics, generateResearchReport } from '../services/api';

const AnalyticsModal = ({ isOpen, onClose, stats }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isExporting, setIsExporting] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [exportMessage, setExportMessage] = useState('');

  if (!isOpen) return null;

  const satisfactionRate = stats.positiveFeedback + stats.negativeFeedback > 0
    ? Math.round((stats.positiveFeedback / (stats.positiveFeedback + stats.negativeFeedback)) * 100)
    : 100;

  const handleExportCSV = async () => {
    setIsExporting(true);
    setExportMessage('');
    try {
      await exportAnalytics();
      setExportMessage('✅ CSV files exported successfully!');
    } catch (error) {
      setExportMessage('❌ Export failed: ' + error.message);
    } finally {
      setIsExporting(false);
      setTimeout(() => setExportMessage(''), 3000);
    }
  };

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    setExportMessage('');
    try {
      await generateResearchReport();
      setExportMessage('✅ Research report generated!');
    } catch (error) {
      setExportMessage('❌ Generation failed: ' + error.message);
    } finally {
      setIsGenerating(false);
      setTimeout(() => setExportMessage(''), 3000);
    }
  };

  return (
    <div className="modal fixed inset-0 z-50 flex items-center justify-center" onClick={onClose}>
      <div className="modal-overlay absolute inset-0 bg-black/50 backdrop-blur-sm" />
      <div
        className="modal-content bg-white/90 dark:bg-slate-800/90 backdrop-blur-lg rounded-2xl shadow-2xl max-w-2xl w-full mx-4 max-h-[90vh] overflow-auto relative border border-blue-200 dark:border-blue-500/30"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header p-6 border-b border-blue-200 dark:border-blue-500/30">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent flex items-center gap-2">
              <span className="text-2xl">📊</span> Research & Analytics
            </h2>
            <button
              className="modal-close bg-transparent border-0 text-xl cursor-pointer text-gray-500 dark:text-gray-400 p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-slate-700 transition-all duration-200"
              onClick={onClose}
            >
              ✕
            </button>
          </div>
          
          {/* Tabs */}
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-4 py-2 rounded-lg transition-all ${
                activeTab === 'overview'
                  ? 'bg-blue-500 text-white'
                  : 'bg-blue-100 dark:bg-slate-700 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-slate-600'
              }`}
            >
              📈 Overview
            </button>
            <button
              onClick={() => setActiveTab('research')}
              className={`px-4 py-2 rounded-lg transition-all ${
                activeTab === 'research'
                  ? 'bg-blue-500 text-white'
                  : 'bg-blue-100 dark:bg-slate-700 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-slate-600'
              }`}
            >
              🔬 Research Tools
            </button>
          </div>
        </div>

        <div className="modal-body p-6">
          <div className="analytics-grid grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="analytics-card bg-gradient-to-br from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl overflow-hidden border border-blue-200 dark:border-blue-500/30">
              <div className="card-header p-4 bg-white/50 dark:bg-slate-700/50 border-b border-blue-200 dark:border-blue-500/30 flex items-center gap-2 font-medium">
                <span className="text-xl">💬</span>
                <span className="text-blue-700 dark:text-blue-300">Conversation Stats</span>
              </div>
              <div className="card-content p-4 space-y-3">
                <div className="stat-row flex justify-between items-center py-2 border-b border-blue-100 dark:border-blue-500/20">
                  <span className="text-sm text-blue-600 dark:text-blue-400 font-medium">Total Messages</span>
                  <span className="text-lg font-bold text-blue-700 dark:text-blue-300">{stats.messageCount}</span>
                </div>
                <div className="stat-row flex justify-between items-center py-2 border-b border-blue-100 dark:border-blue-500/20">
                  <span className="text-sm text-blue-600 dark:text-blue-400 font-medium">User Questions</span>
                  <span className="text-lg font-bold text-blue-700 dark:text-blue-300">{stats.userQuestions}</span>
                </div>
                <div className="stat-row flex justify-between items-center py-2">
                  <span className="text-sm text-blue-600 dark:text-blue-400 font-medium">Bot Responses</span>
                  <span className="text-lg font-bold text-blue-700 dark:text-blue-300">{stats.botResponses}</span>
                </div>
              </div>
            </div>

            <div className="analytics-card bg-gradient-to-br from-cyan-50 to-indigo-50 dark:from-cyan-900/20 dark:to-indigo-900/20 rounded-xl overflow-hidden border border-cyan-200 dark:border-cyan-500/30">
              <div className="card-header p-4 bg-white/50 dark:bg-slate-700/50 border-b border-cyan-200 dark:border-cyan-500/30 flex items-center gap-2 font-medium">
                <span className="text-xl">👍</span>
                <span className="text-cyan-700 dark:text-cyan-300">Feedback Analytics</span>
              </div>
              <div className="card-content p-4 space-y-3">
                <div className="stat-row flex justify-between items-center py-2 border-b border-cyan-100 dark:border-cyan-500/20">
                  <span className="text-sm text-cyan-600 dark:text-cyan-400 font-medium">Positive</span>
                  <span className="text-lg font-bold text-cyan-700 dark:text-cyan-300">{stats.positiveFeedback}</span>
                </div>
                <div className="stat-row flex justify-between items-center py-2 border-b border-cyan-100 dark:border-cyan-500/20">
                  <span className="text-sm text-cyan-600 dark:text-cyan-400 font-medium">Negative</span>
                  <span className="text-lg font-bold text-cyan-700 dark:text-cyan-300">{stats.negativeFeedback}</span>
                </div>
                <div className="stat-row flex justify-between items-center py-2">
                  <span className="text-sm text-cyan-600 dark:text-cyan-400 font-medium">Satisfaction Rate</span>
                  <span className="text-lg font-bold text-cyan-700 dark:text-cyan-300">{satisfactionRate}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsModal;
