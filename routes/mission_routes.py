from fastapi import APIRouter, HTTPException
from logging import getLogger

from business_logic.services import Services
import business_logic.exceptions as exceptions
import business_logic.models as models

logger = getLogger()
router = APIRouter(prefix='/missions')
service = Services()


@router.post("", status_code=201)
def create_mission(data: models.MissionModel):
    try:
        response = service.create_mission(data=data)
        return response
    except exceptions.InvalidImportance:
        raise HTTPException(status_code=400, detail={
                            "massage": f"failed, Importance must be between 1-10"})

    except exceptions.InvalidDifficulty:
        raise HTTPException(status_code=400, detail={
                            "massage": f"failed, Difficulty must be between 1-10"})


@router.get("")
def get_all_missions():
    return service.get_missions()


@router.get("/{id}")
def get_mission_by_id(id: int):
    try:
        return service.get_mission_by_id(id=id)
    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={
                            "massage": f"failed, {id} not exists"})


@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    try:
        return service.assign_mission(m_id=id, a_id=agent_id)

    except exceptions.AgentNotExists:
        logger.error(f"agent not found, id: {id}")
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {agent_id}"})

    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={
                            "massage": f"failed, mission {id} not exists"})

    except exceptions.MissionNotNew:
        raise HTTPException(status_code=400, detail={
                            "message": "failed, mission must be in status new to assign"})

    except exceptions.InactiveAgent:
        raise HTTPException(status_code=400, detail={
                            "message": f"failed,  {agent_id} -> inactive"})

    except exceptions.AgentOverTheMissionsLimit:
        raise HTTPException(status_code=400, detail={
                            "message": f"failed, agent {agent_id} has more than {service.max_mission_to_agent} missions"})

    except exceptions.CriticalForJunior:
        raise HTTPException(status_code=400, detail={
                            "message": f"failed, agent {agent_id} is a junior for critical mission"})
    except exceptions.CriticalForSenior:
        raise HTTPException(status_code=400, detail={
                            "message": f"failed, agent {agent_id} is a senior for critical mission"})

@router.put("/{id}/start")
def start_mission(id:int):
    try:
        return service.start_mission(id=id)
    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={
                            "massage": f"failed, mission {id} not exists"})
    except exceptions.StartUnassignedMissionError:
        raise HTTPException(status_code=400, detail="status not update -> can not start mission not in unassign status")

@router.put("/{id}/complete")
def complete_mission(id:int):
    try:
        return service.complete_mission(id=id)

    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={
                            "massage": f"failed, mission {id} not exists"})
    
    except exceptions.CompleteMissionNotInProgress:
        raise HTTPException(status_code=400, detail="status not update -> can not complete mission not in progress status ")



@router.put("/{id}/fail")
def fail_mission(id:int):
    try:
        return service.failed_mission(id=id)
    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={
                            "massage": f"failed, mission {id} not exists"})
    except exceptions.CompleteMissionNotInProgress:
        raise HTTPException(status_code=400, detail="status not update -> can not fail mission not in progress status ")

@router.put("/{id}/cancel")
def cancel_mission(id:int):
    try:
        return service.cancel_mission(id=id)

    except exceptions.CancelCompleteMission:
        raise HTTPException(status_code=400, detail="status not update -> you can not cancel mission that complete")
    except exceptions.MissionNotExists:
        raise HTTPException(status_code=404, detail={
                            "massage": f"failed, mission {id} not exists"})
