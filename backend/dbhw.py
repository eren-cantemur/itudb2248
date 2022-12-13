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
  gameId TEXT,
  playerId INTEGER,
  gamePartUnit INTEGER,
  gamePartSnapCount INTEGER,
  playerProfileUri TEXT,
  homeCity TEXT,
  homeState TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXIST plays (
  playId INTEGER PRIMARY KEY,
  gameID INTEGER,
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

# Function to retrieve all rows from the database
def get_all_rows():
  cursor.execute("""
    SELECT * FROM my_table
  """)
  return cursor.fetchall()

def row_exists(id):
  cursor.execute("""
    SELECT 1 FROM my_table
    WHERE id = ?
  """, (id,))
  return cursor.fetchone() is not None

# Function to search for rows that match a given search term
def search_rows(search_term):
  cursor.execute("""
    SELECT * FROM my_table
    WHERE name LIKE ? OR age LIKE ?
  """, (f"%{search_term}%", f"%{search_term}%"))
  return cursor.fetchall()

# Function to count the number of rows in the database
def count_rows():
  cursor.execute("""
    SELECT COUNT(*) FROM my_table
  """)
  return cursor.fetchone()[0]

# Function to retrieve a single row by id
def get_row(id):
  cursor.execute("""
    SELECT * FROM my_table
    WHERE id = ?
  """, (id,))
  return cursor.fetchone()

# Function to update a row by id
def update_row(id, name, age):
  cursor.execute("""
    UPDATE my_table
    SET name = ?, age = ?
    WHERE id = ?
  """, (name, age, id))
  conn.commit()

def add_row(name, age):
  cursor.execute("""
    INSERT INTO my_table (name, age)
    VALUES (?, ?)
  """, (name, age))
  conn.commit()

# Function to delete a row by id
def delete_row(id):
  cursor.execute("""
    DELETE FROM my_table
    WHERE id = ?
  """, (id,))
  conn.commit()

# Close the connection
conn.close()


@app.route('/add_row', methods=['POST'])
def add_row():
  # Parse the request data
  data = request.get_json()
  name = data.get('name')
  age = data.get('age')

  # Add the row to the database
  add_row(name, age)

  # Return a success response
  return jsonify({'success': True})

  # API route to check if a row with a given id exists in the database
@app.route('/row_exists', methods=['POST'])
def row_exists():
  # Parse the request data
  data = request.get_json()
  id = data.get('id')

  # Check if the row exists
  exists = row_exists(id)

  # Return the result
  return jsonify({'exists': exists})

# API route to search for rows that match a given search term
@app.route('/search_rows', methods=['POST'])
def search_rows():
  # Parse the request data
  data = request.get_json()
  search_term = data.get('search_term')

  # Search for rows that match the search term
  rows = search_rows(search_term)

  # Return the search results
  return jsonify({'rows': rows})

# API route to count the number of rows in the database
@app.route('/count_rows', methods=['GET'])
def count_rows():
  # Count the number of rows in the database
  count = count_rows()

  # Return the row count
  return jsonify({'count': count})

# API route to add a new row to the database
@app.route('/add_row', methods=['POST'])
def add_row():
  # Parse the request data
  data = request.get_json()
  name = data.get('name')
  age = data.get('age')

  # Add the row to the database
  add_row(name, age)

  # Return a success response
  return jsonify({'success': True})

# API route to retrieve all rows from the database
@app.route('/get_all_rows', methods=['GET'])
def get_all_rows():
  # Retrieve all rows from the database
  rows = get_all_rows()

  # Return the rows
  return jsonify({'rows': rows})

# API route to retrieve a single row by id
@app.route('/get_row', methods=['POST'])
def get_row():
  # Parse the request data
  data = request.get_json()
  id = data.get('id')

  # Retrieve the row by id
  row = get_row(id)

  # Return the row
  return jsonify({'


