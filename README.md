# 💬 Project – LAN Messaging

**LAN Messaging** is a Python 3 project that allows two machines connected to the same local network to communicate with each other.  
It offers a lightweight, user-friendly messaging interface using core Python modules.

---

## 📘 Description

LAN Messaging enables instant communication between two devices on the same LAN (Local Area Network).  
The software is written entirely in **Python 3**, leveraging several built-in modules to ensure smooth functionality and a simple graphical interface.

**Main modules used:**
- `Tkinter` — for the graphical interface  
- `Socket` — for the network connection between machines  
- `Functools` — for callback and function management  
- `Colorsys` — for color conversions  
- `Random` — for random color or theme generation  

All of these modules are included natively with Python 3 — **no external installation is required**.

---

## ⚙️ Prerequisites

- **Python 3.0 or later** installed on your machine  
- All required modules are standard in Python 3:

## 💾 Installation

Download or clone this repository:

  1- [https://github.com/UpsilonWolf/LAN-Messaging.git]

  2- Place the folder “Messaging Project” (or lan-messaging) in the directory of your choice.

  3- Ensure that Python 3 is correctly installed on your machine.

## 🚀 Running the Program

Open a terminal or command prompt in the project directory.

Start the server by running:

python Server.py


The server will prompt you to select a communication port.

In another terminal window (or on another machine on the same network), run the client interface:

python Client_Interface.py


When prompted, enter:

The server’s IP address

The port number used by the server

The username you want to use for the session

Once connected, enjoy chatting over your local network! 🎉

## ❓ Help & Troubleshooting

If you encounter any problems:

Ensure both devices are on the same LAN network

Verify the IP address and port number match between server and client

Check your firewall settings (Python connections must be allowed)

If the issue persists, please:

Open an Issue on this GitHub repository

Or contact the developers directly for support

We appreciate bug reports and suggestions to improve the project!

## 💬 Thank You!

Thank you for using LAN Messaging 💡
We hope you enjoy this lightweight and practical LAN communication tool.

If you appreciate this project, please consider giving it a ⭐ on GitHub — your support helps us continue developing and improving it.
Happy chatting! 🖤

