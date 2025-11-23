# 🚀 DevOpsMCP - Quick Deployment Guide

## 🎯 מה יש לנו?

✅ **5 פרויקטים:**
- HotRetailSys (Project ID: 1)
- PaymentsGateway (Project ID: 2)
- MobileApp (Project ID: 3)
- DataWarehouse (Project ID: 4)
- CloudInfra (Project ID: 5)

✅ **55 באגים** עם תאריכים מגוונים (אוגוסט-נובמבר 2025)

✅ **4 Endpoints:**
- POST /api/health
- POST /api/get_projects
- POST /api/bugs/get_bug_fix_trends
- POST /api/bugs/get_bugs_summary

---

## 🚀 העלאה ל-Google Cloud Run

### דרך 1: סקריפט אוטומטי (הכי קל!)

```powershell
cd C:\DevOpsMCP
.\deploy-cloudrun.ps1
```

הסקריפט יעשה הכל בשבילך!

### דרך 2: פקודה ידנית

```powershell
cd C:\DevOpsMCP

# וודא שהתחברת ל-Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# העלה ל-Cloud Run
gcloud run deploy devopsmcp `
  --source . `
  --region us-central1 `
  --allow-unauthenticated `
  --memory 512Mi `
  --timeout 300
```

**זה הכל!** תקבל URL כמו:
```
https://devopsmcp-xxxxx-uc.a.run.app
```

---

## 🔗 חיבור ל-ChatGPT

### שלב 1: בדוק שהשרות עובד

```powershell
$url = "https://devopsmcp-xxxxx-uc.a.run.app"

# Health check
Invoke-RestMethod -Uri "$url/api/health" -Method POST

# Get projects
Invoke-RestMethod -Uri "$url/api/get_projects" -Method POST
```

### שלב 2: עדכן mcp.json

ערוך את `mcp.json` ושנה את השורה:
```json
"url": "http://localhost:8090/openapi.json"
```

ל:
```json
"url": "https://devopsmcp-xxxxx-uc.a.run.app/openapi.json"
```

### שלב 3: חבר ל-ChatGPT

1. פתח **ChatGPT** → **Settings**
2. לחץ על **Apps & Connectors**
3. לחץ על **"Add Connector"**
4. בחר **"OpenAPI"**
5. הזן:
   ```
   https://devopsmcp-xxxxx-uc.a.run.app/openapi.json
   ```
6. לחץ **"Import"**
7. אשר את ה-Actions

---

## 🧪 בדיקה ב-ChatGPT

נסה את הפקודות הבאות:

```
1. "מה הפרויקטים הזמינים?"
2. "הראה לי טרנד של באגים שתוקנו ב-30 הימים האחרונים"
3. "כמה באגים תוקנו בפרויקט MobileApp?"
4. "תן לי סיכום של הבאגים הפעילים"
5. "מה סטטוס ה-API?"
```

---

## 📊 דוגמאות שימוש

### דוגמה 1: כל הפרויקטים
```
User: "מה הפרויקטים הזמינים?"
ChatGPT: יש 5 פרויקטים:
1. HotRetailSys - Core retail operations
2. PaymentsGateway - Payment processing
3. MobileApp - Mobile application
4. DataWarehouse - Data warehouse and BI
5. CloudInfra - Cloud infrastructure
```

### דוגמה 2: טרנד באגים
```
User: "הראה לי טרנד באגים ב-30 ימים"
ChatGPT: נמצאו 25 באגים שתוקנו ב-30 הימים האחרונים:
- 6 באגים ב-HotRetailSys
- 4 באגים ב-PaymentsGateway
- 8 באגים ב-MobileApp
- 4 באגים ב-DataWarehouse
- 3 באגים ב-CloudInfra
```

### דוגמה 3: פרויקט ספציפי
```
User: "כמה באגים תוקנו ב-MobileApp?"
ChatGPT: בפרויקט MobileApp תוקנו 6 באגים ב-30 הימים האחרונים.
התאריכים: ספטמבר-נובמבר 2025
```

---

## 💰 עלויות

**Google Cloud Run - Free Tier:**
- ✅ 2 מיליון בקשות חינם בחודש
- ✅ 360,000 GB-seconds חינם
- ✅ 180,000 vCPU-seconds חינם

**לרוב המקרים זה לגמרי חינם!**

---

## 📚 מסמכים נוספים

- **CLOUD_RUN_DEPLOY.md** - מדריך פריסה מפורט
- **HOW_TO_USE.md** - מדריך שימוש ב-API
- **QUICKSTART.md** - התחלה מהירה

---

## 🔧 ניהול השרות

### צפייה בלוגים
```powershell
gcloud run services logs read devopsmcp --region us-central1
```

### עדכון השרות
```powershell
gcloud run deploy devopsmcp --source . --region us-central1
```

### מחיקת השרות
```powershell
gcloud run services delete devopsmcp --region us-central1
```

---

## 🎉 סיימת!

השרות שלך זמין ומחובר ל-ChatGPT!

**URL שלך:**
```
https://devopsmcp-xxxxx-uc.a.run.app
```

**Swagger UI:**
```
https://devopsmcp-xxxxx-uc.a.run.app/docs
```

**OpenAPI JSON:**
```
https://devopsmcp-xxxxx-uc.a.run.app/openapi.json
```

---

**בהצלחה! 🚀**
