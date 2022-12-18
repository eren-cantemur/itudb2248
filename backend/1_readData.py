import sqlite3
import csv


def change_empty_values(dictionary):
    # Iterate over the keys and values in the dictionary
    for key, value in dictionary.items():
        # If the value is an empty string, set it to "NULL"
        if value == "":
            dictionary[key] = None
    return dictionary


# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute("""
PRAGMA foreign_keys = ON;
""")
conn.commit()

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
    );
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS plays (
  playId INTEGER PRIMARY KEY,
  gameId INTEGER,
  playSequence INTEGER,
  quarter INTEGER,
  playType TEXT,
  playType2 TEXT,
  playNumberByTeam INTEGER,
  FOREIGN KEY (gameId) REFERENCES games(gameId)
  );
""")
conn.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS combine (
  combineId INTEGER PRIMARY KEY,
  combineYear INTEGER,
  combinePosition TEXT,
  combineHeight REAL,
  combineWeight REAL,
  combineHand REAL
  );
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
  playerId INTEGER PRIMARY KEY,
  combineId INTEGER,
  nameFirst TEXT,
  nameLast TEXT,
  position TEXT,
  college TEXT,
  heightInches REAL,
  FOREIGN KEY(combineId) REFERENCES combine(combineId)
  );
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
  fumNull INTEGER,
  FOREIGN KEY(playId) REFERENCES plays(playId),
  FOREIGN KEY(playerId) REFERENCES players(playerId)
  );
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS gameParticipation (
  gamePartId INTEGER PRIMARY KEY,
  gameId INTEGER,
  playerId INTEGER,
  gamePartUnit TEXT,
  gamePartSnapCount INTEGER,
  playerProfileUrl TEXT,
  homeCity TEXT,
  homeState TEXT,
  FOREIGN KEY(gameId) REFERENCES games(gameId),
  FOREIGN KEY(playerId) REFERENCES players(playerId)
  );
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rusher (
  rushId INTEGER PRIMARY KEY,
  playId INTEGER,
  playerId INTEGER,
  rushPosition TEXT,
  rushType TEXT,
  rushDirection TEXT,
  rushLandmark TEXT,
  rushYards INTEGER,
  FOREIGN KEY (playId) REFERENCES plays(playId),
  FOREIGN KEY (playerId) REFERENCES players(playerId)
  );
""")
conn.commit()


# Read data from CSV file and write it to the database
# with open('games.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         try:
#             cursor.execute("""
#       INSERT INTO games (gameId, season, week, gameDate, gameTimeEastern, gameTimeLocal, seasonType)
#       VALUES (?, ?, ?, ?, ?, ?, ?)
#     """, (row['gameId'], row['season'], row['week'], row['gameDate'], row['gameTimeEastern'],
#                 row['gameTimeLocal'], row['seasonType']))
#             print("Game: " + row["gameId"])
#         except:
#           pass

# conn.commit()

# with open('plays.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#       try:
#         cursor.execute(" INSERT INTO plays (playId, gameID, playSequence, quarter, playType, playType2, playNumberByTeam) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                        (row['playId'], row['gameId'], row['playSequence'], row['quarter'], row['playType'], row['playType2'], row['playNumberByTeam']))
#         print("Play: " + row["playId"])
#       except:
#         pass
# conn.commit()

# with open('combine.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         row = change_empty_values(row)
#         try:  
#           cursor.execute(" INSERT INTO combine (combineId, combineYear, combinePosition, combineHeight, combineWeight, combineHand) VALUES (?, ?, ?, ?, ?, ?)",
#                         (row['combineId'], row['combineYear'], row['combinePosition'], row['combineHeight'], row['combineWeight'], row['combineHand']))
#           print("Combine: " + row["combineId"])
#         except:
#           pass
# conn.commit()

# with open('players.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         row = change_empty_values(row)
#         try:
#           cursor.execute(" INSERT INTO players (playerId, combineId, nameFirst, nameLast, position, college, heightInches) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                         (row['playerId'], row['combineId'], row['nameFirst'], row['nameLast'], row['position'], row['college'], row['heightInches']))
#           print("Player: " + row["playerId"])
#         except:
#           pass
# conn.commit()


# cursor.execute("""
#   ALTER TABLE combine
#   ADD COLUMN playerId INTEGER REFERENCES players(playerId)
# """)
# conn.commit()

# with open('combine.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         row = change_empty_values(row)
#         print("Combine: " + row["combineId"] + "Player: " + row["playerId"])
#         try:
#             cursor.execute(" UPDATE combine SET playerId=(?) WHERE combineId=(?)",
#                            (row["playerId"], row["combineId"]))
#         except:
#             pass
# conn.commit()


# with open('fumbles.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         row = change_empty_values(row)
#         try:
#           cursor.execute("""
#         INSERT INTO fumbles (fumId, playId, playerId, fumPosition, fumType, fumOOB, fumTurnover, fumNull)
#         VALUES (?, ?, ?, ?, ?, ?, ?, ?)
#       """, (row['fumId'], row['playId'], row['playerId'], row['fumPosition'], row['fumType'], row['fumOOB'], row['fumTurnover'], row['fumNull']))
#           print("Fumble: " + row["fumId"])
#         except:
#           pass
# conn.commit()


# with open('gameParticipation.csv') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         row = change_empty_values(row)
#         try:
#           cursor.execute(" INSERT INTO gameParticipation (gamePartId, gameId, playerId, gamePartUnit, gamePartSnapCount, playerProfileUrl, homeCity, homeState) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#                         (row['gamePartId'], row['gameId'], row['playerId'], row['gamePartUnit'], row['gamePartSnapCount'], row['playerProfileUrl'], row['homeCity'], row['homeState']))
#           print("GamePart: " + row["gamePartId"])
#         except:
#           pass
# conn.commit()

with open('rusher.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        row = change_empty_values(row)
        try:
          cursor.execute(" INSERT INTO rusher (rushId, playId, playerId, rushPosition, rushType, rushDirection, rushLandmark, rushYards) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (row['rushId'], row['playId'], row['playerId'], row['rushPosition'], row['rushType'], row['rushDirection'], row['rushLandmark'], row['rushYards']))
          print("Rush: " + row["rushId"])
        except:
          pass
conn.commit()
