import sqlite3


def create_connection(db_path: str) -> sqlite3.Connection:
    """Create a connection to SQLite database."""
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise


def initialize_database(connection: sqlite3.Connection) -> None:
    """Initialize database schema with links table."""
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS links (
            url TEXT PRIMARY KEY,
            depth INTEGER,
            UNIQUE(url)
        )
    """
    )
    connection.commit()


def insert_link(connection: sqlite3.Connection, url: str, depth: int) -> None:
    """Insert a unique link into the database."""
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO links (url, depth) VALUES (?, ?)", (url, depth)
        )
        connection.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicate links


def get_links(connection: sqlite3.Connection) -> set[str]:
    """Retrieve all existing links from the database."""
    cursor = connection.cursor()
    cursor.execute("SELECT url FROM links")
    return {row[0] for row in cursor.fetchall()}
