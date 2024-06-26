import asyncio
import socket
import os
import sys
import ctypes
from user_interface import UserInterface
from server_api import Server

if getattr(sys, 'frozen', False):
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

class AutoWriterApp:
    def __init__(self):
        self.ui = UserInterface()
        self.ui.protocol("WM_DELETE_WINDOW", self.shutdown)
        self.server = Server("Auto Writer Server", self.ui.log_box_signal)
        self.server_task = None

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return str(local_ip)
        except Exception as e:
            self.log(f"Error obtaining local IP: {e}", error=True)
            return None

    async def start_server(self):
        try:
            self.log("Starting Server...")
            self.ui.set_server_state(UserInterface.SERVER_STATE_STARTING)
            await self.server.start()
            self.log("Server Started!")
            self.ui.set_server_state(UserInterface.SERVER_STATE_RUNNING)
            ip = self.get_local_ip()
            if ip:
                self.log("Ensure Client and Server are on the same network (Hotspot | WIFI | etc)")
                self.log("Enter the Server Location in the Client App and test the connection")
                self.log(f"Server Location: {ip}")
            else:
                self.log("Cannot obtain local IP", error=True)
        except Exception as e:
            self.log(f"Error starting server: {e}", error=True)
            self.ui.set_server_state(UserInterface.SERVER_STATE_NOT_RUNNING)

    async def stop_server(self):
        try:
            self.log("Stopping Server...")
            self.ui.set_server_state(UserInterface.SERVER_STATE_STOPPING)
            await self.server.stop()
            self.log("Server Stopped!")
            self.ui.set_server_state(UserInterface.SERVER_STATE_NOT_RUNNING)
        except Exception as e:
            self.log(f"Error stopping server: {e}", error=True)
            self.ui.set_server_state(UserInterface.SERVER_STATE_NOT_RUNNING)

    async def handle_start_stop(self, start):
        if start:
            if not self.server_task:
                self.server_task = asyncio.create_task(self.start_server())
        else:
            if self.server_task:
                await self.stop_server()
                self.server_task = None

    def log(self, message, error=False):
        formatted_message = f"[{'ERROR' if error else 'INFO'}] {message}"
        self.ui.log_box_signal.emit(formatted_message)

    async def run(self):
        self.ui.start_stop_signal.connect(lambda start: asyncio.create_task(self.handle_start_stop(start)))
        while True:
            self.ui.update()
            await asyncio.sleep(0.01)

    def shutdown(self):    
        os._exit(0)

async def main():
    app = AutoWriterApp()
    try:
        await app.run()
    except KeyboardInterrupt:
        pass
    finally:
        app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
