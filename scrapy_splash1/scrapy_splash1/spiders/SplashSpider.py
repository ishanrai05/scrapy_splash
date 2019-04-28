from scrapy.spiders import Spider
from ..items import MapItem
from scrapy_splash import SplashRequest

import json

class MySpider(Spider):
    name = "jsscraper"

    url_list = ["https://www.google.com/maps/place/I.S.B.T.+Kashmere+Gate/@28.6687121,77.2281838,17z/data=!4m7!3m6!1s0x390cfd07c389825f:0x3fb8c05f034fcac8!6m1!1v5!8m2!3d28.6687074!4d77.2303778/",
    "https://www.google.com/maps/place/Anand+Vihar+ISBT+Terminal/@28.6458568,77.3125006,17z/data=!4m7!3m6!1s0x390cfb3988225935:0xa69f33f024f392d9!6m1!1v5!8m2!3d28.6458521!4d77.3146893"
    ]

    lines = {}

    map_data = {
        'exeptions':[],
        'from':'I.S.B.T. Kashmere Gate',
        'services': [
                    'Mo-Sa'
                ],
        'stations': [],
        'time':[],
        'to':''
    }

    map_list =  {
        'start_date': '2017-11-01',
        'end_date': '2020-10-31',
        'updated': '2017-11-27',
        'lines': {}
    }

    def start_requests(self):
        for url in self.url_list:
            yield SplashRequest(
                url=url,
                callback=self.parse,
                args={"wait":3},
                endpoint='render.html'
            )

    def parse(self, response):
        for j in response.css("div.section-listbox-root"):
            mapItem = MapItem()
            mapItem['from_'] = j.css('.section-header-title::text').extract_first()
            for q in response.css("div.section-line-local"):
                
                # print (q)
                
                mapItem["to"] = q.css(".section-common-line-headsign::text").extract_first()
                mapItem["time"] = q.css(".section-common-line-time::text").extract_first()
                mapItem["lines"] = q.css(".renderable-component-text-box-content::text").extract_first()
                self.map_data['from'] = mapItem['from_']
                self.map_data['stations']= [mapItem['from_'], mapItem["to"]]
                self.map_data['to'] = mapItem['to']
                dtime = [mapItem["time"], '10:27 am']
                self.map_data['time'] = [dtime]
                # Automate it
                # self.map_data['lines'] = mapItem["lines"]
                if mapItem['lines'] not in self.lines:
                    self.lines[mapItem['lines']] = self.map_data.copy()
                else:
                    self.lines[mapItem['lines']]['time'].append(dtime)
                self.map_list['lines'] = self.lines
                with open("schedule.json","w") as f:
                    json.dump(self.map_list,f, indent=4)
                yield mapItem
