from asyncio import sleep
from app.config.db.session import redis_client


async def process_image(image_id: str, worker_id: str):
    print(f"Processing image: {image_id}")
    await sleep(1)
    await redis_client.decr(f"worker:{worker_id}:load")
