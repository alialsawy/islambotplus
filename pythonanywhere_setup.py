#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إعداد البوت الإسلامي على PythonAnywhere
نسخة محسنة للتشغيل على PythonAnywhere
"""

import os
import time
import random
import logging
import threading
from datetime import datetime
import schedule
import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException

# إعداد التسجيل للـ PythonAnywhere
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('/home/yourusername/mysite/bot.log'),  # سيتم تغيير yourusername
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("IslamicBot")

class IslamicBotPythonAnywhere:
    def __init__(self):
        """تهيئة البوت للعمل على PythonAnywhere"""
        # قراءة متغيرات البيئة
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.environ.get('TELEGRAM_CHANNEL_ID')
        
        if not self.bot_token or not self.channel_id:
            raise ValueError("يجب تعيين TELEGRAM_BOT_TOKEN و TELEGRAM_CHANNEL_ID في متغيرات البيئة")
        
        # التأكد من أن channel_id ليس None
        self.channel_id = str(self.channel_id)
        
        self.bot = telebot.TeleBot(self.bot_token)
        self.user_counts = {}
        self.is_running = True
        
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
                "🌅 أذكار الصباح\n\n﴿ أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ لَا شَرِيكَ لَهُ ﴾\n\nاللهم ما أصبح بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر.\n\n🌟 بداية يوم مباركة بذكر الله",
                "🌅 أذكار الصباح\n\n﴿ اللَّهُمَّ بِكَ أَصْبَحْنَا وَبِكَ أَمْسَيْنَا وَبِكَ نَحْيَا وَبِكَ نَمُوتُ وَإِلَيْكَ النُّشُورُ ﴾\n\nأعوذ بالله من الشيطان الرجيم، اللَّهُ لَا إِلَـهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ.\n\n✨ الحمد لله على نعمة الإسلام",
                "🌅 أذكار الصباح\n\n﴿ رَضِيتُ بِاللهِ رَبًّا وَبِالإِسْلَامِ دِينًا وَبِمُحَمَّدٍ صَلَّى اللهُ عَلَيْهِ وَسَلَّمَ رَسُولًا ﴾\n\nحَسْبِيَ اللَّهُ لا إِلَـهَ إِلاَّ هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ.\n\n🎯 توكل على الله في كل أمورك"
            ],
            "evening_azkar": [
                "🌙 أذكار المساء\n\n﴿ أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ لَا شَرِيكَ لَهُ ﴾\n\nاللهم ما أمسى بي من نعمة أو بأحد من خلقك فمنك وحدك لا شريك لك، فلك الحمد ولك الشكر.\n\n🌟 ختام يوم بذكر الله العظيم",
                "🌙 أذكار المساء\n\n﴿ اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ ﴾\n\nأستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه.\n\n💫 اللهم أعنا على ذكرك وشكرك",
                "🌙 أذكار المساء\n\n﴿ اللَّهُمَّ عَافِنِي فِي بَدَنِي، اللَّهُمَّ عَافِنِي فِي سَمْعِي، اللَّهُمَّ عَافِنِي فِي بَصَرِي ﴾\n\nلا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير.\n\n🛡️ حماية الله ورعايته"
            ],
            "quran_verse": [
                "📖 آية من القرآن الكريم\n\n﴿ وَمَن يَتَّقِ اللَّهَ يَجْعَل لَّهُ مَخْرَجًا * وَيَرْزُقْهُ مِنْ حَيْثُ لَا يَحْتَسِبُ ﴾\n[الطلاق: 2-3]\n\n🎯 التقوى مفتاح الفرج والرزق. من راقب الله في السر والعلن، فتح له أبواب الخير من حيث لا يتوقع.",
                "📖 آية من القرآن الكريم\n\n﴿ إِنَّ مَعَ الْعُسْرِ يُسْرًا * إِنَّ مَعَ الْعُسْرِ يُسْرًا ﴾\n[الشرح: 5-6]\n\n🌈 بشارة ربانية بأن الفرج آت. مهما اشتدت المحن، فإن اليسر يأتي معها، وليس بعدها فحسب.",
                "📖 آية من القرآن الكريم\n\n﴿ وُجُوهٌ يَوْمَئِذٍ نَّاضِرَةٌ * إِلَىٰ رَبِّهَا نَاظِرَةٌ ﴾\n[القيامة: 22-23]\n\n✨ أعظم نعيم في الجنة هو النظر إلى وجه الله الكريم. اللهم اجعلنا من أهل هذا النعيم العظيم."
            ],
            "daily_hadith": [
                "📚 حديث شريف\n\n\"الدين النصيحة، قلنا: لمن يا رسول الله؟ قال: لله ولكتابه ولرسوله ولأئمة المسلمين وعامتهم\"\n🌟 رواه مسلم\n\n💡 النصح الصادق من أسس الدين. كن ناصحاً أميناً لله ثم للناس، فهذا جوهر الإيمان.",
                "📚 حديث شريف\n\n\"المؤمن للمؤمن كالبنيان يشد بعضه بعضاً\"\n🌟 رواه البخاري ومسلم\n\n🤝 التعاون والتكافل أساس قوة الأمة. كن سنداً لإخوانك كما تحب أن يكونوا سنداً لك.",
                "📚 حديث شريف\n\n\"من كان في حاجة أخيه كان الله في حاجته، ومن فرج عن مسلم كربة فرج الله عنه كربة من كرب يوم القيامة\"\n🌟 رواه البخاري ومسلم\n\n❤️ الجزاء من جنس العمل. من أحسن إلى الناس أحسن الله إليه، ومن فرج كربهم فرج الله كربه."
            ],
            "religious_post": [
                "✨ بوست ديني\n\n🌙 في هدوء الليل وسكونه، تشع روحانية الذكر والدعاء. هذه اللحظات المباركة هي موعدنا الحقيقي مع الخالق جل وعلا.\n\n📿 اجعل من ليلك حديقة إيمان:\n• قراءة القرآن بتدبر وخشوع\n• الاستغفار والتوبة النصوح\n• الدعاء بانكسار وحضور قلب\n• تسبيح الله وحمده\n\n💎 فالليل خير جليس للمؤمن التائب",
                "✨ بوست ديني\n\n🌅 مع إشراقة كل فجر جديد، يمنحنا الله فرصة ذهبية للبداية من جديد. كل يوم صفحة بيضاء نكتب فيها قصة حياتنا.\n\n🎯 اجعل يومك مليئاً بالخير:\n• ذكر الله في كل وقت وحال\n• العمل الصالح النافع للناس\n• الإحسان والرحمة بالخلق\n• طلب العلم والحكمة\n\n🌟 فكل لحظة في الحياة أمانة ستُسأل عنها يوم القيامة",
                "✨ بوست ديني\n\n🤲 الدعاء سلاح المؤمن وعدته في كل أحواله. به يستجلب الخير، ويدفع الشر، ويحقق الأماني.\n\n🔑 آداب الدعاء المستجاب:\n• الوضوء والطهارة\n• استقبال القبلة واستحضار عظمة الله\n• البدء بالحمد والثناء والصلاة على النبي\n• الدعاء بأسماء الله الحسنى\n• الختام بالصلاة على النبي والتأمين\n\n💫 ادع الله وأنت موقن بالإجابة، فهو القادر على كل شيء"
            ],
            "companion_story": [
                "👤 قصة صحابي - أبو بكر الصديق رضي الله عنه\n\n💎 الصاحب الأول والصديق الأعظم\n\nكان أول من آمن بالنبي ﷺ من الرجال، ولم يتردد لحظة واحدة. قال فيه النبي: \"ما دعوت أحداً إلى الإسلام إلا كانت له كبوة إلا أبا بكر\".\n\n🌟 موقف مؤثر:\nفي رحلة الهجرة، اختبأ مع النبي في غار ثور. لما اقترب المشركون قال: 'يا رسول الله، لو نظر أحدهم تحت قدميه لرآنا!' فقال النبي: 'يا أبا بكر، ما ظنك باثنين الله ثالثهما؟'\n\n💝 الدرس: الثقة الكاملة بالله تطرد الخوف وتجلب الطمأنينة",
                "👤 قصة صحابي - عمر بن الخطاب رضي الله عنه\n\n⚔️ الفاروق الذي فرق بين الحق والباطل\n\nكان من أشد أعداء الإسلام، لكن الله هداه فأصبح من أعظم المدافعين عنه. قال النبي ﷺ: \"اللهم أعز الإسلام بأحب الرجلين إليك: عمر بن الخطاب أو عمرو بن هشام\".\n\n🌟 موقف مؤثر:\nلما تولى الخلافة، كان يتفقد الرعية بنفسه ليلاً. ذات ليلة سمع بكاء أطفال، فتبع الصوت ووجد أماً تطبخ الماء والحصى لتسكت أطفالها الجياع. فبكى عمر وحمل الطعام بنفسه.\n\n💝 الدرس: العدل والرحمة والتواضع أساس القيادة الحقة",
                "👤 قصة صحابي - عثمان بن عفان رضي الله عنه\n\n🕊️ ذو النورين الحيي الكريم\n\nتزوج ابنتي النبي ﷺ رقية ثم أم كلثوم، فسمي ذا النورين. كان من أكثر الصحابة حياءً وكرماً، جهز جيش العسرة بماله.\n\n🌟 موقف مؤثر:\nعندما حوصر في بيته، نصحه الصحابة بالقتال، فقال: \"لا أكون أول من خلف رسول الله ﷺ في أمته بسفك الدماء\". فاختار الصبر حتى قُتل وهو يتلو القرآن.\n\n💝 الدرس: الحياء والكرم والصبر على الأذى من صفات المؤمن الحق"
            ],
            "daily_dua": [
                "🤲 دعاء مستجاب\n\n\"رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ\"\n\n🕌 هذا الدعاء الجامع من أحب الأدعية إلى الله، يشمل خير الدنيا والآخرة. ادع به في كل سجدة وبين السجدتين.",
                "🤲 دعاء مستجاب\n\n\"اللَّهُمَّ اهْدِنِي فِيمَن هَدَيْتَ وَعَافِنِي فِيمَن عَافَيْتَ وَتَوَلَّنِي فِيمَن تَوَلَّيْتَ\"\n\n✨ دعاء القنوت المبارك. اطلب من الله الهداية في كل أمورك، والعافية في دينك وبدنك، وأن يتولاك برحمته.",
                "🤲 دعاء مستجاب\n\n\"اللَّهُمَّ أَعِنِّي عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ\"\n\n🌟 علمه النبي ﷺ لمعاذ بن جبل. ادع بهذا الدعاء بعد كل صلاة، فهو طريق الوصول إلى أعلى درجات العبودية."
            ],
            "daily_reminder": [
                "💭 تذكرة إيمانية\n\n\"وَمَا خَلَقْتُ الْجِنَّ وَالْإِنسَ إِلَّا لِيَعْبُدُونِ\"\n[الذاريات: 56]\n\n🎯 تذكر الهدف الأسمى من وجودك في هذه الحياة. كل نفس تتنفسه فرصة للتقرب إلى الله أكثر.",
                "💭 تذكرة إيمانية\n\n\"الصلاة عماد الدين، من أقامها فقد أقام الدين، ومن هدمها فقد هدم الدين\"\n[حديث شريف]\n\n🕌 حافظ على صلاتك في وقتها مع الجماعة، فهي الركن الذي لا يسقط بحال من الأحوال.",
                "💭 تذكرة إيمانية\n\n\"وَتَزَوَّدُوا فَإِنَّ خَيْرَ الزَّادِ التَّقْوَى\"\n[البقرة: 197]\n\n⚡ الدنيا مزرعة الآخرة. كل عمل صالح تقدمه اليوم، تجده غداً في ميزان حسناتك يوم القيامة."
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
        logger.info("✅ تم تهيئة البوت الإسلامي على PythonAnywhere")
        
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
            try:
                self.handle_callback(call)
            except Exception as e:
                logger.error(f"خطأ في معالجة الضغط: {e}")
    
    def send_main_menu(self, message):
        """إرسال القائمة الرئيسية"""
        welcome_text = """🌙 أهلاً وسهلاً بك في البوت الإسلامي
        
