import os
import telebot
from uteis import *
from telebot import types
from t import *
from commands import *


if os.path.exists('database'):
    pass
else:
    os.makedirs('database')
    
      


def Help_main(chat_id, message_id):
    button_names = ['Banir','welcome','FILTROS','fechar grupo']
    markup = create_botoes(button_names)       
    try:
        bot.edit_message_text("Olá, em que posso te ajudar?", chat_id=chat_id, message_id=message_id, reply_markup=markup)
    except:
        try:
             bot.send_message(text="Olá, em que posso te ajudar?", chat_id=chat_id, reply_markup=markup)
        except telebot.apihelper.ApiTelegramException as e:
            if "Bad Request: message to edit not found" in str(e):
                bot.send_message(chat_id=chat_id, text="Olá, em que posso te ajudar?", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_Bot(msg):
    Help_main(msg.chat.id, msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data in ['Banir', 'voltar','welcome','FILTROS','fechar grupo'])
def handle_confirmation(callback_query):
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id
    data = callback_query.data
    if data == 'FILTROS':
        help='''Comandos:
 - /f <gato> <reply>: Toda vez que alguém disser "gato", o bot responderá com "sentença".Para filtros de várias palavras, cite o gatilho.
 - /fall: Lista todos os filtros de chat.
 - /fdel <trigger>: Impede o bot de responder ao "gato".
 - /fdelall: Interrompe TODOS os filtros no chat atual.  Isto não pode ser desfeito.
 - use os comandos em grupo'''
        markup = create_botoes(['voltar'])
        bot.edit_message_text(help, chat_id, message_id, reply_markup=markup)
   
    if data == 'Banir':
        markup = create_botoes(['voltar'])
        bot.edit_message_text("/ban :Com esse comando você pode banir pessoas, se você for um administrador, é claro.\n /unban se bater o arrepedimento ", chat_id, message_id, reply_markup=markup)
    elif data == 'welcome':
        markup = create_botoes(['voltar'])
        bot.edit_message_text("Use o comando /welcome on para ativar as boas vindas \n/welcomeoff para desativar /welcomeSent use em resposta a uma mensasagem para defina como boas vindas.", chat_id, message_id, reply_markup=markup)
    elif data == 'fechar grupo':
        markup = create_botoes(['voltar'])
        bot.edit_message_text('ei vc n quer que pesssoas mal intecionadas mande coisa erradas durantr a noite no seu grupo temos a soluçao que talvez possa ajudar \n\n/lock use esse comando para fechar o grupo \n/unlock para abrir o grupo  ', chat_id, message_id, reply_markup=markup)
         
    elif data == 'voltar':
        Help_main(chat_id, message_id)

@bot.message_handler(func=lambda f:True)
def responder(m):
    if os.path.exists(os.path.join('./database',str(m.chat.id)+'.json')):
         if m.chat.type != 'private':
            init={'info_Group':{'Name':m.chat.title,'Id_Group':m.chat.id}}
            save(init,m.chat.id)
    try:
        with open(os.path.join('./database',str(m.chat.id)+'.json'), "r",encoding='utf-8') as arquivo:
            memory = json.load(arquivo)
            memory=memory['Filtros_Chat']
    except:
        memory = {}
    if m.text.lower() in memory:
        send(m.chat.id,file_id=memory[m.text]["fileid"],typef=memory[m.text]["tipo"],nmr=m.message_id,caption=memory[m.text]["caption"])
    else:
        pass

print (bot.get_me().first_name)
#bot.polling()
bot.infinity_polling()

