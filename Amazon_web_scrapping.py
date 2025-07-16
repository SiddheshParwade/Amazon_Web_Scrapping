#===============================================================================================#
# Author:       Siddhesh Parwade
#
# Motive:       To practice and demonstrate web scraping skills by building a script
#               that collects real-world e-commerce data (Earphones listings) from
#               Amazon, handles errors gracefully, and saves structured output.
#
# Description : Scrapes Earphones listings from Amazon across multiple pages,
#               extracting product name, price, and rating. Handles request headers
#               to mimic browsers, retries failed pages, and saves data to a CSV.
#
# Capability  : It can easily retrive 100 pages of amazon within 1 hour (without proxies) , 
#               if you uses rotating proxies then it works better.
# ==============================================================================================#

import requests
from bs4 import BeautifulSoup
import time
import random
import csv

## URL without page to increment it pages!
url="https://www.amazon.in/s?k=earphones&page=3&crid=1SM3W8RFKRHL1&qid=1752304572&sprefix=earphone%2Caps%2C199&xpid=prDEIYf8vSoc1&ref=sr_pg_"

products=[]
unfetchedPages=[]

## Diffrent agents for use each in diffrent request!

user_agents = [
    # Windows browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/123.0 Safari/537.36",

    # Linux browsers
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0",

    # Mac browsers
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/16 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",

]

session = requests.Session()

def pageScraper(i, j):
    for page in range(i, j):
        main_url = url + str(page)
        
         ## This headers will work better for amazon!
        
        headers = {
            "accept-ch": "ect,rtt,downlink,device-memory,sec-ch-device-memory,viewport-width,sec-ch-viewport-width,dpr,sec-ch-dpr,sec-ch-ua-platform,sec-ch-ua-platform-version",
            "accept-ch-lifetime": "86400",
            "alt-svc": 'h3=":443"; ma=86400',
            "cache-control": "no-transform",
            "content-encoding": "gzip",
            "content-language": "en-IN",
            "content-security-policy": "upgrade-insecure-requests;report-uri https://metrics.media-amazon.com/",
            "content-security-policy-report-only": "default-src 'self' blob: https: data: mediastream: 'unsafe-eval' 'unsafe-inline';report-uri https://metrics.media-amazon.com/",
            "content-type": "text/html;charset=UTF-8",
            "date": "Sat, 12 Jul 2025 07:24:56 GMT",
            "expires": "-1",
            "pragma": "no-cache",
            "server": "Server",
            "vary": "Content-Type,Accept-Encoding,User-Agent",
            "via": "1.1 223eafb65ba9a4a1e7198f4bb6ac8e74.cloudfront.net (CloudFront)",
            "x-amz-cf-id": "W9AtPFqXnTxD0Dxwk7td9AzDtCVMmgKWw2MBAM27EE_6xoSMBbRyUQ==",
            "x-amz-cf-pop": "BOM78-P11",
            "x-amz-rid": "X3SMMNB69D9BMG4T8SSN",
            "x-cache": "Miss from cloudfront",
            "x-content-type-options": "nosniff",
            "x-frame-options": "SAMEORIGIN",
            "x-xss-protection": "1;",
            "device-memory": "4",
            "downlink": "10",
            "dpr": "1.25",
            "ect": "4g",
            "rtt": "50",
            "sec-ch-device-memory": "4",
            "sec-ch-dpr": "1.25",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-ch-ua-platform-version": '"19.0.0"',
            "sec-ch-viewport-width": "1536",
            "upgrade-insecure-requests": "1",
            "user-agent": random.choice(user_agents),
            "viewport-width": "1536"
        }


        print("\n\n\n")
        print("User-Agent :  ", headers["user-agent"])
        print("Target-Url :  ",main_url)

        wait_time = random.randint(10, 15)
        print(f"Waiting for {wait_time} seconds before request...")
        time.sleep(wait_time)

        r = session.get(main_url, headers=headers)
        print(r.status_code)

        if r.status_code != 200:
            print(f"Request failed: {r.status_code}")
            unfetchedPages.append(page)
            continue

        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            cards = soup.find_all('div', class_='a-section a-spacing-small a-spacing-top-small') ## If code does not work please check the class name of <div> that contain info
        except AttributeError:
            print(f"⚠️ Page {page} structure not found. Skipping.")
            continue
        
        for card in cards:
            a = card.find("a", class_="a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal") ## If code does not work please check the class name of <a> that contain info
            names = a.find('span')  ## If code does not work please check the class name of div that contain info
            ratings = card.find("span", class_="a-icon-alt") ## If code does not work please check the class name of div that contain info
            prices = card.find("span", class_="a-offscreen") ## If code does not work please check the class name of div that contain info

            name = names.text.strip() if names else "None"
            rating = ratings.text.strip() if ratings else "None"
            price = prices.text.strip() if prices else "None"

            products.append([page, name, price, rating])

        print(f"✅ Products collected: {len(products)} till Page {page}")

## Define the number of pages you want to retrive, more pages takes more time!

pageScraper(1,21) # Retrives 20 pages

while unfetchedPages:
    pages_to_retry = unfetchedPages.copy()
    unfetchedPages.clear()
    print("\n\nUnfetched Pages Going To Fetch Again:", pages_to_retry, "\n\n")
    for i in pages_to_retry:
        pageScraper(i, i+1)
    

    
print("\n\n\n----------------------------------------Final Products----------------------------------------------------")

print("   Page_No    :    Name    :    Price    :    Rating    ")
for i in products:
    print(i[0]," : ",i[1]," : ",i[2]," : ",i[3])
    
with open('amazon_products.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['Page_No','Name', 'Price', 'Rating'])
    writer.writerows(products)

print("\n\n*****CSV file written: amazon_products.csv*****")