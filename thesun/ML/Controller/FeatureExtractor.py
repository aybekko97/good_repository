#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import numpy as np
import pandas as pd

class FeatureExtractor:
    def normalize_data(self, dataframe):
        dataframe = dataframe.copy()
        
        for col in dataframe:
            new_col = []
            for elem in dataframe[col]:
                if type(elem) == unicode:
                    new_col += [elem.encode('utf-8')]
                else:
                    new_col += [elem]
            dataframe[col] = new_col

        
        dataframe = dataframe.query('geocode_lat != \'None\'')

        dataframe[u'geocode_lat'] = dataframe[u'geocode_lat'].convert_objects(convert_numeric = True)
        dataframe[u'geocode_long'] = dataframe[u'geocode_long'].convert_objects(convert_numeric = True)
    
        dataframe[u'price'] = dataframe[u'price'].map(lambda x: x.translate(None, ' ₸') if type(x) == str else x)
        dataframe[u'price'] = dataframe[u'price'].convert_objects(convert_numeric = True)

        dataframe[u'all_space'] = dataframe[u'all_space'].map(lambda x: x.rstrip(' м2') if type(x) == str else x)
        dataframe[u'all_space'] = dataframe[u'all_space'].convert_objects(convert_numeric = True)

        dataframe[u'living_space'] = dataframe[u'living_space'].map(lambda x: x.rstrip(' м2') if type(x) != float else '0')
        dataframe[u'living_space'] = dataframe[u'living_space'].convert_objects(convert_numeric = True)

        dataframe[u'kitchen_space'] = dataframe[u'kitchen_space'].map(lambda x: x.rstrip(' м2') if type(x) != float else '0')
        dataframe[u'kitchen_space'] = dataframe[u'kitchen_space'].convert_objects(convert_numeric = True)

        dataframe[u'built_time'] = dataframe[u'built_time'].map(lambda x: x.rstrip(' г.п.') if type(x) == str else x)
        dataframe[u'built_time'] = dataframe[u'built_time'].convert_objects(convert_numeric = True)
        
        dataframe[u'age'] = 2017 - dataframe[u'built_time']
        
        dataframe = self.modify_house_type(dataframe)
        dataframe = self.get_log_space(dataframe)
        dataframe = self.get_price_for_sqr_meter(dataframe)
        dataframe = self.get_distance(dataframe)
        
        # Fake, krisha.kz deleted this posts
        dataframe = dataframe.query('all_space >= 10')
        dataframe = dataframe.query('all_space >= 25 or price <= 20000000')

        return dataframe
    
    def modify_house_type(self, dataframe):
        dataframe = dataframe.copy()
        
        instance = dataframe[u'house_type'][dataframe.index[0]]
        if type(instance) != object and type(instance) != str and type(object) != unicode:
            dataframe[u'house_type'].fillna(2, inplace = True)
            return dataframe
        
        new_house_type = []
        for house_type in dataframe[u'house_type']:
            if house_type == 'кирпичный':
                new_house_type += [3]
            elif house_type == 'монолитный':
                new_house_type += [4]
            elif house_type == 'панельный':
                new_house_type += [1]
            elif house_type == 'каркасно-камышитовый':
                new_house_type += [0]
            else:
                new_house_type += [2]
            
            
        dataframe[u'house_type'] = new_house_type
        return dataframe
    
    def get_log_space(self, dataframe):
        dataframe = dataframe.copy()
        dataframe[u'log_space'] = np.log(dataframe[u'all_space']) / np.log(1.4)
        return dataframe

    def get_price_for_sqr_meter(self, dataframe):
        dataframe = dataframe.copy()
        dataframe[u'price_for_sqr_meter'] = dataframe.apply(self.calculate_price_for_sqr_meter, axis = 1)
        return dataframe

    def calculate_price_for_sqr_meter(self, x):
        return (x[u'price'] + 0.0) / x[u'all_space']
    
    def get_distance(self, dataframe):
        dataframe['distance'] = (dataframe['geocode_lat'] ** 2 + dataframe['geocode_long'] ** 2) ** 0.5
        return dataframe
    
    def learning_data(self, dataframe, part):
        dataframe = dataframe.copy()
        
        if part >= 1:
            return dataframe
        
        geocode_lat  = dataframe[u'geocode_lat']
        geocode_long = dataframe[u'geocode_long']
        
        mid_lat  = geocode_lat.sum() / len(dataframe)
        mid_long = geocode_long.sum() / len(dataframe)
        
        max_radius = 0
        for i in dataframe.index:
            dist_lat  = mid_lat - geocode_lat[i]
            dist_long = mid_long - geocode_long[i]
            max_radius = max(max_radius, (dist_lat ** 2 + dist_long ** 2) ** 0.5)
        
        percent = part ** 0.5
        inside = []
        while percent <= 1:
            inside = []
            for i in dataframe.index:
                dist_lat  = mid_lat - geocode_lat[i]
                dist_long = mid_long - geocode_long[i]
                dist = (dist_lat ** 2 + dist_long ** 2) ** 0.5
                
                if dist <= max_radius * percent:
                    inside += [i]
            if len(inside) >= len(dataframe) * part or percent == 1:
                break
            percent = min(percent + part, 1.0)
        
        random.shuffle(inside)
        chosen = []
        for i in range(0, len(inside)):
            chosen += [inside[i]]
            if i + 1 >= len(dataframe) * part:
                break
                
        return dataframe.ix[chosen]