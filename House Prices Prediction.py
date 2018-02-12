#importing packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.model_selection import train_test_split
from scipy.stats import norm
get_ipython().magic('matplotlib inline')

import time
start_time = time.time()

#import train and test
train = pd.read_csv("/Users/Dario/Desktop/Kaggle/train.csv")
test = pd.read_csv("/Users/Dario/Desktop/Kaggle/test.csv")


#histogram Saleprice variable
'''sns.distplot(train["SalePrice"])
plt.title('Histogram SalePrice')
plt.show()'''


#Show outliers
'''plt.scatter(x="GrLivArea",y="SalePrice",data=train)
plt.title('GrLivArea vs SalePrice')
plt.xlabel('GrLivArea')
plt.ylabel('SalePrice')
plt.show()'''


# We remove outliers above plotted 
#house with area greater than 4000 and price smaller than $800K 
train = train.drop(train[(train['GrLivArea']>4000) & (train['SalePrice']<800000)].index)


# plot without outliers
'''plt.scatter(x="GrLivArea",y="SalePrice",data=train)
plt.title('GrLivArea vs SalePrice without outliers')
plt.xlabel('GrLivArea')
plt.ylabel('SalePrice')
plt.show()'''

#transform SalePrice column in the Train in a log-scale
train["SalePrice"] = np.log(train["SalePrice"])

#histogram of Saleprice in log-scale
'''sns.distplot(train["SalePrice"])
plt.title('Histogram SalePrice')
plt.show()'''

#here we dropped 'Id' columns for Train and Test
train.drop("Id", axis = 1, inplace= True)
test.drop("Id", axis = 1, inplace= True)

#now our Train has 1456 rows
'''train.shape'''

#assign to y_train (our dependent variable) variable only the logarithm of SalePrice column of the Train
y_train = train["SalePrice"]

# here we concatenate train and test
data = pd.concat([train,test])

#dropping Saleprice from concatenated dataset
data.drop("SalePrice", inplace = True, axis = 1)

#Heatmap to see correlation between variable
'''plt.figure(figsize = (30,6))
sns.heatmap(data.isnull(), cmap = "viridis", cbar = False)'''

#Fill Na's in Alley with 'NoAlley'
data["Alley"] = data["Alley"].fillna("NoAlley")

#Fill Na's in PoolQC with 'NoPool'
data["PoolQC"] = data["PoolQC"].fillna("NoPool")

#Fill Na's in MiscFeature with 'None'
data["MiscFeature"] = data["MiscFeature"].fillna("None")

#Fill Na's in Fence with 'NoFence'
data["Fence"] = data["Fence"].fillna("NoFence")

#Fill Na's in FireplaceQu with 'NoFireplace'
data["FireplaceQu"] = data["FireplaceQu"].fillna("NoFirePlace")

#Fill Na's in LotFrontage with the mean of values in LotFrontage column
data["LotFrontage"] = data["LotFrontage"].fillna(data["LotFrontage"].mean())

#Fill Na's in Garage variables with 'NoGarage'
data["GarageQual"] = data["GarageQual"].fillna("NoGarage")
data["GarageCond"] = data["GarageCond"].fillna("NoGarage")
data["GarageFinish"] = data["GarageFinish"].fillna("NoGarage")
data["GarageType"] = data["GarageType"].fillna("NoGarage")

#Fill Na's in Garage(YrBlt,Cars,Area) variables with 0
data["GarageYrBlt"] = data["GarageYrBlt"].fillna(0)
data["GarageCars"] = data["GarageCars"].fillna(0)
data["GarageArea"] = data["GarageArea"].fillna(0)

# Make a crosstab for utilities
'''table=pd.crosstab(index=data["Utilities"],columns="count")
table.columns=['freq']
table'''

# we dropped Utilities variable because all house have 'All public Utilities'
# except for one which has Electricity and Gas Only.
data.drop("Utilities",axis = 1, inplace = True)

