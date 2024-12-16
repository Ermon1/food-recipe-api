from unittest.mock import patch
from psycopg2 import OperationalError as psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase  # Use TestCase instead of SimpleTestCase
from django.conf import settings

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(TestCase):  # Change to TestCase to allow database interaction
    """Test custom Django management commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for the database when it's ready."""
        patched_check.return_value = True
        
        call_command('wait_for_db')
        
        # Assert that check was called once with the 'default' database
        patched_check.assert_called_once_with(database=settings.DATABASES['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for the database when getting OperationalError."""
        
        # Simulate multiple errors followed by success
        patched_check.side_effect = [psycopg2Error] * 2 + [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')
        
        # Assert that check was called 6 times (2 psycopg2Error, 3 OperationalError, 1 success)
        self.assertEqual(patched_check.call_count, 6)
        
        # Assert that the final call was with the 'default' database
        patched_check.assert_called_with(database=settings.DATABASES['default'])
