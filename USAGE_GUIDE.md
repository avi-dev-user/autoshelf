# 🚀 AutoShelf v1.0.0 - מדריך שימוש

## ברוכים הבאים ל-AutoShelf החדש! 
AutoShelf עבר שדרוג מלא והוא עכשיו תומך גם ב-macOS וגם ב-Linux, עם יכולת לרוץ כשירות רקע קבוע!

---

## 🌟 מה חדש?

### ✅ תמיכה חוצת פלטפורמות
- **macOS**: ממשק GUI מקורי עם system tray
- **Linux**: ממשק tkinter מודרני וידידותי למשתמש
- זיהוי אוטומטי של המערכת

### ✅ מצב שירות רקע קבוע
- רץ ברקע ללא צורך לפתוח ממשק
- מתחיל אוטומטית בהפעלת המערכת
- עובד גם אחרי כיבוי והפעלה מחדש
- ניטור בריאות וטיפול באירועים בלתי צפויים

---

## 🚀 איך להפעיל?

### 1. **הפעלה רגילה (GUI)**
```bash
cd /home/user/projects/autoshelf
python3 autoshelf.py
```

### 2. **מצב דמון (רקע)**
```bash
# הפעלה ברקע
python3 daemon.py start

# בדיקת סטטוס
python3 daemon.py status

# עצירה
python3 daemon.py stop

# הפעלה במצב foreground (לצורכי debug)
python3 daemon.py foreground
```

### 3. **מצב שירות systemd (קבוע)**
```bash
# התקנת השירות
./service_manager.sh install

# הפעלת השירות
./service_manager.sh start

# בדיקת סטטוס
./service_manager.sh status

# עצירת השירות
./service_manager.sh stop

# הסרת השירות
./service_manager.sh uninstall
```

---

## ⚙️ ניהול השירות

### 🔍 **בדיקת בריאות המערכת**
```bash
./health_monitor.py status
./health_monitor.py check
```

### 📊 **פקודות systemd מתקדמות**
```bash
# סטטוס מפורט
systemctl --user status autoshelf@avi.service

# לוגים בזמן אמת
journalctl --user -u autoshelf@avi.service -f

# התחלה מחדש
systemctl --user restart autoshelf@avi.service
```

---

## 📁 הגדרות נוכחיות

- **תיקיית מעקב**: `/tmp/autoshelf_test` (לבדיקות)
- **שיטת ארגון**: לפי סוג קובץ
- **קטגוריות זמינות**: Documents, Images, Audio, Code, Videos, Archives

### 🔧 **לשינוי הגדרות**:
1. הפעל GUI: `python3 autoshelf.py`
2. לחץ על "Settings"
3. שנה את התיקיה הרצויה (למשל `/home/user/Downloads`)
4. השירות יתעדכן אוטומטית

---

## 🎯 בדיקה מהירה

### בדוק שהמערכת עובדת:
```bash
# 1. וודא שהשירות רץ
./service_manager.sh status

# 2. צור קובץ בדיקה
echo "בדיקה" > /tmp/autoshelf_test/test.txt

# 3. בדוק שהוא אורגן לתיקיית documents
ls -la /tmp/autoshelf_test/documents/
```

---

## 🔄 התחלה מחדש אוטומטית

השירות מוגדר להתחיל אוטומטית:
- ✅ בהפעלת המחשב
- ✅ אחרי כיבוי והפעלה מחדש  
- ✅ בשחזור מ-crash/error
- ✅ גם אחרי logout/login

---

## 🆘 פתרון בעיות

### בעיה: השירות לא מתחיל
```bash
# בדוק לוגים מפורטים
journalctl --user -u autoshelf@avi.service --no-pager

# או הפעל במצב debug
python3 daemon.py foreground
```

### בעיה: קבצים לא מאורגנים
```bash
# בדוק שהתיקיה נצפית
python3 daemon.py status

# בדוק הרשאות
ls -la /tmp/autoshelf_test/
```

### בעיה: השירות נעצר
```bash
# health monitor יתקן זאת אוטומטית
./health_monitor.py check

# או התחל מחדש ידנית
./service_manager.sh restart
```

---

## 🎉 סיכום

**AutoShelf עכשיו:**
- ✅ עובד על Linux ו-macOS
- ✅ רץ ברקע באופן קבוע
- ✅ מתחיל אוטומטית בהפעלת המערכת
- ✅ יציב ואמין עם מנגנון שחזור
- ✅ ממשק GUI מתקדם לניהול
- ✅ כלי ניהול שירות פשוטים

**השירות כבר מותקן ורץ!** 🚀

---

*נוצר עם ❤️ עבור חוויית ארגון קבצים מושלמת*