import sqlite3

class Database:
    def __init__(self, path_to_db: str):
        self.con = sqlite3.connect(path_to_db)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
    
    def add_movie(self, title: str, added_by: int, path_to_cover_img: str = None, year_of_release: int = None, runtime_in_minutes: int = None, streaming_platform: str = None) -> int:
        pass

    def add_tag(self, movie: int, category: int) -> int:
        query = self.cur.execute("INSERT INTO Tagging (movie, category) VALUES (?, ?)", (movie, category))
        return query.lastrowid

    def add_tags(self, data: list[tuple]) -> int:
        query = self.cur.execute("INSERT INTO Tagging VALUES (?)", data)
        return query.lastrowid

    def add_category(self, category_name: str) -> int:
        pass
    
    def add_oscar(self, movie: int, category: str) -> int:
        pass

    def add_awarding(self, award: int, winner: int) -> int:
        pass

    def add_artist(self, first_name: str, surname: str) -> int:
        pass

    def add_rating(self, movie: int, rater: int, stars: float, rank: int = None) -> int:
        pass

    def add_viewer(self, first_name: str, surname: str) -> int:
        pass
    
    def __del__(self):
        self.cur.close()
        self.con.close()
