from flask import Flask, g, jsonify, render_template
import sqlite3
import os

DATABASE = 'database.db'

# Create app
app = Flask(__name__)
app.config['DEBUG'] = True

# check if the database exist, if not create the table
# and insert a few lines of data
if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # NOTE: SQLite creates a ROWID (64bit signed integer) automatically
    cur.execute("CREATE TABLE users \
                (nombre TEXT, apellido TEXT, password TEXT);")
    conn.commit()
    cur.execute("INSERT INTO users VALUES('Mike', 'Tyson', '1234');")
    cur.execute("INSERT INTO users VALUES('Thomas', 'Jasper', '12345');")
    cur.execute("INSERT INTO users VALUES('Jerry', 'Mouse', '123456');")
    cur.execute("INSERT INTO users VALUES('Peter', 'Pan', '1234567');")
    conn.commit()
    conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/users")
def index():
    cur = get_db().cursor()
    res = cur.execute("select * from users")
    return render_template('index.html', users=res)
    # return jsonify(res.fetchall())


if __name__ == "__main__":
    app.run()
