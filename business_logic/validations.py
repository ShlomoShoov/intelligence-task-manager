"""
this file contain all the validation needed

"""
import business_logic.models as models
import business_logic.exceptions as exceptions

def valid_agent_rank(rank:str):
    return rank in models.valid_ranks

def valid_difficulty(difficulty:int):
    return 1 <= difficulty <= 10

def valid_importance(importance:int):
    return  1 <= importance <= 10

def valid_assign_mission(mission:dict,agent:dict):
    if not mission['status'] == "NEW":
        raise exceptions.MissionNotNew
    if agent['is_active'] == False:
        raise exceptions.InactiveAgent
    if mission['risk_level'] == 'CRITICAL':
        if agent['agent_rank'] == "Senior":
            raise exceptions.CriticalForSenior
        if agent['agent_rank'] == "Junior":
            raise exceptions.CriticalForJunior
        
def valid_complete_mission(mission:dict):
    if not mission["status"] == "IN_PROGRESS":
        raise exceptions.CompleteMissionNotInProgress
    
def valid_start_mission(mission:dict):
    if not  mission["status"] == "ASSIGNED":
        raise exceptions.StartUnassignedMissionError
    
def valid_cancel_mission(mission:dict):
    if not mission["status"] in ["ASSIGNED", "NEW"]:
        raise exceptions.CancelCompleteMission
        

