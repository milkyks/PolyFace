import requests
import shutil
import telebot
import poly_face

token = 'API_TOKEN'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Send me any photo')


@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(message.chat.id, 'Please wait...')
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    while True:
        try:
            r = requests.get('https://api.telegram.org/file/bot{}/{}'.format(token, file.file_path), stream=True)
            r.raw.decode_content = True
            break
        except ConnectionError as e:
            print(e)
    with open('1.jpg', 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    bot.send_message(message.chat.id, poly_face.get_link())


bot.polling()
