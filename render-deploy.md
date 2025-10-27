# 🎨 Render Deployment (Free Alternative)

Render offers excellent free hosting for Python apps!

## 🚀 Quick Render Deployment

1. **Go to**: https://render.com
2. **Sign up** with GitHub
3. **Click "New +"** → **"Web Service"**
4. **Connect GitHub** and select your repository
5. **Configure**:
   - **Name**: sheetsense-ai
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements-deploy.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

## ⚙️ Environment Variables

Add these in Render dashboard:

```
AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

## 🎯 Benefits

- ✅ **Free tier: 750 hours/month**
- ✅ **Auto-deploy from GitHub**
- ✅ **Custom domains**
- ✅ **SSL certificates**
- ✅ **Great for demos**

Your app will be live at: `https://sheetsense-ai.onrender.com`