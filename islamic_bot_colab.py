#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
البوت الإسلامي للتليجرام - نسخة Google Colab
Bot إسلامي شامل مع المحتوى الأصيل والعداد التفاعلي
"""

import os
import time
import random
import logging
import signal
import threading
from datetime import datetime
import schedule
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("IslamicBot")

class IslamicBotColab:
    def __init__(self, bot_token, channel_id):
        """تهيئة البوت الإسلامي"""
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.bot = telebot.TeleBot(bot_token)
        self.user_counts = {}
        
        # جدولة المحتوى اليومي
        self.schedule_times = {
            "morning_azkar": "06:00",
            "quran_verse": "08:00",
            "daily_hadith": "12:00",
            "religious_post": "14:00",
            "daily_reminder": "17:00",
            "companion_story": "19:00",
            "daily_dua": "20:00",
            "evening_azkar": "21:00"
        }
        
        # المحتوى الإسلامي الأصيل
        self.content = {
            "morning_azkar": [
                "🌅 أذكار الصباح\n\n﴿ أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ ﴾\n\n🌟 بداية يوم مباركة بذكر الله",
                "🌅 أذكار الصباح\n\n﴿ اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا ﴾\n\n✨ الحمد لله على نعمة الإسلام"
            ],
            "evening_azkar": [
                "🌙 أذكار المساء\n\n﴿ أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ ﴾\n\n🌟 ختام يوم بذكر الله العظيم",
                "🌙 أذكار المساء\n\n﴿ اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ ﴾\n\n💫 اللهم أعنا على ذكرك"
            ],
            "quran_verse": [
                "📖 آية من القرآن الكريم\n\n﴿ وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا ﴾\n\n🎯 التقوى طريق النجاة",
                "📖 آية من القرآن الكريم\n\n﴿ إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾\n\n🌈 بعد الضيق فرج"
            ],
            "daily_hadith": [
                "📚 حديث شريف\n\n\"الدين النصيحة\"\n🌟 رواه مسلم\n\n💡 النصح الصادق من أسس الدين",
                "📚 حديث شريف\n\n\"المؤمن للمؤمن كالبنيان يشد بعضه بعضاً\"\n🌟 رواه البخاري\n\n🤝 التعاون أساس القوة"
            ],
            "religious_post": [
                "✨ بوست ديني\n\n🌙 في هدوء الليل تشع روحانية الذكر والدعاء. هذه اللحظات المباركة تقربنا من خالقنا.\n\n📿 اجعل من ليلك موعداً مع الله:\n• قراءة القرآن بتدبر\n• الاستغفار والتوبة\n• الدعاء بخشوع\n\n💎 فالليل خير جليس للمؤمن",
                "✨ بوست ديني\n\n🌅 مع إشراقة كل فجر جديد، يمنحنا الله فرصة للبداية من جديد. كل يوم صفحة بيضاء نكتب فيها أعمالنا.\n\n🎯 اجعل يومك مليئاً بـ:\n• ذكر الله في كل وقت\n• العمل الصالح النافع\n• الإحسان إلى الناس\n\n🌟 فكل لحظة أمانة ستُسأل عنها"
            ],
            "companion_story": [
                "👤 قصة صحابي - أبو بكر الصديق رضي الله عنه\n\n💎 الصاحب الأول والصديق الأعظم\n\nكان أول من آمن بالنبي ﷺ من الرجال، ولم يتردد لحظة واحدة.\n\n🌟 موقف مؤثر:\nفي الهجرة، اختبأ مع النبي في غار ثور. عندما اقترب المشركون، قال: 'لو نظر أحدهم تحت قدميه لرآنا!' فقال النبي: 'ما ظنك باثنين الله ثالثهما؟'\n\n💝 الدرس: الثقة الكاملة بالله تطرد الخوف",
                "👤 قصة صحابي - عمر بن الخطاب رضي الله عنه\n\n⚔️ الفاروق الذي فرق بين الحق والباطل\n\nكان من أشد أعداء الإسلام، لكن الله هداه فأصبح من أعظم المدافعين عنه.\n\n🌟 موقف مؤثر:\nلما تولى الخلافة، كان يتفقد الرعية بنفسه. ذات ليلة سمع بكاء أطفال، فذهب ووجد أماً تطبخ الماء والحصى لتسكت أطفالها الجياع. فبكى وحمل الطعام بنفسه.\n\n💝 الدرس: العدل والرحمة أساس القيادة"
            ],
            "daily_dua": [
                "🤲 دعاء مستجاب\n\n\"رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ\"\n\n🕌 الدعاء الجامع للخير",
                "🤲 دعاء مستجاب\n\n\"اللَّهُمَّ اهْدِنِي فِيمَن هَدَيْتَ وَعَافِنِي فِيمَن عَافَيْتَ\"\n\n✨ اطلب الهداية والعافية"
            ],
            "daily_reminder": [
                "💭 تذكرة إيمانية\n\n\"وما خلقت الجن والإنس إلا ليعبدون\"\n\n🎯 تذكر الهدف من وجودك في هذه الحياة",
                "💭 تذكرة إيمانية\n\n\"الصلاة عماد الدين، من أقامها فقد أقام الدين\"\n\n🕌 حافظ على صلاتك في وقتها"
            ]
        }
        
        # أذكار للعداد التفاعلي
        self.azkar_types = {
            "istighfar": {
                "text": "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
                "target": 100,
                "title": "الاستغفار"
            },
            "tasbih": {
                "text": "سبحان الله",
                "target": 33,
                "title": "التسبيح"
            },
            "tahmid": {
                "text": "الحمد لله",
                "target": 33,
                "title": "التحميد"
            },
            "takbir": {
                "text": "الله أكبر",
                "target": 34,
                "title": "التكبير"
            },
            "salawat": {
                "text": "اللهم صل وسلم على نبينا محمد",
                "target": 10,
                "title": "الصلاة على النبي"
            }
        }
        
        self.setup_handlers()
        
    def setup_handlers(self):
        """إعداد معالجات الأوامر"""
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.send_main_menu(message)
        
        @self.bot.message_handler(commands=['azkar'])
        def azkar_command(message):
            self.send_azkar_menu(message)
            
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.handle_callback(call)
    
    def send_main_menu(self, message):
        """إرسال القائمة الرئيسية"""
        welcome_text = """🌙 أهلاً وسهلاً بك في البوت الإسلامي
        
