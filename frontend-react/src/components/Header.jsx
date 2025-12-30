import React from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const Header = ({ onMenuToggle, onThemeToggle, onNewChat, theme }) => {
  return (
    <header className="header h-16 border-b border-white/20 dark:border-gray-700/50 flex items-center justify-between px-6 sticky top-0 z-40 shadow-lg backdrop-blur-md" style={{
      background: theme === 'light'
        ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.95) 0%, rgba(5, 150, 105, 0.95) 50%, rgba(52, 211, 153, 0.9) 100%)'
        : 'linear-gradient(135deg, rgba(26, 32, 44, 0.95) 0%, rgba(45, 55, 72, 0.95) 100%)'
    }}>
      <div className="header-left flex items-center gap-4">
        <button
          className="menu-button bg-white/20 dark:bg-gray-700/50 backdrop-blur-sm border-0 text-xl cursor-pointer p-2 rounded-lg transition-all duration-200 text-white hover:bg-white/30 dark:hover:bg-gray-600/50 hover:scale-110"
          onClick={onMenuToggle}
        >
          <span className="text-2xl">☰</span>
        </button>
        <div className="brand flex items-center gap-3">
          <div className="header-lottie w-20 h-20   p-1 ">
            <DotLottieReact
              src="https://lottie.host/4f2729d1-6942-40b3-b1eb-04c80f727a65/C5cnrneDqz.lottie"
              loop
              autoplay
              style={{ width: '72px', height: '72px' }}
            />
          </div>
          <span className="text-3xl font-bold text-white drop-shadow-lg">GreenBot</span>
        </div>
      </div>

      <div className="header-center flex-1 text-center">
        <div className="conversation-title">
          <span className="font-bold text-2xl text-white drop-shadow-md">
            Green University Assistant
          </span>
        </div>
      </div>

      <div className="header-right flex items-center gap-2">
        <button
          className="header-button bg-white/20 dark:bg-gray-700/50 backdrop-blur-sm border-0 text-lg cursor-pointer p-3 rounded-lg transition-all duration-200 text-white hover:bg-white/30 dark:hover:bg-gray-600/50 hover:scale-110 shadow-md"
          onClick={onThemeToggle}
          title="Toggle theme"
        >
          <span className="theme-icon text-xl">{theme === 'light' ? '🌙' : '☀️'}</span>
        </button>
        <button
          className="header-button bg-white/20 dark:bg-gray-700/50 backdrop-blur-sm border-0 text-lg cursor-pointer p-3 rounded-lg transition-all duration-200 text-white hover:bg-white/30 dark:hover:bg-gray-600/50 hover:scale-110 shadow-md"
          onClick={onNewChat}
          title="New chat"
        >
          <span className="text-xl">➕</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
