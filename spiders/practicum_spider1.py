# These are the required packages need for this python file to run completely
import scrapy
from ..items import PracticumItem
from langdetect import detect
import requests
from scrapy_splash import SplashRequest

#This is the list of websites to be scraped
urlslist = [
    'https://www.mckinsey.com/industries/healthcare-systems-and-services/our-insights',
    'https://www.healthmanagement.com/knowledge-share/blog/',
    'https://www.brookings.edu/search/?s=healthcare',
    'https://www.kff.org/search/?s=healthcare&paged=&fs=search&s=healthcare',
    'https://eldercarematters.com/elder-care-senior-care-articles/'
    'https://californiahealthline.org/stories/'
    'https://www.politico.com/search/1?s=newest&q=healthcare',
    'https://khn.org/stories/',
    'https://www.nola.com/news/healthcare_hospitals/',
    'https://www.opportunitylouisiana.com/searchresult?indexCatalogue=myindex&searchQuery=healthcare&wordsMode=0'

]

#This is a dictionary that gets refferenced based on the article currently being scraped

select_dic = {'https://www.mckinsey.com/industries/healthcare-systems-and-services/our-insights': {
    'title': '//div[@class="contentwrapper"]//h1//text()',
    'body': '//article[@itemprop="articleBody"]//p/text()', \
    'author': "//div[@class='author-by-line']//a/text()", \
    'all_elements': "//div[@class='item']/div[@class='text-wrapper']", \
    'element_link': ".//a/@href", \
    'element_type': ".//span/text()", \
    'element_type_constraint': 'Collection', \
    'type': "//div/footer/span/text()", \
    'date': "//div/footer/time[@class='hero-article-info']/text()", \
    'inf_scroll': {'Type': 'build_request', \
                   'parameter_name1': 'ig_page',
                   'Parameters': {'UseAjax': 'true', \
                                  'PresentationId': '{225AFD08 - 2381 - 4FCD - B73F - F68A6859B4FC}', \
                                  'ds': '{F8382F15-08D4-458C-96F8-26623103604B}', \
                                  'showfulldek': 'False', \
                                  'hideeyebrows': 'False', \
 \
                                  },
                   'page_name': 'ig_page', \
 \
                   'page_start': 1}}, \
 \
              'https://www.healthmanagement.com/knowledge-share/blog/': {
                  'title': "//header[@class='entry-header']/h1/text()", \
                  'body': "//div[@class='entry-content']//p//text()", \
                  'author': "//span[@class='author-name']//text()", \
                  'all_elements': "//article", \
                  'element_link': ".//header/h2/a/@href", \
                  'element_type': ".//span/text()", \
                  'element_type_constraint': 'None', \
                  'type': "//h1[@class='page-title']//text()", \
                  'date': "//time/text()", \
                  'inf_scroll': {'Type': 'pagination', \
                                 'next_page': '//a[@class="nextpostslink"]/@href'}},

              'https://www.brookings.edu/search/?s=healthcare': {'title': "//div[@class='headline-wrapper']/h1/text()", \
                                                                 'body': "//div[@class='content-column']//p/text()", \
                                                                 'author': "//div[@class='expert-info']//span/text()", \
                                                                 'all_elements': "//div[@class='article-info']", \
                                                                 'element_link': "./h4/a/@href", \
                                                                 'element_type': "//none", \
                                                                 'element_type_constraint': 'None', \
                                                                 'type': "//div[@class='headline-wrapper']/a/text()", \
                                                                 'date': "//div[@class='headline-wrapper']//time/text()", \
                                                                 'Atwitter': "//div[@class='expert-info']/div[@class='contact']/a/@href", \
                                                                 'inf_scroll': {'Type': 'pagination', \
                                                                                'next_page': "//a[@class='load-more']/@href"}},

              'https://www.kff.org/search/?s=healthcare&paged=&fs=search&s=healthcare': {
                  'title': "//div[@class='box primary']/h2/text()", \
                  'body': "//div[@class='box full-post']//text()", \
                  'author': "//none", \
                  'all_elements': "//article", \
                  'element_link': ".//h5/a/@href", \
                  'element_type': "//none", \
                  'element_type_constraint': 'None', \
                  'type': "//none", \
                  'date': "//p[@class='byline']/span/text()", \
                  'Atwitter': "//none", \
                  'inf_scroll': {'Type': 'pagination', \
                                 'next_page': "//ul[@class='page-numbers']//a[@class='next page-numbers']/@href"}},

              'https://eldercarematters.com/elder-care-senior-care-articles/': {
                  'title': "//h1[@class='page-title cover-wrapper entry-title']/text()", \
                  'body': "//div[@class='content-box-inner']//text()", \
                  'author': "//span[@class='entry-author author vcard']/a/text()", \
                  'all_elements': "//div[@class='content-box-inner']", \
                  'element_link': ".//h3/a/@href", \
                  'element_type': "//none", \
                  'element_type_constraint': 'None', \
                  'type': "//none", \
                  'date': "//span[@class='entry-date']/text()", \
                  'Atwitter': "//none", \
                  'inf_scroll': {'Type': 'pagination', \
                                 'next_page': "//a[@class='next page-numbers']/@href"}},

              'https://californiahealthline.org/stories/': {'title': "//h1[@class='entry-title']/text()", \
                                                            'body': "//div[@class='article-body']//p/text()", \
                                                            'author': "//span[@class='byline']/a/strong/text()", \
                                                            'all_elements': "//div[@class='results-list-text']", \
                                                            'element_link': "./p/a/@href", \
                                                            'element_type': "//none", \
                                                            'element_title': "./p/a/text()", \
                                                            'element_type_constraint': 'None', \
                                                            'type': "/none", \
                                                            'date': "//time[@class='posted-on']/text()", \
                                                            'Atwitter': "//none", \
                                                            'inf_scroll': {'Type': 'pagination', \
                                                                           'next_page': "//li[@class='pagination-next']/a/@href"}},

              'https://www.politico.com/search/1?s=newest&q=healthcare': {'title': "//h2[@class='headline']/text()", \
                                                                          'body': "//p[@class=' story-text__paragraph']/text()", \
                                                                          'author': "//span[@class='vcard']/a/text()", \
                                                                          'all_elements': "//div[@class='summary']", \
                                                                          'element_link': "./header/h3/a/@href", \
                                                                          'element_type': "./header/p/text()", \
                                                                          'element_title': "./header/h3/a/text()", \
                                                                          'element_type_constraint': ['None'], \
                                                                          'type': "/none", \
                                                                          'date': "//p[@class='story-meta__timestamp']/time/@datetime", \
                                                                          'Atwitter': "//none", \
                                                                          'inf_scroll': {'Type': 'politico', \
                                                                                         'next_page': "//div[@class='contextual']//@href"},
                                                                          'page_type': {'Newsletter Entry': {
                                                                              'title': '//header/h1/text()', \
                                                                              'body': '//p/text()', \
                                                                              'author': '//p[@class="byline"]/a/text()', \
                                                                              'date': "//time[@itemprop='datePublished']/@datetime",
                                                                              'Atwitter': '//ul[@class="twitter-authors__list"]//li//text()',
                                                                              'type': '//none'},
                                                                                        'Playbook PlusNewsletter Entry': {
                                                                                            'title': '//header/h1/text()', \
                                                                                            'body': '//p/text()', \
                                                                                            'author': '//p[@class="byline"]/a/text()', \
                                                                                            'date': "//time[@itemprop='datePublished']/@datetime",
                                                                                            'Atwitter': '//ul[@class="twitter-authors__list"]//li//text()',
                                                                                            'type': '//none'}}},

              'https://khn.org/stories/': {'title': "//div[@class='header']/h1/text()", \
                                           'body': "//p/text()", \
                                           'author': "//span[@class='byline']/a/strong/text()", \
                                           'all_elements': "//div[@class='results-list-text']", \
                                           'element_link': "./p/a/@href", \
                                           'element_type': './/span[@class="type"]/text()', \
                                           'element_title': "./p/a/text()", \
                                           'element_type_constraint': ['None'], \
                                           'type': "//none", \
                                           'date': "//time/@datetime", \
                                           'Atwitter': "//none", \
                                           'inf_scroll': {'Type': 'pagination', \
                                                          'next_page': "//li[@class='pagination-next']/a/@href"},
                                           'page_type': {}},

              'https://www.nola.com/news/healthcare_hospitals/': {'title': "//h1[@itemprop='headline']/span/text()", \
                                                                  'body': "//p/text()", \
                                                                  'author': "//ul[@class='list-inline']/li/span/a/text()", \
                                                                  'all_elements': "//div[@class='card-body']", \
                                                                  'element_link': "./div/h2/a/@href", \
                                                                  'element_type': '//none', \
                                                                  'element_title': "./div/h2/a/text()", \
                                                                  'element_type_constraint': ['None'], \
                                                                  'type': "//none", \
                                                                  'date': "//time/@datetime", \
                                                                  'Atwitter': "//none", \
                                                                  'inf_scroll': {'Type': 'none', \
                                                                                 'next_page': "//li[@class='pagination-next']/a/@href"}, \
                                                                  'page_type': {'nonkey': 'blank'}},

              'https://www.opportunitylouisiana.com/searchresult?indexCatalogue=myindex&searchQuery=healthcare&wordsMode=0': {'title': "//h1/span/text()", \
                                                                  'body': "//div[@class='sfnewsContent sfcontent']//p/text()", \
                                                                  'author': "//none", \
                                                                  'all_elements': "//dt[@class='sfsearchResultTitle']", \
                                                                  'element_link': "./a/@href", \
                                                                  'element_type': '//none', \
                                                                  'element_title': "./a/text()", \
                                                                  'element_type_constraint': ['None'], \
                                                                  'type': "//none", \
                                                                  'date': "//time/@datetime", \
                                                                  'Atwitter': "//none", \
                                                                  'inf_scroll': {'Type': 'pagination', \
                                                                                 'next_page': "//div[@class='sf_pagerNumeric']/a[@class='sf_PagerCurrent']/following-sibling::a[1]/@href"}, \
                                                                  'page_type': {'nonkey': 'blank'}}

              }

