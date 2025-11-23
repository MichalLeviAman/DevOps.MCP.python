# ⚡ התחלה מהירה - DevOpsMCP

## 🎯 מה יש לך?

API פשוט שעובד ללא מסד נתונים, מוכן לפריסה!

---

## 🏃‍♀️ הרצה מקומית (5 דקות)

```powershell
# 1. התקנת חבילות
cd C:\DevOpsMCP
pip install -r requirements-cloudrun.txt

# 2. הרצת השרת
python -m app.main_demo

# 3. פתיחת הדפדפן
# http://localhost:8080/docs
```

---

## ☁️ פריסה ל-Google Cloud Run (10 דקות)

### דרישה: Google Cloud SDK
הורדה: https://cloud.google.com/sdk/docs/install

### פריסה בפקודה אחת:

```powershell
# התחברות (פעם אחת)
gcloud auth login

# הפעלת APIs (פעם אחת)
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# פריסה!
cd C:\DevOpsMCP
gcloud run deploy devopsmcp --source . --region us-central1 --allow-unauthenticated --port 8080
```

**זהו!** 🎉

תקבלי URL ציבורי כמו:
```
https://devopsmcp-xxxxx-uc.a.run.app
```

---

## ✅ בדיקה

```powershell
# Health check
curl https://devopsmcp-xxxxx-uc.a.run.app/health

# API Docs
# פתחי בדפדפן: https://devopsmcp-xxxxx-uc.a.run.app/docs

# Test API
$url = "https://devopsmcp-xxxxx-uc.a.run.app/api/bugs/get_bug_fix_trends"
$body = '{"days_back": 7, "project_id": "TEST"}'
Invoke-RestMethod -Uri $url -Method POST -Body $body -ContentType "application/json"
```

---

## 📝 עדכון mcp.json

החליפי את ה-URL ב-`mcp.json`:

```json
{
  "url": "https://devopsmcp-xxxxx-uc.a.run.app/openapi.json"
}
```

---

## 💡 טיפים

- **עלות**: חינמי לשימוש בסיסי (2M בקשות/חודש)
- **עדכון**: הריצי שוב `gcloud run deploy` לאחר שינויים
- **לוגים**: `gcloud run services logs read devopsmcp --region us-central1`

---

למדריך מלא ראי: `DEPLOY_GUIDE_HE.md`
