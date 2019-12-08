import dataloader
import transformer
import numpy as np

correlates = []
desc_map,price_map = dataloader.load_train()
price_map['price'] = transformer.normlize(price_map['price'])
key = ''
desc_map[key] = transformer.normlize(desc_map[key])
print(np.correlate(desc_map[key],price_map['price']))
# for key in desc_map.keys():
#     desc_map[key] = transformer.normlize(desc_map[key])
#     correlates.append(np.correlate(desc_map[key],price_map['price'])[0][1])
# print(correlates)
