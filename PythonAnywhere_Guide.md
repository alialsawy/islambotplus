# 🐍 دليل رفع البوت الإسلامي على PythonAnywhere

## 📋 المتطلبات قبل البدء:

- توكن البوت من @BotFather
- معرف القناة أو اسمها (@channel_name أو -1001234567890)
- حساب مجاني على PythonAnywhere

---

## 🚀 الخطوات التفصيلية:

### **الخطوة 1: إنشاء حساب PythonAnywhere**

1. اذهب إلى: https://www.pythonanywhere.com
2. اضغط على **"Start running Python online in less than a minute!"**
3. اختر **"Create a Beginner account"** (مجاني)
4. املأ البيانات:
   - Username (سيصبح: username.pythonanywhere.com)
   - Email
   - Password
5. تأكد من إيميلك واسجل الدخول

### **الخطوة 2: رفع ملف البوت**

#### طريقة 1: رفع مباشر
1. اذهب إلى تبويب **"Files"**
2. اضغط **"Upload a file"**
3. ارفع ملف `pythonanywhere_setup.py`

#### طريقة 2: إنشاء الملف يدوياً
1. اذهب إلى **"Files"**
2. اضغط **"New file"**
3. اسم الملف: `islamic_bot.py`
4. انسخ محتوى `pythonanywhere_setup.py` والصقه

### **الخطوة 3: تثبيت المكتبات المطلوبة**

1. اذهب إلى تبويب **"Consoles"**
2. اضغط **"Bash"** لفتح terminal جديد
3. نفذ الأوامر التالية:

```bash
pip3.11 install --user pyTelegramBotAPI
pip3.11 install --user schedule
```

انتظر حتى ينتهي التثبيت وترى رسالة النجاح.

### **الخطوة 4: إعداد متغيرات البيئة**

#### طريقة 1: ملف .env (الأسهل)
1. في تبويب **"Files"**، أنشئ ملف جديد اسمه `.env`
2. أضف هذا المحتوى:

```bash
TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN_HERE
TELEGRAM_CHANNEL_ID=YOUR_CHANNEL_ID_HERE
```

**مثال:**
```bash
TELEGRAM_BOT_TOKEN=6123456789:AAEhBOweik6ad6PsVkAh4rZObiOIt1GrqAs
TELEGRAM_CHANNEL_ID=@your_channel
```

#### طريقة 2: متغيرات النظام
1. في الـ **Bash console**, نفذ:

```bash
echo 'export TELEGRAM_BOT_TOKEN="YOUR_TOKEN_HERE"' >> ~/.bashrc
echo 'export TELEGRAM_CHANNEL_ID="YOUR_CHANNEL_ID"' >> ~/.bashrc
source ~/.bashrc
```

### **الخطوة 5: تعديل مسار اللوج**

1. افتح ملف `islamic_bot.py`
2. ابحث عن السطر:
```python
logging.FileHandler('/home/yourusername/mysite/bot.log'),
```
3. استبدل `yourusername` باسم المستخدم الخاص بك
4. مثال: `/home/ahmed123/mysite/bot.log`

### **الخطوة 6: اختبار البوت**

1. في **Bash console**، نفذ:
```bash
cd ~
python3.11 islamic_bot.py
```

2. إذا ظهرت رسائل مثل:
```
✅ تم تهيئة البوت الإسلامي على PythonAnywhere
🚀 بدء تشغيل البوت الإسلامي على PythonAnywhere...
✅ تم إرسال رسالة بدء التشغيل
```

**تهانينا! البوت يعمل** 🎉

### **الخطوة 7: التشغيل المستمر 24/7**

#### لجعل البوت يعمل دائماً:

1. اذهب إلى تبويب **"Tasks"**
2. اضغط **"Create a new task"**
3. في خانة **"Command"**، اكتب:
```bash
python3.11 /home/yourusername/islamic_bot.py
```
4. في **"Hour"** اكتب: `*` (يعني كل ساعة)
5. في **"Minute"** اكتب: `0` (يعني في بداية كل ساعة)
6. اضغط **"Create"**

**ملاحظة**: في الحساب المجاني، يمكنك تشغيل Task واحد فقط.

### **الخطوة 8: مراقبة البوت**

#### لمشاهدة اللوجات:
1. في **Bash console**:
```bash
tail -f ~/mysite/bot.log
```

#### لإيقاف البوت مؤقتاً:
```bash
pkill -f islamic_bot.py
```

#### لإعادة تشغيل البوت:
```bash
python3.11 ~/islamic_bot.py &
```

---

## 🔧 حل المشاكل الشائعة:

### **مشكلة: البوت لا يجد التوكن**
**الحل:**
```bash
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHANNEL_ID
```
إذا لم تظهر القيم، أعد الخطوة 4.

### **مشكلة: "ModuleNotFoundError"**
**الحل:**
```bash
pip3.11 install --user pyTelegramBotAPI schedule
```

### **مشكلة: البوت لا يرسل للقناة**
**الحل:**
1. تأكد من إضافة البوت كمشرف في القناة
2. تأكد من صحة معرف القناة
3. جرب إرسال رسالة يدوية أولاً

### **مشكلة: البوت يتوقف**
**الحل:**
- استخدم **Always-On Tasks** (متاح في الحسابات المدفوعة)
- أو أعد تشغيله يدوياً كل فترة

### **مشكلة: رسالة "Quota exceeded"**
**الحل:**
- الحساب المجاني محدود بـ 100 ثانية CPU يومياً
- قلل تكرار إرسال المحتوى أو انتقل للحساب المدفوع

---

## 💡 نصائح للتحسين:

### **تقليل استهلاك الموارد:**
1. زيادة وقت sleep في الجدولة:
```python
time.sleep(60)  # بدلاً من 30
```

2. تقليل تكرار polling:
```python
self.bot.polling(none_stop=True, interval=2, timeout=30)
```

### **مراقبة أفضل:**
```bash
# إضافة cron job للتأكد من التشغيل
echo "*/10 * * * * pgrep -f islamic_bot.py || python3.11 /home/yourusername/islamic_bot.py &" | crontab -
```

### **نسخ احتياطي:**
```bash
# نسخ احتياطي من اللوجات
cp ~/mysite/bot.log ~/mysite/bot_backup_$(date +%Y%m%d).log
```

---

## 📊 ملخص سريع:

1. **إنشاء حساب** على PythonAnywhere ✅
2. **رفع ملف** `pythonanywhere_setup.py` ✅
3. **تثبيت المكتبات** `pip3.11 install --user pyTelegramBotAPI schedule` ✅
4. **إعداد متغيرات البيئة** في `.env` ✅
5. **تعديل مسار اللوج** في الكود ✅
6. **تشغيل البوت** `python3.11 islamic_bot.py` ✅
7. **إعداد Task** للتشغيل المستمر ✅

**النتيجة:** بوت إسلامي يعمل 24/7 مع 8 أنواع محتوى يومي + عداد أذكار تفاعلي!

---

## 📞 المساعدة:

إذا واجهت أي مشكلة:
1. تحقق من اللوجات: `tail -f ~/mysite/bot.log`
2. تأكد من المتغيرات: `echo $TELEGRAM_BOT_TOKEN`
3. أعد تثبيت المكتبات إذا لزم الأمر
4. تأكد من أن البوت مشرف في القناة

**بارك الله فيك ونفع بهذا العمل** 🤲