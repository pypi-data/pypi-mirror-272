from bayes_opt import BayesianOptimization

def objective_function(设计充填系数, 最大排量, 最大砂比, 最大砂量, 砂浆量, 射孔簇数, 射孔测深, 射孔垂深, 净射孔垂深充填系数, 设计净液量):
    # 合并固定值和可调参数
    features = {**geo_input, '设计充填系数': 设计充填系数, '最大排量': 最大排量, '最大砂比': 最大砂比, '最大砂量': 最大砂量,
                '砂浆量': 砂浆量, '射孔簇数': 射孔簇数, '射孔测深': 射孔测深, '射孔垂深': 射孔垂深,
                '净射孔垂深充填系数': 净射孔垂深充填系数, '设计净液量': 设计净液量}
    # 使用固定值和可调参数进行预测
#     predictions = model.predict([list(features.values())])
    
    # ————————————AutoGluon——————————————
    # 转换为TabularDataset或pandas.DataFrame
    data = TabularDataset(pd.DataFrame([list(features.values())], columns=list(features.keys())))
    predictions = predictor_best.predict(data)
    # ————————————AutoGluon——————————————
    
    
    # 保存迭代结果到DataFrame
    global opt_results
    opt_results = opt_results._append({'设计充填系数': 设计充填系数, '最大排量': 最大排量, '最大砂比': 最大砂比, '最大砂量': 最大砂量,
                                    '砂浆量': 砂浆量, '射孔簇数': 射孔簇数, '射孔测深': 射孔测深, '射孔垂深': 射孔垂深,
                                    '净射孔垂深充填系数': 净射孔垂深充填系数, '设计净液量': 设计净液量, '预测产量值': predictions[0]}, ignore_index=True)
    
    return predictions[0]