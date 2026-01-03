import pandas as pd

def print_stats_table(df_dict):
    """
    打印描述性统计表格 (Mean, Std, Min, Max)
    """
    print("\n" + "="*65)
    print("【论文实证数据】Descriptive Statistics (2017-2024)")
    print("="*65)
    print(f"{'Metric/Country':<20} | {'Mean':<8} | {'Std Dev':<8} | {'Min':<8} | {'Max':<8}")
    print("-" * 65)
    
    for name, df in df_dict.items():
        if df.empty: 
            continue
        # 计算统计量
        desc = df['Value'].describe()
        print(f"{name:<20} | {desc['mean']:<8.4f} | {desc['std']:<8.4f} | {desc['min']:<8.4f} | {desc['max']:<8.4f}")
    
    print("="*65 + "\n")