# 🚀 Auto Writer

Auto Writer is an application suite designed for automated text writing, consisting of both server and client components.

## 🌟 Features

### Server Features

- **User-friendly GUI**: Built with Tkinter for easy server management.
- **FastAPI-powered API**: Efficient and scalable API endpoints.
- **Asynchronous operations**: Utilizes `asyncio` for non-blocking I/O.
- **Real-time logging**: Live updates on server status and operations.
- **Remote control**: Pause, resume, and stop writing operations.
- **Customizable typing speed**: Adjust min and max delay between keystrokes.

### Client Features

- **Connect to Auto Writer Server**: Interface for automated text input.
- **Auto Writer Interface**: For automated text input.
- **Pause and Resume**: Functionality to pause and resume writing.
- **Stop Writing**: Stop writing at any time.

## 🛠️ Tech Stack

### Server Tech Stack

- Python 3.12.4
- FastAPI
- Uvicorn
- PyAutoGUI
- Tkinter

### Client Tech Stack

- ReactJS
- Vite

## 🚀 Getting Started

### Server

```bash
git clone https://github.com/mishrababhishek/auto-writer.git
cd auto-writer/server
pip install -r requirements.txt
python main.py
```
## Client
```bash
git clone https://github.com/mishrababhishek/auto-writer.git
cd auto-writer
npm install
npm run dev
```

## 🔧 Usage

- Server: Use the Tkinter GUI to start, stop, and monitor writing operations. Access API endpoints for remote control.
- Client: Connect to the server via IP address and use the Vite-powered interface to automate text input.

## 🧩 Core Component

- Server Components:
    - main.py: Entry point and main loop.
    - server_api.py: FastAPI server and endpoint definitions.
    - user_interface.py: Tkinter-based GUI.
    - writer.py: Text writing logic with PyAutoGUI.
    - signals.py: Custom signal system for inter-component communication

- Client Components:
    - React components for UI.
    - Integration with server API endpoints.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

## Contribution
Contributions to both the server and client components are welcome! 

## 📄 License
This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.
