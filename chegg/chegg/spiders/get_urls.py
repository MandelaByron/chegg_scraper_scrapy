import httpx
from lxml import etree
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import itertools
import pandas as pd

API_KEY = '848b01434fc3b4899dc4ca9628acbb85'

proxies = {
    'http://' : f"http://scraperapi.premium=true:{API_KEY}@proxy-server.scraperapi.com:8001"
}

headers = {
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}



def get_question_links(main_page_url):
    question_links=[]
    with httpx.Client(timeout=120) as client:
        
        for i in itertools.count(1):
            link=str(main_page_url)+f"?page={i}"
            print(link)
            payload = {'api_key': f'{API_KEY}', 'url': link}
            response=client.get('http://api.scraperapi.com',params=payload)
            print("----status_code---" ,response.status_code)
            
            tree = HTMLParser(response.text)
            ele = tree.css('div.txt-body.question-body a:nth-child(1)')
            print('---questions---',len(ele))
            if len(ele) == 0:
                break
            for i in ele:
                question_link='https://www.chegg.com' + i.attributes['href']
                question_links.append(question_link)
    return question_links

# def parse_questions(list_url):
#     #url='https://www.chegg.com/homework-help/questions-and-answers/problem-438-quarks-carry-spin-1-2--three-quarks-bind-together-make-baryon-proton-neutron-t-q107102122'
#     data=[]
#     with httpx.Client(timeout=120) as client:
#         unprocessed_urls=[]
#         for url in list_url:
#             print(url)
#             payload = {'api_key': f'{API_KEY}', 'url': url,'premium':'true'}
#             response=client.get('http://api.scraperapi.com',params=payload)
#             print(response.status_code)
#             if str(response.status_code) == "500":
#                 unprocessed_urls.append(url)
#                 continue
#             tree = HTMLParser(response.text)
#             try:
#                 ele=tree.css_first('div.styled__KatexContent-sc-1k7k16x-5.jfeNFX').text()
#             except AttributeError:
#                 #//div[@class="styled__QuestionBody-sc-1f9k7g9-2 cYjKgc"]/p
#                 try:
#                     ele=tree.css_first('div.styled__QuestionBody-sc-1f9k7g9-2.cYjKgc p').text()
#                 except:
#                     ele=tree.css_first('div#mobile-question-style').text()
                
#             except:
#                 ele = tree.css_first('div#mobile-question-style').text()

#             #print(ele)
#             items={
#                 'question':ele,
#                 'link':url
#             }
#             print(items)
#             data.append(items)
#         for url in unprocessed_urls:
#             print(url)
#             payload = {'api_key': f'{API_KEY}', 'url': url,'premium':'true'}
#             response=client.get('http://api.scraperapi.com',params=payload)
#             print(response.status_code)
#             if str(response.status_code) == "500":
#                 unprocessed_urls.append(url)
#                 continue
#             tree = HTMLParser(response.text)
#             try:
#                 ele=tree.css_first('div.styled__KatexContent-sc-1k7k16x-5.jfeNFX').text()
#             except AttributeError:
#                 #//div[@class="styled__QuestionBody-sc-1f9k7g9-2 cYjKgc"]/p
#                 try:
#                     ele=tree.css_first('div.styled__QuestionBody-sc-1f9k7g9-2.cYjKgc p').text()
#                 except:
#                     ele=tree.css_first('div#mobile-question-style').text()
                
#             except:
#                 ele = tree.css_first('div#mobile-question-style').text()

#             #print(ele)
#             items={
#                 'question':ele,
#                 'link':url
#             }
#             print(items)
#             data.append(items)
            
#     return data

# question_links=get_question_links(main_page_url=url)
# question_yield=parse_questions(list_url=question_links)

# df=pd.DataFrame(question_yield)
# df.to_csv('physics-archive-2023-january-01.csv',index=False)