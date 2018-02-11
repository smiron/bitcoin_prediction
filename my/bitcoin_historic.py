import requests
import pandas as pd

def getPrices():
    for page in range(1,1000):
        page_string = str(page)
        page_link = 'https://api.coinbase.com/v1/prices/historical?page=' + page_string
        print(page_link)
        r = requests.get(page_link)
        r = r.text

        with open("bitcoin_historic_data.csv", mode='a', encoding='utf-8', newline='') as file:
            file.write(r)
            file.write('\n')

getPrices()