#Fill Na's in Bsmt variables with 'NoBase'
data["BsmtCond"] = data["BsmtCond"].fillna("NoBase")
data["BsmtExposure"] = data["BsmtExposure"].fillna("NoBase")
data["BsmtQual"] = data["BsmtQual"].fillna("NoBase")
data["BsmtFinType2"] = data["BsmtFinType2"].fillna("NoBase")
data["BsmtFinType1"] = data["BsmtFinType1"].fillna("NoBase")
#Fill Na's in Bsmt(Bath,Fin and total) variables with 0
data["BsmtHalfBath"] = data["BsmtHalfBath"].fillna(0)
data["BsmtFullBath"] = data["BsmtFullBath"].fillna(0)
data["BsmtFinSF1"] = data["BsmtFinSF1"].fillna(0)
data["BsmtFinSF2"] = data["BsmtFinSF2"].fillna(0)
data["TotalBsmtSF"] = data["TotalBsmtSF"].fillna(0)
data["BsmtUnfSF"] = data["BsmtUnfSF"].fillna(0)

#Fill Na's in MasVnrType variables with 'None'
data["MasVnrType"] = data["MasVnrType"].fillna("None")

#Fill Na's in MasVnrArea variables with 0
data["MasVnrArea"] = data["MasVnrArea"].fillna(0)

#Fill Na's in MSZoning variables with 'RL'
data["MSZoning"] = data["MSZoning"].fillna("RL")

#Fill Na's in Exterior1st and Exterior2nd variables with 'VinylSd'
data["Exterior2nd"] = data["Exterior2nd"].fillna("VinylSd")
data["Exterior1st"] = data["Exterior1st"].fillna("VinylSd")

#Fill Na's in Electrical variables with 'SBrkr'
data["Electrical"] = data["Electrical"].fillna("SBrkr")

#Fill Na's in KitchenQual variables with 'TA'
data["KitchenQual"] = data["KitchenQual"].fillna("TA")

#Fill Na's in SaleType variables with 'WD'
data["SaleType"] = data["SaleType"].fillna("WD")

#Fill Na's in Functional variables with 'Typ'
data["Functional"] = data["Functional"].fillna("Typ")

#now we create dummies for categorical variables
data = pd.get_dummies(data)

#now we have 299 columns
'''data.shape'''

#after data tyding on the whole data, we split again in Train and Test
train = data[:1456]
test = data[1456:]

#Assigning to X entire train without SalePrice
#Assigning to y only the log of SalePrice
X = train
y = y_train


# # Gradient Boost
#importing Gradient Boosting package from scikit-learn
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.grid_search import GridSearchCV

#First we try with a simple model but we didn't achived a good score
'''GBoost = GradientBoostingRegressor(learning_rate = .05, n_estimators = 500)'''

# So we build up a cross validation model to set best parameters values for our GradientBoost model
#taking a look on the documentation
'''gradient_model = GradientBoostingRegressor()
test_params = {
 "learning_rate":[0.05,0.1,0.15],
 "n_estimators":[3000,4000,5000],
 "max_depth":[1,3,5],
    "alpha":[0.3,0.6,0.9,0.15]}
model = GridSearchCV(estimator = gradient_model,param_grid = test_params)
model.fit(X,y)
print(model.best_params_) '''

# We set on our model the parameters obtained by CV 
#(alpha=0.9,learning_rate = .05, n_estimators = 3000, max_depth = 1)
'''GBoost = GradientBoostingRegressor(learning_rate = .05, n_estimators = 3000, max_depth = 1)'''

#Best Result:
#Handling the parameters we discovered that increasing the number of estimators and
#choosing like loss function 'huber' which is a combination of least absolute deviation and 
#least squares regression we improved.
GBoost = GradientBoostingRegressor(loss = "huber",learning_rate = .05, 
                                  n_estimators = 5000, max_depth = 1)

#fit Model
GBoost.fit(X,y)

#predict on Test-set
pred1 = np.exp(GBoost.predict(test))

#Histogram of prediction
'''sns.distplot(pred1)
plt.title('Gradient Boosting prediction')
plt.show()'''

#Save in a csv file
result = pd.DataFrame(columns= ["Id","SalePrice"])
result["SalePrice"] = pred1
result["Id"] = range(1461,2920)
result.to_csv("/Users/Dario/Desktop/gradient.csv", index = False)

# # Ridge
from sklearn.linear_model import RidgeCV,Ridge
#Ridge cross validation to choose best alpha based on our data
'''ridge_cv = RidgeCV(alphas=np.logspace(start=-5,stop=5,num=150,endpoint=True))
ridge_cv.fit(X,y)
print('Best alpha is :',ridge_cv.alpha_) Best alpha=10.971561867
print('score:',ridge_cv.score(X,y))'''

#Set ridge with alpha got by cross validatio
ridge = Ridge(alpha = 10.971561867)

#fit model
ridge.fit(X,y)

