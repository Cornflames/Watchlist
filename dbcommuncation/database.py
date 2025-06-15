import sqlite3

class Oscar:
    def __init__(self, movie: int, category: str, winners: list[int]):
        self.movie = movie
        self.category = category
        self.winners = winners

class Database:
    def __init__(self, path_to_db: str):
        self.con = sqlite3.connect(path_to_db)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
    
    def read_oscars_for_movie(self, movie: int):
        res = []
        oscars = self.cur.execute("SELECT id, category FROM Oscars WHERE movie = ?", (movie,)).fetchall()
        for oscar in oscars:
            winners = self.cur.execute("SELECT winner FROM Awardings WHERE award = ?", (oscar["id"],)).fetchall()
            res.append(Oscar(movie, oscar["category"], [winner["winner"] for winner in winners]))
        return res
    
    def read_oscars_for_artist(self, artist: int):
        res = []
        oscars = self.cur.execute("SELECT movie, category FROM Oscars WHERE id IN (SELECT award FROM Awardings WHERE winner = ?)", (artist,))
        pass

    
    def select_movie(self, title: str) -> int:
        try:
            res_query = self.cur.execute("SELECT id FROM Movies WHERE title = ?", (title,)).fetchall()
            if len(res_query) == 0:
                raise RuntimeError("Cannot find the movie '{}': there is no record with this title".format(title))
            elif len(res_query) == 1:
                movie_id = res_query[0][0]
            else:
                raise RuntimeError("Cannot uniquely identify the movie '{}': there are several records with this title: {}".format(title, res_query))
        except Exception as e:
            print("ERROR in select_movie: {}".format(e))
            return None
        return movie_id
 
    def add_rating(self, movie_id: int, rater_id: int, stars: float, rank: int = None) -> int:
        try:
            new_rating_id = self.cur.execute(
                "INSERT INTO Ratings (movie, rater, stars, rank) VALUES (?, ?, ?, ?)", 
                (movie_id, rater_id, stars, rank)
            ).lastrowid
            self.con.commit()
        except:
            return None
        return new_rating_id
    
    def get_movie_data(self, id):
        res = dict(self.cur.execute("SELECT * FROM Movies WHERE id = ?", (id,)).fetchone())

        directors = [
            artist["first_name"] + " " + artist["surname"]
            for artist in self.cur.execute("SELECT first_name, surname FROM Artists WHERE id IN (SELECT artist FROM Engagements WHERE movie = ? AND job = 'director')", (id,)).fetchall()
        ]
        res["direction"] = directors
        
        actors = [
            artist["first_name"] + " " + artist["surname"]
            for artist in self.cur.execute("SELECT first_name, surname FROM Artists WHERE id IN (SELECT artist FROM Engagements WHERE movie = ? AND job = 'actor')", (id,)).fetchall()
        ]
        res["cast"] = actors

        if res["added_by"] != None:
            viewer = self.cur.execute("SELECT first_name, surname FROM Viewers WHERE id = ?", (res["added_by"],)).fetchone()
            res["added_by"] = viewer["first_name"] + " " + viewer["surname"]
        
        categories = self.cur.execute("SELECT category_name FROM Categories WHERE id IN (SELECT category FROM Tagging WHERE movie = ?)", (id,)).fetchall()
        if len(categories) > 0:
            res["categories"] = [category["category_name"] for category in categories]
        else:
            res["categories"] = None
        
        oscars = {}
        oscars_res = self.cur.execute("SELECT id, category FROM Oscars WHERE movie = ?", (id,)).fetchall()
        if len(oscars_res) > 0:
            for oscar in oscars_res:
                winners = self.cur.execute("SELECT first_name, surname FROM Artists WHERE id IN (SELECT winner FROM Awardings WHERE award = ?)", (oscar["id"],)).fetchall()
                oscars[oscar["category"]] = [winner["first_name"] + " " + winner["surname"] for winner in winners]
        res["Oscars"] = oscars
        
        ratings = {}
        ratings_res = self.cur.execute("SELECT rater, stars, rank FROM Ratings WHERE movie = ?", (id,)).fetchall()
        if len(ratings_res) > 0:
            for rating in ratings_res:
                rating = dict(rating)
                rater = self.cur.execute("SELECT first_name, surname FROM Viewers WHERE id = ?", (rating.pop("rater"),)).fetchone()
                ratings[rater["first_name"] + " " + rater["surname"]] = rating
        res["Ratings"] = ratings

        return res
    
    def read_to_objects(self):
        pass
    
    def __del__(self):
        self.cur.close()
        self.con.close()

db = Database("./data/watchlist.db")
print(db.get_movie_data(1))
#db.add_rating(1, 1, 3.7)
#id = db.select_movie("The Ninth Gat")
#print(id)
