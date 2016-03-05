import os, datetime
from string import Template

class Builder():

    LEDGER_DATE_FORMAT = '%Y/%m/%d'
    TEMPLATE_PATH = './templates/transaction.template'

    DEFAULT_DATE_FORMAT     = '%m/%d/%y'
    DEFAULT_CURRENCY_SYMBOL = '$'
    DEFAULT_CURRENCY_TEXT   = ''
    DEFAULT_STATUS_SYMBOL   = '*'
    DEFAULT_ACCOUNT         = ">>>UNKNOWN ACCOUNT<<<"
    DEFAULT_PAYEE           = ">>>UNKNOWN PAYEE<<<"

    DEFAULT_COLUMN_MAPPING = {
        'date': 0,
        'description': 1,
        'amount': 2
    }

    def __init__(self, account_name, payee_accounts):
        self.account_name = account_name
        self.payee_accounts = payee_accounts

        self.column_mapping    = self.DEFAULT_COLUMN_MAPPING
        self.date_format       = self.DEFAULT_DATE_FORMAT
        self.currency_sym      = self.DEFAULT_CURRENCY_SYMBOL
        self.currency          = self.DEFAULT_CURRENCY_TEXT
        self.template_contents = self.__get_template_contents()

    def build(self, reader):
        result = []
        for row in reader:
            if (row[self.column_mapping['date']].lower() == 'date'):
                continue

            trans = self.__build_row_transaction(row)
            if trans:
                result.append(trans)

        result = self._process_transactions(result)
        return list(map(lambda t: self.__templated_transaction(t), result))

    def __templated_transaction(self, trans):
        template = Template(self.template_contents)
        return template.substitute(trans)

    def __build_row_transaction(self, row):
        row_date = row[self.column_mapping['date']]
        row_desc = self.__get_description(row)
        row_amount = row[self.column_mapping['amount']]

        date = datetime.datetime.strptime(row_date, self.date_format)
        payee_info = self.__payee_info(row_desc, row_amount)
        if (not payee_info): return None

        return self.__build_transaction(date, row_amount, row_desc, payee_info)

    def __build_transaction(self, date, amount, desc, payee_info):
        return {
            'primary_account': self.account_name,
            'amount': amount,
            'date': date.strftime(self.LEDGER_DATE_FORMAT),
            'status': self.DEFAULT_STATUS_SYMBOL,
            'payee': payee_info['name'],
            'secondary_account': payee_info['account'],
            'description': desc,
            'currency': self.currency,
            'currency_sym': self.currency_sym
        }

    def __payee_info(self, desc, amount):
        info = {}

        payee_key = self._get_payee_key(desc)
        payee_account = self.payee_accounts.get(payee_key)

        if (not payee_account):
            payee_account = self._payee_fallback_search(payee_key, amount)

        if (payee_account == 'skip'): return None

        if (payee_account):
            info['account'] = payee_account[0]
            info['name'] = payee_account[1]
        else:
            info['account'] = self.DEFAULT_ACCOUNT
            info['name'] = self.DEFAULT_PAYEE

        return info

    def __get_template_contents(self):
        template_abs_path = os.path.join(
            os.path.dirname(__file__),
            self.TEMPLATE_PATH
        )

        template_file = open(template_abs_path, 'rt')
        template_contents = template_file.read()
        template_file.close()

        return template_contents

    def __get_description(self, row):
        desc_position = self.column_mapping['description']

        if (isinstance(desc_position, list)):
            return " ".join(map(lambda i: row[i].strip(), desc_position))
        else:
            return row[desc_position]

    # overridables:

    def _get_payee_key(self, desc):
        return desc.strip()

    def _payee_fallback_search(self, payee_key, amount):
        return None

    def _process_transactions(self, transactions):
        return transactions
