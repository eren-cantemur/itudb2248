import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Create a table
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
CREATE TABLE IF NOT EXIST plays (
  playId INTEGER PRIMARY KEY,
  FOREIGN KEY(gameId) REFERENCES games(gameId),
  playSequence INTEGER,
  quarter INTEGER,
  playType TEXT,
  playType2 TEXT,
  playNumberByTeam INTEGER
""")
conn.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS combine (
    combineId INTEGER PRIMARY KEY,
    playerId INTEGER,
    combineYear INTEGER,
    combinePosition TEXT,
    combineHeight REAL,
    combineWeight REAL,
    combineHand REAL
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
conn.commit()

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
with open('games.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute("""
      INSERT INTO games (gameId, season, week, gameDate, gameTimeEastern, gameTimeLocal, seasonType)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (row['gameId'], row['season'], row['week'], row['gameDate'], row['gameTimeEastern'],
          row['gameTimeLocal'], row['seasonType']))
conn.commit()

with open('plays.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO plays (playId, gameID, playSequence, quarter, playType, playType2, playNumberByTeam) VALUES (?, ?, ?, ?, ?, ?, ?)", (row['playId'], row['gameId'], row['playSequence'], row['quarter'], row['playType'], row['playType2'], row['playNumberByTeam']))
    print(row["playId"])
conn.commit()

with open('combine.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO combine (combineId, playerId, combineYear, combinePosition, combineHeight, combineWeight, combineHand) VALUES (?, ?, ?, ?, ?, ?, ?)", (row['combineId'], row['playerId'], row['combineYear'], row['combinePosition'], row['combineHeight'], row['combineWeight'], row['combineHand']))
    print(row["combineId"])
conn.commit()

with open('players.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO combine (playerId, combineId, nameFirst, nameLast, position, college, heightInches) VALUES (?, ?, ?, ?, ?, ?, ?)", ( row['playerId'], row['combineId'], row['nameFirst'], row['nameLast'], row['position'], row['college'], row['heightInches']))
    print(row["playerId"])
conn.commit()

with open('fumbles.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute("""
      INSERT INTO fumbles (fumId, playId, playerId, fumPosition, fumType, fumOOB, fumTurnover, fumNull)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (row['fumId'], row['playId'], row['playerId'], row['fumPosition'], row['fumType'], row['fumOOB'], row['fumTurnover'], row['fumNull']))
conn.commit()


with open('gameParticipation.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO gamePaticipation (gamePartId, gameId, playerId, gamePartUnit, gamePartSnapCount, playerProfileUri) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (row['gamePartId'], row['gameId'], row['playerId'], row['gamePartUnit'], row['gamePartSnapCount'], row['playerProfileUri'], row['homeCity'], row['homeState']))
    print(row["gamePartId"])
conn.commit()

with open('rusher.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute(" INSERT INTO combine (rushId, playId, playerId, rushPosition, rushType, rushDirection, rushLandmark, rushYards) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
    (row['rushId'], row['playId'], row['playerId'], row['rushPosition'], row['rushType'], row['rushDirection'], row['rushLandmark'], row['rushYards']))
    print(row["combineId"])
conn.commit()