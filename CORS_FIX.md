# 🌐 מדריך שימוש ב-API - פתרון בעיית CORS

## ❌ הבעיה: CORS Error ב-Simple Browser

כשמנסים להשתמש ב-Swagger UI דרך Simple Browser של VS Code, יש שגיאת CORS כי ה-Simple Browser משתמש בפרוטוקול `vscode-webview://` ולא `http://`.

---

## ✅ פתרון 1: פתיחה בדפדפן רגיל (מומלץ!)

### דרך A: קליק ישיר על הלינק
1. בטרמינל, תראי:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8090 (Press CTRL+C to quit)
   ```
2. לחצי `Ctrl + Click` על `http://0.0.0.0:8090`
3. או פתחי בדפדפן: `http://localhost:8090/docs`

### דרך B: דרך Command Palette
1. לחצי `Ctrl + Shift + P`
2. הקלידי: `Simple Browser: Show`
3. במקום Simple Browser, פתחי Chrome/Edge רגיל
4. הזיני: `http://localhost:8090/docs`

---

## ✅ פתרון 2: שימוש ב-PowerShell (עובד תמיד!)

### בדיקת רשימת פרויקטים
```powershell
Invoke-RestMethod -Uri http://localhost:8090/api/projects
```

**תוצאה:**
```
project_id project_name    description
---------- ------------    -----------
         1 HotRetailSys    Core retail operations project...
         2 PaymentsGateway Payment processing services...
```

### קבלת Bug Fix Trends - כל הפרויקטים
```powershell
$body = '{"days_back": 14}'
Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends `
  -Method POST `
  -Body $body `
  -ContentType 'application/json'
```

### קבלת Bug Fix Trends - פרויקט ספציפי
```powershell
# עבור HotRetailSys
$body = '{"days_back": 14, "project_id": "HotRetailSys"}'
Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends `
  -Method POST `
  -Body $body `
  -ContentType 'application/json'

# עבור PaymentsGateway
$body = '{"days_back": 30, "project_id": "PaymentsGateway"}'
Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends `
  -Method POST `
  -Body $body `
  -ContentType 'application/json'
```

### סקריפט מלא לבדיקה
```powershell
# 1. רשימת פרויקטים
Write-Host "=== PROJECTS ===" -ForegroundColor Green
$projects = Invoke-RestMethod -Uri http://localhost:8090/api/projects
$projects.projects | Format-Table

# 2. Bug trends - כל הפרויקטים
Write-Host "`n=== ALL PROJECTS - LAST 14 DAYS ===" -ForegroundColor Green
$body = '{"days_back": 14}'
$result = Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body -ContentType 'application/json'
Write-Host "Total Fixed: $($result.total_fixed_bugs)" -ForegroundColor Yellow
$result.daily_aggregation | Where-Object { $_.fixed_count -gt 0 } | Format-Table

# 3. Bug trends - HotRetailSys
Write-Host "`n=== HOTRETAILSYS - LAST 14 DAYS ===" -ForegroundColor Green
$body = '{"days_back": 14, "project_id": "HotRetailSys"}'
$result = Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body -ContentType 'application/json'
Write-Host "Total Fixed: $($result.total_fixed_bugs)" -ForegroundColor Yellow
$result.daily_aggregation | Where-Object { $_.fixed_count -gt 0 } | Format-Table
```

---

## ✅ פתרון 3: שימוש ב-curl (אם מותקן)

```bash
# Get projects
curl http://localhost:8090/api/projects

# Get bug trends
curl -X POST http://localhost:8090/api/bugs/get_bug_fix_trends \
  -H "Content-Type: application/json" \
  -d '{"days_back": 14, "project_id": "HotRetailSys"}'
```

---

## 📊 נתוני המסד נתונים

### פרויקטים זמינים:
1. **HotRetailSys** - Core retail operations project
2. **PaymentsGateway** - Payment processing services

### project_id חייב להיות בדיוק כמו בטבלה:
- ✅ `"HotRetailSys"` - נכון
- ❌ `"hotretailsys"` - לא יעבוד
- ❌ `"HOTRETAILSYS"` - לא יעבוד
- ✅ `"PaymentsGateway"` - נכון

או פשוט **השאירי ריק** לכל הפרויקטים!

---

## 🎯 דוגמאות מעשיות

### דוגמה 1: באגים שתוקנו בשבוע האחרון
```powershell
$body = '{"days_back": 7}'
$result = Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends `
  -Method POST -Body $body -ContentType 'application/json'
  
Write-Host "Fixed in last 7 days: $($result.total_fixed_bugs)"
```

### דוגמה 2: באגים בפרויקט ספציפי
```powershell
$body = '{"days_back": 30, "project_id": "HotRetailSys"}'
$result = Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends `
  -Method POST -Body $body -ContentType 'application/json'
  
Write-Host "Project: $($result.project_name)"
Write-Host "Period: $($result.period_start) to $($result.period_end)"
Write-Host "Total Fixed: $($result.total_fixed_bugs)"
```

### דוגמה 3: השוואה בין פרויקטים
```powershell
$body1 = '{"days_back": 30, "project_id": "HotRetailSys"}'
$r1 = Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body1 -ContentType 'application/json'

$body2 = '{"days_back": 30, "project_id": "PaymentsGateway"}'
$r2 = Invoke-RestMethod -Uri http://localhost:8090/api/bugs/get_bug_fix_trends -Method POST -Body $body2 -ContentType 'application/json'

Write-Host "HotRetailSys: $($r1.total_fixed_bugs) bugs fixed"
Write-Host "PaymentsGateway: $($r2.total_fixed_bugs) bugs fixed"
```

---

## 🔧 אם עדיין רוצה להשתמש ב-Swagger UI

פתחי בדפדפן רגיל (Chrome/Edge/Firefox):
```
http://localhost:8090/docs
```

שם תוכלי:
1. לראות את כל ה-endpoints
2. ללחוץ "Try it out"
3. למלא פרמטרים
4. ללחוץ "Execute"
5. לראות תוצאות

**זה יעבוד ללא בעיות CORS!**

---

## 🚀 הרצת השרת

```powershell
cd C:\DevOpsMCP
$env:PYTHONPATH = "C:\DevOpsMCP"
$env:PORT = 8090
python -m app.main_with_db
```

**השרת יעלה על:** `http://localhost:8090`

---

## 💡 טיפים

1. **Simple Browser של VS Code לא מומלץ ל-Swagger UI** - השתמשי בדפדפן רגיל
2. **PowerShell מושלם לבדיקות מהירות** - ללא UI, תוצאות מיידיות
3. **project_id רגיש לאותיות גדולות/קטנות** - השתמשי בדיוק כמו בטבלה
4. **אפשר להשאיר project_id ריק** - יחזיר נתונים מכל הפרויקטים

---

**הכל עובד מעולה!** 🎉
