import os
from datetime import datetime
from quart import Quart, send_from_directory, request, Response
from Util import ClientIp
from Dao.AsyncUserDao import UserDao
from aiohttp import ClientSession

app = Quart(__name__)

react = os.path.join(os.path.dirname(__file__), "react")

@app.route("/")
async def sentIndex():
	return await send_from_directory(react, "index.html")

@app.route("/theme")
async def sendTheme():
	if datetime.now().hour < 18 and datetime.now().hour >= 6:
		return await send_from_directory(react, "theme-day.css")
	else:
		return await send_from_directory(react, "theme-night.css")
	
@app.route("/style")
async def sendMainStyle():
	async with ClientSession() as session:
		async with session.get("http://apiStyleSheet:8020/main") as res:
			if res.status == 200:
				text = await res.text()
				return Response(text, content_type="text/css")
			else:	
				return "{{NaN}}", res.status
		
@app.route("/lang")
async def sendLang():
	lang = await ClientIp.getCountry(ClientIp.getClientIp())
	filepath = os.path.join(react, "lang", lang + ".lang")
	if not os.path.exists(filepath):
		return send_from_directory(os.path.dirname(filepath), "US.lang")
	return await send_from_directory(os.path.dirname(filepath), os.path.basename(filepath))

@app.route("/favicon")
async def sendFavicon():
	return await send_from_directory(os.path.join(react, "public"), "favicon.png")

@app.route("/item")
async def sendItem():
	return Response("[]", content_type="application/json")

@app.route("/login", methods=["POST"])
async def logIn():
	data = await request.get_json()
	if "id" not in data:
		return {"error": "No id provided"}, 400
	uid = data["id"]
	user = UserDao(uid)
	info = user.getInfo()
	if not info:
		return {"error": "User not found"}, 404
	return {
		"id": info[0],
		"email": info[1],
		"created_at": info[2].isoformat()
	}

@app.route("/<path:filename>")
async def sendPublicFile(filename):
	if ".." in filename or filename.startswith("/") or filename.startswith("\\") or filename.startswith("."):
		return "Invalid filename", 400
	return await send_from_directory(react, filename) #, mimetype="application/javascript" if filename.endswith(".js") else None)