for urls in urlslist:

    class p_spider1(scrapy.Spider):
        name = 'ps1'
        c = 1
        current_all_element = []
        politico = 0
        Article_type = {}

        def start_requests(self):

            yield scrapy.Request(url=urls, callback=self.parse_cover)

#Scrapes article list depending on cite
        def parse_cover(self, response):
            all_element = response.xpath(select_dic[urls]['all_elements'])
            if all_element != [] and all_element != p_spider1.current_all_element:
                p_spider1.current_all_element = all_element
                self.Article_type = {}
                for el in all_element:
                    link = el.xpath(select_dic[urls]['element_link']).extract()
                    # print(link)
                    if len(el.xpath(select_dic[urls]['element_type']).extract()) > 0:
                        self.Article_type[link[0]] = el.xpath(select_dic[urls]['element_type']).extract()[0]


                    # print(el.xpath(select_dic[urls]['element_title']).extract()[0])
                        if detect(el.xpath(select_dic[urls]['element_title']).extract()[0]) != 'es':

                            if self.Article_type[link[0]] not in select_dic[urls]['element_type_constraint']:
                                print(len(all_element))
                                yield response.follow(link[0], callback=self.parse)

                    else:
                        if detect(el.xpath(select_dic[urls]['element_title']).extract()[0]) != 'es':
                            yield response.follow(link[0], callback=self.parse)


