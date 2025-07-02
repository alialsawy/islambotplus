"""
Combined Bot Handler
Handles both scheduled content posting and interactive azkar counter
"""

import threading
import time
import telebot
from telebot import types
from logger_config import setup_logger

logger = setup_logger()

class CombinedBotHandler:
    def __init__(self, bot_token, channel_id, scheduler, azkar_counter):
        """Initialize combined bot handler"""
        self.bot = telebot.TeleBot(bot_token)
        self.channel_id = channel_id
        self.scheduler = scheduler
        self.azkar_counter = azkar_counter
        self.running = False
        
        # Setup message handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.send_main_menu(message)
        
        @self.bot.message_handler(commands=['menu', 'القائمة'])
        def menu_command(message):
            self.send_main_menu(message)
        
        @self.bot.message_handler(commands=['azkar', 'اذكار'])
        def azkar_command(message):
            self.send_azkar_menu(message)
        
        @self.bot.message_handler(commands=['count', 'عد'])
        def count_command(message):
            self.azkar_counter.show_user_counts(message)
        
        @self.bot.message_handler(commands=['reset', 'مسح'])
        def reset_command(message):
            self.azkar_counter.reset_user_counts(message)
        
        @self.bot.message_handler(commands=['schedule', 'جدول'])
        def schedule_command(message):
            self.show_schedule(message)
        
        @self.bot.message_handler(commands=['help', 'مساعدة'])
        def help_command(message):
            self.send_help(message)
        
        # Use azkar_counter's callback handler
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.azkar_counter.handle_callback(call)
    
    def send_main_menu(self, message):
        """Send main bot menu"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Main features
        azkar_btn = types.InlineKeyboardButton("📿 حاسبة الأذكار", callback_data="menu")
        schedule_btn = types.InlineKeyboardButton("📅 جدول النشر", callback_data="schedule")
        markup.add(azkar_btn, schedule_btn)
        
        # Additional options
        help_btn = types.InlineKeyboardButton("❓ المساعدة", callback_data="help")
        markup.add(help_btn)
        
        welcome_text = """
🕌 مرحباً بك في بوت المحتوى الإسلامي

🤖 هذا البوت يقدم لك:

📿 حاسبة الأذكار التفاعلية
📅 نشر المحتوى الإسلامي التلقائي
📖 آيات قرآنية وأحاديث شريفة
🤲 أدعية وتذكيرات إيمانية

اختر ما تريد من القائمة أدناه:
        """
        
        self.bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    
    def send_azkar_menu(self, message):
        """Send azkar counter menu"""
        self.azkar_counter.send_azkar_menu(message)
    
    def show_schedule(self, message):
        """Show current posting schedule"""
        schedule_info = self.scheduler.get_schedule_status()
        
        text = "📅 جدول النشر التلقائي:\n\n"
        text += "🌅 أذكار الصباح: 06:00\n"
        text += "📖 آية قرآنية: 08:00\n"
        text += "📚 حديث شريف: 12:00\n"
        text += "💭 تذكرة إيمانية: 17:00\n"
        text += "🤲 دعاء مستجاب: 20:00\n"
        text += "🌙 أذكار المساء: 21:00\n\n"
        
        text += "📊 حالة الجدولة:\n"
        for info in schedule_info:
            text += f"• {info}\n"
        
        text += "\n🔄 البوت ينشر المحتوى تلقائياً حسب الجدول أعلاه"
        
        self.bot.send_message(message.chat.id, text)
    
    def send_help(self, message):
        """Send help information"""
        help_text = """
❓ تعليمات استخدام البوت:

📿 حاسبة الأذكار:
• /azkar أو /اذكار - فتح حاسبة الأذكار
• /count أو /عد - عرض العدد الحالي
• /reset أو /مسح - مسح العداد

📅 المحتوى التلقائي:
• /schedule أو /جدول - عرض جدول النشر
• البوت ينشر المحتوى تلقائياً 6 مرات يومياً

