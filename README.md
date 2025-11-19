# בוט שבת 🤖

בוט טלגרם המסייע לפתיחה ונעילת קבוצות במהלך שבתות וחגים יהודיים לפי לוח השנה העברי.

## תכונות עיקריות ✨

- **מצב שבת אוטומטי**: נועל את הקבוצה לפני כניסת השבת ופותח אותה מחדש במוצ"ש
- **תמיכה בחגים**: יש
- **תמיכה במספר שפות**: תומך בעברית, אנגלית וצרפתית
- **פקודות למנהלים**: פקודות מיוחדות למנהלי קבוצות
- **הודעות מותאמות אישית**: הגדר הודעות ברוכים הבאים והודעות התראה מותאמות אישית
- **תמיכה באיזורי זמן**: פועל בהתאם לאזור הזמן של ישראל (IST)

## התקנה והרצה 🛠️

1. **שכפול המאגר**
   ```bash
   git clone https://github.com/sudo-py-dev/shabat-bot.git
   cd shabat-bot
   ```

2. **יצירת סביבה וירטואלית והפעלתה**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ב-Windows: venv\Scripts\activate
   ```

3. **התקנת תלויות**
   ```bash
   pip install -r requirements.txt
   ```

4. **הגדרת משתני סביבה**
   - העתק את הקובץ `.env.example` ל-`.env`
   - מלא את טוקן הבוט שלך ואת ההגדרות הנוספות
   ```bash
   cp .env.example .env
   ```

5. **הרצת הבוט**
   ```bash
   python index.py
   ```

## משתני סביבה ⚙️

| משתנה | תיאור | חובה |
|--------|--------|------|
| `BOT_TOKEN` | טוקן הבוט שלך מ-[@BotFather](https://t.me/botfather) | ✅ |
| `BOT_OWNER_ID` | מזהה המשתמש שלך בטלגרם | ✅ |
| `DATABASE_URL` | כתובת חיבור למסד הנתונים | ✅ |
| `BEFORE_SHABAT` | דקות לפני כניסת השבת לשליחת התראות (ברירת מחדל: 40) | ❌ |
| `SKIP_UPDATES` | דילוג על עדכונים בהפעלה (true/false) | ❌ |

## פקודות 🤖

### פקודות למנהלים
- `/start` - התחל את הבוט
- `/help` - הצג תפריט עזרה
- `/lang` - שנה שפה
- `/register` - רשום את הקבוצה הנוכחית
- `/unregister` - בטל רישום של הקבוצה הנוכחית
- `/set` - הגדר הודעות מותאמות אישית (השב על הודעה עם `/set [סוג]`)

### סוגי הודעות זמינים
- `calendar` - הגדר הודעת לוח שנה
- `shabbat` - הגדר הודעת שבת
- `havdalah` - הגדר הודעת הבדלה
- `holiday` - הגדר הודעת חג

## תרומה לפרויקט 🤝

אנחנו שמחים לקבל תרומות! אתם מוזמנים לשלוח בקשת משיכה (Pull Request).

1. בצע פורק (Fork) למאגר
2. צור ענף לתכונה החדשה שלך (`git checkout -b feature/cool-feature`)
3. שמור את השינויים שלך (`git commit -m 'Add cool feature'`)
4. דחוף את הענף (`git push origin feature/cool-feature`)
5. פתח בקשת משיכה

## רישיון 📄

פרויקט זה מופץ תחת רישיון MIT - לפרטים נוספים קרא את קובץ [הרישיון](LICENSE).

## תודות 🙏

- [pyrotgfork](https://telegramplayground.github.io/pyrogram/) - ספריית Python ל-Telegram MTProto API
- [hebcal-api](https://github.com/sudo-py-dev/hebcal-api) - API ללוח השנה היהודי
- [pytz](https://pypi.org/project/pytz/) - הגדרות אזורי זמן עבור פייתון

---

פותח ב-❤️ על ידי [sudo-py-dev](https://github.com/sudo-py-dev)
