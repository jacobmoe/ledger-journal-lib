#!/usr/bin/env python

import fileinput, csv, re
from gringotts_payees import payee_accounts
from lib.command      import Command
from lib.builder      import Builder

class GringottsChecking(Command, Builder):
    def __init__(self):
        Command.__init__(self, 'name')
        Builder.__init__(self, 'Assets:Bank:Checking:Gringotts', payee_accounts)

    def run(self):
        reader = csv.reader(fileinput.input(self.file_names))
        self.output(self.build(reader))

    # in addition to keeping the payee_accounts list, you might
    # want some special rules for identifying a payee
    def _payee_fallback_search(self, desc, amount):
        rent_amount = '-1234.56'
        rent_check_reg = 'CHECK # [1-9]{0,3}'
        rent_payee_info = ['Expenses:Home:Rent', 'He who must not be named']

        if (re.search(rent_check_reg, desc)) and (amount == rent_amount):
            return rent_payee_info

GringottsChecking().run()
