from requestApi import *
from statusCode import *
from environment import *


class BradescoPixCTS:

    def __init__(self, access_token):
        self.access_token = access_token.access_token
        self.environment = Environment(access_token.sandbox)
        self.cert = access_token.cert

    def charge(self, payload, txid=None):
        if txid:
            uri = f"{self.environment.url_api}/cob/{txid}"
            method = "PUT"
        else:
            uri = f"{self.environment.url_api}/cob/"
            method = "POST"

        return RequestApi(uri, method, self.access_token, self.cert, payload)

    def getCharge(self, txid=None, e2eid=None):
        if txid:
            uri = f"{self.environment.url_api}/cob/{txid}"
        elif e2eid:
            uri = f"{self.environment.url_api}/pix/{e2eid}"
        else:
            return "Informe o txid ou o e2eid."

        return RequestApi(uri, "GET", self.access_token, self.cert)

    def refund(self, payload, e2eid, id):
        uri = f"{self.environment.url_api}/pix/{e2eid}/devolucao/{id}"
        return RequestApi(uri, "PUT", self.access_token, self.cert, payload)

    def getRefund(self, e2eid, id):
        uri = f"{self.environment.url_api}/pix/{e2eid}/devolucao/{id}"
        return RequestApi(uri, "GET", self.access_token, self.cert)

    def webhook(self, payload, chave):
        uri = f"{self.environment.url_api}/webhook/{chave}"
        return RequestApi(uri, "PUT", self.access_token, self.cert, payload)

    def getWebhook(self, chave):
        uri = f"{self.environment.url_api}/webhook/{chave}"
        return RequestApi(uri, "GET", self.access_token, self.cert)
    
    def deleteWebhook(self, chave):
        uri = f"{self.environment.url_api}/webhook/{chave}"
        return RequestApi(uri, "DELETE", self.access_token, self.cert)