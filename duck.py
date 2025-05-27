import socketpool
import wifi
import time
import digitalio
import gc
import usb_hid
import board
import random
from board import LED
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_httpserver import Server, Request, Response, JSONResponse, POST


SSID = "PicoWiFiDuck"
PASSWORD = "!@picowsecurity"

def start_access_point():
    print("Creating access point", SSID)
    wifi.radio.stop_station()
    for _ in range(3): 
        try:
            wifi.radio.start_ap(SSID, PASSWORD, channel=6)
            ap_ip = wifi.radio.ipv4_address_ap
            print(f"Access point created at IP: {ap_ip}")
            return True
        except Exception as e:
            print(f"Failed to start AP: {e}")
            time.sleep(2)
    print("Failed to start AP after retries")
    return False

if not start_access_point():
    led = digitalio.DigitalInOut(LED)
    led.direction = digitalio.Direction.OUTPUT
    while True:
        led.value = not led.value 
        time.sleep(0.5)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(random.uniform(0.1, 0.1))
    led.value = False
    time.sleep(random.uniform(0.1, 0.1))


kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
mouse = Mouse(usb_hid.devices)

duckyCommands = {
    'WINDOWS': Keycode.WINDOWS, 'GUI': Keycode.GUI,
    'APP': Keycode.APPLICATION, 'MENU': Keycode.APPLICATION, 'SHIFT': Keycode.SHIFT,
    'ALT': Keycode.ALT, 'CONTROL': Keycode.CONTROL, 'CTRL': Keycode.CONTROL,
    'DOWNARROW': Keycode.DOWN_ARROW, 'DOWN': Keycode.DOWN_ARROW, 'LEFTARROW': Keycode.LEFT_ARROW,
    'LEFT': Keycode.LEFT_ARROW, 'RIGHTARROW': Keycode.RIGHT_ARROW, 'RIGHT': Keycode.RIGHT_ARROW,
    'UPARROW': Keycode.UP_ARROW, 'UP': Keycode.UP_ARROW, 'BREAK': Keycode.PAUSE,
    'PAUSE': Keycode.PAUSE, 'CAPSLOCK': Keycode.CAPS_LOCK, 'DELETE': Keycode.DELETE,
    'END': Keycode.END, 'ESC': Keycode.ESCAPE, 'ESCAPE': Keycode.ESCAPE, 'HOME': Keycode.HOME,
    'INSERT': Keycode.INSERT, 'NUMLOCK': Keycode.KEYPAD_NUMLOCK, 'PAGEUP': Keycode.PAGE_UP,
    'PAGEDOWN': Keycode.PAGE_DOWN, 'PRINTSCREEN': Keycode.PRINT_SCREEN, 'ENTER': Keycode.ENTER,
    'SCROLLLOCK': Keycode.SCROLL_LOCK, 'SPACE': Keycode.SPACE, 'TAB': Keycode.TAB,
    'A': Keycode.A, 'B': Keycode.B, 'C': Keycode.C, 'D': Keycode.D, 'E': Keycode.E,
    'F': Keycode.F, 'G': Keycode.G, 'H': Keycode.H, 'I': Keycode.I, 'J': Keycode.J,
    'K': Keycode.K, 'L': Keycode.L, 'M': Keycode.M, 'N': Keycode.N, 'O': Keycode.O,
    'P': Keycode.P, 'Q': Keycode.Q, 'R': Keycode.R, 'S': Keycode.S, 'T': Keycode.T,
    'U': Keycode.U, 'V': Keycode.V, 'W': Keycode.W, 'X': Keycode.X, 'Y': Keycode.Y,
    'Z': Keycode.Z, 'F1': Keycode.F1, 'F2': Keycode.F2, 'F3': Keycode.F3,
    'F4': Keycode.F4, 'F5': Keycode.F5, 'F6': Keycode.F6, 'F7': Keycode.F7,
    'F8': Keycode.F8, 'F9': Keycode.F9, 'F10': Keycode.F10, 'F11': Keycode.F11,
    'F12': Keycode.F12,
}

