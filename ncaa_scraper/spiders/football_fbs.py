import scrapy
import json
from ..items import TeamItem, GameItem


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
            # extract the season from the url
            season = url.split('/')[-2]
            yield scrapy.Request(url, callback=self.parse_specific_week, meta={'week': week, 'season': season})
            
    def parse_specific_week(self, response):
        print("Parsing URL:", response.url) # for debugging purposes
        week = response.meta['week']
        season = response.meta['season']
        links = response.css('a.gamePod-link::attr(href)').getall()
        for link in links:
            url = "https://data.ncaa.com/casablanca" + link + "/pbp.json"
            # extract the game id from the link
            game_id = link.split('/')[-1]        
            yield scrapy.Request(url, callback=self.parse_game, meta={'week': week, 'season': season, 'game_id': game_id})

    def parse_game(self, response):
        print("Parsing URL:", response.url) # for debugging purposes
        week = response.meta['week']
        data = json.loads(response.body)

        for team in data['meta']['teams']:
            item = TeamItem()
            item['table'] = 'teams'
            item['id'] = team['id']
            item['name'] = team['shortname']
            item['abbr'] = team['sixCharAbbr']
            item['color'] = team['color']
            item['seoName'] = team['seoName']
            
            if team['homeTeam'] == 'true':
                home = team['id']
            else:
                away = team['id']
            
            yield item
        
        item = GameItem()
        item['table'] = 'games'
        item['id'] = response.meta['game_id']
        item['season'] = response.meta['season']
        item['week'] = response.meta['week']
        item['home'] = home
        item['away'] = away

        yield item
        
