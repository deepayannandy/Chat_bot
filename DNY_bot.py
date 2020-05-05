from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import main as replay

def command_handling_fn (update,context):
    a = str(update)
    data = eval(a)
    msg_sender = data['message']['chat']['first_name']
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello "+msg_sender+", How can I help You?")
def msg(update,context):
    a=str(update)
    data = eval(a)
    print(data['message']['chat']['first_name']+" : "+data['message']['text'])
    msg_text=data['message']['text']
    context.bot.send_message(chat_id=update.effective_chat.id, text=replay.chat(msg_text))

def main():
    updater= Updater(token='1068445966:AAGUxOgEp5Kd-87gfiUs9cIFrr5gqbAL2tQ',use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start", command_handling_fn))
    dp.add_handler(MessageHandler(Filters.text, msg))
    updater.start_polling()
    updater.idle()

main()