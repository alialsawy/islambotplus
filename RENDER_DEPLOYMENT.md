# نشر البوت الإسلامي على استضافة Render

## خطوات النشر

### 1. إعداد مستودع Git
```bash
git init
git add .
git commit -m "Islamic Telegram Bot ready for deployment"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. إنشاء خدمة جديدة على Render
1. اذهب إلى [render.com](https://render.com) وسجل الدخول
2. انقر على "New +" واختر "Web Service"
3. اربط مستودع GitHub الخاص بك
4. املأ التفاصيل التالية:

**إعدادات الخدمة:**
- **Name:** islamic-telegram-bot
- **Environment:** Python 3
- **Build Command:** `pip install flask openai pytelegrambotapi schedule gunicorn`
- **Start Command:** `python main.py`

### 3. إعداد متغيرات البيئة (Environment Variables)
في قسم Environment Variables، أضف المتغيرات التالية:

**متغيرات مطلوبة:**
- `TELEGRAM_BOT_TOKEN`: رمز البوت من BotFather
- `TELEGRAM_CHANNEL_ID`: معرف القناة (يبدأ بـ @ أو -)

**متغيرات اختيارية (لديها قيم افتراضية):**
- `MAX_CONTENT_LENGTH`: 500
- `CONTENT_TEMPERATURE`: 0.8
- `RETRY_ATTEMPTS`: 3
- `RETRY_DELAY`: 60
- `MORNING_AZKAR_TIME`: 06:00
- `QURAN_VERSE_TIME`: 08:00
- `DAILY_HADITH_TIME`: 12:00
- `DAILY_REMINDER_TIME`: 17:00
- `DAILY_DUA_TIME`: 20:00
- `EVENING_AZKAR_TIME`: 21:00

### 4. النشر
1. انقر على "Create Web Service"
2. Render سيقوم ببناء ونشر البوت تلقائياً
3. البوت سيبدأ العمل فور انتهاء النشر

## مميزات النشر على Render

✅ **استمرارية العمل:** البوت لن يتوقف أبداً  
✅ **إعادة التشغيل التلقائي:** في حالة حدوث أي خطأ  
✅ **مجاني:** خطة مجانية متاحة  
✅ **سهولة الإعداد:** نشر بنقرة واحدة  
✅ **مراقبة الأداء:** لوحة تحكم لمتابعة الحالة  

## حالة البوت بعد النشر

سيقوم البوت بـ:
- نشر المحتوى الإسلامي حسب الجدولة المحددة
- الرد على التفاعل مع عداد الأذكار
- إعادة المحاولة تلقائياً في حالة حدوث أخطاء
- العمل 24/7 بدون توقف

## استكشاف الأخطاء

إذا واجهت مشاكل:
1. تحقق من صحة `TELEGRAM_BOT_TOKEN`
2. تحقق من أن `TELEGRAM_CHANNEL_ID` صحيح
3. تأكد من أن البوت مدير في القناة
4. راجع سجلات الأخطاء في Render Dashboard

## الملفات المطلوبة للنشر

✅ `render.yaml` - إعدادات Render  
✅ `runtime.txt` - إصدار Python  
✅ `Procfile` - أمر التشغيل  
✅ جميع ملفات Python الأساسية  

البوت جاهز للنشر على Render! 🚀