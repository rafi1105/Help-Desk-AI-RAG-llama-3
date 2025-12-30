import React from 'react';

const Sidebar = ({ isOpen, onClose, stats, onNavigate }) => {
  return (
    <aside
      className={`sidebar fixed top-0 left-0 h-full w-80 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 shadow-lg transform transition-transform duration-300 ease-in-out z-50 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="sidebar-header p-6 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <div className="sidebar-title flex items-center gap-3">
          <span className="text-2xl">📊</span>
          <span className="font-semibold text-lg text-messenger-blue dark:text-blue-400">Analytics</span>
        </div>
        <button
          className="sidebar-close bg-transparent border-0 text-xl cursor-pointer text-gray-500 dark:text-gray-400 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
          onClick={onClose}
        >
          <span>✕</span>
        </button>
      </div>

      <nav className="sidebar-nav p-6">
        <button
          className="nav-item w-full p-4 border-0 bg-transparent text-left rounded-lg cursor-pointer transition-colors duration-200 flex items-center gap-3 mb-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-messenger-blue dark:hover:text-blue-400"
          onClick={() => onNavigate('chat')}
        >
          <span className="text-lg">💬</span>
          <span>Chat</span>
        </button>
        <button
          className="nav-item w-full p-4 border-0 bg-transparent text-left rounded-lg cursor-pointer transition-colors duration-200 flex items-center gap-3 mb-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-messenger-blue dark:hover:text-blue-400"
          onClick={() => onNavigate('analytics')}
        >
          <span className="text-lg">📊</span>
          <span>Analytics</span>
        </button>
        <button
          className="nav-item w-full p-4 border-0 bg-transparent text-left rounded-lg cursor-pointer transition-colors duration-200 flex items-center gap-3 mb-3 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-messenger-blue dark:hover:text-blue-400"
          onClick={() => onNavigate('settings')}
        >
          <span className="text-lg">⚙️</span>
          <span>Settings</span>
        </button>
      </nav>

      <div className="sidebar-content flex-1 p-6">
        <div className="analytics-preview">
          <div className="stat-card bg-messenger-gray dark:bg-gray-700 p-4 rounded-lg mb-3 border border-gray-200 dark:border-gray-600">
            <div className="stat-label text-xs text-messenger-secondary dark:text-gray-400 mb-1 font-medium">
              Total Messages
            </div>
            <div className="stat-value text-2xl font-bold text-messenger-blue dark:text-blue-400">
              {stats.messageCount}
            </div>
          </div>
          <div className="stat-card bg-messenger-gray dark:bg-gray-700 p-4 rounded-lg mb-3 border border-gray-200 dark:border-gray-600">
            <div className="stat-label text-xs text-messenger-secondary dark:text-gray-400 mb-1 font-medium">
              Active Today
            </div>
            <div className="stat-value text-2xl font-bold text-messenger-blue dark:text-blue-400">
              {stats.userQuestions}
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
