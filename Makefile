ROOT  = ../code

SCRAPY = PYTHONPATH=$(ROOT):$(PYTHONPATH) scrapy
CRAWL = $(SCRAPY) crawl

COSMEL_REPO = \
	cosmel_brand_styleme \
	cosmel_brand_styleme_old \
	cosmel_brand_alias \
	cosmel_product_styleme \
	cosmel_product_styleme_old

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

STYLEME_OLD_REPO = \
	styleme_old_product_meta

TARGETS = $(COSMEL_REPO) $(STYLEME_REPO) $(STYLEME_CORPUS) $(STYLEME_OLD_REPO)

.PHONY: all list cosmel styleme styleme_old $(TARGETS)

all: cosmel styleme

cosmel:
	make cosmel_repo

styleme:
	make styleme_repo styleme_corpus

styleme_old:
	make styleme_old_repo

cosmel_repo:
	make $(COSMEL_REPO)

styleme_repo:
	make $(STYLEME_REPO)

styleme_corpus:
	make $(STYLEME_CORPUS)

styleme_old_repo:
	make $(STYLEME_OLD_REPO)

$(TARGETS):
	$(CRAWL) $@

list:
	$(SCRAPY) $@
