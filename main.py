from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = 'YOURE_TOKEN'
BOT_USERNAME: Final = '@your_bot_username'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command, you can add whatever text you want here.')


def handle_response(text) -> str:
    # Create your own response logic

    if 'hello' in text:
        return 'Hey there!'

    if 'how are you' in text:
        return 'I\'m good!'

    return 'I don\'t understand'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = handle_response(text)

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: [{message_type}]')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group

    # Reply normal if the message is in private
    print(response)
    await update.message.reply_text(response)


# Log errors
def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling()
