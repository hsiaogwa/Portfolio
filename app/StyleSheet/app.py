from quart import Quart, send_from_directory
import os

api = Quart(__name__)

@api.route("/main")
async def main():
	return await send_from_directory(os.path.dirname(__file__), "style.css")

@api.route("/theme")
async def theme_auto():
	return await send_from_directory(os.path.dirname(__file__), "theme-test.css")