#predict training model on Test
pred2 = np.exp(ridge.predict(test))

#histogram Ridge model prediction
'''sns.distplot(pred2)
plt.title('Ridge prediction')
plt.show()'''

#save in a csv file
result = pd.DataFrame(columns= ["Id","SalePrice"])
result["SalePrice"] = pred2
result["Id"] = range(1461,2920)
result.to_csv("/Users/Dario/Desktop/ridge.csv", index = False)

# # LGBoost
#importing package Lightgbm
import lightgbm as lgb
from sklearn.grid_search import GridSearchCV

#First we build up a cross validation model to set best parameters values for our Lightgbm model
#taking a look on the documentation --->http://testlightgbm.readthedocs.io/en/latest/Parameters.html
'''lgb_model = lgb.LGBMRegressor()
test_params = {
    "num_leaves":[2,3,4,5,6], #default 31: number of leaves in one tree
  'n_estimators':[1000,2000,3000,4000],
 "learning_rate":[0.01,0.03,0.05,0.08], #default 0.1
  'max_bin':[40,50,60,70],#Small bin may reduce training accuracy but may increase general power (deal with over-fit
}
model = GridSearchCV(estimator = lgb_model,param_grid = test_params)
model.fit(X,y)
print(model.best_params_)'''

#Fit model with parameters obtained in the cross validation
'''model2 = lgb.LGBMRegressor(objective='regression',num_leaves=4,
                              learning_rate=0.03, n_estimators=2000,max_bin = 70)'''

# best result obtained increasing number of estimators and 
#decreasing number of bin to deal the overfitting
model2 = lgb.LGBMRegressor(objective='regression',num_leaves=4,
                              learning_rate=0.03, n_estimators=30000,max_bin = 50)
model2.fit(X,y)

#predict the best model on Test
pred3 = np.exp(model2.predict(test))

#Histogram Lgb prediction
'''sns.distplot(pred3)
plt.title('Lgb prediction')
plt.show()
'''
#save in csv file
result = pd.DataFrame(columns= ["Id","SalePrice"])
result["SalePrice"] = pred3
result["Id"] = range(1461,2920)
result.to_csv("/Users/Dario/Desktop/lgb.csv", index = False)

# # Lasso
import warnings
warnings.filterwarnings("ignore")
from sklearn.linear_model import Lasso,LassoCV

# Cross validation for Lasso Model to find best alpha value
'''lasso = LassoCV(alphas=np.logspace(start=-5,stop=5,num=150,endpoint=True))
lasso.fit(X,y)
print('best alpha is:',lasso.alpha_)  Best alpha=0.000476269037803
print('score:',lasso.score(X,y))'''

#fit model with best alpha got by cross validation model
lasso_cross = Lasso(alpha = 0.000476269037803)
lasso_cross.fit(X,y)

#prediction on Test set
pred4 = np.exp(lasso_cross.predict(test))

#Histogram of Lasso prediction
'''sns.distplot(pred4)
plt.title('Lasso prediction')
plt.show()'''

#save in csv file
result = pd.DataFrame(columns= ["Id","SalePrice"])
result["SalePrice"] = pred4
result["Id"] = range(1461,2920)
result.to_csv("/Users/Dario/Desktop/Lasso.csv", index = False)

# # Final mean 
# score = 0.11627

#so here the final step.
#After saved all the prediction in a csv File we import them
gradient = pd.read_csv("/Users/Dario/Desktop/gradient.csv")
ridge = pd.read_csv("/Users/Dario/Desktop/ridge.csv")
lgb = pd.read_csv("/Users/Dario/Desktop/lgb.csv")
lasso=pd.read_csv("/Users/Dario/Desktop/lasso.csv")

#keeping only the SalePrice prediction, without Id
gradient = list(gradient.SalePrice)
ridge = list(ridge.SalePrice)
lgb = list(lgb.SalePrice)
lasso = list(lasso.SalePrice)

#Here we merged them computing the arithmetic mean.
final = list(zip(gradient,ridge,lgb,lasso))
final1 = []
for i,j,k,l in final:
    final1.append((i+j+k+l)/4)
#save in pred csv the final mean
result = pd.DataFrame(columns= ["Id","SalePrice"])
result["SalePrice"] = final1
result["Id"] = range(1461,2920)
result.to_csv("/Users/Dario/Desktop/pred.csv", index = False)



print("--- %s seconds ---" % (time.time() - start_time))  #  30.213807106018066 seconds 

