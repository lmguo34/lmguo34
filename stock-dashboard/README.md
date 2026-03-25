# 股票行情看板

简单的A股行情查看网站，纯本地运行，不需要后端用Python+FastAPI，前端用ECharts展示K线。

## 功能

- 搜索股票（名称或代码
- 查看实时行情（最新价、涨跌幅、涨跌额、成交量
- 日K/周K/月K线图
- 支持缩放查看历史

## 启动方式

```bash
chmod +x start.sh
./start.sh
```

服务启动后，打开 `frontend/index.html` 就能用了，访问：http://localhost:8000 是API，直接打开html文件就能访问前端。

## 依赖

- Python包已经安装好了：
- akshare - 免费获取股票数据
- fastapi + uvicorn - 后端服务

## 说明

数据来自akshare，免费使用，仅供个人看行情使用，不提供交易功能。
