# -*- coding: utf-8 -*-
"""tide work (see n days predict next days)[Train 1 month].ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xtPqKuO4RiMoK4C3WGV0FD591plC9KUH
"""

from google.colab import drive
drive.mount('/content/drive')

"""# see 3 days & predict & forecast next day

## imports
"""

import numpy
import matplotlib.pyplot as plt
import pandas
import keras
import numpy as np
from itertools import chain
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error

"""## data preparation"""

dataframe = pandas.read_csv("/content/drive/MyDrive/Tide work/datasets/new work dataset/teknaf_jan_apr_2020.csv",
                            header=None, delimiter = "\t", engine="python")

dataframe = dataframe.drop(dataframe.index[0])
dataframe = dataframe.reset_index(drop=True)

see_days = 3

"""## train data"""

start_range_train = 0
end_range_train = 0

for x in range(len(dataframe)):
  if((dataframe[0][x] == '3/1/2020') & (dataframe[1][x] == '0:00')):
    start_range_train = x
  if((dataframe[0][x] == '3/31/2020') & (dataframe[1][x] == '23:55')):
    end_range_train = x


train_data = dataframe.iloc[start_range_train:(end_range_train+1)]
train_data = train_data.drop(columns=[0,1])

# train_data = train_data.values
# train_data = train_data.astype('float32')

train_data = train_data.T
train_data.shape

train_data = np.asarray(train_data)
train_data = train_data.tolist()
train_data = list(chain.from_iterable(train_data))

"""## test data"""

start_range_test = 0
end_range_test = 0

for x in range(len(dataframe)):
  if((dataframe[0][x] == '3/29/2020') & (dataframe[1][x] == '0:00')):
    start_range_test = x
  if((dataframe[0][x] == '4/30/2020') & (dataframe[1][x] == '23:55')):
    end_range_test = x


test_data = dataframe.iloc[start_range_test:(end_range_test+1)]
test_data = test_data.drop(columns=[0,1])

# test_data = test_data.values
# test_data = test_data.astype('float32')

test_data = test_data.T
test_data.shape

test_data = np.asarray(test_data)
test_data = test_data.tolist()
test_data = list(chain.from_iterable(test_data))

"""## X, y for train & test"""

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back):
  dataX, dataY = [], []
  for i in range(0,(len(dataset)-look_back*see_days),look_back):
    a = dataset[i:(i + look_back*see_days)]
    dataX.append(a)
    b = dataset[(i + look_back*see_days):(i + look_back*(see_days+1))]
    dataY.append(b)
  return dataX, dataY

# reshape into X=t and Y=t+1
look_back = 288
trainX, trainY = create_dataset(train_data, look_back)
testX, testY = create_dataset(test_data, look_back)

trainX = np.asarray(trainX)
trainY = np.asarray(trainY)

testX = np.asarray(testX)
testY = np.asarray(testY)

trainX = trainX.astype(np.float)
trainY = trainY.astype(np.float)

testX = testX.astype(np.float)
testY = testY.astype(np.float)

# reshape input to be [samples, time steps, features]
# train_X = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
# test_X = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

train_X = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
test_X = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))

train_X.shape

"""## model train"""

# # create and fit the LSTM network
# model = Sequential()
# model.add(LSTM(512, input_shape=(look_back*see_days, 1)))
# model.add(Dense(look_back))
# model.compile(loss='mean_squared_error', optimizer='adam')
# model.fit(train_X, trainY, epochs=100, batch_size=1, verbose=2) #, callbacks=[es]

"""## make prediction and save model"""

# make predictions
trainPredict = model.predict(train_X)
testPredict = model.predict(test_X)

