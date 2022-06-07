import questionary
import pandas as pd
from datetime import datetime
from pathlib import Path

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
        currency_df = pd.read_csv(Path(f'resources/{currency}.csv'), index_col='Date', parse_dates=True, infer_datetime_format=True)
        currency_df.head()
        currency_df.dropna(axis=1)
        currency_df['Close'].describe()
        subset = currency_df['Close'].loc[start_date:end_date]
        print(f'Cumulative Daily Sum Report')
        print(subset.pct_change().cumsum().tail(5))

    def generate_cumsum(self):
        range = self.get_date_range()
        if range[0]==0 and range[1] == 0:
            return False
        self.cumulative_sum(range[0], range[1], self.get_input_currency())
