from flask import Flask, request, jsonify, render_template
import sqlite3

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

    c.execute(f"PRAGMA foreign_key_list({table});")
    foreign_table = c.fetchall()

    foreign_keys = []
    foreign_tables = []

    for f in foreign_table:
        foreign_keys.append(f[3])
        foreign_tables.append(f[2])

    # close connection
    conn.close()
    return render_template("main_page.html", rows=table_data, table_name=table, column_names=names, foreign_keys=foreign_keys, foreign_tables=foreign_tables, foreign_count=len(foreign_keys))


@app.route('/get_row_data/<table>/<idName>/<id>', methods=['GET'])
def get_row(table, idName, id):
    # Retrieve row from database
    connection = sqlite3.connect('my_database.db')
    query = "SELECT * FROM {} WHERE {} = ?".format(table, idName)
    c = connection.execute(query, (id,))
    names = list(map(lambda x: x[0], c.description))
    row = c.fetchall()

    c.execute(f"PRAGMA foreign_key_list({table});")
    foreign_table = c.fetchall()

    foreign_keys = []
    foreign_tables = []

    for f in foreign_table:
        foreign_keys.append(f[3])
        foreign_tables.append(f[2])

    return render_template("row_page.html", rows=row, table_name=table, column_names=names, foreign_keys=foreign_keys, foreign_tables=foreign_tables, foreign_count=len(foreign_keys))


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

@app.route('/delete_row/<table>', methods=['POST'])
def delete_row_from_table(table):
    # connect to sqlite database
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # retrieve values from POST request body
    values = request.form.items()

    names = []
    valueElements = []

    for i in values:
        names.append(i[0])
        valueElements.append(i[1])

    idName = names[0]
    idValue = valueElements[0]

    # Build the DELETE statement

    delete_sth = 'DELETE FROM {} WHERE {} = {}'.format(
        table,
        idName,
        idValue
    )

    # Execute the DELETE statement
    c.execute(delete_sth)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    return jsonify({'message': 'row deleted successfully'})

@app.route('/update_row/<table>', methods=['POST'])
def update_table_row(table):
    # connect to sqlite database
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()

    # retrieve values from POST request body
    values = request.form.items()
    names = []
    valueElements = []
    for i in values:
        names.append(i[0])
        valueElements.append(i[1])

    primaryKeyName = names[0]
    names.remove(primaryKeyName)
    primaryKeyValue = valueElements[0]
    valueElements.remove(primaryKeyValue)
    
    # Build the UPDATE statement
    update_stmt = 'UPDATE {} SET ({}) = ({}) WHERE {} = {}'.format(
        table,
        ', '.join(str(x) for x in names),
        ", ".join(["?"] * len(names)),
        primaryKeyName,
        primaryKeyValue
    )

    # Execute the UPDATE statement
    c.execute(update_stmt, valueElements)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
    return jsonify({'message': 'row updated successfully'})



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
