# 🚂 Railway Deployment (Free Alternative)

Railway offers free hosting perfect for demos!

## 🚀 Quick Railway Deployment

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Connect your GitHub** and select your repository
5. **Railway auto-detects** Python and deploys!

## ⚙️ Environment Variables

In Railway dashboard, add these variables:

```
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-12-01-preview
PORT=8000
```

## 📦 Required Files

Make sure your repo has:
- `requirements-deploy.txt` (rename from requirements.txt)
- `app.py`
- `frontend/` folder

## 🎯 Benefits

- ✅ **Free tier available**
- ✅ **Automatic deployments**
- ✅ **Custom domain**
- ✅ **HTTPS included**
- ✅ **Perfect for demos**

Your app will be live at: `https://your-app.up.railway.app`