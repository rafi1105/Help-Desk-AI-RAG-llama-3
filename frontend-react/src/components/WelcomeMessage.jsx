import React from 'react';
import { DotLottieReact } from '@lottiefiles/dotlottie-react';

const WelcomeMessage = () => {
  return (
    <div className="message bot appear flex gap-4 mb-6">
      <div className="message-avatar w-12 h-12 rounded-full flex items-center justify-center text-lg flex-shrink-0 shadow-lg border-2 border-white dark:border-gray-700">
        <DotLottieReact
          src="https://lottie.host/ff7d4b1f-0c7e-4d5e-9395-88fef6d7c49e/iHjJjm484E.lottie"
          loop
          autoplay
          style={{ width: '80px', height: '80px' }}
        />
      </div>
      <div className="message-content bg-messenger-gray dark:bg-gray-700 p-4 rounded-2xl max-w-2xl shadow-sm border border-gray-200 dark:border-gray-600">
        <div className="space-y-4">
          {/* Greeting Header */}
          <div className="flex items-center space-x-3 pb-3 border-b border-gray-200 dark:border-gray-600">
            <span className="text-2xl">👋</span>
            <div>
              <h3 className="font-semibold text-lg text-messenger-text dark:text-white">
                Welcome to GreenBot! 👋
              </h3>
              <p className="text-sm text-messenger-secondary dark:text-gray-300 mt-1">
                Your intelligent assistant for Green University of Bangladesh
              </p>
            </div>
          </div>

          {/* Services Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              { icon: '📚', title: 'Admissions', desc: 'Requirements & procedures' },
              { icon: '💰', title: 'Finance', desc: 'Tuition fees & scholarships' },
              { icon: '🏛️', title: 'Programs', desc: 'CSE, BBA, Engineering & more' },
              { icon: '🏢', title: 'Campus', desc: 'Facilities & services' },
              { icon: '📞', title: 'Contact', desc: 'Information & support' },
              { icon: '💻', title: 'Technical', desc: 'Programming & tech help' },
            ].map((service, index) => (
              <div
                key={index}
                className="bg-white dark:bg-gray-600 p-4 rounded-lg border border-gray-200 dark:border-gray-500 hover:border-messenger-blue dark:hover:border-blue-400 transition-colors duration-200"
              >
                <div className="flex items-start space-x-3">
                  <span className="text-xl mt-1">{service.icon}</span>
                  <div>
                    <h4 className="font-medium text-messenger-text dark:text-white">{service.title}</h4>
                    <p className="text-xs text-messenger-secondary dark:text-gray-300 mt-1">{service.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeMessage;
