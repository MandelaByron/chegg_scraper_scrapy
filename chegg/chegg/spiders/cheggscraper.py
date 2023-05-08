import scrapy
from urllib.parse import urlencode
from .get_urls import get_question_links
from selectolax.parser import HTMLParser

API_KEY = '848b01434fc3b4899dc4ca9628acbb85'
def get_scraperapi_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

url='https://www.chegg.com/homework-help/questions-and-answers/physics-archive-2023-january-01'

url_data = get_question_links(main_page_url=url)
class CheggscraperSpider(scrapy.Spider):
    name = 'cheggscraper'
    allowed_domains = ['chegg.com']

    
    def start_requests(self):
        for url in url_data:
            meta={
                'url':url
            }
            link=get_scraperapi_url(url)
            yield scrapy.Request(url=link, callback=self.parse, meta=meta)
            
    def parse(self, response):
        
        tree = HTMLParser(response.text)
        try:
            ele=tree.css_first('div.styled__KatexContent-sc-1k7k16x-5.jfeNFX').text()
        except AttributeError:
            #//div[@class="styled__QuestionBody-sc-1f9k7g9-2 cYjKgc"]/p
            try:
                ele=tree.css_first('div.styled__QuestionBody-sc-1f9k7g9-2.cYjKgc p').text()
            except AttributeError:
                ele=tree.css_first('div#mobile-question-style').text()
            except:
                ele = tree.css_first('div.styled__TextContent-sc-1k7k16x-4.dyKhdh')    
            
        except:
            ele = tree.css_first('div#mobile-question-style').text()


        items = {
            'question':ele,
            'link':response.meta.get('url')
        }

        yield items