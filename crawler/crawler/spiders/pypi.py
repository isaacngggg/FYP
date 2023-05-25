
from scrapy.linkextractors import LinkExtractor
from crawler.items import pypiItem

from scrapy.spiders import CrawlSpider, Rule
from . import normalise
import re

class pypiSpider(CrawlSpider):
    name = "pypi"
    allowed_domains = ["pypi.org","github.com"]
    start_urls = ["https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3"]

    rules = (
    #     Rule(LinkExtractor(allow = ('.*pypi.org/project/.*')), callback ='parse'),
         Rule(LinkExtractor(allow = ('.*pypi.org/search.*')),callback='parse'),
         )

    def parse(self, response):
        print ('parsing')
        response.css(".package-snippet").css('a::attr(href)').get()
        libraries = response.css(".package-snippet").css('a::attr(href)').getall()

        for link in libraries:
            # Extract link for each listing
            #link =
            # Follow the link and parse the individual page
            yield response.follow(link, self.parseLibary)

        # Follow the next page link if available
        
        # paginationlink = response.css ('.button button-group__button').getall()
        # response.xpath('/html/body/main/div/div/div[2]/form/div[3]/div/a[5]/@href').get()
        # for i in range(0,len(sidebartexts)):
        #     n = i+1
        #     if sidebartexts[n] == 'Project Links':
        #         item['homepage'] = response.css ('.sidebar-section:nth-child(' + n + ')').css('a::attr(href)').get()
        
        next_page = response.xpath('/html/body/main/div/div/div[2]/form/div[3]/div/a[5]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parseLibary(self, response):
        # Parse each quote div 
        item=pypiItem()
        item['title'] = response.css('meta[property="og:title"]::attr(content)').get()
        item['description'] = response.css('meta[name="description"]::attr(content)').get()
        item['installMethod'] = response.css ('#pip-command::text').get()
        
        #gitStarPage = response.css('a[data-github-repo-info-target="stargazersUrl"]').get()
        #if next_page:
        #    yield response.follow(next_page, self.parse)
        #sidebartexts = response.css ('.sidebar-section').css('h3::text').getall()
        #for i in range(0,len(sidebartexts)):
             #n = i+1
             #if sidebartexts[n] == 'Project Links':
                 #item['homepage'] = response.css ('.sidebar-section:nth-child(' + n + ')').css('a::attr(href)').get()
                
            # if sidebartexts[n] == 'Statistics':
            #     item['gitHubStar'] = response.css ('.sidebar-section:nth-child(' + n + ')').css('h3::text').getall()
        
        #response.css('a[data-github-repo-info-target="forksUrl"]').get()
        #response.css ('.sidebar-section:nth-child(2)').css('a::attr(href)').get()
        
        item['normalisedDescription'] = normalise(item['description'])
        item['url'] = response.url
        item['spider'] = self.name
        noGit = True
        hrefs = response.css("a::attr(href)").getall()
        # Process the extracted href values
        for href in hrefs:
            # Apply regular expression to extracted href value
            match = re.search(r".*github\.com\/.*\/.*", href)
            if match:
                # if re.match(r".*github\.com\/.*\/.*\/.*",str(href)):
                #     print("No good value:", href)
                #     break
                
                print("Extracted value:", href)
                item['gitHub'] = href
                noGit = False
                yield response.follow(href,self.parseStar,meta = {'item': item})
        if noGit == True:
            yield item
        
    def parseStar(self, response):
        item = response.meta['item']
        item['gitHubStar'] = int(response.css("span[id='repo-stars-counter-star']::attr(title)").get())
        yield item
"""
 scrapy shell -s ROBOTSTXT_OBEY=False "https://pypi.org"
 fetch('https://pypi.org/search/?c=Programming+Language+%3A%3A+Python+%3A%3A+3')
 libraries = response.css(".package-snippet").css('a::attr(href)').get()
 def parseLibary(self, response): response.css('meta[property="og:title"]::attr(content)').get()
 response.follow(libraries, response.css('meta[property="og:title"]::attr(content)').get())
 
 response.css ('.sidebar-section:nth-child(2)').css('a::attr(href)').get()
 
 response.css('.vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed::attr(href)').getall()
 response.css('.vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed').getall()
 vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed
 """