from fastapi import APIRouter, HTTPException
from logging import getLogger

from business_logic.services import Services
import business_logic.exceptions as exceptions
import business_logic.models as models

logger = getLogger()
router = APIRouter(prefix='/missions')
service = Services()

@router.post("")
def create_mission(data:models.MissionModel):
    try:
        response = service.create_mission(data=data)
        return response
    except exceptions.InvalidImportance:
        raise HTTPException(status_code=400, detail={"massage":f"failed, Importance must be between 1-10"})

    except exceptions.InvalidDifficulty:
        raise HTTPException(status_code=400, detail={"massage":f"failed, Difficulty must be between 1-10"})

@router.get("")
def get_all_missions():
    return service.get_missions()

@router.get("/{id}")
def get_mission_by_id(id:int):
    try:
        return service.get_mission_by_id(id=id)
    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={"massage":f"failed, {id} not exists"})
        
