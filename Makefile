CRAWL = scrapy crawl

COSMEL_REPO = \
	cosmel_brand_styleme \
	cosmel_brand_alias \
	cosmel_product_styleme

STYLEME_REPO = \
	styleme_brand_meta \
	styleme_product_meta \
	styleme_product_info \
	styleme_article_meta_product \
	styleme_article_meta_category

STYLEME_CORPUS = \
	styleme_article_body_styleme \
	styleme_article_body_pixnet \
	styleme_article_body_pixnet_post

TARGETS = $(COSMEL_REPO) $(STYLEME_REPO) $(STYLEME_CORPUS)

.PHONY: all cosmel styleme $(TARGETS)

all: cosmel styleme

cosmel:
	make cosmel_repo

styleme:
	make styleme_repo styleme_corpus

cosmel_repo:
	make $(COSMEL_REPO)

styleme_repo:
	make $(STYLEME_REPO)

styleme_corpus:
	make $(STYLEME_CORPUS)

$(TARGETS):
	$(CRAWL) $@
