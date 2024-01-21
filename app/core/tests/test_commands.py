"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


## noqa NOTE:Command.check method here is present in the BaseCommands module
## noqa NOTE:the patch decorator used to mock the behaviour of the db
## noqa NOTE:data inside '' is the file path.

## noqa NOTE:here the check method from the BaseCommand class is mocked to simulate the response.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""
    ## noqa NOTE:patched_check obj is the magic mock object of BaseCommand-->check().
    ## noqa ----here we are able to customize the mock object behaviour.

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        ## noqa NOTE:when check is called in TEST (here) return True.
        patched_check.return_value = True
        ## noqa NOTE:TESTs if the db is ready and if the command 'wait_for_db' exists.
        call_command('wait_for_db')
        ## noqa NOTE:Ensures that we are calling the correct mock obj for the correct db.
        patched_check.assert_called_once_with(databases=['default'])

    ## noqa NOTE:To override the sleep timer of sleep in between db checks.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""

        ## noqa NOTE:This how mocking is performed for OperationalErrors from psycopg2 and normal
        ## noqaOperationalerrors raises when db is not ready.
        ## noqa --here need to raise exception if the database was not ready.
        ## noqa --thus using .side_effect 
        ## noqa ----The first 2 times test raises Psycopg2Error
        ## noqa ----The nxt 3 times raise OperationalError
        ## noqa ----Then return True 
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + \
                                    [True]
        call_command('wait_for_db')
        ## noqa NOTE:To ensure that the call count of mocked check method is correct (2 + 3 + 1) ^
        self.assertEqual(patched_check.call_count, 6)
        ## noqa NOTE:Same as the 'assert_called_once_with' in the above function but this will be called multiple times.
        patched_check.assert_called_with(databases=['default'])
