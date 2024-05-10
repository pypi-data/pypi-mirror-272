import pandas as pd
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
