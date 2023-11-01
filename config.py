HEADERS = {
    "Content-Encoding": "gzip",
    "Content-Security-Policy": "default-src 'none'; connect-src 'self' https://api.vndb.org; img-src *; script-src https://*.vndb.org; style-src 'unsafe-inline' https://vndb.org https://*.vndb.org; form-action 'self'; frame-ancestors 'none'",
    "Content-Type": "text/html; charset=UTF-8",
    "Date": "Fri, 27 Oct 2023 11:59:54 GMT",
    "Server": "nginx",
    "Strict-Transport-Security": "max-age=63072000; includeSubdomains; preload",

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Cookie": "vndb_samesite=1",
    "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="118", "Google Chrome";v="118"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "Windows",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

CHARACTER_INFO_TEMPLATE = {
    "id": None,
    "name": None,
    "aliases": None,
    "measurements": None,
    "birthday": None,
    "hair": None,
    "eyes": None,
    "body": None,
    "clothes": None,
    "items": None,
    "personality": None,
    "role": None,
    "engages_in": None,
    "subject_of": None,
    "visual_novels": None,
    "voiced_by": None,
    "description": None,
}

# coroutine_limit
COROUTINE_LIMIT = 10
# 请求间隔
REQUEST_INTERVAL = 0.3

MAX_TIME_OUT = 10

RATE_LIMIT_WAIT_TIME = 10

EXCEPTION_WAIT_TIME = 5