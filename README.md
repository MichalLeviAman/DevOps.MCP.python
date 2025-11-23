# DevOpsMCP - Model Context Protocol API

**DevOpsMCP** is a production-ready MCP (Model Context Protocol) API service built with **FastAPI** and **Python**, designed for DevOps analytics, bug tracking, and automation workflows. It integrates with **Azure SQL Database** for cloud-native data storage.

## 🚀 Features

- **FastAPI Framework** - High-performance async API
- **Azure SQL Database** - Cloud-native database integration
- **Modular Architecture** - Clean separation of concerns
- **OpenAPI Documentation** - Auto-generated API docs
- **MCP Compliance** - Full Model Context Protocol support
- **Docker Ready** - Containerized deployment
- **Production Ready** - Error handling, logging, and validation

## 📋 Current Actions

### 1. GetBugFixTrends

**Endpoint:** `POST /api/bugs/get_bug_fix_trends`

Analyzes bug fix trends over a specified time period.

**Input:**

- `days_back` (integer, default: 10) - Number of days to analyze
- `project_id` (string, optional) - Filter by project ID

**Output:**

- Total fixed bugs count
- Daily aggregation breakdown
- Trend graph data for visualization
- SQL query details
- Period start/end dates

## 🛠️ Technology Stack

- **Python 3.11**
- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **pyodbc** - Azure SQL connectivity
- **Uvicorn** - ASGI server
- **Docker** - Containerization

## 📦 Project Structure

```
DevOpsMCP/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection management
│   ├── models/
│   │   ├── __init__.py
│   │   └── bug.py           # Bug database models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── bugs.py          # Bug-related endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── bug_schemas.py   # Request/response schemas
│   └── services/
│       ├── __init__.py
│       └── bug_service.py   # Business logic layer
├── tests/
│   ├── __init__.py
│   └── test_bugs.py         # Unit tests
├── .env.example             # Environment variables template
├── .gitignore
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── schema.sql              # Database schema
├── mcp.json                # MCP configuration
└── README.md
```

## 🔧 Local Setup

### Prerequisites

- Python 3.11 or higher
- Azure SQL Database instance
- ODBC Driver 18 for SQL Server

### Installation Steps

1. **Clone or download the project:**

```powershell
cd C:\DevOpsMCP
```

2. **Create virtual environment:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies:**

```powershell
pip install -r requirements.txt
```

4. **Configure environment variables:**

```powershell
cp .env.example .env
```

Edit `.env` with your Azure SQL credentials:

```env
DB_HOST=your-server.database.windows.net
DB_NAME=your-database-name
DB_USER=your-username
DB_PASS=your-password
DB_PORT=1433
```

5. **Set up database schema:**

Connect to your Azure SQL Database and run:

```powershell
# Using Azure Data Studio or SQL Server Management Studio
# Execute the contents of schema.sql
```

Or use sqlcmd:

```powershell
sqlcmd -S your-server.database.windows.net -d your-database-name -U your-username -P your-password -i schema.sql
```

6. **Run the application:**

```powershell
python -m app.main
```

Or use uvicorn directly:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the API:**

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## 🐳 Docker Deployment

### Build Docker Image

```powershell
docker build -t devopsmcp:latest .
```

### Run Container

```powershell
docker run -d `
  --name devopsmcp `
  -p 8000:8000 `
  -e DB_HOST=your-server.database.windows.net `
  -e DB_NAME=your-database-name `
  -e DB_USER=your-username `
  -e DB_PASS=your-password `
  -e DB_PORT=1433 `
  devopsmcp:latest
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
```

Run:

```powershell
docker-compose up -d
```

## ☁️ Azure Deployment

### Option 1: Azure App Service

1. **Create App Service:**

```powershell
az webapp create `
  --resource-group your-rg `
  --plan your-plan `
  --name devopsmcp `
  --runtime "PYTHON:3.11"
```

2. **Configure environment variables:**

```powershell
az webapp config appsettings set `
  --resource-group your-rg `
  --name devopsmcp `
  --settings `
    DB_HOST=your-server.database.windows.net `
    DB_NAME=your-database-name `
    DB_USER=your-username `
    DB_PASS=your-password
```

3. **Deploy code:**

```powershell
az webapp up --name devopsmcp
```

### Option 2: Azure Container Instances

1. **Build and push image to Azure Container Registry:**

```powershell
az acr build `
  --registry your-acr `
  --image devopsmcp:latest `
  --file Dockerfile .
```

2. **Deploy container:**

```powershell
az container create `
  --resource-group your-rg `
  --name devopsmcp `
  --image your-acr.azurecr.io/devopsmcp:latest `
  --cpu 1 `
  --memory 1 `
  --ports 8000 `
  --environment-variables `
    DB_HOST=your-server.database.windows.net `
    DB_NAME=your-database-name
