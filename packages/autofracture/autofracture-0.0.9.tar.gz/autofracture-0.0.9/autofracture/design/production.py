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



# 模型评估指标
def mzc_metrics(y_train_true, y_train_pre, y_test_true, y_test_pre):
    """
    计算模型评估指标。

    参数：
    y_train_true：array-like，训练集真实值。
    y_train_pre：array-like，训练集预测值。
    y_test_true：array-like，测试集真实值。
    y_test_pre：array-like，测试集预测值。

    返回值：
    result1：str，训练集评估结果。
    result2：str，测试集评估结果。
    """
    # 模型评估指标
    r2_train = r2_score(y_train_true, y_train_pre)
    r2_train = round(r2_train, 16)
    r2_test = r2_score(y_test_true, y_test_pre)
    r2_test = round(r2_test, 16)
    mse_train = mean_squared_error(y_train_true, y_train_pre)
    mse_train = round(mse_train, 16)
    mse_test = mean_squared_error(y_test_true, y_test_pre)
    mse_test = round(mse_test, 16)
    rmse_train = sqrt(mse_train)
    rmse_test = sqrt(mse_test)
    mape_train = mean_absolute_percentage_error(y_train_true, y_train_pre)
    mape_test = mean_absolute_percentage_error(y_test_true, y_test_pre)
    mae_train = mean_absolute_error(y_train_true, y_train_pre)
    mae_test = mean_absolute_error(y_test_true, y_test_pre)
    explained_variance_train = explained_variance_score(y_train_true, y_train_pre)
    explained_variance_test = explained_variance_score(y_test_true, y_test_pre)
    max_error_train = max_error(y_train_true, y_train_pre)
    max_error_test = max_error(y_test_true, y_test_pre)

    # 评估结果
    result1 = '''
    Train R² = {:.16f}
    Train MSE = {:.16f}
    Train RMSE = {:.16f}
    Train MAE = {:.16f}
    Train MAPE = {:.16f}
    Train Explained Variance = {:.16f}
    Train Max Error = {:.16f}
    '''.format(r2_train, mse_train, rmse_train, mae_train, mape_train, explained_variance_train, max_error_train)
    print('训练集评价指标：', result1)
    result2 = '''
    Test R² = {:.16f}
    Test MSE = {:.16f}
    Test RMSE = {:.16f}
    Test MAE = {:.16f}
    Test MAPE = {:.16f}
    Test Explained Variance = {:.16f}
    Test Max Error = {:.16f}
    '''.format(r2_test, mse_test, rmse_test, mae_test, mape_test, explained_variance_test, max_error_test)
    print('测试集评价指标：', result2)
    return result1, result2


def model_train(df_train, label, time_limit, k_folds):
    """
    使用给定的训练数据和参数训练模型。

    参数：
        df_train (pandas.DataFrame)：训练数据。
        label (str)：目标标签列名。
        time_limit (int)：训练模型的最大时间限制。
        k_folds (int)：交叉验证的折数。

    返回：
        tuple：包含训练好的模型、训练数据的预测值、测试数据的预测值和评估指标的元组。
    """
    # RMSE 模型评价指标
    metric = 'root_mean_squared_error'
    # 预测模型 案例01
    predictor_01 = TabularPredictor(label=target_label, problem_type="regression", eval_metric=metric).fit(
        train_data=df_train, time_limit=time_limit, num_bag_folds=k_folds, verbosity=1, presets='best_quality')
    # Model 01
    Evaluate_01_Train = predictor_01.evaluate(df_train)
    print(f'{label}训练集指标:', Evaluate_01_Train)
    Evaluate_01_Test = predictor_01.evaluate(df_test)
    print(f'{label}测试集指标:', Evaluate_01_Test)
    # 01
    predictor_01_Ytrain = predictor_01.predict(X_train)  # 预测数据
    predictor_01_Ytest = predictor_01.predict(X_test)
    auto_predictor_metrics1 = mzc_metrics(Y_train, predictor_01_Ytrain, Y_test, predictor_01_Ytest)
    return predictor_01, predictor_01_Ytrain, predictor_01_Ytest, auto_predictor_metrics1
