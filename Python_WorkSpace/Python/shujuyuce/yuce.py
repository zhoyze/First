import numpy as np #数组模块
from pandas import read_csv #导入CSV文件成dataframe结构;
import math #导入数学模块，计算均方根差使用
from keras.models import Sequential #引入Kears模块的序列模型，此模型是将所有层线性叠加
from keras.layers import Dense #输出层使用全连接层
from keras.layers import LSTM,Activation #2;
from sklearn.preprocessing import MinMaxScaler #数据标准化
from sklearn.metrics import mean_squared_error #均方根差，矩阵计算;
import pandas as pd

seed = 7 #随机种子
batch_size = 30  #每批过神经网络的大小
epochs = 400 #神经网络训练的轮次
#filename = '1000a.csv'  #数据文件，两列，一列是时间，另外一列是每天的数据;

footer = 3
look_back=1  #时间窗口，步长为1，即用今天预测明天;

#此函数的目的是将输入的每天的数据作为输入和输,Y是X的下一个输出;
def create_dataset(dataset):
    dataX, dataY = [], []
    for i in range(len(dataset) - look_back - 1):
        x = dataset[i: i + look_back, 0]
        dataX.append(x)
        y = dataset[i + look_back, 0]
        dataY.append(y)
        print('X: %s, Y: %s' % (x, y))
    return np.array(dataX), np.array(dataY)

def build_model():
    model = Sequential()
    model.add(LSTM(units=4, input_shape=(1, look_back)))
    model.add(Dense(units=1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def create_model():
    model = Sequential()
    #输入数据的shape为(n_samples, timestamps, features)
    #隐藏层设置为256, input_shape元组第二个参数1意指features为1
    #下面还有个lstm，故return_sequences设置为True
    model.add(LSTM(units=256,input_shape=(None,1),return_sequences=True))
    model.add(LSTM(units=256))
    #后接全连接层，直接输出单个值，故units为1
    model.add(Dense(units=1))
    model.add(Activation('relu'))
    model.compile(loss='mse',optimizer='adam')
    return model


# 导入数据
num = 10
num2 = 1005
for i in range(num):
    # 设置随机种子
    np.random.seed(seed)
    filename = "data/"+str(i + num2) + ".csv"
    csvFile = open("data5/" + str(i + num2) + ".csv", "a")
    for j in range(1):
        data1 = read_csv(filename, usecols=[3], engine='python', skipfooter=footer)
        dataset = data1.values.astype('float32')
        # 标准化数据
        scaler = MinMaxScaler()
        dataset = scaler.fit_transform(dataset)
        train_size = int(len(dataset) * 0.67)
        validation_size = len(dataset) - train_size
        train, validation = dataset[0: train_size, :], dataset[train_size: len(dataset), :]

        # 创建dataset，让数据产生相关性
        X_train, y_train = create_dataset(train)
        X_validation, y_validation = create_dataset(validation)

        # 将输入转化成为【sample， time steps, feature]
        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
        X_validation = np.reshape(X_validation, (X_validation.shape[0], 1, X_validation.shape[1]))

        # 训练模型
        model = create_model()
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, )

        # 模型预测数据
        predict_train = model.predict(X_train)
        predict_validation = model.predict(X_validation)

        # 反标准化数据 --- 目的是保证MSE的准确性
        predict_train = scaler.inverse_transform(predict_train)
        y_train = scaler.inverse_transform([y_train])
        predict_validation = scaler.inverse_transform(predict_validation)
        y_validation = scaler.inverse_transform([y_validation])

        # 评估模型
        train_score = math.sqrt(mean_squared_error(y_train[0], predict_train[:, 0]))
        print('Train Score: %.2f RMSE' % train_score)
        validation_score = math.sqrt(mean_squared_error(y_validation[0], predict_validation[:, 0]))
        print('Validatin Score: %.2f RMSE' % validation_score)

        # 构建通过训练集进行预测的图表数据
        predict_train_plot = np.empty_like(dataset)
        predict_train_plot[:, :] = np.nan
        predict_train_plot[look_back:len(predict_train) + look_back, :] = predict_train

        # 构建通过评估数据集进行预测的图表数据
        predict_validation_plot = np.empty_like(dataset)
        predict_validation_plot[:, :] = np.nan
        predict_validation_plot[len(predict_train) + look_back * 2 + 1:len(dataset) - 1, :] = predict_validation

        data_f = pd.DataFrame(predict_validation)
        data_f.to_csv("data1/" + str(i + num2) + ".csv", header=0, index=0, mode='a')

        csvFile.close()
        # 图表显示
        # dataset = scaler.inverse_transform(dataset)
        # plt.plot(dataset, color='blue')
        # plt.plot(predict_train_plot, color='green')
        # plt.plot(predict_validation_plot, color='red')
        # plt.show()