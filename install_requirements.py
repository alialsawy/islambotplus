#!/usr/bin/env python3
"""
ملف تثبيت المتطلبات للبوت الإسلامي - Google Colab
"""

import subprocess
import sys

def install_requirements():
    """تثبيت المكتبات المطلوبة"""
    requirements = [
        'pyTelegramBotAPI==4.15.8',
        'schedule==1.2.0'
    ]
    
    print("🔧 تثبيت المكتبات المطلوبة...")
    
    for package in requirements:
        try:
            print(f"📦 تثبيت {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ تم تثبيت {package} بنجاح")
        except subprocess.CalledProcessError as e:
            print(f"❌ فشل في تثبيت {package}: {e}")
            return False
    
    print("🎉 تم تثبيت جميع المكتبات بنجاح!")
    return True

if __name__ == "__main__":
    success = install_requirements()
    if success:
        print("\n🚀 الآن يمكنك تشغيل البوت!")
        print("👉 شغل الملف: islamic_bot_colab.py")
    else:
        print("\n❌ حدث خطأ في التثبيت. حاول مرة أخرى.")