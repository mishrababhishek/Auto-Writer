# 🚀 Auto Writer Server

![Python Version](https://img.shields.io/badge/python-3.12.4-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

Auto Writer Server is a powerful backend component of the Auto Writer application, designed to handle text writing automation with customizable typing speeds and remote control capabilities.

## 🌟 Features

- **🖥️ User-friendly GUI**: Built with Tkinter for easy server management
- **🌐 FastAPI-powered API**: Efficient and scalable API endpoints
- **⚡ Asynchronous operations**: Utilizes `asyncio` for non-blocking I/O
- **🔄 Real-time logging**: Live updates on server status and operations
- **🎛️ Remote control**: Pause, resume, and stop writing operations
- **🔧 Customizable typing speed**: Adjust min and max delay between keystrokes

## 🛠️ Tech Stack

- Python 3.12.4
- FastAPI
- Uvicorn
- PyAutoGUI
- Tkinter

## 🚀 Getting Started

1. Clone the repository:
git clone https://github.com/mishrababhishek/auto-writer.git
Copy
2. Navigate to the project directory:
cd auto-writer/server
Copy
3. Install dependencies:
pip install -r requirements.txt
Copy
4. Run the server:
python main.py
Copy
## 🖥️ User Interface

The server comes with a sleek Tkinter-based GUI for easy management:

- **Start/Stop Server**: Toggle server status with a single click
- **Log Display**: Real-time updates on server operations
- **Server Status**: Visual indicators for server state

## 🌐 API Endpoints

- `/execute/write`: Start a new writing task
- `/execute/pause`: Pause the current writing task
- `/execute/resume`: Resume a paused writing task
- `/execute/stop`: Stop the current writing task
- `/health/connection`: Check server health status

## 🧩 Core Components

- `main.py`: Entry point and main loop
- `server_api.py`: FastAPI server and endpoint definitions
- `user_interface.py`: Tkinter-based GUI
- `writer.py`: Text writing logic with PyAutoGUI
- `signals.py`: Custom signal system for inter-component communication

## 🔐 Security

Ensure that the server is run in a secure environment, as it has the capability to control keyboard input.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [PyAutoGUI](https://pyautogui.readthedocs.io/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

---

Made with ❤️ by - Abhishek Mishra