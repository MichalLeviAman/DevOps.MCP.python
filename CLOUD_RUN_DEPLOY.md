# 🚀 מדריך העלאה ל-Google Cloud Run

## 📋 דרישות מקדימות

1. ✅ חשבון Google Cloud Platform
2. ✅ Google Cloud CLI מותקן
3. ✅ Docker Desktop מותקן (אופציונלי - לבדיקה מקומית)

---

## 🔧 שלב 1: הכנת הסביבה

### התקנת Google Cloud CLI

**Windows:**

```powershell
# הורד והתקן מ:
# https://cloud.google.com/sdk/docs/install

# אחרי ההתקנה, אתחל:
gcloud init
```

### התחברות ל-Google Cloud

```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

---

## 📦 שלב 2: בדיקה מקומית (אופציונלי)

אם יש לך Docker, בדוק שהכל עובד:

```powershell
cd C:\DevOpsMCP

# בנה Docker image
docker build -t devopsmcp:test .

# הרץ locally
docker run -p 8080:8080 devopsmcp:test

# בדוק ב:
# http://localhost:8080/docs
```

---

## 🌐 שלב 3: העלאה ל-Cloud Run

### אופציה א': העלאה ישירה (מומלץ!)

```powershell
cd C:\DevOpsMCP

# העלה ל-Cloud Run בפקודה אחת:
gcloud run deploy devopsmcp `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 512Mi `
  --timeout 300

# Cloud Run יבנה את ה-Docker image ויעלה אותו אוטומטית!
```

### אופציה ב': העלאה דרך Artifact Registry

```powershell
cd C:\DevOpsMCP

# 1. הגדר משתנים
$PROJECT_ID = gcloud config get-value project
$REGION = "us-central1"
$SERVICE_NAME = "devopsmcp"

# 2. צור Artifact Registry repository (פעם אחת)
gcloud artifacts repositories create cloud-run-repo `
  --repository-format=docker `
  --location=$REGION `
  --description="Docker repository for Cloud Run"

# 3. הגדר Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# 4. בנה את ה-Docker image
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-repo/${SERVICE_NAME}:latest .

# 5. העלה ל-Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-repo/${SERVICE_NAME}:latest

# 6. Deploy ל-Cloud Run
gcloud run deploy $SERVICE_NAME `
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-repo/${SERVICE_NAME}:latest `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --memory 512Mi `
  --timeout 300
```

---

## 🎯 שלב 4: קבל את ה-URL

לאחר ההעלאה, תקבל URL כמו:

```
https://devopsmcp-xxxxx-uc.a.run.app
```

בדוק שהשרות רץ:

```powershell
$SERVICE_URL = "https://devopsmcp-xxxxx-uc.a.run.app"

# Health check
Invoke-RestMethod -Uri "$SERVICE_URL/api/health" -Method POST

# Get projects
Invoke-RestMethod -Uri "$SERVICE_URL/api/get_projects" -Method POST
```

---

## 📝 שלב 5: עדכן mcp.json

ערוך את `mcp.json`:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "DevOpsMCP",
    "description": "Azure DevOps Analytics API",
    "version": "1.0.2"
  },
  "servers": [
    {
      "url": "https://devopsmcp-xxxxx-uc.a.run.app",
      "description": "Production Server on Cloud Run"
    }
  ],
  "paths": {
    "/api/health": {
      "post": {
        "summary": "Health Check",
        "operationId": "health",
        "responses": {
          "200": {
            "description": "Service is healthy"
          }
        }
      }
    },
    "/api/get_projects": {
      "post": {
        "summary": "Get Projects",
        "operationId": "get_projects",
        "responses": {
          "200": {
            "description": "List of projects"
          }
        }
      }
    },
    "/api/bugs/get_bug_fix_trends": {
      "post": {
        "summary": "Get Bug Fix Trends",
        "operationId": "get_bug_fix_trends",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "days_back": {
                    "type": "integer",
                    "default": 14
                  },
                  "project_id": {
                    "type": "integer"
                  },
                  "project_name": {
                    "type": "string"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Bug fix trends data"
          }
        }
      }
    },
    "/api/bugs/get_bugs_summary": {
      "post": {
        "summary": "Get Bugs Summary",
        "operationId": "get_bugs_summary",
        "requestBody": {
          "required": false,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "status": {
                    "type": "string"
                  },
                  "limit": {
                    "type": "integer",
                    "default": 10
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Bugs summary data"
          }
        }
      }
    }
  }
}
```

