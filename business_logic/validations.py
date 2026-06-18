"""
this file contain all the validation needed

"""
import business_logic.models as models

def valid_agent_rank(rank:str):
    return rank in models.valid_ranks

def valid_difficulty(difficulty:int):
    return 1 <= difficulty <= 10

def valid_importance(importance:int):
    return  1 <= importance <= 10