🎯 اختر ما تريد:"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📿 عداد الأذكار", callback_data="azkar_menu"),
            types.InlineKeyboardButton("📖 محتوى إسلامي", callback_data="random_content")
        )
        
        try:
            self.bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
        except Exception as e:
            logger.error(f"خطأ في إرسال القائمة الرئيسية: {e}")
    
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
        
        try:
            self.bot.send_message(message.chat.id, text, reply_markup=markup)
        except Exception as e:
            logger.error(f"خطأ في إرسال قائمة الأذكار: {e}")
    
    def handle_callback(self, call):
        """معالجة الضغط على الأزرار"""
        try:
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
        except Exception as e:
            logger.error(f"خطأ في معالجة الاستدعاء: {e}")
    
    def start_azkar_counter(self, call, azkar_type):
        """بدء عداد الأذكار"""
        try:
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
        except Exception as e:
            logger.error(f"خطأ في بدء عداد الأذكار: {e}")
    
    def increment_azkar(self, call, azkar_type):
        """زيادة عدد الأذكار"""
        try:
            user_id = call.from_user.id
            if user_id not in self.user_counts:
                self.user_counts[user_id] = {}
            if azkar_type not in self.user_counts[user_id]:
                self.user_counts[user_id][azkar_type] = 0
                
            self.user_counts[user_id][azkar_type] += 1
            self.start_azkar_counter(call, azkar_type)
        except Exception as e:
            logger.error(f"خطأ في زيادة الأذكار: {e}")
    
    def reset_azkar(self, call, azkar_type):
        """إعادة تعيين عداد الأذكار"""
        try:
            user_id = call.from_user.id
            if user_id not in self.user_counts:
                self.user_counts[user_id] = {}
            
            self.user_counts[user_id][azkar_type] = 0
            self.start_azkar_counter(call, azkar_type)
        except Exception as e:
            logger.error(f"خطأ في إعادة تعيين الأذكار: {e}")
    
    def send_random_content(self, message):
        """إرسال محتوى عشوائي"""
        try:
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
        except Exception as e:
            logger.error(f"خطأ في إرسال المحتوى العشوائي: {e}")
    
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
        while self.is_running:
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
            while self.is_running:
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
        try:
            logger.info("🚀 بدء تشغيل البوت الإسلامي على PythonAnywhere...")
            
            # إرسال رسالة بدء التشغيل
            try:
                self.bot.send_message(self.channel_id, "🌙 سبحان الله - تم تشغيل البوت بنجاح على PythonAnywhere!")
                logger.info("✅ تم إرسال رسالة بدء التشغيل")
            except Exception as e:
                logger.error(f"❌ خطأ في إرسال رسالة البدء: {e}")
            
            # إعداد الجدولة
            self.setup_schedule()
            
            # بدء استقبال الرسائل
            self.start_polling()
            
            # تشغيل الجدولة
            logger.info("✅ البوت يعمل الآن بكامل قوته...")
            self.run_schedule()
            
        except KeyboardInterrupt:
            logger.info("🛑 تم إيقاف البوت بواسطة المستخدم")
            self.is_running = False
        except Exception as e:
            logger.error(f"❌ خطأ عام في تشغيل البوت: {e}")
            # إعادة التشغيل التلقائي
            time.sleep(60)
            self.start()

def main():
    """الدالة الرئيسية"""
    try:
        bot = IslamicBotPythonAnywhere()
        bot.start()
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        # إعادة المحاولة بعد دقيقة
        time.sleep(60)
        main()

if __name__ == "__main__":
    main()