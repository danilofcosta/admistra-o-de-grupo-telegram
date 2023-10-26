import telebot,json,os,re
from telebot import types
from t import *

def create_botoes(button_names):
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(name, callback_data=name) for name in button_names]
    markup.add(*buttons)
    return markup

def save(data,namefile="Dados.json"):
    namefile=os.path.join('./database',str(namefile)+'.json')
    try:
        with open(namefile, "r") as arquivo:
           new= json.load(arquivo)
    except FileNotFoundError:        
        new={}
    new.update(data)
    with open(namefile, "w") as arquivo:
        json.dump(new, arquivo, indent=2)
      

def send(chat_id=None,file_id=None,typef=None,nmr=None, caption=None):
    #print(chat_id,file_id,nmr,typef)
    if typef == "animation":
            bot.send_animation(chat_id, file_id,reply_to_message_id=nmr,caption=caption)

    elif typef == "photo":
            bot.send_photo(chat_id, file_id,reply_to_message_id=nmr,caption=caption)

    elif typef == "audio":
        bot.send_audio(chat_id, file_id,reply_to_message_id=nmr,caption=caption)
        

    elif typef == "document":
        bot.send_document(chat_id, file_id,reply_to_message_id=nmr,caption=caption)

    elif typef == "sticker":
        bot.send_sticker(chat_id, file_id,reply_to_message_id=nmr)
        

    elif typef == "video":
        bot.send_video(chat_id , file_id,caption=caption)
        print("vou enviar um vídeo")
    elif typef == "text" :
               bot.send_message(chat_id,file_id,reply_to_message_id=nmr)
    else:
       print('queijo azul')

def pegafileid(msg):
  m=msg.reply_to_message
  if m.content_type == 'text' :
     d=['text',msg.text.replace("/f","").lower(),m.text,msg.text]
     return d
  else:
      match2 = re.search(r'content_type[^,]*', str(m))
      type=match2.group(0).replace("content_type': '", "")[:-1]
      match = re.search(r'file_id[^,]*', str(m))
      file_id = match.group(0).replace("file_id': '", "")[:-1]
      d=[type,msg.text.replace("/f","").lower(),file_id]
      return d

def load(namefile):
    with open(os.path.join('./database',str(namefile)+'.json'), "r") as arquivo:
        new= json.load(arquivo)
    return new
def is_adm(msg):
    if msg.chat.type == 'private':
        bot.reply_to(msg,'Use em um grupo')
        return False

    elif msg.chat.type in ['supergroup', 'channel']:
        chat_admins = bot.get_chat_administrators(msg.chat.id)
        is_admin = any(chat_admin.user.id == msg.from_user.id   for chat_admin in chat_admins)
        if is_admin:
            return True
        else:
            return False
       