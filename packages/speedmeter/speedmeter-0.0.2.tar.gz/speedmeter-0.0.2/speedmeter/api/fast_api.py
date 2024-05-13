import re

import requests


def get_dl_urls(url_count):
    token = get_fast_token()
    # url = f"{http_protocol}://api.fast.com/netflix/speedtest?https={UseHTTPS}&token={token}&urlCount={url_count}"
    url = f"https://api.fast.com/netflix/speedtest/v2?https=true&token={token}&urlCount={url_count}"

    response = requests.get(url)
    response.raise_for_status()

    re_urls = response.json()
    client = re_urls["client"]

    return [url["url"] for url in re_urls["targets"]], client


def get_fast_token():
    base_url = "https://fast.com"
    fast_body = requests.get(base_url).text

    script_names = re.findall("app-.*\\.js", fast_body)[:1]
    script_url = f"{base_url}/{script_names[0]}"
    script_body = requests.get(script_url).text

    token_match = re.search(r'token:"([a-zA-Z0-9]+)"', script_body)
    if token_match:
        token = token_match.group(1)
        return token
    else:
        return ""
