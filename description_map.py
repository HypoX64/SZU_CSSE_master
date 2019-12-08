import numpy as np

import pandas as pd

value_map = {}
value_map["MSSubClass"] = {'180':1, 
                            '30':2, '45':2, 
                            '190':3, '50':3, '90':3, 
                            '85':4, '40':4, '160':4, 
                            '70':5, '20':5, '75':5, '80':5, '150':5,
                            '120': 6, '60':6}

value_map["MSZoning"] = {'A':1,'C':4, 'FV':1, 'I':3,'RH':3, 'RL':2, 'RP':3, 'RM':2}

value_map["Neighborhood"] = {'MeadowV':1,
                               'IDOTRR':2, 'BrDale':2,
                               'OldTown':3, 'Edwards':3, 'BrkSide':3,
                               'Sawyer':4, 'Blueste':4, 'SWISU':4, 'Names':4,
                               'NPkVill':5, 'Mitchel':5,
                               'SawyerW':6, 'Gilbert':6, 'NWAmes':6,
                               'Blmngtn':7, 'CollgCr':7, 'ClearCr':7, 'Crawfor':7,
                               'Veenker':8, 'Somerst':8, 'Timber':8,
                               'StoneBr':9,
                               'NoRidge':10, 'NridgHt':10}

value_map["Condition1"] = {'Artery':1,
                           'Feedr':2, 'RRAe':2,
                           'Norm':3, 'RRAn':3,
                           'PosN':4, 'RRNe':4,
                           'PosA':5 ,'RRNn':5}

value_map["BldgType"] = {'2FmCon':1, 'Duplx':1, 'TwnhsI':1, '1Fam':2, 'TwnhsE':2}

value_map["HouseStyle"] = {'1.5Unf':1, 
                           '1.5Fin':2, '2.5Unf':2, 'SFoyer':2, 
                           '1Story':3, 'SLvl':3,
                           '2Story':4, '2.5Fin':4}

value_map["Exterior1st"] = {'BrkCmn':1,
                             'AsphShn':2, 'CBlock':2, 'AsbShng':2,
                             'WdShing':3, 'Wd Sdng':3, 'MetalSd':3, 'Stucco':3, 'HdBoard':3,'Other':3,
                             'BrkFace':4, 'Plywood':4, 'PreCast':4,
                             'VinylSd':5,
                             'CemntBd':6,
                             'Stone':7, 'ImStucc':7}

value_map["MasVnrType"] = {'BrkCmn':1, 'None':1, 'CBlock':1,'BrkFace':2, 'Stone':3}

