import React from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const TypingIndicator = () => {
  return (
    <div className="typing-indicator flex items-center gap-4 px-10 pb-10">
      <div className="message-avatar w-12 h-12 rounded-full flex items-center justify-center text-lg flex-shrink-0 shadow-lg border-2 border-white dark:border-gray-700">
        <DotLottieReact
          src="https://lottie.host/ff7d4b1f-0c7e-4d5e-9395-88fef6d7c49e/iHjJjm484E.lottie"
          loop
          autoplay
          style={{ width: '80px', height: '80px' }}
        />
      </div>
      <div className="typing-bubble flex items-center justify-center p-2 bg-messenger-gray dark:bg-gray-700 rounded-2xl border border-gray-200 dark:border-gray-600">
        <DotLottieReact
          src="https://lottie.host/eb2104a9-02a5-4bd5-a040-94d39d20dddc/3EBT472Wr1.lottie"
          loop
          autoplay
          style={{ width: '60px', height: '40px' }}
        />
      </div>
      <div className="typing-text text-sm text-gray-500 dark:text-gray-400 font-medium">
        GreenBot is typing...
      </div>
    </div>
  );
};

export default TypingIndicator;
