import os
# 全局取消所有代理 - 一定要最先执行！
for k in list(os.environ.keys()):
    if k.lower() in ['http_proxy', 'https_proxy', 'no_proxy', 'all_proxy']:
        os.environ.pop(k, None)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
import json

# 现在导入requests，没有代理环境变量了
import requests
requests.adapters.DEFAULT_RETRIES = 3

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 股票列表缓存文件
STOCK_LIST_FILE = os.path.join(os.path.dirname(__file__), 'stock_list.csv')

def get_stock_list():
    """获取股票列表，从缓存读取"""
    if os.path.exists(STOCK_LIST_FILE):
        df = pd.read_csv(STOCK_LIST_FILE)
        return df
    return pd.DataFrame(columns=['code', 'name'])

@app.get("/api/search")
def search_stock(keyword: str):
    """搜索股票"""
    try:
        stock_info = get_stock_list()
        if stock_info.empty:
            return {"code": 1, "msg": "获取股票列表失败，请稍后重试"}
        # 模糊匹配
        result = stock_info[
            stock_info["name"].str.contains(keyword, case=False, na=False) | 
            stock_info["code"].astype(str).str.contains(keyword)
        ]
        # 只返回前20个结果
        result = result.head(20)
        return {"code": 0, "data": result.to_dict("records")}
    except Exception as e:
        return {"code": 1, "msg": str(e)}

@app.get("/api/quote")
def get_quote(code: str):
    """获取实时行情，使用akshare"""
    try:
        code = str(code).zfill(6)
        # 判断是沪市还是深市
        if code.startswith('6') or code.startswith('5') or code.startswith('9'):
            symbol = f'sh{code}'
        else:
            symbol = f'sz{code}'
        
        import akshare as ak
        # 获取最新行情
        df = ak.stock_zh_a_spot()
        stock_row = df[df['代码'] == code]
        
        if stock_row.empty:
            return {"code": 1, "msg": "未找到股票数据"}
        
        row = stock_row.iloc[0]
        name = row['名称']
        price = float(row['最新价'])
        open_price = float(row['开盘'])
        prev_close = float(row['昨收'])
        high = float(row['最高'])
        low = float(row['最低'])
        change = float(row['涨跌额'])
        change_percent = float(row['涨跌幅'])
        volume = int(float(row['成交量']) / 100)  # 转成手
        
        result = {
            "名称": name,
            "最新价": round(price, 2),
            "开盘": round(open_price, 2),
            "最高": round(high, 2),
            "最低": round(low, 2),
            "涨跌额": round(change, 2),
            "涨跌幅": round(change_percent, 2),
            "成交量": volume
        }
        return {"code": 0, "data": result}
    except Exception as e:
        return {"code": 1, "msg": str(e)}

@app.get("/api/kline")
def get_kline(code: str, period: str = "daily"):
    """获取K线数据，使用akshare"""
    try:
        code = str(code).zfill(6)
        # 判断是沪市还是深市
        if code.startswith('6') or code.startswith('5') or code.startswith('9'):
            symbol = f'sh{code}'
        else:
            symbol = f'sz{code}'
        
        # 周期映射
        period_map = {
            "daily": "daily",
            "weekly": "weekly",
            "monthly": "monthly"
        }
        adjust = "qfq"  # 前复权
        
        import akshare as ak
        # 获取K线数据
        df = ak.stock_zh_a_hist(symbol=symbol, period=period_map.get(period, "daily"), 
                               start_date="19900101", end_date="20500101", adjust=adjust)
        
        if df.empty:
            return {"code": 1, "msg": "未获取到K线数据"}
        
        # 转换格式: [日期, 开盘, 最高, 最低, 收盘, 成交量]
        kline_data = []
        for _, row in df.iterrows():
            kline_data.append([
                str(row['日期']),
                float(row['开盘']),
                float(row['最高']),
                float(row['最低']),
                float(row['收盘']),
                float(row['成交量'])
            ])
        
        # 获取股票名称
        name = ak.stock_info_a_code_name()[ak.stock_info_a_code_name()['code'] == int(code)]['name'].values
        stock_name = name[0] if len(name) > 0 else code
        
        return {"code": 0, "data": kline_data, "name": f"{stock_name}({code})"}
    except Exception as e:
        return {"code": 1, "msg": str(e)}

# 挂载前端静态文件（放在最后，不影响API路由）
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
