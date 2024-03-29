# -*- coding: utf-8 -*-
from flask.ext.testing import TestCase
from clubflask.settings import TestConfig
from clubflask.app import create_app
from clubflask.database import db


class DbTestCase(TestCase):
    """Base TestCase for tests that require a database."""

    def create_app(self):
        app = create_app(TestConfig)
        with app.app_context():
            db.create_all()
        return app

    def tearDown(self):
        db.session.remove()
        db.drop_all()