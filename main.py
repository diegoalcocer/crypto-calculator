#!/usr/bin/env python3

import re
import cmd
import bcrypt
import questionary
from api_helper import crypto_api
from database_helper import sql_helper
from database_helper import user_auth
from database_helper import wallet

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
    user = user_auth.User('_guest_',False)

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
        output_quantity = self.transform_currency(input_quantity, input_currency, output_currency)
        print(f'{input_quantity} {input_currency} = {output_quantity:.8f} {output_currency}')

    def transform_currency(self, input_quantity, input_currency, output_currency):
        return input_quantity * crypto_api.get_current_price(input_currency)/crypto_api.get_current_price(output_currency)

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

    def do_wallet(self, line):
        if  not self.user.is_authenticated:            
            username = questionary.text('Username:').ask()
            password = questionary.password('Password:').ask().encode('utf-8')
            self.authenticate_user(username, password)

        if self.user.is_authenticated:            
            user_wallet = wallet.Wallet(self.user)
            if len(user_wallet.wallets)<1:
                print("You Don't have a wallet yet. You can buy Bitcoin, Ethereum, and more with trust")
                question = [{'type': 'select','name': 'create_wallet','message': 'Would you like to purchase Crypto?','choices': ['Yes','No']}]
                create_wallet = questionary.prompt(question)['create_wallet']
                if create_wallet == 'Yes':
                    wallet_option = 'Buy'
                    print(f"You picked: {wallet_option}")
            else:
                wallet_option = self.wallet_options(user_wallet.options)['wallet_option']
                print(f"You picked: {wallet_option}")
            user_wallet.actions(wallet_option)            

    def wallet_options(self, options):
        question = [{
                'type': 'select',
                'name': 'wallet_option',
                'message': 'Please select one of these options',
                'choices': options,
            }]
        result = questionary.prompt(question)
        
        return result
        
    def do_login(self, line):
        """Login To Your Wallet"""
        if len(line.split()) >= 3:
            print('Please try again')
            return
        elif len(line.split()) == 2:
            username = line.split()[0]
            password = line.split()[1]
        elif len(line.split()) == 1:
            username = line.split()[0]
            password = questionary.password('Password:').ask().encode('utf-8')
        elif len(line.split()) == 0:
            username = questionary.text('Username:').ask()
            password = questionary.password('Password:').ask().encode('utf-8')
        self.authenticate_user(username, password)

    def authenticate_user(self, username, password):
        authenticated = sql_helper.auth(username, password)
        if authenticated:
            self.user.name = username
            self.user.is_authenticated = True
            print(f'Welcome {self.user.name}')
            return True
        else:
            print('Invalid credentials')
            return False
    
    def do_cumulative(self,line):
        report = wallet.Report()
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
