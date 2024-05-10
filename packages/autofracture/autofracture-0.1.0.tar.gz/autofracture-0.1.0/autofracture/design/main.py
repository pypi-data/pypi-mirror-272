import os
import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import math
from math import sqrt
import shap
import time
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager
from matplotlib.patches import Rectangle
from matplotlib.font_manager import FontProperties
from matplotlib_inline.backend_inline import set_matplotlib_formats
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from tqdm import tqdm, trange
from minepy import MINE
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from scipy.stats import rankdata, pointbiserialr
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, explained_variance_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error, max_error
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from autogluon.tabular import TabularDataset, TabularPredictor
import warnings
warnings.filterwarnings('ignore')
# plt.rcParams['font.sans-serif'] =['Times New Roman'] 
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = ['STFangsong']
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
pd.set_option('display.max_columns', False)
pd.set_option('display.max_rows', False)


# ————————————————————产量预测模块————————————————————————————
from production import mzc_metrics
from production import model_train
# 导入数据
df_data = pd.read_excel('./01-参数团法-工程-地质-一体化数据库.xlsx')
# 选择目标列
target_label = '30天累产油'
# 划分数据集
label = target_label
df_train,df_test=train_test_split(df_data, test_size=0.2, random_state=42,shuffle =True, stratify =None)
X_train = df_train.drop(target_label, axis=1)
X_test  = df_test.drop(target_label, axis=1)
Y_train = df_train[[target_label]]
Y_test  = df_test[[target_label]]
# 调用预测函数
label = target_label
time_limit = 7200
k_folds    = 10
predictor_best, predictor_best_Ytrain, predictor_best_Ytest, Result_predictor_best = model_train(df_train, label, 7200, 10)


# ——————————————————————————参数优化模块————————————————————————————
from opt import objective_function
# 输入固定值地质参数
geo_input = {
    '垂厚m': 2.1,
    '地层电阻率Ω.m': 5.6,
    '孔隙度%': 22.9,
    '平均渗透率mD': 565.0,
    '含烃饱和度%': 50.0,
    '泥质含量%': 17.4}

# 创建空的DataFrame用于保存迭代结果
opt_results = pd.DataFrame(columns=['设计充填系数', '最大排量', '最大砂比', '最大砂量', '砂浆量', '射孔簇数', '射孔测深', '射孔垂深', '净射孔垂深充填系数', '设计净液量', '预测产量值'])

# 设置工程参数限制
enginnering_pbounds = {'设计充填系数': (0, 1400), 
           '最大排量': (11.9, 20), 
           '最大砂比': (4, 9.3), 
           '最大砂量': (11002, 101170),
           '砂浆量': (0, 10500), 
           '射孔簇数': (1, 17), 
           '射孔测深': (3.5, 132.9), 
           '射孔垂深': (3, 102.1),
           '净射孔垂深充填系数': (270.0, 1561), 
           '设计净液量': (33, 250)}

# 优化模型调用
optimizer = BayesianOptimization(f=objective_function, pbounds=enginnering_pbounds, random_state=1)
optimizer.maximize(init_points=5, n_iter=100)

# 输出优化目标产量与施工参数值
print(optimizer.max)