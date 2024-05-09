class Payload:

    def charge(
        valor_original, # String \d{1,10}\.\d{2}
        chave, # String Chave PIX do integrador.
        txid=None, # String [a-zA-Z0-9]{26,35} PaymentID se não informado o Bradesco gera um ID.
        expiracao=None, # Int Especificado em segundos a partir da data de criação. Quando não informado: default 86400 segundos (24 horas).
        cpf_cnpj=None,
        nome_devedor=None,
        modalidade_alteracao=None, # Permite que o pagador altere o valor.
        solicitacao_pagador=None, # texto a ser apresentado ao pagador 140 caracteres.
        info_adicionais_nome=None,
        info_adicionais_valor=None,
    ):

        # Valores obrigatórios:
        payload = {
            "valor": {
                "original": valor_original,
            },
            "chave": chave,
        }

        if txid:
            payload["txid"] = txid
        if expiracao:
            payload["calendario"] = {"expiracao": expiracao}
        if cpf_cnpj or nome_devedor:
            payload["devedor"] = {}
            if len(cpf_cnpj) == 11:
                payload["devedor"]["cpf"] = cpf_cnpj
            elif len(cpf_cnpj) == 14:
                payload["devedor"]["cnpj"] = cpf_cnpj
            if nome_devedor:
                payload["devedor"]["nome"] = nome_devedor[:200]
        if modalidade_alteracao:
            payload["valor"]["modalidadeAlteracao"] = modalidade_alteracao
        if info_adicionais_nome and info_adicionais_valor:
            payload["infoAdicionais"] = {}
            payload["infoAdicionais"]["nome"] = info_adicionais_nome[:200]
            payload["infoAdicionais"]["valor"] = info_adicionais_valor[:50]
        if solicitacao_pagador:
            payload["solicitacaoPagador"] = solicitacao_pagador[:140]

        return payload

    def refund(e2eid, id, valor, descricao=None, natureza=None):
        payload = {
            "e2eid": e2eid,  # String [a-zA-Z0 9]{32} obrigatório
            # id: Gerado pelo cliente para representar unicamente uma devolução, único por CNPJ do recebedor.
            "id": id,  # String [a-zA-Z0 9 ]{1,35} obrigatório
            "valor": valor,  # String \d{1,10}\.\d{2} obrigatório
            "descricao": descricao,  # String {140} opcional
            # natureza: "ORIGINAL": Devolução é solicitada para um Pix Comum. "RETIRADA": Devolução é solicitada para um Pix Saque.
            "natureza": natureza,  # String {Enum} opcional
        }
        return payload

    def webhook(webhookUrl, chave):
        payload = {
            "webhookUrl": webhookUrl, # URL para notificação
            "chave": chave, # Chave PIX do integrador
        }
        return payload