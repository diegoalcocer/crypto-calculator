import re
import cmd
import questionary
import pandas as pd
from pathlib import Path
from datetime import datetime
from utils import sql_helper
from utils import crypto_api

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

class UserAccount(cmd.Cmd):

    use_rawinput = True
    prompt = 'User Account > '
    options = ['Balance','Buy','Sell']

    def username(self):
        return(self.intro.split()[-1])

    def get_input_quantity(self):
        input_quantity = questionary.text('How much?').ask()
        return float(input_quantity)

    def parse_currency(self, s):
        m = re.search('\(([A-Z]{3,4})\)$', s)
        return m.group(1)

    def get_input_currency(self, question):
        question = [{
                'type': 'select',
                'name': 'input_currency',
                'message': question,
                'choices': currencies,
            }]
        return questionary.prompt(question)

    def do_exit(self, line):
        """Exits the User's Wallet and Returns to Main Crypto-Calculator"""
        return True

    def do_quit(self, line):
        """Exits the User's Wallet and Returns to Main Crypto-Calculator"""
        return True

    def do_EOF(self, line):
        """Exits the User's Wallet and Returns to Main Crypto-Calculator"""
        return True

    def do_add_funds(self, line):
        """Add USD to the User's Wallet"""
        print('Adding USD to your account')
        input_quantity = self.get_input_quantity()
        success = sql_helper.update_wallet(self.username(), input_quantity, 'USD')

    def do_buy(self, line):
        """Shows User The Available Currencies and Their Price. Buy the Selected Crypto."""
        input_currency = self.parse_currency(self.get_input_currency('What Crypto do you want to buy?')['input_currency'])
        input_quantity = self.get_input_quantity()
        unit_value = crypto_api.get_current_price(input_currency)
        price = input_quantity * unit_value
        print(f'{input_currency} price: ${unit_value} USD')

        user_usd_wallet = sql_helper.get_wallet_by_currency(self.username(), 'USD')
        if len(user_usd_wallet) <= 0:
            print('No USD Wallet! Must Add Funds First!')
            return
        elif price > user_usd_wallet[0][3]:
            print('Insufficient funds!')
            return
        else:
            question = [{
                    'type': 'select',
                    'name': 'will_buy',
                    'message': f'Do you want to buy {input_quantity} {input_currency} for ${price} USD?',
                    'choices': ['Yes','No'],
                }]
            if questionary.prompt(question)['will_buy'].lower().startswith('y'):
                sql_helper.update_wallet(self.username(), input_quantity, input_currency)
                sql_helper.subtract_wallet(self.username(), price, 'USD')

    def do_sell(self, line):
        """Shows User The Available Currencies and Their Price. Sell the Selected Crypto."""
        input_currency = self.parse_currency(self.get_input_currency('What Crypto do you want to sell?')['input_currency'])
        input_quantity = self.get_input_quantity()
        unit_value = crypto_api.get_current_price(input_currency)
        price = input_quantity * unit_value
        print(f'{input_currency} price: ${unit_value} USD')

        user_wallet = sql_helper.get_wallet_by_currency(self.username(), input_currency)
        if len(user_wallet) <= 0:
            print(f'No {input_currency} Wallet! Must Add Funds First!')
            return
        elif input_quantity > user_wallet[0][3]:
            print('Insufficient funds!')
            return
        else:
            question = [{
                    'type': 'select',
                    'name': 'will_buy',
                    'message': f'Do you want to sell {input_quantity} {input_currency} for ${price} USD?',
                    'choices': ['Yes','No'],
                }]
            if questionary.prompt(question)['will_buy'].lower().startswith('y'):
                sql_helper.subtract_wallet(self.username(), input_quantity, input_currency)
                sql_helper.update_wallet(self.username(), price, 'USD')

    def do_balance(self, line):
        """Get Your Current Wallet Holdings"""
        wallets = sql_helper.get_wallets(self.username())
        if len(wallets) <= 0:
            print('No Wallets!')
        else:
            print('-----------------------------------------------')
            print('Wallet Balances')
            print('-----------------------------------------------')
            for wallet in wallets:
                print(f' * {wallet[3]} {wallet[2]}')
            print('\n-----------------------------------------------\n')