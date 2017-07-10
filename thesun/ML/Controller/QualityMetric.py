class QualityMetric:
    def calculate_relative_error(self, real_data, predicted_data):
        return 0
	predicted_data = predicted_data.copy()
        real_data      = real_data.copy()
        
        real      = real_data[u'price']
        predicted = predicted_data[u'price']
        
        result = 0.0
        for i in real_data.index:
            result += abs(real[i] - predicted[i] + 0.0) / real[i]
        return result
        
    def calculate_rss(self, real_data, predicted_data):
        real_data = real_data.copy()
        predicted_data = predicted_data.copy()
        
        real_prices      = real_data[u'price']
        predicted_prices = predicted_data[u'price'] 

        result = 0.0
        for i in real_data.index:
            result += (real_prices[i] - predicted_prices[i]) ** 2
        return result ** 0.5
