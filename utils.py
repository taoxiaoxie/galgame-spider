import json
import os
import glob
import re
from datetime import datetime

def rename_json_files(dir_path):
    # 获取指定目录下所有以.json结尾的文件
    json_files = glob.glob(os.path.join(dir_path, '*.json'))

    # 按照文件名排序
    json_files.sort()

    # 重命名文件
    for i, file_path in enumerate(json_files, start=1):
        try:
            dir_name, _ = os.path.split(file_path)
            new_name = f"{i}.json"
            new_path = os.path.join(dir_name, new_name)
            os.rename(file_path, new_path)
            print(f"Renamed {file_path} to {new_path}")
        except:
            pass
def remove_consecutive_commas(s):
    # 匹配两个或更多连续的逗号，可能有空格或换行符
    pattern = re.compile(r',\s*,')
    # 用一个逗号替换匹配到的内容
    return pattern.sub(',', s)

def deprecated_load_all_character_name_and_id():
    dir_path = "visual-novels/VNDB"
    json_file_name = [i for i in os.listdir(dir_path) if i.endswith(".json")]
    json_file_path_list = [os.path.join(dir_path, i) for i in json_file_name]

    combined_json_str = "{"
    for json_file_path in json_file_path_list:
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                # 读取文件内容并去掉开头和结尾的花括号
                file_content = f.read().strip()
                if file_content.startswith("{"):
                    file_content = file_content[1:]
                if file_content.endswith("}"):
                    file_content = file_content[:-1]
                combined_json_str += file_content + ","
        except Exception as e:
            print(f"Error processing file {json_file_path}: {e}")
    # 去掉最后一个逗号并添加闭花括号
    if combined_json_str.endswith(","):
        combined_json_str = combined_json_str[:-1]
    combined_json_str += "}"
    # combined_json_str = remove_consecutive_commas(combined_json_str)
    print(combined_json_str)
    with open("name_and_id.json", "w", encoding="utf-8") as f:
        f.write(combined_json_str)
    # 解析合并后的JSON字符串
    try:
        character_name_and_id = json.loads(combined_json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding combined JSON: {e}")
        character_name_and_id = {}

    return character_name_and_id

def load_all_character_name_and_id():
    json_path = "name_and_id.json"
    return json.load(open(json_path, "r", encoding="utf-8"))

def get_current_time():

    # Get current date and time
    now = datetime.now()

    # Format it in the HTTP date format
    http_date = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return http_date

if __name__ == "__main__":
    character_name_and_id = load_all_character_name_and_id()
    print(character_name_and_id)
    print(len(character_name_and_id))

