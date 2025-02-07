import asyncio
from pprint import pprint

import motor
from beanie import init_beanie

from models import Doc


async def init():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.email_sender
    await init_beanie(database, document_models=[Doc])
    await read_data()


async def read_data():
    # doc = await Doc.find_one()
    docs = await Doc.find(
        # {"Title": {"$regex": "ESC"}}
    ).to_list()
    docs = [d for d in docs if 'ESC' in d.title]
    for d in docs[:5]:
        for person in d.persons:
            print(d.title)
            pprint(person.model_dump())


if __name__ == "__main__":
    asyncio.run(init())
