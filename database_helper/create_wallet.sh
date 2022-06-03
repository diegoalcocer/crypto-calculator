#!/bin/bash

if [[ -z $1 ]]; then
  echo "MUST PROVIDE A FILENAME!"
  echo "EX: $0 <FILENAME>"
  exit
else
  DB=$1
fi

sqlite3 ${DB} "CREATE TABLE wallet (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER NOT NULL,
  currency VARCHAR(64) NOT NULL,
  balance REAL NOT NULL,
  created DATETIME
);

"
