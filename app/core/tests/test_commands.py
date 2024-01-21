"""
Test custom Django management commands.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# NOTE:Command.check method here is present in the BaseCommands module
# NOTE:the patch decorator used to mock the behaviour of the db
# NOTE:data inside '' is the file path.

# NOTE:here the check method from the BaseCommand class is mocked to simulate the response.
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""
    # NOTE:patched_check obj is the magic mock object of BaseCommand-->check().
        # here we are able to customize the mock object behaviour.

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        # NOTE:when check is called in TEST (here) return True.
        patched_check.return_value = True
        
        # NOTE:TESTs if the db is ready and if the command 'wait_for_db' exists.
        call_command('wait_for_db')
        
        # NOTE:Ensures that we are calling the correct mock obj for the correct db.
        patched_check.assert_called_once_with(database = ['default']) 
    

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""

        # NOTE:This how mocking is performed for OperationalErrors from psycopg2 and normal Operationalerrors
            # here need to raise exception if the database was not ready.
            # thus using .side_effect 
                # The first 2 times test raises Psycopg2Error
                # The nxt 3 times raise OperationalError
                # Then return True 
     
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + \
                                    [True]
        
        call_command('wait_for_db')
        # NOTE:To ensure that the call count of mocked check method is correct (2 + 3 + 1) ^
        self.assertEqual(patched_check.call_count, 6)
        # NOTE:Same as the 'assert_called_once_with' in the above function but this will be called multiple times.
        patched_check.assert_called_with(database = ['default'])