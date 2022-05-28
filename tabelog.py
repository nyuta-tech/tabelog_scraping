import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import csv
import time

with open("id_list.txt","r") as f:
    data = f.read()
    areaIds = data.split("\n")

base_url = "https://tabelog.com/osaka/A2701/"
for area_id in areaIds:
    with open('tabelog_new_shops.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(["ここから地域切り替え"])
    for i in range(1,30):
        search_query = f"{area_id}/rstLst/{i}/?SrtT=nod&Srt=D"
        res = requests.get(base_url + search_query)
        time.sleep(1)
        # レスポンスの HTML から BeautifulSoup オブジェクトを作る
        soup = BeautifulSoup(res.text, 'html.parser')
        lxml = html.fromstring(str(soup))
        # 店舗ごとのURL
        shop_urls = lxml.xpath("//div[@data-rd-pos='cassette']/div[@data-rst-id]//h3/a/@href")

        for shop_url in shop_urls:
            try:
                detail_res = requests.get(shop_url)
                time.sleep(1)

                soup = BeautifulSoup(detail_res.text, 'html.parser')
                lxml = html.fromstring(str(soup))

                name = lxml.xpath("//tr[./th[contains(text(),'店名')]]/td//span")[0].text
                address =''.join(lxml.xpath("//tr[./th[contains(text(),'住所')]]/td/p")[0].itertext())
                tel = ''.join(lxml.xpath("//tr[./th[contains(text(),'予約・')]]/td")[0].itertext()).replace("\n","")
                if not re.match(r"\d+",tel):
                    continue

                #csvへの書き出し
                with open('tabelog_new_shops.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([name, address, tel])
                print([name, address, tel])
            except Exception as e:
                print(e)
                continue
            

