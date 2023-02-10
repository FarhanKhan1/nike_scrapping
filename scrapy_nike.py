from bs4 import BeautifulSoup
import requests 
import json
import re
import math
import time
from scrapingbee import ScrapingBeeClient
client = ScrapingBeeClient(api_key='YOUR_API_KEY')
# url_ = "https://www.nike.com/w/mens-tops-t-shirts-9om13znik1"
url_ = input("Paste URL here: ")
response = requests.get(url_)
soup = BeautifulSoup(response.content, "html.parser")
json_script = soup.find("script", id="__NEXT_DATA__")
json_script.text
json_data = json.loads(json_script.text)
attribute_id_string = json_data["props"]["pageProps"]["initialState"]["Wall"]["pageData"]["next"]
total_resources = json_data["props"]["pageProps"]["initialState"]["Wall"]["pageData"]["totalResources"]

attribute_ids = re.search("attributeIds%28(.*?)%29", attribute_id_string).group(1)
print(total_resources)
print(attribute_ids)

anchor = 0
for i in range(math.ceil(int(total_resources/50))):
  print("creating end point...")
  endpoint_ = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=7FF69D93F45F9874026CDC4A96FFCEDD&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds({attribute_ids})%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D48"
  products_response = client.get(endpoint_)
  json_data = json.loads(products_response.text)
  print("Printing first batch...")
  time.sleep(3)
  for item in json_data["data"]["products"]["products"]:
        
    for colorway in item["colorways"]:
        print(" ".join(colorway["pdpUrl"].split("/")[-2].split("-")[:-1]), end=", ")
        print(colorway["pdpUrl"].split("/")[-1], end=", ")
        print(colorway["price"]["currentPrice"])
  anchor+=48

