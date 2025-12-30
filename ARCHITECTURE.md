# GreenBot Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                 │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              React Frontend (Port 3000)                       │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │  App.jsx (Main State Management)                        │ │   │
│  │  │  - Messages state                                        │ │   │
│  │  │  - Theme state                                           │ │   │
│  │  │  - Connection status                                     │ │   │
│  │  │  - Statistics                                            │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  │                                                               │   │
│  │  ┌───────────┐ ┌────────────┐ ┌──────────┐ ┌─────────────┐│   │
│  │  │  Header   │ │  Sidebar   │ │  Chat    │ │  InputArea  ││   │
│  │  │           │ │            │ │Container │ │             ││   │
│  │  └───────────┘ └────────────┘ └──────────┘ └─────────────┘│   │
│  │                                                               │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  Services Layer (api.js)                              │   │   │
│  │  │  - chatService.sendMessage()                          │   │   │
│  │  │  - chatService.sendFeedback()                         │   │   │
│  │  │  - chatService.checkHealth()                          │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                │ HTTP Requests (Axios)
                                │ JSON Payload
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Flask Backend (Port 5000)                         │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  rag_api_server.py (Main API Server)                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐│   │
│  │  │  /chat   │  │/feedback │  │ /health  │  │   /stats    ││   │
│  │  │ endpoint │  │ endpoint │  │ endpoint │  │  endpoint   ││   │
│  │  └──────────┘  └──────────┘  └──────────┘  └─────────────┘│   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  IntegratedSearchSystem                                       │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐│   │
│  │  │  JSON Search   │  │ Instruction    │  │  Enhanced      ││   │
│  │  │  (30K data)    │  │ Response DB    │  │  Chatbot       ││   │
│  │  └────────────────┘  └────────────────┘  └────────────────┘│   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                ↓                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  enhanced_ollama_chatbot.py                                   │   │
│  │  - Feedback learning                                          │   │
│  │  - Pattern recognition                                        │   │
│  │  - Response improvement                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                │ API Calls
                                ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    Ollama Service (Port 11434)                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  LLaMA 3.2:8b Model                                           │   │
│  │  - Natural language understanding                             │   │
│  │  - Response generation                                        │   │
│  │  - Context awareness                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Chat Message Flow
```
User Input
    ↓
InputArea Component
    ↓
App.jsx (State Update)
    ↓
chatService.sendMessage()
    ↓
POST /chat endpoint
    ↓
IntegratedSearchSystem.integrated_search()
    ├─→ JSON Search (enhanced_ndata.json)
    ├─→ Instruction Response Search (30K dataset)
    └─→ Enhanced Chatbot (with feedback learning)
         ↓
         Ollama LLaMA 3.2
         ↓
    Response Generated
    ↓
Backend JSON Response
    ↓
Frontend receives data
    ↓
App.jsx updates messages state
    ↓
ChatMessage Component renders
    ↓
User sees response
```

### Feedback Flow
```
User clicks 👍 or 👎
    ↓
ChatMessage Component
    ↓
onFeedback callback
    ↓
chatService.sendFeedback()
    ↓
POST /feedback endpoint
    ↓
IntegratedSearchSystem.record_feedback()
    ├─→ Save to user_feedback_data.json
    ├─→ Update learning stats
    ├─→ Block disliked answers
    └─→ Retrain models
    ↓
Enhanced chatbot learns
    ↓
Future responses improve
```

## Component Hierarchy

```
App
├── Sidebar
│   ├── Navigation Items
│   └── Analytics Preview
├── Header
│   ├── Menu Toggle
│   ├── Logo
│   ├── Theme Toggle
│   └── New Chat Button
├── ChatContainer
│   ├── WelcomeMessage (if no messages)
│   ├── ChatMessage[] (array of messages)
│   │   ├── Avatar (Lottie)
│   │   ├── Content (formatted)
│   │   └── Feedback Buttons
│   ├── TypingIndicator (when loading)
│   └── Background Animation
├── InputArea
│   ├── Textarea (auto-resize)
│   ├── Send Button
│   ├── Character Counter
│   └── Status Indicator
├── AnalyticsModal
│   └── Statistics Cards
├── SettingsModal
│   ├── Theme Selector
│   └── Auto-scroll Toggle
└── Toast[] (array of notifications)
```

## State Management

