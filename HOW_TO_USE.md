# 🎯 מדריך שימוש מהיר - DevOpsMCP API

## 🌐 איך לפתוח דפדפן ב-VS Code?

### דרך 1: Chrome Browser (מומלץ!)

1. פתחי Chrome
2. הזיני URL: `http://localhost:8090/docs`
3. ⚠️ **הערה:** VS Code Simple Browser לא תומך ב-Swagger UI בגלל CORS

### דרך 2: דרך הקוד

כשהשרת רץ, לחצי `Ctrl + Click` על הקישור בטרמינל:

```
http://127.0.0.1:8090
```

### דרך 3: PowerShell Command

```powershell
Start-Process chrome "http://localhost:8090/docs"
```

---

## 🧪 איך לבדוק את ה-API?

### בדיקה 1: Health Check

**URL:** `POST http://localhost:8090/api/health`

**תגובה:**

```json
{
  "status": "healthy",
  "api": "operational",
  "database": "connected",
  "bug_count": 30
}
```

### בדיקה 2: API Documentation

**URL:** http://localhost:8090/docs

זה יפתח ממשק Swagger UI אינטראקטיבי! (פתחי ב-Chrome)

---

## 📊 איך להריץ שאילתא של Bug Trends?

### אפשרות 1: דרך Swagger UI (הכי קל!)

1. פתחי: http://localhost:8090/docs (ב-Chrome!)
2. לחצי על `POST /api/bugs/get_bug_fix_trends`
3. לחצי `Try it out`
4. ערכי את ה-JSON:

**דוגמה 1 - כל הפרויקטים:**

```json
{
  "days_back": 14
}
```

**דוגמה 2 - לפי project_id (מספר):**

```json
{
  "days_back": 14,
  "project_id": 1
}
```

**דוגמה 3 - לפי project_name (מחרוזת):**

```json
{
  "days_back": 14,
  "project_name": "HotRetailSys"
}
```

5. לחצי `Execute`
6. תראי תוצאות!

---

### אפשרות 2: דרך PowerShell

**כל הפרויקטים:**

```powershell
$body = '{ "days_back": 14 }'
Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body -ContentType 'application/json'
```

**לפי project_id (מספר):**

```powershell
$body = '{ "days_back": 14, "project_id": 1 }'
Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body -ContentType 'application/json'
```

**לפי project_name (מחרוזת):**

```powershell
$body = '{ "days_back": 14, "project_name": "HotRetailSys" }'
Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body -ContentType 'application/json'
```

---

### אפשרות 3: דרך curl

```bash
curl -X POST http://localhost:8090/api/bugs/get_bug_fix_trends \
  -H "Content-Type: application/json" \
  -d '{"days_back": 14, "project_id": 1}'
```

---

## 📋 כל ה-Endpoints הזמינים

### 1️⃣ Health Check

**URL:** `POST http://localhost:8090/api/health`

**Body:** (ריק)

**תגובה:**

```json
{
  "status": "healthy",
  "api": "operational",
  "database": "connected",
  "bug_count": 30
}
```

---

### 2️⃣ Get Projects

**URL:** `POST http://localhost:8090/api/get_projects`

**Body:** (ריק)

**תגובה:**

```json
{
  "projects": [
    {
      "project_id": 1,
      "project_name": "HotRetailSys",
      "description": "Retail management system"
    },
    {
      "project_id": 2,
      "project_name": "PaymentsGateway",
      "description": "Payment processing gateway"
    }
  ],
  "count": 2
}
```

---

### 3️⃣ Get Bug Fix Trends

**URL:** `POST http://localhost:8090/api/bugs/get_bug_fix_trends`

**Body דוגמאות:**

```json
// כל הפרויקטים
{ "days_back": 14 }

// לפי project_id (מספר)
{ "days_back": 14, "project_id": 1 }

// לפי project_name (מחרוזת)
{ "days_back": 14, "project_name": "HotRetailSys" }
```

**תגובה:**

```json
{
  "total_fixed_bugs": 5,
  "daily_aggregation": [...],
  "trend_graph_data": {...},
  "project_id": "1",
  "project_name": "HotRetailSys",
  "period_start": "2025-11-09",
  "period_end": "2025-11-23"
}
```

---

