# html parser


## features
- querySelecting
- query maker
  you give it the element and it will give you a proper query to always select that element wich can be used to dynamicly scrape data of that kind
- find element lists by text
    you provide the text and the program will not just find you the html element with that text but rather it will find every combo of elements that make up that text
- element template maker
  you provide the html element and the program will provide for you the js code nessicary to create that element so can create that element dynamicly



## how you can contribute
-  help make a page waiter
    all this web scraping is great how ever if html doesn't load then the parsing wont work and not everyone wants to deal with the chrome browser part, so the plan is make an api where users provide the url we return the html after waiting for the page to load plus we add a chaching system for speed without any extra work from the user

- report bugs and issues
- suggest new ideas


## snippets
```python

document.create_document_from(html_node_list)
document.create_template(html_node_list)
document.querySelector("div")


```