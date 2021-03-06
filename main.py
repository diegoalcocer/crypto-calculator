#!/usr/bin/env python3

import re
import cmd
import bcrypt
import questionary
from utils import crypto_api, sql_helper
from utils.user_account import *
from utils.report import *

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
    """Crypto-Calculator"""

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

    # Parse a string for the currency ticker
    def parse_currency(self, s):
        m = re.search('\(([A-Z]{3,4})\)$', s)
        if m:
            return m.group(1)
        else:
            return s

    def do_exchange(self, line):
        """Calculate Current Exchange Rate"""
        input_quantity = self.get_input_quantity()
        input_currency = self.parse_currency(self.get_input_currency()['input_currency'])
        output_currency = self.parse_currency(self.get_output_currency()['output_currency'])
        output_quantity = self.transform_currency(input_quantity, input_currency, output_currency)
        print(f'{input_quantity} {input_currency} = {output_quantity:.8f} {output_currency}')

    # Perform the exchange rate between two currencies
    def transform_currency(self, input_quantity, input_currency, output_currency):
        return input_quantity * crypto_api.get_current_price(input_currency)/crypto_api.get_current_price(output_currency)

    # Create a new user and store it to the database
    def do_create_new_user(self, line):
        """Create A New User"""
        if len(line.split()) >= 3:
            print('Unable to create user')
            return
        elif len(line.split()) == 2:
            username = line.split()[0]
            password = line.split()[1]
        elif len(line.split()) == 1:
            username = line.split()[0]
            password = bcrypt.hashpw(
                questionary.password('Password:').ask().encode('utf-8'),
                bcrypt.gensalt(10)).decode('utf-8')
        elif len(line.split()) == 0:
            username = questionary.text('Username:').ask()
            password = bcrypt.hashpw(
                questionary.password('Password:').ask().encode('utf-8'),
                bcrypt.gensalt(10)).decode('utf-8')

        created = sql_helper.create_user(username, password)
        if created:
            print('Successfully created user')
        else:
            print('Unable to create user')

    def do_login(self, line):
        """Login To Your User Account"""
        if len(line.split()) >= 3:
            print('Unable to Authenticate')
        elif len(line.split()) == 2:
            username = line.split()[0]
            password = line.split()[1]
        elif len(line.split()) == 1:
            username = line.split()[0]
            password = questionary.password('Password:').ask().encode('utf-8')
        elif len(line.split()) == 0:
            username = questionary.text('Username:').ask()
            password = questionary.password('Password:').ask().encode('utf-8')

        # Drop to UserAccount shell if the login is successful, else return invalid
        if self.authenticate_user(username, password):
            user_acct = UserAccount()
            user_acct.cmdloop(f'Welcome To Your Account {username}')
        else:
            print('Invalid Credentials')

    # Validate the user's credentials
    def authenticate_user(self, username, password):
        authenticated = sql_helper.auth(username, password)
        if authenticated:
            return True
        else:
            return False

    def do_cumulative(self,line):
        """Create a Report on the daily Cumulative Returns"""
        report = Report()
        report.generate_cumsum()

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
