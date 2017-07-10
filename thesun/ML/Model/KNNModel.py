from Model import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

import sys
sys.path.append("thesun/ML/Controller/")
from QualityMetric import *
from FeatureExtractor import *

class KNNModel(Model):
    def __init__(self, learning_data):
        self.given_features = ['distance', u'age', u'log_space', u'house_type', u'room_number']
        learning_data = learning_data.copy()

        print "Choosing k..."
        self.k = 16
        #self.k   = self.choose_k(learning_data, 1, 1000) 
        print "Chosen k = " + str(self.k)
        
    def predict_price(self, dataframe):
	print dataframe.dtypes
        dataframe = dataframe.copy()
        dataframe = FeatureExtractor().normalize_data(dataframe)
        dataframe[u'price_for_sqr_meter'] = self.knn.predict(dataframe[self.given_features])
	print dataframe[u'price_for_sqr_meter']
	        
        price_for_sqr_meter  = dataframe[u'price_for_sqr_meter']
        all_space            = dataframe[u'all_space']
        price                = dataframe[u'price']
        for i in dataframe.index:
            price[i] = price_for_sqr_meter[i] * all_space[i]

        del dataframe[u'price_for_sqr_meter']
        dataframe[u'price'] = price
        return dataframe
    
    def predict_price_given_knn(self, dataframe, knn_model):
        dataframe = dataframe.copy()
        
        dataframe[u'price_for_sqr_meter'] = knn_model.predict(dataframe[[u'geocode_lat', u'geocode_long']])
        
        price_for_sqr_meter  = dataframe[u'price_for_sqr_meter']
        all_space            = dataframe[u'all_space']
        price                = dataframe[u'price']
        for i in dataframe.index:
            price[i] = price_for_sqr_meter[i] * all_space[i]

        dataframe[u'price'] = price
        return dataframe

    def train(self, dataframe):
        dataframe = dataframe.copy()

        print "Training model..."

        self.knn = KNeighborsRegressor(n_neighbors = self.k)
        self.knn.fit(dataframe[self.given_features], dataframe[[u'price_for_sqr_meter']])
        
        print "Finished training!"
        
    def choose_k(self, dataframe, low_k, high_k):
        dataframe = dataframe.copy()
        train, test = train_test_split(dataframe, test_size = 0.1)

        print "  Choosing between " + str(low_k) + ' ' + str(high_k)
        if low_k > high_k:
            return 0
        
        left  = -1
        right = -1
        ans   = -1
        
        step = (high_k - low_k + 4) / 5
        pos  = low_k + step
        prev = self.get_error_for(low_k, train, test)
        
        while pos <= high_k:
            error = self.get_error_for(pos, train, test)
            
            if ans == -1 or prev + error < ans:
                ans = prev + error
                left = pos - step
                right = pos
            
            if pos == high_k:
                break
            pos = min(pos + step, high_k)
            prev = error
        
        if step == 1:
            return left
        
        return self.choose_k(dataframe, left, right)
    
    def get_error_for(self, k, train, test):
        train = train.copy()
        test  = test.copy()
        
        knn = KNeighborsRegressor(n_neighbors = k)
        knn.fit(train[[u'geocode_lat', u'geocode_long']], train[[u'price_for_sqr_meter']])

        prediction = self.predict_price_given_knn(test, knn)
        return QualityMetric().calculate_relative_error(test, prediction)

            
