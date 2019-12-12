import dataloader
import transformer
import numpy as np
import matplotlib.pyplot as plt

corrcoefs = []
keys = []
# corrcoefs_map ={}
desc_map,price_map = dataloader.load_train()
price_map['price'] = transformer.normlize(price_map['price'])
for key in desc_map.keys():
    desc_map[key] = transformer.normlize(desc_map[key])
    corrcoefs.append(np.corrcoef(desc_map[key],price_map['price'])[0][1])
    keys.append(key)
    # corrcoefs_map[key]

zipped = zip(keys,corrcoefs)
sort_zipped = sorted(zipped,key=lambda x:(x[1],x[0]),reverse=True)
result = zip(*sort_zipped)
keys, corrcoefs = [list(x) for x in result]
plt.title('correlation')
plt.bar(keys,corrcoefs)
plt.xticks(rotation=90)
plt.show()