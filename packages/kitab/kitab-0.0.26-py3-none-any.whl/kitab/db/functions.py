"""
This module contains tailored functions for interacting with the database. These are used by the API and the recommendation model.
"""
import pandas as pd
from kitab.utils import get_embedding
from .db_credentials import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from .sql_interactions import SqlHandler
import logging
from ..logger.logger import CustomFormatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

def get_book_by_ISBN(ISBN: str, verbose: bool = False) -> tuple[dict]:
    """
    Retrieves a book from the database based on its ISBN.
    
    Examples:
        >>> from kitab.db.functions import get_book_by_ISBN
        >>> get_book_by_ISBN("1442942355")

    Parameters:
        ISBN (str): The ISBN of the book to retrieve.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        tuple[dict]: A tuple containing the book information, authors, and genres if found, or None if no book is found.
    """

    # Open connection to the database
    db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    if verbose:
        logger.info("Database connection opened.")
    
    # Retrieve the book with the given ISBN
    book = db.get_table("book", conditions={"isbn": ISBN})
    
    if len(book) == 0:
        logger.info("Book not found.")
        return None
    
    if verbose:
        logger.info("Book retrieved.")
    
    book_author = db.get_table("bookauthor", conditions={"isbn": ISBN})
    book_genre = db.get_table("bookgenre", conditions={"isbn": ISBN})
        
    # If no book found, return None
    if len(book) == 0:
        return None, None, None
    
    book.drop(columns=["embedding"], inplace=True)
    book = book.to_dict(orient='records')[0]

    author_ids = book_author["author_id"].tolist()
    authors = []
    if len(author_ids) > 0:
        author = db.get_table("author", conditions={"author_id": author_ids})
        authors = author["full_name"].tolist()
        if verbose:
            logger.info(f"Authors retrieved.")
    else:
        if verbose:
            logger.info("No authors found.")
    
    genre_ids = book_genre["genre_id"].tolist()
    genres = []
    if len(genre_ids) > 0:
        genre = db.get_table("genre", conditions={"genre_id": genre_ids})
        genres = genre["genre"].tolist()
        if verbose:
            logger.info(f"Genres retrieved.")
    else:
        if verbose:
            logger.info("No genres found.")
    
    book["authors"] = authors
    book["genres"] = genres

    # Return the book
    return book


def get_book_by_title(title: str, verbose: bool = False) -> tuple[dict]:
    """
    Retrieves a book from the database based on its title.
    
    Examples:
        >>> from kitab.db.functions import get_book_by_title
        >>> get_book_by_title("The Ghostly Rental")

    Parameters:
        title (str): The title of the book to retrieve.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        tuple[dict]: A tuple containing the book information, authors, and genres if found, or None if no book is found.
    """
    # Open connection to the database
    db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    if verbose:
        logger.info("Database connection opened.")
    
    # Retrieve the book with the given title
    books = db.get_table("book", conditions={"title": title})
        
    if len(books) == 0:
        if verbose:
            logger.info("Book not found.")
        return None
    else:
        if verbose:
            logger.info("Book ISBN retrieved.")
        ISBN = books["isbn"].values[0]

    # Return the book
    return get_book_by_ISBN(ISBN)


