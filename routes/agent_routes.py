from fastapi import APIRouter, HTTPException
from logging import getLogger

from business_logic.services import Services
import business_logic.exceptions as exceptions
import business_logic.models as models

router = APIRouter(prefix='/agents')
service = Services()
logger = getLogger()


@router.post('', status_code=201)
def crate_agent(data: models.AgentModel):
    logger.info("POST /agents called")
    try:
        response = service.create_agent(data)
        logger.info("Agent created successfully: id=%s",
                    (response["data"]["id"],))
        return response

    except exceptions.RankInvalid:
        logger.error("Got undefined rank: %s", (data.agent_rank))
        raise HTTPException(status_code=400, detail={
                            "message": f"error: rank is not in {models.valid_ranks}"})


@router.get("")
def get_agents():
    logger.info("GET /agents called")
    return service.get_agents()


@router.get("/{id}")
def get_by_id(id: int):
    logger.info(f"GET /agents/id called, id:{id}")
    try:
        response = service.get_agent_by_id(id=id)
        logger.info("agent found")
        return response
    except exceptions.AgentNotExists:
        logger.error(f"agent not found, id: {id}")
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {id}"})


@router.put("/{id}")
def update_agent(id: int, new_data: models.AgentModel):
    logger.info(f"called PUT agent/{id}")
    try:
        response = service.update_agent(id=id, data=new_data)
        logger.info(response["message"])
        return response
    except exceptions.RankInvalid:
        logger.error(f"Got undefined rank: {new_data.agent_rank}")
        raise HTTPException(status_code=400, detail={
                            "message": f"error: rank is not in {models.valid_ranks}"})
    except exceptions.AgentNotExists:
        logger.error(f"Agent not found, id: {id}")
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {id}"})


@router.put("{id}/deactivate")
def deactivate_id(id: int):
    logger.info(f"called PUT agents/{id}/deactivate ")
    try:
        response = service.deactivate_agent(id=id)
        logger.info(response["message"])
        return response

    except exceptions.AgentNotExists:
        logger.error(f"Agent not found, id: {id}")
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {id}"})

@router.get("/{id}/performance")
def get_performance(id:int):
    try:
        response = service.get_agent_performance(id=id)
        return response
    except exceptions.AgentNotExists:
        logger.error(f"Agent not found, id: {id}")
        raise HTTPException(status_code=404, detail={
                            "message": f"id not found: {id}"})
    
