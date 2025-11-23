# מדריך פריסה ל-Google Cloud Run

## דרישות מוקדמות

1. חשבון Google Cloud
2. Google Cloud SDK מותקן: https://cloud.google.com/sdk/docs/install

## שלבי הפריסה

### שלב 1: התחברות ל-Google Cloud

```powershell
# התחברות
gcloud auth login

# הגדרת פרויקט (החליפי YOUR_PROJECT_ID בשם הפרויקט שלך)
gcloud config set project YOUR_PROJECT_ID
```

### שלב 2: הפעלת Cloud Run API

```powershell
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### שלב 3: פריסה ל-Cloud Run (הכי קל!)

```powershell
cd C:\DevOpsMCP

# פריסה ישירה מקוד המקור
gcloud run deploy devopsmcp `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --port 8080 `
  --set-env-vars "DB_HOST=your-server.database.windows.net,DB_NAME=your-db,DB_USER=your-user,DB_PASS=your-password,DB_PORT=1433"
```

### שלב 4: קבלת ה-URL הציבורי

לאחר הפריסה, תקבלי URL כגון:
```
https://devopsmcp-xxx-uc.a.run.app
```

### שלב 5: עדכון mcp.json

עדכני את הקובץ `mcp.json` עם ה-URL החדש:

```json
{
  "url": "https://devopsmcp-xxx-uc.a.run.app/openapi.json"
}
```

## אפשרות חלופית: פריסה עם Docker

```powershell
# בניית Image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/devopsmcp

# פריסה
gcloud run deploy devopsmcp `
  --image gcr.io/YOUR_PROJECT_ID/devopsmcp `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --port 8080
```

## בדיקת הפריסה

```powershell
# בדיקת Health
curl https://devopsmcp-xxx-uc.a.run.app/health

# צפייה ב-API Docs
# פתחי בדפדפן: https://devopsmcp-xxx-uc.a.run.app/docs
```

## הגדרת משתני סביבה (אם יש מסד נתונים אמיתי)

```powershell
gcloud run services update devopsmcp `
  --region us-central1 `
  --set-env-vars "DB_HOST=your-actual-host,DB_NAME=your-db,DB_USER=your-user,DB_PASS=your-password"
```

## צפייה בלוגים

```powershell
gcloud run services logs read devopsmcp --region us-central1
```

## עלויות

- Cloud Run חינמי עד 2 מיליון בקשות בחודש
- אתה משלם רק כשהשירות בשימוש
- עלות מינימלית מאוד לשימוש בסיסי

## פתרון בעיות

אם יש שגיאה בפריסה:
1. בדקי שהפרויקט קיים: `gcloud projects list`
2. בדקי שאת מחוברת: `gcloud auth list`
3. צפי בלוגים: `gcloud run services logs read devopsmcp`
