"""
this file contain all the validation needed

"""
import business_logic.models as models

def valid_agent_rank(rank:str):
    return rank in models.valid_ranks 