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
    combineHeight FLOAT,
    combineWeight FLOAT,
    combineHand FLOAT
)
""")

# Read data from CSV file and write it to the database
with open('data.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    cursor.execute("""
      INSERT INTO my_table (id, name, age)
      VALUES (?, ?, ?)
    """, (row['combineId'], row['playerId'], row['combineYear'], row['combinePosition'], row['combineHeight'], row['combineWeight'], row['combineHand']))

# Save (commit) the changes
conn.commit()