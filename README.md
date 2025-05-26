# Pico WiFi Duck

Pico WiFi Duck is a web-based interface designed to transform a **Raspberry Pi Pico W** into a USB Rubber Ducky, enabling remote execution of **Ducky Script** payloads via Wi-Fi. This tool simulates keyboard inputs on a connected system for authorized testing and educational purposes.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How to Use](#how-to-use)
- [File Structure](#file-structure)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Disclaimer](#disclaimer)
- [Credits](#credits)

## Overview
Pico WiFi Duck provides a user-friendly web interface to write, upload, and execute Ducky Scripts on a Raspberry Pi Pico W. By connecting to a Wi-Fi hotspot hosted by the Pico W, users can remotely send scripts to simulate keyboard inputs on a target system.

## Features
- **Web-Based Editor**: Write or upload Ducky Scripts in a browser-based textarea.
- **File Upload**: Upload `.txt` files containing Ducky Scripts.
- **Payload Execution**: Send scripts to the Raspberry Pi Pico W via a POST request to a specified API endpoint.
- **Real-Time Feedback**: Displays success or error messages for payload execution.
- **Responsive Design**: Adapts to various screen sizes, including mobile devices.
- **Clear Functionality**: Reset the editor and clear status messages.
- **Dark Theme**: Monochrome green aesthetic inspired by terminal interfaces.

## How to Use
1. **Connect to the Hotspot**:
   - SSID: `PicoWiFiDuck`
   - Password: `!@picowsecurity`
2. **Write or Upload a Script**:
   - Type a Ducky Script in the provided textarea or upload a `.txt` file.
3. **Execute the Payload**:
   - Click the **Run** button to send the script to the Raspberry Pi Pico W.
4. **Clear the Editor**:
   - Click the **Clear** button to reset the textarea and status messages.

### Sample Ducky Script
```ducky
REM Open Notepad and say hi
GUI r
DELAY 300
STRING notepad
ENTER
DELAY 500
STRING Hello from Pico WiFi Duck!
```

## File Structure
```
index.html
├── <html>
│   ├── <head>
│   │   ├── Meta tags (charset, viewport)
│   │   ├── Google Fonts (JetBrains Mono)
│   │   ├── CSS (Internal styles for layout, design, and responsiveness)
│   ├── <body>
│   │   ├── Header (Title: Pico WiFi Duck)
│   │   ├── Main (Container with sections)
│   │   │   ├── About Section
│   │   │   ├── How to Use Section
│   │   │   ├── Editor Section (Textarea, Buttons, Status/Error Messages)
│   │   │   ├── Disclaimer Section
│   │   ├── Footer (Credits and GitHub link)
│   │   ├── JavaScript (Handles payload submission, file upload, and UI interactions)
```

## Technologies Used
- **HTML5**: Structure of the web interface.
- **CSS3**: Styling with a dark, green monochrome theme and responsive design.
- **JavaScript**: Client-side logic for handling file uploads, HTTP requests, and UI updates.
- **Google Fonts**: JetBrains Mono for a monospaced, terminal-like aesthetic.
- **Raspberry Pi Pico W**: Hardware to host the Wi-Fi hotspot and execute Ducky Scripts.
- **Ducky Script**: Scripting language for USB Rubber Ducky payloads.

## Setup and Installation
1. **Hardware Setup**:
   - Configure your Raspberry Pi Pico W to run the Pico WiFi Duck firmware (not included in this file).
   - Ensure the Pico W hosts a Wi-Fi hotspot with the SSID `PicoWiFiDuck` and password `!@picowsecurity`.
   - Set up an API endpoint at `http://192.168.4.1/api` to receive POST requests with Ducky Scripts.

2. **Deploy the Web Interface**:
   - Host the `index.html` file on a web server accessible via the Pico W's hotspot (or serve it locally for testing).
   - Ensure the browser can access `http://192.168.4.1` when connected to the hotspot.

3. **Dependencies**:
   - No external JavaScript libraries are required.
   - Ensure a modern browser with JavaScript enabled.

## Usage
- **Access the Interface**:
  - Connect to the `PicoWiFiDuck` hotspot.
  - Open a browser and navigate to the hosted web interface (e.g., `http://192.168.4.1`).
- **Write a Script**:
  - Enter a Ducky Script in the textarea or upload a `.txt` file using the **Upload Script** button.
- **Run the Script**:
  - Click the **Run** button to send the script to the Pico W via a POST request.
  - The status message will indicate success (`✅ Payload executed successfully!`) or failure (e.g., `❌ Error 404: Not Found`).
- **Clear the Editor**:
  - Click the **Clear** button to reset the textarea and hide status/error messages.

### JavaScript Functions
- **`sendHttpRequest(data)`**:
  - Sends a POST request to `http://192.168.4.1/api` with the Ducky Script payload.
  - Updates the UI with status or error messages based on the response.
  - Handles timeouts (50 seconds) and network errors.
- **`main()`**:
  - Retrieves the script from the textarea, validates it, and calls `sendHttpRequest`.
- **`clearPayload()`**:
  - Clears the textarea, file input, and status/error messages.
- **File Input Event Listener**:
  - Handles `.txt` file uploads, validates the file type, and populates the textarea with the file content.

## Disclaimer
This tool is intended for **educational and authorized testing purposes only**. The developers and contributors are not responsible for any misuse or illegal activities conducted with this tool. Use responsibly and ensure compliance with applicable laws and permissions.

## Credits
- **Author**: ThemeHackers
- **Credit**: majdsassi
- **GitHub**: [ThemeHackers](https://github.com/ThemeHackers/)
- **Year**: 2025

---

**Note**: Ensure the Raspberry Pi Pico W is properly configured to handle Ducky Scripts and the API endpoint is operational. This HTML file assumes the backend is set up to receive and process payloads at `http://192.168.4.1/api`.
```
