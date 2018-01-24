from scrapy.cmdline import execute
# execute(['scrapy', 'crawl', 'amazon','--nolog'])
# execute(['scrapy', 'crawl', 'amazon',])


#scrapy crawl amazon -a keyword=iphone8手机
execute(['scrapy', 'crawl', 'amazon','-a','keyword=iphone8手机',])
# execute(['scrapy', 'crawl', 'baidu',])
# execute(['scrapy', 'crawl', 'baidu','--nolog'])
