from Model import *
class StupidModel(Model):
    def __init__(self, learning_data):
        pass
    
    def predict_price(self, dataframe):
        dataframe = dataframe.copy()
        
        prices = dataframe[u'price']
        spaces = dataframe[u'all_space']
    
        for i in dataframe.index:
            prices[i] = self.price_for_sqr_meter * spaces[i]
        
        dataframe[u'price'] = prices
        return dataframe
    
    def train(self, dataframe):
        dataframe = dataframe.copy()
        
        print "Training stupid model..."
        self.price_for_sqr_meter = dataframe[u'price'].sum() / dataframe[u'all_space'].sum()
        print "Finished training!"