### App.jsx State
```javascript
{
  theme: 'light' | 'dark',
  messages: [
    {
      id: number,
      type: 'user' | 'bot',
      content: string,
      timestamp: string,
      metadata?: object
    }
  ],
  isTyping: boolean,
  isSidebarOpen: boolean,
  isAnalyticsOpen: boolean,
  isSettingsOpen: boolean,
  connectionStatus: 'online' | 'offline',
  toasts: [
    {
      id: number,
      message: string,
      type: 'success' | 'error' | 'info'
    }
  ],
  autoScroll: boolean,
  stats: {
    messageCount: number,
    userQuestions: number,
    botResponses: number,
    positiveFeedback: number,
    negativeFeedback: number
  }
}
```

## File Organization

### Frontend Structure
```
frontend-react/
├── public/                    # Static assets
├── src/
│   ├── components/            # React components
│   │   ├── Header.jsx         # ~100 lines
│   │   ├── Sidebar.jsx        # ~100 lines
│   │   ├── ChatContainer.jsx  # ~80 lines
│   │   ├── ChatMessage.jsx    # ~120 lines
│   │   ├── WelcomeMessage.jsx # ~60 lines
│   │   ├── TypingIndicator.jsx# ~40 lines
│   │   ├── InputArea.jsx      # ~100 lines
│   │   ├── AnalyticsModal.jsx # ~80 lines
│   │   ├── SettingsModal.jsx  # ~90 lines
│   │   └── Toast.jsx          # ~50 lines
│   ├── services/
│   │   └── api.js             # API service layer
│   ├── App.jsx                # ~200 lines
│   ├── main.jsx               # ~10 lines
│   └── index.css              # ~150 lines
├── .env                       # Environment variables
├── package.json               # Dependencies
├── vite.config.js             # Vite config
└── tailwind.config.js         # Tailwind config
```

### Backend Structure
```
backend/
├── rag_api_server.py          # Main API (~600 lines)
├── enhanced_ollama_chatbot.py # Enhanced chatbot
├── config.py                  # Configuration
├── enhanced_ndata.json        # Enhanced dataset
├── green_university_30k_instruction_response.json
├── user_feedback_data.json    # Feedback storage
├── disliked_answers.json      # Blocked answers
└── requirements_enhanced.txt  # Python dependencies
```

## Technology Stack

### Frontend Technologies
```
React 18.2.0
├── Core Library
├── React Hooks (useState, useEffect, useRef)
└── Functional Components

Vite 5.0.8
├── Fast dev server
├── Hot Module Replacement
└── Production builds

Tailwind CSS 3.4.0
├── Utility-first styling
├── Dark mode support
└── Responsive design

Axios 1.6.2
└── HTTP client

Additional:
├── Lottie animations
└── PostCSS & Autoprefixer
```

### Backend Technologies
```
Flask
├── REST API framework
├── CORS support
└── JSON handling

LangChain
├── LLM orchestration
└── Chain management

Ollama
└── LLaMA 3.2:1b model

scikit-learn
├── TF-IDF vectorization
├── Cosine similarity
└── Random Forest classifier

NLTK
├── Text preprocessing
├── Lemmatization
└── Stopwords removal
```

## Deployment Ports

```
Development:
- Frontend: 3000 (Vite dev server)
- Backend: 5000 (Flask)
- Ollama: 11434 (Ollama service)

Production:
- Frontend: 4173 (Vite preview)
- Backend: 5000 (Flask production)
- Ollama: 11434 (Ollama service)
```

## API Contract

### POST /chat
```
Request:
{
  "message": "What is the CSE tuition fee?"
}

Response:
{
  "answer": "The CSE tuition fee is...",
  "confidence": 0.95,
  "method": "enhanced_multi_source_llama",
  "analyzed_items": 10709,
  "processing_time": 1.23,
  "source": "multi_source_llama_hybrid"
}
```

### POST /feedback
```
Request:
{
  "feedback": "like",
  "answer": "The response text",
  "question": "The original question"
}

Response:
{
  "status": "success",
  "message": "Feedback recorded",
  "learning_stats": {...}
}
```

## Performance Metrics

### Frontend
- Initial Load: ~1-2s
- Hot Reload: <100ms
- Build Time: ~10-20s
- Bundle Size: ~500KB gzipped

### Backend
- Startup Time: ~5-10s
- Response Time: 1-3s (with LLaMA)
- Response Time: <1s (JSON only)

## Security Considerations

### Implemented
- ✅ CORS configuration
- ✅ Input validation
- ✅ Error handling
- ✅ Environment variables

### Future Enhancements
- [ ] Authentication
- [ ] Rate limiting
- [ ] Input sanitization
- [ ] HTTPS support
- [ ] API key management

---

**This architecture provides a modern, scalable foundation for the GreenBot chatbot system.**
