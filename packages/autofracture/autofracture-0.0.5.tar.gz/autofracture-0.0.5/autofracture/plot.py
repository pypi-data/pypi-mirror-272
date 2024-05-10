import seaborn as sns
import matplotlib.pyplot as plt
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