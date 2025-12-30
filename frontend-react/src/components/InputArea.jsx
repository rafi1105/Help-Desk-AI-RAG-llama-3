import React, { useState, useRef, useEffect } from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const InputArea = ({ onSendMessage, onClearChat, connectionStatus, showSuccessAnimation }) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && connectionStatus === 'online') {
      onSendMessage(message);
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleChange = (e) => {
    setMessage(e.target.value);
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 120) + 'px';
    }
  };

  return (
    <div className="input-container bg-white/90 dark:bg-gray-800/90 backdrop-blur-md border-t-2 border-green-200 dark:border-green-500/30 shadow-lg p-4">
      {/* Success Animation Overlay */}
      {showSuccessAnimation && (
        <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 pointer-events-none">
          <div className="">
            <DotLottieReact
              src="https://lottie.host/95e82915-6c3a-462b-8553-6fad620f3ad3/8bv5RFXIvX.lottie"
              autoplay
              loop={false}
              style={{ width: '200px', height: '200px' }}
            />
          </div>
        </div>
      )}

      <div className="input-wrapper bg-white/60 dark:bg-gray-700/60 backdrop-blur-sm border-2 border-green-200 dark:border-green-500/30 rounded-3xl hover:border-green-300 dark:hover:border-green-400 focus-within:border-green-400 dark:focus-within:border-green-500 transition-all duration-200 p-3 shadow-lg hover:shadow-xl"
        style={{
          boxShadow: '0 4px 24px rgba(16, 185, 129, 0.15)'
        }}>
        <div className="flex gap-3 items-end">
          <textarea
            ref={textareaRef}
            className="message-input flex-1 bg-transparent border-0 outline-none resize-none placeholder-gray-500 dark:placeholder-gray-400 text-gray-800 dark:text-gray-200 text-sm leading-relaxed min-h-[24px] max-h-32"
            placeholder="Type a message..."
            rows="1"
            maxLength="2000"
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
          />

          <button
            className={`send-button rounded-full w-10 h-10 flex items-center justify-center text-white transition-all duration-200 shadow-lg hover:scale-110 active:scale-95 ${
              message.trim() && connectionStatus === 'online'
                ? 'cursor-pointer'
                : 'bg-gray-400 cursor-not-allowed opacity-50'
            }`}
            style={message.trim() && connectionStatus === 'online' ? {
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              boxShadow: '0 4px 16px rgba(16, 185, 129, 0.5)'
            } : {}}
            onClick={handleSubmit}
            disabled={!message.trim() || connectionStatus !== 'online'}
          >
            <span className="send-icon text-base">➤</span>
          </button>
        </div>
      </div>

      <div className="input-footer flex justify-between items-center mt-2 text-xs">
        <div className="input-info flex items-center space-x-4">
          <span className="char-count text-gray-500 dark:text-gray-400 font-medium">
            {message.length}/2000
          </span>
          <span className="status-indicator flex items-center space-x-2">
            <span className={`status-dot w-2 h-2 rounded-full ${connectionStatus === 'online' ? 'bg-green-500' : 'bg-red-500'}`} />
            <span className={`status-text font-medium ${connectionStatus === 'online' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
              {connectionStatus === 'online' ? 'Online' : 'Offline'}
            </span>
          </span>
        </div>
        <div className="input-actions">
          <button
            className="action-button hover:bg-gray-100 dark:hover:bg-gray-700 p-2 rounded-lg transition-colors duration-200 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
            onClick={onClearChat}
            title="Clear conversation"
          >
            <span className="text-lg">🗑️</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default InputArea;
