CRAWL = scrapy crawl

REPO = brand_meta brand_merge brand_alias product_meta product_info article_meta_product article_meta_category
CORPUS = article_body_styleme article_body_pixnet article_body_pixnet_post
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
