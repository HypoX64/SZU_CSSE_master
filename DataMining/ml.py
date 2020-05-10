from sklearn.linear_model import ElasticNet, Lasso,  BayesianRidge, LassoLarsIC,LassoCV
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
import xgboost as xgb
import lightgbm as lgb

import numpy as np
import dataloader
import evaluation
import time
import transformer
import time
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt


def eval(model,train_x,train_y,test_x):
    model.fit(train_x, train_y)
    y_pre = model.predict(test_x)
    for i in range(len(y_pre)):
        y_pre[i] = transformer.convert2price(y_pre[i])
    return evaluation.eval_test(y_pre),y_pre
    # print(dimension,evaluation.eval_test(y_pre))

# KernelRidge()
krr = GridSearchCV(KernelRidge(kernel='polynomial'),cv = 3,
                  param_grid={"alpha": np.logspace(-1, 2, 10),
                              "gamma": np.logspace(-1, 2, 10)})


las = LassoCV(alphas=np.logspace(-5, 2, 50),eps=np.logspace(-5, 2, 20),max_iter=10000)


model_xgb = xgb.XGBRegressor(colsample_bytree=0.4603, gamma=0.0468, 
                             learning_rate=0.05, max_depth=3, 
                             min_child_weight=1.7817, n_estimators=2200,
                             reg_alpha=0.4640, reg_lambda=0.8571,
                             subsample=0.5213, silent=1,
                             random_state =7, nthread = -1)


# ElasticNet
ENet = GridSearchCV(ElasticNet(max_iter = 10000),
                  param_grid={"alpha": np.logspace(-3, 2, 6),
                              "l1_ratio": np.logspace(-2, 2, 5)})

#BayesianRidge
bay = BayesianRidge()

#GradientBoostingRegressor
GBoost = GradientBoostingRegressor(n_estimators=3000, learning_rate=0.01,
                                   max_depth=4, max_features='sqrt',
                                   min_samples_leaf=15, min_samples_split=10, 
                                   loss='huber', random_state =5)

#LGBMRegressor
model_lgb = lgb.LGBMRegressor(objective='regression',num_leaves=5,
                              learning_rate=0.05, n_estimators=720,
                              max_bin = 55, bagging_fraction = 0.8,
                              bagging_freq = 5, feature_fraction = 0.2319,
                              feature_fraction_seed=9, bagging_seed=9,
                              min_data_in_leaf =6, min_sum_hessian_in_leaf = 11)

#SVR
model_svr = GridSearchCV(SVR(kernel="rbf"),
                  param_grid={"C": np.logspace(0, 2, 5),
                              "gamma": np.logspace(-4, -3, 8),
                              "epsilon":np.logspace(-4, -3, 5)})


models = [krr,las,model_xgb,ENet,bay,GBoost,model_lgb,model_svr]
model_names = ['krr','las','model_xgb','ENet','bay','GBoost','model_lgb','model_svr']
for model,model_name in zip(models,model_names):
    print(model_name)
    losss = []
    start_dimension = 60
    end_dimension = 150
    for dimension in range(start_dimension,end_dimension):
        t1 = time.time()
        train_desc,train_price,test_desc = dataloader.load_all(dimension)
        loss,_ = eval(model,train_desc,train_price,test_desc)
        losss.append(loss)

        t2 = time.time()
        print(dimension,loss,' cost time:','%.3f'%(t2-t1),'s')
        t1 = time.time()

    best_dimension = losss.index(min(losss))+start_dimension
    print('Best:',min(losss),' dimension:',best_dimension)

    train_desc,train_price,test_desc = dataloader.load_all(best_dimension)
    loss,pre = eval(model,train_desc,train_price,test_desc)
    dataloader.write_csv(pre, './result/best_'+'%.6f'%loss+'_'+model_name+'.csv')

    plt.plot(np.linspace(start_dimension,dimension,dimension-start_dimension+1),losss)
    plt.xlabel('PCA dimension')
    plt.ylabel('loss')
    plt.title(model_name+' :loss_PCA')
    plt.savefig('./images/'+'%.6f'%loss+'_'+str(best_dimension)+'_'+model_name+".png")
    plt.cla()
    # plt.show()

