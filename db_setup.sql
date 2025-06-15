-- Required to allow the use of foreign keys in SQLite
PRAGMA foreign_keys = ON;

-- Drop tables if they already exist
DROP TABLE IF EXISTS Movies;
DROP TABLE IF EXISTS Engagements;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Oscars;
DROP TABLE IF EXISTS Awardings;
DROP TABLE IF EXISTS Ratings;
DROP TABLE IF EXISTS Viewers;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Tagging;


-- Create Viewers table
CREATE TABLE Viewers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL
);

-- Create Movies table
CREATE TABLE Movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL, -- for convenience, title is the only argument needed for inserting a new movie record
    path_to_cover_img TEXT, -- cover files will be stored in a dedicated folder, paths are *relative*
    year_of_release INTEGER, -- no full date, because they can differ between countries
    runtime_in_minutes INTEGER, -- no float, because the seconds don't matter
    added_by INTEGER,
    FOREIGN KEY (added_by) REFERENCES Viewers(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create Categories table
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL UNIQUE -- values must unique, as they represent distinct categories
);

-- Create Tagging table
-- This is a junction table to mediate between the Movies and Categories tables.
-- It models which categories are assigned to which movies (like a tagging mechanism).
CREATE TABLE Tagging(
    id INTEGER PRIMARY KEY,
    movie INTEGER, -- the movie that falls under the category
    category TEXT, -- the category that is assigned to the movie
    FOREIGN KEY (movie) REFERENCES Movies(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    FOREIGN KEY (category) REFERENCES Categories(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create Artists table
CREATE TABLE Artists (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    surname TEXT NOT NULL
);

-- Create Engagements table
-- This is a junction table to mediate between the Movie and Artist tables.
-- It models which artists were hired for which movie and for which jobs.
CREATE TABLE Engagements (
    id INTEGER PRIMARY KEY,
    movie INTEGER, -- the movie the artist was hired for
    artist INTEGER, -- the artist that was hired for the job
    job TEXT NOT NULL CHECK (job IN (
        'director',
        'actor',
        'composer',
        'producer'
    )), -- the range of allowed values can be altered later on; these are just cosidered as to be most important
    FOREIGN KEY (movie) REFERENCES Movies(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    FOREIGN KEY (artist) REFERENCES Artists(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create Oscars table
CREATE TABLE Oscars (
    id INTEGER PRIMARY KEY,
    movie INTEGER, -- the movie the Oscar refers to
    category TEXT NOT NULL CHECK (category IN (
        'Best Picture',
        'Best Director',
        'Best Actor',
        'Best Actress',
        'Best Cinematography',
        'Best Production Design',
        'Best Adapted Screenplay',
        'Best Sound',
        'Best Animated Short Film',
        'Best Live Action Short Film',
        'Best Film Editing',
        'Best Original Score',
        'Best Original Song',
        'Best Supporting Actor',
        'Best Supporting Actress',
        'Best Visual Effects',
        'Best Original Screenplay',
        'Best Documentary Short Film',
        'Best Documentary Feature Film',
        'Best International Feature Film',
        'Best Costume Design',
        'Best Makeup and Hairstyling',
        'Best Animated Feature Fi'
    )), -- this is a comprehensive list of all current categories (taken from wikipedia)
    FOREIGN KEY (movie) REFERENCES Movies(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create Awardings table
-- This is a junction table to mediate between the Oscars and Artists tables.
-- It models which artists won an academy award in which category.
CREATE TABLE Awardings (
    id INTEGER PRIMARY KEY,
    award INTEGER, -- the Oscar that goes to the winner
    winner INTEGER, -- the artist who won the Oscar
    FOREIGN KEY (award) REFERENCES Oscars(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    FOREIGN KEY (winner) REFERENCES Artists(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Create Ratings table
CREATE TABLE Ratings (
    id INTEGER PRIMARY KEY,
    movie INTEGER, -- the movie that is rated
    rater INTEGER, -- the viewer who rates the movie
    stars REAL NOT NULL, -- floating point ratings are allowed
    rank INTEGER, -- the rank on a ranking list a rater might assign to the movie; can be omitted for now, but might be useful in the future    
    FOREIGN KEY (movie) REFERENCES Movies(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    FOREIGN KEY (rater) REFERENCES Viewers(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);