import pandas as pd
import requests
import io
import os
from src.config import DATA_DIR

def fetch_gdelt(query, mode, label, start_date="20170101000000"):
    """
    通用 GDELT 数据抓取函数
    :param query: GDELT 查询语句
    :param mode: 'timelinetone' 或 'timelinevol'
    :param label: 保存文件的标签名 (无后缀)
    :return: 清洗后的 DataFrame (包含 'Value' 列)
    """
    csv_path = os.path.join(DATA_DIR, f"{label}.csv")
    
    # 1. 缓存检查：如果文件已存在，直接读取
    if os.path.exists(csv_path):
        print(f"[*] Loading from cache: {label}...")
        df = pd.read_csv(csv_path)
    else:
        # 2. 如果不存在，从 API 下载
        print(f"[*] Downloading API: {label} ...")
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": query,
            "mode": mode,
            "format": "csv",
            "STARTDATETIME": start_date,
            "ENDDATETIME": "20241231235959"
        }
        try:
            response = requests.get(url, params=params, timeout=45)
            response.raise_for_status()
            with open(csv_path, "wb") as f:
                f.write(response.content)
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        except Exception as e:
            print(f"[-] Error fetching {label}: {e}")
            return pd.DataFrame()

    # 3. 数据清洗 (这是防止报错的关键)
    # 自动寻找数值列
    val_col = 'Value' if 'Value' in df.columns else df.columns[-1]
    
    # 强制转为数字，非数字变 NaN
    df[val_col] = pd.to_numeric(df[val_col], errors='coerce')
    df.dropna(subset=[val_col], inplace=True)
    
    # 处理时间索引
    if not df.empty:
        time_col = df.columns[0]
        df['Date'] = pd.to_datetime(df[time_col])
        df.set_index('Date', inplace=True)
        df.rename(columns={val_col: 'Value'}, inplace=True)
        return df[['Value']]
    else:
        return pd.DataFrame()