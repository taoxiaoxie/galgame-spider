import httpx
from utils import load_all_character_name_and_id, get_current_time
from config import MAX_TIME_OUT, HEADERS
import asyncio


class GalGameCharacterCrawler:
    def __init__(self, base_url, timeout):
        self.base_url = base_url
        self.timeout = timeout
    async def get_character_info(self, character_id):
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            headers = HEADERS
            headers['Date'] = get_current_time()
            response = await client.get(f"{self.base_url}/c{character_id}", headers=headers)
            print(response)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Error getting character info for character {character_id}: {response.status_code}")
                return None

async def main():
    BASE_URL = "https://vndb.org"  # Replace with the actual API endpoint

    crawler = GalGameCharacterCrawler(BASE_URL, MAX_TIME_OUT)
    character_name_and_id = load_all_character_name_and_id()
    character_ids = list(character_name_and_id.values())

    for character_id in character_ids[:10]:

        character_info = await crawler.get_character_info(character_id)
        if character_info:
            print(character_info)


if __name__ == "__main__":
    asyncio.run(main())
