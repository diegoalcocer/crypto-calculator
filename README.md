# Crypto Calculator

---

## Summary

The Crypto-Calculator is a command-line interface (CLI) utility which allows you to perform the following functions:

1. Retrieve Current Crypto Exchange Rates
2. Create Crypto Cumulative Daily Return Reports 
3. Control User Crypto Accounts and Wallets
   - Create New User Accounts
   - Add Funs to USD Wallet
   - Buy and Sell Cryptocurrencies
   - Retrieve User Wallet Balances

Additionally, there is a supplemental Jupyter Notebook which visually demonstrates historical changes in Bitcoin (BTC), Ethereum (ETH), and Ripple (XRP).  Historical data is collected from [Bitstamp](https://www.bitstamp.net) and analyzed within Pandas DataFrames.

---

## Installation and Usage

```sh
git clone git@github.com:diegoalcocer/crypto-calculator.git
cd crypto-calculator/
pip install -r requirements.txt
```

```sh
python3 main.py

CryptoCalculator > help
Documented commands (type help <topic>):
========================================
EOF  create_new_user  cumulative  exchange  exit  help  login  quit

User Account > help
Documented commands (type help <topic>):
========================================
EOF  add_funds  balance  buy  exit  help  quit  sell
```

---

## Jupyter Notebook Usage

```sh
jupyter lab
Open Browser > http://localhost:8888/lab/tree/crypto_price_charts.ipynb
```

---

## Contributors

1. [Antiwan](https://github.com/admaxwell)
2. [Diego](https://github.com/diegoalcocer)
3. [Travis](https://github.com/travispeska)

## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
