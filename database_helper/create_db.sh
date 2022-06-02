#!/bin/bash

if [[ -z $1 ]]; then
  echo "MUST PROVIDE A FILENAME!"
  echo "EX: $0 <FILENAME>"
  exit
else
  DB=$1
fi

sqlite3 ${DB} "CREATE TABLE users (
  uid INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(64) NOT NULL UNIQUE,
  password VARCHAR(64) NOT NULL,
  wallet VARCHAR(64),
  created DATETIME,
  last_login DATETIME
);

INSERT INTO users (
  username,
  password,
  created
) VALUES (
  'root',
  '\$2b\$10\$14K5uaRoGfv3rD9jI09cu.HWMjn6G3NoOhn5ZYEAsbzxQUIIBtV1O',
  DATETIME('now')
);
"

