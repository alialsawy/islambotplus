"""
Islamic Telegram Bot - Vercel Entry Point
Serverless version for Vercel deployment
"""

import os
import sys
import json
from flask import Flask, request, jsonify
from telegram_bot import TelegramBot
from content_generator import IslamicContentGenerator
from bot_config import BotConfig
from logger_config import setup_logger

# Initialize logger
logger = setup_logger()

# Initialize Flask app
app = Flask(__name__)

# Global bot instance
bot_instance = None
config = None

def initialize_bot():
    """Initialize bot components"""
    global bot_instance, config
    
    try:
        # Load configuration
        config = BotConfig()
        config.validate()
        
        # Initialize bot components
        telegram_bot = TelegramBot(config.telegram_token, config.channel_id)
        content_generator = IslamicContentGenerator()
        
        # Test connections
        if not telegram_bot.test_connection():
            logger.error("❌ Failed to connect to Telegram")
            return False
            
        logger.info("✅ Bot initialized successfully for Vercel")
        bot_instance = {
            'telegram_bot': telegram_bot,
            'content_generator': content_generator,
            'config': config
        }
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize bot: {e}")
        return False

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "bot": "Islamic Telegram Bot",
        "version": "1.0.0",
        "message": "سبحان الله - البوت يعمل بنجاح"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Telegram webhook"""
    try:
        if not bot_instance:
            if not initialize_bot():
                return jsonify({"error": "Bot initialization failed"}), 500
        
        # Process webhook data
        data = request.get_json()
        logger.info(f"📩 Received webhook: {data}")
        
        # Handle the webhook
        # This is a simplified webhook handler
        # In a full implementation, you'd process the update here
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/send-content', methods=['POST'])
def send_content():
    """Manually trigger content sending"""
    try:
        if not bot_instance:
            if not initialize_bot():
                return jsonify({"error": "Bot initialization failed"}), 500
        
        data = request.get_json()
        content_type = data.get('type', 'daily_reminder')
        
        # Generate and send content
        if bot_instance and isinstance(bot_instance, dict):
            content = bot_instance['content_generator'].generate_content(content_type)
            result = bot_instance['telegram_bot'].send_formatted_content(content_type, content)
        else:
            return jsonify({"error": "Bot not initialized"}), 500
        
        return jsonify({
            "status": "success",
            "content_type": content_type,
            "message": "Content sent successfully"
        })
        
    except Exception as e:
        logger.error(f"❌ Send content error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test_bot():
    """Test bot functionality"""
    try:
        if not bot_instance:
            if not initialize_bot():
                return jsonify({"error": "Bot initialization failed"}), 500
        
        # Test message
        test_message = "سبحان الله - اختبار البوت على Vercel"
        if bot_instance and isinstance(bot_instance, dict):
            result = bot_instance['telegram_bot'].send_message(test_message)
        else:
            return jsonify({"error": "Bot not initialized"}), 500
        
        return jsonify({
            "status": "success",
            "message": "Test message sent successfully",
            "telegram_result": result
        })
        
    except Exception as e:
        logger.error(f"❌ Test error: {e}")
        return jsonify({"error": str(e)}), 500

# Initialize bot on startup
if __name__ != '__main__':
    # Running on Vercel
    initialize_bot()

if __name__ == '__main__':
    # Running locally
    initialize_bot()
    app.run(host='0.0.0.0', port=8080, debug=False)