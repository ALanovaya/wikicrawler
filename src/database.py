import sqlite3


class Database:
    def __init__(self, db_path: str):
        self.connection = self.create_connection(db_path)

    def create_connection(self, db_path: str) -> sqlite3.Connection:
        """Create a connection to SQLite database."""
        try:
            connection = sqlite3.connect(db_path)
            return connection
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def initialize_database(self) -> None:
        """Initialize database schema with links table."""
        cursor = self.connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                url TEXT PRIMARY KEY,
                depth INTEGER,
                UNIQUE(url)
            )
            """
        )

    def insert_link(self, url: str, depth: int) -> None:
        """Insert a link into the database."""
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO links (url, depth) VALUES (?, ?)", (url, depth)
        )
        self.connection.commit()

    def get_links(self) -> list:
        """Retrieve all links from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT url FROM links")
        return cursor.fetchall()

    def close(self) -> None:
        """Close the database connection."""
        self.connection.close()
