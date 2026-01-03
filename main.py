from src.config import set_ieee_style
from src.data_loader import fetch_gdelt
from src.analysis import print_stats_table
import src.visualization as viz

def main():
    set_ieee_style()
    print("🚀 Starting GDELT Analysis (IEEE Black & White Edition)...")
    
    # 【总数据收集器】用于最后打印所有表格
    all_data_for_table = {} 

    # ==========================================
    # 1. 核心情感对比
    # ==========================================
    print("\n[Phase 1] Core Sentiment Comparison")
    df_us = fetch_gdelt('"China" sourcecountry:US', 'timelinetone', 'US_Tone')
    df_uk = fetch_gdelt('"China" sourcecountry:UK', 'timelinetone', 'UK_Tone')
    df_ng = fetch_gdelt('"China" sourcecountry:NG', 'timelinetone', 'NG_Tone')
    
    # 收集数据
    all_data_for_table['US Sentiment'] = df_us
    all_data_for_table['UK Sentiment'] = df_uk
    all_data_for_table['NG Sentiment'] = df_ng
    
    viz.plot_comparison(
        {'US Media': df_us, 'UK Media': df_uk, 'Nigeria Media': df_ng},
        "Fig 1. Comparative Sentiment: Global North vs. South",
        "fig1_sentiment_bw.png", "Average Tone"
    )

    # ==========================================
    # 2. 关注度
    # ==========================================
    print("\n[Phase 2] Attention Volume")
    df_us_vol = fetch_gdelt('"China" sourcecountry:US', 'timelinevol', 'US_Vol')
    df_uk_vol = fetch_gdelt('"China" sourcecountry:UK', 'timelinevol', 'UK_Vol')
    
    all_data_for_table['US Volume'] = df_us_vol
    all_data_for_table['UK Volume'] = df_uk_vol
    
    viz.plot_comparison(
        {'US Volume': df_us_vol, 'UK Volume': df_uk_vol},
        "Fig 2. Media Attention Volume Intensity",
        "fig2_volume_bw.png", "Volume Intensity (%)"
    )

    # ==========================================
    # 3. 全球分布 (箱线图 & 矩阵)
    # ==========================================
    print("\n[Phase 3] Global Distribution")
    # 补充下载其他国家
    df_jp = fetch_gdelt('"China" sourcecountry:JA', 'timelinetone', 'Japan_Tone')
    df_in = fetch_gdelt('"China" sourcecountry:IN', 'timelinetone', 'India_Tone')
    df_ru = fetch_gdelt('"China" sourcecountry:RS', 'timelinetone', 'Russia_Tone')
    
    all_data_for_table['Japan Sentiment'] = df_jp
    all_data_for_table['India Sentiment'] = df_in
    all_data_for_table['Russia Sentiment'] = df_ru
    
    country_dict = {
        'US': df_us, 'UK': df_uk, 'Nigeria': df_ng,
        'Japan': df_jp, 'India': df_in, 'Russia': df_ru
    }
    
    viz.plot_heatmap(country_dict)
    viz.plot_boxplot(country_dict)

    # ==========================================
    # 4. 回归分析
    # ==========================================
    print("\n[Phase 4] Regression")
    viz.plot_scatter_regression(df_us_vol, df_us)

    # ==========================================
    # 5. 主题雷达
    # ==========================================
    print("\n[Phase 5] Thematic Analysis")
    themes = ['Trade', 'Military', 'Culture', 'Tech']
    val_us_list = []
    val_ng_list = []
    
    for t in themes:
        # 下载数据
        d_u = fetch_gdelt(f'"China" "{t}" sourcecountry:US', 'timelinetone', f'US_{t}')
        d_n = fetch_gdelt(f'"China" "{t}" sourcecountry:NG', 'timelinetone', f'NG_{t}')
        
        # 存入大表格，方便查阅每个主题的具体得分
        all_data_for_table[f'Theme: US {t}'] = d_u
        all_data_for_table[f'Theme: NG {t}'] = d_n
        
        # 计算均值用于画图
        val_us_list.append(d_u['Value'].mean() if not d_u.empty else 0)
        val_ng_list.append(d_n['Value'].mean() if not d_n.empty else 0)
        
    viz.plot_radar(val_us_list, val_ng_list, themes)

    # ==========================================
    # 6. 最终输出所有表格数据
    # ==========================================
    print("\n" + "#"*70)
    print("FINAL DATA TABLES (Copy this to your paper!)")
    print("#"*70)
    print_stats_table(all_data_for_table)
    print("\n✅ Project Finished.")

if __name__ == "__main__":
    main()