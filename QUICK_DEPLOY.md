# النشر السريع على Render

## طريقة سريعة لنشر البوت

### 1. رفع الملفات
```bash
# تشغيل سكريبت النشر
./deploy.sh
```

### 2. إعداد Render
1. اذهب إلى render.com
2. أنشئ Web Service جديد
3. اربط مستودع GitHub

### 3. الإعدادات
**Build Command:**
```
pip install flask openai pytelegrambotapi schedule gunicorn
```

**Start Command:**
```
python main.py
```

### 4. متغيرات البيئة
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=your_channel_id
```

### 5. النشر
انقر "Deploy" - البوت سيعمل فوراً!

## المزايا
✅ يعمل 24/7  
✅ لا يتوقف أبداً  
✅ إعادة تشغيل تلقائي  
✅ مجاني  

البوت جاهز! 🚀