def add_book_db(book: dict, verbose: bool = False) -> bool:
    """
    Adds a book to the database.
    
    Examples:
        >>> from kitab.db.functions import add_book_db
        >>> add_book_db({
                "isbn": "1442942355",
                "title": "The Ghostly Rental",
                "description": "Employing the subtle methods of presenting mysterious ghost stories in the backdrop of psychological troubles, the novel presents the life of James. The troubles that he faces, combined with the baffling events around him give an aura to the novel that is almost unsurpassable",
                "available": False,
                "authors": [
                    "Henry James"
                ],
                "genres": [
                    "Horror",
                    "Short Stories",
                    "The United States Of America"
                ]
            })

    Parameters:
        book (dict): A dictionary containing the book information.
    
    Returns:
        bool: True if the book was successfully added, False otherwise.
    """
    try:
        # Open connection to the database
        db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        if verbose:
            logger.info("Database connection opened.")
            
        # Extract information from the book dictionary
        ISBN = book["isbn"]
        title = book["title"]
        description = book["description"]
        available = book["available"]
        embedding = get_embedding(book["description"]).tolist()
        
        db.insert_records("book", [{"isbn": ISBN, "title": title, "description": description, "embedding": embedding, "available": available}])
        if verbose:
            logger.info("Book table populated.")
        
        # Add author(s) to the author table if doesn't exist
        authors = book["authors"]
        if len(authors) > 0:
            if verbose:
                logger.info("Authors to be added.")
            author_ids = _get_or_add_authors(db, authors)
            
            db.insert_records("bookauthor", [{"isbn": ISBN, "author_id": int(author_id)} for author_id in author_ids])
            if verbose:
                logger.info("Author table populated.")
        else:
            if verbose:
                logger.info("No authors to be added.")
        
        # Add genres to the genres table if doesn't exist
        genres = book["genres"]    
        if len(genres) > 0:
            if verbose:
                logger.info("Genres to be added.")
            genre_ids = _get_or_add_genres(db, genres)
            
            db.insert_records("bookgenre", [{"isbn": ISBN, "genre_id": int(genre_id)} for genre_id in genre_ids])
            if verbose:
                logger.info("Genre table populated.")
        else:
            if verbose:
                logger.info("No genres to be added.")

        return True
    except:
        return False    
    
def update_book_db(ISBN: str, new_book: dict, verbose: bool = False) -> bool:
    """
    Updates a book in the database.
    
    Examples:
        >>> from kitab.db.functions import update_book_db
        >>> update_book_db("1442942355", {
                "available": True,
                "genres": [
                    "Horror",
                    "Short Stories",
                    "Mystery"
                ]
            })
    
    Parameters:
        ISBN (str): The ISBN of the book to update.
        new_book (dict): A dictionary containing the updated book information.
        verbose (bool): Whether to print verbose output. Defaults to False.
    
    Returns:
        bool: True if the book was successfully updated, False otherwise.
    """
    try:
        # Open connection to the database
        db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        if verbose:
            logger.info("Database connection opened.")
        
        condition = {"ISBN": ISBN}
        new_values = {}
        
        latest_ISBN = ISBN
        
        for key in new_book.keys():
            if key in ["ISBN", "title", "description", "available"]:
                new_values[key] = new_book[key]
            if key == "ISBN":
                latest_ISBN = new_book["ISBN"]
            if key == "description":
                new_values["embedding"] = get_embedding(new_book["description"]).tolist()

        db.update_records("book", new_values, condition)
        if verbose:
            logger.info("Book table updated.")
        
        ISBN = latest_ISBN
        
        # Get the tables
        book_author = db.get_table("bookauthor", conditions={"isbn": ISBN})
        book_genre = db.get_table("bookgenre", conditions={"isbn": ISBN})
        
        # Add author(s) to the author table if doesn't exist
        if "authors" in new_book:
            if verbose:
                logger.info("Authors to be updated.")
            
            authors = new_book["authors"]
            new_author_ids = set(_get_or_add_authors(db, authors))
            current_author_ids = set(book_author[book_author["isbn"] == ISBN]["author_id"].tolist())
            
            removed_authors = current_author_ids - new_author_ids
            added_authors = new_author_ids - current_author_ids
            
            db.remove_records("bookauthor", [{"isbn": ISBN, "author_id": int(removed_author)} for removed_author in removed_authors])
            db.insert_records("bookauthor", [{"isbn": ISBN, "author_id": int(added_author)} for added_author in added_authors])
            
            if verbose:
                logger.info("Author table updated.")
        else:
            if verbose:
                logger.info("No authors to be updated.")
        
        # Add genres to the genres table if doesn't exist
        if "genres" in new_book:
            if verbose:
                logger.info("Genres to be updated.")
            
            genres = new_book["genres"]    
            new_genre_ids = set(_get_or_add_genres(db, genres))
            current_genre_ids = set(book_genre[book_genre["isbn"] == ISBN]["genre_id"].tolist())
        
            removed_genres = current_genre_ids - new_genre_ids
            added_genres = new_genre_ids - current_genre_ids
            
            db.remove_records("bookgenre", [{"isbn": ISBN, "genre_id": int(removed_genre)} for removed_genre in removed_genres])
            db.insert_records("bookgenre", [{"isbn": ISBN, "genre_id": int(added_genre)} for added_genre in added_genres])
            
            if verbose:
                logger.info("Genre table updated.")
        else:
            if verbose:
                logger.info("No genres to be updated.")
            
        return True
    except:
        return False

