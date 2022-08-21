# fptshop_data_scrapper
Scraping a dynamic content page generated from javascript using python and Selenium


## Prerequisites:
- Python 3
- BeautifulSoup
- Selenium
- Pandas, re, json
- msedgedriver

## Workflow:
- extract url of old products on the website, as well as their general infomation like product name, price, the number of old product per model

- change those url which are belong to the old products to the url of new products and then get the detailed configuration of their (because old product page does not show this)

- while in scraping process, the program constantly saves the collected data into a json file, so that we can pause the program and run it again without losing the previous data

- save the data into an excel file for preview

Selenium in the project is used in creating web driver, clicking button, explicit waiting, creating custom wait condition... 
### Input
links of pages contain list of old products and new products (provided in the notebook)
### Output
raw data of products stored in json or excel file: phone.xlxs, laptop.xlxs, tablet.xlxs

## Next steps
- clean the data and do some analysis on it
- implement machine learning project
- learn more about web security, the current project might be unable to run sometimes due to CORS policy (i wrote a line of code in the project to disable CORS check if it happens)

