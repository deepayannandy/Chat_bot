from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import main as replay
import requests
import json



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
def audio(update,context):
    a = str(update)
    data = eval(a)
    print("Audio message Processing! ")
    x=data["message"]["voice"]['file_id']
    text=download_voice(x)
    print(data['message']['chat']['first_name'] + " : " + text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=replay.chat(text))

def download_voice(x):
    url= "https://api.telegram.org/bot1068445966:AAGUxOgEp5Kd-87gfiUs9cIFrr5gqbAL2tQ/getFile"
    r=requests.post(url,params={'file_id':x})
    response=json.loads(r.content)
    #print(response)
    voice_url="https://api.telegram.org/file/bot1068445966:AAGUxOgEp5Kd-87gfiUs9cIFrr5gqbAL2tQ/"+response['result']['file_path']
    #print(voice_url)
    rec=requests.get(voice_url)
    audio=rec.content
    api_url="https://gateway-lon.watsonplatform.net/speech-to-text/api/v1/recognize"
    r= requests.post(url=api_url, data=audio, headers={'Content-Type':'audio/ogg'},auth=('apikey','i9huqEEcDGBWHBknbtsSROctsb1LpZVqwTzT4lN9Y4m4'))
    response= json.loads(r.content)
    try:
        a = str(response)
        data = eval(a)
        #print(data['results'])
        text=data['results'][0]['alternatives'][0]['transcript']
        print(text)
        return text
    except:
        return "I didn't understand what you say!"


def main():
    updater= Updater(token='1068445966:AAGUxOgEp5Kd-87gfiUs9cIFrr5gqbAL2tQ', use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start", command_handling_fn))
    dp.add_handler(MessageHandler(Filters.text, msg))
    dp.add_handler(MessageHandler(Filters.voice, audio))
    updater.start_polling()
    updater.idle()

main()