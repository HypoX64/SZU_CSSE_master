from sklearn.linear_model import ElasticNet, Lasso,  BayesianRidge, LassoLarsIC
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
# import xgboost as xgb
# import lightgbm as lgb

import numpy as np
import torch
import dataloader
import evaluation
import time
import transformer

dimension = 85
train_desc,train_price,test_desc = dataloader.load_all(dimension)


kr = GridSearchCV(KernelRidge(kernel='polynomial'),
                  param_grid={"alpha": np.logspace(-3, 2, 6),
                              "gamma": np.logspace(-2, 2, 5)})

# print(np.logspace(-2, 2, 5))
kr.fit(train_desc, train_price)
y_kr = kr.predict(test_desc)
for i in range(len(y_kr)):
    y_kr[i] = dataloader.convert2price(y_kr[i])
# print(y_kr.shape)
print(dimension,evaluation.eval_test(y_kr))
dataloader.write_csv(y_kr, './result/result.csv')