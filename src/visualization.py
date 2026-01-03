import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from math import pi
import os
from src.config import FIG_DIR

def save_fig(filename):
    path = os.path.join(FIG_DIR, filename)
    # 核心修改：使用 tight_layout 和高 DPI 保存
    plt.savefig(path, dpi=300, bbox_inches='tight')
    print(f"[+] Figure saved: {path}")

# ==========================================
# Fig 1 & 2: 折线图 (极简学术风)
# ==========================================
def plot_comparison(dfs, title, filename, ylabel):
    # 调整画布比例，更宽一点，适合时间序列
    plt.figure(figsize=(10, 5))
    
    # 【核心修改】：移除 Marker，依靠线型区分
    # Solid (实线) = 最重要的数据 (US)
    # Dashed (虚线) = 对比数据 (UK)
    # Dotted (点线) = 特殊数据 (NG)
    styles = [
        {'ls': '-', 'lw': 2.0, 'color': 'black', 'label_suffix': ''},        # 实线，加粗
        {'ls': '--', 'lw': 1.5, 'color': '#444444', 'label_suffix': ''},    # 虚线，深灰
        {'ls': ':', 'lw': 1.8, 'color': '#222222', 'label_suffix': ''}      # 点线
    ]
    
    for i, (label, df) in enumerate(dfs.items()):
        if df.empty: continue
        
        # 使用 30 天移动平均
        smooth = df['Value'].rolling(window=30, min_periods=1).mean()
        
        style = styles[i % len(styles)]
        
        plt.plot(smooth.index, smooth, 
                 label=label, 
                 linestyle=style['ls'], 
                 linewidth=style['lw'],
                 color=style['color'])

    # 0轴线：更淡一点
    plt.axhline(0, color='black', linestyle='-', linewidth=0.5, alpha=0.4)
    
    # 样式美化
    plt.title(title, pad=15, fontweight='bold') # 标题加粗
    plt.ylabel(ylabel, fontweight='bold')
    plt.xlabel("Year", fontweight='bold')
    
    # 图例：放在最合适的位置，去掉边框，更现代
    plt.legend(frameon=False, loc='best')
    
    # 网格：非常淡，只保留横向网格
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    # 【核心修改】：去掉上方和右侧的边框 (Spines) -> 看起来极爽
    sns.despine()
    
    plt.tight_layout()
    save_fig(filename)

# ==========================================
# Fig 3: 热力图 (高对比度数值矩阵)
# ==========================================
def plot_heatmap(data_dict):
    combined = pd.DataFrame()
    for country, df in data_dict.items():
        if not df.empty:
            combined[country] = df['Value'].resample('Y').mean()
    
    if combined.empty: return

    plt.figure(figsize=(8, 5)) #稍微紧凑一点
    
    data_to_plot = combined.T
    data_to_plot.columns = [str(x.year) for x in data_to_plot.columns]
    
    # 使用 'Greys' 并且设置 vmin/vmax 增加对比度
    # cbar=False 如果不需要色条，或者保留
    ax = sns.heatmap(data_to_plot, 
                cmap='Greys', 
                annot=True, 
                fmt=".2f",
                annot_kws={"size": 10, "weight": "bold"}, # 数字加粗
                linewidths=1, 
                linecolor='black',
                vmin=-1.5, vmax=1.5, # 锁定范围，防止颜色太淡
                cbar_kws={'label': 'Avg Tone'})
    
    plt.title("Fig 3. Yearly Average Sentiment Matrix", pad=15, fontweight='bold')
    plt.xlabel("") # 年份本来就很清楚，不需要 Label
    plt.ylabel("")
    plt.tight_layout()
    save_fig("fig3_heatmap_bw.png")

# ==========================================
# Fig 4: 箱线图 (极简风 - 去掉散点)
# ==========================================
def plot_boxplot(data_dict):
    plot_data = []
    for country, df in data_dict.items():
        if not df.empty:
            temp = df.copy()
            temp['Country'] = country
            plot_data.append(temp)
    
    if not plot_data: return
    full_df = pd.concat(plot_data)
    
    plt.figure(figsize=(8, 6))
    order = full_df.groupby('Country')['Value'].median().sort_values().index
    
    # 【核心修改】：完全去掉散点(stripplot)，只保留干净的箱子
    # whis=1.5 是标准 IQR
    sns.boxplot(x='Country', y='Value', data=full_df, order=order,
                color='white',            # 箱子内部白色
                linecolor='black',        # 线条黑色
                linewidth=1.5,            # 线条加粗
                width=0.5,                # 箱子变瘦，更精致
                showfliers=False)         # 不显示异常值点，保持画面干净
    
    # 如果一定要显示分布，可以用这种极其微小的点
    # sns.stripplot(..., size=1, alpha=0.1) -> 但通常不需要

    plt.axhline(0, color='black', linestyle=':', linewidth=1)
    
    plt.title("Fig 4. Sentiment Variance by Region", pad=15, fontweight='bold')
    plt.ylabel("Sentiment Score", fontweight='bold')
    plt.xlabel("")
    
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    sns.despine() # 去边框
    
    plt.tight_layout()
    save_fig("fig4_boxplot_bw.png")

# ==========================================
# Fig 5: 回归散点图 (空心圆点)
# ==========================================
def plot_scatter_regression(vol_df, tone_df):
    if vol_df.empty or tone_df.empty: return
    
    v = vol_df['Value'].resample('M').mean()
    t = tone_df['Value'].resample('M').mean()
    df = pd.DataFrame({'Volume': v, 'Tone': t}).dropna()
    
    plt.figure(figsize=(6, 6)) # 正方形构图
    
    # 散点：纯黑圈，无填充，变小一点
    plt.scatter(df['Volume'], df['Tone'], 
                facecolors='none', edgecolors='black', alpha=0.6, s=40)
    
    # 拟合线
    sns.regplot(x='Volume', y='Tone', data=df, scatter=False, 
                line_kws={'color':'black', 'linestyle':'-', 'linewidth':2})
    
    corr = df.corr().iloc[0,1]
    # 使用图例框风格显示相关系数
    plt.text(0.95, 0.95, f"R = {corr:.2f}", 
             transform=plt.gca().transAxes, 
             fontsize=12, fontweight='bold',
             verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=1))
    
    plt.title("Fig 5. Attention vs. Sentiment", pad=15, fontweight='bold')
    plt.xlabel("Attention Volume", fontweight='bold')
    plt.ylabel("Sentiment Tone", fontweight='bold')
    
    sns.despine()
    plt.tight_layout()
    save_fig("fig5_scatter_bw.png")

# ==========================================
# Fig 6: 雷达图 (线条加粗)
# ==========================================
def plot_radar(val_us, val_ng, themes):
    N = len(themes)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    val_us += val_us[:1]
    val_ng += val_ng[:1]
    
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    
    # US: 实线
    ax.plot(angles, val_us, linewidth=2.5, linestyle='-', color='black', label='US Media')
    
    # NG: 虚线
    ax.plot(angles, val_ng, linewidth=2.5, linestyle='--', color='#444444', label='Nigeria Media')
    
    # 坐标轴设置
    plt.xticks(angles[:-1], themes, color='black', size=12, fontweight='bold')
    ax.set_rlabel_position(45)
    plt.yticks([-1, 0, 1], ["-1.0", "0.0", "1.0"], color="gray", size=8)
    plt.ylim(-2.0, 1.5)
    
    # 网格线变成虚线
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.title("Fig 6. Thematic Divergence", y=1.08, fontweight='bold')
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), frameon=False)
    
    save_fig("fig6_radar_bw.png")