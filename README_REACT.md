# GreenBot - AI Assistant Chatbot

AI-powered chatbot for Green University of Bangladesh with React frontend and Flask backend.

## 🏗️ Architecture

### Frontend (React + Vite)
- Modern React 18 application with Vite build tool
- Tailwind CSS for styling
- Real-time chat interface
- Dark mode support
- Responsive design

### Backend (Flask + Python)
- Flask REST API
- LangChain with Ollama LLaMA 3.2
- RAG (Retrieval-Augmented Generation) system
- Feedback learning system
- 30K+ instruction-response dataset

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama (for LLaMA model)

### Installation

1. **Clone the repository**
```bash
cd d:\VS Code\bot\chatbot
```

2. **Install Backend Dependencies**
```bash
cd backend
pip install -r requirements_enhanced.txt
```

3. **Install Frontend Dependencies**
```bash
cd ../frontend-react
npm install
```

4. **Pull LLaMA Model** (if not already installed)
```bash
ollama pull llama3.2:1b
```

### Running the Application

#### Option 1: Using Batch Script (Windows)
```bash
start_react_app.bat
```

#### Option 2: Using PowerShell Script
```powershell
.\start_react_app.ps1
```

#### Option 3: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python rag_api_server.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend-react
npm run dev
```

### Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📁 Project Structure

```
chatbot/
├── backend/                      # Flask backend
│   ├── rag_api_server.py        # Main API server
│   ├── enhanced_ollama_chatbot.py
│   ├── lora_finetune_llama3.py
│   ├── lora_finetune_ollama.py
│   ├── enhanced_ndata.json      # Enhanced dataset
│   ├── green_university_30k_instruction_response.json
│   └── requirements_enhanced.txt
├── frontend-react/               # React frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API services
│   │   ├── App.jsx              # Main app
│   │   └── main.jsx             # Entry point
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── frontend/                     # Original HTML/CSS/JS (legacy)
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── start_react_app.bat          # Windows startup script
├── start_react_app.ps1          # PowerShell startup script
└── README.md                     # This file
```

## 🔧 Configuration

### Backend Configuration (backend/config.py)
```python
OFFLINE_MODE = False  # Set True for offline mode (JSON only)
```

### Frontend Configuration (frontend-react/.env)
```env
VITE_API_URL=http://localhost:5000
```

## 🌟 Features

### Chat Interface
- ✅ Real-time messaging
- ✅ Typing indicators
- ✅ Message formatting (markdown)
- ✅ Code syntax highlighting
- ✅ Lottie animations

### AI Features
- ✅ LLaMA 3.2 integration
- ✅ RAG system with 30K+ responses
- ✅ Contextual understanding
- ✅ Feedback learning
- ✅ Multi-source search

### User Interface
- ✅ Dark/Light mode
- ✅ Responsive design
- ✅ Analytics dashboard
- ✅ Settings panel
- ✅ Toast notifications

## 🎯 API Endpoints

### Chat Endpoints
- `POST /chat` - Send message to chatbot
  ```json
  {
    "message": "What is the CSE tuition fee?"
  }
  ```

- `POST /feedback` - Submit feedback
  ```json
  {
    "feedback": "like",
    "answer": "The response text",
    "question": "The original question"
  }
  ```

- `GET /health` - Check server health
- `GET /stats` - Get conversation statistics

## 🐛 Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
cd backend
pip install -r requirements_enhanced.txt
```

**Issue**: `Connection refused` to Ollama
```bash
# Start Ollama service
ollama serve

# In another terminal
ollama pull llama3.2:1b
```

### Frontend Issues

**Issue**: `Cannot find module 'vite'`
```bash
cd frontend-react
npm install
```

**Issue**: Backend connection failed
- Ensure backend is running on port 5000
- Check CORS settings in `rag_api_server.py`
- Verify `.env` file has correct API URL

## 📊 Datasets

### Enhanced Data (enhanced_ndata.json)
- Curated Q&A pairs
- Metadata and keywords
- Confidence scores

### Instruction Dataset (green_university_30k_instruction_response.json)
- 30,000+ instruction-response pairs
- University-specific information
- Multiple categories

## 🔄 Migration from Old Frontend

The original HTML/CSS/JS frontend is preserved in the `frontend/` directory. The new React version offers:

- Better performance with Vite
- Component-based architecture
- Modern development experience
- Easier maintenance
- Better state management

## 🛠️ Development

### Backend Development
```bash
cd backend
python rag_api_server.py
```

### Frontend Development
```bash
cd frontend-react
npm run dev
```

### Building for Production
```bash
cd frontend-react
npm run build
npm run preview
```

## 📝 Environment Variables

### Backend
- `OFFLINE_MODE` - Enable/disable offline mode

### Frontend
- `VITE_API_URL` - Backend API URL

## 🎓 Use Cases

- Student inquiries about:
  - Admission requirements
  - Tuition fees
  - Programs and courses
  - Campus facilities
  - Contact information
  - Technical help (programming)

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

This project is for Green University of Bangladesh.

## 👥 Team

Developed for Green University of Bangladesh student assistance.

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in terminal
3. Contact the development team

## 🔜 Future Enhancements

- [ ] Voice input support
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Mobile app version
- [ ] Enhanced feedback system
- [ ] More fine-tuning options

---

**Note**: Make sure to have both backend and frontend running for the application to work properly.
