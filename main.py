import httpx
from utils import load_all_character_name_and_id
from config import MAX_TIME_OUT

class GalGameCharacterCrawler:
    def __init__(self, base_url, timeout):
        self.client = httpx.Client(base_url=base_url, timeout=timeout)

    def get_character_info(self, character_id):
        response = self.client.post("/character", json={"id": character_id})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get character info for {character_id}. Status code: {response.status_code}")
            return None

if __name__ == "__main__":
    BASE_URL = "https://api.vndb.org"  # Replace with the actual API endpoint
    MAX_TIME_OUT = 10  # Replace with your desired timeout value

    crawler = GalGameCharacterCrawler(BASE_URL, MAX_TIME_OUT)
    character_name_and_id = load_all_character_name_and_id()
    character_ids = list(character_name_and_id.values())

    for character_id in character_ids[:10]:

        character_info = crawler.get_character_info(character_id)
        if character_info:
            print(character_info)