🔧 أوامر عامة:
• /start - القائمة الرئيسية
• /menu أو /القائمة - عرض القائمة
• /help أو /مساعدة - هذه الرسالة

🤖 البوت يعمل على مدار الساعة لخدمتك
        """
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu"))
        
        self.bot.send_message(message.chat.id, help_text, reply_markup=markup)
    
    def start_bot_polling(self):
        """Start bot polling in a separate thread - NEVER STOPS"""
        def bot_polling():
            logger.info("🤖 Starting interactive bot polling...")
            polling_restart_count = 0
            
            while True:  # Infinite polling loop
                try:
                    polling_restart_count += 1
                    logger.info(f"🔄 Bot polling attempt #{polling_restart_count}")
                    
                    # Multiple protection layers for polling
                    while True:
                        try:
                            self.bot.polling(none_stop=True, interval=0, timeout=20)
                        except KeyboardInterrupt:
                            logger.info("📶 Ignoring keyboard interrupt in polling...")
                            time.sleep(2)
                            continue
                        except SystemExit:
                            logger.info("📶 Ignoring system exit in polling...")
                            time.sleep(2)
                            continue
                        except Exception as polling_error:
                            logger.error(f"❌ Polling inner error: {polling_error} - restarting in 10 seconds...")
                            time.sleep(10)
                            break  # Break to restart polling
                            
                except Exception as e:
                    logger.error(f"❌ Bot polling outer error: {e} - restarting in 30 seconds...")
                    time.sleep(30)
                    continue
        
        # Start single polling thread to avoid Telegram conflicts
        bot_thread = threading.Thread(target=bot_polling, daemon=True, name="BotPolling-Main")
        bot_thread.start()
        logger.info("✅ Bot polling thread started")
        
        logger.info("✅ Interactive bot started successfully")
    
    def start_scheduler(self):
        """Start the content scheduler - NEVER STOPS"""
        logger.info("📅 Starting content scheduler...")
        
        scheduler_setup_attempts = 0
        while True:
            try:
                scheduler_setup_attempts += 1
                self.scheduler.setup_schedule()
                logger.info(f"✅ Scheduler setup successful (attempt #{scheduler_setup_attempts})")
                break
            except Exception as setup_error:
                logger.error(f"❌ Scheduler setup failed (attempt #{scheduler_setup_attempts}): {setup_error} - retrying in 15 seconds...")
                time.sleep(15)
                continue
        
        # Run scheduler forever with multiple protection layers
        scheduler_iteration = 0
        consecutive_errors = 0
        
        while True:  # Infinite scheduler loop
            try:
                scheduler_iteration += 1
                
                # Log periodic status
                if scheduler_iteration % 120 == 0:  # Every hour (30s * 120)
                    logger.info(f"📅 Scheduler running strong - iteration #{scheduler_iteration}")
                
                # Run pending tasks with protection
                try:
                    self.scheduler.run_pending_tasks()
                    consecutive_errors = 0  # Reset error counter on success
                except KeyboardInterrupt:
                    logger.info("📶 Ignoring keyboard interrupt in scheduler tasks...")
                    time.sleep(5)
                    continue
                except SystemExit:
                    logger.info("📶 Ignoring system exit in scheduler tasks...")
                    time.sleep(5)
                    continue
                except Exception as task_error:
                    consecutive_errors += 1
                    logger.error(f"❌ Scheduler task error #{consecutive_errors}: {task_error}")
                    
                    # Increase delay for consecutive errors
                    error_delay = min(300, 30 + (consecutive_errors * 30))  # Max 5 minutes
                    time.sleep(error_delay)
                    continue
                
                # Normal operation - check every 30 seconds
                time.sleep(30)
                
            except Exception as e:
                consecutive_errors += 1
                logger.error(f"❌ Scheduler outer error #{consecutive_errors}: {e} - continuing in 60 seconds...")
                time.sleep(60)
                continue
    
    def stop(self):
        """Stop the bot handler - IGNORED! Bot never stops"""
        logger.info("📶 Stop request ignored - Bot will continue running!")
        # Never actually stop - ignore all stop requests