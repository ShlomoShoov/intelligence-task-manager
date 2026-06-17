"""
this file is manage all of the CRUD commands that
connect with the table  `agents`

"""
from database.db_connection import ConnectionDB

class AgentDB:
    """
     manage all of the action needed with the table `agents`
     *note* this class DOES NOT responsible for Validation and Error handling
    """
    def __init__(self):
        """
        define all of the fields needs for managing this class methods 
        (table name, connection function and more fields)
        """
        self.connect = ConnectionDB().get_connection
        self.table_name = 'agents'
        self.succeeded_msg = 'succeeded' # this what the create, update and delete function return if everything updated
        self.failed_msg =  'failed' # this what the create, update and delete function return if nothing update (row was not found)

    def create_agent(self,data:dict)->dict:
        """
        create (save to database) an agent and return its object 
        [its data dict as it's in the data base]
        """
        keys = ','.join(list(data.keys()))
        values = list(data.values())

        query = """
                
                """

        with self.connect() as conn:
            with conn.cursor() as crs:
                pass