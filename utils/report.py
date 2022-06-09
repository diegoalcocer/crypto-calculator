import questionary
import pandas as pd
from datetime import datetime
from pathlib import Path

class Report:
    def __init__(self) -> None:
        pass

    # Obtains the currency from the user and returns it    
    def get_input_currency(self):
            question = [{
                    'type': 'select',
                    'name': 'input_currency',
                    'message': 'Please select the currency to analyze',
                    'choices': ['BTC','ETH'],
                }]
            return questionary.prompt(question)['input_currency']
    
    # Obtains the start and end date from the user and returns a tuple with these dates
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

    # Given a period of time (start date - end date) and a currency, generates the daily percentage change and calculates the cumulative sum for the given currency
    def cumulative_sum(self, start_date, end_date, currency):
        '''Given a period of time (start date - end date) and a currency, generates the daily percentage change and calculates the cumulative sum for the given currency'''
        # Read the csv file with historical data, setting the date column as index
        currency_df = pd.read_csv(Path(f'resources/{currency}.csv'), index_col='Date', parse_dates=True, infer_datetime_format=True)
        # clean up data - drop nulls
        # currency_df.head()
        currency_df.dropna(axis=1)
        # currency_df['Close'].describe()
        
        # Obtain the data for column Close for the specified period of time
        subset = currency_df['Close'].loc[start_date:end_date]
        print(f'Cumulative Daily Sum Report')
        # Calculate and print the 5 last records of the cum sum
        print(subset.pct_change().cumsum().tail(5))

    def generate_cumsum(self):
        '''Generate the Daily Cumulative Sum Report for a given period of time and currency'''
        range = self.get_date_range()

        # Verify that the user input (dates) was correct. If incorrect, range = (0,0)
        if range[0] == 0 and range[1] == 0:
            return False
        self.cumulative_sum(range[0], range[1], self.get_input_currency())