trainScore = math.sqrt(mean_squared_error(trainY[:,0], trainPredict[:,0]))
print('Train Score: %.5f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[:,0], testPredict[:,0]))
print('Test Score: %.5f RMSE' % (testScore))

# model.save('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')

# from keras.models import load_model
# model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
# trainPredict = model1.predict(train_X)
# testPredict = model1.predict(test_X)

# trainScore = math.sqrt(mean_squared_error(trainY[:,0], trainPredict[:,0]))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = math.sqrt(mean_squared_error(testY[:,0], testPredict[:,0]))
# print('Test Score: %.2f RMSE' % (testScore))

"""## train & test predict + plot"""

trainY_c = np.resize(trainY,(len(train_data)-look_back*see_days,1))
trainPredict_c = np.resize(trainPredict,(len(train_data)-look_back*see_days,1))
testY_c = np.resize(testY,(len(test_data)-look_back*see_days,1))
testPredict_c = np.resize(testPredict,(len(test_data)-look_back*see_days,1))

# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(trainPredict_c)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[0:len(trainPredict_c), :] = trainPredict_c

fig, ax = plt.subplots(figsize=(20,10))
ax.plot(trainY_c, label = "Real_train")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(trainPredictPlot, label = "predicted_train RMSE:"+str(trainScore))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 predict_train) see "+str(see_days)+" days pred next day")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/see "+str(see_days)+" days pred next day (train).png")

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c
fig, ax = plt.subplots(figsize=(20,10))
ax.plot(testY_c, label = "Real_test")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "predicted_test RMSE:"+str(testScore))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 predict_test Apr) see "+str(see_days)+" days pred next day")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/see "+str(see_days)+" days pred next day (test).png")

"""## forecast 7 days"""

#For 7 days 
from keras.models import load_model
model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
forecast_7days=[]
#test = train_X[-1]
test = test_X[0]
a = test_X[0].tolist()
shift = 0

for i in range(7):
  train = a[0+shift: (look_back*see_days)+shift]
  train = np.asarray(train)
  train = numpy.reshape(train, (1, trainX.shape[1], 1))
  test = model1.predict(train)
  var1 = test[0]
  var1 = var1.tolist()
  var2 = [[i] for i in var1]
  test = numpy.reshape(test, (trainY.shape[1]))
  forecast_7days.append(test)
  # print(a)
  a = a + var2
  # print(a)
  shift = shift + look_back

forecast_7days = numpy.array(forecast_7days)
forcast7Score = math.sqrt(mean_squared_error(testY[:7,0], forecast_7days[:,0]))

#testY_c = np.resize(testY,(len(dataset_test[:2016]),1))
testPredict_c = np.resize(forecast_7days,(look_back*7,1))

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c

fig, ax = plt.subplots(figsize=(20,10))
#ax.plot(dataset_test[:2016], label = "Real_test 7 days ")
ax.plot(testY_c[:2016], label = "Real_test 7 days ")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "Forecast 7 Days of Apr RMSE:"+str(forcast7Score))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 Forecast Apr 1st 7 days) [see "+str(see_days)+" days pred next day]")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/Water level vs Observation (Train - mar'1 to mar'31 Forecast Apr 1st 7 days) see "+str(see_days)+" days pred next day.png")

"""## forecast 14 days"""

#For 14 days 
from keras.models import load_model
model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
forecast_14days=[]
#test = train_X[-1]
test = test_X[0]
a = test_X[0].tolist()
shift = 0

for i in range(14):
  train = a[0+shift: (look_back*see_days)+shift]
  train = np.asarray(train)
  train = numpy.reshape(train, (1, trainX.shape[1], 1))
  test = model1.predict(train)
  var1 = test[0]
  var1 = var1.tolist()
  var2 = [[i] for i in var1]
  test = numpy.reshape(test, (trainY.shape[1]))
  forecast_14days.append(test)
  # print(a)
  a = a + var2
  # print(a)
  shift = shift + look_back

forecast_14days = numpy.array(forecast_14days)
forcast14Score = math.sqrt(mean_squared_error(testY[:14,0], forecast_14days[:,0]))

#testY_c = np.resize(testY,(len(dataset_test[:2016]),1))
testPredict_c = np.resize(forecast_14days,(look_back*14,1))

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c

fig, ax = plt.subplots(figsize=(20,10))
#ax.plot(dataset_test[:2016], label = "Real_test 14 days ")
ax.plot(testY_c[:4032], label = "Real_test 14 days ")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "Forecast 14 Days of Apr RMSE:"+str(forcast14Score))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 Forecast Apr 1st 14 days) [see "+str(see_days)+" days pred next day]")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/Water level vs Observation (Train - mar'1 to mar'31 Forecast Apr 1st 14 days) see "+str(see_days)+" days pred next day.png")

