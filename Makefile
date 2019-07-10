ROOT  = ../code

SCRAPY = PYTHONPATH=$(ROOT):$(PYTHONPATH) scrapy
CRAWL = $(SCRAPY) crawl

COSMEL_REPO = \
	cosmel_brand_meta_styleme \
	cosmel_product_meta_styleme \
	cosmel_brand_alias \
	cosmel_product_purge

COSMEL_CORPUS = \
	cosmel_article_meta_styleme \
	cosmel_article_body_styleme

COSMEL_CONTENT = \
	cosmel_product_descr \
	cosmel_article_content

STYLEME_REPO = \
	styleme_brand_meta \
	styleme_product_meta \
	styleme_product_info

STYLEME_CORPUS = \
	styleme_article_meta_product \
	styleme_article_meta_category \
	styleme_article_body_styleme \
	styleme_article_body_pixnet \
	styleme_article_body_pixnet_post

STYLEME_OLD_REPO = \
	styleme_old_brand_meta \
	styleme_old_product_meta

TARGETS = $(COSMEL_REPO) $(COSMEL_CORPUS) $(COSMEL_CONTENT) $(STYLEME_REPO) $(STYLEME_CORPUS) $(STYLEME_OLD_REPO)

.PHONY: all list $(TARGETS)

all: cosmel styleme styleme_old

cosmel:
	make cosmel_repo cosmel_corpus cosmel_content

styleme:
	make styleme_repo styleme_corpus

styleme_old:
	make styleme_old_repo

cosmel_repo:
	make $(COSMEL_REPO)

cosmel_corpus:
	make $(COSMEL_CORPUS)

cosmel_content:
	make $(COSMEL_CONTENT)

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
