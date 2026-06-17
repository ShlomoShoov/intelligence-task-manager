"""
This file is responsible to all of the actions that connect with
tha table `missions`
"""
from db_connection import ConnectionDB

class MissionDB:
    """
    **MissionDB**
    manage all of the action needed with the table `missions`
    *note* this class DOES NOT responsible
            for Validation and Error handling 
    """
    def __init__(self):
        """
         define all of the fields needs for managing this class methods 
         (table name, connection function, and more)
        """
        self._connect = ConnectionDB().get_connection
        self.table_name = 'agents'
        # this what the create, update and delete function return if everything updated
        self.succeeded_msg = 'succeeded'
        # this what the create, update and delete function return if nothing update (row was not found)
        self.failed_msg = 'failed'

        

    def create_mission(self, data:dict)->dict|None:
        """
        create (save to database) an mission and return its object 
        [its data dict as it's in the data base]
        """
        keys = ','.join(list(data.keys()))
        values = list(data.values())
        values_sample = ",".join(['%s']*len(values))

        query = f"""
                INSERT INTO {self.table_name} ({keys})
                VALUES ({values_sample})
                """

        with self._connect() as conn:
            with conn.cursor() as crs:
                crs.execute(query, values)
                new_id = crs.lastrowid
                conn.commit()

        return self.get_mission_by_id(id=new_id)
    
    def get_all_missions(self)->list[dict]:
        """
        return list of the all missions dicts
        """
        query = f"SELECT * FROM {self.table_name}"

        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                crs.execute(query)
                data = crs.fetchall()
        return data
    
    def get_mission_by_id(self, id: int) -> dict | None:
        """
        return an mission dict by id, if not exists return None
        """
        query = f"SELECT * FROM {self.table_name} WHERE id=%s"

        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                crs.execute(query, (id,))
                data = crs.fetchone()
        return data
    
    def _update_mission(self, id: int, data: dict) -> str:
        """
        get id and a dict of keys and values to update and update the data
        (all data available to change except id).
        return 
        str: self.succeeded_msg if all went well and self.failed_msg 
            if no change has happened (id not exists).
        """
        keys = ','.join([f"{key} = %s" for key in data.keys()])
        values = list(data.values()) + [id]

        query = f"""
                UPDATE {self.table_name} SET {keys}
                WHERE id = %s
                """

        with self._connect() as conn:
            with conn.cursor() as crs:
                crs.execute(query, values)
                has_update = crs.rowcount > 0
                conn.commit()

        if has_update:
            return self.succeeded_msg
        else:
            return self.failed_msg
        

    def assign_mission(self, m_id, a_id)->str:
        """
        update the assigned_agent_id of m_id to a_id 
            return 
            self.succeeded if all went well and self.failed if no change has happened (id not exists (m_id)). 
        """
        new_data = {'assigned_agent_id':a_id}
        return self._update_mission(id=m_id,data=new_data)
    
    def update_mission_status(self, id, status)->str: 
        """
        update the mission status by id
        return self.succeeded if all went well and self.failed if no change has happened (id not exists)
        """
        