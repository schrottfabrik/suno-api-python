import json
import os
import aiohttp
from loguru import logger

BASE_URL = os.getenv("BASE_URL")


COMMON_HEADERS = {
    # "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Referer": "https://suno.com/",
    "Origin": "https://suno.com",
}


async def fetch(url, headers=None, data=None, method="POST"):
    if headers is None:
        headers = {}
    headers.update(COMMON_HEADERS)
    if data is not None:
        data = json.dumps(data)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=method, url=url, data=data, headers=headers
            ) as resp:
                resp.raise_for_status()  # Raises an exception for HTTP errors
                return await resp.json()
        except aiohttp.ClientResponseError as e:
            # Handle HTTP errors
            error_text = await e.response.text()
            raise Exception(f"HTTP Error {e.status}: {error_text}")
        except Exception as e:
            # Handle other exceptions
            raise Exception(str(e))


async def get_feed(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/clip/{ids}"
    response = await fetch(api_url, headers, method="GET")
    return [response]


async def get_feeds(ids, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/feed/v2?ids={ids}"
    response = await fetch(api_url, headers, method="GET")
    clips = response.get("clips")
    if clips:
        return clips
    return response


async def generate_music(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/v2/"
    response = await fetch(api_url, headers, data)
    return response


async def concat_music(data, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/concat/v2/"
    response = await fetch(api_url, headers, data)
    return response


async def generate_lyrics(prompt, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/"
    data = {"prompt": prompt, "lyrics_model": "default"}
    return await fetch(api_url, headers, data)


async def get_lyrics(lid, token):
    headers = {"Authorization": f"Bearer {token}"}
    api_url = f"{BASE_URL}/api/generate/lyrics/{lid}"
    return await fetch(api_url, headers, method="GET")


# You can use this function to send notifications
def notify(message: str):
    logger.info(message)