### 4️⃣ Get Bugs Summary

**URL:** `POST http://localhost:8090/api/bugs/get_bugs_summary`

**Body:**

```json
{
  "status": "Closed",
  "limit": 10
}
```

**פרמטרים:**

- `status` (אופציונלי): "Closed", "Open", "In Progress"
- `limit` (אופציונלי): מספר התוצאות (ברירת מחדל: 10)

**תגובה:**

```json
{
  "bugs": [
    {
      "bug_id": 16,
      "azure_bug_id": "12145",
      "severity": "Medium",
      "status": "Closed",
      "fixed_by": "Bob Brown",
      "fixed_date": "2025-11-11",
      "notes": "..."
    }
  ],
  "count": 3,
  "limit": 10,
  "status_filter": "Closed"
}
```

---

## ❓ שאלות נפוצות

### ש: מה זה project_id ו-project_name?

**ת:** שני פרמטרים אופציונליים לסינון לפי פרויקט:

- **project_id** (INT) - מספר הפרויקט: `1` או `2`
- **project_name** (STRING) - שם הפרויקט: `"HotRetailSys"` או `"PaymentsGateway"`

**אפשר לשלוח:**

- ללא פילטר: `{"days_back": 14}` ← כל הפרויקטים
- עם project_id: `{"days_back": 14, "project_id": 1}` ← רק HotRetailSys
- עם project_name: `{"days_back": 14, "project_name": "PaymentsGateway"}` ← רק PaymentsGateway

### ש: איזה פרויקטים קיימים במסד הנתונים?

**ת:** יש 2 פרויקטים:

- **HotRetailSys** (project_id: 1) - 5 bugs
- **PaymentsGateway** (project_id: 2) - 3 bugs

### ש: למה קיבלתי שגיאת 500?

**ת:** בעיה נפתרה! הייתה בעיה בקוד שתיקנו.

### ש: איך אני יודעת שהשרת רץ?

**ת:** תראי בטרמינל:

```
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### ש: איך עוצרים את השרת?

**ת:** לחצי `Ctrl + C` בטרמינל

---

## 🎨 תוצאה לדוגמה

כשתריצי את השאילתא, תקבלי משהו כזה:

**דוגמה 1 - כל הפרויקטים:**

```json
{
  "total_fixed_bugs": 8,
  "daily_aggregation": [
    {"date": "2025-11-06", "fixed_count": 2},
    {"date": "2025-11-07", "fixed_count": 1},
    {"date": "2025-11-08", "fixed_count": 3},
    {"date": "2025-11-09", "fixed_count": 0},
    {"date": "2025-11-10", "fixed_count": 1},
    {"date": "2025-11-11", "fixed_count": 1}
  ],
  "trend_graph_data": {
    "labels": ["2025-11-06", "2025-11-07", ...],
    "values": [2, 1, 3, 0, 1, 1]
  },
  "sql_query": "SELECT DATE(FixedDate) as FixDate...",
  "period_start": "2025-11-09",
  "period_end": "2025-11-23",
  "project_id": null,
  "project_name": null
}
```

**דוגמה 2 - פרויקט HotRetailSys:**

```json
{
  "total_fixed_bugs": 5,
  "project_id": "1",
  "project_name": "HotRetailSys",
  ...
}
```

---

## 🚀 הרצת השרת מחדש

```powershell
cd C:\DevOpsMCP
$env:PYTHONPATH = "C:\DevOpsMCP"
$env:PORT = 8090
python -m app.main_with_db
```

ואז פתחי ב-Chrome: http://localhost:8090/docs

---

## 💡 טיפים

1. **תמיד פתחי את Swagger UI ב-Chrome** (לא ב-VS Code Simple Browser)
2. ה-API עובד עם **SQLite** ויש בו 30 bugs אמיתיים
3. כל ה-endpoints הם **POST** (לא GET)
4. השאירי את השרת רץ בזמן הפיתוח
5. רענני את הדפדפן אם עשית שינויים
6. בדקי את הלוגים בטרמינל אם יש בעיה
7. השתמשי ב-`days_back: 14` כדי לראות את כל הבאגים (הם מתאריך 6-11 בנובמבר)

---

**בהצלחה!** 🎉
יש עוד שאלות? אני כאן!
