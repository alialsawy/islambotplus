#!/bin/bash

# Deploy Islamic Bot to Vercel - Quick Setup Script
# نص سريع لنشر البوت الإسلامي على Vercel

echo "🚀 بدء نشر البوت الإسلامي على Vercel..."

# Check if required files exist
echo "📋 فحص الملفات المطلوبة..."

required_files=("vercel.json" "vercel_main.py" "requirements-vercel.txt" "bot_config.py" "content_generator.py" "telegram_bot.py")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ملف مفقود: $file"
        exit 1
    fi
done

echo "✅ جميع الملفات الأساسية موجودة"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📂 تهيئة مستودع Git..."
    git init
    git add .
    git commit -m "Initial commit - Islamic Telegram Bot for Vercel"
else
    echo "📂 مستودع Git موجود بالفعل"
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 تثبيت Vercel CLI..."
    npm install -g vercel
fi

echo "🔧 إعداد متغيرات البيئة..."
echo "سيُطلب منك إدخال البيانات التالية:"
echo "1. TELEGRAM_BOT_TOKEN - توكن البوت من @BotFather"
echo "2. TELEGRAM_CHANNEL_ID - معرف القناة"

# Deploy to Vercel
echo "🚀 بدء النشر على Vercel..."
vercel --confirm

echo "✅ تم النشر بنجاح!"
echo ""
echo "📋 الخطوات التالية:"
echo "1. انسخ رابط النشر من الناتج أعلاه"
echo "2. أضف متغيرات البيئة في لوحة تحكم Vercel"
echo "3. إعداد Webhook للبوت:"
echo "   curl -X POST \"https://api.telegram.org/bot<TOKEN>/setWebhook\" \\"
echo "        -H \"Content-Type: application/json\" \\"
echo "        -d '{\"url\": \"https://your-project.vercel.app/webhook\"}'"
echo ""
echo "4. اختبار البوت:"
echo "   curl https://your-project.vercel.app/test"
echo ""
echo "📝 لمزيد من التعليمات، راجع ملف VERCEL_DEPLOYMENT.md"
echo ""
echo "🤲 بالتوفيق! سبحان الله والحمد لله"