🎯 اختر ما تريد:"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📿 عداد الأذكار", callback_data="azkar_menu"),
            types.InlineKeyboardButton("📖 محتوى إسلامي", callback_data="random_content")
        )
        
        self.bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    
    def send_azkar_menu(self, message):
        """إرسال قائمة الأذكار"""
        text = "📿 اختر نوع الذكر:\n\n"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        for key, azkar in self.azkar_types.items():
            markup.add(types.InlineKeyboardButton(
                f"{azkar['title']} ({azkar['target']})", 
                callback_data=f"start_azkar_{key}"
            ))
        
        markup.add(types.InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu"))
        
        self.bot.send_message(message.chat.id, text, reply_markup=markup)
    
    def handle_callback(self, call):
        """معالجة الضغط على الأزرار"""
        if call.data == "main_menu":
            self.send_main_menu(call.message)
        elif call.data == "azkar_menu":
            self.send_azkar_menu(call.message)
        elif call.data == "random_content":
            self.send_random_content(call.message)
        elif call.data.startswith("start_azkar_"):
            azkar_type = call.data.replace("start_azkar_", "")
            self.start_azkar_counter(call, azkar_type)
        elif call.data.startswith("count_"):
            azkar_type = call.data.replace("count_", "")
            self.increment_azkar(call, azkar_type)
        elif call.data.startswith("reset_"):
            azkar_type = call.data.replace("reset_", "")
            self.reset_azkar(call, azkar_type)
    
    def start_azkar_counter(self, call, azkar_type):
        """بدء عداد الأذكار"""
        user_id = call.from_user.id
        if user_id not in self.user_counts:
            self.user_counts[user_id] = {}
        
        if azkar_type not in self.user_counts[user_id]:
            self.user_counts[user_id][azkar_type] = 0
            
        azkar = self.azkar_types[azkar_type]
        count = self.user_counts[user_id][azkar_type]
        
        text = f"📿 {azkar['title']}\n\n"
        text += f"🔤 {azkar['text']}\n\n"
        text += f"📊 العدد: {count}/{azkar['target']}"
        
        if count >= azkar['target']:
            text += "\n\n🎉 تبارك الله! لقد أكملت العدد المطلوب"
            
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("➕ ذكر", callback_data=f"count_{azkar_type}"))
        markup.add(
            types.InlineKeyboardButton("🔄 إعادة تعيين", callback_data=f"reset_{azkar_type}"),
            types.InlineKeyboardButton("📿 الأذكار", callback_data="azkar_menu")
        )
        
        self.bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id, 
            reply_markup=markup
        )
    
    def increment_azkar(self, call, azkar_type):
        """زيادة عدد الأذكار"""
        user_id = call.from_user.id
        if user_id not in self.user_counts:
            self.user_counts[user_id] = {}
        if azkar_type not in self.user_counts[user_id]:
            self.user_counts[user_id][azkar_type] = 0
            
        self.user_counts[user_id][azkar_type] += 1
        self.start_azkar_counter(call, azkar_type)
    
    def reset_azkar(self, call, azkar_type):
        """إعادة تعيين عداد الأذكار"""
        user_id = call.from_user.id
        if user_id not in self.user_counts:
            self.user_counts[user_id] = {}
        
        self.user_counts[user_id][azkar_type] = 0
        self.start_azkar_counter(call, azkar_type)
    
    def send_random_content(self, message):
        """إرسال محتوى عشوائي"""
        content_type = random.choice(list(self.content.keys()))
        content = random.choice(self.content[content_type])
        
        emoji_map = {
            "morning_azkar": "🌅",
            "evening_azkar": "🌙",
            "quran_verse": "📖",
            "daily_hadith": "📚",
            "religious_post": "✨",
            "companion_story": "👤",
            "daily_dua": "🤲",
            "daily_reminder": "💭"
        }
        
        emoji = emoji_map.get(content_type, "🕌")
        formatted_content = f"{emoji} {content}"
        
        self.bot.send_message(message.chat.id, formatted_content)
    
    def send_to_channel(self, content_type):
        """إرسال المحتوى للقناة"""
        try:
            content = random.choice(self.content[content_type])
            
            emoji_map = {
                "morning_azkar": "🌅",
                "evening_azkar": "🌙", 
                "quran_verse": "📖",
                "daily_hadith": "📚",
                "religious_post": "✨",
                "companion_story": "👤",
                "daily_dua": "🤲",
                "daily_reminder": "💭"
            }
            
            emoji = emoji_map.get(content_type, "🕌")
            formatted_content = f"{emoji} {content}"
            
            self.bot.send_message(self.channel_id, formatted_content, parse_mode='HTML')
            logger.info(f"✅ تم إرسال {content_type} للقناة")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال {content_type}: {e}")
            return False
    
    def setup_schedule(self):
        """إعداد جدولة المحتوى"""
        logger.info("📅 إعداد جدولة المحتوى...")
        
        for content_type, time_str in self.schedule_times.items():
            schedule.every().day.at(time_str).do(self.send_to_channel, content_type)
            logger.info(f"   📍 {content_type} مجدول في {time_str}")
    
    def run_schedule(self):
        """تشغيل الجدولة"""
        while True:
            try:
                schedule.run_pending()
                time.sleep(30)
            except Exception as e:
                logger.error(f"❌ خطأ في الجدولة: {e}")
                time.sleep(60)
                continue
    
    def start_polling(self):
        """بدء استقبال الرسائل"""
        def polling_thread():
            logger.info("🤖 بدء استقبال الرسائل...")
            while True:
                try:
                    self.bot.polling(none_stop=True, interval=0, timeout=20)
                except Exception as e:
                    logger.error(f"❌ خطأ في استقبال الرسائل: {e}")
                    time.sleep(30)
                    continue
        
        thread = threading.Thread(target=polling_thread, daemon=True)
        thread.start()
        logger.info("✅ بدء استقبال الرسائل بنجاح")
    
    def start(self):
        """تشغيل البوت"""
        logger.info("🚀 بدء تشغيل البوت الإسلامي...")
        
        # إرسال رسالة بدء التشغيل
        try:
            self.bot.send_message(self.channel_id, "🌙 سبحان الله - تم تشغيل البوت بنجاح!")
        except:
            pass
        
        # إعداد الجدولة
        self.setup_schedule()
        
        # بدء استقبال الرسائل
        self.start_polling()
        
        # تشغيل الجدولة
        logger.info("✅ البوت يعمل الآن...")
        self.run_schedule()

def main():
    """الدالة الرئيسية"""
    print("🌙 مرحباً بك في البوت الإسلامي لـ Google Colab")
    print("=" * 50)
    
    # إدخال المعلومات المطلوبة
    bot_token = input("🤖 أدخل توكن البوت: ").strip()
    channel_id = input("📢 أدخل معرف القناة (مثل: @your_channel أو -1001234567890): ").strip()
    
    if not bot_token or not channel_id:
        print("❌ يجب إدخال التوكن ومعرف القناة!")
        return
    
    try:
        # إنشاء وتشغيل البوت
        bot = IslamicBotColab(bot_token, channel_id)
        bot.start()
        
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

if __name__ == "__main__":
    main()