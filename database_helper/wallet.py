from database_helper import sql_helper
from api_helper import crypto_api
import questionary
import re

class Wallet:
    options = ['Balance','Buy','Sell']
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
    def get_input_quantity(self):
        input_quantity = questionary.text('What is your input amount?').ask()
        return float(input_quantity)
    
    def parse_currency(self, s):
        m = re.search('\(([A-Z]{3,4})\)$', s)
        return m.group(1)

    def get_input_currency(self):
        question = [{
                'type': 'select',
                'name': 'input_currency',
                'message': 'What is your input currency?',
                'choices': self.currencies,
            }]
        return questionary.prompt(question)

        

    def __init__(self, user) :
        if user.is_authenticated:
            self.user_name = user.name
            self.wallets = sql_helper.get_wallets(self.user_name)

    def check_balance(self):
        print('-----------------------------------------------')
        print('Balance')
        print('-----------------------------------------------')
        for wallet in self.wallets:
            print(f'You have {wallet[3]} {wallet[2]}')
        print('')
        print('-----------------------------------------------')
        print('')
    
    def buy_crypto(self):
        '''Shows user the available currencies and their price. Buy a selected amount of the selected cryptocurrency'''
        print('Buying Crypto...')
        input_quantity = self.get_input_quantity()
        input_currency = self.parse_currency(self.get_input_currency()['input_currency'])
        unit_value = crypto_api.get_current_price(input_currency)
        price = input_quantity * unit_value
        print(f'{input_currency} price: ${unit_value}')

        question = [{
                'type': 'select',
                'name': 'will_buy',
                'message': f'Do you want to buy {input_quantity} {input_currency} for ${price}',
                'choices': ['Yes','No'],
            }]
        if questionary.prompt(question)['will_buy'] == 'Yes':
            success = sql_helper.update_wallet(input_currency, input_quantity, self.user_name)

    def actions(self, option):
        if option == 'Balance':
            self.check_balance()
        elif option == 'Buy':
            self.buy_crypto()

    