from app.db.database import MongoManager

db = MongoManager()


async def get_database() -> MongoManager:
    return db