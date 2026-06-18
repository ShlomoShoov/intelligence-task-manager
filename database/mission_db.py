"""
This file is responsible to all of the actions that connect with
tha table `missions`
"""
from database.db_connection import ConnectionDB

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
        self.table_name = 'missions'
        # this what the create, update and delete function return if everything updated
        self.succeeded_msg = 'succeeded'
        # this what the create, update and delete function return if nothing update (row was not found)
        self.failed_msg = 'failed'
        self.no_update = 'no_update'

        self._open_status = [ 'ASSIGNED' , 'IN_PROGRESS']

    
    def _is_id_exists(self,cursor, id:int):
        query = f"SELECT * FROM {self.table_name} WHERE id=%s"
        cursor.execute(query, (id,))
        response = cursor.fetchone()
        return response is not None

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
                if not self._is_id_exists(cursor=crs, id=id):
                    return self.failed_msg
                crs.execute(query, values)
                has_update = crs.rowcount > 0
                conn.commit()

        if has_update:
            return self.succeeded_msg
        else:
            return self.no_update
        

    def assign_mission(self, m_id:int, a_id:int)->str:
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
        new_data = {'status':status}
        return self._update_mission(id=id,data=new_data)
    

    
    def _count_all(self):
        """
        helper function, return how many rows
        """
        key = 'cnt'
        query = f"""
                SELECT COUNT(*)  AS {key} FROM {self.table_name}
                """
        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                crs.execute(query)
                data = crs.fetchone()
        return data[key]


    def _count(self,key:str ,values:list):
        """
        helper function
        count the rows with specific key IN [values]
        """
        cnt_key = 'cnt'
        values_template = ",".join(["%s"]*len(values))
        query = f"""
                SELECT COUNT(*)  AS {cnt_key} FROM {self.table_name}
                WHERE {key} IN({values_template})
                """
        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                
                crs.execute(query,values)

                data = crs.fetchone()
        return data[cnt_key]
    
    def count_missions_by_agents(self,id)->int:
        """
        count how many missions have specific agent
        """
        return self._count(key="assigned_agent_id", values=[id])
        
        
    def count_all_missions(self)->int:
        """
        count all the missions 
        """
        return self._count_all()
    
    def count_by_status(self, status)->int:
        """
        return how many mission with given status
        """
        return self._count(key='status', value=[status])
    
    def count_open_missions(self)->int:
        return self._count(key="status", values=self._open_status)
    
    def count_critical_missions(self)->int:
        return self._count(key="risk_level", values=['CRITICAL'])

if __name__ == "__main__":
    m = MissionDB()
    data = {"title":"pink moon", "description":"we will took this on night",
            "location":"tel aviv", "difficulty":"7", "risk_level":"critical", 'importance':3}
    # m.create_mission(data)
    print(m.get_all_missions())
    print(m.get_mission_by_id(id=2))
    #print(m.assign_mission(m_id=2,a_id=12))
    print(m.count_all_missions())
    print(m.count_critical_missions())
    print(m.update_mission_status(id=2,status="CANCELLED"))
    print(m.count_open_missions())
