from flask import Flask, render_template, request, redirect, jsonify, abort
import sqlite3
import os
from helpers import get_last, insert_data, delete_data, get_all_data

app = Flask(__name__)

# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')

# Create a cursor object
cur = conn.cursor()

# Create the `data` table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT
)''')

# Close the cursor object
cur.close()

# Commit the changes to the database
conn.commit()

# Close the connection to the database
conn.close()

# Define a route to display the data in the database
@app.route('/', methods=['GET', 'POST'])
def index():
    # Use helper to get all rows for listing (if you want latest, use get_last())
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM data')
    data = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        # Use helper to insert the posted data
        text = request.form.get('data', '')
        insert_data(text)
        return redirect('/')

    # Render the index.html template with the data from the database
    return render_template('index.html', data=data)

# Define a route to add a new row to the database
@app.route('/add', methods=['POST'])
def add():
    # Use helper to insert the posted data and redirect back
    text = request.form.get('data', '')
    insert_data(text)
    return redirect('/')

# Define a route to delete a row from the database
@app.route('/delete/<int:id>')
def delete(id):
    # Create a connection to the SQLite database
    conn = sqlite3.connect('database.db')

    # Create a cursor object
    cur = conn.cursor()

    # Delete the row with the specified ID from the `data` table
    cur.execute('DELETE FROM data WHERE id = ?', (id,))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor object
    cur.close()

    # Close the connection to the database
    conn.close()

    # Redirect the user back to the main page
    return redirect('/')


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/dump', methods=['GET'])
def dump_db():
    """Return the entire contents of the `data` table as JSON.

    Protection: require a key that matches the environment variable DUMP_KEY.
    The client may provide the key in the X-Dump-Key header or as ?key= in the query string.
    """

    # get JSON-serializable rows from helper
    rows = get_all_data()
    return jsonify(rows)
