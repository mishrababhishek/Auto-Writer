import asyncio
import socket
import os
from user_interface import UserInterface
from server_api import Server, ServerThread

ui = UserInterface()
server = Server("Auto Writer Server", ui.log_box_signal)
server_thread = ServerThread(server.get_app())

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return str(local_ip)
    except Exception as e:
        log(f"Error obtaining local IP: {e}", error=True)
        return e

async def start_server():
    try:
        log("Starting Server...")
        set_server_state(UserInterface.SERVER_STATE_STARTING)
        server_thread.start()
        log("Server Started!")
        set_server_state(UserInterface.SERVER_STATE_RUNNING)
        ip = get_local_ip()
        if isinstance(ip, Exception):
            log("Cannot obtain local IP", error=True)
            log("Something went wrong!", error=True)
        else:
            log("Ensure Client and Server are on the same network (Hotspot | WIFI | etc)")
            log("Enter the Server Location in the Client App and test the connection")
            log(f"Server Location: {ip}")
    except Exception as e:
        log(f"Error starting server: {e}", error=True)
        set_server_state(UserInterface.SERVER_STATE_NOT_RUNNING)

async def stop_server():
    try:
        log("Stopping Server...")
        set_server_state(UserInterface.SERVER_STATE_STOPPING)
        await server_thread.stop()
        log("Server Stopped!")
        set_server_state(UserInterface.SERVER_STATE_NOT_RUNNING)
    except Exception as e:
        log(f"Error stopping server: {e}", error=True)
        set_server_state(UserInterface.SERVER_STATE_NOT_RUNNING)

async def handle_start_stop(start):
    try:
        if start:
            await start_server()
        else:
            await stop_server()
    except Exception as e:
        log(f"Error handling start/stop: {e}", error=True)

async def run_asyncio_loop():
    try:
        while True:
            await asyncio.sleep(0.01)
    except Exception as e:
        log(f"Error in asyncio loop: {e}", error=True)

async def shutdown(loop):
    try:
        log("Shutting down in 3 seconds...")
        for i in range(3, 0, -1):
            log(f"Shutting down in {i}...")
            await asyncio.sleep(1)
        log("Shutting down now.")
        os._exit(0)
    except Exception as e:
        log(f"Error during shutdown: {e}", error=True)

def on_closing(loop):
    try:
        asyncio.run_coroutine_threadsafe(shutdown(loop), loop)
    except Exception as e:
        log(f"Error on closing: {e}", error=True)

def log(message, error=False):
    formatted_message = f"[{'ERROR' if error else 'INFO'}] {message}"
    ui.log_box_signal.emit(formatted_message)

def set_server_state(state):
    try:
        ui.server_state_signal.emit(state)
    except Exception as e:
        log(f"Error setting server state: {e}", error=True)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    ui.start_stop_signal.connect(lambda start: asyncio.create_task(handle_start_stop(start)))

    async def run_ui():
        try:
            ui.after(10, lambda: loop.create_task(run_asyncio_loop()))
            while True:
                ui.update()
                await asyncio.sleep(0.01)
        except Exception as e:
            log(f"Error running UI: {e}", error=True)

    ui.protocol("WM_DELETE_WINDOW", lambda: on_closing(loop))

    try:
        loop.run_until_complete(run_ui())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log(f"Error in main event loop: {e}", error=True)
    finally:
        loop.close()

if __name__ == "__main__":
    main()
