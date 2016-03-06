import datetime
from transaction import Transaction

class Builder(Transaction):

    DEFAULT_CURRENCY_SYMBOL = '$'
    DEFAULT_CURRENCY_TEXT   = ''
    DEFAULT_STATUS_SYMBOL   = '*'
    DEFAULT_ACCOUNT         = ">>>UNKNOWN ACCOUNT<<<"
    DEFAULT_PAYEE           = ">>>UNKNOWN PAYEE<<<"
    DEFAULT_DATE_FORMAT     = '%m/%d/%y'
    DEFAULT_COLUMN_MAPPING  = {
        'date': 0,
        'description': 1,
        'amount': 2
    }

    def __init__(self, account_name, payee_accounts, opts={}):
        self.account_name   = account_name
        self.payee_accounts = payee_accounts

        self.column_mapping  = self.DEFAULT_COLUMN_MAPPING
        self.date_format     = self.DEFAULT_DATE_FORMAT
        self.currency_symbol = self.DEFAULT_CURRENCY_SYMBOL
        self.status_symbol   = self.DEFAULT_STATUS_SYMBOL
        self.currency        = self.DEFAULT_CURRENCY_TEXT

    def build(self, reader):
        result = []
        for row in reader:
            if (row[self.column_mapping['date']].lower() == 'date'):
                continue

            trans = self.__build_transaction(row)
            if trans:
                result.append(trans)

        return result

    def __build_transaction(self, row):
        row_date = row[self.column_mapping['date']]
        row_desc = self.__get_description(row)
        row_amount = row[self.column_mapping['amount']]

        date = datetime.datetime.strptime(row_date, self.date_format)
        payee_info = self.__payee_info(row_desc, row_amount)
        if (not payee_info): return None

        return Transaction({
            'primary_account': self.account_name,
            'amount': row_amount,
            'date': date,
            'status': self.DEFAULT_STATUS_SYMBOL,
            'payee_name': payee_info['name'],
            'payee_account': payee_info['account'],
            'description': row_desc,
            'currency': self.currency,
            'currency_symbol': self.currency_symbol
        })

    def __payee_info(self, desc, amount):
        info = {}

        payee_key = self._get_payee_key(desc)
        payee_account = self.payee_accounts.get(payee_key)

        if (not payee_account):
            payee_account = self._payee_fallback_search(payee_key, amount)

        if (payee_account == 'skip'): return None

        if (payee_account):
            info['account'] = payee_account[0]
            info['name']    = payee_account[1]
        else:
            info['account'] = self.DEFAULT_ACCOUNT
            info['name']    = self.DEFAULT_PAYEE

        return info

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
