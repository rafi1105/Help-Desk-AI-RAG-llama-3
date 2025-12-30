import React, { useState } from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const ChatMessage = ({ message, onFeedback }) => {
  const [feedbackGiven, setFeedbackGiven] = useState(null);

  const handleFeedback = (type) => {
    setFeedbackGiven(type);
    onFeedback(message.id, type);
  };

  // Get confidence level styling
  const getConfidenceStyle = (confidence) => {
    if (confidence >= 0.8) return { bg: 'bg-green-100 dark:bg-green-900/40', border: 'border-green-400', text: 'text-green-700 dark:text-green-400', icon: '✅' };
    if (confidence >= 0.55) return { bg: 'bg-blue-100 dark:bg-blue-900/40', border: 'border-blue-400', text: 'text-blue-700 dark:text-blue-400', icon: '📊' };
    if (confidence >= 0.3) return { bg: 'bg-amber-100 dark:bg-amber-900/40', border: 'border-amber-400', text: 'text-amber-700 dark:text-amber-400', icon: '⚠️' };
    return { bg: 'bg-red-100 dark:bg-red-900/40', border: 'border-red-400', text: 'text-red-700 dark:text-red-400', icon: '🤖' };
  };

  // Get method display name
  const getMethodDisplay = (method) => {
    if (!method) return 'Unknown';
    if (method.includes('EXACT')) return '📚 Exact Match';
    if (method.includes('VARIATION')) return '📚 Variation Match';
    if (method.includes('DATASET')) return '📚 Dataset';
    if (method.includes('LLM_WITH_CONTEXT')) return '🤖 AI + Context';
    if (method.includes('LLM_ONLY')) return '🤖 AI Generated';
    if (method.includes('TFIDF')) return '📚 Similar Match';
    return method;
  };

  const formatContent = (content) => {
    // Format confidence warnings with special styling (multiple patterns)
    // Pattern 1: ⚠️ *Confidence: 80% - message*
    content = content.replace(
      /⚠️\s*\*Confidence:\s*(\d+)%\s*-\s*([^*]+)\*/g,
      '<div class="confidence-notice mt-4 p-3 bg-amber-50 dark:bg-amber-900/30 border-l-4 border-amber-400 dark:border-amber-500 rounded-r-lg text-sm shadow-sm"><span class="font-semibold text-amber-600 dark:text-amber-400">⚠️ Confidence: $1%</span><span class="text-amber-700 dark:text-amber-300 ml-1">- $2</span></div>'
    );
    
    // Pattern 2: Plain text without asterisks
    content = content.replace(
      /⚠️\s*Confidence:\s*(\d+)%\s*-\s*([^\n<]+)/g,
      '<div class="confidence-notice mt-4 p-3 bg-amber-50 dark:bg-amber-900/30 border-l-4 border-amber-400 dark:border-amber-500 rounded-r-lg text-sm shadow-sm"><span class="font-semibold text-amber-600 dark:text-amber-400">⚠️ Confidence: $1%</span><span class="text-amber-700 dark:text-amber-300 ml-1">- $2</span></div>'
    );
    
    // Format bold text
    content = content.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold">$1</strong>');
    
    // Format code blocks
    content = content.replace(
      /```(\w+)?\n([\s\S]*?)```/g,
      '<div class="bg-gray-100 dark:bg-gray-800 p-4 rounded-lg my-3 overflow-x-auto border border-gray-200 dark:border-gray-600"><pre class="text-sm font-mono"><code>$2</code></pre></div>'
    );
    
    // Format inline code
    content = content.replace(
      /`([^`]+)`/g,
      '<code class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-sm font-mono">$1</code>'
    );
    
    // Format line breaks
    content = content.replace(/\n/g, '<br>');
    
    return content;
  };

  return (
    <div className={`message ${message.type} flex gap-4 mb-8 message-appear ${message.type === 'user' ? 'justify-end' : ''}`}>
      {message.type === 'bot' && (
        <div className="message-avatar w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg border-2 border-white dark:border-gray-700">
          <DotLottieReact
            src="https://lottie.host/ff7d4b1f-0c7e-4d5e-9395-88fef6d7c49e/iHjJjm484E.lottie"
            loop
            autoplay
            style={{ width: '80px', height: '80px' }}
          />
        </div>
      )}

      <div className="flex flex-col max-w-3xl">
        <div
          className={`message-content p-4 rounded-2xl shadow-lg backdrop-blur-sm border-2 ${
            message.type === 'user'
              ? 'text-white ml-auto border-green-200'
              : 'bg-white/90 dark:bg-slate-800/80 border-green-200 dark:border-green-500/30 text-gray-800 dark:text-white'
          }`}
          style={message.type === 'user' ? {
            background: 'linear-gradient(135deg, #10b981 0%, #059669 50%, #34d399 100%)',
            boxShadow: '0 8px 32px rgba(16, 185, 129, 0.4)'
          } : {
            boxShadow: '0 8px 32px rgba(5, 150, 105, 0.15)'
          }}
        >
          <div
            className="prose prose-sm max-w-none dark:prose-invert"
            dangerouslySetInnerHTML={{ __html: formatContent(message.content) }}
          />

          {/* Metadata Info Card - Shows confidence, method, source */}
          {message.type === 'bot' && !message.isError && message.metadata && (
            <div className={`mt-3 p-2 rounded-lg text-xs border-l-4 ${getConfidenceStyle(message.metadata.confidence).bg} ${getConfidenceStyle(message.metadata.confidence).border}`}>
              <div className="flex flex-wrap gap-3 items-center">
                {/* Confidence */}
                <div className={`flex items-center gap-1 ${getConfidenceStyle(message.metadata.confidence).text}`}>
                  <span>{getConfidenceStyle(message.metadata.confidence).icon}</span>
                  <span className="font-semibold">
                    {Math.round((message.metadata.confidence || 0) * 100)}% confidence
                  </span>
                </div>
                
                {/* Method */}
                {message.metadata.method && (
                  <div className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                    <span>{getMethodDisplay(message.metadata.method)}</span>
                  </div>
                )}
                
                {/* Source */}
                {message.metadata.source && (
                  <div className="flex items-center gap-1 text-gray-500 dark:text-gray-500">
                    <span>📁</span>
                    <span className="truncate max-w-[150px]">{message.metadata.source}</span>
                  </div>
                )}
              </div>
            </div>
          )}

          {message.type === 'bot' && !message.isError && (
            <div className="feedback-buttons flex space-x-2 mt-3 pt-3 border-t border-green-100 dark:border-green-500/20">
              <button
                className={`feedback-btn px-3 py-2 rounded-full text-sm transition-all duration-200 flex items-center space-x-1 border backdrop-blur-sm ${
                  feedbackGiven === 'like'
                    ? 'bg-green-100 border-green-300 dark:bg-green-900/30 dark:border-green-500 text-green-600 dark:text-green-400 shadow-lg'
                    : 'bg-white/60 hover:bg-green-100 dark:bg-gray-700/60 dark:hover:bg-green-900/30 border-green-200 dark:border-green-500/30 text-gray-600 dark:text-gray-300 hover:border-green-300 dark:hover:border-green-500 hover:shadow-lg hover:scale-105'
                }`}
                onClick={() => handleFeedback('like')}
                title="This was helpful"
              >
                <span>👍</span>
                <span className="text-xs font-medium">Helpful</span>
              </button>
              <button
                className={`feedback-btn px-3 py-2 rounded-full text-sm transition-all duration-200 flex items-center space-x-1 border backdrop-blur-sm ${
                  feedbackGiven === 'dislike'
                    ? 'border-red-400 dark:border-red-500 text-red-600 dark:text-red-400 shadow-lg'
                    : 'bg-white/60 hover:bg-red-100 dark:bg-gray-700/60 dark:hover:bg-red-900/30 border-green-200 dark:border-green-500/30 text-gray-600 dark:text-gray-300 hover:border-red-300 dark:hover:border-red-500 hover:shadow-lg hover:scale-105'
                }`}
                style={feedbackGiven === 'dislike' ? {
                  background: 'linear-gradient(135deg, #f87171 0%, #ef4444 100%)'
                } : {}}
                onClick={() => handleFeedback('dislike')}
                title="This wasn't helpful"
              >
                <span>👎</span>
                <span className="text-xs font-medium">Not helpful</span>
              </button>
            </div>
          )}
        </div>

        <div className={`message-timestamp text-xs text-gray-500 dark:text-gray-400 mt-1 px-4 ${message.type === 'user' ? 'text-right' : ''}`}>
          {message.timestamp}
        </div>
      </div>

      {message.type === 'user' && (
        <div className="message-avatar w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 shadow-lg border-2 border-white dark:border-gray-700">
          <DotLottieReact
            src="https://lottie.host/27a54662-d9a1-4584-8984-c51941f5adcd/qkDHure2A0.lottie"
            loop
            autoplay
            style={{ width: '80px', height: '80px' }}
          />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
