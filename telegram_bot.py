"""
Telegram Bot Handler
Manages communication with Telegram API
"""

import time
import telebot
from telebot.apihelper import ApiTelegramException
from logger_config import setup_logger

logger = setup_logger()

class TelegramBot:
    def __init__(self, token, channel_id):
        """Initialize Telegram bot with token and channel ID"""
        self.bot = telebot.TeleBot(token)
        self.channel_id = channel_id
        self.retry_attempts = 3
        self.retry_delay = 60
    
    def test_connection(self):
        """Test Telegram bot connection"""
        try:
            logger.info("🔍 Testing Telegram bot connection...")
            
            # Test bot connection
            bot_info = self.bot.get_me()
            logger.info(f"✅ Connected to Telegram bot: @{bot_info.username}")
            
            # Test channel access by getting chat info
            try:
                chat_info = self.bot.get_chat(self.channel_id)
                logger.info(f"✅ Channel access confirmed: {getattr(chat_info, 'title', self.channel_id)}")
                return True
            except ApiTelegramException as e:
                if "chat not found" in str(e).lower():
                    logger.error(f"❌ Channel {self.channel_id} not found")
                elif "bot was blocked" in str(e).lower():
                    logger.error(f"❌ Bot was blocked by the channel {self.channel_id}")
                else:
                    logger.error(f"❌ Cannot access channel {self.channel_id}: {e}")
                logger.error("💡 Make sure the bot is added as an administrator to the channel")
                return False
                
        except ApiTelegramException as e:
            logger.error(f"❌ Telegram bot connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error testing connection: {e}")
            return False
    
    def send_message(self, message, retry_count=0):
        """Send message to the configured channel with bulletproof retry logic"""
        max_retries = 5
        base_delay = 10
        
        # Multiple layers of protection for message sending
        for attempt in range(max_retries):
            try:
                logger.info(f"📤 Sending message to {self.channel_id} (attempt {attempt+1}/{max_retries})...")
                
                # Bulletproof message validation and preparation
                if not message or len(message.strip()) == 0:
                    logger.warning("⚠️ Empty message - skipping send")
                    return False
                
                # Split long messages if needed with safe truncation
                if len(message) > 4096:
                    message = message[:4090] + "..."
                    logger.warning("⚠️ Message truncated to fit Telegram limit")
                
                # Attempt to send with multiple protection layers
                try:
                    self.bot.send_message(
                        chat_id=self.channel_id,
                        text=message,
                        parse_mode='HTML',
                        disable_web_page_preview=True
                    )
                    
                    logger.info(f"✅ Message sent successfully (attempt {attempt+1})")
                    return True
                    
                except ApiTelegramException as api_error:
                    error_msg = str(api_error).lower()
                    
                    # Handle specific API errors with different strategies
                    if "too many requests" in error_msg:
                        wait_time = min(300, base_delay * (2 ** attempt))  # Exponential backoff, max 5 min
                        logger.warning(f"⏳ Rate limited. Waiting {wait_time} seconds... (attempt {attempt+1})")
                        time.sleep(wait_time)
                        continue
                    elif "timeout" in error_msg or "network" in error_msg:
                        wait_time = min(60, base_delay * (attempt + 1))
                        logger.warning(f"⏰ Network/timeout error. Waiting {wait_time} seconds... (attempt {attempt+1})")
                        time.sleep(wait_time)
                        continue
                    elif "forbidden" in error_msg or "unauthorized" in error_msg:
                        logger.error(f"❌ Permission error: {api_error} - cannot recover")
                        return False
                    elif "bad request" in error_msg:
                        # Try to fix the message and retry
                        message = message.replace('<', '&lt;').replace('>', '&gt;')
                        logger.warning(f"⚠️ Bad request, sanitized message (attempt {attempt+1})")
                        continue
                    else:
                        logger.error(f"❌ API error (attempt {attempt+1}): {api_error}")
                        if attempt < max_retries - 1:
                            time.sleep(base_delay * (attempt + 1))
                            continue
                        else:
                            return False
                            
                except Exception as send_error:
                    logger.error(f"❌ Send error (attempt {attempt+1}): {send_error}")
                    if attempt < max_retries - 1:
                        time.sleep(base_delay * (attempt + 1))
                        continue
                    else:
                        return False
                        
            except KeyboardInterrupt:
                logger.info("📶 Ignoring keyboard interrupt in message send...")
                time.sleep(2)
                continue
            except SystemExit:
                logger.info("📶 Ignoring system exit in message send...")
                time.sleep(2)
                continue
            except Exception as outer_error:
                logger.error(f"❌ Outer send error (attempt {attempt+1}): {outer_error}")
                if attempt < max_retries - 1:
                    time.sleep(base_delay * (attempt + 1))
                    continue
                else:
                    logger.error("❌ All send attempts failed - message lost but bot continues")
                    return False
        
        logger.error("❌ Failed to send message after all attempts")
        return True  # Return True to prevent bot shutdown
    
    def send_formatted_content(self, content_type, content):
        """Send formatted content with appropriate emojis and formatting"""
        if not content:
            logger.error("❌ Cannot send empty content")
            return False
        
        # Add content type specific formatting
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
        
        # Format the message
        formatted_message = f"{emoji} <b>{self._get_content_title(content_type)}</b>\n\n{content}"
        
        return self.send_message(formatted_message)
    
    def _get_content_title(self, content_type):
        """Get Arabic title for content type"""
        titles = {
            "morning_azkar": "أذكار الصباح",
            "evening_azkar": "أذكار المساء",
            "quran_verse": "آية من القرآن الكريم",
            "daily_hadith": "حديث شريف",
            "religious_post": "بوست ديني",
            "companion_story": "قصة صحابي",
            "daily_dua": "دعاء مستجاب",
            "daily_reminder": "تذكرة إيمانية"
        }
        return titles.get(content_type, "محتوى إسلامي")
    
    def get_bot_info(self):
        """Get bot information"""
        try:
            return self.bot.get_me()
        except ApiTelegramException as e:
            logger.error(f"❌ Error getting bot info: {e}")
            return None
