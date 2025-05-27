import socketpool
import wifi
from duck import exe
from adafruit_httpserver import Server, Request, JSONResponse, POST, Response

ssid = "Pico WIFI DUCK"
password = "!@picowsecurity"

print("Creating access point", ssid)
wifi.radio.stop_station()
wifi.radio.start_ap(ssid, password, channel=6)
print("Access point created!")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/", methods=["GET"])
def base(request: Request):
    try:
        with open("index.html", "r") as file:
            html_content = file.read()
        headers = {"Content-Type": "text/html"}
        return Response(request, html_content, headers=headers)
    except Exception as e:
        return Response(request, "File not found", status=404)

@server.route("/api", methods=[POST], append_slash=True)
def api(request: Request):
    try:
        req = request.json()
        payload = req.get("content", "")
        if not payload:
            return JSONResponse(request, {"error": "No content provided"}, status=400)
        payload_lines = payload.splitlines()
        exe(payload_lines)
        return JSONResponse(request, {"message": "Done"})
    except Exception as e:
        return JSONResponse(request, {"error": str(e)}, status=500)

server.serve_forever(port=80)

