class Environment:

    def __init__(self, sandbox=False):

        self.sandbox = sandbox

        # Production
        if not sandbox:
            self.url_token = 'https://qrpix.bradesco.com.br/oauth/token'
            self.url_api = 'https://qrpix.bradesco.com.br/v2'
        else:
            self.url_token = 'https://qrpix-h.bradesco.com.br/oauth/token'
            self.url_api = 'https://qrpix-h.bradesco.com.br/v2'
