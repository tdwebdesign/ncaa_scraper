import scrapy
import json
from ..items import TeamItem


class FootballFbsSpider(scrapy.Spider):
    name = "football_fbs"
    allowed_domains = ["www.ncaa.com", "data.ncaa.com"]
    start_urls = ["https://www.ncaa.com/scoreboard/football/fbs/2022"]

    def parse(self, response):
        # Extract all instances of information from the desired tag
        weeks = response.css('span.scoreboardDateNav-dayNumber::text').getall()
        
        # Process or use the extracted data
        for week in weeks:
            # Concatenate the extracted data with the starting URL
            url = f"https://www.ncaa.com/scoreboard/football/fbs/2022/{week}"
            yield scrapy.Request(url, callback=self.parse_specific_week)
            
    def parse_specific_week(self, response):
        print("Parsing URL:", response.url) # for debugging purposes
        links = response.css('a.gamePod-link::attr(href)').getall()
        for link in links:
            url = "https://data.ncaa.com/casablanca" + link + "/pbp.json"
            yield scrapy.Request(url, callback=self.parse_game)

    def parse_game(self, response):
        print("Parsing URL:", response.url) # for debugging purposes
        data = json.loads(response.body)
        for team in data['meta']['teams']:
            item = TeamItem()
            item['table'] = 'teams'
            item['id'] = team['id']
            item['name'] = team['shortname']
            item['abbr'] = team['sixCharAbbr']
            item['color'] = team['color']
            item['seoName'] = team['seoName']
            '''
            if team['homeTeam'] == 'true':
                item['table'] = 'home'
            else:
                item['table'] = 'away'
            
            '''
            
            yield item