def get_table_from_db(table_name: str, conditions: dict = None, verbose: bool = False) -> pd.DataFrame:
    """
    Retrieves a table from the database.
    
    Examples:
        >>> from kitab.db.functions import get_table_from_db
        >>> get_table_from_db("book", conditions={"available": True})

    Parameters:
        table_name (str): The name of the table to retrieve.
        conditions (dict): A dictionary of conditions to filter the table.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the table information.
    """
    # Open connection to the database
    db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    if verbose:
        logger.info("Database connection opened.")
    
    # Retrieve the table from the database
    if conditions:
        table = db.get_table(table_name, conditions=conditions)
    else:
        table = db.get_table(table_name)
        
    if verbose:
        logger.info(f"Table {table_name} retrieved.")
    
    # Return the table
    return table

def _get_or_add_genres(db: SqlHandler, genres: list[str], verbose: bool = False) -> list[int]:
    """
    Get the genre IDs for the given list of genres. If the genres do not exist in the database, add them to the genre table.
    
    Examples:
        >>> from kitab.db.functions import _get_or_add_genres
        >>> _get_or_add_genres(db, genres=["Horror", "Short Stories"])

    Parameters:
        db (SqlHandler): The database handler.
        genres (list[str]): A list of genres.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        list[int]: A list of genre IDs.
    """
    genre_table = db.get_table("genre")
    
    genre_ids = []
    cur_index = max(genre_table["genre_id"] + 1)
    to_insert = []
    
    for genre in genres:
        if genre in genre_table["genre"].values:
            genre_id = genre_table[genre_table["genre"] == genre]["genre_id"].values[0]
        else:
            genre_id = cur_index
            cur_index += 1
            to_insert.append({"genre_id": genre_id, "genre": genre})
        genre_ids.append(genre_id)
    
    # Insert the records
    db.insert_records("genre", to_insert)
    if verbose:
        logger.info("New genres added.")
    
    return genre_ids

def _get_or_add_authors(db: SqlHandler, authors: list[str], verbose: bool = False) -> list[int]:
    """
    Get the author IDs for the given list of authors. If the authors do not exist in the database, add them to the author table.
    
    Examples:
        >>> from kitab.db.functions import _get_or_add_authors
        >>> from kitab.db.db_credentials import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
        >>> from kitab.db.sql_interactions import SqlHandler
        >>> db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        >>> _get_or_add_authors(db, authors=["Henry James"])
    
    Parameters:
        db (SqlHandler): The database handler.
        authors (list[str]): A list of authors.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        list[int]: A list of author IDs.
    """
    author_table = db.get_table("author")
    
    author_ids = []
    cur_index = max(author_table["author_id"]+1)
    to_insert = []
    
    for author in authors:
        if author in author_table["full_name"].values:
            author_id = author_table[author_table["full_name"] == author]["author_id"].values[0]
        else:
            author_id = cur_index
            cur_index += 1
            to_insert.append({"author_id": author_id, "full_name": author})
        author_ids.append(author_id)
    
    # Insert the records
    db.insert_records("author", to_insert)
    if verbose:
        logger.info("New authors added.")
    
    return author_ids

