import sqlite3

con = sqlite3.connect("./data/watchlist.db")
cur = con.cursor()

def add_viewer(first_name, surname):
    cur.execute("INSERT INTO Viewers (first_name, surname) VALUES (?, ?)", first_name, surname)
    con.commit()

def add_viewers(data):
    cur.executemany("INSERT INTO Viewers (first_name, surname) VALUES (?, ?)", data)
    con.commit()

add_viewers([
    ('Benedikt', 'Ehrenwirth'),
    ('Jonathan', 'Ehrenwirth'),
    ('Florian', 'Ehrenwirth'),
    ('Johannes', 'Knoll'),
    ('Konstantin', 'Kraus')
])

con.close()
