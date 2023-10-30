from utils import (load_all_character_name_and_id,
                   get_current_time,
                   print_table_entries,
                   parse_character_info
                   )
from config import (MAX_TIME_OUT,
                    HEADERS,
                    COROUTINE_LIMIT,
                    REQUEST_INTERVAL,
                    RATE_LIMIT_WAIT_TIME,
                    EXCEPTION_WAIT_TIME
                    )
import asyncio
import aiofiles
import logging
import json
import httpx
from tqdm.asyncio import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GalGameCharacterCrawler:
    def __init__(self, base_url, timeout):
        self.base_url = base_url
        self.timeout = timeout

    async def get_character_info(self, character_id):
        retries = 3  # 设置重试次数
        while retries > 0:
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    headers = HEADERS
                    headers['Date'] = get_current_time()
                    url = f"{self.base_url}/{character_id}"
                    response = await client.get(url, headers=headers)
                    if response.status_code == 200:
                        return response.text
                    else:
                        logger.error(f"Failed to get character info for {character_id}, status code: {response.status_code}")
                        logger.error(f"Caused by: {response.text}")
                        if "rate-limited!" in response.text:
                            logger.warning("Rate limit reached, waiting for 10 seconds...")
                            await asyncio.sleep(RATE_LIMIT_WAIT_TIME)
                            return await self.get_character_info(character_id)  # Retry the request
                        return None
            except (httpx.ConnectError, httpx.ReadError) as e:
                logger.error(f"Error while getting character info for {character_id}: {str(e)}")
                retries -= 1
                if retries > 0:
                    logger.info(f"Retrying... ({3 - retries} attempts left)")
                    await asyncio.sleep(EXCEPTION_WAIT_TIME)  # 等待5秒后重试
                else:
                    logger.error(f"Failed to get character info for {character_id} after 3 attempts")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return None

async def save_to_jsonl(data, filename="output.jsonl"):
    async with aiofiles.open(filename, mode='a') as f:
        await f.write(json.dumps(data) + '\n')


async def fetch_and_save_character_info(crawler, character_id, semaphore):
    async with semaphore:
        character_info = await crawler.get_character_info(character_id)
        if character_info:
            parsed_character_info = await parse_character_info(character_info)
            parsed_character_info['id'] = character_id
            logger.info(f"Saved character info for {character_id}")
            await save_to_jsonl(parsed_character_info)

async def main():
    BASE_URL = "https://vndb.org"  # Replace with the actual API endpoint
    crawler = GalGameCharacterCrawler(BASE_URL, MAX_TIME_OUT)
    character_name_and_id = load_all_character_name_and_id()
    character_ids = list(character_name_and_id.values())

    # 定义协程数目
    semaphore = asyncio.Semaphore(COROUTINE_LIMIT)
    logger.info(f"Start to crawl {len(character_ids)} characters")
    # tasks = []
    async for character_id in tqdm(character_ids, total=len(character_ids)):
        await fetch_and_save_character_info(crawler, character_id, semaphore)
        await asyncio.sleep(REQUEST_INTERVAL)  # 请求间隔


if __name__ == "__main__":
    asyncio.run(main())
