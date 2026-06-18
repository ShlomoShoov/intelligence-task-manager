from fastapi import APIRouter, HTTPException

from business_logic.services import Services
import  business_logic.exceptions as exceptions
router = APIRouter(prefix='/reports')

service = Services()

@router.get("/summary")
def get_summary():
    return service.get_summary()

@router.get("/missions-by-status")
def get_by_status():
    return service.get_by_status()

@router.get("/top-agent")
def get_top_status():
    try:
        return service.get_top_agent()
    except exceptions.AgentNotExists:
        raise HTTPException(status_code=404, detail={
                            "message": f"there is no best agent for now (best agent = max(completed missions))"})
