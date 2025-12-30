# GreenBot React Setup Guide

Complete guide to set up and run the GreenBot React application.

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Running the Application](#running-the-application)
4. [Troubleshooting](#troubleshooting)
5. [Development Workflow](#development-workflow)

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Node.js 16 or higher**
   - Download from: https://nodejs.org/
   - Verify installation: `node --version` and `npm --version`

3. **Ollama** (for AI features)
   - Download from: https://ollama.ai/
   - Install and start Ollama service

### Optional Tools
- Git (for version control)
- VS Code (recommended IDE)

## Installation Steps

### Step 1: Navigate to Project Directory

```powershell
cd "d:\VS Code\bot\chatbot"
```

### Step 2: Install Backend Dependencies

```powershell
cd backend
pip install -r requirements_enhanced.txt
cd ..
```

**Note**: If you encounter SSL errors, try:
```powershell
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements_enhanced.txt
```

### Step 3: Install Ollama Model

```powershell
ollama pull llama3.2:1b
```

Wait for the model to download (approximately 1-2 GB).

### Step 4: Install Frontend Dependencies

```powershell
cd frontend-react
npm install
```

**Alternative** (if npm is slow):
```powershell
npm install --legacy-peer-deps
```

### Step 5: Verify Installation

Check that all dependencies are installed:

**Backend:**
```powershell
cd backend
python -c "import flask, langchain_community, sklearn; print('Backend OK')"
```

**Frontend:**
```powershell
cd frontend-react
npm list react vite tailwindcss
```

## Running the Application

### Method 1: Using Batch Script (Easiest)

1. Double-click `start_react_app.bat` in the chatbot directory
2. Two command windows will open:
   - Backend server (Python/Flask)
   - Frontend server (React/Vite)
3. Wait for both servers to start
4. Open browser: http://localhost:3000

### Method 2: Using PowerShell Script

```powershell
.\start_react_app.ps1
```

### Method 3: Manual Start (Recommended for Development)

**Terminal 1 - Backend Server:**
```powershell
cd backend
python rag_api_server.py
```

Wait for message: `Running on http://0.0.0.0:5000`

**Terminal 2 - Frontend Server:**
```powershell
cd frontend-react
npm run dev
```

Wait for message showing the local URL (usually http://localhost:3000)

**Access the application:**
- Open browser: http://localhost:3000

## Troubleshooting

### Backend Issues

#### Issue 1: "ModuleNotFoundError"

**Solution:**
```powershell
cd backend
pip install -r requirements_enhanced.txt
```

#### Issue 2: "Port 5000 already in use"

**Solution:**
```powershell
# Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
```

#### Issue 3: "Connection refused" to Ollama

**Solution:**
```powershell
# Start Ollama service
ollama serve

# Verify model is installed
ollama list
ollama pull llama3.2:1b
```

#### Issue 4: Python not found

**Solution:**
- Add Python to PATH
- Or use full path: `C:\Python39\python.exe rag_api_server.py`

### Frontend Issues

#### Issue 1: "Cannot find module 'vite'"

**Solution:**
```powershell
cd frontend-react
rm -r node_modules
rm package-lock.json
npm install
```

#### Issue 2: "EADDRINUSE: Port 3000 already in use"

**Solution:**
The frontend will automatically try port 3001, 3002, etc. Or manually kill:
```powershell
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

#### Issue 3: Backend connection failed

**Verify:**
1. Backend is running: http://localhost:5000/health
2. Check console for errors
3. Verify `.env` file:
   ```env
   VITE_API_URL=http://localhost:5000
   ```

#### Issue 4: npm install fails

**Solution:**
```powershell
# Clear npm cache
npm cache clean --force

# Install with legacy peer deps
npm install --legacy-peer-deps

# Or use yarn
npm install -g yarn
yarn install
```

### Common Errors

#### "CORS policy" error

**Solution:**
Backend CORS is already configured. If issue persists:
1. Check backend `rag_api_server.py` CORS settings
2. Ensure frontend is accessing correct URL
3. Clear browser cache

#### Page shows blank

**Solution:**
1. Check browser console (F12)
2. Verify both servers are running
3. Check network tab for failed requests
4. Try incognito mode

## Development Workflow

### Making Changes

**Backend Changes:**
1. Edit Python files in `backend/`
2. Restart backend server (Ctrl+C, then re-run)
3. Test changes

**Frontend Changes:**
1. Edit files in `frontend-react/src/`
2. Changes auto-reload (hot module replacement)
3. Check browser for updates

### Adding New Features

**New React Component:**
```jsx
// frontend-react/src/components/NewComponent.jsx
import React from 'react';

const NewComponent = () => {
  return (
    <div>Your content</div>
  );
};

export default NewComponent;
```

**New API Endpoint:**
```python
# backend/rag_api_server.py
@app.route('/new-endpoint', methods=['POST'])
def new_endpoint():
    data = request.get_json()
    return jsonify({'result': 'success'})
```

### Testing

**Backend API Testing:**
```powershell
# Using curl
curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"message\":\"test\"}"

# Or use Postman/Insomnia
```

**Frontend Testing:**
1. Open browser DevTools (F12)
2. Check Console for errors
3. Check Network tab for API calls
4. Test in different browsers

### Building for Production

```powershell
cd frontend-react
npm run build
```

Preview production build:
```powershell
npm run preview
```

## Tips & Best Practices

1. **Always start backend before frontend**
2. **Check console logs for errors**
3. **Keep Ollama running in background**
4. **Use incognito mode to test without cache**
5. **Restart servers after major changes**

## Quick Commands Reference

### Start Everything
```powershell
# Option 1: Batch script
.\start_react_app.bat

# Option 2: PowerShell script
.\start_react_app.ps1

# Option 3: Manual
# Terminal 1: cd backend && python rag_api_server.py
# Terminal 2: cd frontend-react && npm run dev
```

### Stop Everything
```powershell
# Press Ctrl+C in each terminal

# Or force kill
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
```

### Check Status
```powershell
# Backend health
curl http://localhost:5000/health

# Frontend (open in browser)
# http://localhost:3000
```

### View Logs
- Backend: Check terminal output
- Frontend: Check browser console (F12)

## Next Steps

1. ✅ Complete installation
2. ✅ Run application successfully
3. ✅ Test basic chat functionality
4. ✅ Explore analytics dashboard
5. ✅ Try dark mode
6. ✅ Submit feedback
7. 🚀 Start developing!

## Support

If you encounter issues not covered here:

1. Check error messages carefully
2. Search for error online
3. Review backend/frontend logs
4. Check GitHub issues
5. Contact development team

## Resources

- **React Docs**: https://react.dev/
- **Vite Docs**: https://vitejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **Flask Docs**: https://flask.palletsprojects.com/
- **Ollama Docs**: https://ollama.ai/docs

---

**Happy Coding! 🚀**
