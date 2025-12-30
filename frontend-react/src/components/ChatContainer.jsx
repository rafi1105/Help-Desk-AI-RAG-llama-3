import React, { useEffect, useRef } from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';
import ChatMessage from './ChatMessage';
import WelcomeMessage from './WelcomeMessage';
import TypingIndicator from './TypingIndicator';

const ChatContainer = ({ messages, isTyping, autoScroll, onFeedback }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    if (autoScroll) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  return (
    <div className="chat-container flex-1 flex flex-col overflow-hidden relative">
      <div className="messages-area flex-1 overflow-y-auto p-6 scroll-smooth">
        {messages.length === 0 && <WelcomeMessage />}
        
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            message={message}
            onFeedback={onFeedback}
          />
        ))}

        {isTyping && <TypingIndicator />}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Background Animation */}
      <div className="background-animation absolute bottom-2 right-14 z-10 opacity-40 hover:opacity-60 transition-opacity duration-300 pointer-events-none">
        <DotLottieReact
          src="https://lottie.host/4f2729d1-6942-40b3-b1eb-04c80f727a65/C5cnrneDqz.lottie"
          loop
          autoplay
          style={{ width: '600px', height: '600px' }}
        />
      </div>
    </div>
  );
};

export default ChatContainer;
