'''
Desc:
File: /infra/utils/driver.py
File Created: Monday, 17th July 2023 12:01:07 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2023 Camel Lu
'''
import json
import logging

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_request_header_key(entry_url, host, request_header_key, mime_type="json"):
    capabilities = DesiredCapabilities.CHROME
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(options=chrome_options,
                              desired_capabilities=capabilities,)
    driver.get(entry_url)
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    # with open('./logs.json', 'w', encoding='utf-8') as f:
    #     json.dump(logs, f, ensure_ascii=False, indent=2)
    #     f.close()
    for log in logs:
        flag = log["method"] == "Network.requestWillBeSentExtraInfo" and host
        headers = log["params"].get('headers')
        request_header_key_value = headers.get(
            request_header_key) if headers else None
        host_url = headers.get('Host') if headers else None
        if flag and request_header_key_value and host_url in host:
            driver.quit()
            line = f'此次爬取{request_header_key}: {request_header_key_value} '
            logging.info(line)
            return request_header_key_value
    driver.quit()

