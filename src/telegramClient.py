import os

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from bdClient import BDClient
from src.messages import Messages

data_base = BDClient()

bot_token = os.environ.get('BOT_TELEGRAM_TOKEN')
bot = TeleBot(bot_token)


class Customer:
    @staticmethod
    def family_option(message):
        bot.reply_to(message, Messages.whats_redirect_familia)

    @staticmethod
    def criminal_option(message):
        bot.reply_to(message, Messages.whats_redirect_criminal)

    @staticmethod
    def tax_option(message):
        bot.reply_to(message, Messages.whats_redirect_tributario)

    @staticmethod
    def financial_option(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        if consult_client["status"] is False:
            return

        boletos_list = ["familia", "criminal", "tributario"]
        i = 0
        for area in boletos_list:
            try:
                document = open("../repository/boleto_" + str(area) + "_" + str(client_id) + ".pdf", 'rb')
                bot.send_document(client_id, document)
                i += 1
            except FileNotFoundError:
                pass

        if i == 0:
            msg = "Sem boletos cadastrados no momento."
            bot.send_message(client_id, msg)
        else:
            bot.send_message(client_id, "Prontinho, esses são os boletos disponibilizados pelo seu(sua) advogado(a).\n"
                                        "Para voltar ao menu inicial, só nos digitar um: Oi")

    @staticmethod
    def process_consult(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        if consult_client["status"] is False:
            return

        try:
            consult = consult_client["andamento_processual"]
            for processo in consult:
                options = "\n\nProcesso número: " + str(consult[processo]["numero_processo"]) + " | " + str(
                    consult[processo]["local"]) + "\nÚltima atualização: " + str(consult[processo]["andamento"])
                bot.send_message(client_id, options)
            options_list = ["Sim, fazer download.", "Não, estou satisfeito."]
            Menu.build_bottons(options_list, client_id, "Deseja fazer o download das movimentações processuais?")
        except KeyError:
            msg = "Sem andamento processual cadastrado no momento."
            bot.send_message(client_id, msg)

    @staticmethod
    def send_document(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        if consult_client["status"] is False:
            return

        try:
            consult = consult_client["andamento_processual"]
            for processo in consult:
                process_number = str(consult[processo]["numero_processo"]).replace("/", "-")
                document = open("../repository/" + str(process_number) + ".pdf", 'rb')
                bot.send_document(client_id, document)
        except KeyError:
            msg = "Sem andamento processual cadastrado no momento."
            bot.send_message(client_id, msg)

    @staticmethod
    def sending_approval_message(client_id):
        bot.send_message(client_id, Messages.accepted_registration)

    @staticmethod
    def register_client(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            client_name = message.chat.first_name
            bot.send_message(client_id, Messages.cpf_request)
            data_base.insert_new_client(client_id, client_name)
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

    @staticmethod
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
                Admin.sending_new_clients_to_admin()
            else:
                Menu.initial_message(message)
        else:
            Menu.initial_message(message)

    @staticmethod
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
                Admin.sending_new_clients_to_admin()
            else:
                Menu.initial_message(message)
        else:
            Menu.initial_message(message)

    @staticmethod
    def cancel_access_request(message):
        client_id = message.chat.id
        data_base.delete_document(client_id)
        bot.send_message(client_id,
                         "Prontinho, solicitação de acesso cancelada.\nPara voltar ao menu inicial digite: Oi")


class Admin:

    @staticmethod
    def admin_access(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        if consult_client["access_level"] != "Admin":
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        admin_options = ["Liberar acessos", "Upload de andamento", "Upload de custas", "Upload de honorários"]
        text = "Opções disponíveis para administradores:\n\n- Liberar acessos - Para liberar acesso de clientes pendentes.\n\n" \
               "- Upload andamento - Para inserir um andamento processual.\n\n- Upload custas - Para inserir um boleto de " \
               "custas processuais.\n\n- Upload honorários - Para inserir um boleto de custas processuais"
        Menu.build_bottons(admin_options, client_id, text)

    @staticmethod
    def release_client(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        if consult_client["access_level"] != "Admin":
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        waiting_for_approval = list(data_base.consult_waiting_approval())
        if len(waiting_for_approval) == 0:
            bot.reply_to(message, "Não existe solicitações de cadastro para liberação no momento.")
            Admin.admin_access(message)
            return

        new_client_list = ""
        for new_client in waiting_for_approval:
            new_client_list = new_client_list + "\n" + str(new_client["client_name"] + " - " + new_client["cpf"]
                                                           + "\n/aceitar_" + str(
                new_client["client_id"]) + " ou\n" "/recusar_"
                                                           + str(new_client["client_id"]) + "\n\n")
        bot.send_message(client_id, new_client_list)

    @staticmethod
    @bot.message_handler(regexp="/aceitar_")
    def realese_clients(message):
        client_id = int(message.text.split("_")[1])
        consult_client = data_base.consult_client(client_id)
        if consult_client["status"] is False:
            data_base.update_client(consult_client["_id"], "status", True)
            Customer.sending_approval_message(client_id)
            bot.reply_to(message, "Solicitação de cadastro aceita.")
        else:
            bot.reply_to(message, "Cadastro não está pendente de liberação. Provavelmente já foi aceito ou recusado.")
            Admin.release_client(message)

    @staticmethod
    @bot.message_handler(regexp="/recusar_")
    def reject_clients(message):
        client_id = int(message.text.split("_")[1])
        try:
            data_base.delete_document(client_id)
            bot.reply_to(message, "Solicitação de cadastro recusada.")
        except Exception:
            bot.reply_to(message, "Cadastro não está pendente de liberação. Provavelmente já foi aceito ou recusado.")
            Admin.release_client(message)

    @staticmethod
    def upload_consult(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)

        if consult_client is None:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

        if consult_client["access_level"] == "Admin":
            bot.reply_to(message, Messages.construction_message)
            Admin.admin_access(message)
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

    @staticmethod
    def upload_tax(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)
        if consult_client:
            if consult_client["access_level"] == "Admin":
                bot.reply_to(message, Messages.construction_message)
                Admin.admin_access(message)
            else:
                bot.reply_to(message, Messages.invalid_option_to_client)
                return
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

    @staticmethod
    def upload_fee(message):
        client_id = message.chat.id
        consult_client = data_base.consult_client(client_id)
        if consult_client:
            if consult_client["access_level"] == "Admin":
                bot.reply_to(message, Messages.construction_message)
                Admin.admin_access(message)
            else:
                bot.reply_to(message, Messages.invalid_option_to_client)
                return
        else:
            bot.reply_to(message, Messages.invalid_option_to_client)
            return

    @staticmethod
    def sending_new_clients_to_admin():
        admin_list = list(data_base.consult_all_by_one_parameter("access_level", "Admin"))
        for admin in admin_list:
            bot.send_message(admin["client_id"], Messages.new_client)


class Menu:
    @staticmethod
    def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    @staticmethod
    def build_bottons(options, client_id, text):
        if options is not None:
            button_list = []
            for each in options:
                button_list.append(InlineKeyboardButton(each, callback_data=each))
            reply_markup = InlineKeyboardMarkup(Menu.build_menu(button_list, n_cols=2))
            bot.send_message(client_id, text=text, reply_markup=reply_markup)

    @staticmethod
    def trigger_message(message):
        return True

    @staticmethod
    @bot.callback_query_handler(func=trigger_message)
    def callback_options(message):
        if message.data == "Família":
            Customer.family_option(message.message)
        if message.data == "Criminal":
            Customer.criminal_option(message.message)
        if message.data == "Tributário":
            Customer.tax_option(message.message)
        if message.data == "Financeiro":
            Customer.financial_option(message.message)
        if message.data == "Consulta Processual":
            Customer.process_consult(message.message)
        if message.data == "Solicitar Acesso":
            Customer.register_client(message.message)
        if message.data == "Acesso Administrador":
            Admin.admin_access(message.message)
        if message.data == "Sim, fazer download.":
            Customer.send_document(message.message)
            bot.send_message(message.message.chat.id,
                             "Prontinho, ficamos à disposição. Para mais informações, só nos enviar uma "
                             "mensagem :)")
        if message.data == "Não, estou satisfeito.":
            bot.send_message(message.message.chat.id,
                             "Perfeito, ficamos à disposição. Para mais informações, só nos enviar uma "
                             "mensagem :)")
        if message.data == "Cancelar solicitação de acesso":
            Customer.cancel_access_request(message.message)
        if message.data == "Liberar acessos":
            Admin.release_client(message.message)
        if message.data == "Upload de andamento":
            Admin.upload_consult(message.message)
        if message.data == "Upload de custas":
            Admin.upload_tax(message.message)
        if message.data == "Upload de honorários":
            Admin.upload_fee(message.message)
        if message.data == "Encerrar conversa":
            bot.send_message(message.message.chat.id, "Ok, obrigada pelo contato. Tchau, tchau!")

    @staticmethod
    @bot.message_handler(func=trigger_message)
    def initial_message(message):
        client_id = message.from_user.id
        client_name = message.from_user.first_name
        print(client_id, client_name)

        consult_client = data_base.consult_client(client_id)
        print("Já é cliente: " + str(consult_client))

        optional_menu_default = ["Família", "Criminal", "Tributário"]
        optional_menu_admin = "Acesso Administrador"
        optional_menu_client = ["Financeiro", "Consulta Processual"]
        optional_menu_unknown = "Solicitar Acesso"

        if consult_client:
            if consult_client['access_level'] == "Admin":
                optional_menu_default.append(optional_menu_admin)
                for option in optional_menu_client:
                    optional_menu_default.append(option)
                options = optional_menu_default
            elif consult_client["status"] is False:
                bot.send_message(client_id, Messages.waiting_for_approval)
                options = optional_menu_default
            elif consult_client["status"] == "Cadastrando":
                options = ["Cancelar solicitação de acesso"]
                Menu.build_bottons(options, client_id, Messages.registering)
                options = None
            else:
                for option in optional_menu_client:
                    optional_menu_default.append(option)
                options = optional_menu_default
        else:
            ini_message = "Olá, " + str(client_name) + "!\n\n" + Messages.initial_message_text
            bot.reply_to(message, ini_message)
            optional_menu_default.append(optional_menu_unknown)
            options = optional_menu_default

        stop_chat = "Encerrar conversa"
        options.append(stop_chat)
        Menu.build_bottons(options, client_id, 'Por favor, clique em uma das opções de atendimento a seguir:')


bot.polling()