def convertLine(line):
    newline = []
    print(f"Converting line: {line}")
    for key in filter(None, line.split(" ")):
        key = key.upper()
        command_keycode = duckyCommands.get(key)
        if command_keycode is not None:
            newline.append(command_keycode)
        elif hasattr(Keycode, key):
            newline.append(getattr(Keycode, key))
        else:
            print(f"Unknown key: <{key}>")
    return newline

def runScriptLine(line):
    for k in line:
        kbd.press(k)
    kbd.release_all()

def sendString(line):
    layout.write(line)

def parseLine(line):
    try:
        if not line.strip():
            return
        if line.startswith("REM"):
            print(f"Comment: {line}")
        elif line.startswith("DELAY"):
            delay_ms = float(line.split()[1]) / 1000
            print(f"Delaying for {delay_ms} seconds")
            time.sleep(delay_ms)
        elif line.startswith("STRING"):
            print(f"Typing string: {line[7:]}")
            sendString(line[7:])
        elif line.startswith("DEFAULT_DELAY") or line.startswith("DEFAULTDELAY"):
            global defaultDelay
            parts = line.split()
            if len(parts) > 1:
                defaultDelay = int(parts[1]) * 10
                print(f"Set default delay: {defaultDelay} ms")
        elif line.startswith("MOUSEMOVE"):
            parts = line.split()
            if len(parts) >= 3:
                x = int(parts[1])
                y = int(parts[2])
                print(f"Moving mouse: x={x}, y={y}")
                mouse.move(x, y)
        elif line.startswith("MOUSECLICK"):
            print("Mouse click: LEFT")
            mouse.click(mouse.LEFT_BUTTON)
        else:
            newScriptLine = convertLine(line)
            print(f"Executing keys: {newScriptLine}")
            runScriptLine(newScriptLine)
    except Exception as e:
        print(f"Error in line '{line}': {e}")
        led.value = False

def exe(payload_script):
    global defaultDelay
    defaultDelay = 0
    previousLine = ""
    print(f"Executing payload. Free memory: {gc.mem_free()} bytes")
    for line in payload_script:
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("REPEAT"):
            try:
                count = int(line.split()[1])
                for i in range(count):
                    parseLine(previousLine)
                    time.sleep(defaultDelay / 1000)
            except (ValueError, IndexError):
                print(f"Invalid REPEAT value: {line}")
        else:
            parseLine(line)
            previousLine = line
        time.sleep(defaultDelay / 1000)
    print(f"Payload execution completed. Free memory: {gc.mem_free()} bytes")
    led.value = True

@server.route("/", methods=["GET"])
def base(request: Request):
    try:
        with open("index.html", "r") as file:
            html_content = file.read()
        headers = {"Content-Type": "text/html"}
        return Response(request, html_content, headers=headers)
    except Exception as e:
        return Response(request, "File not found", status=404)

@server.route("/api", methods=[POST])
def handle_payload(request: Request):
    try:
        req = request.json()
        payload = req.get("content", "")
        if not payload:
            return JSONResponse(request, {"error": "No content provided"}, status=400)
        if len(payload) > 10000: 
            return JSONResponse(request, {"error": "Payload too large"}, status=400)
        payload_lines = payload.splitlines()
        if len(payload_lines) > 1000:  
            return JSONResponse(request, {"error": "Too many lines in payload"}, status=400)
        led.value = True
        exe(payload_lines)
        return JSONResponse(request, {"message": "Payload executed successfully"})
    except Exception as e:
        led.value = False
        return JSONResponse(request, {"error": str(e)}, status=500)

print(f"Starting server on 192.168.4.1:80. Free memory: {gc.mem_free()} bytes")
server.serve_forever(port=80)
