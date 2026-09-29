"""Basic service tests using a temporary SQLite database."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sqlite3

from library import database, services

class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "test.db"
        self.patcher = patch.object(database, "DB_PATH", self.db)
        self.patcher.start()
        database.initialize()

    def tearDown(self):
        self.patcher.stop()
        self.tmp.cleanup()

    def test_issue_and_return_updates_inventory(self):
        book = services.add_book("Clean Code", "Robert Martin", "ISBN-1", 1)
        member = services.add_member("Asha", "asha@example.com")
        loan = services.issue_book(book, member)
        self.assertEqual(services.list_books()[0]["available_copies"], 0)
        services.return_book(loan)
        self.assertEqual(services.list_books()[0]["available_copies"], 1)

    def test_cannot_issue_unavailable_book(self):
        book = services.add_book("Python", "Guido", "ISBN-2", 1)
        member = services.add_member("Asha", "asha@example.com")
        services.issue_book(book, member)
        with self.assertRaises(ValueError):
            services.issue_book(book, member)

    def test_required_fields(self):
        with self.assertRaises(ValueError):
            services.add_book("", "Author", "", 1)

if __name__ == "__main__":
    unittest.main()
