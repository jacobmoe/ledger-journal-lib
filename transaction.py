import os
from string import Template

class Transaction():

    LEDGER_DATE_FORMAT = '%Y/%m/%d'
    TEMPLATE_PATH = './templates/transaction.template'

    template_abs_path = os.path.join(os.path.dirname(__file__), TEMPLATE_PATH)
    template_file = open(template_abs_path, 'rt')
    TEMPLATE_CONTENTS = template_file.read()
    template_file.close()

    def __init__(self, params):
        self.primary_account = params['primary_account']
        self.amount          = params['amount']
        self.description     = params['description']
        self.date            = params['date'].strftime(self.LEDGER_DATE_FORMAT)
        self.payee_account   = params['payee_account']
        self.payee_name      = params['payee_name']
        self.currency        = params['currency']
        self.status          = params['status']
        self.currency_sym    = params['currency_symbol']

    def format(self):
        template = Template(self.TEMPLATE_CONTENTS)
        return template.substitute(self.__dict__)
