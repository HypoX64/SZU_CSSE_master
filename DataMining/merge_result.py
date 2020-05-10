import dataloader
import numpy as np
import evaluation

krr_price = dataloader.load_submission('./result/regression_best/best_0.026778_krr.csv')
svr_price = dataloader.load_submission('./result/regression_best/best_0.028606_model_svr.csv')
linear_price_noPCA = dataloader.load_submission('./result/dl_best/0.025929_Linear_NOPCA.csv')
linear_price_PCA = dataloader.load_submission('./result/dl_best/0.026172_Linear.csv')
residual_linear_price_noPCA = dataloader.load_submission('./result/dl_best/0.026439_Residual_linear_NOPCA.csv')

final_price = (svr_price+residual_linear_price_noPCA+linear_price_noPCA+linear_price_PCA)/4

loss = evaluation.eval_test(final_price)
print(loss)
dataloader.write_csv(final_price, './result/'+'%.6f'%loss+'_merge'+'.csv')

