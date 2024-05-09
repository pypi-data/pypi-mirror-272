import sys


class StatusCode:

    @staticmethod
    def charge(http_status, bradesco_code=None, param=None):
        table = {
            (201, None): "Cobrança imediata criada.",
            (400, None): "Requisição com formato inválido.",
            (400, "AP002O"): "campo {0} apresenta o valor zero.",
            (400, "AP004O"): "campo {0} é igual ou menor que zero.",
            (400, "AP006O"): "objeto {0} não respeita o schema.",
            (400, "AP012O"): "location referenciado por {0} apresenta tipo 'cobv' (deveria ser 'cob').",
            (400, "AP014O"): "location referenciado por {0} inexiste.",
            (400, "AP015O"): "location referenciado por {0} já está sendo utilizado por outra cobrança.",
            (400, "AP017O"): "campo {0} corresponde a uma conta que não pertence a este usuário recebedor.",
            (400, "AP018A"): "cobrança já existe, não está ATIVA, e a presente requisição busca alterá-la.",
            (400, "AP022"): "Ambos os parâmetros cpf e cnpj estão preenchidos.",
            (403, None): "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None): "Recurso solicitado não foi encontrado.",
            (412, "4001"): "Identificador da transação já está em uso.",
            (412, "4002"): "Chave do DICT inválida.",
            (412, "4004"): "Não foi encontrado dados ao consultar a chave DICT no CWS.",
            (412, "4005"): "Não foi encontrado dados ao consultar a chave DICT no CWS.",
            (412, "4006"): "Data de expiração inferior à data de processamento.",
            (412, "4010"): "A chave informada não faz parte do cpf/cnpj.",
            (412, "4011"): "O Parceiro informado não está autorizado para cadastrar ou editar uma cobrança para a chave pix informada.",
            (500, "4005"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5001"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5002"): "Ocorreu um erro na comunicação com o CWS.",
            (500, "5008"): "Não foi possível cadastrar a cobrança devido a problemas internos.",
            (500, "5010"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5020"): "Erro de comunicação Bacen.",
            (500, "5030"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (503, None): "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)

    @staticmethod
    def getCharge(http_status, bradesco_code=None, param=None):
        table = {
            (200, None): "Requisição realizada com sucesso.",
            (204, "4004"): "Não foi possível encontrar informações da cobranca com txid informado.",
            (400, None): "Requisição com formato inválido.",
            (400, "AP036"): "O parâmetro revisao corresponde a uma revisão inexistente para a cobrança apontada pelo parâmetro txid.",
            (400, "4000"): "Dados de requisição incorretos.",
            (403, None): "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None): "Recurso solicitado não foi encontrado.",
            (404, "4004"): "Não foi possivel encontrar informações da cobrança com Txid informado.",
            (500, "5001"): "Erro inesperado, entre em contato com o suporte Bradesco. Ocorreu um erro na comunicacao com o banco de dados.",
            (500, "5002"): "Ocorreu um erro na comunicação com o CWS.",
            (500, "5010"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5020"): "Erro de comunicação Bacen.",
            (500, "5030"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (503, None): "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)

    @staticmethod
    def refund(http_status, bradesco_code=None, param=None):
        table = {
            (200, None), "Requisição realizada com sucesso.",
            (201, None), "Dados da devolução.",
            (400, "AP006"), "O objeto {0} não respeita o schema.",
            (400, "AP037"), "A presente requisição de devolução, em conjunto com as demais prévias devoluções, se aplicável, excederia o valor do pix originário.",
            (400, "AP038"), "A devolução referenciada pelo e2eid e id não existe.",
            (400, "4000"), "Dados de requisição incorretos.",
            (403, None), "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None), "Recurso solicitado não foi encontrado.",
            (500, "5001"), "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5002"), "Ocorreu um erro na comunicação com o CWS.",
            (500, "5010"), "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5020"), "Erro de comunicação Bacen.",
            (500, "5030"), "Erro inesperado, entre em contato com o suporte Bradesco.",
            (503, None), "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)

    @staticmethod
    def getRefund(http_status, bradesco_code=None, param=None):
        table = {
            (200, None): "Requisição realizada com sucesso.",
            (400, "AP006"): "O objeto {0} não respeita o schema.",
            (400, "AP037"): "A presente requisição de devolução, em conjunto com as demais prévias devoluções, se aplicável, excederia o valor do pix originário.",
            (400, "AP038"): "A devolução referenciada pelo e2eid e id não existe.",
            (400, "4000"): "Dados de requisição incorretos",
            (403, None): "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None): "Recurso solicitado não foi encontrado.",
            (500, "5001"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5002"): "Ocorreu um erro na comunicação com o CWS.",
            (500, "5010"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, "5020"): "Erro de comunicação Bacen.",
            (500, "5030"): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (503, None): "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)

    @staticmethod
    def webhook(http_status, bradesco_code=None, param=None):
        table = {
            (200, None): "Requisição realizada com sucesso.",
            (400, None): "O parâmetro chave não corresponde a uma chave DICT válida.",
            (400, None): "O parâmetro chave não corresponde a uma chave DICT pertencente a este usuário recebedor.",
            (400, None): "Campo webhook.webhookUrl não respeita o schema.",
            (400, 4000): "Dados de requisição incorretos.",
            (403, None): "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None): "Recurso solicitado não foi encontrado.",
            (500, 5001): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, 5002): "Ocorreu um erro na comunicação com o CWS.",
            (500, 5010): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (500, 5020): "Erro de comunicação Bacen.",
            (500, 5030): "Erro inesperado, entre em contato com o suporte Bradesco.",
            (503, None): "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da (janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)
    
    @staticmethod
    def getWebhook(http_status, bradesco_code=None, param=None):
        table = {
            (200, None): "Dados do Webhook.",
            (403, None): "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None): "Recurso solicitado não foi encontrado.",
            (503, None): "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da (janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)
    
    @staticmethod
    def deleteWebhook(http_status, bradesco_code=None, param=None):
        table = {
            (204, None): "Webhook para notificações Pix foi cancelado.",
            (403, None): "Requisição de participante autenticado que viola alguma regra de autorização.",
            (404, None): "Recurso solicitado não foi encontrado.",
            (503, None): "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.",
        }
        return StatusCode.__get_description(table, http_status, bradesco_code, param)

    @staticmethod
    def __get_description(table, http_status, bradesco_code=None, param=None):
        description = table.get((http_status, bradesco_code), "Descrição não encontrada.")
        return description if '{0}' not in description or not param else description.format(param)