```

### Option 3: Azure Kubernetes Service (AKS)

Create Kubernetes manifests and deploy using `kubectl`.

## 🌐 Public Exposure Options

### Option 1: ngrok (Development/Testing)

1. **Install ngrok:**

```powershell
choco install ngrok
```

2. **Expose local server:**

```powershell
ngrok http 8000
```

3. **Update `mcp.json` with ngrok URL:**

```json
{
  "url": "https://your-subdomain.ngrok.io/openapi.json"
}
```

### Option 2: Azure App Service (Production)

Your App Service will have a public URL:

```
https://devopsmcp.azurewebsites.net
```

Update `mcp.json`:

```json
{
  "url": "https://devopsmcp.azurewebsites.net/openapi.json"
}
```

### Option 3: Custom Domain

Configure custom domain in Azure and update DNS settings.

## 🔌 ChatGPT MCP Connector Setup

### Step 1: Ensure API is Publicly Accessible

Your API must be accessible via a public URL (ngrok, Azure, etc.)

### Step 2: Update mcp.json

Ensure `mcp.json` contains the correct public URL:

```json
{
  "name": "DevOpsMCP",
  "version": "1.0.1",
  "type": "openapi",
  "url": "https://your-public-url/openapi.json",
  "actions": [
    {
      "name": "get_bug_fix_trends",
      "endpoint": "/api/bugs/get_bug_fix_trends",
      "method": "POST"
    }
  ]
}
```

### Step 3: Configure in ChatGPT

1. Open ChatGPT
2. Go to Settings → Beta Features
3. Enable "MCP Connector" (if available)
4. Add new MCP connection:
   - **Name:** DevOpsMCP
   - **Type:** OpenAPI
   - **URL:** `https://your-public-url/openapi.json`
   - **Environment Variables:** Configure from `.env` values

### Step 4: Test the Connection

In ChatGPT, try:

```
"Use DevOpsMCP to get bug fix trends for the last 14 days"
```

ChatGPT should invoke the `get_bug_fix_trends` action and return results.

## 🧪 Testing

### Run Unit Tests

```powershell
pytest tests/ -v
```

### Run with Coverage

```powershell
pytest tests/ --cov=app --cov-report=html
```

### Manual API Testing

Using curl:

```powershell
curl -X POST http://localhost:8000/api/bugs/get_bug_fix_trends `
  -H "Content-Type: application/json" `
  -d '{"days_back": 14, "project_id": "PROJ001"}'
```

Using PowerShell:

```powershell
$body = @{
    days_back = 14
    project_id = "PROJ001"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/bugs/get_bug_fix_trends `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

## 📊 Sample Database Data

To test the API with sample data, run this SQL:

```sql
INSERT INTO Bugs (Title, ProjectId, CreatedAt, ClosedAt, Status)
VALUES
    ('Login page crash', 'PROJ001', DATEADD(DAY, -15, GETDATE()), DATEADD(DAY, -10, GETDATE()), 'Closed'),
    ('API timeout error', 'PROJ001', DATEADD(DAY, -12, GETDATE()), DATEADD(DAY, -8, GETDATE()), 'Closed'),
    ('UI alignment issue', 'PROJ001', DATEADD(DAY, -9, GETDATE()), DATEADD(DAY, -5, GETDATE()), 'Closed'),
    ('Database connection', 'PROJ002', DATEADD(DAY, -7, GETDATE()), DATEADD(DAY, -3, GETDATE()), 'Closed'),
    ('Memory leak', 'PROJ001', DATEADD(DAY, -5, GETDATE()), DATEADD(DAY, -2, GETDATE()), 'Closed'),
    ('Security vulnerability', 'PROJ001', DATEADD(DAY, -3, GETDATE()), DATEADD(DAY, -1, GETDATE()), 'Closed'),
    ('Performance degradation', 'PROJ002', DATEADD(DAY, -2, GETDATE()), NULL, 'Open');
```

## 📝 API Validation Checklist

- [ ] API is accessible at public URL
- [ ] `/openapi.json` returns valid OpenAPI schema
- [ ] `/docs` shows Swagger UI
- [ ] Database connection is successful
- [ ] POST `/api/bugs/get_bug_fix_trends` returns data
- [ ] `mcp.json` is correctly configured
- [ ] Environment variables are set
- [ ] ChatGPT can connect to MCP endpoint

## 🔒 Security Considerations

- **Never commit `.env` file** - Use `.env.example` as template
- **Use Azure Key Vault** - Store secrets securely in production
- **Enable SSL/TLS** - Always use HTTPS in production
- **Restrict CORS origins** - Don't use `allow_origins=["*"]` in production
- **Use managed identities** - For Azure service authentication
- **Enable SQL firewall rules** - Restrict database access

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure SQL Database](https://docs.microsoft.com/azure/azure-sql/)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [ngrok Documentation](https://ngrok.com/docs)

## 🤝 Contributing

Future enhancements:

- Additional bug analysis endpoints
- Integration with Azure DevOps API
- Real-time bug tracking webhooks
- Authentication & authorization
- Rate limiting
- Caching layer

## 📄 License

MIT License - Feel free to use and modify as needed.

## 👤 Author

DevOpsMCP Development Team

---

**Version:** 1.0.1  
**Last Updated:** November 20, 2025
