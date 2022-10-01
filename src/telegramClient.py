import os

import telebot
from bdClient import BDClient
from src.messages import Messages

data_base = BDClient()

bot_token = os.environ.get('BOT_TELEGRAM_TOKEN')
bot = telebot.TeleBot(bot_token)


# OPÇÕES CLIENTES
@bot.message_handler(commands=["Familia"])
def family_option(message):
    bot.reply_to(message, Messages.construction_message)
    initial_message(message)


@bot.message_handler(commands=["Criminal"])
def criminal_option(message):
    initial_message(message)


@bot.message_handler(commands=["Tributaria"])
def tax_option(message):
    bot.reply_to(message, Messages.construction_message)
    initial_message(message)


@bot.message_handler(commands=["Financeiro"])
def financial_option(message):
    bot.reply_to(message, Messages.construction_message)
    initial_message(message)


@bot.message_handler(commands=["Consulta_Processual"])
def process_consult(message):
    bot.reply_to(message, Messages.construction_message)
    initial_message(message)


# ADMINISTRADOR
@bot.message_handler(commands=["Acesso_Administrador"])
def admin_access(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)

    if consult_client is None:
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)
        return
    if consult_client["access_level"] != "Admin":
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)
        return

    bot.send_message(client_id, Messages.admin_options)


@bot.message_handler(commands=["Liberar_acessos"])
def release_client(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)

    if consult_client is None:
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)
        return
    if consult_client["access_level"] != "Admin":
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)
        return

    waiting_for_approval = list(data_base.consult_waiting_approval())
    if len(waiting_for_approval) == 0:
        bot.reply_to(message, "Não existe solicitações de cadastro para liberação no momento.")
        initial_message(message)
        return

    new_client_list = ""
    for new_client in waiting_for_approval:
        new_client_list = new_client_list + "\n" + str(new_client["client_name"] + " - " + new_client["cpf"]
                                                       + "\n/aceitar_" + str(
            new_client["client_id"]) + " ou\n" "/recusar_"
                                                       + str(new_client["client_id"]) + "\n\n")
    bot.send_message(client_id, new_client_list)


@bot.message_handler(regexp="/aceitar_")
def realese_clients(message):
    client_id = int(message.text.split("_")[1])
    consult_client = data_base.consult_client(client_id)
    if consult_client["status"] is False:
        data_base.update_client(consult_client["_id"], "status", True)
        sending_approval_message(client_id)
        bot.reply_to(message, "Solicitação de cadastro aceita.")
    else:
        bot.reply_to(message, "Cadastro não está pendente de liberação. Provavelmente já foi aceito ou recusado.")
        release_client(message)


@bot.message_handler(regexp="/recusar_")
def reject_clients(message):
    client_id = int(message.text.split("_")[1])
    try:
        data_base.delete_document(client_id)
        bot.reply_to(message, "Solicitação de cadastro recusada.")
    except Exception:
        bot.reply_to(message, "Cadastro não está pendente de liberação. Provavelmente já foi aceito ou recusado.")
        release_client(message)


@bot.message_handler(commands=["Upload_Andamento"])
def upload_consult(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)
    if consult_client:
        if consult_client["access_level"] == "Admin":
            bot.reply_to(message, Messages.construction_message)
            initial_message(message)
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            initial_message(message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)


@bot.message_handler(commands=["Upload_Custas"])
def upload_tax(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)
    if consult_client:
        if consult_client["access_level"] == "Admin":
            bot.reply_to(message, Messages.construction_message)
            initial_message(message)
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            initial_message(message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)


@bot.message_handler(commands=["Upload_Honorarios"])
def upload_fee(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)
    if consult_client:
        if consult_client["access_level"] == "Admin":
            bot.reply_to(message, Messages.construction_message)
            initial_message(message)
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            initial_message(message)
    else:
        bot.reply_to(message, Messages.invalid_option_to_client)
        initial_message(message)


def sending_new_clients_to_admin():
    admin_list = list(data_base.consult_all_by_one_parameter("access_level", "Admin"))
    for admin in admin_list:
        bot.send_message(admin["client_id"], Messages.new_client)


# CLIENTES - CADASTRO
def sending_approval_message(client_id):
    bot.send_message(client_id, Messages.accepted_registration)


@bot.message_handler(commands=["Solicitar_Acesso"])
def register_client(message):
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)
    if consult_client is None:
        client_name = message.from_user.first_name
        bot.send_message(client_id, Messages.cpf_request)
        data_base.insert_new_client(client_id, client_name)
    else:
        initial_message(message)


@bot.message_handler(regexp="[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}")
def get_cpf(message):
    cpf = message.text
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)
    if consult_client:
        if consult_client["status"] == "Cadastrando":
            data_base.update_client(consult_client["_id"], "cpf", cpf)
            data_base.update_client(consult_client["_id"], "status", False)
            bot.reply_to(message, Messages.waiting_for_approval)
            sending_new_clients_to_admin()
        else:
            initial_message(message)
    else:
        initial_message(message)


@bot.message_handler(regexp="[0-9]{11}")
def get_cpf(message):
    cpf = message.text
    client_id = message.from_user.id
    consult_client = data_base.consult_client(client_id)
    if consult_client:
        if consult_client["status"] == "Cadastrando":
            data_base.update_client(consult_client["_id"], "cpf", cpf)
            data_base.update_client(consult_client["_id"], "status", False)
            bot.reply_to(message, Messages.waiting_for_approval)
            sending_new_clients_to_admin()
        else:
            initial_message(message)
    else:
        initial_message(message)


@bot.message_handler(commands=["cancelar_solicitacao_acesso"])
def cancel_access_request(message):
    client_id = message.from_user.id
    data_base.delete_document(client_id)
    initial_message(message)


def trigger_message(message):
    return True


@bot.message_handler(func=trigger_message)
def initial_message(message):
    client_id = message.from_user.id
    client_name = message.from_user.first_name
    print(client_id, client_name)

    consult_client = data_base.consult_client(client_id)
    print("Já é cliente: " + str(consult_client))

    if consult_client:
        if consult_client['access_level'] == "Admin":
            options = Messages.optional_menu_admin
        elif consult_client["status"] is False:
            options = Messages.waiting_for_approval
        elif consult_client["status"] == "Cadastrando":
            options = Messages.registering
        else:
            options = Messages.optional_menu_client
    else:
        ini_message = "Olá, " + str(client_name) + "!\n\n" + Messages.initial_message_text
        bot.reply_to(message, ini_message)
        options = Messages.optional_menu_unknown
    bot.send_message(client_id, options)


bot.polling()
