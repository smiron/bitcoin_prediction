import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np

pd.set_option('display.line_width', 5000)
pd.set_option('display.max_columns', 60)

print(sys.getdefaultencoding())

#bitcoin_historic = pd.read_csv('./my/bitcoin_historic_data.csv', parse_dates=['date'], dayfirst=True, index_col='date')
#bitcoin_historic = pd.read_csv('./my/bitcoin_historic_data.csv', parse_dates=['date'], dayfirst=True)

twitter_historic_data = open('./my/twitter_historic.csv', encoding='utf-8')
twitter_historic = pd.read_csv(twitter_historic_data, encoding='utf-8', parse_dates=['date'], dayfirst=True, dtype={'id': np.int64, 'date': str, 'lang': str, 'text': str})

langFilter = twitter_historic['lang'] == 'en'

#print(twitter_historic[langFilter][['id', 'text']][:3])

print(twitter_historic.groupby('id').groups[:3])

#print(bitcoin_historic[['price']][:3])
#print( bitcoin_historic[ bitcoin_historic['price'] < 1000 ][['date']][:3] )

#bitcoin_historic.plot(figsize=(15, 10))
#plt.show()