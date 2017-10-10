import scrapy


class AlbumSpider(scrapy.Spider):

    name = 'album_reviews'

    custom_settings = {
        #"DOWNLOAD_DELAY": 3,
        #"CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
        # can get rid of DOWNLOAD_DELAY and CONCURRENT_REQUESTS_PER_DOMAIN to run faster
    }

    #base = 'https://pitchfork.com/reviews/albums/?page='
    start_urls = ['https://pitchfork.com/reviews/albums/?page=' + str(x) for x in range(1,1700)]

    def parse(self, response):
        for href in response.xpath('//a[@class="album-link"]/@href').extract():
            yield scrapy.Request(
                url='https://pitchfork.com' + href,
                callback=self.parse_album,
                meta={'url': href}
            )


    def parse_album(self, response):


        a = response.xpath('//ul[@class="artist-links artist-list"]//li//a/text()')
        if a:
            artist = a.extract()[0]
        else:
            artist = "None"


        al = response.xpath('//h1[@class="review-title"]/text()')
        if al:
            album = al.extract()[0]
        else:
            album = "None"


        p = response.xpath('//time[@class="pub-date"]/@datetime')
        if p:
            pub_date = p.extract()[0]
        else:
            pub_date = "None"


        s = response.xpath('//span[@class="score"]/text()')
        if s:
            score = s.extract()[0]
        else:
            score = "None"


        l = response.xpath('//li[@class="labels-list__item"]/text()')
        if l:
            label = l.extract()[0]
        else:
            label = "None"


        ye = response.xpath('//span[@class="year"]/text()')
        if ye:
            year = ye.extract()[3]
        else:
            year = "None"


        au = response.xpath('//a[@class="authors-detail__display-name"]/text()')
        if au:
            author = au.extract()[0]
        else:
            author = "None"


        at = response.xpath('//span[@class="authors-detail__title"]/text()')
        if at:
            author_title = at.extract()[0]
        else:
            author_title = "None"


        g = response.xpath('//a[@class="genre-list__link"]/text()')
        if g:
            genre = g.extract()[0]
        else:
            genre = "None"


        w = (response.xpath('//div[@class="contents dropcap"]//text()').extract())
        word_count = 0
        for y in w:
            word_count += len(y.split())


        b = response.xpath('//p[@class="bnm-txt"]/text()')
        if b:
            bnm = b.extract()[0]
        else:
            bnm = 'None'


        yield {
            'artist': artist,
            'album': album,
            'publish_date': pub_date,
            'score': score,
            'label': label,
            'year': year,
            'author': author,
            'author_title': author_title,
            'genre': genre,
            'word_count': word_count,
            'bnm': bnm
            }
