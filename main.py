from fastapi import FastAPI
import uvicorn
import initialize
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_routes

# init the project before the server is up
initialize.init()

app = FastAPI()
app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_routes)

if __name__ == "__main__":
    uvicorn.run(app=app)
