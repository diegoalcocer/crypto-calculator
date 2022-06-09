# Crypto Calculator

---

## Summary

The Crypto-Calculator is a command-line interface (CLI) utility which allows you to perform the following functions:

1. Retrieve Current Crypto Exchange Rates
2. Create Crypto Cumulative Daily Return Reports 
3. Control User Crypto Accounts and Wallets
   - Create New User Accounts
   - Add Funds to USD Wallet
   - Buy and Sell Cryptocurrencies
   - Retrieve User Wallet Balances

Additionally, there is a supplemental Jupyter Notebook which visually demonstrates historical changes in Bitcoin (BTC), Ethereum (ETH), and Ripple (XRP).  Historical data is collected from [Bitstamp](https://www.bitstamp.net) and analyzed within Pandas DataFrames.

User and Wallet data is stored locally within an SQLite3 database.  User passwords are bcrypt salted and hashed.

Cryptocurrency exchange rates are performed in real-time via [Alternative.me's Crypto API](https://alternative.me/crypto/api/)

---
## Installation and Usage

```sh
git clone git@github.com:diegoalcocer/crypto-calculator.git
cd crypto-calculator/
pip install -r requirements.txt
```
To start the application:

```sh
python3 main.py
```
Type *help* to get a list of possible actions

```sh
CryptoCalculator > help
Documented commands (type help <topic>):
========================================
EOF  create_new_user  cumulative  exchange  exit  help  login  quit
```
* **create_new_user:** Allows you to create a new user in order to create a wallet, buy and sell crypto
* **exchange:** Access the crypto-calculator that allows you to transform from one currency to another
* **cumulative:** Generates a report of daily cumulative sum for a given period of time and currency

Once you **login** with your user credentials, you can access your *wallet*. Type help to get a list of possible actions

```sh
User Account > help
Documented commands (type help <topic>):
========================================
EOF  add_funds  balance  buy  exit  help  quit  sell
```

* **add_funds:** To be able to buy crypto, you need to have funds in your account. Use this command to add funds to your account
* **balance:** Displays the balance of all your assets (funds and crypto)
* **buy:** Allows you to buy crypto
* **sell:** Allows you to sell crypto

### 📚 resources/

This project uses the following resources required for analysis 

* CSVs required for utils/report.py
   * BTC.csv
   * ETH.csv
* CSVs required for crypto_price_charts.ipynb 
   * Data collected from Bitstamp.net
* Script **create_db.sh** which creates a fresh SQLite3 database
   * Default credentials of **root**: root

---

## Jupyter Notebook Usage

```sh
jupyter lab
Open Browser > http://localhost:8888/lab/tree/crypto_price_charts.ipynb
 - or -
voila crypto_price_charts.ipynb
Open Browser > http://localhost:8866/
```

---
## Contributors

1. [Antiwan](https://github.com/admaxwell)
2. [Diego](https://github.com/diegoalcocer)
3. [Travis](https://github.com/travispeska)

---
## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
