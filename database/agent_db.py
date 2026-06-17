"""
this file is manage all of the CRUD commands that
connect with the table  `agents`

"""
from database.db_connection import ConnectionDB
from database.mission_db import MissionDB

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
        self._connect = ConnectionDB().get_connection
        self.table_name = 'agents'
        # this what the create, update and delete function return if everything updated
        self.succeeded_msg = 'succeeded'
        # this what the create, update and delete function return if nothing update (row was not found)
        self.failed_msg = 'failed'
        self.mission_table_manager = MissionDB()

    def create_agent(self, data: dict) -> dict:
        """
        create (save to database) an agent and return its object 
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
        return self.get_agent_by_id(id=new_id)

    def get_all_agents(self) -> list[dict]:
        """
        return all of the agents dicts
        """
        query = f"SELECT * FROM {self.table_name}"

        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                crs.execute(query)
                data = crs.fetchall()
        return data

    def get_agent_by_id(self, id: int) -> dict | None:
        """
        return an agent dict by id, if not exists return None
        """
        query = f"SELECT * FROM {self.table_name} WHERE id=%s"

        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                crs.execute(query, (id,))
                data = crs.fetchone()
        return data

    def update_agent(self, id: int, data: dict) -> str:
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
        
    def deactivate_agent(self,id:int)->str:
        """
        update agent status to False
        return 
        str: self.succeeded_msg if all went well and self.failed_msg 
            if no change has happened (id not exists).
        """
        new_data = {'is_active':False}
        return self.update_agent(id=id,data=new_data)
    
    def _increment_value(self, id:int, key:str)->str:
        """
        helper function to increment a int value by 1
        return:
        str: self.succeeded_msg if all went well and self.failed_msg 
            if no change has happened (id not exists).
        """
        query = f"""
                UPDATE {self.table_name} SET {key} = {key} +1 WHERE id = %s 
                """
        with self._connect() as conn:
            with conn.cursor() as crs:
                crs.execute(query, (id,))
                has_update = crs.rowcount > 0
                conn.commit()

        if has_update:
            return self.succeeded_msg
        else:
            return self.failed_msg
        

    def increment_completed(self, id:int)->str:
        """
        update completed_missions += 1
        return:
        str: self.succeeded_msg if all went well and self.failed_msg 
            if no change has happened (id not exists).

        """
        return self._increment_value(id=id,key='completed_missions')
    
    def increment_failed(self,id:int)->str: 
        """
        update  failed_missions += 1
        return:
        str: self.succeeded_msg if all went well and self.failed_msg 
            if no change has happened (id not exists).
        
        """
        return self._increment_value(id=id,key='failed_missions')
    
    
        
    def get_agent_performance(self, id:int)->dict|None:
        """
        return 
        dict (if agent exists)
        {
            total:
            the agent total missions
                 (***note*** a responsible problem, if we want to get all of the missions of an agent, 
                 we must connect with the table of `missions` , its better to do it a third class that response for business logic
                 and can connect with the two classes or adding to the agent a field of `total_missions`)
            failed:
            the failed missions 
            completed: 
                the completed missions 
            success_rate: (completed/total) * 100 
                    (*note* logic problem, if we use total to calculate the all missions, even the ones the agent did not finish, we will treat them as 'failed', I'll follow the instructions, but it's better to calc (completed/(completed+failed)) * 100 )
          }
        None :  if agent not exists  
        """
        agent_data = self.get_agent_by_id(id=id)
        if agent_data is None:
            return None
        failed = agent_data['failed_missions']
        completed = agent_data['completed_missions']
        total = self.mission_table_manager.count_missions_by_agents(id=id)
        success_rate = 0 if total == 0 else (completed / total)*100
        return {'failed':failed,
                'completed':completed,
                'total':total,
                "success_rate":success_rate}

    def count_active_agents(self)->int:
        """
        return the number of the active agents
        """
        key = 'cnt'
        query = f"""
                SELECT COUNT(*) as {key} FROM {self.table_name} 
                WHERE is_active=True
                """
        
        with self._connect() as conn:
            with conn.cursor(dictionary=True) as crs:
                crs.execute(query)
                data = crs.fetchone()
        return data[key]
        



if __name__ == "__main__":
    a = AgentDB()
    # a.create_agent({
    #    'name':'dan','specialty':'something', 'agent_rank':'Junior'})
    print(len(a.get_all_agents()))
    print(a.get_agent_by_id(id=8))
    print(a.update_agent(id=3, data={'name':'dani','specialty':'something--', 'agent_rank':'Senior'}))
    print(a.deactivate_agent(id=3))
    print(a.increment_completed(id=3))
    print(a.increment_failed(id=4))
    print(a.count_active_agents())
    print(a.get_agent_performance(3))