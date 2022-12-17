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
CREATE TABLE IF NOT EXISTS combine (
    combineId INTEGER PRIMARY KEY,
    FOREIGN KEY(playerId) REFERENCES players(playerId),
    combineYear INTEGER,
    combinePosition TEXT,
    combineHeight REAL,
    combineWeight REAL,
    combineHand REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS fumbles (
    fumId INTEGER PRIMARY KEY,
    FOREIGN KEY(playId) REFERENCES plays(playId),
    FOREIGN KEY(playerId) REFERENCES players(playerId),
    playerId INTEGER,
    fumPosition TEXT,
    fumType TEXT,
    fumOOB INTEGER,
    fumTurnover REAL,
    fumNull INTEGER
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS games (
    gameId INTEGER PRIMARY KEY,
    season INTEGER,
    week INTEGER,
    gameDate TEXT,
    gameTimeEastern TEXT,
    gameTimeLocal TEXT,
    seasonType REAL
)
""")
conn.commit()
# Read data from CSV file and write it to the database
with open('combine.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO combine (combineId, playerId, combineYear, combinePosition, combineHeight, combineWeight, combineHand) VALUES (?, ?, ?, ?, ?, ?, ?)", (row['combineId'], row['playerId'], row['combineYear'], row['combinePosition'], row['combineHeight'], row['combineWeight'], row['combineHand']))
    print(row["combineId"])
conn.commit()


with open('fumbles.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute("""
      INSERT INTO fumbles (fumId, playId, playerId, fumPosition, fumType, fumOOB, fumTurnover, fumNull)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (row['fumId'], row['playId'], row['playerId'], row['fumPosition'], row['fumType'], row['fumOOB'], row['fumTurnover'], row['fumNull']))

conn.commit()
with open('games.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute("""
      INSERT INTO games (gameId, season, week, gameDate, gameTimeEastern, gameTimeLocal, seasonType)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (row['gameId'], row['season'], row['week'], row['gameDate'], row['gameTimeEastern'],
          row['gameTimeLocal'], row['seasonType']))


# Save (commit) the changes
conn.commit()