def get_authors(ISBNs: list[str], verbose: bool = False) -> dict[str:list]:
    """
    Get the authors for the given list of ISBNs.
    
    Examples:
        >>> from kitab.db.functions import get_authors
        >>> get_authors(ISBNs=["1442942355", "1613720211"])
    
    Parameters:
        ISBNs (list[str]): A list of ISBNs.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        dict[str:list]: A dictionary containing the authors for each ISBN.
    """
    # Open connection to the database
    db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    if verbose:
        logger.info("Database connection opened.")
    
    # Retrieve the authors of the books with the given ISBNs
    authors = db.get_table("bookauthor", conditions={"isbn": ISBNs})
    author_ids = authors["author_id"].tolist()
    
    author_table = db.get_table("author", conditions={"author_id": author_ids})
    
    # Initialize dictionary to store authors for each ISBN
    isbn_authors = {isbn: [] for isbn in ISBNs}
    
    # Populate dictionary with authors
    for _, row in authors.iterrows():
        isbn = row["isbn"]
        author_id = row["author_id"]
        author_name = author_table.loc[author_table['author_id'] == author_id, 'full_name'].iloc[0]
        isbn_authors[isbn].append(author_name)
    
    # Return the dictionary of lists
    return isbn_authors

def get_genres(ISBNs: list[str], verbose: bool = False) -> dict[str:list]:
    """
    Get the genres for the given list of ISBNs.
    
    Examples:
        >>> from kitab.db.functions import get_genres
        >>> get_genres(ISBNs=["1442942355", "1613720211"])
    
    Parameters:
        ISBNs (list[str]): A list of ISBNs.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        dict[str:list]: A dictionary containing the genres for each ISBN.
    """
    # Open connection to the database
    db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    if verbose:
        logger.info("Database connection opened.")

    # Retrieve the genres of the books with the given ISBNs
    genres = db.get_table("bookgenre", conditions={"isbn": ISBNs})
    genre_ids = genres["genre_id"].tolist()
    
    genre_table = db.get_table("genre", conditions={"genre_id": genre_ids})
    
    # Initialize dictionary to store genres for each ISBN
    isbn_genres = {isbn: [] for isbn in ISBNs}
    
    # Populate dictionary with genres
    for _, row in genres.iterrows():
        isbn = row["isbn"]
        genre_id = row["genre_id"]
        genre_name = genre_table.loc[genre_table['genre_id'] == genre_id, 'genre'].iloc[0]
        isbn_genres[isbn].append(genre_name)
    
    # Return the dictionary of lists
    return isbn_genres


def get_history_by_recommendation_isbn(recommendation_isbn: str, verbose: bool = False) -> dict:
    """
    Get the history of recommendations for a book with the given ISBN.
    
    Examples:
        >>> from kitab.db.functions import get_history_by_recommendation_isbn
        >>> get_history_by_recommendation_isbn(recommendation_isbn="1442942355")
    
    Parameters:
        recommendation_isbn (str): The ISBN of the recommended book.

    Returns:
        dict: A dictionary containing the history of recommendations for the book.
    """
    # Open connection to the database
    db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    if verbose:
        logger.info("Database connection opened.")
    
    # Retrieve the history of books that have been recommended
    history = db.get_table("history", conditions={"recommendation_ISBN": recommendation_isbn})
    
    # Return the history
    return history.drop(columns="log_id").to_dict(orient='records')


def add_recommendation_log(description: str, recommendation_isbn: str, successful: bool, verbose: bool = False) -> bool:
    """
    Adds a recommendation log to the history table.
    
    Examples:
        >>> from kitab.db.functions import add_recommendation_log
        >>> add_recommendation_log(description="In a masterful blend of psychological intrigue and spectral disturbances, this novel unfurls the complex life of Clara. Her internal struggles are mirrored by eerie, inexplicable occurrences, weaving a tale that is both deeply personal and chillingly atmospheric, offering an unparalleled exploration of the human psyche shadowed by the paranormal.", recommendation_isbn="1442942355", successful=True)
    
    Parameters:
        description (str): The description of the recommendation.
        recommendation_isbn (str): The ISBN of the recommended book.
        successful (bool): Whether the recommendation was successful or not.
        verbose (bool): Whether to print verbose output. Defaults to False.

    Returns:
        bool: True if the recommendation log was successfully added, False otherwise.
    """
    try:
        # Open connection to the database
        db = SqlHandler(DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        if verbose:
            logger.info("Database connection opened.")
        
        # Insert the recommendation log into the history table
        db.insert_records("history", [{"description": description, "recommendation_isbn": recommendation_isbn, "successful": successful}])
    
        return True
    except Exception as e:
        logger.error("Error adding recommendation log.")
        return False