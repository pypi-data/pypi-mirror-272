def preprocess_data(df_data):
    df_data = df_data[(df_data['30天累产油'] != 0) | (df_data['60天累产油'] != 0)]
    df_data = df_data[df_data['设计装填系数lbs/ft'] != 0]

    # Rename columns
    rename_dict = {
        '设计装填系数lbs/ft': '设计充填系数',
        '最大压裂液泵注速率 bpm': '最大排量',
        '最大支撑剂浓度(lb/gal)': '最大砂比',
        '支撑剂质量(lb)': '最大砂量',
        '真实垂直深度的有效射孔区域内，每英尺的单位重量lbs/ft TVD Net Perfs': '净射孔垂深充填系数',
        '支撑剂(lb/ft)': '实际充填系数',
        '最大处理压力(psi).1': '最大油压',
        '最大环空压力(psi).1': '最大套压',
        '设计填充度(%)': '设计前置液百分比',
        '底部射孔到顶部射孔测深差(m)': '射孔测深',
        '底部射孔到顶部射孔垂深差(m)': '射孔垂深',
        '清洗垫液体积(bbl)': '设计净液量',
        '1号压裂液体体积（bbl）对HRWP的0.5磅/加仑': '1号压裂液体积',
        '2号压裂液体体积 (bbl)/1-4 ppg': '2号压裂液体积',
        '3号压裂液体体积 (bbl)': '3号压裂液体积',
        '4号压裂液体体积 (gal)/4-6 ppg': '4号压裂液体积',
        '5号压裂液体体积 (gal)': '5号压裂液体积',
        '6号压裂液体体积 (gal)/4-8 ppg': '6号压裂液体积',
        '7号压裂液体体积 (gal)/6-8 ppg': '7号压裂液体积',
        '8号压裂液体体积 (gal)': '8号压裂液体积',
        '9号压裂液体体积 (gal)/8-10 ppg': '9号压裂液体积',
        '10号压裂液体体积 (gal)': '10号压裂液体积',
        '冲洗浆液体积 (gal)': 'Flush进液量体积',
        '垫液体积 (gal)': '砂浆量'
    }
    df_data.rename(columns=rename_dict, inplace=True)
    #———————————选择特征——————————————

    feature_label = ['设计充填系数','最大排量','最大砂比','最大砂量','砂浆量','射孔簇数','设计净液量',
                    '射孔测深','射孔垂深',
                    '最大油压','最大套压',
    #                  '净射孔垂深充填系数',
                    '垂厚m','地层电阻率Ω.m','孔隙度%','平均渗透率mD','含烃饱和度%','泥质含量%']

    #—————————————————————————
    target_label     = ['30天累产油']
    target_label_60  = ['60天累产油']
    # 30天累产油, 30天平均累产油, 60天累产油, 60天平均累产油, 90天累产油, 90天平均累产油, 180天累产油, 180天平均累产油, 360天累产油, 360天平均累产油
    #—————————————————————————

    new_data_30_all   = df_data[feature_label+['30天累产油']]
    new_data_30_mean  = df_data[feature_label+['30天平均累产油']]

    new_data_60_all   = df_data[feature_label+['60天累产油']]
    new_data_60_mean  = df_data[feature_label+['60天平均累产油']]

    new_data_90_all   = df_data[feature_label+['90天累产油']]
    new_data_90_mean  = df_data[feature_label+['90天平均累产油']]

    new_data_180_all  = df_data[feature_label+['180天累产油']]
    new_data_180_mean = df_data[feature_label+['180天平均累产油']]

    new_data_360_all  = df_data[feature_label+['360天累产油']]
    new_data_360_mean = df_data[feature_label+['360天平均累产油']]

    #———————————选择数据——————————————
    df_data   = df_data[feature_label+ target_label]


    for col in df_data.columns:
        null_count = df_data[col].isnull().sum()
        print(f"列 {col} 中的空值数量为：{null_count}")

    # ————————————0-空值填充————————————————
    df_data.fillna(0, inplace=True)

    def encode_columns(df_data, *columns):
        '''
        获取指定列不同的类别，创建编码字典，将指定列进行替代为编码值
        该函数会替代原始数据
        '''
        for column_name in columns:
            unique_labels = df_data[column_name].unique()
            label_encoding = {label: index for index, label in enumerate(unique_labels)}
            df_data[column_name] = df_data[column_name].replace(label_encoding)
            
            
    # ————————查看非数值类型列————————
    non_numeric_features = df_data.select_dtypes(exclude=['number']).columns.tolist()

    # print(non_numeric_features)

    # 例如处理"某列"的编码
    # encode_columns(df_data, '区块')

    # ——————————std-异常值删除——————————
    def remove_outliers(df):
        skipped_cols = []
        for column in df.columns:
            try:
                std = df[column].std()
                df = df[(df[column] >= df[column].mean() - 3*std) & (df[column] <= df[column].mean() + 3*std)]
            except:
                skipped_cols.append(column)
        return df, skipped_cols

    # 使用示例：
    outliers_data = df_data
    df_std, skipped_columns = remove_outliers(outliers_data)

    df_data = df_std

    return df_data