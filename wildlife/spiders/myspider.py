import json

import scrapy
from scrapy.http import JsonRequest

speciesManagement = [
    "Algae", "Coastal Pelagic Species (CPS)", "Groundfish",
    "Highly Migratory Species (HMS)", "Inland State Managed Species",
    "Marine State Managed Fish", "Marine State Managed Invertebrates",
    "Nearshore Fishery Management Plan Species", "Other", "Salmon"
]


class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://mfde.wildlife.ca.gov']

    def start_requests(self):
        url = 'https://mfde-api.wildlife.ca.gov/api/landing/CustomQuery'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://mfde.wildlife.ca.gov',
            'Referer': 'https://mfde.wildlife.ca.gov/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }

        for year in range(1989, 2024):
            start_date = f"01{year}"
            end_date = f"12{year}"
            for specieManagement in speciesManagement:
                data = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'speciesManagement': specieManagement,
                    'port': 'Crescent City'
                }
                payload = {
                    "columns": {
                        "year": True,
                        "month": False,
                        "speciesManagement": False,
                        "speciesGroup": False,
                        "speciesName": False,
                        "blockCode": False,
                        "portArea": False,
                        "port": False,
                        "gearGroup": False,
                        "use": False,
                        "condition": False
                    },
                    "filters": {
                        "startDate": start_date,
                        "endDate": end_date,
                        "speciesManagement": [specieManagement],
                        "speciesGroup": [],
                        "speciesName": [],
                        "blockCode": [],
                        "blockCodeMinRange": "",
                        "blockCodeMaxRange": "",
                        "portArea": [],
                        "port": [201],
                        "gearGroup": [],
                        "use": [],
                        "condition": []
                    }
                }
                yield JsonRequest(url=url, data=payload, headers=headers, callback=self.parse, meta={'data': data})

    def parse(self, response):
        # Extract the passed data from the meta
        data = response.meta['data']
        try:
            json_response = json.loads(response.text)
            # print(json_response[0])
            data['pounds'] = json_response[0]['l']
            data['value'] = "${}".format(json_response[0]['v'])
        except json.JSONDecodeError as e:
            self.log(f"Error decoding JSON: {e}")
            return
        # # print(response.text)
        # json_data=json.loads(response.text)
        # print(json_data)
        # # input()
        #
        yield data

