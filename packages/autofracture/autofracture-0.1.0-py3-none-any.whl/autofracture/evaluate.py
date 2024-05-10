import numpy as np
import pandas as pd
from scipy import stats
import time
import math
from math import sqrt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, mean_absolute_percentage_error,max_error,explained_variance_score

# 模型评估指标
def metrics(y_train_true, y_train_pre, y_test_true, y_test_pre):
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
    Train R² = {:.4f}
    Train MSE = {:.4f}
    Train RMSE = {:.4f}
    Train MAE = {:.4f}
    Train MAPE = {:.4f}
    Train Explained Variance = {:.4f}
    Train Max Error = {:.4f}
    '''.format(r2_train, mse_train, rmse_train, mae_train, mape_train, explained_variance_train, max_error_train)
    print('训练集评价指标：', result1)
    result2 = '''
    Test R² = {:.4f}
    Test MSE = {:.4f}
    Test RMSE = {:.4f}
    Test MAE = {:.4f}
    Test MAPE = {:.4f}
    Test Explained Variance = {:.4f}
    Test Max Error = {:.4f}
    '''.format(r2_test, mse_test, rmse_test, mae_test, mape_test, explained_variance_test, max_error_test)
    print('测试集评价指标：', result2)
    return result1, result2

# 模型评估指标
def metrics_test(y_test_true, y_test_pre):
    """
    计算测试集模型评估指标。
    参数：
    y_test_true：array-like，测试集真实值。
    y_test_pre：array-like，测试集预测值。
    返回值：
    result：str，测试集评估结果。
    """
    # 模型评估指标
    r2_test = r2_score(y_test_true, y_test_pre)
    r2_test = round(r2_test, 16)
    mse_test = mean_squared_error(y_test_true, y_test_pre)
    mse_test = round(mse_test, 16)
    rmse_test = sqrt(mse_test)
    mape_test = mean_absolute_percentage_error(y_test_true, y_test_pre)
    mae_test = mean_absolute_error(y_test_true, y_test_pre)
    explained_variance_test = explained_variance_score(y_test_true, y_test_pre)
    max_error_test = max_error(y_test_true, y_test_pre)
    result = '''
    Test R² = {:.4f}
    Test MSE = {:.4f}
    Test RMSE = {:.4f}
    Test MAE = {:.4f}
    Test MAPE = {:.4f}
    Test Explained Variance = {:.4f}
    Test Max Error = {:.4f}
    '''.format(r2_test, mse_test, rmse_test, mae_test, mape_test, explained_variance_test, max_error_test)
    print('测试集评价指标：', result)
    return result
