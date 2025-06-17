import sqlite3
from dataclasses import dataclass

@dataclass
class Oscar:
    movie: int
    category: str
    winner_ids: list[int]
    winners: list[Artist]

@dataclass
class Engagement:
    movie: int
    artist: int
    role: str

@dataclass
class Artist:
    first_name: str
    surname: str
    oscar_ids: list[int] = []
    oscars: list[Oscar] = []
    engagement_ids: list[int] = []
    engagements: list[Engagement] = []


class Database:
    def __init__(self, path_to_db: str):
        self.con = sqlite3.connect(path_to_db)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
    
    def read_artist(self, id: int, nesting: bool = False, propagate: bool = False):
        artist = self.cur.execute("SELECT first_name, surname FROM Artists WHERE id = ?", (id,)).fetchone()
        oscars = self.cur.execute("SELECT award FROM Oscars WHERE winner = ?", (id,)).fetchall()
        engagements = self.cur.execute("SELECT id, movie, role FROM Engagements WHERE artist = ?", (id,)).fetchall()

        if nesting:
            return Artist(artist["first_name"], artist["surname"], [oscar["id"] for oscar in oscars], [])

        return Artist(artist["first_name"], artist["surname"], [oscar["id"] for oscar in oscars], [eng["id"] for eng in engagements])
    
    def read_oscar(self, id: int) -> Oscar:
        oscar = self.cur.execute("SELECT movie, category FROM Oscars WHERE id = ?", (id,)).fetchone()
        winners = self.cur.execute("SELECT winner FROM Awardings WHERE award = ?", (id,)).fetchall()
        return Oscar(oscar["movie"], oscar["category"], [winner["winner"] for winner in winners])
    
    def __del__(self):
        self.cur.close()
        self.con.close()


db = Database("./data/watchlist.db")
#print(db.get_movie_data(1))
#db.add_rating(1, 1, 3.7)
#id = db.select_movie("The Ninth Gat")
#print(id)
