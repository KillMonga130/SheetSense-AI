# 🚀 Azure Portal Deployment Guide

Since Azure CLI needs a new terminal session, let's deploy via Azure Portal:

## 📋 Step 1: Create Web App

1. **Go to Azure Portal**: https://portal.azure.com
2. **Click "Create a resource"**
3. **Search for "Web App"** and select it
4. **Click "Create"**

## ⚙️ Step 2: Configure Web App

**Basics Tab:**
- **Subscription**: Your Azure subscription
- **Resource Group**: Create new → `sheetsense-rg`
- **Name**: `sheetsense-ai-demo` (must be globally unique)
- **Publish**: Code
- **Runtime stack**: Python 3.11
- **Operating System**: Linux
- **Region**: East US (or your preferred region)

**App Service Plan:**
- **Pricing tier**: Basic B1 (or higher for better performance)

**Click "Review + Create"** → **"Create"**

## 🔧 Step 3: Configure Environment Variables

After the web app is created:

1. **Go to your Web App** in Azure Portal
2. **Navigate to**: Configuration → Application settings
3. **Add these settings** (click "New application setting" for each):

```
Name: AZURE_OPENAI_ENDPOINT
Value: https://22112-mh9jpxrc-eastus2.cognitiveservices.azure.com/

Name: AZURE_OPENAI_KEY  
Value: [paste your actual API key from .env file]

Name: AZURE_OPENAI_DEPLOYMENT
Value: gpt-35-turbo

Name: AZURE_OPENAI_API_VERSION
Value: 2024-12-01-preview

Name: SCM_DO_BUILD_DURING_DEPLOYMENT
Value: true
```

4. **Click "Save"** at the top

## 📦 Step 4: Deploy Code

**Option A: ZIP Deployment (Easiest)**

1. **Create a ZIP file** with these files:
   - `app.py`
   - `requirements-deploy.txt` 
   - `startup.sh`
   - `frontend/` folder (entire folder)

2. **Go to**: Deployment Center → ZIP Deploy
3. **Upload your ZIP file**
4. **Wait for deployment** to complete

**Option B: GitHub Deployment**

1. **Push code to GitHub** repository
2. **Go to**: Deployment Center → GitHub
3. **Connect your repository**
4. **Select branch**: main
5. **Save** - automatic deployment will start

## ✅ Step 5: Test Your App

1. **Get your app URL**: `https://sheetsense-ai-demo.azurewebsites.net`
2. **Test health endpoint**: `https://your-app.azurewebsites.net/api/health`
3. **Should return**: `{"status": "healthy", "azure_openai": "connected"}`

## 🎯 Quick ZIP Creation

Run this in PowerShell to create deployment ZIP:

```powershell
# Create ZIP for deployment
$files = @(
    "app.py",
    "requirements-deploy.txt", 
    "startup.sh",
    "frontend"
)

Compress-Archive -Path $files -DestinationPath "sheetsense-deploy.zip" -Force
Write-Host "✅ Created sheetsense-deploy.zip - ready for Azure deployment!"
```

## 🏆 You're Ready!

Once deployed, your SheetSense AI will be live and ready for your Azure Codeathon demo!

**Demo Features to Show:**
1. 🧠 **Formula Generator** - "Calculate 15% commission on sales over $5000"
2. 📊 **Data Query** - Upload Excel file, ask "What's the total revenue?"
3. 💡 **Auto Insights** - Get AI-powered data analysis
4. 🎓 **Formula Explainer** - Explain complex Excel formulas

**Your live demo URL**: `https://sheetsense-ai-demo.azurewebsites.net`