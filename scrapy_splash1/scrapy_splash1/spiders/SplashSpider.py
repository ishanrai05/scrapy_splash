from scrapy.spiders import Spider
from ..items import MapItem
from scrapy_splash import SplashRequest

import json

class MySpider(Spider):
    name = "jsscraper"

    url_list = ["https://www.google.com/maps/place/I.S.B.T.+Kashmere+Gate/@28.6687121,77.2281838,17z/data=!4m7!3m6!1s0x390cfd07c389825f:0x3fb8c05f034fcac8!6m1!1v5!8m2!3d28.6687074!4d77.2303778/",]

    map_data = {
        'Destination':'',
        'Time':'',
    }

    map_list = []

    def start_requests(self):
        for url in self.url_list:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                args={"wait":3},
                endpoint='render.html'
            )

    def parse(self, response):
        for q in response.css("div.section-common-line-headsign-time"):
            mapItem = MapItem()
            mapItem["item1"] = q.css(".section-common-line-headsign::text").extract_first()
            mapItem["item2"] = q.css(".section-common-line-time::text").extract_first()
            self.map_data['Destination'] = mapItem["item1"]
            self.map_data['Time'] = mapItem["item2"]
            self.map_list.append(self.map_data.copy())
            with open("data_file.json","w") as f:
                json.dump(self.map_list,f)
            yield mapItem
