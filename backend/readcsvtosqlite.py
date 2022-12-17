#read combines.csv fumbles.csv games.csv
from flask import Flask, request
import sqlite3
import csv

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS gameParticipation (
  gamePartId INTEGER PRIMARY KEY,
  FOREIGN KEY(gameId) REFERENCES games(gameId),
  FOREIGN KEY(playerId) REFERENCES players(playerId),
  gamePartUnit TEXT,
  gamePartSnapCount INTEGER,
  playerProfileUri TEXT,
  homeCity TEXT,
  homeState TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXIST plays (
  playId INTEGER PRIMARY KEY,
  FOREIGN KEY(gameId) REFERENCES games(gameId),
  playSequence INTEGER,
  quarter INTEGER,
  playType TEXT,
  playType2 TEXT,
  playNumberByTeam INTEGER
)
""")

# Read data from CSV file and write it to the database
with open('gameParticipation.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO gamePaticipation (gamePartId, gameId, playerId, gamePartUnit, gamePartSnapCount, playerProfileUri) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (row['gamePartId'], row['gameId'], row['playerId'], row['gamePartUnit'], row['gamePartSnapCount'], row['playerProfileUri'], row['homeCity'], row['homeState']))
    print(row["gamePartId"])
conn.commit()

with open('plays.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO plays (playId, gameID, playSequence, quarter, playType, playType2, playNumberByTeam) VALUES (?, ?, ?, ?, ?, ?, ?)", (row['playId'], row['gameId'], row['playSequence'], row['quarter'], row['playType'], row['playType2'], row['playNumberByTeam']))
    print(row["playId"])
conn.commit()