"""## forecast 29 days"""

#For 29 days 
from keras.models import load_model
model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
forecast_29days=[]
#test = train_X[-1]
test = test_X[0]
a = test_X[0].tolist()
shift = 0

for i in range(29):
  train = a[0+shift: (look_back*see_days)+shift]
  train = np.asarray(train)
  train = numpy.reshape(train, (1, trainX.shape[1], 1))
  test = model1.predict(train)
  var1 = test[0]
  var1 = var1.tolist()
  var2 = [[i] for i in var1]
  test = numpy.reshape(test, (trainY.shape[1]))
  forecast_29days.append(test)
  # print(a)
  a = a + var2
  # print(a)
  shift = shift + look_back

forecast_29days = numpy.array(forecast_29days)
forcast29Score = math.sqrt(mean_squared_error(testY[:29,0], forecast_29days[:,0]))

#testY_c = np.resize(testY,(len(dataset_test[:2016]),1))
testPredict_c = np.resize(forecast_29days,(look_back*29,1))

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c

fig, ax = plt.subplots(figsize=(20,10))
#ax.plot(dataset_test[:2016], label = "Real_test 29 days ")
ax.plot(testY_c[:8352], label = "Real_test 29 days ")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "Forecast 29 Days of Apr RMSE:"+str(forcast29Score))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 Forecast Apr 1st 29 days) [see "+str(see_days)+" days pred next day]")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/Water level vs Observation (Train - mar'1 to mar'31 Forecast Apr 1st 29 days) see "+str(see_days)+" days pred next day.png")

"""# see 7 days & predict & forecast next day

## imports
"""

import numpy
import matplotlib.pyplot as plt
import pandas
import keras
import numpy as np
from itertools import chain
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error

"""## data preparation"""

dataframe = pandas.read_csv("/content/drive/MyDrive/Tide work/datasets/new work dataset/teknaf_jan_apr_2020.csv",
                            header=None, delimiter = "\t", engine="python")

dataframe = dataframe.drop(dataframe.index[0])
dataframe = dataframe.reset_index(drop=True)

see_days = 7

"""## train data"""

start_range_train = 0
end_range_train = 0

for x in range(len(dataframe)):
  if((dataframe[0][x] == '1/1/2020') & (dataframe[1][x] == '0:00')):
    start_range_train = x
  if((dataframe[0][x] == '3/31/2020') & (dataframe[1][x] == '23:55')):
    end_range_train = x


train_data = dataframe.iloc[start_range_train:(end_range_train+1)]
train_data = train_data.drop(columns=[0,1])

# train_data = train_data.values
# train_data = train_data.astype('float32')

train_data = train_data.T
train_data.shape

train_data = np.asarray(train_data)
train_data = train_data.tolist()
train_data = list(chain.from_iterable(train_data))

"""## test data"""

start_range_test = 0
end_range_test = 0

for x in range(len(dataframe)):
  if((dataframe[0][x] == '3/25/2020') & (dataframe[1][x] == '0:00')):
    start_range_test = x
  if((dataframe[0][x] == '4/30/2020') & (dataframe[1][x] == '23:55')):
    end_range_test = x


test_data = dataframe.iloc[start_range_test:(end_range_test+1)]
test_data = test_data.drop(columns=[0,1])

# test_data = test_data.values
# test_data = test_data.astype('float32')

test_data = test_data.T
test_data.shape

test_data = np.asarray(test_data)
test_data = test_data.tolist()
test_data = list(chain.from_iterable(test_data))

"""## X, y for train & test"""

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back):
  dataX, dataY = [], []
  for i in range(0,(len(dataset)-look_back*see_days),look_back):
    a = dataset[i:(i + look_back*see_days)]
    dataX.append(a)
    b = dataset[(i + look_back*see_days):(i + look_back*(see_days+1))]
    dataY.append(b)
  return dataX, dataY

# reshape into X=t and Y=t+1
look_back = 288
trainX, trainY = create_dataset(train_data, look_back)
testX, testY = create_dataset(test_data, look_back)

