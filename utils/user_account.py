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

    def do_buy(self, line):
        """Shows User The Available Currencies and Their Price. Buy the Selected Crypto."""
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
        if questionary.prompt(question)['will_buy'].lower().startswith('y'):
            success = sql_helper.update_wallet(input_currency, input_quantity, self.username())

    def do_sell(self, line):
        """Sell Crypto"""

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

class Report:
    def __init__(self) -> None:
        pass

    def get_input_currency(self):
            question = [{
                    'type': 'select',
                    'name': 'input_currency',
                    'message': 'Please select the currency to analyze',
                    'choices': ['BTC','ETH'],
                }]
            return questionary.prompt(question)['input_currency']

    def get_date_range(self):

        start = questionary.text("What's the start date (YYYY-MM-dd)").ask()
        try:
            datetime.strptime(start,"%Y-%m-%d")
        except Exception as e:
            print('Error. Please input the date in the correct format')
            return (0,0)

        end = questionary.text("What's the end date (YYYY-MM-dd)").ask()
        try:
            datetime.strptime(end,"%Y-%m-%d")
        except:
            print('Error. Please input the date in the correct format')
            return (0,0)

        return (start, end)


    def cumulative_sum(self, start_date, end_date, currency):
        currency_df = pd.read_csv(Path(f'resources/{currency}.csv'), index_col='Date', parse_dates=True,infer_datetime_format=True)
        currency_df.head()
        currency_df.dropna(axis=1)
        currency_df['Close'].describe()
        subset = currency_df['Close'].loc[start_date:end_date]
        print(f'Cumulative Sum')
        print(subset.pct_change().cumsum().tail(5))

    def generate_cumsum(self):
        range = self.get_date_range()
        if range[0]==0 and range[1]==0:
            return False
        self.cumulative_sum(range[0],range[1],self.get_input_currency())
