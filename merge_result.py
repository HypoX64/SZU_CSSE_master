import dataloader
import numpy as np
import evaluation

krr_price = dataloader.load_submission('./result/regression_best/best_0.026778_krr.csv')
svr_price = dataloader.load_submission('./result/regression_best/best_0.028606_model_svr.csv')
linear_price = dataloader.load_submission('./result/dl_best/0.026172_Linear.csv')
residual_linear_price = dataloader.load_submission('./result/dl_best/0.029055_Residual_linear.csv')

final_price = (krr_price+linear_price)/2

loss = evaluation.eval_test(final_price)
print(loss)
dataloader.write_csv(final_price, './result/'+'%.6f'%loss+'_merge'+'.csv')

