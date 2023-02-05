import logging
import os

from telegram import (ChatAction)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from revChatGPT.ChatGPT import Chatbot

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def configure():
    chatbot_config = {
        "email": os.getenv("OPENAI_USER"),
        "password": os.getenv("OPENAI_PASSWORD"),
        "isMicrosoftLogin": os.getenv("OPENAI_MICROSOFT_LOGIN")
    }
    return Chatbot(chatbot_config)

chatbot = configure()

# Telegram bot name
MY_NAME = os.getenv("TELEGRAM_BOT_NAME")
# Telegram bot token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Whitelisted groups
ALLOWED_GROUPS = os.getenv("TELEGRAM_GROUP_WHITELIST")

# Telegram bot functions
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am a bot that uses ChatGPT to generate responses. You can ask me anything, and I will try my best to respond.')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('I am here to help you! Just ask me a question or send me a message, and I will try my best to respond using ChatGPT.')

def bot_was_mentioned(update):
    for entity in update.message.entities:
        if entity.type == "mention":
            user_name = update.message.text[entity.offset:entity.offset+entity.length]
            if user_name == MY_NAME:
                return True
    return False

def chatgpt_response(update, context):
    if bot_was_mentioned(update):
        # Pretend that the bot is typing
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        # Generate a response using ChatGPT
        response = chatbot.ask(prompt=update.message.text, conversation_id=chatbot.config.get("conversation"))
        # Send the response to the user
        update.message.reply_text(response["message"])

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

if __name__ == "__main__":
    """Start the bot."""
    # Create the Updater and pass it the bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - chatgpt_response on Telegram
    dp.add_handler(MessageHandler(Filters.text & Filters.chat(ALLOWED_GROUPS) & Filters.entity('mention'), chatgpt_response))

    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()