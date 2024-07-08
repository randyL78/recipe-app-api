"""
Django command to pause execution until database is available
"""

from django.core.management.base import BaseCommand

import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for database"""
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False

        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                message = 'Database not available. Waiting 1 second...'
                self.stdout.write(self.style.ERROR(message))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
