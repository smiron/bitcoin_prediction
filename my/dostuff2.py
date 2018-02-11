import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./my/bitcoinTwitterPolarity.csv', parse_dates=['timestamp'], dayfirst=True)
print(df.columns.values)

datag = df[['priceclose','polarity']].groupby(df['timestamp']).mean()

from sklearn.preprocessing import MinMaxScaler

values = datag['priceclose'].values.reshape(-1,1)



# fig, ax1 = plt.subplots()

# datag['priceclose']

# fig.tight_layout()
# plt.show()

# datag['priceclose'].plot()
# plt.show()



sentiment = datag['polarity'].values.reshape(-1,1)
values = values.astype('float32')
sentiment = sentiment.astype('float32')
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

train_size = int(len(scaled) * 0.7)
test_size = len(scaled) - train_size
train, test = scaled[0:train_size,:], scaled[train_size:len(scaled),:]
print(len(train), len(test))
split = train_size

import numpy as np

def create_dataset(dataset, look_back, sentiment, sent=False):
    dataX, dataY = [], []
    
    print(range(len(dataset) - look_back))
    
    for i in range(len(dataset) - look_back):
        if i >= look_back:
            a = dataset[i-look_back:i+1, 0]
            a = a.tolist()
            if(sent==True):
                a.append(sentiment[i].tolist()[0])
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
    #print(len(dataY))
    return np.array(dataX), np.array(dataY)

look_back = 2

trainX, trainY = create_dataset(train, look_back, sentiment[0:train_size],sent=True)
testX, testY = create_dataset(test, look_back, sentiment[train_size:len(scaled)], sent=True)

trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

model = Sequential()
model.add(LSTM(100, input_shape=(trainX.shape[1], trainX.shape[2]), return_sequences=True))
model.add(LSTM(100))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
history = model.fit(trainX, trainY, epochs=300, batch_size=100, validation_data=(testX, testY), verbose=0, shuffle=False)

from math import sqrt
from sklearn.metrics import mean_squared_error

yhat = model.predict(testX)

yhat_inverse_sent = scaler.inverse_transform(yhat.reshape(-1, 1))
testY_inverse_sent = scaler.inverse_transform(testY.reshape(-1, 1))

rmse_sent = sqrt(mean_squared_error(testY_inverse_sent, yhat_inverse_sent))
print('Test RMSE: %.3f' % rmse_sent)

print(testX.shape)