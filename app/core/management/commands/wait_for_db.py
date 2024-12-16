"""
django command to wait for the database to be available
"""
from django.core.management.base import BaseCommand

import time

from django.db.utils import  OperationalError

from psycopg2 import OperationalError as psycopg2Error

from django.conf import settings

from django.db import connections

class Command(BaseCommand):
    """ Django command to wait for database."""
    def handle(self, *args, **options):
        """entrypoint for command"""
        self.stdout.write('Waiting for database')
        db_up=False
        while db_up is False:
            try:
                connection = connections['default']
                connection.ensure_connection()
                db_up=True
            except(OperationalError, psycopg2Error):
                self.stdout.write(self.style.FAIL('Database is un available waiting for 1 second'))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('database is available'))
          
            
        
        