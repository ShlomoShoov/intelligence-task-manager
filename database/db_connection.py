"""
this file responsible for the connection and define 
the data base and its tables


"""

import mysql.connector 

class ConnectionDB:
    def __init__(self):
        """
         define all of the params that the class needs. 
         (connection details and tables and database details)
        
        """


        self.database = 'Intelligence_db'
        self.config = {
                    'host':'127.0.0.1',
                    'user':'root',
                    'password':'1234',
                    'port':3306,
                    }
        self.tables = [
                {
                            'name':'agents',
                            'schema':"""
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL,
                        specialty VARCHAR(100) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        completed_missions INT DEFAULT 0,
                        failed_missions INT DEFAULT 0,
                        agent_rank ENUM('Junior','Senior','Commander') NOT NULL
                        """},
                 {
                   'name':'missions',
                   'schema':"""
                            id INT PRIMARY KEY AUTO_INCREMENT,
                            title VARCHAR(50) NOT NULL,
                            description	TEXT NOT NULL,
                            location VARCHAR(255) NOT NULL,
                            difficulty INT NOT NULL,
                            importance INT NOT NULL,
                            status VARCHAR(50) DEFAULT 'NEW',
                            risk_level VARCHAR(50) NOT NULL,
                            assigned_agent_id INT
                            """}
                
        ]

    def get_connection(self,to_data_base:bool=True)->mysql.connector:
        """
        create and return a connection
        if to_data_base = False it will connect but not to the data base
        """
        config = self.config
        if to_data_base:
            config['database'] = self.database

        connect = mysql.connector.connect(**config)
        return connect
    
    def create_database(self):
        """
        create a database if not exists
        """
        query = f"CREATE DATABASE IF NOT EXISTS {self.database}"
        with self.get_connection(to_data_base=False) as conn:
            with conn.cursor() as crs:
                crs.execute(query)

    def create_tables(self):
        """
        create the tables in `self.tables` 
        """
        with self.get_connection() as conn:
            with conn.cursor() as crs:
                for table in self.tables:
                    query = f"""
                    CREATE TABLE IF NOT EXISTS {table['name']}
                    ({table['schema']})
                    """
                    crs.execute(query)

if __name__ == "__main__":
    c = ConnectionDB()

    c.get_connection()
    c.create_database()
    c.create_tables()

    
        