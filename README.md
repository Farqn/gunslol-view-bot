# Guns.lol Advanced View Bot 🚀

This is a simple automation tool built with Python and Selenium to visit `guns.lol` profiles. It features a dynamic proxy system that refreshes every 5 minutes to ensure views come from different IP addresses.

## ✨ Features
- **Dynamic Proxy Support:** Automatically fetches the latest IP list via the `proxyscrape` API.
- **Auto-Refresh:** Updates the proxy pool every 5 minutes to bypass basic rate limits.
- **User-Friendly:** Easily specify the target profile directly through the terminal.
- **Driver Management:** Automatically handles Chrome Driver installation using `webdriver-manager`.

## 🛠️ Installation & Usage

1. **Install Python:** Ensure you have Python 3.x installed on your system.
2. **Install Dependencies:** Open your terminal in the project folder and run:
   ```bash
   pip install -r requirements.txt