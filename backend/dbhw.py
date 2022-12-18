from flask import Flask, request, jsonify, render_template
import sqlite3
import csv

app = Flask(__name__, template_folder='../frontend')

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Function to retrieve all rows from the database
@app.route('/get_table_data/<table>', methods=['GET'])
def get_table_data(table):
    # connect to sqlite database
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # retrieve all rows from specified table
    c.execute(f"SELECT * FROM {table}")
    table_data = c.fetchall()
    names = list(map(lambda x: x[0], c.description))
    foreignIndexes = []
    foreignTables = []

    if (table == "gameParticipation"):
        foreignIndexes = [1, 2]
        foreignTables = ["games", "players"]
    if (table == "plays"):
        foreignIndexes = [1]
        foreignTables = ["games"]
    if (table == "combine"):
        foreignIndexes = [1]
        foreignTables = ["players"]

    if (table == "fumbles"):
        foreignIndexes = [1, 2]
        foreignTables = ["plays", "players"]


    # close connection
    conn.close()
    return render_template("main_page.html", rows=table_data, table_name=table, column_names=names,
                           foreignIndexes=foreignIndexes, foreignTables=[foreignTables])


@app.route('/get_row_data/<table>/<idName>/<id>', methods=['GET'])
def get_row(table, idName, id):
    # Retrieve row from database
    connection = sqlite3.connect('my_database.db')
    query = "SELECT * FROM {} WHERE {} = ?".format(table, idName)
    c = connection.execute(query, (id,))
    names = list(map(lambda x: x[0], c.description))
    row = c.fetchall()
    foreignIndexes = []
    foreignTables = []

    if (table == "gameParticipation"):
        foreignIndexes = [1, 2]
        foreignTables = ["games", "players"]
    if (table == "plays"):
        foreignIndexes = [1]
        foreignTables = ["games"]
    if table == "combines":
        foreignIndexes = [1]
        foreignTables = ["players"]

    return render_template("main_page.html", rows=row, table_name=table, column_names=names,
                           foreignIndexes=foreignIndexes, foreignTables=[foreignTables])

@app.route('/delete_row/<table>, methods=['POST'])
def delete_row_from_table(table):
    # connect to sqlite database
    print("del")
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # retrieve values from POST request body
    values = request.form.items()
    idName = str(values[0])
    idValue = int(values[1])

    # Build the DELETE statement

    delete_sth = 'DELETE FROM {} WHERE {} = ?'.format(
        table,
        idName
    )

    # Execute the DELETE statement
    c.execute(delete_sth, idValue)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    return jsonify({'message': 'row deleted successfully'})


@app.route('/insert_row/<table>', methods=['POST'])
def insert_table_row(table):
    # connect to sqlite database
    print("in")
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # retrieve values from POST request body
    values = request.form.items()
    names = []
    valueElements = []
    for i in values:
        names.append(i[0])
        valueElements.append(i[1])
    print(names)
    # Build the INSERT statement
    insert_stmt = 'INSERT INTO {} ({}) VALUES ({})'.format(
        table,
        ', '.join(str(x) for x in names),
        ", ".join(["?"] * len(names))
    )

    # Execute the INSERT statement
    print(valueElements)
    c.execute(insert_stmt, valueElements)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    return jsonify({'message': 'row inserted successfully'})



# client side
@app.route('/get')
def home():
    # Connect to the database
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # Retrieve all data from the combine table

    rows = c.fetchall()

    # Close the connection
    conn.close()

    # Render the data as a table in a web page
    return render_template("main_page.html", combine_rows=rows)


# Pass the rows to the template to be rendered as an HTML table


# def row_exists(row_id,tableName):
#   cursor.execute("""
#     SELECT 1 FROM tableName
#     WHERE id = ?
#   """, (row_id,))
#   return cursor.fetchone() is not None

# Function to search for rows that match a given search term
# def search_rows(search_term):
#   cursor.execute("""
#     SELECT * FROM my_table
#     WHERE name LIKE ? OR age LIKE ?
#   """, (f"%{search_term}%", f"%{search_term}%"))
#   return cursor.fetchall()

# # Function to count the number of rows in the database
# def count_rows():
#   cursor.execute("""
#     SELECT COUNT(*) FROM my_table
#   """)
#   return cursor.fetchone()[0]
#
# # Function to retrieve a single row by id
# def get_row(id):
#   cursor.execute("""
#     SELECT * FROM my_table
#     WHERE id = ?
#   """, (id,))
#   return cursor.fetchone()
#
# # Function to update a row by id
# def update_row(id, name, age):
#   cursor.execute("""
#     UPDATE my_table
#     SET name = ?, age = ?
#     WHERE id = ?
#   """, (name, age, id))
#   conn.commit()
#
# def add_row_to_db(name, age):
#   cursor.execute("""
#     INSERT INTO my_table (name, age)
#     VALUES (?, ?)
#   """, (name, age))
#   conn.commit()

# Function to delete a row by id
# def delete_row(id):
#   cursor.execute("""
#     DELETE FROM my_table
#     WHERE id = ?
#   """, (id,))
#   conn.commit()
#
# # Close the connection
# conn.close()


# @app.route('/add_row', methods=['POST'])
# def add_row():
#   # Parse the request data
#   data = request.get_json()
#   tableName = data.get('name')
#
#   return jsonify({'success': True})
# #
#   # API route to check if a row with a given id exists in the database
# @app.route('/row_exists', methods=['POST'])
# def row_exists():
#   # Parse the request data
#   data = request.get_json()
#   id = data.get('id')
#
#   # Check if the row exists
#   exists = row_exists(id)
#
#   # Return the result
#   return jsonify({'exists': exists})
#
# # API route to search for rows that match a given search term
# @app.route('/search_rows', methods=['POST'])
# def search_rows():
#   # Parse the request data
#   data = request.get_json()
#   search_term = data.get('search_term')
#
#   # Search for rows that match the search term
#   rows = search_rows(search_term)
#
#   # Return the search results
#   return jsonify({'rows': rows})
#
# # API route to count the number of rows in the database
# @app.route('/count_rows', methods=['GET'])
# def count_rows():
#   # Count the number of rows in the database
#   count = count_rows()
#
#   # Return the row count
#   return jsonify({'count': count})
#
# # API route to add a new row to the database
# @app.route('/add_row', methods=['POST'])
# def add_row():
#   # Parse the request data
#   data = request.get_json()
#   name = data.get('name')
#   age = data.get('age')
#
#   # Add the row to the database
#   add_row(name, age)
#
#   # Return a success response
#   return jsonify({'success': True})
#
# # API route to retrieve all rows from the database
# @app.route('/get_all_rows', methods=['GET'])
# def get_all_rows():
#   # Retrieve all rows from the database
#   rows = get_all_rows()
#
#   # Return the rows
#   return jsonify({'rows': rows})
#
# # API route to retrieve a single row by id
# @app.route('/get_row', methods=['POST'])
# def get_row():
#   # Parse the request data
#   data = request.get_json()
#   id = data.get('id')
#
#   # Retrieve the row by id
#   row = get_row(id)
#
#   # Return the row
#   return jsonify({'
#
#