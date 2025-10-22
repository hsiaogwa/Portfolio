from quart import request
from aiohttp import ClientSession
from datetime import datetime, timedelta, timezone

def getClientIp():
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(",")[0]
    return request.remote_addr

async def getCountry(ip: str):
    async with ClientSession() as session:
        async with session.get(f"https://ipapi.co/{ip}/json/") as res:
            if res.status == 200:
                data = await res.json()
                return data.get("country_code", "US")
            return "US"

async def getTimeOffset(ip: str):
    async with ClientSession() as session:
        async with session.get(f"https://ipapi.co/{ip}/json/") as res:
            if res.status == 200:
                data = await res.json()
                return data.get("utc_offset", "+0000")
            return "+0000"
        
async def getLocalTime(ip: str):
    offset = await getTimeOffset(ip)
    return datetime.now(timezone.utc) + timedelta(hours=int(offset[:3]), minutes=int(offset[0] + offset[3:]))