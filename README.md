# 🤖 תבנית בוט טלגרם

תבנית בוט טלגרם מודרנית ועשירה בתכונות שנבנתה עם Pyrogram ו-Python. תבנית זו מספקת בסיס מוצק לבניית בוטי טלגרם עם תמיכה בריבוי שפות, אינטגרציה עם מסד נתונים, ניהול אדמינים, פאנל ניהול מתקדם ועוד.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PyroTGFork](https://img.shields.io/badge/PyroTGFork-2.0+-blue)](https://pypi.org/project/pyrotgfork/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Channel-blue)](https://t.me/termux_il)

## ✨ תכונות עיקריות

- **🌐 תמיכה בריבוי שפות** - תמיכה מובנית בעברית ובאנגלית עם יכולת הרחבה קלה
- **👥 ניהול משתמשים** - רישום משתמשים מלא ומעקב אחר העדפות
- **👑 מערכת אדמינים** - בדיקת הרשאות מתקדמת עם בקרות מפורטות
- **⚙️ פאנל ניהול** - ממשק ניהול מתקדם עם שליטה בהגדרות
- **🔒 אבטחה** - אימות דו-שלבי למנהלים ובקרת גישה מפורטת
- **💾 מסד נתונים** - SQLAlchemy ORM עם תמיכה ב-SQLite
- **📊 לוגים מתקדמים** - מערכת לוגים עם שמירת קבצים ופלט צבעוני
- **⚡ ביצועים** - אופטימיזציה של שאילתות ופעולות אסינכרוניות
- **🔔 התראות** - מערכת התראות לאירועים חשובים
- **🔄 ממשק API** - תמיכה בהרחבות ושילובים


### 🏗️ שיפורי ארכיטקטורה
- ארגון מחדש של הקוד לחבילות לוגיות
- הפרדת אחריות ברורה בין רכיבי המערכת
- שיפור ניהול ה-handlers עם מערכת רישום גמישה

### 🛠️ שיפורי קוד
- שכתוב מערכת ההרשאות למנהלים
- שיפור בטיפול בשגיאות ורישום אירועים
- עדכון רמזי סוגים ותיעוד
- אופטימיזציה של ביצועים

### ✨ תכונות חדשות
- אשף התקנה אינטראקטיבי
- ניהול הרשאות מתקדם
- מערכת לוגים משופרת
- ממשק ניהול אינטואיטיבי

## 🚀 התחלה מהירה

### דרישות מערכת

- Python 3.8 ומעלה
- חשבון טלגרם פעיל
- אסימון בוט מ-[@BotFather](https://t.me/botfather)
- API ID ו-API Hash מ-[my.telegram.org](https://my.telegram.org)

### 🛠️ התקנה

1. **שכפול המאגר**
   ```bash
   git clone https://github.com/sudo-py-dev/telegram-bot-template.git
   cd telegram-bot-template
   ```

2. **הגדרת סביבת פיתוח**
   ```bash
   # יצירת סביבה וירטואלית
   python -m venv .venv
   
   # הפעלת הסביבה
   # ל-Linux/macOS:
   source .venv/bin/activate
   # ל-Windows:
   .venv\Scripts\activate.bat
   ```

3. **התקנת תלויות**
   ```bash
   pip install -r requirements.txt
   ```

4. **הגדרת משתני סביבה**
   ```bash
   cp .env.example .env
   # ערוך את הקובץ והוסף את הפרטים שלך
   ```

5. **הרצת הבוט**
   ```bash
   python index.py
   ```

## ⚙️ הגדרת משתני סביבה

העתק את הקובץ `.env.example` ל-`.env` והגדר את המשתנים הבאים:

```env
# ===== הגדרות חובה =====
BOT_TOKEN=your_telegram_bot_token_here  # מאת @BotFather
API_HASH=your_api_hash_here             # מ-https://my.telegram.org
API_ID=your_api_id_here                 # מ-https://my.telegram.org
BOT_CLIENT_NAME=my_bot                 # שם ייחודי לבוט שלך
BOT_OWNER_ID=your_telegram_id          # המזהה הטלגרם שלך

# ===== הגדרות מסד נתונים =====
DATABASE_URL=sqlite+aiosqlite:///my_bot.sqlite  # כתובת מסד הנתונים

# ===== הגדרות לוגים =====
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=bot.log  # קובץ הלוגים
```

### 🛠️ קבלת פרטי גישה

1. **יצירת בוט חדש**
   - שלח הודעה ל-[@BotFather](https://t.me/botfather)
   - השתמש בפקודה `/newbot` ועקוב אחר ההוראות
   - שמור את ה-token שהתקבל

2. **קבלת API ID ו-Hash**
   - היכנס ל-[my.telegram.org](https://my.telegram.org)
   - התחבר עם פרטי חשבון הטלגרם שלך
   - עבור ל-API development tools
   - צור אפליקציה חדשה וקבל את ה-API ID וה-Hash

3. **מזהה משתמש**
   - שלח הודעה ל- [@userinfobot](https://t.me/userinfobot)
   - הקבל את המזהה שלך מהתשובה

## 📁 מבנה הפרויקט

```
telegram-bot-template/
├── bot_management/           # כלי ניהול לבעלי הבוט
│   ├── bot_settings.py       # פקודות והגדרות הבוט
│   ├── callback_handlers.py  # טיפול בשאילתות חוזרות של לוח הבקרה
│   └── setup.py              # כלי התקנה ואתחול לבוט
├── handlers/                 # מנהלי הודעות ושאילתות
│   ├── callback_handlers.py  # טיפול בשאילתות חוזרות
│   ├── command_handlers.py   # פקודות הבוט (/start, /help וכו')
│   ├── join_handlers.py      # טיפול בהצטרפות לקבוצות
│   └── message_handlers.py   # טיפול בהודעות רגילות
├── locales/                  # קבצי תרגום
│   ├── messages.json         # הודעות רב-לשוניות
│   └── privileges.json       # הגדרות הרשאות
└── tools/                    # כלי ליבה ושירותים
    ├── database.py           # מודלים ופעולות מסד נתונים
    ├── enums.py              # קבועים וניהול הודעות
    ├── inline_keyboards.py   # יצירת מקלדות מובנות
    ├── logger.py             # הגדרות רישום
    └── tools.py              # פונקציות עזר
├── .env.example              # תבנית הגדרות סביבה
├── .gitignore               # דפוסי התעלמות מגיט
├── index.py                 # נקודת כניסה ראשית של הבוט
├── requirements.txt         # תלויות Python
├── README.md                # קובץ זה (עברית)
└── README_EN.md             # גרסה באנגלית
```

## ⚙️ לוח בקרת מנהלים

### כניסה ללוח הבקרה
שלח את הפקודה `/admin` בצ'אט פרטי עם הבוט.

### תכונות עיקריות

#### 📊 לוח מחוונים
- סקירה כללית של סטטיסטיקות הבוט
- מצב מערכת בזמן אמת
- התראות ואירועים אחרונים

#### 👥 ניהול משתמשים
- צפייה ברשימת משתמשים
- ניהול הרשאות משתמשים
- חסימת משתמשים

#### ⚙️ הגדרות
- **הגדרות אבטחה**
  - הגבלות גישה
  - יומן אירועים
- **הגדרות בוט**
  - שפת ברירת מחדל
  - עיצוב הודעות
  - תצוגת תצוגה מקדימה

#### 📝 לוגים
- צפייה בלוגים בזמן אמת
- סינון לפי רמת חומרה
- ייצוא לוגים לניתוח

## 🛠️ פיתוח והרחבה

### הוספת פקודות חדשות

1. צור handler חדש ב-`handlers/command_handlers.py`:
   ```python
   from pyrogram import filters
   from tools.tools import with_language
   
   @with_language
   async def my_command(client, message, language: str):
       await message.reply(f"שלום! השפה הנוכחית היא: {language}")
   ```

2. הוסף את הפקודה לרשימת ה-handlers:
   ```python
   from pyrogram.handlers import MessageHandler
   
   commands_handlers = [
       MessageHandler(my_command, filters.command("mycommand")),
       # ... שאר הפקודות
   ]
   ```

### הוספת שפות חדשות

1. הוסף את התרגומים החדשים לקובץ `locales/messages.json`:
   ```json
   {
     "en": {
       "welcome": "Welcome to the bot!"
     },
     "he": {
       "welcome": "ברוכים הבאים לבוט!"
     },
     "es": {
       "welcome": "¡Bienvenido al bot!"
     }
   }
   ```

2. השתמש בהודעות עם מערכת התרגום:
   ```python
   from tools.enums import Messages
   
   @with_language
   async def welcome(client, message, language: str):
       messages = Messages(language=language)
       await message.reply(messages.welcome)
   ```

## 🛠️ שימוש

### הוספת פקודות חדשות למנהל

#### פקודות למנהל הבוט
```python
from tools.tools import owner_only

@owner_only
@with_language
async def admin_command(client, message, language: str):
    # קוד הפקודה למנהל
    pass
```

### הוספת פקודות חדשות

1. **צור פונקציית handler** ב- `handlers/commands.py`:
   ```python
   from tools.tools import with_language
   from tools.enums import Messages

   @with_language
   async def my_command(client, message, language: str):
       await message.reply(Messages(language=language).my_message)
   ```

2. **רשום את הפקודה** ברשימת `commands_handlers`:
   ```python
   commands_handlers = [
       MessageHandler(my_command, filters.command("mycommand")),
       # ... handlers קיימים
   ]
   ```

### הוספת שפות חדשות

1. **הוסף הודעות** ל- `tools/messages.json`:
   ```json
   {
     "fr": {
       "hello": "Bonjour {}",
       "goodbye": "Au revoir"
     }
   }
   ```

2. **עדכן שמות תצוגת שפות** ב- `handlers/callback_buttons.py`:
   ```python
   language_display_names = {
       "he": "עברית 🇮🇱",
       "en": "English 🇺🇸",
       "fr": "Français 🇫🇷"
   }
   ```

### ניהול הגדרות בוט

```python
from database import BotSettings

# קבלת הגדרות
settings = BotSettings.get_settings()

# עדכון הגדרות
BotSettings.update_settings(
    can_join_group=True,
    can_join_channel=False,
    owner_id=123456789
)


### פעולות מסד נתונים

```python
from database import Users, Chats

# צור משתמש
Users.create(user_id=123456789, username="user", language="en")

# קבל משתמש
user = Users.get(user_id=123456789)

# עדכן משתמש
Users.update(user_id=123456789, language="he")

# ספירת משתמשים
user_count = Users.count()
active_users = Users.count_by(is_active=True)

# ספירת צ'אטים
chat_count = Chats.count()
active_chats = Chats.count_by(is_active=True)
```

## 🌍 מערכת ריבוי שפות

הבוט תומך במספר שפות עם מערכת ניהול הודעות חכמה:

- **אחסון הודעות**: כל ההודעות מאוחסנות בפורמט JSON
- **מערכת fallback**: חוזרת לאנגלית אם ההודעה לא נמצאה
- **טעינה דינמית**: שפות נטענות מ- `messages.json` בזמן ריצה
- **הרחבה קלה**: הוסף שפות חדשות על ידי עדכון קובץ JSON

## 👑 מערכת אדמינים

בדיקת הרשאות אדמין מתקדמת עם תמיכה ב:
- **הרשאות מפורטות**: בדיקת זכויות אדמין ספציפיות
- **סוגי צ'אטים**: עובד עם קבוצות, סופרגרופים וערוצים
- **מטמון**: רשימות אדמינים במטמון לביצועים
- **טיפול שגיאות**: טיפול ב- בצ'אטים/הרשאות לא תקינים

```python
from tools.tools import is_admin_message

@is_admin_message(permission_require="can_restrict_members")
async def admin_only_command(client, message):
    await message.reply("אתה אדמין!")
```

## 📊 מערכת לוגים מתקדמת

### תכונות עיקריות
- **📝 רישום מקיף** - תמיכה בכל רמות הלוגים (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **📁 ניהול קבצים** - רוטציה אוטומטית של קבצי לוג
- **🎨 פלט צבעוני** - הבחנה ויזואלית בין סוגי הלוגים
- **⏱️ חותמות זמן** - תיעוד מדויק של זמן האירועים
- **🔍 מידע מפורט** - מיקום קוד, תהליך, ו-thread

### דוגמאות שימוש

```python
from tools.logger import setup_logger

# אתחול לוגר
logger = setup_logger(__name__)

# דוגמאות לוגים
logger.debug("הודעת דיבאג מפורטת")
logger.info("מידע כללי")
logger.warning("אזהרה חשובה")
logger.error("שגיאה קריטית")
logger.critical("שגיאה חמורה")

# הודעת הצלחה מותאמת אישית
logger.success("הפעולה בוצעה בהצלחה!")

# מדידת ביצועים
import time
start_time = time.time()
# קוד למדידת ביצועים
logger.info(f"זמן ביצוע: {time.time() - start_time:.2f} שניות")
```

### הגדרת רמת לוגים

ניתן לקבוע את רמת הלוגים באמצעות משתנה הסביבה `LOG_LEVEL` בקובץ `.env`:

```env
LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=bot.log  # קובץ הלוגים
```

### פלט לדוגמה

```
2023-10-09 15:42:18.123 | DEBUG    | module.name:12 - הודעת דיבאג מפורטת
2023-10-09 15:42:19.456 | INFO     | module.name:15 - מידע כללי
2023-10-09 15:42:20.789 | WARNING  | module.name:18 - אזהרה חשובה
2023-10-09 15:42:21.012 | ERROR    | module.name:21 - שגיאה קריטית
2023-10-09 15:42:21.345 | SUCCESS  | module.name:24 - הפעולה בוצעה בהצלחה!
2023-10-09 15:42:22.678 | CRITICAL | module.name:27 - שגיאה חמורה
```

### התאמה אישית

ניתן להתאים את מערכת הלוגים על ידי עריכת הקובץ `tools/logger.py`:
- הוספת/הסרת emojis
- שינוי צבעים
- שינוי פורמט ההודעה
- הוספת שדות מידע נוספים

## 🔧 תכונות מתקדמות

### מערכת מטמון
- **מטמון מתמיד**: נתונים נשמרים לאחר הפעלה מחדש של הבוט
- **תמיכה ב-TTL**: תפוגה אוטומטית של נתוני מטמון
- **סילוק LRU**: ניקוי אוטומטי של רשומות ישנות
- **עמיד בפני threads**: בטוח לגישה מקבילית

### מודלי מסד נתונים
- **משתמשים**: ניהול משתמשים עם העדפות
- **צ'אטים**: מידע על צ'אטים והגדרות
- **ניתן להרחבה**: קל להוסיף מודלים חדשים

### טיפול שגיאות
- **שמירת זמינות**: הבוט ממשיך לפעול למרות שגיאות
- **משוב למשתמש**: הודעות שגיאה ברורות למשתמשים
- **תמיכה בדיבוג**: לוג שגיאות מפורט

## 🤝 תרומה

1. Fork את המאגר
2. צור ענף תכונה: `git checkout -b feature/amazing-feature`
3. commit את השינויים שלך: `git commit -m 'Add amazing feature'`
4. Push לענף: `git push origin feature/amazing-feature`
5. פתח Pull Request

## 📝 רישיון

פרויקט זה הוא קוד פתוח וזמין תחת [רישיון MIT](LICENSE).

## 🙏 תודות

- [Pyrogram](https://github.com/TelegramPlayGround/Pyrogram) - לקוח טלגרם מודרני ב-Python
- [SQLAlchemy](https://www.sqlalchemy.org/) - toolkit למסדי נתונים
- [python-dotenv](https://github.com/theskumar/python-dotenv) - ניהול משתני סביבה

## 📞 תמיכה

אם יש לך שאלות או צריך עזרה:
- צור issue ב-GitHub
- בדוק את [תיעוד Pyrogram](https://telegramplayground.github.io/pyrogram)

## 🌍 גרסאות שפה

- [עברית README](README.md) - גרסה בעברית (זו)
- [English README](README_EN.md) - גרסה באנגלית

---

⭐ **תן כוכב למאגר אם הוא עזר לך!**
