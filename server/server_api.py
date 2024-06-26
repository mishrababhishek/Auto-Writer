from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import uvicorn
import asyncio
from writer import Writer

class EventRequest(BaseModel):
    text: str
    min_delay: float = 0.05
    max_delay: float = 0.20

class Server:
    def __init__(self, title: str, log_signal):
        self.app = FastAPI(title=title)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  
            allow_credentials=True,
            allow_methods=["*"],  
            allow_headers=["*"],
        )
        self.exec_router = APIRouter(prefix="/execute")
        self.health_router = APIRouter(prefix="/health")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.templates = Jinja2Templates(directory=os.path.join(current_dir, "public"))
        self.log_signal = log_signal
        self.writer = Writer(self.log)
        self.setup_routes()

    def setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            self.log(f"Home page requested from {request.client.host}")
            return self.templates.TemplateResponse("home.html", {"request": request})

        @self.health_router.get("/connection")
        async def connection():
            self.log("Health check requested")
            return {"status": "online"}

        @self.exec_router.post("/write")
        async def write(arg: EventRequest, request: Request):
            self.log(f"Received write request from {request.client.host}")
            self.log(f"Text length: {len(arg.text)}, Min delay: {arg.min_delay}, Max delay: {arg.max_delay}")
            await self.writer.write(arg.text, arg.min_delay, arg.max_delay)
            return {"status": "Finished"}

        @self.exec_router.post("/pause")
        async def pause():
            self.writer.pause()
            self.log("Writer process paused")
            return {"status": "Paused"}

        @self.exec_router.post("/resume")
        async def resume():
            self.writer.resume()
            self.log("Writer process resumed")
            return {"status": "Resumed"}

        @self.exec_router.post("/stop")
        async def stop():
            self.writer.stop()
            self.log("Writer process stopped")
            return {"status": "Stopped"}

        self.app.include_router(self.exec_router)
        self.app.include_router(self.health_router)

    def log(self, message: str, error: bool = False):
        formatted_message = f"[{'ERROR' if error else 'INFO'}] {message}"
        self.log_signal.emit(formatted_message)

    async def start(self):
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000, loop="asyncio")
        self.server = uvicorn.Server(config)
        self.serve_task = asyncio.create_task(self.server.serve())
    
    async def stop(self):
        await self.server.shutdown()
        self.serve_task.cancel()