# CosmEL Spider

## Spiders

### brand
- in:  `https://styleme.pixnet.net/api/searchbrands/`
- out: `brand.meta`

### product
- in:  `brand.meta`
- in:  `https://styleme.pixnet.net/api/searchbrands/{brand_id}/products/`
- out: `product.meta`

### article
- in:  `product.meta`
- in:  `https://styleme.pixnet.net/api/products/{product_id}/articles`
- out: `article.meta`
- out: `product.article`

### article
- in:  `product.meta`
- in:  `https://styleme.pixnet.net/api/products/{product_id}/articles`
- out: `article.meta`
- out: `product.article`

### article_styleme
- in:  `article.meta`
- in:  `https://styleme.pixnet.net/api/articles/{article_id}`
- out: `article.info`
- out: `article.body`

### article_pixnet
- in:  `article.meta`
- in:  `https://emma.pixnet.cc/blog/articles/{article_id}`
- out: `article.info`
- out: `article.body`

### article_pixnet_post
- in:  `article.meta.link`
- out: `article.info`
- out: `article.body`

## Links

https://developer.pixnet.pro

https://styleme.pixnet.net/sitemap.xml

https://styleme.pixnet.net/api/searchbrands/
https://styleme.pixnet.net/api/searchcategory/

https://styleme.pixnet.net/api/search/category/?quality=###&usage_id=16&sort_by=price&sort=asc&page=1&per_page=20
sort_by: article_count, price
sort: desc, asc

https://styleme.pixnet.net/api/searchbrands/448/products/
https://styleme.pixnet.net/api/search/product?brand_id=448

https://styleme.pixnet.net/api/products/10624
https://styleme.pixnet.net/api/products/10624?imgwidth=380&imgheight=380
https://styleme.pixnet.net/api/products/10624/articles?type=impression
https://styleme.pixnet.net/api/products/10624/articles?type=teaching

https://styleme.pixnet.net/api/articles/222159702?with_related_article=1&with_related_product=1
https://emma.pixnet.cc/blog/articles/348867751?user=shunger890
