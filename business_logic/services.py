"""
This file is the middle man between the routers
to the database.
it response for validation, error handling and
transforming the data
"""
from database.agent_db import AgentDB
from database.mission_db import MissionDB
import business_logic.exceptions as exceptions
import business_logic.models as models
import business_logic.validations as validations


class Services:
    """
    this class allow CRUD with the data base 
    in a safe way, it preform validations and
    trowing the right errors
    """

    def __init__(self):
        self._agent_db = AgentDB()
        self._mission_db = MissionDB()
        self._success_msg = 'success'

    #  agent methods:

    def create_agent(self, data: models.AgentModel) -> dict:
        """
        raise:
            RankInvalid
        """
        data.agent_rank = data.agent_rank.title()
        if not validations.valid_agent_rank(rank=data.agent_rank):
            raise exceptions.RankInvalid
        new_data = self._agent_db.create_agent(data=data.model_dump())
        return {"message": "Agent Created", "data": new_data}

    def get_agents(self):
        return self._agent_db.get_all_agents()

    def get_agent_by_id(self, id: int):
        agent = self._agent_db.get_agent_by_id(id=id)
        if agent is None:
            raise exceptions.AgentNotExists
        return agent

    def update_agent(self, id: int, data: models.AgentModel) -> dict:
        data.agent_rank = data.agent_rank.title()
        if not validations.valid_agent_rank(rank=data.agent_rank):
            raise exceptions.RankInvalid
        response = self._agent_db.update_agent(id=id, data=data.model_dump())
        if response == self._agent_db.failed_msg:
            raise exceptions.AgentNotExists
        return {"massage": f"{id} updated!"}

    def deactivate_agent(self, id: int):
        response = self._agent_db.deactivate_agent(id=id)
        if response == self._agent_db.failed_msg:
            raise exceptions.AgentNotExists
        return {"massage": f"{id} deactivate!"}

    def get_agent_performance(self, id: int) -> dict:
        response = self._agent_db.get_agent_performance(id=id)
        if response is None:
            raise exceptions.AgentNotExists
        return response

    # missions route
    def _calc_risk_level(self, difficulty, importance):
        return difficulty*2 + importance
    
    def _get_risk_level(self,risk_number:int):
        return "CRITICAL" if risk_number >= 25 else "HIGH" if risk_number >= 18 else "MEDIUM" if risk_number >= 10 else "LOW"

    def create_mission(self, data: models.MissionModel):
        if not validations.valid_difficulty(difficulty=data.difficulty):
            raise exceptions.InvalidDifficulty
        if not validations.valid_importance(importance=data.importance):
            raise exceptions.InvalidImportance
        risk_level = self._get_risk_level(self._calc_risk_level(difficulty=data.difficulty, importance=data.importance))
        data = data.model_dump()
        data['risk_level'] = risk_level
        response = self._mission_db.create_mission(data)
        return {"massage":"Mission created", "data":response}
    
    def get_missions(self)->list[dict]:
        return self._mission_db.get_all_missions()

    def get_mission_by_id(self, id:int):
        response = self._mission_db.get_mission_by_id(id=id)
        if response is None:
            raise exceptions.MissionNotExists
        return response