**או פשוט השתמש ב-OpenAPI URL:**

```
https://devopsmcp-xxxxx-uc.a.run.app/openapi.json
```

---

## 🤖 שלב 6: חיבור ל-ChatGPT

### דרך א': OpenAPI Connector

1. פתח ChatGPT → Settings
2. לחץ על **Apps & Connectors**
3. לחץ על **"Add Connector"**
4. בחר **"OpenAPI"**
5. הזן את ה-URL:
   ```
   https://devopsmcp-xxxxx-uc.a.run.app/openapi.json
   ```
6. לחץ **"Import"**
7. אשר את ה-Actions

### דרך ב': העלאת קובץ mcp.json

1. פתח ChatGPT → Settings
2. לחץ על **Apps & Connectors**
3. לחץ על **"Add Connector"**
4. בחר **"Upload OpenAPI file"**
5. העלה את `mcp.json` (לאחר עדכון ה-URL)
6. אשר את ה-Actions

---

## 🧪 שלב 7: בדיקה ב-ChatGPT

נסה את הפקודות הבאות ב-ChatGPT:

1. **"מה הפרויקטים הזמינים?"**
2. **"הראה לי טרנד של באגים שתוקנו ב-14 הימים האחרונים"**
3. **"כמה באגים תוקנו בפרויקט HotRetailSys?"**
4. **"תן לי סיכום של הבאגים הסגורים"**

---

## 🔧 ניהול השרות

### צפייה בלוגים

```powershell
gcloud run services logs read devopsmcp --region us-central1
```

### עדכון השרות

```powershell
# לאחר שינויים, העלה שוב:
gcloud run deploy devopsmcp --source . --region us-central1
```

### מחיקת השרות

```powershell
gcloud run services delete devopsmcp --region us-central1
```

### הצגת פרטי השרות

```powershell
gcloud run services describe devopsmcp --region us-central1
```

---

## 💰 עלויות

Cloud Run מחייב לפי שימוש:

- **Free Tier**: 2 מיליון בקשות חינם בחודש
- **עלות**: ~$0.40 לכל מיליון בקשות נוספות
- **זיכרון**: 512MB - ~$0.000024 לשנייה

לרוב האפליקציות קטנות - זה **חינם לחלוטין!**

---

## ⚠️ פתרון בעיות

### שגיאה: "Permission denied"

```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### שגיאה: "API not enabled"

```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### שגיאה: "Port 8080 not exposed"

- וודא שב-Dockerfile יש: `EXPOSE 8080`
- וודא שב-CMD יש: `--port ${PORT}`

### שגיאה: "Database file not found"

- וודא ש-`schema_sqlite.sql` מועתק ב-Dockerfile
- וודא שהפקודה `RUN python -c ...` רצה בהצלחה

---

## 🎉 סיימת!

השרות שלך זמין ב:

- **Swagger UI**: https://devopsmcp-xxxxx-uc.a.run.app/docs
- **OpenAPI JSON**: https://devopsmcp-xxxxx-uc.a.run.app/openapi.json
- **Health Check**: https://devopsmcp-xxxxx-uc.a.run.app/api/health

עכשיו אפשר להשתמש בו מ-ChatGPT, מערכות אחרות, או כל יישום שתרצי!

---

## 📚 מקורות נוספים

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [OpenAPI Specification](https://swagger.io/specification/)
- [ChatGPT Custom Actions](https://platform.openai.com/docs/actions)

**בהצלחה! 🚀**
