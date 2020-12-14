from fastapi import APIRouter, Depends
from aiohttp import ClientSession
from app.db import MongoManager
from app.db import PostDB, OID
from app.db import get_database

router = APIRouter()

URL = "https://m.avito.ru"
KEY = "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir"


@router.post("/add")
async def add(phrase: str, location: str, db: MongoManager = Depends(get_database)):
    async with ClientSession() as session:
        async with session.get(URL + f"/api/1/slocations?key={KEY}&query={location}") as request_loc:
            request_loc_json = await request_loc.json()
            response_loc = request_loc_json.get("result", {"locations": []})
            location_id = int(response_loc["locations"][0]["id"])
            post_response = PostDB(phrase=phrase, location=location_id)
            await db.add_post(post_response)


@router.get('/all')
async def all_posts(db: MongoManager = Depends(get_database)):
    posts = await db.get_posts()
    return posts


@router.get("/stat")
async def stat(stat_id: OID, db: MongoManager = Depends(get_database)):
    post = await db.get_post(post_id=stat_id)
    async with ClientSession() as session:
        async with session.get(URL + f"/api/9/items?key={KEY}&locationId={post.location}&query={post.phrase}") as request_query:
            request_query_json = await request_query.json()
            response_query = request_query_json["result"]
            count = response_query["totalCount"]
            return {"count": count}
