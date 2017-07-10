import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import warnings
import math
import random
warnings.filterwarnings('ignore')

import sys
sys.path.append("thesun/ML/Model/")
from Model import *
from KNNModel import *
from StupidModel import *

sys.path.append("thesun/ML/Controller/")
from QualityMetric import *
from FeatureExtractor import *

class System:
    def __init__(self):
        self.featureExtractor = FeatureExtractor()
        self.dataframe        = pd.read_csv('thesun/Dataset/2/train.csv')
        
        self.dataframe     = self.featureExtractor.normalize_data(self.dataframe)
        self.learning_data = self.featureExtractor.learning_data(self.dataframe, 0.1)
    
    def choose_model(self):
        self.error = -1
        
#        self.try_model(StupidModel(self.learning_data))
        self.try_model(KNNModel(self.learning_data)) 
                        
    def try_model(self, model):
        train, test = train_test_split(self.learning_data, test_size = 0.1)
        model.train(train)
        print "Calculating RE for this model..."        
        prediction = model.predict_price(test)
        error = QualityMetric().calculate_relative_error(test, prediction)
        print "RE = " + str(error)
        
        if self.error == -1:
            self.error = error
            self.model = model
        elif error < self.error:
            self.error = error
            self.model = model
        
    def train_model(self):
        self.model.train(self.dataframe)
