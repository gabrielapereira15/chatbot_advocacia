class Contacts:
    lawyers = {"Criminal": {"Nome": "Thayna", "Fone": "+5511964963320"},
                 "Família": {"Nome": "Eliete", "Fone": "+5511951235300"},
                 "Tributário": {"Nome": "Eliete", "Fone": "+5511951235300"}}


class Messages:
    construction_message = "Obrigada por usar o nosso canal de atendimento.\n" \
                           "Essa opção ainda está em desenvolvimento."

    initial_message_text = "Bem-vindo ao canal de atendimento do escritório EB | Advocacia!\n" \
                           "Nosso horário de atendimento é de segunda à sexta, das 09h às 18h.\n"

    invalid_option_to_client = "Opção inválida para esse usuário.\nPara voltar ao menu inicial digite: Oi"

    waiting_for_approval = "Solicitação de acesso efetuada!\nPor favor, aguarde a aprovação do advogado para " \
                           "liberação do acesso às opções personalizadas.\n\nAssim que o acesso for liberado " \
                           "enviaremos uma notificação."

    cpf_request = "Por favor, informe seu CPF   (Ex: 000.000.000-00)"

    registering = "Solicitação de acesso pendente de finalização.\nPara continuar insira o seu CPF (Ex: " \
                  "000.000.000-00) ou para cancelar a solicitação de acesso clique em"

    accepted_registration = "Olá, seja bem-vindo! Seu cadastro foi aceito pelo(a) advogado(a).\nA partir de agora " \
                            "você tem acesso a opções exclusivas para clientes.\nClique em /iniciar para acessá-las."

    new_client = "Olá, Dr.(a)! Você tem novos clientes solicitando acesso.\nClique em /Liberar_acessos para liberar " \
                 "ou recusar as novas solicitações. "

    whats_redirect_criminal = "Ok, para entrar em contato com a(o) Dr(a). " + Contacts.lawyers["Criminal"]["Nome"] + " da área Criminal, clique no link abaixo: \n\nhttps://wa.me/" + Contacts.lawyers["Criminal"]["Fone"] + ""

    whats_redirect_familia = "Ok, para entrar em contato com a(o) Dr(a). " + Contacts.lawyers["Família"]["Nome"] + " da área da Família, clique no link abaixo: \n\nhttps://wa.me/" + Contacts.lawyers["Família"]["Fone"] + ""

    whats_redirect_tributario = "Ok, para entrar em contato com a(o) Dr(a). " + Contacts.lawyers["Tributário"]["Nome"] + " da área Tributária, clique no link abaixo: \n\nhttps://wa.me/" + Contacts.lawyers["Tributário"]["Fone"] + ""
