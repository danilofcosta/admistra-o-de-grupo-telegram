from t import *
from uteis import *
from telebot import types
from uteis import *
import os,json

@bot.message_handler(commands=["start"])
def welcomeprivate(msg):
    if msg.chat.type == 'private':
        from telebot import types
        markup = types.InlineKeyboardMarkup()
        add_to_group_button = types.InlineKeyboardButton("Adicionar ao Grupo", url="https://t.me/seubot?startgroup=new")
        markup.add(add_to_group_button)

        welcome_message = f"""
        Olá *{msg.from_user.first_name}*!
** [{bot.get_me().first_name}]({bot.get_me().username})** é um bot projetado para facilitar a gestão dos seus grupos de forma segura. Para aproveitar ao máximo as funcionalidades, siga os passos abaixo:

1. **Adicione-me a um supergrupo**: Basta me incluir no grupo que deseja gerenciar.

2. **Conceda permissões de administrador**: Certifique-se de que tenho as permissões necessárias de administrador para que eu possa realizar tarefas no grupo.

*QUAIS SÃO OS COMANDOS?*
Pressione /help para ver todos os comandos disponíveis e entender como utilizá-los.

Espero que você aproveite ao máximo , {msg.from_user.first_name} agradeçe pela preferencia! 😊
        """
        bot.send_message(msg.chat.id, welcome_message, parse_mode='Markdown',reply_markup=markup)


@bot.message_handler(commands=['welcome'])
def welcome_status(msg):
    if is_adm(msg):
        m=msg.text.replace('/welcome ','')
        if m == 'on':
            status={'WELCOME':{'welcome_stutus':True}}
            save(status ,msg.chat.id)
            bot.send_message(msg.chat.id,'boas vindas ativadas ')
        elif m =='off':
            status={'WELCOME':{'welcome_stutus':False}}
            save(status ,msg.chat.id)
            bot.send_message(msg.chat.id,'boas vindas desativadas ')
        elif m=='Sent':
            if msg.reply_to_message:
                dados=pegafileid(msg)
                caption = msg.reply_to_message.caption
                if caption is not None:
                    caption = caption.lstrip()
                new = {'welcome_stutus':{dados[1].lstrip(): {"tipo": dados[0], "fileid":dados[2], "caption":caption}}}
                save(new)
    else:
        bot.send_message(msg.chat.id,'apenas para adms')

@bot.message_handler(commands=["ban", "delban"])
def ban(msg):
    if is_adm(msg):
        if msg.chat.type in ['supergroup', 'channel']:
            chat_admins = bot.get_chat_administrators(msg.chat.id)
            is_admin = any(chat_admin.user.id == msg.from_user.id   for chat_admin in chat_admins)
            if is_admin:
                if msg.reply_to_message:
                    try:
                        user_to_ban_id = msg.reply_to_message.from_user.id
                        bot.ban_chat_member(msg.chat.id, user_to_ban_id)
                        bot.send_message(msg.chat.id, 'Usuário banido')
                        try:
                            bot.delete_message(msg.chat.id,msg.message_id)
                        except:
                            pass
                    except Exception as e:
                        bot.send_message(msg.chat.id, 'Não posso banir um adm mais bem que queria rs')
                else:
                    bot.reply_to(msg, 'Você deve responder a uma mensagem do usuário que deseja banir.')
            else:
                bot.reply_to(msg, "Somente administradores podem usar este comando.")
        else:
            bot.send_message(msg.chat.id,'esse comando so funciana em grupo')
    else:
        bot.send_message(msg.chat.id,'apenas para adms')

@bot.message_handler(commands=["unban"])
def unban(msg):
    try:
        id= msg.text.replace('/unban')
        bot.unban_chat_member(msg.cha.id,id)
    except:
        bot.send_message(msg.chat.id,'passa o id ')


@bot.message_handler(content_types=['new_chat_members'])
def welcome_message(msg):
    try:
        with open(os.path.join('./database',str(msg.chat.id)+'.json'), "r") as arquivo:
            memory = json.load(arquivo)
    except FileNotFoundError:
        status={'WELCOME':{'welcome_stutus':False}}
        save(status ,msg.chat.id)
        with open(os.path.join('./database',str(msg.chat.id)+'.json'), "r") as arquivo:
            memory = json.load(arquivo) 
            if memory['WELCOME']['welcome_stutus']==True :
                    try:
                        memory=load(msg)['WELCOME']
                        send(msg.chat.id,file_id=memory["fileid"],typef=memory["tipo"],nmr=msg.message_id,caption=memory["caption"])
                    except:
                        bot.send_message(msg.chat.id, f"Bem-vindo ao grupo, {msg.from_user.first_name}! 😃\n\n nunca mais saira daqui hahhahahah.")   

