import os
import matplotlib.pyplot as plt
import seaborn as sns

# 定义数据和图片保存路径
DATA_DIR = "data/raw"
FIG_DIR = "figures"

# 确保目录存在
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

def set_ieee_style():
    """配置符合 IEEE 期刊标准的绘图风格"""
    sns.set_style("whitegrid")
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman"],
        "font.size": 12,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "figure.dpi": 300,
        "axes.unicode_minus": False, # 解决负号显示问题
        "savefig.bbox": "tight",
        "lines.linewidth": 1.5
    })