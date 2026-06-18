"""
this file init the project in the first time
"""

from database.db_connection import ConnectionDB


connection = ConnectionDB()
def init():
    """
    call this function to init the project for the first time
    """
    connection.create_database()
    connection.create_tables()