import asyncio
import os
import uvicorn
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from writer import Writer  
from signals import Signals

class ServerThread:
    def __init__(self, app) -> None:
        self.app = app
        self.server = None
        self.task = None
    
    async def run(self) -> None:
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000, loop="asyncio", timeout_keep_alive=1000000)
        self.server = uvicorn.Server(config)
        await self.server.serve()

    def start(self):
        self.task = asyncio.create_task(self.run())
    
    async def stop(self):
        if self.server:
            self.server.should_exit = True
        if self.task:
            await self.task

class EventRequest(BaseModel):
    text: str
    min_delay: float = 0.05
    max_delay: float = 0.20

class BaseServer:
    def __init__(self, title: str, log_box_signal: Signals) -> None:
        self._app = FastAPI(title=title)
        self._exec_router = APIRouter(prefix="/execute")
        self._health_router = APIRouter(prefix="/health")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))
        self._log_box_signal = log_box_signal
        self._setup_routes()
        self._app.include_router(self._exec_router)
        self._app.include_router(self._health_router)
        
    def get_app(self):
        return self._app
        
    def _setup_routes(self):
        pass

    def log(self, message: str, error: bool = False):
        formatted_message = f"[{'ERROR' if error else 'INFO'}] {message}"
        self._log_box_signal.emit(formatted_message)

class EventsApi(BaseServer):
    def _setup_routes(self):
        super()._setup_routes()
        self.writer_process: Writer = None

        @self._exec_router.post("/write")
        async def write(arg: EventRequest, request: Request):
            self.log(f"Received write request from {request.client.host}")
            self.log(f"Text length: {len(arg.text)}, Min delay: {arg.min_delay}, Max delay: {arg.max_delay}")

            if self.writer_process is not None and self.writer_process.is_alive():
                self.log("Previous request is not finished yet. Rejecting new request.", error=True)
                raise HTTPException(status_code=400, detail="Previous request is not finished yet!")
            
            self.log("Starting new writer process")
            self.writer_process = Writer.create_and_start_process(arg.text, arg.min_delay, arg.max_delay)
            
            self.log("Waiting for writer process to complete")
            await asyncio.to_thread(self.writer_process.join)
            
            self.log("Writer process completed")
            return {"status": "Finished"}

        @self._exec_router.post("/pause")
        async def pause():
            if self.writer_process is None or not self.writer_process.is_alive():
                self.log("No ongoing process to pause", error=True)
                raise HTTPException(status_code=400, detail="No ongoing process to pause")
            self.writer_process.pause()
            self.log("Writer process paused")
            return {"status": "Paused"}
        
        @self._exec_router.post("/resume")
        async def resume():
            if self.writer_process is None or not self.writer_process.is_alive():
                self.log("No ongoing process to resume", error=True)
                raise HTTPException(status_code=400, detail="No ongoing process to resume")
            self.writer_process.resume()
            self.log("Writer process resumed")
            return {"status": "Resumed"}

        @self._exec_router.post("/stop")
        async def stop():
            if self.writer_process is None or not self.writer_process.is_alive():
                self.log("No ongoing process to stop", error=True)
                raise HTTPException(status_code=400, detail="No ongoing process to stop")
            self.writer_process.stop()
            self.writer_process = None
            self.log("Writer process stopped")
            return {"status": "Stopped"}

class Server(EventsApi):
    def _setup_routes(self):
        super()._setup_routes()

        @self._app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            self.log(f"Home page requested from {request.client.host}")
            return self._templates.TemplateResponse("home.html", {"request": request})
        
        @self._health_router.get("/connection")
        async def connection():
            self.log("Health check requested")
            return {"status": "online"}