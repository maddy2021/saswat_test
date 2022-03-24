from email.policy import default
import scrapy
import coding_test.spiders.utils as utils
from coding_test.items import CodingTestItem
from scrapy.selector import Selector
import chompjs

class TargetSpider(scrapy.Spider):
    name = 'target'
    allowed_domains = ['target.com']
    start_urls = []

    def start_requests(self):
        yield scrapy.FormRequest(url=self.url,dont_filter=True,callback=self.parse)

    def parse(self, response):
        with open("data.html","wb+") as file:
            file.write(response.body)
        item= CodingTestItem()
        dynamic_data= response.xpath("//*[@id='pageBodyContainer']/script/text()").get(default="").strip()
        json_data = chompjs.parse_js_object(dynamic_data)
        price,currency = extract_price(json_data)
        tcin,upc = extract_tcin_upc(json_data)
        item["url"] = response.url
        item["title"] = extract_title(response,json_data)
        item["price"] = price
        item["currency"] = currency
        item["description"] = extract_desc(response)
        item["tcin"] = tcin
        item["upc"] = upc
        item["specs"] = extract_specification(response)
        yield item

def extract_title(response, json_data):
    title = ""
    try:
        if("@graph" in json_data and len(json_data["@graph"])>0 and "name" in json_data["@graph"][0]):
            title= json_data["@graph"][0]["name"]
        if(title==""):
            title = response.xpath(utils.title_xpath).get(default="").strip()
        return title
    except:
        print("Error while extracting title")
        return ""

def extract_price(json_data):
    price = 0
    currency = ""
    try:
        if("@graph" in json_data and len(json_data["@graph"])>0 and "offers" in json_data["@graph"][0]):
            offers = json_data["@graph"][0]["offers"]
            if("priceCurrency" in offers):
                currency = offers["priceCurrency"]
            if("price" in offers):
                price = offers["price"]
        return (price,currency)
    except:
        print("Error while extracting price and currency")
        return (0,"") 

def extract_tcin_upc(json_data):
    tcin = ""
    upc = ""
    try:
        if("@graph" in json_data and len(json_data["@graph"])>0 and "sku" in json_data["@graph"][0]):
            tcin= json_data["@graph"][0]["sku"]
        if("@graph" in json_data and len(json_data["@graph"])>0 and "sku" in json_data["@graph"][0]):
            upc = json_data["@graph"][0]["gtin13"]
            # upc = 0195994605802
            # Convert 13 digit of upc to 12 digit by not taking first 0
            if upc:
                upc = upc[1:]
        return tcin,upc 
    except:
        print("Error while extracting tcin or upc")
        return tcin,upc

def extract_desc(response):
    try:
        desc = response.xpath(utils.description_xpath).get(default="").strip()
        return desc
    except:
        print("Not able to find description")
        return ""

def extract_specification(response):
    specification_objects = response.xpath(utils.specification_xpath).getall() or []
    specification = {}
    try:
        for spec_obj in specification_objects:
            html_obj = Selector(text=spec_obj)
            key = html_obj.xpath("//div/div/b/text()").get()
            value = html_obj.xpath("//div/div/text()").get()
            if(key and value):
                specification[key.replace(":","")] = value.strip()
        return specification
    except:
        print("Not able to extract specifications")
        return specification




