# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from decouple import config


class TeamPipeline:
    def open_spider(self, spider):
        hostname = config('HOSTNAME')
        port = config('PORT')
        username = config('USERNAME')
        password = config('PASSWORD')
        database = config('DATABASE')
        self.connection = psycopg2.connect(host=hostname, port=port, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if item['table'] == 'teams':
            self.cur.execute("SELECT * FROM teams WHERE id = %s", (item['id'],))
            result = self.cur.fetchone()
            if result:
                print(f"Item with id {item['id']} already exists. Skipping...")
            else:
                self.cur.execute("INSERT INTO teams (id, name, abbr, color, seo_name) VALUES (%s, %s, %s, %s, %s)", \
                    (item['id'], item['name'], item['abbr'], item['color'], item['seoName']))
                self.connection.commit()
        if item['table'] == 'games':
            self.cur.execute("SELECT * FROM games WHERE id = %s", (item['id'],))
            result = self.cur.fetchone()
            if result:
                print(f"Item with id {item['id']} already exists. Skipping...")
            else:
                self.cur.execute("INSERT INTO games (id, season, week, home, away) VALUES (%s, %s, %s, %s, %s)", \
                    (item['id'], item['season'], item['week'], item['home'], item['away']))
                self.connection.commit()
        return item
