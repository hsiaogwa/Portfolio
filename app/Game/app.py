from quart import Quart, Response
import os

app = Quart(__name__)

@app.route("/")
async def hello():
	return Response("Now No Games Here...", content_type="text/html")

@app.route("/<path:filename>")
async def sendFile(filename):
	filepath = os.path.join(os.path.dirname(__file__), filename)
	if not os.path.exists(filepath):
		return Response("File Not Found", status=404)
	return await app.send_static_file(filename)