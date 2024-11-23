from unittest import TestCase, main
import sqlite3
import os
from src.database import Database


class TestDatabase(TestCase):
    def setUp(self):
        self.test_db = "test_database.db"
        self.db = Database(self.test_db)

    def tearDown(self):
        self.db.close()
        os.remove(self.test_db)

    def test_create_connection(self):
        self.assertIsInstance(self.db.connection, sqlite3.Connection)

    def test_initialize_database(self):
        self.db.initialize_database()
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='links'"
        )
        self.assertIsNotNone(cursor.fetchone())

    def test_insert_link(self):
        self.db.initialize_database()
        test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
        test_depth = 1
        self.db.insert_link(test_url, test_depth)

        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM links WHERE url=?", (test_url,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], test_url)
        self.assertEqual(result[1], test_depth)

    def test_get_links(self):
        self.db.initialize_database()
        test_urls = [
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://en.wikipedia.org/wiki/Java_(programming_language)",
        ]
        for url in test_urls:
            self.db.insert_link(url, 1)

        links = self.db.get_links()
        self.assertEqual(len(links), len(test_urls))
        for link in links:
            self.assertIn(link[0], test_urls)

    def test_insert_multiple_links(self):
        self.db.initialize_database()
        test_urls = [
            ("https://en.wikipedia.org/wiki/Python", 1),
            ("https://en.wikipedia.org/wiki/Java", 2),
            ("https://en.wikipedia.org/wiki/C++", 3),
        ]
        for url, depth in test_urls:
            self.db.insert_link(url, depth)

        cursor = self.db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM links")
        count = cursor.fetchone()[0]
        self.assertEqual(count, len(test_urls))

    def test_get_links_empty_database(self):
        self.db.initialize_database()
        links = self.db.get_links()
        self.assertEqual(len(links), 0)

    def test_insert_duplicate_link(self):
        self.db.initialize_database()
        test_url = "https://en.wikipedia.org/wiki/Python"
        self.db.insert_link(test_url, 1)
        self.db.insert_link(test_url, 2)

        cursor = self.db.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM links")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

        cursor.execute("SELECT depth FROM links WHERE url=?", (test_url,))
        depth = cursor.fetchone()[0]
        self.assertEqual(depth, 1)


if __name__ == "__main__":
    main()
