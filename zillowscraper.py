import requests
from bs4 import BeautifulSoup
import csv

class ZillowScraper:
    results = []

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'zguid=23|%24da68f92a-f77b-4bbf-84eb-7a2d31f99348; zgsession=1|e154723f-eda6-4c7e-aa89-969dd007ea52; zjs_user_id=null; zjs_anonymous_id=%22da68f92a-f77b-4bbf-84eb-7a2d31f99348%22; _pxvid=74bd9456-50ff-11ea-9220-0242ac12000d; _px3=3e657262b4821b2e7310db816406f98cbd22dd58d96756a381cb8c984ecfa0f5:esQsQEGRcqE7rD6eTHDFJf5Ph2jck1vLq1csLqFMTbjt4Lm+3bJIzpMQ6k9+jd3Bm9kExUdRHx/imqKGRjYogA==:1000:OxpoXHWx1IG/n/gawOdzUqtQb2ByjF4J5a5IE5urD0g1jztV4/Pimx/nN2HkfaGL1Wq0LSGSzl+FaaXh+L8eNBJKCVYxycWJQtvCRG8DCdnbQawZOR9Qq7uOSCfY63dso90X/I5SnwGGJW5t6L/SpqzRHivwrMtQEOO8c7OnyEE=; search=6|1584507320094%7Crect%3D47.766391745664386%252C-122.11099270458982%252C47.4594955013178%252C-122.57859829541013%26rid%3D16037%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D0%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%09%01%0999562%09%09%09%090%09US_%09',
        'pragma': 'no-cache',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

    }
    def fetch(self, url, params):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url, params=params, headers=self.headers)
        print(' | Status code: %s' % res.status_code)
        
        return res
   
    def save_response(self, res):
        with open('res.html', 'w') as html_file:
            html_file.write(res)

    def load_response(self):
        html = ''
        
        with open('res.html', 'r') as html_file:
            for line in html_file:
                html += line
        
        return html
   
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        cards = content.findAll('article', {'class': 'list-card'})
        
        for card in cards:
            try:
                ba = card.find('ul', {'class': 'list-card-details'}).findAll('li')[1].text.split(' ')[0]
            except:
                ba = 'N/A'
            
            try:
                sqft = card.find('ul', {'class': 'list-card-details'}).findAll('li')[2].text.split(' ')[0]
            except:
                sqft = 'N/A'
            
            try:
                image = card.find('img')['src']
            except:
                image = 'N/A'

            self.results.append({
                'price': card.find('div', {'class': 'list-card-price'}).text,
                'address': card.find('address', {'class': 'list-card-addr'}).text,
                'bds': card.find('ul', {'class': 'list-card-details'}).findAll('li')[0].text.split(' ')[0],
                'ba': ba,
                'sqft': sqft,
                'image': image
            })
    
    def to_csv(self):
        with open('zillow.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
        
    def run(self):
        for page in range(1, 5):
            params = {
                'searchQueryState': '{"pagination":{"currentPage":%s},"usersSearchTerm":"Seattle, WA","mapBounds":{"west":-122.57859829541013,"east":-122.11099270458982,"south":47.4594955013178,"north":47.766391745664386},"mapZoom":11,"regionSelection":[{"regionId":16037,"regionType":6}],"isMapVisible":false,"filterState":{"sortSelection":{"value":"globalrelevanceex"}},"isListVisible":true}' % page
            }

            
            res = self.fetch('https://www.zillow.com/homes/for_sale/Seattle,-WA_rb/', params)
            self.parse(res.text)

        self.to_csv()
        

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()