def disable_chat_options(chat_id, key):
    chat_config = types.ChatPermissions(
        can_send_messages=key,
        can_send_media_messages=key,
        can_send_polls=False,
        can_send_other_messages=key,
        can_add_web_page_previews=key,
        can_change_info=False,
        can_invite_users=key,
        can_pin_messages=key
    )
    bot.set_chat_permissions(chat_id, chat_config)

@bot.message_handler(commands=['lock', 'unlock'])
def command_disable_chat(msg):
    if is_adm(msg) == True:
        if msg.text.replace('/', '') == 'lock':
            disable_chat_options(msg.chat.id, False)
            bot.send_message(msg.chat.id, "Hora da mimir amigos.Grupo fechado ❤️")
        elif msg.text.replace('/', '') == 'unlock':
            disable_chat_options(msg.chat.id, True)
            bot.send_message(msg.chat.id, "Vamos acordar,o galo ja cantou ,bom dia.")
@bot.message_handler(commands=['del'])
def cleaer(msg):
    bot.clear_reply_handlers_by_message_id(msg.reply_to_message.message_id)

@bot.message_handler(commands=["fdel"])
def delfiltro(msg):
    if is_adm(msg) == True:
        chave = msg.text.replace("/fdel ", "")
        with open(f"{msg.chat.id}.json", "r") as arquivo:
            memory = json.load(arquivo)['Filtros_Chat']
        if chave in memory:
            del memory[chave]
            with open("Dados.json", "w") as arquivo:
                json.dump(memory, arquivo)
            bot.send_message(msg.chat.id, f"Chave {chave} excluída")
        else:
            bot.send_message(msg.chat.id, f"A chave {chave} não foi encontrada")
    else:
        bot.send_message(msg.chat.id,'apenas para adms')

@bot.message_handler(commands=["fdelall"])
def delallfiltro(msg):
  markup = types.InlineKeyboardMarkup()
  confirm_button = types.InlineKeyboardButton('Confirmar', callback_data='confirmar')
  cancel_button = types.InlineKeyboardButton('Cancelar', callback_data='cancelar')
  markup.add(confirm_button, cancel_button)  
  bot.send_message(msg.chat.id, "Você tem certeza de que deseja apagar todos os dados?",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['confirmar', 'cancelar'])
def handle_confirmation(callback_query):
    if callback_query.data == 'confirmar':
        with open("Dados.json", "r") as arquivo:
             memory = json.load(arquivo)
             memory.clear()
        with open("Dados.json", "w") as arquivo:
            json.dump(memory, arquivo)
            bot.answer_callback_query(callback_query.id, 'Todos os dados foram apagados.')
    elif callback_query.data == 'cancelar':
        bot.answer_callback_query(callback_query.id, 'Ação cancelada.')
       
@bot.message_handler(commands=["fall"])      
def allfilter(msg):
    with open(f"{msg.chat.id}.json", "r") as arquivo:
      memory = json.load(arquivo)
    message = "FILTROS SALVOS:\n"
    for filtro in memory['Filtros_Chat']:
        message += f"- `{filtro}`\n"
    bot.send_message(msg.chat.id, message)

@bot.message_handler(commands=["f"])
def s(msg):
    init = {'info_Group': {'Name': msg.chat.title, 'Id_Group': msg.chat.id}}
    save(init, msg.chat.id)
    if is_adm(msg) == True:     
        if msg.reply_to_message:
            dados=pegafileid(msg)
            caption = msg.reply_to_message.caption
            if caption is not None:
                caption = caption.lstrip()
            new = {'Filtros_Chat':{dados[1].lstrip(): {"tipo": dados[0], "fileid":dados[2], "caption":caption}}}
            save(new,msg.chat.id)
            bot.reply_to(msg, f"Salvo com sucesso em {load(msg.chat.id)["info_Group"]["Name"]}")
    else:
        bot.send_message(msg.chat.id,'apenas para adms')