trainX = np.asarray(trainX)
trainY = np.asarray(trainY)

testX = np.asarray(testX)
testY = np.asarray(testY)

trainX = trainX.astype(np.float)
trainY = trainY.astype(np.float)

testX = testX.astype(np.float)
testY = testY.astype(np.float)

# reshape input to be [samples, time steps, features]
# train_X = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
# test_X = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

train_X = numpy.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
test_X = numpy.reshape(testX, (testX.shape[0], testX.shape[1], 1))

"""## model train"""

# # create and fit the LSTM network
# model = Sequential()
# model.add(LSTM(512, input_shape=(look_back*see_days, 1)))
# model.add(Dense(look_back))
# model.compile(loss='mean_squared_error', optimizer='adam')
# model.fit(train_X, trainY, epochs=100, batch_size=1, verbose=2) #, callbacks=[es]

"""## make prediction and save model"""

# make predictions
trainPredict = model.predict(train_X)
testPredict = model.predict(test_X)

trainScore = math.sqrt(mean_squared_error(trainY[:,0], trainPredict[:,0]))
print('Train Score: %.5f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[:,0], testPredict[:,0]))
print('Test Score: %.5f RMSE' % (testScore))

# model.save('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')

# from keras.models import load_model
# model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
# trainPredict = model1.predict(train_X)
# testPredict = model1.predict(test_X)

# trainScore = math.sqrt(mean_squared_error(trainY[:,0], trainPredict[:,0]))
# print('Train Score: %.2f RMSE' % (trainScore))
# testScore = math.sqrt(mean_squared_error(testY[:,0], testPredict[:,0]))
# print('Test Score: %.2f RMSE' % (testScore))

"""## train & test predict + plot"""

trainY_c = np.resize(trainY,(len(train_data)-look_back*see_days,1))
trainPredict_c = np.resize(trainPredict,(len(train_data)-look_back*see_days,1))
testY_c = np.resize(testY,(len(test_data)-look_back*see_days,1))
testPredict_c = np.resize(testPredict,(len(test_data)-look_back*see_days,1))

# shift train predictions for plotting
trainPredictPlot = numpy.empty_like(trainPredict_c)
trainPredictPlot[:, :] = numpy.nan
trainPredictPlot[0:len(trainPredict_c), :] = trainPredict_c

fig, ax = plt.subplots(figsize=(20,10))
ax.plot(trainY_c, label = "Real_train")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(trainPredictPlot, label = "predicted_train RMSE:"+str(trainScore))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 predict_train) see "+str(see_days)+" days pred next day")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/see "+str(see_days)+" days pred next day (train).png")

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c
fig, ax = plt.subplots(figsize=(20,10))
ax.plot(testY_c, label = "Real_test")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "predicted_test RMSE:"+str(testScore))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 predict_test Apr) see "+str(see_days)+" days pred next day")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/see "+str(see_days)+" days pred next day (test).png")

"""## forecast 7 days"""

#For 7 days 
from keras.models import load_model
model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
forecast_7days=[]
#test = train_X[-1]
test = test_X[0]
a = test_X[0].tolist()
shift = 0

for i in range(7):
  train = a[0+shift: (look_back*see_days)+shift]
  train = np.asarray(train)
  train = numpy.reshape(train, (1, trainX.shape[1], 1))
  test = model1.predict(train)
  var1 = test[0]
  var1 = var1.tolist()
  var2 = [[i] for i in var1]
  test = numpy.reshape(test, (trainY.shape[1]))
  forecast_7days.append(test)
  # print(a)
  a = a + var2
  # print(a)
  shift = shift + look_back

forecast_7days = numpy.array(forecast_7days)
forcast7Score = math.sqrt(mean_squared_error(testY[:7,0], forecast_7days[:,0]))

#testY_c = np.resize(testY,(len(dataset_test[:2016]),1))
testPredict_c = np.resize(forecast_7days,(look_back*7,1))

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c

