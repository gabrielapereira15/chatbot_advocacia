import os

import telebot
from bdClient import BDClient
from src.messages import Messages

data_base = BDClient()

bot_token = os.environ.get('BOT_TELEGRAM_TOKEN')
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=["Familia"])
def family_option(message):
    bot.reply_to(message, Messages.construction_message)


@bot.message_handler(commands=["Criminal"])
def criminal_option(message):
    bot.reply_to(message, Messages.construction_message)


@bot.message_handler(commands=["Tributaria"])
def tax_option(message):
    bot.reply_to(message, Messages.construction_message)


@bot.message_handler(commands=["Financeiro"])
def financial_option(message):
    bot.reply_to(message, Messages.construction_message)


@bot.message_handler(commands=["Consulta_Processual"])
def process_consult(message):
    bot.reply_to(message, Messages.construction_message)


@bot.message_handler(commands=["Acesso_Administrador"])
def admin_access(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(str(client_id))
    if consult_client["access_level"] == "Admin":
        bot.send_message(client_id, Messages.admin_options)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)


@bot.message_handler(commands=["Liberar"])
def release_client(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(str(client_id))
    if consult_client["access_level"] == "Admin":
        bot.reply_to(message, Messages.construction_message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)


@bot.message_handler(commands=["Cadastrar"])
def register_client(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(str(client_id))
    if consult_client["access_level"] == "Admin":
        bot.reply_to(message, Messages.construction_message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)


@bot.message_handler(commands=["Upload_Andamento"])
def upload_consult(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(str(client_id))
    if consult_client["access_level"] == "Admin":
        bot.reply_to(message, Messages.construction_message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)


@bot.message_handler(commands=["Upload_Custas"])
def upload_tax(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(str(client_id))
    if consult_client["access_level"] == "Admin":
        bot.reply_to(message, Messages.construction_message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)


@bot.message_handler(commands=["Upload_Honorarios"])
def upload_fee(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(str(client_id))
    if consult_client["access_level"] == "Admin":
        bot.reply_to(message, Messages.construction_message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)


def trigger_message(message):
    return True


@bot.message_handler(func=trigger_message)
def initial_message(message):
    client_id = message.from_user.id
    client_name = message.from_user.first_name
    print(client_id, client_name)

    consult_client = data_base.consult_client(str(client_id))
    print("Já é cliente: " + str(consult_client))

    ini_message = "Olá, " + str(client_name) + "!\n\n" + Messages.initial_message_text
    bot.reply_to(message, ini_message)

    if consult_client:
        if consult_client['access_level'] == "Admin":
            options = Messages.optional_menu_admin
        else:
            options = Messages.optional_menu_client
    else:
        options = Messages.optional_menu_unknown
    bot.send_message(client_id, options)


bot.polling()
