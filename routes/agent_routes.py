from fastapi import APIRouter, HTTPException

from business_logic.services import Services
import business_logic.exceptions as exceptions
import business_logic.models as models

router = APIRouter(prefix='/agents')
service = Services()


@router.post('', status_code=201)
def crate_agent(data: models.AgentModel):
    try:
        return service.create_agent(data)

    except exceptions.RankInvalid:
        raise HTTPException(status_code=400, detail={
                            "message": f"error: rank is not in {models.valid_ranks}"})


@router.get("")
def get_agents():
    return service.get_agents()


@router.get("/{id}")
def get_by_id(id: int):
    try:
        return service.get_agent_by_id(id=id)
    except exceptions.AgentNotExists:
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {id}"})


@router.post("/{id}")
def update_agent(id: int, new_data: models.AgentModel):
    try:
        return service.update_agent(id=id, data=new_data)
    except exceptions.RankInvalid:
        raise HTTPException(status_code=400, detail={
                            "message": f"error: rank is not in {models.valid_ranks}"})
    except exceptions.AgentNotExists:
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {id}"})
    

@router.put("/{id}/deactivate")
def deactivate_id(id:int):
    pass