from flask import Flask, request, jsonify, render_template
import sqlite3
import csv

app = Flask(__name__, template_folder='../frontend')

# Connect to the database
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

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
    # close connection
    conn.close()
    return render_template("main_page.html", rows=table_data, table_name=table, column_names=names,
                           foreignIndexes=foreignIndexes, foreignTables=[foreignTables])


@app.route('/get_row_data/<table>/<id>', methods=['GET'])
def get_row(table, id):
    # Retrieve row from database
    connection = sqlite3.connect('my_database.db')
    query = "SELECT * FROM {} WHERE id = ?".format(table)
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

    return render_template("main_page.html", rows=row, table_name=table, column_names=names,
                           foreignIndexes=foreignIndexes, foreignTables=[foreignTables])


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



