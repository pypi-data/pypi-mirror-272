import unittest

from fastapi import FastAPI

from yamlsql.examples.potato import app


class TestExample(unittest.TestCase):
    def test_example(self):
        self.assertIsInstance(app.app, FastAPI)
        self.assertIsNotNone(app.app)
