import unittest
import sqlite3
import os
from src.database import create_connection, initialize_database, insert_link, get_links


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_database.db"
        self.conn = create_connection(self.test_db)

    def tearDown(self):
        self.conn.close()
        os.remove(self.test_db)

    def test_create_connection(self):
        self.assertIsInstance(self.conn, sqlite3.Connection)

    def test_initialize_database(self):
        initialize_database(self.conn)
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='links'"
        )
        self.assertIsNotNone(cursor.fetchone())

    def test_insert_link(self):
        initialize_database(self.conn)
        test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        test_depth = 1
        insert_link(self.conn, test_url, test_depth)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM links WHERE url=?", (test_url,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_url)
        self.assertEqual(result[1], test_depth)

    def test_get_links(self):
        initialize_database(self.conn)
        test_urls = [
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://en.wikipedia.org/wiki/Java_(programming_language)",
        ]
        for url in test_urls:
            insert_link(self.conn, url, 1)

        links = get_links(self.conn)
        self.assertEqual(set(test_urls), links)

    def test_insert_multiple_links(self):
        initialize_database(self.conn)
        test_urls = [
            ("https://en.wikipedia.org/wiki/Python", 1),
            ("https://en.wikipedia.org/wiki/Java", 2),
            ("https://en.wikipedia.org/wiki/C++", 3),
        ]
        for url, depth in test_urls:
            insert_link(self.conn, url, depth)

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM links")
        count = cursor.fetchone()[0]
        self.assertEqual(count, len(test_urls))

    def test_get_links_empty_database(self):
        initialize_database(self.conn)
        links = get_links(self.conn)
        self.assertEqual(len(links), 0)

    def test_insert_duplicate_link(self):
        initialize_database(self.conn)
        test_url = "https://en.wikipedia.org/wiki/Python"
        insert_link(self.conn, test_url, 1)
        insert_link(self.conn, test_url, 2)  # Attempt to insert duplicate

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM links WHERE url=?", (test_url,))
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)  # Should still be only one entry


if __name__ == "__main__":
    unittest.main()
