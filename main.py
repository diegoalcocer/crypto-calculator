#!/usr/bin/env python3

import cmd
import questionary
from api_helper import crypto_api
from database_helper import sql_helper

class CryptoCalculator(cmd.Cmd):
    """Crypto Calculator"""

    intro = "Group 3's CryptoCalculator App"
    use_rawinput = True
    prompt = 'CryptoCalculator > '

    def get_input_quantity(self):
        amount = questionary.text('What is your input amount?').ask()
        return float(amount)

    def get_input_currency(self):
        questions = [
            {
                'type': 'select',
                'name': 'input_currency',
                'message': 'What is your input currency?',
                'choices': ['USD', 'BTC', 'ETC'],
            },
        ]
        return questionary.prompt(questions)


    def do_exchange(self, line):
        """Calculate Current Exchange Rate"""
        input_quantity = self.get_input_quantity()
        input_currency = self.get_input_currency()
        #output_currency = self.get_output_currency()
        print(f'{input_quantity} {input_currency["input_currency"]}')

    def do_exit(self, line):
        """Exits the CryptoCalculator"""
        return True

    def do_quit(self, line):
        """Quits the CryptoCalculator"""
        return True

    def do_EOF(self, line):
        """Ends the CryptoCalculator"""
        return True

if __name__ == '__main__':
    try:
        CryptoCalculator().cmdloop()
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        print('Closing CryptoCalculator')
