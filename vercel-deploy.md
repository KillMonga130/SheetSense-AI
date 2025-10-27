# ⚡ Vercel Deployment (Serverless)

Vercel offers excellent serverless deployment for Python!

## 🚀 Quick Vercel Deployment

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel --prod
   ```

## 📁 Required Files

Create `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "app.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend/$1"
    }
  ],
  "env": {
    "AZURE_OPENAI_ENDPOINT": "https://your-resource.cognitiveservices.azure.com/",
    "AZURE_OPENAI_KEY": "your-api-key-here",
    "AZURE_OPENAI_DEPLOYMENT": "gpt-35-turbo",
    "AZURE_OPENAI_API_VERSION": "2024-12-01-preview"
  }
}
```

## 🎯 Benefits

- ✅ **Completely free**
- ✅ **Serverless (no cold starts)**
- ✅ **Global CDN**
- ✅ **Custom domains**
- ✅ **Perfect performance**

Your app will be live at: `https://sheetsense-ai.vercel.app`