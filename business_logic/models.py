"""
this file define the data models, for validation
"""

from pydantic import BaseModel

valid_ranks = ["Junior" , "Senior" , "Commander" ]


class AgentModel(BaseModel):
    name: str
    agent_rank: str
    specialty: str

class MissionModel(BaseModel):
    title: str
    description: str
    location: str 
    difficulty: int 
    importance: int
