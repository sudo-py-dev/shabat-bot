from enum import Enum
from pyrogram.types import ChatPermissions
from enum import Enum


class Messages(str, Enum):
    # Holiday
    holiday_lock = "כניסת {} ✨ הקבוצה נסגרת עד צאת החג"
    holiday_unlock = "צאת החג 🎉 הקבוצה נפתחת מחדש"

    # Shabbat
    shabbat_lock = "שבת שלום לכולם 🙏 הקבוצה סגורה עד צאת שבת"
    shabbat_unlock = "שבוע טוב לכולם 🌅 הקבוצה פתוחה"

    # Bot interaction
    start_message = "ברוכים הבאים! 🤖 אני בוט שומר שבת אני יעזור לך לשמור שבתות וחגים בקבוצה שלך."
    help_message = (
        "📖 פקודות זמינות:\n\n"
        "🚀 /start — התחלת שימוש\n"
        "ℹ️ /help — עזרה (פקודה זו)\n"
        "🕯️ /calendar — הגדרת הודעת כניסה לשבת\n"
        "   /כניסה\n"
        "🌅 /havdalah — הגדרת הודעת הבדלה\n"
        "   /הבדלה\n"
        "📝 /register — רישום קבוצה לניהול\n"
        "🔒 /permission — עדכון הרשאות\n"
    )

    # Custom messages
    shabbat_updated = "הודעה זו עודכנה בהצלחה ותישלח אוטומטית בכניסת שבת ✅"
    havdalah_updated = "הודעה זו עודכנה בהצלחה ותישלח אוטומטית בצאת שבת ✅"
    reply_to_set_message = "אנא הגב להודעה שתרצה לשמור כהודעת שבת/הבדלה."

    # Registration & permissions
    register_message = "הקבוצה תינעל בשבתות וחגים ✅"
    unregister_message = "הקבוצה לא תינעל בשבתות וחגים ❌"
    permission_message = "ההרשאות עודכנו בהצלחה ✅"

    # Errors
    invalid_or_not_existing_group = "קבוצה לא תקינה או שאינה קיימת ❌"



full_lock = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False
)

class AccessPermission(Enum):
    ALLOW = 1
    DENY = 2
    NOT_ADMIN = 3
    NOT_CONNECTED = 4