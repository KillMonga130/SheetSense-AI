# SheetSense AI - Quick Azure Deployment Script
# Run this in PowerShell with Azure CLI installed

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName = "sheetsense-rg",
    
    [Parameter(Mandatory=$true)]
    [string]$AppName = "sheetsense-ai",
    
    [Parameter(Mandatory=$true)]
    [string]$OpenAIEndpoint,
    
    [Parameter(Mandatory=$true)]
    [string]$OpenAIKey,
    
    [string]$Location = "East US"
)

Write-Host "🚀 Deploying SheetSense AI to Azure..." -ForegroundColor Cyan

# Check if logged in to Azure
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$account = az account show 2>$null
if (-not $account) {
    Write-Host "Please login to Azure first:" -ForegroundColor Red
    Write-Host "az login" -ForegroundColor White
    exit 1
}

# Create Resource Group
Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location

# Deploy ARM template
Write-Host "Deploying Azure resources..." -ForegroundColor Yellow
$deployResult = az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file deploy.json `
    --parameters webAppName=$AppName `
                 azureOpenAIEndpoint=$OpenAIEndpoint `
                 azureOpenAIKey=$OpenAIKey `
    --output json | ConvertFrom-Json

if ($deployResult.properties.provisioningState -eq "Succeeded") {
    $webAppUrl = $deployResult.properties.outputs.webAppUrl.value
    Write-Host "✅ Deployment successful!" -ForegroundColor Green
    Write-Host "🌐 Your app is available at: $webAppUrl" -ForegroundColor Cyan
    
    # Deploy code
    Write-Host "Deploying application code..." -ForegroundColor Yellow
    
    # Create ZIP file for deployment
    $zipPath = "sheetsense-ai.zip"
    Compress-Archive -Path "app.py", "requirements-deploy.txt", "startup.sh", "frontend/*" -DestinationPath $zipPath -Force
    
    # Deploy ZIP
    $appNameUnique = $deployResult.properties.outputs.webAppUrl.value.Split('.')[0].Replace('https://', '')
    az webapp deployment source config-zip --resource-group $ResourceGroupName --name $appNameUnique --src $zipPath
    
    # Clean up
    Remove-Item $zipPath
    
    Write-Host "🎉 SheetSense AI is now live!" -ForegroundColor Green
    Write-Host "Demo URL: $webAppUrl" -ForegroundColor White
    Write-Host "Health Check: $webAppUrl/api/health" -ForegroundColor White
    
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host $deployResult.properties.error.message -ForegroundColor Red
}

Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Test your app at the URL above" -ForegroundColor White
Write-Host "2. Upload sample Excel file and try features" -ForegroundColor White
Write-Host "3. Ready for your Azure Codeathon demo! 🏆" -ForegroundColor White