# 🚀 Azure Deployment Guide for SheetSense AI

## 📋 Prerequisites

1. **Azure CLI** installed and logged in
2. **Azure subscription** with sufficient credits
3. **Resource Group** created
4. **Azure OpenAI Service** deployed with GPT model

## 🎯 Quick Deployment Options

### Option 1: Azure CLI Deployment (Recommended)

```bash
# 1. Login to Azure
az login

# 2. Create Resource Group (if not exists)
az group create --name sheetsense-rg --location "East US"

# 3. Deploy using ARM template
az deployment group create \
  --resource-group sheetsense-rg \
  --template-file deploy.json \
  --parameters webAppName=sheetsense-ai \
               azureOpenAIEndpoint="https://22112-mh9jpxrc-eastus2.cognitiveservices.azure.com/" \
               azureOpenAIKey="your-api-key-here"
```

### Option 2: Azure Portal Deployment

1. **Create App Service**
   - Go to Azure Portal → Create Resource → Web App
   - Name: `sheetsense-ai-[unique]`
   - Runtime: Python 3.11
   - OS: Linux
   - Plan: Basic B1 (or higher)

2. **Configure Environment Variables**
   ```
   AZURE_OPENAI_ENDPOINT = https://22112-mh9jpxrc-eastus2.cognitiveservices.azure.com/
   AZURE_OPENAI_KEY = your-api-key-here
   AZURE_OPENAI_DEPLOYMENT = gpt-35-turbo
   AZURE_OPENAI_API_VERSION = 2024-12-01-preview
   SCM_DO_BUILD_DURING_DEPLOYMENT = true
   ```

3. **Deploy Code**
   - Use GitHub Actions, Azure DevOps, or ZIP deployment
   - Upload all files including `requirements-deploy.txt`

### Option 3: GitHub Actions Deployment

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure Web App

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements-deploy.txt
    
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'sheetsense-ai'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## 🔧 Configuration Steps

### 1. Update Environment Variables

After deployment, set these in Azure App Service Configuration:

```bash
# Required Variables
AZURE_OPENAI_ENDPOINT=https://22112-mh9jpxrc-eastus2.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your-actual-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-35-turbo
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Optional Variables
FLASK_ENV=production
PORT=8000
```

### 2. Enable Application Insights (Optional)

```bash
az monitor app-insights component create \
  --app sheetsense-ai-insights \
  --location "East US" \
  --resource-group sheetsense-rg \
  --application-type web
```

### 3. Configure Custom Domain (Optional)

```bash
# Add custom domain
az webapp config hostname add \
  --webapp-name sheetsense-ai \
  --resource-group sheetsense-rg \
  --hostname yourdomain.com
```

## 🎯 Deployment Verification

### 1. Health Check
Visit: `https://your-app.azurewebsites.net/api/health`

Expected response:
```json
{
  "status": "healthy",
  "azure_openai": "connected"
}
```

### 2. Test Features
1. **Formula Generator**: Try "Calculate 10% tax on sales"
2. **Data Query**: Upload sample Excel file
3. **Auto Insights**: Generate insights from data
4. **Formula Explainer**: Explain `=SUM(A1:A10)`

## 🔍 Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   # Check logs
   az webapp log tail --name sheetsense-ai --resource-group sheetsense-rg
   ```

2. **OpenAI Connection Issues**
   - Verify API key in App Settings
   - Check endpoint URL format
   - Ensure model deployment name matches

3. **File Upload Issues**
   - Check file size limits (default 100MB)
   - Verify CORS settings if needed

### Performance Optimization

1. **Scale Up**: Upgrade to Standard or Premium tier
2. **Scale Out**: Add multiple instances
3. **CDN**: Enable Azure CDN for static files
4. **Caching**: Implement Redis cache for responses

## 📊 Monitoring & Analytics

### Application Insights Queries

```kusto
// Error tracking
exceptions
| where timestamp > ago(24h)
| summarize count() by type

// Performance monitoring
requests
| where timestamp > ago(1h)
| summarize avg(duration) by bin(timestamp, 5m)
```

### Cost Optimization

1. **Auto-scaling**: Configure based on CPU/memory
2. **Deployment slots**: Use staging slots for testing
3. **Reserved instances**: For production workloads

## 🚀 Production Checklist

- [ ] Environment variables configured
- [ ] HTTPS enabled (automatic)
- [ ] Application Insights enabled
- [ ] Backup strategy configured
- [ ] Monitoring alerts set up
- [ ] Custom domain configured (optional)
- [ ] CDN enabled for static content
- [ ] Auto-scaling rules configured

## 🎉 Success!

Your SheetSense AI is now live on Azure! 

**Demo URL**: `https://sheetsense-ai-[unique].azurewebsites.net`

Perfect for your Azure Codeathon presentation! 🏆