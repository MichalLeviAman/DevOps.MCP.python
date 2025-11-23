# 🚀 מדריך פריסה ל-Google Cloud Run - פשוט וקל!

## ✅ מה יש לך עכשיו?

API שעובד מקומית על http://localhost:8080
כל הקבצים מוכנים לפריסה!

---

## 📋 שלב 1: הכנה (חד פעמי)

### 1.1 התקנת Google Cloud SDK

הורידי והתקיני מכאן: https://cloud.google.com/sdk/docs/install

או דרך PowerShell:
```powershell
# הורדה
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")

# התקנה
& $env:Temp\GoogleCloudSDKInstaller.exe
```

### 1.2 התחברות לחשבון Google

```powershell
# התחברות
gcloud auth login

# זה יפתח דפדפן - התחברי עם חשבון Google שלך
```

### 1.3 יצירת פרויקט חדש (או בחירת קיים)

```powershell
# יצירת פרויקט חדש
gcloud projects create devopsmcp-project --name="DevOpsMCP"

# הגדרת הפרויקט כפעיל
gcloud config set project devopsmcp-project

# או רשימת פרויקטים קיימים:
gcloud projects list
```

### 1.4 הפעלת Cloud Run API

```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## 🚀 שלב 2: פריסה ל-Cloud Run (פקודה אחת!)

```powershell
cd C:\DevOpsMCP

gcloud run deploy devopsmcp `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --port 8080
```

זהו! זה הכל! 🎉

### מה קורה כעת?
1. Google Cloud בונה את ה-Docker image אוטומטית
2. מעלה אותו ל-Container Registry
3. מפרס אותו ל-Cloud Run
4. נותן לך URL ציבורי!

---

## 🌐 שלב 3: קבלת ה-URL הציבורי

לאחר הפריסה, תקבלי משהו כזה:
```
Service [devopsmcp] revision [devopsmcp-00001] has been deployed 
and is serving 100 percent of traffic.
Service URL: https://devopsmcp-xxxxx-uc.a.run.app
```

העתיקי את ה-URL!

---

## 🧪 שלב 4: בדיקה שהשירות עובד

### בדיקת Health
```powershell
curl https://devopsmcp-xxxxx-uc.a.run.app/health
```

### פתיחת ה-API Docs
פשוט פתחי בדפדפן:
```
https://devopsmcp-xxxxx-uc.a.run.app/docs
```

### בדיקת ה-API
```powershell
$url = "https://devopsmcp-xxxxx-uc.a.run.app/api/bugs/get_bug_fix_trends"
$body = @{ days_back = 14; project_id = "TEST" } | ConvertTo-Json

Invoke-RestMethod -Uri $url -Method POST -Body $body -ContentType "application/json"
```

---

## 📝 שלב 5: עדכון mcp.json

עכשיו עדכני את הקובץ `mcp.json` עם ה-URL הציבורי שלך:

```json
{
  "name": "DevOpsMCP",
  "description": "MCP API for DevOps Analytics",
  "version": "1.0.1",
  "type": "openapi",
  "url": "https://devopsmcp-xxxxx-uc.a.run.app/openapi.json",
  "actions": [
    {
      "name": "get_bug_fix_trends",
      "endpoint": "/api/bugs/get_bug_fix_trends",
      "method": "POST"
    }
  ]
}
```

---

## 🔄 עדכון הפריסה (אם שינית משהו בקוד)

פשוט הריצי שוב את אותה פקודה:
```powershell
cd C:\DevOpsMCP
gcloud run deploy devopsmcp --source . --region us-central1
```

---

## 💰 עלויות

- **חינמי** עד 2 מיליון בקשות בחודש
- **חינמי** עד 360,000 GB-שניות בחודש
- משלמים רק כשיש שימוש (serverless)
- לשימוש בסיסי - כמעט תמיד חינם!

---

## 📊 ניטור ולוגים

### צפייה בלוגים
```powershell
gcloud run services logs read devopsmcp --region us-central1 --limit 50
```

### מידע על השירות
```powershell
gcloud run services describe devopsmcp --region us-central1
```

### פתיחת הקונסול
```powershell
gcloud run services browse devopsmcp --region us-central1
```

---

## 🔧 הגדרות נוספות (אופציונלי)

### הגדרת משתני סביבה
אם בעתיד תרצי להוסיף מסד נתונים אמיתי:

```powershell
gcloud run services update devopsmcp `
  --region us-central1 `
  --set-env-vars "DB_HOST=your-db.database.windows.net,DB_NAME=mydb,DB_USER=admin,DB_PASS=password123"
```

### הגדלת זיכרון (אם צריך)
```powershell
gcloud run services update devopsmcp `
  --region us-central1 `
  --memory 512Mi
```

### הגדלת מספר instances
```powershell
gcloud run services update devopsmcp `
  --region us-central1 `
  --max-instances 10
```

---

## 🔌 חיבור ל-ChatGPT MCP Connector

### שלב 1: ודאי שה-API נגיש
פתחי: `https://devopsmcp-xxxxx-uc.a.run.app/openapi.json`
אמורה להופיע תגובה JSON

### שלב 2: הוסיפי ל-ChatGPT
1. פתחי ChatGPT
2. הגדרות → Beta Features
3. הפעילי MCP Connector
4. לחצי Add MCP Connection
5. מלאי:
   - Name: `DevOpsMCP`
   - Type: `OpenAPI`
   - URL: `https://devopsmcp-xxxxx-uc.a.run.app/openapi.json`

### שלב 3: נסי בשיחה
```
"Use DevOpsMCP to get bug fix trends for the last 30 days for project TEST"
```

---

## ❌ פתרון בעיות נפוצות

### בעיה: "Permission denied"
```powershell
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### בעיה: "API not enabled"
```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### בעיה: "Billing not enabled"
- היכנסי ל-Google Cloud Console
- הפעילי Billing Account (צריך כרטיס אשראי, אבל יש 300$ קרדיט חינם)

### בדיקת סטטוס
```powershell
gcloud run services list
```

---

## 🗑️ מחיקת השירות (אם רוצה)

```powershell
gcloud run services delete devopsmcp --region us-central1
```

---

## 📞 עזרה נוספת

- [תיעוד Google Cloud Run](https://cloud.google.com/run/docs)
- [מחשבון עלויות](https://cloud.google.com/products/calculator)
- [דוגמאות קוד](https://github.com/GoogleCloudPlatform/cloud-run-samples)

---

## ✅ סיכום מהיר

```powershell
# 1. התקנת gcloud SDK (פעם אחת)
# הורדה מ: https://cloud.google.com/sdk/docs/install

# 2. התחברות
gcloud auth login
gcloud config set project devopsmcp-project

# 3. הפעלת APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 4. פריסה!
cd C:\DevOpsMCP
gcloud run deploy devopsmcp --source . --region us-central1 --allow-unauthenticated --port 8080

# 5. קבלת URL
# תקבלי משהו כמו: https://devopsmcp-xxxxx-uc.a.run.app

# 6. בדיקה
curl https://devopsmcp-xxxxx-uc.a.run.app/health
```

זהו! בהצלחה! 🚀
