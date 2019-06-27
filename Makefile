CRAWL = scrapy crawl

REPO = brand product product_info article
CORPUS = article_styleme article_pixnet article_pixnet_post
TARGETS = $(REPO) $(CORPUS)

.PHONY: all $(TARGETS)

# .NOTPARALLEL:

all:
	make $(TARGETS)

repo:
	make $(REPO)

corpus:
	make $(CORPUS)

$(TARGETS):
	$(CRAWL) $@
