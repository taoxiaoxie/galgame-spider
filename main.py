from utils import (load_all_character_name_and_id,
                   get_current_time,
                   print_table_entries,
                   parse_character_info,
                   remove_null_values_from_jsonl
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
from collections import Counter
from tqdm.asyncio import tqdm
import argparse
import matplotlib.pyplot as plt
import numpy as np

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

async def save_to_jsonl(data, filename="output_test.jsonl"):
    async with aiofiles.open(filename, mode='a') as f:
        await f.write(json.dumps(data) + '\n')


async def fetch_and_save_character_info(crawler, character_id, semaphore):
    async with semaphore:
        character_info = await crawler.get_character_info(character_id)

        if character_info:
            # print_table_entries(character_info)

            parsed_character_info = await parse_character_info(character_info)
            parsed_character_info['id'] = character_id
            # print_table_entries(parsed_character_info)
            logger.info(f"Character info: {parsed_character_info}")
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

def read_and_filter_jsonl(input_file, output_file):
    non_null_data = []
    with open(input_file ,"r") as data_file:
        for line in data_file:
            data=json.loads(line)
            keys_to_delete = [key for key, value in data.items() if value is None]
            for key in keys_to_delete:
                del data[key] 
            non_null_data.append(data)
    # 将处理过的数据写入到新的文件中
    with open(output_file, 'w') as output_file:
        for data in non_null_data:
            output_file.write(json.dumps(data))
            output_file.write("\n")  # 为每个JSON对象添加新的一行

def analyze_fields(file_name, fields = ["personality", "role"]):
    counters = {field: Counter() for field in fields}
    
    with open(file_name, 'r') as data_file:
        for line in data_file: 
            data = json.loads(line)
            for field in fields:
                if field in data and data[field] is not None: # 检查字段是否存在并且不为None
                    counters[field][data[field]] += 1  # 计数器累加
    with open('log.txt', 'a+') as output_file:
        for field in fields:
            print(f"\nAnalysis for field: {field}", file=output_file)
            for key, count in counters[field].most_common():  # 排序输出
                print(f"{key}: {count}", file=output_file)
    plot_counters(counters)

def plot_counters(counters):
    for field, counter in counters.items():
        labels, values = zip(*counter.items())

        # 绘制出bar图
        plt.figure(figsize=(10,5))
        plt.bar(labels, values)

        # 添加标题和标签
        plt.title(f'{field.capitalize()} Distribution')
        plt.xlabel(field)
        plt.ylabel('Count')

        # 显示图形
        plt.show()

# # 假设我们有两个Counter对象
# counters = {
#     'personality': Counter({'cheerful': 235, 'mysterious': 210, 'calm': 200, 'shy': 185, 'bold': 180}),
#     'role': Counter({'main character': 600, 'side character': 540, 'supporting character': 400, 'antagonist': 317}),
# }

# plot_counters(counters)

def analyze_and_plot_fields(input_file, fields):
    # 建立 Counter 对象来统计每个字段
    counters = {field: Counter() for field in fields}

    with open(input_file, 'r') as data_file:
        for line in data_file:
            data = json.loads(line)
            for field in fields:
                if field in data and data[field] is not None:
                    # 分割由逗号分隔的属性，并更新 Counter
                    attributes = data[field].split(",")
                    counters[field].update(attr.strip() for attr in attributes)
    with open('log.txt', 'w') as output_file:
        for field in fields:
            print(f"\nAnalysis for field: {field}", file=output_file)
            for key, count in counters[field].most_common():  # 排序输出
                print(f"{key}: {count}", file=output_file)
    # 对于每个字段，创建一个条形图
    for field in fields:
        labels, values = zip(*counters[field].most_common())
        
        # 设置我们想要的刻度数量
        num_ticks = 100

        # 计算每个刻度之间的间隔
        distance_between_ticks = len(labels) // num_ticks

        plt.figure(figsize=(10,5))
        plt.bar(labels, values)

        # 设置x轴刻度和标签
        plt.xticks(np.arange(0, len(labels), distance_between_ticks), rotation=90)

        plt.title(f'Distribution of {field}')
        plt.xlabel(field)
        plt.ylabel('Count')
        plt.show()

if __name__ == "__main__":
    # asyncio.run(main())
    read_and_filter_jsonl("output_test.jsonl", "output_filter.jsonl")
    analyze_and_plot_fields("output_filter.jsonl", ['personality', 'role'])
