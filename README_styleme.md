## StyleMe Spiders

### brand_meta
- in:  `https://styleme.pixnet.net/api/searchbrands/`
- out: `brand`

### product_meta
- in:  `brand`
- in:  `https://styleme.pixnet.net/api/searchbrands/{brand_id}/products/`
- out: `product`

### product_info
- in:  `product`
- in:  `https://styleme.pixnet.net/api/products/{product_id}`
- out: `product_info`

### article_meta_product
- in:  `product`
- in:  `https://styleme.pixnet.net/api/products/{product_id}/articles`
- out: `article`
- out: `product_article`

### article_meta_category
- in:  `category_sub`
- in:  `https://styleme.pixnet.net/api/articles/categorylist/{category_id}?subcategory_id={subcategory_id}`
- out: `article`

### article_body_styleme
- in:  `article`
- in:  `https://styleme.pixnet.net/api/articles/{article_id}`
- out: `article_info`
- out: `article_body`

### article_body_pixnet
- in:  `article`
- in:  `https://emma.pixnet.cc/blog/articles/{article_id}`
- out: `article_info`
- out: `article_body`

### article_body_pixnet_post
- in:  `article.link`
- out: `article_info`
- out: `article_body`

## Links

https://developer.pixnet.pro

https://styleme.pixnet.net/sitemap.xml

https://styleme.pixnet.net/api/searchbrands/
https://styleme.pixnet.net/api/searchcategory/

https://styleme.pixnet.net/api/search/category/?quality=###&usage_id=16&sort_by=price&sort=asc&page=1&per_page=20
sort_by: article_count, price
sort: desc, asc

https://styleme.pixnet.net/api/search/category/?quality=卸妝產品&efficiencies=卸妝

https://styleme.pixnet.net/api/articles/categorylist/1?subcategory_id=7&page=1&per_page=20&without_category_id=0

https://styleme.pixnet.net/api/searchbrands/448/products/
https://styleme.pixnet.net/api/search/product?brand_id=448

https://styleme.pixnet.net/api/products/10624
https://styleme.pixnet.net/api/products/10624?imgwidth=380&imgheight=380
https://styleme.pixnet.net/api/products/10624/articles?type=impression
https://styleme.pixnet.net/api/products/10624/articles?type=teaching

https://styleme.pixnet.net/api/articles/222159702?with_related_article=1&with_related_product=1
https://emma.pixnet.cc/blog/articles/348867751?user=shunger890