#Selects pagination type based on cite
                if select_dic[urls]['inf_scroll']['Type'] == 'build_request':
                    p_spider1.c += 1
                    params = {'UseAjax': 'true',
                              'PresentationId': '{225AFD08 - 2381 - 4FCD - B73F - F68A6859B4FC}',
                              'ds': '{F8382F15-08D4-458C-96F8-26623103604B}',
                              'showfulldek': 'False',
                              'hideeyebrows': 'False',
                              'ig_page': p_spider1.c

                              }
                    # params =select_dic[urls]['inf_scroll']['Parameters']
                    # params[select_dic[urls]['inf_scroll']['parameter_name1']]=p_spider1.c
                    print('PAGE NUMBER >>>>>>', p_spider1.c,
                          '!!!!!<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                    print(params)
                    yield scrapy.FormRequest(url=urls, method='GET', formdata=params, callback=self.parse_cover)

                if select_dic[urls]['inf_scroll']['Type'] == 'pagination':

                    flink = response.xpath(select_dic[urls]['inf_scroll']['next_page']).extract()[0]
                    print('LETS GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO' + str(flink))
                    if flink != []:
                        yield response.follow(flink, callback=self.parse_cover)

                if select_dic[urls]['inf_scroll']['Type'] == 'politico':
                    next_link = response.xpath(select_dic[urls]['inf_scroll']['next_page']).extract()
                    flink = next_link[-1]
                    yield response.follow(flink, callback=self.parse_cover)

#Parses article page for Title, Author, Text, date, type
        def parse(self, response):
            link = response.request.url
            print(self.Article_type)
            if link in self.Article_type.keys():
                if self.Article_type[link] in select_dic[urls]['page_type'].keys():
                    print(
                        'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
                    sel_title = select_dic[urls]['page_type'][self.Article_type[link]]['title']
                    print(sel_title)
                    sel_body = select_dic[urls]['page_type'][self.Article_type[link]]['body']
                    print(sel_body)
                    sel_author = select_dic[urls]['page_type'][self.Article_type[link]]['author']
                    print(sel_author)
                    sel_date = select_dic[urls]['page_type'][self.Article_type[link]]['date']
                    sel_type = select_dic[urls]['page_type'][self.Article_type[link]]['type']
                    authlist_twit = select_dic[urls]['page_type'][self.Article_type[link]]['Atwitter']
                    title = response.xpath(sel_title).extract()
                    body = response.xpath(sel_body).extract()
                    author = response.xpath(sel_author).extract()
                    Article_type = response.xpath(sel_type).extract()
                    date = response.xpath(sel_date).extract()
                    Atwitter = []
                    if self.Article_type[link] == 'Newsletter Entry':
                        authlist = [x.upper() for x in response.xpath(authlist_twit).extract()]
                        print(authlist)
                        print(response.xpath(sel_author).extract()[0].upper())
                        author_space = response.xpath(sel_author).extract()[0].upper() + ' '
                        print(author_space)
                        if author_space in authlist:
                            twitindx = authlist.index(author_space)
                            print(twitindx)
                            indx = twitindx + 1
                            print(indx)
                            Atwitter = response.xpath(authlist_twit).extract()[indx:]
                            print(Atwitter)
                else:
                    sel_title = select_dic[urls]['title']
                    sel_body = select_dic[urls]['body']
                    sel_author = select_dic[urls]['author']
                    sel_type = select_dic[urls]['type']
                    Atwitter = response.xpath(select_dic[urls]['Atwitter']).extract()
                    title = response.xpath(sel_title).extract()
                    body = response.xpath(sel_body).extract()
                    author = response.xpath(sel_author).extract()
                    Article_type = response.xpath(sel_type).extract()
                    date = response.xpath(select_dic[urls]['date']).extract()
            else:
                sel_title = select_dic[urls]['title']
                sel_body = select_dic[urls]['body']
                sel_author = select_dic[urls]['author']
                sel_type = select_dic[urls]['type']
                Atwitter = response.xpath(select_dic[urls]['Atwitter']).extract()
                title = response.xpath(sel_title).extract()
                body = response.xpath(sel_body).extract()
                author = response.xpath(sel_author).extract()
                Article_type = response.xpath(sel_type).extract()
                date = response.xpath(select_dic[urls]['date']).extract()

            items = PracticumItem()
            titlemerge = ''
            bodymerge = ''
            for t in title:
                titlemerge = titlemerge + t
            for b in body:
                bodymerge = bodymerge + b
            if len(date) > 0:
                items['Article_Date'] = date[0]
            else:
                items['Article_Date'] = ''
            items['Article_url'] = response.request.url

            if len(Article_type) > 0:
                Article_type2 = Article_type[0].replace(' ', '')
                Article_type2 = Article_type2.replace('|', '')
                items['Article_Type'] = Article_type2
            else:
                items['Article_Type'] = ''

            items['Article_Title'] = titlemerge
            items['Article_Text'] = bodymerge
            if len(author) > 0:
                items['Article_Author'] = author[0]
            else:
                items['Article_Author'] = ''
            if len(Atwitter) > 0:
                items['ATwitter'] = Atwitter[0]
            else:
                items['ATwitter'] = ''

            yield items
