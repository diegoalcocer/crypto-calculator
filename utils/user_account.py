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

    # Retrieve the user's username
    def username(self):
        return(self.intro.split()[-1])

    # Ask the user for quantity of a currency
    def get_input_quantity(self):
        input_quantity = questionary.text('How much?').ask()
        return float(input_quantity)

    # Parse a string for the currency ticker
    def parse_currency(self, s):
        m = re.search('\(([A-Z]{3,4})\)$', s)
        return m.group(1)

    # Ask the user for a type of currency
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

    # Add funds to the USD wallet
    def do_add_funds(self, line):
        """Add USD to the User's Wallet"""
        print('Adding USD to your account')
        input_quantity = self.get_input_quantity()
        success = sql_helper.update_wallet(self.username(), input_quantity, 'USD')

    # Perform a buy of a currency.  Uses USD funds from USD wallet.
    def do_buy(self, line):
        """Shows User The Available Currencies and Their Price. Buy the Selected Crypto."""
        input_currency = self.parse_currency(self.get_input_currency('What Crypto do you want to buy?')['input_currency'])
        input_quantity = self.get_input_quantity()
        unit_value = crypto_api.get_current_price(input_currency)
        price = input_quantity * unit_value
        print(f'{input_currency} price: ${unit_value} USD')

        user_usd_wallet = sql_helper.get_wallet_by_currency(self.username(), 'USD')

        # If user has no USD wallet, then make them fund it first
        if len(user_usd_wallet) <= 0:
            print('No USD Wallet! Must Add Funds First!')
            return
        # Else if USD wallet doesn't contain enough funds
        elif price > user_usd_wallet[0][3]:
            print('Insufficient funds!')
            return
        # USD wallet contains enough funds to make purchase
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

    # Perform a sell of a currency. Funds earned from sale are added to USD wallet.
    def do_sell(self, line):
        """Shows User The Available Currencies and Their Price. Sell the Selected Crypto."""
        input_currency = self.parse_currency(self.get_input_currency('What Crypto do you want to sell?')['input_currency'])
        input_quantity = self.get_input_quantity()
        unit_value = crypto_api.get_current_price(input_currency)
        price = input_quantity * unit_value
        print(f'{input_currency} price: ${unit_value} USD')

        user_wallet = sql_helper.get_wallet_by_currency(self.username(), input_currency)
        # If user has no wallet in that currency, then they have no currency to sell
        if len(user_wallet) <= 0:
            print(f'No {input_currency} Wallet! Must Add Funds First!')
            return
        # Else if currency wallet doesn't contain enough funds to make sale
        elif input_quantity > user_wallet[0][3]:
            print('Insufficient funds!')
            return
        # Wallet contains enough funds to make sale
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
