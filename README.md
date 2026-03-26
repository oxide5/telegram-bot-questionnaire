# Telegram Info Forwarder Bot

A lightweight and efficient Telegram bot built with **Python** and **aiogram 3.x**. The bot serves as a bridge between users and an administrator, forwarding messages to a specific ID and logging all interactions into a JSON file for persistent storage.

## Features

* **Message Forwarding:** Automatically forwards any message sent by a user to a predefined Admin ID.
* **Data Logging:** Every interaction is saved locally in a `data.json` file, ensuring no information is lost.
* **Environment Safety:** Sensitive data like the Bot Token and Admin ID are managed via environment variables (`.env`).
* **Asynchronous:** Built on top of `asyncio` for high performance.

## Tech Stack

* **Language:** Python 3.10+
* **Library:** [aiogram 3.x](https://docs.aiogram.dev/)
* **Storage:** JSON (Local File System)
* **Environment Management:** `python-dotenv`

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/oxide5/telegram-bot-questionnaire.git
   cd telegram-bot-questionnaire
