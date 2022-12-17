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
    playerId INTEGER,
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
    playId INTEGER,
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    playerId INTEGER PRIMARY KEY,
    FOREIGN KEY (combineId) REFERENCES combine(combineId)
    nameFirst TEXT,
    nameLast TEXT,
    position TEXT,
    college TEXT,
    heightInches REAL
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rusher (
    rushId INTEGER PRIMARY KEY,
    FOREIGN KEY (playId) REFERENCES play(playId)
    FOREIGN KEY (playerId) REFERENCES players(playerId)
    rushPosition TEXT,
    rushType TEXT,
    rushDirection TEXT,
    rushLandmark TEXT
    rushYards INTEGER
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

with open('players.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO combine (playerId, combineId, nameFirst, nameLast, position, college, heightInches) VALUES (?, ?, ?, ?, ?, ?, ?)", ( row['playerId'], row['combineId'], row['nameFirst'], row['nameLast'], row['position'], row['college'], row['heightInches']))
    print(row["playerId"])
conn.commit()

with open('rusher.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO combine (rushId, playId, playerId, rushPosition, rushType, rushDirection, rushLandmark, rushYards) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
    (row['rushId'], row['playId'], row['playerId'], row['rushPosition'], row['rushType'], row['rushDirection'], row['rushLandmark'], row['rushYards']))
    print(row["combineId"])
conn.commit()














# Save (commit) the changes
conn.commit()