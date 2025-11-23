# DevOpsMCP - Google Cloud Run Deployment Script
# This script automates the deployment to Google Cloud Run

param(
    [string]$ProjectId = "",
    [string]$Region = "us-central1",
    [string]$ServiceName = "devopsmcp"
)

Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   DevOpsMCP - Cloud Run Deployment           ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Check if gcloud is installed
try {
    $gcloudVersion = gcloud version 2>&1 | Select-String "Google Cloud SDK"
    Write-Host "✅ Google Cloud SDK found" -ForegroundColor Green
} catch {
    Write-Host "❌ Google Cloud SDK not found!" -ForegroundColor Red
    Write-Host "   Please install from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Get or set project ID
if ($ProjectId -eq "") {
    $ProjectId = gcloud config get-value project 2>$null
    if ($ProjectId -eq "") {
        Write-Host "❌ No project ID specified!" -ForegroundColor Red
        Write-Host "   Please run: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "`n📋 Deployment Configuration:" -ForegroundColor Cyan
Write-Host "   Project ID: $ProjectId" -ForegroundColor White
Write-Host "   Region: $Region" -ForegroundColor White
Write-Host "   Service Name: $ServiceName`n" -ForegroundColor White

# Confirm deployment
$confirm = Read-Host "Continue with deployment? (Y/N)"
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "`n❌ Deployment cancelled" -ForegroundColor Red
    exit 0
}

Write-Host "`n🚀 Starting deployment...`n" -ForegroundColor Yellow

# Enable required APIs
Write-Host "1️⃣  Enabling required APIs..." -ForegroundColor Cyan
gcloud services enable run.googleapis.com cloudbuild.googleapis.com --project=$ProjectId
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ APIs enabled`n" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to enable APIs" -ForegroundColor Red
    exit 1
}

# Deploy to Cloud Run
Write-Host "2️⃣  Deploying to Cloud Run..." -ForegroundColor Cyan
Write-Host "   This may take 3-5 minutes...`n" -ForegroundColor Yellow

gcloud run deploy $ServiceName `
    --source . `
    --platform managed `
    --region $Region `
    --allow-unauthenticated `
    --memory 512Mi `
    --timeout 300 `
    --project $ProjectId

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Deployment successful!`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ Deployment failed!" -ForegroundColor Red
    exit 1
}

# Get service URL
Write-Host "3️⃣  Getting service URL..." -ForegroundColor Cyan
$serviceUrl = gcloud run services describe $ServiceName --region $Region --project $ProjectId --format="value(status.url)"

Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ✅ Deployment Complete!                      ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "🌐 Service URL:" -ForegroundColor Yellow
Write-Host "   $serviceUrl`n" -ForegroundColor White

Write-Host "📊 OpenAPI URL:" -ForegroundColor Yellow
Write-Host "   $serviceUrl/openapi.json`n" -ForegroundColor White

Write-Host "📝 Swagger UI:" -ForegroundColor Yellow
Write-Host "   $serviceUrl/docs`n" -ForegroundColor White

Write-Host "🧪 Testing endpoints..." -ForegroundColor Cyan

# Test health endpoint
try {
    $health = Invoke-RestMethod -Uri "$serviceUrl/api/health" -Method POST -TimeoutSec 10
    Write-Host "✅ Health check: OK" -ForegroundColor Green
    Write-Host "   Bugs in database: $($health.bug_count)" -ForegroundColor White
} catch {
    Write-Host "⚠️  Health check failed (service may still be starting)" -ForegroundColor Yellow
}

# Test projects endpoint
try {
    $projects = Invoke-RestMethod -Uri "$serviceUrl/api/get_projects" -Method POST -TimeoutSec 10
    Write-Host "✅ Projects endpoint: OK" -ForegroundColor Green
    Write-Host "   Available projects: $($projects.count)" -ForegroundColor White
} catch {
    Write-Host "⚠️  Projects endpoint failed" -ForegroundColor Yellow
}

Write-Host "`n╔═══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Next Steps:                                  ║" -ForegroundColor Yellow
Write-Host "╚═══════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "1️⃣  Open Swagger UI in browser:" -ForegroundColor White
Write-Host "   Start-Process chrome `"$serviceUrl/docs`"`n" -ForegroundColor Gray

Write-Host "2️⃣  Update mcp.json with service URL:" -ForegroundColor White
Write-Host "   Edit mcp.json and replace the URL with:" -ForegroundColor Gray
Write-Host "   $serviceUrl`n" -ForegroundColor Gray

Write-Host "3️⃣  Connect to ChatGPT:" -ForegroundColor White
Write-Host "   - Go to ChatGPT → Settings → Apps & Connectors" -ForegroundColor Gray
Write-Host "   - Add Connector → OpenAPI" -ForegroundColor Gray
Write-Host "   - Enter URL: $serviceUrl/openapi.json`n" -ForegroundColor Gray

Write-Host "4️⃣  View logs:" -ForegroundColor White
Write-Host "   gcloud run services logs read $ServiceName --region $Region`n" -ForegroundColor Gray

Write-Host "✨ Deployment completed successfully!`n" -ForegroundColor Green
