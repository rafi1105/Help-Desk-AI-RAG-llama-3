import { useState, useEffect } from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ChatContainer from './components/ChatContainer';
import InputArea from './components/InputArea';
import AnalyticsModal from './components/AnalyticsModal';
import SettingsModal from './components/SettingsModal';
import Toast from './components/Toast';
import { chatService } from './services/api';

function App() {
  const [theme, setTheme] = useState('light');
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isAnalyticsOpen, setIsAnalyticsOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('offline');
  const [toasts, setToasts] = useState([]);
  const [autoScroll, setAutoScroll] = useState(true);
  const [showSuccessAnimation, setShowSuccessAnimation] = useState(false);
  const [stats, setStats] = useState({
    messageCount: 0,
    userQuestions: 0,
    botResponses: 0,
    positiveFeedback: 0,
    negativeFeedback: 0,
  });

  // Load settings from localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('greenbot-settings');
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      setTheme(settings.theme || 'light');
      setAutoScroll(settings.autoScroll !== undefined ? settings.autoScroll : true);
    }
  }, []);

  // Apply theme
  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    saveSettings();
  }, [theme]);

  // Check server connection
  useEffect(() => {
    checkConnection();
  }, []);

  const checkConnection = async () => {
    try {
      const response = await chatService.checkHealth();
      if (response.status === 'healthy' || response.status === 'initializing') {
        setConnectionStatus('online');
        showToast('Connected to GreenBot server', 'success');
      }
    } catch (error) {
      setConnectionStatus('offline');
      showToast('Unable to connect to server', 'error');
    }
  };

  const saveSettings = () => {
    const settings = { theme, autoScroll };
    localStorage.setItem('greenbot-settings', JSON.stringify(settings));
  };

  const showToast = (message, type = 'info') => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(toast => toast.id !== id));
    }, 5000);
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || connectionStatus === 'offline') return;

    // Show success animation
    setShowSuccessAnimation(true);
    setTimeout(() => setShowSuccessAnimation(false), 2000);

    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: messageText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setMessages(prev => [...prev, userMessage]);
    setStats(prev => ({ ...prev, messageCount: prev.messageCount + 1, userQuestions: prev.userQuestions + 1 }));

    // Show typing indicator
    setIsTyping(true);

    try {
      const response = await chatService.sendMessage(messageText);
      
      // Hide typing indicator
      setIsTyping(false);

      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.answer || 'Sorry, I couldn\'t generate a response.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        metadata: {
          confidence: response.confidence,
          method: response.method,
          source: response.source,
          processing_time: response.processing_time,
        },
      };
      setMessages(prev => [...prev, botMessage]);
      setStats(prev => ({ ...prev, messageCount: prev.messageCount + 1, botResponses: prev.botResponses + 1 }));

    } catch (error) {
      setIsTyping(false);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, I\'m having trouble connecting to the server. Please try again.',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true,
      };
      setMessages(prev => [...prev, errorMessage]);
      showToast('Failed to send message', 'error');
    }
  };

  const handleFeedback = async (messageId, feedbackType) => {
    const message = messages.find(msg => msg.id === messageId);
    if (!message) return;

    const userMessage = [...messages].reverse().find(msg => msg.type === 'user' && msg.id < messageId);

    try {
      await chatService.sendFeedback(feedbackType, message.content, userMessage?.content || '');
      
      if (feedbackType === 'like') {
        setStats(prev => ({ ...prev, positiveFeedback: prev.positiveFeedback + 1 }));
      } else {
        setStats(prev => ({ ...prev, negativeFeedback: prev.negativeFeedback + 1 }));
      }
      
      showToast('Thank you for your feedback!', 'success');
    } catch (error) {
      console.error('Error sending feedback:', error);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    showToast('Started new conversation', 'success');
  };

  const handleClearChat = () => {
    if (window.confirm('Are you sure you want to clear this conversation?')) {
      setMessages([]);
      showToast('Conversation cleared', 'success');
    }
  };

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <div className={`app flex h-screen overflow-hidden relative ${theme === 'light' ? 'animated-green-gradient' : 'bg-gray-900'}`}>
      {/* Animated Green Circles for Light and Dark Mode */}
      <>
        <div className="absolute top-20 left-10 w-96 h-96 rounded-full opacity-20 blur-3xl" style={{
          background: 'radial-gradient(circle, #6ee7b7 0%, transparent 70%)',
          animation: 'float 8s ease-in-out infinite'
        }}></div>
        <div className="absolute bottom-20 right-10 w-80 h-80 rounded-full opacity-20 blur-3xl" style={{
          background: 'radial-gradient(circle, #34d399 0%, transparent 70%)',
          animation: 'float 10s ease-in-out infinite reverse'
        }}></div>
        <div className="absolute top-1/2 left-1/2 w-72 h-72 rounded-full opacity-15 blur-3xl" style={{
          background: 'radial-gradient(circle, #10b981 0%, transparent 70%)',
          animation: 'float 12s ease-in-out infinite'
        }}></div>
      </>

      {/* Sidebar Overlay */}
      <div
        className={`sidebar-overlay fixed inset-0 bg-black/50  z-20 transition-opacity duration-300 ${
          isSidebarOpen ? 'active opacity-100 visible' : 'opacity-0 invisible'
        }`}
        onClick={() => setIsSidebarOpen(false)}
      />

      {/* Sidebar */}
      <div className="relative z-20">
        <Sidebar
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
          stats={stats}
          onNavigate={(section) => {
            if (section === 'analytics') setIsAnalyticsOpen(true);
            if (section === 'settings') setIsSettingsOpen(true);
            if (section === 'chat') setIsSidebarOpen(false);
          }}
        />
      </div>

      {/* Main Content */}
      <main className="main-content flex-1 flex flex-col ml-0 transition-all duration-300 relative z-10">
        <Header
          onMenuToggle={() => setIsSidebarOpen(!isSidebarOpen)}
          onThemeToggle={toggleTheme}
          onNewChat={handleNewChat}
          theme={theme}
        />

        <ChatContainer
          messages={messages}
          isTyping={isTyping}
          autoScroll={autoScroll}
          onFeedback={handleFeedback}
        />

        <InputArea
          onSendMessage={handleSendMessage}
          onClearChat={handleClearChat}
          connectionStatus={connectionStatus}
          showSuccessAnimation={showSuccessAnimation}
        />
      </main>

      {/* Modals */}
      <AnalyticsModal
        isOpen={isAnalyticsOpen}
        onClose={() => setIsAnalyticsOpen(false)}
        stats={stats}
      />

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        theme={theme}
        onThemeChange={setTheme}
        autoScroll={autoScroll}
        onAutoScrollChange={(value) => {
          setAutoScroll(value);
          saveSettings();
        }}
      />

      {/* Toast Container */}
      <div className="fixed top-5 right-5 z-50 space-y-2">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            message={toast.message}
            type={toast.type}
            onClose={() => setToasts(prev => prev.filter(t => t.id !== toast.id))}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