value_map["ExterQual"] = {'Po':1,'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}

value_map["Foundation"] = {'Slab':1, 
                           'BrkTil':2, 'CBlock':2, 'Stone':2,
                           'Wood':3, 'PConc':4}

value_map["BsmtQual"] = {'NA':1, 'Po':2,'Fa':3, 'TA':4, 'Gd':5, 'Ex':6}

value_map["BsmtExposure"] = {'NA':1, 'No':2, 'Av':3, 'Mn':3, 'Gd':4}

value_map["Heating"] = {'Floor':1, 'Grav':1, 'Wall':2, 'OthW':3, 'GasW':4, 'GasA':5}

value_map["HeatingQC"] = {'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}

value_map["KitchenQual"] = {'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}

value_map["Functional"] = {'Sal':1, 'Sev':2, 'Maj2':3, 'Maj1':3, 'Mod':4, 'Min2':5, 'Min1':5, 'Typ':6}

value_map["FireplaceQu"] = {'NA':1, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5}

value_map["GarageType"] = {'CarPort':1, 'NA':1,
                           'Detchd':2,
                           '2Types':3, 'Basment':3,
                           'Attchd':4, 'BuiltIn':5}

value_map["GarageFinish"] = {'NA':1, 'Unf':2, 'RFn':3, 'Fin':4}

value_map["PavedDrive"] = {'N':1, 'P':2, 'Y':3}

value_map["SaleType"] = {'COD':1, 'ConLD':1, 'ConLI':1, 'ConLw':1, 'Oth':1, 'WD':1,
                        'CWD':2, 'VWD':2, 'Con':3, 'New':3}

value_map["SaleCondition"] = {'AdjLand':1, 'Abnorml':2, 'Alloca':2, 'Family':2, 'Normal':3, 'Partial':4} 


def fix_key(key):
    #csv is wrong here
    if key == 'Wd Shng':
        key='WdShing'
    if key == '2fmCon':
        key='2FmCon'
    if key == 'NAmes':
        key='Names'
    if key == 'Duplex':
        key='Duplx'
    if key == 'CmentBd':
        key='CemntBd'
    if key == 'C (all)':
        key='C'
    if key == 'Twnhs':
        key='TwnhsI'
    if key == 'Brk Cmn' or key =='BrkComm':
        key='BrkCmn'
    else:
        key = key
    return key

miss_0 = ["PoolQC" , "MiscFeature", "Alley", "Fence", "FireplaceQu", "GarageQual", "GarageCond", "GarageFinish", "GarageYrBlt", "GarageType", "BsmtExposure", "BsmtCond", "BsmtQual", "BsmtFinType2", "BsmtFinType1", "MasVnrType"]
miss_1=["MasVnrArea", "BsmtUnfSF", "TotalBsmtSF", "GarageCars", "BsmtFinSF2", "BsmtFinSF1", "GarageArea"]
miss_2 = ['LotFrontage']
def fix_miss(name):
    if name in miss_0:
        return 1
    else:
        return 0

def fix_LotFrontage(Full_map):
    data_df = pd.DataFrame(Full_map)
    data_df["LotFrontage"] = data_df.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median()))
    return data_df["LotFrontage"].to_numpy()

def binary(npdata):
    for i in range(len(npdata)):
        if npdata[i]>0:
            npdata[i] = 1
        else:
            npdata[i] = 0
    return npdata

def add_future(features):
    features["TotalHouse"] = features["TotalBsmtSF"] + features["1stFlrSF"] + features["2ndFlrSF"]   
    features["TotalArea"] = features["TotalBsmtSF"] + features["1stFlrSF"] + features["2ndFlrSF"] + features["GarageArea"]
    
    features["TotalHouse_OverallQual"] = features["TotalHouse"] * features["OverallQual"]
    features["GrLivArea_OverallQual"] = features["GrLivArea"] * features["OverallQual"]
    features["my_MSZoning_TotalHouse"] = features["my_MSZoning"] * features["TotalHouse"]
    features["my_MSZoning_OverallQual"] = features["my_MSZoning"] + features["OverallQual"]
    features["my_MSZoning_YearBuilt"] = features["my_MSZoning"] + features["YearBuilt"]
    features["my_Neighborhood_TotalHouse"] = features["my_Neighborhood"] * features["TotalHouse"]
    features["my_Neighborhood_OverallQual"] = features["my_Neighborhood"] + features["OverallQual"]
    features["my_Neighborhood_YearBuilt"] = features["my_Neighborhood"] + features["YearBuilt"]
    features["BsmtFinSF1_OverallQual"] = features["BsmtFinSF1"] * features["OverallQual"]
    
    features["my_Functional_TotalHouse"] = features["my_Functional"] * features["TotalHouse"]
    features["my_Functional_OverallQual"] = features["my_Functional"] + features["OverallQual"]
    features["LotArea_OverallQual"] = features["LotArea"] * features["OverallQual"]
    features["TotalHouse_LotArea"] = features["TotalHouse"] + features["LotArea"]
    features["my_Condition1_TotalHouse"] = features["my_Condition1"] * features["TotalHouse"]
    features["my_Condition1_OverallQual"] = features["my_Condition1"] + features["OverallQual"]
    
   
    features["Bsmt"] = features["BsmtFinSF1"] + features["BsmtFinSF2"] + features["BsmtUnfSF"]
    features["Rooms"] = features["FullBath"]+features["TotRmsAbvGrd"]
    features["PorchArea"] = features["OpenPorchSF"]+features["EnclosedPorch"]+features["3SsnPorch"]+features["ScreenPorch"]
    features["TotalPlace"] = features["TotalBsmtSF"] + features["1stFlrSF"] + features["2ndFlrSF"] + features["GarageArea"] + features["OpenPorchSF"]+features["EnclosedPorch"]+features["3SsnPorch"]+features["ScreenPorch"]
    features['all_quality'] = (features['ExterQual'] +features['BsmtFinType1']+features['BsmtFinType2']+
                            features['KitchenQual']+features['FireplaceQu']+features['GarageQual']+
                            features['PoolQC']+features['Fence'])

    features['YrBltAndRemod']=features['YearBuilt']+features['YearRemodAdd']
    features['TotalSF']=features['TotalBsmtSF'] + features['1stFlrSF'] + features['2ndFlrSF']
    features['Total_sqr_footage'] = (features['BsmtFinSF1'] + features['BsmtFinSF2'] +
                                     features['1stFlrSF'] + features['2ndFlrSF'])
    features['Total_Bathrooms'] = (features['FullBath'] + (0.5 * features['HalfBath']) +
                                   features['BsmtFullBath'] + (0.5 * features['BsmtHalfBath']))

    features['Total_porch_sf'] = (features['OpenPorchSF'] + features['3SsnPorch'] +
                                  features['EnclosedPorch'] + features['ScreenPorch'] +
                                  features['WoodDeckSF'])


    #random features
    random_list = ['GrLivArea','OverallQual','2ndFlrSF','YearBuilt','1stFlrSF','TotalBsmtSF','OverallCond',
    'my_Neighborhood','my_SaleCondition','BsmtFinSF1','my_MSZoning','LotArea','GarageCars','YearRemodAdd','GarageArea']
    length = len(random_list)
    for i in range(length):
        for j in range(i,length):
            if i != j:
                features[random_list[i]+'*'+random_list[j]]=features[random_list[i]]*features[random_list[j]]
                
    return features