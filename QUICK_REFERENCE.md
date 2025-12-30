# 🚀 GreenBot React - Quick Reference

## Start Application

### Option 1: Double-click
```
start_react_app.bat
```

### Option 2: PowerShell
```powershell
.\start_react_app.ps1
```

### Option 3: Manual
```bash
# Terminal 1 - Backend
cd backend
python rag_api_server.py

# Terminal 2 - Frontend  
cd frontend-react
npm run dev
```

## URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:5000
- Health: http://localhost:5000/health

## First Time Setup
```bash
# 1. Install frontend
cd frontend-react
npm install

# 2. Install backend
cd ../backend
pip install -r requirements_enhanced.txt

# 3. Pull AI model
ollama pull llama3.2:1b
```

## Common Commands

### Frontend
```bash
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
npm install          # Install dependencies
```

### Backend
```bash
python rag_api_server.py    # Start server
pip install -r requirements_enhanced.txt  # Install deps
```

## Project Structure
```
frontend-react/src/
├── components/      # React components
├── services/        # API services
├── App.jsx          # Main app
└── main.jsx         # Entry point

backend/
├── rag_api_server.py         # Main API
├── enhanced_ollama_chatbot.py
└── enhanced_ndata.json       # Data
```

## Troubleshooting

### Backend won't start
```bash
# Check Python
python --version

# Reinstall deps
pip install -r requirements_enhanced.txt

# Check Ollama
ollama serve
ollama pull llama3.2:1b
```

### Frontend won't start
```bash
# Check Node
node --version

# Reinstall deps
rm -rf node_modules package-lock.json
npm install

# Or try
npm install --legacy-peer-deps
```

### Connection issues
1. Ensure backend running on port 5000
2. Check `.env` file: `VITE_API_URL=http://localhost:5000`
3. Clear browser cache

## Key Files

### Configuration
- `frontend-react/.env` - Frontend config
- `backend/config.py` - Backend config
- `vite.config.js` - Vite settings
- `tailwind.config.js` - Tailwind settings

### Documentation
- `README_REACT.md` - Main docs
- `SETUP_GUIDE.md` - Detailed setup
- `REACT_MIGRATION_SUMMARY.md` - Migration info

## Features

### Chat
- Real-time messaging
- Typing indicators
- Message formatting
- Feedback (like/dislike)

### UI
- Dark/Light mode
- Responsive design
- Analytics dashboard
- Settings panel
- Toast notifications

### Backend
- LLaMA 3.2 AI
- 30K+ responses
- Feedback learning
- Offline mode support

## Keyboard Shortcuts
- `Ctrl+K` - Focus input (future)
- `Enter` - Send message
- `Shift+Enter` - New line
- `Esc` - Close modals

## Development

### Hot Reload
- Frontend: Auto-reload on save
- Backend: Manual restart needed

### Check Logs
- Frontend: Browser console (F12)
- Backend: Terminal output

### Build Production
```bash
cd frontend-react
npm run build
# Output in dist/
```

## Environment Variables

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
```

### Backend (config.py)
```python
OFFLINE_MODE = False
```

## API Endpoints
- `POST /chat` - Send message
- `POST /feedback` - Submit feedback
- `GET /health` - Check health
- `GET /stats` - Get statistics

## Tech Stack
- React 18
- Vite
- Tailwind CSS
- Axios
- Flask
- LangChain
- Ollama

## Support

### Quick Fixes
1. Restart both servers
2. Clear browser cache
3. Check console for errors
4. Verify ports not in use
5. Check internet connection

### Get Help
- Read SETUP_GUIDE.md
- Check browser console
- Review terminal logs
- Contact development team

## Tips
- ✅ Start backend before frontend
- ✅ Check console for errors
- ✅ Use incognito to test
- ✅ Keep Ollama running
- ✅ Clear cache if issues

---

**Need more help?** Read `SETUP_GUIDE.md` for detailed instructions.
