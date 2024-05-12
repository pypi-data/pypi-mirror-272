REQUIRED_COLUMNS = ["isbn", "title", "description", "author", "genre"]

COMMANDS = (
    "DROP TABLE IF EXISTS BookAuthor;",
        
    "DROP TABLE IF EXISTS Author;",
        
    "DROP TABLE IF EXISTS BookGenre;",
        
    "DROP TABLE IF EXISTS Genre;",
        
    "DROP TABLE IF EXISTS History;",
        
    "DROP TABLE IF EXISTS Book;",
        
    """CREATE TABLE Book (
        ISBN VARCHAR(20) PRIMARY KEY,
        title VARCHAR(2000) NOT NULL,
        description VARCHAR(20000) NOT NULL,
        embedding VECTOR(384) NOT NULL, 
        available BOOLEAN NOT NULL
    );""",
        
    """CREATE TABLE Author (
        author_id SERIAL PRIMARY KEY,
        full_name VARCHAR(200) NOT NULL
    );""",

    """CREATE TABLE Genre (
        genre_id SERIAL PRIMARY KEY,
        genre VARCHAR(100) NOT NULL
    );""",

    """CREATE TABLE BookAuthor (
        ISBN VARCHAR(20),
        author_id INTEGER,
        PRIMARY KEY (ISBN, author_id),
        FOREIGN KEY (author_id) REFERENCES Author(author_id),
        FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON UPDATE CASCADE ON DELETE CASCADE
    );""",

    """CREATE TABLE BookGenre (
        ISBN VARCHAR(20),
        genre_id INTEGER,
        PRIMARY KEY (ISBN, genre_id),
        FOREIGN KEY (genre_id) REFERENCES Genre(genre_id),
        FOREIGN KEY (ISBN) REFERENCES Book(ISBN) ON UPDATE CASCADE ON DELETE CASCADE
    );""",
 
    """CREATE TABLE History (
        log_id SERIAL PRIMARY KEY,
        description VARCHAR(20000) NOT NULL,
        recommendation_ISBN VARCHAR(20) NOT NULL,
        successful BOOLEAN NOT NULL,
        datetime TIMESTAMP NOT NULL DEFAULT (NOW() AT TIME ZONE 'utc'),
        FOREIGN KEY (recommendation_ISBN) REFERENCES Book(ISBN) ON UPDATE CASCADE ON DELETE CASCADE
    );"""
)