fig, ax = plt.subplots(figsize=(20,10))
#ax.plot(dataset_test[:2016], label = "Real_test 7 days ")
ax.plot(testY_c[:2016], label = "Real_test 7 days ")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "Forecast 7 Days of Apr RMSE:"+str(forcast7Score))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 Forecast Apr 1st 7 days) [see "+str(see_days)+" days pred next day]")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/Water level vs Observation (Train - mar'1 to mar'31 Forecast Apr 1st 7 days) see "+str(see_days)+" days pred next day.png")

"""## forecast 14 days"""

#For 14 days 
from keras.models import load_model
model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
forecast_14days=[]
#test = train_X[-1]
test = test_X[0]
a = test_X[0].tolist()
shift = 0

for i in range(14):
  train = a[0+shift: (look_back*see_days)+shift]
  train = np.asarray(train)
  train = numpy.reshape(train, (1, trainX.shape[1], 1))
  test = model1.predict(train)
  var1 = test[0]
  var1 = var1.tolist()
  var2 = [[i] for i in var1]
  test = numpy.reshape(test, (trainY.shape[1]))
  forecast_14days.append(test)
  # print(a)
  a = a + var2
  # print(a)
  shift = shift + look_back

forecast_14days = numpy.array(forecast_14days)
forcast14Score = math.sqrt(mean_squared_error(testY[:14,0], forecast_14days[:,0]))

#testY_c = np.resize(testY,(len(dataset_test[:2016]),1))
testPredict_c = np.resize(forecast_14days,(look_back*14,1))

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c

fig, ax = plt.subplots(figsize=(20,10))
#ax.plot(dataset_test[:2016], label = "Real_test 14 days ")
ax.plot(testY_c[:4032], label = "Real_test 14 days ")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "Forecast 14 Days of Apr RMSE:"+str(forcast14Score))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 Forecast Apr 1st 14 days) [see "+str(see_days)+" days pred next day]")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/Water level vs Observation (Train - mar'1 to mar'31 Forecast Apr 1st 14 days) see "+str(see_days)+" days pred next day.png")

"""## forecast 29 days"""

#For 29 days 
from keras.models import load_model
model1 = load_model('/content/drive/MyDrive/Tide work/datasets/new work dataset/models/1_see_'+str(see_days)+'_days_pred_1_day_april.h5')
forecast_29days=[]
#test = train_X[-1]
test = test_X[0]
a = test_X[0].tolist()
shift = 0

for i in range(29):
  train = a[0+shift: (look_back*see_days)+shift]
  train = np.asarray(train)
  train = numpy.reshape(train, (1, trainX.shape[1], 1))
  test = model1.predict(train)
  var1 = test[0]
  var1 = var1.tolist()
  var2 = [[i] for i in var1]
  test = numpy.reshape(test, (trainY.shape[1]))
  forecast_29days.append(test)
  # print(a)
  a = a + var2
  # print(a)
  shift = shift + look_back

forecast_29days = numpy.array(forecast_29days)
forcast29Score = math.sqrt(mean_squared_error(testY[:29,0], forecast_29days[:,0]))

#testY_c = np.resize(testY,(len(dataset_test[:2016]),1))
testPredict_c = np.resize(forecast_29days,(look_back*29,1))

# shift test predictions for plotting
testPredictPlot = numpy.empty_like(testPredict_c)
testPredictPlot[:, :] = numpy.nan
testPredictPlot[0:len(testPredict_c), :] = testPredict_c

fig, ax = plt.subplots(figsize=(20,10))
#ax.plot(dataset_test[:2016], label = "Real_test 29 days ")
ax.plot(testY_c[:8352], label = "Real_test 29 days ")
ax.set_xlabel("Observation (Interval = 5 mins)")
ax.set_ylabel("Water level (In meter)")
ax.plot(testPredictPlot, label = "Forecast 29 Days of Apr RMSE:"+str(forcast29Score))
ax.set_title("Water level vs Observation (Train->mar'1 to mar'31 Forecast Apr 1st 29 days) [see "+str(see_days)+" days pred next day]")
leg = ax.legend();
fig.savefig("/content/drive/MyDrive/Tide work/datasets/new work dataset/plots/1month/Water level vs Observation (Train - mar'1 to mar'31 Forecast Apr 1st 29 days) see "+str(see_days)+" days pred next day.png")