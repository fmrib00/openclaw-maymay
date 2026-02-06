---
name: a-share-daily-report
description: Generates daily A-share stock market report (A股今日简报) with 9:16 mobile ratio using ZhipuAI Web Search API
---

# A股今日简报 (A-Share Daily Market Report)

生成中国A股每日市场简报，包含11个完整部分，使用9:16竖屏手机格式。

## When to Use This Skill

用户说以下任一内容时触发：
- "today's A share market"
- "A股今日简报"
- "今日股市"
- "生成A股日报"
- "股市简报"

## What This Skill Does

1. 自动填充今天的日期
2. 使用ZhipuAI Web Search API获取市场数据
3. 解析搜索结果提取结构化数据
4. 生成包含11个部分的完整报告
5. 创建9:16手机优化PNG报告
6. 显示结果

## Prerequisites

```bash
pip install zhipuai python-dotenv Pillow
```

确保 `.env` 文件存在于 `~/stock/`：
```
ZHIPUAI_API_KEY=your_api_key_here
```

## Instructions

### Quick Start

运行生成脚本：

```bash
cd /home/yongyue/.openclaw/workspace/skills/a-share-daily-report
python3 generate_report.py
```

### How It Works

1. **Load API Key**: 从 `~/stock/.env` 读取智谱AI API密钥
2. **Fetch Market Data**: 使用ZhipuAI Web Search API执行6次搜索
   - 指数行情
   - 板块涨跌
   - 资金流向
   - 热门概念
   - 财经新闻
   - 市场宽度
3. **AI Parsing**: 使用AI解析搜索结果为结构化JSON数据
4. **Generate Image**: 使用PIL创建1080x1920的PNG图片
5. **Save Files**:
   - 数据: `~/stock/parsed_market_data_YYYYMMDD.json`
   - 图片: `~/stock/A股手机简报_YYYYMMDD.png`

### Report Layout

**Size**: 1080 x 1920 (9:16竖屏)

**Colors**:
- 背景: (8, 12, 25)
- 卡片: (22, 32, 50)
- 强调色: (65, 125, 175)
- 上涨: (60, 175, 110)
- 下跌: (195, 65, 65)
- 警告: (220, 160, 50)

**11 Sections**:
1. 日期标题 + 市场标签
2. 主要指数（4个）
3. 市场宽度 + 涨跌比条
4. 资金流向（3个卡片）
5. 板块TOP3（涨跌各3个）
6. 资金TOP3（流入流出各3个）
7. 热门新闻（3条）
8. 热门概念（8个）
9. 投资建议（3个卡片）
10. 技术指标（6个）
11. 近期事件（3个）

### Configuration Files

Create `~/stock/.env`:
```
ZHIPUAI_API_KEY=your_api_key_here
```

## Report Contains 11 Sections

1. **顶部标题** - 日期 + 星期 + "A股投资日报" + 市场标签
2. **主要指数** - 4个指数卡片 (上证/深证/创业/科创)
3. **市场宽度** - 上涨/下跌/涨停/跌停 + 涨跌比条
4. **资金流向** - 北向/主力/成交 (3个卡片)
5. **板块TOP3** - 领涨/领跌各3个
6. **资金TOP3** - 净流入/净流出各3个
7. **热门新闻** - 3条财经新闻
8. **热门概念** - 8个概念板块
9. **投资建议** - 市场判断/操作策略/关注方向 (3个卡片)
10. **技术指标** - MACD/KDJ/RSI/BOLL/成交量/PE (6个)
11. **近期事件** - 3个重要事件

## Critical Requirements

1. **ALWAYS** use ZhipuAI Web Search API for market data
2. **NEVER** skip any of the 11 sections
3. Use 1080x1920 resolution (9:16)
4. Load data from JSON file
5. Use consistent formatting with previous reports

## Output Files

- Data: `~/stock/parsed_market_data_YYYYMMDD.json`
- Script: `~/stock/mobile_daily_report_YYYYMMDD.py`
- Report: `~/stock/A股手机简报_YYYYMMDD.png`
