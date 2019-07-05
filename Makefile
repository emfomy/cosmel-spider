CRAWL = scrapy crawl

STYLEME_REPO = \
	styleme_brand_meta \
	styleme_brand_merge \
	styleme_brand_alias \
	styleme_product_meta \
	styleme_product_info \
	styleme_article_meta_product \
	styleme_article_meta_category

STYLEME_CORPUS = \
	styleme_article_body_styleme \
	styleme_article_body_pixnet \
	styleme_article_body_pixnet_post

TARGETS = $(STYLEME_REPO) $(STYLEME_CORPUS)

.PHONY: all $(TARGETS)

# .NOTPARALLEL:

all: styleme

styleme:
	make $(STYLEME_REPO) $(STYLEME_CORPUS)

styleme_repo:
	make $(STYLEME_REPO)

styleme_corpus:
	make $(STYLEME_CORPUS)

$(TARGETS):
	$(CRAWL) $@
