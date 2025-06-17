import sqlite3

class Database:
    def __init__(self, path_to_db: str):
        self.con = sqlite3.connect(path_to_db)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
    

    
    def __del__(self):
        self.cur.close()
        self.con.close()
