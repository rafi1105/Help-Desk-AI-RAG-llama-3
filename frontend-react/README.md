# GreenBot React Frontend

Modern React + Vite frontend for the GreenBot AI Assistant chatbot.

## 🚀 Features

- ⚡ Built with React 18 and Vite for blazing fast development
- 🎨 Styled with Tailwind CSS for modern, responsive design
- 🌗 Dark mode support with theme persistence
- 💬 Real-time chat interface with typing indicators
- 📊 Analytics dashboard for conversation insights
- 🎯 Feedback system integrated with backend
- ♿ Accessible and responsive design
- 🎭 Lottie animations for engaging user experience

## 📋 Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- Backend server running on port 5000

## 🛠️ Installation

1. Navigate to the frontend-react directory:
```bash
cd frontend-react
```

2. Install dependencies:
```bash
npm install
```

## 🚀 Running the Application

### Development Mode

Start the development server with hot reload:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Production Build

Build the application for production:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory (optional):

```env
VITE_API_URL=http://localhost:5000
```

If not set, the default backend URL is `http://localhost:5000`.

### Backend Connection

The frontend connects to the backend via the proxy configuration in `vite.config.js`. The backend must be running on port 5000 for the application to work properly.

## 📁 Project Structure

```
frontend-react/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── ChatContainer.jsx
│   │   ├── ChatMessage.jsx
│   │   ├── WelcomeMessage.jsx
│   │   ├── TypingIndicator.jsx
│   │   ├── InputArea.jsx
│   │   ├── AnalyticsModal.jsx
│   │   ├── SettingsModal.jsx
│   │   └── Toast.jsx
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
└── postcss.config.js    # PostCSS configuration
```

## 🎨 Components

### Main Components

- **App.jsx**: Main application component with state management
- **Header.jsx**: Top navigation bar with theme toggle
- **Sidebar.jsx**: Collapsible sidebar with analytics preview
- **ChatContainer.jsx**: Message display area with welcome message
- **ChatMessage.jsx**: Individual message component with feedback buttons
- **InputArea.jsx**: Message input with character counter
- **AnalyticsModal.jsx**: Detailed analytics modal
- **SettingsModal.jsx**: Settings configuration modal
- **Toast.jsx**: Toast notification component

## 🔌 API Integration

The frontend communicates with the backend through the following endpoints:

- `POST /chat` - Send messages to the chatbot
- `POST /feedback` - Submit feedback (like/dislike)
- `GET /health` - Check server health
- `GET /stats` - Get conversation statistics

All API calls are handled through the `src/services/api.js` service layer.

## 🎨 Styling

- **Tailwind CSS**: Utility-first CSS framework
- **Custom CSS**: Additional styles in `src/index.css`
- **Theme Support**: Light and dark mode with CSS variables
- **Responsive**: Mobile-first responsive design

## 🔒 Features

### Theme Management
- Light/Dark mode toggle
- Theme persistence in localStorage
- Smooth transitions between themes

### Chat Features
- Real-time message display
- Typing indicators
- Message formatting (markdown support)
- Feedback system (like/dislike)
- Auto-scroll to new messages

### Analytics
- Total message count
- User questions count
- Bot responses count
- Feedback statistics
- Satisfaction rate calculation

### Settings
- Theme selection
- Auto-scroll toggle
- Settings persistence

## 🐛 Troubleshooting

### Backend Connection Issues

If the frontend cannot connect to the backend:

1. Ensure the backend server is running on port 5000
2. Check CORS settings in the backend
3. Verify the API URL in the configuration

### Build Issues

If you encounter build errors:

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf .vite node_modules/.vite
```

## 📝 License

This project is part of the GreenBot chatbot system for Green University of Bangladesh.

## 🤝 Contributing

To contribute to this project:

1. Follow the existing code style
2. Write clear commit messages
3. Test your changes thoroughly
4. Update documentation as needed

## 📞 Support

For issues or questions, please contact the development team or create an issue in the project repository.
