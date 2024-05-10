import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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

# 灰色关联分析封装函数
def normalize_data(data, method='mean'):
    '''数据无量纲化处理'''
    if method == 'mean':
        return data / data.mean(axis=0)
    elif method == 'first':
        return data / data.iloc[0, :]
    elif method == 'max':
        return data / data.max()
    elif method == 'min':
        return data / data.min()
def gray(input_df, method='mean', target=None, rho=0.5):
    '''
    进行灰色关联分析，计算权重。
    
    参数：
    input_df (pd.DataFrame): 输入的数据框dataframe格式
    method (str): 数据无量纲化方法，默认为'mean'
    target (int): 母序列所在的序号位置，默认为 None，索引是从0开始的，None表示最后一列
    rho (float): 对应系数，默认为0.5
    
    返回：
    pd.DataFrame: 包含权重的数据框
    #### 调用示例：result = gray(input_df, target=1)，输入数据input_df，target此时表示第二列
    '''
    try:
        # 1. 进行无量纲化
        df_normalized = normalize_data(input_df, method)

        # 2. 获取 x 和 y
        if target is None:
            target = len(df_normalized.columns) - 1
        
        x = df_normalized.drop(input_df.columns[target], axis=1)
        y = df_normalized.iloc[:, target]

        # 3. 求解系数
        abs_xik = abs(x.sub(y, axis=0))
        a, b = abs_xik.min().min(), abs_xik.max().max()
        coef = (a + rho * b) / (abs_xik + rho * b)
        coef_m = coef.mean()

        # 4. 返回结果并排序
        result = pd.DataFrame({'Weight': coef_m}).sort_values('Weight', ascending=False)
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()  # 返回一个空的数据框表示出错
    


# 局部放大
def plot_local(Y_train, Y_test, Y_pre_test, xlim_local, ylim_local):
    '''
    绘制局部放大图像。
    y_train_true：array-like，训练集真实值。
    y_train_pre：array-like，训练集预测值。
    y_test_true：array-like，测试集真实值。
    y_test_pre：array-like，测试集预测值。
    xlim_local：tuple，x轴的范围。
    ylim_local：tuple，y轴的范围。
    '''
    fig = plt.figure(figsize=(12, 4))

    # 创建第一个子图，显示整体图像
    ax1 = plt.subplot2grid((1, 3), (0, 0), colspan=2)
    ax1.tick_params(axis='x', direction='in')
    ax1.tick_params(axis='y', direction='in')
    ax1.plot(range(len(Y_train), len(Y_train) + len(Y_test)), Y_test, 'k--', alpha=0.5, label='Actual')
    ax1.plot(range(len(Y_train), len(Y_train) + len(Y_pre_test)), Y_pre_test, color='blue', ls='-', alpha=0.5, label='Predicted')
    ax1.legend()
    ax1.set_xlabel('Data Sample Index')
    ax1.set_ylabel('ROP, m/h')
    # ax1.set_xlim(19809,22011)
    # ax1.set_ylim(-5, 35)
    ax1.legend(loc=2)

    # 创建第二个子图，显示局部放大图像
    ax2 = plt.subplot2grid((1, 3), (0, 2))
    ax2.tick_params(axis='x', direction='in')
    ax2.tick_params(axis='y', direction='in')
    ax2.plot(range(len(Y_train), len(Y_train) + len(Y_test)), Y_test, 'k--', alpha=0.5, marker='o',label='Actual')
    ax2.plot(range(len(Y_train), len(Y_train) + len(Y_pre_test)), Y_pre_test, color='blue', ls='-', marker='o',alpha=0.5, label='Predicted')
    ax2.legend()
    ax2.set_xlabel('Data Sample Index')
    ax2.set_ylabel('ROP, m/h')
    ax2.legend(loc=2)
    ax2.set_xlim(xlim_local)
    ax2.set_ylim(ylim_local)
    # ax2.set_ylim(16, 20)

    # 添加垂直直线
    # ax1.axvline(x=21750, color='red', linestyle='--')
    # ax1.axvline(x=21800, color='red', linestyle='--')

    plt.tight_layout()
    # plt.savefig("./figure/局部放大预测图蓝色.svg",dpi=600,bbox_inches='tight')
    plt.show()