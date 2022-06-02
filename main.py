#!/usr/bin/env python3

import re
import cmd
import questionary
from api_helper import crypto_api
from database_helper import sql_helper

currencies = [
        'US Dollar (USD)',
        'Bitcoin (BTC)',
        'Ethereum (ETH)',
        'Tether (USDT)',
        'Binance Coin (BNB)',
        'Ripple (XRP)',
        'Cardano (ADA)',
        'Solana (SOL)',
        'Dogecoine (DOGE)',
        'Polkadot (DOT)'
        ]

class CryptoCalculator(cmd.Cmd):
    """Crypto Calculator"""

    intro = "Crypto-Calculator App"
    use_rawinput = True
    prompt = 'CryptoCalculator > '

    def get_input_quantity(self):
        input_quantity = questionary.text('What is your input amount?').ask()
        return float(input_quantity)

    def get_input_currency(self):
        question = [{
                'type': 'select',
                'name': 'input_currency',
                'message': 'What is your input currency?',
                'choices': currencies,
            }]
        return questionary.prompt(question)

    def get_output_currency(self):
        question = [{
                'type': 'select',
                'name': 'output_currency',
                'message': 'What is your output currency?',
                'choices': currencies,
            }]
        return questionary.prompt(question)

    def parse_currency(self, s):
        m = re.search('\(([A-Z]{3,4})\)$', s)
        return m.group(1)

    def do_exchange(self, line):
        """Calculate Current Exchange Rate"""
        input_quantity = self.get_input_quantity()
        input_currency = self.parse_currency(self.get_input_currency()['input_currency'])
        output_currency = self.parse_currency(self.get_output_currency()['output_currency'])
        output_quantity = input_quantity * crypto_api.get_current_price(input_currency)/crypto_api.get_current_price(output_currency)
        print(f'{input_quantity} {input_currency} = {output_quantity:.8f} {output_currency}')

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
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print(f'Exception: {e}')
    finally:
        print('Closing CryptoCalculator')
