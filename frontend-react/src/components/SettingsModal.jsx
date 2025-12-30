import React from 'react';

const SettingsModal = ({ isOpen, onClose, theme, onThemeChange, autoScroll, onAutoScrollChange }) => {
  if (!isOpen) return null;

  return (
    <div className="modal fixed inset-0 z-50 flex items-center justify-center" onClick={onClose}>
      <div className="modal-overlay absolute inset-0 bg-black/50 backdrop-blur-sm" />
      <div
        className="modal-content bg-white/90 dark:bg-slate-800/90 backdrop-blur-lg rounded-2xl shadow-2xl max-w-lg w-full mx-4 max-h-[90vh] overflow-auto relative border border-blue-200 dark:border-blue-500/30"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header p-6 border-b border-blue-200 dark:border-blue-500/30 flex justify-between items-center">
          <h2 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-500 bg-clip-text text-transparent flex items-center gap-2">
            <span className="text-2xl">⚙️</span> Settings
          </h2>
          <button
            className="modal-close bg-transparent border-0 text-xl cursor-pointer text-gray-500 dark:text-gray-400 p-2 rounded-lg hover:bg-blue-50 dark:hover:bg-slate-700 transition-all duration-200"
            onClick={onClose}
          >
            ✕
          </button>
        </div>

        <div className="modal-body p-6">
          <div className="settings-section mb-8">
            <h3 className="text-lg font-semibold mb-4 text-blue-700 dark:text-blue-300">Appearance</h3>
            <div className="setting-item flex justify-between items-center py-4 border-b border-blue-100 dark:border-blue-500/20">
              <label className="setting-label font-medium text-gray-700 dark:text-gray-300">Theme</label>
              <div className="setting-control flex gap-2">
                <button
                  className={`theme-option px-4 py-2 border rounded-lg cursor-pointer transition-all duration-200 text-sm font-medium ${
                    theme === 'light'
                      ? 'bg-blue-500 text-white border-blue-500'
                      : 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-500/30 hover:bg-blue-100 dark:hover:bg-blue-800/50'
                  }`}
                  onClick={() => onThemeChange('light')}
                >
                  Light
                </button>
                <button
                  className={`theme-option px-4 py-2 border rounded-lg cursor-pointer transition-all duration-200 text-sm font-medium ${
                    theme === 'dark'
                      ? 'bg-blue-500 text-white border-blue-500'
                      : 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-500/30 hover:bg-blue-100 dark:hover:bg-blue-800/50'
                  }`}
                  onClick={() => onThemeChange('dark')}
                >
                  Dark
                </button>
              </div>
            </div>
          </div>

          <div className="settings-section">
            <h3 className="text-lg font-semibold mb-4 text-blue-700 dark:text-blue-300">Behavior</h3>
            <div className="setting-item flex justify-between items-center py-4">
              <label className="setting-label font-medium text-gray-700 dark:text-gray-300">
                Auto-scroll to new messages
              </label>
              <div className="setting-control">
                <label className="toggle relative inline-block w-12 h-6">
                  <input
                    type="checkbox"
                    checked={autoScroll}
                    onChange={(e) => onAutoScrollChange(e.target.checked)}
                    className="opacity-0 w-0 h-0"
                  />
                  <span
                    className={`toggle-slider absolute cursor-pointer inset-0 transition-all duration-300 rounded-full before:absolute before:content-[''] before:h-5 before:w-5 before:left-0.5 before:bottom-0.5 before:bg-white before:transition-all before:duration-300 before:rounded-full ${
                      autoScroll
                        ? 'bg-blue-500 before:translate-x-6'
                        : 'bg-gray-400 dark:bg-gray-600'
                    }`}
                  />
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
